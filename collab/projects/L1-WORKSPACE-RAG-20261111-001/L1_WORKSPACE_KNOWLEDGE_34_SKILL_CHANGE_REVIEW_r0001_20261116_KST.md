# L1 Workspace Knowledge 분리 설계 — 업무 GPT 회신 및 관리 스킬 수정 범위 검토

- 문서: `L1_WORKSPACE_KNOWLEDGE_34_SKILL_CHANGE_REVIEW_r0001_20261116_KST.md`
- 작성: 2026-11-16 KST / 개정 r0001
- 관련 CoWork Work: `L1-WORKSPACE-RAG-20261111-001` (기존 Work 재사용)
- 목적: 업무 GPT에게 제안할 두 업무 스킬 요구사항을 확정하고, 우리가 관리하는 세 스킬의 실제 수정 후보를 **구현 전 코드 정적 조사**에 근거해 판정
- 판정: **DESIGN=ACCEPT_WITH_CHANGE / 코드 수정=NOT_RUN / 독립 설계 리뷰=결과 미수신 / 업무 호스트 E3=NOT_VERIFIED**
- 범위 제외: 실제 `l1-workspace/knowledge/` 폴더 생성, 업무 호스트 스킬 변경·설치, 그룹 지식 게시, 새 Kernel Profile/schema, 운영 Job/유료 호출/PUBLIC ZIP 게시

## 1. 결론 — 수정 대상은 3개 모두가 아니라, 기존 기능으로 해결할 수 없는 부분부터

**사용자 합의:** 개인 `l1-workspace`의 최상위에 사람이 탐색할 `knowledge/` 폴더를 둔다. `l1-knowledge-updater`만 해당 폴더를 WRITE 하고 `l1-fix-workflow`는 READ_ONLY. `works/<work_id>/`와 Work/Evidence의 정본은 기존 Kernel 소유. Updater가 직접 분석하거나 Workflow Work를 지식화할 때 관련 기존 Work ID와 검증된 Evidence를 재사용한다. 그룹 검증 지식 정본은 기존 `l1sw-dev-knowledge`의 승인된 writer로 게시한다.

**이번 조사에 따른 보완:** 폴더가 다르더라도 같은 Git repository의 root `README.md`, Git index/checkout, pending changes, 공통 원장 갱신에서는 충돌할 수 있다. 스킬의 자연어 선언만으로 쓰기 권한이 분리되지는 않는다. 따라서 `knowledge/` 단독 WRITE는 **공통 Git writer의 인증된 호출자·허용 파일 경로 검증과 동시성 통제**까지 포함해야 한다.

| 순위 | 구성요소 | 이번 판정 | 필요한 대응 |
|---|---|---|---|
| P0 | `l1-fix-workflow` | **최소 보호 보완 후보** | `knowledge/`를 쓰는 작업을 확실히 금지하되 기존 그룹 지식 READ 경로와 Work docs 동작 보존. 실제 우회 경로 조사 |
| P0 | `l1-github` | **공통 writer 경계 점검 우선** | 현재 repo/remote Push guard는 폴더별 쓰기 권한이 아님. 검증된 actor/허용 path + staged diff를 writer에서 강제할 수 있는지 확인; 없으면 최소 보호 기능 후보 |
| P1 | `work-ledger-kernel` | **기존 exporter·Work writer 우선 재사용** | `knowledge/` 보존과 root README 탐색 링크 여부 시험. 기존 `Work` 기록 경로가 그룹 게시 결과 참조를 수용하는지 확인. gap이 확인된 경우만 소규모 보완 |
| 업무 GPT | `l1-knowledge-updater` | **TO-BE 요구 제안** | 지식 폴더 유일한 콘텐츠 writer, 기존 Work/Evidence 인계·후보·Preview·상태 추적·그룹 게시 조정·실패 복구 |
| 업무 GPT | `l1sw-dev-knowledge` | **TO-BE 요구 제안** | 승인받은 내용만 게시, 기존 ID·variant/revision 충돌 확인, 실제 게시 commit/내용 readback과 추적 가능한 결과 반환 |

