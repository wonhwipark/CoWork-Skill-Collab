# 사내 원샷 G0 — 코드리뷰·이슈리뷰 누적의 실제 설치/I-O 계약 검증 (READ ONLY)

- Created: 2026-11-11 KST
- Status: **READY_AS_MANUAL_HANDOFF / NOT_EXECUTED**
- Source GitHub PRIVATE: **`wonhwipark/CoWork-Skill-Collab`**
- Branch: **`main`**
- Exact relative path: **`collab/projects/L1-WORKSPACE-RAG-20261111-001/L1_REVIEW_ACCUMULATION_INHOUSE_G0_READONLY_HANDOFF_r0001_20261111.md`**
- Companion findings: **`collab/projects/L1-WORKSPACE-RAG-20261111-001/L1_REVIEW_ACCUMULATION_G0_PARTIAL_AUDIT_r0001_20261111.md`**
- Design baseline: **`collab/projects/L1-WORKSPACE-RAG-20261111-001/L1_REVIEW_ACCUMULATION_STEP2_SCHEMA_AND_TEST_r0001_20261111.md`**
- Security: 아래 지시는 사내 읽기 전용 진단만. GitHub PRIVATE 외부 협업에도 회사 코드/민감 데이터 게시 금지.
- **독립 Claude Code 리뷰 REQUEST가 아님.** `REQUEST/READY`·watcher/Job enqueue/paid provider call/운영 LIVE 상태 불변.

## Task — user one-shot execution (no intermediate approvals for read-only evidence)

당신은 권한 있는 사내 개발 도구 운영자로서 **실제 설치 상태/도구 계약을 읽기 전용으로 확인**한다. 외부 GPT가 확인하지 못한 E3 증거만 취합하고, 이미 증명된 static 계약은 반복 추론하지 않는다. 같은 장비의 기존 Work/소스/DB/운영설정·자동화·예약작업은 절대 변경하지 않는다.

### H01 — Kernel actual evidence registry and release

1. 실제 사용되는 Kernel/Workflow 코드와 등록된 실행 스킬/패키지 **설치 위치·버전·SHA-256·release_kind/channel/approval**을 읽어서 이전 공개 ZIP v0.7.37-dev.1과 구분한다. 설치되어 있지 않으면 `NOT_INSTALLED`. 스킬 설치/업데이트는 금지.
2. 실제 Kernel `registry_v1.json`의 `analyze` / `deliver` 슬롯에서 `code-analyzer`, `issue-analyzer`, `l1-github`, `p4-code-owner`의 stage/profile/provider/kind 지원을 확인. JSON schema와 실제 runtime validator의 추가 필드 처리 차이가 있는지 **코드를 읽어만 확인**한다.
3. 기존 `record.json`/evidence index, Journal, Work docs Export, Snapshot/Resume 및 실제 Work metadata에서 review session/finding 구현·기존 field 존재 여부 확인. 실 Work 생성·증거 기록·테스트로 수정 금지.
4. 등록 슬롯에 없는 `code_review`, `issue_review` 등 신규 kind를 운영 레지스트리에 추가하지 말 것. 누락은 `GAP`으로만 보고.

### H02 — Git PR review collection and analysis

1. `l1-github` 실제 설치 버전의 `pr-code-analysis` CLI/API 반환 필드, `pr_code_analysis_handoff.json` producer, exact base/head SHA/diff/source repo/root와 `code-analyzer git-pr-range` consumer 매핑을 정적 확인.
2. **PR review body**, **inline PR review comments**, **general issue comments**, **review verdict/approval/dismissed**, **thread resolution**, **edited/deleted events**를 수집할 실제 호스트 MCP tool/REST route가 등록돼 있는지 권한·schema·pagination 메타데이터만 확인. 인가된 메타데이터 조회가 가능하더라도 사용자 업무 데이터 원문을 불필요하게 수집하지 말고, 실제 콘텐츠 읽기 권한·완전성은 `NOT_RUN` 또는 `PARTIAL`로 표시.
3. 각 항목은 `AVAILABLE/UNAVAILABLE/NOT_VERIFIED`, tool/action signature, collection completeness 판단 근거, paging cursor/terminal, permission/URL authority, 변경 이벤트 포착 가능 여부, 원본 Work 변형 0을 기록.
4. `git status` 등 Optional Lock 및 index refresh 가능성이 있는 명령은 운영 source repo에서 무심코 호출하지 않는다. 필요한 SCM 읽기에는 `GIT_OPTIONAL_LOCKS=0`를 기본으로, `git rev-parse`/조회 명령만 승인된 scope에서 사용하고 `git fetch/checkout/switch/rebase/reset/push` 금지. dirty/untracked 미확인은 `UNKNOWN`으로 둔다.

### H03 — Code Analyzer runs, Evidence and MSC

1. 실제 설치 `code-analyzer`의 `git-pr-range`, `git-incremental`, `knowledge-link`, MSC analysis/export action과 output 스키마(§feature_summary.json§, §evidence_index.json§, §scenario_catalog.json§, 분석 Run/절차 evidence)를 **정적 source/fixture만**으로 확인.
2. `CODE_CONFIRMED`와 추론, `MSC_AS_IS/FOCUSED/CHANGE_IMPACT` 및 TO_BE 담당 분리, PR SHA/branch/worktree → SourceSnapshot, Evidence ID→Work ID→문서 목록, run-retention과 오래된 근거 링크 보존 계약 확인.
3. 대규모 소스 full scan, 실제 Provider/LLM 분석 실행, 자동 Job·Run retention apply는 하지 말 것. 소스 경로가 확인 안 되면 `NOT_VERIFIED`, 코드 원문은 사외 업로드 금지.

