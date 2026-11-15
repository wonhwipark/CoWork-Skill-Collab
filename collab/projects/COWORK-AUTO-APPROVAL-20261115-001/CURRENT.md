# COWORK-AUTO-APPROVAL-20261115-001 — CURRENT

## 새 요청: 비판적 평가 기준을 실제 Claude 자동 리뷰에 반영·검증 (2026-11-16 KST)

- **사용자 최신 지시:** 강화된 독립 리뷰 R0~R3의 비판적 검토·수정안/구조 대안 평가를 **자동 리뷰 경로에서 실제로 적용하고 시험하는 작업까지 요청**.
- **GPT 작업 요청서 PRIVATE 게시·재조회 PASS:** [GPT_CRITICAL_REVIEW_AUTO_APPLY_AND_TEST_REQUEST_r0001_20261116.md](GPT_CRITICAL_REVIEW_AUTO_APPLY_AND_TEST_REQUEST_r0001_20261116.md), 기준 계약 `collab/ops/CONTRACTS/REVIEW_TIER_TOKEN_BUDGET_V1.md` §2.1 (commit `1b7ab2175da7bace4d9dced5e01c31087a2bfe73`). 실제 Windows review prompt-builder/REQUEST 본문 전달 지점을 먼저 확인하고 `REUSE→CONNECT→최소 EXTEND`, 결함 강제 0·근거 중심 검토·결함/개선 제안 구분·최소 수정안과 구조 대안의 비용 비교 등을 신규 요청에 반영하고 가짜 runner의 **모델 호출 0** 시험으로 입증하도록 인계.
- **경계:** 위 문서는 Windows 자동 실행 신호가 아니므로 `AUTO_REVIEW_APPLY_REQUEST=POSTED`, `WINDOWS_APPLY_EXECUTION=NOT_RUN`, `PROMPT_INJECTION_TEST=NOT_RUN`. 실행한 호스트 결과가 오기 전 적용 완료라고 표기하지 않음.
- **기존 동결 R2 유지:** `REQ-COWORK-AUTO-APPROVAL-V023-R2-20261115`의 원본 REQUEST/ZIP/SOURCE_PIN, 최대 `POLICY-STATIC-V1-LARGE` USD $3·1회는 불변. 금회 GitHub 최신 조회 시 `APPROVAL_SIG/READY/DISPATCH/RESULT/RECEIPT=NOT_FOUND` / `INDEPENDENT_REVIEW=NOT_RUN` / `AUTO_SIGNING=OFF`(호스트 직접 상태는 별도). 이번 요청으로 새 유료 리뷰·중복 R2/READY 생성하지 않음.
- **NEXT_ONE_ACTION:** Windows Claude Code가 요청서의 단일 실행 프롬프트로 기존 프롬프트 결합 경로와 실제 런타임 반영을 점검하고 격리 dry-run·negative test 후 `CLAUDE_CRITICAL_REVIEW_AUTO_APPLY_VALIDATION_FOR_GPT_20261116.md` 결과/증거와 `CURRENT.md`·`TRACKER.json`을 PRIVATE main에 게시·원격 확인. 유효한 보호 자동 위임·리뷰 요청이 실제 활성화되기 전 모델 호출 0. 기존 R2 상태가 먼저 변경되면 결과/영수증 우선 확인 후 중복 금지.

## R2 v0.2.23 공식 REQUEST·ZIP·SOURCE_PIN 게시 완료, 호스트 처리 대기 (2026-11-15 KST)

