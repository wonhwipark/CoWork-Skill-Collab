# Windows Claude Code 원샷 인계 — 실제 GitHub SHADOW(C) → 독립 리뷰(E) 조건부 연속 수행
작성일: 2026-11-12 KST | 개정: r0001
상태: **HANDOFF_PREPARED_NOT_EXECUTED / MIGRATION_NOT_CUTOVER**
저장소: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`
브랜치: `main`
정확한 인계 경로: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/WINDOWS_C_SHADOW_TO_E_INDEPENDENT_REVIEW_ONE_SHOT_r0001_20261112.md`
작업 ID: `COWORK-DROPBOX-TO-GITHUB-MIGRATION`

## 0. 실행 지시와 승인 경계
사용자 요청은 **C 실GitHub 읽기 전용 SHADOW 검증과 E 정식 독립 리뷰를 하나의 후속 작업으로 연속 처리하는 원샷 운영 방식의 준비 및, 이미 승인된 범위에서의 실행**이다. 이 문서 게시나 "한 번에 진행" 발언을 새로운 PAT/실서명키 발급·민감 소스 반출 허가·유료 리뷰 실행·운영 변경 승인으로 해석하지 않는다. 조건이 실제 충족되면 C→D/B 검증→E로 같은 실행 세션에서 다음 단계에 진입하되 **승인이 없거나 증거가 불완전한 단계만 BLOCKED/NOT_RUN**으로 분리하고 허용된 문서화·정적 검사·자체시험은 계속 수행한다.

**실행 전 필독 정본:**
- `collab/START_HERE.md`
- `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md` — 최상단 최신 단락과 원격 증거 기준
- `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CLAUDE_STAGE1_APPROVED_HOST_SECURITY_RESULT_FOR_GPT_20261111.md`
- `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/WINDOWS_STAGE1_APPROVED_SECURITY_SHADOW_REVIEW_ONE_SHOT_r0001_20261111.md` — 기존 Stage 1 승인 범위, A~E 세부
- `collab/ops/CONTRACTS/NO_PR_COLLABORATION_V1.md`, `collab/ops/CONTRACTS/REVIEW_TRANSPORT_V1.md`
- `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_B7_TRUST_ROOT_AND_APPROVAL_POLICY_DRAFT_r0001_20261110.md`

## 1. 기준선 고정 / 이미 완료된 작업은 반복하지 말 것
- Windows Claude Code 최신 **자체 보고**: A 비관리자 시험 계정·ACL HOST_REAL PASS, B 시험키 PASS/실운영 서명키 BLOCKED_SIGNER_DEVICE, C 실제 호스트 SHADOW 3주기+ETW 파일 I/O PASS(그러나 GitHub 응답은 SYNTHETIC), D ZIP 외부 반출 BLOCKED, E 독립 리뷰 NOT_RUN(호출 0).
- 호스트에서 수정한 결함 3건을 포함하는 리뷰 후보 **`skill-collab-watcher_v0_2_10`**: 로컬 ZIP **174745 bytes**, 보고 SHA-256 **`67ea7fc63ccc1de77a28025b7c4f1b701ee6f4fa387311bca3f3d2bc7432b108`**. 바이트는 GPT 원격 독립 검증되지 않았으므로 로컬 재해시 필수. 원본과 구버전 ZIP 보존, 임의 업버전/교체 금지.
- 자체 시험 보고: 시험 venv 527 PASS/12 SKIP, 운영 Python 492 PASS/14 SKIP. 수집 차이 33건은 `cryptography`가 없는 운영 인터프리터에서 두 테스트 모듈 35항목 미수집/모듈 SKIP 2건으로 설명됨. **SELF_TEST_REPORTED ≠ INDEPENDENT_REVIEW**.
- 시험 계정은 비활성 보존, 샌드박스 보존. 신규 계정/토큰/키/장비/비용을 필요 없이 재생성하지 말 것. 이전 C 합성시험을 실제 GitHub PASS로 소급하지 않는다.

## 2. 한 번 지시 후 단계별 실행 (수동 1회; 자동 백그라운드 금지)

### Gate 0 — 조건·권한 확인(모델 호출 0)
1. `CURRENT.md` 최신 상태와 Stage 1 증거를 재조회하고 호스트 로컬 v0.2.10 후보의 SHA-256·174745B·파일 수·ZIP 안전성 재확인. 다르면 `BLOCKED_BASELINE_MISMATCH`; 임의 ZIP 교체 금지.
2. 사용 중인 자격증명이 이 PRIVATE 저장소만 대상으로 하는 fine-grained **Contents: Read-only** 권한인지 확인. 대상 repo ID·브랜치 main 검증. 이전에 확인된 과권한 자격을 사용하거나 권한을 줄이지 않고 재활용 금지. 토큰은 사용자가 직접 발급/허용된 비밀 저장소로만 배치; **토큰을 채팅·MD·명령 로그·GitHub에 게시하지 않는다**. 토큰 없음이면 `C=BLOCKED_CREDENTIAL`.
3. 기존 Stage 1의 비관리자 시험 계정·전용 SHADOW 폴더·관리자 전용 공개 trust root ACL을 *시험용으로* 재활용할지 확인. 이전 사용자/GPT 판정은 **SHADOW 시험 완료까지 비활성 보존 후 필요 시 재사용**. 운영 계정·상태 폴더/SQLite/WAL/SHM·lock·작업 스케줄러·Bridge/Dashboard/Telegram 및 Dropbox LIVE watcher에는 변경 금지.
4. C와 E를 별도 게이트로 관리. 실제 GitHub SHADOW 통과가 E의 리뷰 승인 또는 GitHub LIVE 활성화를 의미하지 않는다.

