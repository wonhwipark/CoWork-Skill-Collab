# GPT → Windows Claude Code — 기존 PAT 검증·안전 설치·publish-only 원샷 인계

- r0001 / 2026-11-14 KST
- Canonical repository: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`
- Branch: `main`
- Exact relative path: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_EXISTING_PAT_VERIFY_AND_PUBLISH_ONLY_ONE_SHOT_r0001_20261114.md`
- Work ID: `COWORK-DROPBOX-TO-GITHUB-MIGRATION`
- 사용자 지시: **"pat 이미 있어" → "그래진행하자"**. *새 PAT를 발급하라는 반복 요청을 중지하고 기존 PAT의 적합성부터 확인한다.*
- `PAT_EXISTENCE=USER_REPORTED`; `PAT_ELIGIBILITY=NOT_VERIFIED`; `MODEL_CALLS_ALLOWED=0`; `ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER`.
- 범위: 이전에 승인한 B안 감시기 인증 안전 설치/검증 및 **이미 완료된 R2 결과의 publish-only/원격 readback**만. 그 밖의 운영 변경·추가 유료 리뷰·LIVE 미승인.

## 1. 먼저 읽을 정본 — 과거 인계 재실행 금지

1. `collab/START_HERE.md`에서 현재 운영 경계 확인 후, 이번 작업 `CURRENT.md` **최상단**, `TRACKER.json` 및 `GPT_B_R2_SHADOW_DISPOSITION_r0001_20261114.md` 확인.
2. `CLAUDE_B_R2_SHADOW_PREFLIGHT_RESULT_FOR_GPT_20261114.md`의 §5·§3에서 Windows 호스트 관찰/준비된 토큰 스크립트·기존 R2 업로드 상태 확인. 새 R2 리뷰 금지.
3. 로컬 검증 도구(이전 호스트 보고): `b_r2/token_write/Install-EngineWriteToken.ps1`, `b_r2/token_write/verify_engine_write_token.py`. 실제 위치·입력 인수는 **Windows 로컬에서 찾아 사용법/소스 검토**. 파일 존재하지 않으면 허용 범위의 코드 구현 및 오프라인 테스트를 수행하되 운영 설치나 토큰 값 추출을 우회하지 말 것.
4. 필요하면 `collab/ops/CONTRACTS/REVIEW_TRANSPORT_V1.md`·`REVIEW_TIER_TOKEN_BUDGET_V1.md` 확인. GitHub 문서 게시 자체는 watcher 실행 신호가 아니다.

## 2. 기존 PAT 검증 — 우선순위 1

- Windows PC의 기존 credential을 **로컬에서만** 확인. 후보에는 이전에 보고된 read-only fine-grained, classic/무기한 쓰기 토큰 외에 사용자가 보유했다고 밝힌 다른 PAT도 포함될 수 있다. 이미 보유한 토큰이 기존 두 토큰과 같다고 단정하지 말 것.
- 토큰 **값, 접두, 길이, SHA/fingerprint, 비밀 파일 경로·환경변수 값, 계정 식별정보를 콘솔/GitHub/Claude 결과/채팅에 출력하지 않는다.** 사용자에게 토큰 문자열을 붙여넣게 요청하지 않는다. 가능한 안전한 현장 인증/숨김 입력·보호 파일을 활용.
- PASS 조건: GitHub **실제 서버** 기준 토큰이 `wonhwipark/CoWork-Skill-Collab` 한 저장소에 한정되는 **fine-grained PAT**, **Repository Contents: Read and write**, Metadata Read 자동, 유효 만료 **90일 이하**(보유 당시 정책; 만료일까지 충분한 잔여 기간 확인), 다른 불필요 권한 없음, 동기화되지 않는 보호된 Windows 경로에 안전히 보관.
- **설정 JSON의 `repo` 필드나 `gh auth status`만으로 허가된 PAT임을 인정하지 않는다.** 실제 PAT로 GitHub 인증하여 identity/허용 repository/scope·expiry 및 부정 테스트를 확인. 검증되는 범위와 GitHub API가 권한 정보를 직접 노출하지 않아 추론한 부분을 구분. GitHub 커넥터/개발자 gh 로그인의 성공을 **감시기 전용 PAT 검증으로 오인하지 않는다.**
- 기존 PAT가 위 조건을 이미 충족하면 **추가 발급 없이 사용**. 조건 미충족이라면 우회해 classic 광역 토큰을 watcher에 적용하지 말고 어떤 조건이 실패했는지만 `ACTION_REQUIRED_TOKEN_SCOPE_OR_EXPIRY`로 보고. 사용자에게 재발급을 요구하는 것은 이 분기에서만.
- 기존 토큰을 읽기 위해 운영 프로세스/Task/ACL 변경이 필요하면 그 항목은 `BLOCKED_OPERATIONAL_CHANGE`로 격리, 다른 가능한 정적·오프라인 검증 계속.

