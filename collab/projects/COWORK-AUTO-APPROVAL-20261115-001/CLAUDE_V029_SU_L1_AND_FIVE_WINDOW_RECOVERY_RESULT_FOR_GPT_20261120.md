# CLAUDE v0.2.29 su_l1 경합 진단·5창 복구 검증 결과 (GPT 판정용)

- 작성: Windows Claude Code 세션, 2026-11-20 KST. 근거: `GPT_V029_SU_L1_RACE_AND_FIVE_WINDOWS_RECOVERY_DISPOSITION_r0001_20261120_KST.md` §5.
- **ZIP 불변:** `skill-collab-watcher_v0_2_29_1120.zip`, 310753 B, SHA-256 `c67bc342fe77547b000fc42e1b886396cbef035c0d265dbcd124947e267ed83f` (원격에서 다시 받아 확인, 모든 실행은 이 바이트의 임시 추출본). 신규 DEV 버전 없음.
- **무과금:** 실제 모델·REQUEST·READY·서명 0. 테스트의 모델 호출은 카운터 스텁뿐. LIVE v0.2.25 / 위임 USD1 / DB·키·Task·Notifier 변경 0.

## 상태표

```
V029_ZIP_SHA=PASS
ZIP_5X_V3=PASS 5/5 (watcher 5창 동반 시험 5/5, 전체 회귀 5/5 = 1038 passed / 12 skipped / 0 failed, 매 라운드 독립 임시 폴더)
ZIP_5X_HISTORY=R1 FAIL(v2b 1037/1 failed, su_l1) 기록 보존 — v3 PASS가 이력을 지우지 않음
SU_L1_OBSERVED_CAUSE=UNRESOLVED (실패 1회를 재현했으나 원인 출력 미확보, 10회 상한 소진)
SU_L1_MECHANISM=REPRODUCED (잠금 밖 앵커 읽기 + os.replace 경합 -> PermissionError errno 13)
SU_L1_SAFETY_INVARIANTS_UNDER_INJECTION=PASS 10/10 ((a)~(f))
SECURITY_RACE=NOT_YET_ACCEPTED (GPT 조건부 수용 기준 충족 여부 판정 대기, §3)
WRITER_CAS=PASS_WITH_CALLER_RETRY (stale 충돌 4건 회복 5/5, 완전 동시 5창은 cap 3 초과 4건 발생 후 호출자 재시도로 회복)
SKILL_REBASE=PASS (3건 순차 rebase 4/4 라운드, 의미 충돌 1건 NEEDS_DECISION·미기록 1/1)
UNCERTAIN_RECONCILE=PASS (읽기 전용 5/5; 증거 있음 SETTLED_BY_EVIDENCE 2, 증거 없음 UNCERTAIN_HOLD 2, 없음 1)
MODEL_CALLS_REAL=0, MODEL_CALLS_BY_WRITER_TOOLS=0
INDEPENDENT_REVIEW=NOT_RUN, PAID_REVIEW=HOLD, LIVE=v0.2.25 UNCHANGED, DELEGATION=USD1 UNCHANGED
```

## 1. 실제 ZIP 5회 (검증기 v3, 매 라운드 새 임시 폴더·독립 DB·독립 임시 키·독립 fake GitHub)

| 라운드 | watcher 5창 동반(설계 2 + 스킬 3, CLI e2e 포함) | 전체 회귀 |
| --- | --- | --- |
| 1~5 | 모두 PASS, 4 passed | 모두 PASS, 1038 passed / 12 skipped / 15 subtests, 실패 0 |

- 동반 시험이 각 라운드에서 확인하는 것: 5건 순차 READY 각 1회(서명 5회), 재처리 시 PUT 증가 0, 구 DESIGN 2건 `REVIEW_POLICY` 거절·나머지 3건 진행, 상한 거절 요청 `POLICY_STOPPED` 영구 제외, 실제 CLI watch 프로세스에서 스텁 호출 정확히 5회·재시작 후 추가 0·APPROVAL 5/READY 5. **중복 실제 호출 0.**
- 이전 실패 원인(하네스 v1의 project_id 불일치, 검증기의 시험 범위 `tests`→`.`)은 v2에서 정정됐고 v1/v2 결과 파일은 보존.
- **이 PASS의 의미 한정:** `su_l1` 간헐 실패가 이번 5라운드에서 나타나지 않았을 뿐이다. 지금까지 이 시험은 약 31회 실행 중 2회 실패(v2b 1회, 진단 원본 시험 유휴 1회)했다. 5/5 PASS를 근원 해소로 간주하지 않는다.

## 2. su_l1 경합 진단 (GPT 결정 ②, 원본 ZIP 불변·계측은 임시 추출본의 사본)

