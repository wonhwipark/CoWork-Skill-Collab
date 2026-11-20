# CoWork 승인 간소화 + v0.2.29 독립 리뷰 R1 — 1~3단계 통합 원샷

- 날짜: 2026-11-20 KST
- 정본: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`
- 기존 Work: `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/CURRENT.md`
- 이 문서 역할: **한 번의 Windows Claude Code 실행 지시**. 원샷 계획·실행 경계·사후 판정 근거. GitHub 문서 게시 자체는 보호 서명, 유료 호출 또는 Windows 실행 승인이 아님.
- 사용자 최신 지시: 간소화 설계(구 1단계), v0.2.29 한 건 정책 차단 해소(구 2단계), 독립 리뷰 1회(구 3단계)를 **중간 사용자 확인 없이 1개 작업으로 합침**.
- 목표 리뷰 ID(기존 없음을 PRIVATE main에서 2026-11-20 KST 확인): `REQ-COWORK-V029-ONEOFF-R1-20261120`, revision `1`. 호스트 재시작 시 원격·DB·영수증부터 재조회하고 중복 ID 충돌 시 자동 재큐잉/재호출 금지.
- 고정 입력: `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/artifacts/v0_2_29/skill-collab-watcher_v0_2_29_1120.zip`, 정확히 **310753 bytes**, **SHA-256 `c67bc342fe77547b000fc42e1b886396cbef035c0d265dbcd124947e267ed83f`**. 개발후보 원본 바이트 변경 금지.
- 비용: **이번 R1 1건/모델 호출 최대 1회/수동 경로 한정 요청 예산 USD3.00**. 상한 인자는 실제 청구액 절대 보장 아님. 이 1건을 넘어 자동 유료 재리뷰/유료 smoke/추가 agent 호출 금지.
- 호스트 마지막 확인: LIVE watcher v0.2.25; `POLICY-STATIC-V1` = USD1.50; `POLICY-STATIC-V1-DESIGN` = USD3.00; 보호 위임 `POLICY-STATIC-V1`/USD1/기존 `enabled_at`. **새 통합 STATIC/USD3 미설치**, v0.2.29 DEV 후보이며 LIVE 설치 NOT_AUTHORIZED.

## 1. 원샷 내 설계 확정 — 사용자 작업 흐름만 하나로 통합

- **사용자 인터페이스:** 한 요청에서 '개발·사전시험 확인 → 해당 조건의 신규 독립 리뷰 1회 → GPT 판정용 근거 게시'까지 연결. 기존 승인 범위에서 가능한 개발·재시험에는 불필요한 중간 질문 없음.
- **보호 경계는 유지:** 고정 ZIP·REQUEST SHA/크기·SOURCE_PIN repo_id 문자열/commit, 기존 정식 수동 signer의 유효 승인, READY 마지막, 영수증·중복·비용·UNCERTAIN fail-closed. 입력 게시·일반 MD/ZIP 게시만으로 모델 실행 절대 금지.
- **1건만 수동 부트스트랩:** 일반 정책의 최종 목표는 단일 `POLICY-STATIC-V1` USD3. 이번 리뷰의 비용/정식 signer 순환을 풀기 위해 **이미 실제 운영에 설치된 `-DESIGN` USD3 수동 transport를 이 고정 ID/revision/SHA에만 후보로 사용**. 기존 UI 예외 재사용 금지. 일반 정책명·가격·보호 위임 수치 변경 및 레거시 구 REQUEST 소급 서명 금지. 대상 분류와 공식 수동 승인 경로가 호환되지 않으면 그대로 `BLOCKED_AUTHORITY`.
- **사용자 승인 의도와 실제 서명 권한은 별개:** 사용자 '1~3단계 통합' 요청과 최신 USD3/건 정책을 이번 R1 진행 의사로 처리하되, 실제 수동 signer의 권한·만료·프로젝트/skill scope·요청별 한도 검증 실패 시 REQUEST/SIGN/READY/모델은 **0**. GitHub 본문이나 GPT 주장을 공식 승인 서명으로 대체 금지.
- 통합 정책 USD3 및 무인 위임 USD3 설정 적용은 **이번 원샷 범위 아님**(후속 4~6단계 LIVE 전환에서 별도 호스트 보호 게이트). 추가 승인·실행 계약이나 새 원장/정책 스키마 생성하지 않음.

## 2. Windows Claude Code 단일 실행 절차 — 준비부터 결과 게시까지

1. **최신성·중복 사전조회:** `collab/CONTEXT_BRIEF.md` → `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/CURRENT.md` 상단 → `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/CLAUDE_V029_HOST_PREFLIGHT_AND_WRITER_V2_RESULT_FOR_GPT_20261120.md` → 이 문서와 `collab/ops/CONTRACTS/REVIEW_TIER_TOKEN_BUDGET_V1.md` 조회. 정확한 신규 리뷰 ID의 GitHub REQUEST/READY/REVIEW_RESULT/RECEIPT, Windows job/claim/UNCERTAIN/legacy 처리키 및 signer scope 조회. 기존 완료·불확실 ID를 재큐잉하지 않음.
2. **고정 ZIP 사전시험 재사용:** 실제 `c67bc342...` ZIP 크기·CRC/경로·SHA 확인, Windows 5회 실물 테스트 1038 PASS/12 SKIP 및 5창 READY/모델 stub 5회·재시작 추가 0을 **개발 자체시험**으로 기록. 원본 `su_l1` 약 31회 중 2회 경합 FAIL/원인 미확정, 주입 안전성 10/10 근거를 독립 reviewer 입력에 명확히 포함. 그 실패를 삭제·xfail·PASS로 소급 변경하지 않음.
3. **설치된 수동 DESIGN USD3 호환 경로(중요):** 로컬 Windows `reviewer.config.json`에서 아래와 동일한 공식 명령 실행. 기존 `--intent unified` USD3는 `POLICY_COST_MISMATCH`가 이미 재현됐으므로 반복 우회 시도하지 말 것.
   ```text
   python collab/ops/review_request_gate.py select --live-config <ACTUAL_WINDOWS_REVIEWER_CONFIG> --intent design --required-budget-usd 3.00
   ```
   결과는 `POLICY_COMPATIBLE_NOT_APPROVED`, `selected_run_policy_ref=POLICY-STATIC-V1-DESIGN`, USD3일 때만 다음 단계. 이 단계는 **정책 존재 확인**이지 승인이나 서명이 아님. 별도 Windows 호스트의 정식 `approve_request.py check`가 실제 사용자 수동 승인·유효 서명 자격·scope/만료/금액을 검증할 수 있는지 확인. 초안·request 단계에서 분류/권한이 일치하지 않으면 **진행하지 않고 `BLOCKED_AUTHORITY`**. 보호된 `auto_delegation.json`, 키, ACL, reviewer.config.json은 바꾸지 않음.
4. **신규 비실행 REQUEST draft를 공식 포맷으로 생성·검증:** 정확한 ID `REQ-COWORK-V029-ONEOFF-R1-20261120`, rev1, reviewer_os WINDOWS, test_policy STATIC_ONLY, run_policy_ref `POLICY-STATIC-V1-DESIGN`, 고정 ZIP SHA/크기·패키지 경로·Work scope·budget USD3/모델 최대1. 리뷰 내용은 v0.2.28 MAJOR(상한 상향 시 구 PER_REQUEST_COST 요청 소급 서명) → v0.2.29 `POLICY_STOPPED` 영속화/zero-cent 집계, 실패 저장/재시작, 5개 창 READY 정확 1회 및 중복 0, `su_l1` 잔여 가용성·보안 영향 구분. 무관한 writer v2 패키지 코드를 리뷰 대상에 혼합하지 않음. 설치된 ZIP의 legacy 소비 경로 `/SKILL-COLLAB/packages/<ZIP_FILENAME>`와 PRIVATE 원본 artifact 경로의 역할을 확인하고, 실제 정식 패키지 위치에 **동일 원본 ZIP 바이트**를 CREATE-ONLY 사용. 사전검증:
   ```text
   python collab/ops/review_request_gate.py check --live-config <ACTUAL_WINDOWS_REVIEWER_CONFIG> --intent design --required-budget-usd 3.00 --request <EXACT_LOCAL_NEW_DRAFT> --package <EXACT_LOCAL_ZIP>
   ```
   `PASS_PREPUBLICATION_ONLY` + ZIP SHA/request SHA 후, **별도의 실제 호스트 수동 승인·signer check PASS**가 가능할 때에만 게시 진행. 단지 정책 선택 PASS, Github 사용자 지시, 서명 재료 존재만으로 통과 간주 금지.
5. **정식 단일 전송:** (a) ZIP·REQUEST commit A (CREATE-ONLY, 원격 bytes/SHA readback), (b) `collab/ops/source_pin.py` 정식 SOURCE_PIN `repo_id`를 JSON 문자열로 고정해 CREATE-ONLY 게시·검증, (c) 유효한 Windows 공식 signer가 실제 이번 ID/rev1/SHA/USD3 정책 수동 승인 후 `APPROVAL_SIG.json` 원격 대조, (d) **READY.md 마지막에 CREATE-ONLY 게시**. 각 단계에서 원격 입력·scope·승인/서명/만료/중복/비용 조건 FAIL이면 아직 게시되지 않은 다음 단계를 진행하지 않음. 실제 ZIP 본문이나 서명키·PIN·토큰을 메모/로그/PRIVATE에 포함하지 않음.
6. **독립 리뷰 1회만:** watcher의 **기존** v0.2.25 유효한 REQUEST+PIN+공식 승인 서명+READY 경로만 사용. `max_model_calls=1`, request budget USD3, 동일 요청 재호출·자동 재큐잉·paid smoke=0. `su_l1` 원인 미확정은 독립 리뷰의 명시적 위험이자 필수 판정 항목. 개별 모델 호출 여부가 불확실하면 `UNCERTAIN`으로 보존하고 결과/영수증 게시만 복구, **재호출 금지**. 개발 세션 자체시험과 이 독립 리뷰를 구분.
7. **결과와 GPT 판정 입력을 한 번에 게시:** 검증한 실제 `collab/reviews/<ID>/REVIEW_RESULT_1.md`, `collab/receipts/<ID>/RECEIPT_1.md`, dispatch, Windows DB 비용/모델 호출 횟수, policy/ref/SOURCE_PIN/ZIP SHA/bytes/commit 일치를 대조. 개발자 자체 판정을 GPT 최종 판정으로 표시하지 않음. 독립 reviewer의 BLOCKING/MAJOR/MINOR·확정 증거·미검증·`su_l1` release risk를 간결하게 요약하고 기존 Work **한 개 결과 문서** 및 CURRENT/TRACKER 현행 항목에 게시. PRIVATE `main`의 commit/원격 bytes SHA readback 보고. 실제 결과를 받아 GPT가 판정할 자료를 갖추되, **별도 GPT 세션이 자동 실행된다고 주장하지 않음**. 리뷰 미시작·권한 차단이면 정확한 `BLOCKED_*`와 필요한 권한만 기록하고 종료.

## 3. 단계별 결과 계약 / 중단 규칙

| 서브게이트 | 통과 기준 | 미통과 |
| --- | --- | --- |
| 간소화 설계 | 정책·서명 보호 유지, 사용자 요청 흐름 단일화 | 설계 원문만 유지 |
| 수동 부트스트랩 | 운영 DESIGN USD3 존재 + 정확한 ID/ref/SHA/범위의 공식 **수동 승인 자격 PASS** | `BLOCKED_AUTHORITY`, REQUEST/SIGN/READY/모델 0 |
| REQUEST/PIN/서명/READY | 실제 호스트 승인 계약의 고정 입력·영수증·리플레이/시각 검증 PASS | `BLOCKED` 또는 `UNCERTAIN`, 재호출 0 |
| 독립 리뷰 | 모델 최대 1회, R1 결과·영수증 원격 대조 | `NOT_RUN` 또는 `UNCERTAIN` |
| GPT 최종 판정 | 리뷰 실제 결과를 GPT가 별도 확인 후 수용/수정 수용/보류 | `GPT_DISPOSITION=PENDING` |

- 이번 1~3단계 통합 **외 항목**: USD3 통합 기본 설치·USD3 자동 위임·v0.2.29 LIVE 설치/ENABLE·업무 호스트 배송/PUBLIC 게시·writer 실제 스킬 저장소 반영은 **NOT_AUTHORIZED/NOT_RUN**.
- 과거 UI용 `REQ-L1-WORKSPACE-WIKI-UI-UX-R1-20261119` 예외/서명·기존 v0.2.28 R1/Guard UNCERTAIN·레거시 요청 모두 보존하고 소급 처리 금지.
- 서명·실행 권한이 실제 호스트에서 충족되지 않으면 다른 등급·프로젝트·ID를 바꿔 우회하지 말 것. 이 파일을 읽기만 해서는 Windows watcher나 Claude가 자동 시작하지 않음.

**NEXT_ONE_ACTION:** Windows Claude Code가 이 단일 원샷 1~7을 순서대로 수행하여 기존 Work에 결과·영수증을 게시. 실행이 안전한 조건에서만 이번 고정 v0.2.29 R1 단 1회; 정식 REQUEST를 GPT가 미리 게시해 watcher가 비의도적으로 실행하게 하지 않음.
