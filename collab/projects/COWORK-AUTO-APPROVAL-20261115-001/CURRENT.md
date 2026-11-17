# COWORK-AUTO-APPROVAL-20261115-001 — CURRENT

## v0.2.25 Windows LIVE 조건부 배포 완료: HOST_APPLIED=PASS_PARTIAL (2026-11-18 KST)

- 결과: `CLAUDE_V025_WINDOWS_LIVE_CONDITIONAL_DEPLOY_RESULT_FOR_GPT_20261118.md` (PRIVATE `main`, SHA-256 `c61dabd0b7a3a4e5f446fe811dffd557ef74800cc3a50ddb9ddc06d2d5838e80`).
- **설치:** v0.2.23 → v0.2.25(SHA `26d63c8a…213d228` 일치). 백업(DB/트리/설정/Task, 바이트 확인) → 안전 정지 → 원자적 교체 → 정책맵 `POLICY-STATIC-V1=1.50`, `-LARGE=3.00`(불변), `-DESIGN=3.00` 신규, 일·월 상한 `null` 유지 → 재시작.
- **검증:** 격리 회귀 963 passed/12 skipped/7 failed — 전부 비회귀로 근본 원인 확인(6건은 v0.2.25가 의도적으로 제거한 상한을 검증하던 구시험, 1건은 환경 플레이크로 단독 3/3 PASS). SHADOW 8/8 PASS. `review_request_gate.py`는 실제 GitHub LF 입력으로 정상 동작(select/check 모델·원격쓰기 0 확인); 자체 테스트 15/23 FAIL은 그 테스트의 Windows CRLF 하우징 결함(게이트 코드 결함 아님, 직접 재현).
- **2주기+재시작:** `dispatched=0`, 모델 호출 0, 신규 승인/중복 0, 단일 provider(github) 유지, 원격 변화 0.
- **미해결(별도 승인 필요):** 보호 위임 `auto_delegation.json`의 요청당 한도는 여전히 USD 1.00 — 1.50/DESIGN으로 올리는 구체적 승인이 이번 대화에 없어 **의도적으로 미변경**. 따라서 자동 서명은 아직 새 예산 체계로 동작하지 않는다(수동 승인 경로는 새 맵으로 즉시 사용 가능).
- 다음 한 동작: GPT가 위임 수치 변경을 승인할지, `test_review_request_gate.py`의 CRLF 테스트 하우징 수정을 채택할지 판정.

## 2026-11-18 KST — v0.2.26 Windows 플랫폼·Notifier 후속 원샷 인계 게시 (호스트 실행 별도)

- **사용자 지시:** `skill-collab-watcher` 후속 조치 “진행해줘”. [원샷 실행서](GPT_V026_WINDOWS_PLATFORM_AND_NOTIFIER_ONE_SHOT_r0001_20261118_KST.md)를 PRIVATE `main`에 게시하여 v0.2.25 기존 배포 현황 우선 확인→v0.2.26 Windows 전체 회귀/원본 실패 34개 재확인→기존 Notifier 어댑터 읽기 전용·합성 비발송 검증→결과 회수를 한 번에 인계. 기존 승인 v0.2.25 운영 배포 절차와 v0.2.26 개발 후보 시험은 분리.
- **현재 관측:** `CLAUDE_V025_WINDOWS_LIVE_CONDITIONAL_DEPLOY_RESULT_FOR_GPT_20261118.md` 원격 `NOT_FOUND`(GPT 조회 기준). v0.2.26 `development_not_for_deployment`, Linux 신규 회귀 61 PASS/가능 범위 974 PASS, 기준 실패 34개 제외. 기존 v0.2.25 단일 LIVE 조건부 승인·SHA는 불변.
- **변경 범위:** 원샷 MD + 이 CURRENT/파생 TRACKER 갱신만. Windows 호스트 시험·v0.2.25 실제 배포·v0.2.26 운영 설치·Notifier 실제 연계·신규 독립 유료 리뷰·REQUEST/READY/모델 호출 **이번 GPT 세션에서 NOT_RUN / 0회**. 원격 인계 게시만으로 Windows Claude Code 자동 실행은 발생하지 않음.
- **NEXT_ONE_ACTION:** 기존 Windows Claude Code 세션에 위 원샷 실행서 정확한 PRIVATE `main` 상대 경로를 **한 번** 전달하여 현장 검증·결과 파일 `CLAUDE_V026_WINDOWS_PLATFORM_AND_NOTIFIER_RESULT_FOR_GPT_20261118.md`·원격 readback까지 수행. 차단 게이트는 우회/재큐잉 없이 부분 결과로 회수.

---

## 2026-11-18 KST — REQUEST pin·보류 원인 재발 방지 v0.2.26 실제 구현·PRIVATE 후보

- **사용자 지시·실제 변경:** “해결하라고”에 따라 [구현·검증 결과](GPT_REQUEST_PIN_PREFLIGHT_AND_WAIT_FIX_RESULT_r0001_20261118_KST.md). 자동 예약 전/최종 승인/signer가 같은 pin 검증 사용, 숫자형 입력은 예약 전에 차단. 실제 AutoResult를 WAIT_INPUT 원인으로 연결, READY 성공 뒤 낡은 대기 알림 억제, 원인·다음 조치/실행·비용 미확인 표시와 중복 방지. 기존 prepublication 도구 2개/시험을 ZIP에 포함.
- **시험·후보:** 새 회귀 **61 PASS**, Linux 가능 회귀 **974 PASS / 35 SKIP / 원본 실패 34개 제외**. 기준 v0.2.25 전체 Linux는 913 PASS/34 FAIL/35 SKIP로 기록. 전체/Windows PASS 아님. [ZIP](artifacts/v0_2_26/skill-collab-watcher_v0_2_26_1118.zip) **308737 B**, SHA-256 `f08adb6099d06daf494362ed7e33ea66aabcbf749cfd2c027a7f70bcba5540fe`, CRC/경로/전집합 manifest/비밀 검사·재현 빌드 PASS. **development_not_for_deployment**.
- **운영·독립 구분:** v0.2.26 독립 리뷰·Windows 설치/운영 Notifier 연결 `NOT_RUN/NOT_VERIFIED`. 기존 v0.2.25 조건부 배포 승인·고정 SHA를 바꾸지 않음. 운영 키/DB/정책/위임/Task 변경 및 새 REQUEST/READY/유료 모델 호출 0. 기존 UNCERTAIN은 보존·자동 재큐잉 없음.
- **MSC 완료 회수:** 작업 중 기존 MSC R1의 서명/READY/DISPATCH/REVIEW_RESULT/RECEIPT와 GPT 판정 원문 직접 확인, bytes·결속 PASS. **COMPLETED / ACCEPT_WITH_CHANGE / 차단 0·권고 2 / 사이클 종료**. [연결 근거](artifacts/v0_2_26/MSC_CHAIN_VERIFICATION.json). 이번 코드 개발이 운영에 적용돼 리뷰를 재개시켰다는 인과는 주장하지 않음.
- **NEXT_ONE_ACTION:** Windows의 기존 v0.2.25 운영 작업 상태와 후보 플랫폼 시험·기존 Notifier 어댑터 연결을 확인해 회수. 이 개발 후보는 실제 게이트 충족 전 운영 설치하지 않음. MSC는 재리뷰 없이 종료 보존, Guard 정산 별도.

---

## 2026-11-18 KST — 사용자 조건부 Windows LIVE v0.2.25 배포 승인 / 원샷 인계 게시

- **사용자 승인:** GPT가 제안한 'Windows 격리시험 → 운영 백업 → 검증 PASS 시 v0.2.25 설치·단일 LIVE 활성화 → 두 주기/재시작 시험 → 실패 시 안전 롤백'에 사용자 “그래”. 같은 범위 재승인 불필요, 새로운 유료 리뷰·키/토큰 생성·DB 이행/공개 게시 금지.
- **실행 정본:** [GPT_V025_WINDOWS_LIVE_CONDITIONAL_DEPLOY_ONE_SHOT_r0001_20261118_KST.md](GPT_V025_WINDOWS_LIVE_CONDITIONAL_DEPLOY_ONE_SHOT_r0001_20261118_KST.md). Windows Claude Code가 이 한 문서로 설치 전 정책/위임/rollback 확인, SHA-256 고정 v0.2.25 ZIP 검증, 격리 회귀·SHADOW, 유효 보호 범위 내 설정 정합화, 안전 교체, LIVE 검증, 결과·영수증 게시까지 일괄 수행. USER_AUTHORIZATION=CONDITIONAL_DEPLOY, HOST_APPLIED=NOT_RUN.
- **이미 확인한 최신 G0:** v0.2.23 운영, v0.2.25 미설치. 보호 위임 max_request_usd=1.0 및 일 2회/$3/월 $10은 **계속 유효**로 보고되어 목표 $1.50/$3·상한 폐기와 충돌. 이번 배포는 실제 로컬에서 유효 보호 위임 변경 권한/승인 수단이 확인되고 모든 사전 게이트를 통과할 때만 활성화. 임의 위임/키 편집·정책 우회 금지. R2 M1은 패키지 외 사전 게이트 독립 리뷰 공백으로 별도 유지하며 유료 재리뷰 없음.
- **동작 경계:** PRIVATE 문서 게시만으로 Windows 호스트가 자동 실행되지 않음. 모델 호출/READY/패키지 재빌드·LIVE 설치 이번 GPT 세션에서 0. 실제 Windows 결과 `CLAUDE_V025_WINDOWS_LIVE_CONDITIONAL_DEPLOY_RESULT_FOR_GPT_20261118.md` 게시 및 원격 확인 전에는 LIVE_v025=NOT_RUN.
- **NEXT_ONE_ACTION:** Windows Claude Code에 위 원샷 인계서 **경로 한 번만** 전달하여 조건부 배포 작업을 끝까지 시행하고 결과·CURRENT·TRACKER를 PRIVATE main에 게시. 시험 실패 또는 위임 범위 미충족 시 안전 중지/롤백 후 BLOCKED 판정.

---


## G0 호스트 검증 완료 — v0.2.25 LARGE R2 후속 3항목 확인 (2026-11-18 KST)

