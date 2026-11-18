# Claude 독립 설계 리뷰 최신 인계 r0002 — Linux Workspace 전체 URL 뷰어

- Work: `L1-WORKSPACE-RAG-20261111-001`, GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`.
- 최신 요구: 업무 네트워크 내 전체 Workspace 트리 탐색, 파일별 on-demand 렌더링. **Markdown 원본을 전량 HTML 파일로 사전 변환하지 않음**. 개별 Work 공유 allowlist는 기본에서 제외. 시스템 자격정보 보호와 외부 인터넷 노출 차단은 유지.
- 최신 설계: `collab/projects/L1-WORKSPACE-RAG-20261111-001/L1_WORKSPACE_FULL_TREE_WEB_RENDER_VIEWER_DESIGN_DELTA_r0002_20261118_KST.md`.
- **새 고정 리뷰 입력**: `collab/packages/l1-workspace-local-viewer-design_r0002_1118_REVIEW_INPUT.zip`, 91,324 bytes, SHA-256 `6a013a104ebfefeae6dc452965ce99ce5a3f9637ed538c778d8cb5189d5a7e5f`. 기존 r0001 리뷰 ZIP 변경 없음.
- 최신 입력 manifest: `collab/projects/L1-WORKSPACE-RAG-20261111-001/review-inputs/REQ-L1-WORKSPACE-LOCAL-VIEWER-DESIGN-R1-20261118/REVIEW_MANIFEST_r0002.md`.
- 리뷰 범위: r0001 R01~R22 + 최신 R23~R27을 **독립 설계 리뷰 1회**로 묶어 판단. 이전에 완료된 다른 리뷰는 재실행하지 않음.
- **운영 preflight 판정**: `PREFLIGHT_BLOCKED / POLICY_COST_MISMATCH` (실제 최소 정책 USD 1.50, 자동 승인 위임 USD 1.00). 결과: `collab/projects/L1-WORKSPACE-RAG-20261111-001/CLAUDE_L1_WORKSPACE_LOCAL_VIEWER_DESIGN_REVIEW_PREFLIGHT_BLOCKED_FOR_GPT_20261118.md`.
- **현재 상태**: 정식 REQUEST/SOURCE_PIN/서명/READY/유료 Claude 리뷰 모두 `NOT_RUN`. 이번 설계 변경 동의는 USD 1.50 또는 3.00 유료 리뷰 승인이나 운영 위임 설정 변경 승인이 아님.
- **다음 동작**: 사용자 유료 리뷰 예산이 명시적으로 승인된 경우 Windows Claude Code가 동일 요청 ID에 대해 최신 ZIP·실제 설정·정책·중복/UNCERTAIN·한도 검증 → 유효한 기존 signer/수동 승인 경로 → READY 마지막 게시 → Claude 독립 리뷰 1회 → 결과/영수증 게시. 실패 시 HOLD/모델 호출 0. 무단 재큐잉 금지.
- GPT는 실제 결과·영수증을 판정한 뒤 업무 GPT용 최종 제안·작업 지시서를 `wonhwipark/L1Work/main/handoffs/`에 게시한다. Linux 실제 설치/웹 노출/Git authority 변경은 별도 게이트.
