# L1 Knowledge ①~④ 사용자 확정 설계 — Claude Code 1차 독립 리뷰 입력

- 개정: r0001 / 2026-11-16 KST
- Work: `L1-WORKSPACE-RAG-20261111-001` (기존 Work의 설계 흐름)
- 상태: `USER_DESIGN_DECISIONS=FIXED_1_TO_4` / `IMPLEMENTATION=NOT_RUN` / `INDEPENDENT_REVIEW=REQUEST_PREPARING`
- 본 문서는 설계와 요구사항의 고정본이지 실제 설치·권한 강제·그룹 게시·E2E 성공 증거가 아님.
- 검토 대상은 비민감 설계 설명만. 업무용 그룹 지식 원문·회사 코드·상세 MSC·로그·토큰·로컬 비밀을 이 저장소에 반출하지 않음.

## 1. 현재 사실과 결정의 구별

- 관리 스킬 정적 확인: `l1-fix-workflow` 후보 v1.6.69, `work-ledger-kernel` 공개 v0.7.42, `l1-github` 후보 v0.3.57. 이 패키지들은 실제 업무 호스트 설치본 확인이 아님.
- Kernel `work_ux.export_docs`: `works/`, `index/`, root `README.md`를 생성·갱신. `knowledge/` 생성·호환 E2E는 미검증.
- Workflow `github_docs.docs_sync`: dirty/untracked checkout 차단. 공통 Git repository의 동시 갱신 경합은 폴더가 달라도 가능.
- GitHub `push_guard.verify`: repository role/root/remote push 보호지만 per-path 또는 인증된 호출자별 WRITE 차단 근거가 아님.
- Kernel `work_refs.REF_TYPES`: `jira, alias, github_pr, p4_cl, code_root`만 허용. `knowledge` ref_type을 이미 지원한다고 주장하거나 오용하지 않음.
- 업무 GPT용 `l1-knowledge-updater`, `l1sw-dev-knowledge`의 실제 스킬 원문·호스트 기능은 Windows Claude/이 GPT에서 접근할 수 없음; TO-BE 요구 제안만 가능.
- 참고: `L1_WORKSPACE_KNOWLEDGE_34_SKILL_CHANGE_REVIEW_r0001_20261116_KST.md` / `L1_WORK_TO_KNOWLEDGE_FLOW_r0002_20261115_KST.md`. **옛 설계에서 모든 지식에 Work ID를 강제한 부분은 이번 결정 ③으로 대체**.

## 2. 결정 ① — 물리적 구조: FIXED

- 기존 업무용 개인 `l1-workspace`의 Git checkout에 `knowledge/`를 생성.
- `knowledge/` 하위 **폴더 계층·식별자·파일 배치 규칙은 업무용 그룹 `l1sw-dev-knowledge`의 실제 현행 지식 구조와 동일**하게 구성. 기존 group 구조를 확인하지 않고 새로운 Module/Feature/Scenario 물리 규칙을 추측해 생성하지 않음.
- `works/<work_id>/`는 기존 Kernel Work/Evidence 정본, `index/`는 기존 기계 인덱스. `knowledge/`는 지식 내용·개인 수정·초안·그룹 동기화 근거와 GitHub 직접 탐색을 담당.
- 그룹 정본을 개인에 가져오는 초기 동기화와 개인의 후속 변경은 구분. 기존 파일·분류·원본을 자동 이동/삭제/전면 재생성하지 않음.
- `knowledge/`의 파일/내용 작성자가 Updater라도 기존 root `README.md`·Git index/HEAD/push, Kernel exporter가 같은 checkout을 사용하는 관계는 별도 충돌 검증.

## 3. 결정 ② — 소유권과 보호: FIXED

- `l1-knowledge-updater`만 `l1-workspace/knowledge/`의 콘텐츠 파일 생성·수정·삭제와 해당 변경의 Git 게시를 요청할 수 있음.
- `l1-fix-workflow`는 **같은 개인 `knowledge/`에 READ만 허용**. Workflow Bootstrap에서 보호 경로를 등록하고, 실제 파일쓰기 및 staged/commit/push 직전 검증 경계에서 Workflow가 시도한 `knowledge/` 변경을 차단. 생성/수정/삭제/rename/symlink·경로 우회 포함.
- Updater의 정상 허용 쓰기는 막지 않음. 호출자의 스킬 정체성과 repo/worktree/path가 실제 검증되어야 하며 사용자 텍스트·환경변수만으로 인증된 actor를 가장하지 않음.
- 기존 Work export/기존 `works/` 기록, Workflow의 group Knowledge 읽기 전용 bridge는 보존.
- 같은 clone의 dirty/untracked 충돌, 스테이징 혼합, 경합 push, 보호된 root `README.md` rewrite 및 checkout 상태는 **별도 공통 Git writer의 직렬화/충돌 검사** 필요. bootstrap 지침만으로 OS/Git credential 차원의 절대 권한 분리를 완료했다고 보고하지 않음.

