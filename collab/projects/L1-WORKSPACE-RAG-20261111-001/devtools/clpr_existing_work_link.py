"""Conservative CL/PR source-reference linking to an existing Kernel Work.

No Work creation, no evidence registration, no analysis claims, no Knowledge writes.
This module is a development candidate until whole-skill regression and E3 pass.
"""
from __future__ import annotations

from copy import deepcopy

from .issue_brief import (
    _CLPR_P4_REF,
    _CLPR_PR_REF,
    _CLPR_ISSUE_KEY,
    lookup_clpr_existing_work,
)


def _checked_refs(group: dict) -> list[tuple[str, str]]:
    if not isinstance(group, dict):
        raise ValueError("CLPR_GROUP_INVALID")
    jira = group.get("jira_keys", [])
    sources = group.get("source_refs", [])
    if not isinstance(jira, list) or not isinstance(sources, list) or not sources:
        raise ValueError("CLPR_GROUP_REFS_INVALID")
    result = set()
    for key in jira:
        if not isinstance(key, str) or not _CLPR_ISSUE_KEY.fullmatch(key):
            raise ValueError("CLPR_JIRA_INVALID")
        result.add(("jira", key))
    for ref in sources:
        if not isinstance(ref, str):
            raise ValueError("CLPR_SOURCE_REF_INVALID")
        if _CLPR_P4_REF.fullmatch(ref):
            result.add(("p4_cl", ref))
        elif _CLPR_PR_REF.fullmatch(ref) and ref == ref.lower():
            result.add(("github_pr", ref))
        else:
            raise ValueError("CLPR_SOURCE_REF_INVALID")
    return sorted(result)


def link_clpr_existing_work(plan: dict, kernel, *, issue_identity: str, commit: bool = False) -> dict:
    """Link source refs to one unambiguous *existing* Work on explicit commit.

    Does not create Work or record Evidence; errors fail closed before any write.
    Caller must serialize writers for the ledger. The Kernel reference API provides
    per-Work locks, not a cross-Work global uniqueness lock.
    """
    if not isinstance(commit, bool):
        raise ValueError("CLPR_COMMIT_MUST_BE_BOOLEAN")
    if not isinstance(plan, dict) or plan.get("action") != "CLPR_ISSUE_CANDIDATE_PLAN":
        raise ValueError("CLPR_PLAN_INVALID")
    if plan.get("read_only") is not True or not isinstance(plan.get("issue_cases"), list):
        raise ValueError("CLPR_PLAN_NOT_TRUSTED")
    if not isinstance(issue_identity, str) or not issue_identity:
        raise ValueError("CLPR_IDENTITY_REQUIRED")

    # Recheck the whole plan, not just the chosen group. No unsupported reference
    # should be accepted even when another group is selected.
    for group in plan["issue_cases"]:
        _checked_refs(group)
    selected = [g for g in plan["issue_cases"] if g.get("issue_identity") == issue_identity]
    if len(selected) != 1:
        raise ValueError("CLPR_GROUP_NOT_UNIQUE")

    checked = deepcopy(plan)
    lookup_clpr_existing_work(checked, kernel)
    group = next(g for g in checked["issue_cases"] if g["issue_identity"] == issue_identity)
    if group.get("existing_work_lookup") != "UNIQUE_CANDIDATE" or len(group.get("work_candidates", [])) != 1:
        return {"ok": False, "action": "LINK_BLOCKED", "reason": group.get("existing_work_lookup", "UNKNOWN"),
                "writes": 0, "new_work_created": False, "evidence_registration": "NOT_RUN"}
    work_id = group["work_candidates"][0]
    refs = _checked_refs(group)

    # WorkReference.add is individually idempotent but lacks cross-Work uniqueness.
    # Refuse any partial result, match on another Work or non-exact match type.
    missing = []
    for ref_type, value in refs:
        found = kernel.work_reference_find(value, include_archived=True, limit=200)
        matches = found.get("matches") or []
        if not isinstance(matches, list) or found.get("count", 0) > len(matches):
            return {"ok": False, "action": "LINK_BLOCKED", "reason": "PARTIAL_LOOKUP",
                    "writes": 0, "new_work_created": False}
        exact = [row for row in matches if row.get("match_type") in ("jira", "external_ref")]
        if any(row.get("work_id") != work_id for row in exact):
            return {"ok": False, "action": "LINK_BLOCKED", "reason": "CONFLICT_MULTIPLE_WORKS",
                    "writes": 0, "new_work_created": False}
        if not any(row.get("work_id") == work_id for row in exact):
            missing.append((ref_type, value))

    if not commit:
        return {"ok": True, "action": "LINK_PREVIEW", "work_id": work_id, "writes": 0,
                "would_add": len(missing), "new_work_created": False,
                "workspace_written": False, "evidence_registration": "NOT_RUN"}

    writes = 0
    for ref_type, value in missing:
        result = kernel.work_reference_add(work_id, ref_type, value)
        if result.get("ok") is not True:
            raise RuntimeError("CLPR_REF_WRITE_FAILED")
        if not result.get("already_present"):
            writes += 1
        check = kernel.work_reference_find(value, include_archived=True, limit=200)
        exact = [row for row in check.get("matches", []) if row.get("match_type") in ("jira", "external_ref")]
        if check.get("count", 0) > len(check.get("matches", [])) or {row["work_id"] for row in exact} != {work_id}:
            raise RuntimeError("CLPR_REF_READBACK_UNVERIFIED")
    return {"ok": True, "action": "LINK_COMMITTED", "work_id": work_id, "writes": writes,
            "new_work_created": False, "workspace_written": bool(writes),
            "evidence_registration": "NOT_RUN", "analysis_confirmed": False,
            "knowledge_published": False}
