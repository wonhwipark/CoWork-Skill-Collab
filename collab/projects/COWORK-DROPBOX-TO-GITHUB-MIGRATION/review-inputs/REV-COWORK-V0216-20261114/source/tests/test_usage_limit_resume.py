"""Claude plan usage limit (5-hour window): a review the CLI refused BEFORE any model work is resumed automatically once the
window is back; a review cut off DURING the work is sealed and never re-run. Synthetic CLI output only; no model, no network.
The exact text of a real exhausted-account message was not observed, so the patterns are tested on the known phrasings."""
from __future__ import annotations

import time

import pytest

from bundle import github_policy, key_for, publish_bundle
from skill_collab_watcher.fake_runner import FakeReviewRunner
from skill_collab_watcher.models import JobState, ReviewResult
from skill_collab_watcher.orchestrator import USAGE_HOLD_COUNTER
from skill_collab_watcher.review_runner import detect_usage_limit
from test_phase1_github import has_event, run

NOW = 1_800_000_000


def limited(kind="BEFORE_START", wait=120):
    return ReviewResult(ok=False, output_text="", output_format="json", exit_code=1, model_calls=0, usage=None,
                        error=f"usage_limit {kind}", usage_limit=kind, retry_after_sec=wait)


class Sequence(FakeReviewRunner):
    def __init__(self, results):
        super().__init__()
        self.results = list(results)

    def run(self, *a, **k):
        self.calls += 1
        return self.results.pop(0) if self.results else self.canned_result


def policy(**kw):
    return github_policy(require_approval=False, trust_root=None, signature_backend=None, **kw)


def go(env, **kw):
    return run(env, policy=policy(**kw))


def clear_hold(env):
    env.store.set_counter(USAGE_HOLD_COUNTER, 0)


# --- detection -------------------------------------------------------------------------------------------

def test_epoch_reset_time_is_read_from_the_message():
    kind, wait = detect_usage_limit({"result": f"Claude AI usage limit reached|{NOW + 600}", "is_error": True}, "", "", now=NOW)
    assert (kind, wait) == ("BEFORE_START", 600)


def test_clock_style_reset_time_gives_a_positive_wait_under_a_day():
    kind, wait = detect_usage_limit({"result": "You've hit your limit · resets 3pm"}, "", "", now=NOW)
    assert kind == "BEFORE_START" and 0 < wait <= 86400


def test_a_limit_message_without_a_time_has_no_wait_and_the_default_applies_later():
    assert detect_usage_limit({"result": "5-hour limit reached"}, "", "", now=NOW) == ("BEFORE_START", None)


def test_the_message_may_arrive_on_stderr_or_plain_stdout():
    assert detect_usage_limit({}, "", "Error: usage limit reached", now=NOW)[0] == "BEFORE_START"
    assert detect_usage_limit({}, "weekly limit reached", "", now=NOW)[0] == "BEFORE_START"


@pytest.mark.parametrize("parsed", [
    {"result": "usage limit reached", "total_cost_usd": 0.4},
    {"result": "You've hit your session limit", "usage": {"output_tokens": 120}},
    {"result": "You've hit your session limit", "usage": {"cache_creation_input_tokens": 9000}},
])
def test_a_limit_after_work_was_billed_is_not_before_start(parsed):
    assert detect_usage_limit(parsed, "", "", now=NOW)[0] == "DURING"


def test_a_refused_first_request_counts_as_before_start_even_when_the_cli_reports_one_turn():
    parsed = {"result": "You've hit your session limit · resets 3pm (Asia/Seoul)", "num_turns": 1, "total_cost_usd": 0,
              "usage": {"input_tokens": 0, "output_tokens": 0}}
    assert detect_usage_limit(parsed, "", "", now=NOW, elapsed_sec=4)[0] == "BEFORE_START"


def test_a_process_that_ran_long_had_started_working_so_it_is_during():
    assert detect_usage_limit({"result": "You've hit your session limit"}, "", "", now=NOW, elapsed_sec=600)[0] == "DURING"


@pytest.mark.parametrize("label", ["session limit", "weekly limit", "Opus limit", "Sonnet limit", "Fable 5 limit", "usage credit limit"])
def test_every_limit_label_of_the_installed_cli_is_recognised(label):
    assert detect_usage_limit({"result": f"You've hit your {label} · resets 3pm"}, "", "", now=NOW)[0] == "BEFORE_START"


@pytest.mark.parametrize("text", ["You've hit your org's monthly spend limit · ask your admin to raise it",
                                  "Your usage allocation has been disabled by your admin",
                                  "You've hit your monthly spend limit · contact your admin to increase it"])
def test_limits_that_never_reset_by_themselves_are_not_retried(text):
    assert detect_usage_limit({"result": text}, "", "", now=NOW) == (None, None)


def test_the_cli_time_formats_are_parsed_in_local_time():
    import datetime as dt
    base = dt.datetime(2026, 11, 14, 12, 0, 0)
    now = base.timestamp()
    cases = {"resets 3pm (Asia/Seoul)": 3 * 3600, "resets 3:30pm": 3 * 3600 + 1800, "resets 12pm": 24 * 3600,
             "resets 11am": 23 * 3600, "resets Nov 18, 3pm (Asia/Seoul)": 4 * 86400 + 3 * 3600, "resets Dec 2, 2027, 9am": None}
    for text, expected in cases.items():
        wait = detect_usage_limit({"result": "You've hit your weekly limit · " + text}, "", "", now=now)[1]
        if expected is None:
            assert wait is not None and wait > 365 * 86400
        else:
            assert wait == expected, (text, wait)


