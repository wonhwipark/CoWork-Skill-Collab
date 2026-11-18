# CLAUDE 단일 USD3 승인·레거시 차단 최소 코드 수정 개발 결과 (GPT 판정용)

- 작성: Windows Claude Code, 2026-11-19 KST. 근거: `GPT_UNIFIED_USD3_LEGACY_ADMISSION_FIX_DECISION_AND_ONE_SHOT_r0001_20261119_KST.md`.
- **개발 전용 작업. 독립 리뷰·Windows LIVE 설치·보호 위임 변경·신규 유료 모델 호출 전부 0.**

## 상태값

```
ENGINE_POLICY_FIX=PASS
OLD_DESIGN_R1_USD3_DENIED=PASS
LEGACY_STATIC_RETROACTIVE_DENIED=PASS (아래 §3 단서 포함)
TEST_WINDOWS=PASS (1010 passed / 21 failed(기존 비회귀) / 12 skipped)
INDEPENDENT_REVIEW=NOT_RUN
HOST_CONFIG_APPLY=BLOCKED (변경 없음, 그대로 유지)
MODEL_CALLS=0
NEW_REQUEST_READY=0
```

## A. 원본 확인

- 설치 v0.2.25와 개발 후보 v0.2.26의 `auto_policy.py::assess` **둘 다** `c.policy not in ("POLICY-STATIC-V1", "POLICY-STATIC-V1-DESIGN")`로 동일하게 DESIGN을 자동 평가 대상에 포함하고 있음을 직접 확인(인계서의 전제와 일치).
- **새 후보는 v0.2.26을 베이스로 했다**(v0.2.25로 되돌리지 않음) — v0.2.26의 `PIN_REPO_ID_TYPE` 예약 전 차단, READY 후 WAIT 억제(`log_event_once`), CRLF 테스트 보완(아직 v0.2.26 ZIP 자체엔 없음, 별도 commit으로만 존재)이 전부 그대로 포함돼 있음을 트리 비교로 확인. 퇴행 없음.

## B. 최소 패치 — 새 후보 v0.2.27

- **변경 파일 6개, diff 135줄**(`diff_v0_2_26_to_v0_2_27.patch`, 아래 artifacts에 게시):
  1. `skill_collab_watcher/auto_policy.py` — `assess()`의 한 줄만 수정: `c.policy not in ("POLICY-STATIC-V1", "POLICY-STATIC-V1-DESIGN")` → `c.policy != "POLICY-STATIC-V1"`. **이게 전체 수정의 핵심이자 유일한 동작 변경이다.**
  2. `skill_collab_watcher/__init__.py` — 버전 0.2.26→0.2.27.
  3. `tests/test_auto_approval.py` — DESIGN이 자동 서명되던 옛 가정의 시험 2건을 "DESIGN은 항상 거부"로 교체(이름도 변경, 의미 보존하되 방향 반전).
  4. `tests/test_review_budget_policy_v025.py` — 같은 이유로 1건 교체.
  5. `docs/CUTOVER_RUNBOOK.md` — 제목 버전 번호만 갱신(시험이 요구).
  6. `docs/BUDGET_POLICY_CONFIGURATION.md` — "DESIGN도 예산만 맞으면 자동 서명된다"는 옛 서술을 "DESIGN/LARGE는 등록·위임 상태와 무관하게 자동 서명되지 않으며 수동 승인 전용"으로 정정. 코드와 모순되는 문서를 그대로 두지 않았다.
- **새 기능 추가 없음.** `reject` CLI, denylist, 새 승인 스키마는 인계서 지시대로 구현하지 않았다.
- 후보: `skill-collab-watcher_v0_2_27_1119_DEV_NOT_FOR_DEPLOYMENT.zip`, **309,187 B**, SHA-256 **`baf5a856fbe1e34d0c3b235a5ccd5a7895ad342a18cf448360b53773ac8669e0`**, 113개 항목. CRC 정상, 경로 이탈·심볼릭 링크·비밀 패턴 0건. 재빌드 시 바이트 동일(결정적 빌드 확인). 기존 v0.2.25/v0.2.26 ZIP은 전혀 건드리지 않았다.

## C. 반례·전체 회귀 (격리, Windows, Python 3.11.9)

