from __future__ import annotations

import hashlib
import json
import re
import shutil
import threading
import zipfile
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from pathlib import Path

from . import __version__
from .approval import ApprovalRejected, ClockUntrusted, NotConfigured, check_clock, knowledge_refs_hash, verify_approval
from .models import JobState, ReviewResult, ValidationOutcome, ValidationResult
from .review_runner import ReviewRunner
from .state_store import StateStore
from .transport_base import (
    AuthRequired, EntryMeta, RemoteNotFound, Transport, TransportError, UploadConflict,
)
from .validator import SAFE_NAME, LocalPolicy, validate
from .zip_safety import UnsafeZip, package_secret_findings, safe_extract

REMOTE_CURSOR_NAME = "skill_collab_root"
TERMINAL_STATES = (
    JobState.COMPLETED, JobState.FAILED, JobState.REVIEW_UNCERTAIN,
    JobState.CONFLICT, JobState.REJECTED,
)
IN_FLIGHT_STATES = (JobState.CLAIMED, JobState.REVIEW_RUNNING)
RESUMABLE_PUBLISH_STATES = (JobState.RESULT_SAVED, JobState.UPLOAD_PENDING)
MAX_LIST_PAGES = 10_000  # guard against a cursor that never reports has_more=False
NON_ACTIVE_NAME_MARKERS = ("DRAFT", "TEMPLATE", "EXAMPLE")
CONTEXT_DIR_NAME = "__SKILL_COLLAB_CONTEXT__"
# Only exact role basenames are REQUEST/READY files. Sidecars such as
# READY_APPROVAL.json or APPROVAL_SIG.json never match (B-2).
ROLE_FILE = re.compile(r"(REQUEST|READY)(?:_r\d+)?\.md", re.IGNORECASE)
PAUSE_FILE = "PAUSE_REVIEWS"  # any writer may create it: pausing is the safe direction
APPROVAL_FILE = "APPROVAL_SIG.json"
PIN_FILE = "SOURCE_PIN.json"


class ContextMismatch(Exception):
    """A pinned knowledge file does not have the pinned sha256."""


@dataclass
class ScanSummary:
    dispatched: int
    note: str
    pending: int = 0


@dataclass
class GroupResult:
    """dispatched: a review process was started for this request.
    retry: the request is not finished; keep it in pending_requests so the
    next cycle looks at it again even if Dropbox reports no new change."""

    dispatched: bool = False
    retry: bool = False


def group_request_entries(entries: list[EntryMeta], remote_root: str) -> dict[str, dict[str, EntryMeta]]:
    """Only files under <remote_root>/requests/<id>/ are candidate REQUEST
    or READY files. Everything else (packages/, reviews/, receipts/,
    knowledge/, a plain MD edit) is explicitly not a review-dispatch
    signal, per WATCHER_IMPLEMENT_PROMPT_r0001.md section 5."""
    root = remote_root.rstrip("/")
    found: dict[str, dict[str, list[EntryMeta]]] = {}
    for entry in entries:
        if entry.is_deleted or entry.is_folder:
            continue
        if not entry.path.startswith(root + "/requests/"):
            continue
        rel = entry.path[len(root) + len("/requests/"):]
        parts = rel.split("/")
        if len(parts) < 2:
            continue
        request_id, filename = parts[0], parts[-1]
        upper = filename.upper()
        if any(marker in upper for marker in NON_ACTIVE_NAME_MARKERS):
            continue
        match = ROLE_FILE.fullmatch(filename)
        if match is None:
            continue
        role = "request" if match.group(1).upper() == "REQUEST" else "ready"
        found.setdefault(request_id, {}).setdefault(role, []).append(entry)
    groups: dict[str, dict[str, EntryMeta]] = {}
    for request_id, roles in found.items():
        group: dict[str, EntryMeta] = {}
        for role, candidates in roles.items():
            # Two files that both look like the REQUEST (or READY) of one
            # request: do not guess which one GPT meant. The role stays empty,
            # so the request waits and no review starts.
            if len(candidates) == 1:
                group[role] = candidates[0]
        groups[request_id] = group
    return groups


def unrecognised_request_files(entries: list[EntryMeta], remote_root: str, request_id: str) -> list[str]:
    """REQUEST/READY-like names that are not exact basenames. Earlier watchers
    counted these as candidates (READY_APPROVAL.json made READY ambiguous and the
    request pended forever). Enabling them now could start an old request, so
    such a folder is blocked until a new revision is published."""
    prefix = f"{remote_root.rstrip('/')}/requests/{request_id}/"
    found: list[str] = []
    for entry in entries:
        if entry.is_deleted or entry.is_folder or not entry.path.startswith(prefix):
            continue
        name = entry.path[len(prefix):]
        if "/" in name:
            continue
        upper = name.upper()
        if any(marker in upper for marker in NON_ACTIVE_NAME_MARKERS):
            continue
        if name in (APPROVAL_FILE, PIN_FILE) or ROLE_FILE.fullmatch(name):
            continue
        if "REQUEST" in upper or "READY" in upper:
            found.append(name)
    return sorted(found)


