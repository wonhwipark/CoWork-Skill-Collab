"""PEC-HOP minimal evidence excerpt integrity; trusted producer must supply raw bytes.

No file, Git, P4, network, LLM or Knowledge access. This is a verifier, not
a source-authority or access-control verifier. Call only after host-side
source permissions and pinned revision have been independently checked.
"""
from __future__ import annotations
from hashlib import sha256
from hmac import compare_digest
from typing import Any, Mapping


def verify_excerpt(*, source_bytes: bytes | None, excerpt_bytes: bytes | None,
                   source_revision: str | None, expected_revision: str | None,
                   source_sha256: str | None, byte_offset: int | None,
                   byte_length: int | None, source_access_verified: bool = False) -> dict[str, Any]:
    if source_access_verified is not True:
        return {"status": "HOLD", "reason": "SOURCE_ACCESS_UNVERIFIED"}
    if not source_revision or not expected_revision or source_revision != expected_revision:
        return {"status": "HOLD", "reason": "SOURCE_REVISION_UNVERIFIED"}
    if type(source_bytes) is not bytes or type(excerpt_bytes) is not bytes:
        return {"status": "HOLD", "reason": "RAW_SOURCE_OR_EXCERPT_UNAVAILABLE"}
    if type(byte_offset) is not int or type(byte_length) is not int or byte_offset < 0 or byte_length < 1:
        return {"status": "HOLD", "reason": "BYTE_RANGE_UNVERIFIED"}
    if byte_offset + byte_length > len(source_bytes):
        return {"status": "HOLD", "reason": "BYTE_RANGE_OUT_OF_SOURCE"}
    if not isinstance(source_sha256, str) or len(source_sha256) != 64:
        return {"status": "HOLD", "reason": "PINNED_SHA256_UNVERIFIED"}
    actual_digest = sha256(source_bytes).hexdigest()
    if not compare_digest(actual_digest, source_sha256.lower()):
        return {"status": "FAIL", "reason": "SOURCE_SHA256_MISMATCH"}
    segment = source_bytes[byte_offset:byte_offset + byte_length]
    if not compare_digest(segment, excerpt_bytes):
        return {"status": "FAIL", "reason": "EXCERPT_RAW_BYTES_MISMATCH"}
    return {"status": "PASS", "source_sha256": actual_digest,
            "excerpt_sha256": sha256(segment).hexdigest(), "byte_offset": byte_offset,
            "byte_length": byte_length, "verified_source_revision": source_revision}


def verify_batch(claims: list[Mapping[str, Any]] | None) -> dict[str, Any]:
    """Opt-in data-only attachment for code-analyzer reuse validation.

    Never includes source or excerpt bytes in the result.
    """
    if not isinstance(claims, list) or not claims:
        return {"status": "HOLD", "reason": "NO_EXPLICIT_PEC_CLAIMS", "checks": []}
    checks = []
    fields = ("source_bytes", "excerpt_bytes", "source_revision", "expected_revision",
              "source_sha256", "byte_offset", "byte_length", "source_access_verified")
    for idx, claim in enumerate(claims):
        if not isinstance(claim, Mapping):
            result = {"status": "HOLD", "reason": "MALFORMED_CLAIM"}
        else:
            result = verify_excerpt(**{field: claim.get(field) for field in fields})
        checks.append({"index": idx, **result})
    status = ("FAIL" if any(c["status"] == "FAIL" for c in checks)
              else "PASS" if all(c["status"] == "PASS" for c in checks) else "HOLD")
    return {"status": status, "checks": checks, "writes": 0}
