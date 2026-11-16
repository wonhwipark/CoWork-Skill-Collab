# L1 Knowledge Updater — 개인/그룹 Knowledge 충돌 처리·쓰기 권한 스킬 설계 r0002
- 기준: 2026-11-17 KST / CoWork Work `L1-WORKSPACE-RAG-20261111-001`
- 판정 근거: `GPT_FIXED_KNOWLEDGE_R1_REVIEW_DISPOSITION_r0001_20261117_KST.md`
- 계승: `GPT_KNOWLEDGE_1TO4_FIXED_DESIGN_FOR_CLAUDE_r0001_20261116_KST.md` ①~④와 `L1_WORK_TO_KNOWLEDGE_FLOW_r0002_20261115_KST.md`
- 단계: **DESIGN_ACCEPT_WITH_CHANGE**. 구현/호스트 설치/실제 Knowledge write/그룹 게시/코드 시험은 NOT_RUN.
- 원칙: **REUSE → CONNECT → 입증된 최소 EXTEND**. 신규 Knowledge Profile, 2차 원장, 전용 RAG/merge 엔진, 근거 없는 API·필드 추가 없음.
- 민감한 소스·MSC 원문·사용자 토큰·회사 자료를 CoWork PRIVATE/PUBLIC에 게시하지 않음.

## 0. 동작 범위와 고정 결정
1. ① 개인 업무용 `l1-workspace/knowledge/`는 **실제 그룹 공용 `l1sw-dev-knowledge`가 관리하는 현행 지식 파일의 물리 계층·ID·파일 규칙**을 미러링. 원본 그룹 폴더 위치와 group writer는 G0에서 확인할 것. 그 전에는 폴더를 추측해 만들지 않음.
2. ② 개인 `knowledge/`의 콘텐츠 WRITE 요청 주체는 **`l1-knowledge-updater`만**, `l1-fix-workflow`는 READ_ONLY. `works/`와 Evidence 작성은 기존 Kernel 허용 writer가 담당. 동일 Git credential 기반 CLI 우회가 남으면 **보호 완료로 판정 금지**.
3. ③ Work ID는 **optional**. Workflow-origin 지식만 기존 Work ID/N:M origin을 가진다. Updater 직접 지식 정리는 Work를 억지로 만들지 않음. 원래 Work/Evidence는 삭제·변조하지 않음.
4. ④ 그룹의 변경과 개인 편집을 Base/Ours/Theirs로 대조. 자동 merge 성공은 Preview 후보일 뿐 **사용자 승인 아님**. 유효 승인·최신 원격 HEAD/CAS·readback 이후 개인 상태를 갱신.

## 1. 각 정본과 재사용 경계

| 계층/스킬 | 책임 | 변경 원칙 |
|---|---|---|
| `l1-fix-workflow` | 업무 분석·기존 Work 선택·Evidence 연결; 그룹·개인 Knowledge 조회 | 개인 `knowledge/` 직접 쓰기 금지(bootstrap·파일쓰기·stage/push 전). 기존 Work flow 영향 최소화 |
| `work-ledger-kernel` | `works/<id>/`, Evidence, index, export, 기존 기록 API | `knowledge/` 재생성·삭제 금지. T01/T02 뒤 필요시 루트 README 탐색 링크만 보완. `knowledge` ref_type 선제 금지 |
| `l1-github` 및 실제 writer | Git 대상·스테이지·경로·HEAD·push 제어 | 기존 guard 재사용 여부 확인. 인증된 caller/path allowlist·직렬화·CAS 부족 **입증될 때만** 최소 보완 |
| 업무 `l1-knowledge-updater` | 지식 기준본 가져오기·개인 수정·후보·3-way/Preview·게시 orchestration·개인 상태/복구 | 그룹 writer 직접 대체하거나 독립 DB를 만들지 않음. 개인 Knowledge 원문은 Updater만 수정 |
| 업무 `l1sw-dev-knowledge` | 검증된 그룹 기술 지식의 승인·게시·readback | 실제 writer/ID 규칙·중복/충돌 인터페이스 G0 확인 전 호출·게시 금지 |
| code-analyzer/doc-converter | 코드 사실·MSC 원본, Markdown/HTML/SVG 변환 | 이미 검증된 Evidence 재사용; Knowledge 목적 재분석 금지 |

