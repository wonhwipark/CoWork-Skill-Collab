---
schema: SKILL_COLLAB_REVIEW_REQUEST_V1
state: SUBMITTED
request_id: REQ-L1-WORKSPACE-LOCAL-VIEWER-DESIGN-R1-20261118
request_revision: 1
project_id: L1-WORKSPACE-RAG-20261111-001
work_id: L1-WORKSPACE-RAG-20261111-001
skill_id: l1-knowledge-updater
package_path: /SKILL-COLLAB/packages/l1-workspace-local-viewer-design_r0002_1118_REVIEW_INPUT.zip
package_file_id: github:REQ-L1-WORKSPACE-LOCAL-VIEWER-DESIGN-R1-20261118
package_rev: l1-workspace-local-viewer-design-r0002
package_sha256: 6a013a104ebfefeae6dc452965ce99ce5a3f9637ed538c778d8cb5189d5a7e5f
package_size_bytes: 91324
baseline_package_ref: null
knowledge_refs: []
consumer_profiles: [l1-workspace-local-viewer-independent-design-review]
reviewer_os: WINDOWS
test_policy: STATIC_ONLY
run_policy_ref: POLICY-STATIC-V1
output_contract: SKILL_COLLAB_REVIEW_RESULT_V1
goal: single independent R1 scoped design review of full Linux local Workspace URL browsing and on demand document viewers
---

# Linux Workspace 로컬 웹 뷰어 독립 설계 리뷰 — 최신 r0002, USD 1.50 단 1회

## 승인·입력

- **사용자 승인:** 2026-11-18 KST 이 채팅에서 이 리뷰 **1회 최대 USD 1.50** 사용을 명시 승인. 이번 범위만 승인한 것이며, 전역 보호 위임 변경이나 추가 과금·재리뷰 승인이 아님. 별도 기존 호스트 protected signer의 유효한 승인과 원격 PIN/READY 검증은 필수.
- **현재 단계:** 이 본문은 **PREPUBLICATION DRAFT** 파일이다. 경로를 `collab/requests/<ID>/REQUEST.md`로 취급하거나 watcher가 실행하도록 게시하지 말 것. Windows live `review_request_gate.py select/check` PASS 이후에만 **바이트 불변**으로 해당 실제 요청 경로에 게시해야 한다. 단순한 GitHub 게시가 서명/READY가 아니다.
- **고정 비민감 ZIP:** `collab/packages/l1-workspace-local-viewer-design_r0002_1118_REVIEW_INPUT.zip`; 91,324 bytes; SHA-256 `6a013a104ebfefeae6dc452965ce99ce5a3f9637ed538c778d8cb5189d5a7e5f`; Git blob `dcb42fca58f5cd5c281fc3622fc6e6bfccb02285`; 9 members and CRC verification PASS. r0001 패키지로 다운그레이드 금지.
- 최신 `README_R0002_LATEST_FIRST.md`와 `06_FULL_WORKSPACE_TREE_VIEWER_DESIGN_DELTA_r0002.md`를 먼저 확인. 이후 기존 r0001 설계·R01~R22·실측/미검증 근거·업무 제안 초안 검토.

## 리뷰 초점

- 업무 네트워크 사용자에게 Linux Workspace **업무 폴더 전체**를 단일 URL로 탐색·검색·읽기 전용 제공하되 시스템 비밀, symlink root 탈출, `.git` 등은 격리. Work별 공개 allowlist 기본 제외; 외부 인터넷 익명 공개 요구 아님.
- Markdown은 원본 유지 후 클릭 때 HTML 렌더/캐시, MSC HTML(기존 B viewer)은 원본 직접, SVG/JSON/PDF/이미지는 적합한 기존 handler. **모든 문서를 별도 HTML 정본으로 전량 사전 변환 금지**.
- Git 기반 Work 원본·기존 Workflow/Kernel writer는 UI/복제 뷰어와 분리, local authority cutover는 별도 승인·백업·롤백/충돌/단일 writer·G0 입증 후만. 그룹 `l1sw-dev-knowledge` Updater writer CAS/Preview/승인/역링크 유지.
- 질문 R01~R27, 시험 T01~T34를 핵심 보안·writer·렌더 가정에 따라 **USD 1.50, 모델 호출 1회** 예산 내 우선순위 축소 평가. 전체 범위 불가 시 확인한 범위 및 `PARTIAL_SCOPE` 표시, 자동 R2 $3 승격/재시도 0.
- 결함 수 강제하지 말고 근거·위험·최소 변경안·대안과 검증 계획을 한국어로 보고. 실제 Linux G0 미접근을 PASS로 판단하지 말 것.

## 실제 host 이전 게이트와 안전 실행

