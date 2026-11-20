"""Tests for work_writer.py. Mock contents API, mock skill repo, throw-away watcher DB made with the pinned package's StateStore.
No GitHub, no model, no operating state. Run with the package root on sys.path (PKG env var) for the StateStore based tests."""
import hashlib
import json
import os
import sys
import threading

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import work_writer as w  # noqa: E402

PKG = os.environ.get("V029_PKG")
if PKG:
    sys.path.insert(0, PKG)

HEADER = "# W — CURRENT\n"


def entry(n):
    return f"\n## window {n}\n- result {n}\n\n---\n"


# ------------------------------------------------------------------ CAS
def test_cas_creates_then_updates_and_reads_back():
    c = w.MockContents()
    r = w.cas_update(c, "CURRENT.md", w.current_merge(HEADER, "window 1", entry(1)))
    assert r.attempts == 1 and r.conflicts == 0 and r.changed
    r2 = w.cas_update(c, "CURRENT.md", w.current_merge(HEADER, "window 2", entry(2)))
    text = c.files["CURRENT.md"].decode()
    assert text.index("window 2") < text.index("window 1") and text.startswith(HEADER)


def test_cas_is_idempotent_no_duplicate_when_repeated():
    c = w.MockContents()
    m = w.current_merge(HEADER, "window 1", entry(1))
    w.cas_update(c, "CURRENT.md", m)
    puts = c.puts
    r = w.cas_update(c, "CURRENT.md", m)
    assert not r.changed and c.puts == puts and c.files["CURRENT.md"].decode().count("window 1") == 1


def test_four_stale_conflicts_recover_without_loss_or_duplicates():
    c = w.MockContents()
    w.cas_update(c, "CURRENT.md", w.current_merge(HEADER, "seed", "\n## seed\n"))
    stale = c.get("CURRENT.md")
    results = []

    class StaleOnce:
        def __init__(self):
            self.first = True

        def get(self, p):
            if self.first:
                self.first = False
                return stale
            return c.get(p)

        def put(self, *a):
            return c.put(*a)

    for n in range(1, 6):
        results.append(w.cas_update(StaleOnce(), "CURRENT.md", w.current_merge(HEADER, f"window {n}", entry(n))))
    assert [r.conflicts for r in results] == [0, 1, 1, 1, 1] and sum(r.conflicts for r in results) == 4
    text = c.files["CURRENT.md"].decode()
    assert all(text.count(f"window {n}") == 1 for n in range(1, 6)) and "seed" in text


def test_tracker_merge_keeps_other_works_and_updates_only_own_fields():
    c = w.MockContents()
    for n in range(1, 6):
        w.cas_update(c, "TRACKER.json", w.tracker_merge(f"W{n}", {"phase": "REVIEW", "next_action": f"n{n}"}))
    w.cas_update(c, "TRACKER.json", w.tracker_merge("W3", {"phase": "COMPLETE"}))
    works = {x["work_id"]: x for x in json.loads(c.files["TRACKER.json"])["works"]}
    assert len(works) == 5 and works["W3"]["phase"] == "COMPLETE" and works["W3"]["next_action"] == "n3"
    assert all(works[f"W{n}"]["phase"] == "REVIEW" for n in (1, 2, 4, 5))


def test_cas_exhaustion_is_reported_not_silently_overwritten():
    class Always:
        def get(self, p):
            return b"x", "s"

        def put(self, *a):
            raise w.Conflict("p")

    with pytest.raises(w.CasExhausted):
        w.cas_update(Always(), "p", lambda old: b"y", max_retries=3)


def test_threaded_contention_never_loses_an_entry():
    c = w.MockContents()
    errors = []

    def worker(n):
        try:
            w.cas_update(c, "CURRENT.md", w.current_merge(HEADER, f"window {n}", entry(n)), max_retries=8, backoff=0.002)
        except Exception as exc:  # noqa: BLE001
            errors.append(repr(exc))

    ts = [threading.Thread(target=worker, args=(n,)) for n in range(1, 6)]
    [t.start() for t in ts]
    [t.join() for t in ts]
    text = c.files["CURRENT.md"].decode()
    assert not errors and all(text.count(f"window {n}") == 1 for n in range(1, 6))


