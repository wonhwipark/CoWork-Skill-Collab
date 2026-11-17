# Job-list v0.4.38 handoff — 비실행 정식 리뷰 REQUEST 초안

- 상태: NON_EXECUTABLE_DRAFT / NOT_SUBMITTED. 이 파일은 collab/requests 내 정식 REQUEST가 아니므로 watcher 실행 신호가 아니다.
- 기존 Work: JOBLIST-NRTX-20261112-001
- 요청 ID 후보: REQ-JOBLIST-V0438-HANDOFF-R1-20261118. Windows에서 같은 입력/범위의 기존 REQUEST·READY·영수증·불확실 이력을 먼저 확인.
- 대상: PUBLIC wonhwipark/L1Work, commit fb2e0d3e4cad67c3b3759b1d82d41731036aef2b, handoffs/JOBLIST_V0438_MCP_RECOVERY_STATUS_HANDOFF_r0001_20261117_KST.md
- 원문 blob: 211d3b082f859dd80c5e8177e85c96e2c5c202df
- 원문 SHA-256: 2cbf73b2caa3c35f15f270ec4fcbd061b14cd88118616f7380d4e2514facec54
- 리뷰 질문 및 근거: 기존 CLAUDE_JOBLIST_V0438_HANDOFF_REVIEW_PREFLIGHT_r0001_20261118_KST.md
- 제안 정책: skill, POLICY-STATIC-V1, USD 1.50, 모델 호출 최대 1회. LIVE 실제 설정/보호 위임에서 확인 전 확정 금지.

## 임시 REQUEST YAML 내용(실제 게시/실행 금지)

    ---
    schema: SKILL_COLLAB_REVIEW_REQUEST_V1
    state: DRAFT_NOT_SUBMITTED
    request_id: REQ-JOBLIST-V0438-HANDOFF-R1-20261118
    request_revision: 1
    project_id: JOBLIST-NRTX-20261112-001
    work_id: JOBLIST-NRTX-20261112-001
    skill_id: job-list
    package_path: /SKILL-COLLAB/packages/joblist_v0438_handoff_r1_1118_REVIEW_INPUT.zip
    package_file_id: github:REQ-JOBLIST-V0438-HANDOFF-R1-20261118
    package_rev: handoff-r0001-static-review
    package_sha256: REPLACE_WITH_REAL_ZIP_SHA256
    package_size_bytes: REPLACE_WITH_REAL_ZIP_BYTES
    baseline_package_ref: null
    knowledge_refs: []
    consumer_profiles: [joblist-handoff-static-review]
    reviewer_os: WINDOWS
    test_policy: STATIC_ONLY
    run_policy_ref: POLICY-STATIC-V1
    output_contract: SKILL_COLLAB_REVIEW_RESULT_V1
    goal: one independent static review of the pinned Job-list v0.4.38 MCP recovery status handoff
    ---

## 진행 조건

1. Windows 실제 reviewer.config.json에 대해 review_request_gate.py select --intent skill --required-budget-usd 1.50 실행.
2. 비민감 공개 handoff 원문 + 고정 리뷰 질문 + 최소한의 기존 PRIVATE 근거로 REVIEW_INPUT ZIP을 만들고 실제 SHA-256·바이트·CRC·경로·민감정보를 검사.
3. 이 DRAFT를 로컬 임시 REQUEST.md로 복사해 state: SUBMITTED 및 package_sha256/package_size_bytes 실제 값을 넣은 후 review_request_gate.py check를 로컬에서 실행. PASS_PREPUBLICATION_ONLY 이전에는 정식 REQUEST 및 ZIP을 게시하지 말 것.
4. PASS 이후 commit A로 정식 REQUEST와 ZIP을 게시, 원격 바이트 고정 후 SOURCE_PIN repo_id를 문자열로 검증, 보호된 approve_request.py check, 유효 서명과 READY 마지막 게시.
5. Windows v0.2.25 실제 설치 보고와 일반 정책 USD 1.50는 자동 승인 보증이 아님. 마지막 확인된 보호 위임은 max_request_usd=1.00. USD 1.50 수동 권한이 실제 유효하지 않다면 BLOCKED_APPROVAL, 모델 호출 0; 자동 위임/키/DB 수정 금지.
6. 리뷰 1회·결과와 영수증 원격 readback → GPT 판정. 동일 Job-list 실행·운영 MCP 변경·유료 재호출 금지.

## 결과 경로(실제 승인·리뷰 수행 시에만)
- collab/reviews/REQ-JOBLIST-V0438-HANDOFF-R1-20261118/REVIEW_RESULT_1.md
- collab/receipts/REQ-JOBLIST-V0438-HANDOFF-R1-20261118/RECEIPT_1.md
- collab/dispatch/REQ-JOBLIST-V0438-HANDOFF-R1-20261118/DISPATCH_1.md

NEXT_ONE_ACTION: Windows Claude Code가 실제 LIVE 정책 select를 먼저 수행해 신규 정식 요청 사전검증 가능성을 판정.
