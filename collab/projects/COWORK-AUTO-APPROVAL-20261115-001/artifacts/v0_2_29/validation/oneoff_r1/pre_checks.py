import hashlib, json, sqlite3, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8")
REPO = "wonhwipark/CoWork-Skill-Collab"
RID = "REQ-COWORK-V029-ONEOFF-R1-20261120"
DB = r"C:\Users\ME\AppData\Local\skill-collab-watcher-github\state.sqlite3"


def gh(*a):
    r = subprocess.run(["gh", "api", *a], capture_output=True)
    return r.returncode, r.stdout, r.stderr.decode("utf-8", "replace")


for folder in ("requests", "reviews", "receipts", "dispatch"):
    rc, out, err = gh(f"repos/{REPO}/contents/collab/{folder}/{RID}")
    print(folder, "ABSENT(404)" if rc != 0 and "404" in err else ("PRESENT " + out.decode()[:200] if rc == 0 else "ERROR " + err[:100]))
rc, out, err = gh(f"repos/{REPO}/contents/collab/packages/skill-collab-watcher_v0_2_29_1120.zip?ref=main", "--jq", ".sha")
print("collab/packages v0_2_29 zip:", "ABSENT(404)" if rc != 0 and "404" in err else ("PRESENT sha " + out.decode().strip()))
rc, out, err = gh("-H", "Accept: application/vnd.github.raw",
                  f"repos/{REPO}/contents/collab/projects/COWORK-AUTO-APPROVAL-20261115-001/artifacts/v0_2_29/skill-collab-watcher_v0_2_29_1120.zip?ref=main")
print("artifact ZIP:", len(out), hashlib.sha256(out).hexdigest())
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
print("DB jobs for id:", con.execute("SELECT COUNT(*) FROM jobs WHERE request_id=?", (RID,)).fetchone()[0],
      "| auto_claims:", con.execute("SELECT COUNT(*) FROM auto_claims WHERE request_id=?", (RID,)).fetchone()[0],
      "| not-completed jobs:", con.execute("SELECT COUNT(*) FROM jobs WHERE state!='COMPLETED'").fetchone()[0])
con.close()
