# GPT 실행 결과 — 릴리스 무결성·Kernel 실행 회귀·스킬 간 계약 게이트 r0001

- 일자: 2026-11-17 KST
- 기존 Work: `L1-WORKSPACE-RAG-20261111-001`
- 사용자 요청 범위: 이전 제안 1번(릴리스 무결성·Kernel 회귀시험), 2번(스킬 간 계약 검사 최소 보완) **구현·실제 시험·PRIVATE 정본 게시**. 신규 기능/registry 엔진, 운영 호스트 설정, 추가 독립 리뷰, LIVE/Knowledge write 제외.
- 결과: **GATE_CODE=POSTED_MAIN_VERIFIED / TARGETED_FUNCTIONAL_TEST=PASS / MAIN_CI=PASS / PUBLIC_NEW_RELEASE=NOT_RUN_GATE_BLOCKED**. 개발자 자체검증과 독립 리뷰를 혼동하지 않음.

## 1. 수정 내용

| 범위 | 수정 및 동작 |
|---|---|
| 릴리스 manifest | 빌더 `dev/build_l1_knowledge_guard_candidates_r0001_20261117.py`가 실제 ZIP 포함 파일의 전 집합을 기준으로 `MANIFEST_SHA256.json` 및 `PACKAGE_CONTENTS.sha256` 자동 재생성. 이전 manifest 항목만 재해시하던 누락 허용 제거 |
| 버전 메타 | `VERSION`, `SKILL.md` 상단 버전(따옴표 형식 포함), `VERSION.md`, `.skill-release.json`, `.skill-main.json`, `skillsilent/manifest.json`의 패키지 버전 선언 동기화·검증. 이력 텍스트와 skillsilent 자체 도구 버전은 변경하지 않음 |
| 릴리스 품질 검사 | `dev/skill_release_quality_gate.py`: ZIP CRC, 중복·경로 이탈·symlink, 버전 불일치, manifest 누락/미등재·해시 오류를 실패 처리. 사전 검증 실패 시 빌더 예외로 후보 ZIP 배송 단계 중단 |
| Kernel 실행 회귀 | `dev/test_kernel_export_svg_evidence.py`: 실제 `WorkLedgerKernel.work_create`, 등록된 Evidence slot, `work_docs_export`를 사용. MSC SVG 게시·SHA/경로·재실행, 대용량 SVG 코드 차단, 비 MSC SVG 무시 및 기존 MD export를 검증. 문자열 존재 검사로 PASS 대체 금지 |
| 스킬 간 계약 | `collab/ops/CONTRACTS/MSC_SKILL_IO_MATRIX_V1.json`: Workflow=VERIFIED_SCENARIO_IR, Updater=VERIFIED_SEMANTIC_SPEC, 양 경로의 산출물 MSC_HTML; RAW PUML 직접 소스로 승인 금지, 라이프사이클 자동 진전 금지. 기존 소유권 체계 보존 |
| 정책 도달성 | `dev/msc_skill_contract_gate.py`: `doc-converter`의 두 관리 액션(`msc-package`, `msc-scenario-build`)에 `--view-mode`가 실행 코드와 패키지된 `skillsilent/policy.json`에 함께 있는지 검사. 정책이 없는 OpenCode 직접 실행 패키지는 `NOT_APPLICABLE_DIRECT_OPENCODE`로 구분; 운영 정책·allowlist를 새로 변경하거나 강제하지 않음 |
| CI | `.github/workflows/cowork-skill-release-quality.yml` 추가(읽기 전용). 정적 단어 검색이 아닌 합성 실패 사례와 실제 Kernel export, 공개 doc-converter 배포본을 검사. `main`에서 새 candidate ZIP 커밋 시 manifest/version 게이트 실시. 기존 개발 branch CI에도 빌드 전용 게이트 연결. 자동 PUBLIC publisher 자체의 설치·변경을 의미하지 않음 |

## 2. 실제 시험·근거

