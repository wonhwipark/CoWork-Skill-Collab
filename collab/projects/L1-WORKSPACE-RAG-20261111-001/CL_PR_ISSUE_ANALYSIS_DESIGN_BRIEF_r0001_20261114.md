# CL/PR 목록 기반 문제·원인·수정 분석 → Workspace 축적 — 설계 리뷰 기준안 r0001

- 기준일: 2026-11-14 KST
- 부모 Work: `L1-WORKSPACE-RAG-20261111-001` (별도 Work/원장 엔진 신규 생성 요청 아님)
- 검토 대상: `P4 submitted CL 목록 + GitHub merged PR 목록 → 이슈별 Problem / Root Cause / Fix / Verification → 기존 l1-workspace Work/Evidence`
- 단계: DESIGN_REVIEW_INPUT / FIRST_REAL_ANALYSIS_NOT_RUN / GROUP_KNOWLEDGE_WRITE_NOT_RUN
- 출처: 기존 PRIVATE `CURRENT.md`, `L1_REVIEW_ACCUMULATION_SKILL_IO_CONTRACT_AUDIT_r0001_20261111.md`, `L1_REVIEW_ACCUMULATION_G0_PARTIAL_AUDIT_r0001_20261111.md`, `L1_KNOWLEDGE_UPDATER_K58_K6_WORKFLOW_CONTRACT_r0005_20261111.md`, 11/14 최신 피드백 판정
- 본 문서는 비민감 설계안이며 실제 CL/PR 번호·업무 코드·사내 경로·내부 MCP ID·로그·MSC 원문은 포함하지 않음. 리뷰 요청이지 설치·실행·게시 승인 아님.

## 1. 사용자 목표 및 비목표

사용자가 CL/PR 리스트만 제공해도 분석을 시작할 수 있어야 한다. 여러 변경이 하나의 이슈에 속하면 하나의 이슈 케이스로 통합하고, 각 이슈별 증상·원인·변경 이유·검증 근거와 미확인을 별도 기록한다. **1차에는 승인된 업무용 l1-workspace의 기존 Work/Evidence에 축적**하며, 후일 Knowledge Updater의 Preview/검증/승인을 거친 기술 사실만 `l1sw-dev-knowledge`로 등록하고 Work에는 고정 게시 revision 링크를 보존한다.

비목표: 새 범용 issue parser·RAG/vector DB·새 Work ID 발급기·Review Ledger·CAS/복구 엔진의 선제 구현, 그룹 지식 자동 쓰기, 회사 자료의 PRIVATE/PUBLIC 반출, 운영 소스/worktree 수정, 자동 Job 재실행, watcher/LIVE 전환.

## 2. 검증된 계약 / 아직 가설인 접점

| 역할 | 기존 계약에서 확인된 부분 (E1/E2) | 미확인·후속 실측 |
|---|---|---|
| `l1-fix-workflow` | 기존 Work 선택·재개·분석 흐름 연결 | 리스트 묶음 진입점, Work 재사용 규칙, 실제 설치 I/O |
| `l1-github` | `pr-code-analysis`에서 PR base/head full SHA·diff·changed files·handoff 제공; source/worktree guard | merged 상태·실제 반영 commit/squash/backport, comment/review 완전성·pagination, 설치 반환 JSON |
| `p4-code-owner` | Jira→CL `jira-fix-cl-scan` prepare/scan/finalize, CL provenance·integration 규칙 | **CL 번호만으로 시작하는 직접 조회 entrypoint** 존재 여부, P4 before/after file#rev, MCP route/권한 |
| `code-analyzer` | `git-pr-range`, `git-incremental`, Code Facts, MSC_AS_IS/CHANGE_IMPACT, evidence/scenario catalog | P4 file#rev before/after semantic 입력, Git HEAD drift/Run retention, 실제 결과→Work 지속 링크 |
| `issue-analyzer` | 로그/증상 근거 기반 이슈 분석 | CL/PR만 제공 시 무조건 호출하지 않음; 증상·로그가 있으면 선택 |
| `work-ledger-kernel` | Work SSOT `record.json`, 허용 provider/kind/stage/profile Evidence, exporter | 운영 설치 슬롯, review finding의 원장 연결. 개발 후보 E2에서는 code_review/issue_review/P4 direct kind 미등록 |
| `l1-knowledge-updater` | 기술 후보·중복/충돌·K5.8/K6·Preview 정책의 G0 일부 호스트 보고 | 게시/역링크/Provider 본문 소비 E2E 미검증; 현 단계 미실행 |

