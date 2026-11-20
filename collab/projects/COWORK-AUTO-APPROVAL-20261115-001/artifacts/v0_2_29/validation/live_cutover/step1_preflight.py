"""STEP 1 - HOST_PREFLIGHT + LEGACY_GATE. READ-ONLY. Writes only into the local cutover work folder."""
import re, zipfile
from cutover_common import *

r = {"started": time.strftime("%Y-%m-%d %H:%M:%S")}
stop = []

# duplicate / progress check on main
rc = subprocess.run(["gh", "api", f"repos/{REPO}/contents/{W}", "--jq", ".[].name"], capture_output=True, text=True).stdout.split()
r["existing_cutover_files"] = [n for n in rc if "CUTOVER_RESULT" in n or "LIVE_CUTOVER" in n and n.startswith("CLAUDE_")]
if r["existing_cutover_files"]:
    stop.append("a cutover result already exists")
cur = (gh_raw(f"{W}/CURRENT.md") or b"").decode("utf-8", "replace").splitlines()
r["current_top"] = cur[2][:150] if len(cur) > 2 else None

# pinned ZIP
z = gh_raw(f"{W}/artifacts/v0_2_29/skill-collab-watcher_v0_2_29_1120.zip")
(HERE / "pinned.zip").write_bytes(z)
zinfo = {"bytes": len(z), "sha256": hashlib.sha256(z).hexdigest()}
with zipfile.ZipFile(HERE / "pinned.zip") as zf:
    zinfo["members"], zinfo["crc_bad"] = len(zf.namelist()), zf.testzip()
    zinfo["unsafe_paths"] = [n for n in zf.namelist() if n.startswith(("/", "\\")) or ".." in n.split("/") or ":" in n]
r["zip"] = zinfo
if not (zinfo["sha256"] == EXPECT["zip_sha256"] and zinfo["bytes"] == EXPECT["zip_size"] and zinfo["crc_bad"] is None and not zinfo["unsafe_paths"]):
    stop.append("ZIP mismatch")

# live state vs expected
live_tree = tree(LIVE)
r["live"] = {"tree_sha256": tree_sha(live_tree), "config_sha": sha(CFG), "delegation_sha": sha(DELEG), "version_line": (LIVE / "skill_collab_watcher" / "__init__.py").read_text(encoding="utf-8").strip()}
for k, e in (("tree_sha256", "live_tree"), ("config_sha", "config_sha"), ("delegation_sha", "delegation_sha")):
    if r["live"][k] != EXPECT[e]:
        stop.append(f"live {k} differs from the recorded value")

# existing backup bundle: bytes, manifest, DB snapshot and independent GitHub record
man = json.loads((BUNDLE / "MANIFEST.json").read_text(encoding="utf-8"))
bad = [k for k, v in man.items() if not (BUNDLE / k).exists() or sha(BUNDLE / k) != v]
rec = (gh_raw(f"{W}/CLAUDE_V029_LIVE_BACKUP_BUNDLE_RESULT_FOR_GPT_20261120.md") or b"").decode("utf-8", "replace")
r["bundle"] = {"files_in_manifest": len(man), "bad_files": bad, "manifest_sha": sha(BUNDLE / "MANIFEST.json"), "db_snapshot_sha": man.get("state/state.sqlite3"),
               "install_tree_sha": tree_sha(tree(BUNDLE / "install")), "github_record_has_manifest_sha": EXPECT["bundle_manifest"] in rec,
               "github_record_has_db_sha": EXPECT["bundle_db"] in rec, "github_record_has_tree_sha": EXPECT["live_tree"] in rec,
               "private_key_files": [k for k in man if "approver.key" in k or "approver.pass" in k]}
b = r["bundle"]
if bad or b["manifest_sha"] != EXPECT["bundle_manifest"] or b["db_snapshot_sha"] != EXPECT["bundle_db"] or b["install_tree_sha"] != EXPECT["live_tree"] or not (b["github_record_has_manifest_sha"] and b["github_record_has_db_sha"]) or b["private_key_files"]:
    stop.append("backup bundle integrity not established independently")

# tasks, processes, DB, in-flight
r["tasks"] = task_state()
r["watcher_pids"] = watcher_procs()
if r["tasks"].get(TASK) != "Running":
    stop.append("watcher task is not Running at start")
snap = HERE / "preflight_snapshot.sqlite3"
if snap.exists():
    snap.unlink()
r["db"] = db_snapshot(snap)
inflight = [s for s in r["db"]["jobs_by_state"] if s != "COMPLETED"]
if inflight or r["db"]["integrity"] != "ok" or r["db"]["auto_claims_by_stage"] != {"READY_POSTED": 2, "UNCERTAIN": 1}:
    stop.append(f"DB state unexpected: {r['db']}")

# authority (no write performed)
who = ps("whoami /groups")
r["authority"] = {"elevated_high_integrity": "S-1-16-12288" in who, "delegation_open_rw": False, "config_open_rw": False}
for key, p in (("delegation_open_rw", DELEG), ("config_open_rw", CFG)):
    try:
        open(p, "r+b").close()
        r["authority"][key] = True
    except OSError as e:
        r["authority"][key] = f"DENIED {e.errno}"
try:
    r["authority"]["install_dir_acl_has_modify_for_users"] = "Authenticated Users:(I)(M)" in subprocess.run(["icacls", str(LIVE)], capture_output=True, text=True).stdout
except Exception:
    pass
if r["authority"]["delegation_open_rw"] is not True or r["authority"]["config_open_rw"] is not True:
    stop.append("protected file write permission not available")
dele = json.loads(DELEG.read_text(encoding="utf-8"))
r["delegation"] = {k: dele.get(k) for k in ("enabled", "max_request_usd", "enabled_at", "expires_at", "project_families", "skills", "repo_id")}
if dele["enabled_at"] != EXPECT["old_enabled_at"] or dele["expires_at"] != EXPECT["expires_at"]:
    stop.append("delegation dates differ from the recorded values")

# baseline gate on the real config (must still be the old state)
g = subprocess.run([sys.executable, str(HERE.parent / "v028" / "review_request_gate.py"), "select", "--live-config", str(CFG), "--intent", "unified", "--required-budget-usd", "3.00"], capture_output=True, text=True)
r["gate_before"] = (g.stdout or g.stderr).strip()[:120]

# LEGACY_GATE on the fresh snapshot
lg = subprocess.run([sys.executable, str(HERE.parent / "v029_live" / "classify_legacy.py"), str(snap)], capture_output=True, text=True, encoding="utf-8")
cls = json.loads(lg.stdout)
r["legacy"] = {"requests": cls["requests"], "summary": cls["summary"], "static_no_history": cls["summary"].get("NO_HISTORY_STATIC_PENDING", 0),
               "latest_created_utc": max((x["created_utc"] for x in cls["rows"] if x["created_utc"]), default=None)}
(HERE / "legacy_before.json").write_text(json.dumps(cls, ensure_ascii=False, indent=1), encoding="utf-8")
if r["legacy"]["static_no_history"] != 0 or r["legacy"]["summary"].get("CLAIM_UNCERTAIN") != 1:
    stop.append(f"legacy gate not clean: {r['legacy']['summary']}")

r["stop_reasons"] = stop
r["PRECHECK"] = "PASS" if not stop else "FAIL"
save("step1_preflight.json", r)
print(json.dumps(r, ensure_ascii=False, indent=2, default=str))
