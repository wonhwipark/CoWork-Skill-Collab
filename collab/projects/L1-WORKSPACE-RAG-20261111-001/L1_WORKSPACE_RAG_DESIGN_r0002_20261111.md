# L1 Workspace RAG — Work 유형 및 브랜치별 AS-IS 코드 MSC 보강 설계 (r0002)

- Date: 2026-11-11 KST
- Project: `L1-WORKSPACE-RAG-20261111-001` (사외 협업 프로젝트 ID; 사내 Work ID가 아님)
- Supersedes as **design proposal**: `L1_WORKSPACE_RAG_DESIGN_r0001_20261111.md` (원본 보존)
- Status: `DESIGN_REVISION / INHOUSE_NOT_VERIFIED / DEVELOPMENT_NOT_FOR_DEPLOYMENT`
- Transport: `MIGRATION_NOT_CUTOVER / DROPBOX_LIVE`
- Change boundary: **문서 설계만**. Workflow v1.6.67, Kernel 원본, l1-github, 사내 Git/Work/DB/MCP/Job-list/운영 환경 변경하지 않음.

## 1. GPT 판정 요약

**ACCEPT_WITH_CHANGE (설계 방향)**. r0001의 기존 Kernel Work 이력 보존, 개인 `module-library`와 그룹 `l1sw-dev-knowledge` 구분, 검색→본문→실제 Provider 소비 검증, 별도 벡터 DB 보류 원칙은 유지한다.

**필수 추가:** 개별 Git 브랜치/커밋 또는 P4 기준의 현재 코드 분석으로 작성하는 MSC는 `CODE_ANALYSIS` 유형의 Work로 생성할 수 있다. 다만 **ISSUE/FEATURE/REFACTOR Work 안에서 생성한 동일한 AS-IS MSC는 그 Work의 유형을 바꾸지 않고 산출물 유형 `MSC_AS_IS`로 관리**한다. WORK 분류, 산출물 종류, 지식 탐색 태그, 실행 프로파일을 동일한 필드로 합치지 않는다.

현재 확인 사실:
- 기존 Kernel의 `work_ledger_kernel/work_ux.py::WorkUX.export_docs()`는 기존 Work Snapshot들로 루트 `README.md`와 `index/active.json`, `index/latest.json`을 재생성한다. 루트 README만 수동 수정하면 다음 Export 때 사라질 수 있다.
- `work_docs_navigation.py`가 `ISSUE_OVERVIEW.md`, `FOLLOW_UP.md`, `WORK_DISCUSSION.md`, `CODE_CHANGE_NOTE.md`, `REQUIREMENTS.md`, `DESIGN_CURRENT.md`, `CODE_FACTS.md`, `MSC_VIEW.md` 등 존재하는 문서를 링크한다. 중복 탐색기 개발 금지.
- Kernel의 `work_purpose=TRACKING_ONLY/ENGINEERING`, `profile=BUG/BUG-NR/FEATURE/REFACTOR/MAINT` 등은 **새 Work 유형과 다른 축**이다.
- 사용자 확인: 사내 `l1-workspace`에 Work 유형 분류 필드가 현재 없다. 현장 파일/설치본/인덱스의 실제 상태와는 별개의 사용자 제공 사실로 취급.
- 사내 GitHub `l1-workspace`는 외부 GitHub MCP로 접근되지 않는다. 사내 `l1-github`의 `work_docs` 역할/로컬 Git을 이용한 읽기 전용 G0가 필요.

## 2. 4개의 분리된 분류 축 (혼동 금지)

| 축 | 권장 표현 | 뜻 | 근거/제약 |
|---|---|---|---|
| **Work 주목적** | `work_category=ISSUE / FEATURE / REFACTOR / DESIGN / CODE_ANALYSIS / UNCLASSIFIED` | 사용자가 해당 Work를 시작한 주된 이유 | 사용자/승인된 기존 메타데이터로 확정; 문서명 자동 추론 금지 |
| **산출물 유형** | `artifact_kind=CODE_FACTS / MSC_AS_IS / MSC_TO_BE / HLD / TEST_RESULT / ...` | 문서의 성격 | `CODE_ANALYSIS` Work 외에서도 `MSC_AS_IS` 존재 가능 |
| **지식 탐색 맥락** | `module_id / feature_id / scenario_id`, `knowledge_tags` | 재사용 가능한 모듈·피처·시나리오 탐색 | 실제 지식 본문/키의 안정 ID와 링크; Work 유형을 지식의 유일 카테고리로 강제하지 않음 |
| **실행/운영** | 기존 Kernel `work_purpose`, `profile`, status | 수행·권한·라이프사이클 | 현재 계약 유지. 신규 유형으로 실행 권한을 유추하지 않음 |

