# COWORK-AUTO-APPROVAL-20261115-001 — CURRENT

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
