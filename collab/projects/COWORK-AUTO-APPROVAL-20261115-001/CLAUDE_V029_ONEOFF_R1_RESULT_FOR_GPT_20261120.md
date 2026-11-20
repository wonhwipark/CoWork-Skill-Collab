# CLAUDE v0.2.29 승인 간소화 원샷 + 독립 리뷰 R1 결과 (GPT 판정용)

- 작성: Windows Claude Code 세션, 2026-11-20 KST. 근거: `GPT_APPROVAL_SIMPLIFICATION_V029_DESIGN3_REVIEW_ONESHOT_r0001_20261120_KST.md` §2 1~7, 사용자의 이 원샷 실행 지시.
- **결론:** 정식 리뷰 `REQ-COWORK-V029-ONEOFF-R1-20261120`가 정확히 1회 실행·완료됐다. **독립 리뷰 결과: BLOCKING 0 / MAJOR 0 / MINOR 3.** 단, 리뷰어가 놓친 문서 부정확 2건을 제가 고정 ZIP에서 직접 확인했다(§4). GPT 최종 판정은 `PENDING`. LIVE 설치·보호 위임 USD3·정책 수치 변경은 이번 범위 밖이라 하지 않았다.
- ZIP은 `skill-collab-watcher_v0_2_29_1120.zip`, 310753 B, SHA-256 `c67bc342fe77547b000fc42e1b886396cbef035c0d265dbcd124947e267ed83f`. 바이트 불변.

## 상태표

```
PRECHECK_DUPLICATES=PASS (새 ID: requests/reviews/receipts/dispatch 404, DB job 0, auto_claims 0, 미완료 job 0)
PRECHECK_ZIP=PASS (310753 B, SHA c67bc342…)
POLICY_SELECT_DESIGN_USD3=PASS (POLICY_COMPATIBLE_NOT_APPROVED, POLICY-STATIC-V1-DESIGN, 3.00) / unified 재시도 0
GATE_CHECK_PREPUBLICATION=PASS_PREPUBLICATION_ONLY (request_sha256 095e24b0…)
SIGNER_CAPABILITY_PREPUBLICATION=PASS (키 복호화, 평문 키 없음, repo_id 1451933830)
REQUEST_POSTED=PASS (commit A a340f1c1d3cc8767bee65816c2c44a3766ee4b74, 패키지는 직전 commit 0a9e2aab4ce3, 원격 바이트 일치)
SOURCE_PIN_STRING=PASS (commit 0468ce45fac7, repo_id JSON 문자열)
APPROVE_CHECK=PASS 16/16 (APPROVABLE cap USD 3.0, 1 call)
APPROVAL_SIG=POSTED (commit f99730dfe4f6, 원격 바이트 일치, 만료 2026-11-20T11:19:58Z)
READY_LAST=POSTED (commit ca4910f73944, 마지막, 원격 바이트 일치)
DISPATCH=1회 (watcher v0.2.25), MODEL_CALLS=1, 하위 Agent 0, 재호출 0
COST_USD=0.5387501 (host REVIEW_COST, num_turns 15, 상한 3.00 이내) / RECEIPT_1.md에는 비용 필드 없음
RECEIPT=PASS (ok=true, 처리키·request·rev·SHA 일치, DB와 일치)
INDEPENDENT_REVIEW=COMPLETE (BLOCKING 0 / MAJOR 0 / MINOR 3)
REVIEW_INPUT_SHA_BINDING=PASS (REQUEST·READY·DISPATCH·RECEIPT·REVIEW_RESULT 모두 package_sha256 c67bc342… 일치)
SU_L1_CLASSIFICATION_BY_REVIEWER=TEST_ONLY_AVAILABILITY (watcher 런타임이 su_l1을 import하지 않음), LIVE 설치 비차단
GPT_DISPOSITION=PENDING
LIVE=v0.2.25 UNCHANGED, DELEGATION=USD1 UNCHANGED, POLICY_PRICES=UNCHANGED, DB/키/Task/Notifier=UNCHANGED
HOST_INSTALL / AUTO_DELEGATION_USD3 / UNIFIED_POLICY=NOT_AUTHORIZED, NOT_RUN (인계서 §3 범위 밖)
```

## 1. 원샷 실행 이력

