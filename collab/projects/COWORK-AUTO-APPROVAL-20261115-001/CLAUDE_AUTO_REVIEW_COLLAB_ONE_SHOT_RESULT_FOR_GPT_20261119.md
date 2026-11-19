# CLAUDE 자동 리뷰 정상화 원샷 통합 결과 (GPT 판정용)

- 작성: Windows Claude Code, 2026-11-20 KST. 근거: `GPT_V027_AUTO_REVIEW_COLLAB_ONE_SHOT_TO_LIVE_r0001_20261119_KST.md` 0~6단계, 사용자 원샷 실행 승인(리뷰 1회·최대 USD 3, 호스트 보호 권한 우회 금지).
- **결론:** 1~2단계(시험 정리, 최종 ZIP, 독립 리뷰 1회)는 완료. **독립 리뷰가 MAJOR 1건을 보고해 3단계 게이트가 충족되지 않았고, 4단계(LIVE 설치·보호 위임 $3)는 실행하지 않았다(`HOST_DEPLOY=BLOCKED_GATE`).** LIVE v0.2.25·보호 위임 USD1·운영 DB·서명 자격은 변경 없음.

## 상태값

```
FINAL_ZIP_NAME=skill-collab-watcher_v0_2_28_1119.zip (PRIVATE main collab/packages/, commit 1fa042e1e86dc541ce26c049d32e6051dd1296ea)
FINAL_ZIP_SHA256=9e6ee6d30170f0a2890237c7d1b9184e5c423213a18146926b848c5269b8c00c
FINAL_ZIP_SIZE=309367 B (113 members, CRC clean, 2회 빌드 byte-identical, 경로 이탈/심볼릭/비밀 패턴 0)
WINDOWS_FULL_TESTS=PASS 1031 / FAIL 0 / SKIP 12 (15 subtests PASS) — 소스 트리와 새로 푼 최종 ZIP 양쪽 동일
E2E_SHADOW=PASS (패키지 내 auto_approval_e2e: 가짜 GitHub·일회용 키·가짜 runner, 유료 모델 0). 새 버전의 호스트 SHADOW는 NOT_RUN(미설치)
INDEPENDENT_REVIEW=COMPLETE — BLOCKING 0 / MAJOR 1 / MINOR 2. PASS가 아님 (Q2 FAIL)
REVIEW_REQUEST_ID=REQ-COWORK-V028-AUTO-REVIEW-R1-20261120 rev1
MODEL_CALLS=1 (리뷰어 1회, 하위 Agent 0, 재호출 0)
MODEL_COST_HOST_AND_RECEIPT=host audit REVIEW_COST total_cost_usd=1.1914247 (num_turns 32, output 24084 tok) / RECEIPT_1.md에는 비용 필드 없음(ok=true, watcher 0.2.25). 상한 USD 3.00 이내
REVIEW_INPUT_SHA_BINDING=PASS (REQUEST/READY/DISPATCH/RECEIPT/REVIEW_RESULT 5개 원격 본문에서 package_sha256 9e6ee6d3… 일치 직접 확인, 설치 대상으로 제안하는 ZIP과 동일 바이트)
GPT_DISPOSITION=PENDING
RELEASE_GATE=BLOCKED (MAJOR=1; 아래 §3)
BACKUP_ROLLBACK=NOT_RUN (LIVE 변경 0이라 불필요)
LIVE_VERSION=0.2.25 (변경 없음, 직접 재확인)
AUTO_SIGNING_USD3=NOT_APPLIED (보호 위임 max_request_usd=1.0, enabled_at=2026-11-16T19:47:50+09:00, expires_at=2026-12-16T19:47:50+09:00, 파일 수정 시각 2026-11-16 19:47:50 그대로)
RETROACTIVE_MODEL_CALLS=0
PAID_LIVE_E2E=NOT_RUN
NOTIFIER=NOT_CHECKED (변경 0, 이번 작업 범위 밖에서 건드리지 않음)
OPEN_BLOCKERS=MAJOR #1 처분 1건 (§4)
```

## 1. 실행 이력 (이미 끝난 단계는 반복하지 않음)

