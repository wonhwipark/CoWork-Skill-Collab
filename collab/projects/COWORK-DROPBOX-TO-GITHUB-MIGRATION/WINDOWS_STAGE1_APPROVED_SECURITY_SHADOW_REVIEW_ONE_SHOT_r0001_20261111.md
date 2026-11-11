# Windows Claude Code 원샷 — Stage 1 보안분리·호스트 SHADOW·제한 독립 리뷰 r0001
일자: 2026-11-11 KST
저장소: **GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`**
브랜치: **`main`**
상대 경로: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/WINDOWS_STAGE1_APPROVED_SECURITY_SHADOW_REVIEW_ONE_SHOT_r0001_20261111.md`
작업 ID: `COWORK-DROPBOX-TO-GITHUB-MIGRATION`

**사용자 명시 1차 승인 확인:** `USER_STAGE1_APPROVAL_RECORD_r0001_20261111.md` (commit `24337b8effef0b154790a0843d281bba502dbb72`)를 실제 readback. `STAGE1_AUTHORIZED_WITH_GATES`. **LIVE 전환·운영 DB 이행·F1 처분은 승인 범위 밖.**

## 0. 원샷 시작 규칙
1. 시작 직전에 `collab/START_HERE.md`, 최신 `CURRENT.md`, `USER_STAGE1_APPROVAL_RECORD_r0001_20261111.md`, `GPT_V0_2_8_FINAL_PRE_CUTOVER_DISPOSITION_r0001_20261111.md`, `CLAUDE_CUTOVER_ESSENTIAL_GATES_RESULT_FOR_GPT_20261111.md`, `REVIEW_INPUT_MANIFEST_v0_2_8_FOR_GPT_20261111.md`, `NO_PR_COLLABORATION_V1.md`, `REVIEW_TRANSPORT_V1.md`를 읽는다. 앞선 승인 파일 존재만으로 암호학적 reviewer 승인 서명을 생략하지 않는다.
2. 운영 baseline `Dropbox watcher v0.1.5`·4개 Windows 예약 작업·Bridge/Updater/Notifier·Telegram·운영 DB(main/WAL/SHM)/F1·운영 트리거는 모두 보존. GitHub 신규 LIVE를 절대 활성화하지 않는다. 기존 1개 ACTIVE_PROVIDER=Dropbox.
3. 작업 시작 전 Windows 실제 후보 `skill-collab-watcher_v0_2_8_1111.zip`, **173615 bytes**, SHA256 `c6231cc329faff26c6e04a0ca454dec0d62a5eaaa0eb08edf9b6a57280f78daa` 대조. 버전/해시가 다르면 **fail-closed**. 오래된 v0.2.4~v0.2.7을 묵시 대체하지 않음.
4. 최신 결과가 다른 세션에 있다면 중복 계정/키/토큰 생성·모델 리뷰 호출·운영 변경 금지, 그 항목은 결과 확인으로 갈음.
5. 권한이 필요한 범위와 실제 허용된 범위를 기록하고, 막힌 항목은 `BLOCKED/NOT_RUN` 처리한 뒤 다음 가능한 단계 진행. 사용자에게 단계마다 핑퐁하지 말고 **최종 결과에 차단·남은 승인 묶음 제시**. 단, 비밀 생성·운영 영향 작업을 위해 타인의 자격을 추측·우회 금지.

## 1. 실행 순서 (A → E, 중간 게이트 모두 fail-closed)

### A. 분리된 비관리자 watcher 실행 계정·ACL
- 호스트 운영 설정과 분리된 **시험용 비관리자 로컬 계정**을 준비. 기존 LIVE 작업 계정 변경·업그레이드·중지 금지. 새 계정은 Local Administrators, 원격 관리 권한, 기존 운영 상태DB/credential/token 폴더의 쓰기 권한을 갖지 않게 한다.
- 관리자만 수정 가능한 별도 trust root·pin·config 폴더를 준비. 시험 계정의 실제 SID·그룹 유효 ACL(폴더/파일/상위 상속/owner/rename/delete 포함)을 확인. 비관리자 계정은 trusted root/pin/config를 읽을 수만 있고 변경은 못해야 한다. 암호/자격 정보를 GitHub 문서나 출력에 노출 금지.
- 계정 생성·권한 경계는 **시험 폴더/계정에 한정**. 운영 watcher v0.1.5·Windows 예약 작업 4개·운영 설정의 소유자/ACL 변경은 금지.
- 관리자 전용 폴더를 만들 수 없거나 사용자 동의가 운영 host 정책상 적용 불가하면 `BLOCKED_ACL`, 임의로 약한 보호 구성으로 우회하지 않음.