- **사용자 최신 실행 지시:** “그래 자동승인까지 진행해줘” — 기존 통합 R2 1회/최대 $3, 승인된 보호 Windows 사전 위임 범위, 독립 리뷰+GPT PASS 조건부 운영 활성화에 대한 진행 의사 확인. 새 대상은 **v0.2.23**(원래 v0.2.22에서 접두사 호환성만 보완, GPT 정적 PASS).
- **GPT 직접 게시·원격 readback PASS:** 신규 정식 R2 `collab/requests/REQ-COWORK-AUTO-APPROVAL-V023-R2-20261115/REQUEST.md`와 원본 ZIP `collab/packages/skill-collab-watcher_v0_2_23_1115_DEV_NOT_FOR_DEPLOYMENT.zip` 및 승인 범위 참고 `OWNER_SCOPE_RECORD.md`를 **Commit A `8c90827ea6f0771331937d81c719697b322d4039`**에 함께 저장. ZIP은 기존 Git blob `0d7001798d402e5545833e6aaf8c5f4b9d2b8fbf` 그대로 복사, **282340 B, SHA-256 `f941be8a6b53d00baa10a9b097f234b159470e2aa1242ecc33bcf0bdee080ea7`**(이전 직접 검증과 동일). REQUEST `SKILL_COLLAB_REVIEW_REQUEST_V1`/`SUBMITTED`/`POLICY-STATIC-V1-LARGE`/max $3×1, knowledge_refs 3개 각각 원시 SHA-256 확인.
- **SOURCE_PIN:** `collab/requests/REQ-COWORK-AUTO-APPROVAL-V023-R2-20261115/SOURCE_PIN.json` **Commit B `e0e144cc56215b9d5d95cab77714186db6bf6662`**, `source_commit=8c90827e…` / `repo_id=1451933830` / `SKILL_COLLAB_SOURCE_PIN_V1`, 원격 readback PASS.
- **호스트 원샷 정본:** [GPT_R2_V023_HOST_ONE_SHOT_AND_LIVE_GATE_r0001_20261115.md](GPT_R2_V023_HOST_ONE_SHOT_AND_LIVE_GATE_r0001_20261115.md), commit `49caa963cbad9106874b70ba416a72ea964f7c41`, remote readback PASS. 현재 운영 v0.2.20은 READY 없이 REQUEST만으로 모델 호출 불가. 현재 이 채팅의 GitHub 도구는 Windows 호스트 작업/키/프로세스를 직접 실행할 수 없어 **R2 모델/READY/조건부 설치를 실제로 실행했다고 보고하지 않음**.
- **직접 원격 상태 조회:** `REQUEST=POSTED`, `ZIP=POSTED`, `SOURCE_PIN=POSTED`, `APPROVAL_SIG=NOT_POSTED`, `READY=NOT_POSTED`, `DISPATCH/REVIEW_RESULT/RECEIPT=NOT_POSTED`. 따라서 `INDEPENDENT_REVIEW=NOT_RUN`, `AUTO_SIGNING=OFF`, `OPERATING_GITHUB_LIVE=v0.2.20_UNCHANGED`, `NEW_PAID_CALLS_THIS_REQUEST=0`.
- **NEXT_ONE_ACTION:** 실제 Windows 실행 주체가 위 ONE_SHOT 문서로 기존 호스트 검증 절차를 마치고 유효한 READY LAST → 승인된 R2 1회/영수증을 게시하도록 연결. GPT는 R2 검증·판정 후 **차단 결함 0 및 동일 바이트 PASS** 조건으로 앞서 승인된 v0.2.23 설치/30일 보호 위임 자동 승인 LIVE 적용 검증 진행. 이전 요청/승인 반복 금지. 신뢰된 승인 수단 미확인/한도 초과는 `BLOCKED`, 모델 호출 0.

## GPT v0.2.23 최종 정적 PASS — R2 대상 변경 확인만 대기 (2026-11-15 KST)

