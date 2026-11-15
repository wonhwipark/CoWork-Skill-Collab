"""CoWork bounded auto-signing preflight prototype (offline, NO I/O).

The returned ALLOW result is NOT a signature or a review approval.
Windows must do durable atomic reservation, GitHub raw-byte verification,
existing Ed25519 signing and original Watcher verification/dispatch.
"""
from dataclasses import dataclass
import re

_HASH64 = re.compile(r"[0-9a-f]{64}\Z")
_SHA40 = re.compile(r"[0-9a-f]{40}\Z")


@dataclass(frozen=True)
class Delegation:
    enabled: bool
    repo_id: str
    branch: str
    projects: frozenset[str]
    skills: frozenset[str]
    expires_at: int
    earliest_request_at: int
    max_request_cents: int = 100
    max_day_calls: int = 2
    max_day_cents: int = 300
    max_month_cents: int = 1000


@dataclass(frozen=True)
class Candidate:
    request_id: str
    revision: int
    project: str
    skill: str
    repo_id: str
    branch: str
    created_at: int
    commit_a: str
    request_sha256: str
    zip_sha256: str
    policy: str
    estimated_cents: int
    max_calls: int
    attempt: int
    state: str = "REQUESTED"


@dataclass(frozen=True)
class Evidence:
    now: int
    pins_verified: bool
    bytes_and_crc_verified: bool
    signer_and_trust_root_valid: bool
    prior_state: str
    day_calls_used_or_reserved: int
    day_cents_used_or_reserved: int
    month_cents_used_or_reserved: int
    atomic_claim_available: bool


def assess(d: Delegation, c: Candidate, e: Evidence) -> tuple[bool, str]:
    """Pure first gate only. Never produces keys, APPROVAL_SIG or READY."""
    if not d.enabled:
        return False, "DISABLED"
    if e.now >= d.expires_at or d.expires_at <= d.earliest_request_at:
        return False, "DELEGATION_EXPIRED"
    if c.created_at < d.earliest_request_at or c.created_at > e.now:
        return False, "RETROACTIVE_OR_FUTURE_REQUEST"
    if c.repo_id != d.repo_id or c.branch != d.branch:
        return False, "REPOSITORY_OR_BRANCH"
    if not d.projects or not d.skills or c.project not in d.projects or c.skill not in d.skills:
        return False, "SCOPE"
    if c.policy != "POLICY-STATIC-V1" or c.max_calls != 1 or c.attempt != 1:
        return False, "REVIEW_POLICY"
    if c.state not in ("REQUESTED", "SUBMITTED") or not c.request_id or c.revision < 1:
        return False, "REQUEST_FORMAT"
    if not _SHA40.fullmatch(c.commit_a) or not _HASH64.fullmatch(c.request_sha256) or not _HASH64.fullmatch(c.zip_sha256):
        return False, "INVALID_PIN_FORMAT"
    if c.estimated_cents < 1 or c.estimated_cents > d.max_request_cents:
        return False, "PER_REQUEST_COST"
    if (d.max_request_cents > 100 or d.max_day_calls < 1 or d.max_day_calls > 2
            or d.max_day_cents > 300 or d.max_month_cents > 1000):
        return False, "UNSUPPORTED_DELEGATION_LIMIT"
    if e.prior_state != "NEW":
        return False, "DUPLICATE_OR_UNCERTAIN"
    if not (e.pins_verified and e.bytes_and_crc_verified and e.signer_and_trust_root_valid):
        return False, "INPUT_OR_TRUST"
    if not e.atomic_claim_available:
        return False, "NO_ATOMIC_CLAIM"
    if e.day_calls_used_or_reserved >= d.max_day_calls:
        return False, "DAY_CALL_LIMIT"
    if e.day_cents_used_or_reserved + c.estimated_cents > d.max_day_cents:
        return False, "DAY_COST_LIMIT"
    if e.month_cents_used_or_reserved + c.estimated_cents > d.max_month_cents:
        return False, "MONTH_COST_LIMIT"
    return True, "ALLOW_ATOMIC_CLAIM_THEN_EXISTING_SIGNER_ONLY"
