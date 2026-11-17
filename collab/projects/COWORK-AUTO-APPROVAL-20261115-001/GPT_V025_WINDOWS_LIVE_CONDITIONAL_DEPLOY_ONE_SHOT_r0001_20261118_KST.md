# Windows Claude Code 원샷 — v0.2.25 GitHub LIVE 조건부 배포 승인·설치·검증·필요시 롤백

- **저장소:** GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`
- **정본 브랜치:** `main`
- **정확한 인계 상대 경로:** `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/GPT_V025_WINDOWS_LIVE_CONDITIONAL_DEPLOY_ONE_SHOT_r0001_20261118_KST.md`
- **기존 Work:** `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/`
- **승인 사실:** 사용자가 v0.2.25 Windows LIVE 조건부 배포(운영 설치·설정 정합화·격리시험·백업·필요시 롤백)에 대한 GPT의 제안에 “그래”로 명시 동의. **같은 범위의 재승인은 요구하지 말 것.** 이 채팅 동의는 호스트의 보호된 서명 위임·키 변경 권한을 자동으로 대체하지 않는다.
- **금지:** 신규 유료 모델 호출/독립 리뷰 재실행, 새 REQUEST·READY·APPROVAL_SIG, 새 키/토큰, 별도 DB 이행·초기화, PUBIC 게시, provider 추가/동시 LIVE, Notifier 재설치, Telegram 시험 발송, /AI-CONTINUITY/ 변경. 기존 운영 권한을 벗어나는 보호 위임·키 변경은 fail-closed.
- **목표:** **기존 GitHub watcher v0.2.23 → v0.2.25**를 같은 단일 LIVE provider에서 안전 교체. 배포 뒤 보호 범위에서 허용된 일반 리뷰 요청당 $1.50 / DESIGN 요청당 $3.00, 일·월 누적 횟수/비용 상한 제거, 기존 요청당 1회·서명·원본 핀·중복 방지 유지. 할 수 없는 항목은 부분 완료/차단으로 분리하여 과장 금지.

## 0. 입력·현재 확인된 사실

1. 먼저 `collab/CONTEXT_BRIEF.md`, 이 Work `CURRENT.md` **최상단**, 이 문서 및 `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md` 최신 상태, 기존 운영 승인/설치 계약을 필요한 만큼만 확인한다. 최신 사용자 동의와 실호스트 현황을 우선한다.
2. **설치할 원본 ZIP 하나:** `collab/packages/skill-collab-watcher_v0_2_25_1117.zip`, **283930 bytes**, SHA-256 **`26d63c8a03290499b13b2ceb8ff0b70c06eb1b1bcc1a25fe3d8f65fcc213d228`**, 원격 Git blob `660ff3591defd8ccc4abdf3e9b2bf24f21b13918`. 새 빌드·재압축·ZIP 바이트 변경 불가; 원격 raw bytes 기준 SHA·크기·CRC·압축 경로 이탈/심볼릭 링크/비밀 검사.
3. **독립 리뷰 1회 종료:** `REQ-COWORK-BUDGET-V025-LARGE-R2-20261117`, USD 0.8061916, `REVIEW_RESULT_1.md` / `RECEIPT_1.md` / `USAGE_RECEIPT_1.json`. GPT 최종 `ACCEPT_WITH_CHANGE`, BLOCKING 0, M1은 ZIP 밖 `collab/ops/review_request_gate.py`를 독립 리뷰어가 볼 수 없었던 **범위 공백**. [GPT 판정](GPT_V025_LARGE_R2_DISPOSITION_r0001_20261117_KST.md) 유효; 유료 리뷰 2회차 금지.
4. **최신 Windows G0 보고:** [G0 결과](CLAUDE_V025_LARGE_R2_G0_HOST_VERIFICATION_RESULT_FOR_GPT_20261118.md): 실제 운영 트리 `D:\\User\\whpark\\skill-collab-watcher-github` v0.2.23, v0.2.25 미설치. 운영 `config/reviewer.config.json`에서 `daily_budget_usd=null`, `max_dispatches_per_day=null` + 변경 전 백업 존재. 별도 보호 위임 `auto_delegation.json`은 **max_request_usd=1.0, max_day_calls=2, max_day_usd=3.0, max_month_usd=10.0, enabled=true**. 이 위임이 그대로면 목표 $1.50/$3 및 상한 완전 제거 **실효 정책 미충족**. G0 문서에 없는 운영 접근권/설정 지원 API를 추정하지 않는다.
5. **REQUEST 사전 검증 도구는 ZIP 내부 모듈이 아님:** GitHub PRIVATE `collab/ops/review_request_gate.py`, `collab/ops/tests/test_review_request_gate.py`. CI `#44093146832` synthetic 23 PASS. 운영 설치 폴더에 없었다는 G0 사실 유지. 이번 설치에서 watcher 코드에 무검증 자동 연결했다고 주장하지 말 것.