- **GPT 결정:** [GPT_V0223_PREFIX_COMPAT_FINAL_DISPOSITION_r0001_20261115.md](GPT_V0223_PREFIX_COMPAT_FINAL_DISPOSITION_r0001_20261115.md), commit `d4ad638fc6af0151166cf466601fc1620c91b9d3`, remote readback PASS. `PASS_FOR_INDEPENDENT_R2_CANDIDATE_ONLY`. 운영 배포 PASS/독립 리뷰 PASS 아님.
- **규칙 판단:** `_FAMILY.fullmatch` 정규식 `[A-Za-z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)*-`, 최소 7자. 보호된 로컬 위임의 owner-listed `COWORK-`(7자)와 `L1-WORKSPACE-`만 자동 프로젝트 가족으로 인정 가능하며 7자 하한 자체는 실행 권한이 아님. 스킬 exact allowlist/비용·중복·서명·READY 조건 불변. v0.2.22가 승인 입력을 거절했던 호환성 문제 수정 수용.
- **GPT 원격 ZIP 실제 bytes 직접 검증 PASS:** `artifacts/v0_2_23/skill-collab-watcher_v0_2_23_1115_DEV_NOT_FOR_DEPLOYMENT.zip` 282340 B, SHA-256 `f941be8a6b53d00baa10a9b097f234b159470e2aa1242ecc33bcf0bdee080ea7`, ZIP central-directory 102개, Git blob `0d7001798d402e5545833e6aaf8c5f4b9d2b8fbf`; diff 직접 검토. ZIP full CRC/Windows 실측은 호스트 보고 구분.
- **Windows 자체시험:** 구 v0.2.22에 신규 회귀 적용 시 5 FAIL/19 PASS, v0.2.23은 890 PASS/12 SKIP Windows venv+운영 Python 3.11.9 각, 격리 SHADOW 8/8, rollback PASS(호스트 자체 보고). `INDEPENDENT_R2=NOT_RUN`, `REAL_KEY_SIGNING=0`, `READY=NOT_POSTED`, `NEW_PAID_CALLS=0`, `AUTO_SIGNING=OFF`. 기존 GitHub LIVE v0.2.20 변경 없음.
- **변경점 확인만 대기:** 앞선 통합 사용자 승인은 R2 LARGE 최대 $3/1회, 지정 위임 범위/한도/30일 및 리뷰 PASS 조건부 설치까지 확보했으나 **R2 동결 ZIP은 v0.2.22**였음. v0.2.23 SHA `f941be8a…80ea7`로 **리뷰 입력만 바꾸는 것**에 대한 좁은 사용자 확인 후 R2 정식 신규 REQUEST/고정 ZIP/Commit A/SOURCE_PIN → Windows 기존 signer/READY LAST → 독립 리뷰/영수증→GPT 판정. 승인 범위 전체 반복 요청·추가 비용·모델 재호출 금지.
- **NEXT_ONE_ACTION:** 사용자에게 **v0.2.23 바이트에 한하여 기존 $3/1회 R2 적용 가능 여부**만 확인. 변경 승인 전 모델 0, 서명 0, READY 0.

## 승인 접두사 호환성 수정 완료: 후보 v0.2.23 (COWORK-/L1-WORKSPACE- 승인 범위 통과, 옛 후보 거부 재현, 자체시험 890/890, 독립 R2 NOT_RUN, 운영 불변) (Claude 호스트 보고, 2026-11-15 KST)
- 결과: `CLAUDE_V0222_APPROVED_PREFIX_COMPAT_FIX_RESULT_FOR_GPT_20261115.md` (PRIVATE `main`, commit `30e6b7fed42a886fb8f8e3bd10ba671683209c61`, 원격 바이트·SHA-256 `bb4c71d40c2b6064ba48e2df663a18be3350a6db6ca7e0d95e9019eb5a0220a9` 일치).
- 원인: v0.2.22 접두사 최소 길이 8자 → 승인된 `COWORK-`(7자) 거부로 위임 전체 로드 실패. 수정: 영숫자 단어와 `-`로 끝나는 접두사, 최소 7자, 와일드카드·공백·구분자 없는 단어 거부. 매칭·스킬 정확 일치는 불변.
- 시험: 신규 승인 범위 시험을 옛 후보 v0.2.22에서 실행 → 5건 실패(재현), 거절 시험 19건 통과. 수정본 v0.2.23 전부 통과, 전체 회귀 시험 venv·운영 인터프리터 각 890 passed/12 skipped, SHADOW 8/8, 롤백 리허설 ALL_PASS, 운영 DB·키·설치 트리 불변.
- 후보 `skill-collab-watcher_v0_2_23_1115_DEV_NOT_FOR_DEPLOYMENT.zip` 282340 B, sha256 `f941be8a6b53d00baa10a9b097f234b159470e2aa1242ecc33bcf0bdee080ea7`, PRIVATE `artifacts/v0_2_23/`에 ZIP·diff·매니페스트 게시(원격 바이트 일치, 요청·READY 없음). 독립 리뷰 NOT_RUN.
- 미실행: 독립 R2, 실제 서명, APPROVAL_SIG·READY 게시, 위임 활성화, 운영 설치, Notifier 추가. 유료 모델 0.
- 다음 한 동작: GPT 최종 판정. PASS 이후에만 독립 R2 1회(USD 3) 실행.

## 사용자 통합 승인 확보 / v0.2.22 승인 범위 접두사 호환성 수정 대기 — 2026-11-15 KST