- 독립적인 '브랜치 B의 현재 DRX MSC' 요청이면 Work `CODE_ANALYSIS`, 산출물 `MSC_AS_IS` 후보.
- 'DRX 타이밍 버그 분석' ISSUE Work에서 생성한 현재 코드 MSC면 Work `ISSUE` 유지, 산출물 `MSC_AS_IS`.
- 'DRX 동작 개선 후 예상 MSC'는 FEATURE 또는 DESIGN Work의 `MSC_TO_BE`이고, 코드 적용/검증 전에는 현재 코드의 사실로 표현하지 않음.
- `UNCLASSIFIED`은 기존/불명확한 Work의 비파괴 기본값. 제목, 디렉터리명, `DESIGN_CURRENT.md` 존재 여부로 확정 분류 금지.
- `work_category`는 **제안된 신규 메타데이터**이며 현 Kernel의 구현 기능이라고 주장하지 않음. 변경 이력/근거/확정 actor와 보존·재분류 계약은 설계 및 회귀시험 후 결정.

## 3. 개별 브랜치/리비전의 AS-IS MSC — 신뢰 경계

'현재 코드'는 불변인 기준을 반드시 동반한다. 다음은 **제안 메타데이터 계약**이다.

| 필드 | Git (예: SMP1900) | P4 (예: SMP1800/1770) |
|---|---|---|
| product/stack/module/feature/scenario | 승인된 식별자 | 승인된 식별자 |
| source_system, source_repository | `GIT` + 사내 승인된 repo ID | `P4` + 승인된 depot/client 식별 |
| requested_ref | 사용자 지정 branch (표시/조회용) | 요청한 stream/client/CL 범위 |
| **pinned_source_revision** | **전체 commit SHA** | **실제 haveRev/file#rev/CL 증거 조합** |
| source_root/host & worktree | 사내 실측 코드 root 및 식별자 | 사내 실측 client/root |
| tree_state | CLEAN 또는 DIRTY/UNTRACKED 판정 | haveRev/local modify/opened 판정 |
| analysis_revision, generated_at | MSC/분석 자체 개정과 생성 시점 | 동일 |
| evidence | 코드 근거/검증 조건·scope, 내부 참조 | 코드 근거/검증 조건·scope, 내부 참조 |
| validation | VERIFIED / PREVIEW_ONLY / STALE / UNKNOWN | 동일 |

**필수 규칙:**
1. branch는 이동하는 포인터이므로 '브랜치명만 있는 현재 MSC'를 검증된 정본으로 보지 않는다. commit 전환/리베이스 시 기존 MSC 덮어쓰기 대신 새로운 source revision 관계를 기록한다.
2. Dirty/untracked 또는 HEAD와 분석 대상이 다른 경우, 작업 트리 실측 없이 `VERIFIED` 표시 금지. 실제 workspace snapshot/분석 범위 증거가 확보되기 전 `PREVIEW_ONLY` 또는 BLOCKED.
3. 동일 DRX 모듈이 Branch A와 Branch B에 존재해도 두 MSC의 source revision을 분리한다. 별도 **revision comparison** 작업에서만 차이 분석하며 어느 쪽도 무조건 '최신'으로 선택하지 않는다.
4. Work 문서의 CODE_FACTS와 MSC는 출처/시나리오와 연결한다. **MSC는 분석 결과/파생 설명이며 소스 코드 사실의 독립된 최종 증거가 아니다.** 코드 근거와 회귀 검증을 인용한다.
5. MSC participant는 기존 사용자 규칙인 마지막 의미 있는 모듈 폴더 기준의 단일 이름 사용(예: `TxMngr`, `DRX`, `BCH`, `RF_BLOCK`). 세부 조건·변수는 필요 시 CODE_FACTS 상세 절로 보내고 MSC는 인터페이스 흐름 가독성 우선. 실제 폴더 대응은 코드에서 검증.
6. 회사 코드/제품 로그/상세 사내 경로/내부 MSC 원문은 **GitHub PRIVATE 협업 저장소에도 업로드 금지**. 본 계약은 사내 구현을 위한 비민감 추상 설계임.

## 4. 기존 l1-workspace 구조 및 권고 링크

