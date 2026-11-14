# GitHub LIVE 컷오버 — 사용자 명시 승인 및 안전 게이트 원샷 실행 지시

- Rev: r0001 / 2026-11-14 KST
- GitHub PRIVATE repository: `wonhwipark/CoWork-Skill-Collab`
- Branch: `main`
- **정확한 상대 경로:** `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_GITHUB_LIVE_CUTOVER_USER_APPROVAL_AND_GATED_ONE_SHOT_r0001_20261114.md`
- Work ID: `COWORK-DROPBOX-TO-GITHUB-MIGRATION`
- **USER_APPROVED_GITHUB_LIVE_CUTOVER:** 사용자 발언 **"전환해줘"**, 2026-11-14 KST. 이 승인에 대해 동일한 최종 전환 의사 확인을 다시 요청하지 않는다. **실제 전환 조건을 모두 통과했을 때** 단일 GitHub LIVE provider로 전환하도록 요청한 것.
- **현재 실측**: `ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER`, `HOST_CUTOVER_EXECUTED=NO`, `V0218_INDEPENDENT_REVIEW=NOT_RUN`, `N1_PRE_PUBLISH_DB_LOSS=NOT_RESOLVED`.
- 사용자 확정 Classic PAT 사용 유지. 토큰 종류/교체 관련 일반 논의·새 fine-grained 발급 요청 금지.
- 본 GitHub 문서 **게시만으로 Windows Claude Code/Watcher/운영 Task가 자동 실행되지 않음**.

## 1. 이번 사용자 요청의 승인 경계

- **승인 완료:** 전제 조건을 충족한 최종 **GitHub LIVE 전환 자체**. 추가적인 "LIVE로 바꿔도 될까요?" 질문은 금지. **최소 변경·단일 활성 제공자·원본 보호·롤백 우선**.
- **별도 명시 승인 없이 금지:** 신규 **유료** 독립 Claude 리뷰/예산 확대·재호출, PUBLIC ZIP 배포, 운영 비밀/신뢰키 새 발급/교체, 기존 사용자 데이터가 든 운영 DB의 덮어쓰기·이행/초기화, 운영 watcher/Task/Notifier의 광범위한 변경이나 실 알림 발송. 사용자 전환 요청을 이들 별도 작업의 무제한 승인으로 확대하지 않는다. 컷오버에 필수인데 승인이 없는 운영 변경은 `BLOCKED_APPROVAL_REQUIRED`로 분리한다.
- **허용된 사전 작업:** Windows 격리 작업 사본에서 N1/N2 보완·합성시험·ZIP 준비·민감정보 없는 PRIVATE 후보 게시 및 원격 readback, 운영 호스트/Task/DB/Notifier 설정의 읽기 전용 점검, 원본 DB 바이트 불변 사본 백업 및 격리 복원 리허설(기존 승인 범위), 비발송 검증.
- **운영 LIVE는 신뢰/중복/독립 리뷰·의존성·알림/이력/롤백 필수 게이트 통과 전 절대 활성화하지 않는다.** 미검증 항목을 PASS로 가정하지 말 것. 게이트 실패는 기존 비활성 상태 유지; 새 유료 모델 호출·LIVE 작업 우회 금지.

## 2. 최신 기준 근거 — 오래된 인계 중복 수행 금지

1. `collab/START_HERE.md`, `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md` **최상단**, `TRACKER.json`, `GPT_CLASSIC_PAT_E2E_AND_V0218_DISPOSITION_r0001_20261114.md` 참조.
2. 기존 Windows Claude Code 결과 `CLAUDE_CLASSIC_PAT_GITHUB_WRITE_E2E_AND_LIVE_PREFLIGHT_RESULT_FOR_GPT_20261114.md`:
   - Classic PAT: GitHub PRIVATE 임시 브랜치 실제 write/readback/삭제 PASS, 감시기 최초 게시 PUT2·중복/충돌 방지 PASS **호스트 자체 보고**.
   - `v0.2.18` 235650 B, sha256 `519c70e3eabbe9722621afa5bf6365b93d99803c76fee2fe078722a0835522cd` 개발 ZIP 로컬만 존재. N1/N2/S1/S2 자기시험 통과, 독립 리뷰 NOT_RUN.
   - 중요한 잔여 위험: 유료 모델 호출 뒤 remote 결과 업로드 전에 로컬 DB/결과 소실 시 중복 비용 방지 불완전. `v0.2.18`을 그 상태로 설치·LIVE하지 말 것.
   - `cryptography` 운영 Python 미설치, 기존 pending request 1건, Notifier 부모/자식 쌍 정상이나 GitHub 연동 미검증. 기존 Dropbox reviewer watcher는 비활성화 실측, `ACTIVE_PROVIDER=NONE`이 최신 기록.
3. 기존 v0.2.17 R2 정적 독립 리뷰 PASS_WITH_FINDINGS는 **v0.2.18 이후 변경 코드에 소급 적용 불가**. 이전 R2를 다시 청구하지 말 것.

