"""Tests for work_writer_v2. Mock contents API, injected fake gh runner, throw-away DB from the pinned package's StateStore.
No GitHub write, no model, no operating state. Set V029_PKG to the extracted pinned package root for the DB based tests."""
import base64
import hashlib
import json
import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "work_writer"))        # v1 module, published unchanged
PKG = os.environ.get("V029_PKG")
if PKG:
    sys.path.insert(0, PKG)

import work_writer as v1  # noqa: E402
import work_writer_v2 as w  # noqa: E402

HEADER = "# W — CURRENT\n"


def entry(n):
    return f"\n## window {n}\n- result {n}\n\n---\n"


class Scripted:
    """Contents client that returns a stale sha for the first N puts (always Conflict) and counts every call."""

    def __init__(self, fail_puts, inner=None):
        self.inner, self.fail_puts, self.gets, self.puts = inner or v1.MockContents(), fail_puts, 0, 0

    def get(self, p):
        self.gets += 1
        return self.inner.get(p)

    def put(self, p, d, s, m=""):
        self.puts += 1
        if self.puts <= self.fail_puts:
            raise v1.Conflict(p)
        return self.inner.put(p, d, s, m)


# ---------------------------------------------------------------- two-wave caller rule
def test_wave_two_recovers_after_wave_one_is_exhausted_within_eight_attempts():
    c = Scripted(fail_puts=4)
    r = w.cas_two_wave(c, "CURRENT.md", v1.current_merge(HEADER, "window 1", entry(1)), sleep=lambda s: None)
    assert r.status == "DONE" and r.waves == 2 and r.attempts <= 8 and c.puts == 5
    assert c.inner.files["CURRENT.md"].decode().count("window 1") == 1


def test_both_waves_exhausted_is_post_conflict_pending_not_an_exception_and_never_overwrites():
    c = Scripted(fail_puts=99)
    r = w.cas_two_wave(c, "CURRENT.md", v1.current_merge(HEADER, "window 1", entry(1)), sleep=lambda s: None)
    assert r.status == "POST_CONFLICT_PENDING" and r.waves == 2 and r.attempts == 8 and c.puts == 8
    assert "CURRENT.md" not in c.inner.files and "8" in r.evidence


def test_already_applied_remote_state_succeeds_without_a_second_put():
    c = Scripted(fail_puts=0)
    m = v1.current_merge(HEADER, "window 1", entry(1))
    w.cas_two_wave(c, "CURRENT.md", m, sleep=lambda s: None)
    puts = c.puts
    r = w.cas_two_wave(c, "CURRENT.md", m, sleep=lambda s: None)
    assert r.status == "UNCHANGED" and c.puts == puts


@pytest.mark.parametrize("exc", [w.TransportError("auth"), ValueError("bad merge"), w.NeedsDecision("x")])
def test_non_stale_failures_are_never_re_called(exc):
    class Boom(Scripted):
        def put(self, *a):
            self.puts += 1
            raise exc

    c = Boom(fail_puts=0)
    merge = (lambda old: (_ for _ in ()).throw(exc)) if isinstance(exc, (ValueError, w.NeedsDecision)) else v1.current_merge(HEADER, "w", entry(1))
    with pytest.raises(type(exc)):
        w.cas_two_wave(c, "CURRENT.md", merge, sleep=lambda s: None)
    assert c.puts <= 1 and c.gets == 1


def test_readback_mismatch_is_not_retried_by_the_caller_rule():
    class Lying(v1.MockContents):
        def get(self, p):
            data, sha = super().get(p)
            return (b"something else", sha) if self.puts else (data, sha)

    c = Lying()
    with pytest.raises(v1.ReadbackMismatch):
        w.cas_two_wave(c, "CURRENT.md", v1.current_merge(HEADER, "window 1", entry(1)), sleep=lambda s: None)
    assert c.puts == 1


def test_short_read_after_write_staleness_is_tolerated():
    class Stale(v1.MockContents):
        def __init__(self):
            super().__init__()
            self.after_put_reads = 0

        def get(self, p):
            data, sha = super().get(p)
            if self.puts and self.after_put_reads < 2:
                self.after_put_reads += 1
                return None, None
            return data, sha

    c = Stale()
    r = w.cas_update(c, "CURRENT.md", v1.current_merge(HEADER, "window 1", entry(1)))
    assert r.changed


