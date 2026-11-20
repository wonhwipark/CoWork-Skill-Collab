"""Re-check that the baseline is byte-exact again after the automatic rollback and that nothing else moved, before the cutover is attempted a second time."""
from cutover_common import *

r = {"checked": time.strftime("%Y-%m-%d %H:%M:%S")}
s2 = load("step2_stop_backup.json")
r["live"] = {"tree": tree_sha(tree(LIVE)), "config": sha(CFG), "delegation": sha(DELEG), "version": (LIVE / "skill_collab_watcher" / "__init__.py").read_text(encoding="utf-8").strip()}
snap = HERE / "baseline2_snapshot.sqlite3"
if snap.exists():
    snap.unlink()
r["db"] = db_snapshot(snap)
r["tasks"] = task_state()
r["watcher_pids"] = watcher_procs()
ok = (r["live"]["tree"] == EXPECT["live_tree"] and r["live"]["config"] == EXPECT["config_sha"] and r["live"]["delegation"] == EXPECT["delegation_sha"]
      and r["db"]["audit_max_id"] == s2["db_stopped"]["audit_max_id"] and r["db"]["jobs_by_state"] == {"COMPLETED": 9} and r["db"]["integrity"] == "ok"
      and r["tasks"].get(TASK) == "Ready" and not r["watcher_pids"] and r["tasks"].get("SKILL-COLLAB-Notifier") == "Running")
r["BASELINE_RESTORED_AND_STABLE"] = ok
save("step3b_recheck_baseline.json", r)
print(json.dumps(r, ensure_ascii=False, indent=2, default=str))
