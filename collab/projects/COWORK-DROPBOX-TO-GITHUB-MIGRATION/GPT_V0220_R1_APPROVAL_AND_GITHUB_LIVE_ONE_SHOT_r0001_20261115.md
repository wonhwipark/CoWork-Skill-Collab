# GPT → Windows Claude Code: v0.2.20 R1 독립 리뷰 1회 → B1~B3 → GitHub LIVE 원샷

- 작성: 2026-11-15 KST · r0001
- **정확한 저장소**: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`
- **브랜치**: `main`
- **정확한 상대 경로**: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_V0220_R1_APPROVAL_AND_GITHUB_LIVE_ONE_SHOT_r0001_20261115.md`
- **Work ID**: `COWORK-DROPBOX-TO-GITHUB-MIGRATION`
- **사용자 명시 승인**: "v0.2.20 변경 부분에 대한 독립 R1 리뷰 1회(최대 $1)를 승인해. 기존 B1~B3 Windows 운영 변경 및 GitHub LIVE 전환 승인은 유지해. 리뷰 PASS 후 필수 검증을 통과하면 별도 재승인 없이 원샷으로 LIVE 전환해줘." / 이후 "진행해 윈샷으로".
- **확정 승인**: 신규 독립 리뷰 `R1` **1회·최대 USD 1.00**, `POLICY-STATIC-V1`; 과거 B1/B2/B3 Windows 운영 변경과 최종 GitHub LIVE 전환 승인 유지. **Classic PAT 계속 사용**. 같은 승인 재질문 금지.
- **현재 실제 상태**: GitHub 마지막 호스트 보고 `ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER`; `v0.2.20` 자체시험 PASS 보고·**독립 리뷰 NOT_RUN**·로컬 ZIP 미게시. **이 문서를 GitHub에 게시하는 것은 Windows 실행/유료 모델 호출/READY 생성/운영 변경/LIVE 완료가 아님**.

## 0. 선행 최신 정보

1. `collab/START_HERE.md`, 이 작업 `CURRENT.md` **최상단** 및 `TRACKER.json`, `GPT_V0219_R2_BLOCKING_DISPOSITION_AND_V0220_REVIEW_PLAN_r0001_20261115.md`를 우선 확인. 동일한 A/B 승인, LIVE 승인, Classic PAT 사용 결정은 다시 묻지 말 것.
2. 이전 v0.2.19의 독립 R2 `REQ-COWORK-V0219-R2-20261114`는 **이미 1회 종료**, 비용 `$0.9007163`, **BLOCKING 1**. 리뷰 원문: `collab/reviews/REQ-COWORK-V0219-R2-20261114/REVIEW_RESULT_1.md`. 기존 승인/READY/RESULT/영수증 재실행·수정 금지.
3. BLOCKING은 `github_transport.py:GitHubTransport.repository_id()`가 프로세스 전체 생명주기에 숫자 repo ID를 캐시, 동일 transport의 watch 반복 cycle에서 GitHub 서버 실제 ID 변경을 탐지하지 못한다는 N2 결함. v0.2.20은 캐시 제거+같은 transport 2회 scan 회귀로 수정(Windows 자체시험 보고).
4. 마지막 개발 ZIP `skill-collab-watcher_v0_2_20_1115_DEV_NOT_FOR_DEPLOYMENT.zip`: **239432 bytes**, SHA-256 `6a8626375e5e711535abdd261ff48781114802bb345cabe2ed5940b75968f386`, 93개 파일. venv `674 passed / 12 skipped`; Python 3.11.9 `607 passed / 17 skipped`(Windows 자체보고). ZIP은 **Windows 로컬 보관**이며 아직 GitHub PRIVATE 리뷰 입력 미게시. 자체시험 ≠ 독립 리뷰.
5. 기존 Dropbox 운영 DB: COMPLETED 60 / CONFLICT 1 / legacy pending 1 (`L1-KNOWLEDGE-ROADMAP-DESIGN-20261109-001`), 운영 DB main+WAL hash 원본 기준 보존. 이전 Notifier의 provider별 워터마크 개선은 비발송 격리 시험까지 완료, 실제 운영 설치 미실행.

## 1. A — **v0.2.20 독립 R1 딱 1회**, 최대 $1

