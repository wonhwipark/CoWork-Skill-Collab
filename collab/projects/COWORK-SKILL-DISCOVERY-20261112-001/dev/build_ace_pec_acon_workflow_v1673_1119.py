#!/usr/bin/env python3
"""Deterministic ACE/PEC/ACON read-only bridge in the existing Workflow.

Development candidate ONLY. No source/host installation, publishing or writer
changes. Reuses the pinned MSC dual-entry v1.6.72 builder and its safety checks.
"""
from __future__ import annotations
import argparse
import compileall
import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
DEV = REPO / "collab/projects/L1-WORKSPACE-RAG-20261111-001/dev"
PROJECT = Path(__file__).resolve().parent
sys.path.insert(0, str(DEV))
from build_l1_knowledge_guard_candidates_r0001_20261117 import (
    safe_unzip, refresh_package_metadata)
from msc_dual_entry_candidate import patch_workflow, verify_workflow
from reproducible_zip import rezip
from skill_release_quality_gate import validate as release_validate

VERSION = "1.6.73"
ARCHIVE = "l1-fix-workflow_v1_6_73_1119.zip"
BASE = REPO / "collab/projects/L1-WORKSPACE-RAG-20261111-001/candidates/l1-fix-workflow_v1_6_70_1117.zip"
BASE_SHA256 = "1e08302b6a533d2894101427f5a7bb94b43102e00a98f2c6e0b19f534a885ceb"
HELPER = PROJECT / "ace_pec_acon_readonly.py"
TESTS = PROJECT / "test_ace_pec_acon_readonly.py"


def digest(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def test_actual_packaged_helper(packaged: Path) -> int:
    """Run the existing 19 synthetic contract tests against extracted package."""
    if digest(packaged) != digest(HELPER):
        raise RuntimeError("BRIDGE_SOURCE_DIGEST_MISMATCH")
    name = "ace_pec_acon_readonly"
    prior = sys.modules.pop(name, None)
    try:
        spec = importlib.util.spec_from_file_location(name, packaged)
        if not spec or not spec.loader:
            raise RuntimeError("BRIDGE_IMPORT_NOT_AVAILABLE")
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        test_spec = importlib.util.spec_from_file_location("ace_pec_acon_candidate_tests", TESTS)
        if not test_spec or not test_spec.loader:
            raise RuntimeError("TEST_MODULE_NOT_AVAILABLE")
        test_module = importlib.util.module_from_spec(test_spec)
        test_spec.loader.exec_module(test_module)
        suite = unittest.defaultTestLoader.loadTestsFromModule(test_module)
        result = unittest.TextTestRunner(verbosity=1).run(suite)
        if not result.wasSuccessful() or result.testsRun < 20:
            raise RuntimeError("READONLY_BRIDGE_CONTRACT_TEST_FAILED")
        return result.testsRun
    finally:
        sys.modules.pop(name, None)
        if prior is not None:
            sys.modules[name] = prior


def build(output: Path) -> dict:
    if digest(BASE) != BASE_SHA256:
        raise RuntimeError("WORKFLOW_BASE_PIN_MISMATCH")
    if not HELPER.is_file() or not TESTS.is_file():
        raise RuntimeError("BRIDGE_OR_TEST_SOURCE_MISSING")
    output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="acepec-verified-dev-") as tmp:
        extracted = Path(tmp) / "expanded"
        extracted.mkdir()
        safe_unzip(BASE, extracted)
        root = extracted / "l1-fix-workflow"
        if not (root / "SKILL.md").is_file():
            raise RuntimeError("WORKFLOW_PACKAGE_ROOT_MISSING")
        # Preserve previously built v1.6.72 MSC opt-in functionality.
        patch_workflow(root)
        msc = verify_workflow(root)
        # The new module is data-only: no changes to Kernel, Git or Work writers.
        dest = root / "l1_fix_workflow" / "ace_pec_acon_readonly.py"
        if dest.exists():
            raise RuntimeError("BRIDGE_PATH_COLLISION")
        dest.write_bytes(HELPER.read_bytes())
        doc = root / "SKILL.md"
        doc.write_text(doc.read_text(encoding="utf-8") +
            "\n\n### ACE·PEC-HOP·ACON 읽기 전용 파생 판정(개발 후보 1.6.73)\n"
            "- 기존 Work/Kernel Evidence의 검증된 출력만 인자로 전달. 새 스킬/Agent, DB, watcher, 자동 분석, 모델 호출, 지식 쓰기 또는 무단 Git publish를 시작하지 않음.\n"
            "- `l1_fix_workflow.ace_pec_acon_readonly`의 `ace_decision_candidate`, `pec_verify_excerpt`, `acon_compare_existing_results`는 순수 데이터 계산이며 **실제 승인/Writer/호스트 설치 증빙이 아님**.\n"
            "- ACE 원문 순서·유효 승인 근거가 없으면 HOLD. PEC 원본 raw byte offset/length 또는 source SHA 미확인이면 HOLD. ACON은 기존 고정 baseline/compressed 결과만 비교.\n"
            "- Knowledge Updater는 업무 전용 스킬로 기존 계약/권한을 보존하며 코드 반출 요구 없음. 릴리스 전 실설치/G0·독립 코드 검증 필요.\n",
            encoding="utf-8", newline="\n")
        refresh_package_metadata(root, dict(
            version_from="1.6.72", version_to=VERSION, output=ARCHIVE))
        if not compileall.compile_dir(root, quiet=1):
            raise RuntimeError("PACKAGE_PYTHON_COMPILE_FAILED")
        n = test_actual_packaged_helper(dest)
        target = output / ARCHIVE
        rezip(extracted, target)
        gate = release_validate(target, VERSION)
        record = {"status": "DEVELOPMENT_ONLY", "archive": ARCHIVE,
            "size_bytes": target.stat().st_size, "sha256": digest(target),
            "based_on": "workflow 1.6.70 + MSC 1.6.72",
            "actual_packaged_module_test_count": n, "msc_existing_contract": msc,
            "release_gate": gate, "channel": "development_not_for_deployment",
            "independent_code_review": "NOT_RUN",
            "business_host_g0": "NOT_RUN", "public_release": "BLOCKED"}
        (output / "ACE_PEC_ACON_DEV_BUILD_RESULT.json").write_text(
            json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
            encoding="utf-8")
        print("ACE_PEC_ACON_PACKAGED_WORKFLOW_DEVELOPMENT_PASS")
        print(json.dumps(record, ensure_ascii=False, sort_keys=True))
        return record


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()
    build(args.out)
