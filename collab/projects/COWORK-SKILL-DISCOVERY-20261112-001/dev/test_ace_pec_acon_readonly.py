import hashlib
import unittest
from ace_pec_acon_readonly import ace_decision_candidate, pec_verify_excerpt, acon_compare_existing_results

class ReadOnlyContractTests(unittest.TestCase):
    def setUp(self):
        self.rows = [dict(work_id="W1", scope="scope", subject="S1", kind="SELECT",
                          authority_verified=True, origin_verified=True,
                          append_index=n, decision_ref=f"D{n}") for n in [1, 2]]
        self.src = "NR|IPC=TX_READY|조건=정상".encode()
        self.excerpt = "TX_READY".encode()
        self.off = self.src.index(self.excerpt)
        self.sha = hashlib.sha256(self.src).hexdigest()
        self.kw = dict(source_bytes=self.src, excerpt_bytes=self.excerpt,
                       source_revision="pinned", expected_revision="pinned",
                       source_sha256=self.sha, byte_offset=self.off,
                       byte_length=len(self.excerpt), access_verified=True)
    def ac(self, rows):
        return ace_decision_candidate(rows,work_id="W1",scope="scope",subject="S1")
    def test_ace_latest(self):
        self.assertEqual(self.ac(self.rows)["decision_ref"],"D2")
        self.assertFalse(self.ac(self.rows)["authorization_applied"])
    def test_ace_scopes(self):
        self.assertEqual(self.ac([dict(self.rows[0],scope="other")])["status"],"HOLD")
    def test_ace_ambiguous(self):
        self.assertEqual(self.ac([self.rows[0],dict(self.rows[1],append_index=1)])["reason"],"AMBIGUOUS_APPEND_ORDER")
    def test_ace_missing_authority(self):
        self.assertEqual(self.ac([self.rows[0],dict(self.rows[1],authority_verified=False)])["status"],"HOLD")
    def test_ace_missing_origin(self):
        self.assertEqual(self.ac([dict(self.rows[0],origin_verified=False)])["status"],"HOLD")
    def test_ace_revocation(self):
        self.assertEqual(self.ac([self.rows[0],dict(self.rows[1],kind="REVOKE")])["status"],"REVOKED_CANDIDATE")
    def test_ace_invalid_index(self):
        self.assertEqual(self.ac([dict(self.rows[0],append_index=True)])["status"],"HOLD")
    def test_pec_match(self):
        self.assertEqual(pec_verify_excerpt(**self.kw)["status"],"PASS")
    def test_pec_changed_byte(self):
        self.assertEqual(pec_verify_excerpt(**dict(self.kw,excerpt_bytes=b"TX_XEADY"))["status"],"FAIL")
    def test_pec_missing_range(self):
        self.assertEqual(pec_verify_excerpt(**dict(self.kw,byte_offset=None))["status"],"HOLD")
    def test_pec_stale(self):
        self.assertEqual(pec_verify_excerpt(**dict(self.kw,expected_revision="other"))["status"],"HOLD")
    def test_pec_wrong_digest(self):
        self.assertEqual(pec_verify_excerpt(**dict(self.kw,source_sha256="0"*64))["status"],"FAIL")
    def test_pec_unauthorized(self):
        self.assertEqual(pec_verify_excerpt(**dict(self.kw,access_verified=False))["status"],"HOLD")
    def test_pec_no_raw(self):
        self.assertEqual(pec_verify_excerpt(**dict(self.kw,source_bytes=None))["status"],"HOLD")
    def make_runs(self, passed=True, ids=("E1",)):
        return [dict(model_config="model-pinned",source_revision="commit-1",passed=passed,retained_evidence_ids=list(ids)) for _ in range(3)]
    def compare(self, baseline, compressed):
        return acon_compare_existing_results(baseline=baseline,compressed=compressed,pinned_model_config="model-pinned",pinned_source_revision="commit-1",evidence_ids=["E1"])
    def test_acon_valid(self):
        r=self.compare(self.make_runs(),self.make_runs(False,())); self.assertEqual(r["status"],"REVIEW_NEEDED");self.assertFalse(r["causality_proven"])
    def test_acon_repetitions(self):
        self.assertEqual(self.compare(self.make_runs()[:2],self.make_runs())["status"],"NOT_RUN")
    def test_acon_model_variance(self):
        r=self.make_runs();r[0]["model_config"]="different";self.assertEqual(self.compare(r,self.make_runs())["status"],"HOLD")
    def test_acon_revision(self):
        r=self.make_runs();r[0]["source_revision"]="stale";self.assertEqual(self.compare(r,self.make_runs())["status"],"HOLD")
    def test_acon_input_unchanged(self):
        b=self.make_runs();c=self.make_runs();before=(repr(b),repr(c));self.compare(b,c);self.assertEqual(before,(repr(b),repr(c)))

if __name__ == "__main__": unittest.main()
