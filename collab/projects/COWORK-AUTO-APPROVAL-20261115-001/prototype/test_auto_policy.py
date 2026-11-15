"""Offline synthetic tests. No GitHub calls, Windows keys or paid models."""
from dataclasses import replace
import unittest
from auto_policy import Delegation, Candidate, Evidence, assess


class AutoPolicyTest(unittest.TestCase):
    def setUp(self):
        self.d = Delegation(True, "1451933830", "main", frozenset({"TEST-WORK"}),
                            frozenset({"test-skill"}), 99999, 1000)
        self.c = Candidate("REQ-TEST-001", 1, "TEST-WORK", "test-skill", "1451933830",
                           "main", 2000, "c"*40, "a"*64, "b"*64,
                           "POLICY-STATIC-V1", 100, 1, 1)
        self.e = Evidence(3000, True, True, True, "NEW", 0, 0, 0, True)

    def verdict(self, d=None, c=None, e=None):
        return assess(d or self.d, c or self.c, e or self.e)

    def test_allowed(self):
        self.assertEqual(self.verdict(), (True, "ALLOW_ATOMIC_CLAIM_THEN_EXISTING_SIGNER_ONLY"))

    def test_disabled(self):
        self.assertEqual(self.verdict(d=replace(self.d, enabled=False))[1], "DISABLED")

    def test_expired(self):
        self.assertEqual(self.verdict(e=replace(self.e, now=99999))[1], "DELEGATION_EXPIRED")

    def test_retroactive(self):
        self.assertEqual(self.verdict(c=replace(self.c, created_at=999))[1], "RETROACTIVE_OR_FUTURE_REQUEST")

    def test_future(self):
        self.assertEqual(self.verdict(c=replace(self.c, created_at=4000))[1], "RETROACTIVE_OR_FUTURE_REQUEST")

    def test_other_repo(self):
        self.assertEqual(self.verdict(c=replace(self.c, repo_id="123"))[1], "REPOSITORY_OR_BRANCH")

    def test_other_branch(self):
        self.assertEqual(self.verdict(c=replace(self.c, branch="feature"))[1], "REPOSITORY_OR_BRANCH")

    def test_other_project(self):
        self.assertEqual(self.verdict(c=replace(self.c, project="OTHER"))[1], "SCOPE")

    def test_no_allowlist(self):
        self.assertEqual(self.verdict(d=replace(self.d, projects=frozenset()))[1], "SCOPE")

    def test_other_skill(self):
        self.assertEqual(self.verdict(c=replace(self.c, skill="other"))[1], "SCOPE")

    def test_policy_escalation(self):
        self.assertEqual(self.verdict(c=replace(self.c, policy="POLICY-STATIC-V1-LARGE"))[1], "REVIEW_POLICY")

    def test_second_attempt(self):
        self.assertEqual(self.verdict(c=replace(self.c, attempt=2))[1], "REVIEW_POLICY")

    def test_second_call(self):
        self.assertEqual(self.verdict(c=replace(self.c, max_calls=2))[1], "REVIEW_POLICY")

    def test_invalid_state(self):
        self.assertEqual(self.verdict(c=replace(self.c, state="DRAFT_EXAMPLE"))[1], "REQUEST_FORMAT")

    def test_pin_tampering(self):
        self.assertEqual(self.verdict(c=replace(self.c, request_sha256="bad"))[1], "INVALID_PIN_FORMAT")

    def test_request_over_budget(self):
        self.assertEqual(self.verdict(c=replace(self.c, estimated_cents=101))[1], "PER_REQUEST_COST")

    def test_policy_limit_expansion(self):
        self.assertEqual(self.verdict(d=replace(self.d, max_day_calls=3))[1], "UNSUPPORTED_DELEGATION_LIMIT")

    def test_completed_duplicate(self):
        self.assertEqual(self.verdict(e=replace(self.e, prior_state="COMPLETED"))[1], "DUPLICATE_OR_UNCERTAIN")

    def test_uncertain_duplicate(self):
        self.assertEqual(self.verdict(e=replace(self.e, prior_state="REVIEW_UNCERTAIN"))[1], "DUPLICATE_OR_UNCERTAIN")

    def test_crc_failure(self):
        self.assertEqual(self.verdict(e=replace(self.e, bytes_and_crc_verified=False))[1], "INPUT_OR_TRUST")

    def test_key_invalid(self):
        self.assertEqual(self.verdict(e=replace(self.e, signer_and_trust_root_valid=False))[1], "INPUT_OR_TRUST")

    def test_no_atomic_db(self):
        self.assertEqual(self.verdict(e=replace(self.e, atomic_claim_available=False))[1], "NO_ATOMIC_CLAIM")

    def test_day_call_limit(self):
        self.assertEqual(self.verdict(e=replace(self.e, day_calls_used_or_reserved=2))[1], "DAY_CALL_LIMIT")

    def test_day_cost_limit(self):
        self.assertEqual(self.verdict(e=replace(self.e, day_cents_used_or_reserved=250))[1], "DAY_COST_LIMIT")

    def test_month_cost_limit(self):
        self.assertEqual(self.verdict(e=replace(self.e, month_cents_used_or_reserved=950))[1], "MONTH_COST_LIMIT")


if __name__ == "__main__":
    unittest.main()
