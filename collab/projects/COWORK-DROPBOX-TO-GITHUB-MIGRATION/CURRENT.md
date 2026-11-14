# COWORK-DROPBOX-TO-GITHUB-MIGRATION — 현재 상태

## GitHub 단일 LIVE 활성화 완료(호스트 실측): v0.2.20 독립 R1 PASS, B1~B3 적용, ACTIVE_PROVIDER=GITHUB (Claude 호스트 보고, 2026-11-15 KST)
- 결과: `CLAUDE_V0220_R1_AND_GITHUB_LIVE_ACTIVATION_RESULT_FOR_GPT_20261115.md` (PRIVATE `main`, commit `0b0dc5ff24424c835bc2c6a12bbace6cd1af89a0`, 원격 바이트·SHA-256 `89546954852ad1c38bb1be0475a1859861796da4963bf18046fcf0c5e0d476ee` 일치).
- 독립 R1: `REQ-COWORK-V0220-R1-20261115`(POLICY-STATIC-V1), 모델 호출 1, **$0.3769**(상한 $1), **BLOCKING 0**·비차단 1(의도된 `is not None` 가드를 죽은 코드로 지적, 코드 불변). ZIP `6a8626375e5e…`(239432 B) 원격 원시 바이트·CRC 일치, 설치본 바이트 동일. 감시기가 예약·결과·영수증을 자동 게시(결과 `ceff4d145c78`, 영수증 `0f79cd65c9e8`, 예약 `ae7e1213e3b7`, 사용영수증 `3bc7d3a5caa4`).
- B1: 운영 Python 3.11.9에 `cryptography 50.0.2`·`cffi`·`pycparser`만 해시 고정 설치, 운영 인터프리터 674 passed/12 skipped(서명·위조·변조·만료·다른 저장소·핀 불일치 포함). B2: Notifier에 DB 목록+DB별 워터마크(`3bd19b01…`), 비발송 12/12·재기동 후 `last_id 22907` 유지·발송 0. B3: 승인 ZIP 바이트 그대로 `skill-collab-watcher-github`에 설치, 별도 상태 폴더, Task `SKILL-COLLAB-GitHub-Watcher` 단독 기동.
- 실측: `ACTIVE_PROVIDER=GITHUB`, `provider_lease=github` 1행, Dropbox 감시기 Disabled·프로세스 0, 30초 주기 7주기 전부 정상, Stop→Start 재시작 정상, 두 번째 Start 무시(`IgnoreNew`)·두 번째 watch는 잠금으로 종료코드 3, 모델 호출 delta 0(R1 1회 제외), 알림 대상 이벤트 0·Telegram 중복 0 근거(워터마크).
- 보존: 운영 Dropbox DB main/WAL sha256 `4e8bc33a…`/`59de7507…` 작업 전후 동일, pending 1·COMPLETED 60·CONFLICT 1 보존(미이관). 이전 승인 요청 4건은 만료로 재디스패치 불가. 롤백 `rollback_github_live.ps1` 준비(미실행, 격리 리허설 PASS).
- 한계: 신규 유료 요청의 첫 실전 처리 흐름·Telegram 실제 수신·실 CLI 사용량 한도 문자열·별도 계정 SHADOW는 미검증. 다음 정식 서명 REQUEST+READY가 첫 실전 사례.

## 사용자 확정 — v0.2.20 독립 R1 1회($1) 승인·기존 B1~B3 및 GitHub LIVE 승인 유지 (2026-11-15 KST)
- **단일 실행 정본:** [GPT_V0220_R1_APPROVAL_AND_GITHUB_LIVE_ONE_SHOT_r0001_20261115.md](GPT_V0220_R1_APPROVAL_AND_GITHUB_LIVE_ONE_SHOT_r0001_20261115.md), PRIVATE `wonhwipark/CoWork-Skill-Collab`/`main`, commit `ccab1cebb8f0226b94d786ce6ac2b807b9a19efd`, GitHub 원격 readback PASS. 사용자 `진행해 윈샷으로`까지 확인, **동일 승인 재질문 금지**.
- **승인:** v0.2.20 **새 R1 `REQ-COWORK-V0220-R1-20261115` / `POLICY-STATIC-V1` / 최대 $1 / 1회**. 이전 v0.2.19 R2(`$0.9007163`, BLOCKING 1)는 완료·소진, 재호출 금지. B1 Windows 운영 Python `cryptography`, B2 Notifier provider별 워터마크, B3 GitHub watcher 설치/Task + 최종 단일 GitHub LIVE는 **기존 명시 승인 유지**, Classic PAT 정책 그대로.
- **고정 후보(호스트 자체시험 보고):** `skill-collab-watcher_v0_2_20_1115_DEV_NOT_FOR_DEPLOYMENT.zip`, 239432 B, SHA-256 `6a8626375e5e711535abdd261ff48781114802bb345cabe2ed5940b75968f386`, venv `674 PASS / 12 SKIP`·운영 Python `607 PASS / 17 SKIP`. Windows 로컬에만 보관, **원격 ZIP raw-byte SHA/CRC와 독립 리뷰 아직 NOT_RUN**.
- **원샷 Windows 실행 순서:** 로컬/원격 ZIP SHA/크기/CRC·비밀 검사→후보 ZIP+manifest+v0.2.19→20 diff PRIVATE 입력 게시·원격 readback→유효 서명 `REQUEST/READY`(READY 마지막)→독립 R1 **1회** 및 결과·영수증 확인→**리뷰 PASS인 경우에만** 기승인 B1→B2→B3 적용·2주기+재시작 검증→단일 GitHub LIVE. FAIL/불확실 상태는 fail-closed, 유료 재호출 0·원본 데이터 보존.
- **레거시 이력 보존:** Dropbox 운영 DB 완료 60/CONFLICT 1/pending 1 및 main/WAL/SHM, 기존 Task/Notifier/워터마크 변경 시 백업·롤백·중복 알림 0 확인. 미정산 1건 자동 재실행 금지. GitHub LIVE 전환 성공은 **실제 Windows 호스트 Task/Process/Provider 검증** 이후에만 기록.
- **이번 GPT 세션의 사실 상태:** `DOCUMENT_POSTED_AND_READBACK=PASS`; `WINDOWS_R1_MODEL_CALLS=NOT_RUN`; `WINDOWS_B1_B2_B3=NOT_RUN`; `HOST_LIVE_ACTIVATION=NOT_RUN`; **`ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER`** (마지막 호스트 보고 기준). 현재 GitHub 커넥터로 Windows Claude Code 호스트 실행을 직접 시작할 수 없음. **다음 한 동작은 Windows Claude Code에서 위 정본 인계서 1회 실행**. 출력 결과 경로 `CLAUDE_V0220_R1_AND_GITHUB_LIVE_ACTIVATION_RESULT_FOR_GPT_20261115.md`.
- **기존 판정/이력:** 아래 날짜순 근거 원본은 그대로 보존. 이 문서는 REQUEST/READY가 아니며 자동 유료 실행 신호가 아님.

## GPT 공식 판정 — v0.2.19 R2 BLOCKING 수용, v0.2.20 R1 최소 재검토 제안 (2026-11-15 KST)
- **정본 판정:** [GPT_V0219_R2_BLOCKING_DISPOSITION_AND_V0220_REVIEW_PLAN_r0001_20261115.md](GPT_V0219_R2_BLOCKING_DISPOSITION_AND_V0220_REVIEW_PLAN_r0001_20261115.md) (commit `43ad462f30cc7bee7e4e9069912ce06ab6a32d35`, 원격 readback PASS). `GPT_DISPOSITION=ACCEPT_BLOCKING_AND_FIX_PENDING_INDEPENDENT_REVIEW`; `ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER`.
- **GPT 원격 직접 검증:** v0.2.19 reviewer 원문 `collab/reviews/REQ-COWORK-V0219-R2-20261114/REVIEW_RESULT_1.md`, `RECEIPT_1.md`, `USAGE_RECEIPT_1.json`, 호스트 결과 MD를 조회. reviewer 1회(`$0.9007163`, 승인 최대 $3) 완료, 결과 **BLOCKING 1**: 오래 살아 있는 `GitHubTransport.repository_id()` 캐시가 GitHub 저장소 numeric ID 변경 후 N2 검사 우회. 실제 WATCH에서 같은 transport 반복 사용, 독립 reviewer 지적을 GPT 수용. `INDEPENDENT_REVIEW_V0219=FAIL_BLOCKING`.
- **다음 후보 v0.2.20:** Windows Claude Code는 캐시 제거·same transport/2 cycles 회귀 추가 후 venv **674 PASS/12 SKIP**, 운영 Python **607 PASS/17 SKIP** 보고. ZIP `skill-collab-watcher_v0_2_20_1115_DEV_NOT_FOR_DEPLOYMENT.zip`, **239432 B**, sha256 `6a8626375e5e711535abdd261ff48781114802bb345cabe2ed5940b75968f386`, **Windows 로컬 보관·미게시·`INDEPENDENT_REVIEW_V0220=NOT_RUN`**. 수정 자체 시험을 독립 리뷰 PASS로 소급하지 않음.
- **자동 리뷰 파이프라인 진전:** v0.2.19 독립 리뷰 호출 1회, Watcher가 예약/결과/RECEIPT를 실제 PRIVATE에 PUT, 영수증 readback. 별도 `USAGE_RECEIPT`는 개발자 gh 게시로 구분. 추가 유료 재호출 0.
- **LIVE 상태:** B1 운영 `cryptography`, B2 Notifier provider별 워터마크, B3 GitHub watcher 설치·Task 및 단일 LIVE는 reviewer BLOCKING에 따라 **모두 NOT_RUN**, 승인 자체는 **기존 사용자 승인 유지(재질문 금지)**. 기존 Dropbox DB main/WAL 불변, pending 1/완료 60/CONFLICT 1 유지, Telegram 0(호스트 보고).
- **단일 미승인 항목:** v0.2.20의 변경점만 대상으로 신규 독립 **R1 `POLICY-STATIC-V1`, 최대 $1, 정확히 1회** 제안. 예시 ID `REQ-COWORK-V0220-R1-20261115`. **이번 v0.2.19 R2 승인은 사용 완료**, v0.2.20 신규 호출은 명시적 별도 승인 전 `NOT_RUN`. 승인 시 Windows 로컬+PRIVATE 원시 ZIP SHA/CRC 고정→신규 서명 REQUEST/READY→독립 리뷰 1회→PASS일 때 **기승인 B1→B2→B3와 GitHub LIVE** 원샷 재개. 원본·이력·Classic PAT 정책 보존, 변경 승인 재요청 안 함.
- **실제 이번 GPT 세션:** Windows 작업/유료 Claude 호출/운영 변경/LIVE 전환 0; GPT 판정서·CURRENT/TRACKER 기록만 수행. 아래 이전 호스트 결과/승인 역사는 변경 없이 보존.

## v0.2.19 독립 R2 완료: BLOCKING 1건(N2 repo ID 캐시) → 운영 변경 3종·LIVE **미실행**, ACTIVE_PROVIDER=NONE (Claude 자체 보고, 2026-11-15 KST)
- 결과: `CLAUDE_V0219_R2_AND_GITHUB_LIVE_ACTIVATION_RESULT_FOR_GPT_20261115.md` (PRIVATE `main`, commit `39186ffdb301ed398a2beb8c3e2489ba350d2137`, 원격 바이트·SHA-256 `db8fa71e73456c28bf05d58d280768beb2caddbb3849018865af09f1eba49c06` 일치). 승인된 R2 1회만 사용: 모델 호출 1, $0.9007(상한 $3), 27 turns.
- 리뷰: `REQ-COWORK-V0219-R2-20261114`, 대상 ZIP 6e7fee33…(원격 원시 바이트·CRC 재검증 일치). 리뷰어 감시기=v0.2.19 자신, **원격 예약·결과·영수증 PUT 3회 완전 자동**(첫 실전 자동 게시 성공). 결과 `9a151a4233d7`, 영수증 `d4c42710e385`, 예약 `19b6e54ba5af`, 사용영수증 `6247c0c034bc`.
- BLOCKING 1: `repository_id()`가 transport 수명 동안 캐시되어 장기 watch 중 저장소가 바뀌어도 N2 통과 → **합성 재현 후** 후보 v0.2.20에서 캐시 제거. 비차단: GitHub 생성 전용 원자성은 실서버 6 동시 쓰기×4회로 보강 검증(승자 1, 나머지 409/422).
- 후보 `v0.2.20`(`development_not_for_deployment`) 239432 B, sha256 `6a8626375e5e711535abdd261ff48781114802bb345cabe2ed5940b75968f386`, 시험 venv 674/12·운영 인터프리터 607/17, 로컬 보관·미게시, **독립 리뷰 NOT_RUN**(이번 승인은 소진, v0.2.19 결과 소급 불가).
- 미실행(STOP): B1 cryptography 설치, B2 Notifier 워터마크 교체, B3 GitHub watcher Task·LIVE. 운영 DB main/WAL 해시·Task 상태 불변, pending/완료 이력 보존, Telegram 0. B1 격리 리허설(임시 venv, 해시 고정 설치·Ed25519 확인)은 PASS.
- 다음: v0.2.20 새 독립 리뷰 승인(소규모 diff 리뷰 권고는 GPT 판단) 후, B 승인이 유효함을 명시하면 B1→B2→B3 재개.

## 사용자 A+B 통합 명시 승인 — v0.2.19 독립 R2 $3 + Windows 운영 변경 3종 + 단일 GitHub LIVE (2026-11-15 KST)
- **승인 확정:** 사용자 문구 `A안 v0.2.19 독립 R2 리뷰 1회(최대 $3)와 B안 Windows 운영 변경 3종을 모두 승인해. 기존 GitHub LIVE 전환 승인 유지. 필수 검증 통과 후 원샷으로 전환해줘.` 이번 승인에 따라 더 이상의 **동일 승인 재질문 금지**. `PAID_REVIEW_APPROVED=YES`; `OPERATING_CHANGES_APPROVED=YES`; `LIVE_CUTOVER_APPROVED=YES`. Classic PAT 지속 사용 결정 유지.
- **승인·실행 정본:** [GPT_V0219_R2_AND_GITHUB_LIVE_ACTIVATION_APPROVAL_AND_ONE_SHOT_r0001_20261115.md](GPT_V0219_R2_AND_GITHUB_LIVE_ACTIVATION_APPROVAL_AND_ONE_SHOT_r0001_20261115.md), commit `16a4406d623dc1d74b8c2786ed54304d6733534d`, GitHub remote readback PASS. Windows 실행/서명/READY·실 리뷰·설치 자체는 **이 GitHub 문서 게시만으로 자동 시작하지 않는다**.
- **A 대상 고정:** 새 요청 `REQ-COWORK-V0219-R2-20261114`, ZIP `skill-collab-watcher_v0_2_19_1114_DEV_NOT_FOR_DEPLOYMENT.zip`, 보고 크기 239143 B / sha256 `6e7fee3340cc6d0282d1c18fe3db42a90360259dd73fa6d7c0a7698af7afe5c0`. `POLICY-STATIC-V1-LARGE`, 정확히 1회/최대 $3. 실제 Windows에서 **raw bytes SHA/ZIP CRC/manifest/commit 재검증 후** 유효 승인 서명 및 `READY`를 마지막에 게시하고 개발과 분리된 독립 리뷰 실행. 리뷰 BLOCKING/모호한 호출 상태에서 유료 재실행 금지.
- **B 운영 승인 세 가지:** B1 Windows 운영 Python 3.11.9 `cryptography` 고정 의존성 설치 및 실제 Ed25519 검증, B2 기존 Notifier의 provider별 상태 DB/워터마크 개선 설치와 비발송·재시작·중복/누락 0 시험, B3 **리뷰 PASS를 통과한 동일 ZIP**의 별도 GitHub watcher 상태/config/Task 설치와 기존 Dropbox watcher disabled 유지·단일 GitHub LIVE 전환/2주기+재시작/롤백 검사. 기존 레거시 pending 1건과 완료 60·CONFLICT 1은 무손실 보존; 운영 DB 덮어쓰기·임의 재리뷰 금지.
- **현재 실제 상태(이번 GPT 세션):** `HANDOFF_POSTED=PASS`; `WINDOWS_HOST_EXECUTION=NOT_RUN`; `V0219_INDEPENDENT_REVIEW=NOT_RUN`; `R2_MODEL_CALLS_DELTA=0`; `OPERATING_APPLIED=NOT_RUN`; `ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER`. 사용자가 승인한 전환 계획과 호스트에서 검증된 완료 상태는 분리해 기록.
- **다음 한 동작:** Windows Claude Code가 위 정확한 인계서 1회 실행하여 A 리뷰→PASS 시 B1→B2→B3→LIVE를 수행. 결과 경로 `CLAUDE_V0219_R2_AND_GITHUB_LIVE_ACTIVATION_RESULT_FOR_GPT_20261115.md`, CURRENT/TRACKER를 원격 readback 후 GPT 판정. 실패는 `BLOCKED`, 중복 유료 모델 호출 0/기존 운영 데이터 보존. 아래 2026-11-14 이전 판정은 이력으로 유지.

## GPT 정본 판정 — v0.2.19 개발 PASS·LIVE 미전환, 마지막 별도 승인 항목 명시 (2026-11-14 KST)
- **정본:** [GPT_V0219_LIVE_CUTOVER_DISPOSITION_AND_FINAL_APPROVAL_BUNDLE_r0001_20261114.md](GPT_V0219_LIVE_CUTOVER_DISPOSITION_AND_FINAL_APPROVAL_BUNDLE_r0001_20261114.md), commit `66dfbbfaeb8549dc906637031f86c7a517045a92`, 원격 readback PASS. `GPT_DISPOSITION=ACCEPT_PREPARATION_CUTOVER_BLOCKED`; `USER_LIVE_APPROVAL=ALREADY_APPROVED`; `ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER`.
- **근거:** Claude Code 결과 `CLAUDE_GITHUB_LIVE_CUTOVER_EXECUTION_RESULT_FOR_GPT_20261114.md` GitHub blob `bc0c7b3f90c919e31de485182ade6a94f8ecb0b6` 및 manifest 조회. N1 원격 create-only 디스패치 예약을 모델 실행 전 기록하고 소실 시 `REVIEW_UNCERTAIN`으로 차단하는 `v0.2.19` 개발·합성시험 완료 호스트 보고(venv `673 PASS / 12 SKIP`, 운영 Python `606 PASS / 17 SKIP`); 코드 독립 리뷰 아직 `NOT_RUN`.
- **고정 후보:** `skill-collab-watcher_v0_2_19_1114_DEV_NOT_FOR_DEPLOYMENT.zip`, 호스트 보고 **239143 B**, SHA-256 `6e7fee3340cc6d0282d1c18fe3db42a90360259dd73fa6d7c0a7698af7afe5c0`. PRIVATE `review-inputs/REV-COWORK-V0219-20261114/`의 `REVIEW_MANIFEST.md`는 GPT 직접 조회, 실제 ZIP raw-byte SHA/CRC는 GitHub 텍스트 조회 오류로 **GPT NOT_RUN**. 리뷰 실행 전 Windows에서 실바이트 고정 재검증 필요.
- **추가 발견:** 현재 Notifier는 단일 `last_id`여서 GitHub 새 DB로 옮기면 새 알림 누락 위험이 실측됨. provider별 워터마크 후보 비발송 회귀 11건 호스트 보고 PASS, 실제 설치·실알림은 NOT_RUN. 기존 Dropbox pending 1건은 레거시 DB에 무손실 보존되었으나 GitHub로 자동 이관/완료되지 않음.
- **마지막 분리 승인 묶음:** (A) 확정 SHA v0.2.19 독립 Claude R2 1회, `REQ-COWORK-V0219-R2-20261114`, `POLICY-STATIC-V1-LARGE`, **최대 $3** (현재 승인 전/호출 금지) + (B) Windows 운영 변경 세 가지(운영 Python `cryptography` 설치·실검증, Notifier provider별 watermark 후보 설치, GitHub watcher 별도 상태폴더/Task 설치 및 단일 LIVE 활성화). 사용자는 일반 LIVE 전환을 **이미 승인**했으므로 이 승인만 묶어서 한 번에 받을 수 있음.
- **현재 미실행:** 유료 리뷰 0, 운영 Python/Notifier/Task 변경 0, 실제 LIVE 0. 승인 부재는 `BLOCKED`로 유지. Classic PAT 기본 인증은 확정이며 관련 재논의 불필요. `ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER`. 과거 기록 아래 보존.

## GitHub LIVE 컷오버: 게이트 3개 BLOCKED로 **미전환**(ACTIVE_PROVIDER=NONE), N1 잔여 갭은 후보 v0.2.19로 수정 (Claude 자체 보고, 2026-11-14 KST)
- 결과: `CLAUDE_GITHUB_LIVE_CUTOVER_EXECUTION_RESULT_FOR_GPT_20261114.md` (PRIVATE `main`, commit `ed007279b1fd56af24969c86817271adc2640c48`, 원격 바이트·SHA-256 `7c5295c7ec5511ef19c8b78cbe245274e33b34094fe68687e8efe0b79d93b26c` 일치). 사용자 LIVE 승인 반영·재질문 0. 모델 호출 0, 비용 $0, 운영 변경 0.
- N1 잔여 갭(모델 호출 후 업로드 전 로컬 DB/결과 소실 시 2차 유료 호출) 재현 후 수정: 모델 시작 직전 원격 `dispatch/<요청ID>/DISPATCH_<rev>.md` 생성 전용 예약. 크래시 7지점×상태 유지/소실, 구 백업 복원, 예약 불가/타인 기록 19개 시험 통과(v0.2.18에서는 12개 실패). 원격 쓰기가 안 되면 유료 리뷰가 시작되지 않는 동작 변화.
- 후보 `v0.2.19`(`development_not_for_deployment`) 239143 B, sha256 `6e7fee3340cc6d0282d1c18fe3db42a90360259dd73fa6d7c0a7698af7afe5c0`, 시험 venv 673/12·운영 인터프리터 606/17, 재빌드 바이트 동일, 비밀 스캔 0. 입력(ZIP·매니페스트·diff)만 `review-inputs/REV-COWORK-V0219-20261114/`에 게시(요청·READY 없음). **독립 리뷰 NOT_RUN**.
- 차단 사유: ① v0.2.19 독립 리뷰 미승인(BLOCKED_PAID_REVIEW_APPROVAL), ② 운영 인터프리터 cryptography 없음·설치 미승인(BLOCKED_OPERATIONAL_APPROVAL), ③ 운영 Notifier 교체와 GitHub watcher Task/설정 설치 미승인.
- Notifier 발견: 현재 Notifier는 DB 1개+`last_id` 1개라 GitHub 새 상태 DB로 바꾸면 새 알림이 조용히 누락됨(재현). DB별 워터마크 후보를 비발송 리허설로 검증(설치 안 함).
- 호스트 기준선: 운영 DB main/WAL 해시 불변, pending 1건·완료 60·CONFLICT 1 보존(GitHub는 새 상태 폴더 사용 → 해당 Dropbox 시절 요청은 재제출 필요), Task 상태 불변(Notifier만 Running), 이번 셸은 관리자 권한.
- 다음 사용자 결정(한 번에): v0.2.19 R2 리뷰 1회(권고 POLICY-STATIC-V1-LARGE, 최대 $3) + 운영 변경 승인 3종. 모두 승인되면 같은 인계로 [리뷰→설치→2주기+재시작 중복 0→전환] 진행.

## 사용자 GitHub LIVE 컷오버 최종 의사 승인 + 조건부 원샷 인계 (2026-11-14 KST)
- **USER_APPROVED_GITHUB_LIVE_CUTOVER=YES**: 사용자 명시 지시 **"전환해줘"**. **다시 동일 LIVE 전환 승인을 묻지 않는다.** 기준: PRIVATE `main` [GPT_GITHUB_LIVE_CUTOVER_USER_APPROVAL_AND_GATED_ONE_SHOT_r0001_20261114.md](GPT_GITHUB_LIVE_CUTOVER_USER_APPROVAL_AND_GATED_ONE_SHOT_r0001_20261114.md), commit `3f967c985f380fa31412cca1334158194e010d36`, 원격 readback PASS.
- **실제 운영 상태 별개:** `LIVE_ACTIVATED=NO`, `HOST_EXECUTION=NOT_RUN`(이번 GPT 세션), `ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER`. 이 문서 게시만으로 Windows watcher/Task/리뷰 시작되지 않음.
- **원샷 작업:** Windows Claude Code는 (1) N1 디스패치 후 결과 업로드 전 DB/결과 소실 시 중복 유료 호출 0을 fail-closed로 입증하는 최소 수정·합성시험 (2) 최종 ZIP/실제 해시/CRC 고정 및 별도 독립 리뷰 상태 (3) 운영 `cryptography` 검증 (4) 기존 pending 1건/Notifier provider·워터마크 보존/단일 LIVE·롤백을 확인. 현재 v0.2.18은 `development_not_for_deployment`·독립 리뷰 NOT_RUN, 전환 대상 아님.
- **조건부 전환:** 모든 필수 게이트 PASS와 운영 변경에 필요한 각 승인 확인 후 단일 GitHub LIVE 활성화 및 원격 영수증/상태/알림 중복 0 실측. 미승인 추가 유료 리뷰, 운영 DB 이행, Task/Notifier 설정 변경·crypto 설치·PUBLIC 게시 등은 **임의 실행 금지**. 미해결 시 `BLOCKED`로 분리·기존 provider NONE과 원본 불변 유지. 서명된 REQUEST/READY와 모델 비용 방어 우회 금지.
- **사용자 확정 Classic PAT 지속 사용**. 유형 교체/만료 관련 일반 논의·신규 발급 요구 반복 금지.
- **NEXT_ONE_ACTION:** Windows Claude Code가 위 **정확한 인계서**를 1회 실행하여 개발·시험·허용된 준비/게시 완료 후 결과 `CLAUDE_GITHUB_LIVE_CUTOVER_EXECUTION_RESULT_FOR_GPT_20261114.md` 및 CURRENT/TRACKER 원격 readback을 남김. 그때 실제 LIVE 여부를 보고. 과거 기록은 아래 유지.