본 기준안은 E1 문서 확인과 E2 개발 패키지 격리시험을 E3 실제 설치·호스트 PASS로 승격하지 않는다.

## 3. 제안 처리 흐름 (소스 조회·분석은 승인된 업무 실행 호스트에서만)

**S0. Work resolve:** 요청 리스트 정규화와 변경 제공자/대상 repo·depot·product·RAT·branch 정보를 확인. Kernel의 기존 Work ID를 검색/재개하거나 권한 있는 기존 경로로 새로 발급. Work category/새 메타 필드를 임의 추가하지 않음.

**S1. 원본 수집:** Git merged PR의 repo/number, PR 상태·merge 시점, base/head full SHA, 비교 범위, changed files, 실제 target branch 반영 commit(Squash/Rebase/merge 차이)을 구별. P4는 submitted CL·변경 파일/액션, 원본 CL vs integration CL, 파일별 before/after revision/haveRev, 권한·수집 완전성을 확인. 조회 실패/페이지 누락은 PARTIAL/UNAVAILABLE; 가상의 commit/revision 보충 금지.

**S2. 변경 역할 분류:** FIX / FOLLOW_UP / INTEGRATION / BACKPORT / REVERT / REFERENCE / UNKNOWN 후보. Jira ID·description·함수/경로·조건 변화·계보로 연관도를 평가. 1개 이슈←다수 CL/PR, 1개 CL/PR→다수 이슈 가능. **같은 모듈/수정자만으로 병합 불가**. Jira 부재 시 근거기반 후보 그룹 및 UNLINKED/UNKNOWN 허용.

**S3. 분석 범위 고정:** Git pinned SHA와 분석 worktree의 semantic readiness를 대조. P4 전체 단일 CL이 아니라 파일별 revision/scope를 고정. Dirty/untracked, branch drift, missing object, 불명 원본/본선 반영은 현재 코드 VERIFIED 차단하고 historical/inferred로 별도 보존.

**S4. 차이·메커니즘 분석:** 변경된 함수/조건/상태·call graph·callee/caller(depth 1 우선) 및 필요 MSC만 code-analyzer로 분석. 증상·재현·Jira 댓글/로그가 있으면 issue-analyzer 선택 연계. 한쪽 provider의 결과를 다른 provider의 결과로 가장해서 Kernel에 등록하지 않음.

**S5. 이슈별 결과 판정:** Problem=(관측 증상/조건 또는 미확인), Root Cause=(코드근거 확인/추론/불명), Fix=(변경 전후 논리와 효과의 가설), Side Effect/Impact, Verification=(branch별 integration/revert 및 실제 시험 PASS/FAIL/SKIP/NOT_RUN). 'Merged/Submitted'는 시험 PASS가 아님. 원인 확인·수정 반영·시험 결과·현행 적용성은 독립 상태.

**S6. Work 축적:** Kernel의 실제 허용 슬롯에 해당하는 Code Facts/Issue Analysis/MSC 등 Evidence만 정상 경로로 기록. P4 원시 메타·이슈 그룹·review finding은 **기존 Work Artifact/참조로 충분한지 먼저 점검**; 임의 Evidence kind/provider, `record.json` 필드, exporter 생성 `README/index/문서안내` 직접 쓰기 금지. Run-retention 이후에도 Evidence digest/고정 reference 확인, remote work_docs 쓰기 승인·readback 분리. 중복 리스트 재입력은 가능한 기존 Work 참조로 idempotent, 서로 다른 source scope는 무조건 합치지 않음.

**S7. 향후 지식 승격:** 기존 `Module → Feature → Scenario` ID 매핑, Procedure 교차뷰, v0.9 검토행을 실제 ID로 오인하지 않음. Knowledge Updater의 NEW/ENHANCEMENT/DUPLICATE/CONFLICT/RECHECK 후보, Preview·승인·기존 writer/readback·Work 역링크. Work 이력 원본은 보존하고 그룹에는 검증된 기술 사실만; 현재는 후보 설계만.

## 4. 표준 분석 출력 (제안 의미, 설치 필드 아님)

