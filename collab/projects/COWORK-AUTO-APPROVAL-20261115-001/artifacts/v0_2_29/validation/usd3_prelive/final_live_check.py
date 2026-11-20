import hashlib, json, pathlib, sqlite3, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
LIVE = pathlib.Path(r"D:\User\whpark\skill-collab-watcher-github")
APPROVER = pathlib.Path(r"C:\Users\ME\AppData\Local\cowork-approver")
inv = json.loads((pathlib.Path(__file__).parent / "inv" / "inventory.json").read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def tree(root):
    out = {}
    for p in sorted(root.rglob("*")):
        if p.is_file() and not any(s in p.parts for s in (".venv", "__pycache__", "logs", ".git")) and p.suffix != ".pyc":
            out[p.relative_to(root).as_posix()] = sha(p)
    return hashlib.sha256(json.dumps(out, sort_keys=True).encode()).hexdigest()


ps = subprocess.run(["powershell", "-NoProfile", "-Command",
                     "Get-ScheduledTask | Where-Object {$_.TaskName -match 'SKILL-COLLAB|COWORK'} | ForEach-Object { '{0}|{1}' -f $_.TaskName, $_.State }"], capture_output=True, text=True).stdout
tasks_now = sorted(l.strip() for l in ps.splitlines() if l.strip())
tasks_then = sorted("|".join(t.split("|")[:2]) for t in inv["tasks"])
con = sqlite3.connect(f"file:C:/Users/ME/AppData/Local/skill-collab-watcher-github/state.sqlite3?mode=ro", uri=True)
jobs = dict(con.execute("SELECT state, COUNT(*) FROM jobs GROUP BY state").fetchall())
claims = dict(con.execute("SELECT stage, COUNT(*) FROM auto_claims GROUP BY stage").fetchall())
con.close()
res = {"install_tree_unchanged": tree(LIVE) == inv["live_tree"]["tree_sha256"], "config_sha_unchanged": sha(LIVE / "config" / "reviewer.config.json") == inv["config"]["sha256"],
       "delegation_sha_unchanged": sha(APPROVER / "auto_delegation.json") == inv["delegation"]["sha256"], "tasks_unchanged": tasks_now == tasks_then, "tasks_now": tasks_now,
       "jobs_by_state": jobs, "auto_claims_by_stage": claims,
       "version_line": (LIVE / "skill_collab_watcher" / "__init__.py").read_text(encoding="utf-8").strip()}
print(json.dumps(res, ensure_ascii=False, indent=2))
