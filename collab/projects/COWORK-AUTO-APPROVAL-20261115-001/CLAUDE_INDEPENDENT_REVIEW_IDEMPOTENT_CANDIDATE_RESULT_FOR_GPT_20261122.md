# 독립 리뷰 단일 실행·비용 상한 제거 — v0.2.31 격리 후보 결과 (Windows Claude Code)

- 작성: Windows Claude Code, 2026-11-22 KST. Work: `COWORK-AUTO-APPROVAL-20261115-001`. 지시: `INDEPENDENT_REVIEW_IDEMPOTENCY_COST_REMOVAL_HANDOFF_r0001_20261122_KST.md`.
- 기준 후보: v0.2.30(`v0_2_30_cost_gate_removal`)에서 연속 개발. 구 ZIP은 덮어쓰지 않음.
- **결론: v0.2.31 격리 후보 완성. 전체 시험 960 PASS / 0 FAIL / 12 SKIP, 무모델 호출. LIVE 적용 NO.** 단일 실행 내부 비용 상한이 사라지므로 아래 §6의 사용자 결정이 필요하다.

## 1. SOURCE_DIFF (v0.2.30 대비)

| 파일 | 변경 |
|---|---|
| `skill_collab_watcher/review_runner.py` | `build_argv`·`RealReviewRunner`·`run()`·`ReviewRunner` 프로토콜에서 `max_budget_usd` 제거. `--max-budget-usd` 플래그 생성 삭제. 실패 사유 문구의 예산 항목 삭제 |
| `skill_collab_watcher/orchestrator.py` | 디스패치 시 금액을 CLI에 넘기지 않음. 회계 참고값은 `accounting_reference_usd`로만 기록 |
| `skill_collab_watcher/cli.py` | 실행기 생성 시 예산 인자 제거 |
| `skill_collab_watcher/fake_runner.py` | 예산 인자·`last_budget` 제거 |
| `skill_collab_watcher/state_store.py` | 일/월 회계 집계가 `accounting_reference_usd`를 우선 읽고 구 `max_budget_usd`는 호환 폴백. 클레임 금액은 0 허용(음수만 `INVALID_COST`) |
| `skill_collab_watcher/auto_policy.py` | `UNSUPPORTED_DELEGATION_LIMIT` 제거(v0.2.30에서 `PER_REQUEST_COST` 제거 후 잔여) |
| `skill_collab_watcher/__init__.py` | 0.2.31 |
| `docs/CUTOVER_RUNBOOK.md` | 제목 버전만 0.2.31 |
| `tests/` | 금액 인자 계약에 묶인 기존 시험 6개 파일 갱신, 신규 `test_v031_independent_review.py` 8개 추가 |

## 2. REMOVED_COST_GATES

- v0.2.30에서 이미 제거: `PER_REQUEST_COST`(auto_policy), 수동 승인 `--max-usd` 일치 검사.
- v0.2.31에서 추가 제거: CLI `--max-budget-usd` 전달·생성(신규 독립 리뷰 경로 전체), `UNSUPPORTED_DELEGATION_LIMIT`, 금액 0 클레임 거부.
- 금액이 없는 정책도 디스패치 가능(시험으로 확인). 금액은 회계 기록용 `accounting_reference_usd`로만 남음.

## 3. CLI_BUDGET_ARG

- `build_argv` 출력에 `--max-budget-usd`가 나타나지 않음(시험 `test_runner_argv_never_carries_a_budget_cap`, `test_argv_excludes_bare_and_restricts_tools`).
- 런타임 경로 전수 검색 결과 `--max-budget-usd`·`PER_REQUEST_COST`·`UNSUPPORTED_DELEGATION_LIMIT` 없음. 잔여는 §5 참고.
- 실행 시간 상한 `timeout_sec`와 프로세스 종료·취소 보호는 그대로 유지.

## 4. IDEMPOTENCY / UNCERTAIN_BLOCK (기존 메커니즘 + 시험으로 입증)

| 시나리오 | 결과 | 근거 |
|---|---|---|
| 같은 요청을 여러 번 스캔 | 디스패치 1회 | 시험 `test_same_request_is_dispatched_once_across_rescans` PASS |
| 같은 DB로 재시작 | 재디스패치 0 | 시험 `test_restart_on_the_same_database_does_not_redispatch` PASS |
| 새 DB를 가진 두 번째 watcher | 재디스패치 0 | 시험 `test_second_watcher_with_a_fresh_database_does_not_redispatch` PASS. 원격 `dispatch/<id>/DISPATCH_<rev>.md`(create-only)와 완료 결과 확인이 막음 |
| 같은 ID·리비전에 다른 ZIP | CONFLICT, 모델 0 | 시험 `test_same_revision_with_another_package_is_conflict_and_never_reviewed` PASS. 다운로드 전 `job_for_other_package` 단계에서 차단 |
| 모델 시작 후 시간 초과 | REVIEW_UNCERTAIN, 자동 재호출 0 | 시험 `test_runner_timeout_after_model_start_is_uncertain_and_not_retried` PASS |
| 결과 업로드 실패 | 모델 재호출 없이 게시만 재시도, 완료 | 시험 `test_result_upload_failure_publishes_later_without_a_second_model_call` PASS |
| 기타 실행 실패(시간 초과 아님) | 터미널 FAILED, 자동 재시도 없음 | 코드 검토(`orchestrator.py` 실패 분기). 별도 시험 없음 |
| 시작 시 CLAIMED/RUNNING 잔존 | REVIEW_UNCERTAIN 봉인 | 코드 검토(`state_store` 시작 봉인). 별도 시험 없음 |
| 원자적 1회 클레임 | 기존 유지 | `auto_claim` 한 행/(요청,리비전), 기존 시험 PASS |

