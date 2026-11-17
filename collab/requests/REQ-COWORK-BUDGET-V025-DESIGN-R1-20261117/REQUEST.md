---
schema: SKILL_COLLAB_REVIEW_REQUEST_V1
state: SUBMITTED
request_id: REQ-COWORK-BUDGET-V025-DESIGN-R1-20261117
request_revision: 1
project_id: COWORK-AUTO-APPROVAL-20261115-001
work_id: COWORK-AUTO-APPROVAL-20261115-001
skill_id: cowork-review-watcher
package_path: /SKILL-COLLAB/packages/skill-collab-watcher_v0_2_25_1117.zip
package_file_id: github:REQ-COWORK-BUDGET-V025-DESIGN-R1-20261117
package_rev: v0.2.25
package_sha256: 26d63c8a03290499b13b2ceb8ff0b70c06eb1b1bcc1a25fe3d8f65fcc213d228
package_size_bytes: 283930
baseline_package_ref: skill-collab-watcher_v0_2_23_1115_DEV_NOT_FOR_DEPLOYMENT.zip SHA256=f941be8a6b53d00baa10a9b097f234b159470e2aa1242ecc33bcf0bdee080ea7
knowledge_refs: []
consumer_profiles: [windows-single-user-watcher]
reviewer_os: WINDOWS
test_policy: STATIC_ONLY
run_policy_ref: POLICY-STATIC-V1-DESIGN
output_contract: SKILL_COLLAB_REVIEW_RESULT_V1
goal: independent R2 design and security code review of CoWork watcher v0.2.25 per-review budget changes
---

# Windows Claude Code — v0.2.25 자동 승인 비용 정책 R2 독립 리뷰 요청

**요청 목적:** GPT가 개발한 `skill-collab-watcher v0.2.25`의 디자인·보안·상태 계약 및 코드 변경을 독립 검토. 사용자 최신 비용 정책은 일반 스킬 리뷰 건당 USD 1.50, 디자인 리뷰 건당 USD 3.00, 일·월 횟수/누적비용 제한 없음. 이번에는 비용 승인 엔진의 설계·보안 경계를 검토하는 **R2 디자인 리뷰 1회 / `POLICY-STATIC-V1-DESIGN` / 최대 USD 3.00**. 일반 스킬 R1에 대한 일괄 $3 승격 또는 새 비용 승인으로 해석 금지.

**읽을 순서와 고정 범위:** PRIVATE `wonhwipark/CoWork-Skill-Collab/main`의 본 REQUEST 및 `collab/packages/skill-collab-watcher_v0_2_25_1117.zip`(283930 B, SHA-256 `26d63c8a03290499b13b2ceb8ff0b70c06eb1b1bcc1a25fe3d8f65fcc213d228`)을 우선 검증. 같은 Work의 [최신 정책](../../projects/COWORK-AUTO-APPROVAL-20261115-001/GPT_AUTO_REVIEW_BUDGET_POLICY_r0002_20261117_KST.md), [R2 독립 리뷰 상세 인계](../../projects/COWORK-AUTO-APPROVAL-20261115-001/CLAUDE_V025_BUDGET_POLICY_INDEPENDENT_REVIEW_HANDOFF_r0001_20261117_KST.md), 개발 브랜치 `dev/auto-review-budget-policy-20261117`의 `dev/build_v025_review_budgets.py` 및 `dev/patch_v025_budget_tests.py`를 대조. v0.2.23 원본 SHA `f941be8a6b53d00baa10a9b097f234b159470e2aa1242ecc33bcf0bdee080ea7` 및 v0.2.24 SHA `3c78699b734d88202a34ef5fd430f5f278ab1692a437b6affb6b6c64d24ca360`은 비교 원본. 버전·바이트 불일치 시 모델 호출 0으로 보류.

## 독립 확인할 핵심 질문

