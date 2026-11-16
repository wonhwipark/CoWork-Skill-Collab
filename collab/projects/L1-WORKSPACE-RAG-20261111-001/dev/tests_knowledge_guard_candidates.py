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
    ("github", BASE / "l1-github_v0_3_59_1117.zip"),
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
        # Validate regenerated candidate version/release/hash manifests.
        import hashlib
        expected = {"workflow": "1.6.70", "github": "0.3.59", "kernel": "0.7.43"}
        for name, path in V:
            folder = folders[name] / ("l1-fix-workflow" if name == "workflow" else "")
            release_file = folder / ".skill-release.json"
            meta = json.loads(release_file.read_text(encoding="utf-8"))
            assert meta["version"] == expected[name], meta
            assert meta["channel"] == "development_not_for_deployment", meta
            assert meta["archive"] == path.name, meta
            assert (folder / "VERSION").read_text(encoding="utf-8").strip() == expected[name]
            manifest = folder / "MANIFEST_SHA256.json"
            if manifest.is_file():
                obj = json.loads(manifest.read_text(encoding="utf-8"))
                for rel, digest in obj.items():
                    assert hashlib.sha256((folder / rel).read_bytes()).hexdigest() == digest, (name, rel)
            listing = folder / "PACKAGE_CONTENTS.sha256"
            if listing.is_file():
                for ln in listing.read_text(encoding="utf-8").splitlines():
                    digest, rel = ln.split(maxsplit=1)
                    assert hashlib.sha256((folder / rel.strip()).read_bytes()).hexdigest() == digest, (name, rel)
            print("RELEASE_HASH_MANIFEST_PASS", name, expected[name])
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

        # Outbound commits are not visible to git status; compare commits with upstream.
        remote = Path(tmp) / "bare"
        remote.mkdir()
        git(remote, "init", "--bare", "-q")
        git(repo, "branch", "-M", "main")
        git(repo, "remote", "add", "origin", str(remote))
        git(repo, "push", "-q", "-u", "origin", "main")
        assert guard.assert_work_docs_outbound_knowledge_unchanged(repo)["inspected_commits"] == 0
        (repo / "works" / "a.md").write_text("normal outbound edit\n")
        git(repo, "add", "works/a.md")
        git(repo, "commit", "-q", "-m", "work docs only")
        assert guard.assert_work_docs_outbound_knowledge_unchanged(repo)["inspected_commits"] == 1
        git(repo, "push", "-q", "origin", "main")
        (repo / "knowledge").mkdir(exist_ok=True)
        (repo / "knowledge" / "blocked.md").write_text("unpublished knowledge\n")
        git(repo, "add", "knowledge/blocked.md")
        git(repo, "commit", "-q", "-m", "forbidden already committed knowledge")
        assert not git(repo, "status", "--porcelain").strip()
        assert_raises(guard.assert_work_docs_outbound_knowledge_unchanged, repo)
        print("GITHUB_COMMITTED_KNOWLEDGE_DENY_PASS")
        # Kernel only navigation check here; full real Work export will be separate.
        kern = folders["kernel"]
        src = (kern / "work_ledger_kernel" / "work_ux.py").read_text(encoding="utf-8")
        assert 'if knowledge_readme.is_file():' in src
        assert '[Knowledge 탐색](knowledge/README.md)' in src
        assert 'WORK_DOCS_KNOWLEDGE_UNSAFE_PATH' in src
        import inspect
        sys.path.insert(0, str(kern))
        import work_ledger_kernel as kmod
        print("KERNEL_EXPORTS", [x for x in dir(kmod) if not x.startswith("_")][:45])
        from work_ledger_kernel import kernel as kernel_module
        print("KERNEL_CLASSES", [(name,str(inspect.signature(getattr(kernel_module,name)))) for name in dir(kernel_module) if name in ("Kernel","WorkLedgerKernel")])
        from work_ledger_kernel.kernel import WorkLedgerKernel
        import hashlib
        ledger = WorkLedgerKernel(Path(tmp) / "ledger")
        target = Path(tmp) / "kernel-workspace"
        knowledge = target / "knowledge"
        knowledge.mkdir(parents=True)
        (knowledge / "README.md").write_text("# Individual knowledge index\n", encoding="utf-8")
        (knowledge / "case.md").write_text("Unpublished individual edits\n", encoding="utf-8")
        digest_before = {
            p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in knowledge.glob("*.md")
        }
        exported = ledger.work_docs_export(str(target), None)
        assert exported.get("ok") is not False, exported
        assert not any(name.startswith("knowledge/") for name in exported.get("changed_files", []))
        digest_after = {
            p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in knowledge.glob("*.md")
        }
        assert digest_before == digest_after, (digest_before, digest_after)
        root_readme = (target / "README.md").read_text(encoding="utf-8")
        assert "[Knowledge 탐색](knowledge/README.md)" in root_readme
        ledger.work_docs_export(str(target), None)
        assert digest_before == {
            p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in knowledge.glob("*.md")
        }
        print("KERNEL_EXPORTER_T01_T02_PASS", digest_after)
        # Functional SVG regression setup: inspect actual public API, not source tokens.
        import inspect
        from work_ledger_kernel import work_ux as ux_module
        print("KERNEL_EVIDENCE_APIS", [
            (n, str(inspect.signature(getattr(ledger, n))))
            for n in dir(ledger) if any(k in n for k in ("evidence", "artifact", "work_create", "work_add"))
            and callable(getattr(ledger, n))
        ])
        print("WORK_UX_CLASSES", [
            (n, str(inspect.signature(getattr(ux_module, n))))
            for n in dir(ux_module) if n in ("WorkUX", "export_docs")
        ])
        if hasattr(ux_module, "WorkUX"):
            print("WORK_UX_EXPORT_SIGNATURE", inspect.signature(ux_module.WorkUX.export_docs))
            code = inspect.getsource(ux_module.WorkUX.export_docs)
            lines = code.splitlines()
            for i, line in enumerate(lines):
                if any(k in line.lower() for k in ("evidence", "svg", "artifact", "work_id")):
                    print("WORK_UX_EXPORT_LINE", i + 1, line[:180])
        print("TARGETED_SMOKE_PASS (T01/T02, workflow/git local guards; hard OS gate still NOT_RUN)")


if __name__ == "__main__":
    smoke()