**사전 확정 금지:** 세 스킬을 무조건 수정하거나 신규 `KNOWLEDGE` Profile/별도 Work 원장/Knowledge DB/별도 CAS 엔진을 추가하지 않는다. 아래 근거·미확인 표에 따라 REUSE → CONNECT → 입증된 GAP만 최소 EXTEND.

## 2. 검토에 사용한 정확한 소스

| 구분 | 실제 조회한 ZIP | 근거와 범위 |
|---|---|---|
| Workflow | CoWork PRIVATE `main`: `collab/projects/L1-WORKSPACE-RAG-20261111-001/candidates/l1-fix-workflow_v1_6_69_1115.zip` | ZIP 866,671 bytes, `SKILL.md`, `l1_fix_workflow/github_docs.py`, `l1_fix_workflow/group_knowledge_bridge.py` 원문 정적 조회. 개발 후보 / 호스트 설치본 아님 |
| GitHub | CoWork PRIVATE `main`: `collab/projects/L1-WORKSPACE-RAG-20261111-001/candidates/l1-github_v0_3_57_1114.zip` | ZIP 602,555 bytes, `SKILL.md`, `scripts/push_guard.py`, `scripts/l1_github.py` 원문 정적 조회. 개발 후보 / 호스트 설치본 아님 |
| Kernel | PUBLIC `wonhwipark/L1Work/main`: `work-ledger-kernel_v0_7_42_1116.zip` | ZIP 320,083 bytes, `SKILL.md`, `work_ledger_kernel/kernel.py`, `work_ledger_kernel/work_ux.py`, `work_ledger_kernel/work_refs.py`, `work_ledger_kernel/work_docs_navigation.py` 및 관련 기존 테스트 원문 정적 조회. PUBLIC 게시 사실 ≠ 업무 호스트 설치 |

기존 협업 판정 근거의 SHA-256: Workflow v1.6.69 `d4ba119298cd5763fd18ace2d54223fff010a8d2a1703ebab80eb4fa1b35846b`, GitHub v0.3.57 `f1b8fb43d3af427f2c5d52864051c65894f3cb45969ab35ca502f344735611ce`, Kernel v0.7.42 `ece2bce143ef35a1c8cc3bc12ddf6a73e27e0f218fc69fec87844759d9dfc164` (이전 원격 바이트 검증 기록의 값). **이번 세션의 ZIP 전체 CRC·회귀시험 및 호스트 E3는 NOT_RUN**.

관련 정본: `collab/CONTEXT_BRIEF.md`, Work `CURRENT.md`, `L1_WORK_TO_KNOWLEDGE_FLOW_r0002_20261115_KST.md`, 기존 `L1_WORKSPACE_KNOWLEDGE_FOLDER_UPDATER_HANDOFF_r0001_20261116_KST.md`, `collab/knowledge/SKILL_CAPABILITY_CATALOG.md`.

## 3. 요청하신 4개 확인 항목에 대한 코드 근거 판정

### Q1. 기존 Workspace exporter/indexer가 `knowledge/`를 지원하거나 충돌하는가?

**확인된 구현:** Kernel `work_ledger_kernel/kernel.py`의 `work_docs_export()`는 `work_ux.export_docs()`로 위임한다. `work_ux.py:609`부터 exporter는 `works/`, `index/`와 루트 `README.md`를 생성·갱신하고, `work_docs_navigation.py`는 개별 Work 탐색 안내를 생성한다. `tests/test_github_docs_layout_v077.py`는 `works/<work_id>/README.md`, `index/active.json`, `index/latest.json`, root README를 검증한다. 현재 검토 범위에는 별도 `knowledge/` 생성/갱신 기능이 나타나지 않는다.

**중요:** 이것만으로 `knowledge/`가 exporter와 충돌한다거나 완벽하게 보존된다고 확정할 수 없다. exporter가 별도 루트 폴더를 건드리지 않는지, root README 생성 과정의 링크 유지 여부, migration/cleanup의 전체 안전성을 **격리 회귀시험**으로 확인해야 한다.