# ------------------------------------------------------------------ merge3 / rebase
BASE = "a\nb\nc\nd\ne\nf\n"


def test_merge3_non_overlapping_changes_combine():
    merged, conflict = w.merge3(BASE, "a\nB\nc\nd\ne\nf\n", "a\nb\nc\nd\nE\nf\n")
    assert not conflict and merged == "a\nB\nc\nd\nE\nf\n"


def test_merge3_same_line_is_a_conflict_and_never_overwrites():
    merged, conflict = w.merge3(BASE, "a\nHEAD\nc\nd\ne\nf\n", "a\nMINE\nc\nd\ne\nf\n")
    assert conflict and merged is None


def test_merge3_identical_change_is_not_a_conflict():
    merged, conflict = w.merge3(BASE, "a\nB\nc\nd\ne\nf\n", "a\nB\nc\nd\nE\nf\n")
    assert not conflict
    merged2, conflict2 = w.merge3(BASE, "a\nB\nc\nd\ne\nf\n", "a\nB\nc\nd\ne\nf\n")
    assert not conflict2 and merged2 == "a\nB\nc\nd\ne\nf\n"


def test_merge3_adjacent_insert_at_a_replaced_edge_is_a_conflict():
    merged, conflict = w.merge3(BASE, "a\nb\nX\nc\nd\ne\nf\n", "a\nb\nY\nc\nd\ne\nf\n")
    assert conflict


def _regression(files):
    return ("MARK-1" in files["f1.py"] or True), ""


def test_three_modifications_from_one_base_rebase_in_order_without_loss():
    repo = w.SkillRepo({"f1.py": BASE, "f2.py": BASE})
    pins = {}
    mods = [w.Modification("M1", 1, {"f1.py": "a\nB1\nc\nd\ne\nf\n"}),
            w.Modification("M2", 1, {"f1.py": "a\nb\nc\nd\nE2\nf\n"}),
            w.Modification("M3", 1, {"f2.py": "a\nb\nC3\nd\ne\nf\n"})]

    def reg(files):
        return True, ""

    out = [w.apply_modification(repo, m, reg, pins) for m in mods]
    # M2 touches f1.py, which M1 already changed -> REBASED. M3 touches only f2.py, untouched since the base -> APPLIED.
    assert [o["status"] for o in out] == ["APPLIED", "REBASED", "APPLIED"]
    assert repo.files["f1.py"] == "a\nB1\nc\nd\nE2\nf\n" and repo.files["f2.py"] == "a\nb\nC3\nd\ne\nf\n"
    assert w.pins_unchanged(pins) and len({p.sha for p in pins.values()}) == 3


def test_semantic_conflict_is_needs_decision_and_writes_nothing():
    repo = w.SkillRepo({"f1.py": BASE})
    pins = {}
    ok = w.apply_modification(repo, w.Modification("M1", 1, {"f1.py": "a\nONE\nc\nd\ne\nf\n"}), lambda f: (True, ""), pins)
    rev_before, files_before = repo.rev, dict(repo.files)
    bad = w.apply_modification(repo, w.Modification("M2", 1, {"f1.py": "a\nTWO\nc\nd\ne\nf\n"}), lambda f: (True, ""), pins)
    assert ok["status"] == "APPLIED" and bad["status"] == "NEEDS_DECISION" and not bad["written"]
    assert repo.rev == rev_before and repo.files == files_before and "M2" not in pins


def test_failing_regression_blocks_commit_and_pin():
    repo = w.SkillRepo({"f1.py": BASE})
    pins = {}
    r = w.apply_modification(repo, w.Modification("M1", 1, {"f1.py": "a\nX\nc\nd\ne\nf\n"}), lambda f: (False, "boom"), pins)
    assert r["status"] == "REGRESSION_FAILED" and repo.rev == 1 and not pins


