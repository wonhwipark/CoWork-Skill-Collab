# Claude Code 독립 설계 리뷰 요청 — CL/PR 기반 L1 이슈 분석 및 Work 축적 r0001

- Date: 2026-11-14 KST
- Review request ID: `L1-CLPR-ISSUE-DESIGN-20261114-001` (새 Kernel Work ID 아님)
- Parent Work: `L1-WORKSPACE-RAG-20261111-001`
- Target repo/branch: PRIVATE `wonhwipark/CoWork-Skill-Collab` / `main`
- **Primary design:** `collab/projects/L1-WORKSPACE-RAG-20261111-001/CL_PR_ISSUE_ANALYSIS_DESIGN_BRIEF_r0001_20261114.md`
- Baseline: `collab/projects/L1-WORKSPACE-RAG-20261111-001/CURRENT.md` (11/14 최상단 최신 요약 우선)
- Actual skill contracts: `collab/projects/L1-WORKSPACE-RAG-20261111-001/L1_REVIEW_ACCUMULATION_SKILL_IO_CONTRACT_AUDIT_r0001_20261111.md`
- Kernel evidence limitations: `collab/projects/L1-WORKSPACE-RAG-20261111-001/L1_REVIEW_ACCUMULATION_G0_PARTIAL_AUDIT_r0001_20261111.md`
- Knowledge design: `collab/projects/L1-WORKSPACE-RAG-20261111-001/L1_KNOWLEDGE_UPDATER_K58_K6_WORKFLOW_CONTRACT_r0005_20261111.md`
- Latest feedback disposition: `collab/projects/L1-WORKSPACE-RAG-20261111-001/L1_KNOWLEDGE_FEEDBACK_DISPOSITION_r0001_20261114.md`
- **Expected non-sensitive result:** `collab/projects/L1-WORKSPACE-RAG-20261111-001/CLAUDE_CL_PR_ISSUE_ANALYSIS_DESIGN_REVIEW_RESULT_FOR_GPT_r0001_20261114.md`
- Mode/state: `SEMI_AUTO / INTERACTIVE_INDEPENDENT_DESIGN_REVIEW_PREPARED / NOT_QUEUED / REVIEW_NOT_RUN`
- This request document is **not** signed REQUEST/READY; posting is not model invocation, paid-review approval, or installation/deployment authorization.

## 독립 리뷰 임무

정확한 PRIVATE repo/branch 경로의 기본 설계안을 독립적으로 비판 검토한다. 사용자 의도는 P4 submitted CL + GitHub merged PR 목록에서 **같은 실제 이슈에 속하는 변경을 묶고, 문제·근본원인·수정 메커니즘을 확인된 Evidence와 함께 기존 l1-workspace Work에 보존**한 뒤 Knowledge Updater 준비 시 검증된 기술 사실만 승격하는 것이다.

**새 분석 스킬/원장/RAG 엔진을 선제 개발하지 말 것.** 기존 l1-fix-workflow, l1-github, p4-code-owner, code-analyzer, issue-analyzer(선택), work-ledger-kernel 및 knowledge-updater의 실제 I/O/registry 기능을 REUSE → CONNECT → 필요한 최소 EXTEND → DEFER로 판정한다.

## 리뷰 질문 — 실제 동작의 구조적 결함 우선

| ID | 중점 질문 | 필요한 반례/증거 |
|---|---|---|
| R01 BLOCKING | Jira ID 없이 P4 **CL 번호 목록만** 시작하는 공식 조회/분석 경로가 있는가? | `jira-fix-cl-scan`은 Jira-first: 없는 CLI·MCP 이름 임의 가정 금지, CL-only fallback 판정 |
| R02 BLOCKING | Git merged PR의 base/head diff와 merge/squash/rebase 후 **실제 target 반영 SHA**를 분리했는가? | PR merged만으로 본선 및 타 브랜치 수정/시험 PASS 금지 |
| R03 BLOCKING | CL/PR → issue N:M 그룹핑의 신뢰 기준과 근거 손실이 없는가? | Jira 없는 변경, 같은 모듈의 다른 결함, 한 CL에 복수 문제, P4 integration/backport/revert |
| R04 BLOCKING | code-analyzer에 Git full SHA, P4 per-file before/after revision, source root/scope를 오류 없이 전달 가능한가? | HEAD drift, dirty/untracked, missing git object, mixed P4 revision에서 거짓 CODE_CONFIRMED 방지 |
| R05 BLOCKING | 변경된 코드만 보고 Problem/Root Cause/Fix를 확정하는 오류가 없는가? | 증상/로그 부재 시 INFERENCE·UNKNOWN, Fix mechanism과 시험 PASS·현행 적용 구분 |
| R06 MAJOR | `issue-analyzer`가 실제 언제 필요한가? | Jira/log 없는 경우 무조건 호출하는 분석 지연·불필요한 SDM/TXT 의존 금지 |
| R07 BLOCKING | Kernel Evidence registry 및 Work exporter/Run retention 계약을 침범하는가? | `code_review`/`issue_review`/`p4-code-owner` 직접 Evidence 미등록 후보, record.json/README/index 임의 수정 0 |
| R08 MAJOR | 기존 Work 재개, 반복 동일 목록 처리, review Finding과 source scope의 장기 링크가 충분한가? | 중복 Work 0, source revision 변화 시 기존 분석 증거 보존, 새 원장 도입 근거 |
| R09 MAJOR | 향후 기존 Module→Feature→Scenario 지식에 링크될 수 있는가? | v0.9 후보행 vs 실제 ID, 그룹 내용 vs Work 정본, 게시와 역링크 독립 |
| R10 BLOCKING | 회사 자료 반출 금지와 읽기·쓰기 승인/독립 리뷰의 경계가 충분한가? | PRIVATE에 제한자료 0, 회사 코드 없는 E1/E2 리뷰와 업무 호스트 E3 구분 |
| R11 MAJOR | 소량 파일럿으로 실제 가능성을 판단하는 최소 시험은? | 기준안 T01~T14 중 우선순위, PASS/FAIL/SKIP/NOT_RUN의 실근거 |
| R12 MAJOR | 갭이 확인된다면 어느 기존 스킬에 가장 작은 변경이 적합한가? | REUSE/CONNECT/EXTEND/DEFER, 소유권/호환성/롤백/추가 테스트 |

