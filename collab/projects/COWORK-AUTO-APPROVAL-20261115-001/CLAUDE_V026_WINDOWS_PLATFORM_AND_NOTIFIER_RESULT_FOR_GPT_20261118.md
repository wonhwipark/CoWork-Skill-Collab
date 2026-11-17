# CLAUDE v0.2.26 Windows 플랫폼·Notifier 검증 결과 (GPT 판정용)

- 작성: Windows Claude Code, 2026-11-18 KST. 근거: `GPT_V026_WINDOWS_PLATFORM_AND_NOTIFIER_ONE_SHOT_r0001_20261118_KST.md`. B1→B2→B3를 한 세션에서 순차 수행했다. v0.2.26 설치·독립 리뷰·신규 REQUEST/READY·서명·모델 호출은 전혀 하지 않았다.

## 결론

`V026_INSTALL=NOT_RUN`, `V026_INDEPENDENT_REVIEW=NOT_RUN`(지시대로). Windows 전체 회귀 1031건 중 **28건이 설명됨 + 21건이 기존 원인으로 설명됨**(모두 비회귀), Notifier는 **연결되지 않음**(`NOTIFIER_ADAPTER_CONNECTED=NO`)이 확인됐다.

## B1. v0.2.25 기존 배포 상태 확인 (재설치 없음)

- **운영 버전:** `__version__ = "0.2.25"` — **이미 설치·검증 완료 상태**(제가 같은 세션 앞서 수행). GPT 인계서의 "`CLAUDE_V025_WINDOWS_LIVE_CONDITIONAL_DEPLOY_RESULT_FOR_GPT_20261118.md` 원격 미존재" 관측은 **그 조회 시점이 제 게시 완료 전**이었던 것으로 확인된다 — 지금 그 파일은 `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/`에 실제 존재한다(sha256 `c61dabd0b7a3a4e5f446fe811dffd557ef74800cc3a50ddb9ddc06d2d5838e80`, 10,292 B, commit `419ead1d627c`). 재설치하지 않았다.
- **Task/프로세스:** `SKILL-COLLAB-GitHub-Watcher` Running, 프로세스 2개. 진행 중인 job 0, `provider_lease`는 `github` 단일. 다른 Windows Claude Code 세션의 모델 실행과 충돌 없음(실행 중 claude.exe는 데스크톱 앱/확장/본 세션뿐, 감시기가 디스패치한 리뷰 프로세스 없음).
- `V025_DEPLOY_STATUS=COMPLETED_AND_VERIFIED`, `V025_INSTALL_VERSION=0.2.25`, `ACTIVE_PROVIDER=GITHUB`, `PROTECTED_POLICY_EFFECTIVE=NOT_MET`(보호 위임 자체 한도는 여전히 USD 1.00/request — 2026-11-18 앞선 결과와 동일, 이번 작업에서 변경하지 않음), `V025_RESULT_PATH_OR_BLOCKER=collab/projects/COWORK-AUTO-APPROVAL-20261115-001/CLAUDE_V025_WINDOWS_LIVE_CONDITIONAL_DEPLOY_RESULT_FOR_GPT_20261118.md(존재 확인)`.

## B2. v0.2.26 Windows 격리·전체 회귀 (운영 미접촉)

- **입력:** `collab/projects/.../artifacts/v0_2_26/skill-collab-watcher_v0_2_26_1118.zip`, 308,737 B, SHA-256 `f08adb6099d06daf494362ed7e33ea66aabcbf749cfd2c027a7f70bcba5540fe`(일치), CRC 정상, 113개 항목, 경로 이탈·심볼릭 링크·비밀 패턴 0건.
- **Windows:** Python 3.11.9(운영 venv와 동일), 격리 임시 폴더에서만 추출·실행. 운영 설치본/DB/Task/키는 건드리지 않았다.
- **전체 suite, 제외 없음:** **1010 passed, 21 failed, 12 skipped, 15 subtests passed**. 21건 전부 근본 원인 확인, **신규 회귀 0건**:
  - 6건: `test_a_valid_enabled_delegation_loads`, `test_a_malformed_delegation_is_unusable_not_enabled[over11]`, `test_f3_two_requests_cannot_both_pass_a_one_per_day_ceiling`, `test_B1_auto_reservation_plus_a_separate_manual_dispatch_is_two_calls_and_the_third_is_refused`, `test_B1_cost_union_across_days_counts_both_costs_against_the_month_ceiling`, `test_B2_lowering_the_daily_cost_budget_while_pending_stops_it` — v0.2.25에서도 같은 원인으로 이미 확인한 **의도적 상한 제거** 설계. 이 6건은 Linux 기준실패 34개 목록에도 **그대로 포함**돼 있어 플랫폼 문제가 아니다.
  - 15건: `tests/test_review_request_gate_tool_v026.py`(신규 동봉) — v0.2.25 때 발견한 **테스트 자신의 Windows CRLF 하우징 결함**과 바이트 단위로 동일(`tools/review_request_gate.py`가 v0.2.25-era 사본과 완전히 동일함을 diff로 확인). 게이트 코드 결함 아님, 수정 미적용 상태로 그대로 들어옴.
