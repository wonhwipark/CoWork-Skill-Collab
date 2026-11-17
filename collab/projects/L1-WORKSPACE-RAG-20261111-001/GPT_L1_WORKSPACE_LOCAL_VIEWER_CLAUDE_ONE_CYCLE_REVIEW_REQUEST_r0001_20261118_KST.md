# L1 Workspace 로컬 웹 뷰어 전환 — Windows Claude Code 독립 설계 리뷰 정식 요청 인계 r0001

- 날짜: 2026-11-18 KST
- 요청자: GPT / 사용자 명시 지시: **Claude 독립 설계 리뷰 먼저 → 리뷰 반영 → 업무 GPT용 전체 제안·작업 지시 MD 제공**
- 기존 Work: `L1-WORKSPACE-RAG-20261111-001`; 새 Work를 만들지 않음
- 정본: GitHub **PRIVATE** `wonhwipark/CoWork-Skill-Collab`, branch `main`.
- 요청 범위: **새로운 Linux-local Workspace + 선택적 read-only Web Viewer + Group Knowledge 연결 전환 설계만**. 이전 MSC 두 진입 설계 R1 완료 건을 재호출하지 않음.
- 이 인계서는 **Windows 현장 실행을 위한 구체 작업 지시**이며 게시 자체는 REQUEST/승인/READY/모델 호출이 아님.

## 1. 반드시 읽을 입력

1. `collab/CONTEXT_BRIEF.md` → `collab/projects/L1-WORKSPACE-RAG-20261111-001/CURRENT.md` 최신 상단
2. `collab/projects/L1-WORKSPACE-RAG-20261111-001/L1_WORKSPACE_LOCAL_FIRST_WEB_VIEWER_SAFE_TRANSITION_DESIGN_r0001_20261118_KST.md` (설계, G0~G6, P0~P6, T01~T26)
3. `collab/projects/L1-WORKSPACE-RAG-20261111-001/CLAUDE_L1_WORKSPACE_LOCAL_FIRST_WEB_VIEWER_INDEPENDENT_DESIGN_REVIEW_HANDOFF_r0001_20261118_KST.md` (**R01~R22**)
4. `collab/projects/L1-WORKSPACE-RAG-20261111-001/GPT_L1_WORKSPACE_LOCAL_WEB_VIEWER_SAFE_TRANSITION_PREP_RESULT_r0001_20261118_KST.md` (합성시험·미검증 구분)
5. `collab/projects/L1-WORKSPACE-RAG-20261111-001/L1_WORK_TO_KNOWLEDGE_FLOW_r0002_20261115_KST.md` (업무 Work → 그룹 Knowledge)
6. `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/CURRENT.md`, `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md`, 실제 Windows 보호 설정·기존 요청 영수증. 맥락이 불충분하면 계약만 필요한 범위로 추가 조회.

## 2. 실행 순서: 사전 검증 → 정식 한 건 요청 → Claude 독립 리뷰 → 결과 회수

**STEP 0 — 중복/사전권한 읽기 전용 확인**

- 로컬 watcher 실제 설치 버전, LIVE provider, 유효 위임의 대상 프로젝트/skill/기간/요청당 USD 상한/일·월 한도/잔액, POLICY-STATIC-V1 또는 실제 운영 승인된 적합한 DESIGN 정책의 지원 여부, `review_request_gate.py` 지원/실제 `select/check`, SOURCE_PIN repo_id 문자열 타입을 확인.
- 기존 로컬 예약·UNCERTAIN·완료된 리뷰(특히 `REQ-L1-MSC-DUAL-ENTRY-DESIGN-R1-20261117`)와 동일 목적 신규 요청의 중복을 대조. 이전 작업의 REQUEST/READY/영수증은 수정하지 않음.
- 현재 보고된 v0.2.25 운영 보호 위임 한도는 요청당 **USD 1.00**이며, 정책 맵에 DESIGN USD 3이 존재하더라도 **맵 값만으로 위임 증가를 승인한 것이 아님**. 사용자 최신 유효 승인 및 호스트 실제 값을 우선. 필요 시 1 USD/1회 STATIC 범위로 축소하거나 `PREFLIGHT_BLOCKED`. 요청을 새 예산에 맞춘다고 위임/정책/서명을 직접 변경하지 않음.
- 모든 필수 사전 조건 확인 전에는 **REQUEST, SOURCE_PIN, APPROVAL_SIG, READY를 게시하지 않음**. 실패/미확인은 원인·최소 필요한 승인만 결과 메모로 기록, 모델 호출 0.