_PROMPT_TEMPLATE_PATH = Path(__file__).resolve().parents[1] / "prompts" / "review_instructions.md"


def _fetch_context(transport: Transport, result: ValidationResult) -> list[tuple[str, str, bytes]]:
    """Download every pinned knowledge_refs file and compare its sha256 with
    the pin. Runs before the job is claimed, so a missing or changed file
    never costs a model call."""
    fetched: list[tuple[str, str, bytes]] = []
    for ref in result.fields.get("request", {}).get("knowledge_refs") or []:
        data, _meta = transport.download(ref["path"])
        sha = hashlib.sha256(data).hexdigest()
        if sha != str(ref["sha256"]).strip().lower():
            raise ContextMismatch(f"{ref['path']}: sha256 {sha} != pinned {ref['sha256']}")
        fetched.append((ref["path"], sha, data))
    return fetched


FILE_INDEX_NAME = "FILE_INDEX.txt"
MAX_INDEX_LINES = 2000


def _safe_file_name(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]", "_", str(text))


def _file_index(snapshot_dir: Path) -> str:
    """Plain list of the package files and sizes, built without a model, so the
    reviewer does not spend turns on Glob/ls exploration."""
    rows: list[tuple[int, str]] = []
    total = 0
    for path in sorted(snapshot_dir.rglob("*"), key=lambda p: p.relative_to(snapshot_dir).as_posix()):
        if not path.is_file():
            continue
        rel = path.relative_to(snapshot_dir).as_posix()
        if rel.startswith(CONTEXT_DIR_NAME + "/"):
            continue
        size = path.stat().st_size
        total += size
        rows.append((size, rel))
    lines = [f"# {len(rows)} package files, {total} bytes in total (size in bytes, path relative to the snapshot directory)"]
    lines += [f"{size:>9}  {rel}" for size, rel in rows[:MAX_INDEX_LINES]]
    if len(rows) > MAX_INDEX_LINES:
        lines.append(f"... {len(rows) - MAX_INDEX_LINES} more files not listed")
    return "\n".join(lines) + "\n"


def _write_context(
    snapshot_dir: Path, fetched: list[tuple[str, str, bytes]], file_index: str | None = None
) -> list[dict[str, str]]:
    """Place the verified knowledge next to (not inside) the package files, in
    the one reserved folder, so the reviewer can read it with --add-dir."""
    ctx = snapshot_dir / CONTEXT_DIR_NAME
    ctx.mkdir()
    written: list[dict[str, str]] = []
    for index, (remote_path, sha, data) in enumerate(fetched, start=1):
        base = "".join(c if (c.isalnum() or c in "._-") else "_" for c in remote_path.rsplit("/", 1)[-1])
        name = f"{index:02d}_{base[-80:]}"
        (ctx / name).write_bytes(data)
        written.append({"remote_path": remote_path, "sha256": sha, "file": f"{CONTEXT_DIR_NAME}/{name}"})
    if file_index is not None:
        (ctx / FILE_INDEX_NAME).write_text(file_index, encoding="utf-8")
    return written


def _redact_local_paths(text: str, *paths: Path) -> str:
    """The reviewer was told where the snapshot is; its answer must not carry
    this PC's directory layout into Dropbox."""
    for path in sorted({str(p) for p in paths}, key=len, reverse=True):
        for variant in {path, path.replace("\\", "/")}:
            text = text.replace(variant, "<snapshot>")
    return text


def _build_prompt(
    result: ValidationResult, context_files: list[dict[str, str]] | None = None,
    snapshot_dir: Path | None = None,
) -> str:
    """Loads a locally-authored, trusted prompt template (never the
    downloaded package's own text) and fills in only the pinned,
    already-validated REQUEST fields and the verified knowledge file list."""
    req = result.fields.get("request", {})
    template = _PROMPT_TEMPLATE_PATH.read_text(encoding="utf-8")
    context_files = context_files or []
    knowledge = "\n".join(
        f"- {c['file']}  (from {c['remote_path']}, sha256 verified by the watcher: {c['sha256']})"
        for c in context_files
    ) or "- (none pinned in this REQUEST)"
    return template.format(
        request_id=result.request_id,
        request_revision=result.request_revision,
        package_sha256=result.package_sha256,
        skill_id=req.get("skill_id", "UNKNOWN"),
        goal=req.get("goal", "(see the REQUEST text below)"),
        consumer_profiles=", ".join(str(p) for p in (req.get("consumer_profiles") or [])) or "(none specified)",
        context_dir=CONTEXT_DIR_NAME,
        file_index=f"{CONTEXT_DIR_NAME}/{FILE_INDEX_NAME}",
        snapshot_dir=str(snapshot_dir) if snapshot_dir is not None else "(the additional working directory)",
        knowledge_files=knowledge,
        request_body=(result.fields.get("request_body") or "").strip() or "(empty)",
    )


