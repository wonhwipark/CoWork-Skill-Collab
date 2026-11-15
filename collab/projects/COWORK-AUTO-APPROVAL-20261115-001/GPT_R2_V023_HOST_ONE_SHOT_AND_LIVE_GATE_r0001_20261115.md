# CoWork 자동 승인 v0.2.23 — 독립 R2 → GPT 판정 → 조건부 LIVE 원샷 호스트 계약

- 2026-11-15 KST / r0001
- **정확한 PRIVATE 저장소:** `wonhwipark/CoWork-Skill-Collab`
- **브랜치:** `main`
- **정확한 상대 경로:** `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/GPT_R2_V023_HOST_ONE_SHOT_AND_LIVE_GATE_r0001_20261115.md`
- **Work:** `COWORK-AUTO-APPROVAL-20261115-001`
- **R2 신규 ID:** `REQ-COWORK-AUTO-APPROVAL-V023-R2-20261115`
- **기존 운영:** GitHub provider 단일 LIVE v0.2.20(Windows 호스트 마지막 실측 보고), `AUTO_SIGNING=OFF`, Dropbox reviewer Disabled.
- **사용자 최신 의사:** `그래 자동승인까지 진행해줘`. 기존 2026-11-15 한 번의 통합 승인과 합쳐 **v0.2.23 고정 바이트에 대한 단일 R2(최대 USD 3)와 R2·GPT PASS 조건부 Windows 운영 설치·보호 로컬 사전 위임 활성화** 범위에 한정. 불필요한 재승인·Telegram 매 요청 탭 불요. **GitHub 문서 자체는 Windows 보안 실행 권한이 아니다**. Windows 보호된 신뢰된 입력으로 승인 범위·예산 검증 불가면 해당 단계 BLOCKED, 진행한 것으로 보고하지 않는다.
- **중요:** GitHub에 파일을 게시한 것만으로 Windows 세션이 시작되지는 않는다. 기존 운영 Windows watcher v0.2.20은 승인된 `READY.md`가 없으면 R2 자동 모델 호출 0. 이 인계는 실행 가능한 Windows 호스트가 실제로 받았을 때만 동작한다.

## A. GPT가 완료한 원격 입력 고정 (실제 확인)

- **Commit A**: `8c90827ea6f0771331937d81c719697b322d4039`. 동일 커밋에 아래 파일을 게시:
  - `collab/requests/REQ-COWORK-AUTO-APPROVAL-V023-R2-20261115/REQUEST.md` (SKILL_COLLAB_REVIEW_REQUEST_V1, state SUBMITTED, revision 1, project/work `COWORK-AUTO-APPROVAL-20261115-001`, skill `cowork-review-watcher`, `POLICY-STATIC-V1-LARGE`)
  - `collab/packages/skill-collab-watcher_v0_2_23_1115_DEV_NOT_FOR_DEPLOYMENT.zip` (Git blob `0d7001798d402e5545833e6aaf8c5f4b9d2b8fbf`, **282340 B, SHA-256 `f941be8a6b53d00baa10a9b097f234b159470e2aa1242ecc33bcf0bdee080ea7`**; 이미 검증한 개발 후보를 그대로 Git blob 재사용, ZIP 원본 변경 없음)
  - `collab/requests/REQ-COWORK-AUTO-APPROVAL-V023-R2-20261115/OWNER_SCOPE_RECORD.md` (사용자 의사/위임 범위에 대한 **비인증 기록**, 자체 승인 수단 아님)
- **Commit B**: `e0e144cc56215b9d5d95cab77714186db6bf6662`, `collab/requests/REQ-COWORK-AUTO-APPROVAL-V023-R2-20261115/SOURCE_PIN.json`에 `repo_id=1451933830`, `commit=Commit A`, `schema=SKILL_COLLAB_SOURCE_PIN_V1` 고정.
- 세 근거 파일은 기존 Commit A 이전에 PRIVATE에 게시된 원본을 `knowledge_refs`로 연결·해시 고정:
  - `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/artifacts/v0_2_23/CANDIDATE_MANIFEST.md` SHA-256 `1af3bc61d2514e4ce0d33ed16eaae32ccd00e5001f5de9d9657f751d752f9acf`
  - `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/artifacts/v0_2_23/diff_v0_2_22_to_v0_2_23.patch` SHA-256 `30c5d7384c7df06f5ca9057a2c98aaedd2e19c0fba1d1fdc2fb6cdb0ae0a7aa0`
  - `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/artifacts/v0_2_22/diff_v0_2_21_to_v0_2_22.patch` SHA-256 `94bceec69410688f9c99dccf6e024ff6a0fb7be425e152361a7016b4d56f0ef8`
- GPT 재조회: REQUEST, SOURCE_PIN, OWNER_SCOPE_RECORD, package 모두 PRESENT. **APPROVAL_SIG/READY, DISPATCH, REVIEW_RESULT, RECEIPT 없음.** `REQUEST`는 `READY`가 없는 상태에서 모델 호출 트리거가 아님. 원본 ZIP·REQUEST·SOURCE_PIN 절대 덮어쓰기 금지.

## B. 실행 가능한 Windows 호스트 — 일괄 진행 순서 (중간 승인·왕복 최소)

