from __future__ import annotations

import argparse
import hashlib
import json
import signal
import sys
import threading
from dataclasses import asdict, dataclass
from pathlib import Path

from . import __version__
from .approval import TrustRootError, check_trust_root_acl, load_trust_root, watcher_write_findings
from .shadow_guard import ShadowIsolationError, ShadowRunner, account_reach, assert_isolated, verify_after_create
from .signature_backend import default_backend
from .auth_flow import MAX_CODE_ATTEMPTS, REQUIRED_SCOPES, build_flow, describe_token_failure, validate_grant
from .config import Config, ConfigError
from .dropbox_transport import DropboxTransport
from .models import JobState
from .orchestrator import REMOTE_CURSOR_NAME, ScanSummary, _drain, group_request_entries, run_scan_cycle
from .review_runner import RealReviewRunner
from .secret_prompt import PromptCancelled, PromptEmpty, PromptUnavailable, ask_authorization_code
from .secrets_store import load_granted_scope, load_secrets, save_secrets
from .state_store import StateStore
from .transport_base import AuthRequired, Transport, TransportError, UploadConflict
from .validator import LocalPolicy
from .watch_loop import run_watch

EXIT_OK = 0
EXIT_CONFIG = 2
EXIT_LOCKED = 3
EXIT_AUTH_REQUIRED = 4
EXIT_TRANSPORT = 5
EXIT_REFUSED = 6
EXIT_VERIFY_FAILED = 7
EXIT_CANCELLED = 8      # auth-init: dialog cancelled
EXIT_EMPTY_INPUT = 9    # auth-init: OK pressed with nothing entered
EXIT_NO_GUI = 10        # auth-init: no window could be opened

# transport observer event -> audit counter
_API_COUNTERS = {
    "API_TRANSIENT_ERROR": "api_transient_errors",
    "API_RETRY_RECOVERED": "api_recoveries",
    "API_RETRY_EXHAUSTED": "api_retry_exhausted",
    "API_RETRY_ABORTED": "api_retry_aborted",
}
_WATCH_COUNTERS = {
    "WATCH_RECOVERED": "watch_recoveries",
    "WATCH_BACKOFF": "watch_backoffs",
    "LONGPOLL_ERROR": "longpoll_errors",
}


def _load(config_path: str) -> Config:
    return Config.load(config_path)


# --- shutdown -------------------------------------------------------------


class StopSignal:
    """Ctrl+C / Ctrl+Break / SIGTERM set an Event instead of raising inside a
    random line. Every wait in the program is stop.wait(), so a stop request
    ends it at once. A second signal restores the default behaviour."""

    def __init__(self) -> None:
        self.event = threading.Event()
        self._previous: dict[int, object] = {}

    def install(self) -> None:
        for name in ("SIGINT", "SIGTERM", "SIGBREAK"):
            sig = getattr(signal, name, None)
            if sig is None:
                continue
            try:
                self._previous[sig] = signal.signal(sig, self._handle)
            except (ValueError, OSError):  # not the main thread / unsupported
                pass

    def restore(self) -> None:
        for sig, previous in self._previous.items():
            try:
                signal.signal(sig, previous)
            except (ValueError, OSError, TypeError):
                pass
        self._previous.clear()

    def _handle(self, signum, frame) -> None:
        if self.event.is_set():
            self.restore()
            raise KeyboardInterrupt
        print("stop requested - finishing the current step, then exiting (press again to force)", flush=True)
        self.event.set()


# --- runtime wiring ---------------------------------------------------------


@dataclass
class Runtime:
    cfg: Config
    store: StateStore
    transport: Transport
    policy: LocalPolicy
    runner: RealReviewRunner
    allowed: bool
    dry_run: bool
    snapshot_root: Path
    review_run_dir: Path
    stop: threading.Event
    exclusive: bool = False

    def close(self) -> None:
        self.store.close()


