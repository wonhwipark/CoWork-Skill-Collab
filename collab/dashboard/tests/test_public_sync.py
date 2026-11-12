"""CoWork PUBLIC Pages automatic sync: synthetic fail-closed allowlist regressions."""
import base64
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import generate
import public_sync


class AllowlistSyncTests(unittest.TestCase):
    def setUp(self):
        self.state = {
            "schema": public_sync.PRIVATE_SCHEMA, "visibility": "PRIVATE_REPO_ONLY",
            "phase": "MIGRATION_NOT_CUTOVER", "projects": [{"id": "SECRET-PROJECT"}],
            "work_items": [{
                "work_id": "COWORK-GITHUB-DASHBOARD-20261111-001",
                "skill": "cowork-dashboard", "title": "PRIVATE_SECRET_TITLE",
                "owner": "PERSONAL_SECRET_OWNER", "next_action": "PRIVATE_PASSWORD=secret",
                "phase": "DEVELOPMENT", "self_test": "PASS", "independent_review": "NOT_RUN",
            }],
            "transport": {name: {"files_observed": val} for name, val in
                          (("requests", 1), ("reviews", 0), ("receipts", 0))},
            "operations": {"independent_review": "NOT_RUN", "windows_stage1": "NOT_OBSERVED"},
        }

    def test_public_emission_has_no_untrusted_strings_or_ids(self):
        payload = public_sync.build_payload(self.state, "2026-11-12")
        encoded = public_sync.json_bytes(payload).decode("utf-8")
        self.assertEqual(payload["schema"], "COWORK_PUBLIC_STATUS_V1")
        self.assertEqual(payload["counts"]["projects"], 1)
        self.assertEqual(len(payload["work_cards"]), 1)
        for token in ("SECRET-PROJECT", "COWORK-GITHUB-DASHBOARD-20261111-001",
                      "PRIVATE_PASSWORD", "PERSONAL_SECRET_OWNER", "PRIVATE_SECRET_TITLE"):
            self.assertNotIn(token, encoded)
        self.assertIn("CoWork 대시보드", encoded)
        self.assertIn("독립 리뷰 증거 미검증", encoded)
        self.assertNotIn("https://github.com/", encoded)

    def test_unknown_skill_not_disclosed(self):
        self.state["work_items"].append({
            "work_id": "SECRET-2", "skill": "military-secret",
            "title": "PRIVATE SECRET", "phase": "REVIEW",
        })
        payload = public_sync.build_payload(self.state, "2026-11-12")
        self.assertEqual(len(payload["work_cards"]), 1)
        self.assertEqual(payload["counts"]["works"], 2)

    def test_user_named_skill_examples_render_only_if_registered(self):
        empty = public_sync.build_payload(self.state, "2026-11-12")
        self.assertNotIn("l1-fix-workflow", str(empty))
        self.state["work_items"] += [{
            "work_id": "SECRET-WORK-1", "skill": "l1-fix-workflow",
            "title": "TOP SECRET", "next_action": "UNTRUSTED", "phase": "REVIEW",
        }, {
            "work_id": "SECRET-WORK-2", "skill": "l1-github",
            "title": "SENSITIVE", "phase": "REQUIREMENT",
        }]
        payload = public_sync.build_payload(self.state, "2026-11-12")
        out = public_sync.json_bytes(payload).decode("utf-8")
        self.assertEqual(len(payload["work_cards"]), 3)
        for s in ("l1-fix-workflow", "l1-github"):
            self.assertIn(s, out)
        for s in ("TOP SECRET", "SENSITIVE", "UNTRUSTED", "SECRET-WORK-1"):
            self.assertNotIn(s, out)

    def test_completion_and_pass_are_unverified_reports(self):
        self.state["work_items"][0]["phase"] = "COMPLETE"
        self.state["work_items"][0]["independent_review"] = "PASS"
        self.state["operations"]["independent_review"] = "PASS"
        obj = public_sync.build_payload(self.state, "2026-11-12")
        self.assertEqual(obj["work_cards"][0]["phase_label"], "완료 신고 · 증빙 별도")
        self.assertEqual(obj["checks"]["independent_review"], "추가 증거 검증 필요")

    def test_unknown_cutover_state_fails_closed(self):
        for x in ("GITHUB_LIVE", "LIVE_CUTOVER", "UNKNOWN"):
            self.state["phase"] = x
            with self.assertRaises(public_sync.SafetyBlock):
                public_sync.build_payload(self.state, "2026-11-12")

    def test_overflow_missing_and_invalid_state_fails_closed(self):
        for value in (True, -1, "123", 100001):
            self.state["transport"]["requests"]["files_observed"] = value
            with self.assertRaises(public_sync.SafetyBlock):
                public_sync.build_payload(self.state, "2026-11-12")
        self.state["transport"]["requests"]["files_observed"] = 1
        self.state["work_items"][0]["phase"] = "HACKED"
        with self.assertRaises(public_sync.SafetyBlock):
            public_sync.build_payload(self.state, "2026-11-12")

    def test_prepare_rebuild_checks_stale_private_state(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            doc = root / "collab/projects/SAMPLE-1/CURRENT.md"
            doc.parent.mkdir(parents=True)
            doc.write_text("# Synthetic sample\n\n## Current\nDEVELOPMENT=DESIGN_ONLY\n",
                           encoding="utf-8")
            generate.write_outputs(root)
            public_json = public_sync.prepare(root, "2026-11-12")
            self.assertIn(b"COWORK_PUBLIC_STATUS_V1", public_json)
            doc.write_text("# Synthetic changed\n\n## Current\nDEVELOPMENT=DESIGN_ONLY\n",
                           encoding="utf-8")
            with self.assertRaisesRegex(public_sync.SafetyBlock, "stale"):
                public_sync.prepare(root, "2026-11-12")

    def test_missing_write_token_is_blocked_without_api_calls(self):
        raw = public_sync.json_bytes(
            public_sync.build_payload(self.state, "2026-11-12"))
        with patch.object(public_sync, "_request") as network:
            with self.assertRaisesRegex(public_sync.SafetyBlock, "not configured"):
                public_sync.publish_public(raw, "")
            network.assert_not_called()

    def test_public_api_only_uses_exact_allowlisted_path(self):
        with patch.object(public_sync.urllib.request, "urlopen") as net:
            with self.assertRaises(public_sync.SafetyBlock):
                public_sync._request(
                    "https://api.github.com/repos/wonhwipark/L1Work/contents/README.md",
                    "x" * 30)
            net.assert_not_called()

    def test_idempotent_public_readback_without_writes(self):
        raw = public_sync.json_bytes(
            public_sync.build_payload(self.state, "2026-11-12"))
        with patch.object(public_sync, "_read_public_existing",
                          return_value=("a" * 40, raw)), \
             patch.object(public_sync, "_request") as req:
            self.assertEqual(public_sync.publish_public(raw, "x" * 30), "UNCHANGED")
            req.assert_not_called()

    def test_remote_public_bytes_are_verified(self):
        raw = public_sync.json_bytes(
            public_sync.build_payload(self.state, "2026-11-12"))
        with patch.object(public_sync, "_read_public_existing",
                          side_effect=[("a"*40, b"old"), ("b"*40, raw)]) as read, \
             patch.object(public_sync, "_request") as req:
            self.assertEqual(public_sync.publish_public(raw, "x"*30),
                             "POSTED_READBACK_PASS")
            self.assertEqual(read.call_count, 2)
            method = req.call_args.kwargs["method"]
            self.assertEqual(method, "PUT")
            data = json.loads(req.call_args.kwargs["body"])
            self.assertEqual(base64.b64decode(data["content"]), raw)
            self.assertEqual(data["sha"], "a"*40)

    def test_unexpected_public_keys_and_noncanonical_json_block(self):
        raw = public_sync.json_bytes(
            public_sync.build_payload(self.state, "2026-11-12"))
        with self.assertRaises(public_sync.SafetyBlock):
            public_sync.publish_public(raw.rstrip(), "x"*30)
        obj = json.loads(raw)
        obj["private_id"] = "SECRET"
        with self.assertRaises(public_sync.SafetyBlock):
            public_sync.publish_public(public_sync.json_bytes(obj), "x"*30)


if __name__ == "__main__":
    unittest.main()