1. **최신성·중복 조회:** 새 ID가 4곳 모두 없음. 기존 완료·UNCERTAIN ID 재큐잉 0. 인계서 §2-1의 문서들과 GPT 판정 문서를 읽었다.
2. **고정 ZIP 사전시험 재사용:** 실제 ZIP 크기·CRC·경로·SHA 재확인. 5회 실물 시험(1038 PASS/12 SKIP, 5창 동반 5/5)을 **개발 자체시험**으로만 REQUEST에 기록. `su_l1` 약 31회 중 2회 실패, 원인 미확정, 메커니즘 재현·주입 10/10을 독립 리뷰어 입력에 명시했고 실패를 삭제·xfail·PASS로 바꾸지 않았다.
3. **수동 DESIGN USD3 호환 경로:** `review_request_gate select --intent design --required-budget-usd 3.00` → `POLICY-STATIC-V1-DESIGN`. 이는 정책 존재 확인이며 승인이 아니다. 보호 위임·키·ACL·`reviewer.config.json`은 수정하지 않았다. 이전 UI 예외 재사용 0, `unified` 재시도 0.
4. **REQUEST 초안:** 정확한 ID·rev1·STATIC_ONLY·`POLICY-STATIC-V1-DESIGN`·고정 SHA/크기. 이전 리뷰의 입력 누락 지적(M1)을 반복하지 않으려고 diff와 manifest를 본문에 그대로 넣었다. 리뷰 질문 9개(제외 정확성, 레지스트리 비용 순서, 동시성, 소급 경로, 집계, 5창·재시작, `su_l1` 분류, 이전 MINOR 이월, 릴리스 라벨). writer v2 코드는 섞지 않았다.
5. **정식 단일 전송:** 위 상태표 순서대로 create-only. 각 단계에서 원격 바이트를 대조했다.
6. **독립 리뷰 1회:** 기존 v0.2.25 watcher의 `VALIDATED → CLAIMED → REVIEW_DISPATCHED → REVIEW_COST → COMPLETED`, 각 이벤트 1건.
7. **결과 게시:** 이 문서와 `CURRENT.md`·`TRACKER.json`.

**승인 흐름이 실제로 간소화된 지점과 그대로 남은 지점:** 사용자 중간 확인 없이 1~7이 한 번에 진행됐다. 그러나 보호 경계는 유지했다: 입력 게시만으로는 모델이 실행되지 않았고, `approve_request.py`의 16개 점검, 사용자 상한을 직접 입력하는 `--max-usd 3.0`, 보호 signer의 서명, READY 마지막 게시가 모두 남아 있었다.

## 2. 독립 리뷰 결과 (REVIEW_RESULT_1.md, 요약)

- **Q1 제외 정확성:** `auto_exclude`는 `assess`가 `PER_REQUEST_COST`를 반환한 경우에만 호출된다. 일시적·구조적 문제(`PIN_MISSING`, `IDENTITY_UNREADABLE`, `COMMIT_UNREADABLE`, `PACKAGE_INVALID`, `COMMIT_A_MISMATCH`, 범위 밖 등)는 모두 `assess` 이전에 반환되므로 제외되지 않는다. 단, `UNSUPPORTED_DELEGATION_LIMIT`가 `PER_REQUEST_COST` 뒤에 있어 위임 상한 자체가 범위 밖이면 요청이 `POLICY_STOPPED`로 제외된다(MINOR 1, 순서 nit).
- **Q2 레지스트리 비용 순서:** 등록 비용을 위임 상한보다 먼저 올리면 그 사이에 들어온 요청이 영구 제외된다. 문서에 정확히 설명돼 있고 보수적 fail-closed. **운영상 두 값을 함께 올려야 한다**(MINOR 2).
- **Q3 동시성:** `auto_exclude`와 `auto_claim`은 PK로 한 행만 남는다. 먼저 커밋된 쪽이 이긴다. 서로 다른 두 프로세스가 같은 요청을 동시에 처리하는 경우의 TOCTOU는 단일 watcher 전제에 의존하며, 이를 DB 계층에서 막는 증거는 찾지 못했다고 명시.
- **Q4 소급 경로:** 닫힌 것은 비활성 중 첫 관측, 상한 거절(신규), 완료·UNCERTAIN 이력. 운영자 의존으로 남는 것은 `enabled_at`을 과거로 낮추는 경우, 레지스트리 비용·위임 상한 불일치, `POLICY_STOPPED`의 수동 승인.
- **Q5 집계:** `reserved_cents > 0` 필터는 `window_usage`에만 영향. 존재·중복 확인은 0센트 행도 정상 처리. 깨지는 소비처 없음.
- **Q6 5창·재시작:** (request, revision)당 `auto_claim` 1회, 이후 `_resume`. `RESERVED`는 `attempts<2`이면 서명 시도가 최대 2회 가능하나 발행은 create-only라 서로 다른 서명이 둘 다 게시되는 경로는 없다. 코드 구조가 개발자의 "스텁 5회, 재시작 후 0"과 일치(리뷰어는 실행하지 않음).
- **Q7 `su_l1`:** watcher 런타임이 `su_l1`을 import하지 않음(grep), `su_l1/README`가 "NOT wired" 명시. **시험 한정 가용성 문제, LIVE 설치 비차단.** 단 원시 예외가 확보되기 전에는 `su_l1`을 활성화·연결하지 말 것.
- **Q8 이월:** 리뷰어는 이전 MINOR 2건의 본문을 받지 못해 `NOT_RUN`(MINOR 3). 제 REQUEST에 그 본문을 넣지 않은 것이 원인. §4에서 제가 대신 확인했다.
- **Q9 릴리스 라벨:** 라벨은 안전장치가 아니다. ZIP 밖에 기록할 항목: 정확한 SHA·크기, 설치 일시, 라벨을 무시한 운영자 결정, 대체되는 이전 버전·SHA, 호스트 측 `approve_request.py`, 레지스트리 비용과 위임 상한의 정합.
- **리뷰어가 읽은 파일:** `AUTO_APPROVAL.md`, `BUDGET_POLICY_CONFIGURATION.md`, `auto_approval.py`·`auto_policy.py` 전체, `state_store.py` 일부, 신규 시험, `su_l1` README 및 일부. **읽지 않은 것:** `cli.py`, `orchestrator.py`, `validator.py`, `approval_signer.py` 등 변경 없는 모듈, `CUTOVER_RUNBOOK` 본문. 즉 이 리뷰는 **이번 변경분과 호출 지점**에 대한 리뷰이지 전체 감사가 아니다.