def _build_policy(cfg: Config) -> LocalPolicy:
    root = cfg.remote_root.rstrip("/")
    return LocalPolicy(
        active_baseline_id=cfg.baseline_id,
        local_policy_revision=str(cfg.schema_version),
        known_run_policy_refs=cfg.review_policy.known_run_policy_refs,
        approved_knowledge_prefixes=(f"{root}/knowledge/", f"{root}/projects/"),
        approved_package_prefixes=(f"{root}/packages/",),
        run_budgets_usd={
            ref: cfg.review_policy.budget_for(ref)
            for ref in cfg.review_policy.known_run_policy_refs
            if cfg.review_policy.budget_for(ref) is not None
        },
        run_efforts={
            ref: cfg.review_policy.effort_for(ref)
            for ref in cfg.review_policy.known_run_policy_refs
            if cfg.review_policy.effort_for(ref) is not None
        },
        prompt_cache_ttl=cfg.review_policy.prompt_cache_ttl,
        daily_budget_usd=cfg.review_policy.daily_budget_usd,
        max_dispatches_per_day=cfg.review_policy.max_dispatches_per_day,
        usage_limit_wait_sec=cfg.review_policy.usage_limit_wait_sec,
        usage_limit_max_wait_sec=cfg.review_policy.usage_limit_max_wait_sec,
        usage_limit_max_deferrals=cfg.review_policy.usage_limit_max_deferrals,
    )


def _build_runner(cfg: Config) -> RealReviewRunner:
    # Constructing the runner does not start anything; only .run() does, and
    # the orchestrator only calls .run() when dispatch_allowed is true.
    return RealReviewRunner(
        claude_exe=cfg.claude_executable or "claude",
        model=cfg.review_policy.model,
        allowed_tools=cfg.review_policy.allowed_tools,
        max_budget_usd=cfg.review_policy.max_budget_usd,
        timeout_sec=cfg.review_policy.timeout_sec,
        prompt_cache_ttl=cfg.review_policy.prompt_cache_ttl,
        save_transcript=cfg.review_policy.save_transcript,
    )


def read_github_token(token_file: str | None, repo: str | None = None) -> str:
    """The token text from a plain one-line file, or from the JSON form this PC already uses
    ({"token": "...", "repo": "...", "scope": "...", "expires": "..."}), so the existing file needs no copy.
    A JSON file that names a different repository is refused. Error messages never contain file content."""
    if not token_file:
        raise AuthRequired("no GitHub token file is configured")
    try:
        text = Path(token_file).read_text(encoding="utf-8-sig").strip()
    except OSError as exc:
        raise AuthRequired("GitHub token file is unreadable") from exc
    if text.startswith("{"):
        try:
            data = json.loads(text)
        except ValueError:
            raise AuthRequired("GitHub token file is not valid JSON") from None
        value = data.get("token") if isinstance(data, dict) else None
        if not isinstance(value, str) or not value.strip():
            raise AuthRequired("GitHub token file has no token value")
        named = data.get("repo")
        if repo and isinstance(named, str) and named.strip() and named.strip().lower() != repo.lower():
            raise AuthRequired("GitHub token file is for a different repository")
        return value.strip()
    return text


def _build_github_transport(cfg: Config) -> Transport:
    from .github_transport import GitHubTransport

    if not cfg.github_repo:
        raise ConfigError("github.repo is required when transport is github")
    token_file = cfg.github_token_file

    def token() -> str:
        # The credential is read only when a request needs it and is never printed.
        return read_github_token(token_file, cfg.github_repo)

    return GitHubTransport(repo=cfg.github_repo, branch=cfg.github_branch,
                           remote_root=cfg.remote_root, token_provider=token,
                           read_only=(cfg.provider_mode == "SHADOW"))


