#!/usr/bin/env python3
"""CoWork P1/P2: bounded, read-only context and evidence relationships.

No model invocation, network access, disk writes, private-to-public exports, or
cached state. Authorized local checkout only. The output is NOT for publication.
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
    "knowledge": ("L1-WORKSPACE-RAG-20261111-001", ("knowledge", "지식", "rag", "updater", "그룹 지식")),
    "viewer": ("L1-WORKSPACE-RAG-20261111-001", ("viewer", "뷰어", "목차", "오늘의 업무")),
    "nr_analysis": ("NR-L1TX-CODE-ANALYSIS-20261115-001", ("nr l1 tx", "nr l1tx", "init rach", "ul scell")),
    "smoke": ("JOBLIST-SMOKE-20261114-001", ("무모델", "모델 호출 없는", "운송", "smoke")),
    "scope": ("L1-CHANNEL-KNOWLEDGE-SCOPE-20261113-001", ("담당 모듈", "담당 범위", "분류 검토")),
    "issue": ("ISSUE-ANALYZER-20261114-001", ("issue analyzer", "이슈 분석기")),
}
COMMIT = re.compile(r"[0-9a-f]{40}\Z")
REQ_ID = re.compile(r"REQ-[A-Z0-9-]{4,120}\Z")
WORK_ID = re.compile(r"[A-Z][A-Z0-9_-]{5,120}\Z")
MAX_READ = 256_000
MAX_CURRENT_READ = 1_048_576  # CURRENT only; REQUEST and linked evidence retain MAX_READ
CURRENT_REMOTE_BASE = "https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/"
REQUEST_TOKEN = re.compile(r"(?<![A-Z0-9-])REQ-[A-Z0-9-]+")
LOCAL_MD_LINK = re.compile(r"\]\(([^\s)]+\.md)(?:#[^\s)]*)?\)")
READ_ERRORS = (OSError, UnicodeError, RuntimeError)


class RequestScanIncomplete(ValueError):
    """A list-only caller must not mistake a partial scan for a complete one."""


class RequestScanLimitExceeded(RequestScanIncomplete):
    """The P2 request directory exceeded the bounded local scan limit."""


def _specific_routes(q: str) -> list[str]:
    """Strong, bounded intent cues before generic words such as '화면' or 'job'."""
    patterns = (
        ("viewer", r"viewer|뷰어|목차\s*(?:폭|너비)|문서\s*탐색|오늘의\s*업무"),
        ("nr_analysis", r"nr[\s_-]*l1[\s_-]*tx|init[\s_-]*rach|ul[\s_-]*scell"),
        ("smoke", r"무모델|모델\s*호출\s*없는|모델\s*없는|smoke|job\s*운송|worker\s*도달"),
        ("scope", r"담당\s*(?:모듈|범위)|(?:procedure|프로시저).*(?:feature|피처).*분류|분류\s*검토"),
        ("issue", r"issue[\s_-]*analyzer|이슈\s*분석기"),
    )
    return [key for key, pattern in patterns if re.search(pattern, q)]


def _term_matches(q: str, terms: tuple[str, ...]) -> list[str]:
    # Avoid matching an English word inside another word (and '그룹웨어' as 그룹).
    return [term for term in terms
            if (re.search(r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])", q)
                if term.isascii() and term.replace(" ", "").isalnum()
                else term in q)]


def choose(question: str, topic: str | None = None) -> tuple[str, str]:
    """Deterministic router; an explicit topic always overrides inference."""
    if topic:
        if topic not in ROUTES:
            raise ValueError("unknown topic")
        return topic, ROUTES[topic][0]
    q = question.lower()
    strong = _specific_routes(q)
    if strong:
        return strong[0], ROUTES[strong[0]][0]
    scored = [(len(_term_matches(q, terms)), key) for key, (_, terms) in ROUTES.items()]
    best = max((score for score, _ in scored), default=0)
    if best == 0:
        return "skill", ROUTES["skill"][0]
    for key in ("auto", "knowledge", "dashboard", "execution", "collab", "skill",
                "scope", "issue", "smoke", "nr_analysis", "viewer"):
        if (best, key) in scored:
            return key, ROUTES[key][0]
    raise AssertionError("topic routing")


def route_diagnostics(question: str, topic: str | None = None) -> dict:
    """Surface conflicting candidates; never equate keyword selection with proof."""
    selected, _ = choose(question, topic)
    if topic:
        return {"state": "EXPLICIT_TOPIC", "selected_topic": selected,
                "candidate_topics": [selected], "requires_review": False}
    q = question.lower()
    matches = {key: _term_matches(q, terms) for key, (_, terms) in ROUTES.items()}
    strong = _specific_routes(q)
    candidates = [key for key, terms in matches.items() if terms]
    for key in strong:
        if key not in candidates:
            candidates.append(key)
    if strong:
        competing = [key for key in candidates if key not in strong and not (
            (key == "dashboard" and selected == "viewer" and "대시보드" not in q) or
            (key == "execution" and selected in ("nr_analysis", "smoke")
             and not re.search(r"진단|장애|registry", q)))]
        review = len(strong) > 1 or bool(competing)
        state = "MULTI_TOPIC_REVIEW" if review else "SPECIFIC_ROUTE_MATCH"
    elif not candidates:
        state, review = "FALLBACK_UNVERIFIED", True
    elif len(candidates) > 1:
        state, review = "MULTI_TOPIC_REVIEW", True
    else:
        state, review = "SINGLE_TOPIC_MATCH", False
    return {"state": state, "selected_topic": selected,
            "candidate_topics": candidates, "requires_review": review}


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


def question_section_summary(content: str, question: str,
                             max_chars: int = 3600) -> dict:
    """Pick a recent, question-relevant CURRENT section without historical tail scan.

    Inspect at most 48 newest H2 sections in a file already capped at 1 MiB.
    This is a heuristic pointer, not proof that the section is the latest result.
    """
    matches = list(islice(re.finditer(r"(?m)^## ", content), 49))
    if not matches:
        summary = content[:max_chars]
        return {"summary": summary, "summary_truncated": len(content) > len(summary),
                "summary_selection": "TOP_FALLBACK_UNVERIFIED",
                "summary_heading": "", "summary_section_index": -1}
    words = [word for word in re.findall(r"[a-z][a-z0-9_-]*|[가-힣]{2,}", question.lower())
             if word not in {"해줘", "확인", "이어줘", "찾아줘", "관련", "작업", "내용", "수정한"}]
    best_idx, best_score = 0, 0.0
    for idx, match in enumerate(matches[:48]):
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(content)
        section = content[match.start():end]
        heading = section.split("\n", 1)[0].lower()
        preview = section[:1800].lower()
        score = (sum(4 for word in words if word in heading) +
                 sum(1 for word in words if word not in heading and word in preview) -
                 idx * 0.12)
        if score > best_score:
            best_idx, best_score = idx, score
    start = matches[best_idx].start()
    end = matches[best_idx + 1].start() if best_idx + 1 < len(matches) else len(content)
    section = content[start:end].strip()
    summary = section[:max_chars]
    return {
        "summary": summary, "summary_truncated": len(section) > len(summary),
        "summary_selection": "QUESTION_SECTION_MATCH" if best_score >= 2 else "TOP_FALLBACK_UNVERIFIED",
        "summary_heading": section.split("\n", 1)[0],
        "summary_section_index": best_idx,
    }


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
    read_reason = "CURRENT_NOT_VERIFIED"
    try:
        target = safe_file(root, rel, max_bytes=MAX_CURRENT_READ)
        if target:
            with target.open("rb") as stream:
                data = stream.read(MAX_CURRENT_READ + 1)
            if len(data) > MAX_CURRENT_READ:
                contents = None
                read_reason = "CURRENT_READ_LIMIT_EXCEEDED"
            else:
                contents = data.decode("utf-8")
        else:
            contents = None
            read_reason = "CURRENT_MISSING_OR_OVER_LIMIT"
    except READ_ERRORS:
        contents = None
    if contents is None:
        return {
            "topic": key, "work_id": work, "state": "CURRENT_NOT_VERIFIED",
            "read_reason": read_reason, "routing": route_info, "source_path": rel,
            "source_url": CURRENT_REMOTE_BASE + rel,
            "evidence": [], "host_execution": "NOT_VERIFIED",
            "warning": "Local CURRENT is unavailable or over the bounded read limit; inspect source_url directly.",
        }
    section = question_section_summary(contents, question)
    relation_data = _scan_relations(root, work, current=contents)
    return {
        "topic": key, "work_id": work, "routing": route_info,
        "state": "LOCAL_CURRENT_READ_ONLY",
        "source_path": rel, "source_url": CURRENT_REMOTE_BASE + rel,
        "current_bytes": len(data),
        **section,
        **relation_data,
        "delta": diff_summary(root, rel, contents, baseline_commit),
        "host_execution": "NOT_VERIFIED_BY_LOCAL_FILES",
        "warning": (
            "Document/REQUEST/READY existence is not independent review, LIVE host, Linux execution or group publication proof."
            + (" P2 relations are incomplete and NOT_VERIFIED; retained rows are partial. An empty list does not prove no related requests."
               if not relation_data["relations_scan"]["complete"] else "")
            + (" Topic routing requires review; selected Work may not match the question."
               if route_info["requires_review"] else "")
            + (" CURRENT selected section is truncated; inspect source_url and narrower evidence."
               if section["summary_truncated"] else "")
            + (" Section selection is a heuristic or fallback; verify linked evidence."
               if section["summary_selection"] != "QUESTION_SECTION_MATCH" else "")
        ),
    }


def main() -> None:
    p = argparse.ArgumentParser(description="CoWork P1/P2 scoped local context, read-only")
    p.add_argument("--root", type=Path, default=Path("."))
    p.add_argument("--question", required=True, help="What information is needed?")
    p.add_argument("--topic", choices=sorted(ROUTES))
    p.add_argument("--baseline-commit", help="Optional pinned 40-hex prior Git commit")
    args = p.parse_args()
    print(json.dumps(snapshot(args.root.resolve(), args.question, args.topic, args.baseline_commit),
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
