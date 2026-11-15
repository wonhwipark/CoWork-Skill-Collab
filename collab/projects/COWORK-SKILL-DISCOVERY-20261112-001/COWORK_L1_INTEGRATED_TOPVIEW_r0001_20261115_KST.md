# CoWork 협업 × L1 업무·지식 — 통합 탑뷰 및 인계 계약 r0001

- 기준: 2026-11-15 KST / GPT 공통 투두 TD-001 / 기존 Work `COWORK-SKILL-DISCOVERY-20261112-001`
- 권위: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`
- 성격: **비민감 문서의 현행 목표 아키텍처·정본 책임·인계·검증 경계**. 현재 LIVE/provider/버전·설치·승인·실험 결과의 정본이 아님.
- 단일 상단 전체 흐름도는 [공통 지도](../../CONTEXT_BRIEF.md)에 1개만 유지. 이 문서는 그 흐름의 의미·입출력·판정 기준을 상세화하며 그림을 중복 등록하지 않음.
- 선행: [D01~D10 상세 TODO](COWORK_L1_INTEGRATED_CONTEXT_DESIGN_TODO_r0001_20261115_KST.md), [기존 L1 r0002 아키텍처](../L1-WORKSPACE-RAG-20261111-001/L1_E2E_INHOUSE_OFFSITE_ARCHITECTURE_r0002_20261111.md), [Work→Knowledge 흐름](../L1-WORKSPACE-RAG-20261111-001/L1_WORK_TO_KNOWLEDGE_FLOW_r0001_20261114_KST.md), [발견·재사용 계약](../../ops/CONTRACTS/SKILL_DISCOVERY_AND_REUSE_V1.md). 위 고정 과거 문서/고정 리뷰 입력은 삭제·재작성하지 않음.

## 1. 두 작업 층과 연결의 의미

| 구역 | 순서·주 책임 | 출력·다음 입력 | 무엇을 뜻하지 않는가 |
|---|---|---|---|
| CoWork 협업 개발/리뷰 | 요구 → 기존 CoWork Work 선택 → 허용된 개발·자체시험 → 후보 고정 → 분리된 Windows Claude Code 독립 리뷰 → GPT 판정 | 비민감 설계/후보·시험·리뷰·영수증과 해당 Work CURRENT | 단순 후보 작성·문서 게시를 자동 리뷰/독립 PASS로 간주하지 않음 |
| 협업 전달/운영 | 승인된 RELEASE → PUBLIC L1Work 최종 ZIP 또는 허용 인계 MD → 별도 호스트 설치/호출/수신 검증 | 승인된 배포본·정확한 버전/해시·호스트 적용 증거 | PRIVATE 게시가 업무 호스트 설치/Job 성공이 아님. provider LIVE와 자동 서명 개선의 상태는 서로 다름 |
| L1 업무 실행 | 업무 GPT/Agent가 기존 업무 Work 선택 → Workflow/Kernel 및 코드 분석·변환 스킬로 출처 고정 분석 → Evidence·결정 기록 | 업무 `l1-workspace`의 원본 Work/Evidence, source revision·근거·미확인 | Windows 리뷰어가 회사 L1 코드를 직접 읽거나 CoWork가 업무 Work 정본을 소유하는 뜻이 아님 |
| L1 지식화·활용 | 같은 업무 Work의 후보 → Updater 대조/Preview → 유효 승인·기존 writer → 팀 지식 정본 게시/readback → 원래 Work 역링크 → 재사용/RAG 별도 검증 | 업무 `l1sw-dev-knowledge`의 검증된 기술 본문과 게시 revision, 원래 Work 참조 | Preview·분류 완료=지식 게시 아님, 게시=실제 검색/RAG Provider 본문 소비 아님 |
| 피드백 회수 | 문서/스킬/분석/지식/운영 중 책임 구분 → 같은 목적 기존 Work 보완·판정 → 정본 readback → 다음 창 재개 | 해당 Work CURRENT의 다음 행동과 고정된 근거 참조 | 이슈마다 신규 Work·새 스키마/원장/자동화 만들지 않음 |

**연결선은 책임·데이터 전달의 목표 관계**이며 자동 호출 인터페이스의 실존 증거가 아님. `REUSE → CONNECT → 실제 GAP 입증 시 최소 EXTEND` 순서로 진행.

## 2. 정보별 단일 정본과 갱신 조건 (D01/D07)

| 정보 | 유일한 정본/조회 | 갱신 주체와 계기 |
|---|---|---|
| 전체 고정 지도·목적별 진입 | `collab/CONTEXT_BRIEF.md` | GPT, 구조·역할·경로·Work 진입 경로가 바뀌었을 때만 |
| 공통 개선 후보·우선순위·검토 의견 | `collab/GPT_TODO.md` | GPT, 후보 등록/실행 연결/판정이 달라질 때 |
| 개별 CoWork 실행·승인·다음 행동 | 해당 `collab/projects/<WORK_ID>/CURRENT.md` | 담당 GPT/Agent, 실제 판정·새 결과 발생 시 상단 요약 갱신 |
| 상세 결과·결정·리뷰·영수증·열린 메모 | 해당 기존 결과/결정/리뷰/receipt/notes 경로 | 실제 수행자·검증자, 원문과 고정 입력·근거 보존 |
| 스킬 책임·입출력·기본 연결 | `collab/knowledge/SKILL_CAPABILITY_CATALOG.md` | GPT, 실제 스킬 계약/탐색 포인터 변경 때만 |
| 파생 상태·대시보드 | 기존 TRACKER와 허용된 exporter/공개 상태 | 기존 데이터의 검증된 파생. CURRENT를 대체·역쓰기하지 않음 |
| 업무용 Work/분석·Evidence | 업무용 `l1-workspace`의 해당 Kernel Work | 업무 GPT/실행 Agent/Kernel 허용 기록. GitHub.com의 동명 저장소로 추정 금지 |
| 검증된 L1 기술 내용·MSC·HLD·이슈 지식 | 팀 `l1sw-dev-knowledge` | 유효 승인과 기존 writer의 실제 게시/readback. 검증된 상세 설계·AS-IS MSC 포함 가능 |
| LIVE provider·운영 롤백·미정산 | [이관 CURRENT](../COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md) + 실제 호스트/리뷰 영수증 | 해당 운영 Work 담당. 이 통합 문서에 provider 값을 고정하지 않음 |
| 자동 승인·서명 개선 | [자동 승인 CURRENT](../COWORK-AUTO-APPROVAL-20261115-001/CURRENT.md) + 보호된 운영 위임 정책 | 해당 개발·운영 Work. GitHub 문서의 승인 주장만으로 서명 권한 없음 |

## 3. 책임·단계·검증 경계 (D03/D04)

- **GPT:** 요구 범위·같은 Work 선택, 접근 가능한 개발/문서/시험, 리뷰 결과 독립 판정, 원격 정본 게시·검증. 독립 Claude 결과를 GPT 자체검토로 대체하지 않음.
- **Windows Claude Code:** 명시적 독립 리뷰어 또는 허용된 로컬 개발/시험 담당. 같은 개발 세션의 자기 시험은 별도 독립 리뷰가 아님. L1 원본 소스 접근을 가정하지 않음.
- **Python watcher:** 기존 활성 provider에서 유효한 고정 REQUEST + 실제 보호된 서명/승인 + READY(마지막 게시) + 비용·만료·중복 검사 통과 시에만 리뷰 수행. 승인되지 않은 유료 재호출 금지.
- **업무 GPT/Agent/Linux MCP:** 허용된 도구·프로필·원본 기준으로 실제 코드/문서 분석 및 결과/receipt 조회. CoWork GitHub 문서 게시만으로 호스트 실행 시작 안 됨.
- **Workflow/Kernel:** 요청 분류, 기존 업무 Work 검색/재개, 작업·결정·Evidence 소유. 별도 지식 원장 신설 금지.
- **code-analyzer/issue-analyzer 및 doc-converter/hld-composer:** 기존 코드·이슈 사실과 HLD/MSC 산출물. 코드 검증 없이 MSC를 확정 사실로 게시하지 않음.
- **Knowledge Updater/기존 writer:** 후보·중복/충돌·Preview·보완·게시 승인/게시 revision/readback·역링크 조정. 직접 코드 분석 도구의 자동 대체 또는 신규 게시 엔진으로 단정하지 않음.

**정책 최신성:** r0001/r0002 L1 설계에 남아 있는 이전 provider·개인/그룹 상세 분리 문구는 작성 당시 상태. 현재 그룹은 검증된 상세 HLD·설계·AS-IS MSC를 포함할 수 있고, 개인 Workspace는 분석 이력·초안·Evidence를 보존. 실제 운영 provider는 항상 이관 CURRENT 상단과 영수증 확인. 고정 리뷰 입력 ZIP/과거 설계 파일은 수정하지 않음.

## 4. 최소 인계표 — 기존 포맷에서 의미만 매핑 (D05)

| 구간 | 생산자 → 소비자 | 반드시 추적할 의미 | 실제 소유·확인 위치 |
|---|---|---|---|
| CoWork 작업 시작 | GPT → 기존 CoWork Work | 작업 목표, Work ID, 기존 CURRENT, 고정 입력 revision, 변경 파일/기존 결함, 완료 조건 | CoWork CURRENT/설계/결정 |
| 독립 리뷰 | 개발자 → 별도 Claude 리뷰어 | reviewer 대상 ZIP/문서 원본 bytes·SHA/크기, 요청 ID/rev, 비용 상한/유효 승인, 결과·영수증 | PRIVATE 정식 REQUEST/READY·review/receipt; signer·watcher는 운영 계약 |
| 릴리스·수신 | GPT/패키지 → PUBLIC / 업무 실행자 | 승인된 ZIP 해시·실제 게시 commit, 설치 해시, Worker/Job ID, 결과/receipt readback | PUBLIC 원본·호스트 실측은 각자 별도 |
| 분석 실행 | Workflow/Kernel → analyzer/converter | 업무 Work ID, Git SHA 또는 P4 haveRev, 대상 module/feature/scenario, 소스 scope, 결과·Evidence 근거 | 업무 Work와 원본 SCM; CoWork에는 허용된 비민감 상태만 |
| 지식 후보 | 기존 업무 Work → Updater | 업무 Work ID(≠ CoWork Work), 원본 Artifact/Evidence, source pin, 검증 상태, 개인 유지/그룹 게시 의도 | 업무 Work/Updater 기존 기능 |
| 보완 회수 | Updater → Workflow/원래 Work | 부족한 주장·대상 근거·수정 범위·완료 조건, 이전 후보·Work 참조 | 원래 Work. 중복 분석/Work 생성 방지 |
| 지식 게시·연결 | 기존 writer/Updater → Knowledge/원래 Work | 승인된 변경/기준 revision, 실제 게시 revision·readback, Work별 역링크 상태 | 팀 정본 + 업무 Work 둘 다 각각 확인 |

위 내용은 **인계 의미**이지 신규 필수 JSON 필드/API/Kernel stage 확정이 아님. 코드·로그·상세 MSC·고객자료·토큰·개인키 등 반출 금지 원본은 CoWork PRIVATE/PUBLIC에 게시하지 않음.

## 5. 피드백 분기와 중복 방지 (D06)

| 실제 피드백 | 판정·보완 | 다시 확인할 근거 |
|---|---|---|
| 문서/경로 오류 | 수용/수정 수용 후 소유 Work의 문서·CURRENT만 정정. 경로 구조 변화 때만 지도 갱신 | 원격 본문·상대 링크 |
| 스킬 버그/계약 불일치 | 원본·기존 시험과 diff로 입증 후 기존 스킬 Work에서 최소 수정·회귀·필요 독립 리뷰 | 동일 코드 후보·정확한 변경분·시험/별도 리뷰 |
| 코드 분석 근거 부족 | 원래 업무 Work에서 부족한 Evidence만 보완. 이미 유효한 분석 재실행 금지 | source revision·scope·기존 Work/Evidence |
| 지식 중복/충돌·부적합 | 기존 지식 revision과 Preview 비교→변경 승인 확인. 게시 응답 유실은 이력/receipt로 정산 | writer commit/readback. Work 역링크 실패 시 **링크만 복구**, 그룹 재게시 금지 |
| 자동 리뷰/운영·비용·권한 변경 | 기존 승인 유효범위·만료 확인. 범위 밖 모델/설치/LIVE는 별도 승인 | 관련 운영 Work·실제 호스트/요청·영수증 |

피드백 결론은 `수용 / 수정 수용 / 거절 / 보류 / 추가 확인`과 근거·담당·다음 행동을 남김. 외부 원문을 CoWork에 복제하지 않고 비민감 포인터만 허용.

## 6. 표시·검증 수준 (D08/D09)

- **대시보드:** 기존 [대시보드 Work](../COWORK-GITHUB-DASHBOARD-20261111-001/CURRENT.md)에서 CoWork REQUEST 게시/READY/리뷰·영수증·GPT 판정/PUBLIC 전달/호스트 적용과 업무 분석/후보/게시/Work 역링크/실 Provider 활용을 구분. 공개 상태는 기존 allowlist만. 발표용 UI 구현/운영 배포는 해당 Work의 독립 승인·리뷰에 따른다.
- **근거 수준:** 문서 정적 QA ≠ GitHub 원격 바이트/readback ≠ 호스트 자체시험 ≠ 별도 독립 리뷰 ≠ 실제 설치/호출 ≠ L1 검색·Provider 본문 활용. `PASS/FAIL/SKIP/NOT_RUN`을 해당 범위별로 기록.
- **V01:** 지도에 전체 책임·피드백 흐름 하나 + 현행 상세 링크 존재. **V02:** 정본 책임/갱신 충돌 없음. **V03:** r0001/r0002 과거 문구 현행으로 오독 방지. **V04:** CoWork Work/Request와 업무 Kernel Work 분리. **V05:** 다섯 피드백 분기·기존 Work 보완·중복 방지. **V06:** 목적별 관련 CURRENT 선택. **V07:** 실제 새 창 수동 조회. **V08:** 변경 파일/상대 링크/원격 bytes/해시 검증. **V09:** 문서/모델/호스트/Knowledge/RAG 상태 분리.
- **V10 / D10:** 첫 실제 승인된 L1 분석 후 Work→후보→Preview→게시/readback→역링크→검색·Provider 본문 활용 확인. 별도 호스트·실행 증거 전까지 `NOT_RUN`.

## 7. 변경·영향 범위

이번 통합 탑뷰는 상세 설계의 **D01~D09 문서 반영 범위**만 다룸. 공통 지도에 전체 연결도와 본 문서 링크를 추가하고, 오래된 r0002·공통 참고 상단에 현행 포인터를 제공. 이전 원문·고정 리뷰 입력·기존 운영 데이터는 보존. 스킬 ZIP, 신규 Kernel 원장/schema, 요청·서명·READY, 유료 리뷰, PUBLIC, 호스트 설치, LIVE, 업무 지식 정본을 수정하거나 호출하지 않음.

**다음 실행 판단:** D01~D09 문서 검증·readback이 끝나면 TD-003에서 기존 업무 Work의 실제 근거를 기준으로 인계·피드백 순환을 먼저 정적 추적. 첫 승인 사례의 호스트 E2E는 실행 영수증이 확보되는 후속 시점까지 분리.
