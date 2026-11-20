"""STEP 4 - PRESTART_VERIFY (watcher still stopped, zero paid calls). Installed bytes, aligned config + delegation load, unified USD3 gate on the REAL config,
legacy classification against the new enabled_at, SHADOW on a separate DB with a throw-away signer, single provider."""
import shutil
from datetime import datetime
from cutover_common import *
from rollback_lib import rollback

sys.dont_write_bytecode = True
r = {"started": time.strftime("%Y-%m-%d %H:%M:%S")}
s3 = load("step3_install_align.json")
fail = []
assert task_state().get(TASK) != "Running" and not watcher_procs(), "watcher must still be stopped"

# installed bytes
stage = HERE / "stage_zip"
zip_tree = tree(stage)
inst = tree(LIVE)
r["installed"] = {"files": len(inst), "equals_zip_plus_preserved": all(inst.get(k) == v for k, v in zip_tree.items()),
                  "version_line": (LIVE / "skill_collab_watcher" / "__init__.py").read_text(encoding="utf-8").strip(), "tree_sha256": tree_sha(inst)}
if not (r["installed"]["equals_zip_plus_preserved"] and r["installed"]["version_line"] == '__version__ = "0.2.29"'):
    fail.append("installed bytes")

# aligned config + delegation load together, with the installed code
sys.path.insert(0, str(LIVE))
from skill_collab_watcher.auto_approval import load_delegation  # noqa: E402
from skill_collab_watcher.config import Config  # noqa: E402
dele, why = load_delegation(DELEG, time.time(), "windows")
cfg_obj = json.loads(CFG.read_text(encoding="utf-8"))
r["aligned_load"] = {"delegation_usable": dele is not None, "why": why, "max_request_cents": getattr(dele, "max_request_cents", None),
                     "static_registered_usd": cfg_obj["review_policy"]["known_run_policy_refs"]["POLICY-STATIC-V1"]["max_budget_usd"],
                     "large_design_registered": [cfg_obj["review_policy"]["known_run_policy_refs"][k]["max_budget_usd"] for k in ("POLICY-STATIC-V1-LARGE", "POLICY-STATIC-V1-DESIGN")]}
d = json.loads(DELEG.read_text(encoding="utf-8"))
r["delegation_now"] = {k: d.get(k) for k in ("enabled", "policy", "max_request_usd", "enabled_at", "expires_at", "project_families", "projects", "skills", "repo_id", "branch")}
r["delegation_scope_expiry_unchanged"] = (d["expires_at"] == EXPECT["expires_at"] and d["project_families"] == ["COWORK-", "L1-WORKSPACE-"]
                                          and d["skills"] == ["cowork-review-watcher", "cowork-dashboard", "l1-knowledge-updater"] and isinstance(d["repo_id"], str) and d["repo_id"] == "1451933830")
if not (dele is not None and dele.max_request_cents == 300 and r["aligned_load"]["static_registered_usd"] == 3.0 and r["delegation_scope_expiry_unchanged"]):
    fail.append("aligned load")

# production interpreter, installed code, real config
env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
cc = subprocess.run([str(OLD_PY), "-m", "skill_collab_watcher.cli", "--config", str(CFG), "config-check"], cwd=LIVE, capture_output=True, text=True, env=env, timeout=120)
r["config_check"] = {"rc": cc.returncode, "lines": [l for l in cc.stdout.splitlines() if not any(s in l for s in ("token", "secret"))][:16]}
if cc.returncode != 0 or "version: 0.2.29" not in cc.stdout or "max_budget_usd=3.0" not in cc.stdout:
    fail.append("config-check")

# unified USD3 gate on the REAL config
gate = HERE.parent / "v028" / "review_request_gate.py"
g1 = subprocess.run([sys.executable, str(gate), "select", "--live-config", str(CFG), "--intent", "unified", "--required-budget-usd", "3.00"], capture_output=True, text=True)
r["gate_select_unified_real_config"] = (g1.stdout or g1.stderr).strip()[:200]
zipfile_local = HERE.parent / "v029_rev" / "skill-collab-watcher_v0_2_29_1120.zip"
req_text = (HERE.parent / "v029_live" / "staged" / "req_placeholder.md")
rq = f"""---
schema: SKILL_COLLAB_REVIEW_REQUEST_V1
state: SUBMITTED
request_id: REQ-PRESTART-USD3-CHECK-20261120
request_revision: 1
project_id: COWORK-AUTO-APPROVAL-20261115-001
work_id: COWORK-AUTO-APPROVAL-20261115-001
skill_id: cowork-review-watcher
package_path: /SKILL-COLLAB/packages/{zipfile_local.name}
package_file_id: github:REQ-PRESTART-USD3-CHECK-20261120
package_rev: v0.2.29
package_sha256: {EXPECT['zip_sha256']}
package_size_bytes: {EXPECT['zip_size']}
baseline_package_ref: null
knowledge_refs: []
consumer_profiles: [windows-single-user-watcher]
reviewer_os: WINDOWS
test_policy: STATIC_ONLY
run_policy_ref: POLICY-STATIC-V1
output_contract: SKILL_COLLAB_REVIEW_RESULT_V1
goal: local prestart check only, never published
---

# prestart check
"""
(HERE / "prestart_req.md").write_bytes(rq.encode("utf-8"))
g2 = subprocess.run([sys.executable, str(gate), "check", "--live-config", str(CFG), "--intent", "unified", "--required-budget-usd", "3.00", "--request", str(HERE / "prestart_req.md"), "--package", str(zipfile_local)], capture_output=True, text=True)
try:
    sel = json.loads(g1.stdout)
    chk = json.loads(g2.stdout)
