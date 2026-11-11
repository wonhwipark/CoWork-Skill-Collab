"""PRIVATE dashboard collaboration flow: role-based labels and evidence-gated states.

This is a read-only projection, not evidence that a Windows review ran.
"""
from __future__ import annotations

import html
import re
from pathlib import Path


FLOW_CSS = """
.flow-area{margin:28px 0;background:transparent}
.flow-area h2{font-size:23px;margin:4px 0 8px}.flow-area h3{font-size:17px;margin:0}
.flow-heading{display:flex;justify-content:space-between;align-items:flex-end;gap:12px;flex-wrap:wrap;margin:20px 0 14px}
.flow-heading .sub{margin:4px 0 0}
.live-lane{border:1px solid #bad2cc;background:#edf6f3;border-radius:15px;padding:17px 20px;margin:12px 0 24px}
.lane-label{color:#285f51;font-weight:800;font-size:13px}
.lane-path{font-weight:700;line-height:1.9;margin:8px 0;overflow-wrap:anywhere}
.lane-path b{color:#4b7b6d;margin:0 7px}
.live-lane .flow-note{margin:5px 0 0;font-size:12px;color:#48685f}
.target-label{display:flex;gap:12px;align-items:center;margin:20px 0 13px;flex-wrap:wrap}
.flow-strip{counter-reset:flow;list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px 16px}
.flow-node{position:relative;min-width:0;background:#fff;border:1px solid #d7e2ef;border-radius:14px;padding:16px;box-shadow:0 2px 9px rgba(12,38,72,.03)}
.flow-node:after{content:"→";position:absolute;right:-15px;top:45%;font-size:20px;font-weight:750;color:#7087a3;z-index:2}
.flow-node:nth-child(4):after{content:"↓";right:14px;top:auto;bottom:-27px}
.flow-node:last-child:after{display:none}
.flow-number{display:inline-block;color:#3c668e;font-size:12px;font-weight:850;letter-spacing:.05em;margin-bottom:9px}
.flow-node h3{font-size:15px;line-height:1.4;margin-bottom:6px}
.flow-owner{font-size:12px;color:#53677f;margin:5px 0 9px}
.flow-observed{font-size:13px;font-weight:750;color:#264d77;margin:9px 0 6px;overflow-wrap:anywhere}
.flow-note{font-size:12px;color:#56677d;margin:0;line-height:1.55}
.flow-caption{font-size:13px;color:#51647b;margin:13px 0 28px}
.flow-table-scroll{overflow-x:auto;background:#fff;border:1px solid #d7e2ef;border-radius:14px}
.flow-table{width:100%;border-collapse:collapse;font-size:13px;line-height:1.6}
.flow-table th,.flow-table td{padding:12px 14px;text-align:left;border-bottom:1px solid #e5ebf2;vertical-align:top}
.flow-table thead{background:#f1f5fa;color:#253b57}
.flow-table tr:last-child th,.flow-table tr:last-child td{border-bottom:0}
.flow-table tbody th{font-weight:700;width:25%}
.flow-table td:nth-child(2){width:30%}
.flow-links{display:flex;gap:18px;flex-wrap:wrap;margin:14px 0 25px;font-size:13px}
@media(max-width:960px){.flow-strip{grid-template-columns:repeat(2,minmax(0,1fr))}
.flow-node:nth-child(4):after{content:"→";right:-15px;top:45%;bottom:auto}
.flow-node:nth-child(2n):not(:last-child):after{content:"↓";right:14px;top:auto;bottom:-24px}}
@media(max-width:650px){.flow-strip{grid-template-columns:1fr;gap:20px}
.flow-node:not(:last-child):after,.flow-node:nth-child(4):after{content:"↓";right:calc(50% - 7px);top:auto;bottom:-23px}
.flow-table{min-width:550px}.live-lane{padding:14px}.lane-path{font-size:13px}.flow-heading h2{font-size:21px}}
"""

MIGRATION = "COWORK-DROPBOX-TO-GITHUB-MIGRATION"
DASHBOARD = "COWORK-GITHUB-DASHBOARD-20261111-001"
FIELD_RE = re.compile(r"\b([A-Z][A-Z0-9_]{2,50})\s*=\s*([A-Z][A-Z0-9_]{1,80})\b")


def first_section(root: Path, slug: str) -> str:
    f = root / "collab" / "projects" / slug / "CURRENT.md"
    try:
        if f.is_symlink() or not f.is_file() or f.stat().st_size > 200_000:
            return ""
        data = f.read_text(encoding="utf-8")
    except (UnicodeError, OSError):
        return ""
    if "\n## " not in data:
        return ""
    return data.split("\n## ", 1)[1].split("\n## ", 1)[0][:12000]