- **현재 사용자 승인 기록:** [GPT_R2_APPROVAL_AND_V0222_SCOPE_FIX_GATE_r0001_20261115.md](GPT_R2_APPROVAL_AND_V0222_SCOPE_FIX_GATE_r0001_20261115.md), commit `9fafb272864d7b9570650995db27e81675154f35`, 원격 readback PASS. 사용자 “그래”는 이전 [통합 제안](GPT_V0222_DISPOSITION_AND_COMBINED_APPROVAL_GATE_r0001_20261115.md)의 **v0.2.22 독립 R2 LARGE 최대 $3/1회**, 보호 로컬 위임 project families `COWORK-`·`L1-WORKSPACE-`, 3개 exact skill, STATIC-V1 $1/요청, 2회/$3/일, $10/월, 30일 위임, R2 독립 PASS·GPT 판정 **조건부** Windows 설치/자동서명 활성화를 통합 승인한 것으로 기록. 서명/READY/유료 호출은 아직 없음.
- **새로 확인된 blocker:** v0.2.22 `auto_approval.py::_families`가 project family `len(x)>=8`을 필수로 요구하지만 승인된 `COWORK-` 길이는 **7**. 그대로 설치하면 보호 정책이 `POLICY_UNREADABLE`로 거부. `L1-WORKSPACE-`는 규칙 통과. 기존 M2 시험에 실제 승인 접두사 반례가 빠졌음. 운영 활성화/유료 R2 선행 시 비용 낭비 가능.
- **판정:** `APPROVAL_RECORDED`, `V0222_SCOPE_COMPAT=FAIL`, `R2_1CALL_USD3=APPROVED_FOR_ORIGINAL_V0222_NOT_SPENT`, `R2_REQUEST=NOT_POSTED`, `R2_READY=NOT_POSTED`, `REVIEW=NOT_RUN`, `AUTO_SIGNING=OFF`, `OPERATING=v0.2.20_GITHUB_LIVE_UNCHANGED`. 승인받지 않은 새로운 후보 바이트에 원래 R2 비용 승인을 자동 이전하지 않음.
- **NEXT_ONE_ACTION:** Windows Claude Code에 위 문서 **§3 한 번** 인계 → 격리 v0.2.22 복사본에서 정확 `COWORK-` 짧은 접두사 호환성만 안전하게 수정·구버전 FAIL/신본 PASS 회귀 및 전체 Windows 시험/SHADOW/rollback → 고유 v0.2.23 DEV ZIP/실 SHA/CRC·PRIVATE 결과 `CLAUDE_V0222_APPROVED_PREFIX_COMPAT_FIX_RESULT_FOR_GPT_20261115.md` 게시·원격 readback. 설치/실키/REQUEST/READY/유료 호출 0. 이후 GPT가 변경 입력만 좁게 사용자 확정하고 기존 1회 독립 R2와 조건부 LIVE 적용을 이어감.

## GPT v0.2.22 직접 재해시·정적 판정 — 독립 R2 및 위임 범위 사용자 통합 승인 대기 (2026-11-15 KST)

- **GPT 판정 정본:** [GPT_V0222_DISPOSITION_AND_COMBINED_APPROVAL_GATE_r0001_20261115.md](GPT_V0222_DISPOSITION_AND_COMBINED_APPROVAL_GATE_r0001_20261115.md); commit `f3bf1f1e691540c6f4dfec2598d962790c9e39c7`, 원격 본문 readback PASS.
- **판정 `ACCEPT_V0222_FOR_INDEPENDENT_REVIEW_ONLY`:** B1 합집합 비용/횟수, B2 보호 위임 scope 재검증, M1 in-process double signer 경쟁 방지, M2 프로젝트 family를 새 `diff_v0_2_21_to_v0_2_22.patch`로 직접 대조. Windows Claude Code 최종 ZIP 자체시험 `866 passed/12 skipped` 두 Python 환경, 격리 SHADOW 8/8, 구후보 FAIL→신후보 PASS, 운영 원본 불변은 Windows 호스트 보고이며 독립 PASS가 아님.
- **GPT GitHub ZIP 실제 bytes 검증 PASS:** `artifacts/v0_2_22/skill-collab-watcher_v0_2_22_1115_DEV_NOT_FOR_DEPLOYMENT.zip` 280313 B, 101 entries, SHA-256 `1b67de37891cb7fdbae721b9424e312d1cc5b8c68e06e69357555a556d27bd87`, Git blob `caa55e965df2a42693a06cee44e17e2e1cb879e5`. 전체 ZIP CRC는 Windows 호스트 증거, GPT는 미실행.
- **다음 게이트:** 신규 v0.2.22 독립 Claude R2 **`POLICY-STATIC-V1-LARGE` 최대 $3 1회**, **아직 사용자 승인/REQUEST/READY/모델 호출 없음**. 단일 통합 승인안: 기존 LIVE v0.2.20 보존, 보호 로컬 사전 위임 `COWORK-`·`L1-WORKSPACE-` family + 3개 실제 skill exact, `POLICY-STATIC-V1`만 요청당 1회/$1, 일 2회/$3, 월 $10, 30일 만료, 소급 요청 불허. R2 BLOCKING=0 등 GPT 판정 PASS **조건부** 운영 설치/auto signer 활성화·Notifier 이벤트 연결/검증/롤백 승인 제안. 아직 모든 값 `NOT_APPROVED`.
- **실제 운영 상태:** `ACTIVE_PROVIDER=GITHUB`, `OPERATING_VERSION=v0.2.20`(Windows 보고), `AUTO_SIGNING=OFF`, `INDEPENDENT_REVIEW=NOT_RUN`, `NEW_PAID_MODEL_CALLS=0`, `V0222_INSTALL=NOT_RUN`. 현재 대기 Work→Knowledge·dashboard REQUEST는 소급 자동 디스패치 0 유지.
- **NEXT_ONE_ACTION:** 위 문서의 비용/R2·범위·조건부 운영 승인에 대한 사용자 한 번의 명시 응답을 받기. 승인 뒤 신규 R2 패키지 SHA/원격 요청 고정 → Windows 기존 signer/READY LAST→LIVE watcher 독립 리뷰 1회·receipt→GPT 판정. PASS면 허용된 Windows 적용·검증으로 한 번에 마무리. 실패/승인 초과는 fail-closed/모델 재호출 0.

