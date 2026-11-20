"""Anomaly rules for the post-start observation, tested against the REAL audit history before they may trigger a rollback.

Baseline behaviour seen under every earlier version (0.2.20 / 0.2.23 / 0.2.25), tolerated here:
  * VALIDATED followed by APPROVAL_REJECTED(APPROVAL_EXPIRED) for a key that already has such a rejection before the cutover (stale READY, no local job, never CLAIMED);
  * TRANSPORT_ERROR caused by a transient network problem (URLError / RemoteDisconnected / GitHub HTTP 5xx), recovered on the next poll.
Anything that signs, posts READY, reserves, claims, dispatches, completes, costs, fails authentication, or changes jobs / claims / lease is an anomaly."""
import re

DANGER_SUBSTRINGS = ("SIGN", "READY", "DISPATCH", "CLAIM", "RESERV", "COMPLETED", "COST", "APPROVAL_POSTED", "UNCERTAIN", "FAIL", "AUTH")
PAIR_EVENTS = ("VALIDATED", "APPROVAL_REJECTED")
TRANSIENT = re.compile(r"(TransportError: network error: (URLError|RemoteDisconnected|timed out|ConnectionResetError|ConnectionAbortedError)|TransientTransportError: GitHub HTTP 5\d\d)")


def norm_lease(rows):
    return [tuple(str(x)[:25] for x in list(r)[:4]) for r in rows]


def event_is_bad(name: str) -> bool:
    if name in PAIR_EVENTS or name == "TRANSPORT_ERROR":
        return False                      # judged by key / detail below
    if any(s in name for s in DANGER_SUBSTRINGS):
        return True
    return "ERROR" in name


def transport_detail_is_transient(detail: str) -> bool:
    return bool(TRANSIENT.search(detail or ""))


def anomalies(view, base_jobs, base_claims, base_lease, pids, known_expired=frozenset()):
    bad = []
    for e, n in view["events"].items():
        if event_is_bad(e):
            bad.append(f"event {e} x{n}")
    for d in view.get("transport", []):
        if not transport_detail_is_transient(d):
            bad.append(f"non-transient transport problem: {d[:80]}")
    for e, k, d in view.get("pairs", []):
        if e == "APPROVAL_REJECTED" and not (d == "APPROVAL_EXPIRED" and k in known_expired):
            bad.append(f"unexpected rejection {k[:50]} {d}")
        if e == "VALIDATED" and k not in known_expired:
            bad.append(f"VALIDATED for a key without prior expired-approval history: {k[:50]}")
    if dict(view["jobs"]) != dict(base_jobs):
        bad.append(f"jobs changed {view['jobs']}")
    if dict(view["claims"]) != dict(base_claims):
        bad.append(f"auto_claims changed {view['claims']}")
    if norm_lease(view["lease"]) != norm_lease(base_lease):
        bad.append(f"lease changed {view['lease']}")
    if len(pids) > 2:
        bad.append(f"more than one watcher process pair: {pids}")
    return bad
