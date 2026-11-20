import hashlib, json, os, pathlib, sqlite3, subprocess, sys, time, zipfile

sys.stdout.reconfigure(encoding="utf-8")
HERE = pathlib.Path(__file__).parent
REPO = "wonhwipark/CoWork-Skill-Collab"
W = "collab/projects/COWORK-AUTO-APPROVAL-20261115-001"
LIVE = pathlib.Path(r"D:\User\whpark\skill-collab-watcher-github")
STATE = pathlib.Path(r"C:\Users\ME\AppData\Local\skill-collab-watcher-github")
APPROVER = pathlib.Path(r"C:\Users\ME\AppData\Local\cowork-approver")
OLD_PY = pathlib.Path(r"D:\User\whpark\skill-collab-watcher\.venv\Scripts\python.exe")
BUNDLE = pathlib.Path(r"D:\User\whpark\skill-collab-watcher-dist\backup_v0_2_25_install_20261120_200712")
TASK = "SKILL-COLLAB-GitHub-Watcher"
CFG = LIVE / "config" / "reviewer.config.json"
DELEG = APPROVER / "auto_delegation.json"
SKIP = (".venv", "__pycache__", "logs", ".git")
EXPECT = {
    "zip_sha256": "c67bc342fe77547b000fc42e1b886396cbef035c0d265dbcd124947e267ed83f", "zip_size": 310753,
    "live_tree": "f691bcf808cbf81e9c2c2a9be65335e527c2df99ea4d54a427665e4c90045c9f",
    "config_sha": "fbce30a97c06f8d04e2e0029c731c41d2ccd87963196afe80279f10cf7509c27",
    "delegation_sha": "ddead4e497759ac30db9e8d90974cfe4f68114d99ef99cdf85a083e9bf54fd4c",
    "bundle_manifest": "d23b52068733ec7dcce95024f6f919a0e30147e00b502b3bd449d29406256d92",
    "bundle_db": "111c85ab30de926759d1caebec78b65a228dd4ab7bfa126c3587ce13dd465fa5",
    "old_enabled_at": "2026-11-16T19:47:50+09:00", "expires_at": "2026-12-16T19:47:50+09:00",
}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def tree(root, skip=SKIP):
    return {p.relative_to(root).as_posix(): sha(p) for p in sorted(root.rglob("*"))
            if p.is_file() and not any(s in p.parts for s in skip) and p.suffix != ".pyc"}


def tree_sha(t):
    return hashlib.sha256(json.dumps(t, sort_keys=True).encode()).hexdigest()


def gh_raw(path, ref="main"):
    r = subprocess.run(["gh", "api", "-H", "Accept: application/vnd.github.raw", f"repos/{REPO}/contents/{path}?ref={ref}"], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def ps(cmd):
    return subprocess.run(["powershell", "-NoProfile", "-Command", cmd], capture_output=True, text=True).stdout


def task_state():
    out = ps("Get-ScheduledTask | Where-Object {$_.TaskName -match 'SKILL-COLLAB|COWORK'} | ForEach-Object { '{0}|{1}' -f $_.TaskName, $_.State }")
    return dict(l.strip().split("|") for l in out.splitlines() if "|" in l)


def watcher_procs():
    out = ps("Get-CimInstance Win32_Process | Where-Object { $_.Name -match '^pythonw?\\.exe$' -and $_.CommandLine -match 'skill_collab_watcher.cli' -and $_.CommandLine -match ' watch' } | ForEach-Object { $_.ProcessId }")
    return [int(x) for x in out.split() if x.strip().isdigit()]


def db_snapshot(dest):
    src = sqlite3.connect(f"file:{STATE / 'state.sqlite3'}?mode=ro", uri=True)
    dst = sqlite3.connect(dest)
    src.backup(dst)
    dst.close()
    src.close()
    con = sqlite3.connect(dest)
    info = {"integrity": con.execute("PRAGMA integrity_check").fetchone()[0],
            "jobs_by_state": dict(con.execute("SELECT state, COUNT(*) FROM jobs GROUP BY state").fetchall()),
            "auto_claims_by_stage": dict(con.execute("SELECT stage, COUNT(*) FROM auto_claims GROUP BY stage").fetchall()),
            "auto_seen": con.execute("SELECT COUNT(*) FROM auto_seen").fetchone()[0], "lease": [tuple(str(x)[:40] for x in r) for r in con.execute("SELECT * FROM provider_lease")],
            "audit_max_id": con.execute("SELECT MAX(id) FROM audit_log").fetchone()[0]}
    con.close()
    return info


def save(name, obj):
    (HERE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2, default=str), encoding="utf-8")


def load(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))
