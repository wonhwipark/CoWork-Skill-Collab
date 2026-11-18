# GPT 판정·Windows 원샷 — 구 DESIGN R1 비실행 종결과 통합 $3 게이트 재개
- 날짜: 2026-11-19 KST
- 정본: GitHub **PRIVATE `wonhwipark/CoWork-Skill-Collab`**, branch **`main`**
- 기존 Work: `COWORK-AUTO-APPROVAL-20261115-001`
- 연결 호스트 결과: `CLAUDE_UNIFIED_REVIEW_USD3_HOST_RESULT_FOR_GPT_20261119.md` (commit `f9a2f641b67b`, SHA-256 `0ce4a1bf6edc260f89162bc1e3e4f78032a9a1cd32f4347f6b815277ea7cce3f`)
- 근거: 2026-11-19 Windows Claude Code A~C PASS, 소급 실행 위험에 의한 D~F BLOCKED. 사용자 앞선 단일 USD 3 자동 승인 정합화 승인 범위 유지. **새 유료 독립 리뷰 승인 아님.**

## 1. GPT 실체적 판정 (정책/이력)
**`REQ-COWORK-BUDGET-V025-DESIGN-R1-20261117` rev1은 중복 목적의 미시작 구 요청으로서 `SUPERSEDED / DO_NOT_EXECUTE`를 채택.**
- 고정 입력: `run_policy_ref=POLICY-STATIC-V1-DESIGN`, `package_sha256=26d63c8a03290499b13b2ceb8ff0b70c06eb1b1bcc1a25fe3d8f65fcc213d228`, 283930 bytes, 원격 REQUEST blob `3df6940301964c6b499db60203c297e778d02cf0`; SOURCE_PIN blob `39c0076c1aab4de9e67ce942442a8a8a3130bc40`. 2026-11-19 확인된 이 폴더에는 REQUEST와 SOURCE_PIN만 있고 APPROVAL_SIG/READY 없음.
- 완료 대체 요청: `REQ-COWORK-BUDGET-V025-LARGE-R2-20261117` rev1, **동일 ZIP bytes/SHA**, `POLICY-STATIC-V1-LARGE`로 서명·READY·DISPATCH·REVIEW_RESULT·RECEIPT 이미 원격 확인. 결과 `COMPLETED`, `RECEIPT ok=true`, GPT `ACCEPT_WITH_CHANGE` / `REVIEW_CYCLE=CLOSED`. [원 판정](GPT_V025_LARGE_R2_DISPOSITION_r0001_20261117_KST.md).
- 두 요청은 **다른 REQUEST ID**이므로 엔진이 자동으로 동등하거나 종결 처리한다고 가정하지 않음. 완료 대체 이력 때문에 기존 DESIGN에 **새 유료 모델 호출 권한 없음**.
- **정본 판정=PASS, 실제 엔진 종결=NOT_RUN.** 이 문서는 watcher가 인지하는 CANCEL 신호가 아니며 GitHub 본문만으로 `REQUEST.md`/SOURCE_PIN·승인/READY/SQLite 상태는 바뀌지 않음.