def _build_transport(cfg: Config, store: StateStore | None, stop: threading.Event | None) -> Transport:
    if cfg.transport == "github":
        return _build_github_transport(cfg)
    secrets = load_secrets(cfg.state_dir)

    def observer(event: str, detail: str) -> None:
        if store is None:
            return
        store.log_event(event, detail=detail)
        counter = _API_COUNTERS.get(event)
        if counter:
            store.increment_counter(counter)

    return DropboxTransport(
        secrets.get("app_key", ""), secrets.get("refresh_token", ""),
        observer=observer, stop_event=stop,
    )


def _work_dir(cfg: Config) -> Path:
    """LIVE keeps the database, runs, snapshots and the single-instance lock together.
    SHADOW has its OWN folder for all of them (S-1): it never opens the live database,
    its WAL or its SHM, and never contends for the live watcher's lock. The folder is
    proven separate before it is created and again after (check-then-create gap)."""
    if cfg.provider_mode == "LIVE":
        return cfg.state_dir
    assert_isolated(cfg.local_state_dir, cfg.shadow_state_dir)
    work = Path(cfg.shadow_state_dir)
    work.mkdir(parents=True, exist_ok=True)
    return verify_after_create(cfg.local_state_dir, cfg.shadow_state_dir)


def _db_path(cfg: Config) -> Path:
    return _work_dir(cfg) / "state.sqlite3"


def _load_trust(cfg: Config, store: StateStore):
    """The trust root, or None with a TRUST_ROOT_REFUSED event. Every problem
    (unpinned, pin mismatch, rollback, writable by broad groups) fails closed."""
    if not cfg.trust_root_file:
        return None
    try:
        if not cfg.trust_root_sha256:
            raise TrustRootError("TRUST_ROOT_NOT_PINNED")
        trust = load_trust_root(cfg.trust_root_file, expected_sha256=cfg.trust_root_sha256)
        findings = check_trust_root_acl(cfg.trust_root_file)
        if findings:
            raise TrustRootError("TRUST_ROOT_ACL: " + "; ".join(findings))
        store.check_trust_version(trust.version)
        root = Path(cfg.trust_root_file)
        items = [("trust root file", str(root)), ("trust root folder", str(root.parent))]
        if cfg.config_path:
            items += [("config file that holds the pin", cfg.config_path),
                      ("config folder", str(Path(cfg.config_path).parent))]
        findings = watcher_write_findings(items)
        if findings:
            if cfg.trust_root_independence == "enforce":
                raise TrustRootError("TRUST_ROOT_NOT_INDEPENDENT: " + "; ".join(findings))
            store.log_event("TRUST_ROOT_INDEPENDENCE_WARNING", detail="; ".join(findings)[:300])
        store.log_event("TRUST_ROOT_LOADED", detail=f"version={trust.version} keys={len(trust.keys)} frozen={trust.frozen}")
        return trust
    except TrustRootError as exc:
        store.log_event("TRUST_ROOT_REFUSED", detail=str(exc)[:200])
        return None


def _open_runtime(cfg: Config, dry_run_override: bool | None, stop: threading.Event) -> Runtime:
    mode = cfg.provider_mode
    reach = ("NOT_APPLICABLE_LIVE", [])
    if mode == "SHADOW":
        reach = account_reach(cfg.local_state_dir)
        if reach[1] and cfg.shadow_account_isolation == "enforce":
            raise ShadowIsolationError("ACCOUNT_CAN_REACH_LIVE_FOLDER: " + "; ".join(reach[1]))
    # SHADOW opens its OWN database in its OWN folder, writable, never the live one (S-1).
    store = StateStore(_db_path(cfg))
    if mode == "SHADOW":
        store.log_event("SHADOW_ACCOUNT_ISOLATION", detail=f"{reach[0]} findings={len(reach[1])} policy={cfg.shadow_account_isolation}")
    store.check_provider(cfg.transport, mode)  # B-4: one LIVE provider at a time (SHADOW never touches the lease)
    dry_run = cfg.review_policy.dry_run if dry_run_override is None else dry_run_override
    work = _work_dir(cfg)
    review_run_dir = work / "runs"
    review_run_dir.mkdir(parents=True, exist_ok=True)
    policy = _build_policy(cfg)
    if cfg.transport == "github":
        policy.require_approval = mode == "LIVE"
        if mode == "LIVE":
            policy.trust_root = _load_trust(cfg, store)
            policy.signature_backend = default_backend()  # None without cryptography: approvals fail closed
    return Runtime(
        cfg=cfg, store=store, transport=_build_transport(cfg, store, stop),
        policy=policy, runner=ShadowRunner() if mode == "SHADOW" else _build_runner(cfg),
        allowed=cfg.review_policy.enabled and not dry_run and mode == "LIVE", dry_run=dry_run,
        snapshot_root=work / "snapshots", review_run_dir=review_run_dir, stop=stop,
    )


