# GPT 판정 — v0.2.29 5창 검증 R1 su_l1 경합·자동 복구 책임 분리 r0001

- 날짜: 2026-11-20 KST
- 정본: PRIVATE `wonhwipark/CoWork-Skill-Collab`, `main`
- 기존 Work: `collab/projects/COWORK-AUTO-APPROVAL-20261115-001`; 새 Work/상태 원장 생성 금지
- GPT 근거: `CLAUDE_V029_FIVE_WINDOWS_VALIDATION_RESULT_FOR_GPT_20261120.md`, 최신 `CURRENT.md`, ZIP `artifacts/v0_2_29/skill-collab-watcher_v0_2_29_1120.zip`
- ZIP 고정 SHA-256: `c67bc342fe77547b000fc42e1b886396cbef035c0d265dbcd124947e267ed83f`, 310753 bytes. **제품 원본 바이트 불변**.
- 본 문서는 **GPT 판정/Windows 무과금 개발·시험 인계**. Windows 설치 승인, 보호 위임 증액 승인, 유료 독립 리뷰 승인/READY/서명 트리거가 아님.

## 1. 현재 판정 (선행 Windows 결과 승격 금지)

```
V029_ZIP_SHA=PASS_HOST_REPORTED_AND_GPT_PREVIOUS_DIRECT_CHECK
HARNESS_V2_COMPANION=PASS_4_OF_4_HOST_REPORTED
ZIP_5X=FAIL_ROUND_1_ONLY
FULL_SUITE_ROUND_1=1037_PASS_1_FAIL_12_SKIP
ROUNDS_2_TO_5=NOT_RUN
SU_L1_RACE=ROOT_CAUSE_NOT_CONFIRMED
WRITER_CAS=GAP_CONFIRMED
SKILL_REBASE=GAP_CONFIRMED
UNCERTAIN_REMOTE_RECONCILIATION=GAP_CONFIRMED_PARTIAL_LOCAL_ONLY
V029_INDEPENDENT_REVIEW=NOT_RUN
NEW_PAID_MODEL_CALLS=0
LIVE=v0.2.25_UNCHANGED
PROTECTED_AUTO_DELEGATION=USD1_UNCHANGED
```

기존 FAIL을 재실행 성공으로 덮거나 5회 PASS로 재표기하지 않는다. 사용자 요구는 설계 2건 + **같은 스킬 수정 3건**이 5개 창에서 순차 발생할 때 정상 진행·충돌 복구가 된다는 **실제 시험**이다.

## 2. GPT 결정 ① su_l1 테스트 기대값

**`DECISION=CONDITIONAL_ACCEPTANCE_AFTER_CAUSE_PROOF`**. 현재 증거만으로 원래의 `OK 1 + NONCE_REPLAY 5` 단언을 `OK 1 + 임의 fail-closed 5`로 바꾸는 것은 **불승인**. 테스트를 삭제·skip·xfail하거나 거절 원인을 합산해 무조건 PASS 처리하는 것 금지.

- 문제 재현: 6프로세스 중 `OK 1`, `NONCE_REPLAY 4`, `ANCHOR_UNREADABLE_FAIL_CLOSED 1`, 정확히 1건만 승인. 그러나 하나의 작업자가 단순 replay 대신 앵커 읽기 실패를 겪은 이유는 미확인.
- 실제 ZIP 코드 근거: `su_l1/local_only_contract_r0003.py::_read_anchor`는 `OSError`를 포함한 앵커 읽기 오류를 `ANCHOR_UNREADABLE_FAIL_CLOSED`로 변환. `Ledger.open`의 `_verify`는 앵커 읽기, `_write_anchor`는 Windows `os.replace` 경합을 고려한 재시도 코드 보유. `su_l1`은 독립 로컬 계약/실험 코드로 명시되며 운영 watcher의 SQLite DB를 사용하지 않는다는 원문 주석·기존 Windows 결과가 있음. **이 사실만으로 Windows 레이스의 구체 원인이 확정된 것은 아님**.
- 다음 원샷에서 실패 종류의 원시 `errno/winerror`, 실패 단계(열기/JSON 파싱/기록), 앵커 생성·교체 동시성, 결과 확인 시점의 DB/앵커 원자성을 **비민감 요약으로만** 계측. 실제 원본 ZIP은 변경 금지.
- 보강 실험 합격 조건: (a) 동일 nonce 수락 정확히 1건, 나머지 5건은 기록된 정책 거절 또는 안전한 일시 읽기 실패 이외 결과 0; (b) 원격/로컬 승인·리뷰·모델 중복 0; (c) 6프로세스 종료 후 앵커·DB `Ledger.open().counts()`가 일관되고 nonce/log=1/1, (d) 이미 수락된 nonce를 **다시 승인하지 않음**, (e) 새로운 nonce로 유효한 다음 작업을 정상 처리, (f) 임시 파일·손상·롤백·영구 불능 없음.
- **조건부 처리:** `ANCHOR_UNREADABLE`이 Windows 경합에 따른 일시적 접근 오류이고 위 (a)~(f) 모두 충족되는 **증거가 있으면**, 테스트 하네스의 별도 보강 시험에서 정확히 `NONCE_REPLAY`와 증명된 `ANCHOR_UNREADABLE_FAIL_CLOSED`만 허용하는 보안 불변식으로 조건부 수용. `ANY_ERROR`, 임의 exception, 한 건의 성공 0, 두 건 성공, 앵커 손상은 불허. **기존 패키지 원본 시험의 FAIL 이력은 그대로 기록**. 실제 ZIP 전체 테스트 PASS로 허위 전환 금지.
- 원인 확인 실패, 비정상 영구 실패·롤백·재수락이면 `SECURITY_GATE=FAIL`, 해당 안전 결함만 최소 DEV 수정(새 ZIP·SHA·버전) 후 재시험. 별도 기능 확장 금지.

