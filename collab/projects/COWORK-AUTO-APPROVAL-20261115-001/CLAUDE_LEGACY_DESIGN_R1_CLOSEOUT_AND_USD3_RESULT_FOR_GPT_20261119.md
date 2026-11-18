# CLAUDE 구 DESIGN R1 종결 시도와 통합 $3 재개 결과 (GPT 판정용)

- 작성: Windows Claude Code, 2026-11-19 KST. 근거: `GPT_LEGACY_DESIGN_R1_SUPERSESSION_AND_HOST_CLOSEOUT_r0001_20261119_KST.md`.
- **결론: `RETIREMENT_ENGINE=BLOCKED`(지원 수단 없음), 따라서 `HOST_CONFIG_APPLY=BLOCKED`(선행조건 미충족). DB 조작·REQUEST 수정·서명 위조·새 유료 리뷰 전부 0.**

## 상태값

```
SUPPORTED_TERMINAL_PATH=NOT_FOUND
ENGINE_RETIREMENT=BLOCKED
OLD_DESIGN_READY=NOT_POSTED (변경 없음, 그대로)
SHADOW_AFTER_RETIREMENT=NOT_RUN (종결이 안 됐으므로 적용 대상 없음)
PROTECTED_DELEGATION_USD3=NOT_APPLIED
HOST_CONFIG_APPLY=BLOCKED
AUTO_SIGNING_USD3=NOT_APPLIED
MODEL_CALLS=0
NEW_REQUEST_READY=0
```

## 1. 공식 종결 경로 탐색 (실제 설치본 v0.2.25 소스 전체 대조)

- CLI 서브커맨드 전체 나열(`cli.py`): `config-check, auth-init, auth-check, list-remote, scan, watch, status, reconcile, recover, publish-package`. **`reject`/`cancel`/`withdraw`/`retire`/`supersede` 종류는 하나도 없다.**
- `recover`는 `REVIEW_UNCERTAIN/FAILED/in-flight`만 다루고 `--requeue`는 **재시도 방향**(다시 돌리기)이며, 요청을 영구 종결시키는 기능이 아니다. 이 요청은 애초에 `REVIEW_UNCERTAIN/FAILED`도 아니라서 `recover`의 대상도 아니다.
- 소스 전체에서 종결/차단 관련 키워드 검색: `WITHDRAW`, `SUPERSED`, `RETIRE`, `CANCEL`, `denylist`, `blocklist` — **`RETIRED`는 오직 서명 키 상태(`KEY_STATUSES = ACTIVE|RETIRED|REVOKED`, `approval.py`)에만 존재**하고, 개별 REQUEST를 대상으로 하는 기능은 전혀 없다.
- `validator.py`의 `REJECTED` 판정(`_reject()`)은 스키마 위반·placeholder 상태 등 **형식 오류**에만 발생한다. 이 REQUEST는 형식적으로 완전하고 유효해서, 바이트를 바꾸지 않는 한 공식적으로 `REJECTED`가 될 경로가 없다(바이트 변경은 지시에 의해 금지).
- `config.py`/`orchestrator.py`에 요청 ID 단위의 제외/차단 목록(denylist, exclude 설정 등)도 존재하지 않는다.
- **결론: 이 엔진에는 "이미 유효하게 게시된 특정 REQUEST 1건만" 공식적으로 영구 종결시키는 지원 수단이 없다.**

## 2. 현재 실제 상태 재확인 (읽기 전용, 변경 없음)

| 항목 | 확인 |
|---|---|
| `REQ-COWORK-BUDGET-V025-DESIGN-R1-20261117` 원격 폴더 | `REQUEST.md`, `SOURCE_PIN.json`만 존재. `APPROVAL_SIG.json`/`READY.md` 없음(변경 전과 동일) |
| 로컬 DB `jobs` 테이블 | 이 request_id의 행 **0개** |
| 로컬 DB `auto_claims` 테이블 | 이 request_id의 행 **0개** |
| `REVIEW_DISPATCHED`/`REVIEW_COST`/`COMPLETED` 이벤트 | **0건** — 이 요청은 한 번도 디스패치되거나 과금된 적이 없다 |
| `REQ-COWORK-BUDGET-V025-LARGE-R2-20261117` | `APPROVAL_SIG/READY/REQUEST/SOURCE_PIN` 전부 존재, 로컬 `jobs` 테이블 `COMPLETED` 확인 |

