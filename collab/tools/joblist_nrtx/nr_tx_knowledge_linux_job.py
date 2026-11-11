#!/usr/bin/env python3
"""NR L1 Tx research orchestration adapter: existing in-house skills only.

STAGED candidate, not activated by this package. Host-approved local configuration
must attest the exact source commit and execution authority; Job parameters cannot
supply commands, paths or credentials. No group knowledge publish.
"""
from __future__ import annotations
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import tempfile

JOB_ID = "JOB-20261112-NR-L1TX-KNOWLEDGE-MSC-01"
PROFILE = "nr-l1tx-knowledge-research-linux"
RESULT = "output/nr_tx_knowledge_research/latest_result.json"
CONFIG = "data/config/nr_tx_knowledge_research.json"
PROMPT = "references/NR_TX_KNOWLEDGE_RESEARCH_ORCHESTRATION_v0435.md"
SHA = re.compile(r"[0-9a-f]{40}\Z")
ATOM = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,95}\Z")

def _emit(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, prefix=".nrtx-", delete=False) as f:
        json.dump(payload, f, sort_keys=True, ensure_ascii=False, indent=2)
        f.write("\n")
        tmp = Path(f.name)
    os.replace(tmp, path)

def _require_regular(path: Path, code: str, *, limit: int = 32768) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise ValueError(code)
    s = path.stat(follow_symlinks=False)
    if not stat.S_ISREG(s.st_mode) or s.st_size < 1 or s.st_size > limit:
        raise ValueError(code)
    return path.read_bytes()

def _installed_skill(home: Path, name: str) -> Path:
    for parent in (home / "l1sw-private-skills", home / ".claude" / "skills"):
        path = parent / name
        if not path.is_symlink() and path.is_dir() and (path / "SKILL.md").is_file():
            _require_regular(path / "SKILL.md", "SKILL_POLICY_UNREADABLE", limit=1048576)
            return path
    raise ValueError("DEPENDENCY_NOT_VERIFIED_" + name.upper().replace("-", "_"))

def _git(root: Path, *args: str) -> str:
    p = subprocess.run(["git", "-C", str(root), *args], check=False,
                       stdin=subprocess.DEVNULL, capture_output=True, timeout=20)
    if p.returncode or len(p.stdout) > 32768:
        raise ValueError("GIT_IDENTITY_UNVERIFIED")
    return p.stdout.decode("utf-8").strip()

def preflight(root: Path, home: Path) -> dict:
    if sys.platform != "linux" or os.name != "posix" or os.geteuid() == 0:
        raise ValueError("LINUX_NONROOT_REQUIRED")
    if root.resolve() != home / "l1sw-private-skills" / "job-list":
        raise ValueError("JOB_ROOT_NOT_CANONICAL")
    if os.environ.get("JOB_LIST_JOB_ID") != JOB_ID or os.environ.get("JOB_LIST_PROFILE") != PROFILE:
        raise ValueError("JOB_RUNNER_ATTESTATION_MISSING")
    run_id = os.environ.get("JOB_LIST_RUN_ID", "")
    if not re.fullmatch(r"core_\d{8}_\d{6}_[0-9a-f]{8}", run_id):
        raise ValueError("JOB_RUN_ID_INVALID")

    local_config = root / CONFIG
    data = _require_regular(local_config, "HOST_APPROVAL_CONFIG_MISSING")
    st = local_config.stat()
    if st.st_uid != os.geteuid() or (st.st_mode & 0o077):
        raise ValueError("HOST_CONFIG_PERMISSIONS_INVALID")
    cfg = json.loads(data)
    if not isinstance(cfg, dict) or set(cfg) != {"schema_version", "status", "work_id", "source_revision", "allow_group_publish", "approval_id"}:
        raise ValueError("HOST_CONFIG_SCHEMA_INVALID")
    if cfg["schema_version"] != 1 or cfg["status"] != "APPROVED" or cfg["allow_group_publish"] is not False:
        raise ValueError("HOST_APPROVAL_MISSING_OR_TOO_BROAD")
    if not ATOM.fullmatch(str(cfg["work_id"])) or not ATOM.fullmatch(str(cfg["approval_id"])):
        raise ValueError("HOST_WORK_OR_APPROVAL_INVALID")
    if not SHA.fullmatch(str(cfg["source_revision"])):
        raise ValueError("SOURCE_REVISION_UNPINNED")

    # The actual source path is resolved strictly on the in-house host, never
    # carried in the PUBLIC package, remote Job request, or external report.
    code = home / "Project" / "smp1900"
    if code.is_symlink() or not code.is_dir() or code.resolve() != code:
        raise ValueError("APPROVED_SOURCE_ROOT_NOT_FOUND")
    if not (code / ".git").exists():
        raise ValueError("SOURCE_GIT_UNAVAILABLE")
    current = _git(code, "rev-parse", "--verify", "HEAD")
    if current != cfg["source_revision"]:
        raise ValueError("SOURCE_COMMIT_DRIFT")
    if _git(code, "status", "--porcelain", "--untracked-files=normal"):
        raise ValueError("SOURCE_DIRTY_REVIEW_REQUIRED")

    for skill in ("l1-knowledge-updater", "code-analyzer", "doc-converter"):
        _installed_skill(home, skill)
    exe = shutil.which("opencode") or shutil.which("opencode2")
    if not exe:
        raise ValueError("OPENCODE_CLI_UNAVAILABLE")
    if not Path(exe).is_file():
        raise ValueError("OPENCODE_BINARY_INVALID")
    prompt_bytes = _require_regular(root / PROMPT, "JOB_PROMPT_NOT_FOUND", limit=24000)
    return {"code": code, "config": cfg, "exe": exe, "prompt": prompt_bytes.decode("utf-8"), "run_id": run_id}