1. `CURRENT.md` 상단 및 이 파일과 정확한 REQUEST/SOURCE_PIN/Commit A/ZIP/3 knowledge_refs를 **원격에서 최신 재조회**. 이미 동일 ID의 APPROVAL_SIG/READY/dispatch/result/receipt가 있는 경우 새 서명·모델 호출을 시도하지 말고 기존 결과 정산만; 불확실하면 `REVIEW_UNCERTAIN`.
2. 사용자 승인된 `v0.2.23 SHA`, `POLICY-STATIC-V1-LARGE` 최대 **USD $3/호출 1회**, 진행 시점 유효성·repo ID·정책/기존 지출·중복/만료를 **기존 운영 승인 시스템으로 검증**. 현 운영 Watcher 실제 일일 2회/$3 상한 등 더 엄격한 보호를 우회하지 말 것. 이번 R2는 **자동 위임 범위의 STATIC $1 규칙으로 자동 승인되는 대상이 아님**; 기존 승인 처리 경로만. 신뢰된 승인 채널이 GitHub 문구밖에 없거나 개인키/비용 검증 불가 시 `BLOCKED_TRUSTED_APPROVAL`, 요청/파일 보존, 호출 0.
3. 기존 host 검증을 모두 통과하면 `APPROVAL_SIG.json` 및 `READY.md`를 **기존 v0.2.20 계약 그대로** 준비한다. 구체 방식/포맷은 Windows 운영 도구 재사용; 원본 READY 바이트·해시를 보안 계약에 결속하고 검증한 뒤 원격 APPROVAL 게시·readback → **READY LAST** create-only·readback. 모호한 PUT/409/네트워크 응답은 remote exact byte 검증 및 publish-only, 원래 모델/서명 작업 임의 반복 금지.
4. 기존 GitHub LIVE watcher가 정확히 **1회** 독립 Claude R2 수행. `collab/dispatch/<ID>/DISPATCH_1.md`, `collab/reviews/<ID>/REVIEW_RESULT_1.md`, `collab/receipts/<ID>/RECEIPT_1.md`, `USAGE_RECEIPT_1.json`의 최신 경로/원본 bytes 검증, 실제 비용과 파일 SHA/요청 ID·revision 동일성 확인. REVIEW 결과/receipt가 미확실하면 모델 다시 호출하지 않고 `UNCERTAIN`과 누락 경계만 보고.
5. **독립 R2 결과를 GPT가 판정**하기 전에는 v0.2.23 운영 설치 또는 `AUTO_SIGNING` 활성화 금지. R2 BLOCKING=0이어도 자동 배포 완료로 승격하지 말 것; GPT 명시 PASS 및 동일한 패키지 SHA가 필수.
6. **R2 PASS+GPT 판정 PASS를 원격에서 실제 확인한 경우에만** 기존 승인 범위로 Windows v0.2.23을 적용: 정확한 기존 LIVE v0.2.20 Task/설치/DB main·WAL·SHM/Notifier/키·정책 백업/복원 준비, 신규 후보 SHA/CRC/보안검사, 기능 OFF 설치 및 기준 회귀 → 기존 대기 REQUEST가 소급 승인되지 않도록 첫 관측/시작 시각 확정 → Windows **보호된 로컬 위임**을 `enabled=true`, `expires_at=활성화+30일`로 구성 → 2주기/재시작/경합/비인가 호출 0·Notifier 이벤트 검사 → 실패시 즉시 `enabled=false` 및 보존한 v0.2.20 롤백. 단일 LIVE provider GITHUB 유지.
7. **사용자 승인된 보호 로컬 위임 값(새로운 리뷰만):** repo `wonhwipark/CoWork-Skill-Collab` main / server repo_id `1451933830`, project families 정확히 `COWORK-`, `L1-WORKSPACE-`, skills 정확히 `cowork-review-watcher`, `cowork-dashboard`, `l1-knowledge-updater`, `POLICY-STATIC-V1`만, 요청당 1 call/USD 1, 하루 ≤2 calls/USD 3, 월 ≤USD 10, 활성화일로부터 30일, 기존/소급 REQUEST 0. 이번 `POLICY-STATIC-V1-LARGE` R2는 이 위임 안에 넣지 말 것.
8. GPT 결과: `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/CLAUDE_V023_R2_AND_CONDITIONAL_AUTO_SIGN_LIVE_RESULT_FOR_GPT_20261115.md` (현재 상태→실행결과·commit/비용→실제 독립 리뷰 판정·영수증→host 백업·설치·운영·rollback test→NOT_RUN/BLOCKED→산출물 실제 SHA/위치→다음 한 동작). `CURRENT.md`·`TRACKER.json` 갱신, PRIVATE main 원격 readback. 로컬 실제 키·토큰·운영 DB는 게시 금지.

## C. 현재 사실 판정

`OWNER_AUTHORIZED_LATEST_TARGET=v0.2.23`, `REQUEST_POSTED=PASS`, `PACKAGE_POSTED_BLOB_IDENTICAL=PASS`, `SOURCE_PIN_POSTED=PASS`, `READY=NOT_POSTED`, `INDEPENDENT_R2=NOT_RUN`, `NEW_PAID_CALLS=0`, `LIVE_AUTO_SIGNING=OFF`, `GITHUB_LIVE_V0220=UNCHANGED`.

**NEXT_ONE_ACTION:** 이 문서를 Windows 실행 주체가 읽고 실제 보호된 host 승인/검증 → 1회 R2까지 진행해 결과·영수증을 게시. GitHub 글만으로 Windows를 원격 시작할 수는 없다. GPT가 리뷰 결과를 받은 즉시 동일 후보의 조건부 LIVE 적용을 판정·연결한다. 사용자에게 동일 비용·위임 범위·조건부 설치 승인을 다시 요청하지 않음.
