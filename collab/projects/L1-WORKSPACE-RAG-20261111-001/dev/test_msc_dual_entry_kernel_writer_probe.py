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
        # Inspects the already published development skill; never reads business code.
        source=root/"work_ledger_kernel"/"work_ux.py"
        if source.is_file():
            lines=source.read_text(encoding="utf-8").splitlines()
            hits=[i for i,line in enumerate(lines) if any(
                k in line for k in ("MSC_VIEW.md","artifact_publish_map",
                                   "published_path","render_output", "write_communication"))]
            keep=set()
            for ix in hits[:45]:
                keep.update(range(max(0,ix-3),min(len(lines),ix+5)))
            print("KERNEL_WRITER_SOURCE_EXCERPTS",len(lines),"hits",len(hits))
            for lo,hi in ((800,915),(1061,1079)):
                print("KERNEL_OWNER_BLOCK",lo,hi)
                for n in range(lo-1,min(hi,len(lines))):print("KERNEL_OWNER",f"{n+1:04}",lines[n][:260])
            for ix in sorted(keep)[:220]:print("KERNEL_SOURCE",f"{ix+1:04}",lines[ix][:240])
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
        for p,kind in ((html,"render_output"),(md,"render_output")):
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
        # A preserved source relative link is not evidence of a valid published link:
        # Kernel often renames/folders files when publishing.
        md_maps=[x for x in mappings if x.get("sha256")==hashlib.sha256(md.read_bytes()).hexdigest()
                 and str(x.get("published_path","")).endswith(".md")]
        published_md=[dest / "works" / wid / str(x["published_path"]) for x in md_maps]
        links=[]
        for target in published_md:
            if not target.is_file():
                links.append({"published_md":str(target.relative_to(dest)),"status":"MAPPING_FILE_NOT_FOUND"})
                continue
            for label,href in __import__("re").findall(r"\[([^\]]+)\]\(([^)]+)\)",target.read_text(encoding="utf-8")):
                if not href.endswith(".html"): continue
                resolved=(target.parent/href).resolve()
                links.append({"published_md":str(target.relative_to(dest)),"href":href,
                              "status":"VALID" if resolved.is_file() and resolved in htmls else "BROKEN"})
        status=("PASS" if correct and actual_mapping and links and all(x["status"]=="VALID" for x in links) else "BLOCKED")
        result={"status":status,"scope":"SYNTHETIC_KERNEL_WRITER_ONLY",
                "md_mapping":bool(md_maps),"published_md_mapping_paths":[str(x.get("published_path","")) for x in md_maps],"published_relative_links":links,
                "record_evidence":e,"work_docs_export":export_status,
                "html_published":correct,"html_mapping":actual_mapping,
                "files":files[:35],"updater_g0":"NOT_VERIFIED",
                "group_writer_g0":"NOT_VERIFIED","business_host_e3":"NOT_RUN"}
        print("MSC_KERNEL_WRITER_G0_PROBE",json.dumps(result,ensure_ascii=False,sort_keys=True))
        return 0  # A blocked probe is evidence, not a CI regression in existing Kernel.

if __name__=="__main__":
    sys.exit(run())