def run(root: Path | None = None) -> dict:
    skill_root = root or Path(__file__).resolve().parents[1]
    out = {"schema_version": 1, "job_id": JOB_ID, "profile": PROFILE,
           "status": "BLOCKED", "result_code": "NOT_RUN", "analysis": "NOT_RUN",
           "msc": "NOT_RUN", "knowledge_publication": "NOT_RUN",
           "source_write": False, "external_export": False,
           "started_at": dt.datetime.now(dt.timezone.utc).isoformat(),
           "completed_at": None, "reason_codes": []}
    try:
        home = Path.home().resolve()
        pre = preflight(skill_root, home)
        report_dir = skill_root / "output" / "nr_tx_knowledge_research" / pre["run_id"]
        report_dir.mkdir(parents=True, exist_ok=False)
        prompt = pre["prompt"] + "\n\nCURRENT SOURCE REVISION (locally verified): " + pre["config"]["source_revision"] + "\nExisting Work ID: " + pre["config"]["work_id"] + "\n"
        permissions = {"*": "deny", "read": "allow", "glob": "allow", "grep": "allow",
                       "list": "allow", "skill": "allow", "edit": "deny", "write": "deny",
                       "bash": {"skillsilent run code-analyzer *": "allow",
                                "skillsilent run doc-converter *": "allow",
                                "skillsilent run l1-knowledge-updater *": "allow", "*": "deny"},
                       "webfetch": "deny", "websearch": "deny", "external_directory": "deny"}
        env = dict(os.environ)
        env["OPENCODE_CONFIG_CONTENT"] = json.dumps({"permission": permissions, "plugin": []})
        env["OPENCODE_AUTO_SHARE"] = "false"
        env["OPENCODE_DISABLE_AUTOUPDATE"] = "true"
        # Analysis outputs remain on host. External repository data is never
        # passed to this Worker. The in-house OpenCode provider MUST be preapproved.
        with (report_dir / "local_orchestration_transcript.txt").open("wb") as f:
            proc = subprocess.run([pre["exe"], "run", "--dir", str(pre["code"]),
                                   "--agent", "build", prompt],
                                  stdin=subprocess.DEVNULL, stdout=f,
                                  stderr=subprocess.STDOUT, env=env,
                                  timeout=10800, check=False)
        out["run_id"] = pre["run_id"]
        out["work_id"] = pre["config"]["work_id"]
        out["source_revision"] = pre["config"]["source_revision"]
        out["opencode_returncode"] = proc.returncode
        # A model exit=0 is not evidence of code analyzer/doc converter execution.
        out["status"] = "ANALYSIS_PARTIAL" if proc.returncode == 0 else "FAILED"
        out["result_code"] = "REVIEW_REQUIRED" if proc.returncode == 0 else "OPENCODE_EXECUTION_FAILED"
        out["analysis"] = "REQUIRES_ARTIFACT_VALIDATION"
        out["msc"] = "REQUIRES_DOC_CONVERTER_RECEIPT"
        out["reason_codes"] = [out["result_code"]]
    except (ValueError, OSError, RuntimeError, subprocess.TimeoutExpired, UnicodeError) as exc:
        out["reason_codes"] = [str(exc)[:96] if isinstance(exc, ValueError) else type(exc).__name__]
    finally:
        out["completed_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
        _emit(skill_root / RESULT, out)
    print(json.dumps({"job_id": JOB_ID, "status": out["status"],
                      "result_code": out["result_code"], "reason_codes": out["reason_codes"]}))
    # The job core receives a durable semantic result even for a preflight block.
    return out

if __name__ == "__main__":
    result = run()
    raise SystemExit(0)
