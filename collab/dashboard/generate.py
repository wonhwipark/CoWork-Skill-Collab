#!/usr/bin/env python3
"""Build a PRIVATE, read-only GitHub CoWork dashboard from repository files.

No external services, secrets, model calls, review execution or public publishing.
"""
from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path
from urllib.parse import quote

import review_chain

REPO = "wonhwipark/CoWork-Skill-Collab"
PROJECT_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,100}\Z")
STATUS_RE = re.compile(r"(?:CUTOVER|PRE_CUTOVER_READINESS|GPT_DISPOSITION|INDEPENDENT_REVIEW|HOST_SHADOW)\s*[=:]\s*([A-Z][A-Z0-9_]+)")
BLOCKED = {"BLOCKED", "BLOCKED_TRUST", "FAIL", "FAILED"}


def safe_read(path: Path, limit: int = 256_000) -> str | None:
    if path.is_symlink() or not path.is_file() or path.stat().st_size > limit:
        return None
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return None


def project_status(section: str, slug: str) -> tuple[str, str]:
    # States are qualified as source assertions, not executed or verified facts.
    if "MIGRATION_NOT_CUTOVER" in section or "DROPBOX_LIVE" in section:
        return "전환 전", "warning"
    found = STATUS_RE.findall(section)
    if any(x in BLOCKED for x in found):
        return "차단 기록", "danger"
    if "NOT_RUN" in section or any(x.endswith("PARTIAL") for x in found):
        return "검증 진행 중", "warning"
    if "PASS" in section or "COMPLETED" in section:
        return "문서상 진행", "neutral"
    return "상태 확인 필요", "neutral"


def build_state(root: Path, repo: str = REPO) -> dict:
    projects = []
    directory = root / "collab" / "projects"
    if directory.is_dir():
        for folder in sorted(directory.iterdir(), key=lambda x: x.name.lower()):
            if not PROJECT_NAME.fullmatch(folder.name) or folder.is_symlink() or not folder.is_dir():
                continue
            f = folder / "CURRENT.md"
            content = safe_read(f)
            if content is None:
                continue
            heading = next((line.removeprefix("# ").strip() for line in content.splitlines() if line.startswith("# ")), folder.name)
            first_section = content.split("\n## ", 1)[1].split("\n## ", 1)[0] if "\n## " in content else content[:2000]
            topic = first_section.splitlines()[0].strip()[:120]
            status, tone = project_status(first_section, folder.name)
            # Do not reproduce arbitrary source paragraphs, emails, tokens, or local paths.
            path = f"collab/projects/{folder.name}/CURRENT.md"
            projects.append({"id": folder.name, "title": heading[:140], "topic": topic,
                             "status": status, "tone": tone, "source": path,
                             "next_action": "CURRENT.md 원문에서 담당·다음 행동 확인"})
    # File counts are not reviewed/approved status. Missing files are UNKNOWN, not zero completed.
    transport = {}
    for family, target in (("requests", "REQUEST.md"), ("reviews", "REVIEW_RESULT_1.md"),
                           ("receipts", "RECEIPT_1.md")):
        base = root / "collab" / family
        n = 0
        if base.is_dir():
            n = sum(1 for d in base.iterdir() if d.is_dir() and not d.is_symlink() and
                    PROJECT_NAME.fullmatch(d.name) and safe_read(d / target, 300_000) is not None)
        transport[family] = {"files_observed": n, "verified": False,
                             "note": "GitHub 문서만 집계 · Dropbox LIVE/서명/영수증 검증 아님"}
    return {"review_chains": review_chain.collect(root), "schema": "COWORK_GITHUB_DASHBOARD_SHADOW_V2",
            "phase": "MIGRATION_NOT_CUTOVER", "live_provider": "DROPBOX",
            "visibility": "PRIVATE_REPO_ONLY", "source": "GITHUB_TRACKED_FILES_ONLY",
            "disclaimer": "GitHub SHADOW 현황. 미이관 자료는 0건이 아니라 미확인입니다.",
            "projects": projects, "transport": transport}


def url_for(repo: str, path: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo):
        raise ValueError("invalid repository slug")
    if not path.startswith("collab/projects/") or not path.endswith("/CURRENT.md") or ".." in path:
        raise ValueError("invalid source path")
    return "https://github.com/" + repo + "/blob/main/" + quote(path, safe="/")


