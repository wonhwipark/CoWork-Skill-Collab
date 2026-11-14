# CL/PR 기존 스킬 5종 — 격리 Python 3.10/3.11 검증 결과 r0001

- 작업: `L1-WORKSPACE-RAG-20261111-001` / CLPR 단계별 재개
- 기준: 2026-11-14 KST
- 사용자 지시: 중단된 작업을 하나씩 이어서 가능한 범위 끝까지 진행
- 범위: PRIVATE에 이미 존재하는 5종 수정 후보 ZIP의 정확한 바이트를 별도 GitHub Actions branch에서 회귀. 업무 호스트/회사 소스/운영 원장 접근 없음.
- 소스: `wonhwipark/CoWork-Skill-Collab` PRIVATE `main` `collab/projects/L1-WORKSPACE-RAG-20261111-001/candidates/`
- 검증 브랜치: `clpr-validation-20261114`, workflow `.github/workflows/clpr-isolated-validation.yml`
- 최종 검증 커밋: `9083a14befc4654a33813d05f79a321023822713`
- 증거: [GitHub Actions run 43598489441](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/43598489441) / jobs Python 3.10 `132457975817`, Python 3.11 `132457976044`
- **운영 상태: MIGRATION_NOT_CUTOVER. 기존 watcher/DB/WAL/Job/Skill-Updater/Knowledge/실무 Work/설치본 수정 0. 추가 Claude 리뷰/REQUEST/READY/모델 유료 호출 0.**

## 1. 실제 검증 사실

| 검증 항목 | Python 3.10.22 | Python 3.11.18 |
|---|---|---|
| PRIVATE 기존 5종 ZIP 바이트 수/고정 SHA-256 | PASS (5/5) | PASS (5/5) |
| ZIP CRC/경로 이탈/심링크 부정 검사 | PASS (5/5) | PASS (5/5) |
| ZIP 내 `.py` 415개 `compile()` 구문 검사 | PASS | PASS |
| CL-only/P4 안전성 단위시험 2개 suite | PASS 2/2 | PASS 2/2 |
| GitHub PR/병합 단위시험 2개 suite | PASS 2/2 | PASS 2/2 |
| Analyzer share 출력 단위시험 1개 suite | PASS 1/1 | PASS 1/1 |
| Kernel multi-work/core 단위시험 2개 suite | PASS 2/2 | PASS 2/2 |
| Workflow issue brief/core 단위시험 2개 suite | **FAIL 2/2** | **FAIL 2/2** |
| CL/PR 그룹핑·Jira 분리·UNLINKED·중복/비정상 입력 차단 합성 E2 | PASS | PASS |

실제 검증 패키지(기존 공개 ZIP 덮어쓰기 없음):
- `p4-code-owner_v0_6_9_1114.zip` — 152175 B / SHA-256 `51363124aad349dd01f7e21f471bff4ae4d41d33d221ed9e4fb84e4217aab5ba`
- `l1-github_v0_3_57_1114.zip` — 602555 B / SHA-256 `f1b8fb43d3af427f2c5d52864051c65894f3cb45969ab35ca502f344735611ce`
- `l1-fix-workflow_v1_6_68_1114.zip` — 859398 B / SHA-256 `046b7968ff552d590a72c4e7ebb0a29df6760b5a6d07196f17f6eef09770e31a`
- `code-analyzer_v0_15_3_1114.zip` — 574469 B / SHA-256 `dbbd0f9fd4d5173b8f445aa2fabd9f7417593ecd996ac0e2f0ad10278f3626c2`
- `work-ledger-kernel_v0_7_38_1114.zip` — 409318 B / SHA-256 `6797f509d005377f9ba0d6312cc6cfb7017c7502cfcaab3ee61332c7f0a6e788`

## 2. Workflow 실패의 기준선 비교

검증 환경은 원래 누락된 모듈 PYTHONPATH, Kernel 형제 폴더 배치를 보정했다. 보정 전 환경 실패는 스킬 결함으로 판정하지 않는다.

보정 후에도 **수정 후보 Workflow v1.6.68**에 두 단위시험 실패가 재현되었다:
1. `test_tl_issue_brief_v1611.py::test_provider_output_distinguishes_current_execution`: `'wrong match' not found` (표시 문구 불일치).
2. `test_workflow.py::test_gs10_resume_uses_ledger`: `WORK_NOT_FOUND` vs 예상 `RESUME`.

