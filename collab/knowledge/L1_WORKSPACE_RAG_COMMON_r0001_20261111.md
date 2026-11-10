# CoWork 공통 지식 — L1 Workspace RAG·Work 분류·브랜치별 MSC

- Revision: `r0001` / 2026-11-11 KST
- Location: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`, `collab/knowledge/`
- Classification: **NON_SENSITIVE_SHARED_CONTEXT / POINTER_ONLY + VERIFIED_ABSTRACTS**
- Scope: 새 GPT 대화·설계 리뷰·Claude 인계 시 재사용할 **공통 맥락**. 특정 프로젝트 최신 실행 상태나 승인·실제 구현 완료를 선언하는 정본이 아님.
- Authoritative live status: `collab/projects/L1-WORKSPACE-RAG-20261111-001/CURRENT.md`의 **가장 최신 섹션** 및 실제 결과/영수증.
- CoWork transport: **MIGRATION_NOT_CUTOVER / DROPBOX_LIVE**. 이 문서 게시만으로 GitHub watcher·Windows Claude Code·GPT가 자동 실행되지 않음.

## 1. 새 창·협업 공통 진입 규칙

1. 이 문서와 프로젝트의 **최신** `CURRENT.md`를 순서대로 읽는다.
2. RAG `r0002`, 최신 GPT 자체 구조적 리뷰, Claude Code 리뷰 인계서 및 이후 추가된 리뷰 결과·영수증을 확인한다.
3. 새 요청이 기존 리뷰와 동일하다면 **완료된 자체 리뷰를 처음부터 반복하지 말고 델타·미해결 BLOCKING·추가 실측을 중심으로 처리**한다.
4. `GPT_SELF_REVIEW`는 GPT 자체 리뷰이며 `CLAUDE_INDEPENDENT_REVIEW`와 별개. 문서 게시·인계서 작성·READY 준비·리뷰 호출·완료·승인 상태를 각각 구별한다.
5. 사용자에게 추가로 긴 사내 로그/원문을 옮기도록 요구하지 않는다. 이미 공개된 비민감 계약과 사내 측 최소 객관식/상태/근거수준 정보를 활용한다.
6. 원본 설계 r0001·r0002와 기존 Work 기록을 덮어쓰거나 삭제하지 않는다. 새 판단은 개정본과 `CURRENT.md` 최신 섹션에 연결한다.

**권위 순서:** 사내 승인된 실제 설치·실측 증거(E3) > 실제 소스/합성시험(E2) > 문서/설계(E1) > 미확인(E0). 실측이 없으면 `NOT_VERIFIED/NOT_RUN/BLOCKED`를 유지한다.

## 2. 저장소·환경 매핑 (프로젝트별로 공통)

| 역할 | 위치 | 분리해야 하는 개념 |
|---|---|---|
| 사내 개인 Work/문서 | **사내 GitHub `l1-workspace`** (`l1-github` role: `work_docs`) | 사외 GitHub.com 계정의 동일 이름 저장소가 아님. 현재 외부 MCP로 조회 불가 |
| 사내 개인 모듈 지식 | `l1-workspace/module-library/` **제안/실존 미확인** | Work Ledger 이력과 구분; Module → Feature → Scenario 본문 |
| 사내 공통·팀 지식 | `l1sw-dev-knowledge` (knowledge 역할) | 개인 지식의 자동 승격 금지 |
| 사내 제품 Git 코드 | SMP1900 계열 Git checkout/branch/worktree (사내 실제 root는 실측 필요) | 코드 기준 branch+full commit SHA |
| 사내 P4 제품 | SMP1800/1770 등 (실제 client/haveRev/CL 확인 필요) | P4는 Git SHA와 동일화 금지 |
| 사외 협업 기준 | PRIVATE `wonhwipark/CoWork-Skill-Collab` | **비민감 설계·인계·리뷰·판정·상태만** |
| 사내 다운로드용 ZIP | PUBLIC `wonhwipark/L1Work` | 별도 승인된 **최종 배포본만** 게시 |
| 실제 리뷰 운송 LIVE | Dropbox `/SKILL-COLLAB/` | GitHub PRIVATE 문서 게시와 정식 REQUEST/READY는 별개 |

**보안:** 회사 원본 코드/상세 사내 경로/특허/고객 정보/토큰/키/제품 로그/내부 MSC 원문은 **PRIVATE GitHub에도 반출 금지**. 인용하는 문서·파일은 사외 게시 허용 여부를 먼저 판단. `/AI-CONTINUITY/`, 운영 watcher/DB/WAL/SHM/Bridge/Telegram/Job/호스트 설치는 별도 승인 전 불변.

## 3. 기존 Kernel 기반 Work 문서·탐색 구조 (설계 기준)

```text
l1-workspace/                         # 실제 사내 tree는 아직 미검증
  README.md                           # Kernel이 Export로 재생성하는 Work 대시보드
  works/<immutable-work-id>/
    README.md / 문서안내.md / decisions.md
    HANDOFF.md                        # 필요 시
    ISSUE_OVERVIEW.md / FOLLOW_UP.md / WORK_DISCUSSION.md
    CODE_CHANGE_NOTE.md / REQUIREMENTS.md / DESIGN_CURRENT.md
    CODE_FACTS.md / MSC_VIEW.md       # 조건부 생성; 항상 있다고 가정 금지
    artifacts/{analysis,design,verification}/
    state/{work_snapshot.json,resume.json,resume_bundle.zip}   # 조건별
  index/
    active.json
    latest.json                       # 기존 schema 유지
  module-library/                     # 기존 제안 경로; 사내 실제 존재 미검증
