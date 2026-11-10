# L1 Workspace RAG — Work 이력 보존 및 개인 모듈 지식 연계 1차 설계안 (r0001)

- Date: 2026-11-11 KST
- Project: L1-WORKSPACE-RAG-20261111-001 (협업 프로젝트 ID, 사내 실제 Work ID로 생성한 것이 아님)
- Status: DESIGN_DRAFT / INHOUSE_HOST_NOT_VERIFIED / DEPLOYMENT_NOT_APPROVED
- Scope: 기존 Kernel/Workflow/l1-github 기준 **읽기 전용 설계 검토**. 소스·사내 저장소·스킬·MCP·인덱스·운영 설정 수정 금지.
- Current CoWork transport: MIGRATION_NOT_CUTOVER, DROPBOX_LIVE. GitHub PRIVATE에 이 파일을 게시해도 Claude 자동 실행은 시작되지 않음.

## 1. 정본과 근거 수준

1. 사용자가 첨부한 `work-ledger-kernel_v0_7_37_1103.zip`: 318845 bytes, SHA-256 `8cf53c9ba14aed97b9be7b00db39ca5458ba0127ba00b9a1eef3533aba3a06a5`. ZIP의 `docs/GITHUB_WORKSPACE_LAYOUT_v2_20261007.md`와 `docs/WORK_DOCS_NAVIGATION_v0724.md`, `work_ledger_kernel/work_docs_navigation.py`·`work_ux.py`에 기존 Work 문서/탐색 계약이 존재함을 확인. 실제 사내 설치본과 Git 원격 내용은 확인하지 않음.
2. PUBLIC `wonhwipark/L1Work`의 `l1-fix-workflow_v1_6_67_1110.zip`: `docs/GITHUB_WORKSPACE_LAYOUT_v2_20261007.md`, `docs/MODULE_LIBRARY_WORKFLOW_INTEGRATION_v1661.md`, `l1_fix_workflow/module_library.py`, `github_docs.py`, `knowledge_input.py` 및 관련 테스트 파일 존재 확인. **패키지에 코드가 존재한다는 사실과 사내 통합 동작 PASS는 다름.**
3. PUBLIC `wonhwipark/L1Work`의 `l1-github_v0_3_56_1110.zip`: 저장소 역할 설정과 Push Guard 관련 파일이 있으며, `l1-workspace`는 **사내 GitHub**의 `work_docs` 역할로 관리해야 함. 사외 GitHub.com 404로 사내 저장소 부재를 판정할 수 없음. 실제 설정은 사내 `repo-config roles --json`으로 재확인 필요.
4. 선행 Dropbox `L1_Module_Detail_Knowledge_Design_r0001_20261105.md`: 개인 모듈 지식은 Work ID별 이력과 분리한 `module-library/`를 제안, 공통 지식은 `l1sw-dev-knowledge`에 선택적 승인 승격. **제안 경로이지 현재 사내 생성 완료 증거가 아님**.
5. L1 지식 로드맵 r0003 설계 리뷰: 방향 `ACCEPT_WITH_CHANGE`, 실사용 M1 `BLOCKED`. 기존 7개 실행 안전 게이트(설치/호출 경로/본문 digest/owner/root authority 등)는 정적 문서만으로 통과 처리하지 않음.

## 2. 기존 l1-workspace 구조 — 보존 계약

```text
l1-workspace/                         # 사내 work_docs 저장소
├── README.md                         # Work 대시보드
├── works/
│   └── <immutable-work-id>/
│       ├── README.md
│       ├── 문서안내.md                 # 조건부 생성·수동 작성 파일 보호
│       ├── decisions.md
│       ├── HANDOFF.md                 # PC 이동 필요 시
│       ├── ISSUE_OVERVIEW.md / FOLLOW_UP.md / WORK_DISCUSSION.md ...
│       │                               # 실제 Work 상태/내용에 따라 가변
│       ├── artifacts/                 # analysis / design / verification 등 실제 산출물
│       └── state/
│           ├── work_snapshot.json
│           ├── resume.json           # 상황에 따라 존재
│           └── resume_bundle.zip     # 상황에 따라 존재
└── index/
    ├── active.json
    └── latest.json
```

