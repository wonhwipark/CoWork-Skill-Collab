# GPT v0.2.27 독립 리뷰 판정 및 안전한 검증·요청 인계 r0001
- 날짜: 2026-11-19 KST
- PRIVATE 정본: `wonhwipark/CoWork-Skill-Collab` branch `main`
- 기존 Work: `collab/projects/COWORK-AUTO-APPROVAL-20261115-001`
- 개발 결과: [CLAUDE_UNIFIED_USD3_ADMISSION_FIX_DEV_RESULT_FOR_GPT_20261119.md](CLAUDE_UNIFIED_USD3_ADMISSION_FIX_DEV_RESULT_FOR_GPT_20261119.md)
- **GPT 판정: `INDEPENDENT_REVIEW=REQUIRED`, `REVIEW_REQUEST=NOT_POSTED`, `REVIEW_PAID_CALLS=0`, `HOST_LIVE_APPLY=BLOCKED`.** 개발자 자체시험을 독립 리뷰로 승격하지 않음.

## 1. 고정 검토 원본·변경 사실
- v0.2.27 후보: `artifacts/v0_2_27/skill-collab-watcher_v0_2_27_1119_DEV_NOT_FOR_DEPLOYMENT.zip`, **309187 B, SHA-256 `baf5a856fbe1e34d0c3b235a5ccd5a7895ad342a18cf448360b53773ac8669e0`** (Windows host manifest·원격 검증 보고; GPT 별도 ZIP raw byte 직접 계산은 미실행).
- 비교 v0.2.26: SHA-256 `f08adb6099d06daf494362ed7e33ea66aabcbf749cfd2c027a7f70bcba5540fe`.
- 함께 고정할 리뷰 입력: `artifacts/v0_2_27/CANDIDATE_MANIFEST.json`, `artifacts/v0_2_27/diff_v0_2_26_to_v0_2_27.patch`, 특히 `skill_collab_watcher/auto_policy.py`, `auto_approval.py`, `state_store.py`, `orchestrator.py`, `config.py`, 연계 시험/문서. 과거 리뷰 범위 누락(M1)을 반복하지 않도록 ZIP/스냅샷 외부의 patch/manifest는 reviewer가 실제 접근 가능한 **별도 pin된 입력**으로 전달하고 실제 읽은 범위를 기록할 것.
- 실제 diff에서 승인 gate는 `if c.policy not in ("POLICY-STATIC-V1", "POLICY-STATIC-V1-DESIGN")` → `if c.policy != "POLICY-STATIC-V1"`로 변경. 나머지는 버전·테스트·문서의 일관성 수정. old DESIGN request 자동 서명 차단 여부는 실제 입구와 허용 ref의 전파를 독립 확인해야 함.

## 2. 독립 리뷰가 필요한 이유와 한계
1. 작은 diff라도 **유료 모델 실행을 허용/거부하는 정책 경계**이며, 이전에 발견한 특정 request_id의 소급 서명 위험을 직접 해결하는 변경임. 이전 v0.2.25 LARGE R2 완료는 새 v0.2.27 코드를 검토한 근거가 아님.
2. Windows 개발자 자체시험: `1010 PASSED / 21 FAILED / 12 SKIPPED`, isolated E2E `8/8 PASS`. 21 FAIL은 기존 두 묶음(구 일/월 quota 가정 6건, Windows CRLF 테스트 하우징 15건)으로 **호스트가 분류**했으나 full suite **PASS로 표기하지 않음**. 신규 변경과의 비회귀 여부, CRLF fixture 관련 실제 소스·실행 영향은 독립 reviewer가 확인할 것.
3. 구 DESIGN R1의 실제 tuple/ZIP 재현 시험은 **scratch에서 실행 후 후보에 미포함**. 독립 reviewer는 재현 가능한 fixture 또는 고정된 증거가 reviewer snapshot에 있는지 확인하고, 없으면 `NOT_VERIFIED`로 남길 것. 후보에 없는 scratch 테스트를 자동으로 리뷰 PASS로 격상하지 않음.
4. `enabled_at`/earliest_request/first_seen epoch: **오래된 STATIC 요청도 새로운 $3로 소급 승인되지 않아야 함**. 단순히 디자인 ref만 거부하는 것으로 전체 과거 요청 차단을 주장하지 않음. 보호된 새 사전 위임을 설치할 때 사용자가 승인한 안전한 절차로 활성화 시점이 고정되고 신규 REQUEST에만 적용됨을 코드·반례로 확인.
5. 독립 코드 리뷰 범위: `REVIEW_POLICY`가 서명/READY/원격쓰기/유료 모델 호출 **이전**에 효력을 가지는지, DESIGN/LARGE의 우회·상태 전이·경합·거부 후 재평가, 완료/UNCERTAIN 중복 차단, 일반 STATIC/$3 합성 정상 케이스, source pin/SHA/CRC/서명·신뢰 루트·롤백 경계. **STATIC_ONLY** 모드, 실제 Windows LIVE 전환/유료 테스트/키 변경 금지.
6. 판정 형식: blocking/major/minor와 개선 제안 분리, 근거 파일·라인/재현/테스트, `ACCEPT / ACCEPT_WITH_CHANGE / REVISE / HOLD`; `INDEPENDENT_REVIEW` 및 `STATIC_ONLY` 범위, 실제 영수증·비용·모델 호출 횟수 별도 기록. 결과가 0 findings여도 근거를 보고.

