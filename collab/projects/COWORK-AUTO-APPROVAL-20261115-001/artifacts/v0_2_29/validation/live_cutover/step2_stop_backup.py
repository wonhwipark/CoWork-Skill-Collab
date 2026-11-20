"""STEP 2 - STOP the GitHub watcher task (only that one) and take a consistent cutover-time backup. On any failure the task is started again (state unchanged)."""
from cutover_common import *

r = {"started": time.strftime("%Y-%m-%d %H:%M:%S")}
r["pids_before"] = watcher_procs()
r["task_before"] = task_state().get(TASK)
if r["task_before"] != "Running" or not r["pids_before"]:
    sys.exit("STOP: watcher is not in the expected running state; nothing changed")
ok = False
try:
    ps(f"Stop-ScheduledTask -TaskName '{TASK}'")
    for _ in range(30):
        if not watcher_procs() and task_state().get(TASK) != "Running":
            break
        time.sleep(1)
    r["pids_after_stop"] = watcher_procs()
    r["task_after_stop"] = task_state().get(TASK)
    if r["pids_after_stop"] or r["task_after_stop"] == "Running":
        raise RuntimeError("watcher did not stop")
    r["notifier_state"] = task_state().get("SKILL-COLLAB-Notifier")
    # stopped-state consistency: nothing unfinished, then a NEW bundle
    snap = HERE / "stopped_snapshot.sqlite3"
    if snap.exists():
        snap.unlink()
    r["db_stopped"] = db_snapshot(snap)
    if r["db_stopped"]["jobs_by_state"] != {"COMPLETED": 9} or r["db_stopped"]["integrity"] != "ok":
        raise RuntimeError(f"unexpected DB state after stop: {r['db_stopped']}")
    target = r"D:\User\whpark\skill-collab-watcher-dist\backup_v0_2_25_cutover_" + time.strftime("%Y%m%d_%H%M%S")
    mk = subprocess.run([sys.executable, str(HERE.parent / "v029_live" / "make_backup_bundle.py"), target], capture_output=True, text=True, encoding="utf-8")
    if mk.returncode != 0:
        raise RuntimeError("bundle creation failed: " + (mk.stderr or mk.stdout)[-300:])
    b = json.loads(mk.stdout)
    r["cutover_bundle"] = {"target": b["target"], "files": b["files"], "manifest_verified": b["manifest_verified"], "install_tree_equals_live": b["install_tree_equals_live"],
                           "manifest_sha256": b["manifest_sha256"], "db_snapshot_sha256": b["db_snapshot_sha256"], "db_integrity": b["info"]["db_integrity"],
                           "install_tree_sha256": b["info"]["install_tree_sha256"], "private_key_in_bundle": b["private_key_or_passphrase_in_bundle"]}
    cb = r["cutover_bundle"]
    if not (cb["manifest_verified"] and cb["install_tree_equals_live"] and cb["install_tree_sha256"] == EXPECT["live_tree"] and cb["db_integrity"] == "ok" and not cb["private_key_in_bundle"]):
        raise RuntimeError("cutover bundle verification failed")
    ok = True
except Exception as exc:  # noqa: BLE001
    r["error"] = f"{type(exc).__name__}: {exc}"[:400]
finally:
    if not ok:
        ps(f"Start-ScheduledTask -TaskName '{TASK}'")
        time.sleep(8)
        r["restarted_after_failure"] = {"task": task_state().get(TASK), "pids": watcher_procs()}
r["STOP_AND_BACKUP"] = "PASS" if ok else "FAIL_RESTARTED"
save("step2_stop_backup.json", r)
print(json.dumps(r, ensure_ascii=False, indent=2, default=str))
