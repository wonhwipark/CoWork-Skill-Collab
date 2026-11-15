"""GITHUB/LIVE transition state, fail-closed public labels and legacy regressions."""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import generate
import public_sync

class GithubLiveProjectionTests(unittest.TestCase):
    def sample(self):
        return {
            "schema": public_sync.PRIVATE_SCHEMA,
            "visibility": "PRIVATE_REPO_ONLY",
            "phase": "GITHUB_LIVE",
            "projects": [{"id": "SECRET-INTERNAL-WORK"}],
            "work_items": [
                {"work_id": "COWORK-GITHUB-DASHBOARD-20261111-001",
                 "skill": "cowork-dashboard",
                 "title": "SECRET TITLE", "owner": "SECRET PERSON",
                 "next_action": "INTERNAL_SECRET", "phase": "REVIEW"}],
            "transport": {k: {"files_observed": 0}
                          for k in ("requests", "reviews", "receipts")},
            "operations": {"active_provider": "GITHUB", "cutover": "LIVE",
                           "independent_review": "NOT_OBSERVED",
                           "windows_stage1": "NOT_OBSERVED"},
        }

    def test_valid_live_pair_only_emits_fixed_public_labels(self):
        payload = public_sync.build_payload(
            self.sample(), "2026-11-15",
            active_provider=public_sync.GITHUB_LIVE_PROVIDER_LABEL)
        self.assertEqual(payload["cutover"], public_sync.GITHUB_LIVE_CUTOVER_LABEL)
        self.assertEqual(payload["checks"]["active_provider"], public_sync.GITHUB_LIVE_PROVIDER_LABEL)
        self.assertEqual(len(payload["work_cards"]), 1)
        encoded = public_sync.json_bytes(payload).decode("utf-8")
        for private in ("SECRET-INTERNAL-WORK", "SECRET TITLE", "SECRET PERSON",
                        "INTERNAL_SECRET", "COWORK-GITHUB-DASHBOARD-20261111-001"):
            self.assertNotIn(private, encoded)
        self.assertNotIn("https://github.com/", encoded)

    def test_mismatched_live_combination_is_blocked(self):
        s = self.sample()
        for field, value in (("active_provider", "NONE"), ("cutover", "MIGRATION_NOT_CUTOVER"),
                             ("cutover", "NOT_OBSERVED")):
            bad = copy.deepcopy(s)
            bad["operations"][field] = value
            with self.assertRaises(public_sync.SafetyBlock):
                public_sync.build_payload(
                    bad, "2026-11-15",
                    active_provider=public_sync.GITHUB_LIVE_PROVIDER_LABEL)
        with self.assertRaises(public_sync.SafetyBlock):
            public_sync.build_payload(s, "2026-11-15", active_provider="기록 미확인")
        s["phase"] = "MIGRATION_NOT_CUTOVER"
        with self.assertRaises(public_sync.SafetyBlock):
            public_sync.build_payload(
                s, "2026-11-15", active_provider=public_sync.GITHUB_LIVE_PROVIDER_LABEL)

    def test_latest_current_proves_provider_and_cutover_together(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = (Path(tmp) / "collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md")
            path.parent.mkdir(parents=True)
            header = "# Migration\n\n## Latest\nACTIVE_PROVIDER=GITHUB\nCUTOVER=LIVE\n"
            path.write_text(header + "## Older\nACTIVE_PROVIDER=NONE\n", encoding="utf-8")
            self.assertEqual(
                public_sync._read_active_provider(Path(tmp)),
                public_sync.GITHUB_LIVE_PROVIDER_LABEL)
            state = generate.build_state(Path(tmp))
            self.assertEqual(state["phase"], "GITHUB_LIVE")
            self.assertIn("GitHub LIVE", generate.render_html(state))
            self.assertNotIn("GitHub 정식 전환 전", generate.render_html(state))
            path.write_text("# Migration\n\n## Latest\nACTIVE_PROVIDER=GITHUB\n",
                            encoding="utf-8")
            with self.assertRaises(public_sync.SafetyBlock):
                public_sync._read_active_provider(Path(tmp))

    def test_public_label_mismatch_fails_before_network(self):
        proposed = public_sync.build_payload(
            self.sample(), "2026-11-15",
            active_provider=public_sync.GITHUB_LIVE_PROVIDER_LABEL)
        proposed["checks"]["active_provider"] = "활성 리뷰 제공자 없음"
        with patch.object(public_sync, "_request") as network:
            with self.assertRaises(public_sync.SafetyBlock):
                public_sync.publish_public(
                    public_sync.json_bytes(proposed), "x" * 30)
            network.assert_not_called()

    def test_legacy_none_remains_supported(self):
        s = self.sample()
        s["phase"] = "MIGRATION_NOT_CUTOVER"
        s["operations"]["active_provider"] = "NONE"
        s["operations"]["cutover"] = "MIGRATION_NOT_CUTOVER"
        p = public_sync.build_payload(
            s, "2026-11-15", active_provider="활성 리뷰 제공자 없음")
        self.assertEqual(p["cutover"], "정식 전환 전")

if __name__ == "__main__":
    unittest.main()