- 결과: `CLAUDE_V025_LARGE_R2_G0_HOST_VERIFICATION_RESULT_FOR_GPT_20261118.md` (PRIVATE `main`, commit `6ef11fff87e9`, SHA-256 `104b09bb70b9a46b65823ba3c96fd1d12eff89bdc175f53b54120aff12652270`). 비용 보충 `USAGE_RECEIPT_1.json` commit `fb23472c07e0` (SHA-256 `47a24549b7dad2ce928ad1265cf06c42fe1a3233b8393367b778fbe946493f67`).
- **G0:** `review_request_gate.py`는 운영 v0.2.23 트리와 v0.2.25 ZIP 모두에 없음을 직접 확인 → `select/check NOT_RUN`은 오류가 아니라 정확한 결과.
- **운영 경계:** `daily_budget_usd`/`max_dispatches_per_day`가 실제로 `null`, 변경 전 백업 존재, 보호 위임 자체 한도(USD 1/2회 USD 3/월 USD 10) 불변 확인.
- **배포 게이트:** v0.2.25 미설치 그대로(`LIVE_v025_INSTALLED=NO`), 운영 버전 v0.2.23 변경 없음.
- 다음 한 동작: GPT가 `review_request_gate.py` 향후 리뷰 포함 방침과 v0.2.25 설치 게이트(격리 회귀·SHADOW·롤백) 착수 여부 결정.

## 2026-11-17 KST — GPT 독립 R2 최종 판정: ACCEPT_WITH_CHANGE (1사이클 종료)

- **정본:** [GPT 상세 판정](GPT_V025_LARGE_R2_DISPOSITION_r0001_20261117_KST.md). `REQ-COWORK-BUDGET-V025-LARGE-R2-20261117` rev1에 대한 REQUEST/서명/READY/DISPATCH/REVIEW_RESULT/RECEIPT 원격 내용·해시 대조. 실제 REQUEST SHA-256 `2e8cf16ace20a694851df98e339faa7e5d08d02d9149c9c2e518bd2206388066` 및 READY SHA-256 `7c2579cc003c9fb75d7cd85282fc2f694efd1db454ed47a88dcd3e33276a568d`가 승인 payload와 일치. 리뷰 결과 SHA-256 `8d682974537e06589a2fb11f41a4c48808a3c6a905bec4cfe2ab79f5477d0181`, `RECEIPT ok=true`, watcher 0.2.23.
- **판정:** `INDEPENDENT_STATIC_REVIEW=PASS_SCOPE_LIMITED`, `GPT_DISPOSITION=ACCEPT_WITH_CHANGE`, `REVIEW_CYCLE=CLOSED`, `DEPLOYMENT_READY=NO`. BLOCKING 0 / M1 1: review_request_gate.py·테스트는 고정 ZIP 밖으로 독립 리뷰 미수행(범위 공백, 코드 결함 아님). N1 레거시 정책 list 축소 예산은 주의, N2~N6은 리뷰어가 정적 읽기 확인. 새 유료 리뷰 요청/재호출 0.
- **비용:** Windows 호스트 USD 0.8061916/1회, 24턴 보고; GitHub 영수증 자체에 비용 필드 부재(`COST_INDEPENDENT_VERIFIED=NO`). 별도 운영 변경 보고로 `daily_budget_usd/max_dispatches_per_day` 제거(백업 있음), **변경 승인 범위는 GPT 미확인**. Windows `review_request_gate.py select/check` 실제 운영 사전검증도 `NOT_RUN`(기존 approve_request 점검과 별개). 과거 완료를 소급 PASS로 변경하지 않음.
- **NEXT_ONE_ACTION:** Windows Claude Code가 유료 호출·새 리뷰 없이 실호스트 정책/신규 REQUEST 게이트 경로 및 보고된 설정 변경의 유효 승인·백업을 읽기 전용 확인해 같은 Work에 증빙 게시. v0.2.25 호스트 시험/배포·LIVE 설치는 미승인/미검증 범위로 별도 유지.

---


## v0.2.25 독립 R2 완료 (LARGE $3, 수동 승인): BLOCKING 0·MAJOR 1(범위 공백) (2026-11-17 KST)

- 요청: `REQ-COWORK-BUDGET-V025-LARGE-R2-20261117` rev1, `POLICY-STATIC-V1-LARGE`, 패키지 `26d63c8a0329…` 283930 B. 수동 승인 도구 `approve_request.py`(16/16 점검 PASS, `review_request_gate.py`는 운영 트리에 없음)로 서명·READY 마지막 게시, 감시기(v0.2.23) 1회 실행·`COMPLETED`.
- 결과: [`REVIEW_RESULT_1.md`](../../reviews/REQ-COWORK-BUDGET-V025-LARGE-R2-20261117/REVIEW_RESULT_1.md) (SHA-256 `8d682974537e06589a2fb11f41a4c48808a3c6a905bec4cfe2ab79f5477d0181`), [`RECEIPT_1.md`](../../receipts/REQ-COWORK-BUDGET-V025-LARGE-R2-20261117/RECEIPT_1.md) `ok=true`, [`DISPATCH_1.md`](../../dispatch/REQ-COWORK-BUDGET-V025-LARGE-R2-20261117/DISPATCH_1.md). 비용 USD 0.8061916, num_turns 24, 모델 호출 1회.
- **BLOCKING 0.** **MAJOR 1(M1):** `collab/ops/review_request_gate.py`가 리뷰 패키지·file index에 없어 독립 검토 불가 — 코드 결함이 아니라 범위 공백. GPT가 포함 여부 판단 필요.
- **MINOR/관찰 6건**(대부분 확인 사항): 예산 파싱·NaN/Infinity 처리·일월 상한 제거 일관성·위임의 LARGE/DESIGN 자동서명 차단·신뢰 체인·미등록 정책 fail-closed 모두 리뷰어가 직접 읽고 확인.
- **운영 변경(사용자 지시):** 전역 일일 지출·횟수 상한(`daily_budget_usd`/`max_dispatches_per_day`)을 운영 설정에서 제거(백업 보존). 보호 위임 자체 한도(요청당 $1·일 2회 $3·월 $10)는 불변.
- 다음 한 동작: GPT 판정, 특히 M1(review_request_gate.py 검토 범위) 처리 방침.

## 2026-11-17 — 원샷 리뷰 재개용 기존 LARGE $3 신규 REQUEST 고정

- **신규 GPT 작성 REQUEST:** [REQ-COWORK-BUDGET-V025-LARGE-R2-20261117](../../requests/REQ-COWORK-BUDGET-V025-LARGE-R2-20261117/REQUEST.md) revision 1, `run_policy_ref=POLICY-STATIC-V1-LARGE`, `skill_id=cowork-review-watcher`, USD 3.00 최대, 동일 v0.2.25 ZIP SHA-256 `26d63c8a03290499b13b2ceb8ff0b70c06eb1b1bcc1a25fe3d8f65fcc213d228`, 283930 bytes. 이전 DESIGN 요청은 동작 없음/변조 없음/재큐잉 없음.
- **GitHub 실제 고정 및 readback:** commit A `d649921581c32fb5ed8e56b858f3881f029bca91`에 신규 REQUEST와 기존 Git blob `660ff3591defd8ccc4abdf3e9b2bf24f21b13918`인 ZIP이 존재하고 요청 정책 및 크기 확인. commit B `d1995fdfa4c3efc1f202f2b45b5132f938a39297`에 [SOURCE_PIN.json](../../requests/REQ-COWORK-BUDGET-V025-LARGE-R2-20261117/SOURCE_PIN.json) 게시, commit A 결속·repo_id JSON 문자열 `"1451933830"` 및 readback PASS.
- **실행/승인 상태:** 기존 Windows Claude Code 사용자 보고로 v0.2.23 로컬 `POLICY-STATIC-V1-LARGE` USD 3 등록 확인. 그러나 `review_request_gate.py`의 **이번 정확한 요청에 대한 Windows 실호스트 사전 CLI 검증은 NOT_RUN**. 원샷 수행을 위해 사용자 Windows 보고에 근거해 REQUEST만 먼저 고정했으며 **신규 필수 PREPUBLICATION 검증의 형식적 순서는 충족하지 못했다**. 절차 예외를 일반 PASS로 전환 금지. Windows에서 직접 `select/check` 및 원본 요청 bytes·SOURCE_PIN SHA 검증 **통과 전** 서명·READY·유료 실행 금지. 기존 운영 승인·서명·유효한 범위도 별도로 `approve_request.py check`로 확인. 요청 게시=유료 승인 아님.
- **한 번에 처리할 Windows 단계:** 실설정 정책 선검증 → 신규 REQUEST/SOURCE_PIN/원본 ZIP 검증 → 기존 유효 $3 수동 서명 `approve --max-usd 3.0 --execute` → READY LAST → watcher 1회 독립 R2 리뷰 → 결과/영수증 원격 readback → 동일 CURRENT 갱신. 사전 검증/위임 미통과 시 서명·READY·리뷰 0, 정확한 BLOCKED 근거만 게시. 기존 불확실 건과 DB/키/Task/LIVE 상태 수정 금지.
- **현재 판정:** `REQUEST=POSTED`, `SOURCE_PIN=POSTED`, `HOST_PREFLIGHT=NOT_RUN`, `APPROVAL_SIG=NOT_VERIFIED`, `READY=NOT_VERIFIED`, `INDEPENDENT_REVIEW=PENDING`, `LIVE_INSTALL=NOT_RUN`. GPT 최종 결과 판정은 실리뷰 결과가 게시된 다음 별도 권한으로 수행.
- **NEXT_ONE_ACTION:** Windows Claude Code가 신규 REQUEST ID의 정확한 입력으로 위 1회 순서를 끝까지 실행하고 원격 결과를 게시. 모델·비용 검증 없이 기존 DESIGN 요청을 재실행하거나 보호 위임을 수정하지 않음.

---


## 2026-11-17 — REQUEST 신규 게시 전 LIVE 정책 사전 검증 게이트

