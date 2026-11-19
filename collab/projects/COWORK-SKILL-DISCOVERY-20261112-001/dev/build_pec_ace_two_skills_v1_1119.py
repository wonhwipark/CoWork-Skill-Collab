#!/usr/bin/env python3
"""Reproducible PEC Code Analyzer and ACE Workflow two-skill development ZIPs.

Use ONLY published non-sensitive source ZIPs pinned to exact hashes.
Never install or publish to L1Work: a separate release gate is required.
"""
from __future__ import annotations
import argparse
import ast
import compileall
import hashlib
import importlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
DEV = REPO / "collab/projects/L1-WORKSPACE-RAG-20261111-001/dev"
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(DEV))
from build_l1_knowledge_guard_candidates_r0001_20261117 import safe_unzip, refresh_package_metadata
from msc_dual_entry_candidate import patch_workflow, verify_workflow
from reproducible_zip import rezip
from skill_release_quality_gate import validate as release_validate

CAND = REPO / "collab/projects/L1-WORKSPACE-RAG-20261111-001/candidates"
SPEC = (
    ("code-analyzer", "0.15.3", "0.15.4", "code-analyzer_v0_15_3_1114.zip",
     "code-analyzer_v0_15_4_1119.zip",
     "dbbd0f9fd4d5173b8f445aa2fabd9f7417593ecd996ac0e2f0ad10278f3626c2"),
    ("l1-fix-workflow", "1.6.70", "1.6.74", "l1-fix-workflow_v1_6_70_1117.zip",
     "l1-fix-workflow_v1_6_74_1119.zip",
     "1e08302b6a533d2894101427f5a7bb94b43102e00a98f2c6e0b19f534a885ceb"),
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_exact(path: Path, before: str, after: str):
    body = path.read_text(encoding="utf-8")
    if body.count(before) != 1:
        raise RuntimeError(f"ANCHOR_NOT_UNIQUE:{path.name}: {body.count(before)} {before[:50]}")
    path.write_text(body.replace(before, after), encoding="utf-8", newline="\n")


def patch_analyzer(root: Path):
    src = HERE / "pec_hop_excerpt_readonly.py"
    dest = root / "scripts/ca_core/pec_hop_excerpt_readonly.py"
    if dest.exists():
        raise RuntimeError("PEC_MODULE_ALREADY_EXISTS")
    dest.write_bytes(src.read_bytes())
    validator = root / "scripts/ca_core/reuse_validator.py"
    replace_exact(validator, "def validate(manifest, resolution, requested_baseline=None):",
                  "def validate(manifest, resolution, requested_baseline=None, pec_claims=None):")
    replace_exact(validator,
        '    return {\n        "schema": "code-analyzer/reuse-result/v1",',
        '    result = {\n        "schema": "code-analyzer/reuse-result/v1",')
    replace_exact(validator, '        "rn": rn,\n    }\n\ndef main(argv=None):',
        '        "rn": rn,\n    }\n'
        '    # Explicit opt-in; existing reuse consumers and output are unchanged.\n'
        '    if pec_claims is not None:\n'
        '        try:\n'
        '            from .pec_hop_excerpt_readonly import verify_batch\n'
        '        except ImportError:\n'
        '            from pec_hop_excerpt_readonly import verify_batch\n'
        '        result["pec_excerpt_integrity"] = verify_batch(pec_claims)\n'
        '    return result\n\ndef main(argv=None):')
    skill = root / "SKILL.md"
    skill.write_text(skill.read_text(encoding="utf-8") +
        "\n\n### PEC-HOP 기존 Evidence 검증 — read-only 선택 기능 (개발 후보 0.15.4)\n"
        "- `ca_core.reuse_validator.validate(..., pec_claims=[...])`: 호출자가 승인된 원본 byte와 source SHA, revision, byte offset/length 및 발췌 byte를 **업무 환경 안에서** 전달할 때만 PEC 검증 결과를 기존 reuse-result의 선택적 `pec_excerpt_integrity`에 추가.\n"
        "- 기존 기본 validate 호출·재사용 판정은 변경 없음; 접근/원문/구간 증명 없으면 HOLD, 바이트 변조는 FAIL. 원본 출처와 접근권은 신뢰된 producer가 별도 검증해야 함.\n"
        "- 업무 자료 외부 전송, 파일 읽기/쓰기, Git/P4 실행, 근거 재분석, 그룹 Knowledge 쓰기 없음. 실제 현장 사용은 기존 도구 호출부의 권한·인자 연결 검증 후만 가능.\n",
        encoding="utf-8", newline="\n")


def patch_workflow_ace(root: Path):
    patch_workflow(root)  # Preserve existing v1.6.72 MSC opt-in.
    dest = root / "l1_fix_workflow/ace_resume_readonly.py"
    if dest.exists():
        raise RuntimeError("ACE_MODULE_ALREADY_EXISTS")
    dest.write_bytes((HERE / "ace_resume_readonly.py").read_bytes())
    target = root / "l1_fix_workflow/work_inspection.py"
    s = target.read_text(encoding="utf-8")
    tree = ast.parse(s)
    node = next((n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                 and n.name == "inspect_work"), None)
    if node is None:
        raise RuntimeError("INSPECT_WORK_NOT_FOUND")
    returns = [n for n in node.body if isinstance(n, ast.Return)]
    if len(returns) != 1 or not isinstance(returns[0].value, ast.Name) or returns[0].value.id != "data":
        raise RuntimeError("INSPECT_WORK_FINAL_RETURN_CHANGED")
    pos = returns[0].lineno - 1
    lines = s.splitlines(keepends=True)
    additional = (
        '    # Optional read-only ACE decision candidate; never turn it into approval.\n'
        '    if request.get("ace_scope") is not None or request.get("ace_subject") is not None:\n'
        '        from .ace_resume_readonly import select_latest_candidate\n'
        '        raw_decisions = actual if isinstance(actual, list) else []\n'
        '        data["ace_latest_decision_candidate"] = select_latest_candidate(\n'
        '            raw_decisions, work_id=wid,\n'
        '            scope=str(request.get("ace_scope") or ""),\n'
        '            subject=str(request.get("ace_subject") or ""))\n'
    )
    lines.insert(pos, additional)
    target.write_text("".join(lines), encoding="utf-8", newline="\n")
    skill = root / "SKILL.md"
    skill.write_text(skill.read_text(encoding="utf-8") +
        "\n\n### ACE 기존 Work 최신 결정 판정 — read-only 선택 기능 (개발 후보 1.6.74)\n"
        "- 기존 `l1_fix_workflow.work_inspection.inspect_work(..., request)`에서 명시적으로 `ace_scope` 및 `ace_subject`가 요청된 경우만 기존 진단 원문 결정의 검증된 출처·승인·append-index를 확인하여 `ace_latest_decision_candidate`를 파생 결과로 표시.\n"
        "- 원문 결정의 scope/권한/순서가 누락되면 HOLD. 요약 decisions와 Work mtime으로 승인·최신 결론을 추측하지 않음. 기존 조회, Kernel journal/Writer/Knowledge, Job 실행 및 기본 결과는 변경하지 않음.\n"
        "- 업무 Linux 검증·원문/권한 확인은 업무 환경 안에서만 수행. 이 함수는 기존 결정 사용의 참고 후보이며 실제 승인/작업 재실행 트리거가 아님.\n",
        encoding="utf-8", newline="\n")


def run(out: Path) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    result = {}
    with tempfile.TemporaryDirectory(prefix="pec-ace-minimal-") as tmp:
        for name, old, new, src, dest, expected in SPEC:
            archive = CAND / src
            if digest(archive) != expected:
                raise RuntimeError(f"PIN_MISMATCH:{src}:got={digest(archive)}")
            expanded = Path(tmp) / name
            expanded.mkdir()
            safe_unzip(archive, expanded)
            root = expanded / name
            if not (root / "SKILL.md").is_file():
                raise RuntimeError(f"SKILL_ROOT_NOT_FOUND:{name}")
            if name == "code-analyzer":
                patch_analyzer(root)
            else:
                patch_workflow_ace(root)
            refresh_package_metadata(root, {"version_from": old, "version_to": new, "output": dest})
            if not compileall.compile_dir(root, quiet=1):
                raise RuntimeError(f"PACKAGE_COMPILE_FAIL:{name}")
            # Import actual extracted modules in a deliberately synthetic test.
            suite = Path(__file__).with_name("test_pec_ace_two_skill_integration_r0001.py")
            sys.path.insert(0, str(root / "scripts" if name == "code-analyzer" else root))
            try:
                if name == "code-analyzer":
                    for key in list(sys.modules):
                        if key.startswith("ca_core"):
                            del sys.modules[key]
                else:
                    for key in list(sys.modules):
                        if key.startswith("l1_fix_workflow"):
                            del sys.modules[key]
                # Test module is imported only after the relevant extracted root is available.
                test_case = importlib.import_module(suite.stem)
                cases = test_case.run_package_contract(name, root)
            finally:
                sys.path.remove(str(root / "scripts" if name == "code-analyzer" else root))
            path = out / dest
            rezip(expanded, path)
            quality = release_validate(path, new)
            result[name] = {"archive": dest, "sha256": digest(path),
                            "size_bytes": path.stat().st_size,
                            "tests": cases, "package_quality": quality,
                            "channel": "development_not_for_deployment",
                            "independent_code_review": "NOT_RUN",
                            "business_host": "NOT_EXTERNALLY_OBSERVABLE",
                            "public_release": "NOT_POSTED"}
    (out / "PEC_ACE_TWO_SKILL_DEV_BUILD_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8")
    print("PEC_ACE_TWO_SKILL_DEV_BUILD_SUCCESS")
    print(json.dumps(result, sort_keys=True, ensure_ascii=False))
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    ns = parser.parse_args()
    run(ns.out)