1. Windows 운영 설치본 `reviewer.config.json`을 직접 읽어 `collab/ops/review_request_gate.py select --live-config <WINDOWS_LIVE_CONFIG> --intent skill --required-budget-usd 1.50`의 `POLICY_COMPATIBLE_NOT_APPROVED / POLICY-STATIC-V1 / 1.50` 확인.
2. 이 파일 **원시 UTF-8 바이트를 그대로** Windows 로컬 `REQUEST.md` 임시 검증 파일에 복사. 고정 ZIP을 다운로드·CRC/size/sha 재검증. `review_request_gate.py check --live-config <WINDOWS_LIVE_CONFIG> --intent skill --required-budget-usd 1.50 --request <TMP_REQUEST> --package <VERIFIED_R0002_ZIP>`가 `PASS_PREPUBLICATION_ONLY` 및 정확한 raw `request_sha256`를 출력해야 함. **예산 승인이 select/check를 대신하지 않음**.
3. 새 요청 ID/revision/package_SHA의 Windows DB 중복·UNCERTAIN·기존 동일 logical request/영수증·이미 등록된 원격 REQUEST/SOURCE_PIN/APPROVAL_SIG/READY/결과를 재검증. `request_id` 충돌이 있으면 이 요청을 덮어쓰지 않고 HOLD.
4. PASS일 때만 `collab/requests/REQ-L1-WORKSPACE-LOCAL-VIEWER-DESIGN-R1-20261118/REQUEST.md`로 **사전검증한 바이트 동일** 새로 게시. 실제 Commit A SHA와 `request_sha256`, ZIP SHA 및 크기 원격 readback PASS. 기존 `source_pin.py`로 `repo_id` JSON 문자열 `"1451933830"`, `commit` 실제 Commit A인 `SOURCE_PIN.json`을 생성·원격 검증.
5. Windows 기존 `approve_request.py check` 후 **유효한 수동 보호 서명 경로**로 이 요청에 한해 1.50/1회 서명. 기존 `auto_delegation.max_request_usd=1.0`을 우회하거나 변경했다고 주장하지 말 것. 수동 signer가 실제로 $1.50 서명을 허용하지 않으면 `APPROVAL_BLOCKED`, 모델 0. 임의 자체 키/서명·GitHub 문서의 승인 주장으로 대체 금지.
6. 실제 승인 서명 원격 검증 PASS 뒤에만 `SKILL_COLLAB_READY_V1`의 `READY.md`를 마지막으로 게시. 기동 중인 GitHub 단일 LIVE watcher가 유효 요청을 1회만 실행하도록 두고, Windows Claude 별도 유료 호출·새 watcher·재큐잉 금지. `UNCERTAIN` 상태에서 재호출 0.
7. 리뷰/사용량 `collab/reviews/REQ-L1-WORKSPACE-LOCAL-VIEWER-DESIGN-R1-20261118/REVIEW_RESULT_1.md`, `collab/receipts/.../RECEIPT_1.md`와 dispatch 결과 remote readback; `CURRENT.md`·`TRACKER.json` 동기화, GPT 판정 후 PUBLIC `L1Work/main/handoffs/` 업무 GPT 최종 제안/작업지시서 별도 게시.

## 리뷰 이후 비용 설정 정리(사용자 요청)

- **이번 리뷰 전용 임시 override/예외가 실제 생성된 경우에 한하여**, 리뷰 요청이 유효하게 접수되고 완료 또는 실행 불확실이 확정된 뒤 당시 생성한 임시 파일·변경값만 백업·감사 및 rollback 근거와 함께 원복/삭제. **이번 문서는 임시 override를 설치하도록 지시하지 않는다.**
- 기존 v0.2.25의 **일/월 누적 한도는 이미 `null`이며 로직에서 폐기됨**. 따라서 동일 한도 재삭제, SQLite 이력 삭제, 감사/영수증 삭제 불필요·금지.
- 사용자 “요청 후 한도 관련 설정 삭제”는 **기존 보호 위임의 전역 `max_request_usd`, 요청별 금액/서명/READY/중복/비용 검증을 무조건 삭제하는 허가로 해석하지 않는다.** 삭제하면 fail-closed 파괴 또는 불특정 유료 리뷰 개방 위험이 있다. 전역 제한을 완화하려면 별도 범위·기한·서명자 권한 확인 후 새로운 보호 위임을 승인된 값으로 갱신하고 실제 Windows 시험 수행. 이번 건의 USD 1.50 이외 장래 호출 자동 위임 확대/무제한 허용 금지.
- 기존 r0001 인계의 낡은 “최대 $1” 문구는 이 요청 r0002에 **적용하지 않는다**. 실제 REQUEST 등록 이후 현행 지침에서는 최신 r0002/1.50 문서만 연결하고 이전 역사적 기록은 보존.

## 상태·완료 기준

최초 게시 단계 `REQUEST_DRAFT_POSTED`, `LIVE_PREFLIGHT_NOT_RUN`, `FORMAL_REQUEST_NOT_POSTED`, `SIGN_READY_NOT_RUN`, `PAID_REVIEW_NOT_RUN`. 이 드래프트는 GitHub watcher의 실행 트리거가 아님.

Windows 실제 실행 후 `REQUEST_SHA`, `COMMIT_A`, `SOURCE_PIN`, `APPROVAL_SIG`, `READY`, `REVIEW_RESULT`, `USAGE_RECEIPT`, `MODEL_CALLS`, `ACTUAL_COST`, `TEMP_LIMIT_CLEANUP`를 실측 상태로 별도 보고할 것.
