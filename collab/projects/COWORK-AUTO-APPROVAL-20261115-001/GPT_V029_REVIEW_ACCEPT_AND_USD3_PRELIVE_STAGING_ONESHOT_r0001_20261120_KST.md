# v0.2.29 R1 GPT 판정 + USD3 정책 정합화 + LIVE 사전검증 — 통합 1~3 원샷

- 기준: 2026-11-20 KST; PRIVATE `wonhwipark/CoWork-Skill-Collab` branch `main`; 기존 Work `COWORK-AUTO-APPROVAL-20261115-001`
- 사용자 최신 지시: **남은 단계 1~3을 한 번에 수행**, 최종 **4단계 LIVE ENABLE은 별도**. 사용자가 요청한 통합 작업은 승인된 개발/시험·안전 사전검증 수행을 의미하며, 이 문서 자체가 Windows 호스트의 보호된 정책 변경·키/DB/Task 수정·새 유료 호출의 인증 수단은 아님.
- 리뷰: `REQ-COWORK-V029-ONEOFF-R1-20261120` rev1. `collab/reviews/<ID>/REVIEW_RESULT_1.md`, `collab/receipts/<ID>/RECEIPT_1.md`, `collab/dispatch/<ID>/DISPATCH_1.md`.
- 후보: `artifacts/v0_2_29/skill-collab-watcher_v0_2_29_1120.zip`, **310753 B**, **SHA256 `c67bc342fe77547b000fc42e1b886396cbef035c0d265dbcd124947e267ed83f`**; reviewed bytes 그대로 보존.
- 현재 LIVE 호스트(최신 Windows 보고): **v0.2.25**, 설치 STATIC USD1.50 / DESIGN USD3.00 / LARGE USD3.00, 보호 위임 STATIC max_request USD1.00. 통합 STATIC USD3 **NOT_OPERATIONAL**.
- 기존 리뷰 요청은 **CLOSED_NO_RETRY**. 새 REQUEST/READY/서명·유료 모델 호출 0. 기존 완료/대기·GUARD UNCERTAIN·영수증 손실 없이 보존.

## 1. GPT 최종 독립 리뷰 판정 (이번 대화에서 실제 완료)

`GPT_DISPOSITION=ACCEPT_WITH_CONDITIONS`, `INDEPENDENT_REVIEW_R1=COMPLETED`, `REVIEW_BLOCKING=0`, `REVIEW_MAJOR=0`, `REVIEW_MINOR=3` (이 중 세 번째는 **검토 범위 한계/이월 확인 미수행**으로 코딩 결함 확정이 아님). `REVIEW_MODEL_RETRY=FORBIDDEN`.

**GPT 직접 원격 검증:** 새 ID의 REQUEST/READY/SOURCE_PIN(문자열 repo_id `1451933830`)/RESULT/RECEIPT/DISPATCH를 읽어 전체 request ID/rev1/package SHA/processing key 일치; 결과 `COMPLETED`, 영수증 `ok=true`, watcher v0.2.25를 확인. Windows 결과 문서 `CLAUDE_V029_ONEOFF_R1_RESULT_FOR_GPT_20261120.md`는 실제 DB `COMPLETED`·MODEL_CALLS1·USD0.5387501·15 turns·중복0을 보고했으나 GPT는 Windows 운영 DB/CLI 청구 내역을 직접 열지 못함. 비용 근거는 **HOST_REPORTED**, 원격 영수증 본문에는 비용 필드 없음.