except ValueError:
    sel, chk = {}, {}
r["gate_check_unified_real_config"] = {"rc": g2.returncode, "status": chk.get("status"), "run_policy_ref": chk.get("run_policy_ref"), "expected_max_budget_usd": chk.get("expected_max_budget_usd"),
                                       "model_calls": chk.get("model_calls"), "ready": chk.get("ready"), "authorization": chk.get("authorization"), "package_sha256": chk.get("package_sha256")}
if not (g1.returncode == 0 and sel.get("status") == "POLICY_COMPATIBLE_NOT_APPROVED" and sel.get("selected_run_policy_ref") == "POLICY-STATIC-V1"
        and g2.returncode == 0 and chk.get("status") == "PASS_PREPUBLICATION_ONLY" and chk.get("model_calls") == 0 and chk.get("ready") == "NOT_CREATED"
        and chk.get("package_sha256") == EXPECT["zip_sha256"]):
    fail.append("unified gate")

# legacy classification against the NEW enabled_at, real requests + real DB (read-only snapshot)
snap = HERE / "prestart_snapshot.sqlite3"
if snap.exists():
    snap.unlink()
r["db"] = db_snapshot(snap)
lg = subprocess.run([sys.executable, str(HERE.parent / "v029_live" / "classify_legacy.py"), str(snap)], capture_output=True, text=True, encoding="utf-8")
cls = json.loads(lg.stdout)
(HERE / "legacy_after_align.json").write_text(json.dumps(cls, ensure_ascii=False, indent=1), encoding="utf-8")
new_en = datetime.fromisoformat(s3["ENABLED_AT_NEW"]).timestamp()
older = [x for x in cls["rows"] if x["created_utc"] and datetime.fromisoformat(x["created_utc"].replace("Z", "+00:00")).timestamp() < new_en]
r["legacy_after"] = {"requests": cls["requests"], "summary": cls["summary"], "created_before_new_enabled_at": len(older), "static_no_history": cls["summary"].get("NO_HISTORY_STATIC_PENDING", 0),
                     "all_blocked_by_new_enabled_at_or_history": len(older) == cls["requests"]}
if not (r["legacy_after"]["all_blocked_by_new_enabled_at_or_history"] and r["legacy_after"]["static_no_history"] == 0 and cls["requests"] == 18):
    fail.append("legacy after align")
if r["db"]["integrity"] != "ok" or r["db"]["jobs_by_state"] != {"COMPLETED": 9} or r["db"]["auto_claims_by_stage"] != {"READY_POSTED": 2, "UNCERTAIN": 1} or r["db"]["audit_max_id"] != load("step2_stop_backup.json")["db_stopped"]["audit_max_id"]:
    fail.append("db changed while stopped")
r["provider_lease"] = r["db"]["lease"]
r["tasks"] = task_state()
if r["tasks"].get("SKILL-COLLAB-Notifier") != "Running" or [k for k, v in r["tasks"].items() if v == "Running" and k != "SKILL-COLLAB-Notifier"]:
    fail.append("task states")

# SHADOW on a separate temp DB with a throw-away signer, from the same bytes
run = HERE / "shadow_run"
if run.exists():
    shutil.rmtree(run)
shutil.copytree(stage, run)
for t in ("test_usd3_staged_prelive.py", "test_usd3_staged_cli_rehearsal.py"):
    shutil.copyfile(HERE.parent / "v029_live" / t, run / "tests" / t)
env2 = {**env, "STAGED_RESULTS": str(HERE / "shadow_results.jsonl")}
(HERE / "shadow_results.jsonl").unlink(missing_ok=True)
pt = subprocess.run([str(sys.executable.replace("python.exe", "python.exe")), "-m", "pytest", "-q", "-p", "no:cacheprovider", "tests/test_usd3_staged_prelive.py", "tests/test_usd3_staged_cli_rehearsal.py"],
                    cwd=run, capture_output=True, text=True, env=env2, timeout=900)
r["shadow"] = {"rc": pt.returncode, "summary": (pt.stdout.strip().splitlines() or [""])[-1]}
if pt.returncode != 0:
    fail.append("shadow")
r["fail"] = fail
r["PRESTART_CHECK"] = "PASS" if not fail else "FAIL"
if fail:
    r["rollback"] = rollback(load("step2_stop_backup.json")["cutover_bundle"]["target"])
save("step4_prestart.json", r)
print(json.dumps(r, ensure_ascii=False, indent=2, default=str))
