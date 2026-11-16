"""Release-scope direct OpenCode-oriented skill API + Work/Evidence export regression.
Private synthetic fixtures only, zero LLM/model/host and zero skillsilent.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest.mock
import zipfile

ROOT=Path(__file__).resolve().parents[1]
CANDS=ROOT/"candidates"
PRESETS=[
    ("doc-converter_v0_2_24_1116.zip","2ef0929bc0a80a1c0aca67bf3c8fc02f967bddba223b45c27807c363e96229f7"),
    ("work-ledger-kernel_v0_7_41_1116.zip","48d1bf5e24c613e7e0ba04df9946c427c5d1ee39d8d16204966afff07e93497b"),
]

def check(flag,name,note=""):
    if not flag: raise AssertionError(name+": "+str(note))
    print("PASS | "+name+" "+str(note),flush=True)

def unpack(name,expected,dest):
    data=(CANDS/name).read_bytes()
    check(hashlib.sha256(data).hexdigest()==expected,"base-SHA256",name)
    with zipfile.ZipFile(CANDS/name) as z:
        check(z.testzip() is None,"zip-crc",name)
        z.extractall(dest)

def run():
    with tempfile.TemporaryDirectory(prefix="msc-public-release-qa-") as td:
        sandbox=Path(td)
        for name,expected in PRESETS:
            unpack(name,expected,sandbox/name.rsplit(".zip",1)[0])
        converter=(sandbox/"doc-converter_v0_2_24_1116"/"doc-converter")
        kernel=(sandbox/"work-ledger-kernel_v0_7_41_1116")
        sys.path.insert(0,str(kernel))
        sys.path.insert(0,str(converter/"scripts"))
        from work_ledger_kernel.kernel import WorkLedgerKernel
        from work_ledger_kernel.errors import KernelError
        from work_ledger_kernel.work_ux import WorkUX
        import msc_tool
        check(True,"import-kernel-converter-direct-no-skillsilent")
        # Inspect actual registry, never invent a provider/kind/stage tuple.
        storage=sandbox/"ledger"
        k=WorkLedgerKernel(storage)
        profile="BUG"
        w="MSC-TEST-001"
        k.new(w,profile,"synthetic, publish-safe MSC regression")
        slots=k._slots(profile=profile)
        check(bool(slots),"kernel-registry-has-profiles",len(slots))
        print("REGISTRY_SAFE_CHOICES",json.dumps(slots,ensure_ascii=False)[:3600],flush=True)
        excluded={"oracle_manifest","eval_baseline","tooling_baseline","baseline_measure","change_provenance","eval_after","tooling_after","after_measure"}
        eligible=[x for x in slots if x.get("kind") not in excluded and x.get("provider") and x.get("kind") and x.get("stage")]
        check(bool(eligible),"kernel-registry-has-evidence-kind",len(eligible))
        chosen=next((x for x in eligible if x.get("provider") in ("doc-converter","code-analyzer")),eligible[0])
        def register(filename,text,work_id=w):
            source=sandbox/filename
            source.write_text(text,encoding="utf-8")
            kw={key:chosen[key] for key in ("provider","kind","stage")}
            result=k.record_evidence(work_id,source_path=source,**kw,provider_version="release-regression",code_rev="test-synthetic",summary="synthetic test",confidence_state="AUTO_CANDIDATE")
            check(bool(result),"kernel-real-register-evidence",filename)
            return result
        goodsvg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y="30">INIT</text></svg>'
        register("MSC_INIT.svg",goodsvg)
        register("NOT_A_DIAGRAM.svg",goodsvg)
        register("notes.md","# Synthetic test\n")
        root=sandbox/"public-work-view"
        result=k.work_docs_export(str(root),work_id=w)
        check(isinstance(result,dict),"kernel-real-work_docs_export",str(result)[:260])
        path=root/"works"/w
        map_path=path/"state"/"artifact_publish_map.json"
        check(map_path.exists(),"kernel-published-map-exists")
        obj=json.loads(map_path.read_text(encoding="utf-8"))
        names=[x["published_path"] for x in obj["entries"]]
        check(any(x.endswith(".svg") for x in names),"kernel-msc-svg-published",names)
        check(any(x.endswith(".md") for x in names),"kernel-md-unchanged",names)
        check(not any("NOT_A_DIAGRAM" in x for x in names),"kernel-unrelated-svg-skipped",names)
        for x in obj["entries"]:
            data=(path/x["published_path"]).read_bytes()
            check(hashlib.sha256(data).hexdigest()==x["sha256"],"kernel-published-sha",x["published_path"])
        second=k.work_docs_export(str(root),work_id=w)
        check(isinstance(second,dict),"kernel-export-idempotent",str(second)[:150])

        w2="MSC-TEST-002";k.new(w2,profile,"oversize synthetic MSC")
        register("MSC_LARGE.svg",goodsvg+("x"*2000),work_id=w2)
        try:
            WorkUX(k).export_docs(str(sandbox/"public-oversize"),work_id=w2,max_copy_bytes=300)
        except KernelError as exc:
            check("MSC_SVG_TOO_LARGE" in str(exc) or getattr(exc,"code",None)=="MSC_SVG_TOO_LARGE","kernel-oversize-fails-closed",str(exc)[:160])
        else:
            raise AssertionError("kernel-oversize-must-block")

        w3="MSC-TEST-003";k.new(w3,profile,"bad SVG synthetic")
        register("MSC_UNSAFE.svg",'<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script></svg>',work_id=w3)
        try:
            WorkUX(k).export_docs(str(sandbox/"public-unsafe"),work_id=w3)
        except KernelError as exc:
            check("MSC_SVG_UNSAFE" in str(exc) or getattr(exc,"code",None)=="MSC_SVG_UNSAFE","kernel-active-svg-fails-closed")
        else:
            raise AssertionError("kernel-unsafe-must-block")

        # OpenCode calls the converter CLI directly, not via skillsilent.
        proc=subprocess.run([sys.executable,str(converter/"scripts"/"msc_tool.py"),"package","--help"],cwd=converter,text=True,capture_output=True)
        check(proc.returncode==0 and "--view-mode" in proc.stdout,"converter-direct-cli-options",proc.stderr[:180])
        spec={
            "schema":"doc-converter/msc-spec/v1","title":"Synthetic", "kind":"AS_IS",
            "participants":[{"id":"L1","label":"L1"},{"id":"RF","label":"RF"}],
            "steps":[{"type":"divider","label":"INIT"},{"type":"message","id":"S1","from":"L1","to":"RF","label":"REQ","evidence_status":"CODE_CONFIRMED"}]}
        pkg=sandbox/"pkg.json"
        pkg.write_text(json.dumps({"schema":"doc-converter/msc-package/v1","issue_id":"SYNTHETIC","view_mode":"PROCEDURE_FEATURE","diagrams":[{"name":"초기화","spec":spec}]},ensure_ascii=False),encoding="utf-8")
        dest=sandbox/"converter-direct"
        proc=subprocess.run([sys.executable,str(converter/"scripts"/"msc_tool.py"),"package","--input",str(pkg),"--output-dir",str(dest),"--view-mode","PROCEDURE_FEATURE","--allow-unrendered","--json"],cwd=converter,text=True,capture_output=True)
        check(proc.returncode==0,"converter-direct-cli-package",proc.stdout[-300:]+" "+proc.stderr[-160:])
        manifest=json.loads((dest/"MSC_PUBLIC_MANIFEST.json").read_text(encoding="utf-8"))
        check(manifest.get("diagrams") is not None,"converter-direct-manifest")
        check((dest/"MSC_VIEW.md").is_file(),"converter-direct-markdown")
        print("RELEASE_RUNTIME_GATE=PASS",flush=True)

if __name__=="__main__":
    run()
