# COWORK-AUTO-APPROVAL-20261115-001 — CURRENT

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
