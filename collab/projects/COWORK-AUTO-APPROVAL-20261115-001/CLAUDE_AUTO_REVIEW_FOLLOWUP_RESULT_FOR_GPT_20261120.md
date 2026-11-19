# CLAUDE 자동 리뷰 원샷 후속 결과 — MAJOR 보완·영수증 정산 (GPT 판정용)

- 작성: Windows Claude Code, 2026-11-20 KST. 근거: 기존 원샷 Work `COWORK-AUTO-APPROVAL-20261115-001`, 직전 통합 결과 `CLAUDE_AUTO_REVIEW_COLLAB_ONE_SHOT_RESULT_FOR_GPT_20261119.md`, 사용자 지시 "승인·실행 상태 점검 및 MAJOR 보완, 추가 유료 리뷰·재서명·READY 재게시·모델 재호출 금지".
- **결론:** 영수증 정산 완료(`SETTLED`), 리뷰 MAJOR 1건은 **재현 확인 후 dev 코드에서 수정**, 신규 ZIP **v0.2.29**를 별도 버전·SHA로 보존. **v0.2.28 독립 리뷰 PASS는 v0.2.29에 승계하지 않음.** v0.2.29 독립 리뷰는 아직 없음. **LIVE 설치와 USD3 보호 위임 변경은 HOLD 유지.**

## 상태값

```
RECEIPT_SETTLEMENT=SETTLED (watcher DB audit 기준; 영수증 본문에는 비용 필드 없음)
MODEL_CALLS=1 (REVIEW_DISPATCHED 1건, 같은 processing_key 재호출 0)
ACTUAL_COST=USD 1.1914247 (REVIEW_COST total_cost_usd, num_turns 32, output 24084 tok, 상한 USD 3.00 이내)
JOB_STATE=COMPLETED (jobs 테이블, result_path 기록), UNCERTAIN 0
REVIEW_V028_MAJOR_1=CONFIRMED (재현 시험이 v0.2.28에서 실패) → FIXED_IN_DEV v0.2.29
REVIEW_V028_MINOR_1=CONFIRMED (REQUEST 서술 오류) → 문서 정정 완료
REVIEW_V028_MINOR_2=CONFIRMED (AUTO_APPROVAL.md 구 상한 서술) → 문서 정정 완료
V029_ZIP=skill-collab-watcher_v0_2_29_1120.zip, 310753 B, SHA256 c67bc342fe77547b000fc42e1b886396cbef035c0d265dbcd124947e267ed83f, 114 members
V029_TESTS=PASS 1034 / FAIL 0 / SKIP 12 (소스 트리와 추출한 ZIP 바이트 양쪽 동일, 신규 3건 포함)
V029_INDEPENDENT_REVIEW=NOT_RUN (v0.2.28 리뷰 PASS 승계 안 함)
LIVE_VERSION=0.2.25 (변경 없음)
DELEGATION=max_request_usd 1.0, enabled_at 2026-11-16T19:47:50+09:00 (변경 없음)
REQUEST_READY_RESIGN=0, READY_REPOST=0, MODEL_CALLS_THIS_TURN=0
HOST_DEPLOY=HOLD (MAJOR 해소 코드는 리뷰 전이므로 설치 근거 없음)
```

## 1. 영수증·정산 대조 (읽기 전용)

- watcher DB `audit_log`, 키 `REQ-COWORK-V028-AUTO-REVIEW-R1-20261120|1|9e6ee6d3…|1`: `VALIDATED` → `CLAIMED` → `REVIEW_DISPATCHED`(run_policy_ref `POLICY-STATIC-V1-DESIGN`, max_budget 3.0) → `REVIEW_COST`(total_cost_usd 1.1914247, num_turns 32, output 24084, cache write 91464 / read 917329) → `COMPLETED`. 키별 이벤트 수는 각 1건씩이며 중복 디스패치 없음.
- `jobs` 테이블: `COMPLETED`, attempt_count 1, last_error 없음.
- 원격 바이트 재확인(본문 sha256): `RECEIPT_1.md` `c45f21fc…`, `REVIEW_RESULT_1.md` `5c1d9c9a…`, `DISPATCH_1.md` `5f374a23…` — 로컬 사본과 일치. `APPROVAL_SIG.json`·`READY.md`는 원격 존재 확인(게시 시 readback 일치).
- **정산 주의:** `RECEIPT_1.md`에는 비용·호출 필드가 없다(`ok: true`, processing_key, sha, watcher 0.2.25만 있음). 비용의 출처는 DB `REVIEW_COST`이며 영수증으로 확인되는 값이 아니다. GPT가 영수증 스키마 확장을 원하면 별도 처리.

## 2. 독립 리뷰 지적 검토