## GPT 공식 판정 — Classic PAT 쓰기 E2E PASS(격리), v0.2.18 독립 리뷰 전 보완 필요 (2026-11-14 KST)
- **정본:** [GPT_CLASSIC_PAT_E2E_AND_V0218_DISPOSITION_r0001_20261114.md](GPT_CLASSIC_PAT_E2E_AND_V0218_DISPOSITION_r0001_20261114.md), commit `b04ff327a819edea802bb0a25eaedb906494abc5` / remote readback PASS. `GPT_DISPOSITION=ACCEPT_WITH_CHANGE`, `LIVE_READY=NO`, `ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER`.
- **실제 원격 증거:** `CLAUDE_CLASSIC_PAT_GITHUB_WRITE_E2E_AND_LIVE_PREFLIGHT_RESULT_FOR_GPT_20261114.md` (commit `53d2abf12623f19169ed0bc5346e7f4a08a2ce2f`, Git blob `c0a6061eb13215076d612aed0577e78bd8923e56`), 최신 CURRENT/TRACKER 대조. Windows에서 Classic PAT GitHub 임시브랜치 create/update/readback·clean-up 및 Watcher `UPLOAD_PENDING→COMPLETED` PUT 2회, 멱등·충돌 fail-closed·모델 호출 0·운영 DB 불변 **호스트 보고 PASS**. GPT가 Windows 실행을 직접 재시험하거나 삭제된 임시 브랜치 로그를 독립 검증한 것은 아님.
- **개발 후보:** `v0.2.18` N1(원격 리뷰 결과 존재 가드)·N2(원격 숫자 repo ID 확인)·S1/S2 수정·Q8 합성 회귀 `SELF_TEST_REPORTED`. venv **653 PASS/12 SKIP**, 운영 Python **587 PASS/17 SKIP**, Ed25519 68 PASS 보고. ZIP `skill-collab-watcher_v0_2_18_1114_DEV_NOT_FOR_DEPLOYMENT.zip`, **235650 B**, SHA-256 `519c70e3eabbe9722621afa5bf6365b93d99803c76fee2fe078722a0835522cd`는 **로컬 보관/미게시·독립 리뷰 NOT_RUN**, 기존 v0.2.17 R2 PASS 승계 금지.
- **중요 잔여 결함 N1:** 원격 리뷰 결과/영수증이 생긴 **후** 로컬 DB 소실은 가드하지만, 이미 유료 호출됐으나 원격 업로드 **전** DB·결과 소실에서는 외부 이력이 없어 중복 유료 실행 가능. 원격 조회-디스패치 경합도 종합 확인 필요. `N1_LIVE_INVARIANT=NOT_PROVEN`, LIVE 전 영속 디스패치 이력/불확실 상태 fail-closed/재발 방지 합성시험 필요.
- **Notifier 판정 정정:** 2개 `notify_reviews.py` 프로세스는 **venv launcher 부모 + Python 자식**이고 별도 중복 Notifier가 아님. 잠금/워터마크 실측으로 중복 전송 경로 우려 감소. 다만 GitHub Notifier 경로/워터마크 이행과 실제 알림은 NOT_RUN, 운영 변경 미승인.
- **남은 LIVE 게이트:** 최종 N1·N2 포함 수정본의 독립 리뷰(별도 유료 승인 필요), 운영 Python cryptography 실서명 시험/설치(별도 승인), GitHub Notifier 이행·pending 1건 무손실, SHADOW 격리/롤백, 최종 사용자 LIVE 승인. 기존 Classic PAT 계속 사용 확정, 종류/교체 관련 논의 반복 금지.
- **NEXT_ONE_ACTION:** Windows Claude Code가 격리 후보에서 **N1 pre-publish 상태 소실 중복 호출 0** 증거 확보를 위한 최소 추가 보완·합성시험→최종 ZIP/diff/manifest 고정·PRIVATE 업로드/원격 SHA 확인(민감정보 제외). **추가 유료 독립 리뷰·운영 변경·LIVE 실행은 현재 승인하지 않음**. 과거 내용은 아래에 시점별 이력으로 보존.

## Classic PAT 실제 GitHub 쓰기·감시기 자동 게시 E2E PASS, N1/N2는 격리 후보 v0.2.18에서 수정 (Claude 자체 보고, 2026-11-14 KST)
- 결과: `CLAUDE_CLASSIC_PAT_GITHUB_WRITE_E2E_AND_LIVE_PREFLIGHT_RESULT_FOR_GPT_20261114.md` (PRIVATE `main`, commit `53d2abf12623f19169ed0bc5346e7f4a08a2ce2f`, 원격 바이트·SHA-256 `8d447920ee4246dd096ad031f38919f317271856223adbaaebe7c9d7f35a5d1e` 일치).
- 인증: 사용자 확정 기본 인증인 기존 Classic PAT 사용(값·접두·길이 비게시). 서버 repo ID `1451933830`=신뢰 루트 라벨. 임시 브랜치에서 create→readback→update→readback PASS, 임시 브랜치 2개 모두 삭제 확인. `main`·기존 REQUEST/READY/결과/영수증 불변.
- 감시기 E2E(실제 GitHub, 임시 브랜치, 모델 호출 0): `UPLOAD_PENDING`→`COMPLETED`(PUT 2), 재실행·재시작 쓰기 0, 이미 게시됨 readback 정산, 원격 내용 충돌은 `CONFLICT` fail-closed·덮어쓰기 0. 운영 DB main/WAL 해시 불변, Task 상태 불변, Telegram 0.
- 후보 v0.2.18(`development_not_for_deployment`, 235650 B, sha256 `519c70e3eabbe9722621afa5bf6365b93d99803c76fee2fe078722a0835522cd`, 로컬 보관·미게시·**독립 리뷰 NOT_RUN**): N1 재현(상태 소실 후 2차 호출)→원격 결과 가드, N2 서버 숫자 ID 결합(fail-closed), S1/S2 적용. 시험 venv 653 passed/12 skipped, 운영 인터프리터 587/17. v0.2.17 리뷰 PASS를 소급 적용하지 않음.
- Q8 복합 합성: v0.2.17은 상태 소실 단계 전까지 통과(N1과 동일 원인), v0.2.18 전 단계 통과; 실제 CLI 한도 메시지는 NOT_VERIFIED. 실서명 시험 68개 PASS. 운영 인터프리터 `cryptography` 없음(fail-closed)·별도 계정 SHADOW는 NOT_RUN.
- 정정: Notifier `--watch` 2개는 독립 인스턴스가 아니라 venv 런처(부모)+기본 인터프리터(자식) 쌍. 단일 인스턴스 잠금·워터마크 있어 중복 전송 경로 가능성 낮음. 변경 0.
- 미실행/미승인: 기존 리뷰 재실행·추가 유료 호출, 운영 DB·Task·Notifier 변경, 운영 cryptography 설치, PUBLIC 배포, LIVE. ACTIVE_PROVIDER=NONE.

## Classic PAT 실제 GitHub 쓰기 E2E + LIVE 준비 검증 원샷 인계 (2026-11-14 KST)
- **사용자 승인 방향:** 개인 CoWork에서 기존 Classic PAT를 계속 사용. 일반적 PAT 종류/교체 논의 반복 금지. PRIVATE `main`에 [GPT_CLASSIC_PAT_REAL_WRITE_AND_LIVE_PREFLIGHT_ONE_SHOT_r0001_20261114.md](GPT_CLASSIC_PAT_REAL_WRITE_AND_LIVE_PREFLIGHT_ONE_SHOT_r0001_20261114.md) (commit `59cf229fe38a2f1191fb1e39bec7cc60e1a14c20`, remote readback PASS) 게시.
- **지금 할 일:** Windows Claude Code가 기존 토큰으로 GitHub `CoWork-Skill-Collab`의 **격리 임시 브랜치**에서 실제 write→GET readback→정리, 모델 실행 없는 watcher `RESULT_SAVED/UPLOAD_PENDING/COMPLETED` 초기 자동 게시 E2E·멱등·충돌 fail-closed 시험. 기존 R2 유료 리뷰 재호출 **0**, 기존 REVIEW/RECEIPT 불변.
- **추가 가능 범위:** 격리 환경에서 N1(중복 재실행), N2(원격 repo ID), Q8 복합 시나리오를 synthetic 회귀·필요 최소 코드 보완으로 묶어 검증, 운영 `cryptography`는 설치 없이 격리 venv 검증, Notifier 두 프로세스는 읽기 전용 관계 분석만. 새 후보 발생 시 개발용 `v0.2.18`과 자체시험/독립 리뷰 상태 구분. 운영 DB/WAL/SHM·Task·Notifier/실 알림 변경, 추가 유료 리뷰, PUBLIC 배포는 **미승인**.
- **현재 이 세션 실측:** `CLASSIC_PAT_POLICY=USER_APPROVED`, `WINDOWS_CLASSIC_WRITE_PROBE=NOT_RUN`, `WATCHER_NEW_UPLOAD_E2E=NOT_RUN`, `HOST_CODE_FIX=NOT_RUN`, `MODEL_CALL_DELTA=0`(이번 GPT 세션), `HANDOFF_POSTED_AND_READBACK=PASS`.
- **최종 LIVE:** `ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER`. 실제 Windows 시험 결과 판정 후에도 GitHub LIVE 전환은 별도 사용자 승인. 이전 Claude/ GPT 기록은 아래 순서대로 보존.

## 사용자 확정 결정 — 기존 Classic PAT 계속 사용 (2026-11-14 KST)
- **USER_DECISION=CLASSIC_PAT_ACCEPTED_FOR_COWORK**: 개인 CoWork 용도로 기존 Classic PAT를 지속 사용. 앞선 fine-grained 토큰 필수·재발급·만료 조건 요구는 **이번 사용자 결정으로 대체**.
- **NO_REPEAT_DISCUSSION**: 향후 일반적인 PAT 종류 비교·관련 우려 및 교체 권고를 다시 제기하지 않는다. 사용자가 명시적으로 재검토를 요청하는 경우에만 재논의.
- **NEXT_ONE_ACTION**: Windows Claude Code에서 기존 Classic 자격을 사용해 CoWork GitHub 연결·격리 쓰기·readback을 실제 검증하고 비민감 결과만 보고. 미실행 동작은 PASS로 표시하지 않음.
- **운영 단계 분리**: 이 결정이 추가 유료 독립 리뷰, 운영 DB/Task/Notifier 변경, GitHub LIVE 전환까지 승인하는 것은 아님. `ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER`. 아래 과거 판정의 토큰 유형 미충족 문구는 작성 시점 기준 기록으로 보존하되 최신 결정을 우선한다.

## GPT 공식 판정 — 기존 PAT 2종 부적격, 격리 publish-only PASS (2026-11-14 KST)
- **정본 판정:** [GPT_EXISTING_PAT_VALIDATION_DISPOSITION_r0001_20261114.md](GPT_EXISTING_PAT_VALIDATION_DISPOSITION_r0001_20261114.md) (commit `2ab9746da6db86d996c8af4e4b88bfeff063669a`, GitHub readback PASS). `GPT_DISPOSITION=ACCEPT_WITH_CHANGE`; `PAT_ELIGIBILITY=FAIL_CHECKED_2`; `WRITE_PROBE=NOT_RUN`; `PUBLISH_ONLY_ISOLATED=PASS_REPORTED`; `REVIEW_MODEL_CALL_DELTA=0_REPORTED`; `ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER`.
- **실제 확인 범위:** Claude Code 결과 `CLAUDE_EXISTING_PAT_VALIDATION_AND_PUBLISH_ONLY_RESULT_FOR_GPT_20261114.md`(commit `78a489b6ea39f53b334e1e76cc4c185b8860cc49`)를 GPT가 원격 조회. Windows 감시기 자격 폴더 JSON **2개만** 검사. fine-grained read-only/만료 없음 + classic broad/무기한으로 두 개 모두 부적격. 사용자 보유 **별도 PAT는 Windows 다른 계정/자격 관리자/PC/브라우저에 있을 수 있어 '없음' 단정 금지**.
- **정산 결과:** 기게시 R2 결과·영수증 3개 원격/로컬 바이트 동일 보고. 격리 원장에서 `UPLOAD_PENDING→COMPLETED`, HTTP GET 14·모델/쓰기/Telegram 0, 원본 원장 불변(호스트 자체 보고). **실제 엔진 최초 업로드 write E2E 미실행**, 운영 원장 정산·운영 변경 미실행.
- **다음 한 동작:** 사용자가 이미 보유한 별도 적격 fine-grained Contents R/W, CoWork 단일 PRIVATE repo, 만료 ≤90일 PAT를 Windows 보호된 숨김 입력으로 제공/설치할 수 있는지 확인. 조건 충족 시 재발급 없이 테스트용 임시 브랜치 write/readback/cleanup. 조건 미충족일 경우에만 신규 발급 또는 scope/expiry 보완을 요청, 비밀 절대 GitHub/채팅에 게시하지 않음.
- **남은 LIVE 차단:** 운영 `cryptography` 미설치, Notifier 프로세스 2개·GitHub 미연동, N1 nonce/DB 유실 replay, N2 runtime repo ID 결합, 별도 계정 SHADOW·복합 E2E·pending 1건 보존. 추가 유료 리뷰, 운영 DB·Task·Notifier 변경, 실제 LIVE 최종 전환 미승인.
- **이력:** 아래 Claude 자체 결과와 과거 승인·판정은 시점별 근거로 그대로 보존하며 본 판정을 최신 정본으로 우선 적용.

## 기존 PAT 검증 + R2 publish-only: 적격 PAT 없음(ACTION_REQUIRED_TOKEN_SCOPE_OR_EXPIRY), R2 결과 정리 PASS·모델 호출 0 (Claude 자체 보고, 2026-11-14 KST)
- 결과: `CLAUDE_EXISTING_PAT_VALIDATION_AND_PUBLISH_ONLY_RESULT_FOR_GPT_20261114.md` (PRIVATE `main`, commit `78a489b6ea39f53b334e1e76cc4c185b8860cc49`, 원격 바이트·SHA-256 `cb995f6c6acb418b30f703ba9948911f732340c931ffe65abb29c8a776b27a51` 일치).
- PAT: 이 PC의 후보 2개를 서버 응답 기준으로 검사(값·접두·길이 비게시). 후보1=fine-grained·비공개 1개만이지만 만료 없음(읽기 전용), 후보2=classic·광역·무기한 → **둘 다 부적격**, 적격 0. 따라서 설치·임시 브랜치 쓰기 시험은 NOT_RUN(부적격 토큰 미사용, 쓰기 호출 0). 서버가 반환한 repo 숫자 ID는 신뢰 루트 라벨과 일치하나 제품 runtime repo_id 결합은 별도 게이트(N2) 유지.
- 사용자 조치: 이미 보유한 PAT가 조건(fine-grained, `CoWork-Skill-Collab` 단일, Contents R/W, 만료 90일 이하)을 충족하면 `Install-EngineWriteToken.ps1`로 숨김 입력 설치(채팅 붙여넣기 금지), 아니면 해당 조건으로 신규 발급.
- R2 publish-only: 원격 결과·영수증 3개가 로컬 보관본과 **바이트 동일**(ALREADY_PUBLISHED). 격리 원장 사본에서 `UPLOAD_PENDING`→`COMPLETED`(GET 14회뿐, 쓰기 0, 하위 프로세스 0, 원본 원장 불변). 모델 호출 delta 0, 신규 유료 리뷰 0, 알림 0.
- 미실행/미승인: 운영 DB·Task·Notifier 변경, 추가 유료 리뷰, cryptography 운영 설치, LIVE. ACTIVE_PROVIDER=NONE.

## 기존 PAT 검증·publish-only 사용자 실행 지시 및 Windows 원샷 인계 (2026-11-14 KST)
- 사용자 "pat 이미 있어" 이후 "그래진행하자"에 따라, **재발급 선행 요구 폐기 / 기존 보유 PAT의 적합성 검증 우선** 실행 방향 확정. PRIVATE `main` 인계: [GPT_EXISTING_PAT_VERIFY_AND_PUBLISH_ONLY_ONE_SHOT_r0001_20261114.md](GPT_EXISTING_PAT_VERIFY_AND_PUBLISH_ONLY_ONE_SHOT_r0001_20261114.md), commit `de67235b03052baffe4938c98b1a7ab0d038b528`, 원격 readback PASS.
- Windows Claude Code가 로컬 기존 토큰(이전 검사에서 본 read-only fine-grained 또는 classic 이외 별도 PAT 가능)을 **비밀 비노출·실서버 scope/만료/저장소 제한 검증**. 적격 `wonhwipark/CoWork-Skill-Collab` 단일 repo fine-grained Contents R/W + 만료 ≤90일 토큰이 있으면 재발급 불필요. 사용자 인증 조치가 필요할 때만 `ACTION_REQUIRED_TOKEN_SCOPE_OR_EXPIRY`.
- 적격 시 기존 로컬 설치 도구 점검→Windows 보호 설치(운영 watcher Task/계정/DB 불변)→격리 GitHub 임시 브랜치에서 write/readback/cleanup→이미 원격 게시된 `REQ-COWORK-V0217-R2-20261114` 리뷰·영수증의 **동일 바이트/idempotent publish-only 상태 정산**. **모델 호출 신규 0, 중복 게시/덮어쓰기 0**을 확인해야 함.
- **이 세션의 실제 Windows 실행 상태:** `PAT_ELIGIBILITY=NOT_VERIFIED`, `HOST_INSTALL=NOT_RUN`, `WRITE_PROBE=NOT_RUN`, `PUBLISH_ONLY_RECONCILE=NOT_RUN`, `WINDOWS_HANDOFF=POSTED`. 이 GitHub 문서 작성만으로 Windows Claude Code/감시기/유료 리뷰가 자동 시작하지 않음.
- v0.2.17 R2 정적 리뷰 PASS_WITH_FINDINGS, SHADOW 부분 PASS, DB 백업/격리 복구 호스트 보고 유지. 남은 운영 `cryptography`, Notifier 중복, N1/N2, 복합 시험, 미정산 요청 및 최종 LIVE 승인 별개. `ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER`. 기존 보고의 "새 PAT 필요"는 당시 호스트가 검출한 자격의 부적합 진술이며 최신 사용자 보유 PAT에 대한 실측은 아님. 이전 이력은 아래 보존.

## 사용자 확인 — PAT 이미 보유 (2026-11-14 KST, 후속 정정)
- **사용자 확인:** "pat 이미 있어". GPT는 이전의 **'새 PAT를 반드시 생성해야 함' 안내를 정정**하고, **기존 PAT 검증을 우선**한다. `PAT_EXISTENCE=USER_REPORTED`, `PAT_ELIGIBILITY=NOT_VERIFIED`, `ENGINE_WRITE_TOKEN_INSTALLED=NOT_VERIFIED`.
- **호스트 이전 관찰과 구분:** 2026-11-14 Claude B 결과에선 감시기 read-only fine-grained PAT와 classic/무기한 쓰기 토큰만 관측됐으므로, 사용자 보유 토큰이 **동일한 토큰인지 / 별도 fine-grained 쓰기 PAT인지 / 현재 권한·만료·스코프가 충족되는지**를 Windows에서 값 비노출 검증할 것. 기존 토큰이 PRIVATE 단일 repo `wonhwipark/CoWork-Skill-Collab` Contents Read/Write, 허용 만료, 안전 로컬 보관 조건을 만족하면 **새 발급 불필요**. 기존 classic 광역 토큰을 조건 검증 없이 엔진에 쓰거나 새 발급을 강요하지 말 것.
- **다음 한 동작:** Windows Claude Code는 기존 PAT에 대해 비밀 내용·접두·경로를 출력하지 않는 로컬 권한/범위/만료 검증 → 조건 PASS 시 기존 `Install-EngineWriteToken.ps1`, `verify_engine_write_token.py --live`로 안전 설치 및 격리 원격 쓰기 프로브 → 이미 수행한 `REQ-COWORK-V0217-R2-20261114`의 `UPLOAD_PENDING`에 대해 **publish-only 재게시/재조회**(모델 추가 호출 0). 조건 FAIL이면 `ACTION_REQUIRED_TOKEN_SCOPE_OR_EXPIRY`로 정확한 차이만 보고.
- **기타 불변:** 운영 `cryptography` 미설치, Notifier 중복/연동, N1/N2·복합 E2E·SHADOW 격리는 별도 게이트. 추가 유료 리뷰, R0~R3 상시 정책, 운영 Task/DB/Notifier 변경, LIVE 활성화는 승인된 것으로 해석하지 않음. `ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER`.
- **이력:** 아래 "새 PAT 발급 필요"는 토큰 적합성 확인 전 작성 당시 보고이며, 우선순위는 본 최상단의 "기존 토큰 검증 우선"으로 정정. 과거 사실과 시험 기록은 삭제하지 않음.

## GPT 공식 판정 — v0.2.17 R2·SHADOW·DB 백업/복구 통합 검토 (2026-11-14 KST)
- **정본 판정:** [GPT_B_R2_SHADOW_DISPOSITION_r0001_20261114.md](GPT_B_R2_SHADOW_DISPOSITION_r0001_20261114.md), commit `cbed319ee4753c34352fc7b3b79ef5ed7f8c9f82`, readback PASS. `GPT_DISPOSITION=ACCEPT_WITH_CHANGE`; `INDEPENDENT_REVIEW_V0217=COMPLETED_PASS_WITH_FINDINGS`(**정적 범위 한정**); `LIVE_READY=NO`, `ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER`.
- **원격 실증:** Claude 결과 MD, `collab/reviews/REQ-COWORK-V0217-R2-20261114/REVIEW_RESULT_1.md`, `collab/receipts/REQ-COWORK-V0217-R2-20261114/{RECEIPT_1.md,USAGE_RECEIPT_1.json}`, REVIEW_MANIFEST 원격 조회. 모델 1회, $0.9945836≤$3, 23 turns/출력18029 (R2 토큰·턴 목표 미충족). R2 BLOCKING 0, N1/N2/N3/S1/S2 확인. 호스트 시험 644/12·578/17은 `SELF_TEST_REPORTED`; 실제 v0.2.17 바이너리 CRC/SHA는 호스트 보고이며 GPT 직접 raw ZIP 비교는 NOT_RUN.
- **추가 LIVE 게이트:** N1 상태 DB 유실 후 승인 nonce 재사용에 따른 중복 유료 리뷰 위험, N2 `repo_id` 로컬 label-only 비교(원격 실제 GitHub repo ID `1451933830`은 라벨과 일치함을 GPT 확인했지만 실행 시 원격 결합 미구현). 동일 repo 고정 신뢰·이력 보존과 동등한 fail-closed 검증이 없으면 LIVE PASS 불가. N3 token `repo` 문자열은 보안 범위 근거가 아니며 실제 fine-grained 권한 검증 필요. Q8 복합 E2E·실 CLI usage-limit 메시지 미실증.
- **원격 자동 게시:** 엔진 PAT read-only→403/`UPLOAD_PENDING`; `gh` 수동 대체 게시 ≠ watcher publish E2E PASS. 쓰기 토큰은 현재 classic/무기한이므로 미사용; **사용자 GitHub UI에서 PRIVATE repo 단일 Contents R/W, 만료 90일 이하 신규 PAT 발급 ACTION_REQUIRED**. 안전한 로컬 설치 도구를 사용하고 비밀 GitHub/채팅 노출 금지.
- **SHADOW/백업:** SHADOW GET only·모델/Telegram/운영 DB write=0 및 원본 DB main/WAL 불변, 격리 백업 복원 무결성 PASS **호스트 자체 보고**. 단 분리 Windows 계정 enforce·네이티브 I/O·장기가동 NOT_RUN, pending_requests=1 무손실 보존/정산 필수.
- **운영 차단:** Python 3.11.9 운영 interpreter에 `cryptography` 없어 승인 검증 불가(실행 fail-closed); 운영 설치 별도 승인 전 불변. Notifier 두 개의 `notify_reviews.py --watch` 동시 실행 관측, 중복 알림 가능성 및 GitHub Notifier 연결 미검증, 운영 Task/Notifier 변경 미승인.
- **다음 한 동작:** 사용자 전용 최소권한 GitHub PAT 생성/Windows 보호 설치. 이어 Windows Claude Code가 원샷으로 엔진 publish-only E2E·운영 runtime 검증 준비·Notifier 중복 원인 읽기 전용 분석·N1/N2 보완안·Q8 격리 회귀시험. 추가 유료 모델 재리뷰/R0~R3 상시 정책/운영 변경/LIVE 최종 전환 **미승인**. 아래 기존 A·B 결과 및 승인 이력은 시점별 기록으로 보존.

## B안/R2/SHADOW 실행 결과: v0.2.17 R2 리뷰 BLOCKING 0건, SHADOW·DB 리허설 PASS, 쓰기 PAT는 ACTION_REQUIRED (Claude 자체 보고, 2026-11-14 KST)
- 결과: `CLAUDE_B_R2_SHADOW_PREFLIGHT_RESULT_FOR_GPT_20261114.md` (PRIVATE `main`, commit `7968e14a3aed3363fd0fa0e5850d20655cb92a4c`, 원격 바이트·SHA-256 `91ee9613583129ca5b68f6d453344a2205597679546d00b2bb11bb787fe6e8fc` 일치).
- 고정 v0.2.17 ZIP 232575 B, sha256 `824f26c4e28fcc804ed1dd3942a34408c54b9091be34ecb1693cc4cb9d46df03`(재빌드 바이트 동일, 비밀 스캔 0, 시험 venv 644 PASS/12 SKIP, 운영 인터프리터 578/17). review-inputs 게시·원격 CRC 확인.
- R2 리뷰 `REQ-COWORK-V0217-R2-20261114`(POLICY-STATIC-V1-LARGE): 모델 호출 1회, $0.9946(상한 $3), 23 turns(목표 5 초과). BLOCKING 0, 비차단 N1(nonce 재사용 방지 저장소 없음, 확인)·N2(repo_id 라벨, 알려진 갭)·N3, 제안 2(데드코드·taskkill 반환값). 엔진 업로드는 읽기전용 토큰이라 403 `UPLOAD_PENDING`, 개발자 `gh`로 동일 바이트 게시(결과 `c2aeee1757d0`). 코드 수정 없음.
- SHADOW(실호스트, 분리 상태 폴더): 모델 0·GitHub GET만·Telegram 0·라이브 DB main/WAL 불변. 별도 계정 enforce·네이티브 추적은 NOT_RUN. 운영 DB는 SQLite로 열지 않고 바이트 복사 → 복사본 무결성 ok, 격리 복구·건수 일치, v0.2.17 호환 확인.
- ACTION_REQUIRED: 쓰기 토큰이 classic(만료 없음)이라 미사용. fine-grained(Contents R/W, 단일 저장소, 90일 이하) 발급은 사용자 웹 UI 조작 필수; 설치 스크립트·검증기 준비(실설치 NOT_RUN). 운영 인터프리터에 cryptography 없음 → 승인 검증 fail-closed 대기. Notifier 프로세스 2개 동시 실행 관측.
- 미실행/미승인: 운영 DB·Task·Notifier 변경, 추가 유료 리뷰, R0~R3 상시 자동화, LIVE. ACTIVE_PROVIDER=NONE.

