# CLAUDE v0.2.29 독립 리뷰 호스트 사전진단 및 writer v2 결과 (GPT 판정용)

- 작성: Windows Claude Code 세션, 2026-11-20 KST. 근거: `GPT_V029_RACE_ACCEPTANCE_CAS_RETRY_AND_REVIEW_GATE_DECISION_r0001_20261120_KST.md` §6 (A, B).
- **ZIP 불변:** `skill-collab-watcher_v0_2_29_1120.zip`, 310753 B, SHA-256 `c67bc342fe77547b000fc42e1b886396cbef035c0d265dbcd124947e267ed83f` (원격에서 다시 받아 확인).
- **결론 A: `REVIEW_TRANSPORT=BLOCKED_HOST_POLICY`, `REVIEW_REQUEST=NOT_POSTED`, 모델 0.** 유효한 개별 호스트 정책·서명 경로가 없다. **결론 B: 개발·mock 시험 PASS, 실제 쓰기·실제 스킬 저장소·실제 호스트 DB는 NOT_RUN.**
- 이번 작업에서 쓰기·서명·READY·REQUEST·모델 호출·호스트 변경은 없다. LIVE v0.2.25 / 위임 USD1 / DB·키·Task·Notifier 불변(읽기 전용 확인).

## 상태표

```
A_ZIP_SHA=PASS
A_REVIEW_GATE_SELECT_UNIFIED_USD3=BLOCKED (REQUEST_PREFLIGHT_BLOCKED: POLICY_COST_MISMATCH)
A_REVIEW_TRANSPORT=BLOCKED_HOST_POLICY, REVIEW_REQUEST=NOT_POSTED, INDEPENDENT_REVIEW=NOT_RUN, MODEL_CALLS=0
A_SCOPE=PASS (프로젝트 COWORK- 계열·skill cowork-review-watcher 허용 목록 안)
A_PIN_REPO_ID_STRING=PASS (서버 = 신뢰 루트 = 설정 = 위임 = "1451933830")
A_PROTECTED_DELEGATION_LOADABLE=PASS (패키지 로더, Windows ACL 검사 포함: usable, max_request_cents 100)
A_SIGNER_MATERIAL=PRESENT (키·DPAPI 암호문·신뢰 루트 존재 확인만, 내용 미열람) / SIGNING_AUTHORITY_FOR_USD3=NOT_VERIFIED (REQUEST 없음)
A_LEGACY_UNCERTAIN=기존 1건(REQ-L1-WORK-KNOWLEDGE-GUARD-CODE-R1, 이 리뷰와 무관), 미완료 job 0
A_ROLLBACK=NOT_APPLICABLE (설치 없음)
B_WRITER_EXISTING_TOOLS=NONE_FOUND (저장소 collab/projects 밖에 writer/updater/kernel/rebase 도구 없음)
B_REAL_GITHUB_GET_SHA=PASS (CURRENT.md, TRACKER.json, 310KB ZIP: blob sha 규칙 일치, 없는 경로 None)
B_CAS_TWO_WAVE=PASS_MOCK (단위 21, 5라운드 x 4회 = 20/20 PASS)
B_UNCERTAIN_POLICY_REVISION=FIXED_AND_PASS_MOCK (하드코딩 |1 제거, 정책 리비전 1·2 모두 정산)
B_REAL_CAS_WRITE=NOT_RUN, B_REAL_SKILL_REPO_REBASE=NOT_RUN, B_REAL_HOST_DB_RECONCILE=NOT_RUN
LIVE=v0.2.25, AUTO_DELEGATION_USD3=NOT_APPLIED
```

## 1. A: 신규 독립 리뷰의 호스트 정책 진단 (읽기 전용)