- **MAJOR 1 — 확인됨, 재현됨.** `auto_policy.assess`는 `PER_REQUEST_COST`를 claim 생성 전에 반환하고, 그 거절을 영구 기록하지 않는다. 그래서 상한을 올리고 `enabled_at`을 그대로 두면 같은 요청이 다음 폴링에서 READY까지 간다. 시험(`test_a…`)이 v0.2.28에서 `READY_POSTED`를 보여 실패함을 확인했다. 현재 LIVE DB에는 대기 중인 STATIC 요청이 없고, 이번 V028 R1은 수동 승인으로 처리됐다(감사 결과).
- **MINOR 1 — 확인됨.** `approve_request.py`는 ZIP에 없다. 원인은 제가 쓴 REQUEST 본문 문장이다. ZIP 코드 결론에는 영향 없음. `BUDGET_POLICY_CONFIGURATION.md`에 "호스트 측 별도 스크립트, 패키지에 없음"을 명시.
- **MINOR 2 — 확인됨.** `AUTO_APPROVAL.md`의 `max_day_*`/`max_month_*` 서술과 예시 JSON 정정, 일/월 게이트를 제거된 것으로 기술.

## 3. v0.2.29 최소 보완 (dev, 미설치)

- `auto_approval.py::_process`: `assess`가 `PER_REQUEST_COST`를 반환하면 `store.auto_exclude(...)`로 `auto_claims`에 종결 행(`stage=POLICY_STOPPED`, `reserved_cents=0`)을 남긴다. 이후 폴링은 기존 `_resume`의 종결 처리로 서명 없이 멈춘다. DB 스키마 변경 없음.
- `state_store.py::_auto_usage_locked`: `reserved_cents > 0` 행만 사용량 집계에 포함. 제외 행이 호출 횟수로 잡히지 않게 한다.
- 영향 범위: 거절 당시 pin·패키지·commit·scope·정책 검증을 모두 통과하고 **상한만 못 미친** 요청에만 적용. 실패 사유가 일시적인 읽기 오류, PIN 누락 등은 기존대로 claim 없이 다음 폴링에서 재평가된다. 운영 절차 의미: 상한을 올린 뒤 이전에 상한 때문에 거절된 요청을 자동으로 살리려면 **수동 승인**만 가능하다.
- 시험: `tests/test_v029_cost_refused_exclusion.py` 3건. (a) 상한 상향 후 `POLICY_STOPPED`, READY 없음, 서명 0 — v0.2.28에서 실패, v0.2.29에서 통과. (b) 상향 후 처음 보이는 요청은 여전히 `READY_POSTED`. (c) 제외 요청은 사용량 집계에서 호출 0·센트 0.
- 문서: `AUTO_APPROVAL.md`(구 상한 서술 제거, 상향 절차 설명), `BUDGET_POLICY_CONFIGURATION.md`(제외 규칙, approve_request 위치), `CUTOVER_RUNBOOK.md` 제목 버전 0.2.29.

## 4. 변경 파일과 보존

- v0.2.28 대비 변경 6개 파일 + 신규 시험 1개: `auto_approval.py`, `state_store.py`, `__init__.py`, 문서 3개, 신규 시험 1개. 제거 0.
- 보존 위치: PRIVATE main `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/artifacts/v0_2_29/` — ZIP, `CANDIDATE_MANIFEST_v029.json`(`inherits_review_pass_from: null`), `diff_v0_2_28_to_v0_2_29.patch`. v0.2.28 ZIP은 `collab/packages/`에 그대로 두고 변경하지 않음.
- 빌드 재현: 두 번 빌드해 바이트 동일, CRC 정상, 경로 이탈 0, 비밀 패턴 0.

## 5. 차단 사유와 다음 조치 (GPT 판정)

1. **v0.2.29 독립 리뷰 필요.** 설치 전 이 바이트에 대한 독립 리뷰가 필요하다. 추가 유료 리뷰이므로 사용자의 새 승인이 필요하며 이번 작업에서는 실행하지 않았다.
2. **v0.2.28 경로 A 유지 가능.** MAJOR를 절차(상한 상향과 `enabled_at` 갱신을 함께)로 수용한다면 v0.2.28 바이트(SHA `9e6ee6d3…`)를 설치하는 방식이 여전히 가능하다. 다만 v0.2.29의 코드 보완이 같은 위험을 코드로 막으므로 **v0.2.29로 가는 편이 안전하다**는 것이 제 판단이다.
3. **LIVE 설치·USD3 보호 위임 변경: HOLD.** 위 1 또는 2가 확정되기 전에는 `reviewer.config.json`, `auto_delegation.json`(`max_request_usd` 1→3, `enabled_at`), 서명 자격, DB, Task, Notifier를 건드리지 않는다.
4. 영수증 비용 필드 부재는 설치 차단 사유는 아니며, 스키마 확장을 원하면 GPT가 별도 지시.

## 6. 하지 않은 것

재서명, READY 재게시, 모델 재호출, 추가 독립 리뷰, LIVE 정지·설치, 위임 값 변경, 서명키·DB·Task·Notifier 변경, 기존 요청 재큐잉.
