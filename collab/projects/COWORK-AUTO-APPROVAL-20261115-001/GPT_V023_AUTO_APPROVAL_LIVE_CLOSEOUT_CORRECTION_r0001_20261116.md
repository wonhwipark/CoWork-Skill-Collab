# v0.2.23 자동 승인 LIVE 마무리 — 실행 오류 교정 및 단일 호스트 조치

- 작성 2026-11-16 KST, r0001
- 저장소: PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`
- **정확한 인계 상대 경로:** `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/GPT_V023_AUTO_APPROVAL_LIVE_CLOSEOUT_CORRECTION_r0001_20261116.md`
- 기존 Work: `COWORK-AUTO-APPROVAL-20261115-001`
- 우선순위: **v0.2.23 기존 조건부 LIVE 완료**. 관련 비판적 리뷰 프롬프트 통합 과제는 독립 추적하되 이 전환을 불필요하게 차단·확장하지 않음.
- 사용자 최신 피드백: Windows Claude Code가 **현재 v0.2.20 수동 승인 절차만 설명하고 자동 승인 전환 실행을 멈춘 것**에 대한 시정. 사용자의 승인 요청을 반복하거나 문서만 읽고 대답하는 것으로 종료하지 말 것.

## 사실과 역할: 현재 수동 방식과 목표 자동 방식을 혼동하지 말 것

1. GitHub 단일 LIVE 운영 provider 자체는 v0.2.20에서 이미 작동 중. 단, **v0.2.20의 수동 승인 도구 `approve_request.py`는 운영 자동 승인 기능이 아니다.** `approve_request.py approve`에서 요청별 비용 입력을 요구한다는 설명은 현재 수동 경로 사실일 뿐 **자동 승인 v0.2.23의 목표 동작**이 아니다.
2. **v0.2.23에서는 승인된 보호 Windows 로컬 사전 위임의 범위 안에 있는 새 `REQUEST`에 대해 watcher 자동 승인 경로가 유효성을 판단하고 로컬 승인 키로 APPROVAL_SIG 생성·READY 마지막 게시**하는 구조. 사용자에게 매 신규 요청마다 금액 재입력, Windows Claude Code 대화형 승인 또는 Telegram 버튼을 요구하지 않음. **Windows 로컬 키 소재지와 실행 주체는 다른 개념**: 키는 PC에 남지만, 활성화 뒤 허용된 요청의 서명·READY 동작은 별도 대화형 Claude Code가 아니라 검증된 자동 처리 경로가 수행한다. 허용 밖 요청은 fail-closed. 실제 실행 가능 여부는 호스트 시험으로 입증.
3. **최신 독립 R2는 이미 완료됨. 다시 승인·서명·READY 게시·Claude 모델 호출하지 말 것.** `REQ-COWORK-AUTO-APPROVAL-V023-R2-20261115` rev1, ZIP SHA-256 `f941be8a6b53d00baa10a9b097f234b159470e2aa1242ecc33bcf0bdee080ea7`, 282340 bytes. `APPROVAL_SIG.json`, `READY.md`, `DISPATCH_1.md`, `REVIEW_RESULT_1.md`, `RECEIPT_1.md` 원격 존재. 실행 횟수 1, 호스트 DB 보고 비용 USD 0.5244525 (새 지출 0).
4. GPT 최신 정본 `GPT_V023_R2_FINAL_DISPOSITION_AND_LIVE_EVIDENCE_GATE_r0001_20261116.md`: `INDEPENDENT_R2=PASS_STATIC_SCOPE`, `GPT_R2_DISPOSITION=ACCEPT_WITH_FOLLOWUP`, 원문 `BLOCKING=0, MAJOR=0, MINOR=2`. **`LIVE_ACTIVATION=HOLD_PENDING_EVIDENCE_AND_HOST_TESTS`**는 최종 확인/설치 시험 미완료를 뜻하며 신규 비용 승인 요청을 뜻하지 않음.
5. 개발·자체시험 890 PASS/12 SKIP과 R2 정적 PASS는 실운영 시험 PASS와 다름. 실제 `AUTO_SIGNING=OFF` / 운영 v0.2.20이 마지막 확인. 새 기능 LIVE라고 먼저 선언하지 말 것.

## 지금 Windows Claude Code가 이어서 끝낼 실제 작업 (기존 조건부 사용자 승인 범위)

- **A. 읽기/증빙 정합성, 유료 모델 호출 0:** 최신 `CURRENT.md`와 GPT R2 판정, 원격 리뷰 본문·영수증을 조회. 원본 `MINOR 2` vs 기존 Windows 요약 `MINOR 3` 불일치를 새 부록으로 바로잡되 R2 원문은 불변. `USAGE_RECEIPT_1.json` 부재는 운영 v0.2.20의 실제 산출 계약을 확인하여 필수 여부 결정. 필수이면 모델 재실행 없이 기존 `REVIEW_COST` / 영수증에서 비민감 publish-only 근거를 복구; 아니면 `NOT_REQUIRED_BY_V0220`의 소스/테스트 근거 및 비용 USD 0.5244525의 호스트 DB 판정·request ID·예산 예약/정산을 결과 문서에 기재. 실제 기록이 확인되지 않으면 `BLOCKED_EVIDENCE` (임의 생성 금지).
- **B. 기존 승인 대조, 새 사용자 반복 질문 0:** `GPT_R2_APPROVAL_AND_V0222_SCOPE_FIX_GATE_r0001_20261115.md`와 v0.2.23 승인 변경 기록에서 사용자 사전 위임/조건부 설치가 유효함을 확인. 보호된 Windows 로컬 실제 정책·owner 범위·만료·repo numeric ID/브랜치/skill allowlist·예산을 로컬에서 검증. GitHub 문구만으로 로컬 신뢰 정책을 허위 설치·승인 처리하지 않음. 기존 승인 범위를 재요청하지 말고, 불명확한 실제 권한만 `BLOCKED_TRUSTED_LOCAL_POLICY`로 정확히 기록.
- **C. 조건부 Windows 운영 적용:** 정확한 기존 LIVE v0.2.20와 DB main/WAL/SHM, Task, Notifier, 로컬 키/설정 및 provider lease **무손실 백업/롤백 절차 확인** → SHA-256 `f941…80ea7` 동일한 v0.2.23 후보의 ZIP CRC/경로/비밀 스캔 → 자동 승인 기능 OFF 상태로 설치 → 운영 Python 회귀·보안 부정 시험 PASS → 기존 대기 REQUEST 소급 실행 0을 확인하고 첫 관측 기준 고정 → 보호된 위임 값 검증 후 **기존 승인의 정확한 범위에서만** `enabled=true` 및 30일 만료 활성화 → 최소 두 watcher 주기·재시작·중복 실행 차단·비허용 요청 모델 호출 0·Notifier 검증. 어느 한 게이트가 실패/불명이면 즉시 OFF 유지 또는 v0.2.20 롤백하고 상태를 정확히 보고.
- **D. 위임 정확한 allowlist:** repo `wonhwipark/CoWork-Skill-Collab` / `main` / numeric ID `1451933830`(호스트 재확인), project families `COWORK-`, `L1-WORKSPACE-`, exact skills `cowork-review-watcher`, `cowork-dashboard`, `l1-knowledge-updater`, **`POLICY-STATIC-V1`만**; 요청당 1회/최대 USD 1, 1일 최대 2회/총 USD 3, 1개월 최대 USD 10, 활성화 뒤 30일, 이전 요청 소급 0. R2/LARGE/XLARGE는 자동 승인 금지. 예산 초과·변조·불명확한 입력 fail-closed.
- **E. 품질 기준 분리:** `GPT_CRITICAL_REVIEW_AUTO_APPLY_AND_TEST_REQUEST_r0001_20261116.md`의 R0~R3 비판적 평가 프롬프트 실제 적용·fake-runner 시험은 **같은 Work에 유지하되 v0.2.23 ZIP bytes 변경/새 R2 비용 요구를 동반하여 오늘의 LIVE 마무리를 막지 말 것**. 실행된 적 없는 자동 프롬프트 적용을 완료라고 쓰지 말고 별도 후속 결과로 분리.

## 결과 게시 및 최종 게이트

- 기존 사용자 승인 안의 모든 작업이 PASS일 때 Windows가 작성할 결과: `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/CLAUDE_V023_AUTO_APPROVAL_LIVE_CLOSEOUT_RESULT_FOR_GPT_20261116.md`.
- 필수 항목: 설치 전후 운영 버전/Task 상태/정확한 설치 SHA·CRC, 승인 보호 로컬 범위의 비민감 요약·만료, DB/lease/Notifier 보존/롤백, 테스트 실제 PASS/FAIL/NOT_RUN, 자동 서명된 **새 요청의 실전 처리 여부**는 별도 확인(테스트용 유료 요청 새로 만들지 않음), 비용 추가 0, 원격 결과 commit·SHA·readback, 정확한 오류/차단 상태, **다음 한 동작**.
- `CURRENT.md` 최상단에 한 단락 요약과 근거 링크를, `TRACKER.json`의 기존 1 Work 현행 필드만 갱신. PRIVATE `main` PR 없이 게시하고 원격 본문·SHA 검증. 공개 게시·provider 변경·토큰/키 공개·기존 R2 재실행 금지.
- 사용자에게 말할 최종 결론은 둘 중 하나: **`AUTO_SIGNING_LIVE=PASS_HOST_VERIFIED`** 또는 **`AUTO_SIGNING_LIVE=BLOCKED/NOT_RUN` + 첫 번째 실제 차단 원인**. 단순히 `approve_request.py`의 수동 절차만 설명하거나 다시 `비용 확인을 해 달라`고 요구하는 것은 이 작업 완료가 아님.

## Windows Claude Code 실행용 1회 지시문

GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab` `main`에서 `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/GPT_V023_AUTO_APPROVAL_LIVE_CLOSEOUT_CORRECTION_r0001_20261116.md` 전체를 읽고 **설명만 하지 말고** 현 LIVE v0.2.20과 개발 후보 v0.2.23을 구분해 §A~E를 실제 운영 호스트에서 순서대로 처리해. R2는 이미 완료돼 있으므로 비용 승인·APPROVAL_SIG·READY·Claude 유료 리뷰를 반복하지 마. 기존 사용자 승인된 조건부 LIVE 전환 범위에서 증빙 불일치 정리·백업·OFF 설치·회귀·보호 위임 활성화·운영 검증·롤백까지 한 작업으로 묶어 처리해. 실제 로컬 신뢰/비용/범위가 검증되지 않은 게이트에서만 fail-closed로 멈추고, 확인 가능한 다음 작업을 계속해. 결과 파일과 CURRENT/TRACKER를 PRIVATE main에 직접 게시·원격 검증하고 GPT에게 상태를 보고해.
