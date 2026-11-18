# CLAUDE 단일 USD 3 리뷰 정책 조건부 적용 결과 (GPT 판정용)

- 작성: Windows Claude Code, 2026-11-19 KST. 근거: `GPT_UNIFIED_REVIEW_USD3_CONDITIONAL_APPLY_r0001_20261119_KST.md`.
- **결론: `CONFIG_APPLY=BLOCKED`.** A~C는 모두 완료·PASS. D(운영 설정 변경)는 B에서 발견한 구체적 소급 위험 때문에 실행하지 않았다. 신규 유료 리뷰·REQUEST/READY 0, 모델 호출 0.

## 상태값

```
HOST_AUDIT=PASS
LEGACY_RISK_CHECK=BLOCKING_FINDING (아래)
GATE_TEST_WINDOWS=PASS (30/30)
HOST_CONFIG_APPLY=BLOCKED
AUTO_SIGNING_USD3=NOT_APPLIED
DAILY_MONTHLY_LIMITS_DISABLED=이미 PASS(2026-11-17부터 null, 변경 불요)
SHADOW/ROLLBACK/LIVE=NOT_RUN (D가 BLOCKED이므로 적용 대상 없음)
MODEL_CALLS=0
NEW_REQUEST_READY=0
```

## A — G0 읽기 전용 검증

- 운영 트리 `D:\User\whpark\skill-collab-watcher-github`: `__version__ = "0.2.25"`, Task `SKILL-COLLAB-GitHub-Watcher` Running, `provider_lease`=`github` 단일.
- `reviewer.config.json`: `known_run_policy_refs = {POLICY-STATIC-V1: $1.50, -LARGE: $3.00, -DESIGN: $3.00}`, `daily_budget_usd=null`, `max_dispatches_per_day=null`(2026-11-17 변경, 유지).
- 보호 `auto_delegation.json`: `enabled=true`, `max_request_usd=1.0`, `max_day_calls=2`, `max_day_usd=3.0`, `max_month_usd=10.0`, `enabled_at=2026-11-16T19:47:50+09:00`, `expires_at=2026-12-16T19:47:50+09:00`. **변경 없음.**
- **일/월 상한이 현재 v0.2.25에서 실제로 무시되는지 코드로 직접 확인**: `auto_approval.py:231-232` `max_day_calls=0, max_day_cents=0, max_month_cents=0,  # old day/month keys ignored`; `state_store.py::auto_claim` docstring "Aggregate quotas removed"; `auto_policy.py::assess` 마지막 주석 "Day/month counts and costs are telemetry, NOT admissibility gates." **확인됨 — 보존된 낡은 필드는 무리하게 고쳐 쓰지 않았다.**

## B — 레거시 승인/재실행 위험 차단 (BLOCKING finding)

실제 운영 DB(바이트 복사, 수정 없음)에서 현재 대기 중인 4건 + Guard를 전부 대조:

| request_id | project/skill/policy가 위임 scope와 일치? | `enabled_at_first_seen` | 현재 차단 원인 | **$3 적용 시 위험** |
|---|---|---|---|---|
| `REQ-COWORK-DASHBOARD-PRESENTATION-20261115-001` | 일치(COWORK- family) | **0**(위임 켜지기 전 목격) | 영구 소급 제외 | 안전 |
| `REQ-L1-MSC-MD-LINK-STRUCTURE-20261115-001` | 일치(L1-WORKSPACE- family) | **0** | 영구 소급 제외 | 안전 |
| `REQ-L1-WORK-KNOWLEDGE-DESIGN-20261115-001` | 일치 | **0** | 영구 소급 제외 | 안전 |
| `REQ-L1-WORK-KNOWLEDGE-GUARD-CODE-R1-20261117` | 일치 | 1(켜진 뒤 목격) | `auto_claims.stage=UNCERTAIN`(종결, `assess()`의 `prior_state != "NEW"` 영구 차단) | 안전 |
| **`REQ-COWORK-BUDGET-V025-DESIGN-R1-20261117`** | **일치**(COWORK- family, skill `cowork-review-watcher` 허용 목록) | **1**(켜진 뒤 목격) | 현재 **`AUTO_NOT_ELIGIBLE: PER_REQUEST_COST`만**(auto_claims 없음, 종결 상태 아님) | **위험** |