### B. 별도 승인자 기기 키·고정 trust root
- `tools/approval_signer.py`의 `keygen/sign/check`·`tools/trust_root_tool.py`를 실제 ZIP 원본 기준으로 재조회·도구 버전 시험. 사용자의 **별도 승인자 장치**에서만 운영 목적 개인키 생성(사용자/승인자가 직접 승인·인증). **watcher 실행 호스트가 승인자 장치로도 사용된다면 사전의 '분리' 충족 불가 → `BLOCKED_SIGNER_DEVICE`**, 시험 키 대체로 실운영 PASS 선언 금지.
- 개인키/시드·서명 인증 정보는 GitHub PRIVATE, Telegram, 결과 MD, 실행 호스트에 올리거나 복사하지 않는다. 실제 root **공개키**·pin 및 해시만 host 관리자 통제 영역에 설치하고 ACL 검사로 `BLOCKED_TRUST` 해소 실측.
- 승인의 문장 텍스트를 그대로 서명 재료로 신뢰하지 않는다. signer는 요청 ID·ZIP SHA·Git 고정 커밋·policy/cost/nonce/expiry를 계약대로 서명해야 한다.
- 별도 장치 접근, 인증 또는 키 보관 정책이 충족되지 않으면 실키 설치/서명은 `NOT_RUN`, test key로 가능한 독립 보안시험만 반복.

### C. 실제 호스트 read-only SHADOW (1차 승인 범위)
- 샌드박스 폴더에 후보를 분리 설치. 이 시험은 기존 운영 watcher를 교체하지 않는다. GitHub는 이 저장소 한정 **contents-read-only 최소 권한** 자격만 사용; Windows 자격 생성이 필요하면 사용자 인증으로만 생성·설정. 토큰을 출력/커밋/로그/원격 전달하지 말 것.
- SHADOW 전용 `shadow.state_dir`/DB/locks/log/cursor, SHADOW read-only GitHub transport, `ShadowRunner`, `provider_mode=SHADOW`의 실패 시 중단 확인. 호스트의 운영 `state_dir`, 운영 DB main/WAL/SHM, 기존 LIVE mutex·cursor·lease는 SHADOW가 직접 열지 않고 경로상·I/O상 분리.
- 권한이 마련됐을 경우 샌드박스에서 **실제 3개 이상 watch 주기만** 수행; 유한 시간 후 중단·시험용 SHADOW 만 정리. GitHub GET only, 모델 호출·비용 0, 외부 GitHub/Dropbox write 0, Telegram 발송 0, 운영 DB 관련 file open/read/write/lock 0을 **실 프로세스 파일 I/O 계측**과 파일 identity로 확인. 기존 운영 watcher 및 예약 작업 상태 전후 비교.
- Windows Process Monitor/ETW 등이 설치나 UAC를 요구하면 기존 운영 설정에 영향을 주지 않는 범위인지 확인. 자격·권한·계측 실패 시 `HOST_SHADOW=PARTIAL/NOT_RUN` 유지. 스냅샷 합성 tripwire만으로 PASS 판정 금지.
- 새 호스트 SHADOW task를 부팅/로그온 예약 작업으로 등록하지 말 것. **수동·격리 일회성**만. 종료 후 계정/토큰/테스트 폴더를 무조건 삭제하지 말고 회수·보존 계획과 현재 상태만 보고.

### D. 소스 ZIP 실제 반출 분류 및 PRIVATE 게시
- ZIP 70개 항목마다 **파일별 출처·회사 소유/사외 반출 정책·비밀/PII 포함 여부**를 확인. 자동 secret scan PASS는 법적/사내 반출 허가가 아니다. 사용자 메시지는 검사 **진행 승인**이지 금지 자료의 무조건적 반출 허가는 아니다.
- 명백하게 허용되는 외부 독립 원본만 PRIVATE 게시. 기업 코드·운영 로그·DB·토큰·키·반출 불명 소스가 1건이라도 있으면 ZIP 통째로 `BLOCKED_EXPORT_CLASSIFICATION`, 운영 로컬 보존. 허용된 부분만 별도로 게시 가능하지만 원본 ZIP과 동일한 ZIP이라고 해시를 속이지 않는다.
- **반출 권한이 실제로 확인된 173615B ZIP만** 신규 파일명 `collab/packages/skill-collab-watcher_v0_2_8_1111.zip` (존재 확인 후 덮어쓰기 금지) 게시, raw byte SHA256/size/commit/pin readback. PRIVATE 저장소라도 외부 보관소다. 허용 여부 확인이 안되면 업로드 금지.