질문별: 판단(ACCEPT/ACCEPT_WITH_CHANGE/REVISE/HOLD), 심각도(BLOCKING/MAJOR/MINOR), E0-E3 근거, 영향, 최소 수정안, 부정시험 및 미확인 사항을 작성한다. 문서 내 모든 인터페이스가 실제 설치 API는 아님. 미확인은 미지원으로 오판하지 않는다.

## 결과 요구 형식

```text
REVIEW_STATUS: COMPLETED | PARTIAL | NOT_RUN
REVIEW_KIND: INDEPENDENT_DESIGN | NOT_RUN
INPUT_REPO / INPUT_BRANCH / PINNED_INPUT_COMMIT / INPUT_BLOB_SHA
EVIDENCE_LEVEL: E3(real installed host) / E2(actual code) / E1(contract docs) / E0(no evidence)
DESIGN_DISPOSITION: ACCEPT | ACCEPT_WITH_CHANGE | REVISE | HOLD | MORE_INFO
FINDINGS: [id, severity, evidence, impact, minimal_change, negative_test, owner]
SKILL_MATRIX: [name, REUSE|CONNECT|EXTEND|DEFER, verified contract/gap]
CL_ONLY / MERGED_PR / GROUPING / CODE_ANALYSIS / WORK_EVIDENCE / KNOWLEDGE_GATES: ...
TESTS: T01..T14 -> PASS|FAIL|SKIP|NOT_RUN + real evidence
UNVERIFIED_OR_BLOCKED: ...
CODE_PATCH / HOST_EXECUTION / GROUP_WRITE / PUBLIC_RELEASE: NOT_RUN
RESULT_POST / COMMIT / SHA256 / READBACK: actual only
NEXT_ONE_ACTION: ...
```

## 실행·게시 안전 경계

- 이 문서의 **게시는 리뷰 실행이 아님**. 현재 Github watcher LIVE 미승인, `ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER`; 기존 Dropbox watcher가 11/12 Disabled/Stopped 되었다는 최신 기록을 따른다.
- 사용자 승인된 별도 **Claude Code 대화형 독립 리뷰 세션**에서 정확한 이 GitHub 파일 경로를 읽게 하거나, 향후 실제 가동·승인된 리뷰 운송 계약으로 유효 요청이 접수되어야 비로소 리뷰가 수행된다. 신규 유료 호출은 비용·모드 승인을 별도 확인하며, 임의 READY 생성 금지.
- Windows Claude Code가 업무용 소스·MCP/설치본에 접근 못하면 PRIVATE의 비민감 설계 및 공개 후보 패키지 계약으로 E1/E2 범위만 검토하고 E3 호스트 사실은 `NOT_VERIFIED`로 기록. 내부 자료/토큰/로그/상세 MSC는 **PRIVATE에도 게시 금지**.
- 독립 리뷰 세션에서 비민감 결과만 위 `Expected result` 파일에 PR 없이 게시·remote readback; 원격 바이트 SHA256/commit 확인. 게시 불가면 `NOT_POSTED`, REVIEW_STATUS를 실제 실행 수준대로.
- 소스·스킬 ZIP 수정, Kernel 운영 registry/schema 변경, 회사 Git/P4 쓰기, Job-list·MCP 실행, 모델 자동 호출, WATCHER/DB/Task/Telegram/LIVE 변경, PUBLIC 게시, 그룹 지식 자동 쓰기는 모두 제외한다.

## 사용자에게 전달할 단일 실행 문구

PRIVATE `wonhwipark/CoWork-Skill-Collab`, `main`, `collab/projects/L1-WORKSPACE-RAG-20261111-001/CLAUDE_CL_PR_ISSUE_ANALYSIS_DESIGN_REVIEW_REQUEST_r0001_20261114.md`를 읽고 해당 요청서의 CL/PR 이슈별 분석→Workspace 축적 연결에 대한 **독립 설계 리뷰**를 수행해줘. 비민감 결과를 지정 `CLAUDE_CL_PR_ISSUE_ANALYSIS_DESIGN_REVIEW_RESULT_FOR_GPT_r0001_20261114.md`에 게시하고 원격 재조회해줘. 접근 불가 부분은 NOT_VERIFIED로 남기고 코드 수정·유료 자동 호출·운영 변경은 하지 마.
