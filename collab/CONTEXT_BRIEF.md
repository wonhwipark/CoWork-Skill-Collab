# CoWork 공통 맥락 브리프

- 개정: r0004 / 확인 기준 2026-11-14 KST (Work → Knowledge 독립 설계 리뷰 요청 연결)
- 저장소: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`
- 최초 기준 commit: `fdea038df35eec7d102d703b46acdf3a31f3b0ae`; r0002는 운영 경로 보완, r0003는 Work → Knowledge 전환 설계 연결, r0004는 해당 설계의 별도 Claude 독립 리뷰 요청 연결. 아래는 출처별 최신 blob을 따라가는 **읽기용 파생 지도**이며 설치·실행·승인 원장이 아님.
- 읽기 순서: **이 파일 → 아래 표의 관련 CURRENT → 필요한 계약·스킬 원문**. 브리프와 새 근거가 다르면 최신 근거를 따른다.

## 0. L1 협업 역할 이름과 증거 책임

- **설계 GPT:** 허용된 문서/비민감 상태를 바탕으로 L1 지식 상위 설계·스킬 책임·정합성/리뷰 판정. 실제 Linux 코드/호스트 시험을 직접 확인한 것으로 주장하지 않음.
- **업무 GPT:** 실행 LLM 및 Agent의 원문 결과를 전달받아 분석·판정하고, L1 Knowledge Updater·지침·전체 지도·작업별 최신 상태의 정합성을 유지. 파일/코드/MCP 직접 접근은 확인 전 가정하지 않음.
- **실행 LLM:** 허가된 도구/스킬로 분석·격리 구현·시험을 수행하고 Evidence를 보고. 자체 시험과 독립 리뷰는 분리.
- **모바일 Agent:** 사용자 요청을 승인된 Linux MCP에 연결해 Work/Job 진행·조회와 결과 회수를 지원. 실제 도구 실행·결과 성공·Knowledge 게시를 Agent 사용만으로 추정하지 않음.
- 새 문서는 망/위치 명칭 대신 위 역할명과 실제 도구명으로 표현. [역할·용어 계약](ops/CONTRACTS/EXECUTION_PROMPT_TERMINOLOGY_V1.md). 과거 파일명/기록은 추적성을 위해 유지.

## 1. 협업 운용·저장소

- GPT가 범위·개발/시험·리뷰 판정·정본을 총괄하고, Windows Claude Code가 기본 독립 리뷰를 맡는다. 개발 세션 자체시험과 독립 리뷰는 구분한다. 리뷰 불가 항목만 PENDING/NOT_RUN으로 두고 가능한 작업은 계속.
- 사용자 1회 지시 안에서 허용된 조사·수정·시험·패키징·PRIVATE 결과 게시·원격 재조회까지 묶어 진행. 일반 협업은 PR 없이 직접 게시. 이미 승인된 범위의 중간 확인을 반복하지 않음.
- 단일 사용자 SU-SIMPLE 설계 우선. 별도 서명자 PC·로컬 LLM·고급 격리 입증을 기본 의무로 되살리지 않음. 실제 운영 보호·비용 승인·중복 방지·불확실 호출 보존은 해당 최신 계약을 확인.
- **문서/링크 게시 ≠ 모델 리뷰·Job 실행·설치·LIVE 전환.** 유료 독립 리뷰·운영 DB/예약·토큰/신뢰키·PUBLIC 신규 배포·LIVE 변경은 실제 승인 범위와 근거를 확인.
- 회사 코드·상세 MSC/로그·고객자료·비밀은 PRIVATE에도 게시 금지. 비민감 설계/상태만 요약. 역할·도구·저장소 이름으로 표현하고 기존 파일명은 보존.
- 상세 정책: [START_HERE](START_HERE.md), [표기·접근](ops/CONTRACTS/TERMINOLOGY_AND_ACCESS_SCOPE_V1.md). 이미 읽은 브리프를 START_HERE에서 다시 반복 조회하지 않음.

| 위치 | 역할 |
|---|---|
| CoWork PRIVATE | 비민감 협업·설계·리뷰·판정·영수증. 허용된 watcher 자체 후보는 PRIVATE 리뷰 입력 |
| L1Work PUBLIC | 승인된 최종 ZIP은 main 루트, 업무용 GPT/Agent 인계는 main/handoffs, 허용목록 화면·가상 샘플 |
| 업무용 `l1-workspace` | Work ID·상태·분석/결정·수정·시험·리뷰·Evidence 정본. GitHub.com 동명 저장소로 추정 금지 |
| 팀 `l1sw-dev-knowledge` | 검증된 기술 지식 정본. 그룹 게시와 Work 역링크를 각각 확인 |

## 2. L1 지식의 합의 방향

- 기존 Workflow/Kernel/Updater/analyzer/converter/Git·P4를 **REUSE → CONNECT → 확인된 GAP만 최소 EXTEND**. 미확인 API를 미지원으로 단정하거나 새 엔진/원장/schema를 먼저 만들지 않음.
- Workflow는 요청 의도·기존 Work 선택/재개, Kernel은 Work/Evidence, code-analyzer는 Code Facts, doc-converter는 MSC 표현/변환, Knowledge Updater는 기술 후보·중복/충돌·Preview·보완 인계·승인/기존 writer 조정·게시 결과 회수를 담당하는 방향.
- **2026-11-14 사용자 수용 설계:** [Work → Knowledge 전환 흐름](projects/L1-WORKSPACE-RAG-20261111-001/L1_WORK_TO_KNOWLEDGE_FLOW_r0001_20261114_KST.md)에서 분석 저장 → 동일 Work 지식화 요청 → 후보·대조·Preview → 개인 유지 또는 같은 Work 보완 → 승인 게시 → 원격 확인 → 원래 Work 결과 회수를 구체화. 개인 중간 자료는 상태·출처를 붙여 Workflow가 재사용하고, 그룹 게시 전에도 개인 Work에 유지. 구현·API/E2E 확인은 별도이며 자동 호출/새 엔진/schema를 추가한 결정이 아님.
- 그룹에는 HLD·상세설계·검증된 AS-IS MSC·Lifecycle·재사용 이슈 지식까지 수용. Workspace 원본 이력은 보존하고 게시 revision으로 연결. 상세도만으로 개인/그룹을 결정하지 않음.
- **Module → Feature → Scenario** 정본 구조 유지, Procedure/운용 맥락은 교차 탐색 뷰. Work 목적(ISSUE/FEATURE/REFACTOR/DESIGN/CODE_ANALYSIS), 산출물(MSC_AS_IS/MSC_TO_BE 등), 기술 분류, 실행 Profile은 별개이며 미확인 필드를 임의 저장하지 않음.
- 담당 범위: NR BCH(=NR L1 Channel Controller), NR L1 Tx, LTE ChCfg, LTE L1 Tx. SCell Channel 주관/Tx 하위 참여 구분, Search/Measure·DRX 본체의 소유권은 확대하지 않음.
- v0.9는 **215개 검토행(P120/F95)**. 검토행 ID는 실제 Feature/Scenario ID가 아니며 담당자 승인·코드 지원 확인과 분리.
- r0005 + 11/14 판정이 현재 기준. **G0 일부 확인 보고**를 재사용하고 정책 적합성·최소 전달·Kernel stage 호환만 지금 점검. 원본 설치/API·독립 리뷰 전체 PASS는 아님.
- **실제 저장·ID/source/MSC/Evidence 정합·게시/역링크·RAG 본문 활용은 첫 승인된 실제 분석 후속.** 미실행을 현재 분류 설계의 누락/차단으로 삼지 않되 실제 분석·게시·RAG 완료는 검증 전 PASS 금지.
- CL/merged PR 목록 분석은 이슈별 문제·원인·수정·검증 상태를 기존 Work에 1차 축적하고, 추후 검증된 기술 사실을 그룹에 게시하는 설계. Work 원본을 삭제·이동하지 않음.
- Git full SHA/P4 실제 파일 revision·scope·Evidence로 근거를 고정. AS-IS/TO-BE, 원인 확인/수정 반영/시험 성공/현재 적용성을 구분.

## 3. 관리 스킬 — 역할부터 선택

관리 18개 + 별도 업무용 연동 1개. 17 ZIP의 SKILL 정적 확인이 근거이며 최신 호스트 설치/호출 성공 목록은 아님. skillsilent 독립 원본은 추가 확인. 버전/실행 계약은 관련 작업에서 필요한 원문만 조회.

| 요청 기능 | 기존 스킬 |
|---|---|
| Work·연속성 | l1-fix-workflow, work-ledger-kernel |
| 증상·코드 분석/수정 | issue-analyzer, code-analyzer, code-fix |
| HLD·MSC·설계/구현 비교 | hld-composer, doc-converter, hld-code-compare, hld-code-implement |
| 소스·변경 근거 | l1-github, p4-code-owner, l1-cl2git-merge |
| LOC/MCD | l1-sam-fixer |
| 설치·실행 게이트·One-shot·예약·정리 | skill-updater, skillsilent, job-list, autotask-builder, l1-cleanup |
| 별도 지식 후보/게시 연동 | l1-knowledge-updater |

[세부 기능·I/O·한계 카탈로그](knowledge/SKILL_CAPABILITY_CATALOG.md). 분석 결과와 지식 링크/변환 성공을 실제 Provider 입력 성공으로 대체하지 않음.

## 3A. 모바일 Agent → Linux MCP → 기존 스킬 실행 경로

```text
사용자 → 모바일 Agent → Linux MCP
                          ├─ A. Work 검색·재개 → l1-fix-workflow → Kernel Work/Evidence
                          └─ B. 신규 Job-list 구성 필요
                               ├─ 설치·갱신 필요 시 skill-updater 1회 수행 요청
                               └─ 승인된 job-list 활성화·Runner/실행 LLM
                                               ↓
                                    상태·결과·영수증 조회
                                               ↓
                                     업무 GPT 검토·판정
                                               ↓
                                l1-workspace → Knowledge Updater
                                               ↓ (별도 승인/검증 시)
                                       l1sw-dev-knowledge
