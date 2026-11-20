"""v3 of the non-production pinned-ZIP verifier. Differences from v2 (kept side by side, nothing overwritten):
 - runs ALL five rounds even after a failure; every round has its own temp dir (own DBs, own throw-away keys, own fake GitHub);
 - parses FAILED test ids and classifies them; a failing round is never turned into PASS;
 - reports the watcher five-window companion result (real watcher + CLI, stub model) separately from the full-suite result.
Needs pytest + cryptography. No GitHub, no real reviewer CLI, no operating DB/keys/config."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import zipfile
from pathlib import Path, PurePosixPath

EXPECTED_HASH = "c67bc342fe77547b000fc42e1b886396cbef035c0d265dbcd124947e267ed83f"
EXPECTED_SIZE, EXPECTED_MEMBERS, MIN_FULL = 310753, 114, 1038
KNOWN_FLAKE = "su_l1/test_local_only_contract_r0003.py::Race::test_the_same_nonce_in_six_processes_is_accepted_exactly_once"


def check_zip(path: Path) -> dict:
    data = path.read_bytes()
    assert len(data) == EXPECTED_SIZE and hashlib.sha256(data).hexdigest() == EXPECTED_HASH, "ZIP size/SHA mismatch"
    with zipfile.ZipFile(path) as z:
        ms = z.infolist()
        assert len(ms) == EXPECTED_MEMBERS and z.testzip() is None, "ZIP member count/CRC"
        for m in ms:
            n = PurePosixPath(m.filename)
            assert not n.is_absolute() and ".." not in n.parts and ":" not in m.filename, f"unsafe path {m.filename}"
            assert ((m.external_attr >> 16) & 0o170000) != stat.S_IFLNK, f"symlink {m.filename}"
    return {"zip_sha256": EXPECTED_HASH, "size": EXPECTED_SIZE, "members": EXPECTED_MEMBERS, "crc": "PASS"}


def run_step(root: Path, env: dict, label: str, target: list[str], minimum: int) -> dict:
    cmd = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *target]
    done = subprocess.run(cmd, cwd=root, env=env, capture_output=True, text=True, timeout=1500)
    m = list(re.finditer(r"(?<!\d)(\d+) passed\b", done.stdout))
    passed = int(m[-1].group(1)) if m else 0
    failed = sorted(set(re.findall(r"^FAILED (\S+)", done.stdout, flags=re.M)))
    failed = [re.sub(r"\\", "/", f).split(" - ")[0] for f in failed]
    ok = done.returncode == 0 and passed >= minimum
    return {"step": label, "status": "PASS" if ok else "FAIL", "passed": passed, "minimum_pass_required": minimum,
            "returncode": done.returncode, "failed_tests": failed, "summary": (done.stdout.strip().splitlines() or [""])[-1],
            "stdout_tail": done.stdout[-1800:] if not ok else ""}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--zip", required=True, type=Path)
    p.add_argument("--companion-test", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    a = p.parse_args()
    rep = {"schema": "COWORK_V029_5_WINDOWS_REAL_ZIP_TEST_V3", "real_live": False, "real_model_calls": 0, "actual_paid_reviews": 0,
           "actual_remote_ready_posts": 0, "rounds": [], "independent_review": "NOT_RUN"}
    try:
        rep["zip"] = check_zip(a.zip)
        for n in range(1, 6):
            with tempfile.TemporaryDirectory(prefix=f"cowork_v029_v3_r{n}_") as td:
                root = Path(td) / "candidate"
                root.mkdir()
                with zipfile.ZipFile(a.zip) as z:
                    z.extractall(root)
                shutil.copyfile(a.companion_test, root / "tests" / "test_five_windows_actual_zip.py")
                env = {**os.environ, "PYTHONNOUSERSITE": "1", "PYTHONDONTWRITEBYTECODE": "1"}
                t0 = time.monotonic()
                comp = run_step(root, env, "five_window_companion", ["tests/test_five_windows_actual_zip.py"], 4)
                full = run_step(root, env, "full_suite", ["."], MIN_FULL)
                only_flake = bool(full["failed_tests"]) and set(full["failed_tests"]) == {KNOWN_FLAKE}
                rep["rounds"].append({
                    "round": n, "isolated_temp_dir": True, "elapsed_seconds": round(time.monotonic() - t0, 1),
                    "watcher_5window": comp["status"], "full_suite": full["status"],
                    "full_suite_classification": "PASS" if full["status"] == "PASS" else ("ISOLATED_NONPRODUCTION_FLAKE_ONLY" if only_flake else "FAIL"),
                    "steps": [comp, full]})
        r = rep["rounds"]
        rep["watcher_5window_rounds_pass"] = f'{sum(x["watcher_5window"] == "PASS" for x in r)}/5'
        rep["full_suite_rounds_pass"] = f'{sum(x["full_suite"] == "PASS" for x in r)}/5'
        rep["full_suite_failed_tests_seen"] = sorted({t for x in r for t in x["steps"][1]["failed_tests"]})
        rep["watcher_5window_overall"] = "PASS" if all(x["watcher_5window"] == "PASS" for x in r) else "FAIL"
        rep["full_suite_overall"] = ("PASS" if all(x["full_suite"] == "PASS" for x in r) else
                                     "FAIL_WITH_ISOLATED_NONPRODUCTION_FLAKE" if all(x["full_suite_classification"] in ("PASS", "ISOLATED_NONPRODUCTION_FLAKE_ONLY") for x in r) else "FAIL")
    except Exception as exc:  # noqa: BLE001
        rep["error"] = f"{type(exc).__name__}: {exc}"
        rep["watcher_5window_overall"] = rep["full_suite_overall"] = "BLOCKED_OR_FAIL"
    a.output.write_text(json.dumps(rep, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("WATCHER_5WINDOW", rep.get("watcher_5window_overall"), rep.get("watcher_5window_rounds_pass"))
    print("FULL_SUITE", rep.get("full_suite_overall"), rep.get("full_suite_rounds_pass"), rep.get("full_suite_failed_tests_seen"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
