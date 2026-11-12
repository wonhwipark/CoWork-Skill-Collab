# CoWork — ETW 귀속 보정·C 최종 검증·운영 지속성 읽기전용 확인 통합 인계
작성: 2026-11-12 KST | rev: r0001
STATE: GPT_DIAGNOSTIC_PREPARED / WINDOWS_HOST_EXECUTION_NOT_OBSERVED
저장소: **GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`**
브랜치: **`main`**
정확한 경로: **`collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_ETW_ATTRIBUTION_C_FINAL_CHECK_ONE_SHOT_r0001_20261112.md`**
work_id: `COWORK-DROPBOX-TO-GITHUB-MIGRATION`

## 0. 실행 계약과 권한 경계
- **사용자 진행 지시**에 따라 *측정기 보완 → 기존 실패 자료 재분석 → 신뢰 가능한 양성대조 사전검증 → 조건부 C 실계측 1회 → 운영 감시기/대시보드 동작 이력 관찰 → 결과 직접 게시*를 원샷으로 수행한다. 이전 실행 프롬프트/조건과 중복으로 예전 시험을 무의미하게 반복하지 않는다.
- 읽을 자료: `collab/START_HERE.md`, 현재 작업 `CURRENT.md` 최신 절, `GPT_OPERATIONS_RECOVERY_AND_C_ETW_DISPOSITION_r0001_20261112.md`, `CLAUDE_OPERATIONS_RESTART_AND_C_ETW_RERUN_RESULT_FOR_GPT_20261112.md`, 운영 안전 계약.
- 기존 Dropbox **유일한 LIVE v0.1.5**를 변경·중단하지 않는다. v0.2.10 후보도 운영 설치하지 않는다.
- **운영 watcher/updater 재시작, 작업 정의 변경, pythonw 전환, 실제 운영 DB·WAL·SHM/lock 접촉, 신규 토큰/키 발급, 운영 정책·인증 변경, REQUEST/READY 발행, 유료 reviewer 호출, GitHub LIVE 전환, PUBLIC 게시**는 포함되지 않는다. 호스트에서 재중단이 확인되면 원인·시각과 BLOCKED 기록만 남기고 임의 재시작하지 않는다.
- Windows 관리자 권한이 필요한 실제 추적 1회는 **양성대조/ETW provider/프로세스 ID 검증이 먼저 통과한 경우에만** 진행하고, 사용자 관리자 셸 개입이 필요한 환경에서는 준비 완료한 단 하나의 명령과 안전 조건을 제시한다. 사전 통과 전 관리자 명령 반복 지시 금지. 권한/환경이 없어 시행 못 한 경우 `NOT_RUN/BLOCKED`, 나머지 계속.
- 결과/시험 원본에 운영 DB/요청 ID·업무 코드/로그·실 경로·토큰/키 등이 포함될 수 있으므로 **LOCAL_ONLY, GitHub PRIVATE에도 원본 반출 금지**. PRIVATE에는 집계·불리언·비밀 제거된 판정만 게시.

## 1. 기존 C 결과 — 절대 소급 PASS 금지
- Windows 보고: 실제 GitHub Contents read-only GET 3주기/7회(200×5,304×2)·쓰기 0·모델 0 → `C_REAL_GITHUB_READ=PASS(HOST_REAL_REPORTED)`.
- ETW 2차 약 54,580건(129 PID) 중 probe 자체 PID 14524에는 파일 이벤트 0. 미끼 파일과 샌드박스 이벤트는 25308 등 다른 PID에서 관측. 양성대조의 시험 프로세스 귀속 미증명.
- `C_ETW=FAIL_UNTRUSTED_MEASUREMENT`, `C_OVERALL=PARTIAL`. 이 수치나 기존 synthetic C/ACL의 PASS를 **실 운영 DB 무접근의 증명으로 바꾸지 않는다**.
- 운영 감시기 9~10분 새 스캔 8건 이상, 대시보드 2차 시작 후 5분 이상 생존/로그 갱신은 `PASS_SHORT_TERM_REPORTED`; 장기 가동 PASS 아님. 첫 대시보드 0xC000013A 종료 원인 미상. 2차 재시작은 이전 인계 한도 초과로 기록됐으므로 본 인계에서 **추가 재시작 권한 없음**.

## 2. GPT 제공한 원샷 사전검증 코드
- `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/tools/etw_attribution_preflight_r0001.py`
- `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/tools/test_etw_attribution_preflight_r0001.py`
- GPT 환경 `python -m unittest -v test_etw_attribution_preflight_r0001.py` → **9 PASS, 0 FAIL**, 독립 offline normalized-data 합성시험. GitHub 파일은 시험한 로컬 파일과 Git blob hash 일치:
  - 프로그램: SHA-256 `443755937d9eef7a34b84166a75aee31bdcf94721a2fe3a3ec16eeaa5f25eda8` / Git blob `cd02ab5d44315c257812ed3e07cf1d4b3b67d5b3`.
  - 테스트: SHA-256 `cbba9cab12f81a8e7d77e7354c7e4d49efc7619c603062a46a0182e6a3035d19` / Git blob `2f3335292cc241b72ba2777e080ac026214a77fb`.
- **주의**: 이 코드가 읽는 것은 *정규화된 JSON*이며 원본 ETL/CSV parser가 아니다. `collection.*_verified` 플래그는 **Windows에서 실제 검증된 사실을 사람이/도구가 확인한 후에만 true로 설정**할 것. 테스트 자료에 true를 임의로 대입해 운영 실측 PASS를 만들 수 없다.
- 파일 경로 대조는 단순 문자열 정규화 예제이므로 Windows junction/UNC/8.3 alias/NT object path·case·hardlink에 대해 완전하지 않다. Windows에서는 **파일 identity 기반 정규화 검증**이 별도 필수. 이 스크립트의 `NO_ACCESS_EVENTS_IN_VERIFIED_TRACE`는 독립적으로 검증된 Windows 실제 ETW I/O 안전성 PASS가 아니다.
- 기존 호스트 raw ETW 데이터를 먼저 local-only 정규화/검증하도록 하고, 필요하면 host-only ETW parser를 **운영 복사본 또는 격리 스크립트**에서 개발·단위시험한다. RAW ETL/CSV, PID/TID/로그 원문, 운영 폴더 경로가 들어간 normalized JSON은 GitHub에 올리지 말 것.

## 3. ETW 귀속 진단 (관리자 재시험 전에)
A. **기존 보존 추적 먼저 분석**. trace session provider/시작·종료 UTC/이벤트 누락·버퍼 손실·이벤트 컬럼 schema(Event PID, ProcessID, ThreadID, source PID, container/process session)/CSV export mapping/시계 정합성을 확인한다. 이전 PID 14524와 이벤트가 찍힌 25308·부모/자식 프로세스의 생성/종료 시각, image identity/PowerShell runner/wrapper 계층, 세션/로그온 토큰을 대조한다. *단순 PID 숫자 일치만으로 의도적 가공 금지.*
B. **Kernel-Process 및 FileIO provider의 실제 식별자 매핑**. ProcessStart/Stop/parent-child/ThreadStart/Stop과 파일 Open/Read/Write event의 PID/TID 관계를 동일 ETW session에서 확인. 특정 file event가 다른 PID에서 보고되는 이유를 event field semantics까지 포함해 설명. Thread ID만 동일하다고 다른 PID 이벤트를 자동 귀속시키지 않음.
C. **미끼 양성 대조의 실행 주체 일치**. 시험 Python 프로세스나 그 **입증된 자식**이 직접 새로 만든 무해한 marker file을 열고 닫음. 제어 이벤트의 process tree, 생성 시간·TID·파일 identity가 유효할 때만 `POSITIVE_CONTROL=PASS`. 별도 PowerShell/프로세스의 미끼 열기는 '전체 ETW 수집 장치가 동작한다'는 보조 증거일 뿐 시험 대상에 대한 양성 대조가 아님.
D. `etw_attribution_preflight_r0001.py`의 9 synthetic test를 Windows 격리 복사본에서 재실행. ETW 원본→normalized 변환의 parser **golden fixtures** 및 PID 불일치/유효 자식/재사용/시간 범위/누락·이벤트 필드 오류를 재시험. 필요 시 코드 오류 수정·Windows 전용 시험 확대(그때는 새 결과에 별도 시험 수 보고). 원본 파일 덮어쓰기 금지.
E. 다음 조건 전부 검증 시만 `ETW_MEASUREMENT_PREFLIGHT=PASS`: (i) 이벤트 provider & 정확한 PID/TID 필드 매핑, (ii) ProcessStart/child lineage 및 timestamp, (iii) trace 범위 전체와 events lost=0, (iv) 양성 control이 같은 probe process/증명된 child에 귀속, (v) 대상 파일 identity/path alias 매핑, (vi) 새 코드/테스트 회귀 통과. 불명확하면 `FAIL_UNTRUSTED_MEASUREMENT` + raw trace 로컬 보존.

## 4. 조건부 단일 실제 C 재측정
- **절대로 preflight FAIL 상태에서 관리자 셸 재시험 반복하지 말 것.**
- 사전검증 PASS이고 관리자 사용 가능할 때만 1회 수동 실행. 호스트의 사전 승인된 격리형 SHADOW + 현재 유효한 repo **Contents:Read-only** 토큰/비관리자 시험계정 사용. token 값 출력/원격 게시·과권한 gh 쓰기 인증으로 대체 금지.
- 3 watch 주기, 실제 GitHub GET 200/304 카운트, GitHub HTTP write 0, Dropbox write 0, READY 신규 0, model runner 0/과금 $0, Telegram 0, single Dropbox LIVE, runtime code의 운영 state DB/lock open 0을 **서로 독립된 근거**로 기록.
- 동일 trace 안에서 시험 프로세스/입증된 자식의 자체 marker Open 이벤트 ≥1, 이벤트 누락 0, 프로세스 ID·수명·파일 ID 매핑 증명. 운영 `state.sqlite3` / `-wal` / `-shm` / `watch.lock`의 Open/Read/Write/Create/Rename/Delete/Lock을 대상 lineage에서 **0**이라고 판정할 수 있을 때만 `C_ETW_OPERATING_FILE_ISOLATION=PASS_HOST_REAL`.
- ETW 추적 이벤트가 0이어도 양성대조가 불검출/프로세스 귀속 실패면 `FAIL_UNTRUSTED_MEASUREMENT`. 운영 Dropbox watcher 고유 I/O와 시험 SHADOW I/O를 분리해야 함.
- 종료 후 시험계정 비활성·토큰 임시 사본 제거 검증. 미확인/실패 trace 원본 관리자 전용 로컬 보존. 여러 관리자 재시험은 새 명시적 승인 없이는 금지.
- 성공 시 `C_REAL_GITHUB_READ=PASS` + `ETW_CONTROL=PASS` + `C_ETW_ISOLATION=PASS`일 때만 `C_OVERALL=PASS_HOST_REAL`. 그렇지 않으면 PARTIAL.

## 5. 운영 지속성 확인 (읽기 전용, 새로운 자동 감시 없음)
- 본 세션 시작·종료 시점에 Windows scheduler status, 실제 감시기 parent/child PID, watcher last-scan sequence/시간, dashboard updater parent/child PID 및 로그/HTML last-write, notifier/Bridge 상태를 읽기 전용으로 확인. 기존 로그가 허용하면 **최소 2개 관찰 지점**의 경과 시간을 기록하고 실제 스캔·갱신이 증가했는지 확인.
- 해당 시점과 스캔 간격·실패/재시작 카운트·0xC000013A 재발 여부를 구분. **5~10분 통과로 24시간 안정이라고 주장 금지.** 이미 경과한 24시간 분량의 신뢰 가능한 로그가 없으면 `LONG_RUN=PENDING`.
- scheduler 정의·trigger·python.exe/pythonw.exe·데이터 DB·프로세스 신호 변경 금지. 중지 상태라도 **이번 승인에 재시작 권한 없음**. 멈춤의 원인/근거와 부작용 없는 복구 제안만 기록.
- 무인 감시 작업/새 모델 호출/Telegram 발송/백그라운드 타이머 자동 실행 설정 금지.

## 6. 결과 MD 게시 및 종료
- 결과 신규 파일: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CLAUDE_ETW_ATTRIBUTION_AND_C_FINAL_CHECK_RESULT_FOR_GPT_20261112.md`.
- 필수 상태: `ETW_TRACE_REANALYSIS`, `PROCESS_TREE_ATTRIBUTION`, `PID_TID_EVENT_FIELD_MAPPING`, `POSITIVE_CONTROL_PREFLIGHT`, `ETW_MEASUREMENT_PREFLIGHT`, `C_FINAL_RERUN`, `C_READ`, `C_ETW_OPERATING_FILE_ISOLATION`, `C_OVERALL`, `WATCHER_LAST_SCAN_PROGRESS`, `DASHBOARD_LOG_PROGRESS`, `LONG_RUN`, `MODEL_CALLS_NEW`, `USD_SPEND`, `ACTIVE_PROVIDER`, `INDEPENDENT_REVIEW`, `CUTOVER`.
- 사전 통과 시각·시험 주기·trace event 수/파일 귀속 요약·실행 명령·Python 검사 PASS/FAIL/SKIP·Windows API/host 측정 증거 종류·추적 원본 보관 여부를 식별값 없이 기록. 검증 불가 값은 `UNKNOWN`/NOT_RUN.
- 산출물 공개 적합성 확인 후 **PRIVATE `main`에 PR 없이 결과 문서만 직접 게시**, 기존 `CURRENT.md` 최상단에 최신 섹션 추가(과거 이력 보존), 원격 readback/commit SHA/UTF-8 바이트 동등성 검증. 승인되지 않은 raw trace/DB/ZIP/토큰 게시 금지. 초기 게시가 깨지면 강제 push하지 않고 신규 정정 커밋.
- 기존 Windows watcher/updater 운영 파일/설정·SQLite main/WAL/SHM·예약작업/Notifier/Bridge·GitHub LIVE/공식 Claude reviewer에는 일절 변경 금지. `INDEPENDENT_REVIEW=NOT_RUN`, `MIGRATION_NOT_CUTOVER` 유지.
- 한 번 수행한 후 새 오류가 있으면 가능한 격리 수정·사전시험 재반복은 작업 내에서 수행하되, 관리자 실제 ETW 재시험 횟수는 위 1회 제한. 결과를 하나로 통합 보고.
