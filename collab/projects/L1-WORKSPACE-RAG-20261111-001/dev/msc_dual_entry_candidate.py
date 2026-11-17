#!/usr/bin/env python3
"""Pinned MSC dual-entry inspection; development scope only."""
from __future__ import annotations
import argparse, hashlib, json, re, zipfile
from pathlib import Path
BASE_SHA256 = "b0ebd0aa4d771adc30648ab2bce23a3c1648e408984bedb36d0e3da45108312c"
WORKFLOW_SHA256 = None

def excerpt(z, name, start, end):
    lines = z.read(name).decode("utf-8",errors="replace").splitlines()
    print("=== BLOCK",name,start,end,"===")
    for i in range(start-1,min(end,len(lines))):
        print(f"{i+1:04} {lines[i][:250]}")

def inspect(source: Path, workflow: Path | None) -> None:
    digest=hashlib.sha256(source.read_bytes()).hexdigest()
    if digest!=BASE_SHA256: raise RuntimeError("SOURCE_SHA_MISMATCH:"+digest)
    with zipfile.ZipFile(source) as z:
        assert z.testzip() is None
        names=set(z.namelist())
        print("PINNED_CONVERTER",digest,len(names))
        for name, start,end in [
            ("doc-converter/scripts/msc_tool.py",850,945),
            ("doc-converter/scripts/msc_tool.py",990,1085),
            ("doc-converter/scripts/msc_tool.py",1120,1165),
            ("doc-converter/scripts/direct_gateway.py",1,230),
        ]:
            if name in names: excerpt(z,name,start,end)
        policy=json.loads(z.read("doc-converter/skillsilent/policy.json"))
        for key in ("msc-package","msc-scenario-build"):
            print("POLICY",key,json.dumps(policy["actions"][key],ensure_ascii=False))
    if workflow is None:return
    with zipfile.ZipFile(workflow) as z:
        assert z.testzip() is None
        print("WORKFLOW_ZIP",len(z.namelist()),hashlib.sha256(workflow.read_bytes()).hexdigest())
        for name in z.namelist():
            if not name.endswith((".py",".md")) or name.endswith("SKILL.md"):continue
            try: lines=z.read(name).decode("utf-8").splitlines()
            except UnicodeDecodeError: continue
            hits=[i for i,line in enumerate(lines)
                  if re.search(r"msc.*(package|scenario.build|view.mode|converter|handoff|html)|(?:converter|view.mode|html).*msc",line,re.I)]
            if not hits: continue
            print("=== WORKFLOW",name,"LINES",len(lines),"HITS",len(hits),"===")
            shown=set()
            for i in hits[:10]:
                for k in range(max(0,i-3),min(len(lines),i+5)):shown.add(k)
            for i in sorted(shown):print(f"{i+1:04} {lines[i][:230]}")

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--inspect",type=Path,required=True)
    p.add_argument("--workflow",type=Path)
    a=p.parse_args()
    inspect(a.inspect,a.workflow)
