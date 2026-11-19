# v0.2.29 사전 검증 — GPT 격리 모델 5회 결과 및 Windows 실제 ZIP 5회 실행 게이트

- 날짜: 2026-11-20 KST
- 기존 Work: `COWORK-AUTO-APPROVAL-20261115-001`
- 후보 ZIP: `artifacts/v0_2_29/skill-collab-watcher_v0_2_29_1120.zip`
- manifest SHA-256: `c67bc342fe77547b000fc42e1b886396cbef035c0d265dbcd124947e267ed83f`
- 크기: 310753 bytes, 114 members (GitHub PRIVATE main 정본/Windows 호스트 보고)
- 범위: **유료 리뷰 전에 격리 시뮬레이션 5회**, 문제 있으면 수정·재시험, 문제 없을 때만 다음 단계. USER 요청 2026-11-20. 기존 ZIP·영수증·원샷 승인 이력 보존.

## 1. GPT가 이 세션에서 실제 수행한 것

1. PRIVATE GitHub `main`의 후보 ZIP을 `fetch_file(encoding=base64)`로 읽고, JS ZIP 중앙 디렉터리와 raw deflate를 해석해 114개 구성 항목과 `auto_approval.py`, `state_store.py`, `auto_policy.py`, `tests/test_v029_cost_refused_exclusion.py`의 관련 코드를 직접 확인.
2. 변경점: `PER_REQUEST_COST` 때 `store.auto_exclude()` 호출, `auto_claims`에 `POLICY_STOPPED` 및 `reserved_cents=0` 영속화, 사용량 SELECT에서 `reserved_cents > 0` 적용, `_resume`의 `POLICY_STOPPED` 종결 처리.
3. Linux/Python 격리 환경에서 **후보 ZIP 모듈 import가 아닌**, 위 신규 SQL INSERT와 상태 전이를 그대로 옮긴 **재구성 모델**을 매회 서로 다른 새 SQLite DB로 5회 실행. 5회 x 5개 검증 범주 = 25개 체크 통과.
4. 각 회차 검증: (a) cap 때문에 거절된 과거 요청이 `enabled_at` 미갱신 상태에서 USD3로 상향돼도 자동 READY 없음, (b) 신규 정상 요청 1회 허용 및 중복 차단, (c) DB 파일 재열기 후 영구 제외 유지, (d) 0-cent 제외 행을 사용량에서 제거, (e) DESIGN 정책·무효 PIN·구 생성시각 요청 차단/중복 제외.
5. 시험 증거: GPT 실행 환경 `cowork_v029_offline_model_5runs_20261120.py`; JSON `cowork_v029_model_5runs_20261120.json` SHA-256 `ab4327cd3a59fd854cb23e7c89145955a81ce6631d98477e063a62755a43daee`. 로컬 파일로만 보존; GitHub에는 요약만 게시. 모델 호출·보호 서명·GitHub REQUEST/READY 게시 0, LIVE 변경 0.

| Run | 격리 SQLite 모델 |
| --- | --- |
| 1 | PASS_MODEL_ONLY (5개 항목) |
| 2 | PASS_MODEL_ONLY (5개 항목) |
| 3 | PASS_MODEL_ONLY (5개 항목) |
| 4 | PASS_MODEL_ONLY (5개 항목) |
| 5 | PASS_MODEL_ONLY (5개 항목) |

**중요한 범위 제한:** 기존 private ZIP의 바이너리는 GitHub connector 안에서 읽고 관련 소스는 추출했지만, 해당 바이너리를 Python 실행 도구로 직접 materialize 할 수 없었음. 따라서 Python 환경에서 *실제 package code*를 로드한 시험은 `NOT_RUN`. 이 GPT 모델의 5회 PASS로 **v0.2.29 실제 ZIP 5회 시험 / Windows 독립 리뷰 / LIVE 게이트 PASS를 주장하지 않는다.**

`SIMULATION_RESULT=PARTIAL_PASS_MODEL_ONLY`; `V029_ZIP_EXECUTION_5X=NOT_RUN`; `INDEPENDENT_REVIEW_V029=NOT_RUN`; `HOST_DEPLOY=HOLD`; `PAID_CALLS_THIS_STEP=0`.

## 2. 남은 한 작업 — Windows Claude Code 실제 ZIP 격리 실행 5회 (자동 리뷰 생성 전)

기존 Windows 호스트 실행 권한/원샷 범위 확인 후, **실제 ZIP을 정확히 하나의 리뷰 대상 바이너리로 고정**하여 검증. 저장소 `wonhwipark/CoWork-Skill-Collab`, branch `main`, 기존 Work `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/`. 원본 ZIP/manifest/diff를 내려받고 SHA-256 `c67bc342fe77547b000fc42e1b886396cbef035c0d265dbcd124947e267ed83f`, 크기 310753, CRC, 114 members, 경로이탈/민감정보 점검을 수행.

