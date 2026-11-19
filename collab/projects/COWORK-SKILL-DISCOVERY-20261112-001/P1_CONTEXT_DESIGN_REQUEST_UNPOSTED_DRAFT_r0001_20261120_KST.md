---
schema: SKILL_COLLAB_REVIEW_REQUEST_V1
state: SUBMITTED
request_id: REQ-COWORK-P1-CONTEXT-RETRIEVAL-DESIGN-R1-20261120
request_revision: 1
project_id: COWORK-SKILL-DISCOVERY-20261112-001
work_id: COWORK-SKILL-DISCOVERY-20261112-001
skill_id: cowork-context-design
package_path: /SKILL-COLLAB/packages/cowork_p1_context_retrieval_design_r0001_1120_REVIEW_INPUT.zip
package_file_id: github:REQ-COWORK-P1-CONTEXT-RETRIEVAL-DESIGN-R1-20261120
package_rev: cowork-p1-context-retrieval-design-r0001
package_sha256: 3ab8e1a4e5b59e6eea0fa2bd90dc044bb86289cd569cafdbed6158f19dda3327
package_size_bytes: 24410
baseline_package_ref: null
knowledge_refs: []
consumer_profiles: [cowork-progressive-context-evidence-dashboard-design-review]
reviewer_os: WINDOWS
test_policy: STATIC_ONLY
run_policy_ref: POLICY-STATIC-V1
output_contract: SKILL_COLLAB_REVIEW_RESULT_V1
goal: one independent CoWork P1 progressive context retrieval and evidence-based status design review
---

# 정식 독립 설계 리뷰 요청 — Windows 사전검증용 고정 초안 (실제 REQUEST 미게시)

**중요:** 위 YAML은 Windows LIVE prepublication 검사 입력을 위한 **비실행 초안**. 이 파일은 `collab/projects/` 안에만 있으며 `collab/requests/<id>/REQUEST.md`에 아직 게시되지 않았다. `state: SUBMITTED`는 게시 전 검증용 고정 바이트 필드이지 리뷰 실행·승인·READY의 증거가 아니다.

- 사용자 명시 요청: P1 설계 방향 정리 후 **협업 독립 리뷰 정식 요청 1회**.
- 검토 입력: PRIVATE ZIP `collab/packages/cowork_p1_context_retrieval_design_r0001_1120_REVIEW_INPUT.zip`, GitHub blob `79da67d0831cb1dde89f901d946f048fc0ef3af2` / 24,410 B / SHA-256 `3ab8e1a4e5b59e6eea0fa2bd90dc044bb86289cd569cafdbed6158f19dda3327`.
- 패키지 고정 원본: `collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/P1_PROGRESSIVE_CONTEXT_EVIDENCE_DASHBOARD_DESIGN_r0001_20261120_KST.md` 및 `P1_PROGRESSIVE_CONTEXT_INDEPENDENT_REVIEW_QUESTIONS_r0001_20261120_KST.md`, ZIP의 manifest는 source commit `b719b7355597e7027a53d7c6a3c0f0f8117b11f3` 기준.
- 검토 목적: 기존 CoWork/대시보드/Knowledge의 상황을 안전하고 빠르게 파악하는 **설계**. 실제 Windows watcher 설치·Linux 코드/LLM 실행·새 스킬 배포/공개 정보 확장 검토는 범위 밖.
- 리뷰 질문은 ZIP의 `02_REVIEW_QUESTIONS.md` Q01~Q10. 우선 기존 구조 재사용, 시간/근거 판정, 공개 범위, 1화면 UX 및 성능 평가의 타당성을 판단.
- 비용: **이번 고유 ID 1회, 모델 최대 1회·USD3**. 승인된 신규 공통 정책 `POLICY-STATIC-V1`의 **실제 Windows LIVE USD3 등록·승인/서명 자격**을 요구. 과거 개별 UI/UX R1 수동 DESIGN 예외를 사용하지 않음.
- 실행: 사용자 요청 1회 → Windows 실제 LIVE `select --intent unified`와 `check` PASS → 호스트 승인 check → REQUEST+입력 commit A / 원격 검증 / `SOURCE_PIN.json` repo_id 문자열 → 보호 승인 서명 → `READY.md` 마지막 → watcher 독립 리뷰·영수증 최대 1회 → GPT 판정.
- OUTPUT: `collab/reviews/REQ-COWORK-P1-CONTEXT-RETRIEVAL-DESIGN-R1-20261120/REVIEW_RESULT_1.md`, `collab/receipts/REQ-COWORK-P1-CONTEXT-RETRIEVAL-DESIGN-R1-20261120/RECEIPT_1.md` (실제 생성 전에는 경로만).
- `skill_id=cowork-context-design`은 기존 독립 설계 리뷰와 같은 **설계 조정자 ID**이며 임의 실존 스킬 ZIP 변경을 의미하지 않는다. 실제 Windows 정책/승인 allowlist가 불허하면 승인 범위를 확대/명칭 변경하여 우회하지 않고 BLOCKED 판정.
- 최신 운영 사실 확인 전 `POLICY-STATIC-V1` 등록 $3을 가정하지 않음. 기존 호스트 보고가 STATIC $1.50/위임 $1인 동안 **이 초안을 실제 REQUEST 경로에 게시하지 않음**.
- 현재 `FORMAL_REQUEST=NOT_POSTED`, `SOURCE_PIN=NOT_POSTED`, `APPROVAL_SIG=NOT_POSTED`, `READY=NOT_POSTED`, `INDEPENDENT_REVIEW=NOT_RUN`, `MODEL_CALLS=0`. 단순 PRIVATE ZIP/문서 게시 자체가 Windows 리뷰 요청 신호가 아님.