- **PRIVATE main CI: PASS**, [run 43984576507](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/43984576507), source commit `814fa7b7aba91bcde8f783d06e489f6408a03ca2`. 릴리스/계약 negative case **13/13 PASS**. 실제 Kernel 등록 Evidence를 가진 Work export **3/3 PASS**: `KERNEL_SVG_EVIDENCE_EXPORT_HASH_IDEMPOTENT_PASS`, `KERNEL_MSC_SVG_SIZE_FAIL_CLOSED_PASS`, `KERNEL_UNRELATED_SVG_NO_REGRESSION_PASS`.
- **개발 후보 빌드 CI: PASS**, [run 43984284554](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/43984284554). Workflow/Git 보호 기능 테스트, Kernel 개인 Knowledge SHA 보존 T01/T02, 버전/manifest 전집합 검증 및 ZIP CRC/경로/중복 PASS. 마침표 없는 메타 헤더·따옴표 YAML·내장 skillsilent 패키지 버전 불일치를 실제 검사에서 차단한 후 빌더 수정·재시험 PASS.
- 공개 `doc-converter_v0_2_26_1117.zip` **169204 B, SHA-256 `b0ebd0aa4d771adc30648ab2bce23a3c1648e408984bedb36d0e3da45108312c`**. PRIVATE CI에서 실제 PUBLIC 다운로드와 해시 재검증, VERSION=0.2.26, manifest 89개/ZIP 90개 전체 coverage PASS; 두 관리 액션 `--view-mode` 정책·코드 도달성 PASS.
- 새 candidate ZIP을 변경하는 **이번 main commit은 없으므로 `CHANGED_CANDIDATE_CHECKED=0`**. 해당 CI 검사 경로는 설치본 또는 미래 게시 결과를 PASS로 소급하지 않음.
- 새 독립 Windows Claude Code R1=**NOT_RUN**. CI는 GPT 개발·시험이며 기존 승인 대기 리뷰/영수증을 재호출·대체하지 않음.

## 3. 개발 후보 ZIP (PUBLIC 미게시)

PRIVATE `dev/l1-knowledge-guards-20261117`의 `collab/projects/L1-WORKSPACE-RAG-20261111-001/dev/output/`에서 고정 원본으로 재생성, `BUILD_RESULT.json` 확인:

| 파일 | 바이트 | SHA-256 |
|---|---:|---|
| `l1-fix-workflow_v1_6_70_1117.zip` | 758119 | `c9187ee6f8d0cdba8fe3fdae0f072f6c16d83323083b798d30937d7692999017` |
| `l1-github_v0_3_59_1117.zip` | 567266 | `6351b96bcb984f6388fd195cc579a60fa809fac6e14caab0c0c860e2d30b7cf6` |
| `work-ledger-kernel_v0_7_43_1117.zip` | 319792 | `0efb8a83b5bb219ffe1f53c04fe6a179b9359cb5ce0c96fe302b56ffc78146e3` |

모두 `development_not_for_deployment`. 이 릴리스 품질 검증 PASS는 기존 Knowledge Guard 3종의 독립 코드 리뷰, 하드 OS/credential 보호 G0, 그룹 writer CAS, 업무 호스트 E3를 자동 PASS로 전환하지 않음. **PUBLIC `wonhwipark/L1Work/main`에 3개 신규 ZIP 게시하지 않음.**

## 4. 미확인/차단 및 다음 한 행동

- `TARGETED_RELEASE_QA=PASS`, `MAIN_CI=PASS`, `KERNEL_SVG_EVIDENCE_FUNCTIONAL_REGRESSION=PASS`, `MANAGED_VIEW_MODE_POLICY_STATIC=PASS`.
- `REAL_SKILLSILENT_RUNNER=NOT_RUN` (현 OpenCode 직접 실행에는 강제 불필요), `HOST_INSTALL=NOT_VERIFIED`, `BUSINESS_E2E=NOT_RUN`, `INDEPENDENT_CODE_REVIEW=NOT_RUN`, `KNOWLEDGE_GUARDS_PUBLIC_RELEASE=BLOCKED_NOT_POSTED`.
- 다음 한 동작: 기존 Knowledge Guard 코드 R1 결과/영수증 및 업무 환경 G0 검증 여부를 **기존 Work**에서 확인. 승인된 게이트 충족 전까지 개발 후보를 PUBLIC 또는 호스트 설치본으로 승격하지 않음.

이번 실행은 사용자 1·2 범위의 코드·시험·정본 반영 완료이며, 3번 실사용 파일럿(TD-003)은 별도 기존 Work에서 유지.
