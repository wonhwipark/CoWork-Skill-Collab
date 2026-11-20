"""Bounded su_l1 diagnostic on an extracted, pinned v0.2.29 tree. Max 10 runs per condition (idle / loaded).
Each run: 6 processes race the same nonce; then invariants (a)-(f) are checked. Also runs the ORIGINAL unmodified test
up to 10 times per condition and reports its raw pass/fail. Nothing in the package is edited. No GitHub, no model."""
import json
import os
import pathlib
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time

PKG = pathlib.Path(sys.argv[1]).resolve()
OUT = pathlib.Path(sys.argv[2]).resolve()
RUNS = int(sys.argv[3]) if len(sys.argv) > 3 else 10
HERE = pathlib.Path(__file__).parent
WORKER = str(HERE / "diag_worker.py")
sys.path.insert(0, str(PKG / "su_l1"))
import local_only_contract_r0003 as c  # noqa: E402


def start_load():
    n = max(2, (os.cpu_count() or 4))
    return [subprocess.Popen([sys.executable, "-c", "while True: pass"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) for _ in range(n)]


def stop_load(procs):
    for p in procs:
        p.kill()
    for p in procs:
        p.wait()


def race_once():
    d = tempfile.mkdtemp(prefix="su-diag-")
    db, anchor, go = os.path.join(d, "ledger.sqlite"), os.path.join(d, "ledger.anchor"), os.path.join(d, "go")
    diag = os.path.join(d, "diag.jsonl")
    try:
        c.Ledger.bootstrap(db, anchor, acknowledge=c.BOOTSTRAP_ACK)
        procs = [subprocess.Popen([sys.executable, "-I", WORKER, "nonce", db, anchor, "N-SAME", go, diag, str(PKG)],
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for _ in range(6)]
        open(go, "w").close()
        res = []
        for p in procs:
            o, e = p.communicate(timeout=90)
            res.append((p.returncode, (o.strip().splitlines() or [""])[-1], e.strip()[-200:]))
        lines = [r[1] for r in res]
        rec = {"ok": lines.count("OK"), "replay": lines.count("ERR NONCE_REPLAY"),
               "anchor_unreadable": lines.count("ERR ANCHOR_UNREADABLE_FAIL_CLOSED"),
               "other": [x for x in lines if x not in ("OK", "ERR NONCE_REPLAY", "ERR ANCHOR_UNREADABLE_FAIL_CLOSED")],
               "nonzero_exit": [r[0] for r in res if r[0] != 0], "stderr": [r[2] for r in res if r[2]]}
        diags = [json.loads(x) for x in open(diag, encoding="utf-8")] if os.path.exists(diag) else []
        rec["diag"] = diags
        # (c) counts and anchor/DB consistency
        led = c.Ledger.open(db, anchor)
        counts = led.counts()
        con = sqlite3.connect(db)
        meta = dict(con.execute("SELECT k,v FROM meta").fetchall())
        qc = con.execute("PRAGMA quick_check").fetchone()[0]
        con.close()
        anc = json.load(open(anchor, encoding="utf-8"))
        rec["counts"] = {"nonces": counts["nonces"], "log": counts["log"]}
        rec["c_ok"] = (counts["nonces"], counts["log"]) == (1, 1) and anc["seq"] == int(meta["seq"]) == 1 and anc["head"] == meta["head"] and qc == "ok"
        # (d) accepted nonce is never approved again
        try:
            led.consume_nonce("N-SAME", "REQ-N-SAME-AGAIN")
            rec["d_ok"] = False
        except c.ContractError as err:
            rec["d_ok"] = str(err) == "NONCE_REPLAY"
        # (e) a new nonce is processed normally
        try:
            c.Ledger.open(db, anchor).consume_nonce("N-NEW", "REQ-N-NEW")
            rec["e_ok"] = c.Ledger.open(db, anchor).counts()["nonces"] == 2
        except Exception as err:  # noqa: BLE001
            rec["e_ok"] = False
            rec["e_err"] = repr(err)[:120]
        # (f) no leftover temp files, no damage
        rec["f_ok"] = not [n for n in os.listdir(d) if n.endswith(".tmp")]
        rec["a_ok"] = rec["ok"] == 1 and rec["replay"] + rec["anchor_unreadable"] == 5 and not rec["other"] and not rec["nonzero_exit"]
        rec["b_ok"] = rec["ok"] <= 1
        return rec
    finally:
        shutil.rmtree(d, ignore_errors=True)


def original_test_once():
    t = "su_l1/test_local_only_contract_r0003.py::Race::test_the_same_nonce_in_six_processes_is_accepted_exactly_once"
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", t], cwd=PKG, capture_output=True, text=True, timeout=300)
    return r.returncode == 0


report = {"package": str(PKG), "runs_per_condition": RUNS, "conditions": {}}
for cond in ("idle", "loaded"):
    load = start_load() if cond == "loaded" else []
    try:
        time.sleep(1.0 if load else 0)
        races = [race_once() for _ in range(RUNS)]
        orig = [original_test_once() for _ in range(RUNS)]
    finally:
        stop_load(load)
    stages = {}
    for r in races:
        for d in r["diag"]:
            k = f'{d["stage"]}|{d["type"]}|errno={d["errno"]}|winerror={d["winerror"]}|via={">".join(d["frames"][-3:])}'
            stages[k] = stages.get(k, 0) + 1
    report["conditions"][cond] = {
        "race_runs": RUNS, "anchor_unreadable_runs": sum(1 for r in races if r["anchor_unreadable"]),
        "a_ok": sum(r["a_ok"] for r in races), "b_ok": sum(r["b_ok"] for r in races), "c_ok": sum(r["c_ok"] for r in races),
        "d_ok": sum(r["d_ok"] for r in races), "e_ok": sum(r["e_ok"] for r in races), "f_ok": sum(r["f_ok"] for r in races),
        "double_accept_runs": sum(1 for r in races if r["ok"] > 1), "zero_accept_runs": sum(1 for r in races if r["ok"] == 0),
        "other_results": [r["other"] for r in races if r["other"]],
        "unreadable_causes": stages,
        "original_test_pass": sum(orig), "original_test_fail": len(orig) - sum(orig),
        "per_run": [{k: v for k, v in r.items() if k not in ("diag",)} for r in races],
    }
OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
for cond, v in report["conditions"].items():
    print(cond, {k: v[k] for k in ("race_runs", "anchor_unreadable_runs", "a_ok", "b_ok", "c_ok", "d_ok", "e_ok", "f_ok",
                                     "double_accept_runs", "zero_accept_runs", "original_test_pass", "original_test_fail")})
    print("  causes:", v["unreadable_causes"])