def marker(section: str, field: str) -> str:
    if field not in ("WINDOWS_STAGE1_EXECUTION", "HOST_SHADOW", "INDEPENDENT_REVIEW",
                     "GITHUB_PAGES_DEPLOY", "CUTOVER"):
        raise ValueError("unsupported field")
    for match in FIELD_RE.finditer(section):
        if match.group(1) == field:
            return match.group(2)
    return "NOT_OBSERVED"


def snapshot(root: Path) -> dict:
    m = first_section(root, MIGRATION)
    d = first_section(root, DASHBOARD)
    return {
        "windows_stage1": marker(m, "WINDOWS_STAGE1_EXECUTION"),
        "independent_review": marker(m, "INDEPENDENT_REVIEW"),
        "host_shadow": marker(m, "HOST_SHADOW"),
        "cutover": marker(m, "CUTOVER"),
        "pages_deployment": marker(d, "GITHUB_PAGES_DEPLOY"),
        "migration_source": bool(m),
        "dashboard_source": bool(d),
    }


def pretty(raw: str) -> str:
    return {
        "NOT_RUN": "미실행", "NOT_OBSERVED": "기록 미관측",
        "MIGRATION_NOT_CUTOVER": "정식 전환 전",
        "PASS": "배포 성공 기록", "PARTIAL": "일부 확인",
        "BLOCKED": "차단", "BLOCKED_TRUST": "신뢰 검증 차단",
        "PENDING": "대기",
    }.get(raw, "원문 확인 필요")


def observed(state: dict, key: str) -> int:
    value = state.get("transport", {}).get(key, {}).get("files_observed", 0)
    return value if type(value) is int and 0 <= value <= 100000 else 0


def status_rows(state: dict) -> list[tuple[str, str, str]]:
    ops = state.get("operations", {})
    return [
        ("현재 운영 경로", "기존 LIVE 유지 (문서 기준)", "GitHub 정식 전환과 별개"),
        ("GitHub 전환", pretty(ops.get("cutover", "NOT_OBSERVED")), "별도 명시적 승인 전 전환 금지"),
        ("Windows 실행·SHADOW", pretty(ops.get("windows_stage1", "NOT_OBSERVED")), "실제 호스트 실행 증거 필요"),
        ("Claude Code 독립 리뷰", pretty(ops.get("independent_review", "NOT_OBSERVED")), "자체 시험과 구분"),
        ("GitHub 요청·결과·영수증",
         "요청 %d · 결과 %d · 영수증 %d" % (
             observed(state, "requests"), observed(state, "reviews"), observed(state, "receipts")),
         "PRIVATE 파일 관측 수일 뿐 완료 건수가 아님"),
        ("공개 샘플 웹페이지", pretty(ops.get("pages_deployment", "NOT_OBSERVED")),
         "L1Work의 샘플만 PUBLIC, 실제 협업 현황 비공개"),
    ]


