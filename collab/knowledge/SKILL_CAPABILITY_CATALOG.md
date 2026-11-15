# CoWork 공통 스킬 기능 목록

- 개정: r0007 / 2026-11-15 KST (책임·입출력·연결 지도와 실행 상태 분리; 패키지 재감사 아님)
- 새 창은 [공통 맥락 브리프](../CONTEXT_BRIEF.md) → 해당 CURRENT를 먼저 읽고 필요한 상세 기능을 이 목록에서 확인.
- 대상: 사용자 확인한 관리 스킬 18개 + 별도 업무용 연동 스킬 1개. 전체 보유 스킬의 완전성·최신 설치 버전을 뜻하지 않음.
- [이번 패키지 정적 확인·SHA-256·원본 위치](../projects/COWORK-SKILL-DISCOVERY-20261112-001/SKILL_18_PACKAGE_AUDIT_20261112.md) · [최신 상태](../projects/COWORK-SKILL-DISCOVERY-20261112-001/CURRENT.md) · [시작·재사용 절차](../ops/CONTRACTS/SKILL_DISCOVERY_AND_REUSE_V1.md)
- 근거: 17개 실제 공개 ZIP의 SKILL 문서 정적 확인. 실제 구현/API/설치·호스트 실행은 미검증. 입출력은 책임 요약이며 새 함수·필드 정의가 아님.

**유지보수:** 스킬 책임·입출력·연결 계약·근거 위치가 달라질 때 갱신한다. 최신 패키지 버전·호스트 설치·리뷰·배포 상태는 해당 작업 CURRENT에서 읽는다. 과거 패키지 감사의 버전 불일치는 그 감사 시점의 근거이며 현재 상태로 복사하지 않는다.