## 1. 원샷 실행 순서 — 각 게이트 PASS면 바로 다음 단계, 매 단계 사용자 재확인 불필요

### A. 배포 전 상태·승인·무손실 백업 (아직 변경하지 않음)

- 설치 작업자가 실제 Windows 운영 호스트·사용자·권한, 운영 Python/venv, GitHub watcher **단일 활성 Task/PID/provider**, 기존 비활성 Dropbox, 원격 실상태를 확인. 다른 세션/Task가 동시 변경 중이거나 새로 실행할 **유효·미처리 READY가 있어 모델 호출이 발생할 가능성**이 있으면 안전한 quiescent 상태를 확보하기 전 중지. 완료·UNCERTAIN/레거시 pending을 재큐잉·삭제하지 말 것.
- `CURRENT` 및 `G0`가 이미 보고한 보호 위임의 한도와 만료/허용 프로젝트/스킬/서명 권한을 **실제 로컬 보호 정책으로** 재대조. 이번 사용자 승인 범위에서 **정당한 기존 보호 정책 변경 절차가 유효하게 제공되는지** 판단. 현재 권한/유효 절차로 변경 불가하면 delegation 파일을 임의 편집·우회하지 않고 `BLOCKED_POLICY_AUTHORITY`로 멈춰 정확한 권한 차이만 보고. 비용 제한을 불일치 상태로 둔 채 목표 운영 달성 PASS로 보고하지 말 것.
- 충분한 저장 공간, 기존 rollback 버전의 정확 바이트, 보호 정책과 서비스 구성의 변경 전 파일을 검증한 뒤 백업/복구 계획 확정. **가동 중 DB 원본을 SQLite 읽기 질의로 임의 접촉하지 말 것.** 공인된 안전 정지/quiesce 후 DB(main/WAL/SHM) 및 Task XML/설정/설치본/신뢰 루트·Notifier 워터마크 **보존용 바이트/해시**를 별도 백업. 원본 경로·키·토큰/DB bytes는 GitHub에도 게시 금지. 복원은 모델/Job 불확실 후 무조건 과거 DB로 덮어쓰지 않고 차이를 대조해 필요할 때만 수행.
- 기존 LIVE의 설치·교체·rollback 스크립트/서명 검증 방법과 Windows 3.11 사용 경로를 실제 찾아 재사용. 임의 설치 도구/API 발명 금지. Windows/정책/승인·저장소 접근 차단 시 변경하지 않고 결과 보고.

### B. LIVE와 분리된 후보 격리 시험