- Kernel의 Work ID/상태/Evidence 원장이 SSOT. `works/<work-id>` 폴더는 제목·상태가 바뀌어도 재명명하지 않는다.
- `index/active.json`, `index/latest.json` 스키마/생성 동작, Cross-host Snapshot/Resume, 구버전 폴더 migration 정책은 유지.
- `문서안내.md` 자동 생성 파일은 고유 표시자가 있는 경우만 해당 보호 계약 내에서 갱신. 사용자가 직접 작성한 파일, 다른 Work의 원본은 덮어쓰지 않는다.
- 위는 **패키지 설계/코드 기반 구조**다. 사내 Git 서버의 실제 최신 tree는 `NOT_VERIFIED`. 모든 Work에서 나열된 문서가 항상 존재하지는 않는다.

## 3. 개인 지식 구조 — 기존 module-library 우선 재사용

다음은 **제안 구조**이며 실제 사내 트리·스캐너와 대조하기 전 생성/강제 적용 금지.

```text
l1-workspace/
└── module-library/                     # 기존 works/와 별도 지식 영역 (실존 확인 필요)
    ├── README.md                       # module → feature → scenario 탐색
    ├── index/                          # 제안 위치: 루트 Work index/와 충돌 회피
    │   ├── by-module.md
    │   └── by-type/
    │       ├── ISSUE.md
    │       ├── FEATURE.md
    │       ├── REFACTOR.md
    │       └── DESIGN.md
    └── <module-stable-id-or-slug>/
        └── <feature-stable-id-or-slug>/
            └── <scenario-stable-id-or-slug>/
                ├── README.md          # 결론·scope·출처/검증·관련 Work
                ├── FLOW.md            # 실제 증명된 단계·조건·MSC 링크
                ├── SOURCES.md         # source revision/claim anchor
                └── HISTORY.md         # 갱신·충돌·승인·재확인
```

- 실제 `module-library` 스키마/기존 인덱스가 있으면 **기존 계약을 우선**. 위 구조를 별도 새로운 지식 저장소로 재구현하지 않는다.
- 안정 `module_id`·`feature_id`·`scenario_id`·`predicate_id`는 이름/슬러그/폴더와 독립. 실제 존재하는 Work/Evidence만 양방향 링크.
- `ISSUE / FEATURE / REFACTOR / DESIGN`은 **지식 탐색 분류**이고 Kernel 실행 프로파일 `BUG / BUG-NR / FEATURE / REFACTOR / MAINT` 변경이 아님. 일대일 대응을 강요하지 않고 필요한 경우 명시적 매핑·다중 유형 허용.
- 유형별 목차는 동일 본문 링크에서 파생되는 재생성 가능한 문서로, 기술 주장·Work 상태의 정본이 아님.
- 공통 지식 저장소 `l1sw-dev-knowledge`는 별도 owner/approval 영역. 개인 모듈 지식을 자동 승격하거나 무조건 복제하지 않음.

## 4. RAG 조회/소비 동작 계약

`사용자 질문 → 기존 Workflow/Work 의도 판단 → module-library 및 기존 그룹 지식 검색 → 실제 문서 본문 절/anchor read-only 조회 → scope/owner/root/source revision/검증 상태 검사 → 호출 직전 검증한 근거 본문을 Agent/Provider 입력 조립 경계에 주입 → 인용·적용조건·불확실성 포함 답변`

- 반드시 확인할 항목: 문서/절 안정 ID, RAT/stack/product/build/config, source branch/commit 또는 P4 CL, owner/authority 신선도, source anchor, document revision, raw/canonical body digest, 입력에 **실제로 전달된 body**와 verifier, Run/Result/Evidence/Receipt 링크.
- **검색 결과 제목/링크 또는 문서 목록을 본 것만으로 RAG 입력 주입 PASS 처리 금지.**
- 본문 해시만 Provider가 자기 보고한 경우 독립 무결성 검증으로 보지 않는다. 입력 발행 드라이버 측 최종 digest 검증과 동일 payload 사용이 필요.
- scope 불일치/오래된 revision/owner 부재/index stale/문서 prompt-injection의 지시문은 자동 확정 사실로 승격하지 않는다. 실패 시 기존 Work 조회와 코드 분석 흐름을 격리 유지.
- 별도 벡터 DB·임베딩 서버·신규 독립 스킬은 실측 검색 품질 결함이 입증되기 전까지 도입하지 않는다.

## 5. 기술 지식 갱신·배포 계약

Work 수행의 경과·결정·현재 상태·Evidence는 Kernel SSOT에 남김 → 재사용 가능한 기술 사실만 별도 문서 변경 후보로 추출 → 기존 module-library 중복/버전/충돌 분석 → `NEW / ENHANCE / CONFLICT / RECHECK` Preview → 명시적 owner·source authority·push guard 확인 → 승인 후 사내 Git 변경 → 원격 commit·readback 검증 → 새 Work에서 재검색/오적용 거부.

