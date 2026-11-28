---
schema: SKILL_COLLAB_REVIEW_REQUEST_V1
state: SUBMITTED
request_id: REQ-L1-VIEWER-SKILL-MANAGEMENT-DESIGN-R1-20261128
request_revision: 1
project_id: L1-WORKSPACE-RAG-20261111-001
work_id: L1-WORKSPACE-RAG-20261111-001
skill_id: l1-knowledge-updater
package_path: /SKILL-COLLAB/packages/l1_viewer_skill_management_design_r0001_1128_REVIEW_INPUT.zip
package_file_id: github:REQ-L1-VIEWER-SKILL-MANAGEMENT-DESIGN-R1-20261128
package_rev: l1-viewer-skill-management-detailed-design-r0001
package_sha256: 0d755b787468af4567484805256ff6a3cb3625d80924fa4cc6bdabdfdcc0b509
package_size_bytes: 27372
baseline_package_ref: null
knowledge_refs: []
consumer_profiles: [l1-workspace-viewer, skill-updater, job-list, work-ledger-kernel]
reviewer_os: WINDOWS
test_policy: STATIC_ONLY
run_policy_ref: POLICY-STATIC-V1
output_contract: SKILL_COLLAB_REVIEW_RESULT_V1
goal: one independent static architecture and detailed design review of Viewer Operations Skill Management read-only integration
---

# Viewer 운영 관리 Skill Management 상세 설계 — 독립 리뷰 R1

사용자 명시 요청: 실제 원본 근거 기반 상세 설계 완료 후 정식 **독립 설계 리뷰 1회**. 기존 Work `L1-WORKSPACE-RAG-20261111-001` 재사용. 동일 RID 재서명/재실행 및 자동 R2 금지.

고정 ZIP은 실제 [상세 설계 r0001](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/82fc282df1637dc22a11d03d888044e23481f2c7/collab/projects/L1-WORKSPACE-RAG-20261111-001/L1_VIEWER_OPERATIONS_SKILL_MANAGEMENT_DETAILED_DESIGN_r0001_20261128_KST.md)와 리뷰 안내 MD 두 파일을 포함. **상세 설계 원문 SHA-256**: `f9940f72a2f2a4f3304f451eaf728915ffc198905a0b5f32588d4e9c5c5ac8e6`; **리뷰 ZIP SHA-256**: `0d755b787468af4567484805256ff6a3cb3625d80924fa4cc6bdabdfdcc0b509`.

## 리뷰 필수 질문
1. v0.5.8 Viewer의 existing router/adapter와 운영관리 메뉴 설계 충돌·변경범위 과다/부족, Source Map/Knowledge/Recovery/Work Write 보호.
2. Skill Updater·Job-list·Runner/Kernel/MCP 실제 제공 책임을 침범하는지; 새 Collector·DB/API 없이 가능한 최소 구현 구조.
3. 설치/활성/공개 버전, 서로 다른 호스트, digest·source pin, Job/Run/Receipt 존재/성공, stale·partial·권한 거절을 서로 혼동하는 반례.
4. Linux host/사용자 ACL, URL·HTML escaping/XSS, path traversal, leakage of work source/credentials, read-only 사용자 화면 노출 위험.
5. G0 현장 계약 미확인을 무리하게 구현 확정했다고 가정하는 지점, 선결 확인 자료와 안전한 fail-closed 기준.
6. SM-01~SM-20 시험의 핵심 coverage, 구현·통합·운영시험 경계 및 롤백·호환성.

**검토 출력:** 한국어. ACCEPT / ACCEPT_WITH_CHANGE / REVISE / HOLD와 BLOCKING/MAJOR/MINOR별 설계 절, 구체 반례, 권장 최소 수정, 소유자, 재현 수락시험. A안(UI+기존 read adapter) 대 B안(입증된 최소 read projection 확장) 비교 및 선결 G0 한 행동.

**한계 고지:** 공개 패키지 인계 및 기존 문서의 실제 내용은 검토했으나 Viewer v0.5.8의 ZIP 내부 전체 함수·실제 업무 Linux 설치본/권한·MCP 서버 API는 검증하지 못함. 리뷰어도 ZIP에 없는 원본/호스트의 구현 사실을 단정하지 말 것. 회사 소스·민감 로그는 입력 패키지에 없음.

보호된 signer/승인 정책/READY/Watcher 유효성 검증 이후만 유료 Claude 리뷰 실행 가능. **이 REQUEST 게시 자체는 READY·승인 서명이 아님**. 실제 리뷰 영수증·결과가 없는 한 미완료. 실제 Linux 설치/Job/분석·기존 운영 스킬 변경 금지.
