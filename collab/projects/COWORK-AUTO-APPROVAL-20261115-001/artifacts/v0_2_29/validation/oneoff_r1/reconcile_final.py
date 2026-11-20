import hashlib, json, sqlite3, sys, zipfile
sys.stdout.reconfigure(encoding="utf-8")
DB = r"C:\Users\ME\AppData\Local\skill-collab-watcher-github\state.sqlite3"
RID = "REQ-COWORK-V029-ONEOFF-R1-20261120"
KEY = f"{RID}|1|c67bc342fe77547b000fc42e1b886396cbef035c0d265dbcd124947e267ed83f|1"
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
ev = {}
for e, in con.execute("SELECT event FROM audit_log WHERE processing_key=?", (KEY,)):
    ev[e] = ev.get(e, 0) + 1
print("events for key:", ev)
print("job:", con.execute("SELECT state, attempt_count, last_error FROM jobs WHERE processing_key=?", (KEY,)).fetchone())
print("jobs not COMPLETED:", con.execute("SELECT COUNT(*) FROM jobs WHERE state!='COMPLETED'").fetchone()[0],
      "| auto_claims for id:", con.execute("SELECT COUNT(*) FROM auto_claims WHERE request_id=?", (RID,)).fetchone()[0])
cost = [json.loads(d) for (d,) in con.execute("SELECT detail FROM audit_log WHERE processing_key=? AND event='REVIEW_COST'", (KEY,))]
print("cost rows:", [(c["total_cost_usd"], c["num_turns"]) for c in cost])
con.close()
rc = json.loads(open(r"D:\User\whpark\cowork-phase1\v029_rev\RECEIPT_1.md", encoding="utf-8").read())
print("receipt:", {k: rc.get(k) for k in ("ok", "processing_key", "request_id", "request_revision", "package_sha256", "watcher_version")}, "key_match", rc["processing_key"] == KEY)
dp = json.loads(open(r"D:\User\whpark\cowork-phase1\v029_rev\DISPATCH_1.md", encoding="utf-8").read())
print("dispatch:", {k: dp.get(k) for k in ("processing_key", "request_id", "package_sha256", "watcher_version")}, "key_match", dp["processing_key"] == KEY)

# Q8 carry-over, checked by me on the pinned ZIP bytes
z = zipfile.ZipFile(r"D:\User\whpark\cowork-phase1\v029_rev\skill-collab-watcher_v0_2_29_1120.zip")
for name in ("docs/AUTO_APPROVAL.md", "docs/BUDGET_POLICY_CONFIGURATION.md"):
    text = z.read(name).decode("utf-8")
    hits = [(i + 1, l.strip()[:150]) for i, l in enumerate(text.splitlines()) if any(k in l for k in ("max_day", "max_month", "day <=", "approve_request", "month <="))]
    print(name, hits)
