"""Actual extracted package tests for only PEC Code Analyzer and ACE Workflow."""
from __future__ import annotations
import hashlib
import importlib
import unittest
from unittest import mock


class PECTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = importlib.import_module("ca_core.pec_hop_excerpt_readonly")
        cls.reuse = importlib.import_module("ca_core.reuse_validator")

    def setUp(self):
        self.source = "SYNTHETIC_NR|IPC=TX_READY|상태=OK".encode("utf-8")
        self.excerpt = b"TX_READY"
        self.ok = dict(source_bytes=self.source, excerpt_bytes=self.excerpt,
                       source_revision="PIN-R1", expected_revision="PIN-R1",
                       source_sha256=hashlib.sha256(self.source).hexdigest(),
                       byte_offset=self.source.index(self.excerpt),
                       byte_length=len(self.excerpt), source_access_verified=True)

    def test_pec_correct_raw_excerpt(self):
        self.assertEqual(self.mod.verify_excerpt(**self.ok)["status"], "PASS")

    def test_pec_one_byte_tamper(self):
        self.assertEqual(self.mod.verify_excerpt(**dict(self.ok, excerpt_bytes=b"TX_XEADY"))["status"], "FAIL")

    def test_pec_stale_source(self):
        self.assertEqual(self.mod.verify_excerpt(**dict(self.ok, expected_revision="PIN-R0"))["status"], "HOLD")

    def test_pec_absent_offset(self):
        self.assertEqual(self.mod.verify_excerpt(**dict(self.ok, byte_offset=None))["status"], "HOLD")

    def test_pec_out_of_range(self):
        self.assertEqual(self.mod.verify_excerpt(**dict(self.ok, byte_offset=100000))["status"], "HOLD")

    def test_pec_unverified_access(self):
        self.assertEqual(self.mod.verify_excerpt(**dict(self.ok, source_access_verified=False))["status"], "HOLD")

    def test_pec_wrong_source_sha(self):
        self.assertEqual(self.mod.verify_excerpt(**dict(self.ok, source_sha256="0" * 64))["status"], "FAIL")

    def test_pec_empty_batch_holds(self):
        self.assertEqual(self.mod.verify_batch([])["status"], "HOLD")

    def test_pec_batch_mixed_fails(self):
        failed = dict(self.ok, excerpt_bytes=b"CHANGED")
        out = self.mod.verify_batch([self.ok, failed])
        self.assertEqual(out["status"], "FAIL")
        self.assertNotIn("source_bytes", str(out))
        self.assertNotIn("TX_READY", str(out))

    def test_existing_reuse_response_unchanged_without_opt_in(self):
        out = self.reuse.validate({}, {"file_groups":[]})
        self.assertEqual(out["schema"], "code-analyzer/reuse-result/v1")
        self.assertNotIn("pec_excerpt_integrity", out)

    def test_existing_reuse_optional_connection(self):
        out = self.reuse.validate({}, {"file_groups":[]}, pec_claims=[self.ok])
        self.assertEqual(out["pec_excerpt_integrity"]["status"], "PASS")
        self.assertNotIn("pec_excerpt_integrity", self.reuse.validate({}, {"file_groups":[]}))
        self.assertEqual(out["reuse_status"], "REUSE_UNKNOWN")

    def test_invalid_batch_no_exception(self):
        self.assertEqual(self.reuse.validate({}, {"file_groups":[]}, pec_claims={"bad":True})["pec_excerpt_integrity"]["status"], "HOLD")


class ACETests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = importlib.import_module("l1_fix_workflow.ace_resume_readonly")
        cls.inspector = importlib.import_module("l1_fix_workflow.work_inspection")

    def setUp(self):
        self.events = [
            dict(type="DECISION", work_id="SYNTH-1", scope="TX", subject="RACH",
                 ref="EV-1", append_index=5, origin_verified=True, authority_verified=True),
            dict(type="CORRECTION", work_id="SYNTH-1", scope="TX", subject="RACH",
                 ref="EV-2", append_index=8, origin_verified=True, authority_verified=True),
        ]
        self.kw = dict(work_id="SYNTH-1",scope="TX",subject="RACH")

    def test_ace_latest_authoritative_original(self):
        out=self.mod.select_latest_candidate(self.events,**self.kw)
        self.assertEqual(out["decision_ref"],"EV-2")
        self.assertFalse(out["approval_applied"])

    def test_ace_unrelated_scope(self):
        self.assertEqual(self.mod.select_latest_candidate(self.events,**dict(self.kw,scope="OTHER"))["status"],"HOLD")

    def test_ace_missing_authority(self):
        a=[dict(self.events[1],authority_verified=False)]
        self.assertEqual(self.mod.select_latest_candidate(a,**self.kw)["status"],"HOLD")

    def test_ace_missing_origin(self):
        a=[dict(self.events[1],origin_verified=False)]
        self.assertEqual(self.mod.select_latest_candidate(a,**self.kw)["status"],"HOLD")

    def test_ace_missing_order(self):
        a=[dict(self.events[1],append_index=None)]
        self.assertEqual(self.mod.select_latest_candidate(a,**self.kw)["status"],"HOLD")

    def test_ace_ambiguous_order(self):
        a=[self.events[0],dict(self.events[1],append_index=5)]
        self.assertEqual(self.mod.select_latest_candidate(a,**self.kw)["reason"],"AMBIGUOUS_APPEND_ORDER")

    def test_ace_revocation(self):
        a=[self.events[0],dict(self.events[1],type="REVOKE")]
        self.assertEqual(self.mod.select_latest_candidate(a,**self.kw)["status"],"REVOKED_CANDIDATE")

    def test_ace_summary_only_does_not_approve(self):
        a=[dict(type="DECISION",work_id="SYNTH-1",scope="TX",subject="RACH",
                ref=None,date=None,text="Synthetic decision")]
        self.assertEqual(self.mod.select_latest_candidate(a,**self.kw)["status"],"HOLD")

    def test_ace_no_implicit_work_write(self):
        self.assertEqual(self.mod.select_latest_candidate([],**self.kw)["status"],"HOLD")

    def test_inspector_optional_bridge_no_default_change(self):
        # A small, synthetic Kernel stub; no filesystem, external source or model.
        class Kernel:
            def load_record(self,wid): return {"display_name":"Synthetic","evidence_index":[]}
            def status(self,wid): return {}
            def work_resume(self,wid,mode,**kw):
                if mode=="brief": return {"next_actions":["review existing"]}
                if mode=="diagnostic": return {"context_events":[]}
                return {}
        kernel=Kernel()
        with mock.patch.object(self.inspector,"_resolve",return_value=("SYNTH-1",None)):
            baseline=self.inspector.inspect_work(kernel,{"kind":"READ"})
            scoped=self.inspector.inspect_work(kernel,{"kind":"READ","ace_scope":"TX","ace_subject":"RACH"})
        self.assertNotIn("ace_latest_decision_candidate",baseline)
        self.assertEqual(scoped["ace_latest_decision_candidate"]["status"],"HOLD")
        self.assertTrue(scoped["read_only"])


def run_package_contract(name, root):
    cls = PECTests if name == "code-analyzer" else ACETests
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(cls)
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    if not result.wasSuccessful() or result.testsRun != (12 if name == "code-analyzer" else 10):
        raise RuntimeError("ACTUAL_PACKAGE_TWO_SKILL_REGRESSION_FAILED:" + name)
    return {"status":"PASS","count":result.testsRun,"failures":len(result.failures),"errors":len(result.errors)}