**독립 리뷰 결과 반영**
- v0.2.28 MAJOR였던 cap 상향 시 과거 `PER_REQUEST_COST` 거절의 소급 승인 위험은 v0.2.29의 `POLICY_STOPPED` 영구 제외로 **정적 검토상 수정 확인**; 5회 Windows 개발 자체시험도 통과. 리뷰어는 Windows 실행 테스트를 직접 수행하지 않았음.
- MINOR 1 검사 순서(`UNSUPPORTED_DELEGATION_LIMIT`가 `PER_REQUEST_COST` 뒤): 두 경우 모두 fail-closed. **비차단 수용**, 후속 변경 때 관련 소형 시험으로 개선 검토, 이번 ZIP 변경 금지.
- MINOR 2 등록 정책 비용과 보호 위임을 비일관하게 올리는 순간의 신규 적격 요청이 영구 제외되는 운용 주의: **설정 변경 전 watcher 정지, 이중 설정 준비·보호 검증 후 일관된 재기동** 조건으로 수용. 설정 누락/실패 시 새 리뷰가 정상 처리될 것이라고 주장 금지.
- MINOR 3 이전 v0.2.28 MINOR 원문 미제공: 기존 `collab/reviews/REQ-COWORK-V028-AUTO-REVIEW-R1-20261120/REVIEW_RESULT_1.md`와 Windows 현장 대조의 상세를 반영. `approve_request.py`는 host-side 도구이며 패키지 밖임을 수정 확인; 문서의 일/월 상한 설명은 **일부만 정정**. reviewer의 이번 Q8 검증은 그대로 NOT_RUN이며 리뷰 완료로 소급 표기하지 않음.
- 이번 R1 결과의 `su_l1`: watcher runtime에 연결되지 않은 별도 실험(test-only availability); **su_l1 자체는 활성화/연결 금지**, 관측 FAIL 근본 원인 UNRESOLVED 기록. watcher v0.2.29 LIVE 후보에 대한 보안 BLOCKER로 보지 않음.
- **ZIP 밖 정오표**: `docs/AUTO_APPROVAL.md` 29행의 "day/month ceilings inside the same transaction" 및 74행의 "USD limits remain per request/day/month"는 현 코드와 불일치. 현 정책은 요청당 상한만 입장 검증, 일·월 한도는 관측 텔레메트리이며 거절 게이트가 아님. **정오표를 본 문서에 고정**, ZIP 내 문서 수정/v0.2.30 생성/추가 유료 리뷰를 요구하지 않음.
- `docs/CUTOVER_RUNBOOK.md`의 `development_not_for_deployment`는 정적 리뷰 결과만으로 자동 해제되지 않음. LIVE 단계에서 실제 설치 SHA·설치시각·이전 LIVE SHA·승인자/운영 전환 판정·새 정책/보호 위임·롤백 결과를 **별도 명시적 운영 결정**으로 기록. 이 문서는 LIVE override 자체가 아님.
- **한계:** reviewer는 diff + callsite 위주 정적 CODE_REVIEW였고 변경 없는 `cli.py`, `orchestrator.py` 등과 전체 CUTOVER_RUNBOOK을 실행/전부 읽지 않음. 최종 운영 게이트 SHADOW/단일 provider/ACL/서명/legacy 제외/rollback은 실제 호스트에서 추가 확인해야 함.

## 2. 단계 2 — 단일 USD3 정책 정합화의 안전한 사전 준비

**목표(이전 사용자 승인된 통합 정책):** 새 리뷰는 일반/설계 구분 없이 `POLICY-STATIC-V1`, request당 USD3, 1 call, 총 일·월 개수/비용은 admission gate로 쓰지 않음. 범위·프로젝트·skills allowlist·키·trust root·expiry·SOURCE_PIN/READY/중복 fail-closed 계약은 유지. 구 DESIGN/LARGE는 고정 이력 호환 전용.

**이번 단계에서는 운영 LIVE config/위임/DB/Task/Notifier/키/ACL을 직접 바꾸지 않는다.** 아직 v0.2.25이므로 위임과 비용 상한만 먼저 올려 구 REQUEST 소급 승인 위험을 만들지 않음. Windows에서 다음은 **읽기 전용 + 격리 config/가짜 transport/signer**로 수행:
1. watcher v0.2.25 실제 설치 SHA/실효 `reviewer.config.json`·보호 위임(USD1, `enabled_at`, expiry, scope)·Task/lease·신뢰된 보호 변경 도구·운영 ACL 확인. 비밀 본문 출력/원격 게시 금지.
2. 모든 기존 `pending_requests`·`auto_claims`·jobs·seen/status·READY/APPROVAL/RECEIPT/UNCERTAIN·레거시 DESIGN/LARGE/Guard를 로컬 DB **읽기 전용 일관 스냅샷**과 원격 대조로 분류. 과거 요청 적격 상태 변경, 임의 종결/삭제/재큐잉 금지. 원래 시점 비용 거절은 `POLICY_STOPPED` 또는 비적격을 확실히 유지.
3. 별도 임시 설정에서 신규 STATIC 등록 비용 USD3, 보호 위임 상한 USD3을 **같은 staged transaction/원샷 목표 상태**로 만들어 실제 `review_request_gate select/check --intent unified` + 자동 승인 범위·signing/READY mock 테스트. `enabled_at`은 **실제 추후 cutover 시점**에 새로 고정할 값으로만 계획하며 미리 과거 날짜로 확정하거나 낮추지 않음.
4. 합성 old REQUEST(구 USD1/1.5 실패, 기존 DESIGN, 최초 disable 관측, completed, UNCERTAIN)가 신규 policy로 **절대 자동 READY/sign/model로 바뀌지 않음**, 반면 새 유효 범위의 요청만 STATIC USD3에서 가짜 적격성 PASS. `su_l1` OFF 보장. 등록 비용/위임 불일치·만료·repo ID 타입·입력 SHA 불일치·키 부재에서는 fail-closed PASS.
5. 실제 보호 설정의 신뢰된 설치/서명 갱신 수단이 없다면 `STAGED_POLICY_READY=BLOCKED_HOST_AUTH` 기록, 파일 직접 수정·새 키/토큰 생성·과거 요청 우회 금지. staging 완료는 LIVE 정책 USD3 설치가 아님.

## 3. 단계 3 — LIVE 전환 직전 게이트를 한 원샷에서 사전검증

