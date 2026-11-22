#!/usr/bin/env python3
"""CoWork P1/P2: bounded, read-only context and evidence relationships.

No model invocation, network access, disk writes, private-to-public exports, or
cached state. Local PRIVATE checkout only. The output is NOT for publication.
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import subprocess
from itertools import islice
from pathlib import Path, PureWindowsPath

ROUTES = {
    "collab": ("COWORK-DROPBOX-TO-GITHUB-MIGRATION", ("리뷰", "claude", "watcher", "협업", "live", "provider")),
    "auto": ("COWORK-AUTO-APPROVAL-20261115-001", ("자동 승인", "보호 위임", "정책", "usd", "금액", "서명", "승인")),
    "skill": ("COWORK-SKILL-DISCOVERY-20261112-001", ("스킬", "skill", "zip", "버전", "배포", "맥락", "컨텍스트")),
    "dashboard": ("COWORK-GITHUB-DASHBOARD-20261111-001", ("대시보드", "dashboard", "화면", "가독성", "ui")),
    "execution": ("JOBLIST-NRTX-20261112-001", ("job", "linux", "mcp", "llm", "opencode", "실행", "분석")),
    "knowledge": ("L1-WORKSPACE-RAG-20261111-001", ("knowledge", "지식", "rag", "updater", "그룹")),
}
COMMIT = re.compile(r"[0-9a-f]{40}\Z")
REQ_ID = re.compile(r"REQ-[A-Z0-9-]{4,120}\Z")
WORK_ID = re.compile(r"[A-Z][A-Z0-9_-]{5,120}\Z")
MAX_READ = 256_000
REQUEST_TOKEN = re.compile(r"(?<![A-Z0-9-])REQ-[A-Z0-9-]+")
LOCAL_MD_LINK = re.compile(r"\]\(([^\s)]+\.md)(?:#[^\s)]*)?\)")
READ_ERRORS = (OSError, UnicodeError, RuntimeError)


class RequestScanIncomplete(ValueError):
    """A list-only caller must not mistake a partial scan for a complete one."""


class RequestScanLimitExceeded(RequestScanIncomplete):
    """The P2 request directory exceeded the bounded local scan limit."""


def choose(question: str, topic: str | None = None) -> tuple[str, str]:
    """Deterministic, observable topic router; fallback is context Work."""
    if topic:
        if topic not in ROUTES:
            raise ValueError("unknown topic")
        return topic, ROUTES[topic][0]
    q = question.lower()
    scored = [(sum(1 for word in terms if word in q), key) for key, (_, terms) in ROUTES.items()]
    best = max((s for s, _ in scored), default=0)
    if best == 0:
        return "skill", ROUTES["skill"][0]
    # Specific UX, Knowledge and auto-approval questions beat generic review/skill.
    for key in ("dashboard", "knowledge", "auto", "execution", "collab", "skill"):
        if (best, key) in scored:
            return key, ROUTES[key][0]
    raise AssertionError("topic routing")


def route_diagnostics(question: str, topic: str | None = None) -> dict:
    """Explain the legacy topic choice without changing its routing policy.

    Inferred single-Work selection is not proof of a matching user intent.
    """
    selected, _ = choose(question, topic)
    if topic:
        return {"state": "EXPLICIT_TOPIC", "selected_topic": selected,
                "candidate_topics": [selected], "requires_review": False}
    q = question.lower()
    matches = {key: [term for term in terms if term in q]
               for key, (_, terms) in ROUTES.items()}
    candidates = [key for key, terms in matches.items() if terms]
    if not candidates:
        state = "FALLBACK_UNVERIFIED"
    elif len(candidates) > 1:
        state = "MULTI_TOPIC_REVIEW"
    elif "그룹" in matches.get("knowledge", ()) and re.search(r"그룹[가-힣a-z0-9]", q):
        state = "SUBSTRING_MATCH_REVIEW"
    else:
        state = "SINGLE_TOPIC_MATCH"
    return {"state": state, "selected_topic": selected,
            "candidate_topics": candidates, "requires_review": state != "SINGLE_TOPIC_MATCH"}


def safe_file(root: Path, rel: str, max_bytes: int = MAX_READ) -> Path | None:
    if not rel or rel.startswith("/") or "\\" in rel or Path(rel).is_absolute() or PureWindowsPath(rel).drive:
        return None
    parts = Path(rel).parts
    if any(p in ("..", ".", "") for p in parts):
        return None
    target = root / rel
    # Fail closed on symlinks in ALL path components.
    current = root
    for part in parts:
        current = current / part
        if current.is_symlink():
            return None
    if not target.is_file() or target.stat().st_size > max_bytes:
        return None
    try:
        if not target.resolve().is_relative_to(root.resolve()):
            return None
    except (OSError, RuntimeError):
        return None
    return target


def top_summary(content: str, max_chars: int = 3600) -> str:
    """Only current top heading, never the long historical tail."""
    lines = content.splitlines()
    start = next((i for i, s in enumerate(lines) if s.startswith("## ")), None)
    if start is None:
        return content[:max_chars]
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    return "\n".join(lines[start:end]).strip()[:max_chars]


def extract_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    stop = text.find("\n---\n", 4)
    if stop < 0 or stop > 4096:
        return {}
    result: dict[str, str] = {}
    for line in text[4:stop].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            if re.fullmatch(r"[a-z_]+", key.strip()):
                result[key.strip()] = value.strip().strip('"')
    return result


def _request_hints(root: Path, work_id: str, current: str, limit: int) -> list[str]:
    """Hints only: CURRENT and up to four directly linked same-Work documents.

    A hint never proves Work membership; REQUEST metadata is checked separately.
    There is no recursive traversal, network lookup, or new index.
    """
    ids: dict[str, None] = {}

    def add(text: str) -> None:
        for match in REQUEST_TOKEN.finditer(text):
            rid = match.group()
            if REQ_ID.fullmatch(rid):
                ids.setdefault(rid, None)
                if len(ids) >= limit:
                    break

    add(current)
    documents: set[str] = set()
    for match in LOCAL_MD_LINK.finditer(current):
        if len(ids) >= limit or len(documents) >= 4:
            break
        link = match.group(1)
        # Only same-Work relative links; use the unchanged F2 guard before I/O.
        if link.startswith("/") or "\\" in link or ":" in link or PureWindowsPath(link).drive or ".." in Path(link).parts:
            continue
        rel = f"collab/projects/{work_id}/{link}"
        if rel in documents:
            continue
        documents.add(rel)
        try:
            path = safe_file(root, rel)
            if path:
                add(path.read_text(encoding="utf-8"))
        except READ_ERRORS:
            # Hints are optional. Coverage is determined by the request scan.
            continue
    return list(ids)


def _relation_row(root: Path, rid: str, fm: dict[str, str], issues: list[dict]) -> dict:
    pkg = fm.get("package_path", "")
    package_match = re.fullmatch(r"/SKILL-COLLAB/packages/([A-Za-z0-9._-]+\.zip)", pkg)
    package_rel = f"collab/packages/{package_match.group(1)}" if package_match else ""
    files = {
        "request": f"collab/requests/{rid}/REQUEST.md",
        "source_pin": f"collab/requests/{rid}/SOURCE_PIN.json",
        "approval": f"collab/requests/{rid}/APPROVAL_SIG.json",
        "ready": f"collab/requests/{rid}/READY.md",
        "review": f"collab/reviews/{rid}/REVIEW_RESULT_1.md",
        "receipt": f"collab/receipts/{rid}/RECEIPT_1.md",
        "package": package_rel,
    }
    paths = {}
    for key, rel in files.items():
        try:
            paths[key] = "PRESENT_LOCAL_UNVALIDATED" if rel and safe_file(root, rel, max_bytes=100_000_000) else "NOT_FOUND_LOCAL"
        except READ_ERRORS as exc:
            paths[key] = "NOT_VERIFIED_LOCAL"
            issues.append({"request_id": rid, "file": key, "reason": type(exc).__name__})
    return {
        "request_id": rid,
        "request_revision": fm.get("request_revision", "UNKNOWN"),
        "package_sha256_claim": fm.get("package_sha256", "UNKNOWN"),
        "evidence_files": paths,
        "execution_verdict": "NOT_INFERRED_FROM_FILES",
    }


def _scan_relations(root: Path, work_id: str, max_requests: int = 200, current: str = "") -> dict:
    """Keep metadata-matched relationships within a bounded local file scan."""
    if not WORK_ID.fullmatch(work_id) or max_requests < 1:
        raise ValueError("invalid Work or request scan limit")
    answer: list[dict] = []
    issues: list[dict] = []
    checked: set[str] = set()
    limit_exceeded = False

    def inspect(rid: str) -> bool:
        nonlocal limit_exceeded
        if rid in checked or not REQ_ID.fullmatch(rid):
            return True
        if len(checked) >= max_requests:
            limit_exceeded = True
            return False
        checked.add(rid)
        try:
            path = safe_file(root, f"collab/requests/{rid}/REQUEST.md")
            if not path:
                issues.append({"request_id": rid, "reason": "REQUEST_NOT_VERIFIED"})
                return True
            fm = extract_frontmatter(path.read_text(encoding="utf-8"))
            if not WORK_ID.fullmatch(fm.get("work_id", "")):
                issues.append({"request_id": rid, "reason": "REQUEST_METADATA_NOT_VERIFIED"})
            elif fm["work_id"] == work_id:
                answer.append(_relation_row(root, rid, fm, issues))
        except READ_ERRORS as exc:
            issues.append({"request_id": rid, "reason": type(exc).__name__})
        return True

    priority = _request_hints(root, work_id, current, max_requests)
    for rid in priority:
        inspect(rid)
    try:
        request_dir = root / "collab" / "requests"
        if (root / "collab").is_symlink() or request_dir.is_symlink() or not request_dir.is_dir():
            issues.append({"reason": "REQUEST_DIRECTORY_NOT_VERIFIED"})
        else:
            # Only this bounded prefix is sorted. It is never claimed exhaustive
            # when more entries exist; priority hints share the inspection budget.
            candidates = sorted(islice(request_dir.glob("REQ-*"), max_requests + 1))
            limit_exceeded = len(candidates) > max_requests
            for folder in candidates:
                if not inspect(folder.name):
                    break
    except READ_ERRORS as exc:
        issues.append({"reason": "REQUEST_DIRECTORY_NOT_VERIFIED", "error": type(exc).__name__})
    complete = not limit_exceeded and not issues
    state = ("RELATIONS_SCAN_LIMIT_EXCEEDED" if limit_exceeded else
             "RELATIONS_SCAN_INCOMPLETE" if not complete else "LOCAL_FILE_PRESENCE_UNVALIDATED")
    return {
        "relations": answer,
        "relations_state": state,
        "relations_scan": {
            "complete": complete, "checked_requests": len(checked),
            "request_limit": max_requests, "priority_requests": len(priority),
            "limit_exceeded": limit_exceeded, "issues": issues,
        },
    }


def related(root: Path, work_id: str, max_requests: int = 200) -> list[dict]:
    """Legacy strict list API. Use snapshot() for partial results and diagnostics."""
    result = _scan_relations(root, work_id, max_requests)
    if result["relations_scan"]["limit_exceeded"]:
        raise RequestScanLimitExceeded("request scan limit exceeded")
    if not result["relations_scan"]["complete"]:
        raise RequestScanIncomplete("request scan incomplete")
    return result["relations"]


def diff_summary(root: Path, relative: str, current: str, base_commit: str | None) -> dict:
    if base_commit is None:
        return {"state": "NO_BASELINE", "changes": []}
    if not COMMIT.fullmatch(base_commit):
        return {"state": "INVALID_COMMIT", "changes": []}
    try:
        old = subprocess.run(
            ["git", "-C", str(root), "show", base_commit + ":" + relative],
            capture_output=True, check=False, timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return {"state": "BASELINE_NOT_VERIFIED", "changes": []}
    if old.returncode != 0 or len(old.stdout) > MAX_READ:
        return {"state": "BASELINE_NOT_VERIFIED", "changes": []}
    try:
        before = top_summary(old.stdout.decode("utf-8"))
    except UnicodeError:
        return {"state": "BASELINE_NOT_VERIFIED", "changes": []}
    after = top_summary(current)
    lines = list(difflib.unified_diff(before.splitlines(), after.splitlines(), lineterm=""))
    return {"state": "LOCAL_TEXT_DIFF_ONLY", "changes": lines[:20], "truncated": len(lines) > 20}


def snapshot(root: Path, question: str, topic: str | None = None,
             baseline_commit: str | None = None) -> dict:
    key, work = choose(question, topic)
    route_info = route_diagnostics(question, topic)
    if not WORK_ID.fullmatch(work):
        raise ValueError("invalid selected work")
    rel = f"collab/projects/{work}/CURRENT.md"
    try:
        target = safe_file(root, rel)
        contents = target.read_text(encoding="utf-8") if target else None
    except READ_ERRORS:
        contents = None
    if contents is None:
        return {
            "topic": key, "work_id": work, "state": "CURRENT_NOT_VERIFIED",
            "routing": route_info, "source_path": rel, "evidence": [],
            "host_execution": "NOT_VERIFIED",
        }
    summary = top_summary(contents)
    summary_truncated = len(top_summary(contents, max_chars=MAX_READ)) > len(summary)
    relation_data = _scan_relations(root, work, current=contents)
    return {
        "topic": key, "work_id": work, "routing": route_info,
        "state": "LOCAL_CURRENT_READ_ONLY",
        "source_path": rel,
        "summary": summary, "summary_truncated": summary_truncated,
        **relation_data,
        "delta": diff_summary(root, rel, contents, baseline_commit),
        "host_execution": "NOT_VERIFIED_BY_LOCAL_FILES",
        "warning": (
            "Document/REQUEST/READY existence is not independent review, LIVE host, Linux execution or group publication proof."
            + (" P2 relations are incomplete and NOT_VERIFIED; retained rows are partial. An empty list does not prove no related requests."
               if not relation_data["relations_scan"]["complete"] else "")
            + (" Topic routing requires review; selected Work may not match the question."
               if route_info["requires_review"] else "")
            + (" CURRENT top section is truncated; inspect narrower evidence."
               if summary_truncated else "")
        ),
    }


def main() -> None:
    p = argparse.ArgumentParser(description="PRIVATE CoWork P1/P2 scoped context, read-only")
    p.add_argument("--root", type=Path, default=Path("."))
    p.add_argument("--question", required=True, help="What information is needed?")
    p.add_argument("--topic", choices=sorted(ROUTES))
    p.add_argument("--baseline-commit", help="Optional pinned 40-hex prior Git commit")
    args = p.parse_args()
    print(json.dumps(snapshot(args.root.resolve(), args.question, args.topic, args.baseline_commit),
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