- 새 고유 요청: `REQ-COWORK-V0220-R1-20261115`, revision 1, review attempt 1, `POLICY-STATIC-V1`(R1), **모델 호출 최대 1**, 총 승인 비용 상한 **$1.00**. 기존 v0.2.19 R2 예산 잔액을 재사용한다고 해석하지 않음. 재리뷰·추가 model/subagent 호출·정책 자동 승급 금지.
- Windows 로컬의 **현재 고정 v0.2.20 ZIP raw bytes, CRC, 필수 파일, 경로 이탈, 비밀 포함 여부**를 먼저 검사. 239432 B / SHA-256 위 값과 조금이라도 불일치 시 모델 호출 없이 `BLOCKED_TARGET_MISMATCH`로 중지. SHA 변경 시 기존 R1 승인으로 다른 ZIP 검토 금지.
- 허용된 CoWork 코드만 PRIVATE `main`의 `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/review-inputs/REV-COWORK-V0220-20261115/`에 **ZIP + 간결한 REVIEW_MANIFEST + diff(v0.2.19→v0.2.20)** 신규 게시, commit A에 내용 고정, **원격 원시 바이트 재조회+SHA+크기+CRC+commit readback** 일치 확인. 사용자 자료/운영 DB/토큰/개인키/회사 코드 업로드 금지.
- 서명은 **기존 Windows 운영 계약의 승인 서명 도구·신뢰 루트**로 생성. `REQUEST / APPROVAL_SIG / SOURCE_PIN`와 ZIP hash, fixed commit A, repo ID `1451933830`, 비용 정책, 만료, 중복 키를 검증한 뒤 **READY를 마지막에 게시**. 단순한 GitHub 텍스트 게시/쓰기 권한만으로 watcher를 호출하지 않음. 신규 REQUEST/READY가 다른 job을 재기동하지 않는지 확인.
- 독립 reviewer는 **개발과 분리된 명시적 리뷰 세션·입력·결과·영수증**으로 입증. R1 범위는 `repository_id()` 캐시 제거와 호출부, 동일 transport를 여러 WATCH scan에서 재사용할 때 정상 ID/다른 ID/조회불가/403·timeout의 fail-closed, N1 remote dispatch 예약/서명/비용·동시 실행에 미치는 회귀 영향만. 전체 v0.2.19 R2를 되풀이하지 않고 diff와 관련 테스트/콜사이트 중심으로 입력 압축.
- 실제 리뷰 결과 및 `RECEIPT_1`, `USAGE_RECEIPT_1`의 정확한 요청 ID/revision/ZIP SHA/비용/호출 횟수를 원격 readback. 모델 호출 1회 초과·비용 예산 초과 가능성·`REVIEW_UNCERTAIN`·중단/게시 실패 시 재호출 없이 정산/보류. 결과만 재게시 가능한 경우 publish-only 수행.
- 리뷰가 **BLOCKING 0이면서 GPT의 기존 운영 승인 범위에 부합하는 근거를 확보**한 경우에만 B1~B3로 진행. 독립 리뷰 FAIL/NOT_RUN/UNKNOWN/PARTIAL, 원격 ZIP mismatch, 새로운 BLOCKING 발생 시 **LIVE 중단, 추가 유료 모델 호출 0**. 수정 코드는 격리 사본에서만 가능하고 새 ZIP을 같은 리뷰 승인으로 다시 실행 금지.

## 2. B — 기존에 명시 승인된 Windows 운영 변경 3종 유지, R1 PASS 후 단일 작업으로

**B1. 운영 Python `cryptography` 설치/서명검증**
- 실제 Windows watcher 운영 Python 3.11.9 interpreter/환경을 읽어 확인하고 변경 전 백업. 기존 격리 리허설의 `cryptography 50.0.2`, `cffi`, `pycparser` 고정 해시 잠금/호환성을 원본과 재검증해 `--require-hashes` 방식으로 필요한 것만 설치(특정 버전/lock 무검증으로 강제 설치 금지). 실제 운영 host에서 Ed25519 정상·위조·변조·만료·다른 저장소·SOURCE_PIN 오류를 검증. 실패 시 설치변경 롤백 및 LIVE 금지.

**B2. Notifier provider별 DB·워터마크 개선**
- 기존 Notifier와 `last_id`·Task·설정 백업 후 기존 비발송 시험을 다시 수행. GitHub 신규 상태 DB에서 첫 이벤트가 누락되지 않게 provider별 last_id 초기화, 과거 Dropbox 알림 중복 발송 0, 신규 정상 알림 누락 0, 재시작/중복 프로세스 보호(락)와 rollback 검증. 단계적 설치·재시작은 승인 범위 안에서 실시. 테스트 Telegram 발송·과거 알림 재발송 금지. 설치 실패 시 기존 상태로 복원·LIVE 금지.

