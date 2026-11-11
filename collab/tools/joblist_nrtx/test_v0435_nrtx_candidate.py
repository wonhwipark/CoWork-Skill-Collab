"""v0.4.35 staged NR Tx one-shot design and fail-closed tests."""
from __future__ import annotations
import importlib.util
import json
from pathlib import Path
import tempfile
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
WORKER = ROOT / "scripts" / "nr_tx_knowledge_linux_job.py"
spec = importlib.util.spec_from_file_location("nr_tx_knowledge_worker", WORKER)
worker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(worker)

def test_version_and_request_staged():
    assert (ROOT / "VERSION").read_text().strip() == "0.4.35"
    assert json.loads((ROOT / "requests/one-shot-jobs.json").read_text())["jobs"] == []
    staged = json.loads((ROOT / "requests/staged/one-shot-v0.4.35-nr-l1tx-knowledge-research.json").read_text())
    assert len(staged["jobs"]) == 1
    assert staged["jobs"][0] == {
        "job_id": worker.JOB_ID,
        "profile": worker.PROFILE,
        "platform": "linux",
        "priority": 65,
        "expires_at": "2027-01-31T23:59:59+09:00",
        "params": {},
    }

def test_no_old_job_requeue():
    assert worker.JOB_ID != "JOB-20261107-L1-KNOWLEDGE-INPUT-VERIFY-01"
    assert "l1-knowledge-input-verify-linux" != worker.PROFILE

def test_no_remote_prompt_or_paths():
    text = (ROOT / worker.PROMPT).read_text(encoding="utf8")
    for required in ("L2_L1_TX_REQ", "PHY_CONFIG_REQ", "SCELL_STATUS_IND",
                     "code-analyzer", "doc-converter", "l1-knowledge-updater",
                     "SOURCE_PARENT_DIR_V1", "GROUP_WRITE"):
        if required == "GROUP_WRITE":
            assert "GROUP_WRITE" in text or "게시" in text
        else:
            assert required in text
    assert "/home/whpark/" not in text
    assert "/home/whpark/" not in WORKER.read_text(encoding="utf8")

def test_unsupported_platform_blocks():
    with mock.patch.object(worker.sys, "platform", "darwin"):
        try:
            worker.preflight(Path("/untrusted"), Path("/nonexistent"))
        except ValueError as exc:
            assert str(exc) == "LINUX_NONROOT_REQUIRED"
        else:
            raise AssertionError("untrusted platform allowed")

def test_no_host_config_never_invokes_model():
    with tempfile.TemporaryDirectory() as td:
        home = Path(td) / "home"
        root = home / "l1sw-private-skills" / "job-list"
        root.mkdir(parents=True)
        with mock.patch.object(worker.Path, "home", return_value=home), \
             mock.patch.object(worker.os, "geteuid", return_value=1000), \
             mock.patch.object(worker.sys, "platform", "linux"), \
             mock.patch.dict(worker.os.environ, {"JOB_LIST_JOB_ID": worker.JOB_ID,
                                                 "JOB_LIST_PROFILE": worker.PROFILE,
                                                 "JOB_LIST_RUN_ID": "core_20261112_011200_abc123ab"}, clear=True), \
             mock.patch.object(worker.subprocess, "run", side_effect=AssertionError("model invoked")):
            result = worker.run(root)
        assert result["status"] == "BLOCKED"
        assert result["analysis"] == "NOT_RUN"
        assert result["knowledge_publication"] == "NOT_RUN"
        latest = json.loads((root / worker.RESULT).read_text(encoding="utf8"))
        assert latest["status"] == "BLOCKED"