| 번호 | 스킬 / 검색용 별칭 | 입력 → 출력·기능 | 연동 후보 | 경계·미확인 |
|---:|---|---|---|---|
| 1 | `issue-analyzer` / 이슈 분석기 | SDM/TXT/로그·증상 → 원인 근거·분석 보고·승인 수정 인계 | code-analyzer, code-fix, 지식 provider | 로그 경로 요청·과거 사례 재사용; 변환/분석은 기존 pipeline |
| 2 | `code-analyzer` / 코드 분석기 | 고정 소스·scope → CODE FACT·call flow·MSC/HLD 입력 | l1-github, p4-code-owner, hld-composer, doc-converter | 코드 사실의 책임자; 지식 링크 등록은 Provider 호출 성공 아님 |
| 3 | `code-fix` / 코드 수정 | 분석 결과·CL·변경 요청 → 승인 계획·수정·shelve·as-built 보고 | issue-analyzer, code-analyzer, l1-github | 승인된 anchor 수정만; shelve와 submit 분리 |
| 4 | `l1-fix-workflow` / 워크플로우 | 요청·기존 Work → Work 흐름·연속성·계획 조회 | work-ledger-kernel, analyzer, 지식 provider | 기존 Work 선택·재개 우선; 버전·배포 적합성은 해당 CURRENT와 원문 확인 |
| 5 | `work-ledger-kernel` / 작업 원장 | Work·Evidence·승인 → 결정형 상태·staleness·resume/transfer guard | l1-fix-workflow | Work/Evidence 정본; registry/schema 임의 확장 금지 |
| 6 | `hld-composer` / HLD 작성 | 분석 결과·SRS/HLD → 통합/Target HLD·review ledger·gate | code-analyzer, doc-converter | 전진 설계와 코드 기반 역설계 분리; HLD gate는 실제 구현 검증과 별개 |
| 7 | `doc-converter` / 문서·MSC 변환 | MD/HTML/XHTML·scenario IR → 변환 문서·PUML/SVG·검증/manifest | code-analyzer, hld-composer | SOURCE_PARENT_DIR_V1·stack_group·근거 trace 보존; AS-IS fact를 스스로 승인하지 않음 |
| 8 | `hld-code-compare` / 설계 코드 비교 | 복수 HLD·소스/facts → gap_report.yaml·gap_summary.md | code-analyzer, hld-composer, hld-code-implement | MSC는 procedure evidence, draw.io는 supporting evidence; 동등 근거로 취급 금지 |
| 9 | `hld-code-implement` / 설계 구현 | 승인된 gap → sealed scope·FU별 diff·impl_record·P4 shelve | hld-code-compare, hld-composer, doc-converter | G1/G2 승인·최종화 계약; 구현과 HLD 누락 보완 구분 |
| 10 | `l1-github` / Git/GitHub | 저장소·branch/PR·요청 → Git 근거·안전 작업·command journal | code-analyzer, Workflow, l1-cl2git-merge | thin native read 우선; 단일 writer·fork 안전 경계 |
| 11 | `p4-code-owner` / P4 이력 | 파일/API·Jira Fix CL 후보 → 실제 수정자·branch 반영·Postmortem 선별 | issue-analyzer, Workflow | 읽기 전용; 실제 수정자를 공식 module owner로 승격 금지 |
| 12 | `l1-cl2git-merge` / CL→Git 충돌 처리 | 자동 생성된 upstream Open PR·P4 CL → 검증·충돌 해결·pre-push 결과 | l1-github, P4 provider | 일반 이관 엔진 아님; 버전 정합성은 실제 패키지와 해당 작업 근거로 확인 |
| 13 | `l1-sam-fixer` / SAM LOC/MCD | 공식 CSV/HTML → LOC/MCD 분석·수정 후보·보고·검증 shelve | code-analyzer, 지식 provider, P4, build provider | CC/동적 지표 범위 밖; 옛 knowledge-manager 참조와 현재 provider 매핑 추가 확인 |
| 14 | `skill-updater` / 스킬 갱신 | 승인된 공개 ZIP·정책 → 격리 설치·자체시험·롤백 결과 | 기존 OS 예약·Bootstrap, job-list 승인 경로 | 스케줄·런타임 orchestration 미소유; 자체 갱신 별도 Bootstrap 승인 |
| 15 | `skillsilent` / 실행 게이트 | 등록 action·정책 → 허용된 실행/차단 (독립 원문 미확인) | 각 패키지의 manifest/policy | 독립 ZIP 미발견; 패키지 내 policy 존재와 실제 gateway 설치는 별개 |
| 16 | `job-list` / 잡리스트 | 승인 profile/Job → dispatcher·one-shot 결과/영수증 | skill-updater, 승인된 worker/driver | 승인된 Job/profile·Runner·결과를 구분; 실제 버전·활성 Job은 해당 CURRENT와 호스트 근거로 확인 |
| 17 | `autotask-builder` / 예약 작업 | task YAML·일정 → 검증·OS 작업 정의·deploy/status | 공개 child launcher, skill-updater, l1-cleanup | Windows Task Scheduler/Linux user timer; OS 예약만 소유, Job queue/state 불변 |
| 18 | `l1-cleanup` / 정리·보존 | 대상/정책 → audit·plan·HTML/JSON·승인 격리/복구 | autotask-builder, 유효 artifact receipt 제공자 | 기본 조회; OpenCode DB 삭제·purge는 별도 승인; receipt 자동 연동은 미구현 표기 |
| 19 | `l1-knowledge-updater` / 지식 Updater | Procedure/Feature 직접 분석 요청 또는 기존 Workflow Work → 개인 Workspace의 분석·초안·근거 보존 + 검증 지식의 그룹 공용 `l1sw-dev-knowledge` 반영 후보 | 기존 analyzer·converter·Workflow/Kernel의 Work 기록·기존 게시 경로 | 두 진입 모두 같은 Work 보존이 설계 요구. 실제 저장/readback·그룹 반영 구현/API·G0·통합 검증은 L1 CURRENT에서 확인 |

지식 연결 설계: [두 진입·개인 Workspace 보존·그룹 반영 r0002](../projects/L1-WORKSPACE-RAG-20261111-001/L1_WORK_TO_KNOWLEDGE_FLOW_r0002_20261115_KST.md). 그룹 공용 스킬과 그 관리 지식의 실제 저장 위치를 구분하며 동명 GitHub.com 저장소로 추정하지 않음.

## 실제 운영 경로와 스킬의 역할 매핑 — 사용자 보고, 호스트 영수증 미검증

```text
모바일 Agent → Linux MCP
  ├─ 기존 Work 검색·재개 요청 → l1-fix-workflow → work-ledger-kernel
  └─ 신규 Job-list 구성 필요
       ├─ 설치·갱신 필요 시 skill-updater 1회 수행 요청
       └─ 승인된 job-list 등록/활성화/Runner/실행 LLM → 결과·영수증 조회
                    ↳ 필요 시 업무 GPT의 검토 → l1-workspace Evidence
                      → l1-knowledge-updater 지식 후보/Preview
```