def _one_cycle(rt: Runtime) -> ScanSummary:
    summary = run_scan_cycle(
        rt.transport, rt.store, rt.policy, rt.runner, rt.allowed,
        rt.snapshot_root, rt.review_run_dir, rt.cfg.remote_root, stop_event=rt.stop,
        exclusive=rt.exclusive,
    )
    print(
        f"scan complete: dispatched={summary.dispatched} note={summary.note} "
        f"allowed={rt.allowed} pending={summary.pending}",
        flush=True,
    )
    return summary


def _exit_for(note: str) -> int:
    return {"AUTH_REQUIRED": EXIT_AUTH_REQUIRED, "TRANSPORT_ERROR": EXIT_TRANSPORT}.get(note, EXIT_OK)


# --- commands ---------------------------------------------------------------


def cmd_config_check(args) -> int:
    cfg = _load(args.config)
    dropbox = cfg.transport == "dropbox"   # only Dropbox keeps secrets in the live folder; never open it otherwise
    secrets = load_secrets(cfg.state_dir) if dropbox else {}
    rp = cfg.review_policy
    print(f"version: {__version__}")
    print(f"baseline_id: {cfg.baseline_id}")
    print(f"remote_root: {cfg.remote_root}")
    print(f"local_state_dir: {cfg.local_state_dir}")
    print(f"enabled: {rp.enabled}  dry_run: {rp.dry_run}  dispatch_allowed: {rp.dispatch_allowed}")
    print(f"enabled_source: {rp.enabled_source}")
    print(f"prompt_cache_ttl: {rp.prompt_cache_ttl}  save_transcript: {rp.save_transcript}  default_effort: {rp.effort or '(user setting)'}")
    for ref in rp.known_run_policy_refs:
        print(f"  run policy {ref}: max_budget_usd={rp.budget_for(ref)} effort={rp.effort_for(ref) or '(user setting)'}")
    print(f"claude_executable: {cfg.claude_executable or '(auto: PATH)'}")
    print(
        "secrets present: "
        f"app_key={'yes' if secrets.get('app_key') else 'no'} "
        f"refresh_token={'yes' if secrets.get('refresh_token') else 'no'}"
    )
    granted = load_granted_scope(cfg.state_dir) if dropbox else []
    print(f"recorded scopes: {' '.join(granted) if granted else '(none recorded)'}")
    return EXIT_OK


def _verify_stored_credentials(cfg: Config) -> int:
    transport = _build_transport(cfg, None, None)
    try:
        transport.ensure_auth()
    except AuthRequired as exc:
        print(f"AUTH_REQUIRED: stored credentials were rejected ({exc})")
        return EXIT_AUTH_REQUIRED
    except TransportError as exc:
        print(f"TRANSPORT_ERROR: could not verify credentials ({exc})")
        return EXIT_TRANSPORT
    print("auth: OK - Dropbox accepted the stored refresh token")
    return EXIT_OK