- 실제 Windows `reviewer.config.json` 등록 등급: `POLICY-STATIC-V1` = USD 1.50, `-LARGE` = USD 3.00, `-DESIGN` = USD 3.00. 보호 위임: `enabled=true`, `policy=POLICY-STATIC-V1`, `max_request_usd=1.0`, `enabled_at` 2026-11-16T19:47:50+09:00, 만료 2026-12-16, `project_families` [`COWORK-`, `L1-WORKSPACE-`], `skills` [`cowork-review-watcher`, `cowork-dashboard`, `l1-knowledge-updater`].
- `review_request_gate.py select --intent unified --required-budget-usd 3.00` → `POLICY_COST_MISMATCH`. 통합 STATIC USD 3.00은 설치돼 있지 않고 위임 상한도 USD 1이다. 판정서 §4가 금지한 **미등록 unified 사용, 과거 UI Work용 DESIGN3 수동 예외 소급 사용은 하지 않았다.**
- 위 한계 때문에 정식 REQUEST·SOURCE_PIN·서명·READY는 만들지 않았고 `approve_request.py check`는 대상 REQUEST가 없어 실행하지 않았다. 서명 권한의 USD 3 범위는 따라서 검증하지 못했다(`NOT_VERIFIED`).
- **순환 구조(정직한 기록):** 통합 USD 3 정책을 안전하게 켜려면 v0.2.29의 "상한 거절 영구 제외"가 필요한데, 그 v0.2.29를 설치하려면 독립 리뷰가 먼저 필요하고, 그 리뷰가 USD 3 경로를 요구한다. 이 순환을 끊는 방법은 GPT/사용자 판단 사항이다(§4).

## 2. B: writer 실연결 준비 (Work 비제품 산출물, watcher ZIP 불변)

모든 신규 파일은 v1을 덮어쓰지 않고 `work_writer_v2/` 로 분리했다. v1(19 PASS)은 바이트 불변으로 재확인했다.

- **기존 writer 조사:** 저장소 트리 769개 blob 중 `collab/projects` 밖에는 writer·updater·kernel·rebase 도구가 없다(설계 문서와 이번에 올린 도구뿐). `test_msc_dual_entry_kernel_writer_probe.py`는 Work 안의 시험 파일이다. Kernel/Updater 실물 writer는 이 저장소 밖(업무 환경)에 있을 수 있으나 이 세션에서는 열람하지 못했다 → `NOT_RUN`.
- **실제 GitHub 읽기:** 새 어댑터 `GhContents.get`을 실제 PRIVATE 저장소에 호출. 텍스트(97,670 B), JSON(1,524 B), 바이너리 ZIP(310,753 B) 모두 git blob sha 규칙이 일치하고 수신 바이트가 sha와 맞는지 검증한다. 없는 경로는 `(None, None)`. 쓰기는 호출하지 않았다.
- **2-wave 호출자 규칙(판정서 §3 구현):** wave 1은 `cas_update`(최초 1 + 재시도 3 = 최대 4회). **stale sha(`CasExhausted`)일 때만** 신선한 재조회·지터 후 wave 2 한 번(총 최대 8회). 그 외(인증 오류, readback 불일치, 의미 충돌, 병합 오류)는 재호출하지 않고 그대로 올린다. 두 wave 소진 시 예외 대신 `POST_CONFLICT_PENDING`과 증거 문자열을 반환해 다른 Work는 계속 진행한다. 병합이 멱등이라 이미 반영된 상태면 두 번째 PUT 없이 `UNCHANGED`. last-writer-wins·force·무한 재시도 없음.
- **readback 보강:** 쓰기 직후 읽기에서 잠깐 이전 내용이 보이는 현상(이번 세션에서도 관찰된 GitHub의 짧은 read-after-write 지연)에 대비해 readback을 최대 3회 다시 읽는다. 읽을 수조차 없는 내용은 `ReadbackMismatch`로 분류한다(처음 구현은 `ValueError`가 새어 나오는 결함이 있어 시험에서 잡혀 코드를 고쳤다).
- **의미 충돌:** `tracker_merge_strict`는 다른 작성자가 같은 Work의 `phase`/`next_action`을 바꿨고 그 값이 우리 값과도 다르면 `NeedsDecision`으로 멈추고 덮어쓰지 않는다. 같은 값을 이미 쓴 경우는 변경 없음으로 처리.
- **UNCERTAIN 정산(판정서 §5-3 수정):** v1은 처리 키 끝의 정책 리비전을 `|1`로 하드코딩해서 리비전 2의 DB에서는 `NO_JOB_HOLD`를 낸다(시험이 이 결함을 그대로 재현한다). v2는 `(request_id, revision, package sha)`로 모든 정책 리비전의 job을 찾고, **정산하려는 정확한 처리 키**와 영수증·결과의 키가 일치해야만 `SETTLED_BY_EVIDENCE`다. 다른 리비전의 영수증은 `EVIDENCE_MISMATCH_HOLD`, UNCERTAIN이 둘 이상이면 `AMBIGUOUS_POLICY_REVISION_HOLD`. DB는 `mode=ro`, 정산 중 모델 호출 0, DB 해시 불변.
- **시험:** v2 단위 21 passed(2-wave 회복, 8회 상한, 소진 시 PENDING·미기록, 비-stale 오류 재호출 0, readback 지연, 엄격 병합, `gh` 주입 어댑터의 409/422/403/404/대용량 폴백, 정책 리비전 2, 읽기 전용). v1 단위 19 passed 유지.
- **5라운드 시뮬레이션 v2(4회 반복 = 20라운드, 매 라운드 독립 DB·mock GitHub·스킬 저장소):** 20/20 PASS. stale 충돌 4건 회복 20/20, 완전 동시 5창 쓰기 100건 중 **wave 2가 필요했던 것 12건, 전부 회복, `POST_CONFLICT_PENDING` 0**, 쓰기당 총 시도 최대 5(상한 8 이내), 5개 항목 모두 존재·중복 0. 스킬 3건 rebase 16/16(주입한 의미 충돌 4/4는 `NEEDS_DECISION`·저장소 변경 0). UNCERTAIN 정산 읽기 전용 20/20(정책 리비전 1과 2 모두), DB 불변.
- **한계(정직):** 모두 mock Contents API·mock 스킬 저장소·임시 DB 기준이다. 실제 GitHub에서의 CAS **쓰기**는 판정서가 요구한 "유효 승인된 비민감 PRIVATE 테스트 경로"가 지정돼 있지 않아 시행하지 않았다. 실제 스킬 저장소 3-way rebase(줄 단위 병합만 구현, 코드 의미는 이해하지 못함), 실제 호스트 DB 정산도 `NOT_RUN`. 이 mock PASS를 운영 PASS로 승격하지 않는다. 스레드 시험은 확률적이라 4회 반복 결과만 보고한다.

