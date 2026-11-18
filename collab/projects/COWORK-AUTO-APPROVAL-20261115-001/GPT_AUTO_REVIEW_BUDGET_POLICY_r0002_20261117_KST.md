# GPT 결정 · 실행 판정 — 리뷰별 비용 $1.50/$3.00, 일·월 합계 상한 폐기 r0002

> **최신 정책 (2026-11-19 KST):** [신규 단일 USD 3 리뷰 정책·Windows 조건부 적용](GPT_UNIFIED_REVIEW_USD3_CONDITIONAL_APPLY_r0001_20261119_KST.md)이 본 문서의 과거 $1.50/$3 분할 및 과거 일/월 한도 설명보다 우선. 기존 설계·이력 및 실제 보호 로컬 승인 범위는 별개로 보존. **Windows LIVE 적용=NOT_RUN**.

- 날짜: 2026-11-17 KST
- 저장소: PRIVATE `wonhwipark/CoWork-Skill-Collab`, 정본 branch `main`
- 기존 Work: `collab/projects/COWORK-AUTO-APPROVAL-20261115-001`
- **최신 사용자 지시:** "상한 삭제, 디자인리뷰 3달러, 기본스킬 1.5 달러 추후수정가능하도록 변경해줘"
- 이 문서는 [이전 r0001 건당 $1/일 $3/월 $10 정책](GPT_COST_ONLY_AUTO_APPROVAL_POLICY_r0001_20261117_KST.md)을 **신규 요청의 목표 정책 측면에서 대체**. 이전 승인·실행 기록은 당시 사실로 보존.
- **범위:** 코드 후보·자체시험·PRIVATE 저장/원격 확인. Windows LIVE 보호 위임/운영 설정·DB/Task·API 유료 모델·키·PUBLIC 게시 변경은 포함하지 않음.

## 1. 최종 요구 정책

| 구분 | 신규 규칙 |
|---|---|
| 일반 스킬 코드/문서 독립 리뷰 | `POLICY-STATIC-V1` / 요청당 **USD 1.50** |
| 디자인/설계 독립 리뷰 | 신규 `POLICY-STATIC-V1-DESIGN` / 요청당 **USD 3.00** |
| 일일 리뷰 호출 횟수 | **상한 없음** |
| 월간 리뷰 호출 횟수 | **상한 없음** |
| 일일 누적 비용 | **상한 없음** |
| 월간 누적 비용 | **상한 없음** |
| 동일 `request_id + revision` 자동 승인/디스패치 | **정확히 한 번만 허용**; `UNCERTAIN` 무조건 자동 재시도 금지 |
| 프로젝트·스킬 허용 목록, 임시 위임 만료, Ed25519, SOURCE_PIN, 원본 SHA/CRC, READY 마지막 | 기존 fail-closed 보호 **유지** |

**두 비용은 모델 호출 1건당 상한**이며 하루/월 집계 예산이 아니다. Claude CLI `--max-budget-usd`는 실행 제한 기준이나 종료 시 실제 비용이 조금 초과할 수 있어 완전한 결제 하드캡으로 표기하지 않는다.

## 2. 추후 수정 가능하도록 기존 설정 재사용

새 비용 엔진·새 원장·신규 approval schema 없이, 기존 Windows 로컬 `reviewer.config.json`의 **`review_policy.known_run_policy_refs` 객체**를 활용한다.

설정 **예시** (운영 설정 파일이 아닌 인계용 조각):

```json
{
  "max_budget_usd": 1.5,
  "known_run_policy_refs": {
    "POLICY-STATIC-V1": {"max_budget_usd": 1.5},
    "POLICY-STATIC-V1-DESIGN": {"max_budget_usd": 3.0}
  },
  "daily_budget_usd": null,
  "max_dispatches_per_day": null
}
```

위 키들은 모두 `review_policy` 하위에 배치. **실제 운영 파일의 나머지 키/권한/인증은 보존**. 향후 비용은 해당 protected/승인된 로컬 설정의 숫자를 변경하며, 입력을 문자열·NaN·무한대·0으로 지정하면 fail-closed 되도록 패치. 새로운 REQUEST는 금액 대신 등록된 `run_policy_ref`만 지정. 디자인을 추정 분류하여 기존 요청을 고가 등급으로 **자동 승격하지 않음**.

별도의 **보호된 로컬 사전 위임 JSON**에 지정된 요청당 최대 비용이 그보다 작으면 무조건 거부하므로, 디자인 자동 승인에는 `max_request_usd: 3.0`이 유효한 현행 위임·승인 범위에 실제 설치돼야 함. 이를 기존 `max_request_usd: 1.0`에서 문서 게시만으로 자동 변경하지 않는다. 위임 `policy`의 `POLICY-STATIC-V1`은 STATIC_ONLY 검토 모드를 뜻하며, 신규 `run_policy_ref`와 혼동하지 않는다.

