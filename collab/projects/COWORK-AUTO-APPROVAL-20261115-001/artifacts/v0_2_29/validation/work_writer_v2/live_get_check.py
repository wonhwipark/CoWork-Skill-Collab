"""READ-ONLY live check of GhContents.get against the real PRIVATE repo. It never calls put()."""
import hashlib, json, os, sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "work_writer"))
import work_writer_v2 as w  # noqa: E402

g = w.GhContents("wonhwipark/CoWork-Skill-Collab")
W = "collab/projects/COWORK-AUTO-APPROVAL-20261115-001"
out = {}
for name in ("CURRENT.md", "TRACKER.json", "artifacts/v0_2_29/skill-collab-watcher_v0_2_29_1120.zip"):
    data, sha = g.get(f"{W}/{name}")
    out[name] = {"bytes": len(data), "blob_sha": sha[:12], "blob_rule_ok": w.blob_sha(data) == sha, "sha256": hashlib.sha256(data).hexdigest()[:16]}
out["missing_path"] = g.get(f"{W}/__does_not_exist__.md")
out["put_called"] = False
print(json.dumps(out, ensure_ascii=False, indent=2))