def _refuse_unless_dropbox(cfg: Config) -> bool:
    if cfg.transport == "dropbox":
        return False
    print("REFUSED: this command is for the Dropbox provider only (GitHub uses a read-only token file)")
    return True


def cmd_auth_check(args) -> int:
    cfg = _load(args.config)
    if _refuse_unless_dropbox(cfg):
        return EXIT_REFUSED
    secrets = load_secrets(cfg.state_dir)
    if not (secrets.get("app_key") and secrets.get("refresh_token")):
        print("AUTH_REQUIRED: no stored credentials (run auth-init)")
        return EXIT_AUTH_REQUIRED
    rc = _verify_stored_credentials(cfg)
    granted = load_granted_scope(cfg.state_dir)
    if granted:
        print(f"scopes recorded at authorization: {' '.join(granted)}")
        problems = validate_grant(granted, "x")
        for p in problems:
            print(f"WARNING: {p}")
    return rc


def cmd_auth_init(args) -> int:
    """One-time interactive PKCE OAuth. Never called from scan/watch and it
    never touches a claude process. Existing working credentials are kept:
    this only starts a new authorization when none exist or Dropbox rejects
    the stored ones."""
    from dropbox.oauth import DropboxOAuth2FlowNoRedirect

    cfg = _load(args.config)
    if _refuse_unless_dropbox(cfg):
        return EXIT_REFUSED
    existing = load_secrets(cfg.state_dir)
    if existing.get("app_key") and existing.get("refresh_token") and not args.force:
        rc = _verify_stored_credentials(cfg)
        if rc == EXIT_OK:
            print("Nothing to do: valid credentials already exist (use --force to authorize again).")
            return EXIT_OK
        if rc != EXIT_AUTH_REQUIRED:
            return rc  # network trouble is not a reason to overwrite credentials
        print("Stored credentials are no longer valid; starting a new authorization.")

    app_key = args.app_key or input("Dropbox app key: ").strip()
    flow = build_flow(app_key, DropboxOAuth2FlowNoRedirect)
    print("1. Open this URL in a browser and approve access:")
    print(f"   {flow.start()}")
    print(f"   (requests only: {', '.join(REQUIRED_SCOPES)})")
    print("2. A window will open: paste the authorization code there (Ctrl+V) and press OK.", flush=True)
    result = None
    for attempt in range(1, MAX_CODE_ATTEMPTS + 1):
        try:
            auth_code = ask_authorization_code()
        except PromptCancelled:
            print("Cancelled: nothing was saved. Run auth-init again when you have the code.")
            return EXIT_CANCELLED
        except PromptEmpty:
            print("No code was entered: nothing was saved. Run auth-init again.")
            return EXIT_EMPTY_INPUT
        except PromptUnavailable as exc:
            # Deliberately no fallback to input(): that would echo the code.
            print(f"ERROR: {exc}", file=sys.stderr)
            print("Nothing was saved. The code is never requested on the console.", file=sys.stderr)
            return EXIT_NO_GUI
        try:
            result = flow.finish(auth_code)
            break
        except Exception as exc:  # only type / HTTP status / OAuth error word are shown
            summary, hint = describe_token_failure(exc)
            print(f"Dropbox rejected the authorization code ({summary}); nothing was saved.")
            print(hint)
            if attempt < MAX_CODE_ATTEMPTS:
                print(f"Same URL, new attempt {attempt + 1}/{MAX_CODE_ATTEMPTS}: the window opens again "
                      "(Cancel to stop).", flush=True)
    if result is None:
        print("Giving up after repeated rejections; run auth-init again for a fresh URL.")
        return EXIT_REFUSED

    problems = validate_grant(result.scope, result.refresh_token)
    if problems:
        print("Authorization completed but is NOT usable, nothing was saved:")
        for p in problems:
            print(f"  - {p}")
        return EXIT_REFUSED
    path = save_secrets(cfg.state_dir, app_key, result.refresh_token, scope=result.scope)
    print(f"Saved credentials to {path}")
    print("The values are not printed and live outside any Dropbox-synced folder.")
    print("Next: auth-check, then list-remote.")
    return EXIT_OK