- **요청/원인:** 사용자 “정책사전검증 빠지지 않는 방안” 후 “진행해줘”. v0.2.25 리뷰에서 미설치 `POLICY-STATIC-V1-DESIGN`으로 REQUEST를 고정해 Windows v0.2.23이 서명/READY를 차단한 결함 재발 방지. 기존 동일 Work의 PREPUBLICATION 개발/검증만, 신규 리뷰 REQUEST/READY/비용/Windows LIVE 변경 없음.
- **실제 코드:** [`collab/ops/review_request_gate.py`](../../ops/review_request_gate.py) 신규. 실제 Windows 로컬 `reviewer.config.json`의 `review_policy.known_run_policy_refs`를 **반드시 입력**받는 `select`(호환 정책 선택)와 `check`(REQUEST 정확한 bytes SHA-256, ZIP SHA-256·크기·CRC·경로/심볼릭 링크, 기존 SOURCE_PIN 타입/commit 옵션 검사). 목적 `design`의 $3는 DESIGN 등록 시 DESIGN, 미등록이고 기존 `POLICY-STATIC-V1-LARGE` $3가 등록돼 있을 때만 LARGE 선택. 등록/금액 불일치·호스트 설정 없음·원본 불일치 시 exit 2/BLOCKED. `skill` 기본 $1.50 미지원 LIVE는 자동 업그레이드 금지/차단.
- **표준 절차 연결:** [기존 비용 계약](../../ops/CONTRACTS/REVIEW_TIER_TOKEN_BUDGET_V1.md), [AGENTS.md](../../../AGENTS.md), [CLAUDE.md](../../../CLAUDE.md)에 *REQUEST 작성 전 Windows LIVE read-only 조회 → draft 검증 PASS → 동일 원본 SHA의 commit A → SOURCE_PIN → 별도 Windows `approve_request.py check`/유효 승인·READY LAST*를 필수 절차로 명시. 기존 PRIVATE dashboard Actions에서 신규 테스트 자동 실행. 이 PREPUBLICATION PASS는 실제 서명/운영 보호 위임 승인이나 리뷰 실행이 아님.
- **실제 시험:** PRIVATE [CI #44093146832](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/44093146832) **SUCCESS**. 협업 ops unittest **36 PASS (신규 preflight 23 PASS + 기존 source-pin 13 PASS)**, dashboard **77 PASS**, 공개 미리보기 **8 PASS**. 테스트는 synthetic/local이며 모델 호출/Windows LIVE 0. 원격 CI 실제 bytes SHA-256: gate `08bcfd6633a16a1a3f57fdf896024756bdd32f52bf7154c359100ae6980b4eb1`; test `d2fcc4798e81c7d27004c5dc878e9c10c1e47d5566f431e2536b49ef1f41102b`.
- **한계/검증:** `HOST_INSTALLED_CONFIG_PREFLIGHT=NOT_RUN`, `WINDOWS_E2E=NOT_RUN`, `INDEPENDENT_REVIEW=NOT_RUN` (이번 신규 코드). 실제 Windows LIVE 정책의 내용·보호 위임은 GPT 접근 불가. PRIVATE `main`의 필수 status-check/브랜치 보호가 없는 환경에서 **모든 직접 GitHub API 쓰기를 코드만으로 차단하지는 못함**. 표준 작성 흐름의 CLI와 AGENTS/Claude 진입점에 fail-closed 검증을 도입했고, 기존 보호된 Windows 서명·READY가 최종 실행 차단. 이전 v0.2.25 DESIGN 요청은 여전히 BLOCKED, 변경·재큐잉 없음.
- **NEXT_ONE_ACTION:** Windows Claude Code가 **읽기 전용** 실제 호스트 설정에서 `select`를 실행해 설치 정책과 금액의 호환성을 확인·결과만 GPT에 전달. 이후 신규 REQUEST가 필요해지면 해당 원본으로 `check` PASS를 받은 다음 GPT가 게시. 신규 모델 호출/서명/설치·보호 위임 변경은 현재 범위 밖.

---


## 2026-11-17 21:09 KST — v0.2.25 독립 R2 리뷰 정책 미등록 BLOCKED (사용자 전달 Windows Claude Code 결과)

- **새 관측:** 사용자 전달 Windows Claude Code 점검: PRIVATE `main`의 최신 `421ef6524bf9`는 dashboard refresh, 이번 비용 정책과 무관. `REQ-COWORK-BUDGET-V025-DESIGN-R1-20261117`는 **미서명/미READY**. Windows Claude Code는 이번 REQUEST 본문을 읽거나 실행하지 않았다고 보고하며, 이전 정책 미등록 `BLOCKED` 상태 지속.
- **GPT 원격 직접 대조:** 해당 REQUEST 및 SOURCE_PIN 있음; 해당 APPROVAL_SIG, READY, REVIEW_RESULT, RECEIPT 없음. **정식 리뷰 요청 게시 ≠ Windows 실행/유효 승인 ≠ 유료 리뷰 개시**. `REVIEW_v025=NOT_RUN`; `REVIEW_ADMISSION=BLOCKED_POLICY_NOT_REGISTERED`. Windows LIVE 설치본·위임/DB/비용은 사용자 보고 이외 직접 검증하지 않음.
- **구조적 차단 원인:** 신규 `POLICY-STATIC-V1-DESIGN` / USD 3 등급은 미설치 v0.2.25 후보의 기능인데, 이를 v0.2.25 자기 리뷰의 REQUEST에 사용하여 기존 LIVE v0.2.23의 `POLICY-STATIC-V1`/요청 $1 보호 위임으로는 서명 불가. 원본 REQUEST/SOURCE_PIN/ZIP을 임의 변경하거나 READY를 위조해 우회하지 않음.
- **현행 TRACKER 정합화:** `TRACKER.json`의 기존 `phase=COMPLETE`, `independent_review=PASS`는 **v0.2.23 LIVE 및 과거 R2 시험의 역사적 상태**로서 v0.2.25에 적용하면 오표시. 이번 동일 Work의 현재 후속 작업만 `phase=BLOCKED`, `independent_review=PENDING`, `self_test=PASS`로 갱신. 과거 PASS 상세는 아래 이전 기록에 보존.
- **NEXT_ONE_ACTION:** Windows Claude Code가 과거 v0.2.23에서 실제 사용했던 `POLICY-STATIC-V1-LARGE` USD 3 **수동 서명/READY** 리뷰 경로의 현재 로컬 등록·보호 승인 범위를 먼저 읽기 전용 확인. 유효한 USD 3 독립 R2 **1회 승인**이 확인될 때에만 그 기존 등급으로 **별도의 신규 고정 REQUEST**를 합법적으로 준비해 v0.2.25 ZIP을 1회 리뷰; 미승인/미등록이면 BLOCKED 유지하고 필요한 정확한 승인·호스트 상태만 보고. 원래 DESIGN 요청은 미시작 이력으로 보존, 기존 동일 ID를 무단 재편집/재큐잉하지 않음. 독립 리뷰 완료 전 LIVE 교체 금지.

---


## 2026-11-17 v0.2.25 Windows Claude Code 독립 R2 리뷰 정식 요청 게시

- **요청:** [REQ-COWORK-BUDGET-V025-DESIGN-R1-20261117](../../requests/REQ-COWORK-BUDGET-V025-DESIGN-R1-20261117/REQUEST.md) / `request_revision=1` / `skill_id=cowork-review-watcher` / `POLICY-STATIC-V1-DESIGN` **디자인·보안 R2, USD 3.00 이내 1회**. 기존 [상세 인계서](CLAUDE_V025_BUDGET_POLICY_INDEPENDENT_REVIEW_HANDOFF_r0001_20261117_KST.md)와 최신 예산 r0002 재사용, 새 Work 생성/기존 REQUEST 재시도 없음.
- **Commit A 정식 고정:** `40cd39ceeb258cb93a238a4c81fdac1b6e687a61`에 `collab/packages/skill-collab-watcher_v0_2_25_1117.zip` **283930 B**, Git blob `660ff3591defd8ccc4abdf3e9b2bf24f21b13918`, SHA-256 `26d63c8a03290499b13b2ceb8ff0b70c06eb1b1bcc1a25fe3d8f65fcc213d228` 및 원본 `REQUEST.md`를 함께 원자 게시. PRIVATE development ZIP에서 동일 Git blob을 재사용했으므로 바이트가 동일하며 이미 [CI #44011874422](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/44011874422)에서 원격 SHA/CRC PASS.
- **[SOURCE_PIN.json](../../requests/REQ-COWORK-BUDGET-V025-DESIGN-R1-20261117/SOURCE_PIN.json)**: commit A `40cd39ce...`, repo_id JSON **문자열** `"1451933830"`. commit `e4f14b7970811cda5e6f6317fec186b703c1ac84`, 원격 readback PASS. 실제 commit A에서 REQUEST 텍스트·후보 Git blob/283930 B 재확인 PASS.
- **최신 원격 게시 상태 (조회 시점):** `REQUEST=POSTED`, `SOURCE_PIN=POSTED`, `APPROVAL_SIG=NOT_POSTED`, `READY=NOT_POSTED`, `REVIEW_RESULT=NOT_POSTED`; `INDEPENDENT_REVIEW=PENDING`. 현재 Windows LIVE v0.2.23 보고된 보호 위임은 USD 1/건 및 `POLICY-STATIC-V1`만, 이번 `POLICY-STATIC-V1-DESIGN` USD 3을 승인하지 못함. **실서명·모델 호출·비용 사용·실제 Windows 리뷰 시작 미확인**. 요청 게시 = Windows 호스트 직접 실행 또는 금액 승인 아님.
- **다음 한 동작:** Windows Claude Code가 이번 정확한 REQUEST ID 및 기게시 핀/ZIP을 읽고 기존 위임·서명 보호 범위의 현재 유효성을 점검하여 독립 리뷰 실행 가능성/차단을 기록. 보호된 LIVE 정책/키/DB/Task 변경이 필요하면 사용자 기존 승인 범위를 확인하고 승인 밖 작업은 BLOCKED. `READY`를 우회 작성하거나 구식 `POLICY-STATIC-V1` $1로 무단 다운그레이드해 실행하지 않음. 필요시 허용된 별도 독립 Windows 정적 점검을 유료 호출 0으로 수행하고 같은 Work에 결과 게시.

---



## 2026-11-17 최신 정책 — 일·월 상한 전면 폐기, 일반 스킬 $1.5·디자인 $3

- **사용자 최신 지시:** “상한 삭제, 디자인리뷰 3달러, 기본스킬 1.5 달러 추후수정가능하도록 변경해줘”. [최신 정책·개발 결과 r0002](GPT_AUTO_REVIEW_BUDGET_POLICY_r0002_20261117_KST.md)로 이전 건당 $1/일 $3/월 $10 r0001 **대체**. **일·월 리뷰 횟수/누적 비용 상한 모두 없음**, 요청당 일반 스킬 `POLICY-STATIC-V1` USD **1.50**, 디자인 `POLICY-STATIC-V1-DESIGN` USD **3.00**. 기존 요청마다 max_calls=1, UNIQUE/UNCERTAIN fail-closed, 서명/READY LAST, 프로젝트/스킬·만료/핀 확인은 그대로.
- **코드 수정:** 기존 Work/dev/auto-review-budget-policy-20261117에서 원본 v0.2.24 ZIP SHA 고정 → v0.2.25 빌더/테스트 및 `auto_policy/auto_approval/state_store/config/orchestrator`의 일·월 예산·횟수 게이트 제거. 실제 건당 예산 `--max-budget-usd`는 유지, `review_policy.known_run_policy_refs`의 **기존 로컬 설정 맵**으로 두 tier 금액을 후속 변경 가능. 디자인 tier는 로컬에 등록되고 **보호 위임 max_request_usd=3 이상**이 실제 허용된 경우에만 승인. 설정·위임이 현재 1달러라면 신규 금액의 LIVE 반영은 당연히 불가.
- **개발 후보 PRIVATE (PUBLIC NOT_POSTED):** `dev/auto-review-budget-policy-20261117`의 `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/candidates/skill-collab-watcher_v0_2_25_1117.zip`, 283930 bytes, SHA-256 `26d63c8a03290499b13b2ceb8ff0b70c06eb1b1bcc1a25fe3d8f65fcc213d228`, `DEVELOPMENT_NOT_FOR_DEPLOYMENT`. [결과 JSON](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/dev/auto-review-budget-policy-20261117/collab/projects/COWORK-AUTO-APPROVAL-20261115-001/candidates/AUTO_REVIEW_BUDGET_V025_BUILD_RESULT.json).
- **실제 개발 자체시험:** [CI 44011746881](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/44011746881) PASS: 표적 29 PASS/2 SKIP, Linux 지원 전체 582 PASS/30 SKIP/1 DESELECTED. [원격 실제 ZIP 재조회 CI 44011874422](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/44011874422) **REMOTE_BYTE_READBACK_PASS 283930 SHA 동일**. 실모델 호출/서명/READY 신규 생성/운영 설정·DB 변경 0.
- **독립 리뷰 인계:** [CLAUDE_V025_BUDGET_POLICY_INDEPENDENT_REVIEW_HANDOFF_r0001_20261117_KST.md](CLAUDE_V025_BUDGET_POLICY_INDEPENDENT_REVIEW_HANDOFF_r0001_20261117_KST.md) PRIVATE main 게시·원격 readback PASS. Windows Claude Code 독립 리뷰·Windows venv/SHADOW/복구 리허설은 **NOT_RUN**. 인계서 자체는 REQUEST/READY 또는 유료 리뷰 실행 승인이 아님.
- **상태:** `POLICY_DESIGN=COMPLETE`, `CODE_CANDIDATE=PRIVATE_BUILT`, `LINUX_SELF_TEST=PASS`, `REMOTE_SHA_VERIFIED=PASS`, `INDEPENDENT_REVIEW=NOT_RUN`, `WINDOWS_HOST_TEST=NOT_RUN`, `LIVE_CONFIG/PROTECTED_DELEGATION=NOT_APPLIED`, `LIVE_WATCHER_v025=NOT_INSTALLED`, `PUBLIC_RELEASE=NOT_RUN`. 마지막 확인된 LIVE 호스트 보고 v0.2.23, 기존 설정이 아직 실제 작동할 가능성 유지; 문서로 활성화 주장 금지.
- **NEXT_ONE_ACTION:** Windows Claude Code가 동일 Work의 고정 candidate를 독립 코드 리뷰·Windows 격리 시험하고 결과를 PRIVATE main에 게시. 운영 보호 위임/버전 설치는 정확한 별도 유효 승인·백업/롤백 조건과 시험 결과 확인 뒤에만. 과거 불확실 요청 자동 환급·재큐잉 없음.

---

## 2026-11-17 정책 변경 — 일·월 리뷰 횟수 제한 폐기 / 비용·중복 보호 유지

- **사용자 최신 지시:** 일/월 자동 리뷰 횟수 상한 컨셉 삭제. [GPT 비용만 사용하는 승인 정책](GPT_COST_ONLY_AUTO_APPROVAL_POLICY_r0001_20261117_KST.md) 확정. 과거 Windows LIVE의 `max_day_calls=2`는 당시 이력; 신규 정책에는 적용 금지. 요청당 1회/동일 REQUEST 재실행 금지, USD 1/요청·USD 3/KST 일·USD 10/KST 월, 서명/READY/위임 만료·프로젝트/스킬 정확 일치 유지.
- **수정 대상 직접 확인:** 원본 `v0.2.23` ZIP 282340 B SHA `f941be8a6b53d00baa10a9b097f234b159470e2aa1242ecc33bcf0bdee080ea7`에서 `auto_policy.py`의 COUNT 판단, `state_store.py::auto_claim`의 `DAY_CALL_LIMIT`, `auto_approval.py`의 입력·표시 사용을 확인. 실제 집계의 비용 예약은 그대로 보수 유지. `UNCERTAIN/POLICY_STOPPED`의 자동 비용 해제는 새 코드에서 수행하지 않음(증거 없이 해제 금지).
- **개발 후보 ZIP:** `dev/auto-quota-cost-only-20261117` / `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/candidates/skill-collab-watcher_v0_2_24_1117.zip`, 282548 B, SHA-256 `3c78699b734d88202a34ef5fd430f5f278ab1692a437b6affb6b6c64d24ca360`. 원본 고정 빌더·시험 코드 `dev/build_v024_cost_only.py`, `dev/patch_v024_tests.py`, branch CI `.github/workflows/cowork-auto-quota-v024-build.yml`. `DEVELOPMENT_NOT_FOR_DEPLOYMENT`.
- **실제 개발 자체시험:** [Actions #44002235785](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/44002235785) **SUCCESS**, 변경 표적 25 PASS/2 SKIP 및 Linux 허용 전체 회귀 578 PASS/30 SKIP/1 DESELECTED. KST 사용·원자 중복/비용 차단 코드 검사 PASS. Windows 전용 lock/SHADOW 사례는 Linux에서 제외되어 **WINDOWS_FULL_REGRESSION=NOT_RUN**. 실서명/유료 모델 호출 0.
- **계약 게시:** [이전 자동 승인 설계의 최신 결정](AUTOMATIC_SIGNING_MINIMAL_DESIGN_r0001_20261115.md), [공통 비용/리뷰 예산 계약](../../ops/CONTRACTS/REVIEW_TIER_TOKEN_BUDGET_V1.md)에서 기존 횟수상한의 현행 적용 해제. PRIVATE main 문서 반영만 수행했으며 **설치된 LIVE v0.2.23 / Windows 로컬 보호 위임·DB·키/Task·Notifier는 불변**. 새 REQUEST/READY/독립 유료 리뷰 미생성.
- **판정:** `COUNT_POLICY_DESIGN=REMOVED`, `CANDIDATE=BUILT_PRIVATE`, `LINUX_SELF_TEST=PASS`, `INDEPENDENT_CODE_REVIEW=PENDING`, `WINDOWS_HOST_TEST=NOT_RUN`, `LIVE_COUNT_LIMIT_REMOVAL=NOT_APPLIED`, `PUBLIC_RELEASE=NOT_RUN`.
- **NEXT_ONE_ACTION:** Windows Claude Code가 같은 브랜치 고정 후보의 바이트·SHA 및 소스 diff를 독립 확인하고 Windows 운영 인터프리터 전체 회귀·격리 SHADOW·롤백 리허설 후 코드를 독립 리뷰. PASS/유효 승인 범위 확인 전 LIVE 교체 금지. 기존 `REQ-L1-WORK-KNOWLEDGE-GUARD-CODE-R1-20261117`의 미정산 예약은 자동 재큐잉하지 않음.

---

## 새 SOURCE_PIN repo_id 포맷 오류 보정 — 로컬 AUTO_SIGNING_UNCERTAIN 정산 대기 (2026-11-17 KST)
- **원인:** Windows Claude Code 보고 `ApprovalRejected: REPO_ID_MISMATCH`: 신뢰 루트 `repo_id` 문자열 `"1451933830"`와 신규 SOURCE_PIN JSON 숫자 `1451933830`의 타입 불일치. watcher의 fail-closed 정상 동작이며 signer/승인 정책 결함으로 보지 않음. Guard `AUTO_SIGNING_UNCERTAIN`은 사용자 전달된 Windows 호스트 상태, GPT 호스트 DB 직접 확인 아님.
- **생성 측 보정:** [협업 운송 결과](../COWORK-DROPBOX-TO-GITHUB-MIGRATION/SOURCE_PIN_REPO_ID_STRING_REPAIR_RESULT_r0001_20261117_KST.md) — 공통 생성기 `collab/ops/source_pin.py`와 총 13개 회귀, 기존 Guard·MSC SOURCE_PIN의 `repo_id` 타입만 문자열 보정·원격 검증. GitHub Actions 실제 SOURCE_PIN 11/11 타입 검사 PASS. signer/READY/watcher 로컬 버전·DB·키·Notifier·위임 정책 **변경 없음**.
- **미정산:** Guard의 로컬 `AUTO_SIGNING_UNCERTAIN`은 포맷 수정만으로 자동 해제되었다고 주장하지 않음. 변경 이후 두 요청의 원격 APPROVAL_SIG/READY/DISPATCH/REVIEW_RESULT/RECEIPT는 조회 시 미관측. 비용·중복/불확실 로컬 이력은 Windows에서 확인해야 하며 자동 재큐잉 금지.
- **NEXT_ONE_ACTION:** 기존 Windows 호스트에서 **읽기 전용**으로 두 요청의 원인·로컬 예약/실행 이력과 재스캔 결과를 확인. 기존 유효 위임·한도·중복 게이트를 우회하거나 신규 유료 요청을 만들지 않음.

## 자동 승인 v0.2.23 LIVE 전환 완료: AUTO_SIGNING_LIVE=PASS_HOST_VERIFIED (2026-11-16 KST)

- 결과: `CLAUDE_V023_AUTO_APPROVAL_LIVE_CLOSEOUT_RESULT_FOR_GPT_20261116.md` (PRIVATE `main`, commit `169579371514`, SHA-256 `e3339a8f34b48f40b894c12aa1bab443c08c92db5aaeda7f6b9cf0713dcca1d2`). R2 영수증 보충 `USAGE_RECEIPT_1.json` commit `f1279962649e` (SHA-256 `869ae22e1633433d4e199175ba7ba0b08fc345f89fde4b1d717c5a6e5d61f65a`, v0.2.20 계약상 필수 아님, DB 사실만).
- 설치: v0.2.20 → v0.2.23(ZIP `f941be8a…80ea7` 바이트 동일), 백업·롤백 트리(이름 변경)·롤백 명령 준비, DB/키/토큰/Dropbox DB 해시 불변. 운영 회귀 967 passed/12 skipped, 자동 승인 시험 191 passed.
- 활성화: 보호 로컬 위임(ACL 확인) `COWORK-`/`L1-WORKSPACE-`, 3 skill, `POLICY-STATIC-V1`만, 요청당 1회·USD 1, 하루 2회·USD 3, 월 USD 10, 30일. 활성화 직후와 재시작 뒤 각 2주기: 소급 차단 3건, 서명·READY·모델 호출 0.
- 정정: R2 MINOR는 **2건**(이전 호스트 요약의 3건은 오기). Notifier에 자동 승인·불확실·정책 중지 알림과 대기 알림 중복 억제 추가(재시작으로 오래된 대기 요청 3건 알림이 갔을 수 있음, 공개됨).
- 미관측: 활성화 뒤 첫 실제 자동 서명 요청(NOT_OBSERVED). 미실행: 비판적 평가 R0~R3 프롬프트 적용(별도 후속). 다음 한 동작: GPT 판정.

## 운영 자동 승인 미활성화 오류 교정·v0.2.23 LIVE 마무리 원샷 지시 (2026-11-16 KST)

- **사용자 문제 제기:** Windows Claude Code가 현재 v0.2.20의 수동 승인 도구 `approve_request.py`만 설명하면서, 기존 사전 위임에 따른 v0.2.23 자동 승인 LIVE를 진척시키지 못한 협업 오류. GPT가 GitHub 요청 게시와 실제 Windows 실행을 연결하지 못한 점을 명시적으로 인정. 키가 PC에 존재하는 것과 매번 Claude 대화형 승인해야 한다는 주장은 별개.
- **정확한 현재 근거:** 기존 R2 `REQ-COWORK-AUTO-APPROVAL-V023-R2-20261115`는 실제 `APPROVAL_SIG/READY/DISPATCH/REVIEW_RESULT/RECEIPT` 모두 원격 존재, 유료 모델 **1회 완료**, `BLOCKING=0`, `MAJOR=0`, 원문 `MINOR=2`; 비용 `USD 0.5244525`는 Windows DB 보고. GPT 판정 [GPT_V023_R2_FINAL_DISPOSITION_AND_LIVE_EVIDENCE_GATE_r0001_20261116.md](GPT_V023_R2_FINAL_DISPOSITION_AND_LIVE_EVIDENCE_GATE_r0001_20261116.md) `ACCEPT_WITH_FOLLOWUP`, `LIVE_ACTIVATION=HOLD_PENDING_EVIDENCE_AND_HOST_TESTS`. 호스트 요약 MINOR 3 불일치, `USAGE_RECEIPT_1.json` 부재는 재호출 없이 정산 판단 필요. 운영은 최종 호스트 보고 v0.2.20, `AUTO_SIGNING=OFF`.
- **GPT 실행 시정 요청 게시·원격 readback PASS:** [GPT_V023_AUTO_APPROVAL_LIVE_CLOSEOUT_CORRECTION_r0001_20261116.md](GPT_V023_AUTO_APPROVAL_LIVE_CLOSEOUT_CORRECTION_r0001_20261116.md), commit `f7ba4347cd5dac19cc946be5d714287b6fa4433c`. **새 R2·추가 비용·수동 매요청 금액 확인 금지**. 한 번에 `R2 증빙 정합성 확인 → 기존 보호 정책 범위 확인 → 백업 → 기능 OFF v0.2.23 설치·회귀 → 보호된 LOCAL 자동 승인 활성화 → 두 주기/재시작/롤백/Notifier 검증 → 결과/영수증 원격 게시`. 실제 Windows 호스트 작업은 이 채팅 GitHub 게시만으로 자동 시작되지 않으므로 `HOST_CLOSEOUT=NOT_RUN` 유지. 독립적인 비판적 R0~R3 프롬프트 적용은 별도 기존 인계로 병렬 관리, 추가 리뷰로 이번 LIVE 차단 금지.
- **NEXT_ONE_ACTION:** Windows Claude Code가 위 신규 **정확한 상대 경로**를 직접 열어 동작 설명이 아닌 조건부 운영 전환을 처리하고 `CLAUDE_V023_AUTO_APPROVAL_LIVE_CLOSEOUT_RESULT_FOR_GPT_20261116.md` 및 CURRENT/TRACKER를 실제 결과에 따라 게시·원격 readback. 실패 시 차단 게이트만 `BLOCKED`와 근거를 기록하고 모델 재호출·임의 재큐잉·같은 승인 재질문 없이 종료.

## GPT 최신 판정 — v0.2.23 R2 정적 PASS, 조건부 LIVE 증빙 확인 대기 (2026-11-16 KST)
- 정본: [GPT R2 결과·운영 게이트](GPT_V023_R2_FINAL_DISPOSITION_AND_LIVE_EVIDENCE_GATE_r0001_20261116.md). watcher 작성 REVIEW_RESULT_1.md, DISPATCH_1.md, RECEIPT_1.md를 원격 직접 확인. R2 BLOCKING 0 · MAJOR 0, 정적 리뷰 범위 PASS. 기존 R2 승인·서명·READY·모델 호출 1회 이력 보존.
- 판정 차이: 실제 원본 리뷰 MINOR 2건, Claude 요약 및 파생 추적 MINOR 3건. USAGE_RECEIPT_1.json 미게시, 비용 USD 0.5244525는 Windows 호스트 DB REVIEW_COST 보고(원격 RECEIPT_1.md에는 없음). 추가 모델 호출 금지.
- 운영: 최종 호스트 보고 v0.2.20 유지·AUTO_SIGNING OFF, 새 설치/활성화 NOT_RUN. GPT R2 정적 검토는 ACCEPT_WITH_FOLLOWUP, LIVE_ACTIVATION은 HOLD_PENDING_EVIDENCE_AND_HOST_TESTS. 기존 사용자 조건부 승인 반복 요청 없음.
- NEXT_ONE_ACTION: Windows 호스트가 리뷰 본문 MINOR 개수·사용량 영수증의 실제 v0.2.20 계약과 비민감 비용 기록을 재실행 없이 조정한 뒤 기존 조건부 승인·보호 로컬 위임 유효성을 확인, 백업·기능 OFF 설치·회귀·안전 활성화·롤백 증거를 별도 보고. 어느 게이트든 실패하면 활성화 보류.

---

## v0.2.23 독립 R2 완료: BLOCKING 0·MAJOR 0, GPT 판정 대기 (2026-11-16 KST)

- 결과: `CLAUDE_V023_R2_AND_CONDITIONAL_AUTO_SIGN_LIVE_RESULT_FOR_GPT_20261115.md` (PRIVATE `main`, commit `9ca996b94ea7`, SHA-256 `118fb216ed53eb143bb47764c91622298be97b6f99735f3cc0b8ad5ecfdd6a90`). R2 `REVIEW_RESULT_1.md` SHA-256 `7834c201ca3bc6a6665bf6615c5612f7b5a0e3d4d4033a640f8473bcb01148d1`, 패키지 `f941be8a…80ea7`.
- 실행: 사용자 USD 3·1회 확인 → 점검 19/19 → 서명·`READY` 마지막 게시 → 감시기(v0.2.20) 1회 실행·`COMPLETED`, 비용 USD 0.5245, 모델 호출 1회.
- 운영 설치·위임 활성화·`AUTO_SIGNING`: **NOT_RUN (OFF 유지)** — GPT의 R2 판정 PASS 확인 전 금지. 다음 한 동작: GPT 판정.

## 새 요청: 비판적 평가 기준을 실제 Claude 자동 리뷰에 반영·검증 (2026-11-16 KST)

- **사용자 최신 지시:** 강화된 독립 리뷰 R0~R3의 비판적 검토·수정안/구조 대안 평가를 **자동 리뷰 경로에서 실제로 적용하고 시험하는 작업까지 요청**.
- **GPT 작업 요청서 PRIVATE 게시·재조회 PASS:** [GPT_CRITICAL_REVIEW_AUTO_APPLY_AND_TEST_REQUEST_r0001_20261116.md](GPT_CRITICAL_REVIEW_AUTO_APPLY_AND_TEST_REQUEST_r0001_20261116.md), 기준 계약 `collab/ops/CONTRACTS/REVIEW_TIER_TOKEN_BUDGET_V1.md` §2.1 (commit `1b7ab2175da7bace4d9dced5e01c31087a2bfe73`). 실제 Windows review prompt-builder/REQUEST 본문 전달 지점을 먼저 확인하고 `REUSE→CONNECT→최소 EXTEND`, 결함 강제 0·근거 중심 검토·결함/개선 제안 구분·최소 수정안과 구조 대안의 비용 비교 등을 신규 요청에 반영하고 가짜 runner의 **모델 호출 0** 시험으로 입증하도록 인계.
- **경계:** 위 문서는 Windows 자동 실행 신호가 아니므로 `AUTO_REVIEW_APPLY_REQUEST=POSTED`, `WINDOWS_APPLY_EXECUTION=NOT_RUN`, `PROMPT_INJECTION_TEST=NOT_RUN`. 실행한 호스트 결과가 오기 전 적용 완료라고 표기하지 않음.
- **기존 동결 R2 유지:** `REQ-COWORK-AUTO-APPROVAL-V023-R2-20261115`의 원본 REQUEST/ZIP/SOURCE_PIN, 최대 `POLICY-STATIC-V1-LARGE` USD $3·1회는 불변. 금회 GitHub 최신 조회 시 `APPROVAL_SIG/READY/DISPATCH/RESULT/RECEIPT=NOT_FOUND` / `INDEPENDENT_REVIEW=NOT_RUN` / `AUTO_SIGNING=OFF`(호스트 직접 상태는 별도). 이번 요청으로 새 유료 리뷰·중복 R2/READY 생성하지 않음.
- **NEXT_ONE_ACTION:** Windows Claude Code가 요청서의 단일 실행 프롬프트로 기존 프롬프트 결합 경로와 실제 런타임 반영을 점검하고 격리 dry-run·negative test 후 `CLAUDE_CRITICAL_REVIEW_AUTO_APPLY_VALIDATION_FOR_GPT_20261116.md` 결과/증거와 `CURRENT.md`·`TRACKER.json`을 PRIVATE main에 게시·원격 확인. 유효한 보호 자동 위임·리뷰 요청이 실제 활성화되기 전 모델 호출 0. 기존 R2 상태가 먼저 변경되면 결과/영수증 우선 확인 후 중복 금지.

## R2 v0.2.23 공식 REQUEST·ZIP·SOURCE_PIN 게시 완료, 호스트 처리 대기 (2026-11-15 KST)

- **사용자 최신 실행 지시:** “그래 자동승인까지 진행해줘” — 기존 통합 R2 1회/최대 $3, 승인된 보호 Windows 사전 위임 범위, 독립 리뷰+GPT PASS 조건부 운영 활성화에 대한 진행 의사 확인. 새 대상은 **v0.2.23**(원래 v0.2.22에서 접두사 호환성만 보완, GPT 정적 PASS).
- **GPT 직접 게시·원격 readback PASS:** 신규 정식 R2 `collab/requests/REQ-COWORK-AUTO-APPROVAL-V023-R2-20261115/REQUEST.md`와 원본 ZIP `collab/packages/skill-collab-watcher_v0_2_23_1115_DEV_NOT_FOR_DEPLOYMENT.zip` 및 승인 범위 참고 `OWNER_SCOPE_RECORD.md`를 **Commit A `8c90827ea6f0771331937d81c719697b322d4039`**에 함께 저장. ZIP은 기존 Git blob `0d7001798d402e5545833e6aaf8c5f4b9d2b8fbf` 그대로 복사, **282340 B, SHA-256 `f941be8a6b53d00baa10a9b097f234b159470e2aa1242ecc33bcf0bdee080ea7`**(이전 직접 검증과 동일). REQUEST `SKILL_COLLAB_REVIEW_REQUEST_V1`/`SUBMITTED`/`POLICY-STATIC-V1-LARGE`/max $3×1, knowledge_refs 3개 각각 원시 SHA-256 확인.
- **SOURCE_PIN:** `collab/requests/REQ-COWORK-AUTO-APPROVAL-V023-R2-20261115/SOURCE_PIN.json` **Commit B `e0e144cc56215b9d5d95cab77714186db6bf6662`**, `source_commit=8c90827e…` / `repo_id=1451933830` / `SKILL_COLLAB_SOURCE_PIN_V1`, 원격 readback PASS.
- **호스트 원샷 정본:** [GPT_R2_V023_HOST_ONE_SHOT_AND_LIVE_GATE_r0001_20261115.md](GPT_R2_V023_HOST_ONE_SHOT_AND_LIVE_GATE_r0001_20261115.md), commit `49caa963cbad9106874b70ba416a72ea964f7c41`, remote readback PASS. 현재 운영 v0.2.20은 READY 없이 REQUEST만으로 모델 호출 불가. 현재 이 채팅의 GitHub 도구는 Windows 호스트 작업/키/프로세스를 직접 실행할 수 없어 **R2 모델/READY/조건부 설치를 실제로 실행했다고 보고하지 않음**.
- **직접 원격 상태 조회:** `REQUEST=POSTED`, `ZIP=POSTED`, `SOURCE_PIN=POSTED`, `APPROVAL_SIG=NOT_POSTED`, `READY=NOT_POSTED`, `DISPATCH/REVIEW_RESULT/RECEIPT=NOT_POSTED`. 따라서 `INDEPENDENT_REVIEW=NOT_RUN`, `AUTO_SIGNING=OFF`, `OPERATING_GITHUB_LIVE=v0.2.20_UNCHANGED`, `NEW_PAID_CALLS_THIS_REQUEST=0`.
- **NEXT_ONE_ACTION:** 실제 Windows 실행 주체가 위 ONE_SHOT 문서로 기존 호스트 검증 절차를 마치고 유효한 READY LAST → 승인된 R2 1회/영수증을 게시하도록 연결. GPT는 R2 검증·판정 후 **차단 결함 0 및 동일 바이트 PASS** 조건으로 앞서 승인된 v0.2.23 설치/30일 보호 위임 자동 승인 LIVE 적용 검증 진행. 이전 요청/승인 반복 금지. 신뢰된 승인 수단 미확인/한도 초과는 `BLOCKED`, 모델 호출 0.

## GPT v0.2.23 최종 정적 PASS — R2 대상 변경 확인만 대기 (2026-11-15 KST)

- **GPT 결정:** [GPT_V0223_PREFIX_COMPAT_FINAL_DISPOSITION_r0001_20261115.md](GPT_V0223_PREFIX_COMPAT_FINAL_DISPOSITION_r0001_20261115.md), commit `d4ad638fc6af0151166cf466601fc1620c91b9d3`, remote readback PASS. `PASS_FOR_INDEPENDENT_R2_CANDIDATE_ONLY`. 운영 배포 PASS/독립 리뷰 PASS 아님.
- **규칙 판단:** `_FAMILY.fullmatch` 정규식 `[A-Za-z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)*-`, 최소 7자. 보호된 로컬 위임의 owner-listed `COWORK-`(7자)와 `L1-WORKSPACE-`만 자동 프로젝트 가족으로 인정 가능하며 7자 하한 자체는 실행 권한이 아님. 스킬 exact allowlist/비용·중복·서명·READY 조건 불변. v0.2.22가 승인 입력을 거절했던 호환성 문제 수정 수용.
- **GPT 원격 ZIP 실제 bytes 직접 검증 PASS:** `artifacts/v0_2_23/skill-collab-watcher_v0_2_23_1115_DEV_NOT_FOR_DEPLOYMENT.zip` 282340 B, SHA-256 `f941be8a6b53d00baa10a9b097f234b159470e2aa1242ecc33bcf0bdee080ea7`, ZIP central-directory 102개, Git blob `0d7001798d402e5545833e6aaf8c5f4b9d2b8fbf`; diff 직접 검토. ZIP full CRC/Windows 실측은 호스트 보고 구분.
- **Windows 자체시험:** 구 v0.2.22에 신규 회귀 적용 시 5 FAIL/19 PASS, v0.2.23은 890 PASS/12 SKIP Windows venv+운영 Python 3.11.9 각, 격리 SHADOW 8/8, rollback PASS(호스트 자체 보고). `INDEPENDENT_R2=NOT_RUN`, `REAL_KEY_SIGNING=0`, `READY=NOT_POSTED`, `NEW_PAID_CALLS=0`, `AUTO_SIGNING=OFF`. 기존 GitHub LIVE v0.2.20 변경 없음.
- **변경점 확인만 대기:** 앞선 통합 사용자 승인은 R2 LARGE 최대 $3/1회, 지정 위임 범위/한도/30일 및 리뷰 PASS 조건부 설치까지 확보했으나 **R2 동결 ZIP은 v0.2.22**였음. v0.2.23 SHA `f941be8a…80ea7`로 **리뷰 입력만 바꾸는 것**에 대한 좁은 사용자 확인 후 R2 정식 신규 REQUEST/고정 ZIP/Commit A/SOURCE_PIN → Windows 기존 signer/READY LAST → 독립 리뷰/영수증→GPT 판정. 승인 범위 전체 반복 요청·추가 비용·모델 재호출 금지.
- **NEXT_ONE_ACTION:** 사용자에게 **v0.2.23 바이트에 한하여 기존 $3/1회 R2 적용 가능 여부**만 확인. 변경 승인 전 모델 0, 서명 0, READY 0.

## 승인 접두사 호환성 수정 완료: 후보 v0.2.23 (COWORK-/L1-WORKSPACE- 승인 범위 통과, 옛 후보 거부 재현, 자체시험 890/890, 독립 R2 NOT_RUN, 운영 불변) (Claude 호스트 보고, 2026-11-15 KST)
- 결과: `CLAUDE_V0222_APPROVED_PREFIX_COMPAT_FIX_RESULT_FOR_GPT_20261115.md` (PRIVATE `main`, commit `30e6b7fed42a886fb8f8e3bd10ba671683209c61`, 원격 바이트·SHA-256 `bb4c71d40c2b6064ba48e2df663a18be3350a6db6ca7e0d95e9019eb5a0220a9` 일치).
- 원인: v0.2.22 접두사 최소 길이 8자 → 승인된 `COWORK-`(7자) 거부로 위임 전체 로드 실패. 수정: 영숫자 단어와 `-`로 끝나는 접두사, 최소 7자, 와일드카드·공백·구분자 없는 단어 거부. 매칭·스킬 정확 일치는 불변.
- 시험: 신규 승인 범위 시험을 옛 후보 v0.2.22에서 실행 → 5건 실패(재현), 거절 시험 19건 통과. 수정본 v0.2.23 전부 통과, 전체 회귀 시험 venv·운영 인터프리터 각 890 passed/12 skipped, SHADOW 8/8, 롤백 리허설 ALL_PASS, 운영 DB·키·설치 트리 불변.
- 후보 `skill-collab-watcher_v0_2_23_1115_DEV_NOT_FOR_DEPLOYMENT.zip` 282340 B, sha256 `f941be8a6b53d00baa10a9b097f234b159470e2aa1242ecc33bcf0bdee080ea7`, PRIVATE `artifacts/v0_2_23/`에 ZIP·diff·매니페스트 게시(원격 바이트 일치, 요청·READY 없음). 독립 리뷰 NOT_RUN.
- 미실행: 독립 R2, 실제 서명, APPROVAL_SIG·READY 게시, 위임 활성화, 운영 설치, Notifier 추가. 유료 모델 0.
- 다음 한 동작: GPT 최종 판정. PASS 이후에만 독립 R2 1회(USD 3) 실행.

## 사용자 통합 승인 확보 / v0.2.22 승인 범위 접두사 호환성 수정 대기 — 2026-11-15 KST

- **현재 사용자 승인 기록:** [GPT_R2_APPROVAL_AND_V0222_SCOPE_FIX_GATE_r0001_20261115.md](GPT_R2_APPROVAL_AND_V0222_SCOPE_FIX_GATE_r0001_20261115.md), commit `9fafb272864d7b9570650995db27e81675154f35`, 원격 readback PASS. 사용자 “그래”는 이전 [통합 제안](GPT_V0222_DISPOSITION_AND_COMBINED_APPROVAL_GATE_r0001_20261115.md)의 **v0.2.22 독립 R2 LARGE 최대 $3/1회**, 보호 로컬 위임 project families `COWORK-`·`L1-WORKSPACE-`, 3개 exact skill, STATIC-V1 $1/요청, 2회/$3/일, $10/월, 30일 위임, R2 독립 PASS·GPT 판정 **조건부** Windows 설치/자동서명 활성화를 통합 승인한 것으로 기록. 서명/READY/유료 호출은 아직 없음.
- **새로 확인된 blocker:** v0.2.22 `auto_approval.py::_families`가 project family `len(x)>=8`을 필수로 요구하지만 승인된 `COWORK-` 길이는 **7**. 그대로 설치하면 보호 정책이 `POLICY_UNREADABLE`로 거부. `L1-WORKSPACE-`는 규칙 통과. 기존 M2 시험에 실제 승인 접두사 반례가 빠졌음. 운영 활성화/유료 R2 선행 시 비용 낭비 가능.
- **판정:** `APPROVAL_RECORDED`, `V0222_SCOPE_COMPAT=FAIL`, `R2_1CALL_USD3=APPROVED_FOR_ORIGINAL_V0222_NOT_SPENT`, `R2_REQUEST=NOT_POSTED`, `R2_READY=NOT_POSTED`, `REVIEW=NOT_RUN`, `AUTO_SIGNING=OFF`, `OPERATING=v0.2.20_GITHUB_LIVE_UNCHANGED`. 승인받지 않은 새로운 후보 바이트에 원래 R2 비용 승인을 자동 이전하지 않음.
- **NEXT_ONE_ACTION:** Windows Claude Code에 위 문서 **§3 한 번** 인계 → 격리 v0.2.22 복사본에서 정확 `COWORK-` 짧은 접두사 호환성만 안전하게 수정·구버전 FAIL/신본 PASS 회귀 및 전체 Windows 시험/SHADOW/rollback → 고유 v0.2.23 DEV ZIP/실 SHA/CRC·PRIVATE 결과 `CLAUDE_V0222_APPROVED_PREFIX_COMPAT_FIX_RESULT_FOR_GPT_20261115.md` 게시·원격 readback. 설치/실키/REQUEST/READY/유료 호출 0. 이후 GPT가 변경 입력만 좁게 사용자 확정하고 기존 1회 독립 R2와 조건부 LIVE 적용을 이어감.

## GPT v0.2.22 직접 재해시·정적 판정 — 독립 R2 및 위임 범위 사용자 통합 승인 대기 (2026-11-15 KST)

- **GPT 판정 정본:** [GPT_V0222_DISPOSITION_AND_COMBINED_APPROVAL_GATE_r0001_20261115.md](GPT_V0222_DISPOSITION_AND_COMBINED_APPROVAL_GATE_r0001_20261115.md); commit `f3bf1f1e691540c6f4dfec2598d962790c9e39c7`, 원격 본문 readback PASS.
- **판정 `ACCEPT_V0222_FOR_INDEPENDENT_REVIEW_ONLY`:** B1 합집합 비용/횟수, B2 보호 위임 scope 재검증, M1 in-process double signer 경쟁 방지, M2 프로젝트 family를 새 `diff_v0_2_21_to_v0_2_22.patch`로 직접 대조. Windows Claude Code 최종 ZIP 자체시험 `866 passed/12 skipped` 두 Python 환경, 격리 SHADOW 8/8, 구후보 FAIL→신후보 PASS, 운영 원본 불변은 Windows 호스트 보고이며 독립 PASS가 아님.
- **GPT GitHub ZIP 실제 bytes 검증 PASS:** `artifacts/v0_2_22/skill-collab-watcher_v0_2_22_1115_DEV_NOT_FOR_DEPLOYMENT.zip` 280313 B, 101 entries, SHA-256 `1b67de37891cb7fdbae721b9424e312d1cc5b8c68e06e69357555a556d27bd87`, Git blob `caa55e965df2a42693a06cee44e17e2e1cb879e5`. 전체 ZIP CRC는 Windows 호스트 증거, GPT는 미실행.
- **다음 게이트:** 신규 v0.2.22 독립 Claude R2 **`POLICY-STATIC-V1-LARGE` 최대 $3 1회**, **아직 사용자 승인/REQUEST/READY/모델 호출 없음**. 단일 통합 승인안: 기존 LIVE v0.2.20 보존, 보호 로컬 사전 위임 `COWORK-`·`L1-WORKSPACE-` family + 3개 실제 skill exact, `POLICY-STATIC-V1`만 요청당 1회/$1, 일 2회/$3, 월 $10, 30일 만료, 소급 요청 불허. R2 BLOCKING=0 등 GPT 판정 PASS **조건부** 운영 설치/auto signer 활성화·Notifier 이벤트 연결/검증/롤백 승인 제안. 아직 모든 값 `NOT_APPROVED`.
- **실제 운영 상태:** `ACTIVE_PROVIDER=GITHUB`, `OPERATING_VERSION=v0.2.20`(Windows 보고), `AUTO_SIGNING=OFF`, `INDEPENDENT_REVIEW=NOT_RUN`, `NEW_PAID_MODEL_CALLS=0`, `V0222_INSTALL=NOT_RUN`. 현재 대기 Work→Knowledge·dashboard REQUEST는 소급 자동 디스패치 0 유지.
- **NEXT_ONE_ACTION:** 위 문서의 비용/R2·범위·조건부 운영 승인에 대한 사용자 한 번의 명시 응답을 받기. 승인 뒤 신규 R2 패키지 SHA/원격 요청 고정 → Windows 기존 signer/READY LAST→LIVE watcher 독립 리뷰 1회·receipt→GPT 판정. PASS면 허용된 Windows 적용·검증으로 한 번에 마무리. 실패/승인 초과는 fail-closed/모델 재호출 0.

## v0.2.21 GPT 정적 판정 수정 완료: 후보 v0.2.22 (B1·B2·M1·M2, 자체시험 866/866, 독립리뷰 NOT_RUN, 운영 불변) (Claude 호스트 보고, 2026-11-15 KST)
- 결과: `CLAUDE_V0221_GPT_FINDINGS_FIX_RESULT_FOR_GPT_20261115.md` (PRIVATE `main`, commit `6f448b63e607c9ba951f2b5ea09043217de5f6a3`, 원격 바이트·SHA-256 `4413787701b1997ace8d7e4e0064665f95e340159bc19f9530209f53d2a18f20` 일치).
- B1: 자동 예약과 워처 디스패치를 요청 신원 단위 합집합(중복 1회, 비용은 큰 값, 합산)으로 예약 트랜잭션 안에서 집계. 옛 후보는 max() 때문에 세 번째 요청 통과(실패 재현). B2: 서명·승인 게시·READY 게시 직전마다 현재 보호 위임으로 저장 후보 재판정, 축소 시 POLICY_STOPPED(서명·READY·모델 0). 옛 후보 25건 실패.
- M1(간헐 실패)은 시험 타이밍이 아니라 실제 결함: 같은 프로세스의 두 호출이 예약 후 서명 전 단계를 죽은 시도로 오인해 두 번 서명. 옛 후보 12회 중 3회 재현, 수정본 12/12 통과, 프로세스 내 진행 중 가드 추가.
- M2: 정확 프로젝트 외에 끝이 '-'인 가족 접두사 허용(와일드카드 불가, 스킬은 정확 일치, 두 프로젝트 ID 명시 거절). 실제 REQUEST V1은 project_id·work_id가 항상 같음. 범위 확정은 사용자 승인 전이라 미적용.
- 검증: 최종 ZIP 트리에서 시험 venv·운영 인터프리터 각 866 passed/12 skipped(기준선 v0.2.20 674/12), SHADOW 8/8, 롤백 리허설 ALL_PASS, 운영 DB·키·Task·설치 트리 불변. 변이 시험은 v0.2.22에서 재실행하지 않음.
- 후보 `skill-collab-watcher_v0_2_22_1115_DEV_NOT_FOR_DEPLOYMENT.zip` 280313 B, sha256 `1b67de37891cb7fdbae721b9424e312d1cc5b8c68e06e69357555a556d27bd87`, PRIVATE `artifacts/v0_2_22/`에 ZIP·diff·매니페스트 게시(원격 바이트 일치, 요청·READY 없음).
- 미실행/미승인: 독립 리뷰(R2/LARGE $3 1회), 위임 범위 1회 확정, 운영 설치·Notifier 이벤트 추가·활성화. AUTO_SIGNING=OFF, 유료 모델 0, 실서명 0, READY 0.
- 다음 한 동작: GPT 단일 판정과 리뷰·범위 승인 요청 묶음.

## GPT 정적 판정 — v0.2.21 후보 보완 후 독립 리뷰 (2026-11-15 KST)

- **최신 GPT 판정 정본:** [GPT_V0221_STATIC_DISPOSITION_AND_SINGLE_FIX_HANDOFF_r0001_20261115.md](GPT_V0221_STATIC_DISPOSITION_AND_SINGLE_FIX_HANDOFF_r0001_20261115.md), GitHub PRIVATE main commit `5608dec4072710846b6331ecd48f22029914a7ea`, remote readback PASS. `GPT_DISPOSITION=REVISE_BEFORE_INDEPENDENT_REVIEW` / `BLOCKING=2` / `MAJOR=2`.
- **GPT 원격 ZIP 재해시 확인:** v0.2.21 dev 후보 실제 raw bytes 272839, SHA-256 `16921bf4021714345cabc78de5e2e8a6882891615f90b5747622570ca4465d8b` = Windows 보고 일치. Full CRC/Windows 실행은 호스트 자체보고로 구분. 기존 817 PASS/12 SKIP, SHADOW 8/8은 `SELF_TEST_REPORTED`.
- **B1 BLOCKING:** 자동 서명 예약과 기존 별도 수동 리뷰 dispatch를 `max(counts)`로 합치면 서로 다른 예약·실행이 과소 집계됨(예: 자동 예약 A1 + 수동 실행 B1 + 추가 자동 C1 → day 2 한도인데 3건 허용 가능). 기존 watcher 최종 집행이 실제 과금 초과를 허용했다는 뜻은 아님. identity 기반 union 집계/원자 한도 회귀 필요.
- **B2 BLOCKING:** 위임 로컬 정책을 서명/READY 이전에 축소해도 `_still_allowed`는 enabled/expiry/repo만 재검증하고 project/skill/limit 축소를 놓침. 재검증/claim 정책 결속 및 revoke crash 회귀 필요.
- **M1 MAJOR:** 최초 ZIP 추출 회귀 1 FAIL 원인·테스트 이름 미확인, 이후 반복 전부 PASS; 재현·증거 확보. **M2 MAJOR:** 정확 project/skill allowlist와 project_id≠work_id 처리가 신규 Work 무인 자동 리뷰 목표에 맞는지 기존 계약과 대조. 무제한 자동 범위 도입 금지.
- **실제 단계:** `DEVELOPMENT=v0.2.21_COMPLETED_CANDIDATE`, `GPT_STATIC_REVIEW=FAIL_BLOCKING_2`, `INDEPENDENT_REVIEW=NOT_RUN`, `OPERATING_DEPLOYMENT=NOT_RUN`, `AUTO_SIGNING=OFF`, `EXISTING_GITHUB_LIVE=v0.2.20_UNCHANGED`, `NEW_PAID_MODEL_CALLS=0`. 기존 후보·설치·원본 보존, 비용과 실운영 자동위임 승인 없음.
- **NEXT_ONE_ACTION:** Windows Claude Code가 위 판정 정본의 마지막 원샷 지시로 B1/B2 재현·수정·전체 회귀/격리 SHADOW·rollback, M1/M2 판단, 새 dev ZIP/SHA/CRC 및 `CLAUDE_V0221_GPT_FINDINGS_FIX_RESULT_FOR_GPT_20261115.md`를 PRIVATE 게시·원격 readback. 사용자 중간 질문/새 유료 모델 호출 없음. 그 후 GPT가 재판정하고 독립 R2(권고 LARGE $3/1회)와 제한적 사전 위임·운영 적용 범위를 묶어 **별도 명시 승인**을 요청.

## Windows 원샷 완료: 자동 서명·READY 후보 v0.2.21 개발·시험·후보 고정 (Claude 호스트 보고, 2026-11-15 KST) — AUTO_SIGNING=OFF 유지
- 결과: `CLAUDE_AUTO_APPROVAL_ONE_SHOT_RESULT_FOR_GPT_20261115.md` (PRIVATE `main`, commit `c99d49e8b15c73ea312364548cf5213a59c1874e`, 원격 바이트·SHA-256 `76bb3c16360a6993339d78380f0bfa84435ea4d3c7c34028e2e262cb323627e7` 일치). 운영 감시기·DB·Task·Notifier·키 **불변**, 실제 서명 0, READY 게시 0, 유료 모델 호출 0.
- 후보 `skill-collab-watcher_v0_2_21_1115_DEV_NOT_FOR_DEPLOYMENT.zip` 272839 B, sha256 `16921bf4021714345cabc78de5e2e8a6882891615f90b5747622570ca4465d8b`(재빌드 바이트 동일, CRC OK, 비밀 스캔 0). PRIVATE `artifacts/v0_2_21/`에 ZIP·diff·매니페스트 게시(원격 바이트 일치, 요청·READY 없음). 독립 리뷰 **NOT_RUN**.
- 시험(자체): GPT 25건 원본 Windows 3.11.9에서 25/25, 최종 ZIP 전체 회귀 시험 venv·운영 인터프리터 각 817 passed/12 skipped(v0.2.20 기준 674/12, 신규 143), 격리 SHADOW(실제 CLI 별도 프로세스, 가짜 GitHub·계수 스텁·일회용 키) 8/8, 변이 시험 16/17(생존 1건은 동등 변이), 격리 설치·롤백 리허설 PASS. 간헐 실패 1건은 원인 미규명(이후 반복 전부 통과).
- 호스트 읽기 전용 실측: 운영 신뢰 루트 로드·키 ACTIVE 신뢰·DPAPI 복호화 메모리 확인(서명 안 함), 승인 키 파일 ACL(Win32 DACL) 광범위 쓰기 없음, 감시기 프로세스 계정=키 소유자(서명 경로 가능).
- 설계 한계: 서명 능력이 GitHub 입력을 읽는 감시기 프로세스 안에 있음(방어=위임 게이트+fail-closed 순서, 피해 상한 요청당 $1·일 2회·월 $10), commit 시각 위조 가능성(첫 관측 플래그가 2차 방어), GPT 핀 없으면 `PIN_MISSING`.
- 미승인/NOT_RUN: 독립 리뷰(권고 R2/LARGE, $3, 1회), 사용자 위임 범위 1회 확정(허용 Work/skill, 월 $10·30일은 제안값), 운영 설치·Notifier 이벤트 목록 추가·활성화. 현재 대기 요청(Work→Knowledge, 대시보드)은 소급 자동 실행되지 않음(시험 입증).
- 다음 한 동작: GPT가 독립 리뷰 요청과 위임 범위 확정을 한 번에 묶어 사용자에게 제시.

## 최신 실행 상태 — 2026-11-15 KST (GPT 설계·격리시험·원샷 준비 완료)

- **Work:** GPT→GitHub PRIVATE REQUEST 게시 후 Windows 기존 signer의 **제한적 사전 위임 정책**에 따른 자동 승인·`APPROVAL_SIG` 생성·`READY` 마지막 게시. 기존 단일 GitHub LIVE watcher의 독립 Claude 리뷰 1회/영수증/Notifier는 유지. 정상 요청 시 Telegram 추가 승인 버튼/Windows Claude Code 수동 서명 **불필요**하도록 개선.
- **기존 운영은 그대로 LIVE:** 별도 CoWork GitHub 이관 [CURRENT](../COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md) 최상단 `ACTIVE_PROVIDER=GITHUB / CUTOVER=LIVE / v0.2.20`(Windows 호스트 보고·GPT 리뷰/receipt 재조회). 이번 변경으로 provider를 전환하지 않으며 `AUTO_SIGNING=OFF`. 기존 30초 Task·Notifier·DB/키/토큰·레거시 pending 1건 불변.
- **설계 정본:** [AUTOMATIC_SIGNING_MINIMAL_DESIGN_r0001_20261115.md](AUTOMATIC_SIGNING_MINIMAL_DESIGN_r0001_20261115.md), 최종 content commit `9addbb03b2c1a77c65434c135ce243dbc8f2110d`, remote readback PASS. 기존 [Telegram 1탭 대안](../COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_APPROVAL_BRIDGE_MINIMAL_DESIGN_r0001_20261115.md)은 **채택하지 않은 이전 설계**로 보존. GitHub 문구만으로 유료 리뷰 권한을 입증할 수 있다는 주장 금지: 운영 Windows의 보호된 사용자 위임 정책이 승인 근거.
- **GPT 실제 구현 참고:** [prototype/auto_policy.py](prototype/auto_policy.py) Python 순수 함수(3451 B, SHA256 `26cfe6abe6d74361c0d64270cc3c6ca9f1e0da5f3761814df4fea2ca73ac333c`), [prototype/test_auto_policy.py](prototype/test_auto_policy.py) (4291 B, SHA256 `64f816b111c169cc1460a03c48d291b6b8e9b88dd51be50c1d1bd59be53d3c87`). 원격 Git blob이 실제 합성 실행 파일과 일치. 코드는 운영 signer/DB 접근이 없는 **예제**; 그대로 설치 금지.
- **시험:** [GPT_AUTO_APPROVAL_PROTO_TEST_RESULT_r0001_20261115.md](GPT_AUTO_APPROVAL_PROTO_TEST_RESULT_r0001_20261115.md) `Python unittest 25 PASS / 0 FAIL / 0 SKIP` (Linux 격리, GitHub/Windows/서명/Claude 모델 호출 0). `WINDOWS_REAL_CODE_INTEGRATION=NOT_RUN`, `FULL_V0220_REGRESSION=NOT_RUN`, `SHADOW=NOT_RUN`, `ROLLBACK=NOT_RUN`, `INDEPENDENT_REVIEW=NOT_RUN`, `OPERATING_APPLIED=NOT_RUN`.
- **정확한 Windows 단일 실행 인계:** [WINDOWS_ONE_SHOT_DEVELOP_TEST_CANDIDATE_HANDOFF_r0001_20261115.md](WINDOWS_ONE_SHOT_DEVELOP_TEST_CANDIDATE_HANDOFF_r0001_20261115.md) commit `60d44ca5796bdde7b8c2c612d4beb2e47a5c55a6`, remote readback PASS. Windows Claude Code 1회: 실제 Windows v0.2.20 signer/Watcher 소스·Task 계정/ACL·원장 조사 → 격리 최소 구현 → 기존 전체 회귀+오류/중복/crash 시험 → fake SHADOW → DEV 후보 ZIP/SHA/CRC/rollback → PRIVATE 결과·CURRENT/TRACKER 직접 게시·remote readback. 중간 승인 없이 개발 범위 내에서 결함 수정·재시험.
- **현재 승인 경계:** 사용자 최신 지시는 빠른 협업 개선을 위한 **워크플로우 준비/격리 개발·시험 수행**. 자동위임 정책의 정확한 허용 project/skill·월 한도·만료는 아직 사용자 정식 1회 확정 전. 추천 초안 `POLICY-STATIC-V1, request <=$1, day <=2 calls/$3, month <=$10, 30-day expiry`는 **승인된 운영 값 아님**. 실제 Windows 운영 Task/DB/키/코드 설치, AUTO_SIGNING LIVE 활성화, 신규 유료 독립 리뷰, PUBLIC 배포는 **NOT_AUTHORIZED/NOT_RUN**. 기존 특정 요청(Work→Knowledge) $1 승인을 포괄 위임으로 재사용하지 않음.
- **독립 리뷰/배포 분리:** 개발자 자체시험은 독립 Claude 리뷰가 아님; 실제 유료 리뷰 호출은 새 요청/서명/사용자 비용 승인 계약에 따라 별도. 후보는 `development_not_for_deployment` 유지. 이후 후보 증거가 확보되면 GPT가 보완·비용/위임 범위·운영 승인 요청을 **한 번에 묶어서** 다음 LIVE 활성화 최종 게이트 판정.
- **Windows 결과 예상 정확 경로:** `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/CLAUDE_AUTO_APPROVAL_ONE_SHOT_RESULT_FOR_GPT_20261115.md`.
- **다음 한 동작:** Windows Claude Code에 위 인계서를 **한 번** 전달해 무비용 격리 구현·시험·후보·원격 재검증까지 진행. GitHub 문서 게시 자체로 Windows 자동 실행 시작되지 않음. 사용자에게 매 시험 단계마다 재요청·반복 승인 요구 금지.

## 결과 판정 분리

| 영역 | 상태 |
|---|---|
| 기존 GitHub REVIEW PROVIDER LIVE | `PASS_HOST_REPORTED / UNCHANGED` |
| AUTO_SIGNING 설계·GPT prototype | `PREPARED / 25 PASS` |
| Windows 실제 signer/Watcher 구현·시험 | `NOT_RUN` |
| 독립 리뷰 | `NOT_RUN` |
| 위임 정책 사전 승인 / 운영 적용 | `NOT_APPROVED / NOT_RUN` |
| 기존 유료 모델 신규 호출 | `0` |
