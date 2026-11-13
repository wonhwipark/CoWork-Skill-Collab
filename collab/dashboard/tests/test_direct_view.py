"""GitHub Markdown view tests; no network or publishing required."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import generate


class DirectViewTests(unittest.TestCase):
    def test_github_native_view_is_readable_without_pages(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            current = root / "collab/projects/WORK-1/CURRENT.md"
            current.parent.mkdir(parents=True)
            current.write_text("# Example\n\n## 최신\nCUTOVER=MIGRATION_NOT_CUTOVER\n", encoding="utf-8")
            state = generate.write_outputs(root)
            view = (root / "collab/dashboard/VIEW.md").read_text(encoding="utf-8")
            self.assertIn("# CoWork 협업 대시보드", view)
            self.assertIn("PRIVATE · GitHub에서 바로 보기", view)
            self.assertIn("MIGRATION_NOT_CUTOVER", view)
            self.assertIn("WORK-1", view)
            self.assertIn("REQUEST → READY → REVIEW → RECEIPT → GPT 판정", view)
            self.assertIn("파일 수 = 검증 완료 건수 아님", view)
            self.assertEqual(len(state["review_chains"]), 0)

    def test_direct_view_is_stable_and_does_not_claim_live_cutover(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            first = generate.write_outputs(root)
            view1 = (root / "collab/dashboard/VIEW.md").read_bytes()
            generate.write_outputs(root)
            view2 = (root / "collab/dashboard/VIEW.md").read_bytes()
            self.assertEqual(view1, view2)
            self.assertIn(b"MIGRATION_NOT_CUTOVER", view1)
            self.assertNotIn(b"HOST_APPLIED=PASS", view1)
            self.assertEqual(first["live_provider"], "NOT_OBSERVED")


if __name__ == "__main__":
    unittest.main()