def _materialize_snapshot(
    transport: Transport, result: ValidationResult, package_bytes: bytes | None, snapshot_root: Path
) -> Path:
    digest = hashlib.sha256(result.processing_key.encode("utf-8")).hexdigest()[:12]
    dest = snapshot_root / f"{_safe_file_name(result.processing_key)[:100]}_{digest}"
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True, exist_ok=True)
    if package_bytes is None:
        data, _ = transport.download(result.package_path)
    else:
        data = package_bytes
    safe_extract(data, dest)
    return dest


def _save_result_locally(run_dir: Path, result: ValidationResult, review: ReviewResult) -> Path:
    out_dir = run_dir / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{_safe_file_name(result.request_id)}_{_safe_file_name(result.request_revision)}.json"
    path.write_text(
        json.dumps(
            {
                "request_id": result.request_id,
                "request_revision": result.request_revision,
                "package_sha256": result.package_sha256,
                "ok": review.ok,
                "output_text": review.output_text,
                "usage": review.usage,
                "error": review.error,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return path


def _yaml(value) -> str:
    """JSON text is valid YAML; this keeps odd characters in REQUEST values
    from breaking the front matter of the published result."""
    return json.dumps(value, ensure_ascii=False)


def _review_markdown(result: ValidationResult, review: ReviewResult) -> str:
    req = result.fields.get("request", {})
    pinned = [
        {"path": r.get("path"), "sha256": r.get("sha256")}
        for r in (req.get("knowledge_refs") or []) if isinstance(r, dict)
    ]
    limitations = [
        "static review by an automatically started Claude Code process; no package code was executed",
        "knowledge files were delivered as the REQUEST pinned them; which parts were actually read is reported by the reviewer in the text",
        "reviewer host is Windows; Linux, in-house LLM and MCP behaviour are not verified by this review",
    ]
    return (
        f"---\n"
        f"schema: SKILL_COLLAB_REVIEW_RESULT_V1\n"
        f"review_id: {_yaml(result.processing_key)}\n"
        f"responds_to_request_id: {_yaml(result.request_id)}\n"
        f"responds_to_request_revision: {_yaml(result.request_revision)}\n"
        f"package_sha256: {_yaml(result.package_sha256)}\n"
        f"skill_id: {_yaml(req.get('skill_id', 'UNKNOWN'))}\n"
        f"run_policy_ref: {_yaml(req.get('run_policy_ref', 'UNKNOWN'))}\n"
        f"knowledge_refs: {_yaml(pinned)}\n"
        f"consumer_profiles: {_yaml(list(req.get('consumer_profiles') or []))}\n"
        f"reviewer_os: WINDOWS\n"
        f"review_scope: CODE_REVIEW\n"
        f"test_policy: {_yaml(req.get('test_policy', 'STATIC_ONLY'))}\n"
        f"execution_status: {'COMPLETED' if review.ok else 'FAILED'}\n"
        f"limitations: {_yaml(limitations)}\n"
        f"---\n\n# 리뷰 결과\n\n{review.output_text}\n"
    )


class ReadbackMismatch(Exception):
    """The remote result or receipt does not carry this job's identity."""


def _verify_readback(transport: Transport, review_path: str, receipt_path: str,
                     result: ValidationResult, ok: bool) -> None:
    """COMPLETED is only set when the remote files name this exact job (T15).
    The receipt is compared field by field, not byte by byte, because it carries
    the watcher version and a retry after an upgrade must still be accepted."""
    try:
        receipt = json.loads(transport.download_latest(receipt_path)[0].decode("utf-8"))
        review_text = transport.download_latest(review_path)[0].decode("utf-8")
    except (ValueError, UnicodeDecodeError) as exc:
        raise ReadbackMismatch("remote result/receipt is not readable") from exc
    expected = {
        "processing_key": result.processing_key, "request_id": result.request_id,
        "request_revision": result.request_revision, "package_sha256": result.package_sha256, "ok": ok,
    }
    for name, want in expected.items():
        if receipt.get(name) != want:
            raise ReadbackMismatch(f"receipt {name} does not match this job")
    if f"review_id: {_yaml(result.processing_key)}\n" not in review_text:
        raise ReadbackMismatch("result review_id does not match this job")
    if f"package_sha256: {_yaml(result.package_sha256)}\n" not in review_text:
        raise ReadbackMismatch("result package_sha256 does not match this job")


def _publish_result(
    transport: Transport, store: StateStore, remote_root: str, result: ValidationResult,
    review: ReviewResult, result_path: Path,
) -> None:
    if not (SAFE_NAME.fullmatch(str(result.request_id)) and SAFE_NAME.fullmatch(str(result.request_revision))):
        raise ValueError("request_id/request_revision is not a plain name; refusing to build a remote path")
    review_path = f"{remote_root.rstrip('/')}/reviews/{result.request_id}/REVIEW_RESULT_{result.request_revision}.md"
    receipt_path = f"{remote_root.rstrip('/')}/receipts/{result.request_id}/RECEIPT_{result.request_revision}.md"
    md = _review_markdown(result, review)
    receipt = json.dumps(
        {"processing_key": result.processing_key, "request_id": result.request_id,
         "request_revision": result.request_revision, "package_sha256": result.package_sha256,
         "ok": review.ok, "watcher_version": __version__},
        ensure_ascii=False,
    )

    existing = transport.get_metadata(review_path)
    if existing is None:
        transport.upload(review_path, md.encode("utf-8"), mode="add")
    # else: already published by a previous attempt - do not re-upload/duplicate.

    existing_receipt = transport.get_metadata(receipt_path)
    if existing_receipt is None:
        transport.upload(receipt_path, receipt.encode("utf-8"), mode="add")

    _verify_readback(transport, review_path, receipt_path, result, review.ok)


def _read_doc(transport: Transport, entry: EntryMeta | None) -> tuple[str | None, bytes | None]:
    """Strict UTF-8 text plus the untouched bytes that every hash is computed
    over. For valid UTF-8 the bytes equal the text re-encoded, so this keeps the
    hashes the Dropbox watcher has always produced (B-6)."""
    if entry is None:
        return None, None
    data, _ = transport.download(entry.path)
    return data.decode("utf-8"), data


def _read_optional(transport: Transport, path: str) -> bytes | None:
    try:
        data, _ = transport.download(path)
    except RemoteNotFound:
        return None
    return data


def _describe(exc: BaseException) -> str:
    """Short, body-free description for the audit log."""
    return f"{type(exc).__name__}: {str(exc)[:200]}"


def _handle_existing_job(
    transport: Transport, store: StateStore, allowed: bool, remote_root: str,
    pre: ValidationResult, existing,
) -> GroupResult | None:
    """Decide from the stored job alone, before any package download.
    Returns None when the request has never been dispatched and may proceed."""
    key = pre.processing_key
    detail = f"{pre.request_id}"
    if existing.state in TERMINAL_STATES:
        note = "" if existing.processing_key == key else " (same request, revision and package under another policy revision)"
        store.log_event_once("DUPLICATE_SKIPPED", processing_key=key, detail=f"already {existing.state.value}{note}")
        return GroupResult()
    if existing.state in IN_FLIGHT_STATES:
        store.log_event_once("IN_PROGRESS_SKIPPED", processing_key=key, detail=detail)
        return GroupResult()
    if existing.state in RESUMABLE_PUBLISH_STATES:
        if not allowed:
            store.log_event_once("DISPATCH_SKIPPED_NOT_ALLOWED", processing_key=key, detail="publish retry waiting")
            return GroupResult(retry=True)
        return GroupResult(retry=not _retry_publish_only(transport, store, remote_root, pre, existing))
    # DISCOVERED / VALIDATED / WAIT_INPUT / AUTH_REQUIRED: never dispatched yet.
    if not allowed:
        store.log_event_once("DISPATCH_SKIPPED_NOT_ALLOWED", processing_key=key, detail="watcher OFF or dry_run=True")
        return GroupResult(retry=True)
    return None


def process_request_group(
    transport: Transport, store: StateStore, policy: LocalPolicy, runner: ReviewRunner,
    allowed: bool, snapshot_root: Path, review_run_dir: Path, remote_root: str,
    request_id: str, group: dict[str, EntryMeta],
) -> GroupResult:
    """Every read for one request comes from the same pinned revision when the
    transport supports pinning (GitHub), so REQUEST, READY, package and pinned
    knowledge are all taken from one commit."""
    transport.pin_current()
    try:
        return _process_request_group(
            transport, store, policy, runner, allowed, snapshot_root, review_run_dir,
            remote_root, request_id, group,
        )
    finally:
        transport.unpin()


def _check_approval(
    transport: Transport, store: StateStore, policy: LocalPolicy, remote_root: str,
    final: ValidationResult, request_raw: bytes, ready_raw: bytes,
) -> GroupResult | None:
    """None when the approval bundle verifies. Anything else keeps the request
    waiting with zero model calls (fail closed, B-1 / B-7)."""
    root = remote_root.rstrip("/")
    request = final.fields["request"]
    pinned = transport.current_pin()
    if pinned is None:
        store.log_event_once("APPROVAL_UNBOUND", processing_key=final.processing_key,
                              detail="this transport has no pinned source revision")
        return GroupResult(retry=True)
    try:
        provider_time = transport.server_time()
        check_clock(provider_time, datetime.now(timezone.utc))
        store.check_time_ratchet(int(provider_time.timestamp()))
    except ClockUntrusted as exc:
        store.log_event_once("APPROVAL_CLOCK_UNTRUSTED", processing_key=final.processing_key, detail=str(exc))
        return GroupResult(retry=True)
    approval_raw = _read_optional(transport, f"{root}/requests/{final.request_id}/{APPROVAL_FILE}")
    pin_raw = _read_optional(transport, f"{root}/requests/{final.request_id}/{PIN_FILE}")
    if approval_raw is None or pin_raw is None:
        store.log_event_once("APPROVAL_MISSING", processing_key=final.processing_key,
                              detail=f"{final.request_id}: approval bundle incomplete")
        return GroupResult(retry=True)
    expected = {
        "request_id": final.request_id,
        "request_revision": final.request_revision,
        "request_sha256": hashlib.sha256(request_raw).hexdigest(),
        "ready_sha256": hashlib.sha256(ready_raw).hexdigest(),
        "package_path": final.package_path,
        "package_sha256": final.package_sha256,
        "package_size_bytes": int(request["package_size_bytes"]),
        "local_policy_revision": policy.local_policy_revision,
        "run_policy_ref": str(request["run_policy_ref"]),
        "knowledge_refs_hash": knowledge_refs_hash(request.get("knowledge_refs") or []),
    }
    try:
        verify_approval(approval_raw, pin_raw, trust=policy.trust_root, backend=policy.signature_backend,
                        expected=expected, now=datetime.now(timezone.utc))
    except NotConfigured as exc:
        store.log_event_once("APPROVAL_UNVERIFIABLE", processing_key=final.processing_key, detail=str(exc))
        return GroupResult(retry=True)
    except ApprovalRejected as exc:
        store.log_event_once("APPROVAL_REJECTED", processing_key=final.processing_key, detail=str(exc))
        return GroupResult(retry=True)
    return None


def _check_ceilings(store: StateStore, policy: LocalPolicy, final: ValidationResult) -> GroupResult | None:
    """Rolling 24 h ceilings for unattended use. Dispatches whose cost was never
    recorded count at their cap (see StateStore.spend_since)."""
    if policy.max_dispatches_per_day is not None and store.dispatches_since() >= policy.max_dispatches_per_day:
        store.log_event_once("DAILY_LIMIT_BLOCKED", processing_key=final.processing_key,
                              detail="daily review count ceiling reached; the request stays pending")
        return GroupResult(retry=True)
    if policy.daily_budget_usd is not None:
        run_ref = str(final.fields["request"]["run_policy_ref"])
        this_run = policy.run_budgets_usd.get(run_ref, 0.0)
        if store.spend_since() + this_run > policy.daily_budget_usd:
            store.log_event_once("DAILY_BUDGET_BLOCKED", processing_key=final.processing_key,
                                  detail="daily spending ceiling would be exceeded; the request stays pending")
            return GroupResult(retry=True)
    return None


def _process_request_group(
    transport: Transport, store: StateStore, policy: LocalPolicy, runner: ReviewRunner,
    allowed: bool, snapshot_root: Path, review_run_dir: Path, remote_root: str,
    request_id: str, group: dict[str, EntryMeta],
) -> GroupResult:
    try:
        request_text, request_raw = _read_doc(transport, group.get("request"))
        ready_text, ready_raw = _read_doc(transport, group.get("ready"))
    except UnicodeDecodeError:
        store.log_event_once("REJECTED", detail=f"{request_id}: REQUEST/READY is not valid UTF-8")
        return GroupResult()
    except TransportError as exc:
        store.log_event_once("TRANSPORT_ERROR", detail=f"{request_id}: {_describe(exc)}")
        return GroupResult(retry=True)
    if (request_raw or b"").startswith(b"\xef\xbb\xbf") or (ready_raw or b"").startswith(b"\xef\xbb\xbf"):
        store.log_event_once("REJECTED", detail=f"{request_id}: REQUEST/READY starts with a UTF-8 BOM; not allowed")
        return GroupResult()

    pre = validate(request_text, ready_text, None, policy, expected_request_id=request_id,
                   request_bytes=request_raw)

    if not pre.needs_package_download:
        store.log_event_once(pre.outcome.value, processing_key=pre.processing_key, detail=f"{request_id}: {pre.reason}")
        return GroupResult(retry=pre.outcome == ValidationOutcome.WAIT_INPUT)

    # Exact key first. Otherwise look for the same request revision and package
    # under any policy revision (B-5): a finished or in-flight job must not be
    # repeated just because local_policy_revision changed.
    existing = store.get_job(pre.processing_key)
    if existing is None:
        logical = store.find_logical_job(pre.request_id, pre.request_revision, pre.package_sha256)
        if logical is not None and logical.state in TERMINAL_STATES + IN_FLIGHT_STATES + RESUMABLE_PUBLISH_STATES:
            existing = logical
    if existing is not None:
        early = _handle_existing_job(transport, store, allowed, remote_root, pre, existing)
        if early is not None:
            return early
    elif store.job_for_other_package(pre.request_id, pre.request_revision, pre.package_sha256) is not None:
        store.log_event_once("CONFLICT", processing_key=pre.processing_key,
                              detail=f"{request_id}: revision already bound to another package; original kept")
        return GroupResult()

    try:
        package_bytes, _meta = transport.download(pre.package_path)
    except TransportError as exc:
        store.log_event_once("TRANSPORT_ERROR", processing_key=pre.processing_key, detail=_describe(exc))
        return GroupResult(retry=True)
    sha = hashlib.sha256(package_bytes).hexdigest()
    final = validate(request_text, ready_text, (len(package_bytes), sha), policy, expected_request_id=request_id,
                     request_bytes=request_raw)

    store.log_event_once(final.outcome.value, processing_key=final.processing_key, detail=final.reason)

    if final.outcome != ValidationOutcome.VALIDATED:
        return GroupResult()

    try:
        findings = package_secret_findings(package_bytes)
    except (UnsafeZip, zipfile.BadZipFile):
        findings = []  # an unreadable package fails in the snapshot step, before any model call
    if findings:
        store.log_event_once("REJECTED", processing_key=final.processing_key,
                              detail=f"package contains credential-shaped text in {len(findings)} entr(y/ies); not dispatched")
        return GroupResult()

    if policy.require_approval:
        gate = _check_approval(transport, store, policy, remote_root, final, request_raw, ready_raw)
        if gate is not None:
            return gate

    if existing is not None:
        if existing.package_sha256 != final.package_sha256:
            store.update_job_state(final.processing_key, JobState.CONFLICT,
                                    last_error="package_sha256 changed under same request_id+revision")
            store.log_event("CONFLICT", processing_key=final.processing_key, detail="content changed under same key")
            return GroupResult()
    else:
        store.create_job(final.processing_key, final.request_id, final.request_revision,
                          final.package_sha256, JobState.VALIDATED)

    if not allowed:
        store.log_event_once("DISPATCH_SKIPPED_NOT_ALLOWED", processing_key=final.processing_key,
                              detail="watcher OFF or dry_run=True")
        return GroupResult(retry=True)

    # Unattended gates, cheapest first. Each one leaves the request pending (no
    # claim, no model call) and is reported once.
    if transport.get_metadata(f"{remote_root.rstrip('/')}/{PAUSE_FILE}") is not None:
        store.log_event_once("REVIEWS_PAUSED", processing_key=final.processing_key,
                              detail="pause marker present; no review is started")
        return GroupResult(retry=True)
    blocked = _check_ceilings(store, policy, final)
    if blocked is not None:
        return blocked

    # Pinned knowledge is fetched and hash-checked BEFORE the claim: a missing
    # or changed file must cost zero model calls.
    try:
        fetched_context = _fetch_context(transport, final)
    except ContextMismatch as exc:
        store.update_job_state(final.processing_key, JobState.CONFLICT, last_error=_describe(exc))
        store.log_event("CONFLICT", processing_key=final.processing_key, detail=_describe(exc))
        return GroupResult()
    except RemoteNotFound as exc:
        store.log_event_once("TRANSPORT_ERROR", processing_key=final.processing_key,
                              detail=f"pinned knowledge file not found: {_describe(exc)}")
        return GroupResult(retry=True)
    except TransportError as exc:
        store.log_event_once("TRANSPORT_ERROR", processing_key=final.processing_key, detail=_describe(exc))
        return GroupResult(retry=True)

    preflight = getattr(runner, "preflight", None)
    if preflight is not None:
        logged_in, reason = preflight()
        store.increment_counter("preflight_checks")
        if not logged_in:
            store.log_event_once("CLAUDE_AUTH_REQUIRED", processing_key=final.processing_key, detail=reason)
            return GroupResult(retry=True)

    # --- exactly one dispatch for this processing_key from here on ---
    if not store.try_claim(final.processing_key):
        # Another process claimed it between our read and now (or this is a read-only store): no dispatch.
        store.log_event_once("IN_PROGRESS_SKIPPED", processing_key=final.processing_key,
                             detail=f"{request_id}: claim lost to another process")
        return GroupResult()
    store.record_claim(final.processing_key)
    store.log_event("CLAIMED", processing_key=final.processing_key)

    try:
        snapshot_dir = _materialize_snapshot(transport, final, package_bytes, snapshot_root)
        if (snapshot_dir / CONTEXT_DIR_NAME).exists():
            raise ValueError(f"package contains the reserved folder {CONTEXT_DIR_NAME}")
        file_index = _file_index(snapshot_dir)
        context_files = _write_context(snapshot_dir, fetched_context, file_index)
        prompt_text = _build_prompt(final, context_files, snapshot_dir)
    except Exception as exc:  # unsafe/corrupt ZIP, prompt template problem: terminal, and no model was started
        store.update_job_state(final.processing_key, JobState.FAILED, last_error=_describe(exc))
        store.log_event("FAILED", processing_key=final.processing_key, detail=f"snapshot: {_describe(exc)}")
        return GroupResult()

    run_policy_ref = str(final.fields["request"]["run_policy_ref"])
    budget = policy.run_budgets_usd.get(run_policy_ref)
    effort = policy.run_efforts.get(run_policy_ref)
    store.update_job_state(final.processing_key, JobState.REVIEW_RUNNING)
    store.increment_counter("review_dispatch_count")
    store.log_event("REVIEW_DISPATCHED", processing_key=final.processing_key,
                    detail=json.dumps({"run_policy_ref": run_policy_ref, "max_budget_usd": budget,
                                       "effort": effort, "prompt_cache_ttl": policy.prompt_cache_ttl}))

    review_result = runner.run(snapshot_dir, prompt_text, review_run_dir, max_budget_usd=budget, effort=effort)
    if review_result.model_calls:
        store.increment_counter("claude_process_start_count", review_result.model_calls)
        store.increment_counter("model_calls", review_result.model_calls)
    if review_result.usage and review_result.usage.get("total_cost_usd") is not None:
        usage = review_result.usage
        store.log_event("REVIEW_COST", processing_key=final.processing_key, detail=json.dumps({
            "total_cost_usd": usage.get("total_cost_usd"),
            "num_turns": usage.get("num_turns"),
            "subtype": usage.get("subtype"),
            "max_budget_usd": budget,
            "effort": effort,
            "prompt_cache_ttl": policy.prompt_cache_ttl,
            "package_size_bytes": final.fields["request"].get("package_size_bytes"),
            "output_tokens": usage.get("output_tokens"),
            "cache_write_tokens": usage.get("cache_creation_input_tokens"),
            "cache_read_tokens": usage.get("cache_read_input_tokens"),
        }))

    if not review_result.ok:
        if review_result.error and "timeout" in review_result.error:
            store.update_job_state(final.processing_key, JobState.REVIEW_UNCERTAIN, last_error=review_result.error)
            store.log_event("REVIEW_UNCERTAIN", processing_key=final.processing_key, detail=review_result.error)
        else:
            store.update_job_state(final.processing_key, JobState.FAILED, last_error=review_result.error)
            store.log_event("FAILED", processing_key=final.processing_key, detail=review_result.error)
        return GroupResult(dispatched=True)

    review_result.output_text = _redact_local_paths(
        review_result.output_text, snapshot_dir, snapshot_root, snapshot_root.parent)
    result_path = _save_result_locally(review_run_dir, final, review_result)
    store.update_job_state(final.processing_key, JobState.RESULT_SAVED, result_path=str(result_path))
    store.update_job_state(final.processing_key, JobState.UPLOAD_PENDING)

    try:
        _publish_result(transport, store, remote_root, final, review_result, result_path)
        store.update_job_state(final.processing_key, JobState.COMPLETED)
        store.log_event("COMPLETED", processing_key=final.processing_key)
        return GroupResult(dispatched=True)
    except ReadbackMismatch as exc:
        store.update_job_state(final.processing_key, JobState.CONFLICT, last_error=_describe(exc))
        store.log_event("CONFLICT", processing_key=final.processing_key, detail=_describe(exc))
        return GroupResult(dispatched=True)
    except (TransportError, UploadConflict, AuthRequired) as exc:
        store.log_event("UPLOAD_FAILED", processing_key=final.processing_key, detail=_describe(exc))
        # job stays UPLOAD_PENDING; the next cycle's RESUMABLE_PUBLISH_STATES
        # branch retries the upload only - runner.run() is never called again.
        return GroupResult(dispatched=True, retry=True)


def _retry_publish_only(transport: Transport, store: StateStore, remote_root: str,
                         final: ValidationResult, existing) -> bool:
    """Upload-only retry path. Deliberately takes no ReviewRunner argument -
    it is structurally impossible for this function to start a claude
    process. Returns True when nothing is left to retry."""
    # The stored job may belong to an earlier policy revision; keep its key so
    # the receipt and state updates refer to the job that was actually run.
    final = replace(final, processing_key=existing.processing_key, package_sha256=existing.package_sha256)
    if not existing.result_path:
        store.update_job_state(final.processing_key, JobState.FAILED, last_error="no local result to publish")
        store.log_event("UPLOAD_RETRY_MISSING_LOCAL_RESULT", processing_key=final.processing_key)
        return True
    try:
        saved = json.loads(Path(existing.result_path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        store.update_job_state(final.processing_key, JobState.FAILED,
                                last_error="local result file missing or unreadable; a new request revision is required to re-review")
        store.log_event("UPLOAD_RETRY_MISSING_LOCAL_RESULT", processing_key=final.processing_key)
        return True
    review = ReviewResult(
        ok=bool(saved.get("ok")), output_text=saved.get("output_text", ""),
        output_format="json", exit_code=0, model_calls=0, usage=saved.get("usage"),
        error=saved.get("error"),
    )
    try:
        _publish_result(transport, store, remote_root, final, review, Path(existing.result_path))
        store.update_job_state(final.processing_key, JobState.COMPLETED)
        store.log_event("UPLOAD_RETRY_COMPLETED", processing_key=final.processing_key)
        return True
    except ReadbackMismatch as exc:
        store.update_job_state(final.processing_key, JobState.CONFLICT, last_error=_describe(exc))
        store.log_event("CONFLICT", processing_key=final.processing_key, detail=_describe(exc))
        return True
    except (TransportError, UploadConflict, AuthRequired) as exc:
        store.log_event_once("UPLOAD_RETRY_FAILED", processing_key=final.processing_key, detail=_describe(exc))
        return False


def _drain(transport: Transport, first) -> tuple[list[EntryMeta], str]:
    """Follow has_more to the end. A cursor is only meaningful once the
    listing it belongs to is complete."""
    entries = list(first.entries)
    result = first
    for _ in range(MAX_LIST_PAGES):
        if not result.has_more:
            return entries, result.cursor
        result = transport.list_folder_continue(result.cursor)
        entries.extend(result.entries)
    raise TransportError("listing did not terminate (has_more stayed true)")


def _collect_delta(transport: Transport, store: StateStore, remote_root: str) -> tuple[list[EntryMeta], str]:
    cursor = store.get_cursor(transport.cursor_name)
    try:
        first = transport.list_folder(remote_root) if cursor is None else transport.list_folder_continue(cursor)
        return _drain(transport, first)
    except TransportError as exc:
        if cursor is not None and "CURSOR_RESET" in str(exc):
            store.log_event("CURSOR_RESET", detail=str(exc))
            return _drain(transport, transport.list_folder(remote_root))
        raise


def _complete_group(
    transport: Transport, remote_root: str, request_id: str, group: dict[str, EntryMeta]
) -> tuple[dict[str, EntryMeta], list[str]]:
    """A delta may carry only REQUEST or only READY, and an earlier sidecar is
    not in the delta at all, so the request folder is always listed. Returns the
    group and any REQUEST/READY-like names that are not exact basenames."""
    first = transport.list_folder(f"{remote_root.rstrip('/')}/requests/{request_id}")
    entries, _ = _drain(transport, first)
    listed = group_request_entries(entries, remote_root).get(request_id, {})
    return {**listed, **group}, unrecognised_request_files(entries, remote_root, request_id)


def run_scan_cycle(
    transport: Transport, store: StateStore, policy: LocalPolicy, runner: ReviewRunner,
    allowed: bool, snapshot_root: Path, review_run_dir: Path, remote_root: str,
    stop_event: threading.Event | None = None,
    exclusive: bool = False,
) -> ScanSummary:
    store.pending_scope = transport.provider_name
    store.log_event("SCAN_START")
    store.increment_counter("scan_cycles")
    store.seal_interrupted(exclusive=exclusive)  # B-3: only with the watcher lock held, before any dispatch
    try:
        transport.ensure_auth()
    except AuthRequired as exc:
        store.log_event("AUTH_REQUIRED", detail=_describe(exc))
        store.increment_counter("scan_auth_required")
        return ScanSummary(dispatched=0, note="AUTH_REQUIRED")
    except TransportError as exc:
        store.log_event("TRANSPORT_ERROR", detail=_describe(exc))
        store.increment_counter("scan_transport_errors")
        return ScanSummary(dispatched=0, note="TRANSPORT_ERROR")

    try:
        entries, new_cursor = _collect_delta(transport, store, remote_root)
    except AuthRequired as exc:
        store.log_event("AUTH_REQUIRED", detail=_describe(exc))
        store.increment_counter("scan_auth_required")
        return ScanSummary(dispatched=0, note="AUTH_REQUIRED")
    except TransportError as exc:
        store.log_event("TRANSPORT_ERROR", detail=_describe(exc))
        store.increment_counter("scan_transport_errors")
        return ScanSummary(dispatched=0, note="TRANSPORT_ERROR")

    # Order matters: record every request id the delta mentions BEFORE the
    # cursor moves. If anything below fails or the process dies, the id is
    # still in pending_requests and is looked at again next cycle.
    groups = group_request_entries(entries, remote_root)
    for request_id in groups:
        store.add_pending(request_id, "delta")
    store.set_cursor(transport.cursor_name, new_cursor)

    dispatched = 0
    note = "OK"
    # A read-only (SHADOW) store cannot persist pending ids, so it evaluates
    # what this delta mentions directly.
    candidates = sorted(groups) if store.read_only else store.list_pending()
    for request_id in candidates:
        if stop_event is not None and stop_event.is_set():
            note = "STOPPING"
            break
        try:
            group, unrecognised = _complete_group(transport, remote_root, request_id, groups.get(request_id, {}))
            if unrecognised:
                store.log_event_once("LEGACY_SIDECAR_BLOCKED", detail=(
                    f"{request_id}: {', '.join(unrecognised)} not dispatched; publish a new request revision"))
                store.remove_pending(request_id)
                continue
            if not group:
                store.remove_pending(request_id)  # folder has no REQUEST/READY any more
                continue
            result = process_request_group(
                transport, store, policy, runner, allowed, snapshot_root, review_run_dir,
                remote_root, request_id, group,
            )
        except RemoteNotFound:
            store.remove_pending(request_id)  # request folder was deleted
            continue
        except AuthRequired as exc:
            store.log_event("AUTH_REQUIRED", detail=f"{request_id}: {_describe(exc)}")
            store.increment_counter("scan_auth_required")
            note = "AUTH_REQUIRED"
            break
        except TransportError as exc:
            store.log_event_once("TRANSPORT_ERROR", detail=f"{request_id}: {_describe(exc)}")
            store.increment_counter("scan_transport_errors")
            note = "TRANSPORT_ERROR"
            continue
        except Exception as exc:  # one bad request must not stop the others
            store.log_event_once("GROUP_ERROR", detail=f"{request_id}: {_describe(exc)}")
            note = "TRANSPORT_ERROR" if note == "OK" else note
            continue
        if result.dispatched:
            dispatched += 1
        if not result.retry:
            store.remove_pending(request_id)

    pending = len(store.list_pending())
    store.log_event("SCAN_END", detail=json.dumps({"dispatched": dispatched, "pending": pending, "note": note}))
    if note == "OK":
        store.increment_counter("scan_ok_cycles")
    return ScanSummary(dispatched=dispatched, note=note, pending=pending)
