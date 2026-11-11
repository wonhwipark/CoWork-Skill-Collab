# CoWork GitHub 전환 — 1차 준비작업 승인 기록 r0001

날짜: 2026-11-11 KST
저장소: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab` / `main`
work_id: `COWORK-DROPBOX-TO-GITHUB-MIGRATION`
기준 판정: `GPT_V0_2_8_FINAL_PRE_CUTOVER_DISPOSITION_r0001_20261111.md`

## 승인 근거·범위
GPT가 LIVE를 제외한 **1차 승인 묶음 다섯 항목**(비관리자 실행 계정/ACL, 승인자 기기 키·trust root, 호스트 읽기전용 SHADOW, 분류된 소스 ZIP PRIVATE 게시, STATIC $1 한도 독립 리뷰 1회)을 구체적으로 제시한 직후 사용자가 `그래진행해줘`로 진행을 지시함.

판정: **`STAGE1_AUTHORIZED_WITH_GATES`**. 요청 범위 안에서 Windows Claude Code를 통한 승인된 일회성 준비·설치·시험을 허용하되, 다음 기술·보안 선행 조건을 우회하거나 LIVE 전환까지 승인한 것은 아님. **이 문서는 reviewer의 암호학적 APPROVAL_SIG, 모델 호출 명령, REQUEST/READY 또는 host 실행 트리거가 아님.**

### 1차 승인된 작업 — 조건부 실행
1. **분리 계정/ACL:** 테스트용 로컬 비관리자 watcher 계정과 관리자만 쓰는 신뢰 루트/핀/설정 폴더를 마련하고 Windows 유효 권한(그룹·상속·소유자·재시작 후 권한 포함)을 확인. 기존 운영 Dropbox watcher v0.1.5 계정/스케줄러/DB/Bridge/Dashboard/Telegram은 변경 금지. 새 계정에 불필요한 관리자·네트워크 쓰기 권한 금지.
2. **승인자 키:** 실제 개인키는 **사용자/승인자가 소유·제어하는 별도 장치**에만 생성·보관; Windows 감시기 실행 호스트나 GitHub에 개인키를 복사/출력/저장하지 않는다. 승인자 장치와 실행 호스트가 분리 불가능하거나 권한이 불명확하면 `BLOCKED_SIGNER_DEVICE`. 공개키 trust root·pin만 최소권한으로 호스트에 설치, 실제 S-2 fail-closed 검사 통과 요구. 사용자의 승인 응답 자체를 암호 서명으로 사용하지 말 것.
3. **호스트 SHADOW:** v0.2.8 후보 무결성 확인 후 운영과 다른 격리 폴더·별도 상태DB·GitHub contents-read-only 최소 권한 토큰으로 *일회성, 유한한 3주기 이상* 기동. 모델/Telegram/원격 GitHub 쓰기/Dropbox 쓰기/운영 DB main-WAL-SHM 접근=0. 실제 프로세스 파일 I/O 추적과 기존 LIVE 무영향 확인. 시험 후 SHADOW 종료 및 사용된 권한 처리 상태 보고. 다른 ACTIVE_PROVIDER 활성화 금지.
4. **소스 반출/PRIVATE 업로드:** 공개/사외 반출금지 아닌 파일로만 ZIP을 구성하며, 70개 파일 **각각 출처·소유권·반출 정책**을 점검. 검사 통과만으로 회사의 반출 허가를 만들어낼 수 없음. 불확실하면 `BLOCKED_EXPORT_CLASSIFICATION`; **사용자 추가 확인이 필요한 파일은 로컬 보존·업로드 금지**. 허용 확인된 ZIP만 `collab/packages/` 새 이름으로 PRIVATE 게시 후 원격 raw bytes SHA256 readback. 이 동의는 모든 소스 코드에 대한 무조건적 반출 권한이 아님.
5. **정식 독립 리뷰 1회:** 위 게이트와 암호 서명·고정 커밋·신뢰 루트·계정·예산·중복키·policy를 만족하면 `STATIC <= USD 1.00` 상한 **딱 1회** 유효 리뷰 실행을 승인. 모델 호출 이전 예산 산정이 상한 초과/불명확하거나 실행 경로가 자체 구현 세션과 분리되지 않으면 `BLOCKED_REVIEW`, 모델 호출 0. 같은 모델 실행 재시도·재리뷰/예산 증액은 신규 사용자 승인 필요. 결과·영수증 원격 readback 전 COMPLETED 금지.

### 이 단계에 포함되지 않는 항목
- 운영 Dropbox LIVE 중단·교체·스케줄러 수정, 운영 DB/SQLite WAL/SHM 이행·수정·백업 실생성, F1의 실제 HOLD/재큐잉/폐기.
- GitHub LIVE 단일 provider 전환 또는 롤백 실작업, PUBLIC `L1Work` 게시.
- Windows 자동 로그인, 로그온 없는 시작(S4U 또는 저장암호) 적용, 지속 자동감시 활성화, Telegram notifier 신기능 적용.
- API 비용 상한의 자동 증액, 추가 독립 리뷰, 비승인 사용자/회사 비밀 반출, `/AI-CONTINUITY/` 변경.

## 실행 전 안전 조건
- 운영 상태: `MIGRATION_NOT_CUTOVER` / `ACTIVE_PROVIDER=DROPBOX_LIVE`, v0.1.5 불변.
- 기준 소스: Windows 로컬 `skill-collab-watcher_v0_2_8_1111.zip` (Claude 보고 **173615 bytes** / SHA256 `c6231cc329faff26c6e04a0ca454dec0d62a5eaaa0eb08edf9b6a57280f78daa`). 실제 바이트 체크 실패 시 다른 버전으로 묵시 대체 금지.
- 사용자 이름·로컬 절대 경로·토큰·개인키·회사 운영 데이터·내부 로그는 결과 MD에 남기지 않는다.
- 운영 기능에 위험 신호가 보이면 해당 시험을 안전 중단하고 롤백, 다른 허용 업무는 계속. SHADOW 종료·후처리는 LIVE와 별개로만.
- 기존 개발자 자체 시험은 `SELF_TEST_REPORTED`; **별도 독립 리뷰 영수증 없는 `INDEPENDENT_REVIEW=PASS` 불가**.

## 승인 기록과 실행 여부 구분
- `APPROVAL=STAGE1_AUTHORIZED_WITH_GATES`
- `WINDOWS_STAGE1_EXECUTION=NOT_RUN` (이 GitHub 기록 시점, 실행 관측 없음)
- `INDEPENDENT_REVIEW=NOT_RUN`
- `CUTOVER=MIGRATION_NOT_CUTOVER`
- 후속 실측·차단·리뷰·게시의 참조 문서는 별도 원샷 실행 인계 및 Windows 결과 보고를 따름.