## 5. 남은 한계·잔여 항목

- **단일 실행 내부 비용 무상한(핵심 위험):** CLI에 금액 상한이 없으므로 한 번의 리뷰가 제공자 측 상한 없이 턴을 더 쓸 수 있다. 남은 경계는 `timeout_sec`와 `max_calls=1`(외부 CLI 디스패치 횟수)뿐이다. 이를 숨기지 않는다.
- 설정 파일의 `max_budget_usd` 키는 파싱·검증만 남아 있다(잘못된 값이면 설정 로드 실패). 실행 차단이나 CLI 인자로는 쓰이지 않는다.
- `notify_events.py`의 `PER_REQUEST_COST` 문구 매핑은 죽은 문자열(무해), 제거하지 않음.
- Windows 복사본 `tools/review_request_gate.py`의 `POLICY_COST_MISMATCH`는 감시기 실행 경로가 아니며 미변경.
- 두 watcher가 **동시에** 같은 요청을 처리하는 경합은 시험하지 않았다. 순차·새 DB 시나리오만 입증했다.
- `__pycache__`·`.pytest_cache`는 패키지에서 제외.

## 6. SCOPE 개선 — 설계만, 구현·LIVE 없음 (DESIGN_ONLY)

- 현재: `skills`는 리터럴 목록이며 `*`는 문자 그대로 비교되어 어떤 스킬도 통과시키지 않는다(시험 `test_scope_refuses_unlisted_skill_and_treats_star_as_a_literal` PASS).
- 제안(미구현): 사용자가 **서명한 독립 리뷰 의도 매니페스트**(신뢰 루트의 기존 키로 서명, 만료일, 허용 프로젝트 패밀리·스킬 목록, 와일드카드 금지)를 두고, 감시기는 서명·만료·범위를 검증한 뒤에만 자동 경로를 연다. 검증 불가 시 FAIL-CLOSED.
- 기존 `cowork-context-design` 대기 요청은 소급 디스패치하지 않는다. 위임 목록 변경은 별도 명시 승인이 필요하다.

## 7. TEST / NEW_MODEL_CALLS

- 전체 후보 시험: **960 PASS / 0 FAIL / 12 SKIP** (v0.2.30 952 + 신규 8).
- 신규 8개: 반복 스캔 1회, 재시작 1회, 새 DB watcher 0회, 다른 ZIP CONFLICT, 시간 초과 UNCERTAIN, 업로드 실패 후 게시만, 금액 없음 허용, SCOPE 와일드카드 거부.
- 모든 시험은 FakeReviewRunner·인메모리 전송 사용. **실제 `claude` 호출 0, 유료 모델 호출 0.**
- 실제 Windows `claude` CLI 실행: NOT_RUN(범위 밖, 유료 호출 금지).
- 인증·서명 위조·만료 시험은 기존 스위트에 포함되어 PASS(별도 재작성 없음).

## 8. 패키지 / SHA-256

- 작업 폴더: `D:\User\whpark\skill-collab-watcher-dist\candidates\v0_2_31_independent_idempotent\`
- ZIP: `D:\User\whpark\skill-collab-watcher-dist\candidates\v0_2_31_independent_idempotent_candidate.zip`
- ZIP SHA-256 `1df85457ec01eaaa1a63022777f40b658732355e9d4f016a92b07076da950ea3`, **291,484 B**, 103 항목, CRC 정상, 중복 항목 없음
- 트리 SHA-256(파일별 해시 연결) `ec2f3c7c50d8dd9c6225925f490ebcb256cd873735f37bc58bfd64276fef2dd7`
- 구 v0.2.30 ZIP `541cd3f1…` 변경 없음.
- 코드 ZIP은 공개 저장소에 올리지 않았다. 이 결과 문서와 CURRENT만 게시한다.

## 9. LIVE_APPLY / 롤백

- LIVE_APPLY: **NOT_RUN**. v0.2.29 설치본·설정(SHA `2ead4007…`)·위임(SHA `6d826672…`)·DB·Task·Notifier 모두 불변. 기존 요청 재큐잉 0, 위임 확대 0.
- 롤백: 후보는 설치되지 않았다. 적용 시에는 현행 설치본과 DB를 새 백업 번들로 먼저 보존하고, 실패 시 백업으로 복귀한다.

## 10. BLOCKER

- LIVE 적용은 별도 운영 승인 대기.
- 단일 실행 비용 상한 제거에 대한 사용자 확인 필요(§5).
- SCOPE 개선안은 설계 승인 후에만 구현 가능.

## 11. NEXT_ONE_ACTION

1. 사용자가 §5의 비용 무상한 위험과 `timeout_sec` 경계를 수용할지 결정.
2. 수용 시 LIVE 컷오버 승인 여부를 별도로 판단(백업 선행, 격리 재검증, 실제 상태 검증, 실패 시 롤백).
3. SCOPE 서명 의도 매니페스트 설계 승인 여부 결정. 기존 대기 요청은 손대지 않는다.
