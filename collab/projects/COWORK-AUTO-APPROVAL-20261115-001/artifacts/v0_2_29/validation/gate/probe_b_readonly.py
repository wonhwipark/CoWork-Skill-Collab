"""Read-only checks for lane B: (1) is there an existing writer/updater tool in the repo tree, (2) does the real GitHub contents API agree with the
git blob sha rule used by the CAS adapter, (3) does a missing path read as (None, None). No write of any kind."""
import base64, hashlib, json, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8")
REPO = "wonhwipark/CoWork-Skill-Collab"


def gh(*a):
    r = subprocess.run(["gh", "api", *a], capture_output=True)
    return r.returncode, r.stdout, r.stderr.decode("utf-8", "replace")


def blob_sha(b):
    return hashlib.sha1(b"blob %d\x00" % len(b) + b).hexdigest()


rc, out, _ = gh(f"repos/{REPO}/git/trees/main?recursive=1")
tree = json.loads(out)
paths = [t["path"] for t in tree["tree"] if t["type"] == "blob"]
print("tree truncated:", tree.get("truncated"), "blobs:", len(paths))
hits = [p for p in paths if any(k in p.lower() for k in ("writer", "updater", "kernel", "cas_", "rebase")) and not p.startswith("collab/projects/")]
print("writer/updater/kernel-like paths outside collab/projects:", hits[:30] or "none")
in_projects = [p for p in paths if any(k in p.lower().rsplit("/", 1)[-1] for k in ("writer", "updater", "rebase")) and p.startswith("collab/projects/")]
print("under collab/projects (names only):", [p.rsplit("/", 1)[-1] for p in in_projects][:20])

for path in ("collab/projects/COWORK-AUTO-APPROVAL-20261115-001/CURRENT.md", "collab/projects/COWORK-AUTO-APPROVAL-20261115-001/TRACKER.json"):
    rc, out, err = gh(f"repos/{REPO}/contents/{path}?ref=main")
    j = json.loads(out)
    data = base64.b64decode(j["content"])
    print(path.rsplit("/", 1)[-1], "api_sha", j["sha"][:12], "computed_blob_sha", blob_sha(data)[:12], "match", blob_sha(data) == j["sha"], "size", len(data), j["size"])

rc, out, err = gh(f"repos/{REPO}/contents/collab/projects/COWORK-AUTO-APPROVAL-20261115-001/__does_not_exist__.md?ref=main")
print("missing path rc", rc, "404" in err)
