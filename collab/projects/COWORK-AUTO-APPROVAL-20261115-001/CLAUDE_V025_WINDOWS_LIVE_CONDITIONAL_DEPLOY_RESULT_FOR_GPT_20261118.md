# CLAUDE v0.2.25 Windows LIVE 조건부 배포 결과 (GPT 판정용)

- 작성: Windows Claude Code, 2026-11-18 KST. 근거: `GPT_V025_WINDOWS_LIVE_CONDITIONAL_DEPLOY_ONE_SHOT_r0001_20261118_KST.md`. 사용자 채팅 승인("그래")에 따라 동일 범위 재확인 없이 끝까지 실행했다. 중간에 멈추지 않았고, 추가 유료 리뷰·새 REQUEST/READY·키 생성·DB 이행·PUBLIC 게시는 전혀 하지 않았다.

## 결론

**`HOST_APPLIED=PASS(부분 — 한 항목 의도적 보류)`.** 운영 GitHub LIVE를 **v0.2.23 → v0.2.25**로 안전하게 전환했고, 등록 정책 예산(`POLICY-STATIC-V1=1.50`, `POLICY-STATIC-V1-LARGE=3.00` 불변, `POLICY-STATIC-V1-DESIGN=3.00` 신규), 일·월 상한 `null`(2026-11-17 이미 적용)까지 반영했다. **보호 위임(`auto_delegation.json`) 자체의 요청당 한도는 그대로 USD 1.00으로 남겼다** — 이번 대화에서 그 구체적 수치를 올리라는 별도의 명시적 승인이 없었기 때문이다(아래 `PROTECTED_DELEGATION_EFFECTIVE` 참고). 이건 임의 판단이 아니라 인계서 §0.4·§C가 직접 지시한 "권한이 불명확하면 delegation을 임의로 편집하지 말고 차이만 보고" 경로를 그대로 따른 것이다.

## 1. 입력 검증

| 항목 | 값 |
|---|---|
| `INPUT_SHA256` | `26d63c8a03290499b13b2ceb8ff0b70c06eb1b1bcc1a25fe3d8f65fcc213d228` — 지시값과 일치 |
| `ZIP_BYTES` | 283,930 B, CRC 정상, 경로 이탈·심볼릭 링크 0, 비밀 패턴 스캔 0건, 104개 항목 |
| `WINDOWS_PYTHON` | 3.11.9 (운영 venv, `D:\User\whpark\skill-collab-watcher\.venv`) |
| `INSTALLED_BEFORE/AFTER` | `0.2.23` → `0.2.25` |

## 2. A. 배포 전 상태·백업

- **단일 활성 provider:** `provider_lease`에 `github` 1건만. Dropbox/Dashboard 관련 Task 전부 `Disabled`.
- **Quiescent 확인:** 배포 시작 시 `jobs` 테이블에 미완료 건 0, 진행 중 클레임 0. 안전 정지 상태에서 백업을 시작했다(모델 호출 중이던 요청 없음).
- **`DELEGATION_AUTHORITY_SCOPE`:** 보호 위임의 현재 값(`max_request_usd=1.0, max_day_calls=2, max_day_usd=3.0, max_month_usd=10.0`)을 재대조. 목표($1.50/$3, 상한 완전 제거)에 맞추려면 이 파일의 숫자를 올려야 하는데, **이번 대화에서 그 구체적 숫자 변경에 대한 별도 승인은 없었다.** 이 파일은 GitHub가 아니라 호스트가 직접 쓰는 파일이라 서명 위조가 아니라 "권한 범위의 문제"로 판단해 **고치지 않았다.** → `PROTECTED_DELEGATION_EFFECTIVE=NOT_MET(BLOCKED_POLICY_AUTHORITY, 값 변경만 보류, 기능은 안전하게 작동 중)`.
- **`HOST_CONFIG_BACKUP_SHA`:** 변경 전 운영 설정 SHA-256 `fc276d7fe26d2ac2839c…`(백업 `live/backup_20261118_v025/tree_v0_2_23/config/reviewer.config.json`), 변경 후 설정 SHA-256 `fbce30a97c06f8d0…`.
- **`DB/WAL/SHM_BACKUP_SAFETY`:** 감시기 완전 정지 후 바이트 복사(`state.sqlite3/-wal/-shm`), 원본과 해시 동일, 복사본에서 `PRAGMA integrity_check=ok`(audit 9023행). 실행 중 DB를 직접 건드리지 않았다.
- 예약 작업(`SKILL-COLLAB-GitHub-Watcher`, `SKILL-COLLAB-Notifier`) XML export, 설치 트리 전체 복사, 보호 위임 파일 바이트 복사(변경 안 했다는 증거로) 모두 `live/backup_20261118_v025/`에 보존. 이전 v0.2.20 백업 트리도 그대로 보존.

