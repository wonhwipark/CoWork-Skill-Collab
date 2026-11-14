#!/usr/bin/env python3
"""Non-LLM Job-list pipeline smoke worker. Candidate only: not installed."""
from __future__ import annotations
import datetime as dt
import json
import os
from pathlib import Path
import re
import sys
import tempfile

JOB_ID = "JOB-20261114-JOBLIST-E2E-SMOKE-01"
PROFILE = "joblist-e2e-smoke-linux"
RESULT = "output/joblist_e2e_smoke/latest_result.json"
RUN_ID_RE = re.compile(r"core_\d{8}_\d{6}_[0-9a-f]{8}\Z")

def _atomic_new_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() or path.is_symlink():
        raise ValueError("SMOKE_RECEIPT_ALREADY_EXISTS")
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                     prefix=".smoke-", delete=False) as f:
        json.dump(payload, f, ensure_ascii=False, sort_keys=True, indent=2)
        f.write("\n")
        tmp = Path(f.name)
    try:
        if path.exists() or path.is_symlink():
            raise ValueError("SMOKE_RECEIPT_ALREADY_EXISTS")
        tmp.rename(path)
    finally:
        if tmp.exists():
            tmp.unlink()

def preflight(root: Path, home: Path, environ: dict | None = None) -> str:
    env = os.environ if environ is None else environ
    if sys.platform != "linux" or os.name != "posix" or os.geteuid() == 0:
        raise ValueError("LINUX_NONROOT_REQUIRED")
    if root.is_symlink() or root.resolve() != (home / "l1sw-private-skills" / "job-list").resolve():
        raise ValueError("JOB_ROOT_UNEXPECTED")
    if env.get("JOB_LIST_JOB_ID") != JOB_ID or env.get("JOB_LIST_PROFILE") != PROFILE:
        raise ValueError("JOB_RUNNER_ATTESTATION_MISSING")
    run_id = env.get("JOB_LIST_RUN_ID", "")
    if not RUN_ID_RE.fullmatch(run_id):
        raise ValueError("JOB_RUN_ID_INVALID")
    return run_id

def run(root: Path | None = None, home: Path | None = None, environ: dict | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[1]
    home = home or Path.home().resolve()
    run_id = preflight(root, home, environ)
    out_dir = root / "output" / "joblist_e2e_smoke"
    per_run_path = out_dir / run_id / "result.json"
    if per_run_path.exists():
        raise ValueError("SMOKE_RUN_ALREADY_RECORDED")
    report = {
        "schema_version": 1, "job_id": JOB_ID, "profile": PROFILE,
        "run_id": run_id, "status": "SUCCESS",
        "result_code": "SMOKE_WORKER_REACHED",
        "analysis": "NOT_RUN", "msc": "NOT_RUN",
        "knowledge_publication": "NOT_RUN",
        "source_write": False, "external_export": False,
        "llm_invoked": False,
        "completed_at": dt.datetime.now(dt.timezone.utc).isoformat(),
    }
    _atomic_new_json(per_run_path, report)
    latest = out_dir / "latest_result.json"
    if latest.exists() or latest.is_symlink():
        raise ValueError("SMOKE_LATEST_ALREADY_EXISTS")
    _atomic_new_json(latest, report)
    print(json.dumps({"job_id": JOB_ID, "run_id": run_id,
                      "status": report["status"],
                      "result_code": report["result_code"]}))
    return report

if __name__ == "__main__":
    try:
        run()
    except (OSError, ValueError) as exc:
        print(json.dumps({"job_id": JOB_ID, "status": "BLOCKED",
                          "reason_code": str(exc)[:96]}))
        raise SystemExit(3)
