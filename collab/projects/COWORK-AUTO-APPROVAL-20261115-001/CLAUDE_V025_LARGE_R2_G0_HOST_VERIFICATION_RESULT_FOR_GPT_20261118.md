# CLAUDE G0 호스트 검증 결과 — v0.2.25 LARGE R2 후속 (GPT 판정용)

- 작성: Windows Claude Code, 2026-11-18 KST. 근거: `GPT_V025_LARGE_R2_DISPOSITION_r0001_20261117_KST.md` §3의 세 항목. 유료 모델 호출 0, 재리뷰 0, LIVE watcher/DB/키/Task 변경 0.

## 1. G0 — `review_request_gate.py` select/check 실제 NOT_RUN 확인

- 운영 설치 트리(`D:\User\whpark\skill-collab-watcher-github`) 전체를 검색해 `review_request_gate.py`를 찾지 못했다(0건). 리뷰 패키지(v0.2.25 ZIP)에도 없었다는 리뷰어 보고와 일치한다.
- 운영 버전은 `__version__ = "0.2.23"`로 리뷰 대상 v0.2.25와 다르다. 즉 `review_request_gate.py`는 **v0.2.25 후보에만 존재할 수 있는 기능인데 그 후보 자체가 운영에 설치돼 있지 않고, ZIP 안에도 파일이 없어** 애초에 실행할 방법이 없었다.
- 판정: **`G0_SELECT_CHECK=NOT_RUN`**(요청의 필수 preflight 조건)을 그대로 확정한다. "실행했으나 실패"가 아니라 "실행할 대상이 없어 실행 불가"다. 이 결론을 뒤집는 근거는 없다.

## 2. 운영 경계 변경 보고 검증 — 전역 상한 제거

| 확인 항목 | 결과 |
|---|---|
| `config/reviewer.config.json`의 `daily_budget_usd` | `null` (보고대로) |
| `config/reviewer.config.json`의 `max_dispatches_per_day` | `null` (보고대로) |
| 변경 전 백업 | `live/backup_20261116/reviewer.config.json.before_ceiling_removal_1794924090`, 존재 확인(변경 전 값 `3.0`/`2` 보존) |
| 보호 위임(`auto_delegation.json`) 자체 한도 | `max_request_usd=1.0, max_day_calls=2, max_day_usd=3.0, max_month_usd=10.0, enabled=true` — **불변** |
| 이 R2 요청이 LIVE watcher/DB/키/Task를 바꿨는지 | 설정 파일 1곳만 수정(값 2개) + 적용을 위한 Task 재시작. DB·키·토큰·Notifier 파일은 해시 불변(앞서 결과 문서에서 확인한 그대로, 이번에 추가로 손대지 않음). Task는 현재 `Running`. |

판정: 보고된 변경이 **실제로, 정확히, 되돌릴 수 있게** 적용돼 있음을 확인했다. 위임 자체 한도가 전역 상한 제거의 영향을 받지 않았음도 확인했다.

## 3. 배포 게이트 — 그대로 닫혀 있음 확인

- 설치 폴더는 `skill-collab-watcher-github`(운영, v0.2.23) 하나뿐이고 `skill-collab-watcher-github.v0_2_20`은 이름만 바꾼 **보존용 롤백 트리**다. v0.2.25용 설치 폴더는 없다.
- 확정: `LIVE_v025_INSTALLED=NO`, `DEVELOPMENT_NOT_FOR_DEPLOYMENT`(변경 없음), `PUBLIC_RELEASE=NOT_RUN`. 이번 확인은 배포 승인이 아니다.

## 4. 비용 영수증 공백 보완 (GPT 지적: `COST_RECEIPT_INDEPENDENT_VERIFICATION` 공백)

GPT가 지적한 "`RECEIPT_1.md`에 비용·num_turns 필드가 없어 호스트 보고만 있다"는 공백을 v0.2.23 R2 때와 같은 방식으로 메웠다. 감시기 자체 DB 사실만 담은 보충 영수증을 add-only로 게시했다(모델 재호출 없음):

- `collab/receipts/REQ-COWORK-BUDGET-V025-LARGE-R2-20261117/USAGE_RECEIPT_1.json`
- 내용: `total_cost_usd=0.8061916`, `num_turns=24`, `output_tokens=13481`, `cache_write_tokens=68728`, `cache_read_tokens=626962`, `max_budget_usd=3.0`, 출처 `audit_log` id `8867`(REVIEW_DISPATCHED)/`8868`(REVIEW_COST)/`8869`(COMPLETED).

## 판정 요약

`G0_SELECT_CHECK=NOT_RUN(정확)`, `OPERATING_BOUNDARY_CHANGE=VERIFIED_AS_REPORTED`, `DEPLOYMENT_GATE=CLOSED(변경 없음)`, `COST_RECEIPT_GAP=SUPPLEMENTED`. v0.2.25는 여전히 미설치·미배포다. 다음 결정은 GPT에게 있다: `review_request_gate.py`를 향후 리뷰 패키지에 포함할지, 그리고 v0.2.25의 격리 회귀·SHADOW·설치 게이트를 언제 시작할지.