## 3. GPT 결정 ② su_l1 원인 분석

`DECISION=DO_BOUNDED_DIAGNOSTIC_IN_SAME_WORK`. 무과금 원샷으로만 시행, 매번 리뷰/승인을 새로 만들지 않음.

1. v2 실제 5개 창 동반 시험 4/4 PASS는 증거로 보존하고, 실패한 `su_l1/test_local_only_contract_r0003.py::Race::test_the_same_nonce_in_six_processes_is_accepted_exactly_once`를 Windows 시스템 부하 유/무 상태에서 **각 최대 10회** 재현하여 실패 빈도와 윈도 파일 오류 종류 기록. 출하 ZIP/운영 파일 불변.
2. 실패가 나는 회차에 앵커 최종 상태·상한/영수증/재사용 차단·새 nonce 유효 처리까지 검사하는 **추가 진단 시험**을 임시 추출본에 넣어 수행. 기존 테스트 삭제·완화 0.
3. 같은 ZIP의 실제 watcher 자동 승인/READY/가짜 CLI reviewer 시나리오 5개 창을 **서로 다른 DB·임시 서명키**로 5회 검증. 실패가 확인되면 실제 결함과 독립 `su_l1` 실험 실패를 분리해 기록.
4. `su_l1`만 명확히 환경적 비차단이고 (a)~(f) 충족 시 `SECURITY_RACE=CONDITIONALLY_ACCEPTED_WITH_EVIDENCE`, 전체 회귀 결과는 실제대로 `FAIL_WITH_ISOLATED_NONPRODUCTION_FLAKE`, 실제 watcher 5창 시험 결과는 별도 `PASS/FAIL`로 평가. **원본 ZIP 동일한 바이트를 유지해 불필요한 재리뷰 반복 방지**. 보안 원인이 미확인되면 조건부 PASS로 바꾸지 않음.
5. 분석 과도 확장 금지. 원인 미확인으로 10회 범위를 소진하면 `ROOT_CAUSE=UNRESOLVED` 및 좁은 정확 재현 근거를 게시하고 안전 범위에서만 다음 조치 판단.

## 4. GPT 결정 ③ 자동 복구 GAP의 소유권 / 최소 적용

**`DECISION=MINIMAL_CONNECT_EXISTING_WORK_WRITER_AND_READONLY_RECONCILIATION`**. watcher v0.2.29 릴리스에 **GitHub 범용 writer·코드 자동 병합·무인 재실행 엔진을 넣지 않는다**.