## v0.2.21 GPT 정적 판정 수정 완료: 후보 v0.2.22 (B1·B2·M1·M2, 자체시험 866/866, 독립리뷰 NOT_RUN, 운영 불변) (Claude 호스트 보고, 2026-11-15 KST)
- 결과: `CLAUDE_V0221_GPT_FINDINGS_FIX_RESULT_FOR_GPT_20261115.md` (PRIVATE `main`, commit `6f448b63e607c9ba951f2b5ea09043217de5f6a3`, 원격 바이트·SHA-256 `4413787701b1997ace8d7e4e0064665f95e340159bc19f9530209f53d2a18f20` 일치).
- B1: 자동 예약과 워처 디스패치를 요청 신원 단위 합집합(중복 1회, 비용은 큰 값, 합산)으로 예약 트랜잭션 안에서 집계. 옛 후보는 max() 때문에 세 번째 요청 통과(실패 재현). B2: 서명·승인 게시·READY 게시 직전마다 현재 보호 위임으로 저장 후보 재판정, 축소 시 POLICY_STOPPED(서명·READY·모델 0). 옛 후보 25건 실패.
- M1(간헐 실패)은 시험 타이밍이 아니라 실제 결함: 같은 프로세스의 두 호출이 예약 후 서명 전 단계를 죽은 시도로 오인해 두 번 서명. 옛 후보 12회 중 3회 재현, 수정본 12/12 통과, 프로세스 내 진행 중 가드 추가.
- M2: 정확 프로젝트 외에 끝이 '-'인 가족 접두사 허용(와일드카드 불가, 스킬은 정확 일치, 두 프로젝트 ID 명시 거절). 실제 REQUEST V1은 project_id·work_id가 항상 같음. 범위 확정은 사용자 승인 전이라 미적용.
- 검증: 최종 ZIP 트리에서 시험 venv·운영 인터프리터 각 866 passed/12 skipped(기준선 v0.2.20 674/12), SHADOW 8/8, 롤백 리허설 ALL_PASS, 운영 DB·키·Task·설치 트리 불변. 변이 시험은 v0.2.22에서 재실행하지 않음.
- 후보 `skill-collab-watcher_v0_2_22_1115_DEV_NOT_FOR_DEPLOYMENT.zip` 280313 B, sha256 `1b67de37891cb7fdbae721b9424e312d1cc5b8c68e06e69357555a556d27bd87`, PRIVATE `artifacts/v0_2_22/`에 ZIP·diff·매니페스트 게시(원격 바이트 일치, 요청·READY 없음).
- 미실행/미승인: 독립 리뷰(R2/LARGE $3 1회), 위임 범위 1회 확정, 운영 설치·Notifier 이벤트 추가·활성화. AUTO_SIGNING=OFF, 유료 모델 0, 실서명 0, READY 0.
- 다음 한 동작: GPT 단일 판정과 리뷰·범위 승인 요청 묶음.

