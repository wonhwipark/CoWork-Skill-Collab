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
from pathlib import Path

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


def safe_file(root: Path, rel: str, max_bytes: int = MAX_READ) -> Path | None:
    if not rel or rel.startswith("/") or "\\" in rel:
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


def related(root: Path, work_id: str, max_requests: int = 200) -> list[dict]:
    """P2 links from pinned REQUEST metadata. File existence != executed review."""
    request_dir = root / "collab" / "requests"
    if request_dir.is_symlink() or not request_dir.is_dir():
        return []
    answer: list[dict] = []
    candidates = sorted(request_dir.glob("REQ-*"))
    if len(candidates) > max_requests:
        raise ValueError("request scan limit exceeded")
    for folder in candidates:
        rid = folder.name
        if not REQ_ID.fullmatch(rid) or folder.is_symlink() or not folder.is_dir():
            continue
        path = safe_file(root, f"collab/requests/{rid}/REQUEST.md")
        if not path:
            continue
        fm = extract_frontmatter(path.read_text(encoding="utf-8"))
        if fm.get("work_id") != work_id:
            continue
        pkg = fm.get("package_path", "")
        package_rel = ("collab/packages/" + pkg.rsplit("/", 1)[-1]) if pkg.startswith("/SKILL-COLLAB/packages/") and "/" in pkg else ""
        files = {
            "request": f"collab/requests/{rid}/REQUEST.md",
            "source_pin": f"collab/requests/{rid}/SOURCE_PIN.json",
            "approval": f"collab/requests/{rid}/APPROVAL_SIG.json",
            "ready": f"collab/requests/{rid}/READY.md",
            "review": f"collab/reviews/{rid}/REVIEW_RESULT_1.md",
            "receipt": f"collab/receipts/{rid}/RECEIPT_1.md",
        }
        paths = {key: ("PRESENT_LOCAL_UNVALIDATED" if safe_file(root, rel, max_bytes=100_000_000) else "NOT_FOUND_LOCAL") for key, rel in files.items()}
        paths["package"] = "PRESENT_LOCAL_UNVALIDATED" if package_rel and safe_file(root, package_rel, max_bytes=100_000_000) else "NOT_FOUND_LOCAL"
        answer.append({
            "request_id": rid,
            "request_revision": fm.get("request_revision", "UNKNOWN"),
            "package_sha256_claim": fm.get("package_sha256", "UNKNOWN"),
            "evidence_files": paths,
            "execution_verdict": "NOT_INFERRED_FROM_FILES",
        })
    return answer


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
    if not WORK_ID.fullmatch(work):
        raise ValueError("invalid selected work")
    rel = f"collab/projects/{work}/CURRENT.md"
    target = safe_file(root, rel)
    if not target:
        return {
            "topic": key, "work_id": work, "state": "CURRENT_NOT_VERIFIED",
            "source_path": rel, "evidence": [], "host_execution": "NOT_VERIFIED",
        }
    contents = target.read_text(encoding="utf-8")
    summary = top_summary(contents)
    return {
        "topic": key, "work_id": work,
        "state": "LOCAL_CURRENT_READ_ONLY",
        "source_path": rel,
        "summary": summary,
        "relations": related(root, work),
        "delta": diff_summary(root, rel, contents, baseline_commit),
        "host_execution": "NOT_VERIFIED_BY_LOCAL_FILES",
        "warning": "Document/REQUEST/READY existence is not independent review, LIVE host, Linux execution or group publication proof.",
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