## 사용자 통합 승인 — B 쓰기 PAT · v0.2.17 R2 1회 · SHADOW/DB 격리 복구 (2026-11-14 KST)
- **USER_APPROVED:** 사용자 "그래 승인해줘"는 GPT 직전 제안의 **3개 항목**에 대한 명시 승인. (1) CoWork PRIVATE 단일 repo 최소권한·만료형 쓰기 PAT 발급/보호 설치·검증 (2) 최종 고정 `v0.2.17` 독립 R2 구조 리뷰 **정확히 1회 / 최대 $3 / POLICY-STATIC-V1-LARGE** (3) 실호스트 **읽기전용 SHADOW** 및 운영 DB **원본 불변 백업·격리 복사본에만 복구 리허설**. GitHub `main` 인계: [GPT_B_R2_SHADOW_APPROVAL_AND_ONE_SHOT_r0001_20261114.md](GPT_B_R2_SHADOW_APPROVAL_AND_ONE_SHOT_r0001_20261114.md) (commit `5cc01a1cc0fe925bf8df0b8a8f0fadc0afc671cd`; remote readback PASS).
- **권한 경계:** 서명/REQUEST/READY의 실행 검증은 별도 필수. 승인 MD 게시만으로 유료 reviewer/Windows watcher가 시작되지 않는다. 실제 PAT 생성에 사용자 GitHub UI 조치가 필요할 수 있고, 비밀값은 PRIVATE에도 게시하지 않음. SHADOW에서는 모델 호출·GitHub 쓰기·운영 DB/main-WAL-SHM 쓰기·Telegram·운영 Task 변경 각각 0. R2 리뷰 실행은 SHADOW와 별도 격리 수행.
- **명시적 미승인:** `R0~R3` 상시 자동 비용 정책, 추가 유료 리뷰/재리뷰, `v0.2.17` 후속 새 ZIP 공개, 기존 운영 DB 복원/이행, 운영 Task/Notifier 변경 및 실 알림, **최종 GitHub LIVE 활성화**. `ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER`.
- **실행 실측:** 이 문서 시점 `APPROVAL_RECORDED / HANDOFF_POSTED`이며 `PAT_CREATED=NOT_VERIFIED`, `R2_MODEL_CALLS=0` (이번 세션), `SHADOW_HOST_TEST=NOT_RUN`, `DB_REHEARSAL=NOT_RUN`, `v0.2.17 ZIP=LOCAL_ONLY_UNREVIEWED`. 호스트 Claude Code 실행/결과 보고 대기. 기존 A안 R1 결과/영수증과 GPT 판정은 아래 보존.
- **NEXT_ONE_ACTION:** Windows Claude Code에 위 PRIVATE `main` 정확 경로 하나를 전달해 승인된 작업을 원샷 수행. 이후 `CLAUDE_B_R2_SHADOW_PREFLIGHT_RESULT_FOR_GPT_20261114.md`·영수증·CURRENT/TRACKER 원격 확인 → GPT 최종 LIVE 가능성 판정 → 별도 사용자 LIVE 승인.

## GPT 공식 판정 — A안 독립 리뷰 검증 및 v0.2.17 LIVE 게이트 (2026-11-14 KST)
- **정본 판정:** [GPT_A_V0214_INDEPENDENT_REVIEW_DISPOSITION_r0001_20261114.md](GPT_A_V0214_INDEPENDENT_REVIEW_DISPOSITION_r0001_20261114.md) · `GPT_DISPOSITION=ACCEPT_WITH_CHANGE` · `INDEPENDENT_REVIEW_V0214=COMPLETED_WITH_BLOCKING_FINDINGS / RELEASE_GATE=FAIL`.
- **원격 실물 확인:** `collab/reviews/REQ-COWORK-V0214-R1-20261114/REVIEW_RESULT_1.md`, `collab/receipts/REQ-COWORK-V0214-R1-20261114/RECEIPT_1.md`, `USAGE_RECEIPT_1.json`, REQUEST 및 READY 본문을 직접 조회. 비용 `$0.9695416`/1 모델 호출/18 turns/출력 21479 토큰 보고. 기존 R1 목표 3 turns/출력 3000 토큰 미충족(비용 상한 이내).
- **지적별 판정:** F1(다른 정책 키 중복 리뷰), F2(scan/watch 상호배제), F3(일일 한도 비원자 예약)는 **LIVE BLOCKING**. F4(scan 크래시 잔류), F5(Windows 프로세스 트리 잔류)는 **MAJOR / LIVE 이전 검증 필수**. 리뷰에서 발견한 5개를 자체 재현·수정한 `v0.2.17`은 `SELF_TEST_REPORTED`(venv 644 PASS/12 SKIP, 운영 578 PASS/17 SKIP), **미게시·미리뷰·원본 바이트 GPT 미검증**.
- **현재 미검증:** 엔진 결과 업로드 `HTTP 403 / UPLOAD_PENDING`이며 개발자 gh 수동 게시만 확인됨. GitHub 실 repo ID 결합, 실호스트 SHADOW, 운영 백업/복구, Notifier 연결, 암호 라이브러리/skip 원인, 수정본 재리뷰 미완료. `ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER`.
- **다음 한 동작/승인:** (1) 감시기 전용 PRIVATE repo 쓰기 PAT (2) `v0.2.17` 신규 R2 독립 구조 리뷰 1회 최대 $3 (3) 실호스트 SHADOW 및 운영 DB 안전 백업·별도 사본 복구 리허설을 **사용자에게 통합 승인 요청**. R0~R3 상시 비용 정책은 **편의 기능, LIVE 필수 선행은 아님**. 세 승인 및 최종 LIVE 승인은 아직 주어지지 않았으며 어떤 실행도 자동 시작하지 않음.
- **이력 보존:** 아래 Claude A안 보고·과거 인계/판정은 작성 당시 기록으로 유지하며 최신 실행판정은 본 최상단과 연결된 GPT 판정서를 우선.

## A안 실행 결과: v0.2.14 R1 독립 리뷰 1회 완료 — 지적 5건, 수정은 격리 후보 v0.2.17 (Claude 자체 보고, 2026-11-14 KST)
- 결과: `CLAUDE_A_APPROVED_V0214_SINGLE_REVIEW_RESULT_FOR_GPT_20261114.md` (PRIVATE `main`, commit `4f5fd04fd74dbacdf853384e18f8d4e9ac626f32`, 원격 바이트·SHA-256 `6e9adee5c350fb2ee7c36512699fd8a6e473cec9b2c95b2f4ae790c609341b19` 일치).
- 서명키: 단일 PC Ed25519, 개인키 scrypt+AES-GCM 암호화·비밀번호는 DPAPI 블롭만, trust_root_independence=warn. 지문 `9c6f650ce89d…`.
- 리뷰: REQ-COWORK-V0214-R1-20261114, POLICY-STATIC-V1, 모델 호출 1회, $0.9695(상한 $1 준수), 18 turns(R1 목표 초과, CLI `--max-turns` 미지원). 엔진 쓰기는 읽기전용 토큰이라 `UPLOAD_PENDING`, 개발자 `gh`로 동일 바이트 게시(commit A `aedddc49bfdc`, B `2ed6dbafe23b`, 결과 `1df4fb8be6a1`).
- 지적 5건 전부 재현(F1은 롤백·커서 유실 조건부) → 후보 v0.2.17 최소 수정, 시험 venv 644 passed/12 skipped, 운영 인터프리터 578/17. v0.2.17은 미리뷰·미게시, 자동 재리뷰 없음. v0.2.14 ZIP 불변.
- 미실행/미승인: 운영 DB·Task, 새 PAT, 추가 유료 리뷰, LIVE. ACTIVE_PROVIDER=NONE. 남은 결정: B안 쓰기 PAT, 재리뷰 1회, R0~R3 상시 정책, SHADOW·백업/복구 실행.

## 사용자 A안 승인 + 리뷰 등급별 토큰 예산 (2026-11-14 KST)
- 사용자 **A안 명시 승인**: 리뷰 대상 `REV-COWORK-V0214-20261114`의 **기존 `POLICY-STATIC-V1` / R1 / 최대 $1 / 독립 Claude 리뷰 정확히 1회**, 동일 Windows PC Ed25519 단일 서명키/신뢰 루트 암호화 보관 및 `trust_root_independence=warn`까지 포함. **이미 승인된 한 건에 재승인 질문하지 말 것**.
- 사용자는 리뷰당 토큰 사용량을 **단순 정합성(R0), 변경/결함(R1), 구조(R2), 심층(R3)** 등급으로 나눠 관리하도록 지시. `collab/ops/CONTRACTS/REVIEW_TIER_TOKEN_BUDGET_V1.md`(commit `e2a98b3dc2e2a3b08f47271c75610cb27d65ced7`; 이후 단일 사전승인 정책 반영 commit `39fdc6c073be9af96e88db38d6a10947f1dbd388`)에서 토큰 목표/최대 turns/기존 비용 정책 매핑을 정의. 정확한 total token HARD CAP 지원 여부는 Windows 실제 CLI 확인 전 **NOT_PROVEN**.
- **승인 정책 재정리**: 사용자 목표는 매 리뷰마다 별도 비용 승인 요청이 아닌 **일회성 상시 정책 승인 → 승인된 Work·등급·요청 수/일일 비용 안에서 자동 실행**. 향후 상시 승인 자체는 아직 받지 않았으므로 기본 유료 리뷰 자동화를 즉시 활성화하지 않음. 승인 밖 새 비용·등급 상향·재리뷰는 예외.
- Windows용 **A안 원샷 인계** `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_A_APPROVED_V0214_SINGLE_REVIEW_AND_TIER_HANDOFF_r0001_20261114.md`를 PRIVATE main에 게시(commit `c221be18275af31962ccf2b417e062fc7248661a`, remote readback PASS). Windows Claude Code에 이 정확한 경로 하나만 전달하면 승인된 키/서명·R1 리뷰/영수증을 기존 계약에 따라 한 작업으로 추진. 권한/전송이 막히면 해당 부분만 BLOCKED, 그 외 작업은 계속.
- **B안**(새 fine-grained PAT/토큰 포맷·폐기), LIVE 전환, 운영 DB/WAL/SHM·Task·Notifier/Bridge 변경, 신규 PUBLIC 릴리스, 추가 유료 리뷰/재리뷰는 미승인. 사용자의 이 발언은 해당 승인으로 확대 해석 금지.
- **현재 실측**: 문서·설계/인계만 GitHub에 게시됨, Windows A안 실제 실행·키 생성/서명·모델 호출/영수증은 이 세션에서 **NOT_RUN**. `INDEPENDENT_REVIEW=PENDING_EXECUTION`(tracker에서는 `PENDING_APPROVAL` 기존 enum 보존 가능), `ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER`.


## GPT v0.2.14 원샷 프리플라이트 종합 판정 (2026-11-14 KST)
- `CLAUDE_GITHUB_LIVE_ONE_SHOT_PREFLIGHT_RESULT_FOR_GPT_20261114.md`(commit `ad411255ce2a6678aa0f47517a7f0f468439230e`), `review-inputs/REV-COWORK-V0214-20261114/REVIEW_MANIFEST.md` 및 실제 diff·`state_store.py`·`orchestrator.py`·`test_try_claim.py` 원격 조회 후 GPT `ACCEPT_WITH_CHANGE`.
- 결함 원인·수정 직접 확인: 같은 processing_key에 2개 `scan`이 모두 무조건 `CLAIMED`로 갱신하며 리뷰를 2회 시작하는 경합을 `StateStore.try_claim`의 SQLite 단일 조건부 UPDATE (CAS)로 수정. 구조적으로 동일 키 1회 예약. E2E 9개×3 PASS, ZIP unpack/venv 제품 666 PASS·13 SKIP 등은 **Claude 자체 보고**로 기록. 실제 독립 리뷰 아님.
- `v0.2.14` CoWork 소스/ZIP·diff·manifest는 PRIVATE review-inputs 게시 및 원격 해시 검증 **호스트 보고 PASS**. GPT는 diff/핵심 코드 직접 읽음; ZIP raw bytes 자체의 독립 해시/CRC/Windows 재시험은 이 세션에서 직접 미검증.
- 독립 리뷰 체크 포인트 최소화: 새 `try_claim`과 `scan/watch`, policy revision 변동의 논리 중복, 동시 서로 다른 key의 daily cost/dispatch ceiling 검사가 `try_claim` 전이라 원자적으로 보호되는지 **리뷰에서 확인**. 아직 미확정 위험 후보로 보며 추가 설계 개발 강제하지 않음.
- **미완료**: `INDEPENDENT_REVIEW=PENDING_APPROVAL`·`MODEL_CALLS=0`·`CREDENTIAL_MINIMUM=BLOCKED`(원문 토큰 형식 vs JSON file; 쓰기용 fine-grained PAT 없음)·운영 DB backup/restore·실 notifier 연결·GitHub 실제 SHADOW·윈도 런타임 crypto 선택 `NOT_RUN`. `ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER`.
- GPT 판정 파일 `GPT_V0214_PREFLIGHT_DISPOSITION_AND_APPROVAL_GATE_r0001_20261114.md` PRIVATE main 게시(commit `212edc7987a4d2b64d4700e4eea8a8374fa1a805`, remote readback PASS).
- **다음 사용자 승인 2개 한 번에**: (A) `REV-COWORK-V0214-20261114`에 대해 `POLICY-STATIC-V1`·effort medium·최대 $1 **실제 독립 리뷰 1회**, **동일 Windows PC에 1개 Ed25519 서명키/신뢰 루트 생성+암호화 보관 및 `trust_root_independence=warn` 간소화 예외**. (B) `CoWork-Skill-Collab` 한 저장소 Contents Read/Write fine-grained PAT 1개 발급·감시기 안전 설치와 토큰 JSON/원문 포맷 정합, 기존 classic 사용처 확인 후 대체. 실제 유료 리뷰/READY/키·토큰 생성은 사용자 승인 전 실행 금지. 별도 PC/로컬 LLM은 불요.
- **LIVE 전환은 다음 별도 게이트**: 독립 리뷰·실 token·host SHADOW·운영 DB/알림·rollback 격리 리허설이 검증된 후 v0.1.5 교체/단일 GitHub LIVE 최종 명시 승인. 이 판정문 게시로 Windows watcher 자동 동작·운영 LIVE 상태 변경 없음.


## GITHUB_LIVE_ONE_SHOT_PREFLIGHT_RESULT: REVIEW_INPUT_UPLOAD=PASS / INTEGRATION=HOST_ISOLATED_PASS / INDEPENDENT_REVIEW=PENDING_APPROVAL / ACTIVE_PROVIDER=NONE (Claude 자체 보고, 2026-11-14 KST)
- 결과: `CLAUDE_GITHUB_LIVE_ONE_SHOT_PREFLIGHT_RESULT_FOR_GPT_20261114.md` (PRIVATE `main`, commit `ad411255ce2a6678aa0f47517a7f0f468439230e`). 자체 시험 보고이며 독립 리뷰·LIVE 가 아니다.
- 결함 1건 수정: 실제 CLI 진입점 2프로세스 동시 `scan` 이 같은 승인 요청에 reviewer 를 2회 시작 → `StateStore.try_claim`(원자적 compare-and-set)으로 수정, 후보 v0.2.14. 진입점 E2E 9개(실제 Ed25519·실제 CLI·네트워크와 `claude` 만 대체) ×3 PASS, 제품 전체 666 passed/13 skipped(원격에서 내려받은 ZIP 을 풀어도 동일).
- 리뷰 입력 게시: `review-inputs/REV-COWORK-V0214-20261114/` ZIP·diff·소스·`REVIEW_MANIFEST.md`, 원격 raw 바이트 SHA-256 일치, 파일별 고정 commit(결과 §5).
- 독립 리뷰: 유효한 실행·비용 승인이 없어 `PENDING_APPROVAL`, `MODEL_CALLS=0`. 막힌 것: 이 PC 에 운영 서명키·신뢰 루트 없음, 감시기용 쓰기 가능 fine-grained 토큰 없음(`CREDENTIAL_MINIMUM=BLOCKED`).
- 다음 한 동작: GPT 판정 후 사용자에게 승인 묶음(리뷰 1회 + 서명 방식 A/B, 쓰기 토큰 1개, 이후 운영 전환)을 한 번에 전달.

## GPT LIVE 직전 원샷 — GitHub 리뷰·감시기 제품 연동·전환 사전검증 (2026-11-14 KST)
- 사용자 요청: **남은 1~3단계(리뷰 자료 게시·Claude 독립 리뷰·CoWork 감시기 실제 제품 경로 격리 시험)를 Windows Claude Code 한 번의 실행으로 준비·진행**. LIVE 전환은 최종 별도 승인.
- PRIVATE main에 유일 실행 인계서 `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_GITHUB_LIVE_ONE_SHOT_REVIEW_INTEGRATION_PREFLIGHT_r0001_20261114.md` 게시(commit `1a414a5282c2adcf62342acf096598c844cba756`; remote readback PASS). 사용자 제공 프롬프트는 이 경로 하나를 지정.
- 실행 순서: (A) 기존 v0.2.13·Windows 상태·기존 이력 확인 → (B) **격리된 실제 watcher 진입점 E2E**, 중복 호출·재시작·영수증·rollback/notification delta 검증, 결함은 동일 작업에서 수정·재시험 → (C) 해당 **최종** CoWork 소스·ZIP PRIVATE review-inputs/<review_id>/ 원격 바이트 SHA·고정 commit 링크 검증 → (D) 해당 정확한 리뷰 대상에 대해 **유효한 별도 비용/모드 승인 있을 때만** 독립 Claude 리뷰 1회, 없으면 `PENDING_APPROVAL` → (E) 최종 LIVE 전환 승인 패킷/rollback 계획과 한 건의 통합 결과 MD 게시·readback.
- 사용자 승인된 **자료 전달**과 **유료 리뷰 실행/READY/LIVE 변경**은 분리. 2번째 서명자 PC/로컬 LLM/ETW 4축/3종 PAT 강제는 일반 CoWork LIVE 사전검증에서 제거, 단 승인된 호출 한도·중복 방지·비밀/회사 코드 미노출·운영 이력 보존·단일 ACTIVE_PROVIDER·rollback 보호 유지.
- 사용자의 회사 업무 PC/설치/Job 실행과 Windows CoWork watcher 시험은 분리. 별도 독립 리뷰 없이 같은 Claude 개발 세션 자체테스트를 `INDEPENDENT_REVIEW=PASS`로 승격하지 않음. ZIP 수정 후 기존 리뷰 PASS도 승계 금지.
- **현재 실측/보고 상태**: 이 원샷은 Windows에 아직 전달·실행/완료된 것이 아님. `HANDOFF=POSTED`, `REVIEW_INPUT_UPLOAD=NOT_RUN`, `INTEGRATION_E2E=NOT_RUN`, `INDEPENDENT_REVIEW=NOT_RUN`, `GITHUB_LIVE=NOT_APPROVED`, `ACTIVE_PROVIDER=NONE`, `MIGRATION_NOT_CUTOVER`. 운영 DB/Task/Notifier/Bridge/PUBLIC 발행은 불변.
- 다음 한 동작: 사용자가 **이 GitHub PRIVATE main 파일 경로**를 Windows Claude Code에 1번 전달하여 허용 작업을 끝까지 수행하게 함. 결과 `CLAUDE_GITHUB_LIVE_ONE_SHOT_PREFLIGHT_RESULT_FOR_GPT_20261114.md`를 GPT가 원격 확인하여 통합 판정 후 실제 남은 승인만 묶어 제시.


## 사용자 승인 — GitHub 링크 기반 CoWork 소스·ZIP 및 L1Work 리뷰 전달 (2026-11-14 KST)
- 사용자가 **CoWork 감시기 자체 소스·ZIP을 기존 Claude 독립 리뷰에 전달하는 것**을 명시 허용. **L1Work의 스킬 ZIP 및 업무 PC용 Handoff MD 리뷰**도 명시 허용. 리뷰 대상은 실제 GitHub에 게시하고 저장소·branch·고정 commit·파일 링크를 Claude에게 전달하는 방식을 기본으로 합의.
- **전송/게시 분류**: `CoWork-Skill-Collab` PRIVATE `review-inputs/<review_id>/`에 CoWork 후보 소스/ZIP·manifest를 게시 가능(내용·민감정보 검증, 실제 bytes SHA·size·commit 원격 readback 조건). `wonhwipark/L1Work` PUBLIC의 **기게시 스킬 ZIP**과 `handoffs/` 문서의 기존 링크를 리뷰 입력으로 사용 가능. 미승인 신규 ZIP을 PUBLIC 루트에 리뷰용으로 먼저 게시하는 것은 별도 공개 배포 승인이므로 금지. 최종 승인 ZIP은 L1Work/main 루트, Handoff MD는 main/handoffs.
- 이전 `D=2 LOCAL_ONLY` 범위는 **사용자가 명시한 CoWork 감시기 자체 코드의 리뷰 전달에 한해서 해소**. 이 승인으로 회사 L1 원본 코드·고객/기밀자료·토큰 등의 외부 게시가 허용되는 것은 아님. Windows Claude PC는 회사 L1 코드에 접근 불가. 기존 로컬 LLM/별도 서명자 PC·4축 격리 의무를 일반 CoWork 리뷰에 반복 요구하지 않음.
- 기준 인계 `GPT_GITHUB_LINK_REVIEW_TRANSPORT_APPROVAL_AND_ONE_SHOT_r0001_20261114.md` PRIVATE main에 게시(commit `4d5c377dece1b0ae79a7505c7d886db18eb4d51d`, 원격 본문 readback PASS). 신규 CoWork 후보 v0.2.13은 **현재 Windows 로컬에만** 있고 GitHub source/ZIP 실제 업로드 `NOT_RUN`. 현 대화에서 원본 파일 바이트가 없어 업로드를 완료했다고 주장할 수 없음.
- **구분**: 자료 업로드/링크 공유 **승인됨**. **유료 모델 리뷰 호출/READY, 기존 운영 감시기·DB·Task·토큰 변경, L1Work PUBLIC 신규 ZIP 배포, GitHub LIVE 전환은 미승인**. 개발 세션 자체시험과 별도 Claude 독립 리뷰의 결과·영수증을 구분. 현재 `INDEPENDENT_REVIEW=NOT_RUN / ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER`.
- 다음 한 동작: Windows Claude Code가 로컬 v0.2.13의 콘텐츠 검증 후 PRIVATE review-inputs에 **실제 source/ZIP 원격 업로드/sha readback + 고정 GitHub 링크·manifest**를 묶어서 준비해 하나의 결과 MD로 보고. 그다음 사용자에게 실제 모델 리뷰 실행 비용·모드 승인만 요청. 이전 온프레미스 리뷰어/2PC/고급 격리 게이트 재요청 금지.


## GPT 재판정 — SU-SIMPLE 이후 구형 6개 LIVE 승인 목록 정리 (2026-11-14 KST)
- 최신 `CLAUDE_SINGLE_USER_LIVE_FASTTRACK_RESULT_FOR_GPT_20261114.md`(commit `b949a1a93363588989a7209387e4ef6b6540387a`)를 재조회. **구형 LOCAL_ONLY/SU-L1 전제의 §7 6개 승인 목록은 최신 사용자의 SU-SIMPLE 기본 협업 요구에 그대로 적용하지 않는다.** 과거 결과는 삭제하지 않고 기준 변경만 기록.
- **1 온프레미스 리뷰어:** 일반 CoWork 독립 리뷰의 필수 조건에서 제외; **기존 Claude 독립 리뷰 경로 우선**. 다만 CoWork watcher 소스·ZIP의 실제 외부 리뷰 전달 범위는 사용자가 확인하기 전 새 전송 실행하지 않음. 개발 세션 자기검토 `INDEPENDENT_REVIEW=NOT_RUN` 유지.
- **2 토큰:** 신규 읽기용 PAT·별도 결과 쓰기 토큰·개발자 `gh` 전면 교체 3종을 한 번에 강제하지 않는다. 기존 개발자 `gh` 로그인과 watcher 실행용 자격을 분리해 실제 요구 권한부터 파악. 최소 권한 권고와 비밀 노출 금지는 유지; 필요한 자격 설치/교체만 별도 승인.
- **3 비관리자 서비스 계정:** LIVE의 무조건 선행요건에서 제외하고 기존 Windows watcher 권한·경로·DB 쓰기 영향을 **실측에 따라 최소 변경**. 운영 Task/ACL/DB 변경은 승인 전 불변.
- **4 SU-L1:** `local_only_contract_r0003`와 `su_l1_policy_r0001`는 로컬 후보로 보존. **제품 통합 `NOT_RUN`**, 사용자가 요구하지 않은 별도 정책/원장으로 교체·활성화하지 않음. 기존 watcher 중복 0·재시작/영수증 기능 재사용 우선.
- **5 리뷰/LIVE:** 유효한 별도 Claude 독립 리뷰는 허용된 코드 범위·모드·비용 승인을 확인한 후 실행. 최종 GitHub LIVE 활성화·구 운영 데이터/알림·복구 영향이 있는 행위는 결과 검증 뒤 사용자 명시 승인 필요. `ACTIVE_PROVIDER=NONE`, `MIGRATION_NOT_CUTOVER`.
- **6 코드 분류:** Windows Claude Code PC는 회사 L1 원본에 접속 불가라는 사실 확인. 회사 코드·고객자료·비밀은 PRIVATE/PUBLIC/외부 모델로 반출 금지. CoWork watcher 자체 코드·합성 시험 코드는 구별하되, 이전 D2 요청을 자동으로 무효화한 것은 아니므로 **전송 범위 한 번의 사용자 확인**이 필요하다.
- 자체시험 재사용: 호스트 보고 v0.2.13 로컬 후보(642 PASS/13 SKIP 시험 venv), 원장 r0003 28 PASS×3, 변이 14/14. GPT 원본 제품 ZIP·r0003 코드는 읽지 못했으며 수치는 `SELF_TEST_REPORTED`로 유지. 이전 기 구현 성과를 버리지 않고 SU-SIMPLE 목표에 유용한 부분만 통합. `SU_SIMPLE=DESIGN_SELECTED`, `REVIEWER_BLOCKER=RECLASSIFIED`, `INDEPENDENT_REVIEW=NOT_RUN`, `GITHUB_LIVE=NOT_APPROVED`.
- 후속 **Windows 원샷 실행은 아직 요청하지 않음**. 다음 실행 시 정확한 PRIVATE repo/main의 최신 SU-SIMPLE 설계를 기준으로 기존 watcher 경로 재사용·최소 통합 delta만 수행. 이전 6개 질문 또는 LOCAL_ONLY 온프레미스 reviewer 필수 가정을 반복하지 않음.


## SU_L1_FASTTRACK_RESULT: LANE_A=FIXED_AND_RETESTED / E=BLOCKED_LOCAL_REVIEWER / DEVELOPMENT_READY_NOT_FOR_DEPLOYMENT / ACTIVE_PROVIDER=NONE (Claude 자체 보고, 2026-11-14 KST)
- 결과: `CLAUDE_SINGLE_USER_LIVE_FASTTRACK_RESULT_FOR_GPT_20261114.md` (PRIVATE `main`, commit `b949a1a93363588989a7209387e4ef6b6540387a`). 자체 시험 보고이며 독립 리뷰가 아니다. LIVE 전환·운영 변경 없음.
- 원장: r0002의 두 위험(동시 2프로세스 중복 수락, 상태 파일 분실 후 replay)을 재현한 뒤 새 `local_only_contract_r0003`으로 수정. SQLite 원장+OS 잠금+앵커, 1회 bootstrap, 분실·과거 사본·손상은 FAIL_CLOSED, 리뷰 1회 예약·UNCERTAIN 봉인. 28 PASS×3, 변이 14/14 검출. 감시기 제품 경로 연결은 `CONTRACT_INTEGRATION=NOT_RUN`.
- SU-L1: 관리자 보호 로컬 정책+OS 사용자+로컬 artifact 커밋먼트, 기능 플래그 기본 OFF, 별도 서명자 PC 불필요. 19개(1 SKIP)·변이 18/18 검출. 제품에 연결되지 않음.
- 후보 v0.2.13은 로컬에만 보존(원시 해시·크기 비게시). 제품 전체 642 passed/13 skipped(시험 venv), 운영 인터프리터 536 passed/19 skipped.
- 막힌 항목: 로컬 독립 리뷰어 없음(`E=BLOCKED_LOCAL_REVIEWER`, `AUTO_REVIEW=NOT_RUN`). 한계: 동일 PC 관리자 침해는 막지 못함, ETW 실 I/O 증거 NOT_PROVEN.
- 게시 범위: 코드·ZIP은 마스터 §4에 따라 게시하지 않았다(로컬 보존). GPT의 소스 정적 검토는 사용자가 코드 게시를 별도 승인해야 가능하다(`NOT_AVAILABLE_TO_GPT`).
- 다음 한 동작: GPT 통합 판정 후 결과 §7의 사용자 승인 묶음(리뷰어 유무, 신규 PAT, 서비스 계정·ACL, SU-L1 정책 활성화, 실제 리뷰·LIVE, 조직 정책 확인)을 사용자에게 한 번에 전달.