사용자의 **4단계 LIVE ENABLE 별도 승인** 전에는 실제 LIVE 서비스 중단·교체·재기동/자동 서명 활성화 금지. 우선 호스트에서:
1. 이미 있는 보호 백업/복원 절차, DB main/WAL/SHM 일관 스냅샷 방법, watcher 설치 v0.2.25 SHA 및 검토된 v0.2.29 SHA, 실제 signer/위임·정책·작업 스케줄/Notifier, 단일 provider lease/LOCK을 **읽기 전용** 점검. 실제 시스템 백업·중지는 기존 승인 범위와 안전한 보호 도구가 있을 때에만 수행하며, 불가 시 `BACKUP_READY=NOT_VERIFIED`.
2. 운영과 물리적으로 분리된 **임시 DB/로컬 staged config/가짜 GitHub transport·signer·model stub**에서 v0.2.29 ZIP을 검증하고 기존 실제 5회 자체시험 증거 활용. 재현 필요조건(소급/비활성 중 관측/legacy DESIGN·LARGE/Guard UNCERTAIN/중복/정책 변조/타 provider/실패 복구)을 추가 SHADOW로 확인. **모델 호출·실제 GitHub REQUEST/READY 0**.
3. 실제 보호 갱신 순서와 실패 시 원복 계획을 문서화: operator authorized → watcher 안전 정지 + 백업/검증 → reviewed ZIP 설치 → 정확한 STATIC USD3/위임 USD3/새 `enabled_at` 원자적 정합 상태로 보호 설정 적용 → 격리 shadow/host load 확인 → **별도 LIVE 승인 후에만** 재가동·실제 인수 검증. 중간 불일치가 보이면 보호된 v0.2.25/위임 USD1로 롤백, 실패·UNCERTAIN 원시 기록 보존. 이전 완료·불확실 요청 모델 재실행 0.
4. 최종 `HOST_PRELIVE_GATE=PASS|PARTIAL|FAIL|BLOCKED`와 세부 항목(실제 policy apply, signer ACL, pending clean, sha, backup, rollback readiness, old requests no-revival, 2-cycle+restart rehearsal, dynamic scope)을 구분. **모든 안전 게이트 PASS** 및 유효한 별도 LIVE 운영 승인 전에는 마지막 단계 실행 금지. SHADOW를 실제 LIVE 검증 PASS로 표시하지 않음.

## 4. Windows Claude Code 하나의 실행 지시 / 결과 계약

PRIVATE `wonhwipark/CoWork-Skill-Collab` branch `main`에서 `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/CURRENT.md` 최상단→`CLAUDE_V029_ONEOFF_R1_RESULT_FOR_GPT_20261120.md`→본 문서를 읽고, **새 리뷰/유료 호출 없이 단계 2와 3을 하나의 Windows 원샷**으로 수행. 1단계 GPT 판정은 위에 이미 완료돼 있으므로 중복 작업·재리뷰 금지. 해당 Windows 로컬 자격/호스트 읽기 권한이 없어 실제 실행이 막히면 가능한 격리 시험까지 진행하고 막힌 항목만 `BLOCKED/NOT_RUN`로 보고.

산출물은 **같은 Work의 한 결과 문서** `CLAUDE_V029_USD3_PRELIVE_READINESS_RESULT_FOR_GPT_20261120.md`, 현재 CURRENT 상단의 짧은 단일 현행 요약, 기존 TRACKER 현행 필드 갱신만. 결과 문서에 정확하게:
- `GPT_DISPOSITION=ACCEPT_WITH_CONDITIONS`, 독립 리뷰 `COMPLETE`/호스트 비용 USD0.5387501(이미 정산, 신규 비용 0)
- `STAGED_STATIC3_SELECT_CHECK`, `LEGACY_EXCLUSION`, `PROTECTED_POLICY_CAP_ALIGNMENT`, `NEW_ENABLED_AT_PLAN`, `SU_L1_OFF`, `BACKUP_READY`, `ROLLBACK_READY`, `SINGLE_PROVIDER`, `SHADOW_5WINDOW`, `HOST_PRELIVE_GATE`, `INDEPENDENT_REVIEW_NEW=0`, `MODEL_CALLS_NEW=0`, `LIVE_ENABLE=NOT_RUN`.
- 실제 실행/격리 mock/읽기 전용/예상 구성 각각 구분. 바이트 SHA·원격 commit/readback 검증, 호스트 protected config 변경 전/후를 사실대로 기재.
- `development_not_for_deployment` 개발 라벨은 **별도 LIVE 운영 승인 때만** 외부 결정서로 해제 여부 판정. 이 문서로 LIVE 승인·보호 키 변경/비용 증액을 자동 행사하지 않음.

**다음 단 하나의 작업:** Windows Claude Code가 사용자 승인된 단계 1~3 통합의 남은 호스트 사전 준비를 위 §2~4대로 수행·게시. GPT는 그 결과를 확인해 최종 **4단계 LIVE ENABLE**의 기술 준비 PASS 여부를 판정하며 운영 승인과 실행은 별도.
