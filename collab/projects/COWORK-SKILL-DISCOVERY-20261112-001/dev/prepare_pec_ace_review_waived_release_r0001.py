#!/usr/bin/env python3
"""Build scoped public-release payloads only after non-review gates succeed.

Explicit USER waiver 2026-11-19 is restricted to independent code review for
two skill packages. This script does NOT publish, install, invoke a model or
access any business-host resources. Every other mandatory check stays active.
"""
from __future__ import annotations
import argparse
import compileall
import hashlib
import json
import re
import sys
import tempfile
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
DEV = REPO / "collab/projects/L1-WORKSPACE-RAG-20261111-001/dev"
sys.path.insert(0, str(DEV))
sys.path.insert(0, str(HERE))
from build_pec_ace_two_skills_v1_1119 import run as build_development
from build_pec_ace_two_skills_v1_1119 import verify_preservation, SPEC
from build_l1_knowledge_guard_candidates_r0001_20261117 import safe_unzip
from reproducible_zip import rezip
from skill_release_quality_gate import validate as quality_gate

SKILLS = {
  "code-analyzer": {
    "version": "0.15.4", "archive": "code-analyzer_v0_15_4_1119.zip",
    "changed_title": "### PEC-HOP 기존 Evidence 검증 — read-only 선택 기능 (개발 후보 0.15.4)",
    "release_title": "### PEC-HOP 기존 Evidence 검증 — read-only 선택 기능 (사용자 승인 배포 0.15.4)"
  },
  "l1-fix-workflow": {
    "version": "1.6.74", "archive": "l1-fix-workflow_v1_6_74_1119.zip",
    "changed_title": "### ACE 기존 Work 최신 결정 판정 — read-only 선택 기능 (개발 후보 1.6.74)",
    "release_title": "### ACE 기존 Work 최신 결정 판정 — read-only 선택 기능 (사용자 승인 배포 1.6.74)"
  }
}
HASH_FILES = ("MANIFEST_SHA256.json", "PACKAGE_CONTENTS.sha256")
DANGER_NAMES = re.compile(
    r"(?:^|/)(?:\.env|id_rsa|id_ed25519|\.p4tickets|\.netrc|"
    r"credentials\.json|secrets\.json)(?:$|/)|\.(?:pem|p12|pfx|jks|sqlite|db-wal|db-shm)$", re.I)
DANGER_BYTES = re.compile(
    rb"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"
    rb"|\bghp_[A-Za-z0-9]{30,}"
    rb"|\bgithub_pat_[A-Za-z0-9_]{30,}"
    rb"|\bAKIA[0-9A-Z]{16}"
    rb"|\bxox[baprs]-[A-Za-z0-9-]{24,}")
