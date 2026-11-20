"""STEP 5 - restart the GitHub watcher and observe >=2 cycles, then one stop/start and >=2 more cycles. Any signing / READY / dispatch / claim / job change, any error event,
a second provider, or a second watcher process => immediate stop + byte-checked rollback + restart of the old version."""
from cutover_common import *
from rollback_lib import rollback

s2, s4 = load("step2_stop_backup.json"), load("step4_prestart.json")
assert s4["PRESTART_CHECK"] == "PASS"
base = {"audit_max_id": s4["db"]["audit_max_id"], "jobs": {"COMPLETED": 9}, "claims": {"READY_POSTED": 2, "UNCERTAIN": 1}, "seen": 11}
BAD_EVENTS = ("AUTO_RESERVED", "AUTO_SIGNING", "AUTO_APPROVAL_POSTED", "AUTO_READY", "READY_POSTED", "REVIEW_DISPATCHED", "REVIEW_COST", "CLAIMED", "VALIDATED", "COMPLETED", "AUTO_ERROR", "WATCH_ERROR", "AUTH_REQUIRED")
r = {"started": time.strftime("%Y-%m-%d %H:%M:%S"), "phases": []}


def db_view(after_id):
    con = sqlite3.connect(f"file:{STATE / 'state.sqlite3'}?mode=ro", uri=True)
    ev = {}
    for e, n in con.execute("SELECT event, COUNT(*) FROM audit_log WHERE id>? GROUP BY event", (after_id,)):
        ev[e] = n
    pairs = [(a, b or "", c or "") for a, b, c in con.execute("SELECT event, processing_key, detail FROM audit_log WHERE id>? AND event IN ('VALIDATED','APPROVAL_REJECTED')", (after_id,))]
    transport = [c or "" for (c,) in con.execute("SELECT detail FROM audit_log WHERE id>? AND event='TRANSPORT_ERROR'", (after_id,))]
    out = {"transport": transport, "pairs": pairs, "events": ev, "jobs": dict(con.execute("SELECT state, COUNT(*) FROM jobs GROUP BY state").fetchall()),
           "claims": dict(con.execute("SELECT stage, COUNT(*) FROM auto_claims GROUP BY stage").fetchall()), "seen": con.execute("SELECT COUNT(*) FROM auto_seen").fetchone()[0],
           "lease": [tuple(str(x)[:30] for x in rr) for rr in con.execute("SELECT * FROM provider_lease")], "max_id": con.execute("SELECT MAX(id) FROM audit_log").fetchone()[0],
           "notable": [(a, (b or "")[:40], (c or "")[:90]) for a, b, c in con.execute("SELECT event, processing_key, detail FROM audit_log WHERE id>? AND event NOT IN ('SCAN_START','SCAN_END') ORDER BY id LIMIT 25", (after_id,))]}
    con.close()
    return out


import observe_lib


_c = sqlite3.connect(f"file:{STATE / 'state.sqlite3'}?mode=ro", uri=True)
KNOWN_EXPIRED = {x[0] for x in _c.execute("SELECT DISTINCT processing_key FROM audit_log WHERE event='APPROVAL_REJECTED' AND detail='APPROVAL_EXPIRED' AND id<=?", (base["audit_max_id"],))}
_c.close()
r["known_expired_keys_before_cutover"] = sorted(k[:40] for k in KNOWN_EXPIRED)


def anomalies(v):
    return observe_lib.anomalies(v, base["jobs"], base["claims"], s4["db"]["lease"], watcher_procs(), KNOWN_EXPIRED)


def observe(label, min_cycles, timeout):
    t0 = time.time()
    res = {"label": label}
    while time.time() - t0 < timeout:
        v = db_view(base["audit_max_id"])
        bad = anomalies(v)
        cycles = min(v["events"].get("SCAN_START", 0), v["events"].get("SCAN_END", 0))
        if bad:
            res.update(view=v, anomalies=bad, cycles=cycles)
            return res
        if cycles >= min_cycles and watcher_procs():
            res.update(view=v, anomalies=[], cycles=cycles, seconds=round(time.time() - t0))
            return res
        time.sleep(5)
    v = db_view(base["audit_max_id"])
    res.update(view=v, anomalies=anomalies(v) + ["timeout before enough cycles"], cycles=min(v["events"].get("SCAN_START", 0), v["events"].get("SCAN_END", 0)))
    return res


failed = None
try:
    ps(f"Start-ScheduledTask -TaskName '{TASK}'")
    for _ in range(40):
        if watcher_procs():
            break
        time.sleep(1)
    r["started_pids"] = watcher_procs()
    p1 = observe("after_start_2_cycles", 2, 240)
    r["phases"].append(p1)
    if p1["anomalies"]:
        failed = p1["anomalies"]
    else:
        # one restart
        mark = p1["view"]["max_id"]
        ps(f"Stop-ScheduledTask -TaskName '{TASK}'")
        for _ in range(30):
            if not watcher_procs():
                break
            time.sleep(1)
        r["stopped_for_restart"] = {"pids": watcher_procs(), "task": task_state().get(TASK)}
        ps(f"Start-ScheduledTask -TaskName '{TASK}'")
        for _ in range(40):
            if watcher_procs():
                break
            time.sleep(1)
        base["audit_max_id"] = base["audit_max_id"]            # keep the original baseline: everything since the cutover counts
        p2 = observe("after_restart_2_cycles", 4, 300)         # cumulative SCAN counts since the original baseline: 2 before + >=2 after the restart
        p2["restart_mark_audit_id"] = mark
        r["phases"].append(p2)
        if p2["anomalies"]:
            failed = p2["anomalies"]
except Exception as exc:  # noqa: BLE001
    failed = [f"exception {type(exc).__name__}: {exc}"[:300]]

if failed:
    r["FAILED"] = failed
    ps(f"Stop-ScheduledTask -TaskName '{TASK}'")
    time.sleep(5)
    r["rollback"] = rollback(s2["cutover_bundle"]["target"])
    if r["rollback"]["verified"]:
        ps(f"Start-ScheduledTask -TaskName '{TASK}'")
        time.sleep(10)
    r["after_rollback"] = {"task": task_state().get(TASK), "pids": watcher_procs()}
    r["TWO_CYCLES_RESTART"] = "FAIL_ROLLED_BACK" if r["rollback"]["verified"] else "FAIL_ROLLBACK_UNVERIFIED"
else:
    r["TWO_CYCLES_RESTART"] = "PASS"
r["final_tasks"] = task_state()
r["final_pids"] = watcher_procs()
save("step5_start_observe.json", r)
print(json.dumps({k: (v if k != "phases" else [{kk: vv for kk, vv in ph.items() if kk != "view"} | {"events": ph["view"]["events"], "notable": ph["view"]["notable"], "claims": ph["view"]["claims"], "jobs": ph["view"]["jobs"], "lease": ph["view"]["lease"]} for ph in v]) for k, v in r.items()}, ensure_ascii=False, indent=2, default=str))