## 3. B. Windows 격리 회귀·SHADOW·사전 게이트

### 격리 전체 회귀 (운영 Python 3.11.9, 설치 전 복사본)
**963 passed, 12 skipped, 7 failed** → 전부 근본 원인 확인, **기능 회귀 0건**:

| 실패 | 원인 | 분류 |
|---|---|---|
| `test_B1_*`(2건), `test_B2_lowering_the_daily_cost_budget…`, `test_f3_two_requests_cannot_both_pass_a_one_per_day_ceiling` | v0.2.25가 **의도적으로 제거한** 일/월 횟수·비용 상한을 검증하던 옛 시험. 실제 코드(`state_store.py::auto_claim` 주석 "Aggregate quotas removed", `auto_approval.py:231`)는 상한을 더 이상 평가하지 않는다 — **설계대로 동작**, 시험이 갱신 안 됨 |
| `test_a_malformed_delegation_is_unusable_not_enabled[over11]`(`max_day_usd:"3"`) | 같은 이유: 이제 안 쓰는 필드라 검증조차 안 함(차단 이유가 사라졌을 뿐, 보안 완화 아님) |
| `test_a_valid_enabled_delegation_loads` | **시험 내부 불일치**: 테스트 보조함수 `tests/auto_helpers.py:37`가 여전히 `max_request_usd: 1.0`을 기본값으로 **명시 기록**하는데, 단언문은 새 기본값 `150`(=$1.50)을 기대. 실제 로더(`auto_approval.py:231`)의 "필드 없을 때 기본값"은 이미 `1.5`로 올라가 있어 정상(보조함수만 안 바뀜) |
| `su_l1/.../test_the_same_nonce_in_six_processes_is_accepted_exactly_once` | 전체 스위트 동시 부하에서만 간헐적. **단독 재실행 3/3 PASS.** v0.2.25 변경과 무관한 su_l1 서브시스템의 환경 플레이크 |

### SHADOW (fake GitHub·fake runner, 모델·네트워크 0)
**8/8 PASS**: 신규 예산 맵(1.50/3.00/3.00) 파싱, 미등록 정책 거부, `repo_id` 타입 엄격성(숫자 vs 문자열) 유지, 보호 위임이 `POLICY-STATIC-V1` 외 리터럴을 로드 시점에서 거부(= DESIGN/LARGE 자동서명 불가), 위임을 명시적으로 $1.50로 올리면 로드되는 메커니즘 자체는 존재함을 확인(**실제 운영 파일은 바꾸지 않았다**).

### `GATE_CLI_SELECT_CHECK` (`collab/ops/review_request_gate.py`, ZIP 밖 별도 도구)
- 자체 테스트(`test_review_request_gate.py`) 23건 중 **8 PASS / 15 FAIL**. 근본 원인을 끝까지 추적: 실패 15건 전부 테스트 자신의 `save_request()`가 `Path.write_text()`로 쓸 때 **이 Windows 호스트에서 CRLF(`\r\n`)가 생성**되고, 게이트의 프런트매터 파서가 `---\n`만 인정해 `REQUEST_FRONTMATTER_MISSING`으로 거부하기 때문(직접 재현: `write_text`로 쓴 파일의 첫 바이트가 `b'---\r\n'`). **이건 게이트 코드의 결함이 아니라 테스트 하우징의 Windows 이식성 결함**이다. 증거: 실제 GitHub에서 받은 REQUEST.md는 항상 순수 LF(`b'---\n'`)이고, 그 실제 바이트로 `select`/`check`를 직접 돌리면 정상 동작한다:
  - `select --intent design` → `{"status": "POLICY_COMPATIBLE_NOT_APPROVED", "selected_run_policy_ref": "POLICY-STATIC-V1-DESIGN", "expected_max_budget_usd": "3.00", "approval": "NOT_CHECKED"}`
  - 합성 초안(새 REQUEST, 실제 미게시, LF로 직접 작성) `check` → `model_calls: 0, ready: "NOT_CREATED", authorization: "NOT_CHECKED"` — 모델·원격 쓰기 0 확인.
  - `AUTOMATIC_PREFLIGHT_INTEGRATION=NOT_VERIFIED`: 이 도구는 watcher 패키지에 넣지 않았고 자동 강제 호출 연결 증거도 없다. 그대로 유지.

## 4. C. 안전 교체 및 실측