**STEP 1 — 독립 리뷰 고정 입력 생성·게시 (사전 검증 PASS일 때만)**

- 새 고유 request_id 제안: `REQ-L1-WORKSPACE-LOCAL-VIEWER-DESIGN-R1-20261118`; 동일 ID가 이미 존재하면 재사용·덮어쓰기하지 말고 중복 상태 확인 후 STOP.
- **최소 리뷰 입력**: 위 설계 전체, Claude R01~R22 인계, 실제 시험·미검증 결과, Work→Knowledge 설계 요약, source manifest. 회사 코드/상세 업무 MSC/로그/개인 파일/비밀정보 **0**.
- `collab/packages/l1-workspace-local-viewer-design_r0001_1118_REVIEW_INPUT.zip`에 버전·상대 경로·파일별 SHA-256·크기·CRC·민감정보/경로이탈 검사. 실제 ZIP 바이트 재조회와 해시 일치 확인.
- 정식 `collab/requests/<request_id>/REQUEST.md` + `SOURCE_PIN.json`을 **최신 설치된 계약의 정확한 필드와 schema**로 생성. source pin `repo_id`는 반드시 문자열 `"1451933830"`, `commit`은 실제 **Commit A**(ZIP/REQUEST/근거를 게시한 커밋). 요청당 비용은 실제 보호 승인 이하, 호출 정확히 1회, 부적합하면 PARTIAL_SCOPE.
- Commit A 이후 실제 GitHub 원격 ZIP 크기/SHA/내용·REQUEST/Pin 타입을 독립 검증. 잘못된 pin으로 자동 승인 WAIT 유발하지 말 것.
- 운영 watcher가 유효 위임·비용·만료·중복·policy 검사 PASS일 때에만 기존 보호 경로로 **APPROVAL_SIG와 READY를 마지막 게시**. GPT/Claude 대화 텍스트를 승인 서명으로 취급하거나 키 생성·서명 위조 금지. REVIEW_TRANSPORT 보호 계약 준수.

**STEP 2 — Claude 1회 독립 설계 리뷰 (정식 READY와 로컬 검증 PASS일 때만)**

- 리뷰 R01~R22 각각 `PASS/RISK/NOT_VERIFIED/N/A`로 판정. 결함별 심각도(배포·전환 차단 여부), 반례/근거, `REUSE/CONNECT/최소 EXTEND/DEFER`, 변경 책임 스킬, 신규 API 발명 금지.
- 특히 **(a) 기존 Git mode 유지한 개인 SHADOW Viewer**, **(b) 승인된 동료 HTTPS ACL 공유**, **(c) local authority cutover**를 각각 독립적으로 평가. 방안 A Git SSOT+viewer, B local Git SSOT+offhost backup, C 공용 viewer 사본 비교.
- HTML+SVG/MD 링크 2종, 경로 traversal/심링크·hardlink, 원본 보존/동시 Writer, Updater 개인 지식 유일 Writer, 그룹 Preview→CAS→승인→readback, 그룹 성공·역링크 실패의 재게시 금지, 복원 실측, 실패 시 기존 Git 복구 등을 공격적으로 검토.
- `ACCEPT / ACCEPT_WITH_CHANGE / REVISE / HOLD` 중 하나로 종합 판정하되 Linux G0를 Windows에서 수행했다고 주장하지 않음. 별도 코드·실제 업무 시험과 유료 재리뷰 수행 금지.

**STEP 3 — 원격 결과 게시·한 사이클 종료**