## GPT 정적 판정 — v0.2.21 후보 보완 후 독립 리뷰 (2026-11-15 KST)

- **최신 GPT 판정 정본:** [GPT_V0221_STATIC_DISPOSITION_AND_SINGLE_FIX_HANDOFF_r0001_20261115.md](GPT_V0221_STATIC_DISPOSITION_AND_SINGLE_FIX_HANDOFF_r0001_20261115.md), GitHub PRIVATE main commit `5608dec4072710846b6331ecd48f22029914a7ea`, remote readback PASS. `GPT_DISPOSITION=REVISE_BEFORE_INDEPENDENT_REVIEW` / `BLOCKING=2` / `MAJOR=2`.
- **GPT 원격 ZIP 재해시 확인:** v0.2.21 dev 후보 실제 raw bytes 272839, SHA-256 `16921bf4021714345cabc78de5e2e8a6882891615f90b5747622570ca4465d8b` = Windows 보고 일치. Full CRC/Windows 실행은 호스트 자체보고로 구분. 기존 817 PASS/12 SKIP, SHADOW 8/8은 `SELF_TEST_REPORTED`.
- **B1 BLOCKING:** 자동 서명 예약과 기존 별도 수동 리뷰 dispatch를 `max(counts)`로 합치면 서로 다른 예약·실행이 과소 집계됨(예: 자동 예약 A1 + 수동 실행 B1 + 추가 자동 C1 → day 2 한도인데 3건 허용 가능). 기존 watcher 최종 집행이 실제 과금 초과를 허용했다는 뜻은 아님. identity 기반 union 집계/원자 한도 회귀 필요.
- **B2 BLOCKING:** 위임 로컬 정책을 서명/READY 이전에 축소해도 `_still_allowed`는 enabled/expiry/repo만 재검증하고 project/skill/limit 축소를 놓침. 재검증/claim 정책 결속 및 revoke crash 회귀 필요.
- **M1 MAJOR:** 최초 ZIP 추출 회귀 1 FAIL 원인·테스트 이름 미확인, 이후 반복 전부 PASS; 재현·증거 확보. **M2 MAJOR:** 정확 project/skill allowlist와 project_id≠work_id 처리가 신규 Work 무인 자동 리뷰 목표에 맞는지 기존 계약과 대조. 무제한 자동 범위 도입 금지.
- **실제 단계:** `DEVELOPMENT=v0.2.21_COMPLETED_CANDIDATE`, `GPT_STATIC_REVIEW=FAIL_BLOCKING_2`, `INDEPENDENT_REVIEW=NOT_RUN`, `OPERATING_DEPLOYMENT=NOT_RUN`, `AUTO_SIGNING=OFF`, `EXISTING_GITHUB_LIVE=v0.2.20_UNCHANGED`, `NEW_PAID_MODEL_CALLS=0`. 기존 후보·설치·원본 보존, 비용과 실운영 자동위임 승인 없음.
- **NEXT_ONE_ACTION:** Windows Claude Code가 위 판정 정본의 마지막 원샷 지시로 B1/B2 재현·수정·전체 회귀/격리 SHADOW·rollback, M1/M2 판단, 새 dev ZIP/SHA/CRC 및 `CLAUDE_V0221_GPT_FINDINGS_FIX_RESULT_FOR_GPT_20261115.md`를 PRIVATE 게시·원격 readback. 사용자 중간 질문/새 유료 모델 호출 없음. 그 후 GPT가 재판정하고 독립 R2(권고 LARGE $3/1회)와 제한적 사전 위임·운영 적용 범위를 묶어 **별도 명시 승인**을 요청.

