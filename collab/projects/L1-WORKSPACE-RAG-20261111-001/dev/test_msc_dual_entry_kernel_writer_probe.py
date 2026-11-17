#!/usr/bin/env python3
"""Non-mutating-to-remote synthetic Kernel HTML+MSC_VIEW writer G0 probe.

This test creates a disposable local Work and does NOT assert that the business
writer/updater/Knowledge host is installed or supports HTML. It records actual
Kernel behavior and returns BLOCKED if the expected HTML link is not published.
"""
from __future__ import annotations
import hashlib
import json
import os
import sys
import tempfile
import zipfile
from pathlib import Path

ARCHIVE = Path(os.environ["KERNEL_TEST_ARCHIVE"])

def run():
    with tempfile.TemporaryDirectory(prefix="msc-writer-g0-") as tmp:
        base=Path(tmp)
        root=base/"package"; root.mkdir()
        with zipfile.ZipFile(ARCHIVE) as z:
            assert z.testzip() is None
            z.extractall(root)
        sys.path.insert(0,str(root))
        from work_ledger_kernel.kernel import WorkLedgerKernel
        k=WorkLedgerKernel(base/"ledger")
        wid=k.work_create("Synthetic MSC HTML link",profile="BUG")["work_id"]
        fixtures=base/"input";fixtures.mkdir()
        html=fixtures/"01_AS_IS.html"
        html.write_text('<!doctype html><html><body>TEST_ONLY_NO_PRODUCTION_DATA</body></html>',encoding="utf-8")
        md=fixtures/"MSC_VIEW.md"
        md.write_text("# MSC 상세 원본\\n\\n[MSC HTML 다운로드](01_AS_IS.html)\\n",encoding="utf-8")
        e=[]
        for p,kind in ((html,"render_output"),(md,"asis_msc")):
            try:
                record=k.record_evidence(wid,p,kind,"utility","doc-converter","0.2.27",
                                         "synthetic-rev","Synthetic only","AUTO_CANDIDATE")
                e.append({"file":p.name,"kind":kind,"status":"PASS","record":str(record)[:280]})
            except Exception as exc:
                e.append({"file":p.name,"kind":kind,"status":"BLOCKED",
                          "reason":type(exc).__name__+":"+str(exc)[:200]})
        dest=base/"published"
        try:
            export=k.work_docs_export(str(dest),wid)
            export_status={"ok":export.get("ok"),"changed":len(export.get("changed_files") or [])}
        except Exception as exc:
            export_status={"ok":False,"reason":type(exc).__name__+":"+str(exc)[:200]}
        files=[str(p.relative_to(dest)) for p in dest.rglob("*") if p.is_file()] if dest.exists() else []
        htmls=sorted(p for p in dest.rglob("*.html") if p.is_file()) if dest.exists() else []
        html_hashes=[hashlib.sha256(p.read_bytes()).hexdigest() for p in htmls]
        correct=hashlib.sha256(html.read_bytes()).hexdigest() in html_hashes
        mappings=[]
        for p in dest.rglob("*.json") if dest.exists() else []:
            if "artifact" not in p.name.lower(): continue
            try: mappings.extend(json.loads(p.read_text(encoding="utf-8")).get("entries",[]))
            except (ValueError,OSError): pass
        actual_mapping=any(x.get("sha256")==hashlib.sha256(html.read_bytes()).hexdigest()
                           and str(x.get("published_path","")).endswith(".html")
                           for x in mappings)
        status=("PASS" if correct and actual_mapping else "BLOCKED")
        result={"status":status,"scope":"SYNTHETIC_KERNEL_WRITER_ONLY",
                "record_evidence":e,"work_docs_export":export_status,
                "html_published":correct,"html_mapping":actual_mapping,
                "files":files[:35],"updater_g0":"NOT_VERIFIED",
                "group_writer_g0":"NOT_VERIFIED","business_host_e3":"NOT_RUN"}
        print("MSC_KERNEL_WRITER_G0_PROBE",json.dumps(result,ensure_ascii=False,sort_keys=True))
        return 0  # A blocked probe is evidence, not a CI regression in existing Kernel.

if __name__=="__main__":
    sys.exit(run())