def render_html(state: dict, repo: str = REPO) -> str:
    cards = []
    for p in state["projects"]:
        e = html.escape
        href = html.escape(url_for(repo, p["source"]), quote=True)
        cards.append(f'''<article class="card" data-search="{e((p['title']+' '+p['id']+' '+p['topic']).lower(), quote=True)}">
  <div class="card-top"><span class="pill {e(p['tone'])}">{e(p['status'])}</span><span class="minor">GitHub 문서 기준</span></div>
  <h2>{e(p['title'])}</h2><p class="topic">{e(p['topic'])}</p>
  <p class="next">{e(p['next_action'])}</p>
  <a href="{href}" rel="noopener noreferrer">CURRENT.md에서 근거 확인</a>
</article>''')
    count = len(state["projects"])
    reqs = state["transport"]["requests"]["files_observed"]
    reviews = state["transport"]["reviews"]["files_observed"]
    receipts = state["transport"]["receipts"]["files_observed"]
    grid = "\n".join(cards) if cards else '<p class="empty">GitHub에서 확인되는 CURRENT.md가 없습니다. 미이관 상태를 0건 완료로 보지 않습니다.</p>'
    return f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow,noarchive"><title>CoWork · GitHub SHADOW 현황</title>
<style>
:root{{--bg:#f4f7fb;--paper:#fff;--ink:#172840;--muted:#50627a;--border:#dfe6ef;--blue:#234c86;--focus:#176dcd}}*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);font:15px/1.6 system-ui,'Malgun Gothic',sans-serif;color:var(--ink)}}main{{max-width:1120px;margin:auto;padding:26px 20px 72px}}h1{{font-size:clamp(24px,3vw,34px);margin:0}}h2{{font-size:18px;line-height:1.4;overflow-wrap:anywhere}}a{{color:var(--blue);text-underline-offset:3px}}a:focus-visible,input:focus-visible{{outline:3px solid var(--focus);outline-offset:3px}}
.header{{display:flex;align-items:flex-start;justify-content:space-between;gap:15px;flex-wrap:wrap}}.overline{{font-weight:800;letter-spacing:.1em;color:var(--blue);font-size:12px}}.sub,.minor,.topic{{color:var(--muted)}}.banner{{border:1px solid #d2dceb;background:#eef3fa;border-radius:13px;padding:15px 18px;margin:19px 0}}.banner strong{{display:block}}.stats{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:20px 0}}.stat{{background:white;border:1px solid var(--border);padding:15px;border-radius:13px}}.stat strong{{display:block;font-size:26px}}.stat span{{font-size:12px;color:var(--muted)}}.toolbar{{display:flex;justify-content:space-between;gap:14px;align-items:center;flex-wrap:wrap;margin:26px 0 14px}}input{{border:1px solid #bccada;border-radius:10px;padding:12px;font:inherit;width:min(100%,340px);background:white}}.grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}}.card{{background:var(--paper);border:1px solid var(--border);border-radius:16px;padding:18px;min-width:0}}.card-top{{display:flex;align-items:center;justify-content:space-between;gap:8px}}.pill{{border-radius:100px;background:#eaf0f7;color:#284a70;padding:5px 10px;font-size:12px;font-weight:750}}.pill.warning{{background:#fff0d9;color:#80500c}}.pill.danger{{background:#ffe8e8;color:#9b2222}}.next{{border-top:1px solid var(--border);padding-top:12px}}.empty{{padding:25px;background:white;border-radius:12px}}footer{{margin-top:30px;color:var(--muted);font-size:13px}}[hidden]{{display:none!important}}@media(max-width:740px){{.grid{{grid-template-columns:1fr}}.stats{{grid-template-columns:repeat(2,minmax(0,1fr))}}main{{padding:18px 14px 50px}}}}
</style></head><body><main>
<div class="header"><div><div class="overline">COWORK · GITHUB PRIVATE / READ-ONLY DASHBOARD</div><h1>협업 진행 현황</h1><p class="sub">프로젝트 CURRENT.md와 GitHub에 게시된 파일 기준 · 운영 실행 근거와 구별</p></div><span class="pill warning">MIGRATION_NOT_CUTOVER</span></div>
<section class="banner" aria-label="중요 운영 상태"><strong>기존 Dropbox LIVE 유지 · GitHub SHADOW</strong><span>이 화면은 코드 리뷰 실행·배포·LIVE 전환을 수행하지 않습니다. GitHub로 이관되지 않은 자료는 아직 확인할 수 없습니다.</span></section>
<section class="stats" aria-label="GitHub 관측 파일 수"><div class="stat"><strong>{count}</strong><span>현재 문서가 있는 프로젝트</span></div><div class="stat"><strong>{reqs}</strong><span>GitHub 요청 파일 수 (검증 아님)</span></div><div class="stat"><strong>{reviews}</strong><span>GitHub 결과 파일 수 (검증 아님)</span></div><div class="stat"><strong>{receipts}</strong><span>GitHub 영수증 파일 수 (검증 아님)</span></div></section>
<div class="toolbar"><h2>진행 중인 Work</h2><label>프로젝트 검색 <input id="search" type="search" placeholder="Work 이름 또는 키워드" autocomplete="off"></label></div>
<div class="grid" id="cards">{grid}</div><p id="zero" class="empty" hidden>검색 결과가 없습니다.</p>
{review_chain.render_html(state["review_chains"], repo)}
<footer>개발·현황 확인용 PRIVATE 출력입니다. Windows Claude 리뷰·호스트 설치·운영 DB·GitHub PUBLIC 및 Pages를 변경하지 않습니다. 표시된 상태는 소스 문서의 주장입니다.</footer>
</main><script>
const box=document.getElementById('search'),cards=Array.from(document.querySelectorAll('.card')),zero=document.getElementById('zero');
box.addEventListener('input',()=>{{const q=box.value.toLocaleLowerCase('ko');let n=0;for(const c of cards){{const show=c.dataset.search.includes(q);c.hidden=!show;if(show)n++;}}zero.hidden=n>0;}});
</script></body></html>
'''


def render_summary(state: dict, repo: str = REPO) -> str:
    lines = ["# CoWork GitHub SHADOW 대시보드", "", "> **MIGRATION_NOT_CUTOVER** — 운영은 Dropbox LIVE 유지. GitHub 데이터만 표시합니다.",
             "", "이 문서는 GitHub Actions가 생성하는 안내 화면이며 리뷰·설치·배포 승인이나 자동 실행 결과가 아닙니다.", "",
             f"- 문서가 있는 프로젝트: **{len(state['projects'])}개**",
             f"- GitHub REQUEST 파일 관측: **{state['transport']['requests']['files_observed']}개** (검증 안 됨)",
             f"- GitHub REVIEW 파일 관측: **{state['transport']['reviews']['files_observed']}개** (검증 안 됨)",
             f"- GitHub RECEIPT 파일 관측: **{state['transport']['receipts']['files_observed']}개** (검증 안 됨)", "",
             "| 프로젝트 | 문서상 상태 | 근거 |", "|---|---|---|"]
    for p in state["projects"]:
        clean = lambda s: s.replace("|", "\\|").replace("\n", " ")
        lines.append(f"| {clean(p['id'])} | {clean(p['status'])} | [CURRENT.md]({url_for(repo,p['source'])}) |")
    lines += ["", "미이관 파일이나 승인·서명 검증 결과가 없어도, 이 화면은 이를 임의로 성공/0건 완료 처리하지 않습니다.", ""]
    lines.append(review_chain.render_markdown(state["review_chains"], repo))
    return "\n".join(lines)


def write_outputs(root: Path, repo: str = REPO) -> dict:
    state = build_state(root, repo)
    out = root / "collab" / "dashboard"
    out.mkdir(parents=True, exist_ok=True)
    (out / "state.json").write_text(json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "index.html").write_text(render_html(state, repo), encoding="utf-8")
    (out / "SUMMARY.md").write_text(render_summary(state, repo), encoding="utf-8")
    return state


if __name__ == "__main__":
    argp = argparse.ArgumentParser()
    argp.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    argp.add_argument("--repo", default=REPO)
    args = argp.parse_args()
    result = write_outputs(args.root, args.repo)
    print("GitHub shadow dashboard built", len(result["projects"]), "projects")