## 3. 승인된 PAT의 보호 설치·격리 원격 쓰기 시험

1. 준비된 로컬 설치 스크립트와 검증기를 먼저 **정적 검사**. 사용자 보호 ACL, 비밀 비노출, 동기화 폴더 거부, 덮어쓰기 보호, 만료 정책, 기존 운영 구성 불변 확인.
2. 이 스코프로 승인된 **감시기 전용 보호 자격파일**에만 설치; 운영 watcher 실행 설정/Task·기존 credential 교체나 broad-scoped gh 대체는 금지. 인증 방식은 제품의 `read_github_token` JSON/원문 지원을 맞추고 비밀은 문서에 담지 않는다.
3. **토큰 자체**만 사용하여 PRIVATE repo의 격리 **임시 브랜치/시험 파일**에 최소 1회 create/update/readback, 실패 사례(read-only token으로 403 등) 확인. 시험 범위 밖 main/기존 REQUEST/READY/REVIEW_RESULT/RECEIPT는 수정하지 않는다. 임시 브랜치는 성공적으로 만든 것만 기록하고 무손실 삭제. 삭제가 막히면 `CLEANUP_PENDING`과 분리 기록.
4. GitHub repo 실제 ID `1451933830`를 서버에서 읽어 고정 trust-root label과 대조한다. **현재 값이 같아도 제품 runtime repo_id binding이 구현됐다고 선언하지 않는다**(N2 별도 LIVE 게이트).
5. 설치 및 실제 write/readback 증거가 나오면 `PAT_ELIGIBILITY=PASS`, `WRITE_PROBE=PASS`, `TOKEN_INSTALLED=PASS` 등 **각각 실측 결과**로 기록. 실패시 PASS 임의 보고 금지.

## 4. 기존 R2 결과의 publish-only 판정·재시도 (모델 호출 금지)

- 이미 완료·비용 정산된 **단 하나의 리뷰** `REQ-COWORK-V0217-R2-20261114` rev 1, ZIP SHA-256 `824f26c4e28fcc804ed1dd3942a34408c54b9091be34ecb1693cc4cb9d46df03`, `POLICY-STATIC-V1-LARGE`. 기존 리뷰 commit: `REVIEW_RESULT_1.md` `c2aeee1757d0...`, 영수증 `7977241953c9...`, 사용영수증 `c1429f10d07d...`. **R2 정적 리뷰를 다시 시작하지 않는다.**
- 기존 엔진 격리 DB의 `UPLOAD_PENDING`과 로컬 저장 결과/원격 게시 파일을 **먼저 읽기 전용으로 비교**. 개발자 `gh`로 이미 게시된 원격 결과·영수증이 **실제 같은 바이트**라면 신규 게시가 아니라 **idempotent ALREADY_PUBLISHED/readback/reconcile** 처리. 기존 원격 결과를 덮어쓰지 않는다.
- 처리할 잔여 결과가 있으면 **정상 publish-only 경로만** 사용해 재조회 검증. 실제 GitHub 쓰기 검증 시 비용 리뷰·signed APPROVAL/READY를 신규 생성하지 않는다. 결함으로 인해 기존 R2 모델 재시작 위험이 있으면 **즉시 그 단계 중단**하고 읽기 전용 증거만 보고.
- `reviewer_model_calls_delta=0`; `new_paid_review_count=0`; `notification_sent=0`을 증거로 남긴다. 원격 readback 후 로컬 상태가 `UPLOAD_PENDING`에서 완료로 정상 정리되는지 **운영 아닌 격리 원장**에서 검증. 이미 게시됨/충돌은 재호출 0으로 보존하고 fail-closed.
- `ACTIVE_PROVIDER=NONE`에서 LIVE watcher를 깨우지 말고 승인받은 인증/격리 게시 복구 스크립트로만 테스트. 읽기전용 SHADOW 모드에서 쓰기 동작을 수행하지 않는다.