**수정 후보:** 우선 Updater가 독립적으로 `knowledge/README.md` 및 Module별 인덱스를 작성하고 기존 `index/` 기계 파일은 건드리지 않는다. 사람이 GitHub 루트 README에서 한 번에 찾도록 하려면, Kernel `work_ux.py` root README의 **안전한 `knowledge/README.md` 링크 표시만** 최소 확장 후보로 검토한다. 이 때 Kernel은 `knowledge/` 파일을 READ만 하며 직접 WRITE 하지 않는다. 현재 URL·경로·symlink 검증과 사람이 수정한 root README 보호를 유지한다.

판정: **기존 Work exporter REUSE / Knowledge 인덱스 연결 CONNECT / root 탐색 링크는 필요성·시험 확인 후 최소 EXTEND 후보**.

### Q2. Workflow의 `knowledge/` 쓰기를 실제로 차단 가능한가?

**확인된 구현:** Workflow `l1_fix_workflow/group_knowledge_bridge.py`는 그룹 지식 조회에 관해 read-only로 설계돼 있다. 그러나 이것은 `l1-workspace/knowledge/`의 쓰기 금지와 **서로 다른 경계**다. Workflow `l1_fix_workflow/github_docs.py:125`의 `docs_sync()`는 Work 문서 export 전에 해당 checkout이 dirty/untracked이면 차단한다. `docs_push()`는 저장·Git 게시 경로이고 부가 staged path 가능성을 가진다. `l1-github/scripts/push_guard.py:136`의 `verify()`는 canonical repository role, root, Push URL 등 **목적지 저장소 안전성**을 확인하지만, 이번 정적 확인에서는 `knowledge/`의 **호출자별 파일 경로 WRITE 금지**가 입증되지 않았다.

**꼬임 A — 미커밋 `knowledge/` 파일:** Updater가 `knowledge/`에 파일을 생성했지만 commit/push하지 않으면 Workflow의 `docs_sync`는 **저장소 dirty 상태 때문에 차단**될 수 있다. 다른 폴더를 수정하므로 무충돌이라는 해석은 틀리다.

**꼬임 B — 원격 commit 경합:** Updater와 Workflow가 독립 Git 명령으로 동시에 commit/push하면 충돌 가능. 단일 Git writer·직렬화·staged path 검증·expected remote head 확인이 필요하다.

**꼬임 C — 우회:** Workflow 프롬프트에 “read-only”만 적어도, 동일 Git 자격증명으로 raw shell/다른 provider 경로에서 파일을 쓰면 실제 차단이 아니다. GitHub `CODEOWNERS`나 문서 경계만으로 단독 파일쓰기 권한을 보장할 수 없다.

**수정 후보:** `l1-fix-workflow`의 관련 명령·`docs_push` 경유에서 `knowledge/` 직접 수정 요청을 거절하고, `l1-github`의 **신뢰 가능한 공통 writer에서** 호출자 식별·repo role=`work_docs`·최종 변경 파일 목록·`knowledge/` 포함 여부를 비교하여 승인되지 않은 writer의 변경을 fail-closed. `knowledge/` 쓰기는 검증된 Updater 요청만, Work export는 `works/`·기존 generated root/index 허용 목록만. 단 인증된 actor 식별 기능이 없다면 임의 환경변수만으로 인증을 가장하지 않는다. 기존 raw Git 우회가 남으면 `HARD_ENFORCEMENT=NOT_VERIFIED`를 유지한다.

판정: **기존 그룹 Knowledge READ REUSE / Workflow 지침 CONNECT / 실제 경로 WRITE 차단은 확인된 writer 강제수단에 따라 최소 EXTEND 후보**.

### Q3. Updater가 Kernel의 허용 기록 계약으로 기존 Work에 이력을 추가할 수 있는가?

**확인된 구현:** Kernel `kernel.py:534`에 `record_evidence`, `:1364`에 `work_reference_find`, `:1368`에 `work_reference_add`, `:1380`에 `work_create`가 있다. `cli.py`에는 `context`, `record`, `docs-export` 진입점이 존재한다. `work_refs.py:17`의 `REF_TYPES`는 **`jira`, `alias`, `github_pr`, `p4_cl`, `code_root`만** 허용한다.

