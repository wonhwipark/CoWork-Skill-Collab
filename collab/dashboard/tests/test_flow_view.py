"""Synthetic offline regression for the role-based workflow and status diagram."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import flow_view
import generate


class WorkflowDashboardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def current(self, slug, head, older=""):
        f = self.root / "collab" / "projects" / slug / "CURRENT.md"
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text("# Test\n\n## Latest\n" + head + "\n## Older\n" + older, encoding="utf-8")

    def test_latest_section_does_not_inherit_historic_pass(self):
        self.current(flow_view.MIGRATION,
                     "WINDOWS_STAGE1_EXECUTION=NOT_RUN\nINDEPENDENT_REVIEW=NOT_RUN\n"
                     "CUTOVER=MIGRATION_NOT_CUTOVER",
                     "WINDOWS_STAGE1_EXECUTION=PASS\nINDEPENDENT_REVIEW=PASS\nCUTOVER=PASS")
        ops = flow_view.snapshot(self.root)
        self.assertEqual(ops["windows_stage1"], "NOT_RUN")
        self.assertEqual(ops["independent_review"], "NOT_RUN")
        self.assertEqual(ops["cutover"], "MIGRATION_NOT_CUTOVER")

    def test_missing_document_is_unknown_not_pass(self):
        ops = flow_view.snapshot(self.root)
        self.assertEqual(ops["windows_stage1"], "NOT_OBSERVED")
        self.assertEqual(ops["pages_deployment"], "NOT_OBSERVED")

    def test_pages_pass_requires_latest_source_marker(self):
        self.current(flow_view.DASHBOARD, "GITHUB_PAGES_DEPLOY=PASS", "GITHUB_PAGES_DEPLOY=FAIL")
        self.assertEqual(flow_view.snapshot(self.root)["pages_deployment"], "PASS")

    def test_no_inside_outside_terminology_in_new_views(self):
        self.current(flow_view.MIGRATION,
                     "WINDOWS_STAGE1_EXECUTION=NOT_RUN\nINDEPENDENT_REVIEW=NOT_RUN\n"
                     "CUTOVER=MIGRATION_NOT_CUTOVER")
        state = generate.build_state(self.root)
        page = flow_view.render_html(state)
        md = flow_view.render_markdown(state)
        self.assertIn("협업 관리 환경", page)
        self.assertIn("업무 실행 환경", page)
        self.assertIn("협업 관리 환경", md)
        self.assertIn("업무 실행 환경", md)
        self.assertNotIn("사내/", page + md)
        self.assertNotIn("사외", page + md)

    def test_markdown_renders_mermaid_and_qualified_states(self):
        self.current(flow_view.MIGRATION,
                     "WINDOWS_STAGE1_EXECUTION=NOT_RUN\nINDEPENDENT_REVIEW=NOT_RUN\n"
                     "CUTOVER=MIGRATION_NOT_CUTOVER")
        state = generate.build_state(self.root)
        md = flow_view.render_markdown(state)
        self.assertIn(chr(96)*3+"mermaid", md)
        self.assertIn("현재 운영 경로", md)
        self.assertIn("GitHub 목표 경로", md)
        self.assertIn("미실행", md)
        self.assertIn("정식 전환 전", md)
        self.assertIn("완료 건수가 아님", md)

    def test_invalid_untrusted_status_does_not_become_verified(self):
        self.current(flow_view.MIGRATION,
                     "WINDOWS_STAGE1_EXECUTION=HACKED\nINDEPENDENT_REVIEW=PASS")
        state = generate.build_state(self.root)
        page = flow_view.render_html(state)
        self.assertIn("원문 확인 필요", page)
        self.assertNotIn("HACKED", page)

    def test_html_contains_rendered_steps_and_accessibility(self):
        self.current(flow_view.DASHBOARD, "GITHUB_PAGES_DEPLOY=PASS")
        state = generate.build_state(self.root)
        page = generate.render_html(state)
        self.assertIn('class="flow-strip"', page)
        self.assertIn('class="flow-table"', page)
        self.assertIn('aria-label="협업 흐름 및 운영 현황"', page)
        self.assertIn("GitHub PRIVATE", page)
        self.assertIn("업무 실행 환경", page)
        self.assertIn("배포 성공 기록", page)

    def test_real_write_output_includes_flow_and_status(self):
        self.current(flow_view.MIGRATION,
                     "WINDOWS_STAGE1_EXECUTION=NOT_RUN\nINDEPENDENT_REVIEW=NOT_RUN\n"
                     "CUTOVER=MIGRATION_NOT_CUTOVER")
        generate.write_outputs(self.root)
        base = self.root / "collab" / "dashboard"
        page = (base / "index.html").read_text(encoding="utf-8")
        md = (base / "VIEW.md").read_text(encoding="utf-8")
        state = json.loads((base / "state.json").read_text(encoding="utf-8"))
        self.assertEqual(state["schema"], "COWORK_GITHUB_DASHBOARD_SHADOW_V3")
        self.assertEqual(state["operations"]["windows_stage1"], "NOT_RUN")
        self.assertIn("업무 실행 환경", page)
        self.assertIn(chr(96)*3+"mermaid", md)

    def test_deterministic_without_time_or_network(self):
        self.current(flow_view.MIGRATION, "INDEPENDENT_REVIEW=NOT_RUN")
        generate.write_outputs(self.root)
        names = ["index.html", "VIEW.md", "SUMMARY.md", "state.json"]
        parent = self.root / "collab" / "dashboard"
        first = {name: (parent / name).read_bytes() for name in names}
        generate.write_outputs(self.root)
        self.assertEqual(first, {name: (parent / name).read_bytes() for name in names})


if __name__ == "__main__":
    unittest.main()