## 4. 결정 ③ — Knowledge와 Work ID: FIXED

- **개인 Knowledge 식별자는 그룹과 동일한 지식 경로/지식 ID를 기준으로 관리. 모든 개인 지식에 Work ID 필수 아님.**
- 기존 Workflow Work에서 유래한 지식: 원본 Work ID, Evidence/MSC/Source Revision 링크 및 업데이트 이력을 **기존 허용 Kernel 기록 계약 안에서** 원래 Work에 연결.
- Updater가 Work 없이 지식을 직접 생성·수정한 경우: Work를 억지로 만들지 않고 Knowledge 자체의 파일 이력/그룹 동기화 상태를 관리. 개인 `knowledge/` 변경 사실을 기존 Work 생성 이벤트라고 위장하지 않음.
- 하나의 Work에서 여러 지식/하나의 지식에 여러 Work가 기여할 수 있음. 역링크는 존재하는 Work만 유효한 기록 방식으로 연결, 의미가 다른 `alias`/`code_root` ref_type 재사용 금지.
- 승인·그룹 게시 상태는 Work 기록과 별도이며, 지식 내용 작성/수정이 자동으로 그룹 반영 승인이 되지 않음.

## 5. 결정 ④ — 그룹 동기화·충돌·게시: FIXED

1. **초기 가져오기**: 그룹 `l1sw-dev-knowledge`에서 승인된 최신 지식 구조/내용을 개인 `knowledge/`로 동기화. 해당 지식의 **기준 그룹 commit/revision 및 콘텐츠 hash**를 후속 비교 가능하게 보존. 민감 접근/소스 권한 필수.
2. **개인 수정**: Updater가 개인 지식을 변경; 그룹에서 온 기준본과 개인 변경의 관계를 식별. 개인 수정본을 그룹 원격 변경으로 덮어쓰지 않음.
3. **게시 직전 갱신 검사**: 그룹의 현재 원격 revision과 기준 revision 확인. 그룹이 미변경이면 승인된 범위의 게시 후보. 그룹이 변경됐으면 **기준본(Base) / 개인본(Ours) / 최신 그룹본(Theirs)**을 비교.
4. **겹치지 않는 변경**: 기존 Git의 3-way merge를 우선 재사용해 **병합 후보(Preview)** 생성, 사용자가 비교/확인한 후만 게시. 자동 병합 성공은 자동 승인이나 실제 게시 성공과 다름.
5. **충돌 변경**: 자동 게시 **중단**, 충돌 위치/두 변경안/근거와 선택지를 사용자에게 제시. 사용자 결정·최신 그룹 기준 재검증 후 다시 승인/게시. 타인의 수정 손실, 무단 force push, 승인 범위 자동 확대 금지.
6. **게시 실행 전**: 기존 group Knowledge writer가 요구하는 실제 승인·대상 경로·revision/branch head·write scope·중복/정보분류 정책 검증. Preview 후 원격이 또 바뀌면 **CAS/expected HEAD 재검증으로 재차 중단**. 검증되지 않은 API를 새로 있다고 가정하지 않음.
7. **그룹 게시 후**: 실제 group commit/revision/content remote readback 확인 이후에만 개인 `knowledge/`에 게시 상태/그룹 링크/검증 revision/시각 갱신. **그룹 정본은 그룹**, 개인 수정 및 sync 상태는 **개인**으로 분리.
8. **원 Work 역링크**: 해당 지식에 원래 Work ID가 있는 경우에만 동일 그룹 게시 revision을 기존 Kernel 허용 계약으로 기록. Work가 없는 개인 Knowledge는 이 단계 생략.
9. **복구**: 그룹 게시 성공 + 개인 상태 갱신 실패 → 개인 상태만 재시도. 그룹 게시 성공 + Work 역링크 실패 → 링크만 복구. 게시 응답 유실/불확실 → 원격 이력·영수증 정산 전 **그룹 재게시 금지**. 부분 성공을 전체 PASS로 표시하지 않음.
10. **일반 동기화**: 게시 외에도 그룹 변경을 추적하되 개인 미게시 수정이 있는 동안 그룹 최신본의 일방 덮어쓰기 금지. 동기화 실패는 상태로 보존, 코드 분석 또는 유료 리뷰를 임의 재실행하지 않음.

### 게시 충돌 예시

- 개인이 그룹 revision `v10`을 가져와 수정.
- 다른 담당자가 그룹을 `v11`로 게시.
- 개인의 게시 요청에서 `v10/v11` 차이 검출.
- 변경 위치 비중첩: 병합 후보→사용자 확인→현재 HEAD 재검증→게시/readback.
- 동일 내용 충돌: 중단→사용자 해결→새 기준으로 Preview/승인→게시/readback.
- 그룹 게시됐으나 개인 상태 기록 실패: 그룹을 다시 쓰지 않고 게시 사실 재조회 후 개인 상태만 정산.

