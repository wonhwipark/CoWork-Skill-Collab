#!/usr/bin/env python3
"""Pinned Kernel derived Work MSC HTML link projection; development ONLY."""
from __future__ import annotations
import argparse, hashlib, json, compileall, tempfile
from pathlib import Path
from build_l1_knowledge_guard_candidates_r0001_20261117 import safe_unzip, refresh_package_metadata, rezip
from skill_release_quality_gate import validate

VERSION_FROM="0.7.43"
VERSION_TO="0.7.44"
OUT_NAME="work-ledger-kernel_v0_7_44_1118.zip"
EXPECTED_SHA="80c955790aaa65f695c061f7ec2664bd1c7c5ba7e0a7534045960eea7fe2d5f6"
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def once(path,before,after):
    s=path.read_text(encoding="utf-8")
    if s.count(before)!=1:raise RuntimeError("ANCHOR_AMBIGUOUS:"+str(path)+":"+str(s.count(before)))
    path.write_text(s.replace(before,after),encoding="utf-8",newline="\n")

def patch(root):
    p=root/"work_ledger_kernel/work_ux.py"
    once(p,"            msc_artifacts: list[str] = []\n",
         "            msc_artifacts: list[str] = []\n"
         "            msc_html_artifacts: list[str] = []  # published and SHA-checked\n")
    before="""                    if src.suffix.lower() == '.md' and 'MSC_VIEW' in src.stem.upper():
                        msc_artifacts.append(artifact_rel)
"""
    after=before+"""                    if (src.suffix.lower() == '.html'
                            and str(e.get('provider') or '').casefold() == 'doc-converter'):
                        msc_html_artifacts.append(artifact_rel)
"""
    once(p,before,after)
    before="""                msc_lines += ["- [변경 전후 MSC와 설명 보기]("+quote(path,safe='/')+")" for path in sorted(set(msc_artifacts))]
                msc_lines += ["", "## 확인할 내용", "", "- 시작 조건, 주요 변경 순서, 분리된 예외 흐름과 검증 근거를 확인하세요.", ""]
"""
    after="""                msc_lines += ["- [MSC 상세 원본]("+quote(path,safe='/')+")" for path in sorted(set(msc_artifacts))]
                if msc_html_artifacts:
                    msc_lines += ["", "## MSC HTML 다운로드", "",
                                  "> 아래 HTML 링크는 이 Work의 실제 Evidence에서 SHA를 대조해 게시한 경로입니다. 브라우저 표시 확인은 별도입니다.", ""]
                    msc_lines += ["- [MSC HTML 다운로드]("+quote(path,safe='/')+")"
                                  for path in sorted(set(msc_html_artifacts))]
                msc_lines += ["", "## 확인할 내용", "", "- 시작 조건, 주요 변경 순서, 분리된 예외 흐름과 검증 근거를 확인하세요.", ""]
"""
    once(p,before,after)
    sk=root/"SKILL.md"
    sk.write_text(sk.read_text(encoding="utf-8")+
        "\n\n### MSC Work-root 안내 링크 정합성 (개발 후보 0.7.44)\n"
        "- 기존 Work-root MSC_VIEW.md는 Kernel writer만 관리. Converter 상세 MSC_VIEW.md Evidence bytes 불변.\n"
        "- 실제 게시된 doc-converter HTML Evidence의 published_path를 같은 Work 안내에 MSC HTML 다운로드 링크로 표시.\n"
        "- 수동 편집/기존 생성 해시 불일치 시 기존 write_communication 정책대로 보류. 개인 knowledge/ 쓰기 없음.\n"
        "- 브라우저 렌더·업무 호스트 설치·Updater/group writer 검증을 주장하지 않음.\n",encoding="utf-8")
    refresh_package_metadata(root,dict(version_from=VERSION_FROM,version_to=VERSION_TO,output=OUT_NAME))

def run(source,outdir):
    actual=digest(source)
    if actual!=EXPECTED_SHA:raise RuntimeError("KERNEL_SOURCE_SHA_MISMATCH:"+actual)
    outdir.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="kernel-html-link-builder-") as t:
        extracted=Path(t)/"kernel";extracted.mkdir()
        safe_unzip(source,extracted)
        if not (extracted/"work_ledger_kernel/work_ux.py").is_file():
            raise RuntimeError("KERNEL_EXPECTED_ROOT_NOT_FOUND")
        patch(extracted)
        if not compileall.compile_dir(extracted,quiet=1):raise RuntimeError("KERNEL_COMPILE_FAILED")
        output=outdir/OUT_NAME
        rezip(extracted,output)
        qa=validate(output,VERSION_TO)
        record={"archive":OUT_NAME,"sha256":digest(output),"bytes":output.stat().st_size,
                "input_sha256":actual,"gate":qa,"channel":"development_not_for_deployment"}
        (outdir/"KERNEL_MSC_LINK_BUILD_RESULT.json").write_text(
            json.dumps(record,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
        print("KERNEL_MSC_LINK_BUILD_SUCCESS",json.dumps(record,sort_keys=True))
        return record

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--source",required=True,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args()
    run(a.source,a.out)