```text
l1-workspace/                       # 사내 work_docs; 실제 원격 tree G0 미검증
  README.md                         # Kernel Export가 생성하는 Work 대시보드
  works/<immutable-work-id>/
    README.md / 문서안내.md / decisions.md / HANDOFF.md (존재 조건별)
    ISSUE_OVERVIEW.md / CODE_FACTS.md / DESIGN_CURRENT.md ... (존재 조건별)
    artifacts/analysis/             # CODE_FACTS + branch/revision별 MSC_AS_IS 후보
    artifacts/design/               # MSC_TO_BE 후보 (실제 기존 명명 규칙 먼저 확인)
    artifacts/verification/
    state/work_snapshot.json        # Work ID/상태/출처, 분류 필드 확장 시 하위호환
  index/
    active.json
    latest.json                     # 기존 machine index schema 반드시 유지
  module-library/                   # 과거 설계 제안, 실제 존재/스캐너 호환성 미확인
    README.md                       # module → feature → scenario 탐색 후보
    <module>/<feature>/<scenario>/  # 지식 정본 링크/버전 가설, 실제 경로 미확정
```

- **기존 구조를 보존**하고 `work_category`가 실제 도입될 경우 Kernel Export의 Snapshot/README 렌더 지점에서 파생 색인 생성. 별도 `index/by-type/` 또는 `module-library/index/by-type/` 생성은 현재 reader·기존 자동 인덱스와 중복 여부를 먼저 확인. 확정된 경로가 아님.
- Work 중심 대시보드와 module-library 기술지식 탐색은 별도 페이지/뷰다. 서로 링크하되 원문을 이중 복제하지 않는다.
- Kernel `work_docs_navigation.py`의 기존 안내/수동 파일 충돌 보호, Snapshot ID 확인, symlink 보호를 유지. Work ID·원장·Cross-host state·legacy migrate 변경 금지.
- 사내 그룹 지식은 별도 `l1sw-dev-knowledge`; 승인 전 개인 지식을 자동 복제/승격하지 않는다.

## 5. RAG 질의: 브랜치와 시나리오 기준 정확한 코드 지식 반환

```text
질문(제품+브랜치/리비전+모듈/시나리오)
 → intent: Work 이력 vs AS-IS 코드 흐름 vs TO-BE 설계 vs Branch Diff
 → l1-github/승인된 source-root registry에서 요청 코드 기준 해석(읽기 전용)
 → module-library/그룹 지식 후보 검색, 기존 Work evidence link 조회
 → 실제 문서 anchor/body + source revision + scope + owner 확인
 → 요청 HEAD/CL과 지식 출처가 맞는지 검증 (모르면 NO_MATCH/STALE)
 → 입력 발행 드라이버의 최종 payload·digest 검증
 → 실제 Agent/Provider가 받은 동일 body에 한해 근거 인용 답변
```

- 예: 'SMP1900 Branch B DRX 동작 MSC'는 B의 **실측 commit**과 동일한 AS-IS 증거만 반환. A의 분석을 섞어 B의 사실로 답하지 않는다.
- 'Branch A와 B 비교'는 각각의 고정 SHA, MSC/원문 근거를 병렬 확인하고 `DIFF`에 두 revision을 표기. 결과가 없으면 자동 합성 사실 금지.
- '특정 branch의 현재 코드'인데 branch HEAD의 현장 확인이 없으면 '현재'라고 단정하지 않고 마지막 확인 시점을 명시.
- 모델이 지식 문서에 포함된 명령/프롬프트를 실행 권한으로 오해하면 안 된다. RAG 본문은 **비신뢰 입력 데이터**.
- 단순 GitHub 문서 링크/제목의 검색 결과, Provider 자기 보고 해시는 실제 본문 소비 PASS 증거가 아니다. Driver 전/후 실제 payload equality와 Receipt/Evidence가 필요.
- 기존 roadmap G0/M1 blocker(`F-B1-01/02`, `F-N2-01/02`, `F-N1-01`, `F-N3-01`, `F-VERS-01`) 모두 유지. M1 `BLOCKED`를 해제하지 않는다.

## 6. 기존 스킬 책임과 최소 변경 제안