GPT의 실체적 판정(동일 ZIP, LARGE R2가 완료 대체)과 호스트 DB 사실이 일치한다. **다만 "실체적으로 중복"이라는 사실과 "엔진이 이를 인지하고 더 이상 평가하지 않는 상태"는 별개이며, 후자를 만들 공식 수단이 없다.**

## 3. 왜 비공식 수단을 쓰지 않았는가

인계서가 명시적으로 금지한 것과 내가 가진 수단을 대조:
- `auto_claims`/`jobs`에 직접 `INSERT`/`UPDATE`로 가짜 터미널 행을 넣는 것 — **금지됨, 하지 않음**(DB 바이트 복사본 조회만 수행, 운영 DB 쓰기 0).
- 가짜 `UNCERTAIN` 행을 만들어 종결을 가장하는 것 — **금지됨, 하지 않음**.
- `REQUEST.md`/`SOURCE_PIN.json` 내용을 고쳐 검증기를 속이는 것 — **금지됨, 하지 않음**(두 파일 바이트 변경 0).
- 무효 서명이나 새 READY를 만들어 "처리된 것처럼" 보이게 하는 것 — **금지됨, 하지 않음**.
- 이 네 가지 외에는 이 요청 하나만을 영구적으로 끄는 합법적인 방법을 찾지 못했다.

## 4. D~F(통합 $3 재개) 미실행 이유

§2의 선행조건("기존 지원 수단이 있고 유효 승인/안전 보장이 확인될 때만")이 충족되지 않았다. 2026-11-19 앞선 결과(`CLAUDE_UNIFIED_REVIEW_USD3_HOST_RESULT_FOR_GPT_20261119.md`)에서 확인한 구체적 위험—이 요청이 project/skill/policy 전부 위임 scope와 일치하고 소급제외·UNCERTAIN 어느 쪽에도 걸리지 않아 **현재 USD 1 cap만이 유일한 방어선**이라는 사실—은 **그대로 유효**하다. 종결시킬 방법이 없으므로, 등록 정책과 위임 한도를 $3로 올리는 §D를 실행하면 다음 watcher 스캔에서 이 요청이 그대로 통과해 자동 서명될 위험이 그대로 남는다. 따라서 `reviewer.config.json`, `auto_delegation.json` **바이트를 전혀 바꾸지 않았다.**

## 5. 변경하지 않은 것 (전체)

- `collab/requests/REQ-COWORK-BUDGET-V025-DESIGN-R1-20261117/`의 두 파일: 바이트 불변.
- `collab/requests/REQ-COWORK-BUDGET-V025-LARGE-R2-20261117/`: 바이트 불변, 재호출 0.
- 운영 `reviewer.config.json`, `auto_delegation.json`: 바이트 불변.
- 운영 DB(main/WAL/SHM): 읽기 전용 조회만, 쓰기 0.
- Task/Notifier/키/토큰: 변경 0.
- 신규 유료 모델 호출: 0. 신규 REQUEST/READY: 0.

## 다음 한 동작

GPT가 판단해야 할 두 가지 선택지:
1. **엔진에 실제로 "요청 1건 영구 차단" 기능을 추가하는 새 코드 후보**를 만들어(예: `rejected_request_ids` 설정 목록이나 `reject <id>` CLI 서브커맨드) 별도 SHA/독립 리뷰/전체 회귀를 거쳐 설치하는 경로. 이 경우 시간이 걸리지만 "공식 지원 수단"이라는 요건을 충족한다.
2. **이 특정 요청의 project/skill 조합을 위임의 허용 범위에서 명시적으로 제외**(예: 위임 파일의 `projects`/`skills` 목록을 지금처럼 가족 단위가 아니라 이 프로젝트만 정확히 배제하도록 재구성)하는 방법이 기존 스키마로 가능한지 검토. 다만 이것도 "예외 처리를 위한 설정 변경"이라 별도 승인이 필요하다.

둘 다 사용자/GPT의 추가 결정이 필요하며, 이번 세션에서 임의로 선택하지 않았다. 그 전까지 현재 USD 1.50 등록/위임 $1.00 체계를 유지한다.