# ---------------------------------------------------------------- strict tracker merge
def _tracker(c, work, **f):
    v1.cas_update(c, "TRACKER.json", v1.tracker_merge(work, f))


def test_strict_merge_accepts_when_nobody_else_changed_the_work():
    c = v1.MockContents()
    _tracker(c, "W1", phase="REVIEW", next_action="a")
    v1.cas_update(c, "TRACKER.json", w.tracker_merge_strict("W1", {"phase": "COMPLETE", "next_action": "b"}, {"phase": "REVIEW", "next_action": "a"}))
    assert json.loads(c.files["TRACKER.json"])["works"][0]["phase"] == "COMPLETE"


def test_strict_merge_refuses_to_overwrite_a_conflicting_update_by_another_writer():
    c = v1.MockContents()
    _tracker(c, "W1", phase="REVIEW", next_action="a")
    _tracker(c, "W1", phase="BLOCKED", next_action="other writer")
    before = c.files["TRACKER.json"]
    with pytest.raises(w.NeedsDecision):
        v1.cas_update(c, "TRACKER.json", w.tracker_merge_strict("W1", {"phase": "COMPLETE", "next_action": "mine"}, {"phase": "REVIEW", "next_action": "a"}))
    assert c.files["TRACKER.json"] == before


def test_strict_merge_is_fine_when_the_other_writer_already_wrote_the_same_value():
    c = v1.MockContents()
    _tracker(c, "W1", phase="REVIEW", next_action="a")
    _tracker(c, "W1", phase="COMPLETE", next_action="b")
    r = v1.cas_update(c, "TRACKER.json", w.tracker_merge_strict("W1", {"phase": "COMPLETE", "next_action": "b"}, {"phase": "REVIEW", "next_action": "a"}))
    assert not r.changed


# ---------------------------------------------------------------- real adapter with an injected fake gh
def _api_file(data, sha=None, encoding="base64"):
    return json.dumps({"sha": sha or v1.blob_sha(data), "size": len(data), "encoding": encoding,
                       "content": base64.b64encode(data).decode() if encoding == "base64" else ""}).encode()


def test_gh_adapter_get_verifies_the_blob_sha():
    data = b"hello\n"
    g = w.GhContents("o/r", run=lambda a, s=None: (0, _api_file(data), ""))
    assert g.get("p") == (data, v1.blob_sha(data))
    bad = w.GhContents("o/r", run=lambda a, s=None: (0, _api_file(data, sha="0" * 40), ""))
    with pytest.raises(w.TransportError):
        bad.get("p")


def test_gh_adapter_missing_path_reads_as_none_and_other_errors_raise():
    assert w.GhContents("o/r", run=lambda a, s=None: (1, b"", "gh: Not Found (HTTP 404)")).get("p") == (None, None)
    with pytest.raises(w.TransportError):
        w.GhContents("o/r", run=lambda a, s=None: (1, b"", "gh: HTTP 401 Bad credentials")).get("p")


def test_gh_adapter_large_file_falls_back_to_the_blobs_api():
    data = b"x" * 5000
    calls = []

    def run(args, stdin=None):
        calls.append(args[1])
        if "/contents/" in args[1]:
            return 0, json.dumps({"sha": v1.blob_sha(data), "size": len(data), "encoding": "none", "content": ""}).encode(), ""
        return 0, json.dumps({"content": base64.b64encode(data).decode()}).encode(), ""

    assert w.GhContents("o/r", run=run).get("big") == (data, v1.blob_sha(data)) and any("/git/blobs/" in c for c in calls)


@pytest.mark.parametrize("err", ["gh: is at abc but expected def (HTTP 409)", "gh: sha wasn't supplied (HTTP 422)"])
def test_gh_adapter_put_409_and_422_are_conflicts_everything_else_is_an_error(err):
    with pytest.raises(v1.Conflict):
        w.GhContents("o/r", run=lambda a, s=None: (1, b"", err)).put("p", b"x", "sha")
    with pytest.raises(w.TransportError):
        w.GhContents("o/r", run=lambda a, s=None: (1, b"", "gh: HTTP 403 forbidden")).put("p", b"x", "sha")