**중요한 확정 제약:** `work_reference_add(work_id, "knowledge", value)`는 현재 타입 허용 목록에 없으므로 **직접 지원되지 않는다**. `alias`나 `code_root`를 Knowledge 링크인 것처럼 사용하는 오용 금지. 임의 `record.json`, Work README, registry/schema 직접 수정도 금지.

**수정 방향:** Updater는 기존 Work ID를 유일 매칭한 뒤 실제 근거를 허용된 `record_evidence`의 kind/stage/provider 계약으로 등록하거나, 검토·게시 이력은 기존 `context`/Artifact/Work 문서 허용 타입 중 **실제 데이터 의미와 일치하는 경로**에만 append한다. 지원되지 않으면 `LINK_PENDING / ADDITIONAL_CHECK_REQUIRED`; 기존 기록 경로로 표현이 불가능하다는 근거와 회귀 결과가 있을 때에만 Kernel 링크 표현을 최소 확장 후보로 제안한다. 기존 Work/Evidence의 삭제·덮어쓰기 금지.

판정: **Work 생성/검색/일부 기록 REUSE 가능, 정확한 지식 게시 링크 기록 계약은 설치본 I/O·허용 enum 대조 전 미확인**.

### Q4. 그룹 게시 후 개인 Knowledge 상태와 원 Work 역링크를 안전하게 갱신할 수 있는가?

**현재 확인 범위:** 공개·PRIVATE에 있는 우리 세 패키지만으로 Updater·그룹 writer의 실제 반환값, 승인/중복방지 CAS, 원격 readback, 게시 영수증 및 복구 기능까지 확정할 수 없다. 업무 GPT가 두 스킬 설치본의 기존 함수·예외·권한·결과 타입을 직접 확인해야 한다.

**강제 순서:** 후보·Preview → 유효 승인·고정 대상 revision 검증 → **그룹 writer 게시** → 실제 원격 commit/content readback → Updater 전용 `knowledge/` 후보에 게시 결과·상태 반영 → 원래 Work(복수 origin 가능)에 허용된 Kernel 기록으로 역링크. 게시 상태와 링크 상태는 분리하고, 각 원격 readback을 검증한다.

**실패 처리:** 응답 유실 시 원격 history/receipt 정산 전 **재게시 금지**. 그룹 게시 성공 + 개인 상태 갱신 실패 시 개인 상태만 복구. 그룹 게시 성공 + Work 역링크 실패 시 Work 링크만 복구. 기존 evidence/MSC 원본과 이전 게시 revision은 보존하고, 같은 지식의 신규 임시 Work를 만들지 않는다.

판정: **업무 스킬 G0 미조회 / 목표 계약 제안 가능 / 그룹 게시·역링크 E3 NOT_RUN**.

## 4. 우리 3개 스킬별 '실제 손댈 후보' 우선순위

| 우선 | 스킬 및 근거 파일 | 확인된 현재 동작 | 수정 검토 포인트 | 지금 판정 |
|---|---|---|---|---|
| P0 | `l1-fix-workflow/SKILL.md` | `module-library` 조회·후보, 그룹 지식 읽기 전용 bridge, Work docs 관리 | `l1-workspace/knowledge/`는 Updater 소유임을 문서·라우팅에 명확화. 순수 조회를 쓰기 요청으로 바꾸지 않음 | CONNECT 후보 |
| P0 | `l1-fix-workflow/l1_fix_workflow/github_docs.py` | `docs_sync()` dirty guard; `docs_push()` Work docs 게시 | `extra_paths`/단계별 staging이 `knowledge/`를 수정·게시할 수 있는지 점검. Workflow 호출에서 protected path DENY 및 기존 dirty guard 유지 | 조사 후 최소 보호 후보 |
| P0 | `l1-github/scripts/push_guard.py` + 실제 commit/stage 진입점 | repo/remote/root/role 검증 | 최종 staged/commit diff 기준 허용 경로를 **인증된 writer 경계에서** 확인. Updater만 knowledge/ 변경 가능하도록 호출자 검증; 다른 Git action 우회 경로 점검 | 입증된 gap일 때 최소 EXTEND |
| P0 | `l1-github` repo-config/provider 정책 | `work_docs` role과 `knowledge` role 매핑 | 두 저장소 역할과 `work_docs/knowledge/` **하위 폴더**를 혼동하지 않기. 기존 등록·token 유지, 추가 actor/credential 모델은 기존 실측 후 | REUSE + 추가 확인 |
| P1 | `work-ledger-kernel/work_ledger_kernel/work_ux.py:609` | 기존 `works/` + `index/` + root README exporter | `knowledge/`를 훼손하지 않는지 격리 시험. root README에 유효 `knowledge/README.md` 링크 추가 필요 시 표시-only 확장; exporter는 knowledge/에 WRITE 금지 | REUSE 먼저, 확장은 조건부 |
| P1 | `work-ledger-kernel/work_ledger_kernel/work_docs_navigation.py` | Work별 안내 링크 파생 | 원본 Work 탐색을 유지; knowledge/ 인덱스의 writer가 되도록 확대하지 않기 | 변경 불필요 우선 |
| P1 | `work-ledger-kernel/work_ledger_kernel/work_refs.py:17` | 참조 타입 5개 제한 | `knowledge` 타입 임의 추가 금지. 기존 context/artifact/evidence에 게시/역링크 의미를 정확히 기록할 수 있는지 검증 후 필요할 때만 최소 확장 | **현 단계 수정 보류** |
| 보류 | Kernel profile/record schema/registry | 기존 Work ID·프로파일·Evidence 계약 | 신규 `KNOWLEDGE` Profile, 2차 Work ID, 임의 원장/메타데이터 필드 | **변경 금지** |