## 3. 저의 대조·확인

- DB: 이 키의 이벤트가 각 1건(`VALIDATED`, `CLAIMED`, `REVIEW_DISPATCHED`, `REVIEW_COST`, `COMPLETED`), job `COMPLETED`·attempt 1·오류 없음, 미완료 job 0, 비용 0.5387501, 15턴. 영수증과 디스패치의 처리키가 DB 키와 일치. 중복 호출 0.
- LIVE 읽기 전용 재확인: v0.2.25, 등록 등급 1.5/3/3, 위임 `max_request_usd` 1.0, `enabled_at` 2026-11-16, 위임·설정 파일 수정 시각 불변.

## 4. 리뷰어가 놓친 문서 부정확 2건 (제가 고정 ZIP에서 직접 확인)

`docs/AUTO_APPROVAL.md`(고정 바이트)에 코드와 모순되는 서술이 남아 있다. 리뷰어는 "읽은 문서에 부정확한 내용이 없다"고 보고했다.
- 29행: "Atomic reservation (`BEGIN IMMEDIATE`, one row per request and revision, **day/month ceilings inside the same transaction**)" — 실제 `auto_claim`에는 일/월 상한이 없다.
- 74행: "**USD limits remain per request/day/month**; request identity and one-shot execution stay enforced." — 일/월 USD 상한은 더 이상 적용되지 않는다.
- 이전 v0.2.28 MINOR의 상태: (1) `approve_request.py`가 ZIP에 없다는 서술 — **수정 확인**(`BUDGET_POLICY_CONFIGURATION.md` 23행). (2) `AUTO_APPROVAL.md`의 구 상한 서술 — **부분 수정**: 25행 단계 7과 설정 예시는 고쳐졌으나 위 두 곳이 남았다.
- 영향: 운영자가 이 문서만 읽으면 일/월 상한이 있다고 오해할 수 있다. 코드 동작이나 보안에는 영향 없는 문서 오류(MINOR). **바이트가 고정돼 있어 이번 리뷰 대상은 고칠 수 없다.** GPT의 "MINOR로 자동 신규 버전·재유료 리뷰를 만들지 않는다" 원칙에 따라 새 버전은 만들지 않았다.

## 5. GPT 판정이 필요한 항목

1. **독립 리뷰 R1 수용 여부:** BLOCKING 0 / MAJOR 0. 위 §2의 범위 한정(변경분 리뷰)과 §4의 문서 오류를 포함해 `ACCEPT` / `ACCEPT_WITH_CONDITIONS` 판정.
2. **문서 오류 2건 처리:** (a) 정오표를 ZIP 밖 운영 기록에 남기고 같은 바이트를 설치하거나, (b) 문서만 고친 v0.2.30을 만들고 새 독립 리뷰를 받는다(추가 USD 3 승인 필요). 제 판단은 (a)이지만 결정은 GPT.
3. **설치 조건으로 기록할 운영 조건(리뷰어 제기):** 레지스트리 비용과 위임 상한을 함께 올리기, `enabled_at`을 낮추지 않기, Q9 기록 항목, `su_l1` 비활성 유지·원시 예외 확보 전 연결 금지.
4. **이후 단계(LIVE 설치·SHADOW·롤백·위임 USD3·소급 차단 검증):** 별도 호스트 게이트이며 이번에 시작하지 않았다.

## 6. 하지 않은 것

LIVE 설치, 위임·정책 수치·`enabled_at` 변경, 서명키·DB·Task·Notifier 변경, 이전 UI 예외 재사용, `unified` 재시도, 기존 REQUEST·영수증 재서명·재큐잉, 추가 유료 호출, 패키지 바이트 변경.
