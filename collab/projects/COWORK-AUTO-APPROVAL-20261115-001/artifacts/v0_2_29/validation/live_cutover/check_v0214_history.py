import sqlite3, sys
sys.stdout.reconfigure(encoding="utf-8")
con = sqlite3.connect("file:C:/Users/ME/AppData/Local/skill-collab-watcher-github/state.sqlite3?mode=ro", uri=True)
rows = con.execute("SELECT id, ts, event, substr(coalesce(detail,''),1,80) FROM audit_log WHERE processing_key LIKE 'REQ-COWORK-V0214-R1%' ORDER BY id").fetchall()
print("events for REQ-COWORK-V0214-R1:", len(rows))
for r in rows[:40]:
    print(r)
print("--- WATCH_START events (id, ts, version)")
for r in con.execute("SELECT id, ts, substr(detail,1,40) FROM audit_log WHERE event='WATCH_START' ORDER BY id DESC LIMIT 12"):
    print(r)
print("--- jobs rows for V0214:", con.execute("SELECT COUNT(*) FROM jobs WHERE request_id LIKE 'REQ-COWORK-V0214-R1%'").fetchone()[0])
print("--- job_claims rows for V0214:", con.execute("SELECT COUNT(*) FROM job_claims WHERE processing_key LIKE 'REQ-COWORK-V0214-R1%'").fetchone()[0])
print("--- all event names seen after the first v0.2.25 start of the day that involve APPROVAL_REJECTED:")
for r in con.execute("SELECT event, COUNT(*), MIN(ts), MAX(ts) FROM audit_log WHERE event IN ('APPROVAL_REJECTED','VALIDATED') GROUP BY event"):
    print(r)
