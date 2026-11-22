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

    def request(self, rid, work=None):
        path = self.root / "collab" / "requests" / rid / "REQUEST.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"---\nwork_id: {work or self.work}\nrequest_revision: 1\n---\n", encoding="utf-8")
        return path

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
        (self.root / "collab" / "requests").mkdir()
        got = context_query.snapshot(self.root, "what changed?", topic="skill")
        self.assertEqual(got["state"], "LOCAL_CURRENT_READ_ONLY")
        self.assertEqual(got["host_execution"], "NOT_VERIFIED_BY_LOCAL_FILES")
        self.assertEqual(got["relations"], [])
        self.assertEqual(got["relations_state"], "LOCAL_FILE_PRESENCE_UNVALIDATED")
        self.assertTrue(got["relations_scan"]["complete"])
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
            self.request(f"REQ-OTHER-{j:05}", "OTHER-WORK-123")
        rid = "REQ-THIS-WORK-00001"
        request = p / rid / "REQUEST.md"
        request.parent.mkdir()
        request.write_text(f"---\nwork_id: {self.work}\nrequest_revision: 1\n---\n", encoding="utf-8")
        got = context_query.snapshot(self.root, "스킬 조회", topic="skill")
        self.assertEqual(got["relations_state"], "LOCAL_FILE_PRESENCE_UNVALIDATED")
        self.assertEqual(len(got["relations"]), 1)
        self.assertEqual(got["relations"][0]["execution_verdict"], "NOT_INFERRED_FROM_FILES")

    def test_limit_keeps_valid_relationship_in_scanned_prefix(self):
        good = self.request("REQ-A-VALID-00001")
        others = [self.request(f"REQ-OTHER-{j:05}", "OTHER-WORK-123").parent for j in range(200)]
        with mock.patch.object(Path, "glob", return_value=iter([good.parent] + others)):
            got = context_query.snapshot(self.root, "스킬 조회", topic="skill")
        self.assertEqual([row["request_id"] for row in got["relations"]], [good.parent.name])
        self.assertEqual(got["relations_state"], "RELATIONS_SCAN_LIMIT_EXCEEDED")
        self.assertFalse(got["relations_scan"]["complete"])
        self.assertEqual(got["relations_scan"]["checked_requests"], 200)

    def test_current_hint_is_checked_before_unrelated_request_budget(self):
        good = self.request("REQ-Z-LINKED-0001")
        (self.root / self.rel).write_text(f"## Current\n[Request](../../requests/{good.parent.name}/REQUEST.md)\n", encoding="utf-8")
        others = [self.request(f"REQ-OTHER-{j:05}", "OTHER-WORK-123").parent for j in range(201)]
        with mock.patch.object(Path, "glob", return_value=iter(others)):
            got = context_query.snapshot(self.root, "스킬 조회", topic="skill")
        self.assertEqual([row["request_id"] for row in got["relations"]], [good.parent.name])
        self.assertEqual(got["relations_scan"]["priority_requests"], 1)
        self.assertEqual(got["relations_scan"]["checked_requests"], 200)
        self.assertFalse(got["relations_scan"]["complete"])

    def test_linked_result_supplies_priority_hint(self):
        good = self.request("REQ-Z-RESULT-0001")
        current = self.root / self.rel
        current.write_text("## Current\n[Result](result.md)\n", encoding="utf-8")
        current.with_name("result.md").write_text(f"Request: {good.parent.name}\n", encoding="utf-8")
        others = [self.request(f"REQ-OTHER-{j:05}", "OTHER-WORK-123").parent for j in range(201)]
        with mock.patch.object(Path, "glob", return_value=iter(others)):
            got = context_query.snapshot(self.root, "스킬 조회", topic="skill")
        self.assertEqual([row["request_id"] for row in got["relations"]], [good.parent.name])
        self.assertEqual(got["relations_scan"]["priority_requests"], 1)

    def test_invalid_utf8_request_is_isolated_and_good_row_retained(self):
        good = self.request("REQ-VALID-00001")
        bad = self.request("REQ-OTHER-INVALID", "OTHER-WORK-123")
        bad.write_bytes(b"\xff")
        got = context_query.snapshot(self.root, "스킬 조회", topic="skill")
        self.assertIn("NOT_VERIFIED", got["summary"])
        self.assertEqual([row["request_id"] for row in got["relations"]], [good.parent.name])
        self.assertEqual(got["relations_state"], "RELATIONS_SCAN_INCOMPLETE")
        self.assertIn({"request_id": bad.parent.name, "reason": "UnicodeDecodeError"}, got["relations_scan"]["issues"])
        self.assertFalse(got["relations_scan"]["complete"])

    def test_malformed_request_metadata_is_not_treated_as_another_work(self):
        self.request("REQ-VALID-00001")
        bad = self.request("REQ-INVALID-METADATA")
        bad.write_text("not frontmatter\n", encoding="utf-8")
        got = context_query.snapshot(self.root, "스킬 조회", topic="skill")
        self.assertEqual(len(got["relations"]), 1)
        self.assertEqual(got["relations_state"], "RELATIONS_SCAN_INCOMPLETE")
        self.assertIn({"request_id": bad.parent.name, "reason": "REQUEST_METADATA_NOT_VERIFIED"}, got["relations_scan"]["issues"])

    def test_request_read_error_does_not_stop_other_relationships(self):
        good = self.request("REQ-VALID-00001")
        bad = self.request("REQ-UNREADABLE-0001")
        original = Path.read_text

        def read(path, *args, **kwargs):
            if path == bad:
                raise PermissionError("synthetic permission denial")
            return original(path, *args, **kwargs)

        with mock.patch.object(Path, "read_text", read):
            got = context_query.snapshot(self.root, "스킬 조회", topic="skill")
        self.assertEqual([row["request_id"] for row in got["relations"]], [good.parent.name])
        self.assertIn({"request_id": bad.parent.name, "reason": "PermissionError"}, got["relations_scan"]["issues"])

    def test_priority_hints_are_deduplicated_and_work_membership_checked(self):
        good = self.request("REQ-VALID-00001")
        other = self.request("REQ-FOREIGN-00001", "OTHER-WORK-123")
        current = self.root / self.rel
        current.write_text(f"## Current\n{good.parent.name} {good.parent.name} {other.parent.name}\n", encoding="utf-8")
        got = context_query.snapshot(self.root, "스킬 조회", topic="skill")
        self.assertEqual([row["request_id"] for row in got["relations"]], [good.parent.name])
        self.assertEqual(got["relations_scan"]["checked_requests"], 2)
        self.assertEqual(got["relations_scan"]["priority_requests"], 2)
        self.assertTrue(got["relations_scan"]["complete"])

    def test_missing_linked_request_is_explicitly_unverified(self):
        (self.root / "collab" / "requests").mkdir()
        (self.root / self.rel).write_text("## Current\nREQ-MISSING-00001\n", encoding="utf-8")
        got = context_query.snapshot(self.root, "스킬 조회", topic="skill")
        self.assertEqual(got["relations"], [])
        self.assertFalse(got["relations_scan"]["complete"])
        self.assertIn("empty list does not prove", got["warning"])

    def test_missing_request_directory_is_not_an_empty_completed_scan(self):
        got = context_query.snapshot(self.root, "스킬 조회", topic="skill")
        self.assertEqual(got["relations"], [])
        self.assertEqual(got["relations_state"], "RELATIONS_SCAN_INCOMPLETE")
        self.assertIn({"reason": "REQUEST_DIRECTORY_NOT_VERIFIED"}, got["relations_scan"]["issues"])

    def test_evidence_read_error_keeps_request_and_marks_file_unverified(self):
        self.request("REQ-VALID-00001")
        original = context_query.safe_file

        def safe(root, rel, max_bytes=context_query.MAX_READ):
            if rel.endswith("/APPROVAL_SIG.json"):
                raise PermissionError("synthetic permission denial")
            return original(root, rel, max_bytes)

        with mock.patch.object(context_query, "safe_file", side_effect=safe):
            got = context_query.snapshot(self.root, "스킬 조회", topic="skill")
        self.assertEqual(len(got["relations"]), 1)
        self.assertEqual(got["relations"][0]["evidence_files"]["approval"], "NOT_VERIFIED_LOCAL")
        self.assertFalse(got["relations_scan"]["complete"])

    def test_hint_document_paths_stay_within_work_and_do_not_follow_symlinks(self):
        self.request("REQ-VALID-00001")
        current = self.root / self.rel
        outside = self.root / "outside.md"
        outside.write_text("REQ-OUTSIDE-00001\n", encoding="utf-8")
        current.with_name("alias.md").symlink_to(outside)
        current.write_text("## Current\n[x](C:/secret.md) [x](//host/share/secret.md) [x](../outside.md) [x](alias.md)\n", encoding="utf-8")
        original = Path.read_text

        def read(path, *args, **kwargs):
            self.assertNotEqual(path, outside)
            self.assertNotEqual(path, current.with_name("alias.md"))
            return original(path, *args, **kwargs)

        with mock.patch.object(Path, "read_text", read):
            got = context_query.snapshot(self.root, "스킬 조회", topic="skill")
        self.assertEqual(got["relations_scan"]["priority_requests"], 0)
        self.assertTrue(got["relations_scan"]["complete"])

    def test_hint_document_reads_are_bounded_and_not_recursive(self):
        self.request("REQ-VALID-00001")
        current = self.root / self.rel
        current.write_text("## Current\n" + "\n".join(f"[r](r{j}.md)" for j in range(5)), encoding="utf-8")
        for j in range(5):
            current.with_name(f"r{j}.md").write_text("[next](nested.md)\n", encoding="utf-8")
        seen = []
        original = Path.read_text

        def read(path, *args, **kwargs):
            seen.append(path.name)
            return original(path, *args, **kwargs)

        with mock.patch.object(Path, "read_text", read):
            context_query.snapshot(self.root, "스킬 조회", topic="skill")
        self.assertEqual([name for name in seen if name.startswith("r") and name.endswith(".md")], ["r0.md", "r1.md", "r2.md", "r3.md"])
        self.assertNotIn("nested.md", seen)

    def test_invalid_current_returns_unverified_instead_of_crashing(self):
        (self.root / self.rel).write_bytes(b"\xff")
        got = context_query.snapshot(self.root, "스킬 조회", topic="skill")
        self.assertEqual(got["state"], "CURRENT_NOT_VERIFIED")
        self.assertEqual(got["host_execution"], "NOT_VERIFIED")

    def test_legacy_list_api_rejects_incomplete_scan(self):
        self.request("REQ-INVALID-00001").write_bytes(b"\xff")
        with self.assertRaises(context_query.RequestScanIncomplete):
            context_query.related(self.root, self.work)

    def test_directory_error_keeps_already_checked_priority_relationship(self):
        good = self.request("REQ-VALID-00001")
        (self.root / self.rel).write_text(f"## Current\n{good.parent.name}\n", encoding="utf-8")
        with mock.patch.object(Path, "glob", side_effect=PermissionError("synthetic directory denial")):
            got = context_query.snapshot(self.root, "스킬 조회", topic="skill")
        self.assertEqual([row["request_id"] for row in got["relations"]], [good.parent.name])
        self.assertEqual(got["relations_state"], "RELATIONS_SCAN_INCOMPLETE")
        self.assertIn({"reason": "REQUEST_DIRECTORY_NOT_VERIFIED", "error": "PermissionError"}, got["relations_scan"]["issues"])

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


    def test_route_diagnostics_unmatched_fallback_is_not_a_confirmed_match(self):
        got = context_query.route_diagnostics("회의 일정?")
        self.assertEqual(got["selected_topic"], "skill")
        self.assertEqual(got["state"], "FALLBACK_UNVERIFIED")
        self.assertTrue(got["requires_review"])
        self.assertEqual(got["candidate_topics"], [])

    def test_route_diagnostics_multiple_topic_candidates_are_visible(self):
        got = context_query.route_diagnostics("대시보드 스킬 ZIP 현황?")
        self.assertEqual(got["state"], "MULTI_TOPIC_REVIEW")
        self.assertIn("dashboard", got["candidate_topics"])
        self.assertIn("skill", got["candidate_topics"])
        self.assertTrue(got["requires_review"])

    def test_route_diagnostics_known_groupware_substring_trap(self):
        got = context_query.route_diagnostics("그룹웨어 설치 문의")
        self.assertEqual(got["selected_topic"], "knowledge")  # unchanged legacy behavior
        self.assertEqual(got["state"], "SUBSTRING_MATCH_REVIEW")
        self.assertTrue(got["requires_review"])
        self.assertEqual(context_query.route_diagnostics("그룹 지식 업데이트")["state"], "SINGLE_TOPIC_MATCH")

    def test_explicit_topic_overrides_route_warning(self):
        got = context_query.route_diagnostics("회의 일정?", topic="knowledge")
        self.assertEqual(got["state"], "EXPLICIT_TOPIC")
        self.assertFalse(got["requires_review"])
        self.assertEqual(got["candidate_topics"], ["knowledge"])

    def test_snapshot_emits_uncertain_route_and_maintains_read_only_state(self):
        (self.root / "collab" / "requests").mkdir()
        got = context_query.snapshot(self.root, "회의 일정?")
        self.assertEqual(got["state"], "LOCAL_CURRENT_READ_ONLY")
        self.assertEqual(got["routing"]["state"], "FALLBACK_UNVERIFIED")
        self.assertIn("routing requires review", got["warning"])
        self.assertEqual(got["host_execution"], "NOT_VERIFIED_BY_LOCAL_FILES")

    def test_truncated_current_is_not_presented_as_whole_top_section(self):
        (self.root / "collab" / "requests").mkdir()
        (self.root / self.rel).write_text("## Current\n" + ("A" * 5000) + "\n## Historical\nPASS_OLD\n", encoding="utf-8")
        got = context_query.snapshot(self.root, "스킬 ZIP?", topic="skill")
        self.assertTrue(got["summary_truncated"])
        self.assertLessEqual(len(got["summary"]), 3600)
        self.assertIn("top section is truncated", got["warning"])
        self.assertNotIn("PASS_OLD", got["summary"])

    def test_nested_package_path_does_not_alias_same_basename(self):
        rid = "REQ-PACKAGE-ALIAS-0001"
        request = self.request(rid)
        request.write_text(
            "---\n"
            f"work_id: {self.work}\n"
            "package_path: /SKILL-COLLAB/packages/nested/candidate.zip\n"
            "---\n", encoding="utf-8")
        pkg = self.root / "collab" / "packages" / "candidate.zip"
        pkg.parent.mkdir(parents=True)
        pkg.write_bytes(b"unvalidated local bytes")
        got = context_query.related(self.root, self.work)
        self.assertEqual(len(got), 1)
        self.assertEqual(got[0]["evidence_files"]["package"], "NOT_FOUND_LOCAL")


if __name__ == "__main__":
    unittest.main()