### H04 — Jira/Mango P4 read-only route

1. 현재 인가된 Jira/Mango MCP **tool ID와 I/O schema/capability existence**를 조회: Jira issue/comment pagination, P4 submitted describe/files, annotate -c/-I / integration source provenance.
2. `p4-code-owner jira-fix-cl-scan`의 `prepare/scan/finalize` 처리와 `jira_evidence.json`·`p4_evidence.json` 소비 경로를 설치된 실제 코드 기준으로 확인. 이 단계에서 Jira 이슈 실제 다운로드나 운영 CL 조회는 필수 아님.
3. source root/L1 include/exclude allowlist, P4 file#haveRev, `comments_complete`, `files_complete`, `origin_confirmed`, `PENDING` fail-closed 의미를 확인. `INCLUDED_L1`을 root cause·fix PASS·공식 owner로 승격하지 말 것.

### Security and zero-write preflight

- 운영 Work/DB(WAL/SHM 포함)/watcher/Bridge/Telegram/Job/사내 Git·GitHub PUBLIC/Dropbox LIVE 쓰기·동기화·유료 Provider 실행·MCP Action 실행·네트워크 API 데이터 export/스킬 설치/원본 ZIP 수정 **금지**.
- 회사 내부 실제 경로, 소스, commit과 제품 세부 구조, Jira/Mango IDs, 개인 정보, 고객 로그, 토큰/신뢰키, 상세 MSC 내용은 **사외 PRIVATE에도 게시하지 않음**.
- 가능하면 메타데이터용 진단은 기존 설치된 read-only 관리자 도구/정적 파일 조회로 수행. 도구 자체가 telemetry/cache/DB 수정 가능성이 있다면 실행하지 말고 `NOT_RUN`; 단순 read-only 주장만으로 안전하다고 가정하지 말 것.
- Windows/SSH Linux 혼합 가능성이 있으므로 호스트 OS/실행 경로는 추정하지 말 것. 운영 리포지토리의 Python package import/CLI test invocation도 부작용 검사 전 실행 금지.
- 실제 반출 가능 범위가 불확실하면 **게시하지 말고 사내 승인 위치에만 결과 보존**.

### Required internal result format

사내 승인된 **비운영 임시/문서 위치**에 `L1_REVIEW_ACCUMULATION_G0_HOST_INTERNAL.md` 작성:
- `HOST_OS/INSTALL_SOURCE/E3_EVIDENCE_REFERENCES` (내부 전용)
- `H01..H04`: PASS/PARTIAL/FAIL/NOT_RUN, installed package provenance, 실제 tool/action ID/schema, missing/blocked, raw evidence refs (내부 전용).
- `REGISTRY_MATRIX`: stage/profile/provider/kind 실측 vs 제안 리뷰 kind.
- `PR_REVIEW_COLLECTION`: reviews, inline/general comments, threads, dismissed/edited/deleted, pagination, completeness.
- `EVIDENCE_PROVENANCE`: PR SHA → Analyzer Run → Work Evidence → MSC, Jira comments → Fix CL → P4 origin.
- `NO_OPERATIONAL_WRITES`: 명령별 side effects 확인, 추정 대신 미확인을 그대로 표시.
- `IMPLEMENTATION_GAPS`: 최소 코드 변경 권고와 실제 재현 부정시험, `APPROVAL_REQUIRED`.

별도 `L1_REVIEW_ACCUMULATION_G0_NON_SENSITIVE_SUMMARY_FOR_GPT.md`를 작성할 수 있다면 **반출 승인된 추상 상태만** 담아라:
```text
TASK: L1-WORKSPACE-RAG-20261111-001
HOST_G0_STATUS: PASS | PARTIAL | BLOCKED | NOT_RUN
H01_KERNEL: ...
H02_GITHUB: ...
H03_ANALYZER: ...
H04_JIRA_P4: ...
REGISTERED_REVIEW_KIND: YES | NO | UNKNOWN
REAL_PR_COMMENT_INGESTION: YES | PARTIAL | NO | UNKNOWN
REVIEW_LEDGER_WRITER: EXISTS | NOT_FOUND | UNKNOWN
PROVIDER_RAG_M1: BLOCKED | NOT_RUN | VERIFIED_WITH_RECEIPT
OPERATING_WRITES: 0 | UNVERIFIED
BLOCKER_IDS: ...
MINIMAL_INTEGRATION_PLAN: ...
GITHUB_RESULT_POST: NOT_POSTED (기본; 게시 승인·보안 검증이 있을 때만 별도 실행)
```
영문 코드/제품 내부 상세·tool 이름/엔드포인트/조직·개인 식별자/원문은 비민감 요약에 넣지 않는다.

### Output and next action

- 실제 사내 읽기 전용 검사 **완료된 항목만** E3로, 나머지는 E0/E1/E2와 `NOT_RUN`으로 유지.
- 외부 GitHub PRIVATE 결과/영수증 게시 및 readback은 **별도 반출 권한이 명확히 확인된 경우만** 허용; 요청 문서 게시만으로 Claude 리뷰나 GPT 후속 호출은 발생하지 않는다.
- GPT 후속 입력은 **비민감 H01–H04 요약 상태**이며, 그때 최소 Review Ledger Connector 패치 범위·실제 G0 완료 여부를 판정한다.
