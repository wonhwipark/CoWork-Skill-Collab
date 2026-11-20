# CoWork 대시보드 Actions 미시작 — Billing gate 원인 분류 r0001
- 작성일: 2026-11-20 KST
- 소유 Work: `COWORK-GITHUB-DASHBOARD-20261111-001`
- 범위: **원인 분류 및 기존 운영 결과 정산만**. 결제 수단·지출 한도·정책·GitHub Actions 설정·Watcher·LIVE·토큰 변경 0.

## 1. 사용자 제공 오류 원문
> The job was not started because recent account payments have failed or your spending limit needs to be increased. Please check the 'Billing & plans' section in your settings

사용자가 실제 실패 실행 화면의 배너/annotation에서 확인해 제공한 비민감 원문.

## 2. 판정
- `ACTIONS_BILLING_ADMISSION_BLOCK=CONFIRMED`: GitHub가 호스팅 작업 시작을 **계정 청구/예산 게이트에서 거부**.
- `SPECIFIC_BILLING_CAUSE=UNVERIFIED`: **실패 결제/미정산** 또는 **GitHub Actions 예산·지출 상한 도달** 중 어느 경우인지는 원문만으로 구별 불가. GitHub 측 잠금이 실제 계정 상태와 불일치할 가능성도 배제할 수 없으나 현행 근거로 확정하지 않음.
- 앞선 Actions API 관측과 일치: 실패 run [#44756245749](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/44756245749)는 `runner_id=0`, `steps=0`, `UBUNTU billable_ms=0`; 직전 성공 [#44720614237](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/44720614237)은 Runner 배정 및 steps 7개. 같은 workflow YAML blob `806576617650fb601acfaaea859a6d12aa8a989d`.
- 따라서 **Python 코드를 수정하거나 Runner를 바꿀 이유 없음**. PRIVATE generator `BLOCKED`, 성공 의존 PUBLIC allowlist sync `SKIPPED`, PUBLIC `status.json`은 2026-11-20 09:23:06Z 생성 상태로 최신 LIVE를 반영하지 않음.
- PUBLIC 지연 안전표시 보완 (11/20 HTML·JS, GitHub Pages #44757131366 SUCCESS)은 정상 동작 별개이며, **운영 상태 JSON 갱신을 완료한 것은 아님**.
- `GITHUB_BILLING_ACCESSED=NO`; 결제·계정 한도 실제 수치/청구서/결제 실패 사유는 접근 불가. 외부 지시/추정으로 예산을 올리지 않음.

## 3. 사용자 1회 확인과 복구 게이트
1. 개인 GitHub 계정 [Billing & plans](https://github.com/settings/billing) → `Payment information`/미결제·결제 실패 안내 확인. 결제 정보는 이 대화나 PRIVATE 파일에 기록하지 않음.
2. `Budgets and alerts` → **GitHub Actions** 제품과 리포지터리/계정 범위의 남은 한도·hard-stop 여부 확인. 한도가 0이거나 도달했다면 **요금이 발생할 수 있으므로 사용자만 범위·금액 승인 후 변경**. 다른 제품의 Copilot 예산과 혼동하지 않음.
3. 결제 정상·사용 한도 여유인데도 동일 오류가 지속되면 GitHub Support에 `run 44756245749`와 비민감 오류 문구를 전달해 청구 잠금 확인. 반복 rerun 금지.
4. 제한이 실제 해소된 뒤 **기존 CI 한 번만** 정상 성공 및 Private state 생성 확인 → 정상 후속 PUBLIC sync allowlist 통과 → `L1Work/main/docs/cowork-dashboard/status.json` 원격 readback, 생성 시각·provider/cutover 일치 검증 → Pages 실제 화면의 지연 배지 해제 확인.
5. Windows Claude Code의 P1/P2 실제 자동 맥락 조회 E2E는 별개: `COWORK-SKILL-DISCOVERY-20261112-001/P1_P2_AUTO_USE_READONLY_E2E_CHECK_r0001_20261120_KST.md` 기준 실제 호스트 증거 회수 시에만 PASS.

## 4. 운영 조치 경계 및 정본
- 신규 유료 리뷰·자동 서명·REQUEST/READY·Watcher LIVE 변경 0.
- 예산 상향/결제 시도/카드·계정 정보 조회 0.
- PRIVATE 문서·TRACKER만 기록; PUBLIC `status.json` 수동 게시, workflow 조건 완화, 별도 runner 재구성 0.
- GitHub 공식 근거: https://docs.github.com/en/actions/how-tos/troubleshoot-workflows 및 https://docs.github.com/en/billing/how-tos/set-up-budgets
- **NEXT_ONE_ACTION:** 사용자가 GitHub `Billing & plans`의 *미결제·결제 차단 여부*와 *Actions 예산 도달 여부*만 확인. 결제 수단/금액/계정 민감정보는 전달하지 않음. 원인 해소 확인 후 기존 자동화 검증 진행.