## 사용자 보안 간소화 지시 — SU-SIMPLE (2026-11-14 KST)
- 사용자 지시: CoWork 1인 협업에 대해 **별도 서명자 PC·로컬 LLM 의무화·과도한 보안통제**를 기본 협업 조건에서 제거하고, 불필요한 핑퐁을 줄일 것. Windows Claude Code/Watcher PC는 회사 L1 원본 코드에 접근할 수 없음. 모바일은 원격 조작 용도. 업무 PC 소스의 반출 제한은 그대로 존중.
- 설계 원칙 `GPT_COWORK_SINGLE_USER_SIMPLIFIED_COLLAB_RULES_r0001_20261114.md` GitHub PRIVATE main에 게시(commit `68ecc9e23bc4c89103a6f5472f5fdbb1210dcc1b`, remote readback PASS). `ARCHITECTURE=SU-SIMPLE_DESIGN_SELECTED`. 과거 `GPT_SINGLE_USER_LOCAL_ONLY_LIVE_FASTTRACK_MASTER_r0001_20261114.md`의 별도 signer/온프레미스 reviewer/4축 입증/로컬 전용 v2 복잡도는 **일반 CoWork 자동 리뷰의 기본 필수 조건에서 재분류**. 이전 구현·계약·이력은 삭제하거나 임의 우회하지 않음.
- 간소화된 실제 목표: GPT 한 번의 작업 정의 → Windows Claude Code 원샷 개발·자체시험 → **별도 세션/유효 요청의 Claude 독립 리뷰**(CoWork 코드의 외부 모델 전송 허용 조건과 비용 조건을 먼저 확인) → GPT 통합 판정 → `L1Work/main` **루트 최종 ZIP** + `L1Work/main/handoffs/` **업무 PC 인계 프롬프트 MD** → Skill-Updater/Agent는 설치/호스트 실행 영수증 별도. 회사 소스코드·고객자료·비밀은 PRIVATE/PUBLIC 모두 반출 금지.
- 최소 유지: 유효 요청/사용자 승인된 호출·비용, 동일 요청 중복 0·중단 복구, 자격 비밀 미노출, 제품 ZIP 검증, 단일 LIVE·운영 DB/Task 보호. 실제 별도 signer PC·로컬 LLM·서비스 계정/네트워크 격리·4축 ETW 시험은 일반 CoWork 리뷰에 **기본 필수 아님**.
- **중요 경계**: 사용자 발언이 Windows 기기의 회사 코드 접근 불가를 확인한 것이지, CoWork watcher 소스/ZIP 전량의 외부 전송을 명시 승인한 것은 아님. 기존 D2/운영 승인 계약은 실제 적용 전 변경 검토 및 명시적 범위 확인. `CODE_EXPORT=USER_SCOPE_CONFIRMATION_REQUIRED`; `REVIEW_TRANSPORT=REASSESS_LEGACY_CLAUDE_PATH`; `INDEPENDENT_REVIEW=NOT_RUN`; `ACTIVE_PROVIDER=NONE`; `MIGRATION_NOT_CUTOVER`.
- 다음 한 동작: 실제 Windows 실행 인계는 새 SU-SIMPLE 설계 하나를 기준으로 작성, 기존 LOCAl_ONLY/2PC 필수 지침과 병렬로 전달하지 말 것. CoWork 소스의 독립 Claude 리뷰 가능 경로와 운영 minimal gate를 통합 조사한 뒤, 필요 승인만 모아 사용자에게 한 번에 요청. 이번은 **GitHub 문서·상태 갱신만**, 운영 변경/리뷰 호출/LIVE 전환 미실행.