**B3. GitHub watcher 설치/Task 및 LIVE 단일 provider 활성화**
- **R1 PASS를 받은 정확히 동일한 ZIP 바이트**를 승인된 설치본으로 승격(정규 파일명으로 바꿔도 패키지 바이트 해시 동일성 확인), 별도의 GitHub watcher 상태 폴더/config/Task 생성·검증. 기존 Dropbox watcher는 Disabled 유지; 운영 Dropbox DB main/WAL/SHM·레거시 pending 1건을 보존하고 임의 전송·초기화·재리뷰/완료 처리하지 않음.
- 실제 Task/process/lease, 서명 승인 검증·repo ID 실조회·N1 원격 예약, 정책·비용 상한, 정상·오류 통과/거부를 호스트에서 확인. **활성 LIVE provider는 하나만**; 시작 전 Dropbox가 중지됐는지 재확인. GitHub watcher로 단일 전환 후 **2주기+재시작**을 확인하고 모델 재호출 0·완료 이력 중복 0·Telegram 중복/누락 0·리뷰 결과/영수증 remote readback과 rollback 준비를 확인.
- 실패/의심/복원 불가능 상태는 **fail-closed**: 새 GitHub provider OFF, 기존 DB/Task/Notifier 백업 보존, 무승인 Dropbox 자동 LIVE 복귀 금지. 추가 유료 reviewer 호출 금지. 디스패치용 실제 유료 모델을 새로 태워 smoke test하지 않음.
- Windows 관측값이 확인돼야 `ACTIVE_PROVIDER=GITHUB`, `CUTOVER=LIVE`, `HOST_APPLIED=PASS`. 리뷰 성공이나 GitHub 문서 게시만으로 LIVE 완료 선언 금지.

## 3. 최종 결과·판정

- 결과 파일 정확한 상대 경로: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CLAUDE_V0220_R1_AND_GITHUB_LIVE_ACTIVATION_RESULT_FOR_GPT_20261115.md`
- 반드시 구분: `A_REVIEW_REQUEST_ID`, `R1_MODEL_CALLS`, `R1_TOTAL_COST_USD`, `R1_FINDINGS`, `R1_INDEPENDENT_REVIEW`, `ZIP_SHA256_AND_SIZE`, `B1_CRYPTO_HOST`, `B2_NOTIFIER_WATERMARK`, `B3_GITHUB_WATCHER_TASK`, `N1_N2_RUNTIME`, `PENDING_1_PRESERVED`, `DROPBOX_PROVIDER_STOPPED`, `GITHUB_PROVIDER_SINGLE_LIVE`, `TWO_CYCLES_AND_RESTART`, `TELEGRAM_DUPLICATES`, `ROLLBACK_READY`, `ACTIVE_PROVIDER`, `CUTOVER`, `UNVERIFIED/BLOCKED`.
- 각 단계 `PASS/FAIL/SKIP/NOT_RUN/BLOCKED`; 자체시험·독립 리뷰·실호스트 적용의 증거 구분. **운영이 실제로 변경된 경우 반드시 변경 전후 DB(main/WAL/SHM)·Task·Process/Notifier·provider 상태 확인**. 모델 호출 한도/비용·승인 범위 초과 금지.
- 결과 MD와 `CURRENT.md` 최상단·`TRACKER.json`을 GitHub PRIVATE `main`에 **PR 없이 직접 게시**, commit·원격 내용·바이트 해시 readback. 신규 리뷰 결과/영수증도 별도 확인. 미게시/재조회 실패는 `NOT_POSTED/UNVERIFIED`.
- 공개 스킬 ZIP 게시, 운영 데이터·키 이동/교체, `/AI-CONTINUITY/` 변경, 새로운 정책·기능 확장은 범위 밖.
- 이미 승인한 R1(1회 최대 $1) 및 B1~B3·LIVE 전환을 **중간 승인 요청 없이 한 번에 실행**. 장애는 해당 지점만 `BLOCKED`로 보고하고 나머지 허용된 무비용 확인을 마쳐서 단일 결과 보고.

## Windows Claude Code 실행 문구

```text
GitHub PRIVATE wonhwipark/CoWork-Skill-Collab main의 collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_V0220_R1_APPROVAL_AND_GITHUB_LIVE_ONE_SHOT_r0001_20261115.md를 최신 단일 실행 계약으로 사용해줘. v0.2.20 고정 ZIP SHA256 6a8626375e5e711535abdd261ff48781114802bb345cabe2ed5940b75968f386 / 239432B를 검증하고 PRIVATE 리뷰 입력 게시·바이트 재조회 후 서명 유효 REQUEST/READY로 독립 R1 POLICY-STATIC-V1 리뷰를 정확히 1회($1 상한) 수행해줘. PASS일 때만 이미 승인된 B1 cryptography, B2 provider별 Notifier watermark, B3 GitHub watcher Task/별도 상태 설치를 한 작업으로 진행하고 실제 단일 GitHub LIVE 활성화·2주기/재시작/원본 이력/알림/롤백 확인까지 수행해줘. 실패/차단 시 중복 유료 모델 0, 원본 데이터 보존, ACTIVE_PROVIDER=NONE 유지. 과거 v0.2.19 R2·Classic PAT·기존 B/LIVE 승인 재논의 금지. 결과 CLAUDE_V0220_R1_AND_GITHUB_LIVE_ACTIVATION_RESULT_FOR_GPT_20261115.md와 CURRENT.md/TRACKER.json을 PRIVATE main에 직접 게시한 뒤 실제 commit·원격 바이트 readback까지 확인해줘.
```
