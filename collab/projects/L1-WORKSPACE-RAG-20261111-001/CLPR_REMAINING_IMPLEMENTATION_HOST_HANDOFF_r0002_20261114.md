# CL/PR 이슈 분석 기존 5종 — 남은 최소 구현·통합 검증 원샷 인계 r0002

- Parent Work: `L1-WORKSPACE-RAG-20261111-001`
- Repo: PRIVATE `wonhwipark/CoWork-Skill-Collab`
- Branch: `main`
- Path: `collab/projects/L1-WORKSPACE-RAG-20261111-001/CLPR_REMAINING_IMPLEMENTATION_HOST_HANDOFF_r0002_20261114.md`
- Date: 2026-11-14 KST
- Authority: 사용자 '하나씩 이어서 끝까지 진행'에 따른 개발/격리시험 범위. 운영 소스/원장/DB·설치·Job·watcher/LIVE 변경과 새 유료 리뷰/REQUEST/READY는 무승인.
- 실제 결과: [GPT Python 3.10/3.11 후보 검증](GPT_CLPR_ISOLATED_PY310_PY311_VALIDATION_RESULT_r0001_20261114.md), [CI run 43598489441](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/43598489441)
- Original design disposition: [GPT CLPR 판정](GPT_CLPR_DESIGN_REVIEW_DISPOSITION_r0001_20261114.md)
- Baseline handoff: PUBLIC `wonhwipark/L1Work` `main` `handoffs/L1_CLPR_ISSUE_ANALYSIS_IMPLEMENTATION_AND_REGRESSION_ONESHOT_r0001_20261114.md`.
- **Current: DEVELOPMENT=PARTIAL_PATCHED / E2_SYNTHETIC_GROUPING_PASS / FULL_REGRESSION=NOT_COMPLETE / WORK_EVIDENCE_E2E=NOT_RUN / PUBLIC_RELEASE=BLOCKED_NOT_POSTED**.

## 이미 실행·확정된 부분 (재작업 금지)

PRIVATE `main`의 `collab/projects/L1-WORKSPACE-RAG-20261111-001/candidates/`:
1. `p4-code-owner_v0_6_9_1114.zip` SHA-256 `51363124aad349dd01f7e21f471bff4ae4d41d33d221ed9e4fb84e4217aab5ba`
2. `l1-github_v0_3_57_1114.zip` SHA-256 `f1b8fb43d3af427f2c5d52864051c65894f3cb45969ab35ca502f344735611ce`
3. `l1-fix-workflow_v1_6_68_1114.zip` SHA-256 `046b7968ff552d590a72c4e7ebb0a29df6760b5a6d07196f17f6eef09770e31a`
4. `code-analyzer_v0_15_3_1114.zip` SHA-256 `dbbd0f9fd4d5173b8f445aa2fabd9f7417593ecd996ac0e2f0ad10278f3626c2`
5. `work-ledger-kernel_v0_7_38_1114.zip` SHA-256 `6797f509d005377f9ba0d6312cc6cfb7017c7502cfcaab3ee61332c7f0a6e788`

5 ZIP 실제 바이트 hash/CRC/ZipSlip/symlink, 415개 Python parse Python 3.10.22 / 3.11.18 PASS. CLPR grouping/negative tests E2 PASS. 선택한 9 suite 중 7 PASS, Workflow 두 FAIL; 동일 두 FAIL은 원본 `v1.6.67`에서도 동일 재현하여 변경 유발 회귀로 간주하지 않음. **CI 전체 conclusion=failure 유지, SELF_TEST 전체 PASS 아님.** 원본·설치본 수정 금지.

## 남은 작업 A — Work/Evidence 최소 연결 (우선순위 P0)