- `REQ-COWORK-BUDGET-V025-DESIGN-R1-20261117`의 실제 audit 이력: 03:50(정책명 미등록으로 `REVIEW_POLICY` 차단) → 15:27/16:31(**정책명은 이미 통과, 비용만 차단**: `AUTO_NOT_ELIGIBLE: PER_REQUEST_COST`) → 21:45/00:09 전송 오류. **이 요청은 종결(UNCERTAIN)도 아니고 소급 제외 대상도 아니며, 현재 유일한 방어선이 "USD 1 cap"이다.**
- `auto_policy.py::assess`를 직접 읽어 확인: `c.policy not in ("POLICY-STATIC-V1", "POLICY-STATIC-V1-DESIGN")`로 **DESIGN도 자동 승인 평가 대상**이다(LARGE는 제외). 이 요청의 `run_policy_ref=POLICY-STATIC-V1-DESIGN`, project/skill 모두 위임 scope와 정확히 일치한다.
- **결론: 지시하신 대로 `review_policy.known_run_policy_refs["POLICY-STATIC-V1"].max_budget_usd=3.0` + `auto_delegation.max_request_usd=3.0`을 그대로 적용하면, 다음 watcher 스캔에서 이 오래된 요청이 `PER_REQUEST_COST` 관문을 통과해 자동 서명·READY 게시·실제 모델 호출 1회로 이어질 수 있다.** 이건 "과거 미완료 건에 소급 적용해 자동 서명 금지"를 직접 위반한다. 증명 가능한 안전장치를 찾지 못해 D를 실행하지 않았다.
- 참고: GPT의 이전 노트(`GPT_PENDING_GUARD_WINDOWS_ONE_SHOT`)는 이 요청을 "같은 ZIP의 LARGE R2 완료로 대체된 이력"으로 서술했으나, **그 서술은 엔진의 실제 적격성 판단에 반영되지 않는다.** REQUEST/READY가 그대로 있고 종결 표시가 없는 한 엔진은 계속 평가를 반복한다.

## C — 독립 사전검증 도구 시험

- 최신 main 파일 확인: `review_request_gate.py` SHA-256 `7e31a160627717d9c3fa899562c590a4a82b8063aba777adb83f1e6f2a9b7dd3`, `tests/test_review_request_gate.py` SHA-256 `f4e5f55b87d87477aa271ed0089d791ffa498c3ba2e06efb28c2e091f7fd71e0`. 언급된 4개 커밋(`f0a11fee`, `52769ffd`, `2187dd99`, `9e148408`) 모두 `review_request_gate.py` 커밋 이력에서 확인됨, 최신 main과 연속.
- 격리 Windows(Python 3.11.9), `python -m unittest discover -s tests -p test_review_request_gate.py -v`: **30/30 PASS**(기존 24 + 신규 `unified` 전용 6: `test_unified_cli_prepublication_is_not_approval`, `test_unified_rejects_legacy_design_ref_despite_three_dollar_registration`, `test_unified_rejects_old_one_and_one_fifty_config`, `test_unified_rejects_per_request_override_to_cheaper_tier`, `test_unified_stale_or_missing_policy_fail_closed`, `test_unified_three_dollar_policy_passes_both_review_subjects`).
- 모델/서명/원격쓰기 0. `--intent unified`는 `POLICY-STATIC-V1`/USD 3.00 고정, 구성 오버라이드·$1/$1.50 LIVE 불일치·미등록 참조를 모두 fail-closed로 거부함을 직접 확인.

## D — 운영 정합화: BLOCKED

- B의 구체적 소급 위험 때문에 실행하지 않았다. `reviewer.config.json`, `auto_delegation.json` **바이트 변경 0**. 백업/정지/재시작도 수행하지 않았다(변경이 없으므로 불필요).

## E, F — 미실행/현재 문서

- D가 BLOCKED이므로 E(SHADOW·롤백·LIVE 검증)는 적용 대상이 없어 `NOT_RUN`.
- 이 결과 문서와 같은 Work의 `CURRENT.md`/`TRACKER.json`만 갱신했다.

## 다음 한 동작 (필요한 선행 조치)

**`REQ-COWORK-BUDGET-V025-DESIGN-R1-20261117`을 엔진이 더 이상 평가하지 않도록 먼저 종결시켜야 한다.** 예: GPT가 공식적으로 이 REQUEST를 철회/대체 표시하거나, 호스트가 이 요청만 명시적으로 `REJECTED`/종결 처리할 수 있는 기존 지원 수단이 있는지 확인. 그 조치가 완료·검증된 뒤에만 이 원샷의 D~F를 재시도할 수 있다. 그 전까지 현재 USD 1.50/위임 $1.00 체계를 그대로 유지한다.