### C — 실제 GitHub 대상 SHADOW 검증 (읽기 전용)
실제 허가된 토큰이 있고 호스트 격리 조건이 맞을 때만:
1. 기존 샌드박스의 `provider_mode=SHADOW`, `ShadowRunner`, SHADOW 전용 DB/state/lock/cursor, 비관리자 실행을 확인. watcher 자체 provider는 LIVE가 아니며 GitHub 응답이 **FakeGitHub가 아닌 실제 원격 GET**인지 구분·기록.
2. **실제 GitHub에 대해 최소 3개 watch 주기 수동 1회** 실행. GitHub API GET 횟수·상태코드·repo/branch·정확한 관찰 시간·커서 관찰 및 주기 성공/실패 보고. 원격 POST/PUT/PATCH/DELETE 0, GitHub/Dropbox 쓰기 0, REQUEST/READY 새 게시 0, 모델 호출/비용 0, Telegram 0, 기존 감시기 작업 중지 0.
3. ETW 등 실 프로세스 파일 I/O 계측으로 기존 운영 DB `state.sqlite3`, `-wal`, `-shm`, 기존 `watch.lock`의 열기/읽기/쓰기/잠금 **0건** 확인. 운영 폴더 자체의 경로 메타데이터 조회와 운영 DB 내부 파일 I/O를 구별해 보고. 측정 실패는 PASS 금지. 운영 파일을 직접 열어 해시 확인하지 말고 이미 승인된 운영 무영향 관측 사용.
4. 기존 Dropbox watcher ACTIVE, 신규 GitHub SHADOW read-only만 동시 존재. 단일 LIVE invariant가 변하면 즉시 시험 중단, 부작용·롤백 가능성 기록. 검증 실패·토큰 미준비는 `C=PARTIAL/BLOCKED` 후 리뷰 준비 문서화만 진행.
5. SHADOW 종료 후 시험 계정은 비활성으로 복구. 시험 계정/샌드박스는 삭제하지 않고 보존/회수 상태를 기록.

### B/D/E 사전 조건 — 독립 리뷰 실행 전 별도 확인
**C 통과만으로 E 자동 호출 금지.** 아래 모두 PASS이고 각 별도 승인 기록이 명확할 때만 정식 E 진행:
- **B 운영 서명**: 별도 승인자 장치에서 Ed25519 운영 개인키를 승인받아 생성·보관(이 감시기 PC에 개인키 미배치), 실제 공개키/pin은 관리자만 수정 가능한 고정 trust root에 **별도 설치 승인**을 받아 배치, 비관리자 쓰기 거부 실측. 시험키를 운영 서명으로 사용 금지. 없으면 `E=BLOCKED_SIGNER_DEVICE`.
- **D 반출**: v0.1.5 유래 UNCHANGED 코드 34개 등 **전체 ZIP 내 항목별 소유권·반출 정책** 확인 및 **PRIVATE 게시의 별도 명시 승인**. secret/PII scan PASS만으로 허가를 대체하지 않는다. 허가 불명 ZIP은 사내 로컬만 보존; `E=BLOCKED_EXPORT_CLASSIFICATION`.
- **reviewer**: 개발 세션과 다른 독립 실행 주체/경로, 정책 허용 테스트·영수증/서명 검증 runner, 정식 **STATIC USD $1/1회 과금 승인**이 실제 기록되어야 함. 비용 예상 초과 또는 불명이면 호출 0. 단지 "원샷으로 묶어"는 유료 호출 승인 아님.
- **GitHub review transport**: 아직 DRAFT/NOT_ACTIVE이므로 실제 승인·검증 경로를 확인하기 전 **REQUEST/READY 발행·서명·리뷰 호출 금지**. C의 SHADOW를 모델 실행 모드로 전환 금지. 준비 중에는 REVIEW_PREP로만 기록.