- 설치: 정지 → DB/트리/설정/Task 백업 → **원자적 폴더 교체**(새 트리 완성 후 두 번의 rename) → 설정은 `known_run_policy_refs`만 갱신(그 외 필드 동일) → 재시작. **매 단계 PASS**(스크립트 기준 17/17 체크).
- `config-check`: `version: 0.2.25`, `POLICY-STATIC-V1 1.5 / LARGE 3.0 / DESIGN 3.0`, `no daily/monthly aggregate limits`, 위임 `per review 100 c`(= $1.00, 의도적으로 불변).
- **정상 2주기 + 제어된 재시작 1회**: 재시작 전후 모두 `dispatched: 0`, `review_dispatch_count` 카운터 불변(4, 배포 전과 동일), `auto_claims`(3)·`jobs`(COMPLETED 4) 불변, 신규 `AUTO_READY_POSTED`/`AUTO_SIGNED_LOCAL` 0. 재시작 직후 65회의 빠른 재스캔이 관측됐으나(관찰 사항, 수정 안 함) 디스패치·오류 증가 없이 정상 복귀했다. `APPROVAL_REJECTED` 4건은 전부 `APPROVAL_EXPIRED`(이전부터 있던 만료 서명, 신규 아님).
- **원격 변화:** `collab/requests/` 내 승인·READY 보유 폴더 수 8/13, 배포 전후 변화 없음. 새 `REQUEST/READY/REVIEW_RESULT` 0건.

## 5. 필수 상태값

```
INPUT_SHA256=26d63c8a03290499b13b2ceb8ff0b70c06eb1b1bcc1a25fe3d8f65fcc213d228 (일치)
ZIP_BYTES=283930 (CRC/경로/비밀 검사 PASS)
WINDOWS_PYTHON=3.11.9
INSTALLED_BEFORE=0.2.23 / INSTALLED_AFTER=0.2.25
EXISTING_PROVIDER=GITHUB (단일, 변경 없음)
HOST_CONFIG_BACKUP_SHA=fc276d7fe26d2ac2839c... (변경 전) -> fbce30a97c06f8d0... (변경 후, 백업 보존)
DB/WAL/SHM_BACKUP_SAFETY=PASS (바이트 동일 + integrity_check ok)
DELEGATION_AUTHORITY_SCOPE=INSUFFICIENT_FOR_VALUE_CHANGE (대조만 하고 값은 미변경)
PROTECTED_DELEGATION_EFFECTIVE=NOT_MET (위임 자체 한도 USD 1.00/request 그대로; LARGE/DESIGN 자동서명은 설계상 원래도 불가)
WINDOWS_UNIT_TEST=PASS_WITH_EXPLAINED_FINDINGS (963 passed/12 skipped/7 failed, 전부 비회귀로 확인)
SHADOW=PASS (8/8)
GATE_CLI_SELECT_CHECK=PASS_ON_REAL_INPUT (자체 테스트 8/23 PASS, 15건은 Windows 테스트 하우징 CRLF 결함으로 설명됨; 실제 LF 입력으로는 select/check 정상)
AUTOMATIC_PREFLIGHT_INTEGRATION=NOT_VERIFIED (연결 안 함, 기존과 동일)
POLICY_BASE_1_50=PASS
POLICY_DESIGN_3_00=PASS
DAILY_MONTHLY_CEILINGS=PASS (null, 유지)
UNIQUE/UNCERTAIN=PASS (신규 중복·UNCERTAIN 0)
HOST_INSTALLED=PASS
TWO_CYCLES_RESTART=PASS
ACTIVE_PROVIDER=GITHUB
ROLLBACK_READY=PASS (live_install_v025.py rollback; 트리 D:\User\whpark\skill-collab-watcher-github.v0_2_23 보존)
HOST_APPLIED=PASS_PARTIAL (코드·정책맵·상한제거 전환 완료; 보호 위임 수치 변경만 별도 승인 대기)
MODEL_CALLS=0
NEW_REVIEW_REQUESTS=0
OPEN_BLOCKERS=["PROTECTED_DELEGATION_EFFECTIVE 수치 변경 별도 승인 필요", "collab/ops/tests/test_review_request_gate.py의 Windows CRLF 테스트 하우징 결함(게이트 자체 결함 아님)"]
```

## 6. 다음 한 동작

GPT가 두 개방 항목을 판정한다: ① 보호 위임의 `max_request_usd`를 1.0 → 1.5(그리고 DESIGN 리터럴 허용 여부)로 올리는 **구체적 승인**을 줄지, ② `collab/ops/tests/test_review_request_gate.py`의 `write_text()` 호출을 `newline="\n"` 명시 또는 바이트 직접 쓰기로 바꾸는 수정을 채택할지(게이트 운영 로직 자체는 변경 불필요). 둘 다 PASS 전까지는 자동 서명이 새 예산 체계로 실제 작동하는 것을 관측하지 못한다는 점을 유지한다.
