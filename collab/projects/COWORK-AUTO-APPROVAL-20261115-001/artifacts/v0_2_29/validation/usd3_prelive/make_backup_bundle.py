"""REAL backup bundle of the LIVE v0.2.25 install (watcher keeps running; nothing is stopped, installed or changed).
Reads the live install/config/delegation/trust root/tasks/DB (online backup API for the DB) and writes ONLY under the target folder. Create-only: the target must not exist.
No private key and no passphrase file is copied."""
import hashlib, json, pathlib, shutil, sqlite3, subprocess, sys, time

sys.stdout.reconfigure(encoding="utf-8")
TARGET = pathlib.Path(sys.argv[1])
if TARGET.exists():
    sys.exit(f"STOP: target already exists (create-only): {TARGET}")
LIVE = pathlib.Path(r"D:\User\whpark\skill-collab-watcher-github")
STATE = pathlib.Path(r"C:\Users\ME\AppData\Local\skill-collab-watcher-github")
APPROVER = pathlib.Path(r"C:\Users\ME\AppData\Local\cowork-approver")
SKIP = (".venv", "__pycache__", "logs", ".git")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def tree(root):
    return {p.relative_to(root).as_posix(): sha(p) for p in sorted(root.rglob("*")) if p.is_file() and not any(s in p.parts for s in SKIP) and p.suffix != ".pyc"}


def tree_sha(t):
    return hashlib.sha256(json.dumps(t, sort_keys=True).encode()).hexdigest()


TARGET.mkdir(parents=True)
live_tree = tree(LIVE)
for rel in live_tree:
    d = TARGET / "install" / rel
    d.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(LIVE / rel, d)
(TARGET / "protected").mkdir()
for name in ("auto_delegation.json", "trust_root.json", "trust_root.sha256"):
    shutil.copyfile(APPROVER / name, TARGET / "protected" / name)
(TARGET / "state").mkdir()
src = sqlite3.connect(f"file:{STATE / 'state.sqlite3'}?mode=ro", uri=True)
live_counts = {t: src.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in ("jobs", "auto_claims", "auto_seen", "pending_requests")}
dst = sqlite3.connect(TARGET / "state" / "state.sqlite3")
src.backup(dst)
dst.close()
src.close()
snap = sqlite3.connect(TARGET / "state" / "state.sqlite3")
integ = snap.execute("PRAGMA integrity_check").fetchone()[0]
snap_counts = {t: snap.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in live_counts}
jobs_states = dict(snap.execute("SELECT state, COUNT(*) FROM jobs GROUP BY state").fetchall())
snap.close()
tasks = {}
for name in ("SKILL-COLLAB-GitHub-Watcher", "SKILL-COLLAB-Notifier"):
    r = subprocess.run(["schtasks", "/query", "/tn", name, "/xml"], capture_output=True)
    (TARGET / f"task_{name}.xml").write_bytes(r.stdout)
    tasks[name] = r.returncode
(TARGET / "README_RESTORE.txt").write_text(
    "Backup of the LIVE watcher v0.2.25 taken while it was running (nothing was stopped or changed).\n"
    "Contents: install/ (tree without .venv), protected/ (delegation + trust root, NO private key, NO passphrase), state/state.sqlite3 (online-backup-API snapshot),\n"
    "task_*.xml (scheduled task definitions), MANIFEST.json (sha256 of every file), BUNDLE_INFO.json.\n"
    "Restore rule: stop the watcher task first; restore install/, config and protected/ files from here and compare against MANIFEST.json.\n"
    "Restore state/state.sqlite3 ONLY if no paid job was processed after the cutover; otherwise keep the live DB. Do not move or delete D:\\User\\whpark\\skill-collab-watcher (its .venv is the task interpreter).\n"
    "Never restore over a running watcher.\n", encoding="utf-8")
info = {"taken_at": time.strftime("%Y-%m-%d %H:%M:%S"), "install_tree_sha256": tree_sha(live_tree), "install_files": len(live_tree),
        "version_line": (LIVE / "skill_collab_watcher" / "__init__.py").read_text(encoding="utf-8").strip(), "db_integrity": integ,
        "db_counts_live": live_counts, "db_counts_snapshot": snap_counts, "jobs_by_state": jobs_states, "task_export_rc": tasks,
        "config_sha256": sha(LIVE / "config" / "reviewer.config.json"), "delegation_sha256": sha(APPROVER / "auto_delegation.json")}
(TARGET / "BUNDLE_INFO.json").write_text(json.dumps(info, indent=2), encoding="utf-8")
manifest = {p.relative_to(TARGET).as_posix(): sha(p) for p in sorted(TARGET.rglob("*")) if p.is_file() and p.name != "MANIFEST.json"}
(TARGET / "MANIFEST.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")

# independent verification: re-read everything that was written
ok_manifest = all(sha(TARGET / k) == v for k, v in manifest.items())
ok_tree = tree_sha(tree(TARGET / "install")) == tree_sha(live_tree)
res = {"target": str(TARGET), "files": len(manifest) + 1, "manifest_verified": ok_manifest, "install_tree_equals_live": ok_tree, "info": info,
       "private_key_or_passphrase_in_bundle": any(("approver.key" in k or "approver.pass" in k) for k in manifest),
       "manifest_sha256": sha(TARGET / "MANIFEST.json"), "db_snapshot_sha256": manifest["state/state.sqlite3"]}
print(json.dumps(res, ensure_ascii=False, indent=2))