- SHA 고정 ZIP을 독립된 안전 임시 디렉터리에만 해제. 설치본/운영 DB/Task 변경 **전** Windows unit regression과 v0.2.25 변경 영향 함수 테스트를 실행. 임의로 시험 결과를 Linux CI PASS로 대체하지 말 것. 설치본과의 버전·파이썬·의존성 정합 확인.
- **SHADOW/FAKE** runner에서 정책 맵 (`POLICY-STATIC-V1=1.50`, `POLICY-STATIC-V1-DESIGN=3.00`), `--max-budget-usd`, 인증 실패/만료, malformed/NaN/Inf/불일치, $1 위임이면 1.5/3 fail-closed, 등록 policy 빠지면 거절, 일·월 누적 상한 제거와 요청 ID별 1회/UNCERTAIN 재실행 금지, SQLite 경합/재시작·원격 예약 결속, ZIP/문자열 repo_id 확인. 기존 R2 N1의 레거시 정책 list형이면 실제 정액 맵 값과 동작을 확인; 정액이 떨어지는 구성이면 승인 범위 내 기존 dict형 설정으로 최소 이행.
- `collab/ops/review_request_gate.py`는 **별도 저장소 도구**로 source bytes SHA pinned/readback 후 Windows 복사본을 준비해 원본과 비교, 실제 Windows 로컬 reviewer.config.json의 **비밀을 공개하지 않고** `select` / 격리된 **새 가상 REQUEST 초안에 대한 `check`** 기능을 모델/REMOTE WRITE 0으로 시험. 이 도구는 reviewer가 R2에서 읽지 못한 범위라서 `INDEPENDENT_REVIEW=NOT_RUN`을 유지; 현재 watcher 패키지 안에 추가/수정하거나 기존 완료 REQUEST를 수정·재큐잉하지 말 것. 새로운 REQUEST 작성자는 배포 뒤 이 도구의 검증 결과를 받아 REQUEST 게시 전에 확인할 수 있어야 한다. 운영 등록/자동 강제 호출 여부는 실제 연결 증거가 없는 한 `AUTOMATIC_PREFLIGHT_INTEGRATION=NOT_VERIFIED` 표기.
- **A/B 중 어느 것도 FAIL이면 LIVE 교체 금지.** 허용 범위에서 재현/최소 원인 확인 및 격리 후보 수정은 가능하나 **수정된 다른 SHA를 이번 배포 승인 원본으로 교체할 수 없음**. 신규 유료 리뷰 금지.

### C. 조건 충족 시만 원샷 안전 교체 및 실제 확인

- 사용자 승인된 기존 절차로 **동일 검증 ZIP 바이트**를 v0.2.25 신규 버전 설치본으로 준비. 기존 v0.2.23 실행을 quiesce/stop하고 단일 Task·단일 LIVE provider/lease를 유지하도록 **원자적으로 또는 되돌릴 수 있게** 활성 경로를 전환. 기존 DB/완료/UNCERTAIN/영수증, 백업, 예약 Task, 알림 정책 무손실. 다른 GitHub/Dopbox watcher 동시 활성 금지.
- 기존 `reviewer.config.json`의 **필요한 필드만** 목표 비용 맵 $1.50 / $3, 일·월 누적 횟수·비용 gate `null`/비활성으로 설정·검증. 보호 위임의 **갱신이 필요한 경우에는 사용자 본 승인 범위와 실제 유효한 별도 보호 서명/위임 절차가 모두 허용함을 확인한 뒤**, 계약이 요구하는 방식으로만 갱신. 직접 신뢰 루트/키 회전·위조·보안 검사 완화 금지. 유효 보호 위임 없이 $3 자동서명 성공을 주장하거나 실행하지 말 것. 이전 `POLICY-STATIC-V1-LARGE` 수동 승인 방식은 별도 유지.
- 시작 전 **기존 완료·미정산 REQUEST, 원격 READY 목록과 비용 중복 위험** 대조. 실모델 호출 0인 비발송·비실행 smoke로 실제 task/버전/설정/프로세스/락/provider·정상/거부 검증. **2번 이상의 정상 watcher 주기 + 제어된 재시작 1회**에서 오작동·중복·불확실 요청 새 실행 0, 모델 호출 0, notifier 알림 시험 발송 0, 원격 원본 이력 변화 0을 확인. 클린 신규 유효 요청의 실제 유료 리뷰는 이번 승인 범위에 포함되지 않음.
- 조건 통과 + 실제 운영 상태 확인 때에만 `LIVE_INSTALLED=PASS`, `LIVE_VERSION=0.2.25`, `ACTIVE_PROVIDER=GITHUB`, `POLICY_EFFECTIVE=PASS`, `HOST_APPLIED=PASS`로 기록. **SHADOW PASS만으로 LIVE PASS를 만들지 말 것.**
- 이상/성공 불확실 시 새 watcher 중단, 신규 디스패치·서명 중지, 롤백 가능한 **v0.2.23 설치·Task·설정만** 안전하게 복원(복구 가능성과 유효 안전 승인 확인), 비용/완료 이력 DB를 과거 스냅샷으로 무조건 덮어쓰지 않음. 실제 안전하게 복원한 경우만 `ROLLED_BACK=PASS`, 그 외 `BLOCKED/UNCERTAIN` 기록. 사전 오류와 설치 후 장애를 구분. 새로운 provider 활성화/유료 호출 금지.

