# NR L1 Tx 코드 분석 — 모바일 Agent / Linux MCP 1차 실제 실행 요청
- 작성: 2026-11-15 KST
- Tracking key: `NR-L1TX-CODE-ANALYSIS-20261115-001` (문서 추적 키, 실제 Job ID 또는 Work ID가 아님)
- 저장소: `wonhwipark/CoWork-Skill-Collab`, branch `main`
- 요청 경로: `collab/projects/NR-L1TX-CODE-ANALYSIS-20261115-001/EXECUTION_REQUEST.md`
- 검토 기준: `collab/projects/JOBLIST-NRTX-20261112-001/CURRENT.md`, `collab/projects/JOBLIST-SMOKE-20261114-001/CURRENT.md`
- **사용자가 확인한 실제 코드 경로: `/home/whpark/Project/smp1900`**. Linux 실행 호스트에서 이 경로를 소스 checkout으로 사용한다. 실제 Git HEAD/branch·권한은 실행 시 검증하고, 원문 소스는 외부 반출하지 않는다.
- **신규 분석용 Job-list 전달 완료: `v0.4.38`, 패키지 `job-list_v0_4_38_1115.zip`**. 2026-11-15 사용자 승인에 따라 PUBLIC `wonhwipark/L1Work/main` 루트에 게시·원격 바이트 검증 완료 (ZIP SHA-256 `0cdda16fe214f86811d4df25cc04f3453ec93789ddc9bc2b0769e730bb9c16e0`; 커밋 `67ace047d336b81015034df913e11b10a64711d8`). Linux 설치·실행·분석·결과 조회는 별도 사후 검증 중이며 미확인.

## 목적
이미 디버깅한 MCP 연결을 재사용해 **NR L1 Tx의 실제 소스 기반 분석**을 시도한다. **기존 소비된 Job-list v0.4.36 Job ID 재실행/재큐잉 금지**. 신규 Job-list ZIP 배송/설치/활성화와 코드 분석을 혼동하지 않는다.

## 수행 절차 (현재 등록된 MCP 인터페이스만 사용)
1. 먼저 모바일 Agent가 실제 볼 수 있는 **MCP tools/list**와 허용된 호출 계약을 확인한다. Linux 호스트의 최신 수정/적용 상태·호스트 스킬 버전과 실제 등록된 분석 도구를 확인한다. `MCP 도구 검색 성공`, `MCP 호출 성공`, `코드분석 실행 성공`은 별도 상태다.
2. **1순위: 기존 `code-analyzer`의 승인된 분석 동작**을 MCP로 호출한다. 직접 노출되지 않으면 **`l1-fix-workflow`의 기존 분석 전용(비수정) action** 존재 여부를 확인하고, 검증된 때에만 사용한다. `l1-knowledge-updater`는 코드 분석 도구의 대용품이 아니며, 실제 설치 계약에서 확인된 지식 업데이트 조율 용도로만 사용한다. 도구명/action/인자·임의 shell 실행을 추정해 만들지 않는다.
3. `/home/whpark/Project/smp1900`의 현재 checkout 브랜치·HEAD·분석 기준 및 분석에 필요한 범위만 확인. 읽기 전용 소스 분석과 **신규 로컬 결과물/영수증 생성**만 허용. 실제 소스 코드·기존 Knowledge 정본·운영 DB·Job-list Registry/Queue/Receipt·예약 작업·Git 상태를 수정하지 않는다.
4. **1차 최소 유효 분석: `NR-TX-01 Init RACH`**. `L2_L1_TX_REQ` 수신 handler → NR L1 Tx dispatcher 및 조건/상태 갱신 → 실제 PHY IPC 전송 경계까지 함수 호출 및 데이터 흐름을 추적한다. L2/PHY 내부 구현이나 LTE 영역으로 자동 확장하지 않는다. 코드에 없는 경로·메시지·함수명을 추정하지 않는다.
5. 1차 분석에서 CODE FACTS와 실제 근거가 확보되고 같은 실행의 영수증이 검증될 경우, 계속 가능한 범위에서 `NR-TX-02 PHY_CONFIG_REQ (UL SCell 설정)`, `NR-TX-03 SCELL_STATUS_IND (Activation)`, `NR-TX-04 SCELL_STATUS_IND (Deactivation)` 순서로 진행. 각 scenario 별 시작/끝 함수 및 조건부 분기·IPC payload·skip/blocker를 구분. 시간/비용·도구 제한이 있으면 진행 가능한 범위까지만 수행하고 나머지 SKIP/NOT_RUN으로 명시한다.
6. 각 분석 결과는 기존 승인된 로컬 Work/Run/Evidence 연계 계약이 있는 경우에만 신규 기록으로 남긴다. 신규 디렉터리 산출물은 허용되나 그룹 `l1sw-dev-knowledge` 정본 업데이트, 원격 푸시/공개 게시, 코드 수정은 하지 않는다. MSC/Doc Converter는 코드 근거가 확정되고 실제 지원 도구가 있을 때만 후속 생성하며 별도 판정.
7. 결과 조회가 가능한 MCP READ로 **동일 Work/Run/Result 참조**를 재조회한다. 없는 ID나 Result를 만들지 않는다. `DONE/SUCCESS` 또는 단순 LLM 응답을 코드 분석의 PASS로 사용하지 않는다.