- `issue_case`: 안정 Work 참조 + issue group identity + known/unknown Jira links + PRODUCT/RAT/MODULE/FEATURE/SCENARIO (후보·실제 ID 구분)
- `provenance`: 소스 제공자별 repo/depot, branch, full Git SHA / P4 per-file revision, origin-vs-integration, collection completeness, before/after 역할
- `problem`: symptoms, trigger/condition, observed_vs_inferred, proof refs
- `root_cause`: mechanism, code anchors, claim state, competing hypothesis/contradictions
- `fix`: changed logic, why it addresses cause, cross-branch status, revert/backport, side-effect risk
- `verification`: per-product/branch PASS/FAIL/SKIP/NOT_RUN, test snapshot, applicability
- `evidence_links`: existing Kernel Evidence ID and analyzer run/source digest, unresolved links
- `knowledge_transition`: candidate status only, publication NOT_RUN, actual knowledge ID pending validation

위는 출력 **논리 요구**이며 신규 Kernel 필드·레코드 구현 명령이 아니다.

## 5. 1차 파일럿 성공 기준 / 부정 시나리오

작은 비운영 테스트 목록(예: 합성 CL 3개, PR 2개)의 허용된 scope를 사용하며, 첫 실제 데이터는 사용자 및 업무 환경 승인이 필요하다.

| ID | 검토/시험 조건 | 기대 결과 |
|---|---|---|
| T01 | PR 단독, Git pin·diff 정상 | 변경 메커니즘 evidence, 인과 불명은 INFERENCE |
| T02 | P4 submitted CL만 제공, Jira 없음 | 직접 조회 존재/부재 실측; 미지원이면 `ADDITIONAL_CHECK_REQUIRED`, Jira 임의 생성 금지 |
| T03 | 2 CL + PR 1개가 같은 이슈임이 명확 | 하나의 이슈 케이스, 3개 원본 링크 보존 |
| T04 | 동일 모듈에서 별개 이슈 2개 | 병합 금지, 별개 Work 또는 분리된 케이스 |
| T05 | PR merged지만 squash/backport 미연결 | head diff와 target 반영을 별개 판정 |
| T06 | P4 integration CL만 있고 origin 불명 | `PENDING`, 원본 수정자로 오판 금지 |
| T07 | dirty Git HEAD / missing object / P4 file revision mix | stale/unknown, 현재 코드 VERIFIED·Knowledge 게시 차단 |
| T08 | Jira/PR review comments 일부 페이지 누락 | 수집 COMPLETE 금지, 원인 미확정 |
| T09 | 동일 리스트 재입력/순서 변경 | 중복 Work·Finding 0; 명시적 별도 재분석은 revision 이력 보존 |
| T10 | Kernel 미등록 provider/kind에 기록 시도 | fail closed, 운영 registry/schema 임의 변경 0 |
| T11 | Analyzer run 정리 후 Workspace 재열람 | 장기 Evidence ID/해시/문서 링크 무결 |
| T12 | 원인은 확인, 수정 반영 전/시험 NOT_RUN | 서로 다른 상태로 기록, VERIFIED_CLOSED 금지 |
| T13 | 외부 PRIVATE에 회사 코드/로그/상세 MSC 포함 | 전송 차단, 비민감 메타 보고만 허용 |
| T14 | Workspace 저장 성공, 그룹 지식/역링크 미실행 | Workspace 결과만 확인; Knowledge/RAG PASS 주장 금지 |

**파일럿 완료 정의:** 입력 5건 정확 수집/실패 표시 → 이슈 그룹핑 근거 → Problem/RootCause/Fix + claim state → 기존 Work/Evidence 저장·readback → 재실행 중복 없음. Knowledge 승격·실 Provider RAG 소비는 별도 후속 게이트.

## 6. 설계 리뷰에서 우선 판정할 핵심 6건

1. CL-only 시작 경로: Jira-first p4-code-owner의 실제 제약과 우회 없는 최소 CONNECT.
2. GitHub merged PR의 merge-base/head 분석과 실제 적용 SHA의 차이 및 P4 integration 중복.
3. 변경 역할 그룹핑의 출처 신뢰·N:M·충돌·반례·미분류.
4. code-analyzer의 Git/P4 before/after 입력 충족 여부와 부분/증분 분석 비용.
5. Work SSOT·Kernel Evidence registry·exporter/Run-retention 호환성, 새 리뷰 ledger 불필요성.
6. 문제/원인/수정의 사실·추론, fix·test·현재성 분리, Knowledge 후속 연결.

현재 결정: `REUSE_EXISTING_ANALYZERS_FIRST / DESIGN_REVIEW_PENDING / INDEPENDENT_REVIEW_NOT_RUN / HOST_E2E_NOT_RUN / KNOWLEDGE_WRITE_NOT_RUN`.
