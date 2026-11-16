"""No-network regression tests: one review = one GPT decision, no extra cycle."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import review_completion as rc


def snapshot(*items):
    return {"schema": rc.SCHEMA, "review_chains": list(items)}


def review(rid="REQ-1", stage="GPT_NOT_OBSERVED", receipt=True, gpt=False):
    return {"id": rid, "stage": stage, "flags": {
        "request": True, "ready": True, "review": receipt, "receipt": receipt, "gpt": gpt}}


class ReviewCompletionTests(unittest.TestCase):
    def test_first_complete_receipt_only_once(self):
        old = snapshot(review(stage="REVIEW_NOT_OBSERVED", receipt=False))
        now = snapshot(review())
        self.assertEqual(rc.newly_pending(old, now), ["REQ-1"])
        self.assertEqual(rc.newly_pending(now, now), [])

    def test_result_then_receipt(self):
        old = snapshot(review(stage="RECEIPT_NOT_OBSERVED", receipt=False))
        self.assertEqual(rc.newly_pending(old, snapshot(review())), ["REQ-1"])

    def test_after_gpt_decision_cycle_is_terminal(self):
        old = snapshot(review())
        done = snapshot(review(stage="GPT_RECORDED_UNAUTHENTICATED", gpt=True))
        self.assertEqual(rc.newly_pending(old, done), [])
        self.assertEqual(rc.newly_pending(done, done), [])

    def test_review_and_gpt_record_in_same_commit_does_not_alert(self):
        old = snapshot()
        done = snapshot(review(stage="GPT_RECORDED_UNAUTHENTICATED", gpt=True))
        self.assertEqual(rc.newly_pending(old, done), [])

    def test_only_new_ids_trigger(self):
        old = snapshot(review("OLD"))
        current = snapshot(review("OLD"), review("NEW"))
        self.assertEqual(rc.newly_pending(old, current), ["NEW"])

    def test_incomplete_or_mismatch_no_alert(self):
        old = snapshot()
        for stage in ("READY_NOT_OBSERVED", "RECEIPT_MISMATCH", "REVIEW_INCOMPLETE_OR_MISMATCH"):
            now = snapshot(review(stage=stage, receipt=False))
            self.assertEqual(rc.newly_pending(old, now), [])

    def test_reject_receipt_without_request(self):
        bad = review()
        bad["flags"]["request"] = False
        with self.assertRaises(ValueError):
            rc.newly_pending(snapshot(), snapshot(bad))

    def test_reject_inconsistent_stage(self):
        bad = review(stage="GPT_NOT_OBSERVED", receipt=False)
        with self.assertRaises(ValueError):
            rc.newly_pending(snapshot(), snapshot(bad))

    def test_reject_duplicate_ids(self):
        with self.assertRaises(ValueError):
            rc.newly_pending(snapshot(), snapshot(review(), review()))

    def test_reject_wrong_schema(self):
        with self.assertRaises(ValueError):
            rc.newly_pending({"schema": "BAD", "review_chains": []}, snapshot())

    def test_summary_has_no_execution_trigger(self):
        report = rc.summary(["REQ-1"])
        self.assertIn("GPT 판정 필요", report)
        self.assertIn("No retry or automatic model call", report)
        self.assertNotIn("READY.md", report)


if __name__ == "__main__":
    unittest.main()