### E — 정식 독립 리뷰 최대 1회 (모든 게이트 충족 시만)
1. 회사 반출 승인 받은 정확한 v0.2.10 원본 ZIP을 신규 파일명으로 PRIVATE `collab/packages/`에 게시하고, **원격 raw bytes의 SHA-256·size·CRC/경로 검사·commit pin** 재검증. 실패 시 모델 호출 0.
2. 원본 REQUEST V1과 비용·정책·run mode·nonce/expiry·repo numeric ID·fixed commit·logical request identity·기존 Dropbox 처리 중복 여부 확인. commit A 이후 승인자 별도 개인키로 서명된 유효 승인 증거가 필요. READY는 모든 조건이 유효하고 검증된 마지막 단계에만 게시.
3. 별도 독립 reviewer에서 **최대 한 번** 실행. 결과 MD 및 RECEIPT를 `collab/reviews/`, `collab/receipts/`에 게시해 원격 내용·해시·커밋을 재조회. 지적은 GPT가 후속 판정하며 self-test와 독립 리뷰를 구분. reviewer 실행 불확실/게시 실패 시 동일 모델 재호출 금지; `REVIEW_UNCERTAIN` 또는 `NOT_RUN`을 정직하게 보고.
4. 예산 상한 **STATIC $1**은 자동 승인값이 아니라 유효한 별도 승인 후에만 적용. 초과 또는 불명확하면 요청 실행 안 함. 이 인계서 자체는 REQUEST/READY가 아님.

## 3. 최종 통합 산출물과 갱신
- 신규 결과 파일(이전 결과 **덮어쓰기 금지**): `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CLAUDE_C_SHADOW_AND_E_REVIEW_ONE_SHOT_RESULT_FOR_GPT_20261112.md`.
- 필수 필드: `C_REAL_GITHUB_SHADOW`, `B_OPERATING_SIGNER`, `D_EXPORT_APPROVAL`, `E_INDEPENDENT_REVIEW`, `DEVELOPMENT`, `CUTOVER`, `HOST_PRODUCTION_CHANGED`, `MODEL_CALLS`, `USD_SPEND`; 각 PASS/FAIL/PARTIAL/BLOCKED/NOT_RUN과 HOST_REAL/SYNTHETIC/SELF_TEST_REPORTED 구분.
- 근거: 실제 C 주기와 GitHub GET/write, PID별 운영 main/WAL/SHM·lock 이벤트, 시험계정 종료 상태, D 허가 근거(민감 원문 금지), B trust root 독립성, 서명/요청/영수증·상한과 review 세션 분리 증거, 로컬/원격 ZIP 크기·SHA 및 commit.
- 비민감 결과 MD만 PRIVATE main에 **PR 없이 직접 게시**, commit SHA/remote readback 확인. 실패는 `NOT_POSTED/UNVERIFIED`. 동일 작업 `CURRENT.md` **최상단 단락만 최신 결과 추가, 이전 기록 보존**. 대용량 CLI argument 문제 시 분할된 로컬 임시 파일이나 안전한 파일 기반 API 절차 사용; 권한 거부를 우회하지 않는다.
- 코드 수정이 불가피하면 후보 ZIP 원본 보존 후 별도 버전, 실제 자체 시험 상태를 기록하고 **새 버전 자동 배포/교체 금지**.
- **운영 DB 이행, F1 실제 처분, GitHub LIVE 전환, PUBLIC ZIP 배포, watcher 운영 설치/스케줄 변경은 각 별도 승인 전 전부 NOT_RUN**. `ACTIVE_PROVIDER=DROPBOX LIVE v0.1.5`, `CUTOVER=MIGRATION_NOT_CUTOVER`.

## 4. 사용자에게 필요한 조치(현재 실제 미확보로 보고된 항목)
1. repo 단일 Contents Read-only fine-grained 토큰을 사용자/권한자가 생성해 시험용 비밀 보관처에 설치할 수 있도록 허용해야 C 실GitHub SHADOW 실행 가능(토큰 **채팅 전달 금지**).
2. E를 실행하려면 추가로 **별도 서명자 기기 및 키/공개키 설치 승인**, 34개 유래 파일을 포함한 ZIP 반출 승인, 독립 runner/정식 **최대 $1 유료 리뷰 실행 승인**이 필요. 이것들 중 미충족이면 E를 BLOCKED로 기록하고 무호출.
3. 그 외 운영 전환, F1, DB 이행은 해당 결과에 따른 **별도 후속 승인**으로 남긴다.

## 5. Windows Claude Code에 전달할 단일 실행 프롬프트
> GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`의 `main` 브랜치 `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/WINDOWS_C_SHADOW_TO_E_INDEPENDENT_REVIEW_ONE_SHOT_r0001_20261112.md`를 읽고 Stage 1 결과에서 이어서 원샷 실행해줘. 기존 A/합성 C는 재실행하지 말고, C 실제 GitHub read-only SHADOW부터 수행하되 최소 권한 토큰이 없으면 BLOCKED로 기록해. C 후에 B/D/reviewer/과금 승인 게이트를 점검하고 모두 실제 충족한 경우에만 별도 독립 리뷰 E를 1회 이어서 실행해. 승인/권한 없는 키·토큰 생성, ZIP 반출, READY 발행, 유료 리뷰 호출은 금지해. Dropbox LIVE v0.1.5·운영 DB/F1/예약 작업·알림은 변경하지 마. 허용된 단계는 끝까지 진행하고 신규 결과 MD와 CURRENT 갱신분을 PRIVATE main에 PR 없이 게시·원격 readback해. GitHub LIVE 전환은 하지 마.