1. **비용 권한 경계:** 등록된 `run_policy_ref`만 선택 가능하고 REQUEST의 금액 조작이 불가능한가? 보호 위임 `max_request_usd`가 USD 1/1.5이면 $3 디자인 리뷰가 fail-closed 되는가? 잘못된 금액·무한대·NaN·타 프로젝트·만료/취소 시 signer/READY/호출 0이 유지되는가?
2. **상한 제거 완전성:** `auto_policy.assess`, `auto_approval.py`, `state_store.auto_claim`, `orchestrator._check_ceilings`, `state_store.claim`, `Config.load` 어디에도 일·월 횟수/누적 비용 거절이 남지 않았는가? 과거 실패 예약이 타 REQUEST를 차단하지 않으면서 동일 ID의 불확실 실행 재시도는 금지되는가?
3. **정확히 한 번 & 서명 보안:** 동시성·예약/디스패치 레이스, DB/원격 영수증·RESUME, SOURCE_PIN repo_id 문자열, ZIP CRC/경로 이탈·Git commit 고정, Ed25519 승인, READY 마지막, provider 단일 LIVE 경계를 보존하는가?
4. **실제 건당 제한:** locally registered `POLICY-STATIC-V1`(1.5)와 `POLICY-STATIC-V1-DESIGN`(3.0)이 `--max-budget-usd`로 전달되는가? 예산 초과/CLI 실패는 정직한 FAILED/UNCERTAIN이며 무단 자동 재호출이 없는가? 사용자 금액 향후 변경 시 원격 텍스트만으로 보호 위임 우회가 가능한가?
5. **회귀 증거의 한계:** [CI #44011874422](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/44011874422) Linux 29 PASS/2 SKIP 표적 및 582 PASS/30 SKIP/1 선택 제외, 원격 ZIP SHA 재확인은 자체시험일 뿐. Windows 전용 테스트/실서명/LIVE 적용 여부를 독립적으로 구분하고, 부족한 경우 최소 수정·추가 시험을 제시.

**보고:** 명확히 확인한 BLOCKING/MAJOR/MINOR와 개선 제안 분리, 관련 파일/함수·재현 조건·근거·최소 변경·검증. 결함 수를 강제하지 않음. `ACCEPT / ACCEPT_WITH_CHANGE / REVISE / HOLD`, `INDEPENDENT_REVIEW=PASS/FAIL/NOT_RUN`과 확인하지 못한 범위를 구분. 요청당 **모델 호출 1회**, 하위 유료 Agent·추가 review 자동 호출 금지. 과거 요청의 재큐잉 금지.

## 보호 승인 / 실행 조건

이 REQUEST는 **GitHub 게시 자체로 승인·서명·READY를 대체하지 않음**. 실제 Windows 호스트의 **현재 유효한 보호 위임·로컬 등급 등록·허용 프로젝트/스킬·금액·만료·서명자**가 $3 디자인 등급을 허용하는 경우에만 기존 보호된 자동 서명 절차가 `APPROVAL_SIG.json`·`READY.md`를 마지막에 게시할 수 있음. **현재 LIVE v0.2.23은 기존 자동 위임 USD 1/건·`POLICY-STATIC-V1`만 허용한다고 보고되어 본 새 DESIGN tier는 자동 실행 대상이 아님.** 이를 우회하려고 다른 tier로 대체하거나 기존 제한을 임의 수정하지 말 것. Windows Claude Code에서 격리 검증은 기존 승인된 호스트 접근 범위 안에서 별도 진행 가능하지만 이 문서로 LIVE/키/DB/Task/Notifier·PUBLIC 운영 변경 금지.

예상 정식 결과 경로는 `collab/reviews/REQ-COWORK-BUDGET-V025-DESIGN-R1-20261117/REVIEW_RESULT_1.md`, `collab/receipts/REQ-COWORK-BUDGET-V025-DESIGN-R1-20261117/RECEIPT_1.md`. **실제 READY·비용·리뷰를 관측하기 전까지 PENDING/NOT_RUN.**

개발 자체검토와 독립 코드를 구분하고 기존 같은 Work `CURRENT.md`에 최종 결과·SHA·다음 한 조치를 보고할 것.
