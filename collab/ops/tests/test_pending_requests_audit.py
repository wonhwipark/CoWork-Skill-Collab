"""기존 watcher의 실제 SQLite 스키마/API를 사용하는 비유료 회귀."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest
import zipfile

OPS = Path(__file__).resolve().parents[1]
REPO = OPS.parents[1]
spec = importlib.util.spec_from_file_location("pending_requests_audit", OPS / "pending_requests_audit.py")
audit_tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit_tool)


class PendingAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source_tmp = tempfile.TemporaryDirectory()
        given = os.environ.get("WATCHER_SOURCE_ROOT")
        if given:
            cls.source = Path(given).resolve(strict=True)
        else:
            selected = os.environ.get("WATCHER_PACKAGE_VERSION", "0.2.25")
            filename, expected = {
                "0.2.25": ("skill-collab-watcher_v0_2_25_1117.zip", "26d63c8a03290499b13b2ceb8ff0b70c06eb1b1bcc1a25fe3d8f65fcc213d228"),
                "0.2.23": ("skill-collab-watcher_v0_2_23_1115_DEV_NOT_FOR_DEPLOYMENT.zip", "f941be8a6b53d00baa10a9b097f234b159470e2aa1242ecc33bcf0bdee080ea7"),
            }[selected]
            package = REPO / "collab/packages" / filename
            raw = package.read_bytes()
            assert hashlib.sha256(raw).hexdigest() == expected
            cls.source = Path(cls.source_tmp.name)
            with zipfile.ZipFile(package) as archive:
                assert archive.testzip() is None
                for member in archive.infolist():
                    assert (cls.source / member.filename).resolve().is_relative_to(cls.source)
                archive.extractall(cls.source)
        sys.path.insert(0, str(cls.source))
        from skill_collab_watcher.state_store import StateStore
        from skill_collab_watcher.models import JobState
        from skill_collab_watcher.validator import parse_front_matter
        cls.Store, cls.States = StateStore, JobState
        cls.parse = staticmethod(parse_front_matter)

    @classmethod
    def tearDownClass(cls):
        cls.source_tmp.cleanup()

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.requests = self.base / "requests"
        self.requests.mkdir()
        self.db = self.base / "state.sqlite3"
        self.writer = self.Store(self.db)
        self.writer.pending_scope = "github"

    def tearDown(self):
        self.writer.close()
        self.tmp.cleanup()

    def request(self, rid, rev="1", digest="a" * 64):
        path = self.requests / rid / "REQUEST.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"---\nschema: SKILL_COLLAB_REVIEW_REQUEST_V1\nrequest_id: {rid}\nrequest_revision: '{rev}'\npackage_sha256: {digest}\n---\n", encoding="utf-8")
        self.writer.add_pending(rid)

    def job(self, rid, rev="1", digest="a" * 64, state="COMPLETED"):
        self.writer.create_job(f"{rid}|{rev}|{digest}|1", rid, rev, digest, self.States(state))

    def claim(self, rid, rev="1", digest="a" * 64, stage="UNCERTAIN"):
        self.writer.ensure_auto_tables()
        assert self.writer.auto_claim(rid, rev, digest, 100, "SENSITIVE_CANDIDATE_DO_NOT_PRINT", 1,
            max_day_calls=2, max_day_cents=300, max_month_cents=1000) == "CLAIMED"
        self.writer.auto_update(rid, rev, 2, stage=stage,
            approval_text="SENSITIVE_SIGNATURE_DO_NOT_PRINT", ready_text="SENSITIVE_READY_DO_NOT_PRINT",
            detail="SENSITIVE_ERROR_DO_NOT_PRINT")

    def run_audit(self):
        store = self.Store(self.db, read_only=True)
        try:
            statements = []
            store.conn.set_trace_callback(statements.append)
            result = audit_tool.audit(store, self.requests, "github", self.parse)
            self.assertTrue(all(sql.lstrip().split()[0].upper() in ("SELECT", "BEGIN", "ROLLBACK") for sql in statements))
            return result
        finally:
            store.close()

    def test_nine_rows_are_four_completed_one_held_four_waiting(self):
        for i in range(9):
            rid = f"REQ-{i}"
            self.request(rid)
            if i < 4:
                self.job(rid)
        self.claim("REQ-4")
        before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in self.base.glob("state.sqlite3*") if not p.name.endswith("-shm")}
        result = self.run_audit()
        self.assertEqual(result["counts"]["github"], {"completed": 4, "held": 1, "waiting": 4,
            "unverified": 0, "tracked_total": 9, "unresolved_total": 5})
        self.assertEqual(len(self.writer.list_pending("github")), 9)
        self.assertEqual(before, {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in self.base.glob("state.sqlite3*") if not p.name.endswith("-shm")})

    def test_new_revision_is_not_hidden_by_old_completion(self):
        self.request("REQ-A", rev="2")
        self.job("REQ-A")
        self.assertEqual(self.run_audit()["requests"][0]["category"], "WAITING")

    def test_changed_package_same_revision_is_held(self):
        self.request("REQ-A", digest="b" * 64)
        self.job("REQ-A")
        self.assertEqual(self.run_audit()["requests"][0]["category"], "HELD")

    def test_missing_request_cannot_be_marked_completed(self):
        self.writer.add_pending("REQ-A")
        self.job("REQ-A")
        self.assertEqual(self.run_audit()["requests"][0]["category"], "UNVERIFIED")

    def test_uncertain_is_preserved_even_with_completed_job(self):
        self.request("REQ-A")
        self.job("REQ-A")
        self.claim("REQ-A")
        before = self.writer.auto_get_claim("REQ-A", "1")
        row = self.run_audit()["requests"][0]
        self.assertEqual(row["category"], "HELD")
        self.assertEqual(row["manual_signing_admission"], "NOT_ASSESSED")
        self.assertFalse(row["requeue_allowed"])
        self.assertEqual(self.writer.auto_get_claim("REQ-A", "1"), before)

    def test_upload_pending_is_not_completed_or_rerun(self):
        self.request("REQ-A")
        self.job("REQ-A", state="UPLOAD_PENDING")
        self.assertEqual(self.run_audit()["requests"][0]["category"], "HELD")

    def test_no_auto_tables_are_created(self):
        self.request("REQ-A")
        self.run_audit()
        self.assertFalse(self.writer._table_exists("auto_claims"))

    def test_writable_store_is_refused(self):
        with self.assertRaises(ValueError):
            audit_tool.audit(self.writer, self.requests, "github", self.parse)

    def test_other_provider_is_not_matched_to_github_request(self):
        self.request("REQ-A")
        self.claim("REQ-A")
        self.writer.pending_scope = "dropbox"
        self.writer.add_pending("REQ-A")
        result = self.run_audit()
        other = next(r for r in result["requests"] if r["scope"] == "dropbox")
        self.assertEqual(other["category"], "UNVERIFIED")
        self.assertEqual(other["auto_claims"], [])

    def test_sensitive_claim_values_are_not_printed(self):
        self.request("REQ-A")
        self.claim("REQ-A")
        self.assertNotIn("SENSITIVE_", json.dumps(self.run_audit()))

    def test_symlink_outside_request_root_is_not_read(self):
        self.request("REQ-A")
        request = self.requests / "REQ-A/REQUEST.md"
        request.unlink()
        outside = self.base / "private.txt"
        outside.write_text("DO_NOT_READ_SECRET", encoding="utf-8")
        try:
            request.symlink_to(outside)
        except OSError:
            self.skipTest("symlink creation unavailable")
        result = self.run_audit()
        self.assertEqual(result["requests"][0]["identity_error"], "REQUEST_OUTSIDE_ROOT")
        self.assertNotIn("DO_NOT_READ_SECRET", json.dumps(result))

    def test_request_folder_id_mismatch_is_unverified(self):
        self.request("REQ-A")
        p = self.requests / "REQ-A/REQUEST.md"
        p.write_text(p.read_text().replace("request_id: REQ-A", "request_id: REQ-B"))
        self.assertEqual(self.run_audit()["requests"][0]["category"], "UNVERIFIED")

    def test_request_prefix_with_underscore_does_not_match_other_audit_keys(self):
        self.request("REQ_A")
        self.writer.log_event("REVIEW_DISPATCHED", processing_key=f"REQXA|1|{'a'*64}|1")
        self.assertEqual(self.run_audit()["requests"][0]["recorded_execution_events"], {})

    def test_malformed_yaml_is_unverified_and_does_not_abort_other_requests(self):
        self.request("REQ-A")
        self.request("REQ-B")
        (self.requests / "REQ-A/REQUEST.md").write_text("---\ninvalid: [\n---\n", encoding="utf-8")
        result = self.run_audit()
        self.assertEqual(result["counts"]["github"]["unverified"], 1)
        self.assertEqual(result["counts"]["github"]["waiting"], 1)

    def test_invalid_database_fails_closed_without_traceback(self):
        target = self.base / "invalid.sqlite3"
        target.write_text("invalid DB bytes", encoding="utf-8")
        result = subprocess.run([sys.executable, str(OPS / "pending_requests_audit.py"),
            "--watcher-root", str(self.source), "--db", str(target),
            "--requests-root", str(self.requests), "--scope", "github"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(target.read_text(), "invalid DB bytes")

    def test_cli_is_read_only_and_never_creates_missing_db(self):
        target = self.base / "missing/state.sqlite3"
        result = subprocess.run([sys.executable, str(OPS / "pending_requests_audit.py"),
            "--watcher-root", str(self.source), "--db", str(target),
            "--requests-root", str(self.requests), "--scope", "github"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertFalse(target.parent.exists())

    def test_cli_runs_against_real_existing_store(self):
        self.request("REQ-A")
        self.job("REQ-A")
        before = self.writer.conn.execute("SELECT COUNT(*) FROM audit_log").fetchone()[0]
        result = subprocess.run([sys.executable, str(OPS / "pending_requests_audit.py"),
            "--watcher-root", str(self.source), "--db", str(self.db),
            "--requests-root", str(self.requests), "--scope", "github"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        out = json.loads(result.stdout)
        self.assertEqual(out["counts"]["github"]["completed"], 1)
        self.assertEqual(out["model_execution"], "NOT_RUN")
        self.assertEqual(self.writer.conn.execute("SELECT COUNT(*) FROM audit_log").fetchone()[0], before)



class TargetDiagnosticTests(unittest.TestCase):
    """Synthetic SQLite tests for the exact v0.2.35 audit_log/auto_seen columns."""

    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.executescript(
            "CREATE TABLE audit_log(id INTEGER PRIMARY KEY, ts TEXT, event TEXT, processing_key TEXT, detail TEXT);"
            "CREATE TABLE auto_seen(request_id TEXT, revision TEXT);")
        self.store = type("ReadStore", (), {
            "conn": self.conn,
            "_table_exists": lambda _, name: bool(self.conn.execute(
                "SELECT 1 FROM sqlite_master WHERE name=?", (name,)).fetchone()),
        })()

    def tearDown(self):
        self.conn.close()

    def log(self, event, key, detail=""):
        self.conn.execute("INSERT INTO audit_log(ts,event,processing_key,detail) VALUES(?,?,?,?)",
                          ("2026-11-25T02:00:00Z", event, key, detail))

    def result(self):
        return audit_tool._target_diagnostic(self.store, "REQ_A", "1")

    def test_missing_is_not_admission(self):
        r = self.result()
        self.assertEqual(r["auto_seen"], "NO_MATCHING_ROW")
        self.assertEqual(r["events"], [])
        self.assertFalse(r["requeue_allowed"])

    def test_scope_and_seen(self):
        self.conn.execute("INSERT INTO auto_seen VALUES(?,?)", ("REQ_A", "1"))
        self.log("AUTO_NOT_ELIGIBLE", "REQ_A", "SCOPE")
        r = self.result()
        self.assertEqual(r["auto_seen"], "RECORDED")
        self.assertEqual(r["events"][0]["reason_code"], "SCOPE")
        self.assertEqual(r["events"][0]["revision_binding"], "ID_ONLY")

    def test_exact_prefix_and_revision(self):
        self.log("WAIT_INPUT", "REQXA|1", "SECRET")
        self.log("WAIT_INPUT", "REQ_A|2", "SECRET")
        self.log("WAIT_INPUT", "REQ_A|1", json.dumps(dict(
            request_id="REQ_A", revision="1", approval_stage="SCOPE", reason_code="SCOPE")))
        r = self.result()
        self.assertEqual(len(r["events"]), 1)
        self.assertEqual(r["events"][0]["reason_code"], "SCOPE")

    def test_secret_and_bad_json_binding(self):
        self.log("AUTO_ERROR", "REQ_A", "TOKEN secret")
        self.log("WAIT_INPUT", "REQ_A|1", json.dumps(dict(
            request_id="OTHER", revision="1", approval_stage="SCOPE", reason_code="SCOPE")))
        r = self.result()
        self.assertNotIn("TOKEN", json.dumps(r))
        self.assertTrue(all(e["reason_code"] == "NOT_VERIFIED" for e in r["events"]))

    def test_scan_read_only(self):
        self.log("SCAN_START", None)
        self.conn.commit()
        trace = []
        self.conn.set_trace_callback(trace.append)
        self.assertTrue(self.result()["last_scan_at"])
        self.assertTrue(all(s.startswith("SELECT") for s in trace))

    def test_intent_reject_code(self):
        self.log("AUTO_NOT_ELIGIBLE", "REQ_A", "INTENT_REJECTED: EXPIRED")
        self.assertEqual(self.result()["events"][0]["reason_code"], "INTENT_EXPIRED")

    def test_invalid_id(self):
        with self.assertRaises(ValueError):
            audit_tool._target_diagnostic(self.store, "../escape", "1")


if __name__ == "__main__":
    unittest.main()
