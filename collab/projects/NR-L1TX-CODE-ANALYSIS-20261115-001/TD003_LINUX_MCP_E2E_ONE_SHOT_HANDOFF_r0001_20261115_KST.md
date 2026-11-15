# TD-003 첫 실제 인계 검증 — Linux MCP 기존 Job 결과 회수 원샷 r0001

- 기준일: 2026-11-15 KST
- 실행 귀속: **기존** `NR-L1TX-CODE-ANALYSIS-20261115-001`. 맥락 관리 Work `COWORK-SKILL-DISCOVERY-20261112-001`의 TD-003과 결과 링크만 교차 연결.
- 정본: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab` / `main`.
- 기존 [EXECUTION_REQUEST](EXECUTION_REQUEST.md), [NR CURRENT](CURRENT.md), [Job-list 배송 계약 8절](../../ops/CONTRACTS/JOBLIST_PUBLIC_DELIVERY_V1.md), [TD-003 추적](../COWORK-SKILL-DISCOVERY-20261112-001/TD003_MULTI_SKILL_HANDOFF_FEEDBACK_TRACE_20261115.md) 재사용. 신규 Job/REQUEST/READY/별도 Work/임시 운영 Schema 생성 금지.
- **이 문서의 GitHub 게시 = 호스트 호출이 아님.** 실제 모바일 Agent/Linux MCP는 이 채팅에서 연결되어 있지 않음. 아래 텍스트는 기존 인가된 Agent에서만 실행.

## 1. 기존 배포와 고정 식별자

| 항목 | 고정 값·경계 |
|---|---|
| 전달 ZIP | PUBLIC `wonhwipark/L1Work/main` 루트 `job-list_v0_4_38_1115.zip` (이미 게시; 재게시 금지) |
| 예상 ZIP SHA-256 / 크기 | `0cdda16fe214f86811d4df25cc04f3453ec93789ddc9bc2b0769e730bb9c16e0` / `1,570,759` bytes |
| 배포 결과 | PUBLIC 게시/readback PASS. **Linux 설치/활성화/실행의 증거 아님** |
| 유일 신규 Job ID | `JOB-20261115-NR-L1TX-INIT-RACH-EXEC-01` |
| 프로필 | `nr-l1tx-init-rach-analysis-linux`, 등록된 read-only code-analyzer 호출만 |
| 과거 소비 Job | `JOB-20261112-NR-L1TX-KNOWLEDGE-MSC-EXEC-01` **재큐잉/재실행 금지** |
| 허용된 범위 | 호스트 정상 승인 경로의 조회, 필요한 경우 기존 허용된 Skill-Updater 1회, 이미 승인된 신규 Init RACH read-only 분석 1회. 기존 Job 반복 발행·수정/그룹 게시·유료 호출은 불허 |

## 2. 모바일 Agent에 전달할 원샷 지시 (기존 실행 도구가 있을 때만)

> **대상 환경:** Linux MCP에 연결된 기존 모바일 Agent / 등록된 MCP tools/action. 작업용 원본 코드는 호스트 안에서만 읽고 출처·상세 로그·제품 정보 외부 반출 금지.
>
> `JOB-20261115-NR-L1TX-INIT-RACH-EXEC-01`의 **기존 실행 여부부터 READ ONLY**로 조회해. 반드시 먼저 tools/list·실제 허용 action과 현재 Skill-Updater/Job-list 설치 버전, 설치 ZIP SHA, 해당 ID의 Catalog·Registry·Queue·Run·Worker·Result·Receipt·MCP readback 지원 여부를 조회해. `job-list_v0_4_38_1115.zip`의 승인된 SHA/크기와 실제 설치본을 비교해. 이미 실행/소비/불확실한 Job은 새 요청이나 재활성화를 만들지 말고 영수증/이력만 정산해. 대상 Job이 아직 설치되지 않았고 기존 승인 범위에 Skill-Updater 정상 실행 1회가 포함되며 **등록된 정상 비파괴 action이 확인된 경우에만** 1회 실행하고 다시 읽어. 설치 전후 다른 운영 설정/DB·예약 작업/Queue/Registry 수동 조작 금지. 중복 또는 실행 상태 불명이면 `BLOCKED_UNCERTAIN_RUN`.
>
> 현재 Job이 정상 활성화되어 read-only 분석이 가능하고 미실행임이 신뢰 가능한 원장으로 확인되면 **기존 승인된 그 Job 1회에 한하여** `NR-TX-01 Init RACH` (`L2_L1_TX_REQ`에서 PHY IPC 경계) 분석 결과를 회수해. 등록된 `code-analyzer` 또는 원문으로 검증된 비수정 Workflow action만 사용. 임의 도구명·CLI·shell·Job ID 발명 금지. 이후 같은 Job ID의 Runner `run_id`, Worker 시작, Code Facts/실제 source pin, Result/Receipt 및 MCP 결과 재조회가 일치하는지 확인해. `DONE/SUCCESS`·단순 모델 답변만으로 PASS를 선언하지 마.
>
> 코드 사실·분석 Evidence가 이미 확인되고 기존 업무 Work ID 및 실제 Updater 호출 계약이 입증되면, **원래 업무 Work를 재개**해 후보 입력/중복 비교/Preview만 기존 승인 경계에서 점검해. 본문 원본·상세 MSC는 업무 호스트 보존. 기존 Knowledge writer를 통한 **그룹 게시·재게시/역링크 변경·RAG Provider 호출은 이번 승인으로 수행하지 마**. 실제 계약·근거가 없다면 `NOT_VERIFIED/NOT_RUN`로 두고 다음 근거 1개만 보고해.
>
> **결과:** 기존 Job ID, 실제 설치 SHA 확인 여부, `TOOL_VISIBLE / INSTALLED_SHA / CATALOG / REGISTRY / QUEUE / RUN_ID / WORKER_STARTED / RESULT / RECEIPT / MCP_READBACK / CODE_FACTS / WORK_EVIDENCE / UPDATER_PREVIEW` 각각 PASS/FAIL/NOT_VERIFIED/NOT_RUN, 최초 차단 reason, 원본이 노출되지 않는 내부 참조 ID(허용된 경우만), 다음 한 행동을 한국어로 반환해. 지난 소비 Job 재실행 횟수 0, Knowledge write 0, 운영 변경 0도 확인 근거가 있는 경우에만 명시해.

## 3. 판정 기준

| 단계 | PASS 기준 | 미충족 판정 |
|---|---|---|
| 설치/활성화 | 실제 설치 ZIP SHA 고정 + 동일 신규 Job ID의 Catalog/Registry | `NOT_VERIFIED` 또는 `BLOCKED`; 배송 결과로 대체 불가 |
| 실제 실행 | Queue → 동일 Job ID/Run ID → Worker 실제 시작 → Receipt/Result 정합 | `NOT_RUN/NOT_VERIFIED`; DONE만으로 PASS 금지 |
| MCP 결과 조회 | 동일 Job/Run/Result를 MCP READ로 재조회 | `RESULT_UNSUPPORTED`이면 FAIL/BLOCKED, 다른 결과 참조 금지 |
| 코드 분석 | 실제 source revision/scope·Code Facts·Evidence 확인 | 출처 없는 모델 응답은 PASS 불가 |
| 다중 스킬 후보 인계 | 원래 Work 재개 + 원본 Evidence 참조 + Updater 기존 contract의 실제 후보/Preview 반영 확인 | `NOT_RUN/NOT_VERIFIED`; 새 Work/가상 API 금지 |
| 그룹 게시/역링크/RAG | 별도 승인·실제 게시/Work 링크/본문 Provider 증거 각각 필요 | **이번에 NOT_RUN으로 유지**. 무단 실행 금지 |

## 4. 접수·후속 처리

1. 모바일 Agent가 반환한 **비민감 상태/코드/근거 ID만** 원래 NR Work의 결과·CURRENT에 반영. 상세 기술/코드/실행 로그/MSC 원본·키/토큰은 CoWork PRIVATE에도 게시하지 않음.
2. TD-003 맥락 Work에는 NR Work의 고정 근거 링크, 인계 시나리오별 실제 PASS/NOT_RUN 및 남은 한 행동만 연결. 실제 Work 변경 없이 이력 복제 금지.
3. 설치나 실제 조회가 불가능하면 `HOST_TOOL_UNAVAILABLE` / `BLOCKED` 사유를 남기고 종료. 새로운 자동 감시·예약·Job 재큐잉·유료 Claude 리뷰/REQUEST/READY를 임의 생성하지 않음.
4. 실제 팀 Knowledge 게시·역링크·RAG는 기존 승인/접근 수단과 별도의 E2E 증거 확보 뒤 해당 L1 Work에서 판단; 이 제한된 읽기 전용 작업의 완료 기준으로 강제하지 않음.

- **이 문서 작성 직후 세션 상태:** `HOST_TOOL=UNAVAILABLE_IN_CHAT`, `HOST_MCP_RUN=NOT_RUN`, `RECEIPT_READBACK=NOT_VERIFIED`, `TD003_REAL_MULTI_SKILL_E2E=NOT_RUN`. 문서 게시·정적 QA는 별도.
