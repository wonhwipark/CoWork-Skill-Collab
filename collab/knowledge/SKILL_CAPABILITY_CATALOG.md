# CoWork 공통 스킬 기능 목록

- 개정: r0001 / 2026-11-12 KST
- 목적: 사용자가 스킬명을 말하지 않아도 요청 기능에서 기존 재사용 후보를 찾는 시작용 목록.
- 범위: 기존 비민감 GitHub 문서와 사용자 대화에서 언급된 후보의 연결. **18개 전체 확정 목록·최신 버전 감사·설치본 기능 검증은 아니다.**
- 최신 작업 상태: [CURRENT](../projects/COWORK-SKILL-DISCOVERY-20261112-001/CURRENT.md)
- 적용 절차: [발견·재사용 계약](../ops/CONTRACTS/SKILL_DISCOVERY_AND_REUSE_V1.md)
- 아래 입출력은 책임을 설명하는 요약이며 실제 함수명·CLI·API·저장 필드를 정의하지 않는다.

## 근거와 해석

| 코드 | 이번에 읽은 근거 | 원본·검증 한계 |
|---|---|---|
| C1 | [L1 공통 참고](L1_WORKSPACE_RAG_COMMON_r0001_20261111.md) §3·5·7 | 기존 문서의 역할·과거 감사 요약. 이 회차에 18개 ZIP 또는 설치본을 다시 확인하지 않음 |
| C2 | [r0005 후속 메모](../projects/L1-WORKSPACE-RAG-20261111-001/notes/L1_KNOWLEDGE_R0005_FOLLOWUP_MEMO_20261112.md) §2 | 재사용 책임의 검토 기준. 실제 호출 계약은 미확인 |
| C3 | [Job-list/Skill-Updater 전달 계약](../ops/CONTRACTS/JOBLIST_PUBLIC_DELIVERY_V1.md) §1~3·6 | 전달·설치·Job·분석·게시 상태를 분리. 실제 호스트 성공 근거가 아님 |
| U1 | 2026-11-12 사용자 대화의 autotask-builder 언급 | 명칭·별칭 발견 단서. 정식 SKILL 원문·원본 경로·OS별 지원은 미확인 |

기준 조회 commit: `fb5402fdec4412703670a995f46fc9244170d710` (PRIVATE main의 조회 시점). C1~C3의 해당 commit 원문을 근거로 삼는다. 이후 기능·버전 판정에는 최신 원본과 해당 프로젝트 CURRENT를 다시 확인한다.

이 표의 한국어 이름은 검색용 설명이다. 패키지 공식 alias 등록이나 설치 여부를 뜻하지 않는다.

## 기능·입출력·연결 후보

