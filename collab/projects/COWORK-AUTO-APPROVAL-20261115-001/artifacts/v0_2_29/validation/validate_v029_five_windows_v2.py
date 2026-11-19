"""Non-production, fail-closed 5-round verifier for a pinned CoWork watcher ZIP.

Usage (Windows or Linux test machine, never the LIVE install directory):
  python validate_v029_five_windows.py --zip PATH_TO_V029_ZIP \
      --companion-test test_five_windows_actual_zip.py --output test_result.json

Requires: Python, pytest, cryptography. No GitHub API, real reviewer CLI,
operating DB, signing credentials or live configuration is accessed by this
script. The shipped e2e test fixture uses a localhost *fake* server and a
counting Claude CLI stub; localhost networking is required for that fixture.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path, PurePosixPath
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import zipfile

EXPECTED_HASH = "c67bc342fe77547b000fc42e1b886396cbef035c0d265dbcd124947e267ed83f"
EXPECTED_SIZE = 310753
EXPECTED_MEMBERS = 114


def assert_valid_zip(path: Path) -> dict:
    data = path.read_bytes()
    observed_hash = hashlib.sha256(data).hexdigest()
    assert len(data) == EXPECTED_SIZE, f"ZIP size mismatch {len(data)}"
    assert observed_hash == EXPECTED_HASH, f"ZIP SHA mismatch {observed_hash}"
    with zipfile.ZipFile(path) as z:
        members = z.infolist()
        assert len(members) == EXPECTED_MEMBERS, f"ZIP member count {len(members)}"
        assert z.testzip() is None, "ZIP CRC failure"
        for m in members:
            name = PurePosixPath(m.filename)
            assert not name.is_absolute() and ".." not in name.parts, f"ZIP path escape: {m.filename}"
            assert not m.filename.startswith(("/", "\\")) and ":" not in m.filename, f"ZIP unsafe path: {m.filename}"
            kind = (m.external_attr >> 16) & 0o170000
            assert kind != stat.S_IFLNK, f"Symlink refused: {m.filename}"
    return {"zip_sha256": observed_hash, "size": len(data), "members": len(members), "crc": "PASS"}


def main() -> int:
    p = argparse.ArgumentParser(description="Five isolated windows simulation, no operating secrets or real model")
    p.add_argument("--zip", required=True, type=Path)
    p.add_argument("--companion-test", required=True, type=Path)
    p.add_argument("--output", type=Path, default=Path("v029_five_windows_result.json"))
    p.add_argument("--focused-only", action="store_true", help="Development smoke only; not accepted as 5-round full regression")
    args = p.parse_args()
    expected_tests = ("tests/test_v029_cost_refused_exclusion.py", "tests/test_five_windows_actual_zip.py")
    report = {"schema": "COWORK_V029_5_WINDOWS_REAL_ZIP_TEST_V1", "candidate_version": "0.2.29",
              "source": "immutable candidate ZIP", "real_live": False, "real_model_calls": 0,
              "actual_paid_reviews": 0, "actual_remote_ready_posts": 0, "rounds": [],
              "overall": "NOT_RUN", "independent_review": "NOT_RUN"}
    try:
        report["zip"] = assert_valid_zip(args.zip)
        assert args.companion_test.is_file(), "Companion pytest missing"
        for round_num in range(1, 6):
            with tempfile.TemporaryDirectory(prefix=f"cowork_v029_windows_{round_num}_") as td:
                root = Path(td) / "candidate"
                root.mkdir()
                with zipfile.ZipFile(args.zip) as z:
                    z.extractall(root)
                assert (root / "skill_collab_watcher" / "auto_approval.py").exists(), "package source missing"
                assert (root / "tests" / "conftest.py").exists(), "package pytest fixtures missing"
                assert (root / "tests" / "test_v029_cost_refused_exclusion.py").exists(), "cap regression missing"
                shutil.copyfile(args.companion_test, root / "tests" / "test_five_windows_actual_zip.py")
                env = os.environ.copy()
                env.update({"PYTHONNOUSERSITE": "1", "PYTHONDONTWRITEBYTECODE": "1"})
                started = time.monotonic()
                steps = []
                for label, selected, minimum in (
                    ("five_window_companion", ["tests/test_five_windows_actual_zip.py"], 4),
                    ("all_candidate_tests", list(expected_tests) if args.focused_only else ["."], 7 if args.focused_only else 1038),
                ):
                    command = [sys.executable, "-m", "pytest", "-q", *selected]
                    completed = subprocess.run(command, cwd=root, env=env,
                                               capture_output=True, text=True, timeout=1200)
                    matches = list(re.finditer(r"(?<!\d)(\d+) passed\b", completed.stdout))
                    passed = int(matches[-1].group(1)) if matches else 0
                    # A zero-exit test run with all cryptography tests SKIPPED is NOT a PASS.
                    success = completed.returncode == 0 and passed >= minimum
                    steps.append({"step": label, "status": "PASS" if success else "FAIL",
                                  "passed": passed, "minimum_pass_required": minimum,
                                  "returncode": completed.returncode, "command": "python -m pytest -q " + " ".join(selected),
                                  "stdout_tail": completed.stdout[-3500:], "stderr_tail": completed.stderr[-1500:]})
                    if not success:
                        break
                record = {"round": round_num,
                          "status": "PASS" if len(steps) == 2 and all(x["status"] == "PASS" for x in steps) else "FAIL",
                          "elapsed_seconds": round(time.monotonic() - started, 3),
                          "steps": steps}
                report["rounds"].append(record)
                if record["status"] != "PASS":
                    report["overall"] = "FAIL_NO_REVIEW_NO_LIVE"
                    break
        else:
            report["overall"] = "PASS_FOCUSED_ONLY_NOT_RELEASE_GATE" if args.focused_only else "PASS_WATCHER_5X_WRITER_CAS_NOT_RUN"
            report["cross_work_source_rebase"] = "NOT_RUN"
            report["shared_tracker_cas_merge"] = "NOT_RUN"
            report["release_gate"] = "HOLD_UNTIL_SOURCE_WRITER_PROOF_AND_INDEPENDENT_REVIEW"
    except Exception as exc:
        report["overall"] = "BLOCKED_OR_FAIL"
        report["error"] = f"{type(exc).__name__}: {exc}"
    finally:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("RESULT", report["overall"])
        print("ROUNDS", [(x["round"], x["status"]) for x in report["rounds"]])
        print("OUTPUT", args.output.resolve())
    return 0 if report["overall"] == "PASS_WATCHER_5X_WRITER_CAS_NOT_RUN" else 2


if __name__ == "__main__":
    raise SystemExit(main())
