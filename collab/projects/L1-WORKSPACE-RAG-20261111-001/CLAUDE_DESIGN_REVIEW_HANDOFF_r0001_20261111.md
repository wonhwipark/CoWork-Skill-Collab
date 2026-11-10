# Claude Code — L1 Workspace RAG 1차안 독립 설계 리뷰 인계

- Date: 2026-11-11 KST
- Task ID: L1-WORKSPACE-RAG-20261111-001
- Type: STATIC DESIGN REVIEW / DELTA-FOCUSED
- Mode: SEMI_AUTO / REQUEST_PREPARED_NOT_QUEUED
- Source repository: **GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`**
- Branch: **`main`**
- Design input: **`collab/projects/L1-WORKSPACE-RAG-20261111-001/L1_WORKSPACE_RAG_DESIGN_r0001_20261111.md`**
- Input creation commit: **`b34a0907bc0ddfb42af0c7f6dec072dcd11353c8`**. 리뷰 시 실제 최신 파일 SHA/commit 대조.
- Expected safe result path: **`collab/projects/L1-WORKSPACE-RAG-20261111-001/CLAUDE_DESIGN_REVIEW_RESULT_FOR_GPT_20261111.md`**
- This GitHub file is **NOT a valid watcher REQUEST/READY**. Dropbox LIVE 유지. 문서 게시만으로 자동 리뷰/비용 지출 시작되지 않음.

## One-shot review task

1. 위 PRIVATE GitHub 원문을 읽고 `main`의 파일·커밋을 다시 확인. 사용자 첨부 Kernel v0.7.37, PUBLIC Workflow v1.6.67 및 l1-github v0.3.56의 실제 코드/계약과 교차 비교. 설치본이 다르면 버전·원인/영향을 분리.
2. 권한 허용 범위에서 **사내 GitHub** `l1-workspace`의 실제 repo role(`work_docs`), 브랜치·현재 tree(`works/`, `index/`, `module-library/`), 로컬 설치·MCP 등록 여부를 **읽기 전용으로** 검증. 접근 불가/스킬 버전 불명은 `NOT_VERIFIED`로. 사외 GitHub.com 404는 사내 저장소 부재 증거가 아님.
3. 원본 Kernel Work SSOT, 자동 생성 `문서안내.md` 가드, Cross-host Snapshot/Resume, Legacy migration에 대한 영향과 인덱스 경로 충돌을 정밀 검토.
4. Workflow의 `module_library.py`, `github_docs.py`, `knowledge_input.py` 및 관련 MCP 등록의 실제 구현과 `module-library/index/by-type` 제안의 중복 여부를 판단. 생성기/ID 체계를 두 번 만들지 않을 것.
5. `ISSUE/FEATURE/REFACTOR/DESIGN` 지식 분류와 `BUG/BUG-NR/FEATURE/REFACTOR/MAINT` 실행 프로파일을 구분. Work/지식 양방향 참조·다중 유형·scope·stable ID 문제를 검토.
6. RAG에서 **문서 검색→원문 anchor/body 검증→scope/owner/root 검증→입력 발행 드라이버에서 digest 검증→실제 Agent/Provider 입력 주입→출처 있는 답변**의 각 단계를 기존 기능/최소 신규 연결로 매핑. 모델 호출이나 실 제품 시험을 이번 작업에서 하지 말 것.
7. 이전 로드맵 `F-B1-01/02, F-N2-01/02, F-N1-01, F-N3-01, F-VERS-01`의 차단 게이트에 대한 누락·우회·불명확한 집행 주체를 확인. 검증되지 않은 승인 ID, 임의 direct 실행 경로, 미승인 릴리스 사용 금지.
8. 지적을 `BLOCKING / MAJOR / MINOR`, 근거 수준 `E3(real host) / E2(code) / E1(doc) / E0(absent)`로 구분. 항목별 최소 변경·부정 회귀시험을 제안하고 `REUSE/CONNECT/EXTEND/DEFER`로 실제 변경 지점을 분류.
9. **정적 리뷰 외 어떤 변경도 하지 않는다.** 사내 Git/Work/운영 설치/DB/Job/Provider 실행, 원본 스킬 ZIP 변경, GitHub PUBLIC 게시, watcher LIVE 전환, REQUEST/READY/비용 호출 실행 금지.
10. 결과에서 사내 코드/내부 원문/제품 로그/토큰/키/반출금지 경로는 제외. 반출 정책을 확인할 수 없는 경우에는 외부 게시하지 않고 `NOT_POSTED`로 표기. 허용된 비민감 결과 MD만 PRIVATE `main`에 PR 없이 직접 게시하고 remote readback/commit을 확인.

## Required result sections

- REVIEW_STATUS: COMPLETED | PARTIAL | NOT_RUN
- REVIEW_KIND: INDEPENDENT_STATIC (별도 세션 입증 시) | SELF_REVIEW | NOT_RUN
- INPUT_COMMIT / INPUT_BLOB_SHA / INPUT_FILE_SHA256
- CURRENT_TREE / INSTALL_STATUS / MCP_TOOL_MAPPING (E0–E3)
- ISSUE_LIST: id, severity, evidence, impact, suggested minimal change, negative test
- REUSE_CONNECT_EXTEND_DEFER, G0_READ_ONLY, RAG_INPUT_VERIFICATION, CROSS_HOST_REGRESSION
- SECURITY_SCOPE / INHOUSE_WRITES=0 / MODEL_CALLS=0
- RESULT_REMOTE_POST / COMMIT / READBACK
- UNRESOLVED_GATES / GPT_DISPOSITION_REQUESTED

## Operational note

현재 `MIGRATION_NOT_CUTOVER`: GitHub watcher 비활성. 사용자로부터 Windows Claude Code에 본 경로를 전달하여 대화형 정적 검토를 실제 개시하면 별도 검토 결과를 받을 수 있다. 기존 Dropbox LIVE watcher를 사용하는 **정식 리뷰**는 독립된 유효 REQUEST/READY·정책·서명·비용 게이트가 필요하다. 두 종류의 리뷰를 같은 영수증으로 보고하지 않는다.
