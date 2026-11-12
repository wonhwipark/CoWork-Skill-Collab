# Windows 운영 복구 + C 단계 ETW 재측정 — 통합 실행 인계
작성일: 2026-11-12 KST | rev r0001 | 상태: USER_APPROVED / WINDOWS_EXECUTION_NOT_YET_VERIFIED
저장소: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`
브랜치: `main`
정확한 상대 경로: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_WINDOWS_OPERATIONS_RECOVERY_AND_C_ETW_RERUN_ONE_SHOT_r0001_20261112.md`

## 1. 승인 경계
사용자는 직전 보고에 대해 **기존 Dropbox LIVE 리뷰 감시기와 대시보드 갱신기 재시작**, 그리고 **수정된 C 단계 ETW 계측 재실행**을 함께 명시 승인했다. 이 승인 범위를 한 작업으로 묶는다. Windows Claude Code가 실제 실행할 때 기존 호스트 실측 결과를 우선한다.

**포함**: 운영 시작 전 읽기 전용 안전 점검, 기존 예약 작업 2개 정상 시작, 실제 생존·스캔·갱신 관찰, 실패 원인/종료 코드 분석, ETW C 다시 시험, 민감자료 없는 결과 MD 및 GitHub PRIVATE `main` CURRENT 상태 게시·원격 readback.

**제외(미승인)**: 운영 watcher/dash updater 소스/설정/작업 정의 변경, `pythonw.exe` 전환, 계정/인증/토큰/키 변경, 운영 DB 수정·이행·정산·READY 발행/삭제, watcher 버전 교체, 재부팅, GitHub LIVE 전환, PUBLIC ZIP 게시, 유료 모델 리뷰의 새 승인/실행. 기존 Dropbox LIVE 단일 제공자 유지. Bridge/Notifier·기존 예약 작업 정의·스케줄 건드리지 않는다. 본 MD는 REQUEST/READY가 아니며 모델 리뷰 실행 신호가 아니다.

## 2. 최신 기준 확인
1. `collab/START_HERE.md`, 이 프로젝트의 `CURRENT.md` **최상단 최신 절**, `CLAUDE_C_SHADOW_AND_E_REVIEW_ONE_SHOT_RESULT_FOR_GPT_20261112.md`, 기존 C 단계 시험 스크립트와 수정 내역 확인. 이전 C 리허설과 이번 실 GitHub 시험을 구분.
2. 사용자가 전달한 **직전 호스트 보고**: watcher=프로세스 0/마지막 스캔 21:36, dashboard updater=11일 00:10 이후 로그 없음, 두 예약 작업 마지막 결과 `3221225786` (Win32 NTSTATUS `0xC000013A`; 콘솔 강제 종료/CTRL_C_EVENT와 일치할 수 있지만 종료 원인은 미확정), notifier=Running, Bridge=Ready/5분 작업 정상, 재부팅 관측 없음.
3. C 사용자 보고: 최소 권한 비관리자 시험계정 실제 GitHub 3주기, GET 7회 (200×5/304×2), GitHub 쓰기 0/모델 0, `no dispatch` PASS. ETW 원본 70,669 이벤트 중 대상 PID 0, **양성 대조 PID도 0** → 수집/상관관계 실패, `C=PARTIAL, ETW=FAIL`. PID 자체 출력 기준으로 수정된 스크립트는 문법만 PASS. 실패시 추적 파일 보존하도록 변경됨. 운영 DB 접근 0이라는 결론으로 승격하지 않는다.
4. 최신 GitHub 상태가 진행 중 변했을 수 있으므로, 상기 보고와 현재 관측을 시점별로 구분하고 실제 재조회/호스트 실측을 우선한다.

