# GPT → Windows Claude Code: v0.2.29 LIVE 컷오버 승인·실행 원샷

- 2026-11-20 KST / PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`
- **기존 Work:** `collab/projects/COWORK-AUTO-APPROVAL-20261115-001`. 새 Work/리뷰 REQUEST/READY 생성 금지.
- **사용자 최신 명시적 운영 승인:** 대화에서 GPT가 “v0.2.29 LIVE 전환 및 통합 USD3 자동 승인 활성화 조치에 대해 처리 진행할까요?”라고 요청했고, 사용자가 **“그래”**라고 승인. 기존 “백업 번들만” 지시는 앞선 백업 단계에 대한 제한으로 종료했고 **이번 승인으로 전체 컷오버 범위를 허용**한다. 다만 사용자의 채팅/본 MD만으로 로컬 보호 signer·파일 수정 권한이 생기지 않으므로, Windows 호스트가 실제 관리자/보호 자격을 확인해야 한다.
- **실행권한 범위:** 검토된 watcher v0.2.29 고정 ZIP의 Windows LIVE 설치·watcher 작업 정지/재가동·정식 보호된 기존 설정의 `POLICY-STATIC-V1` USD3 비용·자동 위임 `max_request_usd=3`·**새 `enabled_at`** 적용·필요한 백업/원복/보안 권한 검증 및 실행 후 실측·결과 게시. 기존 프로젝트/스킬 allowlist·위임 만료·repo ID·신뢰 루트/기존 키·기존 provider와 다수 정책은 유지. **기존 사용자 명시 승인 범위를 벗어나는 새 키·토큰 생성, 위임 만료 연장, 신규 유료 리뷰·테스트 모델 호출, PUBLIC 게시, 별도 업무 호스트 변경은 제외.**
- **운영자/롤백:** 사용자 = 롤백 최종 책임 및 운영 승인자; Windows Claude Code = 컷오버 실행·검증·필요 시 자동 안전 중지/롤백 수행 담당. 실행 담당자는 실패·정합성 불확실 시 **추가 질문을 기다리지 않고 안전 정지·허용된 기존 상태 복원**을 우선하며, DB 유료 처리 이후에는 스냅샷으로 되돌리지 않는다.
- **개발 라벨 전환 결정:** `development_not_for_deployment`는 기존 개발 후보 문서 표기이며 그 자체로 안전장치가 아님. 이번 사용자의 **정확한 고정 v0.2.29 ZIP SHA**에 대한 조건부 운영 전환 승인을 별도 결재 기록으로 사용한다. 실제 전환 성공 시에만 `HOST_RELEASE_DECISION=APPROVED_AND_APPLIED`를 실제 설치 SHA·시각·기존 버전/설정 SHA/운영 결과와 함께 기록; 미설치/검증 실패는 `APPROVED_BUT_NOT_APPLIED` 또는 `BLOCKED`. ZIP의 과거 문자열 변경 없이 외부 정본에 추적한다.
- **기존 근거:** `LIVE_ENABLE_EXECUTION_REQUEST_V029_20261120_KST.md`; `CLAUDE_V029_USD3_PRELIVE_READINESS_RESULT_FOR_GPT_20261120.md`; `CLAUDE_V029_LIVE_BACKUP_BUNDLE_RESULT_FOR_GPT_20261120.md`; `GPT_V029_REVIEW_ACCEPT_AND_USD3_PRELIVE_STAGING_ONESHOT_r0001_20261120_KST.md`; 독립 리뷰 `REQ-COWORK-V029-ONEOFF-R1-20261120` COMPLETED, GPT ACCEPT_WITH_CONDITIONS. **새 리뷰/재호출 불필요.**

## 1. 고정 설치·백업 입력

- **설치 대상:** `artifacts/v0_2_29/skill-collab-watcher_v0_2_29_1120.zip` (PRIVATE main). **310753 B, SHA-256 `c67bc342fe77547b000fc42e1b886396cbef035c0d265dbcd124947e267ed83f`**. 반드시 실제 다운로드한 bytes/ZIP CRC/경로 검사. 다른 버전으로 대체 금지.
- **교체 전 LIVE:** v0.2.25, 설치 트리 SHA-256 `f691bcf808cbf81e9c2c2a9be65335e527c2df99ea4d54a427665e4c90045c9f`, 설치본 108개 파일(이 중 v0.2.25 패키지 104개 바이트 동일). 현재 설정 SHA `fbce30a97c06f8d04e2e0029c731c41d2ccd87963196afe80279f10cf7509c27`, 위임 SHA `ddead4e497759ac30db9e8d90974cfe4f68114d99ef99cdf85a083e9bf54fd4c`. **Windows 최신 실측에서 값이 달라지면 변경 전 원인·위험을 대조하고 무조건 중지**, 과거 SHA로 덮어쓰기 금지.
- **기존 검증 백업:** `D:\User\whpark\skill-collab-watcher-dist\backup_v0_2_25_install_20261120_200712`, 117 파일, **manifest SHA256 `d23b52068733ec7dcce95024f6f919a0e30147e00b502b3bd449d29406256d92`**, DB snapshot SHA256 `111c85ab30de926759d1caebec78b65a228dd4ab7bfa126c3587ce13dd465fa5`. 호스트가 이 **기존 번들의 위치·bytes·매니페스트/각 파일의 SHA·일관 DB·설치 이전 트리**를 다시 대조. 오래됐거나 다르면 **워처 안전 정지/일관 새 백업**을 승인 범위에서 추가하거나 명확히 BLOCKED. 개인키·암호문을 신규 백업에 복사하거나 원격 게시하지 말 것.
- **주의:** 백업·설치 폴더에 `Authenticated Users:(M)` ACL 상속이 있으므로 매니페스트의 단독 재검사만으로 변조 방지를 단정하지 않는다. 기존에 신뢰 가능한 GitHub 근거의 백업 SHA·운영 실측 트리 SHA와 대조, 필요한 경우 운영자 권한에서 백업 경로 쓰기 권한 최소화·재검증. 범위를 넘는 대규모 ACL/Task 수정 금지; 보안 무결성이 독립적으로 확립되지 않으면 컷오버 중지.
- **고정 보존 경로:** 운영 예약 작업은 **`D:\User\whpark\skill-collab-watcher\.venv\Scripts\pythonw.exe`** 를 참조한다. 구 `D:\User\whpark\skill-collab-watcher` 폴더와 `.venv`는 절대로 이동·삭제·이름 변경하지 말 것. Notifier도 동일 venv를 사용. 기존 Dropbox 시대 작업은 Disabled 유지.

## 2. Windows Claude Code 실운영 컷오버 — 승인된 단일 작업

**최신 원본을 재조회한 뒤 이 실행서 §1~4와 기존 `LIVE_ENABLE_EXECUTION_REQUEST_V029_20261120_KST.md` §2~5를 충족하면서 한 번만 실행.**

1. **HOST_PREFLIGHT:** 현재 PRIVATE main/CURRENT 최신 여부, 동일 작업 완료/진행 중 결과·Task·remote receipt 확인하여 중복 컷오버 방지. 운영자 승인 범위(상기 사용자 명시 승인), 실제 Windows 관리자/보호 파일 수정·정식 서명/로더 권한, Watcher/Notifier task 권한, 단일 provider, 위임 scope·expires_at, ZIP/설치/백업 bytes·SHA/ACL·DB 일관성 확인. 시작 당시 실행 중 job·리뷰·in-flight **0**, 이전 완료/Guard UNCERTAIN 보존. 설치본/백업/신뢰된 권한 하나라도 다르면 **중단**하고 근거 보고; 승인 문서를 보호 서명 자격으로 대신하지 않음.
2. **LEGACY_GATE:** `classify_legacy.py`를 재실행해 실제 LIVE의 STATIC·이력 없음·활성 중 관측 요청 0 여부, Guard 1건 UNCERTAIN·기존 DESIGN/LARGE 구 ID·completed/seen/claim 일치 확인. 마지막 GitHub REQUEST 게시 최초 시각과 signer/정식 policy 로직 대조. 이전 요청 자동 재서명/READY/모델 재호출 0이 보장되지 않으면 중단.
3. **STOP_AND_BACKUP:** GitHub watcher task **한 개만** 중지, in-flight 0 재확인. Notifier와 장애 복구에 필요한 `.venv`/다른 LIVE provider/keys/작업을 무단 변경하지 않음. 설치 트리·설정·보호 위임·권한·작업 XML과 **online backup API**의 DB 일관 스냅샷을 안전하게 보존, 기존 117 파일 백업 readback·독립 근거 대조 및 필요시 컷오버 시점 추가 새 백업. 직접 main/WAL/SHM을 각각 비일관 복사해 복구본으로 간주하지 않음.
4. **INSTALL_AND_ATOMIC_ALIGNMENT:** 고정 ZIP v0.2.29 코드/문서/도구만 운영 트리에 설치하고 `config/reviewer.config.json`·`package/`·신뢰루트/키/DB는 패키지 덮어쓰기로 대체 금지. Watcher 정지·권한 확보 상태에서 기존 `POLICY-STATIC-V1`의 등록 단가 **USD3**, `max_request_usd=3`와 **신규 `enabled_at`를 한 번의 정합된 변경 구간**에 적용하여 watcher가 중간 불일치 설정을 보지 않게 함. `enabled_at`은 **실제 변경 시각 KST**로 기록하고 이전 2026-11-16T19:47:50+09:00보다 늦고 `expires_at=2026-12-16T19:47:50+09:00`보다 빠르게, **모든 기존 원격 REQUEST 최초 commit보다 후**로 설정. DESIGN/LARGE 정책은 역사적 참조로 유지하되 신규 자동 서명에서 제외. 자동 위임의 기존 범위·만료를 상향/연장/확대하지 않음. 보호된 승인/쓰기 권한·ACL을 정식 방식으로 확인할 수 없으면 설정 파일을 임의 JSON 수정하거나 우회하지 말고 BLOCKED.
5. **PRESTART_VERIFY (유료 0):** 실제 v0.2.29 버전·트리 실제 해시/원본 패키지 CRC·config/위임 동시 load/보호 ACL·repo_id 문자열·USD3 `review_request_gate select/check --intent unified` PASS, 실제 DB **읽기 전용** 레거시 분류·중복·소급 신규 `enabled_at` 검증. 임시 분리된 DB/가짜 signer/model transport로 재현 SHADOW하고 **구 ID의 새 서명/READY/모델 0** 입증. 승인 키·비밀값 외부 업로드 금지. 불일치 즉시 watcher가 정지된 상태에서 허용된 안전 롤백.
6. **LIVE_RESTART_AND_OBSERVE:** 안전 게이트 모두 PASS할 때만 watcher task 재가동. **최소 2 주기 + 1회 재시작**을 실제 호스트에서 관찰. 단일 github provider lease, 실제 LIVE watcher v0.2.29/정책 STATIC USD3/보호 위임 USD3/new enabled_at, 기존 구 요청 서명/READY/모델 호출 0, 미확실·완료 건 중복 0, log/Task/Notifier 정상 여부 증거 수집. 새 모델 호출/신규 유료 테스트·새 정식 REQUEST/READY를 만들지 않음. 새 유효한 외부 REQUEST가 실제 도착하지 않았다면 **`NEW_LIVE_PAID_E2E=NOT_RUN`**이라고 표기.
7. **FAIL_CLOSED_ROLLBACK:** task 오류·SHA/ACL·정책 load 불일치·구 요청 적격/서명 발생·duplicate provider·비밀 노출·DB 손상 등 하나라도 발생하면 즉시 watcher 정지, 이전 검증 백업을 통해 트리·설정·보호 위임을 **실제 바이트 대조하며** 안전 복구. **실제 유료 job이 컷오버 이후 발생했다면 DB 스냅샷으로 되돌리지 말고** 현 원시 DB/영수증/UNCERTAIN을 보존. 권한 부족 또는 원본 불변성 미확인 시 임의 재시작/부분 전환 금지, `BLOCKED`/중단 상태를 그대로 보고. 롤백한 경우 v0.2.25/USD1 재로딩과 lease/작업 정상 여부를 실측한 경우에만 `ROLLBACK=PASS`, 아니면 PARTIAL/FAILED.

## 3. 단일 결과 게시 · 상태 판정

- **실제 Windows 수행 결과는 한 파일** `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/CLAUDE_V029_LIVE_CUTOVER_RESULT_FOR_GPT_20261120.md`로 기록 (기존 파일이 이미 있으면 판정/영수증 확인 후 중복 실행 금지). `CURRENT.md` 최상단 현재 요약 + 기존 `TRACKER.json` 현행 필드만 같이 갱신. PRIVATE `main`으로 PR 없이 승인된 비민감 결과를 게시하고 원격 actual bytes SHA/commit readback.
- 필수 필드: `OPERATING_APPROVAL=USER_CONFIRMED_20261120`, `HOST_OPERATOR_AUTH=PASS/BLOCKED`, `PRECHECK`, `BACKUP_SHA/ACL`, `LEGACY_CLASSIFICATION`, `INSTALL_ZIP_SHA`, `PREV_LIVE_SHA`, `WINDOWS_TASK_STATUS`, `STATIC_POLICY_USD3`, `AUTO_DELEGATION_USD3`, `ENABLED_AT_NEW`, `SIGNER_SCOPE_EXPIRY`, `HOST_LOAD/PRESTART_CHECK`, `TWO_CYCLES_RESTART`, `OLD_REQUEST_SIGN_READY_MODEL_ZERO`, `PROVIDER_SINGLE`, `ROLLBACK_REQUIRED/RESULT`, `LIVE_VERSION`, `LIVE_ENABLE=PASS|FAIL|BLOCKED|NOT_RUN`, `LIVE_PAID_E2E=PASS|NOT_RUN`, `MODEL_CALLS_NEW`, `COST_NEW`, `SECURITY_RACE_SU_L1=OFF/UNRESOLVED`, `DEVELOPMENT_LABEL_RELEASE_DECISION`, 실제 설치 시간·운영자/실행 주체·대상 번들 경로·SHA.
- 문서·구 REQUEST/READY/receipt 수정/재실행 금지. 신규 유료 리뷰/재리뷰·유료 smoke 및 GitHub PUBLIC 업로드 0. 참고: 기존 LIVE watcher는 새 정상 업무 요청이 추후 도착할 경우 **승인된 USD3 범위**에서만 자동 실행할 수 있으며 그 정상 실행을 무단 차단하는 기능을 추가하지 않음.
- 성공은 **실제 호스트 v0.2.29 + 등록 STATIC USD3 + 보호 위임 USD3 + 신규 enabled_at + 기존 구 요청 추가 실행 0 + 2주기/재시작 PASS + rollback 준비/바이트 증빙**으로만. Docs/격리시험/REQUEST 게시가 LIVE PASS가 아님.
- 최종 보고 순서: **현재 상태 → 변경 내용 → 실제 시험 → 미검증/차단·필요 승인 → 결과 링크/설치 ZIP SHA → 다음 한 행동**. 실패하면 USER_ACTION에 정확한 차단 사유 하나만 보고; 재실행·반복 승인 요구 금지.

## 4. 전송·실행 계약의 한계

- 본 파일은 **GPT가 승인 범위를 Windows Claude Code에 인계하는 실행 지시**. PRIVATE MD 게시 자체가 watcher의 자동 실행 트리거, Windows Claude Code 실행, 로컬 보호 파일 서명, Task API 호출은 아니다.
- **실제 Windows 수행자가 본 파일을 읽고 실행해야 한다.** ChatGPT의 GitHub 게시만으로 완료를 주장하지 말 것. 비밀정보·보호 신뢰루트·DB snapshot·개인키를 GitHub PRIVATE/PUBLIC에 업로드 금지.
