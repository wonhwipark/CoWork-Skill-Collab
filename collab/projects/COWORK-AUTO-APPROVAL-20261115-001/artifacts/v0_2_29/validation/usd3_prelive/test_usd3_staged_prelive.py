"""STAGED USD3 pre-live tests. Copied into a temp extraction of the pinned v0.2.29 ZIP (tests/) and run there. Synthetic requests, throw-away Ed25519 key,
fake GitHub, no model, no operating state. Registry cost and delegation cap are staged TOGETHER (STATIC = 3.0, max_request_usd = 3.0)."""
import json
import os
import time

import pytest

from auto_helpers import auto, events, has, iso, make_request, remote, write_delegation  # noqa: F401
from bundle import make_transport
from skill_collab_watcher.auto_approval import AutoApprover

OUT = os.environ.get("STAGED_RESULTS")


def note(case, **kw):
    if OUT:
        with open(OUT, "a", encoding="utf-8") as fh:
            fh.write(json.dumps({"case": case, **kw}, ensure_ascii=False) + "\n")


def process(a, info, approver=None):
    t = make_transport(a.env.http)
    t.ensure_auth()
    return (approver or a.approver).process(t, a.env.store, a.policy, "/SKILL-COLLAB", info.rid, info.request.decode("utf-8"), info.request).status


def stage_usd3(a, **over):
    a.policy.run_budgets_usd["POLICY-STATIC-V1"] = 3.0
    return write_delegation(a.delegation, max_request_usd=3.0, **over)


def seen(a, rid, enabled=True):
    a.env.store.ensure_auto_tables()
    a.env.store.auto_note_seen(rid, "1", enabled, int(time.time()))


def put_count(a):
    return len([c for c in a.env.http.calls if c[0] == "PUT"])


def test_aligned_registry_and_cap_admit_a_new_request_at_usd3(auto):
    stage_usd3(auto)
    info = make_request(auto.env.http, "NEW-1")
    assert process(auto, info) == "READY_POSTED"
    claim = auto.env.store.auto_get_claim("NEW-1", "1")
    assert claim["stage"] == "READY_POSTED" and claim["reserved_cents"] == 300 and auto.signer.calls == 1
    note("aligned_new_request", status="READY_POSTED", reserved_cents=claim["reserved_cents"], signer_calls=auto.signer.calls)


def test_registry_raised_but_cap_not_raised_excludes_for_good_and_stays_excluded_after_the_cap_follows(auto):
    auto.policy.run_budgets_usd["POLICY-STATIC-V1"] = 3.0                      # registry first, cap still 1.0: the operational footgun
    info = make_request(auto.env.http, "MISMATCH-1")
    first = process(auto, info)
    claim = auto.env.store.auto_get_claim("MISMATCH-1", "1")
    write_delegation(auto.delegation, max_request_usd=3.0)                     # cap follows later, enabled_at untouched
    second = process(auto, info)
    assert first == "PER_REQUEST_COST" and claim["stage"] == "POLICY_STOPPED" and second == "POLICY_STOPPED"
    assert remote(auto.env, "requests/MISMATCH-1/READY.md") is None and auto.signer.calls == 0
    note("registry_before_cap", first=first, second_after_cap_raise=second, signer_calls=auto.signer.calls)


def _legacy_set(a):
    """Old requests as they exist on the live host before a cutover. Class A is seen-while-enabled with no claim and no remote history (what v0.2.25
    leaves behind for a request that only the cap refused). D was completed under the old regime, E is UNCERTAIN, C was first seen while disabled."""
    old = {}
    for rid, kw in (("OLD-A-STATIC-NO-HISTORY", {}), ("OLD-B-DESIGN-NO-HISTORY", {"policy_ref": "POLICY-STATIC-V1-DESIGN"}),
                    ("OLD-C-SEEN-DISABLED", {}), ("OLD-D-COMPLETED", {}), ("OLD-E-UNCERTAIN", {})):
        old[rid] = make_request(a.env.http, rid, **kw)
    seen(a, "OLD-A-STATIC-NO-HISTORY")
    seen(a, "OLD-B-DESIGN-NO-HISTORY")
    seen(a, "OLD-C-SEEN-DISABLED", enabled=False)
    assert process(a, old["OLD-D-COMPLETED"]) == "READY_POSTED"                # under the old regime (registry 1.0, cap 1.0)
    e = old["OLD-E-UNCERTAIN"]
    sha = __import__("hashlib").sha256(e.package).hexdigest()
    a.env.store.auto_claim("OLD-E-UNCERTAIN", "1", sha, 100, "{}", int(time.time()), max_day_calls=0, max_day_cents=0, max_month_cents=0)
    a.env.store.auto_update("OLD-E-UNCERTAIN", "1", int(time.time()), stage="UNCERTAIN", detail="staged")
    return old


