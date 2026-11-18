# Linux Workspace Viewer — 정식 Claude R1 리뷰 등록 준비 결과 (2026-11-18 KST)

- **판정:** `REVIEW_PACKAGE=PREPARED_REMOTE_VERIFIED`; `FORMAL_REQUEST=BLOCKED_NOT_POSTED`; `SOURCE_PIN=NOT_POSTED`; `APPROVAL_SIG/READY=NOT_POSTED`; `INDEPENDENT_CLAUDE_REVIEW=NOT_RUN`; `HOST_PREFLIGHT=NOT_RUN`; `MODEL_CALLS_THIS_SESSION=0`.
- **기존 Work:** `L1-WORKSPACE-RAG-20261111-001`; 새 Work 및 기존 완료된 `REQ-L1-MSC-DUAL-ENTRY-DESIGN-R1-20261117` 중복 처리 없음.
- **원인:** Windows watcher 실호스트의 설치·위임 대상/기간/잔액/정책/중복·UNCERTAIN/`review_request_gate.py select/check`를 이 GPT 연결에서 직접 실행할 수 없음. 운영 v0.2.25 호스트 보고에는 `POLICY-STATIC-V1=1.50`·`-DESIGN=3.00` 정책맵 등록이 있으나 **보호 자동 서명 위임은 최대 USD 1.00/요청**으로 유지. 정책맵 값이나 이번 요청 지시만으로 위임 확대/서명 승인 대체 불가. 패키지 선게시 != 정식 요청 접수.
- **요청 ID(예약 제안, 아직 실등록 안 됨):** `REQ-L1-WORKSPACE-LOCAL-VIEWER-DESIGN-R1-20261118`. 동일 ID의 `collab/requests/<ID>/REQUEST.md` 및 `collab/reviews/<ID>/REVIEW_RESULT_1.md` 사전 조회 404; 실제 Windows 로컬 DB 중복 여부는 미확인.

## 실제 게시한 고정 입력

- 패키지: `collab/packages/l1-workspace-local-viewer-design_r0001_1118_REVIEW_INPUT.zip`.
- 고정 원본: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab` `main`, source commit `84b9f74ab05750b1789ce254e85d09bce4fd3115`.
- 게시 commit `bf5fe36d292aa7a5e96105de38455908aba33f68`, ZIP 76,097 bytes, SHA-256 `e2b1a2462b3b8eededea394bb662c3782671711ef32ab23620aa11c95a9305eb`, Git blob `72fb645e8ac7f6917827329f9d544f6c3d1e0921`.
- package index: `review-inputs/REQ-L1-WORKSPACE-LOCAL-VIEWER-DESIGN-R1-20261118/REVIEW_MANIFEST.md` (동일 Work 루트 기준). Git blob `64967e7e1b15e3b7c3f78d36f1e5e7478475a24d`.
- ZIP 7개 엔트리: `01_SAFE_TRANSITION_DESIGN.md`, `02_CLAUDE_REVIEW_R01_R22.md`, `03_PREP_EVIDENCE_AND_GAPS.md`, `04_WORK_TO_GROUP_KNOWLEDGE_FLOW.md`, `05_BUSINESS_PROPOSAL_DRAFT.md`, `FILE_INDEX.json`, `README.md`.
- **실제 원격 readback:** GitHub ZIP base64→76,097 raw bytes, blob 일치, 중앙 디렉터리/7개 로컬 헤더/7개 CRC32/manifest blob **PASS**. source SHA-256은 빌드 단계 순수 JS 구현이 SHA-256 공개 테스트 벡터 2개 PASS 후 계산; GitHub 원격 Git blob 일치로 동일 패키지 바이트 확인. ZIP entry는 UTF-8, STORE, 고정 타임스탬프, 상대 경로. 패키지 내 회사 소스·상세 MSC 원문·토큰/비밀 없음(설계/계약 자료만 포함).
- 원샷: `GPT_L1_WORKSPACE_LOCAL_VIEWER_CLAUDE_ONE_CYCLE_REVIEW_REQUEST_r0001_20261118_KST.md`에 위 입력 고정 SHA와 **Windows gate 먼저**·USD 1.00 범위 조건을 추가; remote readback 확인.
- 기존 `CURRENT.md`와 `TRACKER.json`은 변경 상태를 구분해 갱신. 사용자의 Claude 리뷰 1회·그 후 업무 GPT 최종 작업지시 MD 요청은 유지.

## Windows에서 수행해야 하는 정확한 다음 한 동작

1. GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab` / `main` / `collab/projects/L1-WORKSPACE-RAG-20261111-001/GPT_L1_WORKSPACE_LOCAL_VIEWER_CLAUDE_ONE_CYCLE_REVIEW_REQUEST_r0001_20261118_KST.md`를 읽는다.
2. 기존 Windows LIVE v0.2.25 보호 설정·위임 적용 프로젝트/skill/승인 기간·요청당 USD 1.00 이하·잔여 일월 한도·유효한 `POLICY-STATIC-V1` 또는 허용된 DESIGN 정책·`review_request_gate.py select/check`·기존 상태/UNCERTAIN에 대해 read-only preflight.
3. 모두 PASS일 때만 **고정 ZIP을 그대로 사용**해 정확한 운영 스키마의 신규 `REQUEST.md`와 source pin `SOURCE_PIN.json`(`repo_id`는 JSON 문자열 `"1451933830"`), Commit A 실제 SHA로 입력을 고정해 GitHub 원격 readback. 기존 유효 보호 서명자는 그 뒤 APPROVAL_SIG 검증/READY 마지막 게시, 유효 watcher 1회 리뷰, 결과/receipt 게시. 실패/미확인은 REQUEST/READY 없이 `PREFLIGHT_BLOCKED`와 근거만 PRIVATE에 남기고 모델 호출 0.
4. 리뷰 결과가 나온 경우에만 GPT가 지적별 판정해 업무 GPT용 PUBLIC `L1Work/main/handoffs/L1_WORKSPACE_LOCAL_VIEWER_LINUX_PROPOSAL_AND_WORK_ORDER_r0001_20261118_KST.md` 최종화. 운영 Linux 파일, 동료 서비스, Group Knowledge 실제 쓰기/설치 승인은 별도.

**원본/운영 변경 없음:** Windows watcher/DB/WAL/SHM/Task/설정·키·위임, Linux 원본, 기존 리뷰/영수증, 그룹 지식, PUBLIC 스킬 ZIP/최종 인계 MD, LIVE provider는 이 작업에서 건드리지 않음.
