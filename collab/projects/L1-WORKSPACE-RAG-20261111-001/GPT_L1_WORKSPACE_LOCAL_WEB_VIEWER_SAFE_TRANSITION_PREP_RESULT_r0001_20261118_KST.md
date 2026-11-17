# L1 Workspace Linux 로컬 정본·웹 열람 전환 — 설계·준비 실행 결과 r0001

- 날짜: 2026-11-18 KST
- 기존 Work: `L1-WORKSPACE-RAG-20261111-001` (Work 신규 생성·기존 리뷰 재실행 0)
- 사용자 요청: 상세 구조 검토, 안전한 전환 워크플로 정립, 가능한 개발/시험·인계·게시까지 계속. 사용자는 퇴근 중이므로 추가 질문/수동 조작을 선행 조건으로 두지 않음.
- **최종 판정:** `DESIGN_REVIEW_SELF=PASS_SCOPE_LIMITED / SYNTHETIC_KERNEL_LOCAL_EXPORT=PASS / READ_ONLY_G0_HANDOFF=PUBLIC_POSTED / INDEPENDENT_REVIEW_HANDOFF=PRIVATE_POSTED / INDEPENDENT_REVIEW_EXECUTION=NOT_RUN / LINUX_HOST_G0=NOT_RUN / LOCAL_AUTHORITY_CUTOVER=BLOCKED_NOT_RUN / TEAM_WEB_HOST=BLOCKED_NOT_RUN / GROUP_KNOWLEDGE_WRITE=NOT_RUN`.

## 1. 현재 사실·코드 근거

- CoWork PRIVATE `collab/CONTEXT_BRIEF.md`와 본 Work `CURRENT.md` 및 두 진입 설계 `L1_WORK_TO_KNOWLEDGE_FLOW_r0002_20261115_KST.md` 확인. 기존 Work 원본/그룹 Knowledge 승인 정본/웹 읽기 전용 파생 복제본을 별개의 책임으로 구분.
- 개발 후보 Kernel `work-ledger-kernel_v0_7_45_1118.zip` SHA-256 `1bccbbffeaafcefda27b75ca8f430e502bc8c2b475b63bd76425ca7ee1c5d7f8`. 실제 Python의 `WorkLedgerKernel.work_docs_export()`를 **`.git` 미존재 synthetic local directory** 대상으로 호출: Work 문서/README/index 등 **12파일 생성**, 동일 파일 SHA·파일명 불변으로 재export **PASS**. 테스트는 `/mnt/data/local_workspace_migration_probe/source_kernel/` 격리 경로, 민감 회사 파일 0.
- 같은 패키지 내부 기존 `test_github_docs_layout_v077.py` + `test_feature_stage4_export.py`를 Python 격리 환경에서 `pytest -q` 실행하여 **5 PASS (0.49s)**. 이 중 기존 `TL_REVIEW`가 포함된 공유 export 차단 테스트가 포함. 실제 호스트 설치/웹 브라우저 접속과는 구분.
- 개발 후보 Workflow `l1-fix-workflow_v1_6_72_1118.zip` SHA-256 `0eb190e704d7e06d8bddf642bff858319fceb399814c83282a480502d377af02`의 `l1_fix_workflow/github_docs.py` 원문 정적 확인: `docs_sync`는 `l1-github repo-config work_docs` 등록 원격·실제 origin 동일 여부와 Git clean tree 선행 체크; `docs_push`는 Git commit/push/remote readback 필수. 설정만으로 push 없는 로컬 authority가 된다고 주장 불가.
- 전 회차 MSC 합성 검증: Work-root Markdown의 직접 HTML 링크 PASS, Converter 상세 MD 내부 구 상대링크 BROKEN. 새 viewer라도 두 종류 링크를 별도로 확인하고 원본 Evidence MD 자동 바이트 변조 금지.
- 업무 Updater·group writer·actual l1-workspace role·OS backup/SSO/방화벽/웹 서비스는 접근 불가 → `LINUX_G0=NOT_VERIFIED`; 동명 github.com repo로 가정 금지.

## 2. 작성 및 원격 게시