**권장 적용 순서:** (1) 격리된 exporter·docs_sync 동작 시험 → (2) writer와 실제 stage/push 변경 경로 정적 추적 → (3) 기존 허용 Work 기록 타입 매핑 → (4) 입증된 최소 보호만 패치 → (5) 경계/회귀시험 → (6) 기존 승인에 따른 후보 ZIP·리뷰·배포. 이번 요청은 **수정 범위 검토**, 실제 스킬 수정·패키징 지시가 아님.

## 5. 업무 GPT에 제안할 두 스킬의 상세 요구사항

### 5A. `l1-knowledge-updater` — 요구사항 (현재 구현 완료 주장 아님)

- **입력 두 경로:** (A) Module/Procedure/Feature 지식 분석 직접 요청, (B) 기존 Workflow Work ID에 연결된 결과 지식화. 불명확한 Work 검색은 유일 매칭 전 자동 신규 생성 금지.
- **근거:** Work ID/ledger identity, Evidence ID·원본/해시, PUML/MD 원본과 HTML/SVG 파생물, source revision/scope/제품·빌드, 기존 Knowledge ID/variant를 현재 설치 데이터 구조로 참조. Code Analyzer가 유효 근거를 이미 만들었다면 중복 분석 금지.
- **저장:** `knowledge/README.md` + Module→Feature→Scenario별 사람이 읽기 쉬운 후보·링크 인덱스 작성은 **Updater만 WRITE**. 후보에는 개인 초안/보완 대기/그룹 게시 확인 상태를 구별. GitHub에서 Work ID를 몰라도 찾을 수 있어야 함.
- **개인 Work:** 기존 Kernel의 허용된 API로 직접 분석·판정·그룹 게시 결과를 같은 원래 Work에 append. Work ID·Profile·원본 Evidence/MSC 변경 금지. N:M origin Work를 누락하지 않음.
- **Git 동시성:** 공통 승인된 writer의 actor/path 검증과 직렬화/expected revision을 사용. 무조건 shell Git Push·원격 RESET 금지. 스킬 프롬프트 속 '유일 writer' 표기만으로 실제 권한 보장이라고 선언 금지.
- **게시:** 후보·Preview·중복/충돌·권한·source/target revision 검증 후 기존 그룹 writer에 승인된 변경만 전달. 실제 그룹 readback 뒤에만 게시 완료.
- **실패 회수:** 그룹 게시·개인 Knowledge 상태·원래 Work 링크를 독립 기록/복구. 같은 operation의 원격 게시 여부가 불명확하면 HOLD하고 임의 재게시하지 않음.
- **정보 보호:** 개인 제한 Code Evidence/경로/로그/MSC 원문이 그룹/CoWork/PUBLIC로 유출되지 않도록 정보등급 필터. 공개된 링크가 있다고 내용 접근권이 부여되지 않음.