```

- Kernel의 Work ID·Ledger/Evidence 기록이 SSOT. 폴더명은 Work ID 고정. 다른 PC Snapshot/Resume·과거 Work 마이그레이션/Dirty/Reconcile 보호 계약 유지.
- `work_ledger_kernel/work_ux.py::WorkUX.export_docs()`가 root `README.md`, `index/active.json`, `index/latest.json`을 생성한다. **root README 직접 수정으로 영속적인 기능 구현 불가**.
- `work_docs_navigation.py`는 기존 Work의 실제 존재 문서를 `문서안내.md`에 한글로 연결한다. 자동생성 marker가 없는 수동 `문서안내.md`를 덮어쓰지 않음. 기존 안내 및 Work 기록을 새 탐색기로 중복 생성하지 않음.
- `module-library`의 실제 schema/scanner/marker/frontmatter 및 기존 index는 사내 G0 전까지 정본이라고 가정하지 않는다.

## 4. 분류는 네 개의 독립 축

| 축 | 개념 및 후보 값 | 결정 원칙 |
|---|---|---|
| **Work 주목적** | `ISSUE / FEATURE / REFACTOR / DESIGN / CODE_ANALYSIS / UNCLASSIFIED` | **제안 신규 `work_category`**. 사용자 확인/승인 근거로 지정, 기존 Work 미분류는 `UNCLASSIFIED` |
| **산출물 종류** | `MSC_AS_IS / MSC_TO_BE / CODE_FACTS / HLD / TEST_RESULT` 등 | **제안 `artifact_kind`**. Work 유형과 별개, Evidence ID와 연결 |
| **지식 탐색** | `module_id / feature_id / scenario_id / knowledge_tags` | 재사용 가능한 지식/시나리오 탐색, 동일 본문의 파생 인덱스 |
| **실행 정책** | 기존 `work_purpose`, `profile`, work status | 현재 Kernel 계약 유지. 분류값이 권한/실행 승인 근거 아님 |

- 독립적인 브랜치의 '현재 코드 흐름을 분석해 MSC 생성'은 **`CODE_ANALYSIS` Work + `MSC_AS_IS` 산출물**.
- ISSUE Work 도중 생성한 AS-IS MSC는 **Work는 ISSUE**, 산출물만 `MSC_AS_IS`. FEATURE·REFACTOR 역시 동일 원칙.
- TO-BE 설계의 MSC는 `MSC_TO_BE`; 실제 코드가 구현·검증되기 전 **AS-IS로 승격 금지**.
- 단순 `DESIGN_CURRENT.md`의 존재로 Work의 `DESIGN` 분류를 추정하지 않는다.
- `work_category`는 **현재 구현 확인된 필드가 아니다**. 사용자는 사내에 해당 필드가 없다고 확인. field authority·old/new revision·actor·cross-host conflict·legacy fallback 설계/시험이 선행되어야 한다.

## 5. 브랜치별 AS-IS MSC 및 검색의 공통 계약

**지식과 분석 산출물은 SourceSnapshot에 귀속되며, 이동하는 branch 이름에만 귀속되지 않는다.**

`SourceSnapshot` **설계 후보**:
`product_id, RAT/stack, source_system(GIT|P4), repo_or_depot_authority, root_id, requested_branch_or_ref, pinned_revision, scope_files_and_digest, dirty/untracked_or_P4_haveRev_status, analysis_time, tool_version, evidence_ids, source_anchor_ids`.

- Git: **전체 commit SHA** + 사용자가 요청한 branch + 실측 checkout/root/dirty status. Branch HEAD drift·rebase·force-push 시 최신 여부 재확인, 무단 overwrite 금지.
- P4: **실제 file#haveRev와 client/CL**, 여러 파일의 CL 하나가 같은 소스 revision을 뜻한다고 가정 금지.
- 동일 코드 SHA라도 적용 product/RAT/module scope, owner, 작업 트리 조건이 다르면 오적용 금지. 동일 SHA·검증된 동등 scope는 중복 재사용 검토 가능.
- MSC participant 표시는 마지막 의미 있는 폴더의 가독형 이름(예: `TxMngr`, `DRX`, `BCH`, `RF_BLOCK`). **표시명 ≠ 안정 participant ID ≠ 담당 owner**. 동명 폴더/다른 product 충돌 보호.
- MSC는 가독형 **파생 설명**. 검증 가능한 CODE_FACTS/원본 출처/anchor 및 source revision이 없으면 `VERIFIED` 아님. 인터페이스 흐름 중심, 조건·세부 변수는 코드 사실 링크로 연결.
- RAG: **질문 scope → 코드 pin 검증 → 문서 검색 → 실제 anchor/body 조회 → owner/root/source/version 검증 → trusted driver의 pre-call body·digest 검증 → 실제 Provider 입력 전달 → Result/Evidence/Receipt**. 링크나 검색 결과만 보고 성공 처리 금지.
- 상태 의미 분리: `UNCLASSIFIED`(Work 목적 미확정), `UNKNOWN`(증거 불명), `STALE`(source drift), `PREVIEW_ONLY`(사용/게시 제한).
- 새 DB/embeddings/별도 RAG 엔진/중복 `index/by-type`은 실제 기존 reader와 검색 품질 결함 확인 전 `DEFER`.

## 6. 최신 구조적 자체 리뷰의 공통 위험·게이트 (2026-11-11 기준)

**이미 실행된 GPT 자체 리뷰 결과**: `GPT_SELF_REVIEW_STRUCTURAL_r0001_ON_RAG_r0002_20261111.md`.

- Kind: **`GPT_SELF_REVIEW`**, Status `COMPLETED_WITH_GAPS`. **Claude 독립 리뷰/영수증 아님**.
- Issues: **BLOCKING 5 / MAJOR 8 / MINOR 3**.
- Kernel v0.7.37 격리 합성·관련 pytest **11 PASS / 1 FAIL**. FAIL은 기존 exporter 출력과 옛 테스트 README 문구 기대 불일치로 확인했으며 **r0002 신규 회귀라고 단정하지 않음**.
- BLOCKING: (B-01) 실 Provider body/D_call/D_payload 소비 신뢰 드라이버 부재, (B-02) Git/P4 SourceSnapshot 원자적 연결 미완성, (B-03) Kernel `code_rev.py` scope digest symlink 이탈·빈 glob 경계, (B-04) Work export에 포함될 수 있는 사내 민감 산출물의 사외 반출 권한, (B-05) 실제 설치 버전/Job/owner/root/tool ID 미검증.
- MAJOR 우선: 독립 CODE_ANALYSIS Work에서 CODE_FACTS/MSC 자동 탐색 공백, MSC 이름 substring/manifest 연결 한계, `work_category` 이력/old-new PC 호환, CODE_FACTS→MSC Evidence chain, 대형 Git worktree 성능, participant 안정 ID, 기존 테스트 baseline FAIL.
- **G0** 사내 read-only role/tree/installed versions/owner/root/MCP tool mapping: `NOT_VERIFIED`. **M1** 실 Provider 본문 입력·증거 연결: `BLOCKED / NOT_RUN`.
- SELF_REVIEW 결과가 나왔다고 구현/사내 시험/정식 Claude 리뷰의 완료 상태를 올리지 않는다. BLOCKING 수정·재검증은 별도 작업/승인·실측이 필요.
- 새 창에서는 먼저 이 결과를 읽고 `B-01~B-05`와 실제 새 변경분부터 판정한다. 동일 구조적 GPT 리뷰를 근거 없이 재수행하는 대신 **새 입력/코드 변경이 존재할 때** delta review를 명시한다.

## 7. 보유 스킬 18개 감사 자료 — 시간·검증 수준 주의

사용자 제공 출처: `L1_KNOWLEDGE_ROADMAP_18_SKILLS_DIRECT_CHECK_20261110.md` (2026-11-10 KST 스냅샷).

- 당시 **18개 중 17개 ZIP 존재 확인**, 7개 추출 텍스트/manifest 확인, 10개는 파일 존재만; `skillsilent` 독립 ZIP 미발견은 사내 설치 부재 증거가 아님.
- 로드맵에 필요한 재사용 축: `work-ledger-kernel`(Work/Evidence/Exporter), `l1-fix-workflow`(orchestration/module-library), `code-analyzer`(code facts), `doc-converter`/`hld-composer`(MSC/HLD), `l1-github`(role/branch/readback), `p4-code-owner`(P4 관련), `issue-analyzer`(그룹 knowledge), `job-list`(job gate).
- 첨부 보고서는 이전 ZIP 이름(예: Workflow v1.6.65, l1-github v0.3.54)을 기록했다. 이후 확인된 PUBLIC `L1Work/main`에는 Workflow **v1.6.67**, l1-github **v0.3.56** 파일이 있다. 파일 존재/패키지 소스 검토는 **실제 사내 설치·배포 승인·RAG E2E PASS와 다르다**.
- `job-list`의 Profile/Job ID 우회(F-B1-01/02), owner(F-N1-01/F-N3-01), provider D_call(F-N2-01/02), release gate(F-VERS-01) 등 기존 차단 게이트를 누락하지 않는다.
- 보유 스킬 ZIP을 전부 재개발하거나 18개 실검증을 자동 요구하지 말고, **해당 변경 파일·이미 아는 결함·실제 집행 진입점** 중심으로 검사한다.

## 8. 프로젝트 정본 링크 (모든 새 창 공통)

> 저장소 **PRIVATE** `wonhwipark/CoWork-Skill-Collab`, 브랜치 `main`; 아래 모든 경로는 저장소 상대 경로.

| 정본 | 상대 경로 | 사용법 |
|---|---|---|
| **최신 프로젝트 상태** | `collab/projects/L1-WORKSPACE-RAG-20261111-001/CURRENT.md` | **항상 가장 먼저 읽고 최신 섹션 기준** |
| RAG 설계 r0002 | `collab/projects/L1-WORKSPACE-RAG-20261111-001/L1_WORKSPACE_RAG_DESIGN_r0002_20261111.md` | 4축·SourceSnapshot·RAG 경계 |
| GPT r0002 변경 판정 | `collab/projects/L1-WORKSPACE-RAG-20261111-001/GPT_ASSESSMENT_AND_DELTA_r0001_20261111.md` | r0001→r0002 기존 판정 |
| **GPT 구조적 자체 리뷰** | `collab/projects/L1-WORKSPACE-RAG-20261111-001/GPT_SELF_REVIEW_STRUCTURAL_r0001_ON_RAG_r0002_20261111.md` | 이미 완료된 5/8/3 지적 및 시험 증거 |
| Claude 독립 리뷰 인계 | `collab/projects/L1-WORKSPACE-RAG-20261111-001/CLAUDE_DESIGN_REVIEW_HANDOFF_r0002_20261111.md` | **인계/준비만 완료**, 실행·영수증 아님 |
| 이전 원본 | `collab/projects/L1-WORKSPACE-RAG-20261111-001/L1_WORKSPACE_RAG_DESIGN_r0001_20261111.md` | 역사 원본 보존 |
| GitHub 협업 진입점 | `collab/START_HERE.md` | LIVE/보안/승인/운영 경계 |

**최신 상태 값은 이 공통 문서의 작성 시점 스냅샷이다. `CURRENT.md`와 실제 리뷰/결과/영수증이 이후 바뀌면 반드시 최신 증거를 우선한다.**

## 9. 재사용할 새 창 GPT 요청 (그대로 전달 가능)

```text
GitHub PRIVATE wonhwipark/CoWork-Skill-Collab의 main 브랜치에서
collab/knowledge/L1_WORKSPACE_RAG_COMMON_r0001_20261111.md와
collab/projects/L1-WORKSPACE-RAG-20261111-001/CURRENT.md를 먼저 읽어줘.