## 2. 결과 형식 및 종료 기준 — 추가 핑퐁 금지

- 정확한 결과 경로: `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/CLAUDE_V025_WINDOWS_LIVE_CONDITIONAL_DEPLOY_RESULT_FOR_GPT_20261118.md`.
- 필수 보고: `INPUT_SHA256`, `ZIP_BYTES`, `WINDOWS_PYTHON`, `INSTALLED_BEFORE/AFTER`, `EXISTING_PROVIDER`, `HOST_CONFIG_BACKUP_SHA`, `DB/WAL/SHM_BACKUP_SAFETY`, `DELEGATION_AUTHORITY_SCOPE`, `PROTECTED_DELEGATION_EFFECTIVE`, `WINDOWS_UNIT_TEST`, `SHADOW`, `GATE_CLI_SELECT_CHECK`, `AUTOMATIC_PREFLIGHT_INTEGRATION`, `POLICY_BASE_1_50`, `POLICY_DESIGN_3_00`, `DAILY_MONTHLY_CEILINGS`, `UNIQUE/UNCERTAIN`, `HOST_INSTALLED`, `TWO_CYCLES_RESTART`, `ACTIVE_PROVIDER`, `ROLLBACK_READY`, `HOST_APPLIED`, `MODEL_CALLS=0`, `NEW_REVIEW_REQUESTS=0`, `OPEN_BLOCKERS`.
- PASS/FAIL/SKIP/NOT_RUN/UNCERTAIN은 실제 시험·설치 단계별로 분리. 로그/백업은 Windows 로컬 보존, PRIVATE는 비민감 요약·hash/버전/정확한 Windows 증빙 위치(비밀·전체 경로 공개 지양). 기존 R2/영수증/REQUEST/READY 변경 없음.
- 작업 완료·차단 어떤 경우든 **위 결과 MD와 기존 `CURRENT.md` 최상단/현행 `TRACKER.json`를 동일 Work에서 PRIVATE `main`에 PR 없이 직접 게시**, commit·원격 본문과 SHA-256 readback. 새 Work/스키마/리뷰 요청·LIVE provider 생성 금지.
- GPT는 결과 수신 뒤 별도 유료 독립 리뷰 없이 `HOST_APPLIED=PASS/FAIL/PARTIAL`, 배포 승인 조건 충족 여부를 판정한다. 호스트에서 실제 PASS 전에는 문서에 `LIVE_v025=NOT_VERIFIED`로 유지한다.

## 3. Windows Claude Code에 전달할 1회 문구

> GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab` branch `main`의 `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/GPT_V025_WINDOWS_LIVE_CONDITIONAL_DEPLOY_ONE_SHOT_r0001_20261118_KST.md`를 열고, 사용자 승인한 v0.2.25 GitHub LIVE 조건부 배포를 추가 재승인 질문 없이 끝까지 실행해줘. 고정 ZIP SHA-256 `26d63c8a03290499b13b2ceb8ff0b70c06eb1b1bcc1a25fe3d8f65fcc213d228`/283930B를 확인하고 Windows v0.2.23 운영·보호 위임·원격 READY·백업/복구 계약을 먼저 확인한 뒤, Windows 격리 회귀·SHADOW·사전 게이트 검사와 유효한 비용/위임 설정을 확인해. 모두 PASS일 때만 v0.2.25로 안전 교체하고 단일 provider·두 주기+재시작·모델 호출 0·중복 0을 실측해. 보호 위임/키 권한·롤백/원본 검증에 차단이 있으면 우회하지 말고 기존 LIVE를 보존하거나 안전 복원 후 BLOCKED 보고. 추가 유료 리뷰·REQUEST/READY·키/DB 이행/PUBLIC 게시 없이 `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/CLAUDE_V025_WINDOWS_LIVE_CONDITIONAL_DEPLOY_RESULT_FOR_GPT_20261118.md`와 `CURRENT.md`/`TRACKER.json`을 PRIVATE main에 게시, commit/readback을 확인해줘.
