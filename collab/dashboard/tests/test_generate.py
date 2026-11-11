"""Offline unit tests for SHADOW dashboard generator. No network or writes outside temporary repo."""
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import generate


class DashboardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.proj = self.root / "collab" / "projects" / "WORK-1"
        self.proj.mkdir(parents=True)

    def tearDown(self):
        self.temp.cleanup()

    def put(self, body):
        (self.proj / "CURRENT.md").write_text(body, encoding="utf-8")

    def test_migration_not_cutover_and_no_false_completed_zero(self):
        self.put("# Migration\n\n## 최신 상태\nCUTOVER=MIGRATION_NOT_CUTOVER\n")
        state = generate.build_state(self.root)
        self.assertEqual(state["phase"], "MIGRATION_NOT_CUTOVER")
        self.assertEqual(state["projects"][0]["status"], "전환 전")
        self.assertFalse(state["transport"]["receipts"]["verified"])
        self.assertIn("미이관", state["disclaimer"])

    def test_no_external_content_injection(self):
        self.put('# <img src=x onerror=alert(1)>\n\n## <script>alert(2)</script>\n')
        view = generate.render_html(generate.build_state(self.root))
        self.assertIn('&lt;img', view)
        self.assertNotIn('<img src=x onerror', view)
        self.assertNotIn('<script>alert(2)</script>', view)

    def test_repo_path_validation(self):
        with self.assertRaises(ValueError):
            generate.url_for('x/y', 'collab/projects/../../secret/CURRENT.md')
        with self.assertRaises(ValueError):
            generate.url_for('x/y"onclick=', 'collab/projects/WORK-1/CURRENT.md')

    def test_current_only_and_unknown(self):
        (self.root / 'collab' / 'projects' / 'WORK-2').mkdir(parents=True)
        self.put('# Work\n')
        self.assertEqual(len(generate.build_state(self.root)['projects']), 1)
        self.assertEqual(generate.build_state(self.root)['projects'][0]['status'], '상태 확인 필요')

    def test_transport_file_count_not_verified(self):
        self.put('# Work\n')
        d = self.root / 'collab' / 'requests' / 'REQ-A'
        d.mkdir(parents=True)
        (d / 'REQUEST.md').write_text('text', encoding='utf-8')
        state = generate.build_state(self.root)
        self.assertEqual(state['transport']['requests']['files_observed'], 1)
        self.assertFalse(state['transport']['requests']['verified'])

    def test_repeat_output_byte_stable(self):
        self.put('# Work\n## 첫 섹션\nNOT_RUN\n')
        generate.write_outputs(self.root)
        out = self.root / 'collab' / 'dashboard'
        first = [ (out / n).read_bytes() for n in ['index.html','state.json','SUMMARY.md'] ]
        generate.write_outputs(self.root)
        second = [ (out / n).read_bytes() for n in ['index.html','state.json','SUMMARY.md'] ]
        self.assertEqual(first, second)

    def test_oversized_source_not_included(self):
        self.put('# Work\n' + 'x'*260000)
        self.assertEqual(generate.build_state(self.root)['projects'], [])


if __name__ == '__main__':
    unittest.main()