## Windows 원샷 완료: 자동 서명·READY 후보 v0.2.21 개발·시험·후보 고정 (Claude 호스트 보고, 2026-11-15 KST) — AUTO_SIGNING=OFF 유지
- 결과: `CLAUDE_AUTO_APPROVAL_ONE_SHOT_RESULT_FOR_GPT_20261115.md` (PRIVATE `main`, commit `c99d49e8b15c73ea312364548cf5213a59c1874e`, 원격 바이트·SHA-256 `76bb3c16360a6993339d78380f0bfa84435ea4d3c7c34028e2e262cb323627e7` 일치). 운영 감시기·DB·Task·Notifier·키 **불변**, 실제 서명 0, READY 게시 0, 유료 모델 호출 0.
- 후보 `skill-collab-watcher_v0_2_21_1115_DEV_NOT_FOR_DEPLOYMENT.zip` 272839 B, sha256 `16921bf4021714345cabc78de5e2e8a6882891615f90b5747622570ca4465d8b`(재빌드 바이트 동일, CRC OK, 비밀 스캔 0). PRIVATE `artifacts/v0_2_21/`에 ZIP·diff·매니페스트 게시(원격 바이트 일치, 요청·READY 없음). 독립 리뷰 **NOT_RUN**.
- 시험(자체): GPT 25건 원본 Windows 3.11.9에서 25/25, 최종 ZIP 전체 회귀 시험 venv·운영 인터프리터 각 817 passed/12 skipped(v0.2.20 기준 674/12, 신규 143), 격리 SHADOW(실제 CLI 별도 프로세스, 가짜 GitHub·계수 스텁·일회용 키) 8/8, 변이 시험 16/17(생존 1건은 동등 변이), 격리 설치·롤백 리허설 PASS. 간헐 실패 1건은 원인 미규명(이후 반복 전부 통과).
- 호스트 읽기 전용 실측: 운영 신뢰 루트 로드·키 ACTIVE 신뢰·DPAPI 복호화 메모리 확인(서명 안 함), 승인 키 파일 ACL(Win32 DACL) 광범위 쓰기 없음, 감시기 프로세스 계정=키 소유자(서명 경로 가능).
- 설계 한계: 서명 능력이 GitHub 입력을 읽는 감시기 프로세스 안에 있음(방어=위임 게이트+fail-closed 순서, 피해 상한 요청당 $1·일 2회·월 $10), commit 시각 위조 가능성(첫 관측 플래그가 2차 방어), GPT 핀 없으면 `PIN_MISSING`.
- 미승인/NOT_RUN: 독립 리뷰(권고 R2/LARGE, $3, 1회), 사용자 위임 범위 1회 확정(허용 Work/skill, 월 $10·30일은 제안값), 운영 설치·Notifier 이벤트 목록 추가·활성화. 현재 대기 요청(Work→Knowledge, 대시보드)은 소급 자동 실행되지 않음(시험 입증).
- 다음 한 동작: GPT가 독립 리뷰 요청과 위임 범위 확정을 한 번에 묶어 사용자에게 제시.

## 최신 실행 상태 — 2026-11-15 KST (GPT 설계·격리시험·원샷 준비 완료)