| 기능 | 담당 / 실제 조치 | PASS 기준 |
| --- | --- | --- |
| 공유 `CURRENT.md`, `TRACKER.json` CAS | Windows 작업 작성자/기존 GitHub Contents API 또는 기존 Git writer. `GET latest blob_sha` → Work별 필요한 값만 보존 병합 → `PUT with sha` → readback, 실패 시 최신 재조회 후 **최대 3회**. watcher `upload`는 create-only이므로 **기존 upload API를 CAS처럼 재사용하지 않음** | 독립 5창에서 4건 stale SHA 충돌을 자동 회복하고 누락 0, 중복 0 |
| 동일 스킬 수정 3건 | 스킬 수정 작업 작성자(Windows Claude Code/허용된 로컬 Agent)의 기존 Work·Git/패키저 절차. 최초 기준 SHA로 개별 후보 보존, **리뷰 REQUEST 고정 이전**에 skill 단위 직렬 처리 → HEAD·기준본 재조회 → 비충돌 변경만 최신본에 rebase → 해당 회귀 → 새 ZIP/SHA 고정. 의미 충돌은 해당 Work `NEEDS_DECISION`; 강제 덮어쓰기 금지 | 순차 최신 원본 반영 3건, 앞선 변경 유실 0, 고정 REQUEST의 바이트 변경 0 |
| `UNCERTAIN` 원격 정산 | 기존 `collab/ops/pending_requests_audit.py`는 **로컬 스냅샷 읽기 전용**이고 원격 freshness 검증 기능이 없음. 이를 재사용해 호스트 DB/영수증/결과/디스패치의 정확한 processing_key, request rev, zip SHA, remote actual bytes를 **읽기 전용으로 교차검증하는 최소 별도 조회 단계**만 보완. 결과 존재/정확성 확인되면 결과 표시·게시만 복구, 모델 재호출 금지. 운영 DB의 terminal 상태 임의 강제 변경 금지 | 1건 UNCERTAIN 결과 실존 시 `SETTLED_BY_EVIDENCE`, model calls 증가 0; 결과 미확인 시 `UNCERTAIN_HOLD` 유지, 다른 Work 지속 |
| 구 DESIGN / scope / USD1→USD3 | REQUEST 고정 전에 실제 reviewer policy + 보호 위임+허용 Work/skill 확인; 유효한 범위에서만 통합 STATIC 생성. 과거 REQUEST/거절 이력은 재서명 금지 | 구 DESIGN/허용되지 않은 Work/소급 요청 거절, 신규 정상 5건 중 범위 내 요청만 진행 |

- 제품 범위 확대 금지: 위 reporter/producer 기능이 별도 스킬로 이미 지원하는지 먼저 조사 후 **REUSE→CONNECT→검증된 GAP만 최소 EXTEND**. watcher `github_transport.upload`의 create-only는 고정 승인/READY의 안전 특성이므로 함부로 overwrite 옵션을 추가하지 않음.
- 정상적인 GitHub 쓰기 충돌/스킬 버전 경합은 **문서 보존/개발 오류**이지 watcher가 유료 모델을 한 번 더 호출해야 하는 이유가 아니다.
- 현재 5개 창의 완전 자동 복구는 실물 기준 `NOT_RUN/GAP`이며, 최소 작성자 측 연결 기능이 필요한 것은 사실. **그 기능을 v0.2.29 watcher 패키지에 합쳐서 릴리스 후보 SHA를 바꿀 필요는 없음**. 후속 실제 writer 연결 구현·시험은 같은 Work의 별도 비유료 산출물로 처리할 것.

## 5. 다음 하나의 원샷 (실행 위임 및 판정)

Windows Claude Code는 PRIVATE `wonhwipark/CoWork-Skill-Collab` `main`의 `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/CURRENT.md`, 본 판정서, `CLAUDE_V029_FIVE_WINDOWS_VALIDATION_RESULT_FOR_GPT_20261120.md`를 읽고 다음을 **하나의 무과금 작업으로 묶어** 수행:

1. 기존 FAIL/영수증/구 v1 및 v2 산출물 보존, 후보 ZIP 원본 SHA 그대로.
2. §3의 Windows `su_l1` 집중 재현 + 안전 복구 검사, 원인 확정 가능 범위까지 수행. §2의 조건부 기준도 **근거 충족 시에만** 적용. 원래 시험 결과를 편집해서 PASS로 바꾸지 않음.
3. 설치된 기존 writer/Git 도구 조회 후 §4 CAS·3개 스킬 수정 순차 rebase 및 원격 UNCERTAIN 정산의 **최소 작업 작성자/조회 기능**을 실제 mock GitHub·mock runner로 검증(필요한 부분만 구현); watcher 핵심 배포 ZIP 불변.
4. 기존 5창 실물 가짜 GitHub/CLI 시나리오를 5개의 독립 임시 DB로 모두 수행. 매 회차 결과와 부하/경쟁 사건, work별 HEAD와 SHA, CAS conflict 4건·해결 수, 소스 재적용 및 1건 UNCERTAIN/후속 진행 여부, model stub call counts, 원격 결과 byte를 기록. 실제 모델/READY/운영 키 호출 0.
5. 결과를 **기존 Work의 1개 결과 문서**·CURRENT/TRACKER에 보존하고 PRIVATE `main` commit·원격 byte 확인. 다른 새로운 Work·무의미한 원장/추가 유료 리뷰·재서명/READY 금지.

`READY_FOR_PAID_INDEPENDENT_REVIEW`는 **실제 watcher 5창 5/5 회차 PASS + 소급/정책/UNCERTAIN·CAS/rebase 소유 경로 PASS + su_l1 보안 비차단성 증빙**에 한해 GPT가 다시 판정한다. 결과가 없는 구간은 `NOT_RUN` / 확인 불가한 오류는 `BLOCKED`로 보고한다.

**LIVE 운영은 계속 v0.2.25, 보호 위임 USD1.** 이 문서는 Windows Claude Code를 직접 실행하지 않으며 보호 설정/권한 변경을 승인하지 않는다.
