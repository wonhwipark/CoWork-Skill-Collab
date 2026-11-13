"""The claim of a never-dispatched job is an atomic compare-and-set (found by the entry-point E2E: two concurrent
`scan` processes both started the reviewer)."""
import pytest

from skill_collab_watcher.models import JobState
from skill_collab_watcher.state_store import StateStore


def _job(store, key="REQ-1|1|abc|1", state=JobState.VALIDATED):
    store.create_job(key, "REQ-1", "1", "abc", state)
    return key


def test_only_one_of_two_connections_wins_the_claim(tmp_path):
    a, b = StateStore(tmp_path / "s.sqlite3"), StateStore(tmp_path / "s.sqlite3")
    key = _job(a)
    assert a.try_claim(key) is True
    assert b.try_claim(key) is False
    job = b.get_job(key)
    assert job.state == JobState.CLAIMED and job.attempt_count == 1
    a.close(); b.close()


@pytest.mark.parametrize("state", [JobState.CLAIMED, JobState.REVIEW_RUNNING, JobState.RESULT_SAVED, JobState.UPLOAD_PENDING,
                                   JobState.COMPLETED, JobState.FAILED, JobState.REVIEW_UNCERTAIN, JobState.CONFLICT, JobState.REJECTED])
def test_a_job_that_was_ever_dispatched_or_closed_cannot_be_claimed_again(tmp_path, state):
    s = StateStore(tmp_path / "s.sqlite3")
    key = _job(s, state=state)
    assert s.try_claim(key) is False
    assert s.get_job(key).state == state
    s.close()


@pytest.mark.parametrize("state", [JobState.DISCOVERED, JobState.WAIT_INPUT, JobState.VALIDATED, JobState.AUTH_REQUIRED])
def test_never_dispatched_states_can_be_claimed_once(tmp_path, state):
    s = StateStore(tmp_path / "s.sqlite3")
    key = _job(s, state=state)
    assert s.try_claim(key) is True and s.try_claim(key) is False
    s.close()


def test_a_missing_job_and_a_read_only_store_never_claim(tmp_path):
    rw = StateStore(tmp_path / "s.sqlite3")
    key = _job(rw)
    assert rw.try_claim("NOPE|1|x|1") is False
    ro = StateStore(tmp_path / "s.sqlite3", read_only=True)
    assert ro.try_claim(key) is False
    assert rw.get_job(key).state == JobState.VALIDATED
    rw.close(); ro.close()