## 6. 소유 스킬과 최소 수정 검토

| 스킬 | 목표/제약 | 1차 확인 |
|---|---|---|
| `l1-fix-workflow` | bootstrap 보호+실제 쓰기 호출 시 개인 `knowledge/` 거부, 기존 Work 작업/그룹 READ 보존 | `l1_fix_workflow/github_docs.py`, 관련 routing, guarded push |
| `l1-github` | 작업자/경로별 Write 경계, Git staging/HEAD/CAS/중복 push 보호; 이미 있는 단일 writer 재사용 우선 | `scripts/push_guard.py`, commit/stage/dispatcher, repo-config |
| `work-ledger-kernel` | 기존 exporter의 개인 knowledge/ 보존; root README 탐색 링크, 허용 기록 타입 확인 | `work_ledger_kernel/work_ux.py`, `work_refs.py`; 신규 Knowledge profile/원장 선제 금지 |
| 업무 `l1-knowledge-updater` | 그룹 경로 동일 구조 동기화, 유일한 Knowledge writer, baseline/merge/Preview/게시/상태, 선택적 Work 역링크 | 업무 GPT 설치본 G0 요구 |
| 업무 `l1sw-dev-knowledge` | 그룹 지식 검증/승인 게시 writer, CAS/readback/기준 revision/중복 방지 | 업무 GPT 설치본 G0 요구 |

## 7. 독립 리뷰 대상 쟁점 및 반례

- R01: 그룹 지식의 '실제 폴더 구조' 재사용과 개인용 후보 상태 관리가 충돌하는가? 원본 파일·경로 정합성 및 백워드 호환성.
- R02: `knowledge/`를 Kernel exporter가 삭제/변형·root README에서 감추거나 indexer가 충돌시키는가? 최소 REUSE/CONNECT 전략.
- R03: Bootstrap 보호가 실제 쓰기 경로까지 도달하는가? raw git/다른 helper/경로 탈출/rename/symlink/credential로 우회 가능한가?
- R04: 서로 다른 폴더지만 같은 clone·Git index/HEAD·remote push를 공유할 때 dirty checkout·stage·원격 경합 위험.
- R05: Work 없는 지식 변경이 합리적인가? optional Work 링크·N:M·상태/원본 이력의 중복·참조 무결성.
- R06: 기준 revision/내용 hash/타인 변경을 3-way merge와 user Preview에 정확히 고정하는가? 가벼운 상태 기록 가능 여부.
- R07: Markdown 구조적 교차 변경/파일 rename·삭제·Module 이동에서 '비중첩 자동 병합'이 내용 의미상 안전한가? 충돌 시 fail-closed.
- R08: merge Preview 이후의 target HEAD 변경과 group writer 승인·CAS/atomicity 경계; 무단 덮어쓰기·force push 위험.
- R09: 게시 응답 유실·부분 완료·readback 불확실 시 중복 방지/링크만 복구·Work optional.
- R10: user FIXED 방향과 코드 검증 미완료를 정확히 구분; **REUSE→CONNECT→입증된 최소 EXTEND**, 불필요한 새 schema/엔진 금지.
- R11: A) 기존 Git/workflow minimal과 B) 필요가 실제 확인된 구조 보완을 비교하되 결함 개수·대안 개수 강제 금지.

## 8. 요구하는 리뷰 결과 / 제외

- 1차 리뷰는 설계의 **독립 비판적 검토**. 직접 읽은 근거, 심각도 BLOCKING/MAJOR/MINOR(확인된 결함 없으면 NONE), 사용자 합의 수용/수정 권고/보류, 최소 보완안, 소유 스킬, T01~T10 시험 기준, 미검증 API/호스트 사실 분리.
- 결과 등급: `ACCEPT / ACCEPT_WITH_CHANGE / REVISE / HOLD`; 이번 사용자 설계 'FIXED'는 리뷰 대상이며 검증 전 구현 PASS가 아님.
- 코드 패치·ZIP 릴리스·업무 호스트 설치·실제 그룹 Knowledge 게시·새 분석/Job·운영/권한 변경은 범위 밖.
- 이전 정식 미실행 요청 `REQ-L1-WORK-KNOWLEDGE-DESIGN-20261115-001`와 이전 Interactive 문서의 리뷰 실행 여부/영수증을 확인하고 **고정 입력·과거 이력 변경 금지**. 새 요청은 이번 ①~④ 최신 고정 설계에 한정하며 예전 요청을 자동 재큐잉하지 않음.
- 실제 모델 리뷰 실행 여부와 결과/영수증은 신규 정식 REQUEST/READY와 별도로 판정; 요청 MD 게시만으로 실행 완료를 주장하지 않음.