## GPT 단일 사용자 SU-L1 LIVE 최소 핑퐁 원샷 설계 (2026-11-14 KST)
- 사용자는 혼자 Windows Claude Code·Watcher를 운영하고 모바일은 단순 원격 조작 용도임을 확인. **단일 사용자 중심 보안 설계 간소화 + LIVE 목표까지 Claude Code/GPT 왕복 최소화**를 지시. 기존 외부 서명자 PC를 필수 요구하지 않는 별도 `SU-L1 LOCAL_ONLY` 모드를 설계 **후보**로 채택하되 기존 다중 사용자·유료 리뷰 서명 체계는 유지. 로컬 관리자 보호 실행정책, 비관리자 서비스 계정, 비용 0, 코드/ZIP 반출 0, 요청 식별·원자적 원장·재시작 중복 0, 자체 reviewer locality, kill switch 필수. **설계 승인 ≠ 운영 권한 설치·LIVE 승인**.
- GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab` `main`에 **단일 원샷 마스터** `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_SINGLE_USER_LOCAL_ONLY_LIVE_FASTTRACK_MASTER_r0001_20261114.md`를 commit `1fc46533957cb7a8c2eb9677515481d621112660`로 직접 게시, 원격 본문 readback PASS. Windows 실행은 아직 요청 전달 전/관측되지 않음.
- Windows Claude Code는 위 단일 문서로 통합 Lane A~D(로컬 v2 원장 두 운영 결함 해결: **동시성 락 / 장부 파일 분실 후 replay fail-closed**, single-user SU-L1 로컬 승인정책·격리 자체시험, 로컬 독립 reviewer 가용성 확인, 비관리자 LIVE 계정·PAT·원격 비민감 메타데이터 경로·backup/rollback 실행 계획)를 **새로운 중간 인계 없이 하나의 개발 작업**으로 수행하도록 지시. 운영 변경·key/PAT 발급·코드 반출·유료 API·READY·LIVE 활성화는 명시 승인 전까지 금지.
- **LOCAL_ONLY D2 유지**: 외부 Claude API에 제한 코드를 넣을 위험이 있으면 해당 코드 단계만 BLOCKED로 격리하고 다른 비민감 설계·합성시험 계속. 외부 Claude Code 동일 개발 세션 자체 시험은 독립 리뷰 `E`가 아님. 실제 로컬 reviewer/무인 runner가 없으면 `E=BLOCKED_LOCAL_REVIEWER`.
- 사용자에게 필요한 최종 운영 승인·사용자 직접 수행(PAT 등)은 **후속 1회 통합 승인 패킷**으로 묶을 예정이나, 기술·보안상 서로 다른 운영 행위의 개별 명시 승인은 그대로 유지. `SU_L1=DESIGN_READY_NOT_APPLIED / C=PARTIAL / D=LOCAL_ONLY / TOKEN=BLOCKED_OVERPRIVILEGED / E=NOT_RUN / ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER`. 기존 watcher/Bridge/updater Disabled, notifier Running 자체보고 상태 불변.
- 다음 한 동작: Windows Claude Code에 **정확한 PRIVATE main 단일 마스터 경로** 하나를 전달해 가능한 개발·격리시험·로컬 후보 ZIP·PRIVATE 비민감 결과 게시/readback을 중간 질문 없이 실행하도록 요청. `CLAUDE_SINGLE_USER_LIVE_FASTTRACK_RESULT_FOR_GPT_20261114.md`가 게시되면 GPT 한 번의 통합 판정 후 필요한 실운영 승인만 모아 제시.


## GPT 판정 — LOCAL_ONLY 차단 delta / v2 정적 코드 위험 (2026-11-14 KST)
- `CLAUDE_LOCAL_ONLY_BLOCKERS_DELTA_RESULT_FOR_GPT_20261114.md`(commit `596b6732c29149fedd2176879c17c2df88e3c043`), CURRENT/TRACKER, `tools/local_only_contract_r0002.py`, `tools/reviewer_isolation_probe_r0001.py` 원격 읽기 후 **`GPT_DISPOSITION=ACCEPT_WITH_CHANGE`**. 판정서 `GPT_LOCAL_ONLY_BLOCKERS_DELTA_DISPOSITION_r0001_20261114.md` PRIVATE main 게시/remote readback PASS.
- 실측 자기보고: 기존 PC reviewer egress 5/5 연결 `NOT_ISOLATED`, 모델 런타임 없음. 격리 도구 12 PASS, v2 r0002 26 PASS/변이 10/10는 자체시험이고 실제 로컬 독립 리뷰·운영 승인 아님. 사람/온프레미스 모델 reviewer는 여전히 `BLOCKED_LOCAL_REVIEWER`.
- GPT 정적 코드 검토에서 새로운 **운영 BLOCKING 위험 2개** 확인: (1) `State.save()`는 단일 `.tmp`+`os.replace`지만 멀티프로세스 원자 예약/동시성 락 없어 같은 nonce/receipt 이중 허용 가능. (2) 존재하지 않는 state 파일은 빈 `nonces/accepted`로 초기화해 장부 분실·삭제 후 replay FAIL_CLOSED 증명 안 됨. 동일 개발자 테스트 PASS=독립 리뷰 아님. **동시 실행 / state 삭제+재시작 / crash+rollback** delta 회귀시험을 정식 운영 전에 시행하고 별도 독립 보안 리뷰.
- `reviewer_locality`/attestation digest 서명은 **ON_PREM 실행 사실을 직접 증명하지 못함**. DNS/TCP probe도 전체 네트워크 egress 무존재 증명 아님. 조직 승인 실행 환경·방화벽 등 독립 확인 필요.
- B 별도 signer 기기·6개 키트 **내부 이동 정책**과 실제 로컬 reviewer/host의 존재는 현재 미확인. LIVE 전용 비관리자 계정·신규 최소권한 PAT·신뢰 root·v2 정식 계약 승인/운영 적용 미실행.
- **`ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER / C=PARTIAL / D=LOCAL_ONLY / TOKEN=BLOCKED / E=NOT_RUN`** 유지. Dropbox watcher/Bridge/updater Disabled, notifier Running 자체보고. 사용자 두 핵심 사실을 한 번에 확인 후 후속 delta 묶음 진행. 실키·토큰·운영 계정/DB·READY/유료 reviewer/LIVE 변경 금지.


## LOCAL_ONLY_BLOCKERS_DELTA_RESULT: E=BLOCKED_LOCAL_REVIEWER / B=AVAILABLE_UNDESIGNATED / TOKEN=BLOCKED_OVERPRIVILEGED / PROTOCOL_V2=PROTOTYPE_ONLY / ACTIVE_PROVIDER=NONE (Claude 자체 보고, 2026-11-14 KST)
- 결과: `CLAUDE_LOCAL_ONLY_BLOCKERS_DELTA_RESULT_FOR_GPT_20261114.md` (PRIVATE `main`, commit `596b6732c29149fedd2176879c17c2df88e3c043`, 원격 바이트·SHA-256 `3205074049b7db08a62f72b7cb71811a6c831c15084f57667618fbd92b66a234` 일치). 기존 시험 반복 0, 운영 키·토큰·계정·ACL·Task·DB·업로드·외부 모델·유료 리뷰·READY·LIVE·이력 변경 0, 모델 호출 0, 비용 $0. 독립 리뷰 아님.
- **자동 리뷰 재개 임계 경로**: ①로컬 독립 리뷰어 실존과 ③별도 서명자 기기·키트 내부 이동 정책이 미확인이라 나머지가 준비돼도 재개되지 않음. 사용자 필수 확인은 이 두 가지.
- **리뷰어 격리 입증 도구 신규**(시험 12 PASS, 루프백 양성·음성 대조 포함): 이 PC 실측은 `NOT_ISOLATED`(외부 엔드포인트 5/5 접속 가능, 프록시 없음) → 이 PC에서 외부 API 모델 사용은 LOCAL_ONLY가 아니며 로컬 모델 런타임도 없음. 후보 리뷰어 호스트가 정해지면 그 호스트에서 1회 실행. 통과해도 필요조건일 뿐.
- **v2 계약 r0002**: 위협 모델 12개 기준 보강(재시작 후 유지되는 nonce·영수증 장부, 비용 상한 0.00 강제, 영수증에 런타임 격리 증명 다이제스트 필수, 영수증 기간 검사, 손상 상태 fail closed). 시험 26 PASS·변이 10/10 검출. **r0001 게시본의 간헐 시험 결함 공개**(크기 부분 문자열 검사, 약 20% 실패 가능) 후 r0002로 대체. 독립 보안 리뷰·운영 적용은 미승인.
- **LIVE 서비스 계정 설계**(변경 0): 전용 비관리자·배치 로그온만·상태 폴더만 쓰기·trust 읽기·아카이브 권한 0, 승인 후 실측 7항목. 계정 구성이 토큰 설치의 선행 의존이 됨.
- **기게시 식별자 노출 범위**(비파괴, 개수만): 이력 441커밋, 원시 다이제스트 10종/50커밋/HEAD 31파일, 크기 10종/37커밋/21파일, 유래 파일명 45종/14커밋/12파일. 현재 후보 v0.2.12의 다이제스트·크기는 이력에 없음. 추가 게시 중단, 이력 재작성·삭제 없음, 처분은 데이터 분류 소유자 승인 후.
- 다음 한 동작: 사용자가 ①별도 회사 관리 서명자 PC·키트 내부 이동 허용 ②조직 승인 온프레미스 모델 또는 사람 리뷰어의 실존·호스트를 확인한다. 나머지는 각각 별도 승인.

## GPT 판정 — 로컬 전용 5개 결정 권고 (2026-11-14 KST)
- GPT가 `CLAUDE_B1_C1_D2_TOKEN2_LOCAL_ONLY_RESULT_FOR_GPT_20261114.md` (원격 commit `615da26d0257cbb864689c1c3a52210f66f34265`) 원문 재확인. **`GPT_DISPOSITION=ACCEPT_AS_DESIGN_CANDIDATE_WITH_BLOCKERS`**. 사용자 질의 5개에 대해 권장 방향을 `GPT_LOCAL_ONLY_FIVE_DECISIONS_DISPOSITION_r0001_20261114.md`로 작성해 PRIVATE main 게시/readback PASS.
- **권고 1 B**: 별도 조직 관리 Windows PC(실재·6개 키트 내부 이동 정책은 확인 필요), 암호화 키/개인키 호스트 분리. 운영키 생성·trust-root 설치 미승인.
- **권고 2 Token**: 기존 과권한 OAuth 사용 금지, 사용자 직접 신규 단일 저장소 Contents read-only fine-grained 자격 준비. 기존 자격 미사용·신규 발급/설치 미승인.
- **권고 3 E/v2**: 코드·ZIP은 LOCAL_ONLY 유지. 내부에서 진짜 사용 가능한 조직 승인 온프레미스 모델 또는 사람 독립 리뷰어부터 확인. v2 local artifact/solt commitment/GitHub control-plane 메타데이터 계약은 설계·독립 보안 리뷰 후보이며 정식 운영 적용 미승인. Windows 현재 PC에는 로컬 모델 런타임 미관측, 조직 전체의 부재는 증명되지 않음.
- **권고 4 LIVE account**: 별도 비관리자 서비스 계정+GitHub 전용 state/ACL과 기존 Dropbox archive 접근 거부 제안. 실제 Task/run-as/ACL/DB 변경은 별도 운영 승인 후. 이전 SHADOW 계정 증거를 운영자 LIVE 계정에 소급하지 않음.
- **권고 5 historical identifier**: 기존 기게시 ZIP SHA·크기·파일명은 당분간 제한 메타데이터로 취급해 추가 공개 중지·비파괴 인벤토리 후 조직 정책 판정. history force-push/삭제 금지, Git 이력 삭제만으로 완전 삭제 보장 없음.
- **현재 수락·실행 경계**: GPT 권고가 사용자·조직 정책 승인 아님. `B=DEVICE_UNDESIGNATED / C=PARTIAL / D=LOCAL_ONLY / TOKEN=BLOCKED_OVERPRIVILEGED / E=BLOCKED_LOCAL_REVIEWER / ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER`. 새 모델 호출·유료 리뷰·READY·LIVE 미실행.
- 다음 한 동작: 실제 별도 조직 관리 서명자 기기 존재/키트 내부 이동 정책과 조직 승인 로컬 리뷰어·모델의 사용 가능성을 **한 번에 확인**, 이후 B/C/E/v2 보안 게이트 승인 범위 안에서 delta 검증만 지속.


## B1_C1_D2_TOKEN2_LOCAL_ONLY_RESULT: B=AVAILABLE_UNDESIGNATED / C_ALT=PROPOSED(C=PARTIAL) / D=LOCAL_ONLY / TOKEN=OVERPRIVILEGED / E=NOT_RUN / ACTIVE_PROVIDER=NONE (Claude 자체 보고, 2026-11-14 KST)
- 결과: `CLAUDE_B1_C1_D2_TOKEN2_LOCAL_ONLY_RESULT_FOR_GPT_20261114.md` (PRIVATE `main`, commit `615da26d0257cbb864689c1c3a52210f66f34265`, 원격 바이트·SHA-256 `ffb8ea548fc2c1ced1692d1a24c276dd3818b52856b9c11a7740352a5f450ad2` 일치). 운영 키·토큰 설치·운영 DB 열기·예약 작업 변경·업로드·유료 리뷰·READY·LIVE·시험 계정 활성화·모델 호출 0, 비용 $0. 독립 리뷰 아님.
- **토큰**: 기존 GitHub 자격은 클래식 OAuth 계열 `repo`·`workflow`·`read:org`·`gist` 범위의 광역 권한 → `BLOCKED_OVERPRIVILEGED_EXISTING_CREDENTIAL`. 값·접두·경로 조회 0, 최소 권한 기존 PAT는 확인되지 않음.
- **C 계정별 격리**: 운영 상태 폴더·DB·WAL·SHM 유효 권한은 운영자 계정·Administrators·SYSTEM만 전체, 시험 SHADOW 계정·Users·Everyone은 0. 운영 예약 작업 4개는 모두 운영자 계정 실행이라 **LIVE에는 ACL 축 적용 불가(`C_ALT_NOT_APPLICABLE_TO_LIVE`)**. 신규 `shadow.account_isolation=enforce`는 운영 데이터에 권한이 있는 계정으로 SHADOW 시작 시 거부(운영자 계정으로 실측 시 ACCESSIBLE 5건), 시험 17 PASS·변이 5/5 검출. ETW는 NOT_PROVEN 유지.
- **B**: 서명 개인키 평문 저장을 해결(`--passphrase` scrypt+AES-GCM 암호화, Windows ACL 본인 제한, 평문은 `--allow-plaintext-key` 명시), 시험 13 PASS, 서명 키트 6개 파일 재시험. 실기기 미지정·운영 키 0.
- **D2**: 로컬 전용 제어면·영수증 계약 프로토타입(솔트 커밋먼트, 서명 승인, 외부 API 리뷰어 영수증 거부, nonce·중복 거부) 19 PASS·변이 5/5 검출, `tools/`에 코드 없는 설계 증거로 게시. 이 PC에는 로컬 모델 런타임이 없어 `E=BLOCKED_LOCAL_REVIEWER`. 기게시된 ZIP 다이제스트·크기·일부 파일명의 소급 재점검이 사용자 결정 항목.
- 후보 v0.2.12는 로컬 보존이며 **원시 SHA-256·크기는 게시하지 않음**: 불투명 ID `art-68c732d28afd8ceb`, 커밋먼트 `ac238d4d40fd362fb7a46ba80b48969a18f5c56aaae12ab4af0b74886a63f8e7`. 시험 venv 566 passed/12 skipped, 운영 인터프리터 518 passed/15 skipped ×3(수집 차이 45=cryptography 필요한 세 모듈). 이전 후보 ZIP 바이트 보존.
- 다음 한 동작: 사용자가 결과 §7의 다섯 결정(서명자 기기, 새 토큰 발급 여부, 로컬 독립 검토자와 프로토콜 변경 승인, LIVE 계정 구성, 기게시 식별자 처리)을 한 번에 답한다.

## 사용자 결정 반영 — B1/C1/D2/Token2 로컬 전용 경로 (2026-11-14 KST)
- 사용자 의사결정 **`B=1 / C=1 / D=2 / TOKEN=2`**: B는 감시기 외 별도 승인자 기기 사용 가능(실기기 미지정·운영키 미발급), C는 4축 대체 안전성 기준 검토 선택(**C PASS 아님**), D는 **회사 원본·파생 및 신규 코드/ZIP 외부 반출 불가·LOCAL_ONLY**, 토큰은 기존 자격의 최소권한 확인 우선(신규 발급/설치 승인 아님).
- GPT가 최신 `CURRENT.md`, BCD 자체 시험/토큰 F1~F6, B7 신뢰 루트 설계 및 review transport 계약을 확인하고 **단일 Windows delta 인계** `GPT_B1_C1_D2_TOKEN2_LOCAL_ONLY_DELTA_ONE_SHOT_r0001_20261114.md`를 PRIVATE main에 직접 게시(짧은 commit `f3d7cf86`), remote readback PASS. 기존 500+ 제품 시험/ETW/토큰 모의 시험 반복 금지.
- **B 진행**: 운영 signer kit 6개 파일은 기존 자체시험 근거를 재사용하되 기기 지정·내부 이동 허가·저장 매체 보호·개인키 생성/공개 root 설치는 NOT_RUN. Key 값/원본 artifact PRIVATE 게시 금지.
- **C 진행**: 별도 비관리자 SHADOW 계정의 효과적 ACL deny·분리 state 경로/identity·코드 call path·변이 대조의 4축 기준을 정식 수락 계약 **후보로 구체화**. 이전 SHADOW 계정 근거를 LIVE의 다른 계정에 소급하지 않음. `C=PARTIAL / ETW=FAIL_UNTRUSTED_MEASUREMENT / C_ALT=PROPOSED_ONLY` 유지.
- **D 결론**: 로컬 소스/ZIP(현재 v0.2.11 175714B) 및 실제 리뷰 원문은 외부 업로드 금지. 기존 `Commit A ZIP raw SHA → signed READY` GitHub transport 계약은 **D2에서 그대로는 성립하지 않음**. 내부 독립 reviewer·로컬 artifact SHA 증명 + 정책상 허용된 비민감 메타데이터/receipt만 GitHub 게시하는 **새 계약 설계/리뷰 승인 필요**. `GITHUB_LOCAL_ONLY_REVIEW_TRANSPORT=DESIGN_REQUIRED / E=NOT_RUN`; 외부 Claude API가 로컬 환경에서 실행되어도 코드 반출로 이어질 수 있음.
- **토큰 진행**: 기존 GitHub credential을 권한 근거로 실측 확인하되 값·prefix·경로/secret 절대 출력 금지. GitHub CLI 광역 OAuth를 least privilege라고 판단하지 않음. `github_token_check_r0002` GET-only 종료 2=NOT_PROVEN; 사용자 GitHub UI 8항목 O/X는 사람 증거. **`TOKEN_EXISTING_MIN_SCOPE=NOT_VERIFIED / CREDENTIAL=BLOCKED`** 유지.
- **승인·운영 경계**: B1/C1/D2/token2는 준비 방향 선택일 뿐 실운영 키/root 생성·토큰 설치·외부 코드 리뷰 API·유료 reviewer/READY·운영 DB/예약 작업·LIVE 활성화 승인 아님. `ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER` 유지. 원본 Dropbox watcher·Bridge·updater Disabled, notifier Running 자체보고 기록 보존.
- 다음 한 동작: Windows Claude Code가 위 단일 PRIVATE main 인계로 **허용된 로컬 delta 분석·합성 시험·비밀 없는 권한/계정 확인**을 수행 후 `CLAUDE_B1_C1_D2_TOKEN2_LOCAL_ONLY_RESULT_FOR_GPT_20261114.md`와 CURRENT/TRACKER만 원격 게시/readback → GPT가 남은 실제 승인 범위를 일괄 판정.


## GPT 판정 — 토큰 도구 r0002 Windows 자체시험 수용 (2026-11-14 KST)
- GPT가 최신 `CLAUDE_BCD_TOKEN_APPROVAL_PRECHECK_RESULT_FOR_GPT_20261113.md` F1~F6 원문 및 r0002 도구·시험을 원격 확인. GPT 판정은 기존 `GPT_BCD_TOKEN_PRECHECK_DISPOSITION_AND_DELTA_r0001_20261113.md` §9에 **신규 후속 절만 추가**(과거 보고 보존), PRIVATE main 게시 및 remote readback PASS.
- Windows 합성 자체시험: r0002 23 PASS(두 인터프리터), r0001 보존분 포함 34 PASS, 격리 설치 스크립트 18 PASS. 전부 모의 응답/코드 정적 검사이며 실제 PAT/네트워크/관리자 실행 0. 원본 설치 스크립트 변경·실행 0.
- r0001의 '403 write probe로 read-only 확인', '/user/repos 결과가 저장소 1개면 권한 확정' 주장은 **철회**. r0002는 GET-only·미입증 수용, 비밀번호 등 자격 노출 방지. Exit 1=FAIL, Exit 2=NOT_PROVEN, Exit 0 기타=NOT_PROVEN. 사용자 GitHub 설정 8항목 O/X는 확인 진술이며 실제 권한 API 증명 아님.
- **상태 변화 없음**: `CREDENTIAL=BLOCKED_CREDENTIAL / B=BLOCKED_SIGNER_DEVICE / C=PARTIAL / D=BLOCKED_EXPORT_CLASSIFICATION / E=NOT_RUN / ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER`.
- **다음 한 동작:** 사용자 B/C/D/토큰 선택 네 개(각 1/2/3)를 한 번에 받아 조건부 후속 게이트. 승인 없는 실키 생성·원본 ZIP 반출·READY/유료 독립 리뷰·LIVE 전환 금지.


## TOKEN_TOOL_R0002_DELTA_SELF_TEST: r0002 23 PASS · 설치 스크립트 격리 사본 연결 완료 / 실 PAT·네트워크·관리자 셸 0 (Claude 자체 보고, 2026-11-13 KST)
- 결과: `CLAUDE_BCD_TOKEN_APPROVAL_PRECHECK_RESULT_FOR_GPT_20261113.md`에 후속 섹션 F1~F6 추가(commit `2a86a131bce3ced49899bab7b488fa314fd19fc0`, 원격 바이트·SHA-256 `3986e3f3a69b61ce89270b69fce6514e50471496ba1aacca377854385434126f` 일치, 이전 본문 14,244 B는 바이트 그대로 보존). SELF_TEST_REPORTED, 독립 리뷰 아님.
- 도구 r0002 2개는 원격 고정 경로에서 받아 §5와 크기·SHA-256 일치 확인. 시험: r0002 23 PASS(시험 venv·운영 인터프리터), r0001 보존분과 합쳐 34 PASS/0 FAIL. 모두 모의 응답.
- 설치 스크립트 원본은 실행·수정하지 않았고 원문 검토에서 3건 확인(r0001+`--probe-write` PUT 사용, 종료코드 미해석, 결과와 무관한 "Token installed" 출력). 격리 사본은 r0002 연결, 종료 1=FAIL·2=NOT_PROVEN·그 외(0/시간 초과 포함)=NOT_PROVEN이며 어떤 값도 준비 확립이 아님. 합성 18 PASS, 원본은 4개 위반 전부 검출, 변이본 1건 검출. 스크립트는 사용자 절대 경로 포함으로 로컬 보존.
- 이전 결과의 "403이면 쓰기 불가"·"정확히 저장소 1개" 서술은 철회, r0001 전체 PASS는 설치 준비 증거로 쓰지 않음. 비민감 GitHub 설정 체크리스트 8항목은 사용자 진술 증거로 분류.
- 상태 변동 없음: ACTIVE_PROVIDER=NONE, B=BLOCKED_SIGNER_DEVICE, C=PARTIAL, D=BLOCKED_EXPORT_CLASSIFICATION, 토큰=BLOCKED_CREDENTIAL, E=NOT_RUN. 다음 한 동작: 사용자가 B/C/D/토큰 결정을 숫자로 한 번에 답한다.

## GPT 토큰 검증기 delta 완료 / Windows 자체시험 인계 준비 (2026-11-13 KST)
- DEVELOPMENT=IMPLEMENTED
- SELF_TEST=PASS
- INDEPENDENT_REVIEW=NOT_RUN
- GPT_DISPOSITION=ACCEPT_WITH_CHANGE
- ACTIVE_PROVIDER=NONE / CUTOVER=MIGRATION_NOT_CUTOVER. B=BLOCKED_SIGNER_DEVICE, C=PARTIAL, D=BLOCKED_EXPORT_CLASSIFICATION, CREDENTIAL=BLOCKED_CREDENTIAL 유지.
- 판정·정확한 Windows delta 인계: `GPT_BCD_TOKEN_PRECHECK_DISPOSITION_AND_DELTA_r0001_20261113.md` §6. 기존 마스터/대규모 제품 시험을 반복하지 않고 토큰 도구와 설치 스크립트 격리 사본 연결만 확인.
- GPT가 r0001 기본 실행의 잘못된 전체 PASS를 모의 응답으로 재현. r0002 2개 별도 추가(r0001 원본 보존): GET-only, 쓰기 probe 거부, 실제 저장소 선택/권한은 NOT_PROVEN; 종료1=실패, 종료2=부분확인. 도구만으로 설치 승인/읽기 전용 확정 불가.
- GPT Linux 합성 자체시험: 기존11+신규23=34 PASS/0 FAIL/0 SKIP. 실제 PAT/Windows/운영 설치 NOT_RUN. v0.2.11 ZIP(175714B, sha256 174b9fd83361cc85ce3fb1b4b503335dc701bff9e38415ae23a11256ef8b6350)은 Claude SELF_TEST_REPORTED/로컬 보존; 원본 제품 코드 GPT 검증 NOT_RUN.
- 사용자 B/C/D/토큰 응답 대기. 현재 지시는 개발/시험/PRIVATE 게시 후속 범위이며 키·토큰·반출·유료 리뷰·READY·운영 변경·LIVE 승인 아님.
- REMOTE_READBACK=PASS — bundle commit `2d612a53e3e411e0367f47164b89c51ccb419d1e`의 5개 파일을 고정 커밋에서 재조회해 UTF-8 바이트·SHA-256 일치 확인. 도구 sha256: `2ab292aa63b23f010620548c91f43cb02a9b182fad10dc5122f63dc0e79fccc4`, 시험 sha256: `36b14ff5c2676df44542e66cacdd165e9ec399f936dc1a7e79a5bf69d50452bf`, 판정서 sha256: `4c4232342b50dd9d3bebf06a46a35689444eb73a06a8c71799e8603c1215e002`, TRACKER sha256: `a32cdf50405380bd777dbed3d87b5a8cf2f90f0b45a6f6cbdf6e6feb62bc3214`. 실제 대시보드 TRACKER 검증기 로컬 후보 수락 PASS. 이 검증은 Windows 실행/운영 승인과 별개.
- 다음 한 동작: Windows Claude Code에서 위 정확한 repo/main/인계서 §6을 1회 실행 → 기존 Claude 결과에 후속 섹션 추가·PRIVATE 원격 재검증. Windows 실행은 아직 관측되지 않음.

## BCD_TOKEN_APPROVAL_PRECHECK_RESULT: B·D·토큰 BLOCKED / C PARTIAL(대체 증거 4축 수집) / ACTIVE_PROVIDER=NONE (Claude 자체 보고, 2026-11-13 KST)
- 결과: `CLAUDE_BCD_TOKEN_APPROVAL_PRECHECK_RESULT_FOR_GPT_20261113.md` (PRIVATE `main`, commit `8870f37a60eb2463fa6441314b141eac89791960`, 원격 바이트·SHA-256 `7b4f87dd54bdb160778c66d6d16fb93d547f1b13eb184c9398bc77e041666eaf` 일치). 관리자 셸·새 ETW·운영 DB 열기·모델 호출·비용 0, 키 생성·root 설치·업로드·READY·LIVE 0. 독립 리뷰 아님.
- B: 승인자 기기용 **서명 키트 6개 파일**(v0.1.5 유래 코드 없음)을 구성하고 임시 시험 키로 keygen→sign→check→1바이트 변조 거부까지 시험. 운영 키는 BLOCKED_SIGNER_DEVICE. C: 대체 4축 증거(시험계정 SID 유효 권한 운영 폴더·DB·WAL·SHM 모두 0x0 / 경로 가드·identity / 라이브 폴더 참조 함수 전수 조사 6개 / 변이 시험 4종 전부 검출). 전수 조사에서 결함 1건 발견·수정(`config-check`·`auth-check`·`auth-init`이 SHADOW·GitHub에서도 라이브 폴더·비밀을 사용). 수락 기준 승인 전 C=PARTIAL. D: 유래 46(34+12)/신규 24, v0.1.5 유래 줄 약 52%, 대안 3종(전량 게시/신규 24만/사내 로컬 리뷰). 토큰: 검증기(시험 11 PASS)·설치 스크립트 준비, 발급은 사용자 몫.
- 후보 **v0.2.11** 로컬 ZIP 175714 B, sha256 `174b9fd83361cc85ce3fb1b4b503335dc701bff9e38415ae23a11256ef8b6350`(536 passed/12 skipped, 운영 인터프리터 501/14 x3, 간헐 시험 실패 원인 규명·수정). v0.2.10 ZIP은 바이트 보존. 둘 다 미게시.
- 다음 한 동작: 사용자가 결과 §6의 B/C/D/토큰 숫자 선택으로 한 번에 응답.

## GPT B·C·D·GitHub 인증 단일 승인 패킷 (2026-11-13 KST)
- 사용자의 GitHub LIVE 최소 반복 진행 의사에 따라 **B 서명자 기기, C 대체 증거/ETL 선택, D 원 소스 반출 분류, GitHub Contents:Read-only 자격**을 한 번에 묻는 단일 패킷 작성. `GPT_BCD_TOKEN_SINGLE_APPROVAL_PACKET_r0001_20261113.md` PRIVATE main commit `2046f5b75f8b1574c9d35d53cd331a1966f60e7c`, 원격 원문 readback PASS.
- B 별도 장치/운영키 생성, C 수락기준 변경/추가 실측, D 사외 유래 코드 반출, PAT 발급·배포는 각자 별도 승인·권한 경계. 이번 문서는 **DECISION_PACKET_READY**, Windows 미실행 및 유료 reviewer·REQUEST/READY·운영 watcher 설치·GitHub LIVE 미승인.
- 기존 완료/자체보고 재활용: Dropbox 감시기·Bridge·갱신기 Disabled(Notifier KEEP), v0.2.10 로컬 후보, ETW r0002 합성 시험, C 실제 GET-only. **B=BLOCKED, C=PARTIAL, D=BLOCKED, E=NOT_RUN, ACTIVE_PROVIDER=NONE, MIGRATION_NOT_CUTOVER** 그대로.
- 다음 한 동작: 사용자 Windows Claude Code에 정확한 PRIVATE main 패킷을 읽고 4개 게이트 준비/조건별 최소 작업을 한 번에 보고하도록 전달(운영 변경·키·반출·유료 reviewer 금지). 이후 사용자에게 4개 숫자 선택으로 동시 승인 여부 확인.


## GPT 판정 — LIVE 최소 반복 통합 결과 수용 (2026-11-13 KST)
- GPT가 통합 Claude 결과 `CLAUDE_GITHUB_LIVE_FAST_TRACK_READINESS_RESULT_FOR_GPT_20261113.md`(Git blob `113583de3bf63a6de84c145bcd12410a1038a47d`), Bridge/updater 비활성화 결과 및 ETW r0002 도구·테스트 원문, TRACKER 원격 재조회. 판정서 `GPT_MINIMUM_REWORK_RESULT_DISPOSITION_r0001_20261113.md` PRIVATE main 직접 게시·readback PASS.
- **`GPT_DISPOSITION=ACCEPT_WITH_LIMITATIONS`**. Dropbox 감시기·Bridge·갱신기 Disabled/PID0 호스트 자체보고 PASS 수용; Notifier는 Running/유지. Bridge/updater 종료는 별도 Windows 사용자 관리자 셸 1회, 통합 마스터 실행은 관리자 0·새 ETW 0·운영 DB 연결 0·모델 0·비용 $0. 실제 재부팅·재로그인 이후 지속 검증은 NOT_RUN.
- 코드 delta: ETW 보조 r0002 별도 추가(기존 r0001 보존), 수명 외 이벤트 차단·8.3 확장·파일 identity 방어, **신규 20 PASS(Claude 자체 보고)**. 변환기 Clock-Time/PID 귀속 신뢰성은 미복구. 운영 DB 파일 무접근 ETW는 여전히 **`NOT_PROVEN`**, `C=PARTIAL`; 4요소 ACL/state isolation/file-ID/runtime call path의 **대체 수락안은 PROPOSED_ONLY**. 본 판정만으로 C 승인 변경/PASS 불가.
- v0.2.10 후보 원본 ZIP(174745 B, SHA256 `67ea7fc63ccc1de77a28025b7c4f1b701ee6f4fa387311bca3f3d2bc7432b108`)은 Windows 로컬 보존만. 출처 분류 **34 UNCHANGED + 12 CHANGED = 기존 유래 46개**, NEW 24개. 기존 유래 파일 사외 반출 허가 미확인. 전체 원본 바이트 GPT 검증/PRIVATE 업로드/독립 리뷰 NOT_RUN.
- 자체시험·합성 롤백 스냅샷 PASS는 실운영 이행·복구나 Claude 독립 리뷰 PASS와 구분. **`B=BLOCKED_SIGNER_DEVICE / C=PARTIAL / D=BLOCKED_EXPORT_CLASSIFICATION / E=NOT_RUN / GITHUB_LIVE=NOT_APPROVED / ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER`**. 비관리자 read-only 토큰의 실제 정식 보관처 설치는 미확인(과거 일시적으로 실 GitHub GET을 시험한 것과 별개).
- 최소 반복: 앞으로 새 인계서 연속 생성/중복 테스트 대신 최신 마스터와 실제 delta만 확인. 사용자 승인 패킷 **B 별도 서명자 기기, C 대체기준 vs ETL 재분석 선택, D 46개 유래 소스+NEW 소유·반출 확인, repo Contents:Read-only 토큰 설치**를 한 번에 요청; E 유료 독립 리뷰와 최종 LIVE 설치/전환은 선행 요건 검증 후 별도 명시 승인.
- 원격 결과 판정 문서 `GPT_MINIMUM_REWORK_RESULT_DISPOSITION_r0001_20261113.md`; 다음 한 동작: 사용자에게 B/C/D/토큰 승인 의사·제약을 묶어서 확인. 실제 키 생성/운영 DB 변경/업로드/유료 리뷰/READY/운영 설치/ LIVE 전환 0.


## GITHUB_LIVE_MINIMUM_REWORK_RESULT: C/B/D/E 게이트 BLOCKED·PARTIAL, ACTIVE_PROVIDER=NONE (Claude 자체 보고, 2026-11-13 KST)
- 결과: `CLAUDE_GITHUB_LIVE_FAST_TRACK_READINESS_RESULT_FOR_GPT_20261113.md` (PRIVATE `main`, commit `d80064781c7cbb12a382faadd2b24db2a5f09426`, 원격 readback 일치). 마스터 하나만 기준, 기존 증거 재사용, 관리자 셸·새 ETW 추적·운영 DB 열기·모델 호출·비용 모두 0. 독립 리뷰 아님, LIVE 전환 아님.
- delta: ETW 사전검증 `r0002`(수명 밖 이벤트 오류화, 8.3 이름·파일 identity 방어; 원본 r0001 보존, 9 PASS 유지 + 신규 20 PASS, commit `9a89ae98d87ec9480f191c0b75986ba55b6b0bf2`). `TRACKER.json`의 허용 enum 밖 값(phase/self_test)으로 대시보드가 등록을 무시했을 가능성을 실제 검증기로 확인하고 정정(commit `046cca71144a40c05c54eb1ddde8eb0e4b557d4d`). v0.2.10 롤백 리허설은 스냅샷 사본에서 항목별 PASS(실운영 롤백 NOT_RUN).
- 상태: C=PARTIAL(ETW FAIL_UNTRUSTED 유지, C_ALT_EVIDENCE=PROPOSED_ONLY), B=BLOCKED_SIGNER_DEVICE, D=BLOCKED_EXPORT_CLASSIFICATION(34 UNCHANGED+12 CHANGED는 v0.1.5 유래), E=NOT_RUN, 읽기 전용 토큰 BLOCKED_CREDENTIAL. v0.2.10 ZIP(174745B, sha256 `67ea7fc63ccc1de77a28025b7c4f1b701ee6f4fa387311bca3f3d2bc7432b108`)은 로컬 보존.
- 다음 한 동작: 결과 §7 승인 패킷(B 서명자 기기, C 수락 방식, D 반출 확인, 읽기 전용 토큰)에 사용자가 한 번에 응답.

## DROPBOX_BRIDGE_UPDATER_RETIRE_RESULT: BRIDGE=DISABLED_STOPPED / UPDATER=DISABLED_STOPPED / NOTIFIER=UNCHANGED_RUNNING / ACTIVE_PROVIDER=NONE (Claude 자체 보고, 2026-11-13 KST)
- 결과: `CLAUDE_DROPBOX_BRIDGE_UPDATER_RETIRE_RESULT_FOR_GPT_20261113.md` (PRIVATE `main`, commit `195e79c33e6cf8c3d34bc7b0a4e861952890bca0`). 자체 실측 보고이며 독립 리뷰가 아니다. GitHub LIVE 전환이 아니다.
- 근거: 의존성 감사 결론(Bridge·갱신기 RETIRE_CANDIDATE)과 사용자의 직접 지시(Dropbox 대시보드를 보지 않음). 사용자가 관리자 셸에서 검증된 스크립트 1개를 1회 실행해 Bridge Disable·Stop 후 갱신기(게시 중 아님 확인 후) Disable·Stop.
- 결과: Bridge·갱신기 작업 `Disabled`, 프로세스 0. 두 작업 정의는 보존본 대비 `Enabled=false` 한 줄만 다름. 알림기는 정의 바이트 동일·같은 프로세스·워터마크 불변. 감시기는 Disabled·프로세스 0 유지. 운영 DB·설정·비밀·로그·Dropbox·Telegram·모델 호출 변경 0.
- 알아 둘 점: 스크립트의 알림기 확인 줄은 변수명 대소문자 충돌로 잘못 출력됐으나(출력 오류) 사후 단독 확인으로 정상 확인. Dropbox `index.html`은 마지막 값(요청 65·결과 60)에 고정된다. 재부팅·재로그인 후 유지와 장기 안정은 미검증(`LONG_RUN=PENDING`). 복구는 관리자 셸에서 갱신기 → Bridge 순서로 Enable 후 Start.
- 다음 한 동작: GPT가 판정하고, 알림기의 GitHub 알림 경로 이행·유지 여부는 사용자 별도 승인으로 결정.

## GPT 실행 통합 — GitHub LIVE 최소 반복 마스터 (2026-11-13 KST)
- 사용자 최우선 목표: **반복 최소화와 GitHub LIVE 신속 전환**. GPT는 여러 개로 분산된 Windows 실행 인계를 단일 기준 `GPT_GITHUB_LIVE_MINIMUM_REWORK_MASTER_r0001_20261113.md`로 통합. PRIVATE main commit `0ec5845aa8109eb6e3381dd16b629999f379d2f5`, 원격 전체 내용 readback PASS.
- 새로운 master는 **증거 ledger 작성 → 기존 PASS/FAIL/NOT_RUN 재사용 → 불일치 delta만 격리 코드 수정·시험 → C/B/D/E·설치/롤백 승인 필요 항목을 최종 한 묶음으로 보고**. 이전 `GPT_GITHUB_LIVE_FAST_TRACK_PARALLEL_ONE_SHOT_r0001_20261113.md`, 잔여 서비스 감사/정리 인계서는 중복으로 실행하지 않고 참고 자료로 사용. Windows는 **단일 최신 마스터 인계서만** 실행 진입점.
- 이미 완료되어 반복 불필요: Dropbox 감시기 Disable+DB 복사본 무결성(호스트 자체 보고), 잔여 Bridge/updater/notifier 의존성 감사 PASS, v0.2.10 synthetic 자체시험, 비관리자 ACL 실측, 실 GitHub GET-only PASS, ETW parser 실패 재현. 불확실/환경 변화시 해당 부분만 검증하며 이력 PASS를 무조건 운영 PASS로 승격하지 않음.
- 우선 중요 게이트: **C=PARTIAL/ETW=FAIL_UNTRUSTED_MEASUREMENT**, **B=BLOCKED_SIGNER**, **D=BLOCKED_EXPORT_CLASSIFICATION(기존 34개 유래 소스)**, **E=NOT_RUN**, LIVE 설치/DB·알림 이행/롤백 NOT_RUN. 단일 승인 패킷으로 최종 정산하되 각각의 승인 행위는 독립. 승인되지 않은 운영 키 생성/파일 반출/유료 리뷰/READY/운영 변경 및 LIVE 전환은 실행하지 않는다.
- Bridge·Dropbox Dashboard updater=RETIRE_CANDIDATE; Notifier=KEEP. **Bridge/updater Stop+Disable은 별도 승인 대기**, 하지만 GitHub LIVE 준비와 병렬 진행 가능하므로 비핵심 잔여 정리 때문에 개발을 중단하지 않는다. GitHub/Dropbox 자동 리뷰 **ACTIVE_PROVIDER=NONE** 유지.
- 결과를 별도 새 문서로 계속 분기하지 않고 기발행 예정의 `CLAUDE_GITHUB_LIVE_FAST_TRACK_READINESS_RESULT_FOR_GPT_20261113.md` 하나에 통합. `CURRENT.md`와 `TRACKER.json` 동시에 갱신, PRIVATE main PR 없이 remote readback. 서명/반출/유료비용/LIVE 승인 필요 항목만 마지막에 모아 사용자에게 제시.
- **현재 실행상태=`MASTER_HANDOFF_PREPARED / WINDOWS_EXECUTION_NOT_YET_OBSERVED / MIGRATION_NOT_CUTOVER`**. GitHub 인계 게시만으로 Windows/Claude 자동 실행되지 않음. 다음 한 동작: 사용자 Windows Claude Code에서 최신 마스터 정확 경로 1회 실행 후 GPT 결과 판정.


## GPT 판정 — Bridge·Dropbox Dashboard updater 정리 후보 수용 (2026-11-13 KST)
- GPT가 `CLAUDE_POST_DROPBOX_DISABLE_DEPENDENCY_AUDIT_RESULT_FOR_GPT_20261113.md` 및 CURRENT/TRACKER 원문 재조회. Claude `HOST_REAL_READ_ONLY / SELF_TEST_REPORTED` 결과를 **`DEPENDENCY_AUDIT=PASS_REPORTED`**로 수용. `ACTIVE_PROVIDER=NONE`, 호스트 감사 변경 0.
- Bridge는 `HOST_APPLIED` 완료된 v0.1.9 1회 설치용 수신기, 5분 주기 `ALREADY_COMPLETED`, 제어 대상 갱신기만 → **`RETIRE_CANDIDATE` 1순위**. Dashboard updater는 Dropbox 폴더→Dropbox index.html 전용, 입력/출력 고정·GitHub Actions/Pages 독립 → **`RETIRE_CANDIDATE` 2순위**. Notifier는 `KEEP`(프로세스 별도 평가, 공용 Telegram 모듈·비밀/notify_note 삭제 금지).
- 사용자 의도: Dropbox 대시보드를 현재 보지 않는 것으로 기존 대화에서 알려짐. 해당 사실을 Stop+Disable 실행 승인으로 확대하지 않음. 추가 중지 동작은 **`AWAITING_EXPLICIT_APPROVAL`**.
- 원본 SHM 수정 시각 30초 주기는 notifier polling과 상관만 확인. 쓰기 주체/인과는 미입증. main/WAL 불변은 파일 메타데이터 관측 수준. 나머지 자동화 전체 디스크 검색은 수행하지 않음.
- Bridge+갱신기 정리 계획 및 사전 안전조건: `GPT_RESIDUAL_DROPBOX_DEPENDENCY_DISPOSITION_AND_DISABLE_PLAN_r0001_20261113.md` PRIVATE main 게시/remote readback PASS. 승인 후 정체·백업→**Bridge 먼저** Disable/Stop(5분 재실행 차단)→갱신기 Disable/Stop(로그온 trigger, restart 3회/5분)→PID0·프로세스 재생성0·다른 작업 정의 해시 불변 확인. 알림기/공용 venv·인증/DB/원본 Dropbox 자료 불변.
- `C_OVERALL=PARTIAL`, `INDEPENDENT_REVIEW=NOT_RUN`, `ACTIVE_PROVIDER=NONE`, `MIGRATION_NOT_CUTOVER` 유지. GitHub LIVE 전환이나 유료 독립 리뷰 실행 없음.
- 다음 한 동작: 사용자에게 **Bridge와 Dropbox Dashboard updater만 Stop+Disable** 명시 승인 요청. 승인 전 Windows 작업 중지 0.


## POST_DROPBOX_DISABLE_DEPENDENCY_AUDIT: DEPENDENCY_AUDIT=PASS / DASHBOARD=RETIRE_CANDIDATE / NOTIFIER=KEEP / BRIDGE=RETIRE_CANDIDATE / HOST_CHANGES=0 (Claude 자체 보고, 2026-11-13 KST)
- 결과: `CLAUDE_POST_DROPBOX_DISABLE_DEPENDENCY_AUDIT_RESULT_FOR_GPT_20261113.md` (PRIVATE `main`, commit `1dc9fb70deb1e18f5a7c7a59d3fe1c5f42c613c1`). 읽기 전용 감사이며 정리 실행이 아니다. 독립 리뷰가 아니다. GitHub LIVE 전환이 아니다.
- 감시기: 감사 시점 Disabled·프로세스 0, 새 자동 재시작 경로 없음(`ACTIVE_PROVIDER=NONE`). 재부팅·재로그인 후 유지는 미검증(마지막 부팅 11-03).
- Bridge: 갱신기 v0.1.9 1회 설치 수신기, 이미 `HOST_APPLIED`, 매 주기 즉시 반환, 대상은 갱신기 작업 하나뿐이며 감시기를 제어하는 경로 없음 → `RETIRE_CANDIDATE`(가장 먼저).
- Dashboard updater: Dropbox 전용(감시기 DB를 읽지 않음), 입력이 늘지 않아 같은 값만 반복 확인, GitHub 대시보드와 독립 → `RETIRE_CANDIDATE`. Dropbox 화면을 실제로 보는지는 미확인이라 사용자 확인 필요.
- Notifier: 프로세스는 감시기 전용이지만 Telegram 모듈·비밀을 노트 알림이 공유 → 프로세스 중지는 가능하나 `KEEP`(보류), 모듈·비밀 삭제 금지.
- SHM: 수정 시각이 정확히 30초 간격으로 갱신되어 알림기 폴링과 일치(`CORRELATED_NOTIFIER`, 핸들·쓰기 인과는 미확정). main·WAL 불변.
- 호스트 변경 0(작업 생성·Stop·Disable·DB 연결·발송·모델 호출 없음). 의존성 검색 범위는 이 PC의 사용자 작업·자동화 폴더이며 전 디스크가 아니다.
- 다음 한 동작: GPT가 판정하고, 사용자가 Dropbox 대시보드 사용 여부를 답한 뒤 Bridge → 갱신기 순서의 Stop+Disable(관리자 셸)을 별도 승인으로 결정한다.

## GPT Fast Track 병렬 준비 인계 (2026-11-13 KST)
- 사용자 지시: GitHub LIVE까지 **빠르게 진행**. 중간 핑퐁을 줄이기 위해 잔여 Dropbox 서비스 의존성(A), C 호스트·ETW 증거 보완(B), 운영 서명·ZIP 반출·독립 리뷰 준비(C), LIVE 검증·롤백 사전 설계(D)를 **병렬 작업으로 통합**. 운영 키 발급/설치, 사내 코드 반출, 정식 유료 reviewer, 운영 watcher 설치·운영 DB 이행 및 GitHub LIVE 전환을 승인한 것으로 해석하지 않음.
- 최신 기준: `ACTIVE_PROVIDER=NONE / WATCHER_DISABLE=PASS_REPORTED`, `C_OVERALL=PARTIAL`(실GitHub GET-only PASS, ETW parser 신뢰 불가), `B_SIGNER=BLOCKED`, `D_EXPORT=BLOCKED`(v0.1.5 유래 34항목 소유·반출 분류 미완), `E_INDEPENDENT_REVIEW=NOT_RUN`, `MIGRATION_NOT_CUTOVER`. 현재 후보 v0.2.10 ZIP은 로컬 보존·development_not_for_deployment.
- 신규 Windows 원샷 인계: `GPT_GITHUB_LIVE_FAST_TRACK_PARALLEL_ONE_SHOT_r0001_20261113.md` PRIVATE main, commit `820c73f2b28ff868f9171df6e50b57484e871a97`, 원격 원문 readback PASS. 이전 `WINDOWS_POST_DROPBOX_DISABLE_DEPENDENCY_AUDIT_ONE_SHOT_r0001_20261113.md`와 결과를 **재사용하고 이미 끝난 항목은 반복하지 않음**.
- Windows에서 가능한 정적·합성 검증/격리 개발은 한 번에 마무리하고 모델 호출/추가 WATCHER/운영 DB 접근 없이 `CLAUDE_GITHUB_LIVE_FAST_TRACK_READINESS_RESULT_FOR_GPT_20261113.md` 및 CURRENT/TRACKER를 PRIVATE main에 게시·검증. ETW 동일 관리자 시험 무한 반복 금지. 기존 ETW 수락 조건을 임의로 해제하지 않으며 C 대체 증거는 **제안만** 준비.
- **현재 단계는 `FAST_TRACK_HANDOFF_PREPARED_NOT_EXECUTED`**. 문서 게시만으로 Windows Claude Code가 실행되거나 GitHub LIVE로 전환되지 않는다. 다음 한 동작: Windows Claude Code가 정확한 PRIVATE repo/main/인계 경로를 읽고 병렬 원샷 수행, 최종 승인 묶음을 한 번에 보고 → GPT 종합 판정.


## GPT 후속 — Dropbox 잔여 서비스 의존성 READ_ONLY 감사 인계 (2026-11-13 KST)
- 현재 `ACTIVE_PROVIDER=NONE / WATCHER_DISABLE=PASS_REPORTED / MIGRATION_NOT_CUTOVER` 유지. 기존 watcher 비활성화 GPT 판정 `GPT_DROPBOX_WATCHER_DISABLE_DISPOSITION_r0001_20261113.md` 및 `START_HERE.md` 최신 기준을 확인. 사용자 '다음 스텝 진행' 요청에 따라 **추가 서비스 중지 없이** 잔여 의존성 READ_ONLY 인벤토리 단계 준비.
- 현재 PRIVATE `collab/dashboard/`와 `.github/workflows/cowork-dashboard.yml`는 GitHub에서 별도 자동 갱신. Windows의 Dropbox Dashboard updater와 구분. PUBLIC Pages는 `L1Work` 별도 배포·허용목록/토큰 게이트가 있으므로 완전 자동 동기화 여부는 별도 판단.
- Windows에서 실제 조사할 3개: **Dashboard updater / Telegram notifier / Bridge**. 각각 TASK/PID/재시작 경로·input/output 및 다른 실행 기능 의존성, SHM 변경 가설, 스케줄과 서비스 공유를 운영 DB 직접 SQLite 오픈 없이 점검. 분류 `DROPBOX_REVIEW_ONLY / SHARED_OTHER_WORK / INDEPENDENT_REQUIRED / UNKNOWN`, 결과 `KEEP / RETIRE_CANDIDATE / BLOCKED_UNKNOWN`. **이 단계의 운영 변경=0**.
- 신규 Windows 단일 실행 인계: `WINDOWS_POST_DROPBOX_DISABLE_DEPENDENCY_AUDIT_ONE_SHOT_r0001_20261113.md` PRIVATE main 게시 및 remote readback PASS. 실행 보고 예정 `CLAUDE_POST_DROPBOX_DISABLE_DEPENDENCY_AUDIT_RESULT_FOR_GPT_20261113.md`.
- GitHub 문서 게시 자체로 Windows 호스트 검사/중지/ETW 관리자 실행이 시작되는 것은 아니다. `READ_ONLY_HANDOFF_PREPARED / WINDOWS_AUDIT=NOT_RUN`. 사용자 Claude Code에서 해당 정확한 repo/main/경로를 지시한 뒤 실제 결과 판정. 중지·Disable·재활성화/키·토큰 변경/유료 리뷰/GitHub LIVE 전환은 별도 승인.
- `C_OVERALL=PARTIAL`, `ETW=FAIL_UNTRUSTED_MEASUREMENT`, `RESTORE_READY=PARTIAL`, `INDEPENDENT_REVIEW=NOT_RUN` 유지. 이전 기록의 Dropbox LIVE 표현은 당시 이력이고 최신 ACTIVE_PROVIDER=NONE을 우선.


## GPT 최종 판정 — Dropbox 리뷰 감시기 비활성화 수용 (2026-11-13 KST)
- GPT가 `CLAUDE_DROPBOX_WATCHER_SAFE_DISABLE_RESULT_FOR_GPT_20261112.md`, CURRENT.md, TRACKER.json을 PRIVATE main에서 직접 재조회. **GPT_DISPOSITION=ACCEPT_WITH_LIMITATIONS / WATCHER_DISABLE=PASS_REPORTED / ACTIVE_PROVIDER=NONE**. Windows 현장 증거는 Claude 및 사용자의 자체 실측 보고이며 GPT의 실제 호스트 검사와 구분.
- 단일 Dropbox watcher 예약작업 Disabled, 런처·자식 PID 0, lock 해제, 중지 후 약 4분간 4개 지점 관측, 신규 모델/비용 0·누적 호출 카운터 61 유지. 기존 요청·결과·영수증 보존. 중지 후 DB main/WAL 복사 및 복사본 `integrity_check/quick_check=ok`, 진행 작업 0. **RESTORE_READY=PARTIAL**: 작업 정의 복원은 SKIP, 장기/재부팅/재로그인 확인 PENDING.
- DB SHM 수정 시각 변화 원인은 notifier 읽기 폴링으로 추정되나 독립 확인되지 않음. Dashboard updater/Notifier/Bridge는 계속 동작 보고되며, 이들 운영 구성요소 변경은 **미승인**. 운영 DB 직접 `mode=ro` 관찰도 SHM 영향을 줄 수 있어 경로 분리 조사 필요.
- `C_ETW=FAIL_UNTRUSTED_MEASUREMENT / C_OVERALL=PARTIAL`, `INDEPENDENT_REVIEW=NOT_RUN` 및 `CUTOVER=MIGRATION_NOT_CUTOVER` 유지. GitHub SHADOW는 자동 리뷰 LIVE가 아니며 지금은 provider 없음.
- GPT 판정서 `GPT_DROPBOX_WATCHER_DISABLE_DISPOSITION_r0001_20261113.md`, PRIVATE main 게시 및 remote readback PASS. `TRACKER.json`의 schema 외 값(`phase=DROPBOX_WATCHER_DISABLED_ARCHIVED`, `self_test=SELF_TEST_REPORTED`)을 유효 값 `DISPOSITION`, `NOT_VERIFIED`로 수정; Windows 자체 보고는 CURRENT에 보존. `collab/START_HERE.md`의 오래된 'Dropbox LIVE 동작 중' 문구도 최신 ACTIVE_PROVIDER=NONE으로 정정·readback.
- **다음 단계:** 남은 세 구성요소(Dashboard updater/Notifier/Bridge) 공용·Dropbox 전용 의존성 및 재기동 경로를 읽기전용 인벤토리화하고, 추가 Disable·삭제는 새로 명시 승인받기. 자동화/검증 외 GitHub LIVE 전환 금지.


## DROPBOX_WATCHER_SAFE_DISABLE_RESULT: WATCHER_DISABLE=PASS / ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER (Claude 자체 보고, 2026-11-12 KST)
- 결과: `CLAUDE_DROPBOX_WATCHER_SAFE_DISABLE_RESULT_FOR_GPT_20261112.md` (PRIVATE `main`, commit `e6e88524fc2bc562ed16966b8d15e5b7ae5ced1c`, 원격 readback은 이 절 게시 후 별도 확인). 자체 실측 보고이며 독립 리뷰가 아니다. GitHub LIVE 전환이 아니다.
- 실행: Claude 세션(비관리자)의 `Disable-ScheduledTask`는 액세스 거부로 변경 없이 중단했고, 사용자가 관리자 셸에서 검증된 스크립트 1개를 실행했다(작업 이름·동작 일치, 프로세스 정확히 2개, 리뷰어 자식 0, 유휴 구간 확인 후 Disable → Stop).
- 결과: 예약 작업 `Disabled`, 감시기 프로세스 0, 락 해제. 중지 전 진행 중·불확실·실패 작업 0, 모델 신규 호출 0(카운터 61 유지), 비용 $0. 중지 후 정지 상태에서 DB 일관 백업(main·WAL 해시 일치)과 복사본 복원 시험 통과(`integrity_check=ok`, 작업 COMPLETED 60·CONFLICT 1). 작업 정의 복원 시험은 새 작업 생성이라 SKIP(`RESTORE_READY=PARTIAL`).
- 변경하지 않은 것: 대시보드 갱신기·Notifier·Bridge(작업 정의 해시 불변, 같은 프로세스), Dropbox 원본 요청·영수증·ZIP·운영 DB 데이터. 백업과 작업 정의는 로컬 보호 폴더에만 있고 게시하지 않았다.
- 알아 둘 점: 새 Dropbox 요청은 자동 처리되지 않는다(`ACTIVE_PROVIDER=NONE`). 대시보드 갱신기는 계속 Dropbox에 게시하며 요청 상태는 더 이상 갱신되지 않는다. 복구는 작업 Enable 후 Start(관리자 권한, 별도 승인). ETW 게이트는 변경 없음(`C=PARTIAL`, `ETW=FAIL_UNTRUSTED_MEASUREMENT`).
- 다음 한 동작: GPT가 결과를 판정하고, 남은 Dropbox 의존 구성요소 처리와 GitHub 리뷰 경로 준비는 사용자 별도 승인 후 결정.

## 사용자 승인 — Dropbox 리뷰 감시기 안전 Disable (2026-11-12 KST)
- 사용자 “그래”를 직전 질문의 **Dropbox 리뷰 감시기만 안전 중지·기존 예약작업 Disable 및 DB/요청/리뷰/영수증 보존** 명시 승인으로 접수. 승인 기록 `USER_DROPBOX_WATCHER_SAFE_DISABLE_APPROVAL_r0001_20261112.md` (PRIVATE main, commit `ad300ef5f11c08224d4c48d9154d2306979dc8a0`, readback PASS).
- **Windows 원샷 실행 인계** `WINDOWS_DROPBOX_WATCHER_SAFE_DISABLE_ONE_SHOT_r0001_20261112.md` (PRIVATE main, commit `48b9f10d3ffa17349159fe4a93804958a51e1ce7`, readback PASS). 단계: 실제 task·프로세스 확인 → 인플라이트/REQUEST/READY/영수증/비용 중복 위험 확인 → 데이터·task 원본 무손실 백업/rollback 준비 → watcher 1개만 Disabled+Stop → PID 0/자동 재시작 차단/모델 호출 0/다른 컴포넌트 무영향 검증 → 결과 PRIVATE 게시.
- 백업 일관성·미정산 리뷰 안전성이 입증되지 않으면 fail-closed `BLOCKED`, 대상 watcher를 건드리지 않는다. 운영 DB main/WAL/SHM/로그/ZIP 원본·이력 삭제 및 PRIVATE 원본 반출 금지.
- Dashboard updater/Notifier/Bridge/Dispatcher, 그 외 예약작업 및 GitHub LIVE 전환, watcher 버전 설치·DB 이행·pythonw 전환은 **미승인/변경 금지**. `C_ETW=FAIL_UNTRUSTED_MEASUREMENT`, `C_OVERALL=PARTIAL`, `INDEPENDENT_REVIEW=NOT_RUN` 그대로 보존.
- 현재 **`WATCHER_DISABLE=APPROVED_NOT_YET_OBSERVED`**. 승인 문서 게시만으로 Windows 호스트 작업이 실행되지 않음. 성공 실측 후 `ACTIVE_PROVIDER=NONE`, `DROPBOX_WATCHER=DISABLED_ARCHIVED`, `CUTOVER=MIGRATION_NOT_CUTOVER` 기록 예정. 기존 실제 보고 마지막 LIVE는 Dropbox v0.1.5이며 현재 실행 여부 GPT 직접 미관측.
- 다음 한 동작: Windows Claude Code가 위 정확한 PRIVATE/main 인계서를 읽고 단일 실행, 결과 `CLAUDE_DROPBOX_WATCHER_SAFE_DISABLE_RESULT_FOR_GPT_20261112.md` 및 CURRENT/TRACKER 직접 게시·remote readback → GPT 최종 판정.


## GPT 판정 — ETW 재분석 실패·Dropbox LIVE 존치 재평가 (2026-11-12 KST)
- GPT가 최신 `CLAUDE_ETW_ATTRIBUTION_AND_C_FINAL_CHECK_RESULT_FOR_GPT_20261112.md` 및 CURRENT 원문 원격 재조회. 결과: `ACCEPT_WITH_CHANGE / C=PARTIAL_ACCEPTED / ETW=FAIL_UNTRUSTED_MEASUREMENT`. GPT 코드 9건 + 호스트 합성 22건 = **31 PASS(SELF_TEST_REPORTED)**, 실제 ETW time/ProcessStart 해석 실패로 C 실측 NOT_RUN. 운영 DB/WAL/SHM/lock 무접근 NOT_PROVEN.
- 50~55분 감시기·갱신기 단기 동작 관측 수용, `LONG_RUN=PENDING`. 관리자 셸 총 3회(새 trace 1회) 기록. 동일 ETW 관리자 재시험 반복 보류. `mode=ro` 운영 DB 관찰의 WAL/SHM 영향 미측정 문제와 GPT 코드 수명 밖 이벤트 silent drop/8.3 alias 미보장 이슈 후속 개선.
- 사용자 의견: Dropbox LIVE 협업 **실사용 종료**. GPT 권장 **운영 reviewer watcher Stop + Scheduled Task Disable, 로그/DB/WAL/SHM/요청/영수증/ZIP 보존**. 다만 사용자 명시 최종 중지 실행 승인 전 **`DROPBOX_DISABLE=PROPOSED_NOT_EXECUTED`**. Dashboard updater/Notifier/Bridge는 의존성 확인 전 자동 중지 금지.
- 실제 Dropbox LIVE 중단 후 새 GitHub LIVE가 승인되기 전 `ACTIVE_PROVIDER=NONE`으로 자동 리뷰 서비스 공백 발생 가능. 운영 이력/미정산 요청 안전성·롤백 확인 후에만 disable. GitHub SHADOW≠LIVE. `MIGRATION_NOT_CUTOVER` 유지.
- 상세 GPT 판정 `GPT_ETW_RESULT_AND_DROPBOX_LIVE_REEVALUATION_r0001_20261112.md`, PRIVATE main 직접 게시·remote readback PASS. 운영 호스트 변경/정식 독립 리뷰/새 토큰/키 발급/실 LIVE 전환 0. 다음 한 행동은 사용자 DropBox 감시기 안전 비활성화 승인 여부 확인.


## ETW_ATTRIBUTION_AND_C_FINAL_CHECK_RESULT: C=PARTIAL / ETW=FAIL_UNTRUSTED_MEASUREMENT (Claude 자체 보고, 2026-11-12 KST)
- 결과: `CLAUDE_ETW_ATTRIBUTION_AND_C_FINAL_CHECK_RESULT_FOR_GPT_20261112.md` (PRIVATE `main`, commit `1e7e79ff63baa325164f020fd3e275459a6c3fc8`, 원격 readback 확인은 결과 문서 게시 후 별도 기록). 자체 보고이며 독립 리뷰가 아니다. 관리자 셸은 사용자가 실행했다.
- 진단 코드: GPT 도구 SHA-256·Git blob 일치, GPT 9 PASS 재현. 호스트 정규화 도구와 시험을 추가해 합계 31 PASS(로컬 보존, 미게시).
- ETW: 사전검증 추적(새 추적 1회)은 수집 손실 0으로 수집됐으나 시간 열(`Clock-Time`)과 프로세스 시작 payload를 해석하지 못해 **POSITIVE_CONTROL_PREFLIGHT=FAIL_UNTRUSTED_MEASUREMENT**. 도구 결함과 실제 귀속 불일치를 구분하지 못함. 보존 원본 재분석(분류기 수정 후)도 FAIL. **C_FINAL_RERUN=NOT_RUN_PREFLIGHT_FAILED**, **C_ETW_OPERATING_FILE_ISOLATION=NOT_PROVEN**, **C_OVERALL=PARTIAL**. 관리자 셸 실행은 3회(1회차는 제 스크립트 버그로 P0에서 중단, 2회차 새 추적 1회, 3회차 새 추적 없는 재분석).
- 운영 지속성(읽기 전용): 재시작 후 감시기 약 55분·갱신기 약 50분 동안 신규 스캔/로그 증가, 프로세스 불변, `0xC000013A` 재발 없음. 두 관측 사이 관리자 시험이 있었으나 영향 없음. LONG_RUN=PENDING. MODEL_CALLS_NEW=0, USD_SPEND=0, ACTIVE_PROVIDER=Dropbox LIVE v0.1.5, INDEPENDENT_REVIEW=NOT_RUN, CUTOVER=MIGRATION_NOT_CUTOVER.
- 다음 한 동작: GPT가 C=PARTIAL 수용 및 보완 근거(비관리자 ACL 접근 거부 + SHADOW 코드 경로) 사용 여부를 판정하거나, 새 명시적 승인으로 보강 도구 1회 재분석(Clock-Time 자동 보정 또는 Get-WinEvent 직접 해독, 통과 시 C 실측 1회)을 허용. 승인 전 관리자 실행은 요청하지 않는다.

## GPT ETW 귀속 보완 및 C 조건부 최종시험 인계 (2026-11-12 KST)
- 상태: `GPT_DIAGNOSTIC_PREPARED / WINDOWS_HOST_NOT_YET_RUN / C_OVERALL=PARTIAL / MIGRATION_NOT_CUTOVER`. 사용자의 '진행' 요청을 ETW 사전검증·조건부 한 차례 실측·운영 지속성 읽기 전용 확인에 한정. 기존 Dropbox LIVE v0.1.5 유지.
- GPT 직접 **정규화된 ETW 이벤트/프로세스 lineage 검증** 보조 Python 코드 및 단위시험 2개 신규 작성. `tools/etw_attribution_preflight_r0001.py`(SHA256 `443755937d9eef7a34b84166a75aee31bdcf94721a2fe3a3ec16eeaa5f25eda8`), `tools/test_etw_attribution_preflight_r0001.py`(SHA256 `cbba9cab12f81a8e7d77e7354c7e4d49efc7619c603062a46a0182e6a3035d19`). 로컬 Python 표준 라이브러리 unittest **9 PASS / 0 FAIL**, GitHub PRIVATE main 각 파일 원격 내용·Blob 해시 로컬 원본과 일치.
- 테스트 내용: 같은 PID·입증된 자식 marker 정상, 다른 PID marker/무관한 subprocess/프로세스 PID 재사용/누락 provider·이벤트/시간 범위 오류는 fail-closed, 운영 경로 이벤트 있는 경우 차단. **실 Windows ETW 원본을 직접 해독한 것이 아니라 normalized 합성입력 시험**으로, 운영 SHADOW 무접근 PASS 증거 아님.
- Windows 단일 인계: `GPT_ETW_ATTRIBUTION_C_FINAL_CHECK_ONE_SHOT_r0001_20261112.md`, PRIVATE main 직접 게시/원격 readback PASS. 첫 단계는 기존 6개 관리자 전용 ETW 추적 재분석(원본 비반출)과 PID/TID·Kernel Process/File provider·양성 대조 귀속 사전 증명, 조건 충족 시 **관리자 ETW 실측 단 1회**, 실패 시 C=PARTIAL 유지.
- 기존 감시기/갱신기 안정성은 현장 조회 가능 시 읽기 전용으로 주기·로그 증가 확인, 장기(24h) 근거 없으면 PENDING; **재시작/예약작업 정의 변경/자동 감시 설정 미승인**. E 정식 독립 리뷰·키/토큰 발급·원본 ZIP 반출·운영 DB 이행·GitHub LIVE 전환은 NOT_RUN.
- Windows Claude Code 실제 실행은 GitHub 문서 게시만으로 시작되지 않음. 결과 예정 `CLAUDE_ETW_ATTRIBUTION_AND_C_FINAL_CHECK_RESULT_FOR_GPT_20261112.md`. PR 불필요, 단일 인계 후 Windows 로컬 실행→PRIVATE MD/CURRENT 게시→remote readback.


## GPT 운영 복구·C ETW 최종 판정 (2026-11-12 KST)
- 원격 원문 `CLAUDE_OPERATIONS_RESTART_AND_C_ETW_RERUN_RESULT_FOR_GPT_20261112.md`와 정정된 CURRENT 직접 확인. GPT 판정 **`ACCEPT_WITH_CHANGE / C_OVERALL=PARTIAL`**.
- 감시기 단기 복구 `PASS`(새 스캔 8회 이상/약 9분, 신규 리뷰 모델 호출 0), 대시보드 `PASS_AFTER_SECOND_START`(로그 3회 증가/5분 이상). **장기가동·재로그인 안정성은 NOT_RUN**. 첫 갱신기 종료 0xC000013A 원인 미확정. 인계서가 허용한 기존 작업 시작 1회를 초과한 2차 재시작은 **PROCESS_DEVIATION**으로 남기며 소급 승인하지 않는다.
- C 실 GitHub 읽기 전용 `PASS(HOST_REAL_REPORTED)`: 3주기 GET 7회, 쓰기/모델/Telegram 0. **C ETW `FAIL_UNTRUSTED_MEASUREMENT`**: 대상 자체 PID의 ETW 이벤트 0, 양성 대조는 다른 PID에만 나타나 프로세스/스레드 연결 확인 실패. 따라서 **운영 main/WAL/SHM/lock 파일 무접근은 NOT_PROVEN**, C 종합 PARTIAL 유지. 무조건적인 동일 관리자 시험 반복 중단.
- 후속 우선순위: 관리자 재시험보다 **ETW 양성 대조 PID/TID·자식 트리·Kernel provider와 event identity 사전 검증**, 조건 충족 시 한 번만 실제 재측정. 신뢰성 확보 안 되면 C=PARTIAL 유지하고 운영 ACL/정적 코드 구조는 보완 증거로만 사용.
- GitHub 게시 사고: 첫 CURRENT 한글 깨짐 커밋 `e0ca9838...` 뒤 올바른 `bcad4180...`로 교정됨, 현재 본문은 정상. UTF-8 원본 바이트 remote readback을 기본 필수로 적용. 게시용 과권한 `gh` 로그인과 시험용 Contents:Read-only PAT를 별도 관리.
- GPT 판정 문서 `GPT_OPERATIONS_RECOVERY_AND_C_ETW_DISPOSITION_r0001_20261112.md` PRIVATE main 게시/remote readback PASS. Windows watcher/DB/작업 정의/Telegram/토큰·키 변경하지 않음. Dropbox LIVE 유지 / 독립 리뷰 NOT_RUN / `MIGRATION_NOT_CUTOVER`.

## OPERATIONS_RESTART_AND_C_ETW_RERUN_RESULT: C=PARTIAL / 운영 복구 PASS (Claude 자체 보고, 2026-11-12 KST)
- 결과: `CLAUDE_OPERATIONS_RESTART_AND_C_ETW_RERUN_RESULT_FOR_GPT_20261112.md` (PRIVATE `main`, commit `404728eabfca8d24a74afa882d94360cce8e7689`, 원격 readback 바이트·SHA-256 일치 확인). 자체 시험 보고이며 독립 리뷰가 아니다. 사용자 승인 범위 안에서 실행했다.
- A 복구: 기존 감시기·대시보드 갱신기 예약 작업을 정의 그대로 시작. WATCHER_RESTART=PASS(마지막 스캔 21:36 KST 이후 신규 스캔 8회 이상, 모델 호출 0), DASHBOARD_RESTART=PASS_AFTER_SECOND_START(1차는 약 3분 뒤 같은 코드 0xC000013A로 종료, C 시험 시간대와 겹쳤으나 인과 미확정. C와 겹치지 않은 2차 시작은 5분 이상 생존, 로그 갱신). 종료 원인은 미확정이며 pythonw 전환은 승인 범위 밖이라 실행하지 않음.
- B C 재측정: C_REAL_GITHUB_READ=PASS(HOST_REAL, 3주기 GET 7회 200x5/304x2, 쓰기 0). ETW는 **FAIL_UNTRUSTED_MEASUREMENT**: 시험 프로세스의 자체 출력 PID에서 이벤트 0, 미끼 파일 열기는 다른 PID에서만 관측되어 양성 대조 실패. **운영 DB 무접근은 입증되지 않았다**(PASS 선언 금지). 원본 추적 파일은 관리자 전용 폴더에 보존, 게시하지 않음.
- 상태: C_OVERALL=PARTIAL, MODEL_NEW_CALLS=0, COST_INCURRED=0, SHADOW_ACCOUNT_RESTORED_DISABLED=PASS, DROPBOX_ACTIVE_PROVIDER=Dropbox LIVE v0.1.5 유지, INDEPENDENT_REVIEW=NOT_RUN, CUTOVER=MIGRATION_NOT_CUTOVER.
- 게시 정정 기록: 이 절의 첫 게시본(commit `e0ca9838754c334e53ffbc29e42d0ad9c16bb9d2`)은 한글이 깨진 채 올라가 같은 날 바로 이 정정본으로 교체했다. 결과 문서 본문은 영향 없음.
- 다음 한 동작: GPT가 C=PARTIAL 수용 여부를 판정. ETW 재측정이 필요하면 TID 교차검증과 프로세스 트리(Kernel-Process) 보강 후 사용자의 관리자 셸 실행 1회. 운영 변경·유료 리뷰·LIVE 전환은 여전히 미승인.

## 사용자 승인 — 기존 LIVE 운영 복구 + C ETW 재측정 (2026-11-12 KST)
- 사용자가 **리뷰 감시기/대시보드 갱신기 기존 예약 작업 재시작 + 수정 ETW C 계측 재실행**을 하나의 작업으로 명시 승인. 작업 정의·구성·계정·인증·운영 DB·LIVE 제공자 변경이나 신규 유료 리뷰 호출 승인 아님.
- 사용자 전달 호스트 보고: watcher 프로세스 0, 마지막 스캔 21:36 KST, updater 로그 11일 00:10 이후 없음, 두 작업 LastTaskResult 3221225786(0xC000013A; 콘솔 종료와 부합하나 인과 미확정), notifier/Bridge 정상. **호스트 실제 복구 여부는 아직 NOT_RUN/미확인**.
- C 사용자 전달: 실 GitHub GET 3주기/7회(200×5, 304×2) 읽기 전용 PASS 보고, 모델·쓰기 0. ETW 70,669건 중 대상 PID 이벤트 0, 양성대조 이벤트 0 → **ETW=FAIL / C=PARTIAL**, 운용 DB main/WAL/SHM 무접근 PASS 선언 금지. PID 자동 인식 수정은 문법검사만 PASS이고 재계측 NOT_RUN.
- GPT 원샷 Windows 인계: `GPT_WINDOWS_OPERATIONS_RECOVERY_AND_C_ETW_RERUN_ONE_SHOT_r0001_20261112.md` PRIVATE main PR 없이 게시 및 remote readback PASS. 사전 실행·중복 모델 호출 안전 확인 후 기존 작업 재시작(조건 불충족시 원상보존), 실제 새 scan/update 로그 확인, 양성대조 있는 ETW 실측, 결과 MD 및 CURRENT 갱신.
- 결과 예정: `CLAUDE_OPERATIONS_RESTART_AND_C_ETW_RERUN_RESULT_FOR_GPT_20261112.md`. **현재 문서 게시만으로 Windows 호스트에 시작 명령이 전달되거나 운영이 복구된 것이 아님.** 실제 실행은 사용자 Windows Claude Code의 단일 인계서 호출 필요.
- 기존 Dropbox LIVE 유지(`MIGRATION_NOT_CUTOVER`), GitHub 실제 REVIEW/READY·유료 reviewer·PUBLIC 배포 및 LIVE 전환 미승인.

## C_E_ONE_SHOT_RESULT: BLOCKED (Claude 자체 보고, 2026-11-12 KST)
- 결과: `CLAUDE_C_SHADOW_AND_E_REVIEW_ONE_SHOT_RESULT_FOR_GPT_20261112.md` (PRIVATE `main`, commit `ecef1a1ac9aaaebbb4cc98c55033d4eddaf380af`, 원격 readback 일치). Gate 0: v0.2.10 ZIP 로컬 재해시 174745B/70항목/SHA 일치. C 실GitHub SHADOW=BLOCKED_CREDENTIAL(읽기 전용 토큰 미배치, 과권한 기존 자격 재활용 안 함), B=BLOCKED_SIGNER_DEVICE, D=BLOCKED_EXPORT_CLASSIFICATION, E=BLOCKED(REQUEST/READY 0, 모델 호출 0, USD 0). 호스트 운영 변경 0, 시험 계정 비활성·샌드박스 보존. ACTIVE_PROVIDER=Dropbox LIVE v0.1.5 / MIGRATION_NOT_CUTOVER.

## C→E 원샷 후속 인계 준비 (2026-11-12 KST)
- 사용자 요청: C 실제 GitHub Contents read-only SHADOW와 E 정식 독립 리뷰를 **중간 핑퐁 없이 하나의 작업 지시로, 단계별 승인 게이트 충족 시 순차 수행**. 문서 작성/게시에 대한 요청이며 토큰 발급·키 설치·소스 반출·유료 reviewer 호출 승인으로 해석하지 않음.
- 새 Windows 실행 인계: `WINDOWS_C_SHADOW_TO_E_INDEPENDENT_REVIEW_ONE_SHOT_r0001_20261112.md` (PRIVATE main, commit `285efacbc4b53fc457599156f08ee3b5e5750250`, 원격 readback 내용 확인). 기존 Stage 1 A와 합성 C 시험을 재사용하고 v0.2.10(174745B; 보고 SHA-256 `67ea7fc63ccc1de77a28025b7c4f1b701ee6f4fa387311bca3f3d2bc7432b108`)을 리뷰 후보로 고정.
- C 실제 GitHub SHADOW: `BLOCKED_CREDENTIAL / NOT_RUN` (해당 repo 한정 Contents:Read-only fine-grained 토큰 미확보 보고). E 정식 리뷰: `BLOCKED/NOT_RUN` (운영 승인자 별도 기기 실키·34개 v0.1.5 유래 소스 반출 허가·독립 reviewer 경로 및 STATIC $1 실제 승인 확인 전 실행 금지). 모델 호출 0으로 유지하며 READY 게시도 금지.
- 현재 결과: `HANDOFF_PREPARED_NOT_EXECUTED`; `DEVELOPMENT=SELF_TEST_REPORTED`; `INDEPENDENT_REVIEW=NOT_RUN`; `CUTOVER=MIGRATION_NOT_CUTOVER`; ACTIVE LIVE는 Dropbox v0.1.5 보존. 운영 DB/F1/LIVE 전환/작업 스케줄/Telegram 변경 승인 없음.
- 다음 한 동작: Windows Claude Code에 위 PRIVATE `main` 인계 경로를 명시하여 Stage 1 후속으로 실행. 승인/권한이 없는 단계는 BLOCKED, 허용된 작업은 진행; 신규 결과 MD 및 CURRENT 최신 기록을 직접 게시·원격 readback한 뒤 GPT가 결과 판정.

관찰일: 2026-11-10 KST | work_id: COWORK-DROPBOX-TO-GITHUB-MIGRATION




## STAGE1_APPROVED_HOST_RESULT: PARTIAL (Claude 자체 시험 보고, 2026-11-12 KST)
- 결과: `CLAUDE_STAGE1_APPROVED_HOST_SECURITY_RESULT_FOR_GPT_20261111.md` (PRIVATE `main`, commit `221dd0f73f73f1d18bcc2b87f12f825e1631d12c`, 원격 readback 16115B 동일). A 비관리자 계정·ACL PASS(HOST_REAL); B 시험키 PASS / 실키 BLOCKED_SIGNER_DEVICE; C 비관리자 SHADOW 3주기 ETW 계측 PASS(운영 DB·WAL·SHM·lock 이벤트 0, GitHub 응답 SYNTHETIC, 실GitHub BLOCKED_CREDENTIAL); D ZIP BLOCKED_EXPORT_CLASSIFICATION(로컬 보존); E 독립 리뷰 BLOCKED/NOT_RUN(모델 호출 0). 33건 수집 차이=cryptography 의존 2개 모듈 35개 미수집−모듈 SKIP 2. 결함 3건 수정 → 후보 v0.2.10 (174745B, sha256 67ea7fc63ccc1de77a28025b7c4f1b701ee6f4fa387311bca3f3d2bc7432b108, 로컬). Dropbox LIVE 유지 / GitHub CUTOVER=NOT_RUN / INDEPENDENT_REVIEW=NOT_RUN.

## 사용자 1차 승인 접수·Windows 실행 인계 (2026-11-11 KST)
- 사용자 응답 `그래진행해줘`를 직전 GPT 1차 묶음 다섯 항목 승인으로 접수: `STAGE1_AUTHORIZED_WITH_GATES`. LIVE, F1 실제 처분, 운영 DB 이행, 기존 Dropbox LIVE watcher 작업·DB·예약 작업 변경 승인 아님.
- **승인 기록:** `USER_STAGE1_APPROVAL_RECORD_r0001_20261111.md` PRIVATE `main`, commit `24337b8effef0b154790a0843d281bba502dbb72`, 원격 readback PASS.
- **Windows 단일 실행 인계:** `WINDOWS_STAGE1_APPROVED_SECURITY_SHADOW_REVIEW_ONE_SHOT_r0001_20261111.md` PRIVATE `main`, commit `ae653ff69085586cbab17f2834b452e63a80346f`, 원격 readback PASS. 대상: 비관리자 시험 계정+관리자 전용 trust root ACL, 승인자 별도 장치 개인키, read-only 실제 호스트 SHADOW 3주기+I/O 실측, 파일별 반출 허가 후 PRIVATE ZIP, 유효 서명/비용 상한 `STATIC $1`의 정식 독립 리뷰 최대 1회.
- 단계별 조건: 별도 승인자 장치 및 운영 signer·trusted ACL·소스 반출 정책·독립 리뷰 runner/영수증 계약이 충족 안 되면 해당 항목 `BLOCKED/NOT_RUN`으로 중단, 모델 호출 0. 70개 파일 자체 비밀 검사 PASS는 회사 반출 허가를 대신하지 않음. SHADOW는 모델 호출/Telegram/remote write 0, 기존 운영 SQLite main/WAL/SHM 접근 0.
- Windows 실제 실행은 GitHub 문서 게시만으로 시작되지 않으므로 **`WINDOWS_STAGE1_EXECUTION=NOT_RUN`** (현재 관측). 결과 예정 `CLAUDE_STAGE1_APPROVED_HOST_SECURITY_RESULT_FOR_GPT_20261111.md`. 기존 v0.2.8 후보 ZIP 173615B, 보고 SHA256 `c6231cc329faff26c6e04a0ca454dec0d62a5eaaa0eb08edf9b6a57280f78daa`, 사용자 승인 실행 후 현장 검증 대기.
- GPT 직접 실행 범위: 승인·인계 MD 게시/재조회만 PASS, 호스트 계정·키·토큰·SHADOW 설치/실행·실 리뷰는 **NOT_RUN**. `INDEPENDENT_REVIEW=NOT_RUN`, `CUTOVER=MIGRATION_NOT_CUTOVER`, 기존 Dropbox LIVE 유지.
- **다음 한 동작:** Windows Claude Code 대화에서 새 원샷 인계서의 정확한 PRIVATE repo/main/상대 경로를 전달해 한 번 실행. 결과 MD 직접 게시·remote readback 후 GPT 판정. LIVE는 추후 별도 2차 명시 승인.


## GPT 최종 판정 — v0.2.8 전환 필수 게이트 (2026-11-11 KST)
- **GPT_DISPOSITION=ACCEPT_WITH_CHANGE / PRE_CUTOVER_READINESS=PARTIAL / CUTOVER=MIGRATION_NOT_CUTOVER**. 상세 판정 `GPT_V0_2_8_FINAL_PRE_CUTOVER_DISPOSITION_r0001_20261111.md` PRIVATE main 신규 게시·원격 readback PASS (commit `70f015c38f0072c8082d4afaf1b9c6bbf21d257a`).
- Claude 결과 `CLAUDE_CUTOVER_ESSENTIAL_GATES_RESULT_FOR_GPT_20261111.md`와 70개 파일 매니페스트 `REVIEW_INPUT_MANIFEST_v0_2_8_FOR_GPT_20261111.md`를 GPT가 원격 재조회. 최신 ZIP `skill-collab-watcher_v0_2_8_1111.zip` 보고 크기 173615B/SHA256 `c6231cc329faff26c6e04a0ca454dec0d62a5eaaa0eb08edf9b6a57280f78daa`. ZIP 로컬 보관/PRIVATE 미게시, GPT 원본 바이트 독립 검증 NOT_RUN.
- 코드·합성 시험 자체 보고 522 PASS/0 FAIL/12 SKIP, Windows 운영 인터프리터 487 PASS/0 FAIL/14 SKIP; 런북 불일치 및 시험 ZIP 타임스탬프 결함 수정은 조건부 수용. **시험 수집 수 차이**: 534 vs 501 (33건 차이)는 collect-only/skip 근거 추가 확인 필요. 폐기된 v0.2.6/0.2.7은 원본 보존.
- SHADOW S-1의 운영 DB 무접근 격리 설계/Windows 합성 tripwire/실 GitHub GET 7회는 수용, **실제 호스트 SHADOW 설치·파일 I/O 추적은 NOT_RUN**. 운영 DB를 과거 세션에서 열었을 때의 SHM 영향은 배제할 수 없음.
- **S-2 BLOCKED_TRUST**: 현 대화형 관리자 계정/프로필은 trust root·핀 변경권한을 가져 LIVE 독립성 검사 거부. 시험용 비관리자 계정, 관리자 쓰기 전용 신뢰 폴더, 승인자 개인키의 별도 기기 보관 및 실제 ACL 검증 필요.
- F1은 Dropbox WAIT_INPUT 그대로 보존(실제 HOLD/이행 NOT_RUN). DB 백업·이행·rollback·중복 알림 0은 격리 사본 리허설만 수용. `INDEPENDENT_REVIEW=NOT_RUN`, `HOST_SHADOW=NOT_RUN`, `PRODUCTION_CHANGED=false` (Windows 자체 보고).
- **다음 한 동작:** LIVE 제외 1차 승인 묶음(비관리자 계정/ACL, 승인자 키·신뢰 루트, 실제 호스트 read-only SHADOW, 파일별 반출 승인 뒤 PRIVATE ZIP, 비용 상한 $1의 독립 리뷰 1회)을 **명시적으로** 사용자에게 확인. 이후 운영 DB·F1 실제 처분·GitHub LIVE는 별도 2차 승인. 기존 Dropbox LIVE v0.1.5·운영 DB/예약 작업/Telegram/키/토큰 불변.


## Windows 실행 결과 — 전환 필수 게이트 G0~G4 (Claude 자체 시험 보고, 2026-11-11)
- 상태: `PRE_CUTOVER_READINESS=PARTIAL ; HOST_SHADOW=NOT_RUN ; INDEPENDENT_REVIEW=NOT_RUN ; DB_LIVE_MIGRATION=NOT_RUN ; CUTOVER=MIGRATION_NOT_CUTOVER ; PRODUCTION_CHANGED=false ; MODEL_CALLS=0`. 개발 자체 시험(SELF_TEST_REPORTED)이며 독립 리뷰가 아님.
- 결과 원문 `CLAUDE_CUTOVER_ESSENTIAL_GATES_RESULT_FOR_GPT_20261111.md`, 독립 리뷰 입력 자료 `REVIEW_INPUT_MANIFEST_v0_2_8_FOR_GPT_20261111.md` (실행 요청 아님). PRIVATE main, PR 없이 게시, 원격 바이트 재검증 완료. 이전 결과와 CURRENT 이력은 보존.
- 후보 `skill-collab-watcher_v0_2_8_1111.zip`, 173,615 bytes, SHA-256 `c6231cc329faff26c6e04a0ca454dec0d62a5eaaa0eb08edf9b6a57280f78daa`. Windows 로컬 보관, development_not_for_deployment, PRIVATE 게시 없음(반출 승인 대기). 이전 후보 v0.2.0~v0.2.5 불변, 중간본 v0.2.6·v0.2.7은 폐기 보존.
- 시험: 522 PASS / 0 FAIL / 12 SKIP (운영 인터프리터에서는 487 PASS / 0 FAIL / 14 SKIP). T 23 PASS·3 PARTIAL·12 NOT_RUN, S 10 PASS(시험 키). 간헐 실패 1건(시험 헬퍼 2초 경계)과 런북·코드 불일치 1건을 찾아 수정.
- S-1 해결: SHADOW는 운영 DB를 아예 열지 않음(자체 폴더·자체 DB, 경로 가드, 읽기 전용 전송, 실행 불가 러너). Windows 파일 핸들 tripwire와 실제 `watch` 명령, 실제 GitHub GET으로 격리 환경에서 확인. 실제 호스트 프로세스의 파일 I/O 추적은 NOT_RUN.
- S-2: 감시기 계정이 신뢰 루트·핀을 바꿀 수 있는지 검사하는 기능 구현. **이 호스트 구성(대화형 관리자 계정)은 LIVE에서 거부됨(BLOCKED_TRUST)**. 비관리자 실행 계정과 관리자 전용 신뢰 폴더 구성이 필요. 승인자 서명 도구와 제공자 시계 단조 증가 가드 추가.
- F1(READY 대기 요청)은 Dropbox에 그대로 보존. 이번 작업에서 운영 DB는 열지 않음. G4 리허설(스냅샷 사본)에서 보류 전환·롤백·복원·알림 중복 0 통과. 운영 DB 실제 이행·보류 실행·LIVE는 NOT_RUN.
- 필요한 승인 묶음(LIVE 제외): 실행 계정·폴더 구성, 승인자 키·신뢰 루트, 호스트 SHADOW(읽기 전용 토큰·I/O 추적), 소스 반출 분류 승인, 정식 독립 리뷰 1회. 이후 별도: 운영 DB 이행·F1 처분·LIVE 전환.
- 이 갱신은 상태 기록이며 READY 신호, 리뷰·과금·운영 변경 승인이 아닙니다.

## 전환 필수 게이트 원샷 통합 인계 (2026-11-11 KST)
- 사용자 요청: Dropbox→GitHub 전환에 실제 필수인 안전 게이트만 묶어 **Windows 개발/시험/후보·종합 결과 준비를 한 번에 수행**하고, 운영 전환 승인 직전까지 진행. **실제 운영변경·유료 리뷰·PRIVATE 소스 ZIP 반출·LIVE 전환 승인은 이번 '그래'에 포함하지 않음**.
- 통합 인계 **`GPT_CUTOVER_ESSENTIAL_GATES_ONE_SHOT_HANDOFF_r0001_20261111.md`** 를 PRIVATE `main`에 PR 없이 게시·원격 내용 readback PASS. commit `9a3c1a3780647f6f0e25a804268b6292b001694f`; 이전 `GPT_STAGE1_SHADOW_TRUST_REVIEW_ONE_SHOT_r0001_20261111.md`는 역사와 상세 참고로 보존하며 신규 실행 인계의 S-1/S-2에 통합.
- 후보 기준 정합화: **v0.2.5**(Windows 로컬, 보고 155288 B / SHA256 `40a1a944ec55d7414051374a67e264fd4fe03dadfcdead449ff37bac86dd93e6`)를 최신 개발 후보로 취급; v0.2.4(146879 B)는 기존 SHADOW/Trust 검토 이력. 둘 다 원본 ZIP GPT 직접 수령·바이트 독립검증은 NOT_RUN.
- 작업 범위: G0 현재 호스트 읽기전용 점검/F1 무손실 보존 상태 → G1 운영 DB main/WAL/SHM 미접근 SHADOW·B-7 신뢰검증의 **격리 코드 작업** → G2 회귀/신규 ZIP 무결성 → G3 독립 리뷰 **준비만** → G4 운영 DB 전환·복구·단일 LIVE의 **격리 리허설 자료**. 범위 밖을 `NOT_RUN/BLOCKED`로 기록하고 계속 수행.
- 재부팅 후 무로그온 실행 S4U, 스케줄러 변경, 일일 상한·Notifier 신규 기능은 **이번 필수 GitHub LIVE 전환 게이트에서 분리**.
- 새 Windows 결과 파일 예고: `CLAUDE_CUTOVER_ESSENTIAL_GATES_RESULT_FOR_GPT_20261111.md` (GitHub PRIVATE `main`, 비민감 결과, remote readback 필수). **Windows Claude Code 실행은 아직 관측되지 않음**. 현재 상태 `CUTOVER_ESSENTIAL_HANDOFF=PREPARED_NOT_EXECUTED`; `INDEPENDENT_REVIEW=NOT_RUN`; `CUTOVER=MIGRATION_NOT_CUTOVER`.
- 운영 Dropbox watcher v0.1.5·DB/WAL/SHM·예약 작업·Telegram·GitHub READY·모델 호출·PUBLIC·LIVE 전환은 이번 문서 정리로 변경하지 않음. 실제 host SHADOW, 서명키, 리뷰, DB 운영 이행, LIVE는 **개별 명시 승인 후**.
- **다음 한 동작**: Windows Claude Code 대화에서 새로운 통합 인계의 정확한 repo/branch/path를 지정하여 **단일 실행**. 미승인 차단을 제외한 작업은 끝내고 결과 MD 직접 게시·readback 후 GPT 판정과 승인 묶음 제시.


## GPT 판정 — 로그온 없는 시작 호환성 (2026-11-11 KST)
- 결과 원문 `CLAUDE_NO_LOGON_START_COMPAT_RESULT_FOR_GPT_20261111.md` 직접 확인. `COMPAT_STATUS=PARTIAL`, R01 PASS(READ_ONLY), R02 PARTIAL, R03 PASS(SYNTHETIC), R04 분석, R05 조건부 PASS(READ_ONLY), R06 계획만 수용.
- GPT 판정 `ACCEPT_WITH_CHANGE / HOST_LOGONLESS_E2E=NOT_RUN`; 상세 `GPT_NO_LOGON_START_COMPAT_DISPOSITION_r0001_20261111.md` PRIVATE main 게시·원격 readback PASS (commit `2f4e43e937dfc30e8943162d4b12f423e4c423d8`).
- 자동 로그인 비권장. S4U 우선 검증하되 Claude 인증 보호 저장소/실제 배치 실행 권한/암호 상태가 UNKNOWN. 암호 저장 방식으로 자동 fallback 금지. `claude_executable` 절대경로·WorkingDirectory 및 Notifier/Updater/Bridge 의존성 확인 필요.
- 별도 SHADOW 안전판정 S-1에 따라 SQLite mode=ro도 SHM 변경 가능. 현재 R05의 '변경 없음'은 운영 스냅샷 자체 보고이며 DB main/WAL/SHM 바이트 불변의 독립 확인은 아님.
- **운영 변경 0**: 기존 Dropbox LIVE watcher v0.1.5, 작업 스케줄러, 운영 DB/WAL/SHM, Telegram/Bridge/Dashboard, 토큰·키, Claude 모델 호출, GitHub READY, PUBLIC 배포, 실제 재부팅·무로그온 부팅 E2E 변경/실행 없음. 독립 리뷰 `NOT_RUN`.
- 다음 한 동작: 다른 SHADOW/신뢰 루트 보안 게이트와 충돌 없는 격리 시험 계획을 확정하고, 실제 시험용 작업 등록·부팅 E2E는 사용자 별도 명시 승인 후 진행.


## 최신 GPT 직접 실행 — 1차 SHADOW 안전 검증 (2026-11-11 KST)
- 상태: `STAGE1_PREP_SAFETY=PARTIAL / WINDOWS_HOST_NOT_RUN / MIGRATION_NOT_CUTOVER`. 사용자 '진행'을 1차 안전 검증 진행 지시로 반영함. **Dropbox LIVE 유지**, 운영 DB/Watcher/Task/Telegram/키/토큰/READY/유료 독립 reviewer 변경 없음.
- GPT 합성시험(실행 완료): `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/tools/shadow_isolation_preflight_r0001.py` — 4541 bytes, SHA256 `0550d4ddba6766ffa643f9fcf604a12271ebd5f7852e6b309046523525b7f811`. `5 PASS/0 FAIL`, 원본 WAL DB main/WAL/SHM 바이트 불변·상위/하위/symlink 경로 중첩 차단. 파일 GitHub PRIVATE 게시 및 raw readback PASS. **별도 합성 테스트**이며 v0.2.4의 410 자체 PASS에 더하지 않음.
- 설계판정 S-1: SQLite read-only `mode=ro`여도 SHM 변화 가능. 운영 LIVE SQLite 자체를 열지 않는 **완전 분리 SHADOW DB/상태 폴더**를 우선안으로 제안. 운영 host 실제 ProcMon/Windows file identity/비가변 접근 0 및 GitHub GET only 검증 아직 NOT_RUN. 별도 일관성 있는 snapshot 제작은 운영 권한/영향 검증 필요.
- B-7 신뢰 루트: signer key/신뢰 공개 루트/ACL 및 pin 독립성이 실제 Windows에서 확인되기 전 운영 승인 NOT_RUN. 운영 key 발급이나 token 생성은 하지 않음.
- **1차 Windows 통합 인계서**: `GPT_STAGE1_SHADOW_TRUST_REVIEW_ONE_SHOT_r0001_20261111.md` (PRIVATE main, PR 없이 게시·readback PASS). Windows 사용자 전달·호스트 실행은 아직 관측되지 않음. 결과 예정 `CLAUDE_STAGE1_HOST_SECURITY_RESULT_FOR_GPT_20261111.md`.
- 소스 후보는 여전히 Windows 로컬 v0.2.4 (146879 bytes, reported SHA256 `854d2d324033dac77771ed7145feabf0a659b3450d7b7579c54f487ae3f6ed20`). 외부 게시·실 ZIP 검증/코드 patch/호스트 회귀 수행하지 못함. 독립 리뷰 `NOT_RUN`.
- 2차 운영 DB 이행/F1 hold/실 GitHub LIVE cutover는 **명시적 후속 승인 없이는 미실행**.


## 최신 GPT 판정 — v0.2.4 최종 전환 준비 (2026-11-11 KST)
- 상태: **GPT_DISPOSITION=ACCEPT_WITH_CHANGE / PRE_CUTOVER_PARTIAL**. 운영 `MIGRATION_NOT_CUTOVER` / Dropbox LIVE 유지. 실제 GitHub 호스트 SHADOW, 독립 Claude 정식 리뷰/영수증, 운영 DB 이행/실 LIVE는 NOT_RUN.
- Claude 자체 보고 원문 `CLAUDE_FINAL_PRE_CUTOVER_GATE_RESULT_FOR_GPT_20261110.md`, 리뷰 입력 `REVIEW_INPUT_MANIFEST_v0_2_4_FOR_GPT_20261110.md` 재조회. 후보 `skill-collab-watcher_v0_2_4_1110.zip` (146879B, reported SHA256 `854d2d324033dac77771ed7145feabf0a659b3450d7b7579c54f487ae3f6ed20`, Windows 로컬). GPT raw ZIP/code 재검증 NOT_RUN.
- 개발 자체 시험 410 PASS/0 FAIL/12 SKIP, T 23 SYNTH PASS/3 PARTIAL/12 NOT_RUN, S 10 REAL TEST-KEY PASS. F1=정상 WAIT_INPUT이고 운영 pending 1건과 일치, 나머지 예외·거부 요청 설명됨. 실제 HOLD 처리/호스트 설치/리뷰 호출 없음.
- **중요 신규 위험 S-1:** SQLite `mode=ro` 사본 SHADOW에서 메인·WAL 불변이나 **SHM 파일 변화 관측**. 단일 LIVE·DB 무쓰기 요구에 맞는 SHM 처리 검증/일관된 격리 스냅샷 설계 없이 **실제 운영 호스트 SHADOW 승인 불가**. 사본 변화가 운영 DB 손상을 뜻하는 것은 아님.
- **S-2:** B-7 신뢰 루트 fingerprint/핀·Windows ACL·버전 래칫/시계 역행의 실제 독립성과 운영 signer 도구 미완성. 64항목 ZIP의 실제 바이트·반출 분류 및 정식 독립 리뷰 필수.
- **GPT 상세 판정:** `GPT_V0_2_4_FINAL_GATE_DISPOSITION_r0001_20261111.md` (PRIVATE main 게시, readback PASS). 1차 안전 승인 묶음(키/신뢰 루트, 안전 SHADOW, ZIP 게시 반출 승인, 유료 독립 리뷰 1회)과 2차 운영 DB 이행·GitHub LIVE 승인 분리.
- 실제 LIVE/운영 watcher·DB·예약작업·Telegram 변경 없음. REQUEST/READY 발행 또는 모델 호출 없음. 사용자에게 작은 인계 반복 요구 없이 승인할 항목을 묶어 보고.


## 지금 읽을 최신 상태 — GPT 단독 진행 (2026-11-10 KST)
- `MIGRATION_NOT_CUTOVER`: **Dropbox LIVE 계속 유지**, GitHub LIVE/SHADOW 운영 전환 미승인. Claude Code 토큰 사용 불가로 정식 독립 리뷰 `NOT_RUN`.
- GPT 직접 Dropbox 원격 메타데이터 검사: 요청 폴더 65개 → REQUEST/READY 정상 63쌍; **READY 없는 2개 폴더**. 한 폴더는 REVIEW_RESULT 형태 및 RECEIPT 파일이 존재, 다른 하나는 리뷰·영수증이 없음. **Windows 운영 DB pending 1건과의 연결은 UNKNOWN**. 운영 요청/DB 변경 0.
- GPT 직접 보안계약 정리 `GPT_B7_TRUST_ROOT_AND_APPROVAL_POLICY_DRAFT_r0001_20261110.md` (초안, 운영키·토큰·운영 venv 설치 없음).
- GPT 별도 오프라인 `skill-collab-github-review-gate_v0_1_0_1110.zip` 참조 코드 **41 PASS**. 구형 코드는 시간이 만료 후 뒤로 이동하면 서명이 다시 유효할 수 있는 시간 역행 검사 공백 있음. **Windows v0.2.3 재현 아님**.
- GitHub 고정 진입점 `collab/START_HERE.md` 오래된 Phase1 미시작 표기를 제거하고 `CURRENT.md`를 정본 포인터로 변경. `collab/ops/CONTRACTS/REVIEW_TRANSPORT_V1.md` 오래된 `review_attempt` 처리키 설명 주의 보충.
- **GPT 종합 원문:** `GPT_SOLO_PROGRESS_AND_CUTOVER_RISK_ASSESSMENT_r0001_20261110.md` (PRIVATE main, PR 없이 게시 및 원격 readback PASS).
- **최신 Windows 후보는 그대로** `skill-collab-watcher_v0_2_3_1110.zip`, 131400 bytes, Claude 보고 SHA256 `9a4201295156ea93b572f4a7d0f8bc6b566130c31c1cae72c55d6c8c8489cf41`, `development_not_for_deployment`; Windows 로컬 전용이라 GPT가 ZIP 소스 재검증·수정·테스트는 NOT_RUN. Claude 자체 시험 348 PASS/12 SKIP 및 C-4 Dropbox 정상 63쌍 비교 수용(기존 기록 참조).
- 남은 차단: (1) pending 1건/READY 없는 폴더 2개 운영 DB 연관성 확인과 무손실 정산·보존, (2) B-7 운영 신뢰 루트 실보안 검증, (3) 실제 호스트 SHADOW, (4) 정식 독립 리뷰/영수증, (5) 운영 DB 백업·이행, (6) 사용자 명시 LIVE 승인.
- 추가 사용자 핑퐁 없이 GPT 가능한 분석·설계·문서화 완료. **새 유료 모델 호출/REQUEST/READY/키발급/운영 변경/PUBLIC 게시 0**.

## 현재 상태
- P0-A 대상 구조: **PRIVATE + 기존 PUBLIC** 확정.
- P1 PRIVATE 저장소 생성/ChatGPT 연결: **PASS** — `wonhwipark/CoWork-Skill-Collab`, visibility `private`, default branch `main`, GPT `pull/push/admin` 확인.
- P1 기본 운영 폴더/안내 문서: **PASS** — README/START_HERE/운영 기준/계약/빈 이관 Manifest/리뷰·영수증·요청·패키지·대시보드 자리표시자 등 16개 파일(Windows 호스트 READ_ONLY 스크립트/인계 포함)이 PRIVATE main에 존재하고 원격 readback 확인. 실제 ZIP 및 요청 데이터는 0건.
- P0-B Dropbox 인벤토리: PARTIAL. 운영규칙 r0010/r0009/r0008, 게시 가드 확인. 원본 ZIP raw SHA와 전체 항목 분류는 NOT_RUN.
- P0-C ZIP/문서 공개 적합성 검사: 합성 입력 오프라인 단위시험 18 PASS(이전 실행), 실제 운영 ZIP 샘플 E2E NOT_RUN.
- Windows watcher 설치 v0.1.5: Claude Code가 일부 소스를 직접 확인했다고 원문 보고. 설정·이중 LIVE·전체 모듈·실제 adapter 통합: PARTIAL/NOT_RUN.
- GitHub transport adapter **Windows 실제 통합 구현/배포: NOT_RUN**. GPT의 보안 게이트 오프라인 후보 41 PASS는 기존 보고값이며 Windows 독립 재검증 NOT_RUN.
- Windows Claude Code **대화형 정적 검토 원문: PRIVATE main 게시·GPT 직접 읽음** (CLAUDE_STATIC_REVIEW_RESULT_FOR_GPT_20261110.md, 원격 blob 70593e0549448d27408b86fd05fe2a732656603c; Windows 보고 local/remote 22,700B 및 SHA-256 일치). BLOCKING B-1~B-7 판정 ACCEPT_WITH_CHANGE. 정식 REQUEST/READY 독립 리뷰/영수증: NOT_RUN.
- 실 GitHub 리뷰 파일럿/SHADOW/CUTOVER: NOT_RUN.
- PUBLIC L1Work 배포·사내 다운로드: 이번 이관 작업에서 NOT_RUN.
- Dashboard GitHub adapter/모바일: NOT_RUN.
- DEFAULT_REVIEW_MODE: SEMI_AUTO, Work AUTO_PENDING_SETUP 유지.

## 2026-11-10 운영 절차 결정
- **정규 협업에서 PR을 필수 절차로 사용하지 않음.** PRIVATE main의 직접 파일 게시+Commit A/B+서명/커밋/중복 검증으로 Dropbox와 동일한 REQUEST/READY 흐름을 구현한다.
- `collab/ops/CONTRACTS/NO_PR_COLLABORATION_V1.md`를 이 결정의 계약으로 사용한다. PR #1은 이전 설계 검토 자료로만 보존한다.
- Claude 정적 리뷰 B-1~B-7 전부 읽고 설계 r0002 반영. 우선순위 B-2(사이드카), B-5(실제 처리키·정책), B-3(중단/봉인), 이후 B-4/B-6/B-1/B-7. 전체 48개(T01~T38/S01~S10) 시험 명세 게시·개별 E2E는 NOT_RUN. 파일: GITHUB_ADAPTER_AND_REVIEW_FLOW_DESIGN_r0002_20261110.md 및 ACCEPTANCE_TEST_MATRIX_r0001_20261110.md.


## 2026-11-10 PHASE1 원샷 작업 합의
- 사용자가 반복 프롬프트 전달을 줄이기 위해 **1단계 Windows 개발·회귀시험·ZIP·결과보고를 단일 작업**으로 묶도록 승인함.
- 통합 인계: `PHASE1_WINDOWS_ONE_SHOT_HANDOFF_r0001_20261110.md` → **GitHub 게시 및 readback PASS**.
- **사용자 확인: 이전 Claude Code 실행 프롬프트는 전달하지 않았음**. 따라서 Windows 어댑터 구현·시험·패키징 실행은 여전히 `NOT_STARTED`; 새 인계서는 `PREPARED_NOT_DELIVERED`.
- 이 GitHub 문서 게시만으로 집 PC의 Claude Code 자동 실행은 시작되지 않음. 실제 시작은 사용자가 단일 짧은 실행 지시를 Claude Code 대화에 전달한 시점에만 가능.
- 운영 watcher, 인증·토큰·키, 정식 REQUEST/READY, PUBLIC 배포, PR 생성, LIVE 전환에는 변화 없음.

## PHASE1 Windows 개발 결과 및 GPT 판정 (2026-11-10)
- 사용자 전달/Windows Claude 실행: **DONE**. 이전 PREPARED_NOT_DELIVERED 상태는 과거 이력으로만 유지.
- 비민감 원문: `CLAUDE_PHASE1_IMPLEMENTATION_RESULT_FOR_GPT_20261110.md` PRIVATE main 게시 확인. 커밋 a3f30d85, Windows 보고 raw SHA-256 17e88579…/9694B, GPT는 원문 내용 확인(로컬 ZIP 미검증).
- 격리 코드 후보 `skill-collab-watcher_v0_2_0_1110.zip`: Windows 로컬에만, 108936 bytes, reported SHA256 1003c1aba21b8e6ac4db0ca599cadb9ba83950097e8eb82d97c9849a24b7ba52; `development_not_for_deployment`.
- pytest 보고: 272 PASS / 0 FAIL / 12 SKIP = Dropbox 232 PASS·12 SKIP + 신규 40 PASS. 기존 기준 236 PASS/8 SKIP 차이 미해명. T/S 48건 중 21 합성 PASS(일부 T20 및 S test-double), 27 NOT_RUN; 실 서명/실 API/독립 리뷰/LIVE 모두 NOT_RUN.
- GPT 판정: **PHASE1 ACCEPT_WITH_CHANGE / PARTIAL**. B-2/B-3/B-4/B-5/B-6/T08 조건부, B-1/B-7 실제 키·암호 라이브러리 운영 적용 보류. B-3 운영 DB 잔존 행 봉인, B-6 과거 READY 해시 호환 및 Telegram provider 표기 확인 필수.
- 단일 판정 원문: `GPT_PHASE1_DISPOSITION_AND_PHASE2_GATE_r0001_20261110.md`. 사용자 승인 전 운영 watcher/DB/task 설치·수정, cryptography 설치, 키·토큰 발급, SHADOW/LIVE, 공개 배포 금지.

## 이번 단계 범위
GPT가 Claude 리뷰 원문을 직접 확인한 뒤 r0002 설계 및 48개 시험 명세를 PRIVATE main에 PR 없이 게시하고 원격 readback 검증. 기존 Dropbox 요청/READY/영수증·watcher/Bridge/Dashboard/Telegram 변경 없음. 운영 ZIP/Public 게시 없음.

## 차단 및 승인
- Windows watcher 원문 검토 일부 완료; 미정독 세부 모듈 및 실제 권한/토큰 환경 추가 확인 필요.
- 파일별 반출 분류/원본 ZIP 실제 bytes 및 SHA-256 필요.
- 새 GitHub watcher를 LIVE로 바꾸려면 독립 Claude 리뷰/회귀시험 및 사용자 명시 승인 필요.
- PRIVATE `main` 브랜치 보호는 아직 확인/설정되지 않았으며 자동 운영 전 보강 필요.

## 최신 실행 계획 — PHASE2 원샷 인계 준비 (2026-11-10)
- 사용자 요구: 당분간 중간 피드백 없이 **보완→회귀·서명·가능한 실 API 읽기전용 검증→새 ZIP→PRIVATE main의 결과 MD 게시 및 원격 재검증**까지 하나의 Claude Code 작업으로 통합.
- 정식 인계: `PHASE2_END_TO_END_ONE_SHOT_HANDOFF_r0001_20261110.md` (**GitHub PRIVATE main 게시 및 내용 재조회 PASS**). GitHub 문서 게시만으로 Windows Claude Code가 자동 실행되는 것은 아님.
- 실행 상태: **PREPARED_NOT_DELIVERED / PHASE2_NOT_STARTED**. Windows Claude Code 대화에서 사용자가 통합 지시를 실행해야 시작.
- 격리 테스트용 Ed25519/암호 라이브러리: 통합 명령을 **명시적으로 전달할 때만** 일회성 시험 범위 허가. 운영 신뢰키·PAT·LIVE·유료 리뷰·PUBLIC 배포는 승인 대상에서 제외.
- 다음 결과 원문: `CLAUDE_PHASE2_END_TO_END_RESULT_FOR_GPT_20261110.md` (개발자 자체 시험이며 정식 독립 리뷰 아님). GitHub PRIVATE main에 PR 없이 올리고 readback 검증하도록 인계.
- 기존 Dropbox watcher/DB/예약작업은 변경 금지.

## 다음 한 동작
Windows Claude Code에 위 PHASE2 원샷 인계서를 **한 번만 실행**하도록 전달한다. 결과 원문을 PRIVATE main에 게시·재검증하면 GPT가 종합 판정한다. 차단 항목은 NOT_RUN을 기록하고 그 밖의 허용된 작업은 계속한다.

## PHASE2 원샷 실행 결과 (Claude 자체 시험 보고, 2026-11-10)
- 실행 상태: PHASE2_STATUS = PARTIAL. 정식 독립 리뷰가 아니며 INDEPENDENT_REVIEW=NOT_RUN.
- 결과 원문: CLAUDE_PHASE2_END_TO_END_RESULT_FOR_GPT_20261110.md (PRIVATE main, PR 없이 게시, 원격 바이트 재검증 완료, 커밋 fd2bfc58).
- 전체 시험: 312 PASS / 0 FAIL / 13 SKIP. SKIP은 실 Ed25519 모듈 1건(라이브러리 설치 권한 거부), GUI 옵트인 8건, 프로젝트 .venv 조건 4건.
- 인수시험 48건: T 38건 중 PASS(합성) 23, PARTIAL 3, NOT_RUN 12. S 10건은 테스트 더블 기준 PASS. 실 Ed25519 검증은 전부 NOT_RUN.
- 실 GitHub 읽기 전용 점검: PASS (GET만, 쓰기 없음).
- 후보 ZIP: skill-collab-watcher_v0_2_1_1110.zip, 125,653 bytes, SHA-256 d1e612fe70b34ec6e10109be58f95dfb79c9c620ff85e076152ae6d631aa0fd2. 로컬 보관, development_not_for_deployment, 공개 게시 없음.
- 모델 리뷰 호출 0회. 운영 watcher, 운영 DB, 예약 작업, Bridge, Dashboard, Telegram 설정 변경 없음.
- 미해결: 실 서명 라이브러리 설치 승인, Dropbox 실샘플 바이트 대조(B-6), 신뢰키 수명주기 정책(B-7), 운영 DB 스키마 적용 승인과 백업.
- 이 갱신은 상태 기록일 뿐 READY 신호나 리뷰 실행 승인이 아닙니다.

## 가장 최근 상태 — Windows v0.2.2 전달 결과 및 GPT 판정 (2026-11-10 KST)
- 사용자가 전달한 신규 Windows Claude 결과: **v0.2.2, pytest 314 PASS / 0 FAIL / 13 SKIP**, 격리 운영 DB 사본+실 GitHub 기반 전환/롤백 리허설 수행, WAL mode=ro 및 provider별 cursor key 분리 수정 보고.
- 후보: `skill-collab-watcher_v0_2_2_1110.zip`, **126729 bytes**, 보고 SHA-256 `7ec4f63e175b582ceec1f809281fba003f4248331a3f296689e7e19981323410`, Windows 로컬 `dist_phase2`. **GPT는 해당 ZIP·원문을 독립 검증하지 못함**. v0.2.2 상세보고서 아직 GitHub에 게시되지 않았다는 사용자 전달.
- 중요: PRIVATE에는 **이전 v0.2.1 Phase2 결과 원문(312 PASS/13 SKIP)이 이미 존재**, v0.2.2와 혼동·덮어쓰기 금지.
- 운영 전환 차단: Dropbox pending 요청 1건 무손실 인계 확인 실패, notifier 초기 구동 시 과거 event 65건 재발송 가능성, 실 Ed25519 NOT_RUN, 기존 Dropbox B-6 실샘플 NOT_RUN, 운영 DB 3개 table 추가 전 백업/승인 필요.
- GPT 판정 **ACCEPT_WITH_CHANGE / PARTIAL**, production watcher/DB/task 변경이나 GitHub LIVE/cutover 승인 아님.
- 통합 인계: `GPT_V0_2_2_DISPOSITION_AND_CUTOVER_READINESS_ONE_SHOT_r0001_20261110.md` GitHub PRIVATE main **게시·재조회 PASS**. 다음 Windows 작업은 격리 환경에서 남은 결함 수정, 시험키·암호 모듈 권한이 되는 경우 실 서명 S 시험, B-6 비교, pending/알림·DB 전환/롤백, 새 ZIP 패키징, **결과 원문을 GitHub PRIVATE에 직접 게시**까지 한 번에 수행.
- 현 단계: `HANDOFF_PREPARED_NOT_EXECUTED`. GitHub 문서 게시 자체는 Windows Claude Code에 대한 자동 실행 요청이 아니며 사용자 전달 전 새로운 실행 관측 없음.
- 기존 Dropbox LIVE 유지. 승인되지 않은 운영 신뢰키/PAT 생성·운영 DB 마이그레이션·실 유료 독립 리뷰·PUBLIC 게시·LIVE 전환 없음.

## 핑퐁 최소화 운영 결정 (2026-11-10)
- 사용자의 새 요구를 반영하여 v0.2.2 통합 인계서 `GPT_V0_2_2_DISPOSITION_AND_CUTOVER_READINESS_ONE_SHOT_r0001_20261110.md`의 **§5 핑퐁 최소화 실행 규칙**을 확정. **한 번 실행 → 허용 범위 내 수정·재시험 반복 → 새 ZIP → PRIVATE main에 결과 보고/remote readback → 사용자 최종 판정 요청 1회**.
- 중간 질문은 원칙적으로 중지하고 권한/보안·유료 모델 호출·LIVE cutover/PUBLIC 배포 등 승인 필요 사항은 마지막 보고서에 취합한다. 개발 Claude 자기 시험은 독립 리뷰가 아님.
- 현재 상태: **통합 인계서 업데이트 게시 및 재조회 완료, 신규 Windows 실행은 아직 관측되지 않음**. 운영 Dropbox watcher/DB/Telegram/task 변경 없음.

## v0.2.3 전환 준비 검증 결과 (Claude 자체 시험 보고, 2026-11-10)
- 상태: CUTOVER_READINESS_STATUS = PARTIAL. 정식 독립 리뷰가 아니며 INDEPENDENT_REVIEW=NOT_RUN. 운영 provider는 여전히 Dropbox LIVE.
- 결과 원문: CLAUDE_CUTOVER_READINESS_RESULT_FOR_GPT_20261110.md (PRIVATE main, PR 없이 게시, 원격 바이트 재검증 완료). 이전 v0.2.1 결과 문서와 CURRENT 이력은 보존.
- 후보: skill-collab-watcher_v0_2_3_1110.zip, 131,400 bytes, SHA-256 9a4201295156ea93b572f4a7d0f8bc6b566130c31c1cae72c55d6c8c8489cf41. 로컬 보관, development_not_for_deployment. v0.2.0/0.2.1/0.2.2 원본 불변.
- 시험: 348 PASS / 0 FAIL / 12 SKIP (GUI 옵트인 8, 프로젝트 .venv 조건 4). 후보 ZIP을 풀어 낸 사본에서도 동일.
- C-1 대기 요청 소실: 해결. 제공자별 대기 범위 분리, 정산 없는 전환 거부, 보류 전환은 감사·알림 기록. 사본 리허설로 보존 확인.
- C-2 알림 폭주: 해결. 제공자+epoch 워터마크, 초기화 없이는 발송 거부, 운영 notifier 위치 이어받기. 실 Telegram 발송 없음.
- C-3 실서명: 격리 가상환경 + 해시 고정 cryptography + 시험 키로 S01~S10 PASS(REAL). 운영 신뢰 루트·키 미생성.
- C-4 Dropbox 실샘플 B-6 대조: NOT_RUN (로컬 사본 없음, 원격 읽기는 보호된 자격 증명 필요).
- C-5 DB 이행: 온라인 백업 사본에서 이행·무결성·재개방·구버전 호환·복원 PASS. 운영 DB 무변경.
- 모델 호출 0회, 운영 watcher/DB/예약 작업/Telegram 변경 없음.
- 전환 차단 요건: C-4, 운영 신뢰 루트 수명주기(B-7), 정산되지 않은 Dropbox 대기 요청 1건 처리, 호스트 SHADOW, 독립 리뷰와 영수증, 사용자 명시 승인.
- 이 갱신은 상태 기록이며 READY 신호나 리뷰 실행 승인이 아닙니다.

## C-4 보충 (Claude 자체 시험 보고, 2026-11-10)
- C-4 Dropbox 실샘플 B-6 대조: PASS(REAL, 읽기 전용). 요청 63쌍에서 원본 바이트 해시, 재인코딩 해시, READY 선언값이 모두 일치 (불일치 0). BOM 0, CRLF 0, 비슷한 이름의 사이드카 폴더 0.
- 원문: CLAUDE_CUTOVER_READINESS_ADDENDUM_C4_FOR_GPT_20261110.md (PRIVATE main, 원격 바이트 재검증 완료). 이전 결과 문서의 C-4 NOT_RUN을 이 항목이 대체함.
- 열린 요건: B-7 운영 신뢰 루트, 정산되지 않은 Dropbox 대기 요청 1건, 호스트 SHADOW, 독립 리뷰, 사용자 명시 승인. 운영 변경·모델 호출 없음.

## GPT의 C-4 보충 판정 및 마지막 준비 통합 (2026-11-10)
- 원문 `CLAUDE_CUTOVER_READINESS_ADDENDUM_C4_FOR_GPT_20261110.md` 직접 재조회/판정: **C4_ACCEPT (정상 REQUEST/READY 63쌍의 실 Dropbox SHA 호환, 63/63 일치, 유사 사이드카 0)**. 실표본에 BOM/CRLF가 없어 해당 경로는 합성 근거만.
- 65개 중 쌍이 아닌 폴더 2개 원인과 운영 미정산 pending 1건 관련성은 UNKNOWN; 무손실 정산 확인 전 운영 LIVE 전환 차단 유지.
- GPT의 다음 단일 읽기 전용 준비 작업: `GPT_C4_ADJUDICATION_AND_REMAINING_GATES_r0001_20261110.md` PRIVATE main 게시/원격 readback PASS. pending 연관성 read-only 확인, B-7 운영 trust 설계, SHADOW 격리 시험 및 정식 독립 리뷰 입력 준비를 **한 번에 수행→결과 MD GitHub 직접 게시**.
- 운영 Dropbox LIVE 불변, v0.2.3 후보 ZIP 불변 (131400 bytes, SHA-256 9a4201295156ea93b572f4a7d0f8bc6b566130c31c1cae72c55d6c8c8489cf41). 운영 변경/정식 리뷰/실 모델 호출/호스트 SHADOW/LIVE/운영 DB 이행은 여전히 NOT_RUN.
- 상태: NEXT_HANDOFF_PREPARED_NOT_EXECUTED; Windows Claude Code에 지시 전달 전 추가 실행은 관측되지 않음.

## 최종 전환 전 게이트 결과 (Claude 자체 시험 보고, v0.2.4)
- 상태: PRE_CUTOVER_STATUS = PARTIAL. 정식 독립 리뷰가 아니며 INDEPENDENT_REVIEW=NOT_RUN. 현재 LIVE는 여전히 Dropbox.
- 결과 원문: CLAUDE_FINAL_PRE_CUTOVER_GATE_RESULT_FOR_GPT_20261110.md. 독립 리뷰 입력 자료: REVIEW_INPUT_MANIFEST_v0_2_4_FOR_GPT_20261110.md (실행 요청 아님). 둘 다 PRIVATE main, PR 없이 게시, 원격 바이트 재검증 완료.
- 미정산 대기 1건: READY를 기다리는 정상 대기이며 불완전 폴더 중 하나와 동일. 분실·중복 아님. HOLD로 보존. 나머지 불완전 폴더 1개는 완료된 작업(READY 제거 후), 쌍은 맞지만 작업이 없는 3개는 검증 단계에서 REJECTED로 종료된 건. 미설명 폴더 0.
- B-7 신뢰키 정책: 설계와 구현 완료(해시 고정, 버전 래칫, 폐기·회전·동결, 승인 수명 상한, 시계 검증, 파일 권한 검사). 운영 키 발급은 하지 않음.
- SHADOW: 운영 상태 폴더의 복사본과 실제 GitHub 읽기로 리허설 통과(GET만, DB 메인·WAL 동일, 운영 폴더 무변경). 호스트 설치·가동은 NOT_RUN.
- 후보 skill-collab-watcher_v0_2_4_1110.zip, 146,879 bytes, SHA-256 854d2d324033dac77771ed7145feabf0a659b3450d7b7579c54f487ae3f6ed20. 로컬 보관, development_not_for_deployment. 이전 후보 불변.
- 시험 410 PASS / 0 FAIL / 12 SKIP (GUI 8, .venv 조건 4). 실서명 S01~S10 PASS(REAL, 시험 키). 운영 모델 호출 0, 운영 변경 0.
- 남은 승인(묶음): 승인 키·신뢰 루트 부트스트랩, 호스트 SHADOW, 소스 ZIP 게시, 정식 독립 리뷰 1회. 그 뒤 별도: 운영 DB 이행, LIVE 전환.
- 이 갱신은 상태 기록이며 READY 신호나 리뷰 실행 승인이 아닙니다.

## 무인 리뷰 실행 준비 (Claude 자체 시험 보고, v0.2.5, 2026-11-11)
- 범위: 리뷰 자동 실행만. 개발 작업은 사용자가 시작. 상태: UNATTENDED_REVIEW_STATUS = PARTIAL. 정식 독립 리뷰가 아니며 INDEPENDENT_REVIEW=NOT_RUN. 현재 LIVE는 여전히 Dropbox.
- 결과 원문: CLAUDE_UNATTENDED_REVIEW_READINESS_RESULT_FOR_GPT_20261111.md. 독립 리뷰 입력 자료: REVIEW_INPUT_MANIFEST_v0_2_5_FOR_GPT_20261111.md (실행 요청 아님). 둘 다 PRIVATE main, PR 없이 게시, 원격 바이트 재검증 완료. 이전 문서와 CURRENT 이력은 보존.
- 추가한 안전장치: Claude 로그인 사전 점검(만료 시 요청 소모 없이 대기), 롤링 24시간 비용·횟수 상한(기본 꺼짐), 저장소의 PAUSE_REVIEWS 파일로 원격 정지, 감시기 정지 감지 알림. 모두 실패 시 '대기 + 알림'.
- 후보 skill-collab-watcher_v0_2_5_1110.zip, 155,288 bytes, SHA-256 40a1a944ec55d7414051374a67e264fd4fe03dadfcdead449ff37bac86dd93e6. 로컬 보관, development_not_for_deployment. 이전 후보 불변.
- 시험 448 PASS / 0 FAIL / 12 SKIP. 실제 CLI 사전 점검 PASS(모델 호출 없음). 운영 요청 65개 실데이터 차이 시험 64/65 동일(1건은 의도된 개선). 모델 호출 0, 운영 변경 0.
- 호스트 사실: 예약 작업은 사용자 로그온 시작(Interactive)이라 재부팅 후 로그온 전에는 실행되지 않음. 실패 시 3회까지 재시작.
- 미실행(승인 필요): 재부팅 후 무인 시작 구성(자동 로그인 또는 로그온 무관 실행), 일일 상한값 설정, 후보 설치와 재시작, 운영 notifier에 새 알림 연결. 구독 사용량 한도의 실제 오류 형식은 미관찰.
- 이 갱신은 상태 기록이며 READY 신호나 리뷰 실행 승인이 아닙니다.


## Windows 로그온 없는 시작 검토 인계 (2026-11-11)
- 사용자 지시: Windows 자동 로그인은 비권장; `시스템 시작 시 + 사용자 로그온 여부와 관계없이 실행` 대안을 **운영 설정 변경 없이** 우선 검토.
- 원샷 인계: `WINDOWS_NO_LOGON_START_COMPAT_HANDOFF_r0001_20261111.md` PRIVATE `main`에 PR 없이 직접 게시, 원격 readback PASS (commit `9935e5b5dd0295daf086c738d249965e11f867dc`).
- 상태: `HANDOFF_PREPARED_NOT_EXECUTED`; Windows Claude Code 시험 수행·결과 게시·진짜 로그온 없는 재부팅 E2E = `NOT_RUN`. 기존 v0.2.5 후보, 운영 watcher v0.1.5, 예약 작업, 운영 DB/WAL/SHM, Telegram, GitHub/Dropbox LIVE 변경 0.
- 인계의 허용 범위: read-only 스케줄러·인증 의존성 조회와 격리 synthetic 호환성 시험만. 스케줄 신규 등록·자동 로그인·자격 저장·재부팅·운영설치·모델 호출·READY·PUBLIC·LIVE 전환 금지.
- 다음 한 동작: 사용자가 Windows Claude Code 대화에서 새 인계서의 정확한 `main` 경로를 읽고 R01–R06을 단일 실행하도록 지시. 승인 필요 실제 호스트 시험은 별도 게이트로 분리.
