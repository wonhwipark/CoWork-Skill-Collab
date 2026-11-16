"""Isolated offline QA for MSC skill candidate ZIPs. Never writes production files."""
import hashlib
import os
from pathlib import Path
import py_compile
import runpy
import stat
import sys
import tempfile
import traceback
import zipfile

REPO = Path(__file__).resolve().parents[4]
ROOT = REPO / "collab/projects/L1-WORKSPACE-RAG-20261111-001"
TARGETS = [
    ("doc-converter_v0_2_23_1116.zip", "43805ae0ce1b08205125441f383f6bdfc6f114ef53bb2609295827f10b1ce23e", "doc-converter",
     ["test_msc_name_collision_v0222.py", "test_msc_b_view_v0223.py"]),
    ("work-ledger-kernel_v0_7_40_1116.zip", "b8077fd717f326fb7bc556407b8e8b8a7f32a580e143ec3a6d646d3b1e9df7ce", ".",
     ["test_msc_svg_export_v0740.py"]),
]
failures = []
checks = []

def check(ok, name, detail=""):
    checks.append((bool(ok), name, detail))
    print(("PASS" if ok else "FAIL") + " | " + name + (" | " + detail if detail else ""), flush=True)
    if not ok:
        failures.append(name + " " + detail)

def safe_name(name):
    p = Path(name)
    return not p.is_absolute() and ".." not in p.parts and "\\" not in name and "\x00" not in name

def execute_test(path, cwd, pkgdir):
    oldcwd = Path.cwd()
    oldpath = sys.path[:]
    try:
        os.chdir(cwd)
        sys.path.insert(0, str(cwd))
        sys.path.insert(0, str(pkgdir))
        mod = runpy.run_path(str(path))
        tests = sorted((k, v) for k, v in mod.items() if k.startswith("test_") and callable(v))
        check(bool(tests), "tests-found " + path.name, str(len(tests)))
        for name, func in tests:
            try:
                func()
                check(True, path.name + "::" + name)
            except Exception as exc:
                check(False, path.name + "::" + name, type(exc).__name__ + ": " + str(exc)[:350])
                traceback.print_exc()
    except Exception as exc:
        check(False, "load-tests " + path.name, type(exc).__name__ + ": " + str(exc)[:350])
        traceback.print_exc()
    finally:
        os.chdir(oldcwd)
        sys.path[:] = oldpath

for filename, expected, dirname, test_names in TARGETS:
    f = ROOT / "candidates" / filename
    if not f.is_file():
        check(False, "candidate-present", filename)
        continue
    digest = hashlib.sha256(f.read_bytes()).hexdigest()
    check(digest == expected, "zip-sha " + filename, digest)
    if digest != expected:
        continue
    try:
        with zipfile.ZipFile(f, "r") as zf:
            bad = zf.testzip()
            check(bad is None, "full-crc " + filename, str(bad))
            members = zf.infolist()
            safe = all(safe_name(m.filename) and
                       not stat.S_ISLNK((m.external_attr >> 16) & 0xFFFF) for m in members)
            check(safe, "zip-path-and-symlink " + filename, str(len(members)) + " members")
            check(len({m.filename for m in members}) == len(members), "zip-unique-names " + filename)
            if not safe or bad:
                continue
            with tempfile.TemporaryDirectory(prefix="msc-candidate-qa-") as td:
                zf.extractall(td)
                root = Path(td) / dirname
                if dirname == ".":
                    root = Path(td)
                python_files = sorted(root.rglob("*.py"))
                syntax_fail = []
                for path in python_files:
                    try:
                        py_compile.compile(str(path), doraise=True)
                    except Exception as exc:
                        syntax_fail.append(path.relative_to(root).as_posix() + ": " + str(exc)[:160])
                check(not syntax_fail, "py-compile " + filename, f"{len(python_files)} files; " + str(syntax_fail[:6]))
                if filename.startswith("doc-converter"):
                    tests_dir = root / "tests"
                    pkgdir = root / "scripts"
                else:
                    tests_dir = root / "tests"
                    pkgdir = root
                for test in test_names:
                    path = tests_dir / test
                    if path.is_file():
                        execute_test(path, root, pkgdir)
                    else:
                        check(False, "test-present " + filename, test)
    except Exception as exc:
        check(False, "zip-processing " + filename, type(exc).__name__ + ": " + str(exc))
        traceback.print_exc()
print(f"MSC_QA_TOTAL={len(checks)} PASS={len(checks) - len(failures)} FAIL={len(failures)}", flush=True)
sys.exit(1 if failures else 0)