| 대상 | REUSE / CONNECT / EXTEND / DEFER | 설계 범위 |
|---|---|---|
| `work-ledger-kernel` | **EXTEND 후보** | 사용자 승인 가능한 Work 분류 필드와 이력, Snapshot/export README 유형별 파생 색인. 기존 index 스키마·Work SSOT는 불변 |
| `l1-fix-workflow v1.6.67` | **REUSE / CONNECT 설계** | 기존 code-analysis/module-library/knowledge_input 경로 및 Git/P4 scope. **이번 회차 원본 수정 없음** |
| `code-analyzer` | **REUSE / CONNECT** | pin된 source revision의 CODE_FACTS 및 MSC 근거 연결; 실제 코드 함수/실행 검증 필요 |
| `doc-converter`, `hld-composer` | **REUSE / DEFER** | AS-IS/TO-BE 표기, MSC 가독성/participant 규칙; 이미 가능한 기능 중복 구현 금지 |
| `l1-github` | **REUSE** | 사내 `work_docs` 역할과 Git branch/HEAD/status 검증·승인된 Push Guard. 외부 MCP 연결을 요구하지 않음 |
| `job-list` / Provider driver | **CONNECT (blocked)** | 실제 설치·Profile/ID·source root·pre-call digest·Receipt 집행; 운영 호출은 미승인 |
| 새 DB/embedding/전용 RAG skill | **DEFER** | 실제 검색 실패/품질 증빙 전 불필요 |

모든 책임은 실제 설치본·코드·인터페이스 확인 후 확정. 후보 ZIP 버전과 운영 설치/승인 상태 혼동 금지.

## 7. G0~M4 완료/차단 기준

| Gate | 최소 확인 및 부정시험 | 상태 |
|---|---|---|
| G0 | 사내 work_docs role, 실제 branch/tree/snapshot, 설치 ZIP 승인 상태·version/hash, source root, MCP/tool mapping, 현행 type field 실측 | **NOT_RUN** |
| M0 (추가 설계 검증) | CODE_ANALYSIS/UNCLASSIFIED 분류 계약, 기존 Work 호환, source SHA/P4 revision, AS-IS vs TO-BE, dashboard 재생성/충돌 반례 | **DESIGN_ONLY** |
| M1 | 선택된 source/branch와 일치하는 document body/anchor가 **실제** Provider 입력·독립 Receipt/Evidence에 남음. 다른 branch/stale/dirty 차단 | **BLOCKED / NOT_RUN** |
| M2 | 승인된 개인 지식 후보/모듈 인덱스 Preview·중복/경합/충돌/다중 scope 구분 | **NOT_RUN** |
| M3 | 승인된 사내 Git 게시 + commit/readback + 타 Work 재검색 + 틀린 branch/scope 거부 | **NOT_RUN** |
| M4 | 품질 데이터 확인 후 고급 검색 결정 | **DEFER** |

필수 부정 회귀: (a) Branch A SHA로 Branch B 질문 답변 금지, (b) branch 이름은 같지만 HEAD 변한 경우 STALE, (c) Dirty/untracked를 verified로 표시 금지, (d) 동일 Work ISSUE 안의 AS-IS MSC가 CODE_ANALYSIS Work로 오분류되지 않음, (e) 수동 `문서안내.md` 유지, (f) 기존 `index/active.json`과 `latest.json` schema 호환, (g) Cross-host 과거 Snapshot 불변, (h) 검색 결과만 있어도 body/driver digest 미확인이면 Provider 소비 PASS 금지.

## 8. 독립 리뷰 및 운영 안전

- 현재 r0001 인계서 존재만 확인됨. 기존 예측 경로의 Claude 리뷰 결과/영수증은 **미확인**, 따라서 `INDEPENDENT_REVIEW=NOT_RUN`.
- 새 리뷰 인계 `CLAUDE_DESIGN_REVIEW_HANDOFF_r0002_20261111.md`는 이 델타에 집중. 리뷰어는 source/r0001과 diff만 검토해도 되며 요구 범위 밖의 유료/운영 실행은 하지 않는다.
- GitHub 문서 게시 ≠ watcher REQUEST/READY. 공식 Dropbox LIVE 리뷰는 별도로 유효 서명·정책·비용 승인 절차가 필요.
- 본 문서가 사내 Git 설치·코드 변경·Work 이력·유료 모델 호출·PUBLIC 배포·LIVE 전환을 승인하지 않는다.

## 9. 최종 GPT 설계 판정

`DESIGN_DIRECTION=ACCEPT_WITH_CHANGE` / `DEVELOPMENT=DESIGN_ONLY` / `SELF_TEST=STATIC_SOURCE_CHECK_ONLY` / `INDEPENDENT_REVIEW=NOT_RUN` / `INHOUSE_TREE=NOT_VERIFIED` / `RAG_PROVIDER_INPUT=NOT_VERIFIED`.

**다음 한 동작:** Windows Claude Code가 PRIVATE `main`의 r0002 인계서를 별도 독립 세션으로 읽고 **정적 설계 리뷰**를 수행(사용자가 명시적으로 실행했을 때만). 동시에 사내 실제 tree/installed tools 실측은 권한/보안 범위 내에서만 read-only, 조회 불가 항목은 NOT_RUN으로 격리한다.
