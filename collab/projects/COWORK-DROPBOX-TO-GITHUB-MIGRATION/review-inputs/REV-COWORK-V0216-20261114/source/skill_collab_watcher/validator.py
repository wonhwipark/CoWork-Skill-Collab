from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field

import yaml

from .models import ValidationOutcome, ValidationResult

REQUEST_SCHEMA = "SKILL_COLLAB_REVIEW_REQUEST_V1"
READY_SCHEMA = "SKILL_COLLAB_READY_V1"
PLACEHOLDER_STATES = {"DRAFT_EXAMPLE"}


def _is_placeholder(value) -> bool:
    if value is None:
        return True
    if isinstance(value, str) and value.strip() in ("", "UNKNOWN", "DRAFT_EXAMPLE"):
        return True
    return False


class FrontMatterError(ValueError):
    pass


def parse_front_matter(text: str) -> dict:
    """Safe-load only. Never use yaml.load / the default (unsafe) loader -
    these files are untrusted remote input."""
    if not text.startswith("---"):
        raise FrontMatterError("missing leading '---'")
    end = text.find("\n---", 3)
    if end == -1:
        raise FrontMatterError("unterminated front matter block")
    block = text[3:end]
    try:
        data = yaml.safe_load(block)
    except yaml.YAMLError as exc:
        raise FrontMatterError(str(exc)) from exc
    if not isinstance(data, dict):
        raise FrontMatterError("front matter is not a mapping")
    return data


def front_matter_body(text: str) -> str:
    """Text after the closing '---' (the human-written part of a REQUEST)."""
    end = text.find("\n---", 3)
    if end == -1:
        return ""
    return text[end + len("\n---"):].lstrip("\r\n")


def _safe_remote_path(path: str, prefixes: tuple[str, ...], suffix: str | None = None) -> bool:
    """Case-insensitive prefix check (Dropbox paths are case-insensitive) that
    refuses '..', '.', backslashes and empty segments, so a REQUEST cannot
    point the watcher at a file outside the approved folders."""
    if not isinstance(path, str) or "\\" in path or not path.startswith("/"):
        return False
    parts = path.split("/")[1:]
    if any(p in ("", ".", "..") for p in parts):
        return False
    low = path.lower()
    if suffix and not low.endswith(suffix):
        return False
    return any(low.startswith(p.lower()) for p in prefixes)


@dataclass
class LocalPolicy:
    active_baseline_id: str
    local_policy_revision: str
    known_run_policy_refs: list[str]
    approved_knowledge_prefixes: tuple[str, ...] = ("/SKILL-COLLAB/knowledge/", "/SKILL-COLLAB/projects/")
    approved_package_prefixes: tuple[str, ...] = ("/SKILL-COLLAB/packages/",)
    run_budgets_usd: dict[str, float] = field(default_factory=dict)
    run_efforts: dict[str, str] = field(default_factory=dict)
    prompt_cache_ttl: str = "1h"
    daily_budget_usd: float | None = None
    max_dispatches_per_day: int | None = None
    usage_limit_wait_sec: int = 1800        # used when the CLI does not say when the window resets
    usage_limit_max_wait_sec: int = 86400   # never wait longer than this per deferral (24 h)
    usage_limit_max_deferrals: int = 12     # per job; then the job is FAILED instead of waiting forever
    require_approval: bool = False
    trust_root: object | None = None
    signature_backend: object | None = None


def _reject(reason: str) -> ValidationResult:
    return ValidationResult(outcome=ValidationOutcome.REJECTED, reason=reason)


def _conflict(reason: str) -> ValidationResult:
    return ValidationResult(outcome=ValidationOutcome.CONFLICT, reason=reason)


def _wait(reason: str) -> ValidationResult:
    return ValidationResult(outcome=ValidationOutcome.WAIT_INPUT, reason=reason)


REQUIRED_REQUEST_FIELDS = (
    "schema", "state", "request_id", "request_revision", "package_path",
    "package_sha256", "package_size_bytes", "run_policy_ref", "reviewer_os",
    "test_policy", "output_contract",
)
REQUIRED_READY_FIELDS = (
    "schema", "state", "request_id", "request_revision", "request_path",
    "request_sha256", "package_sha256", "baseline_id",
)


SAFE_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}")


