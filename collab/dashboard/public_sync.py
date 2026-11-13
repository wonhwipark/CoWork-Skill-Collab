"""Publish ONLY public-safe, explicitly allowlisted CoWork status to L1Work Pages.

Private workflow computes this from PRIVATE dashboard state; only fixed public aliases,
controlled enum statuses and aggregate counts are emitted. No private strings, IDs,
links, next actions, reviewer receipts or secrets are copied into the output.

A separately configured, PUBLIC-L1Work-only fine-grained token is required to publish.
Run no external API for "prepare". Publish fails closed on malformed/stale data or HTTP error.
"""
from __future__ import annotations

import argparse
import base64
from datetime import datetime, timezone, timedelta
import json
import os
from pathlib import Path
import re
import urllib.error
import urllib.request

import generate

PUBLIC_REPO = "wonhwipark/L1Work"
PUBLIC_PATH = "docs/cowork-dashboard/status.json"
PUBLIC_SCHEMA = "COWORK_PUBLIC_STATUS_V1"
PRIVATE_SCHEMA = "COWORK_GITHUB_DASHBOARD_SHADOW_V4"
TOKEN_ENV = "COWORK_PUBLIC_DASHBOARD_WRITE_TOKEN"
KST = timezone(timedelta(hours=9))
PHASE_LABELS = {
    "REQUIREMENT": "요구·설계",
    "DEVELOPMENT": "개발·시험 신고",
    "REVIEW": "리뷰 단계 신고",
    "DISPOSITION": "판정·보완 신고",
    "COMPLETE": "완료 신고 · 증빙 별도",
    "BLOCKED": "검증 게이트 대기",
    "UNKNOWN": "단계 미확인",
}
PUBLIC_WORKS = {
    "COWORK-DROPBOX-TO-GITHUB-MIGRATION": (
        "협업 운송 전환", "review-watcher", "협업 관리·업무 실행",
        "LIVE 전환 선행 조건에 대한 사용자 결정·검증 근거 확인",
    ),
    "COWORK-GITHUB-DASHBOARD-20261111-001": (
        "CoWork 대시보드", "dashboard", "GPT",
        "HTML 화면 및 자동 갱신 상태 검증",
    ),
    "COWORK-SKILL-DISCOVERY-20261112-001": (
        "스킬 발견·재사용", "skill-discovery", "GPT",
        "추가 확인이 필요한 스킬 근거 검토",
    ),
    "JOBLIST-NRTX-20261112-001": (
        "업무 자동화 후보", "job-list", "GPT",
        "운영 적용 전 후보 시험 범위와 검증 게이트 확인",
    ),
    "L1-WORKSPACE-RAG-20261111-001": (
        "지식 구조 설계", "knowledge-design", "GPT",
        "실행 환경 확인 후 설계 검증",
    ),
}
# The user's two named examples are safe public skill labels, but only render
# when a real PRIVATE TRACKER has an independent work item for that skill.
PUBLIC_SKILL_EXAMPLES = {
    "l1-fix-workflow": ("l1-fix-workflow", "workflow", "GPT",
                        "작업 근거와 독립 리뷰 단계 확인"),
    "l1-github": ("l1-github", "github", "GPT",
                  "작업 근거와 독립 리뷰 단계 확인"),
}
MAX_PUBLIC_WORKS = 30


class SafetyBlock(ValueError):
    """No public content produced or updated."""


def _reported_status(value: str) -> str:
    if value in ("NOT_RUN", "PENDING"):
        return "미실행·대기"
    if value == "NOT_OBSERVED":
        return "기록 미관측"
    return "추가 증거 검증 필요"


def _phase_progress(raw: str) -> int:
    return {"REQUIREMENT": 1, "DEVELOPMENT": 2, "REVIEW": 3,
            "DISPOSITION": 4, "COMPLETE": 5}.get(raw, 0)