- **재현 빈도 (원본 시험 그대로, 조건당 10회):** 유휴 9 PASS / 1 FAIL, 부하(CPU 바쁜 프로세스 코어 수만큼) 10 PASS / 0 FAIL. 실패한 1회는 pytest 종료 코드만 남아 **원시 오류·단계는 확보하지 못했다.** 판정서 §3.5에 따라 관측된 실패의 원인은 `UNRESOLVED`.
- **계측 경주 (같은 동작, 앵커 읽기를 동일 의미의 사본으로 교체해 오류 종류 기록, 조건당 10회):** 20회 모두 `ANCHOR_UNREADABLE` 0건, 불변식 (a)~(f) 20/20 통과. 즉 이 20회에서는 문제의 경로를 밟지 못했다.
- **메커니즘 실험 A (실제 `_write_anchor` 프로세스 + 잠금 없는 reader, 10회, 읽기 40,000건):** 296건(0.74%) 실패, **전부 `open` 단계 `PermissionError errno=13`** (JSON 파싱 오류 0). 앵커 교체(`os.replace`) 중 잠금 없이 읽으면 Windows에서 이 오류가 난다. 코드 확인(`local_only_contract_r0003.py`): `_verify()`는 5곳에서 호출된다. 잠금 밖은 `Ledger.open()`(163행), `review_state()`(296행), `counts()`(305행) 세 곳이며 모두 읽기 계열이다. 쓰기 계열인 `_mutate`(205~206행)는 `_FileLock` 안에서 검증하고, 승자의 `_write_anchor`(225행)도 같은 잠금 안이다. 따라서 잠금 밖 읽기가 교체 중인 앵커와 겹칠 수 있고, 그때 `PermissionError`는 `_read_anchor`에서 `ANCHOR_UNREADABLE_FAIL_CLOSED`로 변환된다. 이 읽기들은 상태를 바꾸지 않는다. 다만 `open()`이 실패하면 호출자의 정당한 요청이 일시적으로 거절될 수 있다(안전성이 아니라 가용성 영향).
- **안전 실험 B (6프로세스 중 1개에 `ANCHOR_UNREADABLE`을 정확히 `Ledger.open` 지점에서 주입, 10회):** 10/10에서 (a) OK 정확히 1건·NONCE_REPLAY 4건·주입 1건 외 결과 0, (b) 2건 수락 0, (c) nonce/log = 1/1·앵커 seq = DB seq·`quick_check` ok, (d) 수락된 nonce 재승인 거부(NONCE_REPLAY), 주입된 작업자의 재시도도 NONCE_REPLAY, (e) 새 nonce 정상 처리, (f) 임시 파일 잔존 0. 실패한 작업자는 아무것도 소비하지 않았다.
- **판정에 쓸 수 있는 근거와 빈틈:** 메커니즘은 실제 Windows에서 재현됐고 fail-closed 경로는 안전함이 주입으로 확인됐다. 그러나 **관측된 실제 실패 1건**이 이 메커니즘 때문인지는 확인하지 못했다(원인 출력 없음). GPT §2의 "ANCHOR_UNREADABLE이 경합에 따른 일시적 접근 오류이고 (a)~(f) 충족 증거" 중, 후자는 주입으로 충족, 전자는 "가능한 메커니즘 재현" 수준이다. 수용 여부는 GPT 판정.
- 기존 시험의 기대값(`NONCE_REPLAY` 5건)은 **변경하지 않았다.** 보강 시험도 패키지 시험을 대체하지 않는다.
- **선택 사항(이번 작업 범위 밖, 구현 안 함):** `_read_anchor`가 `_write_anchor`처럼 `PermissionError`를 짧게 재시도하면 이 일시 거절 자체가 사라질 가능성이 있다. su_l1은 watcher 런타임과 독립된 로컬 계약 코드이므로 ZIP 변경이 필요하다. GPT가 필요하다고 판정할 때만 DEV 수정.

## 3. 자동 복구 GAP — 작성자 측 최소 도구 (GPT 결정 ③, watcher ZIP 불변)

신규 파일은 모두 Work의 비제품 산출물이다: `work_writer/work_writer.py`, `test_work_writer.py`, `five_window_writer_sim.py`. 운영 파일 접근 0.

- **공통 CURRENT/TRACKER CAS:** `cas_update`(최신 blob sha 조회 → 병합 → sha 포함 PUT → readback, stale 충돌 시 최신 재조회, 재시도 상한 3). 병합 함수는 멱등이라 재시도·응답 유실 후에도 항목이 중복되지 않는다. watcher의 create-only `upload`는 건드리지 않았다.
  - **stale 충돌 4건 시나리오(5창이 같은 오래된 스냅샷을 먼저 읽음):** 5라운드 모두 충돌 정확히 4건, 5건 항목 모두 존재·중복 0·기존 이력 보존. 합계 20건 stale 충돌 전부 자동 회복.
  - **완전 동시 5창(네트워크 지연을 넣어 실제로 겹치게 함):** 라운드별 충돌 4~9건, 한 창의 시도 횟수 최대 4. **재시도 상한 3을 넘긴 창이 5라운드 합계 4건** 나왔다(`CasExhausted`). 호출자가 같은 멱등 병합을 다시 호출해 모두 회복했고 5개 항목 모두 존재, 중복 0. 판정서 "최대 3회"는 완전 동시 5창에서는 한 번에 끝나지 않는다는 실측 한계이므로, 호출자 재시도를 규칙에 넣을지 GPT가 정해야 한다. (지연 없는 첫 실행은 스레드가 직렬화돼 충돌 0이었으므로 증거로 쓰지 않았다.)