정확한 **PUBLIC 원본 Workflow v1.6.67** ZIP SHA-256 `a3c5f055845a0711692afea5b09c0e53e93dfba89adc792c0f2e73385899b30a`도 다운받아 동일 두 suite/동일 후보 Kernel 테스트 환경으로 실행했으며 Python 3.10/3.11에서 **동일 두 실패를 재현**했다. 이번 CLPR 패치 유발 회귀라는 근거는 없지만 기존 FAIL이 있으므로 **FULL_REGRESSION=PASS로 선언하지 않는다**. 원인·수정은 별도 최소 범위 판정이 필요하다.

워크플로 CI 전체 결과 `failure`는 위 기존 실패를 의도적으로 숨기지 않고 수집한 결과다. 7개 suite PASS는 전체 회귀 PASS가 아니다.

## 3. CLPR 합성 E2의 한계

- `plan_clpr_issue_cases`에 합성 P4 CL 2건+PR 1건을 입력, 공통 Jira만 후보 그룹, 근거 없는 변경은 UNLINKED.
- 서로 다른 Jira 키를 가진 변경을 자동 합병하지 않음.
- 중복 P4 입력·비 HTTPS PR 입력을 거부.
- 반환에서 `workspace_written=false`, `provider_executed=false`, `knowledge_published=false` 확인.
- **실제 Work/Evidence create/write/readback=NOT_RUN**, 이 기능은 `clpr-issue-plan`의 설계상 읽기 전용 단계 밖이며 후속 연결이 아직 미구현.
- P4 historical per-file before/after snapshot, 실 Mango MCP, Git target remote, branch drift, 코드 인과/원인 확정, E3 업무 호스트, 사용자 Work 중복 write 0 등은 미검증.

## 4. GPT 판정 / release gate

- `DEVELOPMENT=PARTIAL_PATCHED` (기존 5종 후보 보존, 이번 작업에서 후보 소스 추가 수정 없음)
- `STATIC_SOURCE_AND_ZIP=PASS` (5종, 415 Python 소스; 검증된 범위만)
- `TARGETED_SELF_TEST=PARTIAL_7_PASS_2_BASELINE_FAIL_PER_PYTHON`
- `CLPR_SYNTHETIC_E2=PASS`
- `FULL_REGRESSION=FAIL/NOT_COMPLETE`
- `WORKSPACE_E3=NOT_RUN`, `P4_HISTORICAL_SNAPSHOT=NOT_IMPLEMENTED_VERIFIED`, `WORK_EVIDENCE_WRITE_READBACK=NOT_IMPLEMENTED_VERIFIED`
- `POST_PATCH_INDEPENDENT_REVIEW=NOT_RUN` (새 리뷰 요청 없음)
- `SECURITY_FULL_SCAN/HOST_ROLLBACK=NOT_RUN`
- `PUBLIC_RELEASE=BLOCKED/NOT_POSTED` — 기존 PRIVATE 개발 후보를 PUBLIC 전달 ZIP으로 간주하지 않음.
- `HOST_SKILL_UPDATER/KNOWLEDGE/LIVE=NOT_RUN`.

## 5. 다음 최소 작업 / 중단 게이트

1. **기존 두 Workflow FAIL을 신규 코드 결함으로 소급하지 않고** 수정 필요성·기존 기능 영향 판단. 별도 범위 확대 없이 기존 baseline과 비교하며 회귀 관리.
2. 기존 Kernel의 `work_reference_add` / `work_context_event` / 등록된 `record_evidence` 등 **허용 API를 통한 Work 연결만** 검토; CLPR 후보 자체를 가짜 분석 Evidence로 저장 금지. 기존 Work 조회/재개·참조 중복 방지/다중 Work 충돌 차단을 먼저 완성하고 합성 write/readback 시험.
3. P4 historical snapshot은 실제 허가된 Mango MCP 제공 계약과 rev/역사 자료 확보 여부부터 확인. 미지원이면 INFERENCE/NOT_VERIFIED, 무인가 CLI 호출 금지.
4. 최종 배포 전 C01~C12 확대 회귀, 민감정보·호환·롤백 및 승인된 업무 호스트 E3 별도 수행. 필수 게이트 미충족이면 PRIVATE development 후보만 보존.
5. 추가 유료 독립 리뷰·PUBLIC root 게시·LIVE 전환 등 별도 게이트를 무단 수행하지 않음.

**NEXT_ONE_ACTION:** PRIVATE `main`의 위 5종 원본 후보 ZIP을 유지하고, 기존 Work/Evidence 허용 API·입력 I/O를 기준으로 직렬 저장 연결 및 중복 방지에 한정한 소규모 격리 구현·시험을 실시할 수 있는 실행 호스트에서 진행. 업무 호스트/E3는 적법한 접근권·실행 근거 없이 PASS로 보고하지 않음.