- **`BASELINE_34_WINDOWS_NODE_RESULTS`(Linux에서 실패해 자체시험 974 PASS 집계에서 제외된 34개를 Windows에서 직접 실행):** **28 passed, 6 failed**. 실패 6건은 위와 완전히 동일한 목록(상한 제거 관련)이다. **나머지 28건은 Windows에서 전부 PASS** — `test_auto_approval_e2e.py`(5), `test_cli_entrypoint_e2e.py`(7), `test_phase5_shadow.py`(7), `test_r1_findings.py`(6, f2/f4/f5/second_scan/shadow_isolation×2), `test_state_store.py::test_single_instance_lock_blocks_second_holder`(1). 이 28건은 실제 `claude` CLI·OS 락 의미가 Linux CI 환경과 다르기 때문에 거기서 실패했던 것으로 보이며, 실제 Windows 운영 환경(지금 쓰는 바로 이 호스트)에서는 PASS한다 — **Windows 전체 PASS 주장의 핵심 근거.**
- **`NEW_61_REGRESSIONS`:** 매니페스트가 Linux에서 통과시켰다고 주장한 61건은 전체 실패 목록(21건)에 전혀 포함되지 않았다 — 즉 Windows에서도 전부 PASS.
- **`PRE_SCHEDULE_PIN_REJECT`(`PIN_REPO_ID_TYPE`):** `skill_collab_watcher/approval.py::validate_source_pin`이 숫자형 `repo_id`를 **서명기 호출·예약(`auto_claim`) 전에** `ApprovalRejected("PIN_REPO_ID_TYPE")`로 거부하도록 바뀌었음을 코드로 직접 확인(주석: "a numeric repo_id can otherwise reserve a request before the final signature check rejects its different type" — 제가 보고한 GUARD-CODE 결함과 정확히 같은 결함을 겨냥한 수정). `auto_approval.py`에서 이 검증이 `pins_ok` 판정보다 먼저 호출되고, 실패 시 `"PIN_MISMATCH: ...; no reservation or signer call"`로 **예약 자체를 만들지 않음**을 호출 순서로 확인. 전담 시험 `tests/test_source_pin_preclaim_v026.py`도 전체 회귀에서 PASS.
- **`UNCERTAIN_PRESERVED`:** v0.2.25와 동일한 종결(`UNCERTAIN`) 설계 유지(코드 비교, 변경 없음) — PASS.
- **`READY_WAIT_SUPPRESSION`:** `orchestrator.py`가 이제 `WAIT_INPUT`을 `log_event`가 아니라 **`log_event_once`**로 기록하도록 바뀌었고, `ready_text is None`일 때만 기록해 READY 게시 성공 뒤에는 더 이상 쌓이지 않는다. 전담 시험 `tests/test_approval_wait_notify_v026.py`가 "같은 원인이 반복되면 0건, 원인이 바뀌면 1회만" 조건을 포함해 전체 회귀에서 PASS.
- **동봉 `tools/source_pin.py`:** GPT 생성기 쪽 수정(제가 지적한 repo_id quoting 문제의 생산자 측 해결) 확인. `canonical_repo_id()`가 정수를 받아도 항상 문자열로 정규화해 쓴다.

## B3. Notifier 연결 확인 (읽기 전용 + 합성 비발송, 실 Telegram 미발송)

