"""Pure local regression: no network, watcher, signing, READY or paid calls."""
import contextlib
import io
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import review_request_gate as gate

REQ = "REQ-COWORK-REVIEW-GATE-R2-20261117"
SHA_COMMIT = "f" * 40
REPO_ID = "1451933830"


class GateTests(unittest.TestCase):
    def setUp(self):
        self.ctx = tempfile.TemporaryDirectory()
        self.addCleanup(self.ctx.cleanup)
        self.root = Path(self.ctx.name)
        self.package = self.root / "candidate.zip"
        with zipfile.ZipFile(self.package, "w") as z:
            z.writestr("skill_collab_watcher/__init__.py", "# test package\n")
        self.config = self.root / "reviewer.config.json"
        self.policy_map = {
            "POLICY-STATIC-V1": {"max_budget_usd": 1.0},
            "POLICY-STATIC-V1-LARGE": {"max_budget_usd": 3.0},
        }
        self.save_config()
        self.request = self.root / "REQUEST.md"
        self.fields = {
            "schema": "SKILL_COLLAB_REVIEW_REQUEST_V1", "state": "SUBMITTED",
            "request_id": REQ, "request_revision": "1",
            "project_id": "COWORK-AUTO-APPROVAL-20261115-001",
            "work_id": "COWORK-AUTO-APPROVAL-20261115-001",
            "skill_id": "cowork-review-watcher",
            "package_path": "/SKILL-COLLAB/packages/candidate.zip",
            "package_sha256": hashlib.sha256(self.package.read_bytes()).hexdigest(),
            "package_size_bytes": str(self.package.stat().st_size),
            "reviewer_os": "WINDOWS", "test_policy": "STATIC_ONLY",
            "run_policy_ref": "POLICY-STATIC-V1-LARGE",
        }
        self.save_request()

    def save_config(self):
        self.config.write_text(json.dumps({"review_policy": {"known_run_policy_refs": self.policy_map}}), encoding="utf-8")

    def save_request(self):
        self.request.write_text("---\n" + "".join(f"{key}: {val}\n" for key, val in self.fields.items()) +
                                "knowledge_refs: []\n---\n\n# Review\n", encoding="utf-8")

    def pass_check(self, intent="design", max_usd="3.00"):
        return gate.check_request(self.request, self.package, self.config,
                                  intent=intent, required_budget=gate._target_money(max_usd))

    def run_cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = gate.main(list(args))
        return code, out.getvalue(), err.getvalue()

    def test_old_live_legacy_large_design_passes(self):
        r = self.pass_check()
        self.assertEqual(r["run_policy_ref"], "POLICY-STATIC-V1-LARGE")
        self.assertEqual(r["authorization"], "NOT_CHECKED")
        self.assertEqual(r["request_sha256"], hashlib.sha256(self.request.read_bytes()).hexdigest())
        self.assertEqual(r["model_calls"], 0)

    def test_new_design_preference_when_installed(self):
        self.policy_map["POLICY-STATIC-V1-DESIGN"] = {"max_budget_usd": 3.0}
        self.save_config()
        self.assertEqual(gate.select_policy(gate._json(self.config), "design", gate._target_money("3")),
                         "POLICY-STATIC-V1-DESIGN")

    def test_self_bootstrap_mismatch_is_blocked(self):
        self.fields["run_policy_ref"] = "POLICY-STATIC-V1-DESIGN"
        self.save_request()
        with self.assertRaisesRegex(gate.GateReject, "RUN_POLICY_NOT_LIVE_MATCH"):
            self.pass_check()

    def test_no_host_evidence_fails_closed(self):
        self.config.unlink()
        with self.assertRaises(gate.GateReject):
            self.pass_check()

    def test_unknown_tier_fails_closed(self):
        self.policy_map = {"POLICY-STATIC-V1": {"max_budget_usd": 1.0}}
        self.save_config()
        with self.assertRaisesRegex(gate.GateReject, "POLICY_NOT_INSTALLED"):
            self.pass_check()

    def test_configured_cost_disagrees_with_expected(self):
        self.policy_map["POLICY-STATIC-V1-LARGE"] = {"max_budget_usd": 6.0}
        self.save_config()
        with self.assertRaisesRegex(gate.GateReject, "POLICY_COST_MISMATCH"):
            self.pass_check()

    def test_basic_legacy_one_dollar_not_silently_upgraded(self):
        self.fields["run_policy_ref"] = "POLICY-STATIC-V1"
        self.save_request()
        with self.assertRaisesRegex(gate.GateReject, "POLICY_COST_MISMATCH"):
            self.pass_check("skill", "1.50")

    def test_basic_after_live_config_change(self):
        self.policy_map["POLICY-STATIC-V1"] = {"max_budget_usd": 1.5}
        self.save_config()
        self.fields["run_policy_ref"] = "POLICY-STATIC-V1"
        self.save_request()
        self.assertEqual(self.pass_check("skill", "1.50")["run_policy_ref"], "POLICY-STATIC-V1")

    def test_missing_or_unparseable_registry(self):
        for bad in ({}, {"review_policy": {}}, {"review_policy": {"known_run_policy_refs": ["POLICY-STATIC-V1-LARGE"]}}):
            self.config.write_text(json.dumps(bad), encoding="utf-8")
            with self.assertRaises(gate.GateReject):
                self.pass_check()

    def test_bad_numbers_rejected(self):
        for v in ("3.0", True, 0, -3, float("inf"), float("nan"), 3.001):
            self.policy_map["POLICY-STATIC-V1-LARGE"] = {"max_budget_usd": v}
            self.save_config()
            with self.assertRaises(gate.GateReject):
                self.pass_check()

    def test_modified_package_rejected(self):
        self.package.write_bytes(self.package.read_bytes() + b"modified")
        with self.assertRaisesRegex(gate.GateReject, "PACKAGE_SIZE_MISMATCH"):
            self.pass_check()

    def test_bad_sha_rejected(self):
        self.fields["package_sha256"] = "f" * 64
        self.save_request()
        with self.assertRaisesRegex(gate.GateReject, "PACKAGE_SHA256_MISMATCH"):
            self.pass_check()

    def test_malformed_zip_rejected(self):
        self.package.write_bytes(b"not a zip")
        self.fields["package_sha256"] = hashlib.sha256(self.package.read_bytes()).hexdigest()
        self.fields["package_size_bytes"] = str(self.package.stat().st_size)
        self.save_request()
        with self.assertRaisesRegex(gate.GateReject, "INVALID_PACKAGE_ZIP"):
            self.pass_check()

    def test_zip_traversal_rejected(self):
        with zipfile.ZipFile(self.package, "w") as z:
            z.writestr("../escape.txt", "bad")
        self.fields["package_sha256"] = hashlib.sha256(self.package.read_bytes()).hexdigest()
        self.fields["package_size_bytes"] = str(self.package.stat().st_size)
        self.save_request()
        with self.assertRaisesRegex(gate.GateReject, "UNSAFE_PACKAGE_MEMBER"):
            self.pass_check()

    def test_duplicate_policy_field_rejected(self):
        self.request.write_text(self.request.read_text().replace(
            "run_policy_ref: POLICY-STATIC-V1-LARGE\n", "run_policy_ref: POLICY-STATIC-V1-LARGE\nrun_policy_ref: POLICY-STATIC-V1-DESIGN\n"), encoding="utf-8")
        with self.assertRaisesRegex(gate.GateReject, "REQUEST_DUPLICATE_FIELD"):
            self.pass_check()

    def test_wrong_scope_rejected(self):
        self.fields["work_id"] = "COWORK-OTHER"
        self.save_request()
        with self.assertRaisesRegex(gate.GateReject, "PROJECT_WORK_SCOPE_MISMATCH"):
            self.pass_check()

    def test_invalid_request_path_rejected(self):
        self.fields["package_path"] = "/SKILL-COLLAB/packages/../candidate.zip"
        self.save_request()
        with self.assertRaisesRegex(gate.GateReject, "INVALID_PACKAGE_PATH"):
            self.pass_check()

    def test_source_pin_string_passes(self):
        pin = self.root / "SOURCE_PIN.json"
        pin.write_text(json.dumps({"schema": "SKILL_COLLAB_SOURCE_PIN_V1", "commit": SHA_COMMIT, "repo_id": REPO_ID}))
        gate.check_source_pin(pin, REPO_ID, SHA_COMMIT)

    def test_source_pin_numeric_and_wrong_commit_rejected(self):
        pin = self.root / "SOURCE_PIN.json"
        for bad in ({"schema": "SKILL_COLLAB_SOURCE_PIN_V1", "commit": SHA_COMMIT, "repo_id": 1451933830},
                    {"schema": "SKILL_COLLAB_SOURCE_PIN_V1", "commit": "e" * 40, "repo_id": REPO_ID}):
            pin.write_text(json.dumps(bad))
            with self.assertRaises(gate.GateReject):
                gate.check_source_pin(pin, REPO_ID, SHA_COMMIT)

    def test_select_cli_is_not_approval(self):
        code, out, _ = self.run_cli("select", "--live-config", str(self.config), "--intent", "design")
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)["status"], "POLICY_COMPATIBLE_NOT_APPROVED")

    def test_check_cli_blocked_is_nonzero(self):
        self.fields["run_policy_ref"] = "POLICY-STATIC-V1-DESIGN"
        self.save_request()
        code, out, err = self.run_cli("check", "--live-config", str(self.config), "--intent", "design",
                                      "--request", str(self.request), "--package", str(self.package))
        self.assertEqual(code, 2)
        self.assertFalse(out)
        self.assertIn("REQUEST_PREFLIGHT_BLOCKED", err)

    def test_check_cli_pass_is_prepublication_only(self):
        code, out, err = self.run_cli("check", "--live-config", str(self.config), "--intent", "design",
                                      "--request", str(self.request), "--package", str(self.package))
        self.assertEqual((code, err), (0, ""))
        self.assertEqual(json.loads(out)["status"], "PASS_PREPUBLICATION_ONLY")
        self.assertEqual(json.loads(out)["request_sha256"], hashlib.sha256(self.request.read_bytes()).hexdigest())

    def test_incomplete_source_pin_cli_is_blocked(self):
        code, out, err = self.run_cli("check", "--live-config", str(self.config), "--intent", "design",
                                      "--request", str(self.request), "--package", str(self.package),
                                      "--expected-repo-id", REPO_ID)
        self.assertEqual(code, 2)
        self.assertIn("INCOMPLETE_SOURCE_PIN_CHECK", err)


if __name__ == "__main__":
    unittest.main()