### E. 정식 독립 리뷰 1회 — 상한 **STATIC $1**
- 모델 호출 수행 전 검증: 실제 공개 trust root·정상 signer에서 서명된 유효 REQUEST/READY, ZIP 실제 SHA·고정 commit pin, 승인 ID·revision·processing key, 정책·만료·nonce, 리뷰 예산 추정 `<= USD 1.00`, 독립 reviewer **개발과 분리된 명시 세션/실행 기록**, 동일 logical request 선행 디스패치 없음.
- GitHub SHADOW watcher는 **모델 호출 금지**. 리뷰를 위해 SHADOW를 LIVE처럼 바꾸지 않는다. 별도의 정식 승인된 리뷰 실행 경로가 존재하지 않으면 `INDEPENDENT_REVIEW=NOT_RUN/BLOCKED_TRANSPORT`; 임의 `claude -p` 또는 같은 개발 세션의 self-review를 `INDEPENDENT_REVIEW=PASS`로 바꾸지 말 것.
- **STATIC $1은 호출당 최대 한도이자 이번 1회 승인 상한**. 예상 비용이 초과/알 수 없거나 scope가 너무 넓으면 `COST_APPROVAL_REQUIRED`, 무호출. 비용 자동 증액·리뷰 재호출·같은 요청 재큐잉 금지.
- 서명된 READY는 실제 실행 가능한 승인 신호이므로 **모든 보호 게이트가 작동하는 승인된 reviewer 경로가 존재함을 확인한 마지막 단계에서만**. 불확실하면 서명 이전 REVIEW_PREP 수준 보존.
- 실행 가능하고 1회 리뷰를 수행했다면 별도의 reviewer 원문과 RECEIPT를 생성·PRIVATE `collab/reviews/` 및 `collab/receipts/`에 원격 게시, hash·readback 확인 후에만 `INDEPENDENT_REVIEW=PASS` (리뷰가 PASS 판정일 때만); 지적사항은 사실대로 보고. 실패나 불확실은 `REVIEW_UNCERTAIN`, 추가 리뷰 호출 0.

## 2. 자체시험 보강(중간 차단과 무관하게 실행)
- 새 계정/ACL 또는 SHADOW 결과를 바꾸는 수정이 있다면 소스 ZIP 원본은 보존하고 신규 버전 패키지에만 반영, 새 SHA·크기·시험 결과를 보고.
- 2026-11-11 GPT 지적: `pytest` venv **522+12=534 수집** vs 운영 인터프리터 **487+14=501 수집**의 **33개 차이**. `pytest --collect-only`, import/skip/collection 단계 근거로 설명. 수집되지 않은 시험을 SKIP으로 보고하지 말 것. 시험을 새로 추가/삭제한 탓인지 가상환경에 의존하는 파일인지 분리.
- S-1/S-2 반례, 운영 DB main/WAL/SHM I/O0, 패키징 ZIP deterministic timestamp, 런북·코드 문구 일치 회귀 유지. mutation/coverage는 실행 가능할 때만, 미실행이라면 NOT_RUN.

## 3. 리포트·검증
**결과 파일(기존 결과 덮어쓰지 않고 신규):**
`collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CLAUDE_STAGE1_APPROVED_HOST_SECURITY_RESULT_FOR_GPT_20261111.md`

- A~E별 `PASS/FAIL/PARTIAL/BLOCKED/NOT_RUN` + 증거 종류(`HOST_REAL/SYNTHETIC/SELF_TEST_REPORTED`)와 정확한 실행 범위.
- 계정 존재 여부, ACL 구분 테스트/실패 이유, 개인키 분리 여부(키 자체 미공개), SHADOW cycles·GitHub GET/write·모델/Telegram 호출수, 실제 I/O 증거, DB main/WAL/SHM 운영 영향, ZIP 실 바이트·원격 pin, REQUEST/READY·reviewer 별도 session·receipt, 비용, F1 상태, 후속 LIVE 승인 차단.
- 비밀/사내 반출금지 자료는 PRIVATE **결과 MD에도 기록하지 않음**. 로컬 자격/사용자명/절대 경로는 요약으로 치환.
- 허용된 결과 MD만 `main`에 **PR 없이 직접 게시**. GitHub commit SHA와 remote readback 실제 확인. 새 `CURRENT.md`의 **맨 앞 한 단락**에 `STAGE1_APPROVED_HOST_RESULT` 상태와 근거를 추가(기존 이력 보존).
- `DEVELOPMENT=SELF_TEST_REPORTED`, `INDEPENDENT_REVIEW=NOT_RUN`은 정식 별도 review receipt가 없으면 유지. 일부 실패로 다른 단계의 자체 시험을 중단하지 말 것.
- **최종 운영 상태는 Dropbox LIVE 유지 / GitHub CUTOVER=NOT_RUN**. 후속 2차 실제 DB 이행·F1 처분·GitHub LIVE는 별도 사용자 승인.
- 결과 MD 업로드 실패 시 `NOT_POSTED`, 원격 readback 실패는 `UNVERIFIED`; 임의 자동 반복 리뷰 호출 금지.

## 4. Windows Claude Code에 전달할 한 줄
GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`의 `main` 브랜치 `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/WINDOWS_STAGE1_APPROVED_SECURITY_SHADOW_REVIEW_ONE_SHOT_r0001_20261111.md`와 `USER_STAGE1_APPROVAL_RECORD_r0001_20261111.md`를 읽고, 사용자 승인된 Stage 1 A~E를 순서대로 원샷 수행해줘. 기존 Dropbox LIVE와 DB/작업/알림은 변경하지 말고, 권한·별도 서명자 기기·반출 분류·정식 리뷰 경로·STATIC $1 게이트는 우회하지 마. 중간 막힘은 BLOCKED로 남기고 허용된 작업을 계속한 뒤 신규 결과 MD를 PRIVATE main에 직접 게시하고 원격 readback까지 확인해줘. 운영 이행이나 GitHub LIVE 전환은 절대 실행하지 마.
