#!/usr/bin/env python3
"""MSC dual-entry follow-up development only; never install or publish a release."""
from __future__ import annotations
import argparse, hashlib, json, re, zipfile
from pathlib import Path

BASE_SHA256 = "b0ebd0aa4d771adc30648ab2bce23a3c1648e408984bedb36d0e3da45108312c"

def inspect(source: Path) -> None:
    data = source.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != BASE_SHA256:
        raise RuntimeError("SOURCE_SHA_MISMATCH:" + digest)
    with zipfile.ZipFile(source) as z:
        assert z.testzip() is None
        files = [i.filename for i in z.infolist()]
        print("MSC_SOURCE_PIN_PASS", len(data), digest, "FILES", len(files))
        for name in files:
            if any(x in name.lower() for x in (".py", "policy.json", "skill.md")):
                print("FILE", name)
        for name in files:
            if not name.endswith(".py"):
                continue
            data = z.read(name).decode("utf-8", errors="replace").splitlines()
            hits = [i for i, line in enumerate(data)
                    if re.search(r"view.mode|view_mode|html.view|html_view|PROCEDURE_FEATURE|msc.package|scenario.build|MSC_VIEW|view-mode|html-viewer|render.*html|html.*render", line, re.I)]
            if not hits:
                continue
            keep=set()
            for i in hits[:22]:
                keep.update(range(max(0,i-4),min(len(data),i+6)))
            print("=== EXCERPT", name, "LINES", len(data), "HITS",len(hits),"===")
            for i in sorted(keep):
                print(f"{i+1:04} {data[i][:250]}")
        for name in files:
            if name.endswith("skillsilent/policy.json"):
                policy=json.loads(z.read(name))
                print("POLICY_ACTIONS", json.dumps(policy, ensure_ascii=False)[:11000])

if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--inspect",type=Path,required=True)
    a=p.parse_args()
    inspect(a.inspect)
