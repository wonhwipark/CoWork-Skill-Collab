"""Carry forward all v0.2.24 tests; rewrite only aggregate-budget assumptions."""
from pathlib import Path

def one(p: Path, before: str, after: str) -> None:
    s=p.read_text(encoding="utf-8")
    if s.count(before)!=1:
        raise RuntimeError(f"TEST_ANCHOR {p} count={s.count(before)} for {before[:120]!r}")
    p.write_text(s.replace(before,after),encoding="utf-8",newline="\n")

def patch_tests(root: Path) -> None:
    p=root/"tests"/"test_auto_approval.py"
    one(p,
      'd.max_request_cents == 100 and d.max_day_calls == 0 and d.max_day_cents == 300 and d.max_month_cents == 1000',
      'd.max_request_cents == 150 and d.max_day_calls == 0 and d.max_day_cents == 0 and d.max_month_cents == 0')
    # The protected limit is now per request, not aggregate.
    one(p, '({"max_request_usd": 1.5}, {}),', '({"max_request_usd": 0.0}, {}),')
    one(p, '({"max_day_usd": 4.0}, {}),', '')
    one(p, '({"max_month_usd": 11.0}, {}),', '')
    one(p, '''def test_day_count_is_unlimited_until_cost_budget_is_consumed(auto):
    for rid in ("REQ-A", "REQ-B", "REQ-C", "REQ-D"):
        make_request(auto.env.http, rid)
    auto.cycle()
    assert [approval_posted(auto.env, r) for r in ("REQ-A", "REQ-B", "REQ-C", "REQ-D")] == [True, True, True, False]
    assert denied_for(auto.env, "DAY_COST_LIMIT") and type(auto.signer).calls == 3''',
    '''def test_no_day_count_or_cost_ceiling_is_applied(auto):
    for rid in ("REQ-A", "REQ-B", "REQ-C", "REQ-D"):
        make_request(auto.env.http, rid)
    auto.cycle()
    assert all(approval_posted(auto.env, r) for r in ("REQ-A", "REQ-B", "REQ-C", "REQ-D"))
    assert type(auto.signer).calls == 4''')
    one(p,
      'assert approval_posted(auto.env, "REQ-A") and not approval_posted(auto.env, "REQ-B") and denied_for(auto.env, "DAY_COST_LIMIT")',
      'assert approval_posted(auto.env, "REQ-A") and approval_posted(auto.env, "REQ-B")')
    one(p, 'assert statuses == ["READY_POSTED", "READY_POSTED", "MONTH_COST_LIMIT"]',
      'assert statuses == ["READY_POSTED"] * 3')
    one(p, '    assert denied_for(auto.env, "MONTH_COST_LIMIT")',
      '    assert not denied_for(auto.env, "MONTH_COST_LIMIT")')
    # Add end-to-end tests of real auto-signing decision with trusted local tier.
    with p.open("a",encoding="utf-8") as f:
        f.write('''
def test_configurable_basic_and_design_tiers_are_signed_only_when_locally_allowed(auto):
    write_delegation(auto.delegation, max_request_usd=3.0)
    auto.policy.known_run_policy_refs.append("POLICY-STATIC-V1-DESIGN")
    auto.policy.run_budgets_usd["POLICY-STATIC-V1"] = 1.5
    auto.policy.run_budgets_usd["POLICY-STATIC-V1-DESIGN"] = 3.0
    make_request(auto.env.http, "REQ-A", policy_ref="POLICY-STATIC-V1")
    make_request(auto.env.http, "REQ-B", policy_ref="POLICY-STATIC-V1-DESIGN")
    auto.cycle()
    assert approval_posted(auto.env, "REQ-A")
    assert approval_posted(auto.env, "REQ-B")
    assert type(auto.signer).calls == 2

def test_design_tier_cannot_escalate_past_protected_delegation(auto):
    write_delegation(auto.delegation, max_request_usd=1.5)
    auto.policy.known_run_policy_refs.append("POLICY-STATIC-V1-DESIGN")
    auto.policy.run_budgets_usd["POLICY-STATIC-V1-DESIGN"] = 3.0
    make_request(auto.env.http, "REQ-A", policy_ref="POLICY-STATIC-V1-DESIGN")
    auto.cycle()
    assert not approval_posted(auto.env, "REQ-A")
    assert type(auto.signer).calls == 0
''')
    # v0.2.24 legacy findings switched to day-cost stops; now that is gone.
    p=root/"tests"/"test_v022_findings.py"
    one(p, 'assert outcomes.count("CLAIMED") == 2 and outcomes.count("DAY_COST_LIMIT") == 4',
        'assert outcomes.count("CLAIMED") == 6 and outcomes.count("DAY_COST_LIMIT") == 0')
    # Additional pure/state functional tests: no model, no remote dispatch.
    (root/"tests"/"test_review_budget_policy_v025.py").write_text('''"""New v0.2.25 per-request budgets and aggregate-free reservations."""
from dataclasses import replace
import json
import time
import pytest
from skill_collab_watcher.auto_policy import Candidate, Delegation, Evidence, assess
from skill_collab_watcher.state_store import StateStore, kst_window_starts
from skill_collab_watcher.config import _parse_run_policy_refs, ConfigError

def scenario():
    now=int(time.time())
    d=Delegation(enabled=True,repo_id="123",branch="main",
        projects=frozenset({"project"}),skills=frozenset({"skill"}),
        expires_at=now+3600,earliest_request_at=now-120,
        max_request_cents=300)
    c=Candidate(request_id="REQ-1",revision=1,project="project",skill="skill",
        repo_id="123",branch="main",created_at=now-5,
        commit_a="a"*40,request_sha256="b"*64,zip_sha256="c"*64,
        policy="POLICY-STATIC-V1",estimated_cents=150,max_calls=1,attempt=1)
    e=Evidence(now=now,pins_verified=True,bytes_and_crc_verified=True,
        signer_and_trust_root_valid=True,prior_state="NEW",
        day_calls_used_or_reserved=999,day_cents_used_or_reserved=900000,
        month_cents_used_or_reserved=9000000,atomic_claim_available=True)
    return d,c,e

def test_configurable_tier_budgets_are_locally_registered():
    tiers={"POLICY-STATIC-V1":{"max_budget_usd":1.5},
           "POLICY-STATIC-V1-DESIGN":{"max_budget_usd":3.0}}
    names,budgets,efforts=_parse_run_policy_refs(tiers)
    assert names==list(tiers) and budgets=={"POLICY-STATIC-V1":1.5,
                                             "POLICY-STATIC-V1-DESIGN":3.0}
    assert efforts=={}
    with pytest.raises(ConfigError):
        _parse_run_policy_refs({"POLICY-STATIC-V1-DESIGN":{"max_budget_usd":float("inf")}})

def test_basic_and_design_allow_unlimited_aggregate_telemetry():
    d,c,e=scenario()
    assert assess(d,c,e)[0]
    assert assess(d,replace(c,policy="POLICY-STATIC-V1-DESIGN",
                            estimated_cents=300),e)[0]
    assert assess(d,replace(c,policy="POLICY-STATIC-V1-DESIGN",
                            estimated_cents=301),e)[1]=="PER_REQUEST_COST"

def test_scope_and_exactly_once_prevent_untrusted_escalation():
    d,c,e=scenario()
    assert assess(d,replace(c,policy="POLICY-STATIC-V1-LARGE"),e)[1]=="REVIEW_POLICY"
    assert assess(d,replace(c,max_calls=2),e)[1]=="REVIEW_POLICY"
    assert assess(d,replace(c,project="other"),e)[1]=="SCOPE"
    assert assess(d,c,replace(e,prior_state="UNCERTAIN"))[1]=="DUPLICATE_OR_UNCERTAIN"

def test_atomic_reservations_exceed_old_limits_but_duplicate_still_blocks(tmp_path):
    s=StateStore(tmp_path/"state.sqlite3")
    s.ensure_auto_tables()
    now=kst_window_starts(int(time.time()))[0]+3600
    kw=dict(max_day_calls=1,max_day_cents=0,max_month_cents=0)
    for i in range(12):
        rid=f"REQ-{i}"
        assert s.auto_claim(rid,"1","a"*64,300,"{}",now,**kw)=="CLAIMED"
    assert s.auto_claim("REQ-1","1","a"*64,300,"{}",now,**kw)=="EXISTS"
    assert s.window_usage(now)["day_cents"]>=3600
    assert s.auto_claim("BAD","1","a"*64,0,"{}",now,**kw)=="INVALID_COST"
    s.close()
''',encoding="utf-8")