## 3. Windows Claude Code 원샷 작업 — 단계별 진짜 PASS/FAIL

### A. 호스트 현황·복구 기준선 고정 (무변경)
- 현재 프로세스·Task·provider·계정·Python interpreter/cryptography 상태·기존 LIVE DB main/WAL/SHM 해시·stat·pending 1건·review/receipt/audit/cursors·Notifier 워터마크와 중복 발송 경계 읽기 전용 확인. 운영 DB를 SQLite 연결로 직접 열면 shm 갱신될 수 있으므로 이전에 검증한 **바이트 복사→격리 사본 읽기** 방법 사용.
- 활성 모델 reviewer/예약 작업, pending/REVIEW_UNCERTAIN, 미정산 이력/완료 작업을 별도 목록으로 식별. 원본 main/WAL/SHM·운영 Task·Notifier 설정·비밀은 **선행 승인 없이 불변**. 백업 바이트/해시·격리 복원 성공과 재설치/롤백 경로 기록.
- 현재와 다른 실측 발견 시 문서보다 실측 우선. 불확실한 요청은 무손실 보존하고 유료 재시도 0.

### B. 최종 candidate 단일화 — 개발·합성시험은 원샷
- 현재 `v0.2.18`의 N1 **post-dispatch/pre-publish DB 및 로컬 결과 소실** 문제를 최소 수정. 모델 실행 전에 **지속되고 독립적으로 재조회 가능한 유료 디스패치 이력**을 기록하고 중복 키(요청 ID/revision/ZIP SHA 등) 예약을 원자적으로 처리하는 등 동등한 fail-closed 설계로 구현. 어느 시점의 crash/restart/원격 네트워크 장애에서도 이전 실행 여부가 불확실하면 `REVIEW_UNCERTAIN`으로 보존하고 **새 모델 호출 0**을 시험으로 입증.
- 순서: 서명·SOURCE_PIN·정책·회수/일일 비용 게이트 → 정확한 논리 키 확인 → 재시작 후 조회 가능한 reservation 확인 → reviewer 호출. 조회/저장 실패 시 모델 호출 0. 외부 repo 권한/정책 수정 없이 실행.
- synthetic crash injection: dispatch 직전, reservation 직후, 모델 시작·진행 중, 모델 결과 저장 전, 저장 후 원격 게시 전, `UPLOAD_PENDING`, 완료, 로컬 DB/원격 조회 실패, 동시 scan/watch, 정책 개정·커서 소실, 격리 백업복원. **중복 유료 호출/완료 이력 손실 0**을 입증하되 실제 Claude 모델 호출 0.
- N2 실제 GitHub repo ID 결합과 기존 v0.2.17 R1/R2 회귀, 실제 Ed25519(격리 venv), 기존 Windows timeout/taskkill 및 publish-only 멱등성을 통합 시험. 추가 기능 확장 금지.
- 새 후보가 필요하면 `v0.2.19` 등 신규 버전으로 원본 보존. `<skill>_v<major>_<minor>_<patch>_<MMDD>.zip` 정규명 규칙; 후보 ZIP CRC·ZIP slip·필수 파일·민감정보·실제 SHA-256·크기·정상 및 부정 시험 결과 검증. **후보는 아직 `development_not_for_deployment`**.

### C. 독립 리뷰·운영 실행 게이트 (미승인 유료 호출 금지)
- **새 후보에 대한 독립 검증은 필수**. 현재 명시적으로 승인된 것은 **최종 LIVE 전환 의사**이지 미정의 리뷰 요금이 아님. 새로운 유료 R1/R2/R3 리뷰는 별도의 확정된 대상 SHA/리뷰 ID/예산·호출 횟수의 명시적 승인 없으면 `BLOCKED_PAID_REVIEW_APPROVAL`, 모델 호출 0. 재발급·모델 호출·READY를 임의 생성하지 말 것.
- Claude Code가 구현한 동일 개발 세션의 자체 시험을 `INDEPENDENT_REVIEW=PASS`로 승격 금지. 별도 독립 리뷰 요청/실행/영수증 또는 검증된 독립 리뷰 증거가 확보된 최종 동일 ZIP에 한해 통과 처리.
- 운영 Python에 `cryptography`가 없으면 승인 검증은 불가(fail-closed). 필요한 운영 설치·패키지 배치·운영 Task/Notifier 설정 변경은 기존 승인·권한을 **각각** 확인한 후 실행. 미승인/불가 시 `BLOCKED_OPERATIONAL_APPROVAL`(새 모델 호출 0). 격리 venv 시험으로 운영 호환 PASS를 대신하지 않음.
- GitHub notifier provider별 상태/워터마크 이행, pending 1건 무손실 처리 또는 명시적 격리 보존, 과거 완료 결과와 Telegram 중복 0, 단일 provider lease/이중 LIVE 0, 부정 승인 fail-closed, 원본 보존·롤백 시험을 실제 호스트에서 검증.
- '별도 계정 enforce/ETW 장기 시험'이 승인·실행 가능하지 않으면 현재 SU-SIMPLE 가이드와 실제 위협/호스트 제약에 따라 우선순위 판정. 운영 DB/main-WAL-SHM 무변경·별도 상태·원격 GET-only SHADOW의 독립 증거는 필수. 미실행을 PASS로 기록하지 않음.

