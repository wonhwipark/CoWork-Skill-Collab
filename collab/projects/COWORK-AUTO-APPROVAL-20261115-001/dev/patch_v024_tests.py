"""Rewrite only tests whose expected verdict was the removed day COUNT gate."""
from pathlib import Path

def one(path:Path,before:str,after:str):
    s=path.read_text(encoding="utf8")
    if s.count(before)!=1:raise RuntimeError(f"TEST_ANCHOR {path} count={s.count(before)} snippet={before[:85]!r}")
    path.write_text(s.replace(before,after),encoding="utf8",newline="\n")

def patch_tests(root:Path):
    p=root/"tests/test_auto_approval.py"
    one(p,"d.max_day_calls == 2 and d.max_day_cents","d.max_day_calls == 0 and d.max_day_cents")
    one(p,'    ({"max_day_calls": 3}, {}),\n',"")
    one(p,'''def test_the_day_call_limit_allows_two_and_refuses_the_third(auto):
    for rid in ("REQ-A", "REQ-B", "REQ-C"):
        make_request(auto.env.http, rid)
    auto.cycle()
    assert [approval_posted(auto.env, r) for r in ("REQ-A", "REQ-B", "REQ-C")] == [True, True, False]
    assert denied_for(auto.env, "DAY_CALL_LIMIT") and type(auto.signer).calls == 2''',
    '''def test_day_count_is_unlimited_until_cost_budget_is_consumed(auto):
    for rid in ("REQ-A", "REQ-B", "REQ-C", "REQ-D"):
        make_request(auto.env.http, rid)
    auto.cycle()
    assert [approval_posted(auto.env, r) for r in ("REQ-A", "REQ-B", "REQ-C", "REQ-D")] == [True, True, True, False]
    assert denied_for(auto.env, "DAY_COST_LIMIT") and type(auto.signer).calls == 3''')
    one(p,'''    assert not approval_posted(auto.env) and has(auto.env, "AUTO_NOT_ELIGIBLE", "DAY_CALL_LIMIT")''',
        '''    assert approval_posted(auto.env)  # dispatch count with no recorded cost is not a cost gate''')
    one(p,'''    assert s.auto_claim("R", "3", "a" * 64, 100, cj, t + 3, **kw) == "DAY_CALL_LIMIT"
    assert s.auto_claim("R", "3", "a" * 64, 100, cj, _kst_day(1), **kw) == "CLAIMED"     # the next KST day has room''',
        '''    assert s.auto_claim("R", "3", "a" * 64, 100, cj, t + 3, **kw) == "CLAIMED"
    assert s.auto_claim("R", "3", "a" * 64, 100, cj, _kst_day(1), **kw) == "EXISTS"
    assert s.auto_claim("R", "4", "a" * 64, 100, cj, _kst_day(1), **kw) == "CLAIMED"''')
    p=root/"tests/test_auto_policy_gpt_proto.py"
    one(p,'''    def test_policy_limit_expansion(self):
        self.assertEqual(self.verdict(d=replace(self.d, max_day_calls=3))[1], "UNSUPPORTED_DELEGATION_LIMIT"''',
        '''    def test_legacy_day_call_limit_is_ignored(self):
        self.assertTrue(self.verdict(d=replace(self.d, max_day_calls=3))[0])''')
    one(p,'''    def test_day_call_limit(self):
        self.assertEqual(self.verdict(e=replace(self.e, day_calls_used_or_reserved=2))[1], "DAY_CALL_LIMIT"''',
        '''    def test_call_count_telemetry_does_not_reject_request(self):
        self.assertTrue(self.verdict(e=replace(self.e, day_calls_used_or_reserved=200))[0])''')
    p=root/"tests/test_v022_findings.py"
    one(p,
        'max_day_calls=2, max_day_cents=900, max_month_cents=9000',
        'max_day_calls=2, max_day_cents=200, max_month_cents=9000')
    one(p,
        'assert outcomes.count("CLAIMED") == 2 and outcomes.count("DAY_CALL_LIMIT") == 4',
        'assert outcomes.count("CLAIMED") == 2 and outcomes.count("DAY_COST_LIMIT") == 4')
    one(p,
        'def test_B2_lowering_the_daily_call_limit_while_pending_stops_it(auto, monkeypatch):',
        'def test_B2_lowering_the_daily_cost_budget_while_pending_stops_it(auto, monkeypatch):')
    one(p,
        '_narrow_at(monkeypatch, auto, "before_sign", max_day_calls=1)',
        '_narrow_at(monkeypatch, auto, "before_sign", max_day_usd=1.0)')
    assert not any('"DAY_CALL_LIMIT"' in f.read_text(encoding="utf8") for f in
                   (root/"tests").rglob("*.py"))