def validate(
    request_text: str | None,
    ready_text: str | None,
    package_meta: tuple[int, str] | None,
    policy: LocalPolicy,
    expected_request_id: str | None = None,
    request_bytes: bytes | None = None,
) -> ValidationResult:
    """package_meta = (size_bytes, sha256) of the bytes actually downloaded,
    or None if the package has not been downloaded yet.

    expected_request_id is the name of the requests/<id>/ folder the files
    were read from; the REQUEST must name itself the same way.

    request_bytes are the stored bytes of the REQUEST; READY.request_sha256 is
    checked against them, never against a re-encoded copy of the text."""

    if request_text is None:
        return _wait("no REQUEST file in this requests/<id>/ folder yet")

    try:
        req = parse_front_matter(request_text)
    except FrontMatterError as exc:
        return _conflict(f"malformed REQUEST front matter: {exc}")

    if req.get("schema") != REQUEST_SCHEMA:
        return _reject(f"unknown/missing REQUEST schema: {req.get('schema')!r}")
    if req.get("state") in PLACEHOLDER_STATES:
        return _reject("REQUEST state is DRAFT_EXAMPLE (template, not a real request)")
    missing = [f for f in REQUIRED_REQUEST_FIELDS if _is_placeholder(req.get(f))]
    if missing:
        return _reject(f"REQUEST has placeholder/missing fields: {missing}")

    # request_id / request_revision become local file names and remote folder
    # names, so only a plain name is accepted ("..\\x", "a/b", spaces: rejected).
    for key in ("request_id", "request_revision"):
        if not SAFE_NAME.fullmatch(str(req[key])):
            return _reject(f"REQUEST {key} is not a plain name ([A-Za-z0-9._-], max 128, starts alphanumeric): {str(req[key])[:60]!r}")
    if expected_request_id is not None and str(req["request_id"]) != expected_request_id:
        return _reject(
            f"REQUEST request_id {str(req['request_id'])!r} does not match its folder requests/{expected_request_id}/"
        )

    if ready_text is None:
        return _wait("REQUEST present but no matching READY yet")

    try:
        ready = parse_front_matter(ready_text)
    except FrontMatterError as exc:
        return _conflict(f"malformed READY front matter: {exc}")

    if ready.get("schema") != READY_SCHEMA:
        return _reject(f"unknown/missing READY schema: {ready.get('schema')!r}")
    if ready.get("state") in PLACEHOLDER_STATES:
        return _reject("READY state is DRAFT_EXAMPLE (template, not a real READY)")
    missing = [f for f in REQUIRED_READY_FIELDS if _is_placeholder(ready.get(f))]
    if missing:
        return _reject(f"READY has placeholder/missing fields: {missing}")

    request_id = str(req["request_id"])
    request_revision = str(req["request_revision"])

    if str(ready["request_id"]) != request_id or str(ready["request_revision"]) != request_revision:
        return _conflict("READY request_id/request_revision does not match REQUEST")
    if str(ready["package_sha256"]) != str(req["package_sha256"]):
        return _conflict("READY package_sha256 does not match REQUEST package_sha256")
    if str(ready["baseline_id"]) != policy.active_baseline_id:
        return _conflict(
            f"READY baseline_id {ready['baseline_id']!r} != active baseline {policy.active_baseline_id!r}"
        )

    raw_request = request_bytes if request_bytes is not None else request_text.encode("utf-8")
    actual_request_sha256 = hashlib.sha256(raw_request).hexdigest()
    if str(ready["request_sha256"]) != actual_request_sha256:
        return _conflict("READY request_sha256 does not match actual REQUEST bytes (changed after READY was pinned)")

    package_sha256 = str(req["package_sha256"])

    if not _safe_remote_path(str(req["package_path"]), policy.approved_package_prefixes, suffix=".zip"):
        return _reject(f"package_path is not a .zip under an approved packages/ folder: {req['package_path']!r}")

    for ref in req.get("knowledge_refs") or []:
        path = ref.get("path") if isinstance(ref, dict) else None
        sha = ref.get("sha256") if isinstance(ref, dict) else None
        if not path or not _safe_remote_path(path, policy.approved_knowledge_prefixes):
            return _reject(f"knowledge_refs path not under an approved prefix: {path!r}")
        if _is_placeholder(sha):
            return _reject(f"knowledge_refs sha256 is a placeholder for {path!r}")
        if not re.fullmatch(r"[0-9a-f]{64}", str(sha).strip().lower()):
            return _reject(f"knowledge_refs sha256 is not a 64-character hex digest for {path!r}")

    if str(req["run_policy_ref"]) not in policy.known_run_policy_refs:
        return _reject(f"run_policy_ref not locally registered: {req['run_policy_ref']!r}")

    processing_key = f"{request_id}|{request_revision}|{package_sha256}|{policy.local_policy_revision}"

    if package_meta is None:
        return ValidationResult(
            outcome=ValidationOutcome.WAIT_INPUT,
            reason="REQUEST+READY valid but package not downloaded yet",
            processing_key=processing_key,
            request_id=request_id,
            request_revision=request_revision,
            package_sha256=package_sha256,
            package_path=str(req["package_path"]),
            fields={"request": req, "ready": ready, "request_body": front_matter_body(request_text)},
            needs_package_download=True,
        )

    size, sha = package_meta
    if int(req["package_size_bytes"]) != size or package_sha256 != sha:
        return _conflict(
            f"downloaded package size/sha256 mismatch: expected ({req['package_size_bytes']}, {package_sha256}), "
            f"got ({size}, {sha})"
        )

    return ValidationResult(
        outcome=ValidationOutcome.VALIDATED,
        reason="ok",
        processing_key=processing_key,
        request_id=request_id,
        request_revision=request_revision,
        package_sha256=package_sha256,
        package_path=str(req["package_path"]),
        fields={"request": req, "ready": ready, "request_body": front_matter_body(request_text)},
    )