| 산출물 | 목적 | 위치·원격 commit | 원본 로컬 SHA-256 |
|---|---|---|---|
| 전환 상세 설계 r0001 | A→B→C 단계, P0~P6 게이트, 권한·원본·백업/rollback, T01~T26 부정시험 | PRIVATE `main`: `collab/projects/L1-WORKSPACE-RAG-20261111-001/L1_WORKSPACE_LOCAL_FIRST_WEB_VIEWER_SAFE_TRANSITION_DESIGN_r0001_20261118_KST.md`, final commit `8d693bcadb148993932889f09ee1a5e364664fdb` | `8acb1e57c9dbf1a8568c09045893426f89228b08f259280c8b73d45c4da94cad` |
| 업무 GPT G0 인계 r0001 | Linux 설치본/원격 의존성/웹·그룹 writer A~P **16개 숫자** 읽기 전용 요청 | PUBLIC `wonhwipark/L1Work/main/handoffs/L1_WORKSPACE_LOCAL_WEB_VIEWER_LINUX_G0_READONLY_HANDOFF_r0001_20261118_KST.md`, commit `f03651fa269ab16985afc964ac7752b065e212f3` | `87d48d67fbe9916159da12e440b89955e085c86260232ecc81946b6b2cba37a3` |
| 인계 목록 | 업무 GPT가 새창에서도 바로 찾도록 목록 상단 링크 | PUBLIC `wonhwipark/L1Work/main/handoffs/README.md`, commit `5ad0108727f0cdbbb0ae33def2833f96402f20f9` | 해당 원격 readback 링크 PASS |
| Windows Claude 독립 리뷰 인계 r0001 | R01~R22 설계·보안 반례/경계 검토 및 승인 정책 preflight | PRIVATE `main`: `collab/projects/L1-WORKSPACE-RAG-20261111-001/CLAUDE_L1_WORKSPACE_LOCAL_FIRST_WEB_VIEWER_INDEPENDENT_DESIGN_REVIEW_HANDOFF_r0001_20261118_KST.md`, commit `0caaecfb10933fef5f83da274ded3825d5c1252a` | `51d5169292f5fc5a29d55dd26ef38ab3c0abe1283c08b69b1e96268f767a95e4` |

원격 파일은 각각 재조회하여 file source와 전체 문자열 바이트가 일치한 것을 확인. 최종 바이트 SHA-256은 동일 UTF-8 원본 로컬 파일에서 측정. Git blob SHA는 SHA-256과 구별.

## 3. 안전 전환 업무 흐름

**기존 GitHub/업무 Linux 설치본을 즉시 없애지 않는다.** 먼저 Git 원격/Workflow/Updater/그룹 writer의 G0, 원본 Ledger/백업·실제 웹 보안 인프라를 확인한다. Kernel의 local export를 활용하되 실제 원본을 export 대상으로 직접 변경하지 않으며, 검증된 snapshot·staging에만 읽기 전용 복제. 다음에는 개인 localhost 웹 뷰어를 기존 GitHub writer 변경 없이 시험한다. 이후 동료 공유 필요·승인·HTTPS·ACL이 통과되면 선택 Work의 read-only share. 마지막으로 별도 승인된 이력/백업 복구·단일 writer·코드 독립 리뷰·회귀/수락/rollback 조건이 충족되는 경우에만 `LOCAL_AUTHORITY_CUTOVER`를 검토한다.

- **현재 Gate:** G1 kernel local synthetic만 확인. G0 실제 업무 설치본, G2 실제 보안/링크, G3 개인 웹, G4 동료 웹, G5 local-authority, G6 그룹 E3 **미실행**.
- 기존 스킬 Knowledge Guard 개발 후보/MSC 3종은 `development_not_for_deployment`, PUBLIC ZIP 릴리스는 별개 차단 유지.
- Windows LIVE v0.2.25 환경에서 `POLICY-DESIGN`과 protected delegation의 예산/서명·실제 select/check를 이 세션에서 검증할 접근권이 없으므로 정식 REVIEW REQUEST/READY/유료 호출을 만들지 않음. 독립 리뷰 인계만 게시; **`INDEPENDENT_REVIEW=NOT_RUN / REVIEW_REQUEST=NOT_POSTED`**. 기존 완료 MSC R1 설계 리뷰도 반복 실행하지 않음.
- 업무 회사 코드·상세 MSC·실제 Work/로그/호스트 경로/키/토큰 PRIVATE/PUBLIC 반출 0, Linux host/운영 설정/그룹 Knowledge write/Windows Task/Watcher 변경 0.

## 4. NEXT_ONE_ACTION

업무 GPT/허용 Linux Agent가 공개 `L1_WORKSPACE_LOCAL_WEB_VIEWER_LINUX_G0_READONLY_HANDOFF_r0001_20261118_KST.md`를 읽고 **A~P 16개 숫자**로 현재 호스트 근거를 회신하도록 한다(실제 실행/유료 Job 없음). 그 결과로 기존 웹 서비스/백업/권한/실 Writer가 확인되면 같은 Work에서 개인 SHADOW viewer의 구체 서비스/코드·수락 시험을 확정한다. G0 미확인/실패 시 현행 Git/원본/권한을 그대로 유지하며 `LOCAL_AUTHORITY_CUTOVER=BLOCKED`.
