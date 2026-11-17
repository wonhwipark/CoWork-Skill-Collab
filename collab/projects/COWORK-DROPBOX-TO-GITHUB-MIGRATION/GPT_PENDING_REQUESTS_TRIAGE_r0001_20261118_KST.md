# pending_requests 9건 분류·후속 판정
- 기준: 2026-11-18 KST. 기존 Work `COWORK-DROPBOX-TO-GITHUB-MIGRATION`.
- 입력: 사용자가 전달한 Windows 감시기 점검. `pending_requests=9`, 로컬 `jobs.COMPLETED` 4건 및 Guard `AUTO_SIGNING_UNCERTAIN`은 **호스트 보고**이며 GPT의 운영 DB 직접 조회가 아님.
- GPT 확인: PRIVATE `wonhwipark/CoWork-Skill-Collab/main`의 원격 파일·결과·영수증. 조회 트리 `1fd5bb7a05a33c17fe99c3b1a0dc9ee1e569d736`에서 해당 5개 요청에는 READY/정식 결과/실행 영수증이 없고, MSC 두 진입 요청에는 승인·READY·디스패치·결과·영수증이 존재.
- 재사용: 기존 요청·결과·판정과 같은 Work를 REUSE. 새 원장·요청·자동화·스키마를 만들지 않음.

## 1. 대기 수와 실제 조치를 분리
원시 추적 행 9건은 실행 가능한 리뷰 9건을 의미하지 않음. 사용자 분류인 미해결 5/완료 잔존 4를 수용하되, 미해결 5도 신규 실행·정산·대체·보류를 분리해야 함.

| 요청 | 확인·보고된 상태 | GPT 판정과 다음 처리 |
|---|---|---|
| REQ-COWORK-BUDGET-V025-DESIGN-R1-20261117 | POLICY-STATIC-V1-DESIGN 미등록 BLOCKED, READY 없음 | 같은 v0.2.25 ZIP에 대한 LARGE R2 리뷰·GPT 판정이 이미 완료됨. **추가 리뷰 불필요한 미시작 대체 이력**으로 분류. 정책을 새로 등록해 이 구요청을 실행하지 않음. Windows에서 기존 지원 절차로 미시작 보류/종결 여부 정산 필요; 로컬 종결을 이번 문서로 완료했다고 보고하지 않음. |
| REQ-L1-WORK-KNOWLEDGE-GUARD-CODE-R1-20261117 | AUTO_SIGNING_UNCERTAIN 종결 상태(호스트 보고), 원격 승인/READY/결과 없음 | **우선 정산 대상**. pin 타입 수정으로 재시도하지 않음. Windows에서 signing audit/jobs/dispatch/비용·예약을 읽기 전용 대조. 미호출·기존 유효 승인·정상 수동 경로가 입증될 때만 기존 보호 signer의 수동 처리 가능성을 판정. 불확실 상태를 임의 초기화/재큐잉하지 않음. '무조건 수동 승인하면 해결'로 확정하지 않음. |
| REQ-COWORK-DASHBOARD-PRESENTATION-20261115-001 | READY 없음, SUBMISSION_STATUS에 cost_authority=NOT_CONFIRMED_FOR_THIS_ID | **실행 대기/승인 범위 추가 확인**. 파일 존재만으로 실행 승인·큐 등록을 인정하지 않음. 현재 입력의 적용성과 기존 권한을 해당 대시보드 Work에서 확인한 뒤 처리. 이번에 유료 리뷰 시작 안 함. |
| REQ-L1-MSC-MD-LINK-STRUCTURE-20261115-001 | READY/정식 결과 없음, 대화형 리뷰·GPT ACCEPT_WITH_CHANGE는 이미 존재 | **대화형 검토 완료 / watcher 정식 리뷰 NOT_RUN**을 유지. 이미 수용·보완한 검토를 단지 추적 행을 없애기 위해 유료 재실행하지 않음. 기존 입력·검토 이력 보존. |
| REQ-L1-WORK-KNOWLEDGE-DESIGN-20261115-001 | READY 없음. 구요청 $1/1회 승인·signer 대기 이력 존재 | **구요청 보류 및 중복 범위 대조**. 후속 FIXED R1 설계 리뷰·판정이 이미 존재하므로 구요청의 남은 검토 범위가 있는지 기존 입력과 대조한 뒤 정리. 동일 범위로 자동 실행하거나 정식 완료로 소급하지 않음. |
| REQ-COWORK-V0214-R1-20261114 | 원격 결과 존재, RECEIPT ok=true; 로컬 COMPLETED 보고 | 실행 대기에서 제외할 완료 이력. 삭제·재호출 불필요. |
| REQ-COWORK-V0217-R2-20261114 | 원격 결과 존재, RECEIPT ok=true; 로컬 COMPLETED 보고 | 실행 대기에서 제외할 완료 이력. 삭제·재호출 불필요. |
| REQ-COWORK-V0219-R2-20261114 | 원격 결과 존재, RECEIPT ok=true; 로컬 COMPLETED 보고 | 실행 대기에서 제외할 완료 이력. 리뷰의 BLOCKING 유무와 실행 완료는 별개. 삭제·재호출 불필요. |
| REQ-COWORK-V0220-R1-20261115 | 원격 결과 존재, RECEIPT ok=true; 로컬 COMPLETED 보고 | 실행 대기에서 제외할 완료 이력. 삭제·재호출 불필요. |