| 스킬명 / 검색용 별칭 | 먼저 검토할 기능 | 입력 → 출력 요약 | 연동 후보·책임 경계 | 근거·원본 확인 상태 |
|---|---|---|---|---|
| `l1-fix-workflow` / Workflow, 워크플로우 | 요청 해석·기존 Work 선택/재개·분석 조율 | 작업 의도·기존 Work → 작업 흐름·분석 요청 | Kernel, analyzer, Knowledge Updater. 기존 순수 스터디 경로에 새 Work를 강제하지 않음 | C1/C2. 원본은 승인된 기존 패키지·설치 SKILL에서 확인 필요 |
| `work-ledger-kernel` / Kernel, 작업 원장 | Work/Evidence 정본·허용 registry·파생 export | 허용된 작업/근거 → 원장·참조·파생 문서 | Workflow가 재사용. 새 원장·임의 kind/provider/schema 추가를 가정하지 않음 | C1/C2. registry·설치 API는 별도 확인 |
| `code-analyzer` / 코드 분석기 | 고정 소스의 코드 사실·분석 근거·AS-IS MSC 후보 | source revision·scope → facts·anchor·분석 artifact | l1-github/P4, Workflow, doc-converter. 변환 출력만으로 분석 검증 PASS 아님 | C1/C2. 기존 CURRENT의 패키지 참고명 `code-analyzer_v0_15_2_1107.zip`; 최신/설치 버전 재확인 안 함 |
| `issue-analyzer` / 이슈 분석기 | 이슈 원인·근거 정리의 기존 경로 | 이슈 자료·근거 → 분석 결과 | Workflow, code-analyzer, 기존 지식 검색. 상세 지원 I/O는 원문 확인 후 결정 | C1/C2. 원본 경로·API 미확인 |
| `doc-converter` / 문서 변환기, MSC 변환기 | 기존 MSC 변환·표현·participant 가독성 규칙 | 분석 artifact·표현 규칙 → 변환 문서/MSC 표현 | code-analyzer의 사실·AS-IS/TO-BE·출처를 보존. Updater에 변환기를 중복 구현하기 전 검토 | C1/C2/C3. 정확한 규칙·설치 호출은 추가 확인 |
| `hld-composer` / HLD 작성 | 기존 HLD 구성 기능 | 설계/분석 자료 → HLD 후보 | analyzer·doc-converter·Updater. 자동 호출 가능 여부는 원문 확인 | C1 §7의 후보. 실제 I/O·원본 경로 미확인 |
| `l1-github` / GitHub, Git 기여 워크플로우 | 저장소 역할·branch/revision·변경 근거·기존 게시/조회 | 요청 scope·Git 상태 → 고정 소스/변경 근거·조회 결과 | analyzer, Kernel, 기존 writer. 단순 조회는 기존 thin path 우선; 기능명만 보고 CAS 지원 확정 금지 | C1/C2. 기존 CURRENT의 참고명 `l1-github_v0_3_56_1110.zip`; 최신/설치 버전 재확인 안 함 |
| `p4-code-owner` / P4 근거·담당 분석 | P4 파일 revision·Fix CL·통합 귀속의 기존 근거 | 승인된 P4/Jira 자료 → 근거·귀속 후보 | analyzer, Workflow. owner/통합 판정을 원인·수정시험 PASS와 구분 | C1/C2 및 기존 CURRENT. 참고명 `p4-code-owner_v0_6_7_1012.zip`; 실제 설치 계약 미확인 |
| `job-list` / Job, 잡리스트 | 승인된 작업 목록·실행 gate·결과/영수증 경로 | 유효 Job·profile·승인 → 실행 후보·결과/영수증 | 기존 driver·Skill-Updater. 예약 시점의 소유자와 작업 내용의 소유자를 구분 | C1/C2/C3. 이번 작업에서 Job/API 실행 없음 |
| `skill-updater` / Skill-Updater, 패키지 갱신 | 승인된 ZIP 발견·다운로드·설치 경로 | 승인된 버전 ZIP·정책 → 설치 후보·호스트 설치 결과 | job-list·기존 OS 예약 경로. ZIP 게시와 설치/Job 실행은 별도 | C3. 원본 SKILL·OS별 hook·설치본 미확인 |
| `autotask-builder` / 오토 타스크 빌더, 예약 작업 | 예약 실행이 필요한 요청의 우선 확인 후보 | 일정·실행 대상 → 예약 정의/검증 여부 확인 대상 | job-list, skill-updater와 연결 가능성 확인. 실제 등록·OS·지원 명령은 원문 전 확정 금지 | U1. 정식 명칭·원본 위치·I/O 미확인; 사용자에게 이름을 다시 묻기 전 기존 자료를 탐색 |
| `skillsilent` / SkillSilent, 스킬 사일런트 | 기존 허용 action·실행 정책 관련 확인 후보 | 허용 action/정책 → 실행 가능 여부는 계약 확인 대상 | job-list·기존 driver. 승인 우회나 자동 허용의 근거로 사용 금지 | C1은 독립 ZIP 미발견, C3은 등록된 비파괴 action 언급. 설치 부재/기능 부재로 단정 금지 |
| `l1-knowledge-updater` / L1 Knowledge Updater, 지식 Updater | 지식 분류·후보·중복/충돌·Preview·승인·writer 조율 | facts/기존 지식·근거 → 지식 후보·게시 판정 | Workflow/Kernel/analyzer/converter·기존 writer 재사용. `skill-updater`와 목적이 다름 | C2/C3 및 r0005 계약. 실제 설치 I/O·writer 보장 미확인 |

원본 위치가 미확인인 행은 먼저 기존 목록·패키지·설치 문서를 필요한 범위에서 찾는다. 검색 실패를 기능 부재로 바꾸거나 임의 API/stub를 만들지 않는다. 이 목록은 원본을 대체하지 않는다.

## 요청 표현에서 먼저 찾을 후보

| 사용자 요청의 기능 | 우선 확인할 기존 후보 | 후속 확인 |
|---|---|---|
| 현재 브랜치 동작·MSC·시나리오 | l1-github/P4 → code-analyzer → doc-converter | source 적용성·분석 근거·participant/변환 규칙 |
| 이슈 원인·수정 이력·기술 지식화 | issue-analyzer, Workflow/Kernel, Knowledge Updater | 원인 검증·수정·시험·게시 승인 상태를 분리 |
| HLD·설계 설명·문서 출력 | hld-composer, doc-converter | 설치본 지원 형식·AS-IS/TO-BE·근거 보존 |
| 정해진 시각/주기에 기존 작업 실행 | autotask-builder, job-list, skill-updater | 각 원문의 예약·실행·설치 책임과 승인. 이 표가 예약을 실행하지 않음 |
| Work 재개·결과 추적·문서 탐색 | Workflow, Kernel | 기존 Work·원장·Exporter 재사용 |
| 스킬 ZIP 갱신 | skill-updater 및 기존 배포 계약 | 최종 ZIP·공개 승인·호스트 설치 결과 |

## 보강·유지 원칙

- 새 작업은 요청 기능으로 후보를 고르고 관련 원문만 읽는다. 사용자가 모든 스킬명을 알려줘야 시작하는 방식으로 운영하지 않는다.
- 문서 언급, 패키지 존재, 패키지 원문 확인, 격리 시험, 호스트 설치 사실, 실제 호출 성공을 별도로 기록한다. 근거가 없는 상태는 UNKNOWN/NOT_VERIFIED다.
- 사용자 요청으로 **18개 전체 원문·PRIVATE 대조는 다음 별도 작업으로 보류**했다. 이 회차에 18개 전체 검증 완료·목록 완전성·최신 설치 버전을 주장하지 않는다.
- 다음 대조에서는 기존 감사 자료와 허용된 정본을 사용해 정확한 이름/원본 위치/기능/버전 근거를 이 표에 보강한다. 별도 DB·엔진·자동 감시를 신설하지 않는다.