def test_cutover_with_a_new_enabled_at_revives_no_old_request(auto):
    old = _legacy_set(auto)
    sig_before, puts_before = auto.signer.calls, put_count(auto)
    time.sleep(2.2)
    stage_usd3(auto, enabled_at=iso(time.time()))                               # cap + registry + a NEW enabled_at, together
    time.sleep(2.2)
    result = {rid: process(auto, info) for rid, info in old.items()}
    for rid in ("OLD-A-STATIC-NO-HISTORY", "OLD-B-DESIGN-NO-HISTORY", "OLD-C-SEEN-DISABLED", "OLD-E-UNCERTAIN"):
        assert result[rid] != "READY_POSTED" and remote(auto.env, f"requests/{rid}/READY.md") is None, (rid, result[rid])
    assert result["OLD-D-COMPLETED"] == "READY_POSTED"                          # idempotent terminal answer, not a new publication
    assert auto.signer.calls == sig_before and put_count(auto) == puts_before and auto.env.runner.calls == 0
    fresh = make_request(auto.env.http, "NEW-AFTER-CUTOVER")
    assert process(auto, fresh) == "READY_POSTED" and auto.signer.calls == sig_before + 1
    note("cutover_with_new_enabled_at", statuses=result, signer_calls_delta_old=0, put_delta_old=0, runner_calls=auto.env.runner.calls,
         new_request_after_cutover="READY_POSTED")


def test_cutover_WITHOUT_a_new_enabled_at_shows_why_the_refresh_is_mandatory(auto):
    old = _legacy_set(auto)
    stage_usd3(auto)                                                            # cap + registry raised, enabled_at left old (default: 60 s in the past)
    result = {rid: process(auto, info) for rid, info in old.items()}
    note("cutover_without_new_enabled_at", statuses=result)
    assert result["OLD-B-DESIGN-NO-HISTORY"] != "READY_POSTED"                  # v0.2.29 never auto-signs the DESIGN tier
    assert result["OLD-C-SEEN-DISABLED"] != "READY_POSTED" and result["OLD-E-UNCERTAIN"] != "READY_POSTED"
    # without the refresh, class A is NOT protected by the timestamp: this documents that the operator step is required, not optional
    assert result["OLD-A-STATIC-NO-HISTORY"] in ("READY_POSTED", "RETROACTIVE_OR_FUTURE_REQUEST")


@pytest.mark.parametrize("name,delegation,request_kw", [
    ("expired_delegation", {"expires_at": iso(time.time() - 5)}, {}),
    ("delegation_for_another_repo", {"repo_id": "999"}, {}),
    ("skill_not_allowed", {"skills": ["another-skill"]}, {}),
    ("project_not_allowed", {"projects": ["another-project"]}, {}),
    ("delegation_disabled", {"enabled": False}, {}),
    ("legacy_design_tier", {}, {"policy_ref": "POLICY-STATIC-V1-DESIGN"}),
    ("legacy_large_tier", {}, {"policy_ref": "POLICY-STATIC-V1-LARGE"}),
    ("numeric_repo_id_in_pin", {}, {"pin_repo_id": 1451933830}),
    ("package_sha_mismatch", {}, {"sha_override": "0" * 64}),
    ("package_size_mismatch", {}, {"size_delta": 1}),
    ("pin_missing", {}, {"pin": False}),
])
def test_fail_closed_after_the_staged_change(auto, name, delegation, request_kw):
    stage_usd3(auto, **delegation)
    info = make_request(auto.env.http, f"NEG-{name}"[:60].replace("_", "-"), **request_kw)
    status = process(auto, info)
    assert status != "READY_POSTED" and auto.signer.calls == 0 and remote(auto.env, f"requests/{info.rid}/READY.md") is None
    note("fail_closed", name=name, status=status, signer_calls=auto.signer.calls)


def test_missing_signer_is_fail_closed(auto):
    stage_usd3(auto)
    ap = AutoApprover(auto.settings, auto.env.store, signer=None, now_fn=lambda: time.time())
    info = make_request(auto.env.http, "NO-SIGNER-1")
    status = process(auto, info, approver=ap)
    assert status != "READY_POSTED" and remote(auto.env, "requests/NO-SIGNER-1/READY.md") is None
    note("missing_signer", status=status)


def test_five_windows_at_the_staged_usd3_policy(auto):
    stage_usd3(auto, projects=[f"SIM-WORK-{i}" for i in range(1, 6)])
    kinds = ("design", "design", "skill", "skill", "skill")
    infos = [make_request(auto.env.http, f"W5-{i}", project=f"SIM-WORK-{i}", body_extra=f"review_kind: {k}") for i, k in enumerate(kinds, 1)]
    got = [process(auto, i) for i in infos]
    assert got == ["READY_POSTED"] * 5 and auto.signer.calls == 5
    puts = put_count(auto)
    again = [process(auto, i) for i in infos]
    assert put_count(auto) == puts and auto.signer.calls == 5 and auto.env.runner.calls == 0
    design_tier = make_request(auto.env.http, "W5-LEGACY-DESIGN", project="SIM-WORK-1", policy_ref="POLICY-STATIC-V1-DESIGN")
    assert process(auto, design_tier) != "READY_POSTED" and auto.signer.calls == 5
    note("five_windows_staged_usd3", first=got, repeat=again, signer_calls=auto.signer.calls, extra_puts_on_repeat=0, legacy_design_status=process(auto, design_tier))