# ------------------------------------------------------------------ UNCERTAIN reconcile (needs the pinned package for the real schema)
needs_pkg = pytest.mark.skipif(not PKG, reason="set V029_PKG to the extracted pinned package root")


def _db(tmp_path, rid, zip_sha, state):
    from skill_collab_watcher.models import JobState
    from skill_collab_watcher.state_store import StateStore
    path = tmp_path / "state.sqlite3"
    s = StateStore(path)
    key = f"{rid}|1|{zip_sha}|1"
    s.create_job(key, rid, "1", zip_sha, JobState.CLAIMED)
    s.log_event("REVIEW_DISPATCHED", processing_key=key, detail="{}")
    s.update_job_state(key, state)
    s.close()
    return str(path), key


def _remote(rid, key, zip_sha, with_result=True, with_receipt=True, tamper=False):
    files = {}
    if with_result:
        files[f"reviews/{rid}/REVIEW_RESULT_1.md"] = (f'---\nreview_id: "{key}"\npackage_sha256: "{"0"*64 if tamper else zip_sha}"\n---\nresult\n').encode()
    if with_receipt:
        files[f"receipts/{rid}/RECEIPT_1.md"] = json.dumps({"processing_key": key, "request_id": rid, "package_sha256": zip_sha, "ok": True}).encode()
    return files.get


@needs_pkg
def test_uncertain_with_matching_remote_evidence_is_settled_and_db_is_untouched(tmp_path):
    from skill_collab_watcher.models import JobState
    sha = "a" * 64
    db, key = _db(tmp_path, "REQ-U", sha, JobState.REVIEW_UNCERTAIN)
    before = hashlib.sha256(open(db, "rb").read()).hexdigest()
    v = w.reconcile_uncertain(db, _remote("REQ-U", key, sha), "REQ-U", "1", sha)
    assert v["verdict"] == "SETTLED_BY_EVIDENCE" and v["dispatch_events"] == 1 and v["model_calls_started_by_reconcile"] == 0
    assert hashlib.sha256(open(db, "rb").read()).hexdigest() == before


@needs_pkg
@pytest.mark.parametrize("kw,expected", [({"with_receipt": False}, "PARTIAL_EVIDENCE_HOLD"), ({"with_result": False, "with_receipt": False}, "UNCERTAIN_HOLD"),
                                         ({"tamper": True}, "EVIDENCE_MISMATCH_HOLD")])
def test_uncertain_without_exact_evidence_stays_on_hold(tmp_path, kw, expected):
    from skill_collab_watcher.models import JobState
    sha = "b" * 64
    db, key = _db(tmp_path, "REQ-U", sha, JobState.REVIEW_UNCERTAIN)
    v = w.reconcile_uncertain(db, _remote("REQ-U", key, sha, **kw), "REQ-U", "1", sha)
    assert v["verdict"] == expected


@needs_pkg
def test_completed_job_is_not_treated_as_uncertain(tmp_path):
    from skill_collab_watcher.models import JobState
    sha = "c" * 64
    db, key = _db(tmp_path, "REQ-U", sha, JobState.COMPLETED)
    assert w.reconcile_uncertain(db, _remote("REQ-U", key, sha), "REQ-U", "1", sha)["verdict"] == "NOT_UNCERTAIN"


def test_only_later_windows_of_the_same_skill_wait_behind_an_unsettled_uncertain():
    wins = [{"id": "D1", "skill": "design"}, {"id": "D2", "skill": "design2"}, {"id": "S1", "skill": "s"}, {"id": "S2", "skill": "s"}, {"id": "S3", "skill": "s"}]
    plan = w.plan_after_uncertain(wins, {"S1": "UNCERTAIN_HOLD"})
    assert plan == {"D1": "PROCEED", "D2": "PROCEED", "S1": "UNCERTAIN_HOLD", "S2": "WAIT_DEPENDENCY", "S3": "WAIT_DEPENDENCY"}
    assert set(w.plan_after_uncertain(wins, {"S1": "SETTLED_BY_EVIDENCE"}).values()) == {"PROCEED"}
