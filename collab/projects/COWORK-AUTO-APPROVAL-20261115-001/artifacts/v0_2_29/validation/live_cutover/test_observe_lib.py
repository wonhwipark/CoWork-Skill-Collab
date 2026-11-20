"""Observation rules tested against the REAL audit history (every event name and every TRANSPORT_ERROR detail ever recorded) and against synthetic dangerous cases."""
import json, pathlib, sqlite3
import observe_lib as o

HERE = pathlib.Path(__file__).parent
s4 = json.loads((HERE / "step4_prestart.json").read_text(encoding="utf-8"))
BASE = ({"COMPLETED": 9}, {"READY_POSTED": 2, "UNCERTAIN": 1}, s4["db"]["lease"])
DB = "file:C:/Users/ME/AppData/Local/skill-collab-watcher-github/state.sqlite3?mode=ro"
BENIGN_HISTORY = {"SCAN_START", "SCAN_END", "VALIDATED", "WAIT_INPUT", "WATCH_RECOVERED", "WATCH_BACKOFF", "APPROVAL_REJECTED", "TRANSPORT_ERROR", "AUTO_PRE_EXISTING_REQUEST", "AUTO_NOT_ELIGIBLE",
                  "TRUST_ROOT_LOADED", "TRUST_ROOT_INDEPENDENCE_WARNING", "WATCH_START", "APPROVAL_REPO_ID_UNVERIFIABLE", "DUPLICATE_SKIPPED", "AUTO_DUPLICATE_BLOCKED", "DAILY_BUDGET_BLOCKED"}
DANGEROUS_HISTORY = {"REVIEW_DISPATCHED", "REVIEW_COST", "COMPLETED", "CLAIMED", "AUTO_RESERVED", "AUTO_SIGNED_LOCAL", "AUTO_READY_POSTED", "AUTO_APPROVAL_POSTED", "AUTO_SIGNING_UNCERTAIN"}


def q(sql, *a):
    con = sqlite3.connect(DB, uri=True)
    rows = con.execute(sql, a).fetchall()
    con.close()
    return rows


def healthy_view(key, extra_events=None, transport=()):
    ev = {"SCAN_START": 1, "TRUST_ROOT_LOADED": 1, "WATCH_START": 1, "AUTO_NOT_ELIGIBLE": 1, "AUTO_PRE_EXISTING_REQUEST": 1, "WAIT_INPUT": 2, "VALIDATED": 1, "APPROVAL_REJECTED": 1}
    ev.update(extra_events or {})
    return {"events": ev, "pairs": [("VALIDATED", key, "ok"), ("APPROVAL_REJECTED", key, "APPROVAL_EXPIRED")], "transport": list(transport),
            "jobs": {"COMPLETED": 9}, "claims": {"READY_POSTED": 2, "UNCERTAIN": 1}, "lease": s4["db"]["lease"]}


def known():
    return {r[0] for r in q("SELECT DISTINCT processing_key FROM audit_log WHERE event='APPROVAL_REJECTED' AND detail='APPROVAL_EXPIRED' AND id<=?", s4["db"]["audit_max_id"])}


def v0214():
    return q("SELECT processing_key FROM audit_log WHERE event='APPROVAL_REJECTED' AND processing_key LIKE 'REQ-COWORK-V0214-R1%' ORDER BY id LIMIT 1")[0][0]


def test_every_event_name_in_the_real_history_is_classified_correctly():
    names = {r[0] for r in q("SELECT DISTINCT event FROM audit_log")}
    assert names <= BENIGN_HISTORY | DANGEROUS_HISTORY, names - (BENIGN_HISTORY | DANGEROUS_HISTORY)
    for n in names & BENIGN_HISTORY:
        assert not o.event_is_bad(n), n
    for n in names & DANGEROUS_HISTORY:
        assert o.event_is_bad(n), n


def test_every_real_transport_error_detail_is_recognised_as_transient():
    details = [r[0] for r in q("SELECT detail FROM audit_log WHERE event='TRANSPORT_ERROR'")]
    assert len(details) >= 40
    bad = [d for d in details if not o.transport_detail_is_transient(d)]
    assert not bad, bad[:3]


def test_real_non_transient_transport_problems_are_not_tolerated():
    for d in ("REQ-X: TransportError: GitHub HTTP 401 Bad credentials", "TransportError: GitHub HTTP 403 forbidden", "AuthRequired: token rejected", "REQ-X: TransportError: unexpected shape"):
        v = healthy_view(v0214(), transport=[d])
        assert o.anomalies(v, *BASE, [1, 2], known()), d


def test_a_healthy_start_with_a_transient_network_error_and_the_known_pair_is_clean():
    d = "REQ-COWORK-BUDGET-V025-DESIGN-R1-20261117: TransportError: network error: URLError"
    assert o.anomalies(healthy_view(v0214(), transport=[d]), *BASE, [1, 2], known()) == []


def test_unknown_key_pair_and_non_expired_rejection_are_anomalies():
    assert o.anomalies(healthy_view("REQ-NEW-1|1|" + "a" * 64 + "|1"), *BASE, [1, 2], known())
    v = healthy_view(v0214())
    v["pairs"] = [("VALIDATED", v0214(), "ok"), ("APPROVAL_REJECTED", v0214(), "SIGNATURE_INVALID")]
    assert o.anomalies(v, *BASE, [1, 2], known())


def test_signing_ready_dispatch_claim_and_state_changes_are_caught():
    for e in DANGEROUS_HISTORY | {"WATCH_ERROR", "AUTH_REQUIRED", "REVIEW_FAILED", "AUTO_ERROR"}:
        assert o.anomalies(healthy_view(v0214(), {e: 1}), *BASE, [1, 2], known()), e
    for key, val in (("jobs", {"COMPLETED": 9, "CLAIMED": 1}), ("claims", {"READY_POSTED": 3, "UNCERTAIN": 1}), ("lease", [("1", "dropbox", "1", "x")])):
        v = healthy_view(v0214())
        v[key] = val
        assert o.anomalies(v, *BASE, [1, 2], known()), key
    assert o.anomalies(healthy_view(v0214()), *BASE, [1, 2, 3, 4], known())


def test_lease_tuple_vs_list():
    assert o.norm_lease([("1", "github", "1", "2026-11-14T22:57:57.244538+00:")]) == o.norm_lease([["1", "github", "1", "2026-11-14T22:57:57.244538+00:00"]])
