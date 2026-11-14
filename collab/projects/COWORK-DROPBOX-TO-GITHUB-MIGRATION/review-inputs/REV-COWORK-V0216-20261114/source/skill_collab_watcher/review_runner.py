from __future__ import annotations

import json
import os
import re
import subprocess
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Protocol

from .models import ReviewResult


CLAUDE_CWD_NAME = "_review_cwd"
TRANSCRIPT_DIR_NAME = "transcripts"
MAX_TRANSCRIPT_BYTES = 30 * 1024 * 1024
CACHE_5M_ENV = "FORCE_PROMPT_CACHING_5M"
PREFLIGHT_TIMEOUT_SEC = 30


class ReviewRunner(Protocol):
    def run(
        self, snapshot_dir: Path, prompt_text: str, run_dir: Path,
        max_budget_usd: float | None = None, effort: str | None = None,
    ) -> ReviewResult:
        ...


def _parse_cli_output(stdout: str) -> dict:
    """The CLI's final answer as a dict. `--output-format json` prints one
    object; `--output-format stream-json` prints one event per line and the
    last `type == "result"` event carries the same fields."""
    try:
        parsed = json.loads(stdout)
        return parsed if isinstance(parsed, dict) else {}
    except (json.JSONDecodeError, TypeError):
        pass
    result: dict = {}
    for line in (stdout or "").splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(event, dict) and event.get("type") == "result":
            result = event
    return result


# Message templates read from the installed CLI (claude 2.1.218, strings of the executable; no limit was provoked):
#   `You've hit your ${label}${" · resets " + when}` with label in {session limit, weekly limit, Opus limit, Sonnet limit,
#   Fable 5 limit, usage credit limit}; `when` is "3pm" / "3:30pm" (within 24 h) or "Nov 18, 3pm" (later), local time,
#   usually followed by " (<time zone>)". Older builds print "Claude AI usage limit reached|<epoch>".
# Limits that never reset by themselves (organisation spend cap, admin-disabled usage) are NOT retryable: ordinary FAILED.
USAGE_LIMIT_RE = re.compile(
    r"you['\u2019]ve hit your [^\n\u00b7|]{0,40}?limit|usage limit reached|(?:session|weekly|5-hour|five-hour|opus|sonnet) limit"
    r"|out of (?:extra )?usage", re.IGNORECASE)
NON_RETRYABLE_RE = re.compile(
    r"spend limit|contact your admin|ask your admin|disabled by your admin|usage allocation has been disabled"
    r"|usage limit is set to \$0|seat type doesn't include|org_level_disabled|org_spend_cap", re.IGNORECASE)
_EPOCH_RE = re.compile(r"\|\s*(\d{10})\b")
_RESET_RE = re.compile(
    r"resets?\s+(?:at\s+)?(?:(?P<mon>[A-Za-z]{3})[a-z]*\.?\s+(?P<day>\d{1,2}),?\s+(?:(?P<year>\d{4}),?\s+)?)?"
    r"(?P<h>\d{1,2})(?::(?P<m>\d{2}))?\s*(?P<ap>am|pm)", re.IGNORECASE)
_MONTHS = {m: i for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}
BEFORE_START_MAX_ELAPSED_SEC = 120.0   # a refusal arrives within seconds; a process that ran longer had started working


def _reset_wait_seconds(blob: str, now: float) -> int | None:
    m = _EPOCH_RE.search(blob)
    if m:
        return max(0, int(m.group(1)) - int(now))
    c = _RESET_RE.search(blob)
    if not c:
        return None
    hour, minute, ap = int(c.group("h")), int(c.group("m") or 0), c.group("ap").lower()
    if not (1 <= hour <= 12 and 0 <= minute < 60):
        return None
    hour = (hour % 12) + (12 if ap == "pm" else 0)
    local_now = datetime.fromtimestamp(now)
    try:
        if c.group("mon"):
            month = _MONTHS.get(c.group("mon").lower())
            if month is None:
                return None
            year = int(c.group("year") or local_now.year)
            target = datetime(year, month, int(c.group("day")), hour, minute)
            if target <= local_now and not c.group("year"):
                target = target.replace(year=year + 1)
        else:
            target = local_now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if target <= local_now:
                target += timedelta(days=1)
    except ValueError:
        return None
    return max(0, int((target - local_now).total_seconds()))


def detect_usage_limit(parsed: dict, stdout: str, stderr: str, now: float | None = None,
                       elapsed_sec: float | None = None) -> tuple[str | None, int | None]:
    """(kind, seconds until the window resets or None); kind is None for any other failure (including limits that never
    reset by themselves). BEFORE_START only when nothing was billed (no cost, no output tokens) and the process was
    short-lived; otherwise DURING, which is never retried automatically. `num_turns` is NOT used: a refused first request
    can still be reported as one turn."""
    blob = "\n".join([str(parsed.get("result") or ""), str(parsed.get("error") or ""), stdout or "", stderr or ""])
    if not USAGE_LIMIT_RE.search(blob) or NON_RETRYABLE_RE.search(blob):
        return None, None
    now = time.time() if now is None else now
    wait = _reset_wait_seconds(blob, now)
    usage = parsed.get("usage") if isinstance(parsed.get("usage"), dict) else {}
    billed = bool(parsed.get("total_cost_usd")) or bool(usage.get("output_tokens")) or bool(usage.get("cache_creation_input_tokens"))
    slow = elapsed_sec is not None and elapsed_sec > BEFORE_START_MAX_ELAPSED_SEC
    return ("DURING" if (billed or slow) else "BEFORE_START"), wait


