#!/usr/bin/env python3
"""Pinned v0.2.24 development builder. Never changes Windows LIVE installation."""
from __future__ import annotations
import argparse,hashlib,json,re,stat,subprocess,sys,tempfile,zipfile
from pathlib import Path,PurePosixPath
BASE="collab/packages/skill-collab-watcher_v0_2_23_1115_DEV_NOT_FOR_DEPLOYMENT.zip"
BASE_SHA="f941be8a6b53d00baa10a9b097f234b159470e2aa1242ecc33bcf0bdee080ea7"
OUT="skill-collab-watcher_v0_2_24_1117.zip"

def one(path:Path,before:str,after:str):
    s=path.read_text(encoding="utf8")
    n=s.count(before)
    if n!=1:raise RuntimeError(f"ANCHOR_COUNT {path} = {n}: {before[:100]!r}")
    path.write_text(s.replace(before,after),encoding="utf8",newline="\n")

def patch(root:Path):
    d=root/"skill_collab_watcher"
    p=d/"auto_policy.py"
    one(p,"    max_day_calls: int = 2\n","    max_day_calls: int = 0  # legacy, ignored for authorization\n")
    one(p,
        "    if (d.max_request_cents > 100 or d.max_day_calls < 1 or d.max_day_calls > 2\n            or d.max_day_cents > 300 or d.max_month_cents > 1000):",
        "    if (d.max_request_cents > 100 or d.max_day_cents > 300 or d.max_month_cents > 1000):")
    one(p,
        '    if e.day_calls_used_or_reserved >= d.max_day_calls:\n        return False, "DAY_CALL_LIMIT"\n',
        '    # Day call counts remain telemetry only; monetary ceilings decide admission.\n')
    p=d/"state_store.py"
    one(p,
        "        Returns CLAIMED, EXISTS, DAY_CALL_LIMIT, DAY_COST_LIMIT, MONTH_COST_LIMIT or READ_ONLY.",
        "        Returns CLAIMED, EXISTS, DAY_COST_LIMIT, MONTH_COST_LIMIT or READ_ONLY.")
    one(p,
        '            if usage["day_calls"] + 1 > max_day_calls:\n                verdict = "DAY_CALL_LIMIT"\n            elif usage["day_cents"] + cents > max_day_cents:',
        '            # Deprecated max_day_calls parameter is intentionally ignored.\n            if usage["day_cents"] + cents > max_day_cents:')
    p=d/"auto_approval.py"
    one(p,
        'f"limits: per request {d.max_request_cents} c, day {d.max_day_calls} calls/{d.max_day_cents} c, month {d.max_month_cents} c"',
        'f"limits: per request {d.max_request_cents} c, day {d.max_day_cents} c, month {d.max_month_cents} c"')
    one(p,
        'max_request_cents=_cents(raw.get("max_request_usd", 1.0), "max_request_usd"), max_day_calls=int(raw.get("max_day_calls", 2)),',
        'max_request_cents=_cents(raw.get("max_request_usd", 1.0), "max_request_usd"), max_day_calls=0,')
    p=d/"__init__.py"
    text=p.read_text(encoding="utf8")
    if "0.2.23" in text:p.write_text(text.replace("0.2.23","0.2.24"),encoding="utf8")
    p=root/"docs/CUTOVER_RUNBOOK.md"
    one(p, "Cutover runbook: Dropbox to GitHub (v0.2.23,", "Cutover runbook: Dropbox to GitHub (v0.2.24,")
    p=root/"docs/AUTO_APPROVAL.md"
    p.write_text(p.read_text(encoding="utf8")+
        "\n\n### v0.2.24 development cost-only admission\n"
        "- Daily and monthly review call counts are not admission gates. Legacy max_day_calls is ignored.\n"
        "- USD limits remain per request/day/month; request identity and one-shot execution stay enforced.\n"
        "- UNCERTAIN reservations are not refunded without a proven no-dispatch record.\n",encoding="utf8")
    policy=(d/"auto_policy.py").read_text(encoding="utf8")
    store=(d/"state_store.py").read_text(encoding="utf8")
    assert '"DAY_CALL_LIMIT"' not in policy+store
    assert "BEGIN IMMEDIATE" in store and "PRIMARY KEY (request_id, revision)" in store
    assert '"DAY_COST_LIMIT"' in store and '"MONTH_COST_LIMIT"' in store
    assert "c.max_calls != 1 or c.attempt != 1" in policy

def build(repo:Path,out:Path):
    source=repo/BASE
    if hashlib.sha256(source.read_bytes()).hexdigest()!=BASE_SHA:raise RuntimeError("SOURCE_SHA_MISMATCH")
    with tempfile.TemporaryDirectory(prefix="auto-cost-only-v024-") as temp:
        root=Path(temp)
        with zipfile.ZipFile(source) as z:
            if z.testzip():raise RuntimeError("ORIGINAL_ZIP_CRC_FAIL")
            names=set()
            for info in z.infolist():
                parts=PurePosixPath(info.filename).parts
                if info.filename in names or info.filename.startswith("/") or ".." in parts or "\\" in info.filename or stat.S_IFMT(info.external_attr>>16)==stat.S_IFLNK:
                    raise RuntimeError("UNSAFE_ORIGINAL_ZIP")
                names.add(info.filename)
            z.extractall(root)
        patch(root)
        from patch_v024_tests import patch_tests
        patch_tests(root)
        out.mkdir(parents=True,exist_ok=True)
        dst=out/OUT
        with zipfile.ZipFile(dst,"w",zipfile.ZIP_DEFLATED,compresslevel=8) as z:
            for p in sorted(root.rglob("*")):
                if p.is_file() and "__pycache__" not in p.parts and p.suffix!=".pyc":
                    info=zipfile.ZipInfo(p.relative_to(root).as_posix(),date_time=(2026,11,17,0,0,0))
                    info.compress_type=zipfile.ZIP_DEFLATED
                    info.external_attr=(0o100644<<16)
                    z.writestr(info,p.read_bytes())
        with zipfile.ZipFile(dst) as z:
            if z.testzip() or len(z.namelist())!=len(set(z.namelist())):raise RuntimeError("OUTPUT_ZIP_INVALID")
        print(json.dumps({"candidate":str(dst),"bytes":dst.stat().st_size,"sha256":hashlib.sha256(dst.read_bytes()).hexdigest(),"release":"development_not_for_deployment"},indent=2))
        return root

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",type=Path,default=Path("."))
    ap.add_argument("--out",type=Path,required=True)
    a=ap.parse_args()
    build(a.repo.resolve(),a.out.resolve())