RAG 설계 r0002, 최신 GPT_SELF_REVIEW 결과와 이후 리뷰/영수증을 확인해.
이미 수행된 GPT 자체 구조적 리뷰는 반복하지 말고, 실제로 변경된 설계/코드,
미해결 BLOCKING 5건과 G0/M1 게이트를 중심으로 델타 검토해줘.

Kernel·Workflow·RAG·GitHub 역할, CODE_ANALYSIS Work와 MSC_AS_IS/TO_BE의
분리, Git/P4 SourceSnapshot 및 source/owner/root 권한, 기존 18개 스킬
재사용·중복·호환성·부정 회귀시험을 점검해.

이슈는 BLOCKING/MAJOR/MINOR, E0~E3, 수용/수정 수용/거절/보류로 구분하고,
현실적인 다음 한 동작을 판정해. 새 결과가 있을 때만 비민감 MD를
GitHub PRIVATE의 해당 프로젝트에 게시하고 원격 readback을 검증해.

이 작업이 자체 검토라면 REVIEW_KIND=GPT_SELF_REVIEW로 기록해.
Claude Code 독립 리뷰로 간주하지 마. 운영 watcher/DB/Job/Telegram,
스킬 설치본, 사내 Git, REQUEST/READY, PUBLIC 배포, LIVE 전환은 변경하지 마.
```

## 10. 현재 승인/실행 상태

`COMMON_DOC=SHARED_REFERENCE`; `DESIGN=REVISED_R0002`; `GPT_SELF_REVIEW=COMPLETED_WITH_GAPS`; `INDEPENDENT_CLAUDE_REVIEW=NOT_RUN`; `INHOUSE_HOST=NOT_VERIFIED`; `M1_RAG_PROVIDER=BLOCKED`; `SOURCE_PATCH/PACKAGE/DEPLOYMENT=NOT_RUN`; `LIVE=DROPBOX_LIVE`.

이 공통 정보 등록 자체는 신규 리뷰 요청/유료 호출/코드 변경/실행 승인/운영 이관이 아니다.