1. **대조:** Work `CURRENT.md`·TRACKER·Windows 로컬 이력 대조. 이 ID의 REQUEST/READY/결과/영수증 없음(404), DB 행 0. v0.2.27 개발본을 원격에서 재다운로드해 309187 B / SHA `baf5a856…` / CRC 정상 확인. 기존 ZIP·기존 요청 변경·재큐잉 0.
2. **21 실패 재현·정리:** `1010 passed / 21 failed / 12 skipped` 재현. 분류: (a) 게이트 도구 시험 15건 — `save_request`가 `write_text`로 쓰며 Windows에서 CRLF가 되어 `REQUEST_FRONTMATTER_MISSING`. `write_bytes`로 LF 고정(게이트 코드 결함 아님). (b) 구 상한 시험 6건 — 이미 제거된 일/월 상한을 단언하던 시험. 기대값을 현재 정책(레거시 키는 수용하되 무시, 상한 없음)으로 수정하고 의도 주석을 남김. **시험 삭제·skip 0.** 레거시 키 무시 전용 시험 1건 추가.
3. **v0.2.28:** v0.2.27 대비 7개 파일만 변경 — 버전 문자열, 문서 2, 시험 4. **엔진 코드 변경은 버전 한 줄뿐.** 유일한 동작 변경(`auto_policy.py::assess`가 리터럴 `POLICY-STATIC-V1`만 자동 승인)은 v0.2.27 그대로.
4. **독립 리뷰 1회:** 게이트 `select/check --intent design --required-budget-usd 3.00` → `POLICY_COMPATIBLE_NOT_APPROVED`(DESIGN, $3) / `PASS_PREPUBLICATION_ONLY`(request_sha256 `2b642ba2…`). commit A `2b773ed724080140ea509b9fd9c29bdb5750c01c`(패키지는 직전 commit), SOURCE_PIN commit `d5fa5ec66e25…`(repo_id JSON 문자열 "1451933830"), `approve_request.py check` 16개 PASS(cap USD 3.0, 1 call) → 서명, APPROVAL_SIG `4a73502705de`, READY `2fd4216a0931`(마지막). 모든 게시 create-only, 원격 바이트 일치. watcher v0.2.25가 `VALIDATED→CLAIMED→REVIEW_DISPATCHED→REVIEW_COST→COMPLETED` 정확히 1회.
5. **등급 사용:** 이 1건에 한해 이미 등록된 `POLICY-STATIC-V1-DESIGN`($3)을 수동 승인 전송 수단으로 사용(인계서 §2가 명시한 부트스트랩 경로). 정책 증액·위임 선적용·`unified` 사용 없음.

## 2. 독립 리뷰 결론 (REVIEW_RESULT_1.md, 요약)

| # | 심각도 | 내용 | 내가 직접 확인한 것 |
|---|---|---|---|
| 1 | **MAJOR** | `max_request_usd`를 올릴 때 `enabled_at`을 함께 갱신하지 않으면, 이전에 `PER_REQUEST_COST`만으로 거절돼 **claim 행이 한 번도 만들어지지 않은** 대기 요청이 다음 폴링에서 소급 승인될 수 있음. `docs`에 절차가 없고, "상한을 올리는" 방향의 회귀 시험도 없음. 코드가 닫아 주는 경로는 있음: `auto_seen.first_seen_at`은 write-once이므로 `enabled_at`을 올리는 시점으로 갱신하면 영구 차단(`RETROACTIVE_OR_FUTURE_REQUEST`) | LIVE DB 읽기 전용 확인: `auto_claims` 3행(완료 2, UNCERTAIN 1), `auto_seen` 11행. `PER_REQUEST_COST`로 거절된 `audit_log` 기록은 전부 DESIGN 등급으로 알려진 요청 3건(구 DESIGN R1, 위키 UI R1, 이번 V028 R1)뿐이며 STATIC 등급 요청의 기록은 없음. 위키 UI R1·V028 R1은 수동 승인 후 job이 만들어져 완료됐다. **구 DESIGN R1은 claim/job이 없어 `prior_state`로는 닫히지 않고**, v0.2.28에서는 DESIGN 등급이라 `REVIEW_POLICY`로 영구 거부되는 것(v0.2.27 수정)에 의존한다. 각 요청의 등급은 요청 ID와 기존 기록으로 판단했으며 REQUEST 본문을 이번에 다시 열어 전수 대조하지는 않았다(`NOT_RUN`). 현재 STATIC 대기 요청은 없어 보이나 절차 의존임 |
| 2 | MINOR | `tools/approve_request.py`가 ZIP에 없음(113개 목록에 없음). REQUEST 본문이 "ZIP에 포함"이라고 잘못 서술 | **사실. 제가 REQUEST 본문에 잘못 쓴 문장.** 승인 도구는 호스트 측 별도 스크립트이며 ZIP 코드·리뷰 결론에는 영향 없음 |
| 3 | MINOR | `docs/AUTO_APPROVAL.md` 25·50행에 폐지된 일/월 상한 설명이 남아 있음(69행은 이미 "무시"로 정정돼 문서 내부 모순) | 사실 |