**두 진입**: (A) Updater 직접 Module/Procedure/Feature 지식 갱신, (B) Workflow의 기존 Work/Evidence를 Updater 후보로 전환. A는 기존 Work가 실제 있는 경우 재개/연결하되, 단순 Knowledge 편집은 무조건 Work 생성하지 않음. B는 재분석 없이 Work 원본·source revision 고정. 두 흐름은 개인 초안 → 그룹 기준 대조 → Preview/승인 → 그룹 게시/readback → 개인 상태 정산에서 합류.

## 2. BLOCKING B01 해소 — Kernel ref_type을 속이지 않는 origin 연결

- **필수 정본 방향**: Knowledge 파일에서 원 Work로 가는 provenance(Work ID, 관련 Evidence/MSC/source revision의 기존 안전한 참조)를 **개인 Knowledge의 허용된 본문/기존 메타 구조**에 보존. 해당 지식이 Work 유래가 아닐 때 Work 링크 없음. 그룹 게시 시 개인용 Work/Evidence의 비공개 위치·원문은 **write set에서 제외**하고 필요한 비민감 출처만 별도 승인. 그룹 파일의 구조·schema에 이 필드를 새로 강요하지 않음.
- **원래 Work에서 Knowledge로 돌아가는 링크**는 두 번째 연결이다. Kernel의 기존 `context/record_evidence`/허용 Work 문서 append 동작이 **정확히 이 의미를 수용하는 경우**에만 기존 writer로 남긴다. `work_refs.REF_TYPES`의 `jira/alias/github_pr/p4_cl/code_root`를 knowledge로 오용하지 않음.
- 기존 Kernel 기록 계약이 Knowledge 출처·링크를 표현하지 못하면 `WORK_SIDE_LINK=PENDING_UNSUPPORTED`로 분리. 지식 쪽 origin 참조와 그룹 readback을 보존하며, Work-side 링크를 강제하는 스키마 수정·거짓 SUCCESS 금지. **이 경우 전체 '양방향 링크 완료' 판정은 차단**, 추후 실제 gap에 대한 최소 EXTEND 별도 판정.
- 개인 Knowledge에 origin을 넣는 기존 지원 형식이 없다면 새로운 frontmatter 키/sidecar를 창작하지 않음. **`ORIGIN_STORAGE=BLOCKED_G0`**; 그룹 구조·writer·개인/그룹 필드 분리 가능 여부 실측 필요. 개인 전용 origin을 그룹에 전파하거나 무단 삭제하지 않음.
- 동시성 때문에 Work/Knowledge 링크 기록 실패가 그룹 재게시를 발생시키면 안 됨. 각 연결 단계의 완료 상태는 기존 유효 저장/영수증을 활용.

## 3. MAJOR M01/M02 — 실제 WRITE 강제와 직렬화

**권장 실행 경계(설계 후보, 설치 확정 아님)**: 기존 단일 인증된 Git writer 재사용을 우선. Workflow에 **Group/Workspace 읽기 전용 credential과 읽기 전용 checkout/OS 권한**, Updater/신뢰 writer에 **별도 제한된 쓰기 credential 및 소유 checkout/worktree**가 실재함을 증명. Workflow에는 writer 자격증명·서명키·raw push 권한을 주지 않음. 원본 Git repo는 동일해도 clone별 index를 분리하면 공유 staging 경합을 축소할 수 있음. 독립 checkout 구성은 호스트 G0·보존/롤백 승인 후만 적용.

- **중요**: 동일 OS 계정·쓰기 credential으로 Workflow가 raw Git/shell에 접근한다면 프롬프트·pre-commit hook·`push_guard`만으로 'Updater 유일 WRITE'를 보장할 수 없음. 이때 `POLICY=FIXED`, `HARD_ENFORCEMENT=NOT_VERIFIED`, 개인/그룹 보호 경로의 실제 쓰기·게시 **BLOCKED**. guard는 심층 방어이며 credential 격리 대체 불가.
- writer는 인증된 실행 주체(사용자 문자열·env var만 신뢰 금지), 실제 repo/root/realpath, git staged + unstaged + untracked 변경, rename의 old/new path, symlink/경로탈출, 최종 commit 대상 path allowlist를 확인. `knowledge/` 콘텐츠는 검증된 Updater writer만 허용. Work exporter는 `works/`·기존 `index/`·유효한 root README만 허용하며 `knowledge/`는 READ.
- **동시 작업**: per-checkout writer lock(기존 기능 우선), 저장소 dirty/untracked 판정 → 결정된 write set 검증 → stage → staged diff 재검증 → commit → latest HEAD 재조회/expected ref 검증 → push → readback. lock 없거나 owner/race 불분명할 경우 **RETRY 없이 HOLD**. 서로 다른 checkout도 같은 원격 ref 경쟁은 expected-head/CAS가 처리. 기존 guard로 호출자 인증이 안 되는 경우 미구현으로 남김.
- read-only Workflow 조회는 계속 허용하되 타인 지식의 수정 작업은 Workflow에 자동 위임 금지.

