import sqlite3, sys
sys.path.insert(0, ".")
sys.stdout.reconfigure(encoding="utf-8")
import observe_lib as o
con = sqlite3.connect("file:C:/Users/ME/AppData/Local/skill-collab-watcher-github/state.sqlite3?mode=ro", uri=True)
print("event name | count | flagged_by_current_rule")
for e, n in con.execute("SELECT event, COUNT(*) FROM audit_log GROUP BY event ORDER BY COUNT(*) DESC"):
    print(f"{e:36} {n:6}  {'BAD' if o.event_is_bad(e) else 'ok'}")
