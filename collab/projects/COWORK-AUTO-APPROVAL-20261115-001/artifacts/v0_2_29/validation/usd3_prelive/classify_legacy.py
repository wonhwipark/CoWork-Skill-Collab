"""READ-ONLY classification of every REQUEST on main against the consistent DB snapshot. Answers: after a cap raise to USD3 and a NEW enabled_at at cutover,
can any existing request become auto-eligible? Nothing is written to GitHub or to the operating DB."""
import json, re, sqlite3, subprocess, sys, time
from datetime import datetime, timezone

sys.stdout.reconfigure(encoding="utf-8")
SNAP = sys.argv[1]
REPO = "wonhwipark/CoWork-Skill-Collab"


def gh(*a):
    r = subprocess.run(["gh", "api", *a], capture_output=True)
    return r.returncode, r.stdout.decode("utf-8", "replace")


rc, out = gh(f"repos/{REPO}/contents/collab/requests?ref=main", "--jq", ".[].name")
ids = [x for x in out.split() if x.startswith("REQ-")]
con = sqlite3.connect(f"file:{SNAP}?mode=ro", uri=True)
jobs = {}
for rid, state in con.execute("SELECT request_id, state FROM jobs"):
    jobs.setdefault(rid, []).append(state)
claims = dict(con.execute("SELECT request_id, stage FROM auto_claims").fetchall())
seen = {r[0]: (r[1], r[2]) for r in con.execute("SELECT request_id, first_seen_at, enabled_at_first_seen FROM auto_seen")}
pending = {r[0] for r in con.execute("SELECT request_id FROM pending_requests")} if True else set()
now = time.time()
rows = []
for rid in ids:
    rc, files = gh(f"repos/{REPO}/contents/collab/requests/{rid}?ref=main", "--jq", "[.[].name]|join(\",\")")
    names = set(files.strip().split(",")) if rc == 0 else set()
    rc, raw = gh("-H", "Accept: application/vnd.github.raw", f"repos/{REPO}/contents/collab/requests/{rid}/REQUEST.md?ref=main")
    fm = {}
    if rc == 0:
        head = raw.split("\n---\n")[0]
        for line in head.splitlines():
            m = re.fullmatch(r"([a-z_]+): ?(.*)", line)
            if m:
                fm[m.group(1)] = m.group(2).strip()
    rc, cj = gh(f"repos/{REPO}/commits?path=collab/requests/{rid}/REQUEST.md&per_page=100", "--jq", "[.[].commit.committer.date]|last")
    created = cj.strip().strip('"')
    try:
        created_ts = datetime.fromisoformat(created.replace("Z", "+00:00")).timestamp()
    except ValueError:
        created_ts = None
    remote_hist = [n for n in ("APPROVAL_SIG.json", "READY.md") if n in names]
    # remote dispatch/receipt/review presence
    hist2 = []
    for folder in ("dispatch", "receipts", "reviews"):
        rc, _ = gh(f"repos/{REPO}/contents/collab/{folder}/{rid}?ref=main", "--jq", ".[0].name")
        if rc == 0:
            hist2.append(folder)
    policy = fm.get("run_policy_ref", "?")
    if jobs.get(rid) or hist2 or remote_hist:
        cls = "TERMINAL_HISTORY"
    elif claims.get(rid):
        cls = "CLAIM_" + claims[rid]
    elif rid in seen and seen[rid][1] == 0:
        cls = "SEEN_WHILE_DISABLED"
    elif policy != "POLICY-STATIC-V1":
        cls = "NO_HISTORY_NON_STATIC_TIER"
    else:
        cls = "NO_HISTORY_STATIC_PENDING"
    rows.append({"id": rid, "policy": policy, "class": cls, "jobs": jobs.get(rid), "claim": claims.get(rid), "seen": seen.get(rid), "in_pending_table": rid in pending,
                 "remote": remote_hist + hist2, "created_utc": created, "created_before_now": (created_ts is not None and created_ts < now)})
summary = {}
for r in rows:
    summary[r["class"]] = summary.get(r["class"], 0) + 1
print(json.dumps({"requests": len(rows), "summary": summary, "rows": rows}, ensure_ascii=False, indent=1))