## 2. Windows Claude Code 단일 조건부 호스트 작업
1. **선행 확인(무쓰기):** PRIVATE main의 이 문서·위 호스트 결과, 기존 이관 CURRENT·자동 승인 CURRENT를 읽고 Windows watcher v0.2.25 실제 설치본에서 **공식 지원하는 정확한 1건 취소/철회/대체/종결 경로가 존재하는지** 소스/CLI/StateStore/API/운영 계약으로 확인. 재평가되는 state machine 조건(`prior_state`, `pending_requests`, `auto_claims` 등)을 명시. 해당 구 DESIGN R1의 `request_id/rev/package_sha` 및 미서명·미READY·미실행·미과금 원격/DB 기록을 재검증.
2. **기존 지원 수단이 있고 유효 승인/안전 보장이 확인될 때만 정확히 1건 종결:** 사전 DB main/WAL/SHM·설정·Task/권한 보존 및 bytes SHA·복원 수단 확인 → 단일 provider 실행 경쟁 배제 → **공식 엔진 상태 전이**로 해당 구 DESIGN R1만 `WITHDRAWN/SUPERSEDED/REJECTED` 중 실제 지원된 terminal 상태에 1회 기록. 기존 고정 REQUEST/SOURCE_PIN/APPROVAL_SIG/READY/REVIEW/RECEIPT 내용을 수정·삭제하지 말고 감사·선택 근거·처리키 보존. 단순 `CURRENT`/TRACKER 표시·임의 로컬 DB UPDATE/INSERT·가짜 UNCERTAIN·무효 승인 서명·새 READY·임의 삭제로 종결을 가장하지 말 것.
3. **종결 후 격리 무과금 재평가:** 실제 설치 코드의 완전한 평가 경로로 `max_request_usd=3` 가정과 `POLICY-STATIC-V1=$3` 가정에 대해 과거 DESIGN R1이 **설정에 상관없이 영구 거부됨**을 증명. 다른 미해결 3건은 `enabled_at_first_seen=0`, Guard는 `UNCERTAIN`, 이미 완료된 LARGE R2는 `COMPLETED`로 재실행 0을 확인. DB/원격/알림 중복 0. **단순 현재 $1 한도 차단은 종결 PASS가 아님.**
4. **안전성 PASS일 때만 기존 D~F 재개:** `GPT_UNIFIED_REVIEW_USD3_CONDITIONAL_APPLY_r0001_20261119_KST.md`의 D~F를 **같은 원샷에서** 수행하되 보호된 로컬 변경 권한/사전위임 유효성·allowlist·expiry·서명 검증·백업·SHADOW/2주기·롤백과 단일 provider 조건 유지. 신규 리뷰 요청의 기본 ref는 `POLICY-STATIC-V1`/USD 3, 일·월 누적 제한 없음, 요청당 1회.
5. **지원 수단 부재/불확실 시:** 비공식 DB 조작·옛 REQUEST 수정·서명 위조를 하지 말고 **`RETIREMENT_ENGINE=BLOCKED, HOST_CONFIG_APPLY=BLOCKED`**로 보존. 해당 단계 자체가 실제 미입증 gap임을 같은 Work에 상세 기록. 허용되지 않은 새 watcher 버전·PUBLIC ZIP·정식 유료 리뷰를 자동 시작하지 말 것.
6. **결과 게시:** PRIVATE main `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/CLAUDE_LEGACY_DESIGN_R1_CLOSEOUT_AND_USD3_RESULT_FOR_GPT_20261119.md`; 관련 CURRENT/TRACKER는 **실제 결과에 맞춰** 요약 갱신. 최소 필드: `SUPPORTED_TERMINAL_PATH`, `ENGINE_RETIREMENT`, `OLD_DESIGN_READY`, `SHADOW_AFTER_RETIREMENT`, `PROTECTED_DELEGATION_USD3`, `HOST_CONFIG_APPLY`, `AUTO_SIGNING_USD3`, `MODEL_CALLS`, `NEW_REQUEST_READY`, 변경 전후 복원·bytes SHA 및 commit/readback. 상태는 PASS/FAIL/BLOCKED/NOT_RUN 구분. 키·토큰·DB 내부 민감 데이터 게시 금지.

## 3. 불변 조건·완료 기준
- **유료 Claude 모델 호출 0**, 신규 REQUEST/READY 0, 기존 불확실 Guard 자동 재시도 0, 완료된 LARGE R2 재호출 0.
- 원본 ZIP/REQUEST/SOURCE_PIN/승인·리뷰 이력 무변경; 과거 대기 3건 소급 실행 0.
- `ENGINE_RETIREMENT=PASS`는 **실제 watcher 적격성 차단 + 감사 증거**가 있을 때만. 문서 게시나 원격 REQUEST 폴더 별칭으로 PASS 주장 불가.
- Windows에서 공식 종결 수단이 없어 BLOCKED면 **기존 v0.2.25 운영·보호 위임 USD 1 유지**. 이미 승인된 $3 통합 정책을 이유로 old-design 재실행이나 보호 권한 우회 금지.

**NEXT_ONE_ACTION:** Windows Claude Code가 이 문서의 1~6을 한 번 실행하고 결과를 PRIVATE main에 게시·실제 readback. GPT는 엔진 차단과 새 보호 위임 적용을 분리해 최종 판정.