## 3. 우선순위 A — 기존 운영 프로세스 복구 (즉시, 순서 준수)
1. **실제 복구 전 read-only 관측**: 기존 watcher/updater 작업명·PID/부모 PID·작업 정의(실행 사용자/경로/동작/시작 옵션)·LastTaskResult/LastRunTime, 로그 최근 기록, 단일 인스턴스, 현재 Dropbox LIVE 요청/실행 원장/REVIEW_UNCERTAIN/잔여 LOCK을 확인. 실제 큐 원문/개인정보는 외부 게시 금지. 로그·DB에 쓰기 없는 방식으로 진단; SQLite read-only 조회의 WAL/SHM 영향에도 주의. Windows 프로세스 관측과 작업 정의 조회로 가능한 선에서 수행.
2. **기존 승인·중복 호출 안전 확인**: 활성 유효 READY/보류 요청이 있더라도 새로운 유료 reviewer 호출을 승인한 것은 아니다. 기존 정책의 정식 유효 서명/예산/중복키/REVIEW_UNCERTAIN 재호출 방지와 이전 요청별 기발급 승인 여부를 확인한다. 위험을 해소하지 못하면 watcher 신규 시작은 `BLOCKED_REVIEW_CALL_RISK`로 보고하고, 대시보드 갱신기만 복구하며 다른 허용 시험을 진행한다. 운영 중 정상 허가된 요청을 임의 삭제·보류·수정하지 않는다.
3. 전제조건 충족시 **기존 작업 스케줄러 정의 그대로**, 사용자 승인한 기존 watcher와 dashboard updater 예약 작업만 명시적으로 시작한다. 새 작업/계정/작업 정의를 생성하지 않는다. 이미 실행 중이면 중복 시작하지 않는다. 작업이 종료/오류로 표시되거나 멈췄다면 정확히 해당 기존 예약 작업만 1회 시작, 실패 원인 수집 후 무한 재시도 금지.
4. **복구 확인**: 실제 Python PID/command line·단일 인스턴스/작업 스케줄러 실행상태, watcher의 **새 스캔 시각이 이전 21:36보다 증가**했는지, updater의 새로운 갱신 로그와 갱신 시각이 11일 00:10에서 증가했는지 확인. 가능한 경우 정상적인 2개 이상 주기 관찰. 단순 `Running` 또는 LastTaskResult 0만으로 완료 주장 금지. 알림기·Bridge도 전후 상태가 불변인지 확인.
5. 출발 시각/수동 start 결과/자동 재종료 여부/NTSTATUS 해석·실제 확인 근거를 기록. 코드 `0xC000013A`만으로 '사용자가 창을 닫았다'고 단정하지 않는다.
6. 재시작 후 운영 큐·알림 중복/감시기 모델 실행·유료 과금 여부를 확인하되 **새로 리뷰 호출을 유발하는 진단 금지**. 정상운영에서 기승인 요청 처리 사실을 새 승인으로 오인하지 않는다.