- watcher 표준 결과 `collab/reviews/<request_id>/REVIEW_RESULT_1.md`와 `collab/receipts/<request_id>/RECEIPT_1.md`, 디스패치 이력·승인 결속 실제 저장·원격 readback 확인.
- 사람이 읽을 정리본을 기존 Work `collab/projects/L1-WORKSPACE-RAG-20261111-001/CLAUDE_L1_WORKSPACE_LOCAL_FIRST_WEB_VIEWER_DESIGN_REVIEW_RESULT_FOR_GPT_r0001_20261118_KST.md`에 기록하고, 리뷰 진입·실행의 실제 SHA/비용/미검증 근거를 별도 EVIDENCE JSON에 기록. **리뷰 미실행 시 위 완료 산출물 생성 금지**.
- `CURRENT.md` 상단 최신 상태, 기존 `TRACKER.json` 관련 현행 값만 정합화. 리뷰 완료 시 **GPT가 1회 판정**하게 하며 미완료는 `PENDING/BLOCKED`로 정확히 표시.
- 결과 게시 장애/실행 불확실 시 분석·모델/Job 재실행하지 말고 로컬 receipt·audit·원격 상태만 정산.

## 3. 리뷰 이후 업무 GPT 인계 계약

- 리뷰 결과가 원격에 존재하면 **GPT가 지적별 수용·수정수용·보류 판정**, 업무용 제안·작업 지시서 draft를 리뷰 결과와 실제 G0 미확인을 반영하여 개정.
- 업무용 최종 MD 게시 위치: `wonhwipark/L1Work` **PUBLIC** `main/handoffs/L1_WORKSPACE_LOCAL_VIEWER_LINUX_PROPOSAL_AND_WORK_ORDER_r0001_20261118_KST.md`. **회사 자료 0·비민감 실행 계약만**, CoWork 저장소 경로·토큰 의존성 주입 금지. 리뷰 완료 전 이 최종본 게시·승인된 실행서라고 선언하지 말 것.
- 업무 GPT/승인된 Linux Agent는 먼저 READ_ONLY G0 A~P를 실행하고 **개인 synthetic SHADOW viewer의 상세 구현 사양만** 확정. 실제 호스트 설치·서버 시작·동료 공개·Git authority 전환·group write는 독립 게이트 및 필요한 승인 없이는 금지.
- [정본 업무 인계(기존)](https://github.com/wonhwipark/L1Work/blob/main/handoffs/L1_WORKSPACE_LOCAL_WEB_VIEWER_LINUX_G0_READONLY_HANDOFF_r0001_20261118_KST.md), [새 업무용 제안·작업지시 초안](L1_WORKSPACE_LOCAL_VIEWER_LINUX_PROPOSAL_AND_WORK_ORDER_DRAFT_r0001_20261118_KST.md). 초안은 검토 전이며 실행승인 아님.

## 4. 완료 조건 / 사용자 전달

- **정식 요청 제출과 Claude 실행은 별개**. REQUEST/SOURCE_PIN 게시, APPROVAL_SIG/READY, DISPATCH, REVIEW_RESULT/RECEIPT, GPT 판정, 최종 L1Work 인계 게시를 단계별로 구분.
- 만료·위임 부족·Windows 접근 불가 시 그 상태를 그대로 보고하고, 이미 검증된 설계/인계를 재사용. 리뷰가 완료된 것처럼 PUBLIC 최종 작업지시서를 배포하지 않음.
- 이번 요청이 기존 업무 GitHub/P4·Linux 파일·웹 서버·Knowledge writer/Windows watcher 설정을 변경할 권한을 추가하지 않음.

**Windows Claude Code 1회 전달 문구**: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab` branch `main`의 `collab/projects/L1-WORKSPACE-RAG-20261111-001/GPT_L1_WORKSPACE_LOCAL_VIEWER_CLAUDE_ONE_CYCLE_REVIEW_REQUEST_r0001_20261118_KST.md`와 그 안의 입력 문서들을 확인해줘. 최신 유효 Windows 승인·서명·예산·중복 preflight PASS면 이번 로컬 Workspace 전환 설계만 신규 정식 REQUEST/SOURCE_PIN으로 고정해 Claude 독립 설계 리뷰 **1회** 수행하고 표준 결과·영수증·기존 Work 상태를 PRIVATE main에 PR 없이 게시·readback해줘. 막히면 승인 경계를 우회하지 말고 정확한 HOLD 사유만 기록해줘. 기존 완료 MSC 리뷰는 재실행하지 마.
