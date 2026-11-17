# Windows Claude Code — Job-list handoff 독립 리뷰 원샷 실행서 r0002

- 저장소: PRIVATE wonhwipark/CoWork-Skill-Collab, branch main, PR 없이 직접 게시.
- 기존 Work: JOBLIST-NRTX-20261112-001
- 목표: PUBLIC L1Work의 Job-list v0.4.38 복구 현황 handoff에 대한 독립 정적 리뷰 1회와 결과 회수. Linux 호스트 복구/재실행은 범위 밖.
- 상태: NON_EXECUTABLE_HANDOFF. 이 문서는 REQUEST/READY나 유료 호출 권한이 아님.

## 입력 (순서대로)
1. collab/CONTEXT_BRIEF.md와 collab/projects/JOBLIST-NRTX-20261112-001/CURRENT.md 최상단
2. collab/projects/JOBLIST-NRTX-20261112-001/CLAUDE_JOBLIST_V0438_HANDOFF_REVIEW_PREFLIGHT_r0001_20261118_KST.md (대상·8개 리뷰 질문)
3. collab/projects/JOBLIST-NRTX-20261112-001/JOBLIST_V0438_HANDOFF_REVIEW_REQUEST_DRAFT_r0001_20261118_KST.md (비실행 요청 초안)
4. collab/ops/CONTRACTS/REVIEW_TIER_TOKEN_BUDGET_V1.md와 collab/ops/review_request_gate.py
5. Windows 실제 LIVE reviewer.config.json·보호 위임·동일 입력 리뷰 이력 (비밀 값 출력 금지)

## 승인된 범위에서 끝까지 이어갈 순서
1. Windows LIVE v0.2.25 설치 보고를 실제 프로세스/설정으로 재확인. POLICY-STATIC-V1 USD 1.50 맵이 등록됐는지 확인. 보호 위임 max_request_usd=1.00은 변경되기 전까지 유효한 경계로 취급.
2. Windows 실제 config로 읽기 전용 게이트 select --intent skill --required-budget-usd 1.50 실행. POLICY_COMPATIBLE_NOT_APPROVED가 아니면 BLOCKED_PREPUBLICATION·모델 호출 0.
3. 호환되면 고정 PUBLIC 원문(commit fb2e0d3e4cad67c3b3759b1d82d41731036aef2b, blob 211d3b082f859dd80c5e8177e85c96e2c5c202df, SHA-256 2cbf73b2caa3c35f15f270ec4fcbd061b14cd88118616f7380d4e2514facec54), r0001 리뷰 질문, 기존 비민감 근거만 포함하는 정적 REVIEW_INPUT ZIP 준비. CRC·파일별 해시·안전성 검사.
4. DRAFT에 실제 ZIP 크기/SHA를 반영해 로컬 임시 SUBMITTED REQUEST로 만들고 게이트 check 실행. PASS_PREPUBLICATION_ONLY이면 그 동일 바이트로 commit A (ZIP/REQUEST), 원격 readback·source SHA/크기 검증 → SOURCE_PIN JSON repo_id 문자열 생성·검증.
5. 기존 approve_request.py check로 이번 ID·프로젝트·스킬·금액 USD 1.50·만료·중복·유효 보호 위임 검사. 자동 위임 USD 1.00을 우회하지 말고, 별도로 유효한 수동 USD 1.50 승인 권한이 있을 때만 서명·READY를 마지막에 게시. 유효 범위 없다면 BLOCKED_APPROVAL·모델 호출 0·기존 Work에 차단 사유 기록.
6. 승인된 READY가 존재할 때만 watcher를 통해 독립 Claude 정적 리뷰 최대 1회. 중복·불확실 상태면 절대 재호출하지 않음. 리뷰 결과·영수증·실제 비용·입력 SHA 원격 readback 뒤 CURRENT/TRACKER 최소 갱신.
7. 원격 게시 실패는 동일 리뷰 결과의 게시 재시도만 허용. 모델·Job·Watcher/LIVE 재실행 금지. 운영 MCP/DB/키/서비스/코드/Job-list ZIP/Public 원문 모두 불변.

## 리뷰 품질
- ACTIVE, DONE/SUCCESS와 분석 Worker 도달·CODE_FACTS/MSC 완료를 혼동하지 않는지.
- RESULT_UNSUPPORTED와 allowlist/Registry/Bootstrap 9/6/5의 미확인 계약을 과장하지 않는지.
- 모바일 Agent READ/PLAN 미지원 경계와 Linux 로컬 Job-list 실행 가능성을 구분하는지.
- GitHub PAT 401 원인 분리, 회사 제한 자료·토큰·호스트 정보 유출 위험, 소비 Job 중복 실행 방지.
- 근거 없는 개선 확장 강제 금지; 결함 0개라도 허용. ACCEPT/ACCEPT_WITH_CHANGE/REVISE/HOLD, 근거·심각도·최소 보완·검증 수준을 한국어 보고.

## 최종 보고 항목
HOST_LIVE_POLICY / REVIEW_INPUT_ZIP_BYTES_SHA / PREFLIGHT / FORMAL_REQUEST / SOURCE_PIN / APPROVAL_SIG / READY / MODEL_CALLS / REVIEW_RESULT / RECEIPT / COST_USD / NEXT_ONE_ACTION.

독립 리뷰 완료 영수증이 없으면 완료 주장 금지. 승인 밖 운영 변경·모델 호출은 차단하고 가능한 문서·시험은 계속 진행.
