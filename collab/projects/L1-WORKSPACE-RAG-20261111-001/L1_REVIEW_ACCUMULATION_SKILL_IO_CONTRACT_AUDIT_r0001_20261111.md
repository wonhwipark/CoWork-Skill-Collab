# L1 리뷰 누적 — 기존 스킬 실제 I/O 계약 인벤토리 (Step 1, r0001)

- 작성일: 2026-11-11 KST
- Workstream: L1-WORKSPACE-RAG-20261111-001
- Status: `STEP1_STATIC_CONTRACT_REVIEW_COMPLETE / HOST_E2E_NOT_VERIFIED`
- 판정: `REUSE_EXISTING_ANALYSIS + ADD_REVIEW_LEDGER_CONNECTOR` (구현/설치 승인 아님)
- Reviewed scope: Git·P4 코드리뷰 / Jira 이슈 수정 이력 / Work Evidence·지식 축적 연결의 **현행 계약만** 확인
- 운영: `MIGRATION_NOT_CUTOVER / DROPBOX_LIVE` 유지. 기존 스킬 ZIP/호스트/DB/MCP/REQUEST/READY/운영 상태 변경 없음.
- 용어: `DOC_VERIFIED`=공개 패키지 내부 문서·템플릿 실제 열람, `IMPLEMENTATION_UNVERIFIED`=Python 구현 상세 및 동작을 이 세션에서 통합 실행/입출력 실측하지 못함, `HOST_NOT_VERIFIED`=사내 설치·MCP 접근 없음.

## 1. 실제 열람 근거 및 버전 고정

PUBLIC `wonhwipark/L1Work`의 `main`에 존재하는 아래 3개 ZIP 및 해당 Markdown/JSON **ZIP 내부 파일을 압축 해제하여 읽음**. ZIP Git blob SHA는 파일 확인 식별용이며 해당 패키지의 설치 승인·런타임 해시와 동일하지 않다.

| 스킬/ZIP | Git blob SHA | 이 회차 실제 확인한 내부 계약 |
|---|---|---|
| `code-analyzer_v0_15_2_1107.zip` | `6017f81f51e9747286825648599fc13770cb8903` | `references/git_pr_range.md`, `git_incremental.md`, `knowledge_link.md`, `code_analyzer_msc_contract.md`, `feature_analysis_schema.md`, `run_retention.md`, `l1_responsibility_gate.md` |
| `p4-code-owner_v0_6_7_1012.zip` | `ee5801e2d8021a54d224f18d321002a3f1742716` | `references/jira_fix_cl_postmortem.md`, `integration_history_rules.md`, `move_history_rules.md`, `templates/jira_fix_cl_evidence.example.json`, `jira_l1_scope.example.json`, `p4_history_report.md` |
| `l1-github_v0_3_56_1110.zip` | `47f76743a6ca7ce20ecaaf943ef5aa634a77f66d` | `references/pr_code_analysis.md`, `file_history.md`, `pr_history.md`, `repo_role_and_push_guard.md` |

컨텍스트: PUBLIC `l1-fix-workflow_v1_6_67_1110.zip`, `work-ledger-kernel_v0_7_37_1103.zip`는 앞선 r0002 GPT 구조 리뷰에서 별도 다루었음. 이 회차의 세 스킬은 **사내 설치 상태가 아님**. 특정 소스 `scripts/*.py`의 전체 실행 호출/런타임 반환 실측은 `NOT_RUN`; 정적 계약 문서의 내용만으로 기능 E2E PASS를 주장하지 않는다.

## 2. Git PR 리뷰 I/O 계약: l1-github → code-analyzer

### 2.1 l1-github `pr-code-analysis`

**실제로 문서화된 입력:**
- PR URL (host/repo/PR 전체 보존) 또는 PR 번호
- provider로 조회한 **정확한** `base_sha` / `head_sha`; 수동 입력의 SHA도 검증 대상
- Git repo/worktree, 선택적 skillsilent/code-analyzer 존재 여부