- **Work:** GPT→GitHub PRIVATE REQUEST 게시 후 Windows 기존 signer의 **제한적 사전 위임 정책**에 따른 자동 승인·`APPROVAL_SIG` 생성·`READY` 마지막 게시. 기존 단일 GitHub LIVE watcher의 독립 Claude 리뷰 1회/영수증/Notifier는 유지. 정상 요청 시 Telegram 추가 승인 버튼/Windows Claude Code 수동 서명 **불필요**하도록 개선.
- **기존 운영은 그대로 LIVE:** 별도 CoWork GitHub 이관 [CURRENT](../COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md) 최상단 `ACTIVE_PROVIDER=GITHUB / CUTOVER=LIVE / v0.2.20`(Windows 호스트 보고·GPT 리뷰/receipt 재조회). 이번 변경으로 provider를 전환하지 않으며 `AUTO_SIGNING=OFF`. 기존 30초 Task·Notifier·DB/키/토큰·레거시 pending 1건 불변.
- **설계 정본:** [AUTOMATIC_SIGNING_MINIMAL_DESIGN_r0001_20261115.md](AUTOMATIC_SIGNING_MINIMAL_DESIGN_r0001_20261115.md), 최종 content commit `9addbb03b2c1a77c65434c135ce243dbc8f2110d`, remote readback PASS. 기존 [Telegram 1탭 대안](../COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_APPROVAL_BRIDGE_MINIMAL_DESIGN_r0001_20261115.md)은 **채택하지 않은 이전 설계**로 보존. GitHub 문구만으로 유료 리뷰 권한을 입증할 수 있다는 주장 금지: 운영 Windows의 보호된 사용자 위임 정책이 승인 근거.
- **GPT 실제 구현 참고:** [prototype/auto_policy.py](prototype/auto_policy.py) Python 순수 함수(3451 B, SHA256 `26cfe6abe6d74361c0d64270cc3c6ca9f1e0da5f3761814df4fea2ca73ac333c`), [prototype/test_auto_policy.py](prototype/test_auto_policy.py) (4291 B, SHA256 `64f816b111c169cc1460a03c48d291b6b8e9b88dd51be50c1d1bd59be53d3c87`). 원격 Git blob이 실제 합성 실행 파일과 일치. 코드는 운영 signer/DB 접근이 없는 **예제**; 그대로 설치 금지.
- **시험:** [GPT_AUTO_APPROVAL_PROTO_TEST_RESULT_r0001_20261115.md](GPT_AUTO_APPROVAL_PROTO_TEST_RESULT_r0001_20261115.md) `Python unittest 25 PASS / 0 FAIL / 0 SKIP` (Linux 격리, GitHub/Windows/서명/Claude 모델 호출 0). `WINDOWS_REAL_CODE_INTEGRATION=NOT_RUN`, `FULL_V0220_REGRESSION=NOT_RUN`, `SHADOW=NOT_RUN`, `ROLLBACK=NOT_RUN`, `INDEPENDENT_REVIEW=NOT_RUN`, `OPERATING_APPLIED=NOT_RUN`.
- **정확한 Windows 단일 실행 인계:** [WINDOWS_ONE_SHOT_DEVELOP_TEST_CANDIDATE_HANDOFF_r0001_20261115.md](WINDOWS_ONE_SHOT_DEVELOP_TEST_CANDIDATE_HANDOFF_r0001_20261115.md) commit `60d44ca5796bdde7b8c2c612d4beb2e47a5c55a6`, remote readback PASS. Windows Claude Code 1회: 실제 Windows v0.2.20 signer/Watcher 소스·Task 계정/ACL·원장 조사 → 격리 최소 구현 → 기존 전체 회귀+오류/중복/crash 시험 → fake SHADOW → DEV 후보 ZIP/SHA/CRC/rollback → PRIVATE 결과·CURRENT/TRACKER 직접 게시·remote readback. 중간 승인 없이 개발 범위 내에서 결함 수정·재시험.
- **현재 승인 경계:** 사용자 최신 지시는 빠른 협업 개선을 위한 **워크플로우 준비/격리 개발·시험 수행**. 자동위임 정책의 정확한 허용 project/skill·월 한도·만료는 아직 사용자 정식 1회 확정 전. 추천 초안 `POLICY-STATIC-V1, request <=$1, day <=2 calls/$3, month <=$10, 30-day expiry`는 **승인된 운영 값 아님**. 실제 Windows 운영 Task/DB/키/코드 설치, AUTO_SIGNING LIVE 활성화, 신규 유료 독립 리뷰, PUBLIC 배포는 **NOT_AUTHORIZED/NOT_RUN**. 기존 특정 요청(Work→Knowledge) $1 승인을 포괄 위임으로 재사용하지 않음.
- **독립 리뷰/배포 분리:** 개발자 자체시험은 독립 Claude 리뷰가 아님; 실제 유료 리뷰 호출은 새 요청/서명/사용자 비용 승인 계약에 따라 별도. 후보는 `development_not_for_deployment` 유지. 이후 후보 증거가 확보되면 GPT가 보완·비용/위임 범위·운영 승인 요청을 **한 번에 묶어서** 다음 LIVE 활성화 최종 게이트 판정.
- **Windows 결과 예상 정확 경로:** `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/CLAUDE_AUTO_APPROVAL_ONE_SHOT_RESULT_FOR_GPT_20261115.md`.
- **다음 한 동작:** Windows Claude Code에 위 인계서를 **한 번** 전달해 무비용 격리 구현·시험·후보·원격 재검증까지 진행. GitHub 문서 게시 자체로 Windows 자동 실행 시작되지 않음. 사용자에게 매 시험 단계마다 재요청·반복 승인 요구 금지.

## 결과 판정 분리

| 영역 | 상태 |
|---|---|
| 기존 GitHub REVIEW PROVIDER LIVE | `PASS_HOST_REPORTED / UNCHANGED` |
| AUTO_SIGNING 설계·GPT prototype | `PREPARED / 25 PASS` |
| Windows 실제 signer/Watcher 구현·시험 | `NOT_RUN` |
| 독립 리뷰 | `NOT_RUN` |
| 위임 정책 사전 승인 / 운영 적용 | `NOT_APPROVED / NOT_RUN` |
| 기존 유료 모델 신규 호출 | `0` |
