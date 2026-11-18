# Windows Claude Code — Local Workspace Viewer r0002 정식 요청·한정 승인·요청 후 설정 정리 원샷

- GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`.
- Request ID: `REQ-L1-WORKSPACE-LOCAL-VIEWER-DESIGN-R1-20261118`, revision 1; Work: `L1-WORKSPACE-RAG-20261111-001`.
- **사용자 최신 명시 승인:** 2026-11-18 KST 채팅 “진행해줘. 요청후 한도관련설정 삭제해줘” = **이번 Claude 독립 설계 리뷰 1회, 요청당 최대 USD 1.50**. 사용자에게 **동일 비용 승인을 다시 요청하지 않는다**. 이 문서는 동의·인계 증빙이지 서명키/APPROVAL_SIG·정식 REQUEST 아님.
- **현재 입력은 이미 준비됨:** `collab/packages/l1-workspace-local-viewer-design_r0002_1118_REVIEW_INPUT.zip`, 91324 bytes / SHA-256 `6a013a104ebfefeae6dc452965ce99ce5a3f9637ed538c778d8cb5189d5a7e5f` / git blob `dcb42fca58f5cd5c281fc3622fc6e6bfccb02285`. r0001 ZIP 불변.
- **실행 전 REQUEST 바이트 고정 초안(저장소 경로 중요):** `collab/projects/L1-WORKSPACE-RAG-20261111-001/REQUEST_PREFLIGHT_DRAFT_LOCAL_VIEWER_R0002_150USD_20261118.md`. **watcher가 감시하는 `collab/requests/<ID>/REQUEST.md`와 다른 경로이므로 아직 정식 접수가 아님**.
- 최신 설계 `collab/projects/L1-WORKSPACE-RAG-20261111-001/L1_WORKSPACE_FULL_TREE_WEB_RENDER_VIEWER_DESIGN_DELTA_r0002_20261118_KST.md`; 최신 리뷰 질문 R01~R27, 테스트 T01~T34.
- 과거 Windows `review_request_gate.py select --intent skill --required-budget-usd 1.00`은 `POLICY_COST_MISMATCH`; 실제 LIVE v0.2.25 기본 `POLICY-STATIC-V1` USD 1.50 등록 호스트 보고(사전 실행 근거 `CLAUDE_L1_WORKSPACE_LOCAL_VIEWER_DESIGN_REVIEW_PREFLIGHT_BLOCKED_FOR_GPT_20261118.md`). 과거 $1.00 설정을 고집하여 재차 차단하지 말고 정확히 $1.50를 선택하되 최신 운영 설치본을 **지금 다시 확인**.

## 순차 실행 — 묶어서 끝까지, 단일 LIVE watcher만

1. `collab/CONTEXT_BRIEF.md`, Work `CURRENT.md`, 최신 승인/정책 `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/CURRENT.md`, 이 문서를 확인. Windows 현재 실제 LIVE provider/version, 보호 설정, 사용자 승인 범위, 유효 signer/만료, 동일 ID의 REQUEST/PIN/SIG/READY/review/receipt 및 Windows DB의 동일 logical request·UNCERTAIN를 **read-only** 확인. 이미 처리·실행·불확실하면 재요청/모델 재호출 없이 증빙 정리만.
2. **Prepublication gate (모델/쓰기 0):** 최신 설치 `reviewer.config.json`과 exact ZIP 바이트로 `python collab/ops/review_request_gate.py select --live-config <실제 Windows LIVE config> --intent skill --required-budget-usd 1.50` → `POLICY_COMPATIBLE_NOT_APPROVED`, `selected_run_policy_ref=POLICY-STATIC-V1`, `1.50`. 위 고정 REQUEST draft 원본 바이트를 로컬 검증 파일로 복사해 `python ... review_request_gate.py check --live-config <실제 Windows LIVE config> --intent skill --required-budget-usd 1.50 --request <실제 임시 REQUEST 파일> --package <정확한 r0002 ZIP>` → `PASS_PREPUBLICATION_ONLY`, raw request_sha256/ZIP SHA/size·CRC 확인.
3. **이중 확인 PASS인 경우에만** 실제 정식 경로 `collab/requests/REQ-L1-WORKSPACE-LOCAL-VIEWER-DESIGN-R1-20261118/REQUEST.md`에 **사전검증한 바이트 그대로** 게시해 Commit A SHA 고정, 원격 원본 readback. 기존 지원 `source_pin.py`로 Commit A + `repo_id` JSON 문자열 `"1451933830"`을 포함한 `SOURCE_PIN.json` 생성·원격 검증. 다른 요청의 완료/영수증/서명·ZIP 변경 금지.
4. 현재 Windows `approve_request.py check`로 정책·scope·USD 1.50 1회/기한·잔여 권한/중복을 재검증. **사용자 이번 명시 승인 + 실제 유효 수동 서명 권한**으로 이 요청만 서명·검증. 과거 자동 서명 보호 `auto_delegation.json`의 `max_request_usd=1.0`는 **이번 수동 승인 $1.50와 혼동하지 말 것**. 수동 경로가 실제 미지원이면 HOLD/READY 0, 글로벌 설정 임의 변경 0. `APPROVAL_SIG.json` 유효 검증 후 `READY.md`를 마지막으로 게시, GitHub readback.
5. **기존 GitHub 단일 LIVE watcher**만 Claude R1 독립 리뷰 1회(최대 USD 1.50) 수행하도록 둔다. 별도 Claude CLI 호출/서브에이전트 유료 호출/재시도/새 watcher 생성 금지. `UNCERTAIN` 발생 시 별도 승인 없이 재큐잉 0. 결과/receipt/dispatch를 원격 게시·검증하고 `CURRENT.md`, `TRACKER.json`를 최신으로 업데이트.
6. **요청 후 한도 설정 정리 (사용자 후속 지시)**: 먼저 실제 요청·서명·READY·모델 상태를 확인. 과거 `$1.00` **구형 리뷰 인계 제한**을 이번 요청에 적용하지 않도록 최신 유효 안내/템플릿만 정리하고 오래된 이력·영수증·고정 입력은 보존. **이번 요청 때문에 생성한 임시 설정 override/임시 제한이 존재하면** 요청 접수·운영 검증 후 정확히 그 override만 원복/삭제하고 근거를 보고. 이번 요청에는 **전역 비용·안전 설정 삭제를 위해 새 임시 override를 만들지 않는다**.
7. **중요 보호 경계:** 운영 v0.2.25에서 일/월 상한은 이미 정책상 폐기/설정 null. `auto_delegation.max_request_usd`는 보호된 건당 상한이며 삭제하면 signer fail-closed 또는 범위 없는 유료 요청 수락 위험. `max_request_usd`, `review_policy.known_run_policy_refs`, 서명·SOURCE_PIN·READY·중복·만료 보호는 **삭제하지 말 것**. 만약 사용자가 의도한 것이 전역 $1.00 보호 위임 상한의 영구 제거라면, 이번 $1.50 단일 승인을 **미래 무제한 리뷰 위임으로 확대하지 않음**. 해당 설정은 별도 신규 범위·만료·승인과 실제 호스트 회귀/복구가 필요하며 지금은 `NOT_CHANGED/DEFERRED` 보고.
8. 최종 결과: `collab/projects/L1-WORKSPACE-RAG-20261111-001/CLAUDE_LOCAL_VIEWER_R0002_150USD_REVIEW_SUBMISSION_RESULT_FOR_GPT_20261118.md`에 각 상태·실제 SHA·등록/서명/READY·모델호출·비용/영수증·한도 정리 범위·다음 행동 기록. GitHub PRIVATE main 원격 byte/SHA 검증. `REQUEST/RUN=BLOCKED`면 정확한 blocker를 남기고 임의 승인·모델 0; 가능한 비유료 작업은 끝까지.

### 모델 호출 0 기준

- 임의로 생성한 GitHub 승인 문서나 외부 커밋을 **Ed25519 서명/READY로 취급 금지**.
- Live config·서명자·원본 pin·요청 예산·중복·만료 중 하나라도 미검증이면 REQUEST 게시 전 STOP 또는 signer 전 STOP; 실패 지점 정확히 보고.
- 예산 부족 시 디자인 $3로 자동 승급 금지. 과거 완료 `REQ-L1-MSC-DUAL-ENTRY-DESIGN-R1-20261117` 절대 수정·재실행 금지.

## GPT 후속

유효한 리뷰 원문과 비용 영수증을 확인·판정해, 업무 GPT용 최종 단계별 제안·작업 지시 MD를 `wonhwipark/L1Work/main/handoffs/` 게시. 실제 업무 Linux 원본 및 웹 공개/설치는 별도 G0·승인·게이트.