### 5B. `l1sw-dev-knowledge` — 요구사항 (현재 구현 완료 주장 아님)

- **정본:** 기존 Module→Feature→Scenario 지식 및 Procedure 교차 탐색, HLD/상세설계/확인된 AS-IS MSC와 승인된 TO-BE를 각각 분리.
- **입력:** Updater가 생성한 승인 대상·기존 Knowledge ID/variant·write set·고정 근거·기준 대상 revision; 실제 writer가 권한·승인 범위를 재검증.
- **중복/충돌:** 기존 ID·내용·variant 중복 확인, CREATE/UPDATE 대상 충돌 검사. 승인 이후 바뀐 대상·근거를 조용히 덮어쓰기 금지.
- **결과:** 게시 성공 시 실제 Knowledge ID/variant, commit/revision, content digest 및 readback 근거를 반환. 게시 실패·충돌·응답 유실을 구분하고, 원격 이력 조회로 이미 반영된 operation인지 확인 가능한 기존 계약 재사용.
- **권한:** 그룹 스킬의 writer는 그룹 저장소 정본만 소유하고 개인 `knowledge/`나 Kernel `works/`를 직접 수정하지 않음. Updater가 개인 결과를 조정.

### 5C. 업무 GPT가 회신할 표 (실제 설치 근거를 요구)

| 체크 | 업무 스킬 실측 질문 | 답변 요구 |
|---|---|---|
| U01 | Updater의 실제 Work 선택/재개, Kernel 기록/원격 readback 함수·입력 타입은? | 실제 파일·함수·호출 조건·지원/미지원 |
| U02 | `knowledge/` 생성/인덱싱/WRITE 경로 및 호출자·repo 역할/권한은? | 기존 경로 매핑·경로 차단·동시성 보장 근거 |
| U03 | Preview, 기존 Knowledge ID/variant, 중복/충돌·승인, write set·target revision 처리 현황은? | REUSE/CONNECT/GAP/미확인 |
| U04 | 그룹 writer 게시·결과·원격 readback·응답 유실 정산은? | 실제 성공/실패 계약과 보류 조건 |
| U05 | 그룹 게시 결과 → 개인 `knowledge/` 상태 → 원래 Work(복수) 역링크는? | 단계별 저장 주체, 허용 Kernel 이벤트, 복구 계획 |
| U06 | 설치본 버전/구현과 이번 GPT의 개발 패키지 간 차이는? | 코드/계약 사실과 미실행 E3의 분리 |

## 6. 충돌/회귀 검증 시나리오 — 다음 격리 시험용, 전부 NOT_RUN

| ID | 입력·상황 | 필수 수락 조건 |
|---|---|---|
| T01 | 기존 Work exporter 실행, 별도 `knowledge/` 파일 존재 | `knowledge/` 파일 내용·해시 유지, `works/`·`index/` 정상, 예기치 않은 삭제·move 0 |
| T02 | root README 생성/재생성 | `knowledge/` 탐색 경로 표시 필요성·링크 유효성 확인, 수동 문서 파괴 금지 |
| T03 | Updater의 `knowledge/` 파일 변경 미커밋 | Workflow `docs_sync`의 기존 dirty 차단 유지, 미커밋 파일 누락·우회 없음 |
| T04 | Workflow가 `knowledge/`를 docs_push extra_paths/stage | 권한 없는 변경 0, pre-commit/pre-push 단계에서 차단 |
| T05 | Workflow raw Git/provider 우회 시도 | 실제 신뢰 경계에서 거부; 불가능하면 HARD_ENFORCEMENT 미검증으로 기록 |
| T06 | Updater와 Workflow 동시 Git 쓰기 | serial/expected remote head 불일치 차단, 누락/덮어쓰기 0 |
| T07 | Work 검색에서 다중 후보 | 신규 Work 중복 0, 불명확 자동 매칭 0 |
| T08 | 기존 Work의 Evidence·MSC·Source Revision 재사용 | 유효 근거로 재분석 0, 다른 소스/범위면 현재 사실 승격 금지 |
| T09 | Kernel 허용 ref_type 밖 Knowledge 값 전달 | 명확히 거부, 기존 타입을 가장해 저장 0 |
| T10 | Updater가 기존 Work에 실제 허용 event/artifact 기록 | 원본 보존, append/readback 성공, 재실행 중복 0 |
| T11 | Preview 후 그룹 기준 revision 변경 | 승인 재검토·그룹 write 0 |
| T12 | 그룹 게시 성공 + 응답 유실 | 원격 영수증 정산 후 중복 게시 0 |
| T13 | 그룹 게시 성공 + 개인 knowledge 갱신 실패 | 개인 상태만 복구, 그룹 재게시 0 |
| T14 | 그룹 게시 성공 + Work 역링크 실패 | Work 링크만 복구, 그룹 재게시 0 |
| T15 | 한 지식에 복수 Work 원본 | origin 근거 모두 보존, Work별 링크 상태 독립 |
| T16 | 미승인 후보를 Workflow/RAG가 읽음 | 그룹 확정 사실로 오인 0; source/current 적용성 검사 |
| T17 | symlink/path traversal/동명 대소문자 경로 | 쓰기 0, repo 외부 탈출 0, Work 본문 훼손 0 |
| T18 | 과거 승인·철회·branch 변경/롤백 | 원본·승인·게시 이력 보존, 현재 적용성 재검증 |