- `모바일 Agent`는 요청·조회, `Linux MCP`는 인터페이스, `skill-updater`는 승인된 패키지 설치·검증, `job-list`는 승인 Job/Runner, `l1-fix-workflow`/Kernel은 Work·Evidence를 소유한다. **skill-updater가 Job을 직접 실행하거나 MCP가 자동 지식 게시한다고 가정하지 않는다.**
- 신규 Job마다 무조건 Updater를 실행하는 규칙이 아니다. 필요 시 **단발 실행 요청**과 실제 적용 결과, Registry 활성화, Worker 시작, 분석 완료, 결과 조회를 별도 기록한다. 기존 소비된 one-shot은 임의 재실행하지 않는다.
- 정확한 Linux MCP tool/승인/실행·영수증은 요청 목적에 맞는 CURRENT와 호스트 근거로 확인한다. [Job-list 진단](../projects/JOBLIST-NRTX-20261112-001/CURRENT.md), [NR 실제 분석](../projects/NR-L1TX-CODE-ANALYSIS-20261115-001/CURRENT.md), [Smoke](../projects/JOBLIST-SMOKE-20261114-001/CURRENT.md)를 구분하며 유사 사용 경험을 현재 E2E PASS로 승격하지 않는다.
- 공통 역할 표기는 **설계 GPT / 업무 GPT / 실행 LLM / 모바일 Agent**로 통일하고, [실행 프롬프트 용어 계약](../ops/CONTRACTS/EXECUTION_PROMPT_TERMINOLOGY_V1.md)을 따른다.

## 요청 기능에서 후보 찾기

| 요청 | 먼저 검토할 후보 |
|---|---|
| 로그·원인·수정 | issue-analyzer → code-analyzer/code-fix |
| 현재 코드 동작·MSC | l1-github/P4 근거 → code-analyzer → doc-converter |
| HLD·설계/구현 차이 | hld-composer → hld-code-compare → 승인된 hld-code-implement |
| Work 재개·이력 | l1-fix-workflow + work-ledger-kernel |
| P4 CL의 Git PR 충돌 | l1-cl2git-merge + l1-github |
| SAM LOC/MCD | l1-sam-fixer |
| 주기 실행·패키지 갱신 | autotask-builder의 OS 예약 / skill-updater의 설치 / job-list의 승인 Job을 구분 |
| 산출물·디스크 정리 | l1-cleanup의 audit/plan부터 확인 |
| 지식 스킬 업데이트 | l1-knowledge-updater와 기존 분석·변환 기능의 연결 검토 |

## 재사용 판단

요청 기능으로 후보를 찾고 프로젝트 CURRENT·열린 메모·관련 원문을 확인한다. REUSE / CONNECT / 입증된 최소 EXTEND / DEFER·추가 확인을 판단하며 사용자가 스킬명을 알려줄 때까지 기다리지 않는다. 미확인 API·record는 구현 대상으로 확정하지 않는다.

G0 설치 사실과 G1 가정을 분리한다. SourceSnapshot·CAS·N:M·복구는 기존 Kernel/Updater/Git 제공자 우선. K5.8은 설계표만, 기존 Knowledge/metadata 변경 금지. 문서·ZIP 확인·호스트 설치·실호출·독립 리뷰를 구분한다. [r0005 후속 최신 판정](../projects/L1-WORKSPACE-RAG-20261111-001/L1_KNOWLEDGE_FEEDBACK_DISPOSITION_r0001_20261114.md)은 G0 일부 확인 보고 수신을 반영한다. 실제 저장·source/MSC/Evidence·게시/AI 활용은 첫 승인된 분석 후속이며 현재 분류·연계 설계의 누락/완료 차단으로 취급하지 않는다. 전체 설치/API·독립 리뷰 PASS는 아님.

[개선 검토](../projects/COWORK-SKILL-DISCOVERY-20261112-001/NEW_CHAT_CONTEXT_BOOTSTRAP_REVIEW_r0001_20261114.md)의 통합 브리프·고정 진입 문서 경로 적용. 자동 로더·프로젝트 설정·스킬 원문 변경 없음.
