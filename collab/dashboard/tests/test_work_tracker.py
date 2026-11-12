"""Work Tracker V1 regression: isolated skill streams and fail-closed status."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import generate
import work_tracker


class WorkTrackerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.base = self.root / "collab" / "projects"

    def tearDown(self):
        self.tmp.cleanup()

    def project(self, name, text="# Example\n## Latest\nDEVELOPMENT=DESIGN_ONLY\n"):
        root = self.base / name
        root.mkdir(parents=True, exist_ok=True)
        (root / "CURRENT.md").write_text(text, encoding="utf-8")
        return root

    @staticmethod
    def works(*records):
        return {"schema": work_tracker.SCHEMA, "works": list(records)}

    @staticmethod
    def entry(work_id, skill, phase, **kwargs):
        return {"work_id": work_id, "skill": skill, "phase": phase, **kwargs}

    def test_each_project_has_a_unique_work_card(self):
        self.project("WORK-A")
        self.project("WORK-B")
        works = work_tracker.collect(self.root)
        self.assertEqual([w["work_id"] for w in works], ["WORK-A", "WORK-B"])
        self.assertEqual([w["record_source"] for w in works],
                         ["CURRENT_ONLY_UNSTRUCTURED"] * 2)
        self.assertEqual(works[0]["owner"], "미등록")

    def test_two_skills_track_independently_in_single_project(self):
        p = self.project("WORK-TOOLS")
        data = self.works(
            self.entry("WORK-FIX", "l1-fix-workflow", "DEVELOPMENT",
                       owner="GPT", self_test="NOT_RUN", independent_review="NOT_RUN",
                       next_action="개발 검증"),
            self.entry("WORK-GITHUB", "l1-github", "REVIEW",
                       owner="Claude Code", self_test="PASS", independent_review="PENDING",
                       next_action="독립 리뷰 결과 확인"),
        )
        (p / "TRACKER.json").write_text(json.dumps(data), encoding="utf-8")
        got = work_tracker.collect(self.root)
        self.assertEqual(len(got), 2)
        self.assertEqual([w["skill"] for w in got], ["l1-fix-workflow", "l1-github"])
        self.assertNotEqual(got[0]["work_id"], got[1]["work_id"])
        self.assertEqual([w["phase"] for w in got], ["DEVELOPMENT", "REVIEW"])
        self.assertEqual(got[0]["self_test"], "NOT_RUN")
        self.assertEqual(got[1]["independent_review"], "PENDING")
        self.assertEqual(work_tracker.counts(got)["review"], 1)
        self.assertEqual(work_tracker.counts(got)["active"], 1)

    def test_registered_pass_is_not_verified_runtime_pass(self):
        p = self.project("WORK-X")
        data = self.works(self.entry("WORK-FIX", "l1-fix-workflow", "COMPLETE",
                                     self_test="PASS", independent_review="PASS"))
        (p / "TRACKER.json").write_text(json.dumps(data), encoding="utf-8")
        got = work_tracker.collect(self.root)
        self.assertEqual(got[0]["record_source"], "REGISTERED_METADATA_UNVERIFIED")
        self.assertIn("운영 근거 별도", got[0]["evidence"])
        page = work_tracker.render_html(got, lambda p: generate.url_for(generate.REPO, p))
        self.assertIn("TRACKER.json 신고 값", page)

    def test_invalid_manifest_does_not_replace_current(self):
        p = self.project("WORK-C")
        for obj in ({"schema": "wrong", "works": []},
                    self.works(self.entry("DUP", "l1-github", "REVIEW"),
                               self.entry("DUP", "l1-fix-workflow", "DEVELOPMENT")),
                    self.works(self.entry("../bad", "l1-github", "COMPLETE"))):
            (p / "TRACKER.json").write_text(json.dumps(obj), encoding="utf-8")
            got = work_tracker.collect(self.root)
            self.assertEqual(len(got), 1)
            self.assertEqual(got[0]["work_id"], "WORK-C")
            self.assertEqual(got[0]["phase"], "REQUIREMENT")

    def test_no_unbacked_in_progress_skill_fabrication(self):
        self.project("WORK-EXISTING", "# Existing\n\n## Current\nNo registered skill\n")
        text = generate.render_html(generate.build_state(self.root))
        self.assertNotIn("l1-fix-workflow", text)
        self.assertNotIn("l1-github", text)
        self.assertIn("Work ID: WORK-EXISTING", text)
        self.assertIn("단계 미확인", text)

    def test_latest_section_not_old_completion(self):
        self.project("WORK-P", "# X\n\n## Latest\nINDEPENDENT_REVIEW=NOT_RUN\n"
                              "DEVELOPMENT=DESIGN_ONLY\n\n## Archive\nINDEPENDENT_REVIEW=PASS\n")
        got = work_tracker.collect(self.root)
        self.assertEqual(got[0]["independent_review"], "NOT_RUN")
        self.assertEqual(got[0]["phase"], "REQUIREMENT")

    def test_html_escaping_and_no_raw_untrusted_markup(self):
        p = self.project("WORK-A")
        data = self.works(self.entry("WORK-1", "l1-github", "DEVELOPMENT",
                       title='<img src=x onerror="alert(1)">',
                       owner='GPT <script>alert(2)</script>',
                       next_action='test <b>safe</b>'))
        (p / "TRACKER.json").write_text(json.dumps(data), encoding="utf-8")
        html = work_tracker.render_html(work_tracker.collect(self.root), lambda p: generate.url_for(generate.REPO, p))
        self.assertIn("&lt;img", html)
        self.assertNotIn("<img src=x", html)
        self.assertIn("&lt;b&gt;safe&lt;/b&gt;", html)

    def test_output_contains_independent_streams_and_is_deterministic(self):
        p = self.project("WORK-TOOLS")
        data = self.works(self.entry("WORK-FIX", "l1-fix-workflow", "DEVELOPMENT"),
                          self.entry("WORK-GITHUB", "l1-github", "REVIEW"))
        (p / "TRACKER.json").write_text(json.dumps(data), encoding="utf-8")
        first = generate.write_outputs(self.root)
        self.assertEqual(first["schema"], "COWORK_GITHUB_DASHBOARD_SHADOW_V4")
        self.assertEqual(len(first["work_items"]), 2)
        folder = self.root / "collab" / "dashboard"
        initial = {n: (folder / n).read_bytes() for n in ["state.json", "index.html", "VIEW.md"]}
        generate.write_outputs(self.root)
        self.assertEqual(initial, {n: (folder / n).read_bytes() for n in initial})
        self.assertIn("l1-fix-workflow", initial["index.html"].decode("utf-8"))
        self.assertIn("l1-github", initial["VIEW.md"].decode("utf-8"))


if __name__ == "__main__":
    unittest.main()
