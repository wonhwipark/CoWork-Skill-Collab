#!/usr/bin/env python3
"""Isolated candidate smoke tests; never touches user repositories."""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

BASE = Path(__file__).resolve().parent / "output"
V = [
    ("workflow", BASE / "l1-fix-workflow_v1_6_70_1117.zip"),
    ("github", BASE / "l1-github_v0_3_58_1117.zip"),
    ("kernel", BASE / "work-ledger-kernel_v0_7_43_1117.zip"),
]


def assert_raises(fn, *a, **kw):
    try:
        fn(*a, **kw)
    except Exception as exc:
        return type(exc).__name__, str(exc)
    raise AssertionError("EXPECTED_DENIAL_NOT_RAISED")


def git(root, *args):
    cp = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)
    if cp.returncode:
        raise RuntimeError(f"git {args}: {cp.stderr}")
    return cp.stdout


def smoke():
    with tempfile.TemporaryDirectory(prefix="l1kg-qa-") as tmp:
        folders = {}
        for name, path in V:
            assert path.is_file(), f"Missing {path}"
            with zipfile.ZipFile(path) as z:
                assert z.testzip() is None
                target = Path(tmp) / name
                z.extractall(target)
                folders[name] = target
                for meta in (".skill-release.json", "MANIFEST_SHA256.json",
                             "PACKAGE_CONTENTS.sha256", "VERSION"):
                    candidates = list(target.glob(meta)) + list(target.glob("*/" + meta))
                    for p in candidates:
                        txt = p.read_text(encoding="utf-8", errors="replace")
                        print("META", name, p.relative_to(target), txt[:800].replace("\n", " "))
        # Workflow local file/path guard functional smoke.
        wf = folders["workflow"] / "l1-fix-workflow"
        sys.path.insert(0, str(wf))
        from l1_fix_workflow.github_docs import _reject_personal_knowledge_write_paths
        root = Path(tmp) / "workspace"
        (root / "works").mkdir(parents=True)
        (root / "knowledge").mkdir()
        _reject_personal_knowledge_write_paths(root, ["works/W1/README.md", "index/active.json"])
        for s in ("knowledge/a.md", "knowledge/A.md", "../knowledge/a.md",
                  "/absolute/knowledge/a.md", "works/../knowledge/a.md"):
            result = assert_raises(_reject_personal_knowledge_write_paths, root, [s])
            print("WF_DENY_PASS", s, result[0])
        (root / "works" / "indirect").symlink_to(root / "knowledge", target_is_directory=True)
        assert_raises(_reject_personal_knowledge_write_paths, root, ["works/indirect/a.md"])
        print("WF_GUARD_SMOKE_PASS")
        # Git common writer (Workflow work-docs path) smoke.
        gh = folders["github"]
        spec = importlib.util.spec_from_file_location("l1_test_push_guard", gh / "scripts" / "push_guard.py")
        guard = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(guard)
        repo = Path(tmp) / "gitrepo"
        repo.mkdir()
        git(repo, "init", "-q")
        git(repo, "config", "user.name", "Test")
        git(repo, "config", "user.email", "test@example.invalid")
        (repo / "README.md").write_text("baseline\n")
        git(repo, "add", "README.md")
        git(repo, "commit", "-q", "-m", "init")
        (repo / "works").mkdir()
        (repo / "works" / "a.md").write_text("normal\n")
        assert guard.assert_work_docs_knowledge_unchanged(repo)["ok"]
        (repo / "knowledge").mkdir()
        (repo / "knowledge" / "b.md").write_text("protected\n")
        assert_raises(guard.assert_work_docs_knowledge_unchanged, repo)
        git(repo, "add", "knowledge/b.md")
        assert_raises(guard.assert_work_docs_knowledge_unchanged, repo)
        git(repo, "reset", "-q")
        (repo / "knowledge" / "b.md").unlink()
        (repo / "knowledge").rmdir()
        assert guard.assert_work_docs_knowledge_unchanged(repo)["ok"]
        print("GITHUB_GUARD_SMOKE_PASS")
        # Kernel only navigation check here; full real Work export will be separate.
        kern = folders["kernel"]
        src = (kern / "work_ledger_kernel" / "work_ux.py").read_text(encoding="utf-8")
        assert 'if knowledge_readme.is_file():' in src
        assert '[Knowledge 탐색](knowledge/README.md)' in src
        assert 'WORK_DOCS_KNOWLEDGE_UNSAFE_PATH' in src
        print("KERNEL_NAV_SOURCE_SMOKE_PASS (not E2E)")
        print("TARGETED_SMOKE_PASS (T01/T02 full exporter and hard OS gate still NOT_RUN)")


if __name__ == "__main__":
    smoke()
