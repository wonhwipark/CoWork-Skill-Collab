# L1 Review Accumulation — G0 PARTIAL 사전검증 결과 r0001

- Date: 2026-11-11 (Asia/Seoul)
- Task: L1-WORKSPACE-RAG-20261111-001 / Review accumulation Step 3 (G0)
- **STATUS: G0_PARTIAL / HOST_REQUIRED / M1_BLOCKED**
- **REVIEW_KIND: GPT_STATIC_AND_ISOLATED_TEST** (Claude 독립 리뷰 아님)
- **DEVELOPMENT: NO_SOURCE_PATCH / NO_PACKAGE_BUILD**
- **INHOUSE_REMOTE_ACCESS: NOT_AVAILABLE** (사내 GitHub·Jira/Mango MCP·Windows 설치본 접근 못함)
- **OPERATING: MIGRATION_NOT_CUTOVER / DROPBOX_LIVE**
- **REQUEST_READY / WATCHER / JOB / PROVIDER / LIVE_CHANGE: 0**

## 1. 실제 읽은 근거 (E0/E1/E2/E3 구분)

- GitHub PRIVATE main의 \`CURRENT.md\`, \`L1_REVIEW_ACCUMULATION_SKILL_IO_CONTRACT_AUDIT_r0001_20261111.md\`, \`L1_REVIEW_ACCUMULATION_STEP2_SCHEMA_AND_TEST_r0001_20261111.md\`, RAG r0002 및 GPT_SELF_REVIEW.
- PUBLIC \`wonhwipark/L1Work\` main의 최신 검색된 ZIP: code-analyzer \`v0.15.2\` (513,811 B), p4-code-owner \`v0.6.7\` (106,017 B), l1-github \`v0.3.56\` (572,047 B), l1-fix-workflow \`v1.6.67\` (749,307 B), work-ledger-kernel \`v0.7.37\` (318,845 B), job-list \`v0.4.34\` (1,551,031 B). 공개 패키지 최신 목록이 사내 실제 설치본 목록은 아니다.
- 사용자가 첨부한 실제 \`work-ledger-kernel_v0_7_37_1103.zip\` = SHA-256 \`8cf53c9ba14aed97b9be7b00db39ca5458ba0127ba00b9a1eef3533aba3a06a5\`, 318,845 B. ZIP 내부 \`VERSION\`, \`.skill-release.json\`, \`skillsilent/manifest.json\`에 실제 \`0.7.37-dev.1\`, \`release_kind=development_validation_only\`, \`channel=development_not_for_deployment\`. **운영 설치 대상 승인 아님**.
- E2 실제 코드·계약: \`contracts/registry_v1.json\`, \`work_ledger_kernel/contracts/evidence.schema.json\`, \`record.schema.json\`, \`work_ledger_kernel/kernel.py::record_evidence()\`, \`validate_evidence_meta()\`, \`validate_record()\`. 임시 작업 디렉터리에서 분리 실행. 내부 회사 코드/계정·장비 데이터 사용 없음.
- E1 기존 PUBLIC 패키지 계약문서: l1-github PR base/head/diff/handoff, code-analyzer git-pr-range/git-incremental/evidence/MSC, p4-code-owner jira-fix-cl-scan and integration history. 사내 host/MCP tool ID/승인 릴리스는 E0.

## 2. H01: Kernel Evidence registry — E2 실 코드 확인 / E3 NOT_RUN

\`kernel.py::record_evidence\`는 실제 \`provider/kind/stage/profile\`을 registry slots와 대조하고 미등록 시 \`REGISTRY_MISMATCH\`를 반환한다. Evidence 파일은 Work ID 전용 위치에 사본/해시가 기록되고 \`record.json\`의 \`evidence_index\` 및 Journal을 갱신한다. 기존 \`index/active.json\`, \`latest.json\`과 Work README/문서안내는 파생 Export이므로 Review Ledger SSOT로 덮어쓰지 않는다.

### 확인된 등록 슬롯 (패키지 코드, 사내 host 등록 상태 아님)

| stage | provider | 허용 evidence_kind | profile |
|---|---|---|---|
| analyze | code-analyzer | \`asis_callflow\`, \`asis_msc\`, \`impact\`, \`structure_metric\`, \`behavior_delta_set\` | BUG, BUG-NR, FEATURE, REFACTOR, PERF, MAINT, TOOLING |
| analyze | issue-analyzer 또는 l1sw-dev-log-analyzer-plus | \`issue_analysis\`, \`repro_attempt\`, \`behavior_delta_set\` | BUG, BUG-NR |
| deliver | l1-github 또는 user | \`delivery\` | BUG, BUG-NR, FEATURE, REFACTOR, PERF, MAINT, TOOLING |
| utility | doc-converter | \`render_output\` | BUG, BUG-NR, FEATURE, REFACTOR, PERF, MAINT, TOOLING |

**미등록:** \`kind=code_review\`, \`kind=issue_review\`, \`provider=p4-code-owner\`. \`l1-github\`는 분석 stage provider가 아니며 \`deliver\` 슬롯 전용. **새 논리 \`review_kind\`와 Evidence \`kind\`는 다름.** 기존 \`asis_msc\` 등은 실제 code-analyzer 근거에만 연결하고, p4-code-owner 결과를 code-analyzer 명의로 위장하여 기록하지 않음.

### 직접 수행한 임시 Work 합성 시험

| Test | 실제 관측 | 판정 |
|---|---|---|
| G0-K01 code-analyzer/MAINT/analyze/asis_msc | Evidence 등록 | PASS |
| G0-K02 미등록 \`code_review\` kind | \`REGISTRY_MISMATCH\` | PASS (차단 확인) |
| G0-K03 미등록 \`issue_review\` kind | \`REGISTRY_MISMATCH\` | PASS |
| G0-K04 p4-code-owner provider direct | \`REGISTRY_MISMATCH\` | PASS |
| G0-K05 l1-github analyze provider | \`REGISTRY_MISMATCH\` | PASS |
| G0-K06 같은 \`evidence_id\` 재등록 | \`EVIDENCE_ID_EXISTS\` | PASS |

**6 PASS / 0 FAIL,** 임시 Ledger에는 성공한 synthetic Evidence 1개만 보존 후 임시 디렉터리 자동 폐기. 사내 운영 Ledger·MCP/Provider 호출 없음.

### 신규 발견: schema/runtime parity mismatch

- \`evidence.schema.json\`의 JSON Schema Draft 2020-12는 \`additionalProperties=false\`이다.
- 그러나 현재 런타임 \`validate_evidence_meta()\`는 필수 필드·digest 패턴·confidence 검사만 수행하고 unknown metadata field는 거부하지 않음.
- 추가 \`review_id\`가 포함된 synthetic Evidence metadata: **runtime validator ACCEPT**, 동일 metadata에 표준 \`jsonschema.validate\`: **REJECT** 확인.
- \`record_evidence\`는 자체적으로 허용 metadata를 생성하므로 이것을 임의 외부 \`review_id\` write 허용/승인으로 오해하면 안 됨. 정확한 schema 집행 경로·구버전 reader 호환을 검증할 필요.
- **권고:** 원장 record/evidence 객체에 리뷰 필드를 임의 추가하지 말고, 우선 기존 Evidence ID를 가리키는 비정본 \`ReviewSession/Finding\` 논리 연결 계약을 유지. 별도 writer·schema extension은 호스트 G0·회귀시험 후 별도 승인.

## 3. H02: GitHub PR review ingestion — E1 계약 확인 / E3 NOT_RUN

- \`l1-github pr-code-analysis\`: PR URL/번호 → base/head SHA, diff/stat/changed files, \`pr_code_analysis_handoff.json\`, PR head용 분석 worktree. 기존 사용자 worktree 변경 금지.
- \`code-analyzer git-pr-range\`: exact SHA+handoff → \`PR_RANGE_READY/UNAVAILABLE\`, \`semantic_workspace_ready\`, \`scope_handoff\`. \`COMMIT_OBJECT_MISSING\` 시 무작정 분석 성공 판정 금지.
- **PR review lifecycle/comment completeness**는 별도 확인 필요: Pull Request review objects (APPROVED/CHANGES_REQUESTED/DISMISSED 등), inline review comments, issue-style general comments, discussion threads, edited/deleted/dismissed events, pagination·권한·ETag/관측 시점.
- \`pr_history.md\`는 Git commit 재작성 가이드이고 리뷰 코멘트 수집기가 아님. 현재 참조 계약만으로 전체 GitHub PR review history 수집 PASS는 불가.
- **G0 host output:** tool ID/transport/schema/API scope/권한/누락·페이지 종결 판단, source PR exact SHA, \`review_collection=COMPLETE|PARTIAL|UNAVAILABLE\` (다른 수집 경로 구분).

## 4. H03: Code Analyzer artifact / MSC — E1 계약 확인 / E3 NOT_RUN

- 이미 문서화된 feature output: \`feature_summary.json\` (\`code-analyzer/feature-analysis/v1\`), \`evidence_index.json\` 항목 \`id/type/file/line_start/line_end/symbol/relation\`, \`scenario_catalog.json\` (\`code-analyzer/scenario-catalog/v1\`).
- MSC \`AS_IS/FOCUSED/CHANGE_IMPACT\`는 코드 사실 파생 표현이며 \`CODE_CONFIRMED\`와 추론 분리. \`TO_BE_USER_APPROVED\`는 code-analyzer 소유 아님.
- \`git-incremental\`의 \`NO_CHANGE/INCREMENTAL_READY/FULL_ANALYSIS_REQUIRED\`와 run-retention 정책 존재. 문서에 있는 action 존재가 사내 실행 가능 확인은 아님.
- **G0 host output:** 실제 installed run output schema, run_id 및 code_rev/source scope identity, Evidence anchor→Work ID 매핑, Run compact 후 영구 링크 정합성, 이전 CODE_ANALYSIS-only Work exporter 빈 문서 반례. 기업 코드/MSC 본문은 외부 전송 금지.

## 5. H04: Jira/P4 evidence — E1 계약 확인 / E3 NOT_RUN

- \`p4-code-owner jira-fix-cl-scan\`은 \`prepare → scan → finalize\` 단계. 해당 스크립트 자체는 Jira/P4 서버에 접속하지 않고 **실제 사내 Agent가 권한 있는 Jira/Mango read-only MCP**로 \`jira_evidence.json\`, \`p4_evidence.json\`을 수집해야 함.
- 필수 필드: \`comments_complete\` (모든 댓글 pagination), \`changes[].submitted/files_complete/origin_confirmed/source_cls[]\`, 실제 L1 depot allowlist. 결과 \`INCLUDED_L1/EXCLUDED_NON_L1/PENDING\`.
- \`INCLUDED_L1\`은 실제 L1 SW 코드 수정 관련성 선별이지 Root Cause·버그 해결 PASS·공식 조직 Owner/개인 책임 증거가 아니다.
- **G0 host output:** 승인된 실제 Jira/Mango tool ID, 접근 가능 여부, 댓글/CL completeness 및 integration provenance 처리, P4 haveRev/file#rev 출처; 미확인은 PENDING.

## 6. 현 단계 결함 판정과 최소 보완 결정

| ID | Severity | 내용 | 조치 |
|---|---|---|---|
| G0-B01 | BLOCKING for code/host rollout | 실제 설치본 버전·해시·release approval 및 사내 tool 권한 E3 없음 | 호스트 격리 G0 없이 구현/운영 PASS 금지 |
| G0-B02 | BLOCKING for review persistence | 신규 review kinds/providers가 기존 Kernel 슬롯에 등록되지 않음 | 무승인 registry 수정·provider 가장 금지; 기존 Evidence Ref 기반 connector 설계 |
| G0-M01 | MAJOR | Evidence JSON Schema와 runtime validator의 extra-field 처리 불일치 | 데이터 계약/쓰기 경계·회귀시험 확정 |
| G0-M02 | MAJOR | PR comment/review/dismissal의 실제 전체 수집 API 불명 | 실 tool 목록·pagination 확인 전 COMPLETE 금지 |
| G0-M03 | MAJOR | Analyzer Run-retention 후 Review Finding Evidence 링크 무결성 미검증 | 영구 ID+hash 기반 Reference; 실제 호스트 리드백 시험 |
| G0-M04 | MAJOR | Jira/P4 실제 scope/권한·원본 이력 미확인 | 실제 MCP·source scope 승인 후 읽기 전용 검사 |
| G0-M05 | MAJOR | Kernel 패키지 개발 후보 \`0.7.37-dev.1\`의 운영 사용 오인 가능 | 정식 설치·승인본과 구분, \`F-VERS-01\` fail-closed 유지 |

## 7. 실제 시험과 남은 시험의 경계

- §DONE:§ 로컬 E2 코드/manifest/source schema 검사, 격리 합성 등록 6 PASS, schema/runtime parity 재현, PUBLIC ZIP 목록 read-only 확인, GitHub PRIVATE 설계/상태 검증.
- §NOT_RUN:§ 사내 Kernel/Workflow/Analyzer/GitHub/P4 installed version·MCP/PR/CL/Jira E2E, Windows host, 운영 Work ID, 실제 RAG Provider 호출/본문 소비, Project script patch, ZIP build, 독립 Claude 리뷰.
- §M1 STATUS: BLOCKED§. 기존 7대 security/owner/root/job/version/digest gates 모두 유지.

## 8. 다음 한 동작

동봉된 별도 파일 \`L1_REVIEW_ACCUMULATION_INHOUSE_G0_READONLY_HANDOFF_r0001_20261111.md\`의 정확한 repo/main/path를 사내 접근 권한이 있는 Windows Claude Code/사내 Agent에 전달해 **H01–H04 읽기 전용** 실제 설치/인터페이스 인벤토리를 수집한다. 인가되지 않은 데이터를 GitHub PRIVATE에도 반출하지 말고, 증거 없는 항목은 \`NOT_RUN/UNKNOWN\`으로 남긴다.

\`CURRENT.md\`에 이 부분 완료와 호스트 차단·원격 게시/재조회 실측 상태를 기록한다.