def test_gh_adapter_put_sends_the_sha_and_returns_the_new_blob_sha():
    seen = {}

    def run(args, stdin=None):
        seen["body"] = json.loads(stdin)
        return 0, json.dumps({"content": {"sha": "n" * 40}}).encode(), ""

    assert w.GhContents("o/r", run=run).put("p", b"x", "oldsha") == "n" * 40 and seen["body"]["sha"] == "oldsha" and seen["body"]["branch"] == "main"


# ---------------------------------------------------------------- UNCERTAIN reconcile with a dynamic policy revision
needs_pkg = pytest.mark.skipif(not PKG, reason="set V029_PKG to the extracted pinned package root")


def _db(tmp_path, rid, zsha, rows):
    from skill_collab_watcher.models import JobState
    from skill_collab_watcher.state_store import StateStore
    path = tmp_path / "state.sqlite3"
    s = StateStore(path)
    for rev, state in rows:
        key = f"{rid}|1|{zsha}|{rev}"
        s.create_job(key, rid, "1", zsha, JobState.CLAIMED)
        s.log_event("REVIEW_DISPATCHED", processing_key=key, detail="{}")
        s.update_job_state(key, state)
    s.close()
    return str(path)


def _remote(rid, key, zsha, receipt_key=None):
    return {f"reviews/{rid}/REVIEW_RESULT_1.md": f'---\nreview_id: "{key}"\npackage_sha256: "{zsha}"\n---\nr\n'.encode(),
            f"receipts/{rid}/RECEIPT_1.md": json.dumps({"processing_key": receipt_key or key, "request_id": rid, "package_sha256": zsha, "ok": True}).encode()}.get


@needs_pkg
def test_policy_revision_two_is_found_and_settled_while_v1_hardcoded_key_misses_it(tmp_path):
    from skill_collab_watcher.models import JobState
    z = "d" * 64
    db = _db(tmp_path, "REQ-P", z, [(2, JobState.REVIEW_UNCERTAIN)])
    key = f"REQ-P|1|{z}|2"
    v = w.reconcile_uncertain(db, _remote("REQ-P", key, z), "REQ-P", "1", z)
    assert v["verdict"] == "SETTLED_BY_EVIDENCE" and v["policy_revisions"] == ["2"] and v["model_calls_started_by_reconcile"] == 0
    assert v1.reconcile_uncertain(db, _remote("REQ-P", key, z), "REQ-P", "1", z)["verdict"] == "NO_JOB_HOLD"      # the defect the v2 change fixes


@needs_pkg
def test_receipt_for_another_policy_revision_does_not_settle(tmp_path):
    from skill_collab_watcher.models import JobState
    z = "e" * 64
    db = _db(tmp_path, "REQ-P", z, [(2, JobState.REVIEW_UNCERTAIN)])
    v = w.reconcile_uncertain(db, _remote("REQ-P", f"REQ-P|1|{z}|2", z, receipt_key=f"REQ-P|1|{z}|1"), "REQ-P", "1", z)
    assert v["verdict"] == "EVIDENCE_MISMATCH_HOLD"


@needs_pkg
def test_two_uncertain_policy_revisions_for_one_request_are_ambiguous_and_held(tmp_path):
    from skill_collab_watcher.models import JobState
    z = "f" * 64
    db = _db(tmp_path, "REQ-P", z, [(1, JobState.REVIEW_UNCERTAIN), (2, JobState.REVIEW_UNCERTAIN)])
    v = w.reconcile_uncertain(db, _remote("REQ-P", f"REQ-P|1|{z}|2", z), "REQ-P", "1", z)
    assert v["verdict"] == "AMBIGUOUS_POLICY_REVISION_HOLD" and v["dispatch_events_total"] == 2


@needs_pkg
def test_reconcile_is_read_only_and_completed_jobs_are_not_uncertain(tmp_path):
    from skill_collab_watcher.models import JobState
    z = "a" * 64
    db = _db(tmp_path, "REQ-P", z, [(1, JobState.COMPLETED)])
    before = hashlib.sha256(open(db, "rb").read()).hexdigest()
    v = w.reconcile_uncertain(db, _remote("REQ-P", f"REQ-P|1|{z}|1", z), "REQ-P", "1", z)
    assert v["verdict"] == "NOT_UNCERTAIN" and hashlib.sha256(open(db, "rb").read()).hexdigest() == before