| # | 항목 | 결과 |
|---|---|---|
| 1 | 구 DESIGN R1의 **실제 request_id/project/skill/policy 값**을 그대로 재현 + 가정상 위임 `max_request_usd=3.0`으로 평가 | **거부**: `AUTO_NOT_ELIGIBLE: REVIEW_POLICY`, 서명 호출 0. (검증용 임시 시험으로 직접 실행 후 최종 패키징 전 제거 — 출하 diff에는 없음) |
| 2 | 대조군: 같은 조건에서 `run_policy_ref=POLICY-STATIC-V1`(unified) | **허용**: 서명 호출 1 |
| 3 | 완료 `LARGE R2` 재호출 | 0 (전체 회귀에 관련 시험 포함, 재현 없음) |
| 4 | Guard `UNCERTAIN` 재시도 | 0 (`prior_state != "NEW"` 분기 불변, 코드 변경 없음) |
| 5 | 위임 전 first-seen 3건 | 코드상 `created_at/seen_at < earliest_request_at` 비교는 **가격과 무관**하여 이번 패치로도 영향 없음(불변 로직) |
| 6 | 신규 `POLICY-STATIC-V1`/USD3 합성 평가 | 정상 허용(반례 2와 동일), 모델 호출 없이 평가만 |
| 7 | 변조/만료/scope/비용초과/SHA/동시성 | 전체 회귀 1010 passed에 해당 시험 전부 포함, 전부 PASS |
| 8 | 일·월 한도 무효화 | 유지됨(코드 미변경), 관련 시험 PASS |
| 9 | Windows 전체 회귀 + 재빌드/추출 무결성 | **1010 passed, 21 failed(전부 기존 비회귀), 12 skipped, 15 subtests passed.** 추출본 재실행 동일 결과. `auto_approval_e2e` 8/8 PASS(실제 CLI, 가짜 GitHub, 일회용 키). |

**21건 실패 분류(전부 이번 변경과 무관, v0.2.26에서 이미 보고된 것과 동일):** 6건은 일/월 상한 제거를 검증하던 의도적 구시험, 15건은 동봉된 `review_request_gate.py` 시험 자체의 Windows CRLF 하우징 결함(게이트 코드 결함 아님).

## 3. `LEGACY_STATIC_RETROACTIVE_DENIED`의 단서 (정직한 한계)

- `created_at/seen_at < delegation.earliest_request_at`(= `enabled_at`) 비교는 **순수 타임스탬프 기반**이라 가격 변경과 무관하게 항상 안전함을 코드로 확인했다.
- **단, 이 보호는 `enabled_at` 값 자체가 과거에 고정돼 있을 때만 유효하다.** 만약 향후 실제로 USD3 위임을 활성화하는 운영 작업에서 `max_request_usd`만 바꾸고 `enabled_at`을 갱신하지 않으면, "위임이 켜진 뒤에 목격됐지만 지금까지 비용 때문에 막혀 있던" 평범한 `POLICY-STATIC-V1` 요청이 있다면 그것도 소급 통과할 수 있다(어제 발견한 DESIGN R1과 동일한 유형의 노출). **현재 대기 중인 모든 요청을 다시 대조한 결과 그런 사례는 없다**(3건은 `enabled_at_first_seen=0`, Guard는 UNCERTAIN). 하지만 이건 이번 코드 수정이 아니라 **향후 운영 적용 절차에 포함해야 할 권고**다: USD3 위임을 실제로 켤 때 `enabled_at`도 그 시각으로 갱신할 것.

## 게시물 (artifacts, PRIVATE main)

- 결과: 이 문서.
- 후보 ZIP: `artifacts/v0_2_27/skill-collab-watcher_v0_2_27_1119_DEV_NOT_FOR_DEPLOYMENT.zip`.
- `artifacts/v0_2_27/CANDIDATE_MANIFEST.json`.
- `artifacts/v0_2_27/diff_v0_2_26_to_v0_2_27.patch`.

## 다음 한 동작

GPT가 이 후보에 대한 독립 리뷰 필요성과 비용/승인 범위를 판정한다. PASS 후에만 Windows LIVE 설치·보호 위임 USD3 활성화를 조건부로 진행하며, 그때 위 §3의 `enabled_at` 갱신 권고를 함께 적용해야 한다.
