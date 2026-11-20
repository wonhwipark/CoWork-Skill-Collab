"""STEP 6 - independent final verification of the live state after the cutover (read-only)."""
from cutover_common import *

r = {"verified_at": time.strftime("%Y-%m-%d %H:%M:%S")}
s2, s3, s4, s5 = load("step2_stop_backup.json"), load("step3_install_align.json"), load("step4_prestart.json"), load("step5_start_observe.json")
stage = HERE / "stage_zip"
zip_tree = tree(stage)
inst = tree(LIVE)
r["installed"] = {"version_line": (LIVE / "skill_collab_watcher" / "__init__.py").read_text(encoding="utf-8").strip(), "tree_sha256": tree_sha(inst), "equals_step4_tree": tree_sha(inst) == s4["installed"]["tree_sha256"],
                  "zip_files_all_identical": all(inst.get(k) == v for k, v in zip_tree.items()), "preserved_package_files": sorted(k for k in inst if k.startswith("package/")),
                  "config_sha256": sha(CFG), "delegation_sha256": sha(DELEG), "config_equals_step3": sha(CFG) == s3["config_new_sha"], "delegation_equals_step3": sha(DELEG) == s3["delegation_new_sha"]}
d = json.loads(DELEG.read_text(encoding="utf-8"))
c = json.loads(CFG.read_text(encoding="utf-8"))
r["policy_now"] = {"static_registered_usd": c["review_policy"]["known_run_policy_refs"]["POLICY-STATIC-V1"]["max_budget_usd"], "large_design_registered": [c["review_policy"]["known_run_policy_refs"][k]["max_budget_usd"] for k in ("POLICY-STATIC-V1-LARGE", "POLICY-STATIC-V1-DESIGN")],
                   "delegation": {k: d.get(k) for k in ("enabled", "policy", "max_request_usd", "enabled_at", "expires_at", "project_families", "projects", "skills", "repo_id", "branch")},
                   "daily_budget_usd": c["review_policy"].get("daily_budget_usd"), "max_dispatches_per_day": c["review_policy"].get("max_dispatches_per_day")}
r["tasks"], r["watcher_pids"] = task_state(), watcher_procs()
cmd = ps("Get-CimInstance Win32_Process | Where-Object { $_.Name -match '^pythonw?\\.exe$' -and $_.CommandLine -match 'skill_collab_watcher.cli' -and $_.CommandLine -match ' watch' } | ForEach-Object { $_.ProcessId.ToString() + '|' + $_.ExecutablePath + '|' + $_.ParentProcessId }")
r["watcher_processes"] = [l.strip() for l in cmd.splitlines() if l.strip()]

snap = HERE / "final_snapshot.sqlite3"
if snap.exists():
    snap.unlink()
r["db"] = db_snapshot(snap)
con = sqlite3.connect(snap)
r["running_versions_from_watch_start"] = [(row[0][:19], json.loads(row[1]).get("version")) for row in con.execute("SELECT ts, detail FROM audit_log WHERE event='WATCH_START' ORDER BY id DESC LIMIT 8")]
since = s4["db"]["audit_max_id"]
r["events_since_final_baseline"] = dict(con.execute("SELECT event, COUNT(*) FROM audit_log WHERE id>? GROUP BY event", (since,)).fetchall())
r["signing_or_dispatch_events_since_baseline"] = [e for e in r["events_since_final_baseline"] if any(s in e for s in ("SIGN", "READY", "DISPATCH", "CLAIM", "RESERV", "COMPLETED", "COST"))]
r["model_calls_new"] = con.execute("SELECT COUNT(*) FROM audit_log WHERE id>? AND event IN ('REVIEW_DISPATCHED','REVIEW_COST')", (since,)).fetchone()[0]
r["jobs_total"] = con.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]
r["claims_total"] = con.execute("SELECT COUNT(*) FROM auto_claims").fetchone()[0]
con.close()

names = subprocess.run(["gh", "api", f"repos/{REPO}/contents/collab/requests", "--jq", ".[].name"], capture_output=True, text=True).stdout.split()
before = json.loads((HERE / "legacy_before.json").read_text(encoding="utf-8"))
lg = subprocess.run([sys.executable, str(HERE.parent / "v029_live" / "classify_legacy.py"), str(snap)], capture_output=True, text=True, encoding="utf-8")
after = json.loads(lg.stdout)
sig = lambda rows: sorted((x["id"], tuple(x["remote"])) for x in rows)
r["remote"] = {"request_folders": len([n for n in names if n.startswith("REQ-")]), "same_request_set_and_history_as_before": sig(before["rows"]) == sig(after["rows"]),
               "summary_before": before["summary"], "summary_after": after["summary"], "static_no_history": after["summary"].get("NO_HISTORY_STATIC_PENDING", 0)}
cc = subprocess.run([str(OLD_PY), "-m", "skill_collab_watcher.cli", "--config", str(CFG), "config-check"], cwd=LIVE, capture_output=True, text=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}, timeout=120)
r["config_check"] = [l for l in cc.stdout.splitlines() if l.startswith(("version", "  run policy", "auto_approval: delegation"))]
gate = HERE.parent / "v028" / "review_request_gate.py"
g = subprocess.run([sys.executable, str(gate), "select", "--live-config", str(CFG), "--intent", "unified", "--required-budget-usd", "3.00"], capture_output=True, text=True)
r["gate_select_unified"] = json.loads(g.stdout) if g.returncode == 0 else g.stderr.strip()
r["old_interpreter_folder_intact"] = OLD_PY.exists()
r["notifier"] = r["tasks"].get("SKILL-COLLAB-Notifier")
r["bundles"] = {"verified_original": str(BUNDLE), "cutover_bundle": s2["cutover_bundle"]["target"], "cutover_bundle_manifest_sha256": s2["cutover_bundle"]["manifest_sha256"],
                "cutover_bundle_db_snapshot_sha256": s2["cutover_bundle"]["db_snapshot_sha256"]}
ok = (r["installed"]["version_line"] == '__version__ = "0.2.29"' and r["installed"]["equals_step4_tree"] and r["installed"]["zip_files_all_identical"] and r["installed"]["config_equals_step3"] and r["installed"]["delegation_equals_step3"]
      and r["tasks"].get(TASK) == "Running" and r["tasks"].get("SKILL-COLLAB-Notifier") == "Running" and len(r["watcher_pids"]) == 2 and r["db"]["integrity"] == "ok" and r["db"]["jobs_by_state"] == {"COMPLETED": 9}
      and r["db"]["auto_claims_by_stage"] == {"READY_POSTED": 2, "UNCERTAIN": 1} and not r["signing_or_dispatch_events_since_baseline"] and r["model_calls_new"] == 0 and r["remote"]["same_request_set_and_history_as_before"]
      and r["remote"]["static_no_history"] == 0 and r["policy_now"]["static_registered_usd"] == 3.0 and r["policy_now"]["delegation"]["max_request_usd"] == 3.0 and r["running_versions_from_watch_start"][0][1] == "0.2.29" and r["old_interpreter_folder_intact"])
r["FINAL_LIVE_STATE_OK"] = ok
save("step6_final_verify.json", r)
print(json.dumps(r, ensure_ascii=False, indent=2, default=str))
