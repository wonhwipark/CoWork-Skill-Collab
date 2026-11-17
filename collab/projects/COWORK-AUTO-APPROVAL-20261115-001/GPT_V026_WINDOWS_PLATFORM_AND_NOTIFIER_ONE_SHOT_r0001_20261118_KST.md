# Windows Claude Code 원샷 — skill-collab-watcher v0.2.26 플랫폼·Notifier 검증과 v0.2.25 기존 배포 상태 정산

- 작성: GPT / 2026-11-18 KST
- 정확한 저장소: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`
- **이 문서의 정확한 상대 경로:** `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/GPT_V026_WINDOWS_PLATFORM_AND_NOTIFIER_ONE_SHOT_r0001_20261118_KST.md`
- 같은 Work: `COWORK-AUTO-APPROVAL-20261115-001`
- 사용자 최신 지시: `skill-collab-watcher` 후속 조치(기존 v0.2.25 운영 결과 확인 → v0.2.26 Windows 회귀·Notifier 어댑터 확인 → 독립 리뷰/배포 판정에 필요한 근거 회수)를 “진행해줘”.
- **범위:** 기존 승인된 v0.2.25 조건부 배포와 **별도**인 v0.2.26 개발 후보의 Windows 격리시험/읽기 전용 운영 호환 확인, 비민감 결과 게시. 이 문서의 PRIVATE 게시는 Windows 자동 실행, 유료 리뷰, v0.2.26 설치 또는 별도 운영 승인 아님.

## A. 최신 사실 및 고정 입력

1. `collab/CONTEXT_BRIEF.md` → 이 Work `CURRENT.md` 상단 → [v0.2.26 구현·시험 결과](GPT_REQUEST_PIN_PREFLIGHT_AND_WAIT_FIX_RESULT_r0001_20261118_KST.md) → 운영 이관 Work `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md`의 최신 부분 → 실제 Windows 설치/알림 스크립트를 필요한 만큼 확인. 최신 실호스트 결과가 앞선 문서보다 우선.
2. **v0.2.25 운영 배포는 기존 조건부 승인 별도 작업**: `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/GPT_V025_WINDOWS_LIVE_CONDITIONAL_DEPLOY_ONE_SHOT_r0001_20261118_KST.md`. 고정 원본 `collab/packages/skill-collab-watcher_v0_2_25_1117.zip` / 283930 bytes / SHA-256 `26d63c8a03290499b13b2ceb8ff0b70c06eb1b1bcc1a25fe3d8f65fcc213d228`. 이미 같은 작업 실행/진행 중이면 **중복 실행 금지**. 원래 승인 범위·보호 위임·롤백 조건을 이 문서로 확장하거나 바꾸지 않음.
3. **v0.2.26 개발 후보만**: `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/artifacts/v0_2_26/skill-collab-watcher_v0_2_26_1118.zip`, **308737 bytes**, SHA-256 **`f08adb6099d06daf494362ed7e33ea66aabcbf749cfd2c027a7f70bcba5540fe`**, 113 members, status `development_not_for_deployment`. `artifacts/v0_2_26/CANDIDATE_MANIFEST.json`, `VALIDATION.json`, `diff_v0_2_25_to_v0_2_26.patch` 확인. 후보 ZIP 재빌드·재압축·운영 설치 금지.
4. 이전 개발 자체시험은 Linux 이식 가능 범위 **974 PASS / 35 SKIP / 원본 실패 34개 제외**, 신규 회귀 **61 PASS**. 전체 suite/Windows PASS **아님**. 새 후보 독립 리뷰 `NOT_RUN`, 운영 Notifier 어댑터 연계 `NOT_VERIFIED`. 기존 MSC 리뷰는 `COMPLETED/ACCEPT_WITH_CHANGE/CLOSED`로 재리뷰 금지.
5. 기존 LIVE provider는 GitHub 단일 provider이며 최근 마지막 호스트 보고는 **v0.2.23 운영, v0.2.25 미설치**. `CLAUDE_V025_WINDOWS_LIVE_CONDITIONAL_DEPLOY_RESULT_FOR_GPT_20261118.md`의 원격 미존재는 GPT의 마지막 조회 시점에만 해당하므로 Windows에서 먼저 최신 확인.

## B. 하나의 세션에서 순차 수행할 작업

### B1. v0.2.25 기존 승인 작업 상태 확인·충돌 방지
- Windows 실제 Task/PID, 활성 provider, watcher 버전, 최근 deployment 결과 파일·commit, 설치/원격 SHA, 보호 위임(비밀 제외), 진행 중 다른 Windows Claude Code 작업, pending/UNCERTAIN 및 현재 모델 실행 상태를 읽기 전용 확인.
- 이미 v0.2.25가 설치·검증됐으면 결과/원격 증거만 회수하고 **다시 설치하지 않음**. 실패/진행 중이면 이유·진행 주체·현재 LIVE 보존 상태를 기록.
- **아직 시작하지 않았고**, 기존 조건부 배포 승인·호스트 보호 권한·quiescence/백업/rollback 게이트가 모두 유효하고 다른 작업과 충돌하지 않을 때에만 **상기 기존 v0.2.25 원샷 문서 그대로** 수행. 단계별 재승인을 반복 요청하지 말 것. 권한/위임 한계로 차단되면 정책 파일 임의 편집·우회 금지, 기존 LIVE 보존 후 `BLOCKED` 기록.
- v0.2.26 ZIP으로 v0.2.25 원샷의 고정 입력을 대체하거나 새 비용/서명 권한을 발명하지 말 것.
- B1이 BLOCKED여도 운영 변경 없는 B2/B3 격리 검증이 안전하면 계속 진행.

### B2. v0.2.26 Windows 전용 격리·회귀 시험
- 실제 Windows Python 경로, 버전(예전 G0는 3.11.9), 의존성·격리 venv와 소스 체크아웃의 commit을 확인. v0.2.26 **원격 원시 bytes** 다운로드 후 SHA-256/크기/CRC/113 members/경로 이탈·심볼릭 링크·비밀 패턴·manifest hash를 안전한 임시 폴더에서 확인. 운영 설치 루트/운영 DB/WAL/SHM/운영 Task/키/토큰을 만지지 말 것.
- 격리된 Windows에서 **전체 suite를 제외 없이 실행**하고 PASS/FAIL/SKIP 및 실패 node ID·원인 분리. Linux에서 제외됐던 기준 실패 34개도 Windows에서 실행하여 플랫폼 차이/fixture/실제 결함을 구분. 테스트 로그 비밀값은 PRIVATE에 게시하지 않음.
- `SOURCE_PIN.repo_id`의 JSON 문자열 타입·commit 길이·schema 공통 검증, 잘못된 숫자형 pin의 `PIN_REPO_ID_TYPE` **자동 예약 전 차단**, 기존 UNCERTAIN 보존/재큐잉 0, READY 성공 뒤 WAIT 미발행, 동일 원인/단계 중복 통지 0 및 원인 변경 1회만, 비용과 모델 미호출/미확인 구분을 Windows fake runner·fake signing·fake sender로 테스트.
- `collab/ops/source_pin.py`와 `review_request_gate.py` 동봉 및 실제 Windows의 `select/check` 함수·동일 pinned 입력 사용 가능 여부를 **가상 요청과 비밀 제거된 실제 정책 조회**로 확인. README/실제 실행 경로 없이 자동 강제 사용됐다고 단정 금지.
- 결함이 있으면 운영 설치·모델 호출 없이 최소 수정안을 별도로 제시하고 재시험. v0.2.26 기존 고정 ZIP의 bytes를 몰래 바꾸지 말 것. 수정 ZIP이 필요하면 새 버전 후보·SHA 및 기존 Work 내 결과로 분리, 사용자 기존 v0.2.25 운영 승인과 혼동 금지.

### B3. Notifier 기존 연결 확인(읽기 전용 + 합성 비발송)
- Windows의 **실제 운영 Notifier 어댑터/설치 스크립트와 호출 지점**을 찾아, v0.2.26의 `notify_events.run_once`·메시지 포맷/워터마크·상태 감사 연동 경로를 실제 코드에 근거하여 매핑. 기존 Windows ↔ Telegram 연동은 사용자 확인된 상태이므로 재연동·키 변경·시험 Telegram 메시지 전송 금지.
- 별도 어댑터가 후보 함수를 호출하지 않으면 `NOTIFIER_ADAPTER_CONNECTED=NO` 및 최소 gap 표시. 실제 운영 Notifier 설치·Task 설정 변경 금지. fake sender와 기존 완료/READY/UNCERTAIN 합성 이벤트로 0회/1회 중복 알림·워터마크 지속·READY 뒤 낡은 대기 억제를 시험.
- `collab/dashboard/review_completion.py`(GitHub Actions 요약)와 기존 Windows Notifier(Telegram)의 책임을 구분. 중복 연결이 실제로 필요하지 않으면 신규 Bridge/엔진·스키마 제안 금지.
- 검증 자체가 운영 LIVE나 실제 Telegram 수신 성공의 증거는 아님. `NOTIFIER_ADAPTER_READONLY`, `NOTIFIER_FAKE_TEST`, `TELEGRAM_LIVE_APPLIED=NOT_RUN`을 각각 기록.

### B4. 최종 결과·별도 판정 게이트
- v0.2.26 독립 리뷰는 **개발 세션 자기시험과 별개**. 새로운 유료 리뷰/REQUEST/SOURCE_PIN/APPROVAL_SIG/READY/서명·디스패치 비용/권한이 확인·승인되지 않았으므로 **지금 생성하거나 실행하지 않음**. 기존 MSC와 v0.2.25 R2의 완료 사이클은 재호출 금지.
- Windows 플랫폼 테스트·Notifier 호출 검증이 모두 PASS여도 **v0.2.26 운영 설치 승인으로 승격 금지**. GPT가 새 후보의 독립 리뷰 필요성/기존 배포 유지·운영 승인 범위를 결과 수신 후 구분 판정.
- 모든 원본 요청·auto_claims·SQLite/비용/서명/READY/완료/UNCERTAIN/레거시 이력 무손실. 유효 리뷰나 잡 실행 불확실 시 재큐잉 0. provider 동시 LIVE 금지. `/AI-CONTINUITY/` 수정 0.

## C. 종료 시 GitHub PRIVATE main에 실제 게시 및 readback

- **결과 문서 경로**: `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/CLAUDE_V026_WINDOWS_PLATFORM_AND_NOTIFIER_RESULT_FOR_GPT_20261118.md`.
- **실행 기록 필수 필드:** `WINDOWS_HOST_ID_REDACTED`, `WINDOWS_PYTHON`, `V025_DEPLOY_STATUS`, `V025_INSTALL_VERSION`, `ACTIVE_PROVIDER`, `PROTECTED_POLICY_EFFECTIVE`, `V025_RESULT_PATH_OR_BLOCKER`, `V026_SOURCE_SHA256`, `V026_SOURCE_BYTES`, `V026_CRC_MEMBERS`, `V026_FULL_SUITE_PASS_FAIL_SKIP`, `BASELINE_34_WINDOWS_NODE_RESULTS`, `NEW_61_REGRESSIONS`, `PRE_SCHEDULE_PIN_REJECT`, `UNCERTAIN_PRESERVED`, `READY_WAIT_SUPPRESSION`, `NOTIFIER_ADAPTER_CALL_SITE`, `NOTIFIER_ADAPTER_READONLY`, `NOTIFIER_FAKE_TEST`, `TELEGRAM_LIVE_APPLIED`, `V026_INSTALL=NOT_RUN`, `V026_INDEPENDENT_REVIEW=NOT_RUN`, `MODEL_CALLS_BY_THIS_TASK=0`, `NEW_REQUEST_READY=0`, `OPEN_BLOCKERS`.
- 실제 시험과 미실행을 `PASS/FAIL/SKIP/NOT_RUN/BLOCKED`로 각각 구분하고, SHA/바이트/commit, 민감정보 제거된 근거 링크 및 다음 한 동작을 포함. 기존 v0.2.25 결과 파일이 실제로 생성됐다면 그것도 같은 Work에서 링크. v0.2.25 미실행 이유와 v0.2.26 결과를 합치지 말 것.
- 기존 `CURRENT.md` **최상단**과 필요한 기존 `TRACKER.json` 현행 필드만 결과에 맞춰 갱신. 새로운 Work/원장/스키마 생성 금지. PR 없이 게시 후 **commit·원격 본문·실제 bytes SHA-256** 재확인. 게시 실패로 모델/시험/Job을 재실행하지 않음.
- 이 인계서 자체는 Windows Claude Code를 기동하지 않는다. 기존 Claude Code 실행 세션에 **이 정확한 상대 경로 한 번만** 전달하면, 최신 입력 조회부터 결과 게시까지 추가 질문 없이 허용 범위 내에서 묶어서 처리한다.
