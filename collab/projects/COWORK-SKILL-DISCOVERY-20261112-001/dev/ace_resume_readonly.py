"""Read-only ACE latest-decision candidate from *authenticated* existing Work events.

Does not grant approval, mutate Kernel, or invent an event schema. Existing
events lacking scope, original sequence and independent origin/authority
checks fail closed to HOLD. Callers may review the existing Work normally.
"""
from __future__ import annotations
from typing import Any, Mapping, Sequence


def select_latest_candidate(events: Sequence[Mapping[str, Any]] | None, *,
                            work_id: str, scope: str, subject: str) -> dict[str, Any]:
    if not work_id or not scope or not subject:
        return {"status": "HOLD", "reason": "WORK_SCOPE_NOT_PINNED", "approval_applied": False}
    if not isinstance(events, (tuple, list)):
        return {"status": "HOLD", "reason": "RAW_DECISIONS_UNAVAILABLE", "approval_applied": False}
    matching = []
    for item in events:
        if not isinstance(item, Mapping):
            continue
        # Only explicitly matched entries in the original journal, never brief
        # summaries (which may lack ref/date/original ordering).
        if (item.get("work_id") == work_id and item.get("scope") == scope
                and item.get("subject") == subject and item.get("type") in ("DECISION", "CORRECTION", "REVOKE")):
            matching.append(item)
    if not matching:
        return {"status": "HOLD", "reason": "NO_PINNED_ORIGINAL_DECISION", "approval_applied": False}
    if any(item.get("origin_verified") is not True
           or item.get("authority_verified") is not True
           or type(item.get("append_index")) is not int
           or item["append_index"] < 0
           or not isinstance(item.get("ref"), str) or not item["ref"]
           for item in matching):
        return {"status": "HOLD", "reason": "ORIGINAL_ORDER_OR_AUTHORITY_UNVERIFIED", "approval_applied": False}
    indexes = [item["append_index"] for item in matching]
    if len(indexes) != len(set(indexes)):
        return {"status": "HOLD", "reason": "AMBIGUOUS_APPEND_ORDER", "approval_applied": False}
    current = max(matching, key=lambda item: item["append_index"])
    return {"status": "REVOKED_CANDIDATE" if current["type"] == "REVOKE"
            else "SELECTED_CANDIDATE", "decision_ref": current["ref"],
            "append_index": current["append_index"], "approval_applied": False}