```

- **실제 기존 사용 경로는 사용자 보고**, 현재 MCP tool/API·권한·Updater 실제 적용·Job 활성화·최종 분석/MSC·영수증·E2E는 각각 검증 필요. 문서만으로 자동 호출, 성공 또는 신규 인터페이스 존재를 주장하지 않음.
- `skill-updater`는 조건부 **1회 실행 요청** 대상이지 Job 스케줄러가 아님. 요청, 호출, 적용, Registry/Runner, 결과 읽기와 지식 게시를 구별. 소비된 one-shot은 임의 재실행 금지.
- [스킬 카탈로그](knowledge/SKILL_CAPABILITY_CATALOG.md)는 책임과 후보 호출 관계, [Job CURRENT](projects/JOBLIST-NRTX-20261112-001/CURRENT.md)는 설치·Registry·MCP 결과 조회의 실제 진단/차단 이력, [L1 CURRENT](projects/L1-WORKSPACE-RAG-20261111-001/CURRENT.md)는 지식 연계의 검증 상태 정본.
- **업무 GPT 초기 비교:** 시스템 지도와 업무 GPT의 실제 설치/실행 결과·기존 프로젝트 지침을 `CONFIRMED / USER_REPORTED / INFERRED / NOT_VERIFIED`로 대조. 지침(상시 운영 규칙)·지도(상위 구조)·CURRENT(진행/결정)·Work/Evidence(원본)·Knowledge 후보(검증된 사실)를 분리해 필요한 최소 문서 갱신안만 적용하고 설치/게시/운영 변경은 별도 승인.

## 4. 요청별 최신 위치·확인 시점의 상태

| 요청/업무 | 읽을 정본 | 현재 요약·다음 조치 |
|---|---|---|
| 협업·독립 리뷰·LIVE | [이관 CURRENT](projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md) | ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER. v0.2.14 GPT 판정 ACCEPT_WITH_CHANGE, 호스트 격리시험 PASS는 Claude 자체 보고. 독립 리뷰 PENDING_APPROVAL, 실제 비용·키/토큰·LIVE 승인 범위는 최신 판정에서 확인 |
| L1 지식·RAG·연계 | [L1 CURRENT](projects/L1-WORKSPACE-RAG-20261111-001/CURRENT.md) | r0005와 Work→Knowledge 사용자 수용 설계 유지. 별도 Claude 대화형 독립 설계 리뷰 요청서 게시, 전달 미확인·실행 대기. 구현/E2E 미확인·첫 분석 후속. 별도 CL/PR 최신 후보/회귀·배포 상태는 CURRENT 최상단 실측을 확인 |
| 현재 코드 MSC·HLD | [L1 CURRENT](projects/L1-WORKSPACE-RAG-20261111-001/CURRENT.md) | code-analyzer 근거 → doc-converter 표현. 고정 source의 AS-IS와 승인 설계 TO-BE를 구분 |
| 분류·SCell 등 담당 범위 | [범위 CURRENT](projects/L1-CHANNEL-KNOWLEDGE-SCOPE-20261113-001/CURRENT.md) | v0.9 215행 담당자 검토 대기. [분류표](knowledge/references/L1_NR_LTE_Confluence_Module_Procedure_Feature_Table_v0_9_20261113_KST.md)에서 포함/변경/제외부터 |
| Job 요청·상태·결과 | [Job CURRENT](projects/JOBLIST-NRTX-20261112-001/CURRENT.md) | v0.4.36 PUBLIC 게시 기록. 실제 분석/MSC·MCP 결과 조회 완료 미확인. Queue DONE/Receipt SUCCESS만으로 완료 금지, 소비된 Job 재실행 금지 |
| 화면·협업 흐름 | [대시보드 CURRENT](projects/COWORK-GITHUB-DASHBOARD-20261111-001/CURRENT.md) | Executive v3 목적→단계→다음 조치. 허용목록 자동 갱신과 reviewer LIVE는 별개 |
| Issue Analyzer 변경/배포 | [Issue CURRENT](projects/ISSUE-ANALYZER-20261114-001/CURRENT.md) | v0.11.50은 로컬 후보·PUBLIC NOT_POSTED, 부분 자체시험/독립 리뷰·호스트 미완료. parser 기본 sdm2-parser 후보, 첫 배송도 PUBLIC 루트 |
| 새 창·스킬 발견 | [발견 CURRENT](projects/COWORK-SKILL-DISCOVERY-20261112-001/CURRENT.md) | 이 브리프·고정 진입 문서 적용 범위. 상세 원문은 관련 기능만 추가 확인 |

CL/PR: [설계안](projects/L1-WORKSPACE-RAG-20261111-001/CL_PR_ISSUE_ANALYSIS_DESIGN_BRIEF_r0001_20261114.md) · [독립 리뷰 요청](projects/L1-WORKSPACE-RAG-20261111-001/CLAUDE_CL_PR_ISSUE_ANALYSIS_DESIGN_REVIEW_REQUEST_r0001_20261114.md). 요청서 존재는 실행 증거가 아님. [업무용 GPT 인계 r0005](https://github.com/wonhwipark/L1Work/blob/main/handoffs/L1_KNOWLEDGE_UPDATER_WORKFLOW_INHOUSE_HANDOFF_r0005_1111.md)는 기존 경로 유지.

- **Work→Knowledge 설계 리뷰:** [요청서](projects/L1-WORKSPACE-RAG-20261111-001/CLAUDE_WORK_TO_KNOWLEDGE_DESIGN_REVIEW_REQUEST_r0001_20261114.md)의 `L1-WORK-KNOWLEDGE-DESIGN-20261114-001`는 기존 CL/PR 리뷰와 별개. 사용자 지시로 요청 문서 등록, Windows 전달 `NOT_VERIFIED` / 리뷰 `PENDING_EXECUTION` / 결과 미수신. 이 브리프 변경만으로 자동 리뷰·유료 CLI를 실행하지 않음.

## 5. 최신성·진입·갱신 규칙

1. 위 상태는 출처 기준 시점의 스냅샷. 관련 CURRENT의 현재 요약·새 결과·열린 메모를 확인한 뒤 판단. 첫 ## 현재 요약 우선, 오래된 문서의 끝에 더 새 기록이 있으면 날짜·근거로 대조.
2. 아래 source blob과 최신 main의 해당 파일이 다르면 **그 영역 요약은 재확인 대상**. bot 대시보드 등 무관한 파일만 바뀐 것을 전체 정책 변경으로 취급하지 않음. 출처 불명/조회 불가 상태를 PASS로 보완하지 않음.
3. source CURRENT/정책/카탈로그를 바꾸는 작업은 이 파일의 관련 요약·확인일·source blob도 함께 갱신하거나 해당 영역을 확인 필요로 표시. 상태 DB나 새 원장을 만들지 않음.
4. 읽기 기본은 브리프+관련 CURRENT. 쓰기/배포/실행 판단에 필요한 계약·실제 스킬 원문은 추가 확인. 모든 계약·18개 감사·이미 완료된 G0를 매번 반복하지 않음.
5. 문서 연결을 읽는 세션에 적용. **프로젝트 설정·새 창 백그라운드 자동 선조회 기능을 이 작업으로 변경하지 않음.** GitHub 조회 권한·도구가 있는 새 창에서 이 경로를 요청하면 사용.
6. 최소 시작 요청: PRIVATE wonhwipark/CoWork-Skill-Collab의 main에서 collab/CONTEXT_BRIEF.md를 먼저 읽고, 내 요청에 맞는 CURRENT와 열린 메모를 확인해 기존 스킬을 재사용해 진행해줘.

### 확인한 source blob

약어 경로는 모두 `collab/` 기준. Git blob은 문서 버전 pin이며 시험 PASS를 뜻하지 않음. 기존 원문은 위 기준 commit에서 확인, 마지막 4행은 브리프와 같은 게시에서 문서 포인터/요약을 정정한 버전이다.

| 출처 | Git blob |
|---|---|
| projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md | `2fd68858d4902ac2f888a7351f84b0540ef16917` |
| projects/L1-WORKSPACE-RAG-20261111-001/L1_KNOWLEDGE_FEEDBACK_DISPOSITION_r0001_20261114.md | `16b522a61be3c8c4257d42491ad0f22679de053b` |
| projects/L1-CHANNEL-KNOWLEDGE-SCOPE-20261113-001/CURRENT.md | `54bde1ac3e22ff53e1c306f148886f103563e361` |
| projects/COWORK-GITHUB-DASHBOARD-20261111-001/CURRENT.md | `debd9d81d1d4fd828139ec7e1197a47ec4c4de02` |
| projects/L1-WORKSPACE-RAG-20261111-001/CL_PR_ISSUE_ANALYSIS_DESIGN_BRIEF_r0001_20261114.md | `b7838b5e86e3c88d322c5111ffccee0a4e835456` |
| projects/ISSUE-ANALYZER-20261114-001/CURRENT.md | `466d4967b75074693a95797c47463f607767bdda` |
| knowledge/SKILL_CAPABILITY_CATALOG.md (r0005, 운영 경로 보강) | `483d62e2ad95ae074ab9119f2ec591331975639f` |
| projects/L1-WORKSPACE-RAG-20261111-001/CURRENT.md (이번 Work→Knowledge 리뷰 요청 연결) | `f1f6716534247b27313ebbfa222fa7f8079b6599` |
| projects/JOBLIST-NRTX-20261112-001/CURRENT.md (동시 요약 정정) | `c8f0c02f8a3825563f4389c68fbad9485d4dadcf` |
| START_HERE.md (기존 진입 연결) | `0ea7951af62a1d90387b330181cc4304e1c4d99e` |
| ops/CONTRACTS/EXECUTION_PROMPT_TERMINOLOGY_V1.md (r0002 역할 용어) | `8905149948a7021d1e7013b7d1ee85c87997d8a4` |
| projects/L1-WORKSPACE-RAG-20261111-001/L1_WORK_TO_KNOWLEDGE_FLOW_r0001_20261114_KST.md | `fa6b02e1628186f38165bfee2e0699c6640bd6f0` |