def _cli_usage(parsed: dict) -> dict | None:
    """Token usage plus the cost facts needed to size budgets later."""
    usage = dict(parsed.get("usage") or {})
    for key in ("total_cost_usd", "num_turns", "subtype"):
        if parsed.get(key) is not None:
            usage[key] = parsed[key]
    return usage or None


def build_argv(
    claude_exe: str,
    model: str | None,
    allowed_tools: list[str],
    snapshot_dir: Path,
    max_budget_usd: float | None,
    effort: str | None = None,
    stream: bool = False,
) -> list[str]:
    """Flags chosen from `claude --help` on the installed 2.1.218 build
    (checked 2026-11-01, no model call):

    - `-p --output-format json`: non-interactive, parseable result+usage.
      `stream: True` switches to `stream-json --verbose` (one event per turn,
      same final result event) so a per-turn transcript can be kept locally.
    - `--tools <csv>`: restricts the *available* tool set itself (unlike
      --allowedTools, which only skips the approval prompt for tools that
      are still available). Static review only needs read tools.
    - `--permission-mode dontAsk`: never prompts (no TTY) and denies anything
      outside the working directories. `bypassPermissions` (used up to 0.1.2)
      let the Read tool open ANY file the user can read, e.g. secrets.json in
      the parent of the run dir - measured with canary files on 2026-11-03.
      With dontAsk only cwd (an empty dir) and --add-dir (the snapshot) are
      readable.
    - `--setting-sources user`: excludes "project"/"local" settings, so a
      reviewed package's own .claude/settings.json never auto-loads. The user
      settings still apply (this PC: model sonnet, effortLevel xhigh), which is
      why `--effort` is passed explicitly when a run policy names one.
    - `--strict-mcp-config` with no `--mcp-config`: zero MCP servers load,
      so a package's own .mcp.json cannot expand the sandbox.
    - `--no-session-persistence`: no resumable session is written to disk.
    - `--add-dir <snapshot_dir>`: grants read access to the downloaded
      package without using it as cwd (cwd stays the trusted run_dir, so
      CLAUDE.md auto-discovery never walks into the package).
    - deliberately NOT `--bare`: this account authenticates via claude.ai
      OAuth/subscription (confirmed via `claude auth status`), and --bare
      only reads ANTHROPIC_API_KEY/apiKeyHelper, never OAuth/keychain.
    """
    argv = [
        claude_exe,
        "-p",
        "--output-format", "stream-json" if stream else "json",
    ]
    if stream:
        argv.append("--verbose")
    argv += [
        "--tools", ",".join(allowed_tools),
        "--permission-mode", "dontAsk",
        "--setting-sources", "user",
        "--strict-mcp-config",
        "--no-session-persistence",
        "--add-dir", str(snapshot_dir),
    ]
    if model:
        argv += ["--model", model]
    if effort:
        argv += ["--effort", effort]
    if max_budget_usd is not None:
        argv += ["--max-budget-usd", str(max_budget_usd)]
    return argv