유효한 `run_policy_ref`/요청 허용 프로젝트·스킬 범위는 모두 기존 현행 `validate`·`auto_policy.assess`·서명/핀 검증에 적용. 기존 `POLICY-STATIC-V1-LARGE`/XLARGE를 자동 승인으로 우회·확대하지 않으며, DESIGN은 로컬 정책에 명시된 경우에만 허용.

## 3. 실제 수정 내용

- `auto_policy.py`: 기본 V1와 디자인 V1-DESIGN 정적 리뷰만 허용, `max_request_cents`의 위임별 양수 유한 검증과 요청별 보호 유지. 일/월 호출·비용을 한도 판단에서 삭제. `Evidence.day_cents/month_cents`는 관측용으로 보존.
- `auto_approval.py`: 이전 `max_day_usd/max_month_usd` 위임 키는 호환·이력용으로 수용하되 신규 승인 제한으로 사용하지 않음. 서명 전 건당 `max_request_usd` 검증 유지. 상태 출력은 per-review cap만 표기.
- `state_store.py::auto_claim`: 기존 SQLite `BEGIN IMMEDIATE`·고유키, 실패·불확실 기록 보존. `DAY_COST_LIMIT/MONTH_COST_LIMIT` 거부만 삭제. 오래된 예약을 DB에서 지우거나 임의 비용 정산하지 않음.
- `config.py`·`orchestrator.py`·`state_store.claim`: 레거시 일반 Watcher의 `daily_budget_usd`/`max_dispatches_per_day`도 **실제 입장·원자 디스패치에서 사용하지 않음**. 런타임 예산은 여전히 요청당 `--max-budget-usd`.
- 패키지 내부 `docs/BUDGET_POLICY_CONFIGURATION.md`: 본문과 동일한 운영 인계 설정 조각 포함. 구버전 호출자 인자·SQLite 컬럼은 삭제/DB 이행하지 않음.

## 4. 구현·시험 증거

- **부모 고정본** `dev/auto-quota-cost-only-20261117`의 `skill-collab-watcher_v0_2_24_1117.zip` SHA-256 `3c78699b734d88202a34ef5fd430f5f278ab1692a437b6affb6b6c64d24ca360`.
- 새 빌더·회귀시험: `dev/auto-review-budget-policy-20261117`의 `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/dev/build_v025_review_budgets.py`, `patch_v025_budget_tests.py`.
- **개발 후보 v0.2.25:** `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/candidates/skill-collab-watcher_v0_2_25_1117.zip`, **283930 B**, SHA-256 **`26d63c8a03290499b13b2ceb8ff0b70c06eb1b1bcc1a25fe3d8f65fcc213d228`**.
- **[개발 CI #44011746881](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/44011746881): SUCCESS**, 표적 29 PASS/2 SKIP, Linux 지원 스위트 582 PASS/30 SKIP/1 DESELECTED. 실제 조작 경로에서 새 등급 설정·기본/디자인 허용·위임 미달 차단·중복 금지·일/월 비용 사용치가 높은 경우 허용을 검증. Fake runner, 모델 호출 0.
- **[원격 바이트 재조회 CI #44011874422](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/44011874422): SUCCESS**. GitHub PRIVATE branch의 실제 ZIP·JSON을 push 후 fetch/git show로 다시 읽어 ZIP CRC, 크기, SHA-256 직접 일치: `REMOTE_BYTE_READBACK_PASS 283930 26d63c8a...`.
- 이 시험은 Linux runner 개발자 자체시험이며 Windows 실호스트 검증이나 Claude Code 독립 리뷰를 대신하지 않는다.

## 5. 판정과 적용 경계

| 구분 | 상태 |
|---|---|
| 요구정책·개발 후보 코드 | **COMPLETE** |
| Linux 자체 회귀시험·PRIVATE 후보 원격 SHA | **PASS** |
| Windows 전용 잠금/SHADOW/운영 Python 시험 | **NOT_RUN** |
| Windows Claude Code 독립 코드 리뷰 | **NOT_RUN / PENDING_HANDOFF** |
| 운영 보호 위임·`reviewer.config.json` 현행 값 변경 | **NOT_RUN** |
| Windows LIVE watcher 신규 ZIP 설치·전환 | **NOT_RUN** |
| PUBLIC ZIP 게시·유료 모델 호출·새 REQUEST/READY | **NOT_RUN** |

**다음 한 행동:** Windows Claude Code가 PRIVATE 동일 Work의 독립 리뷰 인계로 고정 v0.2.25 ZIP SHA·변경 diff·Windows 격리 시험을 수행하고 결과를 PRIVATE main에 보고. 코드·시험 PASS와 사전 승인 범위/보호 백업이 확인되기 전 LIVE 변경은 실행하지 않음.

기존 Guard·MSC `AUTO_SIGNING_UNCERTAIN`과 legacy REQUEST/READY/리뷰/영수증/DB는 보존하고 과거 비용을 자동 환급·재실행하지 않는다.