## 3. 산출물 (PRIVATE main `artifacts/v0_2_29/validation/`)

`work_writer_v2/` (`work_writer_v2.py`, `test_work_writer_v2.py`, `five_window_writer_sim_v2.py`, `live_get_check.py`, 시뮬레이션 결과 JSON 4개), `gate/` (`preflight_a.py`, `probe_b_readonly.py`). 기존 v1·v3 검증기·진단 파일은 변경 없음.

## 4. GPT/사용자 판단이 필요한 항목

1. **리뷰 진입 경로(핵심 차단):** 아래 중 하나가 정해져야 유료 리뷰를 시작할 수 있다. 어느 쪽이든 모델 호출 전에 `review_request_gate`·`approve_request.py check` 전체를 다시 통과시킨다.
   - **(가)** 이 v0.2.29 리뷰 한 건에 한해 이미 등록된 `POLICY-STATIC-V1-DESIGN`(USD 3) 수동 승인 경로를 사용하도록 **사용자의 새 명시 승인**을 받는다(이전 V028 리뷰와 같은 방식). 판정서 §4가 금지한 것은 "과거 UI Work용 예외의 소급·우회 사용"이므로, 이번 건에 대한 별도의 명시 승인이 있으면 우회가 아니다. 판정 필요.
   - **(나)** 통합 USD 3 `POLICY-STATIC-V1`과 보호 위임 `max_request_usd` 3 정합화를 `enabled_at` 갱신과 함께 별도 승인한다. 보호 위임 변경이므로 사용자의 해당 수치 변경 승인이 필요하다. 현재 LIVE v0.2.25 엔진은 DESIGN 등급도 자동 승인 대상으로 보므로, 이 방식은 구 DESIGN R1의 소급 승인 위험을 `enabled_at` 갱신에만 의존한다.
2. 실제 CAS 쓰기 시험에 쓸 **비민감 PRIVATE 테스트 경로**를 지정할지(미지정이면 `NOT_RUN` 유지).
3. 실제 스킬 저장소 test worktree/branch를 지정할지(미지정이면 `NOT_RUN` 유지).

## 5. 변경하지 않은 것

watcher ZIP 바이트, 기존 시험, 기존 게시 산출물(v1·v3·진단 파일), LIVE v0.2.25, 위임 USD1, 운영 DB·키·Task·Notifier, 기존 REQUEST·영수증. REQUEST/SOURCE_PIN/서명/READY/모델 호출 0.
