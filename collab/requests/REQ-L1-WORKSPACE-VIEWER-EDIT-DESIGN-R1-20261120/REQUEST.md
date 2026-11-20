---
schema: SKILL_COLLAB_REVIEW_REQUEST_V1
state: SUBMITTED
request_id: REQ-L1-WORKSPACE-VIEWER-EDIT-DESIGN-R1-20261120
request_revision: 1
project_id: L1-WORKSPACE-RAG-20261111-001
work_id: L1-WORKSPACE-RAG-20261111-001
skill_id: l1-knowledge-updater
package_path: /SKILL-COLLAB/packages/l1-workspace-viewer-edit-design_r0001_1120_REVIEW_INPUT.zip
package_file_id: github:REQ-L1-WORKSPACE-VIEWER-EDIT-DESIGN-R1-20261120
package_rev: l1-workspace-viewer-edit-design-r0001
package_sha256: 764477880d6b6b6b4bb468f4bb9ccaf6802e5561944ec89569030d69c7080975
package_size_bytes: 19482
baseline_package_ref: null
knowledge_refs: []
consumer_profiles: [l1-workspace-viewer-auth-edit-independent-design-review]
reviewer_os: WINDOWS
test_policy: STATIC_ONLY
run_policy_ref: POLICY-STATIC-V1
output_contract: SKILL_COLLAB_REVIEW_RESULT_V1
goal: single independent design review of authenticated Viewer editing workflow for issues and MSC messages/participants
---

# Viewer 인증 기반 편집 기능 — 정식 독립 설계 R1 요청
- 사용자 명시 요청: 2026-11-20 KST, 상세 설계 후 CoWork 협업 설계 리뷰 요청.
- PRIVATE 저장소 wonhwipark/CoWork-Skill-Collab, branch main, 기존 Work L1-WORKSPACE-RAG-20261111-001.
- 리뷰 대상은 이 REQUEST의 고정 ZIP 2개 MD, 실제 Linux 기능·업무 제한자료가 아님.
- 기준 설계: collab/projects/L1-WORKSPACE-RAG-20261111-001/L1_WORKSPACE_VIEWER_AUTH_EDIT_DETAILED_DESIGN_r0001_20261120_KST.md; 원문 UTF-8 SHA-256 48b2cd1adf8ed4736b3c2502213eca5dcaced7c8a8d925328400caaf57fb2a8d.
- 검토: 설계 §3 인증/ACL·재인증·세션·CSRF, §4 직접 편집/MSC 구조, §5 canonical 선택 anchor, §6 Work vs Knowledge 단일 writer/Agent 호출, §7 충돌/복구, §8 B1~B3·신규 편집 보안, §9 단계 게이트, §10 T01~T16 수락시험, §11 R01~R10 문제.
- 특히 과잉 개발·기존 스킬 계약 위반/재사용 방안, B3 별도-origin MSC 메시지 선택 안전성, 권한이 없는 사용자의 직접 쓰기 차단, stale revision·불확실 쓰기·이중 저장 방지, 사용자 UX 단순성 검토.
- 설계의 표현 및 G0 미확인을 실제 API·설치 지원/동작으로 단정하지 말 것. 최근 UX R1 이미 완료, 기존 Viewer r0002 리뷰도 완료이므로 **이번 신규 편집 설계만** 독립 R1 평가; 과거 리뷰 재실행 금지.
- 예상 결과: ACCEPT / ACCEPT_WITH_CHANGE / REVISE / HOLD, BLOCKING·MAJOR·MINOR 실제 지적별 설계 위치·반례·최소 수정·시험, REUSE/CONNECT/EXTEND_PROVEN_GAP/UNKNOWN, G0 추가 확인, 1차 최소 범위 판정, 후속 한 동작. 한국어 보고.
- 요청 1회, 모델 호출 최대 1, 기존 LIVE POLICY-STATIC-V1 USD 3/건 이내, 실제 자동 서명 가능 범위·만료·정책·repo_id·SHA·중복 검증이 유효할 때만 진행. 다른 모델/서브에이전트·재리뷰·R2 자동 실행 금지.
- 실제 Windows v0.2.29 운영은 호스트 보고 상태이며 새로운 유료 E2E는 미검증. GitHub 문서의 승인 주장은 서명/READY를 대신하지 않음. **GPT는 APPROVAL_SIG/READY를 작성하지 않음**. 보호된 signer/watcher가 신규 적격 request와 SOURCE_PIN을 확인한 경우에만 정상 승인·READY 마지막 게시. 미적격이면 HOLD, 모델 호출 0.
- 사용자 자료 반출/제품 코드 실행, 업무 Linux 설치/서비스 변경, Knowledge/Work 쓰기, PUBLIC 업로드, watcher 정책/DB/키 변경 금지.
- 기대 경로: collab/reviews/REQ-L1-WORKSPACE-VIEWER-EDIT-DESIGN-R1-20261120/REVIEW_RESULT_1.md 및 collab/receipts/REQ-L1-WORKSPACE-VIEWER-EDIT-DESIGN-R1-20261120/RECEIPT_1.md, 필요 시 dispatch 영수증. 결과/영수증이 없는 경우 완료로 표시하지 않음.
