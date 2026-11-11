#!/usr/bin/env python3
"""Build the self-contained, *synthetic-only* public CoWork preview.

This module intentionally never opens project, request, review, receipt or
operational state files. It does not accept data or text from the repository.
Publishing the output requires a separate explicit user approval.
"""
from __future__ import annotations

import argparse
import html
from pathlib import Path

SCHEMA = "COWORK_PUBLIC_PREVIEW_V1"
RELEASE_GATE = "NOT_APPROVED"
DATA_CLASSIFICATION = "SYNTHETIC_ONLY"

# Fixed, externally safe copy. Do NOT interpolate PRIVATE work IDs, counts,
# people, paths, issues, revisions, dates, tokens, URLs or source documents.
EXAMPLE_STAGES = (
    ("01", "요청 접수", "작업이 등록되면 요청 목적과 범위를 확인하는 단계입니다."),
    ("02", "검토 및 피드백", "검토 결과를 분류하고 필요한 후속 보완을 정리하는 단계입니다."),
    ("03", "판정 및 마무리", "확인된 결과를 판정하고 다음 작업을 결정하는 단계입니다."),
)


def render() -> str:
    """Produce stable HTML without reading any external/private input."""
    cards = "\n".join(
        '<article class="step"><div class="step-top"><span class="step-no">'
        + html.escape(num) + '</span><span class="tag">샘플 단계</span></div>'
        + '<h3>' + html.escape(title) + '</h3><p>' + html.escape(description)
        + '</p></article>'
        for num, title, description in EXAMPLE_STAGES
    )
    return '''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,nofollow,noarchive">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'none'; img-src 'none'; connect-src 'none'; form-action 'none'">
<title>CoWork | 공개용 대시보드 미리보기</title>
<style>
:root { color-scheme: light; --ink:#1b2942; --muted:#516178; --line:#dce4ee; --paper:#fff; --bg:#f4f7fb; --accent:#315e90; }
* { box-sizing:border-box; }
body { margin:0; font-family:system-ui,-apple-system,"Malgun Gothic",sans-serif; color:var(--ink); background:var(--bg); line-height:1.6; }
main { width:min(1080px,100%); margin:auto; padding:40px 24px 80px; }
header { display:flex; flex-direction:column; gap:8px; }
.eyebrow { color:var(--accent); font-size:12px; font-weight:800; letter-spacing:.1em; }
h1 { font-size:clamp(26px,4vw,40px); line-height:1.25; margin:0; letter-spacing:-.045em; }
h2 { font-size:21px; margin:0; } h3 { font-size:19px; margin:12px 0 5px; }
p { margin:0; } .muted { color:var(--muted); }
.notice { margin-top:24px; padding:20px 22px; border:1px solid #cbd9ea; border-radius:16px; background:#eaf1fa; }
.notice strong { display:block; font-size:17px; margin-bottom:6px; }
.status { display:inline-block; margin-top:13px; padding:5px 11px; border-radius:100px; background:#fff; border:1px solid #bfcfe1; color:#264e7b; font-size:12px; font-weight:750; }
.section-head { display:flex; flex-direction:column; gap:4px; margin:34px 0 16px; }
.grid { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:16px; }
.step { padding:23px; background:var(--paper); border:1px solid var(--line); border-radius:18px; min-width:0; }
.step-top { display:flex; justify-content:space-between; align-items:center; gap:8px; }
.step-no { color:var(--accent); font-weight:850; font-size:24px; }
.tag { font-size:12px; padding:4px 9px; border:1px solid #d3dfeb; border-radius:99px; color:#52677e; }
.step p { color:var(--muted); font-size:14px; }
.summary { border:1px solid var(--line); border-radius:16px; padding:22px 24px; background:#fff; }
.summary strong { display:block; margin-bottom:8px; }
footer { margin-top:32px; color:var(--muted); font-size:13px; border-top:1px solid var(--line); padding-top:18px; }
@media(max-width:760px) { main { padding:22px 15px 48px; } .grid { grid-template-columns:1fr; } }
</style>
</head>
<body>
<main data-schema="''' + SCHEMA + '''" data-classification="''' + DATA_CLASSIFICATION + '''" data-release="''' + RELEASE_GATE + '''">
<header>
<div class="eyebrow">COWORK · PUBLIC PREVIEW CONCEPT</div>
<h1>협업 진행 대시보드</h1>
<p class="muted">웹브라우저에서 즉시 열 수 있도록 준비한 공개용 화면 시안</p>
</header>
<section class="notice" aria-label="데이터 및 공개 상태">
<strong>샘플 데이터만 표시하는 미리보기입니다.</strong>
<p>실제 업무 현황, 내부 프로젝트, 리뷰 이력 또는 운영 상태를 반영하지 않습니다. 공개 웹사이트 게시도 아직 승인되지 않았습니다.</p>
<span class="status">배포 승인 전 · 비운영 데모</span>
</section>
<section aria-label="예시 업무 흐름">
<div class="section-head"><h2>업무 진행 흐름</h2><p class="muted">아래 카드는 동작 구조를 보여주기 위한 예시입니다.</p></div>
<div class="grid">''' + cards + '''</div>
</section>
<section aria-label="공개 범위 안내">
<div class="section-head"><h2>공개 화면에 표시할 내용</h2></div>
<div class="summary"><strong>공개 승인된 정보만 표시</strong>
<p class="muted">실제 데이터를 연결하려면 별도 공개 승인과 항목별 반출 심사가 필요합니다. 승인 전에는 예시 화면만 유지합니다.</p></div>
</section>
<footer>© CoWork · 공개용 후보 화면. 개인정보·운영정보·내부 링크·실제 이슈 및 리뷰 내용은 포함하지 않습니다.</footer>
</main>
</body>
</html>
'''


def write(output: Path) -> int:
    """Write the fixed preview to the chosen PRIVATE/locally scoped output path."""
    payload = render().encode("utf-8")
    if len(payload) > 120_000:
        raise ValueError("public preview unexpectedly large")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(payload)
    return len(payload)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("index.html"))
    args = parser.parse_args()
    print("SYNTHETIC_ONLY, NOT_APPROVED, PRIVATE_CANDIDATE, bytes:", write(args.output))