**실제로 문서화된 동작/출력:**
- PR 메타데이터, base/head SHA, `merge-base(base, head)..head`의 diff/stat/changed files
- `pr_code_analysis_handoff.json` handoff
- PR head와 분리된 임시 detached 분석 worktree 필요 시 생성/재사용; 현재 사용자 worktree 전환·commit·push 금지
- JSON `analysis_mode=standalone-l1-github | code-analyzer-enhanced`
- `code_analyzer_handoff.required=false`로 enhanced analyzer가 없어도 standalone 분석 준비 가능

**인터페이스 예:** `py scripts/l1_github.py pr-code-analysis --pr <PR_URL> --json`. 정확한 반환 JSON 전체 필드·comment pagination·승인 상태 수집은 **추가 코드/호스트 검증 필요**.

### 2.2 code-analyzer `git-pr-range`

**입력:** `--code-root`, `--handoff <pr_code_analysis_handoff.json>`, 또는 `--pr N --base <full_sha> --head <full_sha>`; optional skillsilent 런타임 경로.

**출력/상태 계약:**
- `PR_RANGE_READY`: merge-base..head 범위의 변경 파일·hunk 계산
- `PR_RANGE_UNAVAILABLE` 또는 `COMMIT_OBJECT_MISSING`: 정확한 SHA이지만 로컬 object 없음
- `semantic_workspace_ready=true|false`: code-root HEAD가 PR head와 일치할 때만 semantic scope 즉시 사용 가능; 불일치 시 분석 workspace 준비 책임은 l1-github
- `scope_handoff`: code-analyzer의 변경 파일 의미분석 범위 전달

Git checkout/fetch/rebase 수행 책임은 code-analyzer가 아님. 통합은 `l1-github` metadata/diff → `code-analyzer` semantic scope 순서가 안전하다. **새 PR-diff parser 도입 불필요**.

### 2.3 code-analyzer 증분 코드 분석

**입력:** `git-incremental --code-root <root> [--base <prior_commit>] --json`, 기본 caller/callee depth 1.

**출력:**
- `NO_CHANGE` → `next_action=SKIP_ANALYSIS`; 단 pending/skipped procedure가 있으면 SKIP 금지
- `INCREMENTAL_READY` → `changed_files[]`, `affected_procedures[]`, `unresolved_ranges[]`, `next_action`
- `FULL_ANALYSIS_REQUIRED` → baseline 누락/비선조/예산 초과/diff 오류 등
- `affected_procedures[]`의 entry-line 추정 범위는 `APPROX_ENTRY_LINE`로 표시; 실제 AST 증거 아님

기본 출력은 analyzer 전용 run별 `git_incremental_plan.json`. 이 Run과 Work ID의 **영속 링크**는 별도 리뷰 누적 어댑터가 필요. Run 유지/삭제 정책이 존재하므로 지식 정본은 단순 `<run_id>` 파일 경로만 의존하면 안 됨.

### 2.4 코드·MSC 근거 계약

- code-analyzer가 소유하는 것은 `AS_IS`, `FOCUSED`, `CHANGE_IMPACT`의 코드 중심 MSC와 code-confirmed procedure facts.
- `TO_BE_USER_APPROVED` 승인 상태는 code-analyzer가 생성·소유하지 않음.
- 각 MSC step은 가능한 경우 `file / symbol / line or stable anchor / call(API, message) / evidence state` 연결.
- Feature Analysis 예시 JSON: `schema=code-analyzer/feature-analysis/v1`, `feature`, `code_root`, `focus[]`, `enablement`, `scope{files/classes/symbols/modules}`, `main_scenarios[]`, `main_deltas`, `open_questions[]`, `limitations[]`, `evidence_refs[]`.
- `evidence_index.json` 항목 기본 `id,type,file,line_start,line_end,symbol,relation`.
- `scenario_catalog.json`의 최소 `id,name,trigger,participants,steps,evidence_refs,confidence`.
- `knowledge-link-register`는 **주소 등록**이며 검색/본문 읽기/Provider 실제 RAG 입력 소비가 아님. `REGISTERED`와 `PROVIDER_ACCESS_NOT_VERIFIED` 구분 필수.

