"""READ-ONLY host inventory for the USD3 pre-live gate. Writes only into a temp folder given as argv[1] (snapshot rehearsal). No secret value is read or printed."""
import hashlib, json, os, pathlib, re, shutil, sqlite3, subprocess, sys, tempfile, time, zipfile

sys.stdout.reconfigure(encoding="utf-8")
OUT = pathlib.Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
LIVE = pathlib.Path(r"D:\User\whpark\skill-collab-watcher-github")
STATE = pathlib.Path(r"C:\Users\ME\AppData\Local\skill-collab-watcher-github")
APPROVER = pathlib.Path(r"C:\Users\ME\AppData\Local\cowork-approver")
REPO = "wonhwipark/CoWork-Skill-Collab"
rep = {}


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def tree(root, skip=(".venv", "__pycache__", "logs", ".git")):
    files = {}
    for p in sorted(root.rglob("*")):
        if p.is_file() and not any(s in p.parts for s in skip) and p.suffix != ".pyc":
            files[p.relative_to(root).as_posix()] = sha256(p)
    return files


# 1. installed tree vs the v0.2.25 package that was installed
live_files = tree(LIVE)
rep["live_tree"] = {"files": len(live_files), "tree_sha256": hashlib.sha256(json.dumps(live_files, sort_keys=True).encode()).hexdigest(),
                    "version_line": (LIVE / "skill_collab_watcher" / "__init__.py").read_text(encoding="utf-8").strip()}
r = subprocess.run(["gh", "api", "-H", "Accept: application/vnd.github.raw", f"repos/{REPO}/contents/collab/packages/skill-collab-watcher_v0_2_25_1117.zip?ref=main"], capture_output=True)
z025 = r.stdout
rep["v025_package"] = {"bytes": len(z025), "sha256": hashlib.sha256(z025).hexdigest()}
zp = OUT / "v025.zip"
zp.write_bytes(z025)
with zipfile.ZipFile(zp) as z:
    pkg = {n: hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if not n.endswith("/") and "__pycache__" not in n}
same = [n for n in pkg if live_files.get(n) == pkg[n]]
diff = [n for n in pkg if n in live_files and live_files[n] != pkg[n]]
missing = [n for n in pkg if n not in live_files]
extra = [n for n in live_files if n not in pkg]
rep["live_vs_v025_package"] = {"package_files": len(pkg), "identical": len(same), "different": diff[:20], "missing_in_live": missing[:20], "only_in_live": extra[:20]}

# 2. effective config prices and delegation (no secret values)
cfg = json.loads((LIVE / "config" / "reviewer.config.json").read_text(encoding="utf-8"))
rep["config"] = {"tiers": {k: v["max_budget_usd"] for k, v in cfg["review_policy"]["known_run_policy_refs"].items()},
                 "daily_budget_usd": cfg["review_policy"].get("daily_budget_usd"), "max_dispatches_per_day": cfg["review_policy"].get("max_dispatches_per_day"),
                 "acl_check": cfg["auto_approval"].get("acl_check"), "valid_hours": cfg["auto_approval"].get("valid_hours"),
                 "sha256": sha256(LIVE / "config" / "reviewer.config.json")}
d = json.loads((APPROVER / "auto_delegation.json").read_text(encoding="utf-8"))
rep["delegation"] = {**{k: d.get(k) for k in ("enabled", "policy", "max_request_usd", "enabled_at", "expires_at", "project_families", "projects", "skills", "repo_id", "branch")},
                     "sha256": sha256(APPROVER / "auto_delegation.json")}

# 3. ACL summary (principal classes only)
def acl(path):
    out = subprocess.run(["icacls", str(path)], capture_output=True, text=True).stdout
    rows = []
    for line in out.splitlines():
        m = re.search(r"(\S+)\s*:\s*\(([^)]*)\)(?:\(([^)]*)\))*", line.strip()) or re.search(r"^\s*(?:\S+\s+)?(\S+):(\(.*\))", line)
        if ":" in line and "(" in line:
            who, perms = line.strip().rsplit(":", 1)[0].split(" ")[-1], line.strip().rsplit(":", 1)[1]
            rows.append((who.split("\\")[-1] if "\\" in who else who, perms))
    return rows
rep["acl"] = {"delegation": acl(APPROVER / "auto_delegation.json"), "approver_key": acl(APPROVER / "approver.key.enc"), "live_config": acl(LIVE / "config" / "reviewer.config.json")}

# 4. scheduled tasks and watcher processes
ps = subprocess.run(["powershell", "-NoProfile", "-Command",
                     "Get-ScheduledTask | Where-Object {$_.TaskName -match 'SKILL-COLLAB|COWORK'} | ForEach-Object { $i = Get-ScheduledTaskInfo -TaskName $_.TaskName; '{0}|{1}|{2}|{3}' -f $_.TaskName, $_.State, $i.LastRunTime, $i.LastTaskResult }"],
                    capture_output=True, text=True).stdout
rep["tasks"] = [l.strip() for l in ps.splitlines() if l.strip()]
pr = subprocess.run(["powershell", "-NoProfile", "-Command",
                     "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'skill_collab_watcher|skill-collab' } | ForEach-Object { '{0}|{1}' -f $_.ProcessId, ($_.CommandLine -replace '\\s+',' ').Substring(0,[Math]::Min(150,($_.CommandLine).Length)) }"],
                    capture_output=True, text=True).stdout
rep["processes"] = [l.strip() for l in pr.splitlines() if l.strip()]

# 5. DB: consistent snapshot via the online backup API into the temp folder, then integrity and class counts
src = sqlite3.connect(f"file:{STATE / 'state.sqlite3'}?mode=ro", uri=True)
snap_path = OUT / "state_snapshot.sqlite3"
dst = sqlite3.connect(snap_path)
src.backup(dst)
dst.close()
snap = sqlite3.connect(snap_path)
rep["db"] = {"integrity_check": snap.execute("PRAGMA integrity_check").fetchone()[0],
             "tables": {t: snap.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for (t,) in snap.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")},
             "provider_lease": [tuple(str(x)[:60] for x in r) for r in snap.execute("SELECT * FROM provider_lease")],
             "jobs_by_state": dict(snap.execute("SELECT state, COUNT(*) FROM jobs GROUP BY state").fetchall()),
             "auto_claims_by_stage": dict(snap.execute("SELECT stage, COUNT(*) FROM auto_claims GROUP BY stage").fetchall()),
             "auto_seen": snap.execute("SELECT COUNT(*) FROM auto_seen").fetchone()[0]}
snap.close()
src.close()
rep["db"]["snapshot_sha256"] = sha256(snap_path)
rep["state_dir_files"] = sorted(p.name for p in STATE.iterdir() if p.is_file())

# 6. su_l1 wiring
hits = [str(p.relative_to(LIVE)) for p in (LIVE / "skill_collab_watcher").rglob("*.py") if "su_l1" in p.read_text(encoding="utf-8", errors="ignore")]
rep["su_l1_references_in_live_runtime"] = hits
rep["su_l1_in_live_config"] = "su_l1" in json.dumps(cfg)

(OUT / "inventory.json").write_text(json.dumps(rep, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
print(json.dumps(rep, ensure_ascii=False, indent=2, default=str))