## 4. MAJOR M03/④ — 그룹 sync와 3-way 안전 조건

**기준 revision을 정확히 구분**:
- `group_base_commit`: 초기 가져온 **그룹 전체 commit SHA** (그룹 writer가 승인한 안정 branch/ref 기준). 게시 CAS와 기준 앵커.
- 각 knowledge 파일: **그룹 원본 경로 + 파일 blob/content hash(SHA-256) + 복원 가능한 Base 내용**. group commit만 같아도 파일 식별자가 바뀌면 구조 변경으로 판단. 물리 상태 저장 방식은 기존 Git refs/기존 updater 저장소 계약을 **G0에서 확인**; 새 manifest·DB를 미리 요구하지 않음.
- `Ours`: 개인의 현재 편집본/관련 metadata; `Theirs`: 게시 직전 그룹 HEAD에서 가져온 해당 파일. Base 복원 실패, hash 불일치·권한 오류면 HOLD.

| 상황 | 동작·수락 조건 |
|---|---|
| 그룹 HEAD 미변경 | 개인 diff로 Preview → 대상/승인/HEAD 재검증 → 게시 |
| 그룹 HEAD 변경, 파일 변경 비중첩 | Git 3-way 후보 + **문서 의미/링크 검토 Preview** → 사용자 승인 → HEAD CAS 후 게시 |
| 내용 중첩/충돌 | 개인 변경·그룹 변경 모두 보존, 자동 게시 0. 사용자 선택·갱신 Preview |
| **rename/move/delete, ID/variant 변경**, 경로 구조 충돌 | **항상 STRUCTURAL_CONFLICT/HOLD**, Git 자동 rename 탐지·nonoverlap 판정만으로 처리 금지 |
| 승인 후 원격 HEAD 재변경 | stale Preview·승인 무효, 다시 비교/사용자 승인. force push 금지 |
| 개인 미게시 변경 중 그룹 sync | 개인 파일 덮어쓰기 0, Base/Ours/Theirs 비교 후 새 Preview 또는 HOLD |
| 그룹 게시 성공 + 개인 상태 갱신/Work-side 링크 실패 | **그룹 재게시 0**. 원격 commit·내용 readback 확인 후 미완료 개인 단계만 복구 |
| 게시 응답 유실·원격 판정 불명 | 별도 기존 receipt/history로 처리 여부 정산 전 **UNKNOWN/HOLD, 재게시 0** |

**복구 한도**: 기존 승인된 공통 retry/backoff가 있으면 그것 우선. 없으면 개인 상태 또는 링크 복구 한정 최대 **3회** 지수 backoff + 이후 수동 정산 대기. 그룹 재게시 자동 재시도 0. 새 operation ID/schema를 정의하지 않고 기존 요청/게시영수증 식별자를 재사용(없다면 식별 계약 G0 BLOCKED).

## 5. 입력·출력·판정 관찰점 (스키마 신규 제안 아님)

| 단계 | 기존 데이터/근거로 확인할 항목 | 성공 근거 |
|---|---|---|
| Discover/G0 | 실제 group 저장 위치·폴더/ID/variant, 개인 checkout, 설치 스킬/허용 caller/credential | 조회 source commit·스킬 entrypoint 확인 |
| Import | 그룹 commit+각 파일 hash/Base 복원 가능, 정보등급·경로 동일성 | 개인 저장 readback, 원본 무삭제 |
| Work-origin | optional Work ID, 기존 Evidence ID/MSC 원본/source revision | 원본 참조 무손실, Work 허위 생성 0 |
| Draft/Preview | 개인 diff, 그룹 최신 HEAD, Base/Ours/Theirs, structural conflict | 사용자에게 변경/충돌/기준 revision 명확히 표시 |
| Approve/Publish | 유효 사용자 승인, 실제 그룹 writer, head CAS, 경로/권한·중복 검사 | 그룹 commit/내용 readback 일치 |
| Reconcile | 개인 상태, optional Work-side 링크, 기존 영수증·이력 | 단계별 PASS/FAIL/UNKNOWN, 중복 게시 0 |

예시 상태명은 논리 판정용이며 설치 코드의 신규 enum/필드를 강요하지 않음. 핵심 출력은 승인된 Knowledge 대상(경로/ID), 참조한 그룹 commit, 실제 group 게시 commit, 파일 hash, readback 결과, 별도의 개인 상태/Work 링크 결과. 인증정보·민감 Evidence를 그룹 및 CoWork PUBLIC/PRIVATE로 복제하지 않음.