class RealReviewRunner:
    """The only class in this project allowed to start a `claude` process.

    Every other module (orchestrator, validator, transports, cli scan/
    status/recover) must reach every decision - WAIT_INPUT, CONFLICT,
    REJECTED, DUPLICATE, AUTH_REQUIRED - without touching this class.
    tests/test_no_model_calls.py never imports or instantiates this class;
    it only uses FakeReviewRunner, and a separate static check greps the
    rest of the package for subprocess/Popen calls outside this file.
    """

    def __init__(
        self,
        claude_exe: str,
        model: str | None,
        allowed_tools: list[str],
        max_budget_usd: float | None,
        timeout_sec: int,
        prompt_cache_ttl: str = "1h",
        save_transcript: bool = False,
    ):
        self.claude_exe = claude_exe
        self.model = model
        self.allowed_tools = allowed_tools
        self.max_budget_usd = max_budget_usd
        self.timeout_sec = timeout_sec
        self.prompt_cache_ttl = prompt_cache_ttl
        self.save_transcript = save_transcript

    def _child_env(self) -> dict[str, str] | None:
        """Only the review process gets the cache-TTL switch; the user's own
        interactive Claude sessions and global settings are not touched."""
        if self.prompt_cache_ttl != "5m":
            return None
        env = dict(os.environ)
        env[CACHE_5M_ENV] = "1"
        return env

    def _keep_transcript(self, run_dir: Path, snapshot_dir: Path, stdout: str) -> None:
        """Best effort, local only (never uploaded). Failure to write must not
        change the review outcome."""
        try:
            data = stdout.encode("utf-8")
            if not data or len(data) > MAX_TRANSCRIPT_BYTES:
                return
            out = run_dir / TRANSCRIPT_DIR_NAME
            out.mkdir(parents=True, exist_ok=True)
            (out / f"{snapshot_dir.name}.jsonl").write_bytes(data)
        except OSError:
            pass

    def preflight(self) -> tuple[bool, str]:
        """Is the CLI logged in? `claude auth status` makes no model call. An
        unattended watcher checks this before claiming a job, so an expired login
        pauses the queue instead of turning the next request into a terminal
        FAILED. Only a reason code is returned: the account details in the CLI's
        answer are never kept."""
        try:
            proc = subprocess.run(
                [self.claude_exe, "auth", "status", "--json"],
                capture_output=True, encoding="utf-8", errors="replace",
                shell=False, timeout=PREFLIGHT_TIMEOUT_SEC,
            )
        except subprocess.TimeoutExpired:
            return False, "CLAUDE_CLI_TIMEOUT"
        except OSError:
            return False, "CLAUDE_CLI_NOT_FOUND"
        try:
            parsed = json.loads(proc.stdout)
        except (json.JSONDecodeError, TypeError):
            return False, "CLAUDE_STATUS_UNREADABLE"
        if proc.returncode == 0 and isinstance(parsed, dict) and parsed.get("loggedIn") is True:
            return True, "ok"
        return False, "CLAUDE_NOT_LOGGED_IN"

    def run(
        self, snapshot_dir: Path, prompt_text: str, run_dir: Path,
        max_budget_usd: float | None = None, effort: str | None = None,
    ) -> ReviewResult:
        budget = self.max_budget_usd if max_budget_usd is None else max_budget_usd
        argv = build_argv(self.claude_exe, self.model, self.allowed_tools, snapshot_dir, budget,
                          effort=effort, stream=self.save_transcript)
        # Empty working directory: it is the only place besides the snapshot
        # the reviewer may read, so it must not hold results or state.
        cwd = run_dir / CLAUDE_CWD_NAME
        cwd.mkdir(parents=True, exist_ok=True)
        started = time.monotonic()
        try:
            # encoding is explicit: text=True alone decodes with the Windows
            # ANSI code page (cp949 here), but the CLI speaks UTF-8.
            proc = subprocess.run(
                argv,
                input=prompt_text,
                capture_output=True,
                encoding="utf-8",
                errors="replace",
                cwd=str(cwd),
                env=self._child_env(),
                shell=False,
                timeout=self.timeout_sec,
            )
        except subprocess.TimeoutExpired:
            # Unknown whether the model was actually invoked before the
            # timeout - count it as a call and let the caller mark the job
            # REVIEW_UNCERTAIN rather than silently retrying.
            return ReviewResult(
                ok=False, output_text="", output_format="json", exit_code=-1,
                model_calls=1, usage=None, error=f"timeout after {self.timeout_sec}s",
            )

        if self.save_transcript:
            self._keep_transcript(run_dir, snapshot_dir, proc.stdout)
        parsed = _parse_cli_output(proc.stdout)
        usage = _cli_usage(parsed)
        cli_failed = parsed.get("is_error") is True or str(parsed.get("subtype", "")).startswith("error")
        if proc.returncode == 0 and not cli_failed:
            output_text = parsed.get("result") if parsed else proc.stdout
            return ReviewResult(
                ok=True, output_text=output_text if isinstance(output_text, str) else proc.stdout,
                output_format="json", exit_code=0, model_calls=1, usage=usage,
            )
        # Exit code 1 + subtype error_max_budget_usd was measured for a run that
        # exceeded --max-budget-usd (result null, cost recorded). Say why, so an
        # operator can tell a budget stop from any other failure.
        limit_kind, limit_wait = detect_usage_limit(parsed, proc.stdout, proc.stderr, elapsed_sec=time.monotonic() - started)
        if limit_kind:
            return ReviewResult(
                ok=False, output_text="", output_format="json", exit_code=proc.returncode, model_calls=0, usage=usage,
                error=f"usage_limit {limit_kind}", usage_limit=limit_kind, retry_after_sec=limit_wait,
            )
        reason = f"claude_cli_failed exit={proc.returncode}"
        if parsed.get("subtype"):
            reason += f" subtype={parsed['subtype']}"
        if parsed.get("total_cost_usd") is not None:
            reason += f" total_cost_usd={parsed['total_cost_usd']}"
        if budget is not None:
            reason += f" max_budget_usd={budget}"
        stderr_tail = proc.stderr[-1500:] if proc.stderr else ""
        return ReviewResult(
            ok=False,
            output_text=json.dumps(parsed, ensure_ascii=False) if parsed else (proc.stdout or "")[:20000],
            output_format="json",
            exit_code=proc.returncode, model_calls=1, usage=usage,
            error=(reason + (f" | stderr: {stderr_tail}" if stderr_tail else ""))[:4000],
        )
