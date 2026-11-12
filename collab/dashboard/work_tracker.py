"""Independent-work tracker for the PRIVATE CoWork dashboard.

- Every project CURRENT is represented as one independently identifiable Work.
- A project may register multiple skill-specific Works in TRACKER.json.
- Metadata is DOCUMENT-REPORTED, not runtime evidence; no reviewer invocation.
- No external calls, no PUBLIC synchronization, no free-form source-path dereference.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

VALID_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,100}\Z")
VALID_SKILL = re.compile(r"[a-z][a-z0-9_-]{0,63}\Z")
SCHEMA = "COWORK_WORK_TRACKER_V1"
PHASES = {
    "REQUIREMENT": ("요구·범위", 1),
    "DEVELOPMENT": ("개발·시험", 2),
    "REVIEW": ("독립 리뷰", 3),
    "DISPOSITION": ("GPT 판정", 4),
    "COMPLETE": ("완료 기록", 5),
    "BLOCKED": ("차단·보류", 0),
    "UNKNOWN": ("단계 미확인", 0),
}
TESTS = {"PASS", "FAIL", "SKIP", "NOT_RUN", "NOT_VERIFIED"}
REVIEW = {"PASS", "FAIL", "PENDING", "NOT_RUN", "NOT_VERIFIED"}
MAX_PROJECTS = 300
MAX_WORKS = 500


def _safe_file(path: Path, size: int) -> str | None:
    try:
        if path.is_symlink() or not path.is_file() or path.stat().st_size > size:
            return None
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return None


def _text(value: object, limit: int, default: str) -> str:
    if not isinstance(value, str):
        return default
    # Restrict to single-line display labels. Never embed raw paragraphs, links, markup.
    value = re.sub(r"[\r\n\t\x00-\x1f]", " ", value).strip()
    return value[:limit] if value else default


def _first_current(doc: str) -> str:
    if "\n## " in doc:
        return doc.split("\n## ", 1)[1].split("\n## ", 1)[0][:15000]
    return doc[:3000]


def _marker(section: str, key: str) -> str:
    # A project CURRENT can have many historical sections; read only current head.
    for line in section.splitlines()[:120]:
        match = re.fullmatch(r"(?:(?:[-*] *)|(?:\*\*))?"
                             + re.escape(key)
                             + r"(?:\*\*)?\s*[:=]\s*([A-Z][A-Z0-9_]*)\b.*", line.strip())
        if match:
            return match.group(1)
    return "NOT_VERIFIED"


def _base_record(slug: str, current: str) -> dict:
    section = _first_current(current)
    development = _marker(section, "DEVELOPMENT")
    self_test = _marker(section, "SELF_TEST")
    independent_review = _marker(section, "INDEPENDENT_REVIEW")
    phase = ("REQUIREMENT" if development == "DESIGN_ONLY" else
             "DEVELOPMENT" if development in {"IMPLEMENTED", "CANDIDATE", "DEVELOPMENT"} else
             "UNKNOWN")
    return {
        "work_id": slug,
        "skill": "미지정",
        "title": _text(next((l.removeprefix("# ") for l in current.splitlines()
                             if l.startswith("# ")), slug), 110, slug),
        "phase": phase,
        "owner": "미등록",
        "self_test": self_test if self_test in TESTS else "NOT_VERIFIED",
        "independent_review": (independent_review if independent_review in REVIEW
                               else "NOT_VERIFIED"),
        "next_action": "CURRENT.md 최신 상태 및 다음 담당 확인",
        "source": f"collab/projects/{slug}/CURRENT.md",
        "record_source": "CURRENT_ONLY_UNSTRUCTURED",
        "evidence": "CURRENT 문서 관측. 단계·진행률은 증명되지 않음",
    }


def _registered(raw: dict, slug: str, defaults: dict) -> list[dict] | None:
    if not isinstance(raw, dict) or raw.get("schema") != SCHEMA:
        return None
    works = raw.get("works")
    if not isinstance(works, list) or not 1 <= len(works) <= 30:
        return None
    result: list[dict] = []
    ids: set[str] = set()
    for w in works:
        if not isinstance(w, dict):
            return None
        work_id, skill = w.get("work_id"), w.get("skill")
        phase = w.get("phase", "UNKNOWN")
        if (not isinstance(work_id, str) or not VALID_ID.fullmatch(work_id)
                or work_id in ids or phase not in PHASES):
            return None
        if not isinstance(skill, str) or not VALID_SKILL.fullmatch(skill):
            return None
        self_test = w.get("self_test", "NOT_VERIFIED")
        review = w.get("independent_review", "NOT_VERIFIED")
        if self_test not in TESTS or review not in REVIEW:
            return None
        ids.add(work_id)
        result.append({
            "work_id": work_id,
            "skill": skill,
            "title": _text(w.get("title"), 110, skill),
            "phase": phase,
            "owner": _text(w.get("owner"), 45, "미등록"),
            "self_test": self_test,
            "independent_review": review,
            "next_action": _text(w.get("next_action"), 165, "CURRENT.md 확인 필요"),
            "source": defaults["source"],
            "record_source": "REGISTERED_METADATA_UNVERIFIED",
            "evidence": "프로젝트 TRACKER.json 신고 값 · 운영 근거 별도 확인 필요",
        })
    return result


def collect(root: Path) -> list[dict]:
    """Read CURRENT per Work; if registered, split one project into multiple skill Works."""
    base = root / "collab" / "projects"
    if base.is_symlink() or not base.is_dir():
        return []
    records: list[dict] = []
    ids: set[str] = set()
    folders = sorted((p for p in base.iterdir() if p.is_dir() and not p.is_symlink()
                      and VALID_ID.fullmatch(p.name)), key=lambda p: p.name)
    for folder in folders[:MAX_PROJECTS]:
        current = _safe_file(folder / "CURRENT.md", 256_000)
        if current is None:
            continue
        fallback = _base_record(folder.name, current)
        metadata = _safe_file(folder / "TRACKER.json", 35_000)
        registered = None
        if metadata is not None:
            try:
                registered = _registered(json.loads(metadata), folder.name, fallback)
            except (json.JSONDecodeError, ValueError):
                registered = None
        entries = registered if registered is not None else [fallback]
        for item in entries:
            if item["work_id"] in ids:
                # Do not conflate two projects having the same Work ID.
                raise ValueError("duplicate Work ID across projects: " + item["work_id"])
            ids.add(item["work_id"])
            records.append(item)
            if len(records) >= MAX_WORKS:
                return records
    return records


def counts(works: list[dict]) -> dict[str, int]:
    return {
        "all": len(works),
        "active": sum(x["phase"] in {"REQUIREMENT", "DEVELOPMENT", "DISPOSITION"} for x in works),
        "review": sum(x["phase"] == "REVIEW" for x in works),
        "blocked": sum(x["phase"] == "BLOCKED" for x in works),
        "complete": sum(x["phase"] == "COMPLETE" for x in works),
        "unknown": sum(x["phase"] == "UNKNOWN" for x in works),
        "registered": sum(x["record_source"] == "REGISTERED_METADATA_UNVERIFIED" for x in works),
    }


CSS = """
.tracker{background:#fff;border:1px solid #dfe6ef;border-radius:18px;padding:24px;margin-top:28px}
.tracker-heading{display:flex;align-items:end;justify-content:space-between;gap:16px;flex-wrap:wrap}
.tracker-heading h2{font-size:23px;margin:4px 0}
.tracker-sub{color:#52647a;font-size:13px;margin:6px 0}
.tracker-metrics{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px;margin:19px 0}
.tracker-stat{border:1px solid #dbe4ee;border-radius:12px;padding:12px;background:#f6f9fc}
.tracker-stat strong{font-size:25px;display:block;font-variant-numeric:tabular-nums}
.tracker-stat span{font-size:11px;color:#536681}
.tracker-search{font:inherit;background:white;border:1px solid #b9cada;border-radius:10px;padding:9px 12px;min-width:225px;max-width:100%}
.tracker-list{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}
.tracker-work{border:1px solid #dce5ed;border-radius:14px;padding:19px;min-width:0;background:#fff}
.tracker-work-top{display:flex;justify-content:space-between;gap:12px;align-items:center;flex-wrap:wrap}
.tracker-skill{font-size:11px;color:#4d6b92;font-weight:800}
.tracker-phase{font-size:11px;border-radius:7px;padding:5px 9px;background:#eff3f8;color:#3f5c7b;font-weight:800}
.tracker-work h3{font-size:16px;line-height:1.35;margin:11px 0}
.tracker-id{font-size:11px;color:#61718a;overflow-wrap:anywhere}
.tracker-steps{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:5px;margin:15px 0}
.tracker-step{min-width:0}
.tracker-progress{height:7px;border-radius:6px;background:#dbe3ee;margin-bottom:6px}
.tracker-step.current .tracker-progress{background:#4d83b7}
.tracker-step.past .tracker-progress{background:#a1b8ca}
.tracker-step small{display:block;font-size:10px;text-align:center;color:#64768c}
.tracker-meta{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:10px 0}
.tracker-meta p{font-size:12px;color:#4c5e75;margin:0}
.tracker-next{margin:14px 0;background:#f5f8fb;padding:11px;border-radius:9px;font-size:12px}
.tracker-note{font-size:11px;color:#667890;margin:12px 0}
.tracker-work a{font-size:12px;font-weight:750}
@media(max-width:850px){.tracker-list{grid-template-columns:1fr}.tracker-metrics{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media(max-width:550px){.tracker{padding:15px}.tracker-metrics{grid-template-columns:repeat(2,minmax(0,1fr))}.tracker-work{padding:15px}.tracker-meta{grid-template-columns:1fr}.tracker-search{min-width:0;width:100%}}
"""


def render_html(works: list[dict], url_for) -> str:
    esc = html.escape
    k = counts(works)
    boxes = "".join(
        '<div class="tracker-stat"><strong>' + str(k[key]) + '</strong><span>' + label
        + '</span></div>' for key, label in (
            ("all", "관측 Work"), ("active", "개발·판정(신고)"),
            ("review", "리뷰 단계(신고)"), ("blocked", "차단 단계(신고)"),
            ("unknown", "단계 미확인"))
    )
    cards = []
    labels = ["요청", "개발", "리뷰", "판정", "완료"]
    for w in works:
        stage_label, stage_num = PHASES[w["phase"]]
        stages = "".join(
            '<div class="tracker-step ' +
            ("current" if stage_num == i else "past" if stage_num > i else "") +
            '"><div class="tracker-progress"></div><small>' + label + '</small></div>'
            for i, label in enumerate(labels, 1)
        )
        # Explicitly label rendered phases as metadata, never verified completion.
        link = esc(url_for(w["source"]), quote=True)
        term = esc((w["title"] + " " + w["work_id"] + " " + w["skill"]).lower(), quote=True)
        cards.append(
            '<article class="tracker-work" data-work-search="' + term + '">'
            '<div class="tracker-work-top"><span class="tracker-skill">' +
            esc(w["skill"]) + '</span><span class="tracker-phase">' +
            esc(stage_label) + '</span></div><h3>' + esc(w["title"]) +
            '</h3><div class="tracker-id">Work ID: ' + esc(w["work_id"]) + '</div>' +
            '<div class="tracker-steps">' + stages + '</div>' +
            '<div class="tracker-meta"><p>담당: ' + esc(w["owner"]) +
            '</p><p>자체시험: ' + esc(w["self_test"]) +
            '</p><p>독립 리뷰: ' + esc(w["independent_review"]) +
            '</p><p>근거: ' + esc(w["record_source"]) + '</p></div>' +
            '<div class="tracker-next"><b>다음 조치</b> · ' +
            esc(w["next_action"]) + '</div>' +
            '<p class="tracker-note">' + esc(w["evidence"]) + '</p>' +
            '<a href="' + link + '" rel="noopener noreferrer">CURRENT.md 원문 확인</a></article>'
        )
    return (
        '<section class="tracker" aria-label="병렬 Work별 독립 진행 현황">'
        '<div class="tracker-heading"><div><span class="overline">WORK TRACKER / INDEPENDENT STREAMS</span>'
        '<h2>작업별 진행 현황</h2>'
        '<p class="tracker-sub">동시에 진행하는 작업을 Work ID별로 독립 추적. '
        '단계 위치는 문서 신고 값이며 실제 단계 완료를 의미하지 않습니다.</p></div>'
        '<label>작업명 검색 <input class="tracker-search" id="tracker-search" '
        'type="search" placeholder="스킬 또는 Work ID 검색" autocomplete="off"></label></div>'
        '<div class="tracker-metrics">' + boxes + '</div>'
        '<div class="tracker-list">' + "".join(cards) + '</div>'
        '<p id="tracker-zero" class="empty" hidden>일치하는 Work가 없습니다.</p>'
        '<p class="tracker-note">여러 스킬이 하나의 프로젝트에 속해도 TRACKER.json에 '
        '서로 다른 Work ID를 등록하면 개별 카드로 분리됩니다. '
        '미등록 스킬의 실제 진행 상황은 임의로 생성하지 않습니다.</p></section>'
    )


def render_markdown(works: list[dict], url_for) -> str:
    result = [
        "## 작업별 진행 현황 · 독립 Work Tracker",
        "",
        "각 Work는 고유 ID로 구분. 단계/시험/리뷰 표시는 문서 신고값이며 실제 완료 검증이 아닙니다.",
        "",
        "| Work ID | 스킬 | 진행 단계(신고) | 담당 | 시험(신고) | 독립 리뷰(신고) | 다음 조치 |",
        "|---|---|---|---|---|---|---|",
    ]
    for w in works:
        clean = lambda v: str(v).replace("|", "／").replace("\n", " ")
        result.append("| [" + clean(w["work_id"]) + "](" + url_for(w["source"]) +
                      ") | " + clean(w["skill"]) + " | " + PHASES[w["phase"]][0] +
                      " | " + clean(w["owner"]) + " | " + clean(w["self_test"]) +
                      " | " + clean(w["independent_review"]) + " | " +
                      clean(w["next_action"]) + " |")
    result.extend(["", "스킬별 병렬 작업은 각 프로젝트의 TRACKER.json으로 등록합니다. "
                         "등록 전에는 확인되지 않은 실제 진행률을 추정하지 않습니다.", ""])
    return "\n".join(result)