def cmd_list_remote(args) -> int:
    cfg = _load(args.config)
    transport = _build_transport(cfg, None, None)
    try:
        transport.ensure_auth()
        entries, _cursor = _drain(transport, transport.list_folder(cfg.remote_root))
    except AuthRequired as exc:
        print(f"AUTH_REQUIRED: {exc}")
        return EXIT_AUTH_REQUIRED
    except TransportError as exc:
        print(f"TRANSPORT_ERROR: {exc}")
        return EXIT_TRANSPORT
    root = cfg.remote_root.rstrip("/")
    print(f"remote_root: {cfg.remote_root}  files(recursive): {len(entries)}")
    for e in sorted(entries, key=lambda x: x.path):
        print(f"  {e.size:>9}  {e.rev}  {e.path}")
    request_files = [e for e in entries if e.path.startswith(root + "/requests/")]
    groups = group_request_entries(entries, cfg.remote_root)
    print(f"requests/ files: {len(request_files)}  request groups: {len(groups)}")
    print(f"request_queue: {'EMPTY' if not request_files else 'NOT_EMPTY ' + ','.join(sorted(groups))}")
    return EXIT_OK


def cmd_scan(args) -> int:
    cfg = _load(args.config)
    stop = threading.Event()
    rt = _open_runtime(cfg, args.dry_run, stop)
    try:
        return _exit_for(_one_cycle(rt).note)
    finally:
        rt.close()


def cmd_watch(args) -> int:
    from .lock import SingleInstanceLock

    cfg = _load(args.config)
    lock_path = _work_dir(cfg) / "watch.lock"
    signals = StopSignal()
    try:
        with SingleInstanceLock(lock_path):
            signals.install()
            rt = _open_runtime(cfg, args.dry_run, signals.event)
            rt.exclusive = True
            try:
                poll = args.poll_interval or cfg.poll_interval_sec
                mode = {
                    "version": __version__,
                    "enabled": cfg.review_policy.enabled,
                    "enabled_source": cfg.review_policy.enabled_source,
                    "dry_run": rt.dry_run,
                    "dispatch_allowed": rt.allowed,
                    "poll_interval_sec": poll,
                    "longpoll": bool(args.longpoll),
                    "longpoll_timeout_sec": cfg.longpoll_timeout_sec,
                    "max_cycles": args.max_cycles,
                    "max_runtime_sec": args.max_runtime_sec,
                    "max_backoff_sec": args.max_backoff_sec,
                }
                rt.store.log_event("WATCH_START", detail=json.dumps(mode))
                print(f"watch mode: {json.dumps(mode)}", flush=True)

                def on_event(event: str, detail: str) -> None:
                    rt.store.log_event(event, detail=detail)
                    counter = _WATCH_COUNTERS.get(event)
                    if counter:
                        rt.store.increment_counter(counter)

                def do_longpoll(timeout: int) -> bool:
                    cursor = rt.store.get_cursor(rt.transport.cursor_name)
                    if cursor is None:
                        return False
                    rt.store.increment_counter("longpoll_calls")
                    return rt.transport.longpoll(cursor, timeout)

                result = run_watch(
                    run_cycle=lambda: _one_cycle(rt),
                    stop=signals.event,
                    poll_interval=poll,
                    max_backoff=args.max_backoff_sec,
                    max_cycles=args.max_cycles,
                    max_runtime_sec=args.max_runtime_sec,
                    longpoll=do_longpoll if args.longpoll else None,
                    longpoll_timeout=cfg.longpoll_timeout_sec,
                    on_event=on_event,
                )
                rt.store.log_event("WATCH_END", detail=json.dumps(asdict(result)))
                print(f"watch finished: {json.dumps(asdict(result))}", flush=True)
                if result.auth_required:
                    print("AUTH_REQUIRED: credentials are missing or were rejected; run auth-init.", file=sys.stderr)
                    return EXIT_AUTH_REQUIRED
                return EXIT_OK
            finally:
                signals.restore()
                rt.close()
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return EXIT_LOCKED


