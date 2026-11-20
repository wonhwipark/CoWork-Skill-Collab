"""Narrow su_l1 mechanism experiments on the extracted pinned tree (nothing in the package is edited).
A: one process rewrites the anchor with the real c._write_anchor while another reads it with an instrumented copy of
   c._read_anchor (same semantics): which OS error does an UNLOCKED reader get during os.replace?  10 trials.
B: inject ANCHOR_UNREADABLE into exactly one of six racing workers at the unlocked Ledger.open() verify and check
   invariants (a)-(f): nothing consumed by the failed worker, exactly one OK, replay refused, new nonce OK.  10 trials."""
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import time

PKG = pathlib.Path(sys.argv[1]).resolve()
OUT = pathlib.Path(sys.argv[2]).resolve()
TRIALS = int(sys.argv[3]) if len(sys.argv) > 3 else 10
sys.path.insert(0, str(PKG / "su_l1"))
import local_only_contract_r0003 as c  # noqa: E402

WRITER = r'''
import os, sys, time
sys.path.insert(0, sys.argv[1] + "/su_l1")
import local_only_contract_r0003 as c
path, go, n = sys.argv[2], sys.argv[3], int(sys.argv[4])
while not os.path.exists(go): time.sleep(0.001)
for i in range(n):
    c._write_anchor(path, {"genesis": "g", "seq": i + 1, "head": "h"})
print("DONE")
'''
READER = r'''
import json, os, sys, time, collections
path, go, n = sys.argv[1], sys.argv[2], int(sys.argv[3])
while not os.path.exists(go): time.sleep(0.001)
causes = collections.Counter(); ok = 0
for i in range(n):
    stage = "open"
    try:
        with open(path, "r", encoding="utf-8") as fh:
            stage = "json"; data = json.load(fh)
        stage = "shape"
        if set(data) != {"genesis", "seq", "head"} or not isinstance(data["seq"], int): raise ValueError
        ok += 1
    except (OSError, ValueError, TypeError) as exc:
        causes[f"{stage}|{type(exc).__name__}|errno={getattr(exc,'errno',None)}|winerror={getattr(exc,'winerror',None)}"] += 1
print(json.dumps({"reads": n, "ok": ok, "causes": causes}))
'''
INJECT = r'''
import os, sys, time
sys.path.insert(0, sys.argv[7] + "/su_l1")
import local_only_contract_r0003 as c
op, db, anchor, key, start, inject = sys.argv[1:7]
if inject == "1":
    first = {"done": False}
    real = c._read_anchor
    def once(path):
        if not first["done"]:
            first["done"] = True
            raise c.ContractError("ANCHOR_UNREADABLE_FAIL_CLOSED")
        return real(path)
    c._read_anchor = once
deadline = time.monotonic() + 30
while not os.path.exists(start) and time.monotonic() < deadline: time.sleep(0.002)
try:
    c.Ledger.open(db, anchor).consume_nonce(key, "REQ-" + key); print("OK")
except c.ContractError as err:
    print("ERR", err)
'''

d0 = pathlib.Path(tempfile.mkdtemp(prefix="su-mech-"))
(d0 / "writer.py").write_text(WRITER, encoding="utf-8")
(d0 / "reader.py").write_text(READER, encoding="utf-8")
(d0 / "inject.py").write_text(INJECT, encoding="utf-8")
report = {"package": str(PKG), "A_mechanism": [], "B_injection": []}

for t in range(TRIALS):
    d = tempfile.mkdtemp(prefix="su-a-")
    path, go = os.path.join(d, "anchor"), os.path.join(d, "go")
    c._write_anchor(path, {"genesis": "g", "seq": 0, "head": "h"})
    w = subprocess.Popen([sys.executable, "-I", str(d0 / "writer.py"), str(PKG), path, go, "400"], stdout=subprocess.PIPE, text=True)
    r = subprocess.Popen([sys.executable, "-I", str(d0 / "reader.py"), path, go, "4000"], stdout=subprocess.PIPE, text=True)
    open(go, "w").close()
    wo, ro = w.communicate(timeout=120)[0], r.communicate(timeout=120)[0]
    rr = json.loads(ro.strip().splitlines()[-1])
    report["A_mechanism"].append({"writer": wo.strip(), "reads": rr["reads"], "ok": rr["ok"], "failed": rr["reads"] - rr["ok"], "causes": rr["causes"]})
    shutil.rmtree(d, ignore_errors=True)

for t in range(TRIALS):
    d = tempfile.mkdtemp(prefix="su-b-")
    db, anchor, go = os.path.join(d, "l.sqlite"), os.path.join(d, "l.anchor"), os.path.join(d, "go")
    c.Ledger.bootstrap(db, anchor, acknowledge=c.BOOTSTRAP_ACK)
    procs = [subprocess.Popen([sys.executable, "-I", str(d0 / "inject.py"), "nonce", db, anchor, "N-SAME", go, "1" if i == 0 else "0", str(PKG)],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for i in range(6)]
    open(go, "w").close()
    lines = []
    for p in procs:
        o, e = p.communicate(timeout=90)
        lines.append((o.strip().splitlines() or [""])[-1])
    counts = c.Ledger.open(db, anchor).counts()
    rec = {"lines": lines, "ok": lines.count("OK"), "unreadable": lines.count("ERR ANCHOR_UNREADABLE_FAIL_CLOSED"),
           "replay": lines.count("ERR NONCE_REPLAY"), "counts": [counts["nonces"], counts["log"]]}
    rec["a_b_ok"] = rec["ok"] == 1 and rec["unreadable"] == 1 and rec["replay"] == 4 and rec["counts"] == [1, 1]
    try:
        c.Ledger.open(db, anchor).consume_nonce("N-SAME", "REQ-AGAIN")
        rec["d_ok"] = False
    except c.ContractError as err:
        rec["d_ok"] = str(err) == "NONCE_REPLAY"
    # the injected worker retries its own request: refused as replay, never a second accept
    retry = subprocess.run([sys.executable, "-I", str(d0 / "inject.py"), "nonce", db, anchor, "N-SAME", go, "0", str(PKG)], capture_output=True, text=True)
    rec["retry_result"] = (retry.stdout.strip().splitlines() or [""])[-1]
    try:
        c.Ledger.open(db, anchor).consume_nonce("N-NEW", "REQ-NEW")
        rec["e_ok"] = c.Ledger.open(db, anchor).counts()["nonces"] == 2
    except Exception as err:  # noqa: BLE001
        rec["e_ok"] = False
    rec["f_ok"] = not [n for n in os.listdir(d) if n.endswith(".tmp")]
    report["B_injection"].append(rec)
    shutil.rmtree(d, ignore_errors=True)

shutil.rmtree(d0, ignore_errors=True)
a_fail = sum(x["failed"] for x in report["A_mechanism"])
causes = {}
for x in report["A_mechanism"]:
    for k, v in x["causes"].items():
        causes[k] = causes.get(k, 0) + v
report["summary"] = {
    "A_trials": TRIALS, "A_total_reads": sum(x["reads"] for x in report["A_mechanism"]), "A_failed_reads": a_fail, "A_causes": causes,
    "B_trials": TRIALS, "B_a_b_ok": sum(x["a_b_ok"] for x in report["B_injection"]), "B_d_ok": sum(x["d_ok"] for x in report["B_injection"]),
    "B_e_ok": sum(x["e_ok"] for x in report["B_injection"]), "B_f_ok": sum(x["f_ok"] for x in report["B_injection"]),
    "B_retry_replay": sum(1 for x in report["B_injection"] if x["retry_result"] == "ERR NONCE_REPLAY"),
}
OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