## 5. 결과 정리·품질 게이트

- 이전 문서에 남은 **"PAT 발급 필요"는 구 관찰에 근거한 판단**이므로 신규 PAT 의무로 되살리지 않는다. 최상단 사용자 정정과 새 호스트 실측이 우선.
- 새 리뷰/ZIP 패치/crypto 운영 설치/Notifier 프로세스 종료·수정/운영 DB 수정/Task 변경/실 알림/R0~R3 상시 정책/최종 LIVE 전환 = **NOT_APPROVED**.
- 결과를 `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CLAUDE_EXISTING_PAT_VALIDATION_AND_PUBLISH_ONLY_RESULT_FOR_GPT_20261114.md`에 **비민감 요약**으로 기록. `PAT_CANDIDATES_CHECKED`(수만 기록) / `PAT_ELIGIBILITY` / `INSTALL` / `WRITE_PROBE` / `PUBLISH_ONLY` / `MODEL_CALL_DELTA` / `CLEANUP` / `REMAINING_LIVE_GATES`를 PASS/FAIL/NOT_RUN/ACTION_REQUIRED 구분.
- 같은 작업에서 `CURRENT.md` **최상단에 새 결과를 덧붙이고 기존 이력 보존**, `TRACKER.json` 유효 enum으로 갱신. PRIVATE `main`에 **PR 없이 직접 게시**하고 원격 commit·문서 실제 bytes/sha256 readback 확인.
- 필요한 작업 인증/보호 폴더 접근이 막히면 **해당 항목만 ACTION_REQUIRED/BLOCKED**로 남기고 나머지 가능한 시험은 실행. 개인키/토큰을 GitHub PRIVATE에도 올리지 않는다.
- 최종 운영상태 `ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER` 유지. **LIVE는 별도 최종 승인**.

## Windows Claude Code에 전달하는 1회 프롬프트

```text
GitHub PRIVATE wonhwipark/CoWork-Skill-Collab, main의 collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_EXISTING_PAT_VERIFY_AND_PUBLISH_ONLY_ONE_SHOT_r0001_20261114.md를 최신 원샷 인계서로 읽고 Windows에서 승인된 범위를 끝까지 수행해줘. 사용자가 이미 PAT가 있다고 확인했으므로 신규 발급부터 요구하지 말고 기존 토큰을 값/경로 노출 없이 직접 검증해. 적격 fine-grained Contents Read/Write 단일 PRIVATE repo 토큰이면 기존 로컬 보호 설치 도구로 안전하게 설치하고 임시 브랜치에서 원격 write/readback 시험 후 정리해줘. 이미 게시된 R2 결과는 먼저 바이트 비교하여 publish-only idempotent 재확인/정리만 수행하고 모델 추가 호출·리뷰 재실행 0을 보장해. R0~R3 상시 정책·운영 DB/Task/Notifier 변경·cryptography 운영 설치·LIVE 전환은 금지. 결과 MD 및 CURRENT/TRACKER를 PRIVATE main에 PR 없이 게시하고 원격 readback까지 확인해줘.
```