_STATUS_COUNTERS = (
    "review_dispatch_count", "claude_process_start_count", "model_calls",
    "scan_cycles", "scan_ok_cycles", "scan_auth_required", "scan_transport_errors",
    "api_transient_errors", "api_recoveries", "api_retry_exhausted", "api_retry_aborted",
    "watch_recoveries", "watch_backoffs", "longpoll_calls", "longpoll_errors",
)


def cmd_reconcile(args) -> int:
    """Read-only backlog accounting per provider; opens the database with mode=ro."""
    cfg = _load(args.config)
    store = StateStore(_db_path(cfg), read_only=True)
    try:
        print(json.dumps(store.reconciliation_manifest(), indent=2, sort_keys=True))
    finally:
        store.close()
    return EXIT_OK


def cmd_status(args) -> int:
    cfg = _load(args.config)
    store = StateStore(_db_path(cfg))
    try:
        for name in _STATUS_COUNTERS:
            print(f"{name}: {store.get_counter(name)}")
        print(f"cursor_present: {store.get_cursor(REMOTE_CURSOR_NAME) is not None}")
        print(f"pending_requests: {store.list_pending()}")
        print("recent events:")
        for ts, event, key, detail in store.recent_events(limit=args.events):
            print(f"  {ts}  {event:<28} {key or '-'}  {detail or ''}")
    finally:
        store.close()
    return EXIT_OK


def cmd_recover(args) -> int:
    cfg = _load(args.config)
    store = StateStore(_db_path(cfg))
    try:
        stuck = store.jobs_in_states(
            [JobState.REVIEW_UNCERTAIN, JobState.CLAIMED, JobState.REVIEW_RUNNING, JobState.FAILED]
        )
        if not stuck:
            print("no uncertain/in-flight/failed jobs.")
            return EXIT_OK
        for job in stuck:
            print(f"{job.processing_key}  state={job.state.value}  last_error={job.last_error}")
        if args.requeue:
            print("requeue is disabled: a job that may already have run a model call is never re-dispatched. "
                  "Publish a new request revision to review again.")
            return EXIT_REFUSED
        print("nothing changed; uncertain, in-flight and failed jobs stay as they are.")
        return EXIT_OK
    finally:
        store.close()


