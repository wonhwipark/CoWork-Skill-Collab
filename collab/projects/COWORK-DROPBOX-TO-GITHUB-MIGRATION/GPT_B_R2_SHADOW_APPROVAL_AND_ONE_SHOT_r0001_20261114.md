# CoWork GitHub LIVE 준비 — B안 + v0.2.17 R2 + 실호스트 SHADOW/DB 리허설 통합 승인·실행 인계

- 기준일: 2026-11-14 KST / r0001
- 기준 저장소: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`
- 기준 브랜치: `main`
- 정확한 상대 경로: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_B_R2_SHADOW_APPROVAL_AND_ONE_SHOT_r0001_20261114.md`
- Work: `COWORK-DROPBOX-TO-GITHUB-MIGRATION`
- 승인 상태: `USER_APPROVED_2026-11-14_KST` (대화에서 앞서 GPT가 제시한 **3개 항목**에 대해 사용자 "그래 승인해줘")
- 문서 상태: 사용자 승인 의도를 기록한 인계서. **서명된 APPROVAL/REQUEST/READY 자체가 아니며 GitHub 문서 게시만으로 watcher 실행하지 않는다.**
- 현재 운영 상태: `ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER`

## 1. 사용자 승인 범위 — 3개 항목만

**B안 — 감시기 쓰기 PAT: 승인.**
- GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab` **단일 저장소에만** 사용되는, 기한이 있는 fine-grained PAT의 **발급·안전 설치·검증**을 허용한다.
- 감시기 목적에 필요한 최소 권한: repository Contents Read/Write 및 GitHub가 자동 부여하는 Metadata Read. 다른 저장소, 워크플로 수정, Secrets, 관리자 권한, 광역 classic `repo` 교체/폐기까지 승인한 것은 아니다.
- 값·접두·파일경로·비밀이 로그/PRIVATE/PUBLIC에 나오지 않도록 한다. Windows 보호 위치(Dropbox 등 동기화 폴더 밖)에 저장. 기존 읽기전용 자격/개발자 `gh` 로그인과 역할 분리. 실제 token JSON/원문 파일 계약·만료 검사·원격 읽기/쓰기 동작 검증. 쓰기 권한의 시험은 격리된 승인 테스트 경로에만 하고 운영 요청·영수증을 손상시키지 않는다.
- PAT 생성에 GitHub 웹 UI나 사용자 로그인 조치가 필요하면 **그 행위만 ACTION_REQUIRED**로 보고한다. 자격을 우회하거나 토큰 값을 요청서에 붙이지 않는다.

**v0.2.17 R2 독립 리뷰: 승인.**
- 격리 개발 후보 **정확한 `v0.2.17` 최종 바이트와 고정 SHA-256**에 대해 **독립 Claude Code 구조 리뷰 정확히 1회**, 등급 `R2`, 정책 `POLICY-STATIC-V1-LARGE`, 최대 비용 **USD $3.00**, 별도 새 Review ID, 노력 수준은 지원/정책에 맞는 기본값을 사용한다.
- 모델 호출 전에 최종 ZIP/manifest/diff를 **CoWork 자체 비민감 코드만** PRIVATE `review-inputs/<new_review_id>/`에 신규 게시·원격 고정 commit/실제 SHA-256/ZIP CRC 확인. 기존 v0.2.14/v0.2.16, 이전 리뷰 결과는 불변.
- 리뷰 범위: v0.2.14→v0.2.17 **전체 변경 중 위험 부분**(v0.2.16 usage-limit 대기/재개·토큰 JSON/Notifier 변경, F1~F5 회귀수정, `scan`/`watch`, 다른 policy revision/재승인/커서 손실, 다른 key의 비용/횟수 원자 예약, `REVIEW_UNCERTAIN`, 결과 게시 실패 시 모델 재호출 0, Windows `.cmd` timeout/process tree, SHADOW exit code 6, repo_id 원격 identity, 서명/토큰/crypto runtime).
- 검증된 사용자 승인 문서와 정식 서명·SOURCE_PIN·REQUEST·READY 계약을 따라야 한다. READY를 마지막에 게시, 사전 사용자 승인 예산·해시·일일 횟수·중복 확인. `ACTIVE_PROVIDER=NONE`이므로 **일반 운영 LIVE 대신 격리된 승인 리뷰 실행 경로**로 1회 수행하되 승인/서명/모델 호출 제한을 우회하지 않는다.
- CLI 2.1.218에서 `--max-turns`가 미지원이라는 기존 실측을 우선 적용하고, 지원되지 않는 옵션 재시도 금지. 입력 최소화·정식 `--max-budget-usd 3` 지원 확인·예산 초과 fail-closed. R2 5 turns·40k/6k 토큰은 **목표**이며 강제 가능하다고 주장하지 않는다. 정책 예산을 안전하게 강제할 수 없으면 호출 없이 `BLOCKED_BUDGET_ENFORCEMENT`.
- 첫 모델 호출이 완료됐으나 게시가 실패하면 `UPLOAD_PENDING` 보존, 동일 요청 재호출 **0**. 새 수정본/추가 재리뷰는 **이 승인에 포함하지 않음**. 동일 개발 세션 시험은 독립 리뷰로 인정하지 않는다.

**실호스트 SHADOW + 운영 DB 백업/격리 복구 리허설: 승인.**
- Windows 실제 호스트에서 **분리 계정·격리 DB/상태 경로**로 GitHub SHADOW **읽기만** 시험한다. SHADOW 모드에서 모델 호출 0, GitHub 원격 쓰기 0, 운영 DB/main-WAL-SHM 쓰기 0, Telegram/Notifier 발송 0, 예약 작업 변경 0, LIVE 활성화 0을 입증한다.
- **실제 운영 DB의 일관된 백업과 격리 복사본에만 복구**하는 리허설을 허용한다. 소스 DB의 main/WAL/SHM 수정 또는 기존 운영 데이터 이행·교체·초기화·운영 Task 설치는 승인하지 않음. 안전한 읽기 경로를 확증할 수 없거나 복사 도중 원본 DB side-effect가 발생할 우려가 있으면 이 항목만 `BLOCKED_SOURCE_DB_SAFETY`로 두고 운영 DB를 열지 않는다.
- 백업 내용/암호·개인정보·토큰·경로는 PRIVATE에도 게시하지 않는다. 검증된 복사본의 크기/해시·복구 `PRAGMA integrity_check`/운영 데이터 불변 확인 결과·롤백 체크리스트 등의 **비민감 증거**만 게시. 복구 시험이 운영 경로를 덮어쓰지 않도록 한다.
- 운영 인터프리터 시험의 17개 SKIP을 분류하고, 서명 검증 crypto 라이브러리 호환성·실호스트 호출 경계 확인. Notifier와 GitHub 전환은 **연동 가능성·차이 분석/비발송 리허설**만 허용하며 실제 알림 발송이나 설정 전환은 미승인.
- SHADOW가 GitHub 원격에 결과를 게시하거나 유료 reviewer를 호출하지 않도록 **R2 리뷰 실행과 SHADOW 읽기 전용 시험은 모드·상태·프로세스를 분리**한다.

## 2. 이번 승인에 포함하지 않는 사항

- **GitHub LIVE 활성화/기존 Dropbox watcher 재활성화, 활성 provider 전환, 운영 Windows Task 변경/설치, 운영 데이터 DB 마이그레이션/복원, 실 알림 발송**: `NOT_APPROVED`.
- **R0~R3 상시 자동 유료 리뷰 예산 정책**: `NOT_APPROVED`. 설계만 유지하며 이번에 승인된 **v0.2.17 R2 한 건**을 다른 신규 작업 승인으로 확대하지 않는다.
- `v0.2.17` 이후 추가 유료 리뷰/재리뷰, 심층 R3 승급, 비용 $3 초과, PUBLIC 신규 ZIP 게시, 다른 저장소 변경: `NOT_APPROVED`.
- 회사 L1 코드/고객자료/토큰/운영 비밀을 PRIVATE에도 올리지 않는다. `/AI-CONTINUITY/` 불변.

## 3. Windows Claude Code 원샷 실행 순서

1. PRIVATE `main`의 `collab/START_HERE.md`, 이번 Work `CURRENT.md` 최상단, `TRACKER.json`, `GPT_A_V0214_INDEPENDENT_REVIEW_DISPOSITION_r0001_20261114.md`, 이 인계서와 `REVIEW_TRANSPORT_V1.md`만 필요한 범위로 재확인. 이미 완료된 A안 R1 리뷰는 다시 호출하지 않는다.
2. v0.2.17 **로컬 격리 후보**에서 ZIP 자체 바이트/CRC·path traversal·민감정보·버전·소스·diff를 실측해 고정한다. v0.2.16 usage-limit와 F1~F5, repo_id 실제 원격 binding·등록부·재시작 경계, SHADOW 거부 종료코드를 중심으로 별도 테스트 실행. PASS/FAIL/SKIP 실제 결과와 변경 파일을 기록. 패치가 필요하면 리뷰 전에 최종 후보를 다시 고정하며, 그 이후 리뷰 대상 바이트를 바꾸지 않는다.
3. 최소권한 쓰기 PAT를 안전하게 발급/설치할 수 있는 사용자 인증 경로를 확인. 사용자의 수동 조치가 필수면 그 부분만 `ACTION_REQUIRED`; 임의 API 토큰 생성·광역 기존 `gh` 자격을 감시기용으로 재사용 금지. 사전 승인된 격리 테스트 경로에서 Contents Read/Write·만료·token format·repo_id 정합성을 실측.
4. 최종 `v0.2.17` ZIP + SHA/diff/manifest를 PRIVATE review-inputs에 업로드하고 원격 바이트/해시/고정 commit을 확인. signed request/approval/READY를 기존 계약대로 별도 준비하고 유효성·비용·중복 검사 후 **승인된 R2 리뷰 1회만** 실행. 결과/사용량 영수증은 엔진으로 게시·원격 재조회. 게시 실패 때는 `UPLOAD_PENDING`, 동일 모델 재호출 금지, 서명/승인 보호를 우회하지 않는다.
5. **R2 모델 리뷰와 분리**된 실호스트 SHADOW 읽기 전용 검증을 수행. 분리 state·DB/계정, GitHub remote write=0, reviewer model calls=0, Telegram=0, 운영 DB/WAL/SHM write=0, single LIVE 보호를 실제 로그/해시/권한 근거로 확인. 원본 DB 안전 백업·격리 복사본 복구·무손실/복원 계획만 수행하고 원본 운영 상태는 변경하지 않는다.
6. 테스트 실패·결함이 발생하면 승인된 범위의 격리 후보를 수정·재시험하되 **모델 재리뷰는 1회 제한**. 리뷰 후 후보를 수정하면 기존 리뷰를 수정본 PASS로 승계하지 않고 신규 리뷰 승인 요청으로 남긴다. SHADOW/복구/알림 등 미수행은 정직하게 `NOT_RUN/BLOCKED`.
7. 단 하나의 통합 결과 `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CLAUDE_B_R2_SHADOW_PREFLIGHT_RESULT_FOR_GPT_20261114.md` 및 `CURRENT.md`·`TRACKER.json`을 PRIVATE `main`에 **PR 없이 직접 게시**하고 remote commit/본문 bytes SHA readback을 재검증. 기존 `CURRENT.md` 과거 이력은 보존. 결과에 각 구분별 `PASS/FAIL/SKIP/NOT_RUN`, 사용 비용/토큰/호출 횟수, 새 ZIP SHA/크기/경로, independent review 결과, 인증/SHADOW/DB/복구/Notifier 실제 증거, 남은 LIVE 차단·최종 승인 필요 사항을 명시.

## 4. GPT 후속 판정 및 LIVE 게이트

- GPT가 원격 통합 결과·R2 독립 리뷰·영수증·최종 ZIP을 다시 읽어 개별 지적을 `수용/수정수용/거절/보류/추가 정보 필요`로 판정하고, 실제 확인 가능한 게이트만 해제한다.
- 운영 결과 재조회·실호스트 백업/격리 복구·Notifier 이행·기존 미정산 요청 무손실 보존·중복 알림 0·단일 ACTIVE_PROVIDER와 rollback 점검 **후에도**, **LIVE 전환에는 사용자의 별도 명시적 최종 승인**이 필요하다.
- **이 문서 작성·게시만으로 Windows Claude Code 자동 호출/유료 리뷰 시작/LIVE 전환이 일어나지 않는다.**

## Windows Claude Code 실행 문구

```text
GitHub PRIVATE wonhwipark/CoWork-Skill-Collab, main의 collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_B_R2_SHADOW_APPROVAL_AND_ONE_SHOT_r0001_20261114.md를 유일한 최신 인계서로 읽고, 이미 승인된 3개 작업(감시기 전용 최소권한 만료형 Contents Read/Write PAT 준비·검증, 최종 v0.2.17 고정 ZIP의 R2/POLICY-STATIC-V1-LARGE 독립 리뷰 1회 최대 $3, 실호스트 읽기전용 SHADOW+운영 DB 안전 백업/격리 사본 복구 리허설)을 승인 범위 안에서 원샷 수행해줘. 기존 v0.2.14 리뷰 재호출 금지, 결과 업로드 실패 시 모델 재호출 금지. R0~R3 상시 유료 정책, 새 리뷰 2회 이상, 운영 DB/Task/알림 변경, PUBLIC 배포, GitHub LIVE 전환은 승인하지 않았어. 사용자 GitHub UI PAT 생성이 필수면 그 부분만 ACTION_REQUIRED로 두고 나머지 가능한 검증은 진행해줘. 결과 MD와 CURRENT/TRACKER를 PRIVATE main에 PR 없이 게시해 원격 byte/hash readback 확인해줘.
```
