"""STEP 3 - INSTALL the pinned v0.2.29 ZIP and apply STATIC USD3 + delegation USD3 + a NEW enabled_at in one guarded interval (the watcher is stopped).
Any failure triggers a byte-checked rollback from the cutover bundle. The watcher is NOT started here."""
import re, shutil, zipfile
from datetime import datetime, timedelta, timezone
from cutover_common import *
from rollback_lib import acl_lines, atomic_write, rollback

r = {"started": time.strftime("%Y-%m-%d %H:%M:%S")}
s2 = load("step2_stop_backup.json")
bundle = s2["cutover_bundle"]["target"]
assert task_state().get(TASK) != "Running" and not watcher_procs(), "watcher must be stopped"
stage = HERE / "stage_zip"
if stage.exists():
    shutil.rmtree(stage)
with zipfile.ZipFile(HERE / "pinned.zip") as zf:
    zf.extractall(stage)
zip_tree = tree(stage)
live_before = tree(LIVE)
r["zip_files"] = len(zip_tree)
r["live_only_before"] = sorted(set(live_before) - set(zip_tree))
r["zip_only"] = sorted(set(zip_tree) - set(live_before))[:15]
r["acl_before"] = {"delegation": acl_lines(DELEG), "config": acl_lines(CFG)}
changed = []
try:
    # ---- install: package files only; config/reviewer.config.json and package/ are not in the ZIP and are never touched
    for rel, h in zip_tree.items():
        dst = LIVE / rel
        if dst.exists() and sha(dst) == h:
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        atomic_write(dst, (stage / rel).read_bytes())
        changed.append(rel)
    r["files_written"] = len(changed)
    stale = [rel for rel in r["live_only_before"] if rel != "config/reviewer.config.json" and not rel.startswith("package/")]
    r["stale_v025_only_files"] = stale
    for rel in stale:                                  # files that belonged to v0.2.25 and are not part of the reviewed v0.2.29 package
        (LIVE / rel).unlink()
    after = tree(LIVE)
    expect_after = {**zip_tree, **{k: v for k, v in live_before.items() if k == "config/reviewer.config.json" or k.startswith("package/")}}
    r["installed_tree_equals_zip_plus_preserved"] = after == expect_after
    r["version_line"] = (LIVE / "skill_collab_watcher" / "__init__.py").read_text(encoding="utf-8").strip()
    if not r["installed_tree_equals_zip_plus_preserved"] or r["version_line"] != '__version__ = "0.2.29"':
        raise RuntimeError("installed tree does not equal ZIP + preserved files")
    r["preserved"] = {"config_sha_same": sha(CFG) == EXPECT["config_sha"], "package_dir_files": sorted(k for k in after if k.startswith("package/"))}

    # ---- remote requests re-check right before the delegation write
    names = subprocess.run(["gh", "api", f"repos/{REPO}/contents/collab/requests", "--jq", ".[].name"], capture_output=True, text=True).stdout.split()
    r["remote_requests_now"] = len([n for n in names if n.startswith("REQ-")])

    # ---- aligned change: registry STATIC 3.00 (config) + delegation cap 3.0 + new enabled_at (delegation)
    cfg_text = CFG.read_text(encoding="utf-8")
    pat = re.compile(r'("POLICY-STATIC-V1":\s*\{\s*"max_budget_usd":\s*)1\.5')
    if len(pat.findall(cfg_text)) != 1:
        raise RuntimeError("config pattern for POLICY-STATIC-V1 not unique")
    new_cfg = pat.sub(r"\g<1>3.0", cfg_text)
    old_obj, new_obj = json.loads(cfg_text), json.loads(new_cfg)
    old_obj["review_policy"]["known_run_policy_refs"]["POLICY-STATIC-V1"]["max_budget_usd"] = 3.0
    if old_obj != new_obj:
        raise RuntimeError("config change is more than the single STATIC price")
    d_text = DELEG.read_text(encoding="utf-8")
    kst = timezone(timedelta(hours=9))
    enabled_at = datetime.now(kst).replace(microsecond=0).isoformat()
    for pattern, repl in ((r'("max_request_usd":\s*)1\.0', r"\g<1>3.0"), (r'("enabled_at":\s*")[^"]+(")', rf"\g<1>{enabled_at}\g<2>")):
        if len(re.findall(pattern, d_text)) != 1:
            raise RuntimeError(f"delegation pattern not unique: {pattern}")
        d_text = re.sub(pattern, repl, d_text)
    d_obj = json.loads(d_text)
    orig = json.loads((pathlib.Path(bundle) / "protected" / "auto_delegation.json").read_text(encoding="utf-8"))
    expect_obj = {**orig, "max_request_usd": 3.0, "enabled_at": enabled_at}
    if d_obj != expect_obj or not (datetime.fromisoformat(enabled_at) > datetime.fromisoformat(EXPECT["old_enabled_at"]) and datetime.fromisoformat(enabled_at) < datetime.fromisoformat(EXPECT["expires_at"])):
        raise RuntimeError("delegation change is more than cap + enabled_at, or enabled_at outside the allowed window")
    atomic_write(CFG, new_cfg.encode("utf-8"))
    atomic_write(DELEG, d_text.encode("utf-8"))
    r["ENABLED_AT_NEW"] = enabled_at
    r["config_new_sha"], r["delegation_new_sha"] = sha(CFG), sha(DELEG)
    r["acl_after"] = {"delegation": acl_lines(DELEG), "config": acl_lines(CFG)}
    r["acl_unchanged"] = r["acl_after"] == r["acl_before"]
    r["delegation_diff"] = {k: (orig.get(k), d_obj.get(k)) for k in d_obj if orig.get(k) != d_obj.get(k)}
    r["config_diff"] = "known_run_policy_refs.POLICY-STATIC-V1.max_budget_usd: 1.5 -> 3.0 (only)"
    r["INSTALL_AND_ALIGNMENT"] = "PASS_NOT_STARTED"
except Exception as exc:  # noqa: BLE001
    r["error"] = f"{type(exc).__name__}: {exc}"[:400]
    r["rollback"] = rollback(bundle)
    r["INSTALL_AND_ALIGNMENT"] = "FAIL_ROLLED_BACK" if r["rollback"]["verified"] else "FAIL_ROLLBACK_UNVERIFIED"
save("step3_install_align.json", r)
print(json.dumps(r, ensure_ascii=False, indent=2, default=str))