def cmd_publish_package(args) -> int:
    """Upload one file under <remote_root>/packages/ without ever replacing
    different bytes at an existing path, then read it back and compare."""
    cfg = _load(args.config)
    root = cfg.remote_root.rstrip("/")
    remote_path = args.remote_path
    if not remote_path.startswith(root + "/packages/") or not remote_path.lower().endswith(".zip"):
        print(f"REFUSED: remote path must be a .zip under {root}/packages/")
        return EXIT_REFUSED
    local = Path(args.file)
    data = local.read_bytes()
    sha = hashlib.sha256(data).hexdigest()
    print(f"local: {local}  size={len(data)}  sha256={sha}")
    if args.expect_sha256 and args.expect_sha256.lower() != sha:
        print("REFUSED: local file does not match --expect-sha256")
        return EXIT_REFUSED

    transport = _build_transport(cfg, None, None)
    try:
        transport.ensure_auth()
        existing = transport.get_metadata(remote_path)
        if existing is None:
            try:
                meta = transport.upload(remote_path, data, mode="add")
                action = "PUBLISHED"
            except UploadConflict:
                existing = transport.get_metadata(remote_path)
                meta = existing
                action = "ALREADY_PRESENT"
        else:
            meta, action = existing, "ALREADY_PRESENT"
        back, back_meta = transport.download(remote_path)
    except AuthRequired as exc:
        print(f"AUTH_REQUIRED: {exc}")
        return EXIT_AUTH_REQUIRED
    except TransportError as exc:
        print(f"TRANSPORT_ERROR: {exc}")
        return EXIT_TRANSPORT

    back_sha = hashlib.sha256(back).hexdigest()
    print(f"remote: {back_meta.path}  size={back_meta.size}  id={back_meta.file_id}  rev={back_meta.rev}")
    print(f"remote sha256 (downloaded and hashed here): {back_sha}")
    if back_sha != sha or len(back) != len(data):
        print(f"REFUSED: remote bytes differ from the local file ({action}); nothing was overwritten.")
        return EXIT_REFUSED if action == "ALREADY_PRESENT" else EXIT_VERIFY_FAILED
    print(f"{action}: remote bytes are identical to the local file")
    return EXIT_OK


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="skill-collab-watcher")
    parser.add_argument("--config", default=None, help="path to reviewer config JSON")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("config-check", help="print resolved config and secret presence (no values)")
    p.set_defaults(func=cmd_config_check)

    p = sub.add_parser("auth-init", help="one-time interactive Dropbox PKCE/offline authorization")
    p.add_argument("--app-key")
    p.add_argument("--force", action="store_true", help="authorize again even if stored credentials work")
    p.set_defaults(func=cmd_auth_init)

    p = sub.add_parser("auth-check", help="verify stored credentials with Dropbox (read-only)")
    p.set_defaults(func=cmd_auth_check)

    p = sub.add_parser("list-remote", help="list the remote root and report whether the request queue is empty (read-only)")
    p.set_defaults(func=cmd_list_remote)

    p = sub.add_parser("scan", help="run exactly one scan cycle and exit")
    p.add_argument("--dry-run", action="store_true", default=None)
    p.set_defaults(func=cmd_scan)

    p = sub.add_parser("watch", help="run scan cycles in a loop (manual ON only - no service/startup registration)")
    p.add_argument("--dry-run", action="store_true", default=None)
    p.add_argument("--once", dest="max_cycles", action="store_const", const=1, help="same as --max-cycles 1")
    p.add_argument("--max-cycles", type=int, default=None)
    p.add_argument("--max-runtime-sec", type=float, default=None, help="stop after this many seconds")
    p.add_argument("--poll-interval", type=int, default=None)
    p.add_argument("--longpoll", action="store_true", help="wait for remote changes with Dropbox long-poll between cycles")
    p.add_argument("--max-backoff-sec", type=float, default=300.0)
    p.set_defaults(func=cmd_watch)

    p = sub.add_parser("status", help="print counters and recent audit events")
    p.add_argument("--events", type=int, default=20)
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("reconcile", help="read-only: pending requests per provider and job states")
    p.set_defaults(func=cmd_reconcile)

    p = sub.add_parser("recover", help="list REVIEW_UNCERTAIN/FAILED/in-flight jobs; --requeue to reset them")
    p.add_argument("--requeue", action="store_true")
    p.set_defaults(func=cmd_recover)

    p = sub.add_parser("publish-package", help="upload a .zip under <remote_root>/packages/ (never overwrites different bytes)")
    p.add_argument("--file", required=True)
    p.add_argument("--remote-path", required=True)
    p.add_argument("--expect-sha256")
    p.set_defaults(func=cmd_publish_package)

    args = parser.parse_args(argv)
    if args.config is None:
        args.config = str(Path(__file__).resolve().parents[1] / "config" / "reviewer.config.json")
    try:
        return args.func(args)
    except ConfigError as exc:
        print(f"CONFIG ERROR: {exc}", file=sys.stderr)
        return EXIT_CONFIG
    except ShadowIsolationError as exc:
        print(f"SHADOW REFUSED: {exc}", file=sys.stderr)
        return EXIT_REFUSED


if __name__ == "__main__":
    raise SystemExit(main())