@pytest.mark.parametrize("text", ["context window exceeded", "network error", "max budget exceeded", "permission denied", ""])
def test_other_failures_are_not_usage_limits(text):
    assert detect_usage_limit({"result": text, "is_error": True}, text, text, now=NOW) == (None, None)


# --- orchestrator behaviour --------------------------------------------------------------------------------

def test_a_refused_start_is_held_then_resumed_without_losing_or_duplicating_the_review(github_env):
    github_env.runner = Sequence([limited(wait=120)])
    pkg = publish_bundle(github_env.http)
    go(github_env)
    key = key_for(pkg)
    assert github_env.runner.calls == 1
    assert github_env.store.get_job(key).state == JobState.VALIDATED
    assert has_event(github_env.store, "USAGE_LIMIT_DEFERRED")
    hold = github_env.store.get_counter(USAGE_HOLD_COUNTER)
    assert time.time() < hold <= time.time() + 200
    for _ in range(3):                                   # still inside the window: no new call
        go(github_env)
    assert github_env.runner.calls == 1
    assert has_event(github_env.store, "USAGE_LIMIT_WAITING")
    clear_hold(github_env)                               # the window is back
    go(github_env)
    assert github_env.runner.calls == 2
    assert github_env.store.get_job(key).state == JobState.COMPLETED
    go(github_env)
    assert github_env.runner.calls == 2                  # finished: never again


def test_the_hold_applies_to_every_request_because_the_limit_is_account_wide(github_env):
    github_env.runner = Sequence([limited(wait=600)])
    publish_bundle(github_env.http, request_id="REQ-1")
    publish_bundle(github_env.http, request_id="REQ-2")
    go(github_env)
    assert github_env.runner.calls == 1                  # REQ-2 was not even tried in the same cycle's hold
    go(github_env)
    assert github_env.runner.calls == 1


def test_a_limit_during_the_review_is_sealed_uncertain_and_never_retried(github_env):
    github_env.runner = Sequence([limited("DURING")])
    pkg = publish_bundle(github_env.http)
    go(github_env)
    key = key_for(pkg)
    assert github_env.store.get_job(key).state == JobState.REVIEW_UNCERTAIN
    clear_hold(github_env)
    for _ in range(3):
        go(github_env)
    assert github_env.runner.calls == 1


def test_waiting_is_capped_per_job(github_env):
    github_env.runner = Sequence([limited(wait=60)] * 5)
    pkg = publish_bundle(github_env.http)
    for _ in range(5):
        go(github_env, usage_limit_max_deferrals=2)
        clear_hold(github_env)
    assert github_env.runner.calls == 3                  # two deferrals, the third refusal ends the job
    assert github_env.store.get_job(key_for(pkg)).state == JobState.FAILED


def test_a_weekly_limit_is_probed_at_the_cap_without_using_up_the_deferral_budget(github_env):
    github_env.runner = Sequence([limited(wait=5 * 86400)] * 6)
    pkg = publish_bundle(github_env.http)
    for _ in range(5):
        go(github_env, usage_limit_max_wait_sec=3600, usage_limit_max_deferrals=2)
        clear_hold(github_env)
    assert github_env.store.get_job(key_for(pkg)).state == JobState.VALIDATED     # still waiting, not FAILED
    assert github_env.runner.calls == 5


def test_while_held_the_package_is_not_downloaded_again(github_env):
    github_env.runner = Sequence([limited(wait=600)])
    publish_bundle(github_env.http)
    go(github_env)
    before = len([c for c in github_env.http.calls if "packages" in c[1]])
    for _ in range(4):
        go(github_env)
    after = len([c for c in github_env.http.calls if "packages" in c[1]])
    assert after == before


def test_the_wait_is_bounded_even_if_the_reset_time_is_far_away(github_env):
    github_env.runner = Sequence([limited(wait=10 * 86400)])
    publish_bundle(github_env.http)
    go(github_env, usage_limit_max_wait_sec=3600)
    assert github_env.store.get_counter(USAGE_HOLD_COUNTER) <= time.time() + 3601


def test_without_a_limit_nothing_changes(github_env):
    pkg = publish_bundle(github_env.http)
    go(github_env)
    assert github_env.runner.calls == 1 and github_env.store.get_job(key_for(pkg)).state == JobState.COMPLETED
    assert github_env.store.get_counter(USAGE_HOLD_COUNTER) == 0


def test_a_deferred_review_is_announced_once(tmp_path):
    from skill_collab_watcher.notify_events import NotifyState, run_once
    from skill_collab_watcher.state_store import StateStore
    s = StateStore(tmp_path / "s.sqlite3")
    st, sent = NotifyState(), []
    st.bootstrap(s.conn, "github", 1)
    for _ in range(3):
        s.log_event("USAGE_LIMIT_DEFERRED", processing_key="REQ-1|1|abc|1", detail="deferral 1")
        run_once(s.conn, st, provider="github", repo="o/r", send=sent.append, epoch=1)
    assert len(sent) == 1 and "자동으로 이어서" in sent[0]
    s.close()


def test_a_month_day_that_already_passed_this_year_means_next_year():
    import datetime as dt
    now = dt.datetime(2026, 11, 14, 12, 0, 0).timestamp()
    wait = detect_usage_limit({"result": "You've hit your weekly limit \u00b7 resets Nov 10, 3pm"}, "", "", now=now)[1]
    assert wait is not None and wait > 300 * 86400