**시험 상태:** T01~T18 `NOT_RUN` (설계 수락 기준). 과거 MSC 패키지 자체시험이나 별도 Work 테스트를 여기의 완료 근거로 승격하지 않음.

## 7. 업무 GPT 전달용 단일 요청 문구 (3,000자 이내)

> 첨부 `L1_WORKSPACE_KNOWLEDGE_34_SKILL_CHANGE_REVIEW_r0001_20261116_KST.md`를 기준으로, 실제 설치된 `l1-knowledge-updater` 및 `l1sw-dev-knowledge` 두 스킬의 기존 계약만 **읽기 전용 G0**로 확인해줘. `l1-workspace/works/`의 원본 Work·Kernel Evidence 보존, 최상위 `knowledge/`의 Updater 단독 WRITE / Workflow READ_ONLY, Module→Feature→Scenario 탐색, 기존 Work 결과 재사용, 후보·Preview·유효 승인→그룹 writer 게시/readback→개인 상태·원 Work 역링크가 목표야. 새 Kernel KNOWLEDGE Profile·별도 원장·schema·분석 엔진 추가는 기본 금지. U01~U06에 대해 설치 파일·함수·허용 입력/출력·권한/충돌/복구 근거를 표로 정리하고 각 항목 REUSE/CONNECT/입증된 최소 EXTEND/미확인을 구별해줘. 기존 writer/approved scope 확인 전 Work·그룹·metadata 쓰기, 설치, 모델/Job 재실행은 하지 마. 실제 첫 승인 분석 E3를 문서 QA로 PASS 처리하지 말고, 가장 작은 다음 검증 한 동작과 미확인 조건을 회신해줘.

## 8. 작업·승인 경계 및 다음 행동

- 이번 수행: **패키지 원본 정적 조사 및 설계/수정 범위 판정만**, 스킬 코드 수정·패키징·업무 호스트 설치·운영 DB/Job/그룹 정본 쓰기 **NOT_RUN**.
- 협업 독립 설계 리뷰 결과: 기존 CoWork 요청의 결과/실행 근거 미수신 — 완료로 표시 금지. 별도 유료 리뷰/서명/READY 신규 생성 없음.
- 가장 중요한 다음 한 행동: **우리 세 스킬의 격리 테스트에서 T01(Exporter의 knowledge 보존)과 T04(Workflow의 knowledge 변경 차단)를 먼저 실측한 후, 업무 GPT의 U01~U06 설치본 결과와 합쳐 최소 변경 파일/회귀 범위를 확정.**
- 기존 Work의 상세 개발·시험·리뷰 이력은 CoWork PRIVATE Work `CURRENT.md`와 관련 결과 문서를 그대로 유지한다. 본 문서는 기존 정본/영수증을 덮어쓰지 않는다.