**금지:** 자동 Work ID 변경, 이전 증거 덮어쓰기, 미승인 지식 게시, 원격 Push 성공 추정, 그룹 지식 자동 승격.

## 6. 단계별 게이트

| 단계 | 검증 목표 | 최소 증거 | 상태 |
|---|---|---|---|
| G0 | 사내 `l1-workspace` 실제 구조·저장소 역할·설치본 버전/해시·MCP/tool ID 읽기 확인 | 사내 read-only 확인·원본 불변 | NOT_RUN |
| M1 | 개인·그룹 문서 검색→scope/해시 검증→실 Provider 입력 소비 | 입력 발행 직전 동일 body/anchor와 독립 Receipt·Evidence | BLOCKED/NOT_RUN |
| M2 | 개인 지식 후보 생성·기존 문서 대조·유형별 인덱스 Preview | 중복/경합/권한/문서 자동생성 가드 | NOT_RUN |
| M3 | 승인된 개인 지식 게시·다른 Work에서 재사용 | 사내 Git readback, 동일 scope 적용·다른 scope 거부 | NOT_RUN |
| M4 | 선택적 검색 고도화 | 성능·검색 품질 증빙 후 최소 확장 | DEFER |

기존 로드맵의 `F-B1-01`, `F-B1-02`, `F-N2-01`, `F-N2-02`, `F-N1-01`, `F-N3-01`, `F-VERS-01` 차단 게이트를 재사용한다. 서류상 명세가 있다는 이유로 구현/실행 PASS로 승격하지 않는다.

## 7. Claude Code 독립 리뷰 초점

1. Kernel 첨부 ZIP 코드 및 기존 문서로 `2`의 필수/선택 파일 구분·자동생성/수동문서 보호 정책을 확인.
2. Workflow v1.6.67 `module_library.py`, `github_docs.py`, `knowledge_input.py`의 **실제 기능**과 제안 `3`·`4`의 중복/충돌 검토.
3. 사내 Git `work_docs` 역할의 실제 repo/branch/checkout 및 기존 `module-library`, `index`를 읽기 전용으로 확인. 확인 불가 시 `NOT_RUN`.
4. 유형별 탐색 `ISSUE/FEATURE/REFACTOR/DESIGN`의 안정 ID/다중 유형/Work profile 구분·가독성.
5. 실제 RAG 문서 본문 주입·출처 추적의 검증점 및 필요한 최소 MCP 연결.
6. owner/root/revision/body digest/Provider pre-call 신뢰 경계와 기존 로드맵 7대 차단 게이트 적용 가능성.
7. Cross-host Resume, 기존 Work/Legacy 파일, dirty/diverged·symlink·untracked·동시쓰기·잘못된 source/scope의 반례.
8. 신규 스킬·DB 없이 `REUSE / CONNECT / EXTEND / DEFER`로 구현 책임 매핑하고 가장 작은 회귀 테스트 제안.

## 8. 리뷰·보안·운영 범위

- **설계 정적 리뷰만 요청.** 코드 수정·설치·사내 Git/원장 쓰기·Job enqueue·Provider 호출·운영 인덱싱·LIVE/SHADOW 전환·PUBLIC 배포는 모두 범위 밖.
- 사내 제품 소스/민감 내부 경로/기밀 로그/토큰/신뢰키/원본 내용은 GitHub PRIVATE에도 외부 게시 금지. 결과는 반출 가능한 추상화·상태만.
- 기존 Workflow v1.6.67 및 Kernel v0.7.37 원본 유지. 리뷰 결과·영수증 없이 `INDEPENDENT_REVIEW=PASS` 표기 금지.
- 이 프로젝트 문서의 GitHub PRIVATE 게시 자체는 REQUEST/READY가 아님. 활성 리뷰 LIVE는 기존 Dropbox, GitHub watcher는 아직 활성화되지 않음.

## 9. 결론

`DESIGN_DIRECTION=PROPOSED / CURRENT_TREE=NOT_VERIFIED / RAG_PROVIDER_INPUT=NOT_VERIFIED / INDEPENDENT_REVIEW=NOT_RUN`.

우선 사내 기존 `work_docs` 및 `module-library`를 읽기 전용으로 확인하고, 기존 Kernel/Workflow 인터페이스에 **최소 연결**을 적용할 수 있는지 독립 검토한다. 실제 변경은 별도 승인과 호스트 검증 후 판단한다.