## 6. 기존 스킬 최소 변경 우선순위
- **P0 / `l1-fix-workflow`**: bootstrap+모든 실쓰기 경로의 knowledge 경로 거부, 기존 그룹 Knowledge READ/Work docs 정상 유지. 호출자별 Git 강제는 이 스킬만으로 입증 불가.
- **P0 / `l1-github`**: 공통 writer/권한·staged allowlist·lock/CAS REUSE 조사. gap이 증명되고 호스트 권한 경계가 가능할 때만 최소 경로/actor 검증 확장. raw git 우회를 못 막으면 보호 완료 불가.
- **P1 / `work-ledger-kernel`**: exporter 보존·root README 링크 T01/T02 우선. 기존 Work 기록 API 의미 매핑; ref type/profile 신규 추가 보류.
- **업무 GPT G0 / `l1-knowledge-updater`, `l1sw-dev-knowledge`**: group 현행 구조/기존 writer, Knowledge origin metadata 지원, Base 저장·복원, 기존 Preview/승인·CAS·중복/응답 유실 정산·remote readback 함수 확인. **업무 소스 접근 없는 Windows 리뷰를 구현 검증으로 대체하지 않음**.

## 7. 게이트·회귀시험 — Claude T01~T10 그대로 추적
| 시험 | 입력/반례 | PASS 조건 |
|---|---|---|
| T01 | `knowledge/`가 있는 Workspace에서 Kernel exporter 전체 재생성 | 기존 지식 파일 SHA 유지·삭제 0 |
| T02 | root README 재생성/탐색 | Knowledge 링크 유효, 사용자 문서 훼손 0 |
| T03 | Workflow 외 raw git으로 `knowledge/` 변경/게시 | **OS/Git 보호 경계**에서 차단; 같은 credential이면 FAIL/BLOCKED |
| T04 | Workflow rename·symlink·path escape | 실제 쓰기·stage·push 차단 |
| T05 | Workflow docs_sync 와 Updater writer 동시 시도 | 혼합 stage/commit 0, 직렬화·HEAD 충돌 탐지 |
| T06 | Work-origin Knowledge 링크와 Work-side 링크 기록 | 지원 계약대로 진실한 링크만 생성. 미지원이면 원본 유지·PENDING, `alias/code_root` 오용 0 |
| T07 | Base v10→그룹 v11 비중첩 | merge Preview·명시 승인·CAS/readback까지 진행, 임의 auto-push 0 |
| T08 | Base v10→그룹 v11 중첩 | 자동 게시 0, 양측 원본/근거 보존 |
| T09 | 그룹 게시 성공·개인 상태 갱신 실패/응답 유실 | 원격 정산 후 개인만 복구, 중복 그룹 게시 0 |
| T10 | 그룹 rename/move/delete 동시성 | `STRUCTURAL_CONFLICT/HOLD`, 사용자 재승인 전 게시 0 |

**공통 게이트**: 기존 전체 Work/MSC/문서 회귀, 패키지 무결성/권한/민감정보/경로 검사, 실제 허용 업무 호스트 단계별 실측. 시험 구분 PASS/FAIL/SKIP/NOT_RUN, 개발 자체시험과 독립 리뷰 및 실제 E3 분리. 지금 T01~T10 **모두 NOT_RUN**.

## 8. 미확인·차단과 다음 한 행동
- **G0 BLOCKED**: 실제 그룹 폴더/파일 ID, Updater source/provenance 형식, 그룹 writer 승인/CAS/readback API, 공유 Git 자격증명 우회 가능성, Common writer lock, Kernel 정당한 Work-side 링크 기록 계약.
- 모든 예시 `work_id`·`Knowledge ID`는 실존한다고 추정하지 않음. `SourceSnapshot/CAS`도 별도 신규 코드 엔진 명칭이 아니라 요구 의미로만 사용.
- 신규 유료 Claude 리뷰·REQUEST/READY·Linux 설치·그룹 게시·PUBLIC ZIP·LIVE 변경 **0/NOT_RUN**.

**NEXT_ONE_ACTION:** 업무 GPT가 설치본과 승인된 경로에 대한 **READ_ONLY G0 매핑**을 반환. G0에서 실제로 입증된 gap만 기존 스킬에 최소 패치하고 T01~T10 격리 시험(적법한 OS/Git 권한 환경에서 T03), 이후 별도 배포 게이트 판단.