## 3. 정식 REQUEST 진입은 설치 정책·승인에 종속
- 최신 신규 기본은 **단일 `POLICY-STATIC-V1` / 건당 최대 USD 3.00**. 현재 Windows LIVE v0.2.25 보고상 이 ref는 **$1.50**으로 등록됐고, 보호된 `auto_delegation.json`은 **$1.00**. 따라서 지금 신규 unified $3 REQUEST를 표준 자동 루트에 바로 게시/READY하면 **사전 정책 호환성 또는 보호 위임 검증이 실패**하는 것이 정상. 정책 사전검증 PASS 없이 REQUEST 게시하지 않는다.
- **부트스트랩 해법 검토:** 기존 Windows에 이미 등록된 `POLICY-STATIC-V1-LARGE` 또는 `-DESIGN`(둘 다 $3)은 자동 서명은 금지해도 *실제 지원되는 정식 수동 승인* 경로에서 이번 고정 v0.2.27만 독립 리뷰할 수 있는지, `review_request_gate.py select/check`와 `approve_request.py check`, 기존 유효한 서명자·금액 승인·프로젝트/스킬 scope로 먼저 read-only 확인. 이것은 **예전 등급을 신규 기본 정책으로 되돌리는 것이 아니라**, 통합 정책 LIVE 전의 단 한 차례 bootstrapping 예외 제안. 유효한 별도 비용 승인과 최소 권한/호스트 서명이 실제로 확인되기 전 승인됐다고 가정하지 않는다.
- **완료 기준:** 가능한 경우 한 개의 정식 REQUEST/revision에 대해 이전 REQUEST ID를 재사용하지 않고 고정 ZIP/REQUEST SOURCE_PIN commit A→remote byte/SHA→유효 기존 승인·서명→READY 마지막→watcher 독립 리뷰 1회→결과·영수증·원격 readback→GPT 판정 순서. 이미 완료된 v0.2.25 LARGE R2나 오래된 DESIGN R1을 재활성화하는 방식으로 대체하지 않음.
- 어떤 검증이라도 실패하거나 **현재 승인 근거가 없다면 `REQUEST=NOT_POSTED / INDEPENDENT_REVIEW=PENDING_AUTHORIZATION`**로 유지. 유료 리뷰를 재시도 없이 1회만. 해당 범위를 넘는 정책/위임/호스트 설치 임의 변경 금지.

## 4. Windows Claude Code의 다음 한 번의 작업 (무과금 preflight)
A. 이 문서·위 manifest/diff와 현재 Windows v0.2.25 실제 `reviewer.config.json`, signer/approve_request 계약 및 호스트 설정의 실제 상태를 조회. 이전 구 요청/UNCERTAIN/완료 기록은 변경 금지.
B. **기존 수동 $3 리뷰 경로가 실제 가능하고 승인된 상태인지 읽기 전용 확인**, 사전 정책 select/check 가능한 명시적 ref, REQUEST 신규 ID/정확한 ZIP/리뷰 스냅샷 입력 계약과 비용 승인(있다면 만료/허용 scope)을 보고. `POLICY_COMPATIBLE_NOT_APPROVED`는 **승인 완료가 아님**.
C. code review 없이도 검증 가능한 회귀 중 21 FAIL의 개별 목록·기존 baseline 동일 증거와 source pin/epoch cutover의 가정 등을 read-only로 대조. 다른 목적의 신규 후보/설치/유료 호출을 시작하지 않음.
D. 결과를 PRIVATE main 동일 Work에 `CLAUDE_V027_INDEPENDENT_REVIEW_PREFLIGHT_FOR_GPT_20261119.md`로 게시하고 CURRENT/TRACKER 동기화, SHA·commit/readback 확인. **사용자 기존 명시 승인 범위 밖의 새 유료 비용 지출이면 계속 PENDING**; 다음 GPT 판정에서 승인 범위만 확인해 정식 리뷰 1회를 진행. 창 간 반복 질의 최소화.

## 5. 현재 상태
- `GPT_DECISION=INDEPENDENT_REVIEW_REQUIRED`
- `PACKAGE=DEV_NOT_FOR_DEPLOYMENT`
- `PREPUBLICATION_GATE_UNIFIED_USD3=BLOCKED_ON_CURRENT_LIVE_POLICY`
- `OLD_DESIGN_R1=SUPERSEDED_DO_NOT_EXECUTE`
- `WINDOWS_LIVE=v0.2.25 / PROTECTED_DELEGATION_MAX_USD=1.00`
- `NEW_REVIEW_REQUEST=NOT_POSTED`, `NEW_READY=0`, `PAID_MODEL_CALLS=0`.
- **NEXT_ONE_ACTION:** Windows가 4-A~D를 한 번에 무과금 실행하고 수동 $3 부트스트랩 경로의 **사실·승인 조건**을 반환. 유효 승인 없이 자동 실행하지 않음.