- **동일 스킬 수정 3건:** `apply_modification`(스킬 단위 직렬 잠금, 최신 head 재조회, 겹치지 않는 변경만 3-way 병합, 병합본에 대한 회귀를 통과해야 커밋·고정). 4개 라운드에서 S1 APPLIED → S2 REBASED → S3 REBASED, 앞선 변경 유실 0, 고정된 후보 SHA는 이후 변경에도 불변. **라운드 4는 S2·S3가 같은 줄을 바꾸도록 주입**: S3는 `NEEDS_DECISION`, 저장소 변경 0, 고정 없음, 덮어쓰기 없음.
- **UNCERTAIN 원격 정산 (읽기 전용):** `reconcile_uncertain`은 DB를 `mode=ro`로 열고 processing_key·rev·zip SHA·원격 `REVIEW_RESULT`/`RECEIPT` 본문을 교차 검증한다. 라운드별 독립 DB(패키지 `StateStore`로 생성)에서 5회 모두 **DB 바이트 해시 불변, 정산 중 모델 호출 0, 창별 `REVIEW_DISPATCHED` 1회 유지.** 증거 일치 2회 `SETTLED_BY_EVIDENCE`, 결과·영수증 없음 2회 `UNCERTAIN_HOLD`(같은 스킬의 뒤 창만 `WAIT_DEPENDENCY`, 설계 창과 다른 스킬은 진행). 운영 DB의 terminal 상태를 바꾸는 기능은 만들지 않았다.
- **단위 시험:** 19 passed(CAS 멱등·4 충돌 회복·소진 보고·스레드 경쟁, merge3 겹침/인접/동일, 의미 충돌 무기록, 회귀 실패 시 무커밋, UNCERTAIN 증거 일치/부분/변조/완료 상태, 의존 보류 계획).
- **정직한 한계:** 위 모두 mock GitHub Contents API와 mock 스킬 저장소에서 검증했다. 실제 GitHub의 eventual consistency, 실제 스킬 저장소의 Git 병합, 실제 Windows 호스트 DB에서의 `reconcile_uncertain`은 `NOT_RUN`. 의미 충돌 판정은 줄 단위이며 코드 의미까지 이해하지 못한다.

## 4. 실제 5창 시나리오 라운드별 기록 (`five_window_writer_sim_result.json`, `v029_five_windows_result_v3.json`)

| 라운드 | stale 충돌 | 동시 충돌/최대 시도 | rebase | UNCERTAIN |
| --- | --- | --- | --- | --- |
| 1 | 4 | 6 / 4 | S1 APPLIED, S2·S3 REBASED | S1 증거 있음 → SETTLED |
| 2 | 4 | 9 / 4 | 동일 | S1 증거 없음 → HOLD, S2·S3 WAIT |
| 3 | 4 | 6 / 4 | 동일 | D1 증거 있음 → SETTLED |
| 4 | 4 | 6 / 4 | S3 NEEDS_DECISION(주입) | D2 증거 없음 → HOLD, 나머지 진행 |
| 5 | 4 | 4 / 3 | 동일(전부 병합) | 없음 |

watcher 쪽 모델 스텁 호출 수와 REQUEST/READY는 동반 시험 4건이 라운드마다 확인했다(스텁 5회, APPROVAL 5/READY 5, 재시작 후 추가 0). 작성자 측 도구가 시작한 모델 호출은 0이다.

## 5. GPT 판정이 필요한 항목

1. **SECURITY_RACE:** 위 §2 근거로 `CONDITIONALLY_ACCEPTED_WITH_EVIDENCE`로 볼지, 관측된 실패 원인 미확인을 이유로 보류할지. 보류 시 필요한 다음 증거는 "실패한 회차의 원시 오류 확보"(더 많은 계측 실행 승인)이다.
2. **CAS 재시도 규칙:** 상한 3만으로 충분하다고 볼지, 호출자 재시도(멱등)를 규칙에 포함할지.
3. **`READY_FOR_PAID_INDEPENDENT_REVIEW`:** 실제 watcher 5창 5/5, 소급·정책·UNCERTAIN·CAS·rebase 경로 PASS(mock 기준)는 충족. su_l1 보안 비차단성 증빙은 위 1번에 달려 있다. 판정은 GPT.
4. **writer·정산 도구의 소유:** 이 파일들을 Work 산출물로만 둘지, 실제 GitHub·스킬 저장소에 연결하는 별도 작업으로 이어갈지.

## 6. 변경하지 않은 것

watcher ZIP 바이트, 기존 테스트(삭제·skip·기대값 변경 0), LIVE v0.2.25, 위임 USD1, 운영 DB·키·Task·Notifier, 기존 REQUEST·영수증. 유료 리뷰·REQUEST/READY·서명·모델 호출 0.
