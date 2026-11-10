# Windows 로그온 없는 시작 방식 — 격리 호환성 점검 인계 r0001
날짜: 2026-11-11 KST | work_id: COWORK-DROPBOX-TO-GITHUB-MIGRATION
상태: PREPARED_NOT_EXECUTED / READ_ONLY_AND_ISOLATED_TEST_ONLY

## 0. 목표와 현재 사실
- 사용자 선택: Windows 자동 로그인은 권장하지 않음. '시스템 시작 시' 트리거와 '사용자 로그온 여부와 관계없이 실행' 방식의 기술적 호환성을 먼저 검토.
- 사용자 금지: **실제 운영 설정은 변경하지 말 것**. 이 문서는 설치·실행·운영 전환·리뷰 승인 신호가 아님.
- 현재 Dropbox LIVE watcher v0.1.5는 사용자 로그온 트리거/대화형 제한 계정, 5분 간격 최대 3회 재시작, 중복 실행 무시.
- GitHub 후보 v0.2.5는 개발용으로만 로컬 보관; 448 PASS/0 FAIL/12 SKIP은 개발자 자체 시험. INDEPENDENT_REVIEW=NOT_RUN.
- 기준: PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`, `collab/START_HERE.md`, `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md`, `CLAUDE_UNATTENDED_REVIEW_READINESS_RESULT_FOR_GPT_20261111.md`.

## 1. Windows Claude Code에 허용한 일회성 조사 범위
1) READ_ONLY: 현재 Task Scheduler의 트리거, LogonType(Interactive/Password/S4U/ServiceAccount), RunLevel, user context, working directory, 실행 인스턴스 정책, 재시작·전원·네트워크 조건을 **비밀·사용자명·로컬 경로 없이 요약**. 기존 작업의 등록/수정/삭제/실행/중지 금지.
2) READ_ONLY: 비대화형 컨텍스트와 Claude Code 인증의 의존성 조사. `claude auth status`는 현재 사용자 세션에서 단 한 번의 모델 미호출 조회만 허용. 인증 토큰/환경변수 값, 로그, 프로필 내부 secret, Credential Manager, LSA, DPAPI 내부값을 읽거나 반출하지 말 것.
3) 격리 복사본(운영 자료가 아닌 비민감 synthetic fixture)에서만 Task Scheduler XML 구조/트리거·계정 컨텍스트 조건을 **정적 또는 모의시험**. 이 단계에서 Windows 작업을 새로 등록하는 것도 금지. Windows 부팅/로그오프/자동로그인 변경 금지.
4) 세 방식 비교: (A) 현재 로그온 시 실행, (B) 부팅 트리거 + 로그온 여부 무관 계정(일반 암호 저장), (C) S4U 암호 미저장. 실제 네트워크/보호된 사용자 자격 증명 접근에서 S4U의 제약, GUI/세션0 비대화형 특성, `USERPROFILE`/HOME/작업 디렉터리 및 CLI 인증 연결을 점검.
5) '로그온 없이 실제 성공'은 이 범위에서 **NOT_RUN**으로 보고할 것. 정적 호환성 추정이나 현재 대화형 로그인 확인을 실제 부팅 호스트 E2E PASS로 표현 금지.
6) 실제 오류(구독 상한 등)를 보기 위한 Claude 모델 호출, 유료 리뷰 호출, 임의 재시도, GitHub REQUEST/READY 게시, Telegram 전송, 예약 작업 신규 등록 금지.

## 2. 검증 체크리스트와 완료 기준
- R01 READ_ONLY: 현 트리거가 로그온 기반이며 boot 트리거가 없음을 기존 조회와 대조. `PASS/FAIL/NOT_RUN`.
- R02 READ_ONLY: 권한 상승 없이 비대화형 Task principal과 사용자 프로필/인증 의존성을 표로 도출. `PASS/PARTIAL/NOT_RUN`.
- R03 STATIC: 네트워크·기밀정보 사용 없는 합성 XML/런처 시험으로 입력 설정·실패 경로를 재현. `PASS/FAIL/NOT_RUN`.
- R04 SECURITY: 자동 로그인 비권장 사유, 일반 암호 저장 방식의 권한·물리 접근 위험, S4U 제약, 최소 권한·자격증명 보관 방식 분석.
- R05 SAFETY: 운영 watcher 프로세스/DB(SQLite main/WAL/SHM)/예약 작업/Bridge/Dashboard/Telegram/설정에 쓰기·설치·재시작 0, GitHub 원격 쓰기(결과 MD 제외) 0, 모델 호출 0을 관측 근거로 보고.
- R06 READINESS: 실제 로그온 없는 부팅 E2E를 안전하게 하려면 필요한 별도 사용자 승인, 롤백, 단일 LIVE/단일 실행 게이트를 명확히 제시. 실제 호스트 시험은 `NOT_RUN`으로 남길 것.
- 기존 v0.2.5 후보 ZIP·기존 문서 변경 금지. 새 버전 ZIP도 이 조사에서 요구하지 않음.

## 3. 출력·게시 규칙
- 산출물: `CLAUDE_NO_LOGON_START_COMPAT_RESULT_FOR_GPT_20261111.md` **신규 파일**, PRIVATE `main`의 동일 이관 프로젝트 폴더에 PR 없이 직접 게시. 로컬·원격 원문 readback과 커밋 SHA 확인.
- 보고: `COMPAT_STATUS: PASS_STATIC|PARTIAL|BLOCKED`, R01–R06 각 시험과 증거 종류(`REAL_READ_ONLY / SYNTHETIC / NOT_RUN`), `REAL_LOGONLESS_BOOT_E2E=NOT_RUN`, `PRODUCTION_CHANGED=false`, `MODEL_CALLS=0`, 차단 항목 및 다음 승인 하나.
- 파일 게시 전 내부 경로, 로그인 ID, 인증정보, 실제 기업 코드/로그/고객자료를 제거. 사외 반출 적합성 불명확하면 게시하지 않고 `REDACTION_REQUIRED / NOT_POSTED`만 보고.
- 출력이 준비될 때까지 `CURRENT.md`의 개발/배포/독립 리뷰 상태를 PASS로 격상하지 말 것.

## 4. 금지·중단
- Windows 자동 로그인 설정, Task Scheduler 운영 작업 등록·수정·삭제·실행·중지, 실제 재부팅/로그오프, 계정 암호 저장, Claude 인증 변경, 새 PAT/운영 신뢰키·서명, live DB/작업/알림 변경 **모두 금지**.
- 운영 Dropbox LIVE와 GitHub 전환 상태는 `MIGRATION_NOT_CUTOVER` 유지. 감시기 후보 설치·재시작, GitHub SHADOW 설치/모델 호출/READY, PUBLIC 배포/LIVE 전환 모두 금지.
- read-only 확인에 비밀이 노출될 위험 또는 쓰기 필요가 생기면 해당 항목 `BLOCKED`; 가능한 다른 정적 점검은 계속.

## 5. Windows Claude Code에 전달할 한 줄
`wonhwipark/CoWork-Skill-Collab`의 `main` 브랜치 `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/WINDOWS_NO_LOGON_START_COMPAT_HANDOFF_r0001_20261111.md`를 읽고 운영 변경 없이 R01–R06 읽기전용·격리 호환성만 원샷 검토해. 결과 MD는 비민감 내용만 PRIVATE main에 직접 게시하고 원격 재조회해. 실제 스케줄 등록·재부팅·로그온 없는 E2E·모델 호출·READY는 실행하지 마.
