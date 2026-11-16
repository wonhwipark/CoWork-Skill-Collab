"""Deterministic SOURCE_PIN_V1 tests: no repo, network or watcher operations."""
import contextlib
import io
import json
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import source_pin

COMMIT = "939b5b9f4c59534d908bc48ced59cfd25a4e8f64"
REPO = "1451933830"


class SourcePinTests(unittest.TestCase):
    def test_integer_producer_input_is_quoted_json_string(self):
        text = source_pin.dumps_source_pin(source_commit=COMMIT, repo_id=1451933830)
        self.assertIn('"repo_id": "1451933830"', text)
        self.assertIs(type(json.loads(text)["repo_id"]), str)

    def test_string_producer_input_is_still_string(self):
        self.assertEqual(source_pin.make_source_pin(source_commit=COMMIT, repo_id=REPO)["repo_id"], REPO)

    def test_existing_numeric_json_is_fail_closed_not_normalized(self):
        bad = {"schema": source_pin.SCHEMA, "commit": COMMIT, "repo_id": 1451933830}
        with self.assertRaisesRegex(source_pin.SourcePinError, "JSON string"):
            source_pin.verify_source_pin(bad, expected_repo_id=REPO)

    def test_valid_string_pin_matches_trust_root(self):
        pin = json.loads(source_pin.dumps_source_pin(source_commit=COMMIT, repo_id=REPO))
        self.assertEqual(source_pin.verify_source_pin(pin, expected_repo_id=REPO), pin)

    def test_wrong_repo_rejected(self):
        pin = source_pin.make_source_pin(source_commit=COMMIT, repo_id=REPO)
        with self.assertRaisesRegex(source_pin.SourcePinError, "REPO_ID_MISMATCH"):
            source_pin.verify_source_pin(pin, expected_repo_id="123")

    def test_bool_and_float_not_integer_repo_ids(self):
        for value in (True, False, 1451933830.0, None, "0", "0012", "-1"):
            with self.subTest(value=value), self.assertRaises(source_pin.SourcePinError):
                source_pin.make_source_pin(source_commit=COMMIT, repo_id=value)

    def test_commit_must_be_pinned_sha(self):
        for commit in ("", "not-a-sha", "A" * 40, "f" * 39, "f" * 41):
            with self.subTest(commit=commit), self.assertRaises(source_pin.SourcePinError):
                source_pin.make_source_pin(source_commit=commit, repo_id=REPO)

    def test_schema_and_extra_keys_fail_closed(self):
        pin = source_pin.make_source_pin(source_commit=COMMIT, repo_id=REPO)
        for change in ({"schema": "V2"}, {"READY": "READY"}, {"repo_id": 1451933830}):
            with self.subTest(change=change), self.assertRaises(source_pin.SourcePinError):
                source_pin.verify_source_pin({**pin, **change})

    def test_cli_create_to_stdout_without_remote_write(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            status = source_pin.main(["create", "--repo-id", REPO, "--commit", COMMIT])
        self.assertEqual(status, 0)
        self.assertEqual(json.loads(out.getvalue())["repo_id"], REPO)

    def test_cli_refuses_overwrite_existing_file(self):
        with tempfile.TemporaryDirectory() as td:
            path = pathlib.Path(td) / "SOURCE_PIN.json"
            path.write_text("historical pin is immutable", encoding="utf-8")
            with contextlib.redirect_stderr(io.StringIO()):
                rc = source_pin.main(["create", "--repo-id", REPO, "--commit", COMMIT, "--output", str(path)])
            self.assertEqual(rc, 2)
            self.assertEqual(path.read_text(encoding="utf-8"), "historical pin is immutable")

    def test_cli_check_accepts_new_pin_and_rejects_legacy_numeric(self):
        with tempfile.TemporaryDirectory() as td:
            path = pathlib.Path(td) / "pin.json"
            path.write_text(source_pin.dumps_source_pin(source_commit=COMMIT, repo_id=REPO), encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(source_pin.main(["check", str(path), "--expected-repo-id", REPO]), 0)
            path.write_text(json.dumps({"schema": source_pin.SCHEMA, "commit": COMMIT, "repo_id": 1451933830}), encoding="utf-8")
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(source_pin.main(["check", str(path), "--expected-repo-id", REPO]), 2)


if __name__ == "__main__":
    unittest.main()