### D. 컷오버 (모든 필수 게이트 PASS, 필요한 운영 변경 승인 확인된 때에만)
- 단일 GitHub watcher provider를 활성화하고 기존 비활성 Dropbox watcher를 재활성화하지 않음. 동시에 LIVE 2개 금지. 신규 watcher 시작 후 Task/process/pid/lease와 실제 모드 확인, 허용된 signed REQUEST만 탐색. 최소 2회 상태 주기+재시작 후 중복 리뷰·알림 0, 실제 결과·영수증 원격 readback·원본/이관 데이터 일치 확인.
- 기존 Notifier 전환이 필요하면 provider별 cursor/watermark를 격리 백업하고 최초 시작 시 오래된 완료 이력 재발송 0을 검증. 새 유료 리뷰를 실전 smoke로 호출하지 말 것(미승인).
- 이상 또는 복구가 불확실하면 **즉시 fail-closed 중지**, 원본 백업/커서/영수증 보존, 새 provider OFF. Dropbox 재활성화는 별도 승인/롤백 계약을 따르고 이중 LIVE를 만들지 않는다.
- 실제 전환 이후에만 `CUTOVER=LIVE`, `ACTIVE_PROVIDER=GITHUB`, `HOST_APPLIED`, `ROLLBACK_READY` 등을 실측 근거와 함께 표시. 문서가 먼저 바뀌었다는 이유로 LIVE를 선언하지 않는다.

## 4. 결과 문서와 최신 상태 업데이트

- 경로: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CLAUDE_GITHUB_LIVE_CUTOVER_EXECUTION_RESULT_FOR_GPT_20261114.md`
- 결과 표 필수: `USER_LIVE_APPROVAL=APPROVED`, `DEVELOPMENT`, `SELF_TEST`, `INDEPENDENT_REVIEW`, `N1_CRASH_DUPLICATE_0`, `N2_REPO_BINDING`, `CRYPTO_OPERATING`, `PENDING_REQUEST_PRESERVED`, `NOTIFIER_MIGRATION`, `ROLLBACK_TEST`, `HOST_INSTALL`, `TASK_APPLIED`, `ACTIVE_PROVIDER`, `CUTOVER_STATE`, `MODEL_CALLS_DELTA`, `PAID_COST`, `BLOCKED_REASONS`. 각각 **PASS/FAIL/SKIP/NOT_RUN/BLOCKED**, 증거 종류와 구체 원인.
- 결과 MD, `CURRENT.md` 최상단(기존 전체 이력 보존), `TRACKER.json`(스키마 유효 enum) PRIVATE `main` PR 없이 게시하고 git commit/원격 bytes/SHA readback 확인. 못 하면 `NOT_POSTED/UNVERIFIED`라고 보고.
- 비밀/고객/회사 L1 코드/운영 데이터/개인키는 PRIVATE에도 게시 금지, `/AI-CONTINUITY/` 불변. PUBLIC ZIP 게시 금지.
- **중간 재승인 반복 금지**: 선행 작업은 가능한 범위를 모두 수행하고 차단 항목만 `BLOCKED`로 분리하여 최종 한 번 보고. **이미 허용된 최종 LIVE 전환 의사는 재질문하지 않음**. 유료 검토·실제 운영 변경의 별도 승인 필요 항목은 조작하지 않음.

## 5. Windows Claude Code에 전달할 프롬프트

```text
GitHub PRIVATE wonhwipark/CoWork-Skill-Collab, main의 collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_GITHUB_LIVE_CUTOVER_USER_APPROVAL_AND_GATED_ONE_SHOT_r0001_20261114.md 를 이번 최종 인계로 읽고 사용자 "전환해줘" 승인을 반영해 실행해줘. LIVE 전환 의사를 재확인하지 말고, N1 pre-publish crash 중복 방지 최소 수정/회귀·후보 고정·독립 리뷰 상태·운영 Python 서명·Notifier 이력·롤백을 점검하고 이미 허용된 범위의 작업은 원샷으로 끝내줘. 필수 게이트 PASS와 필요한 개별 운영 승인 확인시에만 GitHub 단일 LIVE로 전환하고, 실패/미승인 단계가 있으면 모델 호출 0·운영 원본 불변·ACTIVE_PROVIDER=NONE을 유지해줘. 추가 유료 모델 리뷰/신규 READY/비밀 발급/운영 DB 임의 이행/Task·Notifier 미승인 변경/PUBLIC 게시 금지. 결과 CLAUDE_GITHUB_LIVE_CUTOVER_EXECUTION_RESULT_FOR_GPT_20261114.md 및 CURRENT.md·TRACKER.json을 PRIVATE main에 게시하고 원격 readback까지 확인해줘. Classic PAT 계속 사용은 확정이며 그 논의는 반복하지 마.
```
