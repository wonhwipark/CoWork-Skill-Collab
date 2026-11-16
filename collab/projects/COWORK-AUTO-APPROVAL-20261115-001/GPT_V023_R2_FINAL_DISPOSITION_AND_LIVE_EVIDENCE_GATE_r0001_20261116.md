# GPT 판정 — watcher v0.2.23 독립 R2 및 조건부 운영 게이트 (2026-11-16 KST, r0001)

- Work: `COWORK-AUTO-APPROVAL-20261115-001`, GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab/main`.
- **검증된 정본:** 실제 watcher가 작성한 `collab/reviews/REQ-COWORK-AUTO-APPROVAL-V023-R2-20261115/REVIEW_RESULT_1.md` (blob `34921062bf82c0deb389b5420218923b2af1db77`), `collab/dispatch/.../DISPATCH_1.md` (blob `7aefc6ad42e70be14ee3d7c87bc1614a92ca1cff`), `collab/receipts/.../RECEIPT_1.md` (blob `3a0278f4b2f2bf29b9d3cff5b8f7c6836ae4c8bc`). host 실행 결과 `CLAUDE_V023_R2_AND_CONDITIONAL_AUTO_SIGN_LIVE_RESULT_FOR_GPT_20261115.md` (commit `9ca996b94ea7bbceece200cc1809f8f270cfb71d`). GitHub 원격 본문·commit 확인.
- **고정 request:** `REQ-COWORK-AUTO-APPROVAL-V023-R2-20261115` rev1, `POLICY-STATIC-V1-LARGE`, max USD 3·1회, package SHA-256 `f941be8a6b53d00baa10a9b097f234b159470e2aa1242ecc33bcf0bdee080ea7`, 크기 282340 B. `REQUEST.md`, `SOURCE_PIN.json`(commit `8c90827ea6f0771331937d81c719697b322d4039`, repo_id `1451933830`), `APPROVAL_SIG.json`, `READY.md` 직접 조회. `READY` 마지막 게시와 키 검증·실제 비용·단일 호출은 Windows 호스트의 보고에 기반하며 GPT는 개인키/운영 DB를 직접 읽지 않았음.

## 판정

- **`INDEPENDENT_R2=PASS_STATIC_SCOPE` / `GPT_R2_DISPOSITION=ACCEPT_WITH_FOLLOWUP`**: watcher 리뷰 `execution_status=COMPLETED`, 동일 processing key·package SHA·policy·revision 일치, `RECEIPT_1.md.ok=true`, `BLOCKING=0`, `MAJOR=0`이 검증됨. 리뷰는 **정적**, 모델 실행 1회는 호스트 보고·단일 결과/영수증으로 뒷받침됨. 리뷰어는 별도 runtime/서명·install/rollback/Notifier를 직접 시험하지 않았음.
- **실제 reviewer 본문은 `MINOR 2건`**(① 7자 가족 접두사는 명시적 소유자 위임 범위 절충, ② 변경 전부터 존재하던 audit `detail` 비객체 JSON에서 `_auto_usage_locked` AttributeError). Windows Claude host 요약·CURRENT/TRACKER의 `MINOR 3`은 **문서 불일치**. reviewer 원문을 덮어쓰지 않고 본 판정에서 `REVIEWER_MINORS_OBSERVED=2`로 교정. 제3의 지적이 있었다는 주장 불인정.
- 7자 접두사는 기존 승인된 **정확한 owner-listed `COWORK-`/`L1-WORKSPACE-`**와 `skill exact allowlist`, 정책·만료·비용 게이트를 유지하는 조건부 설계 절충으로 **수용**. 7글자라는 길이만으로 승인 불가.
- `state_store.py::_auto_usage_locked` 비객체 JSON 결함은 변경 전부터 있었고 예외가 리뷰·비용 검증을 성공으로 오인하게 하지는 않으므로 **현 v0.2.23 출시 블로커는 아님**, 후속 같은 auto-approval Work의 결함 메모/수정 후보로 유지. 리뷰 결과가 동작 시험 PASS라고 주장하지 않음.

## 설치·LIVE 전환 전에 해소할 증빙

1. 기존 호스트 인계 `GPT_R2_V023_HOST_ONE_SHOT_AND_LIVE_GATE_r0001_20261115.md` §B.4가 기대한 `USAGE_RECEIPT_1.json`은 실제 GitHub `collab/receipts/REQ-COWORK-AUTO-APPROVAL-V023-R2-20261115/`에 **없음**. `RECEIPT_1.md`는 343 B이고 실제 비용이 수록되지 않았음. 호스트는 **모델 재호출 없이**, v0.2.20 운영 계약에서 별도 usage receipt가 필수인지 확인하고, 필수면 DB `REVIEW_COST`와 호출 신원·최종 비용·예산 예약/정산의 비민감 **publish-only 증거**를 기존 경로/계약에 맞게 복구; 아니면 `NOT_REQUIRED_BY_V0220` 근거와 `REVIEW_COST` 비민감 스냅샷을 문서에 적어야 함. 보고된 비용 USD `0.5244525`는 GPT가 DB를 직접 검증하지 못한 **호스트 관측**. 총 USD 3.0 이하라는 비용 보고는 타당하나 원격 영수증 정합성은 미완.
2. MINOR 2↔3 불일치는 리뷰 원문을 유지하고 Windows host 요약 정정 부록 또는 명시적 `COUNT_CORRECTION`으로 해소. 이 항목 때문에 유료 리뷰를 다시 수행하지 말 것.
3. 운영 설치/자동 위임 활성화는 **사용자 이전 조건부 승인 범위 내에서만**, 실제 Windows 호스트의 `BACKUP→OFF 설치→Python 기준 회귀→기존 보류 요청 소급 0/예산·만료·서명 보호→2주기·재시작·롤백/중복/Notifier 확인`이 모두 PASS일 때 실행. 설치 중 기능 OFF 및 `enabled=false` 유지가 기본. 실패·UNKNOWN이면 활성화 중지/원상 복구. 유효한 로컬 보호 승인과 owner-listed scope를 GitHub 문구만으로 추정하지 말 것.

## 현재 상태·다음 한 동작

- `R2_REQUEST/APPROVAL/READY/DISPATCH/REVIEW_RESULT/RECEIPT_1=POSTED`. 정식 R2 모델 호출 1회 완료로 **재요청·재서명·READY 재게시·모델 재호출 금지**.
- **`OPERATING_VERSION=v0.2.20` / `AUTO_SIGNING=OFF`**는 마지막 Windows 호스트 보고 기준. 새 v0.2.23 운영 설치·보호 자동 위임 활성화는 `NOT_RUN`; GPT가 설치를 실행했다고 주장하지 않음.
- **`GPT_R2_STATIC_GATE=PASS`이지만 `LIVE_ACTIVATION=HOLD_PENDING_EVIDENCE_AND_HOST_TESTS`**. 이는 과거 사용자의 조건부 승인 취소·재승인 요구가 아니라 실제 안전 검증 게이트.
- **NEXT_ONE_ACTION:** Windows Claude Code/운영 호스트가 위 두 증빙 불일치와 실제 운영 계약을 **모델 0·publish-only/읽기 전용**으로 정리한 다음, 기존 조건부 승인·보호 로컬 범위가 유효하면 §B.6의 백업·기능 OFF 설치·회귀·보호 활성화를 순차 수행하고, 실제 결과/영수증/롤백 근거를 이 Work에 게시. 어떤 게이트든 실패하면 `BLOCKED/NOT_RUN`으로 남길 것.
