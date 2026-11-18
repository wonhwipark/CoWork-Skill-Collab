"""Pure read-only ACE/PEC-HOP/ACON contract candidate for existing skills.

No filesystem, network, credential, Git, model or Work writes. This module is
NOT a deployed skill, an authorization engine, or proof of installed behavior.
Caller must obtain and verify source, authority, revision and access rights.
"""
from __future__ import annotations

from hashlib import sha256
from typing import Any, Mapping, Sequence


def ace_decision_candidate(records: Sequence[Mapping[str, Any]], *, work_id: str,
                           scope: str, subject: str) -> dict[str, Any]:
    """Select a candidate from externally authenticated, ordered Work decisions.

    Never grants access or authorization: every matching record requires
    'authority_verified' and 'origin_verified' from an independent caller.
    Missing/ambiguous order or authorization fails closed to HOLD.
    """
    if not work_id or not scope or not subject:
        return {"status": "HOLD", "reason": "SCOPE_UNVERIFIED"}
    selected = [r for r in records if r.get("work_id") == work_id
                and r.get("scope") == scope and r.get("subject") == subject]
    if not selected:
        return {"status": "HOLD", "reason": "NO_MATCHING_DECISION"}
    if any(r.get("authority_verified") is not True or r.get("origin_verified") is not True
           or type(r.get("append_index")) is not int or r["append_index"] < 0
           or not isinstance(r.get("decision_ref"), str) or not r["decision_ref"]
           or r.get("kind") not in ("SELECT", "REVOKE") for r in selected):
        return {"status": "HOLD", "reason": "DECISION_PROVENANCE_OR_AUTHORITY_UNVERIFIED"}
    seen = [r["append_index"] for r in selected]
    if len(set(seen)) != len(seen):
        return {"status": "HOLD", "reason": "AMBIGUOUS_APPEND_ORDER"}
    final = max(selected, key=lambda r: r["append_index"])
    return {"status": "REVOKED_CANDIDATE" if final["kind"] == "REVOKE"
            else "SELECTED_CANDIDATE", "decision_ref": final["decision_ref"],
            "append_index": final["append_index"], "authorization_applied": False}


def pec_verify_excerpt(*, source_bytes: bytes | None, excerpt_bytes: bytes | None,
                       source_revision: str, expected_revision: str,
                       source_sha256: str, byte_offset: int | None,
                       byte_length: int | None, access_verified: bool) -> dict[str, Any]:
    """Verify exact raw bytes; an entire-file digest alone is insufficient."""
    if access_verified is not True or not source_revision or source_revision != expected_revision:
        return {"status": "HOLD", "reason": "ACCESS_OR_REVISION_UNVERIFIED"}
    if not isinstance(source_bytes, bytes) or not isinstance(excerpt_bytes, bytes):
        return {"status": "HOLD", "reason": "RAW_BYTES_UNAVAILABLE"}
    if type(byte_offset) is not int or type(byte_length) is not int or byte_offset < 0 or byte_length < 0:
        return {"status": "HOLD", "reason": "BYTE_RANGE_UNVERIFIED"}
    if byte_offset + byte_length > len(source_bytes):
        return {"status": "HOLD", "reason": "BYTE_RANGE_INVALID"}
    if not isinstance(source_sha256, str) or len(source_sha256) != 64:
        return {"status": "HOLD", "reason": "FILE_DIGEST_UNVERIFIED"}
    if sha256(source_bytes).hexdigest() != source_sha256:
        return {"status": "FAIL", "reason": "PINNED_SOURCE_DIGEST_MISMATCH"}
    actual = source_bytes[byte_offset:byte_offset + byte_length]
    if len(excerpt_bytes) != byte_length or sha256(actual).digest() != sha256(excerpt_bytes).digest():
        return {"status": "FAIL", "reason": "EXCERPT_BYTES_MISMATCH"}
    return {"status": "PASS", "source_sha256": source_sha256,
            "excerpt_sha256": sha256(actual).hexdigest(), "byte_length": byte_length}


def acon_compare_existing_results(*, baseline: Sequence[Mapping[str, Any]],
                                  compressed: Sequence[Mapping[str, Any]],
                                  pinned_model_config: str, pinned_source_revision: str,
                                  evidence_ids: Sequence[str]) -> dict[str, Any]:
    """Compare supplied, already-run evaluations; never calls a model.

    A 3+3 minimum is a screening rule, not a statistically significant proof
    of compression causality. No new experiments are triggered.
    """
    if len(baseline) < 3 or len(compressed) < 3:
        return {"status": "NOT_RUN", "reason": "INSUFFICIENT_EXISTING_REPETITIONS"}
    if not pinned_model_config or not pinned_source_revision or not evidence_ids \
       or any(not isinstance(i, str) or not i for i in evidence_ids):
        return {"status": "HOLD", "reason": "PIN_OR_EVIDENCE_UNVERIFIED"}
    required = set(evidence_ids)
    all_rows = list(baseline) + list(compressed)
    if any(r.get("model_config") != pinned_model_config
           or r.get("source_revision") != pinned_source_revision
           or type(r.get("passed")) is not bool
           or not isinstance(r.get("retained_evidence_ids"), (tuple, list))
           or any(not isinstance(v, str) for v in r["retained_evidence_ids"])
           for r in all_rows):
        return {"status": "HOLD", "reason": "ENVIRONMENT_OR_RESULT_UNVERIFIED"}
    missing = sorted(required - set.intersection(*(set(r["retained_evidence_ids"]) for r in compressed)))
    baseline_passes = sum(r["passed"] for r in baseline)
    compressed_passes = sum(r["passed"] for r in compressed)
    return {"status": "REVIEW_NEEDED", "baseline_passes": baseline_passes,
            "baseline_runs": len(baseline), "compressed_passes": compressed_passes,
            "compressed_runs": len(compressed), "evidence_missing_from_all_compressed_runs": missing,
            "causality_proven": False}
