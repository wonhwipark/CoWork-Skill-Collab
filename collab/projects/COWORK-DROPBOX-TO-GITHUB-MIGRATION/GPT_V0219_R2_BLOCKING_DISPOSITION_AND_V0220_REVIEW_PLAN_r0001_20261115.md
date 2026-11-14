# GPT 판정 — v0.2.19 R2 BLOCKING 1건 / v0.2.20 최소 수정 및 LIVE 재개 게이트

- 기준일: 2026-11-15 KST · r0001
- 저장소: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab` / branch `main`
- 정확한 상대 경로: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_V0219_R2_BLOCKING_DISPOSITION_AND_V0220_REVIEW_PLAN_r0001_20261115.md`
- Work ID: `COWORK-DROPBOX-TO-GITHUB-MIGRATION`
- 호스트 실행 보고: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CLAUDE_V0219_R2_AND_GITHUB_LIVE_ACTIVATION_RESULT_FOR_GPT_20261115.md` (Git blob `409219e2aa3ce0fd6e7a66f3c4d235e7b76eb1d3`)
- **실제 독립 리뷰 원문**: `collab/reviews/REQ-COWORK-V0219-R2-20261114/REVIEW_RESULT_1.md` (Git blob `6d873ca0421ef63241c74586971848de7056821e`)
- **실제 영수증**: `collab/receipts/REQ-COWORK-V0219-R2-20261114/RECEIPT_1.md` (Git blob `bf4f8a8dc293e6437efbf39472a103addfdec6f8`); `USAGE_RECEIPT_1.json` (Git blob `e083e6f5d819e02537e19ee7cecb8df68f31420f`)
- **GPT_DISPOSITION=ACCEPT_BLOCKING_AND_FIX_PENDING_INDEPENDENT_REVIEW**
- `R2_V0219=COMPLETED_FAIL_BLOCKING_1`, `MODEL_CALLS=1`, `COST_USD=0.9007163`, `MAX_APPROVED_COST_USD=3.00`, `COST_BUDGET_RESPECTED=YES`
- `V0220_DEVELOPMENT=SELF_TEST_REPORTED_PASS`, `V0220_INDEPENDENT_REVIEW=NOT_RUN`
- `OPERATING_B1_B2_B3=APPROVED_BUT_NOT_APPLIED`, `LIVE_CUTOVER=APPROVED_BUT_NOT_APPLIED`, `ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER`.

## 1. GPT 독립 증거 대조

1. PRIVATE 원격의 독립 리뷰 원문, `RECEIPT_1.md`, `USAGE_RECEIPT_1.json`, 호스트 결과 MD와 최신 CURRENT/TRACKER를 재조회. 리뷰 request `REQ-COWORK-V0219-R2-20261114`, rev 1, package SHA `6e7fee3340cc6d0282d1c18fe3db42a90360259dd73fa6d7c0a7698af7afe5c0`가 일치.
2. 실제 reviewer 결과는 **BLOCKING 1**: `github_transport.py`의 `GitHubTransport.repository_id()`가 `self._repo_id`를 WATCH process lifetime으로 캐시해, 동일 `owner/name` 아래 GitHub 저장소 실제 ID가 바뀌어도 N2 승인 검사가 오래된 ID를 신뢰. `cli.py`의 run watch는 동일 transport를 계속 사용. 매 scan마다 새 transport로 테스트한 기존 N2 시험에는 이 결함이 숨겨졌음.
3. Claude 개발자가 캐시 결함을 두 번째 scan에서 **합성 재현**하고, 작은 수정으로 v0.2.20에 캐시 제거+same-transport 다중 scan 회귀 시험을 추가했다고 보고. 시험 `venv 674 PASS/12 SKIP`, 기본 운영 Python 환경 `607 PASS/17 SKIP`, FAIL 0 보고. 이는 **SELF_TEST_REPORTED**이며 독립 리뷰 결과가 아님.
4. v0.2.19 자체 reviewer는 독립 프로세스/독립 입력으로 수행, reviewer engine이 자동으로 원격 dispatch reservation·result·receipt 3건 PUT 했고 `COMPLETED` 처리. `USAGE_RECEIPT_1.json`은 별도 개발자 gh 게시이므로 **사용량 영수증 자체는 watcher 자동 게시 아님**.
5. 실제 GitHub create-only 경합 6 동시 쓰기 × 4번에서 승자 1/패자 409·422, 즉시 GET을 호스트가 추가 검증. 결과를 **HOST_TEST_REPORTED**로 수용하며 리뷰어가 직접 실행했다고 주장하지 않음.
6. 승인된 R2 호출 1회 및 비용 $0.9007163은 원격 사용 영수증과 합치. 실제 turns 27, output 20,963으로 R2 목표 미충족이나 `max_turns` CLI 미지원이라는 제한이 명시되어 있음. **호출 재시도 승인 여분으로 취급하지 않음.**
7. 운영 B1 cryptography, B2 Notifier provider watermark, B3 watcher Task 설치는 리뷰 BLOCKING 때문에 **미실행**. 기존 운영 DB main/WAL, 완료 60·CONFLICT 1·pending 1, 기존 Task/Notifier/Telegram 변경 없음(Windows 호스트 보고). 실제 LIVE 완료 아님.

## 2. 항목별 판정

| 항목 | GPT 판정 | 처리 |
|---|---|---|
| v0.2.19 R2 독립 리뷰 | **수용 / BLOCKING 1** | 정상 수행·비용·영수증 확인. PASS로 바꾸지 않음 |
| N2 캐시 결함 | **수용** | `repository_id()` 호출 간 캐시 수명, 1 transport / 2 scans 실제 repo ID 교체 테스트가 누락되어 명확한 수정 필요 |
| v0.2.20 최소 수정 | **수정 수용, 독립 리뷰 보류** | 캐시 제거는 원인에 부합. 기존 리뷰 결과의 PASS 소급 불가. v0.2.20 ZIP은 아직 LOCAL ONLY; GPT raw bytes/CRC 직접 검증하지 못함 |
| R2 원격 예약·결과·영수증 | **수용** | Watcher 최초 실 리뷰의 자동 게시 PASS. Usage receipt는 개발자 gh 게시로 따로 구분 |
| N1 원격 예약 경합 보강 | **수용(HOST)** | 실서버 병렬 create-only 단일 승자 보고. 장기 WATCH에서 N2 회귀 해결 여부는 미검증 |
| B1~B3 Windows 운영 승인 | **이전 승인 유지** | 사용자 승인했으나 BLOCKING 차단 때문에 0건 적용. **B 승인 재확인 요구 금지**; 동일 3종만 후보 리뷰 PASS 뒤 진행 |
| GitHub LIVE | **이전 승인 유지 / 미전환** | `ACTIVE_PROVIDER=NONE`, 실제 호스트 적용 0. 완료 허위 보고 금지 |

## 3. 단 하나 남은 새 승인: v0.2.20 좁은 독립 리뷰

- **유료 신규 호출 승인: 아직 없음.** 이전 A `v0.2.19` R2 1회 허용은 실행·정산되어 소진됨. `v0.2.20` 새 ZIP/새 SHA에는 재사용 불가.
- GPT 권고: 새 후보 **diff 중심 R1 / `POLICY-STATIC-V1` / 최대 USD 1.00 / 정확히 1회**로 범위를 압축. 변경 파일 `github_transport.py`의 `repository_id()` 캐시 제거와 테스트에서 같은 transport의 **2회 이상 scan**, 저장소 숫자 ID 변경, GET 403/404/timeout, N1 원격 예약·기존 서명/fail-closed 영향, 실 watch loop 재사용을 한정 검토. 좁은 수정이므로 기존 전체 ZIP을 다시 R2 심층 탐색하도록 하지 않는다.
- 호스트 보고 **잠정 대상**: `skill-collab-watcher_v0_2_20_1115_DEV_NOT_FOR_DEPLOYMENT.zip`, 크기 **239432 bytes**, SHA-256 `6a8626375e5e711535abdd261ff48781114802bb345cabe2ed5940b75968f386`, 93개 파일, CRC/secret scan PASS **호스트 자체보고**, **PRIVATE 리뷰 입력/REQUEST/READY 미게시, 독립 리뷰 NOT_RUN**. 사용자가 R1 비용을 승인하더라도 모델 호출 전 **로컬 원본 및 원격 고정 ZIP 실바이트/SHA/CRC와 diff**를 먼저 확인.
- 제안 리뷰 ID `REQ-COWORK-V0220-R1-20261115` rev 1. 동일 건 새 모델 호출 1, 최대 $1, 재호출 0, fail-closed. 유료 리뷰 실행은 **사용자의 명시적 신규 승인 후에만**.
- 새 리뷰 PASS/경미 지적 시만 이전에 **이미 승인된 B1→B2→B3**를 원샷 재개. 임의 신뢰키 변경, 운영 DB의 과거 pending 1건 재실행/이행, 새 PUBLIC 배포, 추가 리뷰 호출 금지. 실제 Windows 설치/Task/Notifier/2주기+재시작/실 알림 중복·누락 검증 이후에만 `ACTIVE_PROVIDER=GITHUB` 선언.
- 새 R1에 BLOCKING 또는 불확실/실패가 있으면 추가 유료 재리뷰 0, LIVE 미전환·원본 보존.

## 4. 다음 한 동작

사용자에게 **새 v0.2.20 R1 독립 리뷰 1회(최대 $1)** 승인만 받으면, Windows Claude Code는 (1) 고정 ZIP/원격 raw bytes 검증 → (2) signed REQUEST/READY 마지막 게시 → (3) 개발 세션과 독립된 리뷰 1회 및 receipts readback → (4) PASS 시 **기승인 B1~B3와 단일 GitHub LIVE 전환**까지 같은 명령 흐름으로 수행할 수 있다. Classic PAT 지속 사용 및 LIVE/B 재승인 재질문 금지.

**승인 전 실제 상태:** `V0220_REVIEW=NOT_RUN`, `B_APPLIED=NOT_RUN`, `CUTOVER=NOT_CUTOVER`, `ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER`.