- 현 `l1-fix-workflow` `clpr-issue-plan` 및 `plan_clpr_issue_cases()`는 읽기 전용이며 `workspace_written=false`, `provider_executed=false`.
- 실제 기존 Work를 먼저 조회: `lookup_clpr_existing_work()`. 다중 Work 매칭·미수집/미검증 ref·서로 다른 source scope 발견 시 자동 합병 또는 신규 Work 발급 금지.
- 기존 Kernel의 **실제 허용 API**(`work_reference_add`, `work_context_event`, 기존 Work doc/Artifact, 정규 `record_evidence` API) 사용 가능성만 코드/계약에서 확인. 임의 Kernel registry/schema/record.json/README/index, 가짜 provider/kind, `delivery` 슬롯 우회 금지.
- 안정적인 P4 `p4:<authority>:<number>`와 GitHub HTTPS PR ref를 중복 없이 보존. 추가·재실행/순서 변화에서 기존 Work ID·ref 재사용, 기록 중복 0 확인.
- **중요:** CLPR 그룹핑 '후보'를 원인 확정/분석 Evidence로 기록 금지. 실제 analyzer 결과/코드 anchor가 있을 때만 등록된 Evidence kind/stage/provider로 저장. Problem/RootCause/Fix/Verification/CurrentApplicability의 확인·추론·불명 상태 각각 독립.
- 합성 업무가 아닌 **격리 원장**에서 파일 해시, write→readback, 반복 입력 idempotency, 다중 Work conflict, 등록되지 않은 Evidence 조합 차단, exports/manifest 불변 검증. 실제 업무 Work 쓰기 별도 승인.

## 남은 작업 B — P4 과거 변경과 Code Analyzer 연결 (P0, 근거 기반)

- 허가된 Mango MCP의 실제 `describe/files/integration`, 파일별 `rev/from_rev` 입력 계약과 읽기 전용 증거를 우선 확인. 미확인 도구 이름·직접 `p4` CLI·`p4 sync` 임의 실행 금지.
- 과거 CL before/after 원문/스냅샷 미확보 시 `CODE_CONFIRMED` 차단하고 `INFERENCE`/UNKNOWN으로 보존. Snapshot은 실제 제공 계약·권한·필요성이 입증된 경우에만 최소 도입.
- PR merge commit/head/base/target 적용 분리, checkout/branch drift·dirty/untracked/missing object는 VERIFIED 금지. 동일 repo PR은 직렬 실행.
- 사내 코드·로그·상세 MSC/토큰은 GitHub PRIVATE에도 저장하지 않고, 소스 범위/회사 코드 분석은 인가된 실행 호스트 내부에서만.

## 남은 작업 C — 전체 회귀 및 배포 게이트

- PUBLIC 원본과 PRIVATE 후보 버전 drift를 확인 후 격리 복사본만 수정. 신규 버전 ZIP 별도 이름, SHA-256, bytes, ZIP CRC/ZipSlip/심링크, 실제 VERSION/manifest/skillsilent, 민감정보 점검.
- Python 3.10/3.11 실제 전체 관련 회귀와 C01~C12 부정시험; 기존 두 Workflow FAIL은 baseline vs candidate 판정 근거 유지, 필요한 범위 내에서만 별도 결함 수정.
- **실호스트 E3는 별개:** approved Mango MCP, merged PR 실제 target, 실제 Kernel Work/Evidence 저장·재조회·중복 Work 0, rollback 가능성. 인가 없으면 E3=NOT_RUN.
- 기존 Claude 설계 리뷰 `REPORTED_COMPLETE`; 새 패치 독립 리뷰는 `NOT_RUN`. 사용자 기존 지시에 따라 새 유료 리뷰/REQUEST/READY 생성 0. 실제 필요한 독립 리뷰 게이트는 거짓 PASS로 우회하지 않음.
- PUBLIC `wonhwipark/L1Work` `main` 루트에 최종 ZIP 게시하는 것은 **모든 배포 필수 게이트 PASS와 유효한 공개 승인 조건 충족 시에만**. 그 전 개발 후보는 PRIVATE에 보존하고 `PUBLIC_RELEASE=BLOCKED/NOT_POSTED`.

## 최종 결과 보고와 읽기 재검증

승인된 실제 범위까지 가능한 작업을 한 번에 수행하되, 접근 불가 항목만 `BLOCKED/NOT_RUN`으로 격리. 새 후보/테스트 근거/결함 수정·다시 검증한 결과를 PRIVATE `main`의 **새 결과 MD**에 PR 없이 직접 게시한 후 원격 재조회 및 실제 SHA-256/bytes/commit 확인. 같은 Work `CURRENT.md`와 `TRACKER.json`은 **기존 이력을 보존한 채** 최신 상태 갱신.

**NEXT_ONE_ACTION:** GitHub PRIVATE `main`의 본 r0002 인계와 기존 후보 5개를 기준으로, 코드/Kernel 허용 API에 접근 가능한 승인된 개발 실행 호스트에서 A→B→C 순서로 격리 최소 구현·회귀시험. 호스트·권한·정책에 막히면 그 항목만 `BLOCKED`; PUBLIC 또는 운영 변경으로 우회 금지.