**리뷰 누적 결론:** code-analyzer의 근거와 MSC는 리뷰 Finding의 Evidence로 연결하되, 분석 Run 완료/코드 사실 ≠ 리뷰 승인 또는 Knowledge 승격.

## 3. P4 Jira 이슈 리뷰 I/O 계약: p4-code-owner

### 3.1 `jira-fix-cl-scan` 3단계

**입력:** 사용자 제공 Jira Issue Key가 포함된 Markdown 파일과 명시적 L1 depot file allowlist. 허용된 Jira MCP가 이슈 Summary/Description/**모든 페이지 댓글**을 실제 조회, Mango MCP가 Perforce CL `describe -s` 및 integration provenance를 읽음.

**중요 경계:** 로컬 `jira-fix-cl-scan` Python 스크립트는 Markdown/증거 JSON의 parsing·CL 후보 선별·보고서 생성만 처리. **Jira/P4 서버 조회는 Agent가 실제 노출된 읽기 전용 MCP tool로 수행해야 하며 스크립트가 직접 접근하지 않음.** 임의 CLI P4 호출·툴명 하드코딩 금지.

| Stage | 명시된 입력 | 주요 출력/판정 |
|---|---|---|
| `prepare` | `--stage prepare --input <file>` | `jira_requests.json`, `run_manifest.json`, `run_id` |
| `scan` | 실제 `jira_evidence.json` + `--stage scan --run-id <id>` | `cl_candidates.json`, `p4_requests.json`; 역할 `FIX_CANDIDATE / INTEGRATION_CANDIDATE / REVERT_CANDIDATE / REFERENCE_ONLY / UNKNOWN_ROLE` |
| `finalize` | 실제 `p4_evidence.json`, L1 allowlist, `--stage finalize --run-id <id>` | Target/Excluded/Pending Lists, 상세/요약 Evidence JSON, 이슈별 `INCLUDED_L1 / EXCLUDED_NON_L1 / PENDING` |

**Jira JSON 주요 필드:** `issues[].issue_key, retrieval_status, summary, feature, description, comments_complete, comments[]{id,body,author,created}`. 댓글 페이지가 누락되면 `comments_complete=false`.

**P4 JSON 주요 필드:** `changes[].cl,status,submitted,user,change_kind,files_complete,files[]{path,action},origin_confirmed,source_cls[]`. P4 성공 보고는 실제 MCP 결과로만 설정하고, integration source CL 미추적·파일 목록 불완전·L1 scope 미등록이면 `PENDING`.

**판정 한계:** `INCLUDED_L1`은 해당 Jira의 P4-verified L1 SW 수정 후보 식별이지 Root Cause, 수정 정답, 테스트 PASS, 개인 결함 책임의 증거가 아니다. 전체 이슈 분석은 Workflow + code-analyzer가 별도 검증해야 한다.

### 3.2 `integration_history_rules` 및 파일 계보

- `p4 annotate -c`는 현재 branch의 line-wise 반영 CL, `-I`는 integration origin CL로 구분.
- API 범위의 원본 실제 변경 CL을 먼저 판정하고 integration 반영 CL과 구별. `-I` 실패 시 원본 변경자 `UNKNOWN`.
- move/add·move/delete, integrate, manual copy/delete의 **공식 계보/휴리스틱 후보**를 구분.
- 파일 편집/이동자나 integration 담당자 = 조직 공식 Owner라는 주장은 금지.
- `p4_history_report.md`에는 실제 수정자/CL, branch 반영자와 source origin, before/after, lineage, 불확실성, fast-stop 상태가 별도 정의됨.

**리뷰 누적 결론:** Issue Key → CL/Evidence/lineage는 재사용 가능. 이슈 근본 원인·해결 검증·Finding verdict/재오픈 이력은 기존 Workflow/Kernel에 연결해야 한다.

## 4. l1-github read-only history 및 역할 계약

- `file-history`, `file-blame`, `code-owner`, `file-at`는 Git source 변경 이력/라인 attribution 및 특정 commit 버전 read-only 조회를 위한 action. `code-owner`는 HEAD에서 살아 있는 코드에 기여한 최신 author로서 **declared CODEOWNERS/조직 Owner와 다름**.
- `repo-config roles --json`, `--role work_docs`로 사내 work_docs 저장소·호스트 경로 확인하는 계약.
- Source code repository와 Work docs/Knowledge repository는 역할 분리. Push Guard는 identity/role/remote verification; repo 등록만으로 Push 승인 불가.
- `pr_history.md`는 squash/cherry-pick/rebase의 **Git 이력 안내 문서**이지 GitHub PR 리뷰 댓글 이력을 저장하는 인터페이스가 아님.

## 5. 기존 기능으로 충분한 범위와 명확한 갭

| 요구 | 현재 패키지 문서 근거 | 결정 / 빈자리 |
|---|---|---|
| 정확한 PR base/head·diff·변경 범위 | l1-github PR code analysis + code-analyzer git-pr-range | `REUSE`, 실제 installed API와 error mode 검증 필요 |
| 코드 변경의 시나리오·영향·MSC | code-analyzer MSC + feature analysis + incremental | `REUSE`, Work Evidence 및 SourceSnapshot과 연결 |
| Jira 전체 댓글+Fix CL 추적 | p4-code-owner `jira-fix-cl-scan` | `REUSE`, Jira/Mango 실 MCP tool·권한 필요 |
| P4 API 원본 수정자 / integration | p4-code-owner integration/move rules | `REUSE`, owner authority와 별개 |
| Git blame/commit/파일 이력 | l1-github file history | `REUSE`, 리뷰 comment 수집과 다름 |
| GitHub PR review discussion/comment/approval 전체 수집 | 확인한 계약에서 명시적 수집·pagination/평가 상태 SSOT 확인 못함 | `GAP / NEED_CODE_OR_HOST_CHECK`; 새로운 수집기 선제 제작 금지 |
| 리뷰 `review_id / finding_id / review_revision / resolution_state`의 Work별 누적 | 현재 검토한 3개 계약에 **공통 영속 출력 스키마 없음** | `CONNECT / EXTEND` 후보, Kernel SSOT 검토 후 다음 단계 |
| Finding → Issue / PR / CL / CODE_FACTS / MSC 교차 링크 | 개별 증거/범위 ID 존재, 통합된 링크 계약 미검증 | `CONNECT` 후보 |
| 반복 지적의 중복/충돌/지식 승격 | existing Gotcha Preview / 승인 정책과 잠재 연계 | `CONNECT` 후보, 실제 소비/승격은 `NOT_RUN` |
| 실제 Provider 본문 RAG 소비 | `knowledge_link` 등록만으로 충분치 않음 | `M1 BLOCKED`; 기존 7대 Gate 유지 |

## 6. Step 2 이전에 고정할 최소 통합 인터페이스 (설계 후보; 구현 아님)

`ReviewSession`: `review_id, review_revision, review_kind(CODE_REVIEW/ISSUE_REVIEW), work_id, target_type(PR/JIRA/P4_CL), target_ref, source_snapshot_id, tool_run_ids[], collection_completeness, created_at, status`.

`Finding`: `finding_id, review_id, severity, claim, evidence_ids[], scope, disposition(ACCEPT/ACCEPT_WITH_CHANGE/REJECT/HOLD), resolution_state(OPEN/FIXED/REOPENED/UNVERIFIED), verification_state(PASS/FAIL/NOT_RUN), supersedes_finding_id?, knowledge_candidate_id?`.

**판정 요구:**
- Session/revision 안정 ID는 PR 리비전·이슈 재조회·CL 신규 추가를 보존하고, 동일 ID 인입은 무해하게 재처리.
- `work_category`(Work 주목적)와 `review_kind`(활동 타입), `artifact_kind`(MSC_AS_IS 등)는 서로 다른 축.
- 형상관리 기준: Git full SHA, P4 per-file haveRev/CL; 정확한 source root/product/branch/build/dirty state와 함께 연결. 1개 PR에 여러 리뷰세션, 1개 Issue에 여러 CL 허용.
- 리뷰 `OPEN`·`FIXED` 상태는 푸시/merge나 L1 포함 판정만으로 자동 전환하지 않음. 실제 수정·시험 근거 필요.
- code-analyzer run retention과 별도로 장기 Work Evidence/비민감 요약을 보호; 원문/코드/설계는 사내 권한 경계 준수.

## 7. 사내 G0 확인 목록 및 후속 부정 회귀시험 (NOT_RUN)

| ID | 실제 확인할 항목 | 통과·거부 조건 |
|---|---|---|
| C01 | 실제 설치 버전/hash/release status·CLI action export | PUBLIC 후보와 설치 드리프트 구분 |
| C02 | l1-github PR API JSON 및 code-analyzer handoff | base/head/diff 정확 일치, missing commit fail-closed |
| C03 | `semantic_workspace_ready`/단독 fallback | 원본 working tree 변경 0; 부정확한 scope 제한 |
| C04 | Jira MCP comment pagination·ADF·누락 | 불완전 시 `comments_complete=false`, PENDING |
| C05 | Mango P4 CL submitted/files/lineage 및 scope allowlist | integration origin 불명/목록 불완전은 PENDING |
| C06 | code-analyzer 실제 output schema/evidence ID+MSC | CODE_CONFIRMED와 추론 분리, SourceSnapshot 검증 |
| C07 | GitHub PR review comment 수집 API 실제 존재 여부 | 코멘트·일반 PR discussion·review verdict 종류와 pagination 각각 확인 |
| C08 | review_id/finding_id 중복·불변·수정 상태 | 같은 ref 재조회 시 중복 0, resolved/reopen 이력 보존 |
| C09 | Work docs exporter/Kernel schema, Evidence handoff | 이전 Work/수동 문서/index/resume 무손실 |
| C10 | Run-retention·Git 문서 이력·Knowledge Preview | 원본 Run compact 이후 Work 근거 링크 무결성 |
| C11 | source/owner authority·cross-product scope | Git/P4 reviewer attribution을 owner로 자동 승격 금지 |
| C12 | GitHub PRIVATE 반출 가드 | 회사 원문/내부 경로·토큰 외부 게시 0 |

## 8. Step 1 실측 요약

- `STATIC_CONTRACT_DOC_INSPECTION=PASS` (3 ZIP 실제 확인, 지정 Markdown/JSON 내용 직접 확인)
- `EXACT_PYTHON_SOURCE_IO_CROSS_CHECK=PARTIAL/NOT_VERIFIED` (파일 엔트리 인벤토리 존재, 전체 구현 상세/런타임 반환 실측 미완료)
- `INHOUSE_CLI/MCP/PR/JIRA/P4_LIVE_E2E=NOT_RUN`
- `REVIEW_LEDGER_PERSISTENCE=NOT_IMPLEMENTED_OR_NOT_VERIFIED` (기존 스킬에 없다고 단정하지 않고 설치 계약/전체 코드 확인 전까지 갭)
- `WORKFLOW_OR_KERNEL_PATCH=NOT_RUN`
- `CLAUDE_INDEPENDENT_REVIEW=NOT_RUN`
- `REQUEST_READY / OPERATING_WATCHER / LIVE / PUBLIC_RELEASE=UNCHANGED`

**다음 1개 단계:** Step 2에서 실제 Kernel Work SSOT를 훼손하지 않는 `ReviewSession + Finding + SourceSnapshot + Evidence` 최소 스키마/중복키 설계(문서만) → 사내 읽기 전용 C01~C07 검증 후 구현 여부 판정. 외부에서 내부 자료를 임의 재현하거나 자동 반출하지 않는다.