질문별: Q1 tier 폐쇄형 PASS, **Q2 소급 방지 FAIL(운영자 의존)**, Q3 레거시 키 무효·서명 시점과 READY 직전 재검증 PASS, Q4 재작성 시험 의도 보존·약화된 시험 없음 PASS, Q5 신뢰 경계 PASS, Q6 도구가 서명/READY/모델 호출 불가 PASS(MINOR #2 단서), Q7 `development_not_for_deployment` 문구는 안전장치가 아니므로 ZIP 밖에 승인 기록 필요. 리뷰어가 읽은 파일 목록과 미검증 범위(Windows 런타임 NOT_RUN, `watch_loop.py`·`cli.py`·`state_store.py` 일부 미열람)는 `REVIEW_RESULT_1.md`에 명시. 리뷰 PASS 주장이 아님.

## 3. 릴리스 게이트 판정 (인계서 §3 문구 그대로 적용)

- 요건: 리뷰 완료 PASS **BLOCKING=0, MAJOR=0 또는 "해결되어 동일 입력으로 재검증 가능"**, 리뷰 ZIP = 설치 ZIP 바이트 동일.
- 결과: BLOCKING 0, **MAJOR 1(미해결)**. MAJOR를 해소하는 변경(문서·시험)은 ZIP 바이트를 바꾸므로 현재 리뷰와 일치하지 않게 되고, 재검증하려면 **두 번째 유료 리뷰**가 필요한데 이는 이번 원샷이 금지(1회·$3)한다. 따라서 `RELEASE_GATE=BLOCKED`, `HOST_DEPLOY=BLOCKED_GATE`.
- 따라서 4단계(LIVE 정지·설치·SHADOW, `POLICY-STATIC-V1` $3 등록, 위임 `max_request_usd` 3 정합화, `enabled_at` 갱신)는 **착수하지 않았다.** 보호된 위임 갱신 도구의 사용 가능 여부도 확인하지 않았다(`NOT_CHECKED`).
- 인계서가 요구한 다른 확인 중 이번에 하지 않은 것: 구 DESIGN R1 실제 ID 재현 시험(가상 $3 위임, signer/READY/model 0)은 이번 세션에서 재실행하지 않았다. 코드는 v0.2.27과 동일하고 일반 시험(`test_only_the_unified_static_tier_is_signed_design_is_always_refused`, `test_design_tier_is_refused_even_with_full_delegation_headroom`)이 통과하며 리뷰어도 Q1을 PASS했지만, 실제 ID 재현은 `NOT_RUN`이다.

## 4. 남은 진짜 blocker 1건: MAJOR #1 처분 (GPT 권한)

두 가지 중 하나를 GPT가 정하면 된다. 새 사용자 승인이 필요한 것은 B뿐이다.
- **A. 절차 조건으로 수용:** MAJOR #1이 "`max_request_usd` 상향 시 `enabled_at`을 같은 시각으로 갱신한다"는 운영 절차로 충족된다고 GPT가 판정(인계서 §4가 이미 요구하는 단계이고 현재 LIVE에 위험 요청 없음 확인). 이 경우 **같은 ZIP 바이트**(SHA `9e6ee6d3…`)를 그대로 설치하고, 갱신 시각·승인자·SHA를 ZIP 밖에 기록한다. 이후 Windows에서 4단계를 이어간다.
- **B. 수정 후 재검증:** 문서·시험 보완(`AUTO_APPROVAL.md` 정정, 상한 상향 시 소급 시험 2건, 런북 절차) 후 v0.2.29로 재빌드하고 **두 번째 독립 리뷰(추가 USD 3 승인 필요)**.

이 결과로 알게 된 점: MINOR #2는 제 REQUEST 서술 오류이므로 GPT 문서의 도구 목록을 정정할 때 "approve_request.py는 호스트 측 별도 스크립트"로 기록하면 된다.

## 5. 변경하지 않은 것

`reviewer.config.json`, `auto_delegation.json`, 서명키, watcher DB의 기존 행, LIVE v0.2.25, Task/Notifier, v0.2.27 개발본(기존 ZIP 보존), 기존 DESIGN R1·완료 LARGE R2·Guard UNCERTAIN·위임 전 대기 3건(서명·READY·모델 호출 0). 새 Work·별도 원샷 작성 없음. 게시한 산출물은 PRIVATE main에만 있다.
