#!/usr/bin/env python3
"""Build pinned development-only MSC dual-entry candidates from existing skills.

No group/workspace writes, public delivery, host installation, reviewer call,
approval, schema migration or runtime provider changes.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib
import json
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path
from unittest import mock
from argparse import Namespace

from build_l1_knowledge_guard_candidates_r0001_20261117 import (
    safe_unzip, refresh_package_metadata)
from reproducible_zip import rezip
from skill_release_quality_gate import validate as release_validate

BASE_SHA256 = "b0ebd0aa4d771adc30648ab2bce23a3c1648e408984bedb36d0e3da45108312c"
WORKFLOW_SHA256 = "1e08302b6a533d2894101427f5a7bb94b43102e00a98f2c6e0b19f534a885ceb"
CONVERTER_VERSION = "0.2.28"
WORKFLOW_VERSION = "1.6.72"
FLAG = "--html-viewer"

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def replace_once(path: Path, before: str, after: str):
    t=path.read_text(encoding="utf-8")
    if t.count(before)!=1:
        raise RuntimeError(f"AMBIGUOUS_SOURCE_ANCHOR:{path.name}:{before[:70]} count={t.count(before)}")
    path.write_text(t.replace(before,after),encoding="utf-8",newline="\n")

def patch_converter(root: Path):
    m=root/"scripts/msc_tool.py"
    replace_once(m,
        'if render["ok"] and view_mode == "PROCEDURE_FEATURE":',
        'if render["ok"] and (view_mode == "PROCEDURE_FEATURE" or bool(getattr(ns, "html_viewer", False))):')
    replace_once(m,
        'json=ns.json, view_mode=getattr(ns, "view_mode", None), _payload=package)',
        'json=ns.json, view_mode=getattr(ns, "view_mode", None), html_viewer=bool(getattr(ns, "html_viewer", False)), _payload=package)')
    for var,func in (("ab","cmd_scenario_build"),("b","cmd_package")):
        before=f'{var}.set_defaults(func={func})'
        after=f'{var}.add_argument("{FLAG}",action="store_true"); {before}'
        replace_once(m,before,after)
    policy_file=root/"skillsilent/policy.json"
    policy=json.loads(policy_file.read_text(encoding="utf-8"))
    for name in ("msc-package","msc-scenario-build"):
        a=policy["actions"][name]
        if any(FLAG in a[k] for k in ("allowed_flags","value_flags","boolean_flags")):
            raise RuntimeError("FLAG_ALREADY_PRESENT:"+name)
        a["allowed_flags"].append(FLAG)
        a["boolean_flags"].append(FLAG)
    policy_file.write_text(json.dumps(policy,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    sk=root/"SKILL.md"
    sk.write_text(sk.read_text(encoding="utf-8")+"\n\n### MSC 독립 HTML 선택 출력 (개발 후보 0.2.28)\n"
      "- `--view-mode ISSUE`의 이슈/AS-IS/TO-BE 문서 의미는 유지. 명시적 `--html-viewer`일 때에만 B HTML 추가 생성.\n"
      "- `PROCEDURE_FEATURE`의 기존 HTML 기본 출력은 유지. 다른 action 및 기본 ISSUE 호출은 무변경.\n"
      "- SVG 렌더 성공 시에만 HTML/manifest 경로 기록. Converter는 Git/Knowledge writer가 아님.\n"
      "- Work-root MSC 작업 안내와 Converter MSC 상세 원본은 서로 다른 역할. 게시 경로와 열람 URL은 최종 writer/readback 확인 후 확정.\n",encoding="utf-8")
    refresh_package_metadata(root,dict(version_from="0.2.26",version_to=CONVERTER_VERSION,
                               output="doc-converter_v0_2_28_1118.zip"))

def patch_workflow(root: Path):
    p=root/"l1_fix_workflow/scenario_msc.py"
    replace_once(p,
        "'profile':'L1_USER_SCENARIO','allow_unrendered':True,",
        "'profile':'L1_USER_SCENARIO','allow_unrendered':True,\n"
        "                       'view_mode':'ISSUE','html_viewer_flag':'--html-viewer',\n"
        "                       'html_viewer_opt_in':True,")
    sk=root/"SKILL.md"
    sk.write_text(sk.read_text(encoding="utf-8")+"\n\n### MSC 이슈 HTML 전달 (개발 후보 1.6.72)\n"
       "- 기존 Work MSC 요청은 `ISSUE` 목적을 유지하고, 검증된 scenario IR가 있을 때 doc-converter `msc-scenario-build --view-mode ISSUE --html-viewer`를 전달하는 **계획**만 생성.\n"
       "- 실제 CLI 실행은 승인된 기존 Agent/runner가 담당. Updater 선행 호출/지식 자동 쓰기/Work 신규 발급을 요구하지 않음.\n"
       "- Work MSC 작업 안내/Converter MSC 상세 원본/HTML 확대 보기 또는 다운로드 표기 구분. 실제 URL은 최종 writer가 게시 후 검증.\n"
       "- 수동 문서의 단일 writer 마커·revision 미확인 및 충돌은 Preview/HOLD. 자동 덮어쓰기 금지.\n",encoding="utf-8")
    refresh_package_metadata(root,dict(version_from="1.6.70",version_to=WORKFLOW_VERSION,
                               output="l1-fix-workflow_v1_6_72_1118.zip"))

def verify_converter(root: Path) -> dict:
    scripts=root/"scripts"
    sys.path.insert(0,str(scripts))
    try:
        for name in ("msc_tool","direct_gateway"):
            if name in sys.modules:del sys.modules[name]
        m=importlib.import_module("msc_tool")
        g=importlib.import_module("direct_gateway")
        p=m.build_parser()
        for action in ("package","scenario-build"):
            ns=p.parse_args([action,"--input","x.json","--output-dir","out",FLAG])
            assert ns.html_viewer is True
            plain=p.parse_args([action,"--input","x.json","--output-dir","out"])
            assert plain.html_viewer is False
        policy=json.loads((root/"skillsilent/policy.json").read_text(encoding="utf-8"))
        for action in ("msc-package","msc-scenario-build"):
            meta=policy["actions"][action]
            assert FLAG in meta["allowed_flags"] and FLAG in meta["boolean_flags"]
            assert FLAG not in meta["value_flags"]
            assert g.validate_child_args(meta,["--input","x.json","--output-dir","out",FLAG])[0]
            assert not g.validate_child_args(meta,["--input","x.json","--output-dir","out","--not-allowed"])[0]
        spec={"schema":"doc-converter/msc-spec/v1","kind":"AS_IS","title":"Synthetic",
              "participants":[{"id":"L1"},{"id":"RF"}],
              "steps":[{"type":"divider","label":"INIT"},
                       {"type":"message","id":"S1","from":"L1","to":"RF",
                        "label":"SYNTH_REQ","evidence_status":"CODE_CONFIRMED"}]}
        def renderer(_p,svg,**_kw):
            svg.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200"><text x="20" y="60">INIT</text></svg>',encoding="utf-8")
            return {"ok":True,"status":"READY"}
        cases=[]
        for mode,flag,expected in [("ISSUE",False,False),("ISSUE",True,True),
                                   ("PROCEDURE_FEATURE",False,True)]:
            with tempfile.TemporaryDirectory(prefix="msc-dual-test-") as t:
                out=Path(t)/"out";out.mkdir()
                package={"schema":"doc-converter/msc-package/v1","issue_id":"SYNTHETIC",
                         "view_mode":mode,"diagrams":[{"name":"01_AS_IS","spec":spec}]}
                ns=Namespace(input=str(Path(t)/"input.json"),output_dir=str(out),
                             overwrite=False,allow_unrendered=False,timeout=5,json=True,
                             view_mode=mode,html_viewer=flag,_payload=package)
                with mock.patch.object(m,"_render_puml",side_effect=renderer):
                    code=m.cmd_package(ns)
                assert code==0,(mode,flag,code)
                manifest=json.loads((out/"MSC_MANIFEST.json").read_text(encoding="utf-8"))
                row=manifest["diagrams"][0]
                assert ("html" in row)==expected,(mode,flag,row)
                assert (out/"01_AS_IS.html").is_file()==expected,(mode,flag)
                view=(out/"MSC_VIEW.md").read_text(encoding="utf-8")
                assert ("**문제:**" in view)==(mode=="ISSUE"),mode
                public=json.loads((out/"MSC_PUBLIC_MANIFEST.json").read_text(encoding="utf-8"))
                assert (public["diagrams"][0]["html"] is not None)==expected
                cases.append(f"{mode}/optin={flag}/html={expected}")
        # scenario-build action preserves the opt-in when it delegates to package.
        with tempfile.TemporaryDirectory(prefix="msc-scenario-pass-") as t:
            pth=Path(t)/"ir.json"
            pth.write_text(json.dumps({"schema":"l1-scenario-ir/v1"}),encoding="utf-8")
            with mock.patch.object(m,"_json_load",return_value={"schema":"l1-scenario-ir/v1"}):
                adapter=importlib.import_module("scenario_ir_adapter")
                with mock.patch.object(adapter,"adapt_scenario_ir",return_value={"schema":"doc-converter/msc-package/v1","diagrams":[{"name":"A","spec":spec}]}):
                    captured=[]
                    with mock.patch.object(m,"cmd_package",side_effect=lambda ns: captured.append(ns) or 0):
                        ns=Namespace(input=str(pth),output_dir=str(Path(t)/"out"),
                                     overwrite=False,allow_unrendered=True,timeout=5,json=True,
                                     view_mode="ISSUE",html_viewer=True)
                        assert m.cmd_scenario_build(ns)==0
                        assert captured[0].view_mode=="ISSUE" and captured[0].html_viewer is True
        cases.append("scenario-build/pass-through")
        return {"status":"PASS","cases":cases,"managed_policy":2,"version":CONVERTER_VERSION}
    finally:
        sys.path.remove(str(scripts))
        for name in ("msc_tool","direct_gateway","scenario_ir_adapter"):
            sys.modules.pop(name,None)

def verify_workflow(root: Path) -> dict:
    sys.path.insert(0,str(root))
    try:
        from l1_fix_workflow.scenario_msc import build_msc_handoff
        a=build_msc_handoff("CREATE","Synthetic issue MSC","WORK-SYNTHETIC",{})
        c=a["artifact_pipeline"]["convert"]
        assert a["actual_execution"]=="NOT_STARTED"
        assert c["view_mode"]=="ISSUE" and c["html_viewer_opt_in"] is True
        assert c["html_viewer_flag"]==FLAG
        assert c["one_shot_action"]=="msc-scenario-build"
        assert a["publication"]["github_push"] is False
        return {"status":"PASS","cases":["existing-work plan only","no implicit publisher","ISSUE HTML opt-in handoff"]}
    finally:
        sys.path.remove(str(root))
        for name in list(sys.modules):
            if name=="l1_fix_workflow" or name.startswith("l1_fix_workflow."):del sys.modules[name]

def run(source: Path, workflow: Path, output: Path):
    assert sha(source)==BASE_SHA256,("CONVERTER_PIN_MISMATCH",sha(source))
    assert sha(workflow)==WORKFLOW_SHA256,("WORKFLOW_PIN_MISMATCH",sha(workflow))
    output.mkdir(parents=True,exist_ok=True)
    result={}
    with tempfile.TemporaryDirectory(prefix="msc-dual-candidates-") as t:
        work=Path(t)
        for key,archive,root_name,version,out_name,patch,test in [
            ("doc-converter",source,"doc-converter",CONVERTER_VERSION,"doc-converter_v0_2_28_1118.zip",patch_converter,verify_converter),
            ("l1-fix-workflow",workflow,"l1-fix-workflow",WORKFLOW_VERSION,"l1-fix-workflow_v1_6_72_1118.zip",patch_workflow,verify_workflow)]:
            extraction=work/key;extraction.mkdir()
            safe_unzip(archive,extraction)
            root=extraction/root_name
            assert root.is_dir(),("ROOT_MISSING",root_name)
            patch(root)
            verified=test(root)
            import compileall
            assert compileall.compile_dir(root,quiet=1),("PY_COMPILE_FAILED",key)
            dest=output/out_name
            rezip(extraction,dest)
            quality=release_validate(dest,version)
            result[key]={"archive":out_name,"sha256":sha(dest),"size_bytes":dest.stat().st_size,
                         "version":version,"tests":verified,"release_gate":quality,
                         "channel":"development_not_for_deployment"}
    (output/"MSC_DUAL_ENTRY_BUILD_RESULT.json").write_text(
        json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("MSC_DUAL_ENTRY_BUILD_SUCCESS")
    print(json.dumps(result,ensure_ascii=False,sort_keys=True))
    return result

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--converter",required=True,type=Path)
    ap.add_argument("--workflow",required=True,type=Path)
    ap.add_argument("--out",required=True,type=Path)
    ns=ap.parse_args()
    run(ns.converter,ns.workflow,ns.out)
