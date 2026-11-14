# CoWork → Windows Claude Code 원샷: Classic PAT 실제 GitHub 쓰기·게시 E2E + LIVE 준비 게이트

- 2026-11-14 KST · r0001
- **정확한 저장소:** GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`
- **정확한 브랜치:** `main`
- **정확한 상대 경로:** `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_CLASSIC_PAT_REAL_WRITE_AND_LIVE_PREFLIGHT_ONE_SHOT_r0001_20261114.md`
- **Work ID:** `COWORK-DROPBOX-TO-GITHUB-MIGRATION`
- **사용자 확정:** CoWork는 개인 운영이며 **기존 Classic PAT를 앞으로도 기본으로 사용**. fine-grained 전환·새 PAT 발급·만료 기한 강제를 **이번 작업의 조건으로 삼지 않는다**. 관련 일반 논의를 반복하지 않는다.
- **이 문서는 GitHub PRIVATE 인계서이며 Windows 실행/사용자 인증/운영 설치/유료 모델 호출/LIVE 승인이 아니다.**
- **운영 현재 상태:** `ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER`.
- **금지:** 추가 유료 Claude 리뷰, 신규 READY로 리뷰 디스패치, 운영 DB/WAL/SHM·예약 작업·Notifier/Bridge 변경, 실제 Telegram 발송, PUBLIC ZIP 배포, GitHub LIVE 전환.

## 1. 실제 최신 상태를 기준으로 시작

1. `collab/START_HERE.md` 및 이 Work의 `CURRENT.md` **최상단**, `TRACKER.json`, `GPT_B_R2_SHADOW_DISPOSITION_r0001_20261114.md`를 확인. 이 인계서를 유일한 이번 실행 범위로 삼고 구형 fine-grained 강제 프롬프트는 다시 실행하지 말 것.
2. 이미 완료된 `REQ-COWORK-V0217-R2-20261114` R2 정적 리뷰 결과 및 영수증은 **원격 게시·비용 지불·격리 원장 publish-only 시험 완료**(호스트 보고). `MODEL_CALL_DELTA=0`이 필수. 이 리뷰를 다시 시작하거나 기존 원본 요청·영수증을 수정하지 않는다.
3. Windows 로컬 격리 후보 `v0.2.17`과 토큰 설치/검증 도구 `b_r2/token_write/Install-EngineWriteToken.ps1`, `verify_engine_write_token.py`, `probe_existing_pats.py`의 실제 경로·기능을 확인. 없다면 해당 부분만 `NOT_AVAILABLE`로 기록 후 가능한 독립 단계 계속.

## 2. Classic PAT 기본 인증 계약을 사용해 실제 연결 검증 — 최우선

- **이 PC에서 이미 확인된 감시기 쓰기용 Classic PAT**를 재사용한다. PAT 타입·무기한 만료 자체를 FAIL로 판정하는 기존 게이트를 **격리 시험용 코드/설정에서만** Classic 허용으로 바꾼다. 코드 수정·회귀는 격리 작업 복사본에서만 수행하며 기존 Windows 운영 설치본·기존 자격파일을 승인 없이 덮어쓰지 않는다.
- 토큰 값·접두·길이·해시·보관 경로·환경변수·개인정보·GitHub 계정 정보를 **어떤 GitHub 파일, 도구 인자, 콘솔 로그, Claude 채팅, 결과 문서에도 출력하지 않는다**. Python 메모리/사용자 보호된 로컬 자격 경로에서만 사용하며 `gh` 개발자 로그인 성공을 감시기 PAT 검증으로 오인하지 않는다.
- 고정 목적지: `wonhwipark/CoWork-Skill-Collab`; GitHub 서버 실제 저장소 ID `1451933830`과 일치 여부, 해당 PAT로 GET 및 Contents write가 가능한지 실측. 사용자 승인 Classic을 기술적 형식 문제만으로 불가 처리하지 말고, **정상 동작 여부로** 판단.
- **임시 테스트 브랜치**를 유일한 원격 쓰기 대상에 사용. 단일 비민감 fixture 파일을 PAT 자체로 create→readback→update→readback→cleanup, 실제 HTTP 및 원격 SHA/바이트 검증. `main` 기존 REQUEST/READY, 리뷰/영수증, 배포 ZIP·대시보드·운영설정 변경 금지. 임시 브랜치 삭제 실패 시 `CLEANUP_PENDING`으로 남겨 후속 정리(운영 삭제 확대 금지).
- PAT가 기술적으로 실패하면 status/원인(권한 거부·형식·엔진 설정 미연결 등)만 설명하고 허용된 격리 코드 수정·재시험을 하나의 작업으로 처리. 인증 우회·불필요한 새 PAT 발급 질문 금지.
- `PAT_TYPE_ACCEPTED=CLASSIC_PER_USER_DECISION`은 사용자 정책이고, **`GITHUB_WRITE_E2E=PASS`는 실제 시험 성공이 있어야만 기록**.

## 3. 감시기 게시 경로 E2E — Claude 모델 호출 0

- 테스트는 **독립 fixture 결과/영수증**을 만든 뒤 **GitHub watcher 코드의 실제 게시/재개 경로**를 격리 state DB와 *임시 브랜치*로 사용. 모드 `SHADOW_READ_ONLY` 자체에는 절대로 쓰기 활성화 금지. 별도 오프라인/격리 transport 시험 프로세스에서만 테스트.
- 리뷰 요청을 새로 디스패치하지 않고, 모델 실행기/CLI 실행은 구조적으로 불가능하게 막는다. 새 `REQUEST/READY/APPROVAL_SIG`를 생성하지 말 것.
- `RESULT_SAVED→UPLOAD_PENDING→COMPLETED` 첫 자동 게시·remote readback, 재시도 시 `ALREADY_PUBLISHED` 멱등 정산, 원격 파일 내용 충돌시 fail-closed·덮어쓰기 0, 재시작 시 중복 게시/리뷰 0, 실제 엔진/발행기 결과를 확인.
- 이전 R2 실물 3개에 대해서는 이미 `ALREADY_PUBLISHED`와 격리 원장 `UPLOAD_PENDING→COMPLETED` 시험 보고가 있으므로 **추가 유료 실행 없이 원격 정합만 확인**. 원본 운영 원장 상태를 직접 수정하지 않는다.
- 테스트 도구가 main 전용이고 임시 브랜치가 불가하면 안전하지 않은 실행을 강행하지 말고 독립 branch 지원을 격리 복사본에 최소 수정하여 단위/루프백 회귀 후 재시도. 운영분기 변경이 필요하면 `NOT_RUN_BLOCKED_BY_ISOLATION`로 기록.
- 증거: 목적지 repo/브랜치, 비밀 없는 HTTP method/status, fixture 바이트 SHA/size, 영수증 GET 확인, `MODEL_CALLS=0`, `PAID_COST_DELTA=0`, `TELEGRAM_SENDS=0`, `OPERATING_DB_WRITES=0`.

## 4. 남은 LIVE 게이트를 동시에 축소 — 운영 변경 금지

1. **운영 cryptography gap:** 운영 Python 3.11.9 환경 불변. 격리 venv에만 이미 있는 Ed25519 백엔드로 실서명 PASS/FAIL/만료·오염·다른 저장소 부정시험. 운영 인터프리터의 `cryptography` 미설치는 별도 운영 설치 승인이 필요한 게이트로 명시.
2. **N1 승인 재사용:** 로컬 DB 상태 소실·복원·기존 READY 재노출 시 새 모델 호출 0을 검증 가능한 synthetic 테스트로 재현. 확인된 갭은 기존 패키지 수정 없이 격리 후보 `v0.2.18`에서 최소 패치/회귀시험 수행 가능. 보호된 완료 이력·서명 nonce 사용 기록/승인 유효기간을 재사용하는 방향으로 중복 방지를 검증. 실제 비용 리뷰는 절대 실행하지 않는다.
3. **N2 실제 GitHub repo ID 결합:** 신뢰 루트/서명/핀과 GitHub 서버 ID `1451933830`을 코드 경로에서 비교하는 fail-closed 판정을 격리 후보에 구현/시험 가능. 정상·다른 repo·미조회·API 403/timeout 케이스를 확인. 신뢰키 생성/교체·운영 신뢰루트 변경은 금지.
4. **복합 Q8:** usage-limit 대기→재시작→local policy revision 변경/롤백→커서 유실→동시 scan/watch 잠금→중복 호출 0을 실제 모델 없이 합성시험. 실 CLI 사용량 제한 문자열이 실제 관측되지 않았으면 `NOT_VERIFIED` 유지하고 일부러 유료 한도 소진을 유발하지 않는다.
5. **Notifier 중복:** `notify_reviews.py --watch` 2개 관측의 부모 PID·명령줄·Task·송신 대상 관계를 읽기 전용 조회하여 중복 전송 경로 가능성 분석. 종료·일정 변경·설정 수정·실전송 금지. 기존 pending 1건과 영수증 중복 방지·워터마크 이전안을 비발송 계획으로 작성.
6. **SHADOW 강화:** 별도 계정 enforce/네이티브 I/O/장기 가동은 필요한 관리자 승인 없으면 `NOT_RUN`. 이미 통과한 단기 SHADOW·격리 백업복구 결과를 다시 무의미하게 반복하지 않는다.

- 후보 코드를 바꾼 경우 `v0.2.17` 리뷰 PASS를 **수정된 `v0.2.18`에 소급 적용하지 않는다**. `v0.2.18` ZIP을 만들면 신규 버전·실제 SHA256·크기·CRC·파일/비밀 스캔·자체시험을 기록하고 **`development_not_for_deployment`**로 격리 보관. PRIVATE 리뷰용 게시 가능 여부를 코드 비밀 스캔 결과와 전송 허용범위 확인 후 판단. **새 유료 리뷰나 PUBLIC 배포는 이 승인에 포함되지 않음**.
- N1/N2가 코드 변경 없이 이미 검증 가능한 운영 불변식으로 해결되는지 확인해 불필요한 기능 확장을 피한다. 필요한 수정만 적용하고 결과 통합.

## 5. 결과 및 판정용 산출물

- 결과 MD 정확한 경로: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CLAUDE_CLASSIC_PAT_GITHUB_WRITE_E2E_AND_LIVE_PREFLIGHT_RESULT_FOR_GPT_20261114.md`
- 구분: `PAT_CLASSIC_ACCEPTED`, `PAT_GITHUB_READ`, `PAT_BRANCH_WRITE_READBACK`, `BRANCH_CLEANUP`, `WATCHER_INITIAL_UPLOAD_E2E`, `IDEMPOTENT_PUBLISH`, `N1`, `N2`, `Q8`, `CRYPTO_TEST_VENV`, `CRYPTO_OPERATING`, `NOTIFIER_READ_ONLY_AUDIT`, `SHADOW_ACCOUNT_ENFORCE`, `OPERATING_DB_INVARIANTS`, `PAID_CALLS_DELTA`, `ACTIVE_PROVIDER`. 실제 값은 `PASS/FAIL/SKIP/NOT_RUN/BLOCKED`로 기록.
- 각 독립 결함의 수정·비수정·재시험 및 `v0.2.18`이 있으면 후보 무결성/해시와 자기시험/독립 리뷰 상태 구분.
- 결과 MD·기존 `CURRENT.md` 최상단·`TRACKER.json`을 GitHub PRIVATE **main에 PR 없이 직접 게시**, 원격 commit+내용/바이트 readback 확인, 이전 기록 보존. 비밀·토큰·회사 L1 코드 게시 금지.
- 모델 호출 0, 운영 변경 0, LIVE 전환 0. **`ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER` 유지**. 다음 사용자 액션은 운영 설치나 최종 LIVE처럼 필요한 항목에 한정.

## Windows Claude Code 실행 프롬프트

```text
GitHub PRIVATE wonhwipark/CoWork-Skill-Collab, main의 collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_CLASSIC_PAT_REAL_WRITE_AND_LIVE_PREFLIGHT_ONE_SHOT_r0001_20261114.md를 이번 최신 원샷 인계서로 읽고, 기존 Classic PAT를 CoWork의 확정 기본 인증으로 사용해 실제 GitHub 임시브랜치 write/readback/cleanup과 watcher 게시 경로 E2E를 모델 호출 0으로 검증해줘. 기존 fine-grained 강제 조건이나 PAT 교체 논의를 반복하지 말 것. N1/N2/Q8는 격리 코드·합성시험에서 필요한 최소 보완까지 묶어서 수행하되 운영 설치·DB/Task/Notifier/실알림·추가 유료 리뷰·PUBLIC 배포·LIVE 전환은 하지 마. 최신 결과 MD, CURRENT.md, TRACKER.json을 PRIVATE main에 PR 없이 게시하고 commit/원격 바이트 재조회까지 검증해줘.
```