BINARY_NESTED = re.compile(r"\.(?:zip|7z|rar|p12|pfx|tar|gz)$", re.I)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def refresh_hashes(root: Path):
    """Recompute the installed archive's actual complete file universe."""
    paths = sorted(
        p.relative_to(root).as_posix() for p in root.rglob("*")
        if p.is_file() and p.name not in HASH_FILES
        and "__pycache__" not in p.relative_to(root).parts
        and p.suffix != ".pyc"
        and p.relative_to(root).parts[0] != "artifacts"
    )
    if not paths:
        raise RuntimeError("EMPTY_RELEASE_HASH_UNIVERSE")
    mapping = {rel: sha(root / rel) for rel in paths}
    found = 0
    if (root / "MANIFEST_SHA256.json").is_file():
        (root / "MANIFEST_SHA256.json").write_text(
            json.dumps(mapping, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
            encoding="utf-8", newline="\n")
        found += 1
    if (root / "PACKAGE_CONTENTS.sha256").is_file():
        (root / "PACKAGE_CONTENTS.sha256").write_text(
            "".join(f"{mapping[rel]}  {rel}\n" for rel in paths),
            encoding="utf-8", newline="\n")
        found += 1
    if not found:
        raise RuntimeError("RELEASE_MANIFEST_MISSING")
    return len(paths)


def scan_release(root: Path):
    """Blocking high-confidence public secret/archive safety scan."""
    inspected=0
    for p in root.rglob("*"):
        if not p.is_file() or "__pycache__" in p.parts or p.suffix == ".pyc":
            continue
        rel=p.relative_to(root).as_posix()
        if DANGER_NAMES.search(rel) or BINARY_NESTED.search(rel):
            raise RuntimeError("PUBLIC_BLOCKED_SUSPICIOUS_FILE:"+rel)
        raw=p.read_bytes()
        if DANGER_BYTES.search(raw):
            raise RuntimeError("PUBLIC_BLOCKED_CREDENTIAL_PATTERN:"+rel)
        inspected += 1
    return inspected


def check_only_expected_relabel(development: Path, final: Path, skill: str):
    with zipfile.ZipFile(development) as za, zipfile.ZipFile(final) as zb:
        old = {n:za.read(n) for n in za.namelist()}
        new = {n:zb.read(n) for n in zb.namelist()}
    if set(old)!=set(new):
        raise RuntimeError("RELEASE_MEMBER_UNIVERSE_CHANGED:"+skill)
    allowed={"SKILL.md", ".skill-release.json", *HASH_FILES}
    changed={n.split("/",1)[1] for n in old if old[n]!=new[n]}
    if not changed or not changed <= allowed:
        raise RuntimeError("RELEASE_UNEXPECTED_CODE_CHANGE:"+skill+":"+repr(sorted(changed)))
    return sorted(changed)


def run_release(out: Path):
    out.mkdir(parents=True, exist_ok=True)
    record={"review":"SKIPPED_BY_USER_REQUEST_2026_11_19",
            "waiver_scope":"PEC_CODE_ANALYZER_AND_ACE_WORKFLOW_ONLY",
            "no_export":"ENFORCED_IN_DESIGN_NOT_HOST_VERIFIED",
            "host_install":"NOT_RUN",
            "skills":{}}
    with tempfile.TemporaryDirectory(prefix="pec-ace-release-") as temp:
        root=Path(temp)
        dev=root / "development"
        built=build_development(dev)
        for skill, spec in SKILLS.items():
            src=dev/spec["archive"]
            entry=built[skill]
            if entry.get("tests",{}).get("status")!="PASS" or entry.get("source_preservation",{}).get("status")!="PASS":
                raise RuntimeError("NON_REVIEW_DEVELOPMENT_GATE_FAILED:"+skill)
            if sha(src)!=entry["sha256"]:
                raise RuntimeError("DEVELOPMENT_PIN_CHANGED:"+skill)
            expanded=root/(skill+"-public-release")
            expanded.mkdir()
            safe_unzip(src,expanded)
            pkg=expanded/skill
            relpath=pkg/".skill-release.json"
            meta=json.loads(relpath.read_text(encoding="utf-8"))
            if meta.get("channel")!="development_not_for_deployment":
                raise RuntimeError("EXPECTED_DEVELOPMENT_CHANNEL_MISSING:"+skill)
            meta["channel"]="public_release"
            meta["release_kind"]="user_explicit_delivery_with_independent_review_waived"
            meta["independent_code_review"]="SKIPPED_BY_USER_REQUEST"
            meta["release_date"]="2026-11-19"
            meta["built_at"]="2026-11-19T20:03:00+09:00"
            meta["waiver_scope"]="PEC_CODE_ANALYZER_AND_ACE_WORKFLOW_ONLY"
            meta["archive"]=spec["archive"]
            relpath.write_text(json.dumps(meta,sort_keys=True,indent=2,ensure_ascii=False)+"\n",
                               encoding="utf-8",newline="\n")
            sk=pkg/"SKILL.md"
            old=sk.read_text(encoding="utf-8")
            if old.count(spec["changed_title"])!=1:
                raise RuntimeError("RELEASE_DOC_TITLE_ANCHOR_INVALID:"+skill)
            new=old.replace(spec["changed_title"],spec["release_title"])
            new += ("\n\n**PUBLIC 전달 범위(2026-11-19)**: 사용자 명시 지시로 독립 코드 리뷰 생략 "
                    "(NOT_RUN/USER_WAIVED). 나머지 소스 pin·CRC·해시·기존 소스 보존·합성 회귀 "
                    "검증은 별도 기록. 업무 Linux 설치/실제 Work·Evidence E2E는 현장 책임이며 "
                    "외부로 코드·로그·시험 결과를 회신하지 않음. 자동 활성화·권한 승격을 승인하는 "
                    "조항은 아님.\n")
            sk.write_text(new,encoding="utf-8",newline="\n")
            security_count=scan_release(pkg)
            hash_count=refresh_hashes(pkg)
            if not compileall.compile_dir(pkg,quiet=1):
                raise RuntimeError("RELEASE_PY_COMPILE_FAILED:"+skill)
            target=out/spec["archive"]
            rezip(expanded,target)
            release_quality=quality_gate(target,spec["version"])
            changed=check_only_expected_relabel(src,target,skill)
            if release_quality["status"]!="PASS" or release_quality["covered"]!=hash_count:
                raise RuntimeError("FULL_FINAL_RELEASE_GATE_FAILED:"+skill)
            with zipfile.ZipFile(target) as z:
                root_meta=json.loads(z.read(skill+"/.skill-release.json"))
                if (root_meta.get("channel")!="public_release"
                    or root_meta.get("independent_code_review")!="SKIPPED_BY_USER_REQUEST"):
                    raise RuntimeError("RELEASE_WAIVER_METADATA_INVALID")
            record["skills"][skill]={
                "archive":target.name,"sha256":sha(target),"size_bytes":target.stat().st_size,
                "quality":release_quality,"source_preservation":entry["source_preservation"],
                "packaged_synthetic_tests":entry["tests"],
                "security_scanned_files":security_count,
                "allowed_release_relabels":changed,
                "independent_code_review":"SKIPPED_BY_USER_REQUEST",
                "release_channel":"public_release",
                "public_posted":"NOT_YET"}
    (out/"PEC_ACE_REVIEW_WAIVED_RELEASE_RESULT.json").write_text(
        json.dumps(record,indent=2,sort_keys=True,ensure_ascii=False)+"\n",
        encoding="utf-8",newline="\n")
    print("TWO_SKILLS_USER_REVIEW_WAIVED_RELEASE_NON_REVIEW_GATES_PASS")
    print(json.dumps(record,sort_keys=True,ensure_ascii=False))
    return record


if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",type=Path,required=True)
    args=ap.parse_args()
    run_release(args.out)