def render_html(state: dict) -> str:
    esc = html.escape
    ops = state.get("operations", {})
    steps = [
        ("01", "요구·범위 확정", "GPT · 협업 관리 환경", "승인과 인계 기록", "실행 승인과 구별"),
        ("02", "REQUEST / READY", "GitHub PRIVATE · 협업 관리 환경",
         "요청 파일 %d개 관측" % observed(state, "requests"), "파일 존재 ≠ 유효 승인"),
        ("03", "승인·신뢰 검증", "Python watcher · 업무 실행 환경",
         "호스트 실행 %s" % pretty(ops.get("windows_stage1", "NOT_OBSERVED")),
         "서명·정책·비용·중복 확인"),
        ("04", "독립 검토", "Claude Code · 업무 실행 환경",
         "독립 리뷰 %s" % pretty(ops.get("independent_review", "NOT_OBSERVED")),
         "개발자 자체 시험과 구분"),
        ("05", "리뷰·영수증", "GitHub PRIVATE · 협업 관리 환경",
         "결과 %d개 · 영수증 %d개" % (observed(state, "reviews"), observed(state, "receipts")),
         "완료·서명 별도 확인"),
        ("06", "판정·피드백", "GPT · 협업 관리 환경", "결과 근거 확인·후속 조치", "판정은 모델 실행 승인 아님"),
        ("07", "현황 자동 갱신", "GitHub Actions · 협업 관리 환경", "PRIVATE 문서 기준 요약", "리뷰 호출·운영 변경 없음"),
    ]
    cards = "".join(
        '<li class="flow-node"><span class="flow-number">' + esc(num)
        + '</span><h3>' + esc(title) + '</h3><p class="flow-owner">' + esc(owner)
        + '</p><p class="flow-observed">' + esc(status) + '</p>'
        + '<p class="flow-note">' + esc(note) + '</p></li>'
        for num, title, owner, status, note in steps
    )
    trs = "".join(
        '<tr><th scope="row">' + esc(name) + '</th><td><strong>' + esc(value)
        + '</strong></td><td>' + esc(note) + '</td></tr>'
        for name, value, note in status_rows(state)
    )
    return (
        '<section class="flow-area" aria-label="협업 흐름 및 운영 현황">'
        '<div class="flow-heading"><span class="overline">WORKFLOW / ROLE / STATUS</span>'
        '<h2>협업 구조와 현재 상태</h2>'
        '<p class="sub">환경은 위치가 아니라 역할로 구분합니다: '
        '<b>협업 관리 환경</b>(GPT·GitHub) / <b>업무 실행 환경</b>(Windows·Claude Code).</p></div>'
        '<div class="live-lane"><span class="lane-label">현재 운영 경로 · 변경 없음</span>'
        '<div class="lane-path">GPT 요구·판정 <b>→</b> 기존 LIVE 운송 <b>→</b> '
        'Windows 감시기 / Claude Code <b>→</b> 결과·영수증 / GPT</div>'
        '<p class="flow-note">기존 운영 유지(문서 기준). 실제 Windows 호스트의 최신 운영 확인과 혼동하지 않습니다.</p></div>'
        '<div class="target-label"><h3>GitHub 목표 경로</h3><span class="pill warning">정식 전환 전</span></div>'
        '<ol class="flow-strip">' + cards + '</ol>'
        '<p class="flow-caption">카드의 화살표는 계획된 처리 순서입니다. '
        'READY·리뷰 파일 관측을 승인·실행·LIVE 전환 완료로 판정하지 않습니다.</p>'
        '<div class="flow-heading"><h3>실제 기록 기반 STATUS</h3>'
        '<p class="sub">각 CURRENT.md 최신 섹션과 GitHub 파일 관측 수를 구분했습니다.</p></div>'
        '<div class="flow-table-scroll"><table class="flow-table">'
        '<thead><tr><th scope="col">항목</th><th scope="col">현재</th>'
        '<th scope="col">검증 한계</th></tr></thead><tbody>' + trs + '</tbody></table></div>'
        '<div class="flow-links">'
        '<a href="https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/'
        + MIGRATION + '/CURRENT.md">운송·Windows 전환 현황</a>'
        '<a href="https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/'
        + DASHBOARD + '/CURRENT.md">대시보드 배포 현황</a></div></section>'
    )


def render_markdown(state: dict) -> str:
    fence = chr(96) * 3
    lines = [
        "## 협업 흐름과 상태 · 역할 기준",
        "",
        "**협업 관리 환경** — GPT · GitHub / **업무 실행 환경** — Windows 감시기 · Claude Code",
        "",
        fence + "mermaid",
        "flowchart TB",
        '  subgraph LIVE["현재 운영 경로 · 변경 없음"]',
        '    L1["GPT 요구·판정"] --> L2["기존 LIVE 운송"]',
        '    L2 --> L3["Windows 감시기 / Claude Code"]',
        '    L3 --> L4["결과·영수증 / GPT"]',
        "  end",
        '  subgraph NEXT["GitHub 목표 경로 · 정식 전환 전"]',
        '    A["GPT 요구·범위 확정"] --> B["GitHub PRIVATE / REQUEST·READY"]',
        '    B --> C["Windows watcher / 승인·신뢰 검증"]',
        '    C --> D["Claude Code / 독립 리뷰"]',
        '    D --> E["GitHub PRIVATE / 리뷰·영수증"]',
        '    E --> F["GPT / 판정·피드백"]',
        '    F --> G["GitHub Actions / 대시보드"]',
        "  end",
        '  L4 -. "필수 게이트 및 별도 LIVE 승인 이후" .-> A',
        fence,
        "",
        "> 화살표는 설계된 경로입니다. Windows 실행·서명 검증·독립 리뷰의 PASS를 뜻하지 않습니다.",
        "",
        "### 운영·검증 상태",
        "",
        "| 구분 | 현재 상태 | 근거 범위 |",
        "|---|---|---|",
    ]
    for name, value, note in status_rows(state):
        lines.append("| %s | **%s** | %s |" % (name, value, note))
    lines += [
        "",
        "[전환·Windows 원문](../projects/" + MIGRATION + "/CURRENT.md)"
        " · [대시보드 원문](../projects/" + DASHBOARD + "/CURRENT.md)",
        "",
    ]
    return "\n".join(lines)