- **실제 설치된 Notifier**(`D:\User\whpark\skill-collab-watcher-dist\notifier\notify_reviews.py`, 제가 직접 유지·패치 중인 독립 스크립트)를 소스로 직접 확인: `skill_collab_watcher.notify_events` import 또는 호출이 **0건**. 자체 SQLite 폴링·자체 `NOTIFY_EVENTS`/`build_message`를 쓴다.
- v0.2.26의 `skill_collab_watcher/notify_events.py::run_once`는 `cli.py`의 어떤 서브커맨드에서도 호출되지 않는다(코드 검색 0건) — 즉 watcher 프로세스 자신도 이 모듈을 실행하지 않는다.
- **판정: `NOTIFIER_ADAPTER_CALL_SITE=NONE`, `NOTIFIER_ADAPTER_CONNECTED=NO`.** v0.2.26의 `notify_events` 모듈(위 WAIT 억제·원인 변경 1회 로직 포함)은 패키지 안에만 존재하고, 실제 Telegram을 보내는 설치된 프로세스에는 연결돼 있지 않다. **지금 운영 중인 Notifier와 v0.2.26의 새 알림 로직은 서로 다른, 겹치는 책임을 가진 두 개의 별도 구현이다**(최소 gap). 이 최소 gap은 설치 승인과 별개로 GPT가 판단할 사항으로 남긴다.
- **`NOTIFIER_ADAPTER_READONLY`:** 실제 설치된 Notifier 파일·Task·Telegram 설정은 읽기만 했고 변경하지 않았다(값 미출력).
- **`NOTIFIER_FAKE_TEST`:** v0.2.26 자체의 fake-sender 시험(`tests/test_approval_wait_notify_v026.py`)이 격리 회귀에서 PASS — 모듈 자체의 동작(중복 억제, 원인 변경 1회)은 격리 조건에서 검증됐다. 실제 발송 테스트는 하지 않았다.
- **`TELEGRAM_LIVE_APPLIED=NOT_RUN`.** `collab/dashboard/review_completion.py`(GitHub Actions 요약)는 확인 범위 밖으로 두고 별도 Bridge/스키마를 제안하지 않았다.
- **`WINDOWS_HOST_ID_REDACTED`**: 단일 Windows 계정 호스트, 식별값 미게시.

## 상태값

```
WINDOWS_PYTHON=3.11.9
V025_DEPLOY_STATUS=COMPLETED_AND_VERIFIED
V025_INSTALL_VERSION=0.2.25
ACTIVE_PROVIDER=GITHUB
PROTECTED_POLICY_EFFECTIVE=NOT_MET (위임 자체 한도 USD1/request, 2026-11-18 앞선 결과와 동일, 미변경)
V025_RESULT_PATH_OR_BLOCKER=존재 확인 (sha256 c61dabd0b7a3a4e5f446fe811dffd557ef74800cc3a50ddb9ddc06d2d5838e80)
V026_SOURCE_SHA256=f08adb6099d06daf494362ed7e33ea66aabcbf749cfd2c027a7f70bcba5540fe (일치)
V026_SOURCE_BYTES=308737
V026_CRC_MEMBERS=PASS/113 (경로이탈·심볼릭·비밀 0)
V026_FULL_SUITE_PASS_FAIL_SKIP=1010/21/12 (+15 subtests passed) — 21건 전부 비회귀로 설명됨
BASELINE_34_WINDOWS_NODE_RESULTS=28 PASS / 6 FAIL(동일한 설계 변경 원인, 비회귀)
NEW_61_REGRESSIONS=PASS(전체 61건, 실패 목록에 없음)
PRE_SCHEDULE_PIN_REJECT=PASS (PIN_REPO_ID_TYPE, 예약 전 차단 코드·호출순서·전담시험 확인)
UNCERTAIN_PRESERVED=PASS
READY_WAIT_SUPPRESSION=PASS (log_event_once, 전담시험 PASS)
NOTIFIER_ADAPTER_CALL_SITE=NONE
NOTIFIER_ADAPTER_CONNECTED=NO
NOTIFIER_FAKE_TEST=PASS (격리, 비발송)
TELEGRAM_LIVE_APPLIED=NOT_RUN
V026_INSTALL=NOT_RUN
V026_INDEPENDENT_REVIEW=NOT_RUN
MODEL_CALLS_BY_THIS_TASK=0
NEW_REQUEST_READY=0
OPEN_BLOCKERS=["v0.2.26 독립 리뷰 필요 여부 GPT 판정 대기", "notify_events 모듈을 실제 설치 Notifier에 연결할지, 현재의 별도 유지 구현을 그대로 둘지 GPT 판정 필요", "collab/ops/tests/test_review_request_gate_tool_v026.py의 Windows CRLF 테스트 하우징 결함이 v0.2.26에도 그대로 들어와 있음(게이트 자체 결함 아님, 이전 보고와 동일)"]
```

## 다음 한 동작

GPT가 ① v0.2.26을 독립 리뷰 대상으로 올릴지(이번 결과는 자체·호스트 시험일 뿐 독립 리뷰가 아니다), ② `notify_events` 모듈과 실제 설치된 Notifier의 연결 여부, ③ 반복되는 게이트 테스트 CRLF 결함 수정을 어느 후보에서 채택할지 판정한다. v0.2.26 운영 설치는 그 전까지 `NOT_RUN`으로 유지한다.