**각 회차는 서로 독립된 임시 추출 폴더 + 임시 SQLite DB + 가짜 GitHub transport/signer/runner만 사용. Windows LIVE watcher, 운영 DB/WAL/SHM, 호스트 키/설정, Task/Notifier는 읽기 전용 외 접근 금지. 네트워크/실제 LLM/유료 호출 0.**

매회 실제 ZIP 내부 소스에서 `python -m pytest -q` 전체 테스트와 3개 신규 회귀 테스트를 실행(Windows 자체 보고 기준 기대 1034 PASS / 0 FAIL / 12 SKIP). 다섯 회차에 고유한 안전 시나리오를 각각 추가로 확인:
1. **Run1 cap 소급:** 저가 상한에서 PER_REQUEST_COST→`POLICY_STOPPED` 영속화→USD3 상향, 같은 `enabled_at`, READY/서명/모델 0.
2. **Run2 재시작/중복:** DB 재오픈과 2개 이상의 반복 스캔, `POLICY_STOPPED`/완료/UNCERTAIN 어떤 상태도 재진입·재모델 0.
3. **Run3 정상·정책:** 상향 이후 새 `POLICY-STATIC-V1`은 eligible, 구 `-DESIGN`/`-LARGE`, 범위 밖/무효 PIN/타임스탬프는 fail-closed, 실제 signer 없이 mock 1회.
4. **Run4 경쟁/원자성:** 동시 스캔과 `auto_exclude` vs `auto_claim` 경쟁, SQLite uniqueness/BEGIN IMMEDIATE 및 `reserved_cents=0` 집계 영향. 재현 불가면 NOT_RUN, PASS로 꾸미지 말 것.
5. **Run5 실패 주입/복구:** `auto_exclude` 저장 실패, 승인 서명 직전/후 및 READY 생성 실패, create-only 충돌, watchdog 재시작, 새 cap 후 옛 REQUEST 재평가. **이전 cap 거절이 저장 실패로 누락되었을 때도 소급 실행이 없음을 확인**. 안전을 증명하지 못하면 FAIL/BLOCKED (핵심 위험 경로).

각 회차별 **명시적 PASS/FAIL/SKIP/NOT_RUN**, 실제 실행 명령·환경, ZIP SHA, 테스트 갯수, Mock signer/READY/LLM 카운트, 영수증과 근거를 보존. 5회 모두 실제 ZIP 기준 PASS(보안 예외 중 NOT_RUN 0) 전에는 **리뷰 REQUEST/READY/유료 모델 호출·LIVE 설치/위임 변경 0**. 결함 발견 시 출하 ZIP을 수정하지 말고 새 개발 후보 patch로 보완하고 다섯 회차 처음부터 재확인. 이 범위를 넘는 기능 확장 금지.

## 3. 5회 실제 검증 PASS 이후 단계
- 원샷의 다음 단계에 진입하되, 새 유료 독립 리뷰(최대 USD3)는 **현재 유효한 명시 승인 및 호스트 서명 범위**를 먼저 확인. 승인 없거나 범위 미확인이면 `REVIEW_REQUEST=BLOCKED_APPROVAL`, 모델 0. 유료 모델 호출을 시뮬레이션의 자동 후속 트리거로 만들지 않음.
- 승인·정본 해시·REQUEST/READY·중복·비용 preflight가 모두 유효한 경우에만 별도 정식 R1 **1회**, 기존 review `REQ-COWORK-V028-AUTO-REVIEW-R1-20261120` 절대 재실행/재큐잉 금지.
- 독립 리뷰 실제 PASS + 호스트 보호 설치 승인, rollback, single provider, legacy 소급 배제, SHADOW 검증 확인 후에만 LIVE 설치/USD3 변경. 리뷰 FAIL이면 기존 v0.2.25·위임 USD1 유지.
- 결과를 기존 Work의 `CURRENT.md`와 `TRACKER.json`에 필요한 현행 요약만 반영하고 회차별 상세 결과를 본 Work 안의 1개 추가 결과 문서에 기록. PRIVATE main commit 및 원격 bytes 검증. PUBLIC·업무 호스트 전달·유료 smoke 없음.

**NEXT_ONE_ACTION:** Windows Claude Code가 위의 실제 ZIP 5회 격리 시뮬레이션부터 실행하여 결과를 정본에 게시. GPT는 그 결과를 판정하여 다음 단계로 진행할지 결정.