## 4. 우선순위 B — 수정된 C 실제 GitHub SHADOW ETW 재시험
1. 감시기 복구와 별개의 비관리자 시험계정/완전 격리 SHADOW에서만 수행. 현재 유효한 repo 한정 Contents:Read-only PAT 사용, 기존 과권한 자격 재사용 금지, 민감값 출력·로그·GitHub 게시 금지. 시험용 계정 활성화/정리는 이전에 승인된 격리 시험 범위로 한정. 운영 DB·main/WAL/SHM·lock·LIVE task·notifier/Bridge 변경 금지.
2. 수정된 호스트 스크립트를 실제 실행하고 **시험 프로세스가 출력한 PID + 시작/종료 시각 + 프로세스 트리(자식 포함)**로 ETW 이벤트와 상관관계 설정. PID 재사용/ETW 이벤트의 provider/시계/버퍼 누락 가능성 검사. PID 이외 file path/event type/행위도 함께 검증.
3. **양성 대조 필수**: 동일 수집·해석 경로에서 독립적으로 제어된 안전한 미끼 파일 열기/읽기/닫기 이벤트가 ETW에 검출되지 않으면 즉시 `ETW=FAIL_UNTRUSTED_MEASUREMENT`. 추적 원본을 보존하고 어떤 경우에도 '운영 DB 파일 접근 0' PASS 금지.
4. 양성 대조가 입증된 경우, **해당 시험 PID/자식 프로세스의 운영 파일** `state.sqlite3`, `-wal`, `-shm`, `watch.lock`에 대한 Open/Read/Write/Create/Rename/Delete/Lock 관측을 유형별로 분류. 단순 총 이벤트 0이 아니라 수집 검출 가능성·필터·양성 대조·운영 파일과의 경로 대조 증명. 기존 운영 watcher의 정상 I/O와 SHADOW 시험 프로세스 I/O를 구분.
5. 실제 GitHub Contents GET에 대해 **연속 3주기**, 200/304·GET 수·쓰기 메서드 0·신규 REQUEST/READY 0·모델/Telegram 0·단일 Dropbox LIVE/SHADOW 상태를 기록. 준비 조건 미충족시 해당 시험을 `BLOCKED`하고 합성 결과로 대체하지 않는다.
6. 실험 종료 후 시험계정 비활성/토큰 사본 안전 삭제(원본 신뢰 저장소/운영 자격 자체는 건드리지 않음)/격리 실행 상태 정리. **실패/불완전 측정 시 원본 추적파일은 접근 보호된 로컬 격리 위치에 보존**하고 원격 PRIVATE라도 raw 로그/경로/식별자/자격증명 게시 금지. PASS더라도 필요한 비민감 증거 집계만 게시하고 원본 보존/삭제 사유 기록.
7. PID 수정·구문검사 PASS는 ETW 계측 성공 증거가 아님. `C_REAL_GITHUB_READ`와 `C_ETW_OPERATING_FILE_ISOLATION`을 **별도 상태**로 기록; 두 조건 모두 실제 PASS인 경우에만 `C=PASS(HOST_REAL)`.

## 5. 결과 게시 (PR 없음, 원샷 종료)
- 새 결과 문서: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CLAUDE_OPERATIONS_RESTART_AND_C_ETW_RERUN_RESULT_FOR_GPT_20261112.md`. 이전 결과를 덮어쓰지 말 것.
- 비민감 요약만 기록. 필수 판정: `WATCHER_RESTART`, `DASHBOARD_RESTART`, `SCAN_PROGRESS`, `DASHBOARD_PROGRESS`, `C_REAL_GITHUB_READ`, `C_ETW_POSITIVE_CONTROL`, `C_ETW_OPERATING_FILE_ISOLATION`, `C_OVERALL`, `DROPBOX_ACTIVE_PROVIDER`, `MODEL_NEW_CALLS`, `COST_INCURRED`, `SHADOW_ACCOUNT_RESTORED_DISABLED`, `HOST_CONFIG_UNCHANGED`, `INDEPENDENT_REVIEW=NOT_RUN`, `CUTOVER=MIGRATION_NOT_CUTOVER`.
- 실패·부분 성공 시 `BLOCKED/FAIL/PARTIAL`을 정확히 기록하고 나머지 작업 계속. 로그 증거는 로컬에 보존. 진단을 위해 기존 운영 DB·감시기 정책을 수정하지 않는다.
- 결과 MD를 GitHub PRIVATE `main`에 **PR 없이 직접 게시**하고 `CURRENT.md` **최상단에 단일 최신 절 추가**. 원격 파일 내용·Git commit SHA 재조회. 게시 실패 시 `NOT_POSTED/UNVERIFIED`, 결과 로컬 보존.
- 이 승인에서 `pythonw.exe` 전환, 예약 작업 정의 변경, 운영 키·토큰 변경, 반출·정식 유료 독립 리뷰, PUBLIC 배포, LIVE cutover **실행 불가**. 필요하면 차후 제안만 별도 기록.

## 6. 실행 의미
이 GitHub 문서의 게시만으로 Windows Claude Code가 자동 실행되지는 않는다. Windows Claude Code가 이 인계서를 읽어 **기존 예약 작업 복구 → C 재측정 → 결과 MD 게시**를 한 번에 실제 수행해야 한다.
