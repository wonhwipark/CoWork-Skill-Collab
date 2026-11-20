"""Backup + rollback REHEARSAL, isolated. Reads the live install/config/delegation/DB/tasks (read-only) and writes ONLY under ./rehearsal.
It never stops a task, never writes to the live install, the live state dir or the approver folder."""
import hashlib, json, os, pathlib, shutil, sqlite3, subprocess, sys, time

sys.stdout.reconfigure(encoding="utf-8")
BASE = pathlib.Path(__file__).parent / "rehearsal"
if BASE.exists():
    shutil.rmtree(BASE)
BASE.mkdir()
LIVE = pathlib.Path(r"D:\User\whpark\skill-collab-watcher-github")
STATE = pathlib.Path(r"C:\Users\ME\AppData\Local\skill-collab-watcher-github")
APPROVER = pathlib.Path(r"C:\Users\ME\AppData\Local\cowork-approver")
OLD_VENV_PY = pathlib.Path(r"D:\User\whpark\skill-collab-watcher\.venv\Scripts\python.exe")
SKIP = (".venv", "__pycache__", "logs", ".git")
rep = {"started": time.strftime("%Y-%m-%d %H:%M:%S")}


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


# ---- BACKUP (to ./rehearsal/bundle) ----------------------------------------------------------------------------
bundle = BASE / "bundle"
(bundle / "install").mkdir(parents=True)
live_tree = tree(LIVE)
for rel in live_tree:
    dst = bundle / "install" / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(LIVE / rel, dst)
(bundle / "protected").mkdir()
for name in ("auto_delegation.json", "trust_root.json", "trust_root.sha256"):
    shutil.copyfile(APPROVER / name, bundle / "protected" / name)          # no private key and no passphrase file is copied
(bundle / "state").mkdir()
src = sqlite3.connect(f"file:{STATE / 'state.sqlite3'}?mode=ro", uri=True)
before_counts = {t: src.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in ("jobs", "auto_claims", "auto_seen", "audit_log", "pending_requests")}
dst = sqlite3.connect(bundle / "state" / "state.sqlite3")
src.backup(dst)
dst.close()
after_counts = {t: src.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in before_counts}
src.close()
snap = sqlite3.connect(bundle / "state" / "state.sqlite3")
snap_counts = {t: snap.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in before_counts}
integ = snap.execute("PRAGMA integrity_check").fetchone()[0]
snap.close()
tasks = {}
for name in ("SKILL-COLLAB-GitHub-Watcher", "SKILL-COLLAB-Notifier"):
    r = subprocess.run(["schtasks", "/query", "/tn", name, "/xml"], capture_output=True)
    (bundle / f"task_{name}.xml").write_bytes(r.stdout)
    tasks[name] = {"rc": r.returncode, "bytes": len(r.stdout)}
manifest = {p.relative_to(bundle).as_posix(): sha(p) for p in sorted(bundle.rglob("*")) if p.is_file()}
(bundle / "MANIFEST.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")
rep["backup"] = {"install_files": len(live_tree), "install_tree_sha256": tree_sha(live_tree), "bundle_files": len(manifest),
                 "db_snapshot_integrity": integ, "db_counts_live_before": before_counts, "db_counts_snapshot": snap_counts, "db_counts_live_after": after_counts,
                 "snapshot_matches_live_counts": snap_counts == before_counts or snap_counts == after_counts, "task_xml": tasks,
                 "private_key_or_passphrase_copied": any(("approver.key" in k or "approver.pass" in k) for k in manifest)}

# ---- ROLLBACK REHEARSAL (restore into ./rehearsal/restore, never over the live folders) ----------------------------
restore = BASE / "restore"
shutil.copytree(bundle / "install", restore / "install")
(restore / "state").mkdir()
shutil.copyfile(bundle / "state" / "state.sqlite3", restore / "state" / "state.sqlite3")
restored_tree = tree(restore / "install")
rep["rollback"] = {"restored_tree_equals_live_tree": tree_sha(restored_tree) == tree_sha(live_tree), "restored_files": len(restored_tree),
                   "restored_version_line": (restore / "install" / "skill_collab_watcher" / "__init__.py").read_text(encoding="utf-8").strip(),
                   "bundle_manifest_verified": all(sha(bundle / k) == v for k, v in manifest.items() if k != "MANIFEST.json" and (bundle / k).exists())}
cfg = json.loads((restore / "install" / "config" / "reviewer.config.json").read_text(encoding="utf-8"))
cfg["local_state_dir"] = str(restore / "state")
(restore / "restore_config.json").write_text(json.dumps(cfg), encoding="utf-8")
py = OLD_VENV_PY if OLD_VENV_PY.exists() else pathlib.Path(sys.executable)
env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
r = subprocess.run([str(py), "-m", "skill_collab_watcher.cli", "--config", str(restore / "restore_config.json"), "recover"],
                   cwd=restore / "install", capture_output=True, text=True, env=env, timeout=120)
rep["rollback"]["production_interpreter_used"] = str(py).endswith(r"skill-collab-watcher\.venv\Scripts\python.exe")
rep["rollback"]["restored_cli_recover"] = {"rc": r.returncode, "stdout": r.stdout.strip()[:200], "stderr": r.stderr.strip()[-200:]}
chk = sqlite3.connect(restore / "state" / "state.sqlite3")
rep["rollback"]["restored_db_integrity"] = chk.execute("PRAGMA integrity_check").fetchone()[0]
chk.close()
rep["live_unchanged_after_rehearsal"] = {"install_tree_sha256_same": tree_sha(tree(LIVE)) == tree_sha(live_tree),
                                         "delegation_sha_same": sha(APPROVER / "auto_delegation.json") == manifest["protected/auto_delegation.json"]}
rep["prod_interpreter_dependency"] = {"old_install_venv_python_exists": OLD_VENV_PY.exists(), "path": str(OLD_VENV_PY)}
(BASE / "rehearsal_result.json").write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(rep, ensure_ascii=False, indent=2))
