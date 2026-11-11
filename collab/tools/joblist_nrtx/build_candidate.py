#!/usr/bin/env python3
"""Build a non-deployable NR Tx Job-list candidate from the immutable public ZIP.

No internal code or site config is included. This script never publishes to the
public skill-update root, activates a Job, or runs any in-house skill.
"""
from __future__ import annotations
import copy
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

OLD = "0.4.34"
NEW = "0.4.35"
BASE_FILE = "job-list_v0_4_34_1109.zip"
OUT_FILE = "job-list_v0_4_35_1112.zip"
EXPECTED_GIT_BLOB = "13353c5db1d09752507b865fe3d4e5fc456f495c"
EXPECTED_SIZE = 1551031
JOB_ID = "JOB-20261112-NR-L1TX-KNOWLEDGE-MSC-01"
PROFILE = "nr-l1tx-knowledge-research-linux"
REQUEST = "requests/staged/one-shot-v0.4.35-nr-l1tx-knowledge-research.json"

def text_json(data: dict) -> bytes:
    return (json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf8")

def path_ok(name: str) -> None:
    p = Path(name)
    if name.startswith("/") or ".." in p.parts or "\\" in name or "\0" in name:
        raise ValueError("ZIP_PATH_TRAVERSAL")

def replace_one(src: bytes, old: bytes, new: bytes, label: str) -> bytes:
    if src.count(old) != 1:
        raise ValueError("PATCH_ANCHOR_AMBIGUOUS_" + label)
    return src.replace(old, new, 1)

def build(base: Path, tool_dir: Path, out_dir: Path) -> Path:
    binary = base.read_bytes()
    sha = hashlib.sha1(b"blob " + str(len(binary)).encode("ascii") + b"\0" + binary).hexdigest()
    if sha != EXPECTED_GIT_BLOB or len(binary) != EXPECTED_SIZE:
        raise ValueError("BASELINE_ZIP_BYTES_MISMATCH")
    with zipfile.ZipFile(base) as oldzip:
        if oldzip.testzip() is not None:
            raise ValueError("BASELINE_BAD_CRC")
        infos = oldzip.infolist()
        old_root = "job-list_v0_4_34/"
        new_root = "job-list_v0_4_35/"
        if not all(i.filename.startswith(old_root) for i in infos):
            raise ValueError("BASELINE_ROOT_INCONSISTENT")
        found = set()
        data = {}
        for info in infos:
            path_ok(info.filename)
            if info.filename in found:
                raise ValueError("BASELINE_DUPLICATE_PATH")
            found.add(info.filename)
            name = info.filename[len(old_root):]
            data[name] = oldzip.read(info.filename) if not info.is_dir() else b""

    assert data["VERSION"].decode("utf8").strip() == OLD
    assert json.loads(data["requests/one-shot-jobs.json"]) == {"schema_version": 1, "jobs": []}
    data["VERSION"] = (NEW + "\n").encode()
    release = json.loads(data[".skill-release.json"])
    assert release["name"] == "job-list" and release["version"] == OLD
    release["version"] = NEW
    release["revision"] = int(release["revision"]) + 1
    release["built_at"] = "2026-11-12"
    release["channel"] = "candidate"
    data[".skill-release.json"] = text_json(release)
    lifecycle = json.loads(data["lifecycle.json"])
    assert lifecycle["version"] == OLD
    lifecycle["version"] = NEW
    lifecycle["notes"].insert(0, "v0.4.35 STAGED NR L1 Tx Knowledge Updater research: one bounded Linux Profile and fixed four-scenario prompt; no active Job, no host install/Provider E2E/independent review, no group publication. Release only after separately verified host and deployment gates.")
    data["lifecycle.json"] = text_json(lifecycle)

    skill = data["SKILL.md"]
    skill = replace_one(skill, b"version: 0.4.34", b"version: 0.4.35", "SKILL_FRONTMATTER")
    intro = b"""# job-list v0.4.35 -- STAGED NR Tx knowledge research candidate

**DEVELOPMENT_NOT_FOR_DEPLOYMENT.** Zero active One-shot Jobs; no install or execution signal.
This staged package adds a Linux NR L1 Tx research profile targeting the existing
l1-knowledge-updater with code-analyzer and doc-converter. It cannot infer unapproved
skill entrypoints or publish shared technical knowledge. Review the on-host approval,
in-house provider wiring and Knowledge Updater contract before any promotion.

"""
    data["SKILL.md"] = skill.replace(b"# job-list v0.4.34", intro + b"# Historical v0.4.34", 1)
    pre = """# job-list v0.4.35 — NR L1 Tx four-scenario research candidate

Status: STAGED / DEVELOPMENT_NOT_FOR_DEPLOYMENT / zero active jobs.
Preserves existing v0.4.34 history and records. New fixed Linux Profile:
nr-l1tx-knowledge-research-linux. The staged request is NOT queued or runnable
until exact host/Updater/Code Analyzer/Doc Converter approval, reliable evidence
capture, independent review and public-release criteria are verified.
Investigation: Init RACH, UL SCell configure, activation, deactivation.
No automatic group knowledge publish, source modifications or external export.

"""
    data["README.md"] = pre.encode("utf8") + data["README.md"]
    for f in ("skillsilent/manifest.json", "skillsilent/contract.json"):
        d = json.loads(data[f])
        assert d.get("skill_version") == OLD
        d["skill_version"] = NEW
        data[f] = text_json(d)
    core = data["scripts/job_core.py"]
    core = replace_one(core, b'VERSION = "0.4.34"', b'VERSION = "0.4.35"', "CORE_VERSION")
    anchor = b"BUILTIN_SAFE_PROFILES: dict[str, dict[str, Any]] = {\n"
    profile = (
        b"    # v0.4.35 NR L1 Tx candidate: only the fixed Worker, no remote command/path/prompt params.\n"
        b'    "nr-l1tx-knowledge-research-linux": {\n'
        b'        "enabled": True, "skill": "job-list",\n'
        b'        "entrypoint": "scripts/nr_tx_knowledge_linux_job.py",\n'
        b'        "args": [], "timeout_sec": 11500, "retry": 0,\n'
        b'        "required_outputs": ["output/nr_tx_knowledge_research/latest_result.json"],\n'
        b'        "semantic_result_path": "output/nr_tx_knowledge_research/latest_result.json",\n'
        b'        "semantic_result_required": True, "env": {}, "parameters": {},\n'
        b'        "supersede_policy": {"enabled": False},\n'
        b'    },\n'
    )
    core = replace_one(core, anchor, anchor + profile, "PROFILE_INSERT")
    data["scripts/job_core.py"] = core
    # Retire exact-version assertions in the two baseline release tests; keep
    # their functional gates and all other checks unchanged.
    data["tests/test_v0434_dependency_gate.py"] = replace_one(
        data["tests/test_v0434_dependency_gate.py"],
        b".read_text().strip()=='0.4.34'", b".read_text().strip()=='0.4.35'", "TEST_RELEASE_VERSION")
    data["tests/test_v0431_knowledge_input_stage.py"] = replace_one(
        data["tests/test_v0431_knowledge_input_stage.py"],
        b"core.VERSION=='0.4.34'", b"core.VERSION=='0.4.35'", "TEST_CORE_VERSION")
    data["tests/test_v0435_nrtx_candidate.py"] = (
        tool_dir / "test_v0435_nrtx_candidate.py").read_bytes()

    for f in ("install.py",):
        if f in data:
            # Installer may include the exact current release label; never mass-
            # rewrite historical notes or bundled tests/fixtures.
            data[f] = data[f].replace(b'0.4.34', b'0.4.35')

    data[REQUEST] = text_json({
        "schema_version": 1,
        "jobs": [{
            "job_id": JOB_ID, "profile": PROFILE, "platform": "linux",
            "priority": 65, "expires_at": "2027-01-31T23:59:59+09:00",
            "params": {}
        }]
    })
    data["scripts/nr_tx_knowledge_linux_job.py"] = (tool_dir / "nr_tx_knowledge_linux_job.py").read_bytes()
    data["references/NR_TX_KNOWLEDGE_RESEARCH_ORCHESTRATION_v0435.md"] = (
        tool_dir / "NR_TX_KNOWLEDGE_RESEARCH_ORCHESTRATION_v0435.md").read_bytes()

    # Detect the original sha256sum format; use the canonical two-space style.
    old_manifest = data.get("PACKAGE_CONTENTS.sha256", b"").decode("utf8")
    records = [x for x in old_manifest.splitlines() if x.strip() and not x.startswith("#")]
    if not records or not re.fullmatch(r"[0-9a-f]{64}\s{1,2}[*]?\S.*", records[0]):
        raise ValueError("UNKNOWN_PACKAGE_SHA_MANIFEST_FORMAT")
    paths = sorted(x for x in data if x and not x.endswith("/") and x != "PACKAGE_CONTENTS.sha256")
    data["PACKAGE_CONTENTS.sha256"] = ("".join(
        hashlib.sha256(data[k]).hexdigest() + "  " + k + "\n" for k in paths)).encode("utf8")
    dest = out_dir / OUT_FILE
    dest.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(dest, "w") as z:
        for info in infos:
            rel = info.filename[len(old_root):]
            newinfo = copy.copy(info)
            newinfo.filename = new_root + rel
            z.writestr(newinfo, data[rel])
        added = sorted(set(data) - {i.filename[len(old_root):] for i in infos})
        for rel in added:
            newinfo = zipfile.ZipInfo(new_root + rel, (2026, 11, 12, 1, 0, 0))
            newinfo.compress_type = zipfile.ZIP_DEFLATED
            newinfo.external_attr = 0o100644 << 16
            z.writestr(newinfo, data[rel])
    verify(dest, data, old_root, new_root)
    return dest

def verify(zippath: Path, data: dict, oldroot: str, newroot: str) -> None:
    with zipfile.ZipFile(zippath) as z:
        assert z.testzip() is None
        names = z.namelist()
        assert len(names) == len(set(names))
        assert all(x.startswith(newroot) for x in names)
        for n in names:
            path_ok(n)
            p = n[len(newroot):]
            if not n.endswith("/"):
                assert z.read(n) == data[p], p
        assert json.loads(z.read(newroot + "requests/one-shot-jobs.json"))["jobs"] == []
        assert json.loads(z.read(newroot + REQUEST))["jobs"][0]["job_id"] == JOB_ID
        assert z.read(newroot + "VERSION") == (NEW + "\n").encode()
        assert z.read(newroot + "scripts/nr_tx_knowledge_linux_job.py").count(b"JOB-20261112") == 1
        # Every sha256sum path must be the exact package payload, not fabricated.
        manifest = z.read(newroot + "PACKAGE_CONTENTS.sha256").decode("utf8").splitlines()
        for rec in manifest:
            sha, rel = rec.split("  ", 1)
            assert hashlib.sha256(z.read(newroot + rel)).hexdigest() == sha, rel
        assert len(manifest) == sum(1 for p in data if p and not p.endswith("/") and p != "PACKAGE_CONTENTS.sha256")
        assert b"Job-list public" not in z.read(newroot + "references/NR_TX_KNOWLEDGE_RESEARCH_ORCHESTRATION_v0435.md")
    print("ZIP_CRC=PASS", "MANIFEST=PASS", "ACTIVE_JOBS=0",
          "VERSION=" + NEW, "PACKAGE_BYTES=" + str(zippath.stat().st_size),
          "PACKAGE_SHA256=" + hashlib.sha256(zippath.read_bytes()).hexdigest(), flush=True)

def main() -> None:
    repo = Path(__file__).resolve().parent
    base = Path(sys.argv[1]).resolve()
    out = Path(sys.argv[2]).resolve()
    target = build(base, repo, out)
    print("PACKAGE_CANDIDATE", target, flush=True)

if __name__ == "__main__":
    main()