## Job-list v0.4.38 패키징·실행 조건
- 신규 활성 One-shot 요청은 **새 Job ID 1개**로 생성. 기존 `JOB-20261112-NR-L1TX-KNOWLEDGE-MSC-EXEC-01`, 이전 Smoke Job ID는 절대 재사용하지 않음.
- Profile/Worker는 등록된 실제 `code-analyzer` 또는 승인된 비수정 `l1-fix-workflow` action만 사용. 실측되지 않은 호출 형식과 Job-list 실행 복구를 PASS로 추정하지 않음.
- `v0.4.36` ZIP 원본과 운영 Registry/Queue/Receipt/DB는 보존하고 새 버전은 격리 구성·회귀시험. Skill-Updater에 의해 실행 가능한 PUBLIC 루트 게시와 운영 활성화는 배포 게이트 통과 후 승인 범위에서 별도로 수행.

## 필수 결과 (코드 원문/회사 내부 경로·로그는 호스트 내 보존)
- `TOOL_VISIBLE / TOOL_CALLED / ANALYSIS_STARTED / CODE_FACTS_VERIFIED / RESULT_READBACK`: PASS/FAIL/NOT_RUN/NOT_VERIFIED
- 실제 사용한 스킬, 호스트 기준 source revision(외부 출력 가능 여부 정책 준수), 내부 결과 참조 ID (외부로 허용된 ID만)
- 시나리오별 상태 및 source-grounded function/path/line 존재 여부(본문·원문은 호스트 보존), 최초 실패 단계 및 non-sensitive blocker
- `GROUP_KNOWLEDGE_WRITE=NOT_RUN`, `SOURCE_WRITE=NOT_RUN`, `JOBLIST_OLD_REEXECUTION=0` 실제 확인 여부
- 성공하면 상태 코드/건수/결과 참조만 모바일 Agent에 반환. 실패하면 정확한 reason code와 필요한 다음 한 조치를 반환.

## Stop 조건
- 분석용 MCP Tool이 노출되지 않거나 실제 권한이 없는 경우 `BLOCKED_MCP_ANALYSIS_NOT_EXPOSED`.
- 변경 작업만 지원되거나 도구 계약이 미확인인 경우 실행하지 않고 `BLOCKED_CONTRACT_UNVERIFIED`.
- 최신 디버깅 수정의 실제 적용 상태를 확인하지 못하더라도 이미 정상 동작이 검증된 별도 READ 분석 경로라면 그 경로만 진행. Job-list 파이프라인의 신규 운영 활성화는 하지 않는다.
- 회사 원문 소스·고객 자료·내부 실행 로그·개인키·토큰의 외부 전송 금지.
