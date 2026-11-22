"""P1/P2 read-only scoped retrieval/relations/delta regression tests."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import context_query


class ContextQueryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.work = "COWORK-SKILL-DISCOVERY-20261112-001"
        self.rel = f"collab/projects/{self.work}/CURRENT.md"
        path = self.root / self.rel
        path.parent.mkdir(parents=True)
        path.write_text("# CURRENT\n\n## 2026-11-20 current\n- **STATE:** NOT_VERIFIED\n- **NEXT:** Check source\n\n---\n\n## 2026-11-17 old\n- **STATE:** PASS_OLD\n", encoding="utf-8")

    def test_router_and_fallback(self):
        self.assertEqual(context_query.choose("대시보드 화면 가독성")[0], "dashboard")
        self.assertEqual(context_query.choose("그룹 knowledge 반영")[0], "knowledge")
        self.assertEqual(context_query.choose("USD3 보호 위임 정책")[0], "auto")
        self.assertEqual(context_query.choose("Linux MCP worker")[0], "execution")
        self.assertEqual(context_query.choose("스킬 zip 버전")[0], "skill")
        self.assertEqual(context_query.choose("arbitrary question")[0], "skill")

    def test_top_summary_excludes_historical_pass(self):
        p = self.root / self.rel
        current = context_query.top_summary(p.read_text(encoding="utf-8"))
        self.assertIn("NOT_VERIFIED", current)
        self.assertNotIn("PASS_OLD", current)

    def test_missing_current_never_passes(self):
        data = context_query.snapshot(self.root, "리뷰", topic="collab")
        self.assertEqual(data["state"], "CURRENT_NOT_VERIFIED")
        self.assertEqual(data["host_execution"], "NOT_VERIFIED")

    def test_request_linked_without_execution_claim(self):
        rid = "REQ-COWORK-TEST-20261120"
        path = self.root / "collab" / "requests" / rid / "REQUEST.md"
        path.parent.mkdir(parents=True)
        path.write_text("---\nschema: SKILL_COLLAB_REVIEW_REQUEST_V1\n"
                        f"work_id: {self.work}\nrequest_revision: 1\n"
                        "package_path: /SKILL-COLLAB/packages/candidate.zip\n"
                        "package_sha256: abc012\n---\n", encoding="utf-8")
        (self.root / "collab" / "packages").mkdir(parents=True)
        (self.root / "collab" / "packages" / "candidate.zip").write_bytes(b"not a verified ZIP")
        rows = context_query.related(self.root, self.work)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["request_id"], rid)
        self.assertEqual(rows[0]["evidence_files"]["package"], "PRESENT_LOCAL_UNVALIDATED")
        self.assertEqual(rows[0]["evidence_files"]["review"], "NOT_FOUND_LOCAL")
        self.assertEqual(rows[0]["evidence_files"]["ready"], "NOT_FOUND_LOCAL")
        self.assertEqual(rows[0]["execution_verdict"], "NOT_INFERRED_FROM_FILES")

    def test_other_work_is_not_crosslinked(self):
        rid = "REQ-COWORK-TEST-OTHER"
        path = self.root / "collab" / "requests" / rid / "REQUEST.md"
        path.parent.mkdir(parents=True)
        path.write_text("---\nwork_id: OTHER-WORK-123\n---\n", encoding="utf-8")
        self.assertEqual(context_query.related(self.root, self.work), [])

    def test_symlink_and_traversal_fail_closed(self):
        target = self.root / self.rel
        link = self.root / "collab" / "alias.md"
        link.symlink_to(target)
        self.assertIsNone(context_query.safe_file(self.root, "collab/alias.md"))
        self.assertIsNone(context_query.safe_file(self.root, "../outside"))
        self.assertIsNone(context_query.safe_file(self.root, "/etc/passwd"))
        self.assertIsNone(context_query.safe_file(self.root, "collab/../../etc/passwd"))

    def test_diff_without_baseline_does_not_guess(self):
        current = (self.root / self.rel).read_text(encoding="utf-8")
        self.assertEqual(context_query.diff_summary(self.root, self.rel, current, None)["state"], "NO_BASELINE")
        self.assertEqual(context_query.diff_summary(self.root, self.rel, current, "bad")["state"], "INVALID_COMMIT")
        self.assertEqual(context_query.diff_summary(self.root, self.rel, current, "0"*40)["state"], "BASELINE_NOT_VERIFIED")

    def test_snapshot_explicitly_does_not_verify_host(self):
        got = context_query.snapshot(self.root, "what changed?", topic="skill")
        self.assertEqual(got["state"], "LOCAL_CURRENT_READ_ONLY")
        self.assertEqual(got["host_execution"], "NOT_VERIFIED_BY_LOCAL_FILES")
        self.assertEqual(got["relations"], [])
        self.assertEqual(got["relations_state"], "LOCAL_FILE_PRESENCE_UNVALIDATED")
        self.assertEqual(got["delta"]["state"], "NO_BASELINE")


    def test_snapshot_scan_limit_returns_explicit_degraded_state(self):
        p = self.root / "collab" / "requests"
        p.mkdir(parents=True)
        for j in range(201):
            (p / f"REQ-OTHER-{j:05}").mkdir()
        # The limit applies to all folders, even if none belongs to this Work.
        got = context_query.snapshot(self.root, "스킬 조회", topic="skill")
        self.assertEqual(got["state"], "LOCAL_CURRENT_READ_ONLY")
        self.assertIn("NOT_VERIFIED", got["summary"])
        self.assertEqual(got["relations_state"], "RELATIONS_SCAN_LIMIT_EXCEEDED")
        self.assertEqual(got["relations"], [])
        self.assertIn("incomplete and NOT_VERIFIED", got["warning"])
        self.assertEqual(got["host_execution"], "NOT_VERIFIED_BY_LOCAL_FILES")

    def test_snapshot_at_limit_does_not_drop_valid_relation(self):
        p = self.root / "collab" / "requests"
        p.mkdir(parents=True)
        for j in range(199):
            (p / f"REQ-OTHER-{j:05}").mkdir()
        rid = "REQ-THIS-WORK-00001"
        request = p / rid / "REQUEST.md"
        request.parent.mkdir()
        request.write_text(f"---\nwork_id: {self.work}\nrequest_revision: 1\n---\n", encoding="utf-8")
        got = context_query.snapshot(self.root, "스킬 조회", topic="skill")
        self.assertEqual(got["relations_state"], "LOCAL_FILE_PRESENCE_UNVALIDATED")
        self.assertEqual(len(got["relations"]), 1)
        self.assertEqual(got["relations"][0]["execution_verdict"], "NOT_INFERRED_FROM_FILES")

    def test_windows_drive_paths_rejected_before_filesystem_access(self):
        with mock.patch.object(Path, "is_symlink", side_effect=AssertionError("filesystem accessed")), \
             mock.patch.object(Path, "is_file", side_effect=AssertionError("filesystem accessed")), \
             mock.patch.object(Path, "stat", side_effect=AssertionError("filesystem accessed")):
            for path in ("C:/Windows/win.ini", "C:relative.txt", "Z:/private", "//server/share/secret", r"\\server\share\secret"):
                with self.subTest(path=path):
                    self.assertIsNone(context_query.safe_file(self.root, path))

    def test_router_documents_existing_known_false_positive(self):
        # No router policy change in F3: retain and document its known bias.
        self.assertEqual(context_query.choose("그룹웨어 설치 문의")[0], "knowledge")
        self.assertEqual(context_query.choose("전혀 관계없는 질문")[0], "skill")

    def test_request_scan_is_bounded(self):
        p = self.root / "collab" / "requests"
        p.mkdir(parents=True)
        for j in range(3):
            (p / f"REQ-MOCK-{j:05}").mkdir()
        with self.assertRaises(ValueError):
            context_query.related(self.root, self.work, max_requests=2)


if __name__ == "__main__":
    unittest.main()