대체 근거: [자동 승인 CURRENT](../COWORK-AUTO-APPROVAL-20261115-001/CURRENT.md)의 v0.2.25 LARGE R2 완료 및 [GPT 판정](../COWORK-AUTO-APPROVAL-20261115-001/GPT_V025_LARGE_R2_DISPOSITION_r0001_20261117_KST.md). 기존 DESIGN 입력과 LARGE 입력은 같은 ZIP SHA-256 `26d63c8a03290499b13b2ceb8ff0b70c06eb1b1bcc1a25fe3d8f65fcc213d228`를 가리킴. **문서상 대체 판정은 watcher 취소/종결 적용이 아님**.

기존 대화형 MSC 근거: [GPT 판정](../L1-WORKSPACE-RAG-20261111-001/GPT_MSC_MD_LINK_STRUCTURE_REVIEW_DISPOSITION_r0001_20261116_KST.md).
후속 Knowledge 설계 근거: [FIXED R1 판정](../L1-WORKSPACE-RAG-20261111-001/GPT_FIXED_KNOWLEDGE_R1_REVIEW_DISPOSITION_r0001_20261117_KST.md). 후속 리뷰 존재만으로 서로 다른 고정 입력의 완전 동등성을 주장하지 않음.

## 2. 새로 확인한 MSC 완료
`REQ-L1-MSC-DUAL-ENTRY-DESIGN-R1-20261117`는 실제 원격 결과 `execution_status=COMPLETED`, `RECEIPT ok=true`, 일치하는 processing_key를 확인. REQUEST/READY bytes SHA-256이 승인 payload와 일치.
[이번 GPT 판정](../L1-WORKSPACE-RAG-20261111-001/GPT_MSC_DUAL_ENTRY_R1_DISPOSITION_r0001_20261118_KST.md): ACCEPT_WITH_CHANGE, 차단 0·비차단 권고 2. REQUEST→독립 리뷰 1회→GPT 판정 사이클 종료. 구현·설치·업무 E3 완료는 아님. pin 수정이 자동 처리 재개의 직접 원인이었는지는 로컬 signing audit 미조회로 추론에 한정.

## 3. 집계 결함 후보와 안전한 수정 방향
- `pending_requests`가 보존하는 모든 추적 행을 그대로 '대기'로 표시하면 완료 이력 4건까지 포함하는 오해가 생김. **집계/표시 결함 후보는 수용**, 실제 SQL·설치 코드의 원인·수정·회귀는 NOT_RUN.
- 우선 기존 jobs 및 요청별 상태를 대조해 완료를 실행 대기에서 제외하고, 승인 대기/정책 차단/불확실 종결/완료 잔존을 표시에서 구분하는 방향 검토. 새 DB 필드·상태 enum이 필요하다고 확정하지 않음.
- 숫자를 줄이려고 pending 행을 일괄 DELETE하지 않음. 완료·불확실·레거시 이력과 중복 방지 근거, DB/WAL/SHM은 보존.
- 현재 v0.2.25 조건부 Windows 배포 인계와 별개. 이 문서가 운영 DB·설정·보호 위임 변경 승인을 확대하지 않음. 별도 LIVE 배포가 진행 중이면 해당 결과를 우선 확인하며 중복 작업하지 않음.

## 4. 이번 수행·경계
원격 파일 대조·SHA 계산·기존 Work 판정 기록만 수행. Windows/SQLite 직접 조사·housekeeping 코드 패치·호스트 설치·운영 설정·서명/READY·새 REQUEST·유료 모델·재큐잉·PUBLIC 게시=NOT_RUN.
원격 4개 완료 영수증은 GPT가 직접 읽었고, 로컬 jobs.COMPLETED 및 재과금 방지 실제 DB 제약은 호스트 보고로 구분.

**NEXT_ONE_ACTION:** Windows Claude Code의 기존 유효 작업 범위에서 Guard 불확실 이력과 구 DESIGN 요청의 미시작 대체 상태를 우선 읽기 전용 정산하고, 완료 4건 포함 집계의 실제 코드 위치·수정 필요성만 확인. 새로운 유료 리뷰나 DB 초기화 없이 같은 Work에 결과를 남김. GPT 세션에는 Windows 직접 실행 연결이 없어 HOST_ACTION=NOT_RUN.