def _count(state: dict, family: str) -> int:
    item = state["transport"][family]
    value = item.get("files_observed")
    if type(value) is not int or not 0 <= value <= 100000:
        raise SafetyBlock("invalid transport count")
    return value


def _read_active_provider(root: Path) -> str:
    """Read only a bounded latest CURRENT section; export a controlled status label."""
    path = root / "collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md"
    try:
        if path.is_symlink() or not path.is_file() or path.stat().st_size > 220_000:
            return "기록 미확인"
        doc = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return "기록 미확인"
    if "\n## " not in doc:
        return "기록 미확인"
    head = doc.split("\n## ", 1)[1].split("\n## ", 1)[0][:16000]
    found = set(re.findall(r"\bACTIVE_PROVIDER\s*=\s*([A-Z_]+)\b", head))
    if not found:
        return "기록 미확인"
    if len(found) != 1:
        raise SafetyBlock("conflicting provider reports in latest CURRENT section")
    provider = found.pop()
    if provider == "NONE":
        return "활성 리뷰 제공자 없음"
    if provider == "DROPBOX":
        return "Dropbox 리뷰 제공자 (문서 기록)"
    # Migration has NOT cut over; new/unknown provider needs separate approval.
    raise SafetyBlock("unapproved active provider marker")


def build_payload(state: dict, date: str, *,
                  active_provider: str = "기록 미확인",
                  generated_at: str | None = None) -> dict:
    """Only fixed text/enum labels and aggregate numbers cross PUBLIC boundary."""
    if not isinstance(state, dict) or state.get("schema") != PRIVATE_SCHEMA:
        raise SafetyBlock("unexpected PRIVATE state schema")
    if state.get("visibility") != "PRIVATE_REPO_ONLY":
        raise SafetyBlock("unexpected source visibility")
    if state.get("phase") != "MIGRATION_NOT_CUTOVER":
        raise SafetyBlock("cutover state outside published approval")
    if not re.fullmatch(r"20[0-9]{2}-[01][0-9]-[0-3][0-9]", date):
        raise SafetyBlock("invalid date")
    if active_provider not in {
            "활성 리뷰 제공자 없음", "Dropbox 리뷰 제공자 (문서 기록)", "기록 미확인"}:
        raise SafetyBlock("invalid public provider label")
    if generated_at is not None:
        if not isinstance(generated_at, str) or not re.fullmatch(
                r"20\d\d-\d\d-\d\dT\d\d:\d\d:\d\dZ", generated_at):
            raise SafetyBlock("invalid generated_at format")
        try:
            datetime.strptime(generated_at, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError as exc:
            raise SafetyBlock("invalid generated_at time") from exc
    projects = state.get("projects")
    works = state.get("work_items")
    if not isinstance(projects, list) or not isinstance(works, list):
        raise SafetyBlock("missing Work items or projects")
    if len(projects) > 300 or len(works) > 500:
        raise SafetyBlock("source count too large")
    operations = state.get("operations")
    if not isinstance(operations, dict):
        raise SafetyBlock("missing operations evidence")
    independent_review = operations.get("independent_review", "NOT_OBSERVED")
    windows_stage1 = operations.get("windows_stage1", "NOT_OBSERVED")
    if independent_review not in {"NOT_RUN", "PENDING", "NOT_OBSERVED", "PASS", "FAIL", "PARTIAL"}:
        raise SafetyBlock("unexpected independent review marker")
    if windows_stage1 not in {"NOT_RUN", "PENDING", "NOT_OBSERVED", "PASS", "FAIL", "PARTIAL"}:
        raise SafetyBlock("unexpected host marker")
    output = []
    used_primary = set()
    example_counts: dict[str, int] = {}
    for w in works:
        if not isinstance(w, dict) or not isinstance(w.get("phase"), str):
            raise SafetyBlock("invalid Work record")
        phase = w["phase"]
        if phase not in PHASE_LABELS:
            raise SafetyBlock("unexpected stage marker")
        item_id, skill = w.get("work_id"), w.get("skill")
        if not isinstance(item_id, str) or not isinstance(skill, str):
            raise SafetyBlock("missing Work key")
        if item_id in PUBLIC_WORKS:
            if item_id in used_primary:
                raise SafetyBlock("duplicate public category")
            used_primary.add(item_id)
            title, category, owner, next_action = PUBLIC_WORKS[item_id]
        elif skill in PUBLIC_SKILL_EXAMPLES:
            # Publicly approved skill names but no PRIVATE Work ID or title.
            title, category, owner, next_action = PUBLIC_SKILL_EXAMPLES[skill]
            number = example_counts.get(skill, 0) + 1
            example_counts[skill] = number
            if number > 5:
                raise SafetyBlock("too many public example Works")
            if number > 1:
                title += " · 개별 작업 " + str(number)
        else:
            # New unapproved skill names remain PRIVATE.
            continue
        action_kind = ("USER" if item_id == "COWORK-DROPBOX-TO-GITHUB-MIGRATION"
                       and phase == "BLOCKED" else
                       "REVIEW" if phase == "REVIEW" else
                       "BLOCKED" if phase == "BLOCKED" else "OTHER")
        output.append({
            "title": title, "category": category, "owner": owner,
            "phase_label": PHASE_LABELS[phase],
            "phase_index": _phase_progress(phase),
            "action_kind": action_kind,
            "review_label": "독립 리뷰 증거 미검증",
            "test_label": "자체시험 기록 · 별도 검증",
            "next_action": next_action,
        })
    if len(output) > MAX_PUBLIC_WORKS:
        raise SafetyBlock("too many public Work cards")
    payload = {
        "schema": PUBLIC_SCHEMA,
        "snapshot_date": date,
        "source": "APPROVED_AGGREGATE_ONLY",
        "sync_mode": "AUTOMATED_ALLOWLIST",
        "cutover": "정식 전환 전",
        "counts": {
            "projects": len(projects),
            "requests": _count(state, "requests"),
            "reviews": _count(state, "reviews"),
            "receipts": _count(state, "receipts"),
            "works": len(works),
        },
        "checks": {
            "independent_review": _reported_status(independent_review),
            "windows_stage1": _reported_status(windows_stage1),
            "active_provider": active_provider,
        },
        "work_cards": output,
    }
    if generated_at is not None:
        payload["generated_at"] = generated_at
    return payload


def json_bytes(payload: dict) -> bytes:
    return (json.dumps(payload, ensure_ascii=False, indent=2,
                       sort_keys=True) + "\n").encode("utf-8")


def prepare(root: Path, date: str | None = None) -> bytes:
    """Fail if the dashboard cache was not generated from CURRENT/TRACKER inputs."""
    f = root / "collab/dashboard/state.json"
    try:
        if f.is_symlink() or not f.is_file() or f.stat().st_size > 300_000:
            raise SafetyBlock("missing/untrusted PRIVATE state file")
        raw = json.loads(f.read_text("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise SafetyBlock("invalid PRIVATE state") from exc
    rebuilt = generate.build_state(root)
    if raw != rebuilt:
        raise SafetyBlock("stale PRIVATE dashboard state: run generator first")
    date = date or datetime.now(KST).date().isoformat()
    return json_bytes(build_payload(
        raw, date, active_provider=_read_active_provider(root),
        generated_at=os.getenv("COWORK_STATUS_AT") or None))


def _request(url: str, token: str, *, method: str = "GET", body: bytes | None = None) -> dict:
    if url != "https://api.github.com/repos/" + PUBLIC_REPO + "/contents/" + PUBLIC_PATH:
        raise SafetyBlock("unapproved output destination")
    req = urllib.request.Request(url, data=body, method=method, headers={
        "Authorization": "Bearer " + token,
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "CoWork-allowlisted-Pages-sync",
        "Content-Type": "application/json",
    })
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = resp.read(80000)
        return json.loads(data)


def _read_public_existing(url: str, token: str) -> tuple[str | None, bytes | None]:
    try:
        obj = _request(url, token)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None, None
        raise
    if obj.get("encoding") != "base64":
        raise SafetyBlock("unexpected GitHub content encoding")
    encoded = obj.get("content", "")
    sha = obj.get("sha")
    if not isinstance(sha, str) or not re.fullmatch("[0-9a-f]{40}", sha):
        raise SafetyBlock("invalid existing public content SHA")
    return sha, base64.b64decode(encoded)


def publish_public(payload: bytes, token: str) -> str:
    if not token or len(token) < 20:
        raise SafetyBlock("public write token not configured")
    try:
        obj = json.loads(payload)
    except (ValueError, UnicodeError) as exc:
        raise SafetyBlock("invalid proposed JSON") from exc
    # Strict no extra sensitive/unapproved keys; reconstruct deterministic bytes.
    required = {"schema", "snapshot_date", "source", "sync_mode", "cutover",
                "counts", "checks", "work_cards"}
    if not isinstance(obj, dict) or not (set(obj) == required or
                                         set(obj) == required | {"generated_at"}):
        raise SafetyBlock("unexpected proposed public fields")
    if obj.get("schema") != PUBLIC_SCHEMA or obj.get("source") != "APPROVED_AGGREGATE_ONLY":
        raise SafetyBlock("invalid public schema")
    if len(payload) > 16000:
        raise SafetyBlock("public payload too large")
    if obj.get("generated_at") is not None:
        value = obj["generated_at"]
        if not isinstance(value, str) or not re.fullmatch(
                r"20\d\d-\d\d-\d\dT\d\d:\d\d:\d\dZ", value):
            raise SafetyBlock("invalid publish timestamp")
        try:
            at = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        except ValueError as exc:
            raise SafetyBlock("invalid publish timestamp") from exc
        if abs((datetime.now(timezone.utc) - at).total_seconds()) > 1800:
            raise SafetyBlock("stale/future publish timestamp")
    if not isinstance(obj.get("work_cards"), list) or len(obj["work_cards"]) > MAX_PUBLIC_WORKS:
        raise SafetyBlock("unapproved public card payload")
    # The emitted data was generated by build_payload; only canonical serialized form accepted.
    if payload != json_bytes(obj):
        raise SafetyBlock("unexpected public JSON serialization")
    url = "https://api.github.com/repos/" + PUBLIC_REPO + "/contents/" + PUBLIC_PATH
    sha, existing = _read_public_existing(url, token)
    if existing == payload:
        return "UNCHANGED"
    data = {
        "message": "docs(pages): auto-refresh approved CoWork status [allowlist-only]",
        "content": base64.b64encode(payload).decode("ascii"),
        "branch": "main",
    }
    if sha is not None:
        data["sha"] = sha
    _request(url, token, method="PUT", body=json.dumps(data).encode("utf-8"))
    _, readback = _read_public_existing(url, token)
    if readback != payload:
        raise SafetyBlock("remote PUBLIC readback mismatch")
    return "POSTED_READBACK_PASS"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["prepare", "publish"])
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--out", type=Path)
    parser.add_argument("--file", type=Path)
    parser.add_argument("--date")
    args = parser.parse_args()
    if args.mode == "prepare":
        if args.out is None:
            raise SystemExit("prepare requires --out")
        result = prepare(args.root, args.date)
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_bytes(result)
        print("ALLOWLIST_BUILD=PASS", len(result), "bytes")
    else:
        if args.file is None:
            raise SystemExit("publish requires --file")
        expected = prepare(args.root, args.date)
        if args.file.read_bytes() != expected:
            raise SafetyBlock("prepared payload changed/stale")
        token = os.getenv(TOKEN_ENV, "")
        result = publish_public(expected, token)
        print("PUBLIC_SYNC=" + result)


if __name__ == "__main__":
    main()
