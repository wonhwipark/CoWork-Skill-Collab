"""Offline synthetic tests for GitHub review-chain display (no LIVE operations)."""
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import review_chain

RID = "DASHBOARD-EXAMPLE-001"
SHA = "a" * 64


class ReviewChainTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.folders = {}
        for kind in ("requests", "reviews", "receipts"):
            folder = self.root / "collab" / kind / RID
            folder.mkdir(parents=True)
            self.folders[kind] = folder

    def tearDown(self):
        self.tmp.cleanup()

    def put(self, kind, name, content):
        (self.folders[kind] / name).write_text(content, encoding="utf-8")

    def chain(self, ready=True, review=True, receipt=True, gpt=True):
        req = f"---\nrequest_id: {RID}\nrequest_revision: '1'\npackage_sha256: {SHA}\nwork_id: WORK-A\n---\n"
        self.put("requests", "REQUEST.md", req)
        if ready:
            self.put("requests", "READY.md", f"---\nrequest_id: {RID}\nrequest_revision: 1\npackage_sha256: {SHA}\nrequest_sha256: {hashlib.sha256(req.encode()).hexdigest()}\nstate: READY\n---\n")
        if review:
            self.put("reviews", "REVIEW_RESULT_1.md", f"---\nresponds_to_request_id: {RID}\nresponds_to_request_revision: 1\npackage_sha256: {SHA}\nexecution_status: COMPLETED\nreview_id: {RID}|1|{SHA}|1\n---\n### B-1: <img src=x onerror=alert(1)>\n")
        if receipt:
            self.put("receipts", "RECEIPT_1.md", json.dumps({"request_id": RID, "request_revision": "1", "package_sha256": SHA, "ok": True, "processing_key": f"{RID}|1|{SHA}|1"}))
        if gpt:
            self.put("reviews", "GPT_DISPOSITION.json", json.dumps({"request_id": RID, "request_revision": "1", "package_sha256": SHA, "verdict": "ACCEPT_WITH_CHANGE", "findings": [{"id": "B-1", "decision": "DEFER", "summary": "test & <payload>"}]}))
        return review_chain.collect(self.root)[0]

    def test_unmigrated_not_completed(self):
        self.assertEqual(review_chain.collect(self.root), [])
        self.assertIn("미이관", review_chain.render_markdown([], "owner/repo"))

    def test_request_awaits_ready(self):
        x = self.chain(ready=False, review=False, receipt=False, gpt=False)
        self.assertEqual(x["stage"], "READY_NOT_OBSERVED")

    def test_complete_document_linked_not_signed(self):
        x = self.chain()
        self.assertEqual(x["stage"], "GPT_RECORDED_UNAUTHENTICATED")
        self.assertTrue(all(x["flags"].values()))
        self.assertEqual(x["findings"][0]["decision"], "DEFER")

    def test_fail_closed_on_request_hash_mismatch(self):
        x = self.chain()
        path = self.folders["requests"] / "REQUEST.md"
        path.write_text(path.read_text() + "tampered")
        x = review_chain.collect(self.root)[0]
        self.assertEqual(x["stage"], "READY_MISMATCH")
        self.assertFalse(x["flags"]["gpt"])

    def test_fail_closed_on_bad_receipt(self):
        self.chain()
        data = json.loads((self.folders["receipts"] / "RECEIPT_1.md").read_text())
        data["ok"] = False
        self.put("receipts", "RECEIPT_1.md", json.dumps(data))
        self.assertEqual(review_chain.collect(self.root)[0]["stage"], "RECEIPT_MISMATCH")

    def test_gpt_missing_is_not_completed(self):
        x = self.chain(gpt=False)
        self.assertEqual(x["stage"], "GPT_NOT_OBSERVED")
        self.assertEqual(x["findings"][0]["decision"], "NOT_ADJUDICATED")
        self.assertNotIn("<img src=x onerror", review_chain.render_html([x], "owner/repo"))

    def test_mismatched_gpt_revision(self):
        self.chain()
        path = self.folders["reviews"] / "GPT_DISPOSITION.json"
        data = json.loads(path.read_text())
        data["request_revision"] = "2"
        path.write_text(json.dumps(data))
        self.assertEqual(review_chain.collect(self.root)[0]["stage"], "GPT_DISPOSITION_MISMATCH")

    def test_all_links_restricted_to_private_repo_paths(self):
        with self.assertRaises(ValueError):
            review_chain.href("owner/repo", "collab/requests/../../secret/REQUEST.md")
        with self.assertRaises(ValueError):
            review_chain.href("owner/repo", "https://evil.example")

    def test_render_does_not_copy_review_body_or_html_payload(self):
        x = self.chain(gpt=False)
        view = review_chain.render_html([x], "owner/repo")
        self.assertIn("&lt;img", view)
        self.assertNotIn("<img src=x onerror", view)


if __name__ == "__main__":
    unittest.main()
