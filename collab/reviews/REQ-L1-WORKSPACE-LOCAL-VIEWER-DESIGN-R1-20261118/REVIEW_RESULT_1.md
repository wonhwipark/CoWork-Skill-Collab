---
schema: SKILL_COLLAB_REVIEW_RESULT_V1
review_id: "REQ-L1-WORKSPACE-LOCAL-VIEWER-DESIGN-R1-20261118|1|6a013a104ebfefeae6dc452965ce99ce5a3f9637ed538c778d8cb5189d5a7e5f|1"
responds_to_request_id: "REQ-L1-WORKSPACE-LOCAL-VIEWER-DESIGN-R1-20261118"
responds_to_request_revision: "1"
package_sha256: "6a013a104ebfefeae6dc452965ce99ce5a3f9637ed538c778d8cb5189d5a7e5f"
skill_id: "l1-knowledge-updater"
run_policy_ref: "POLICY-STATIC-V1"
knowledge_refs: []
consumer_profiles: ["l1-workspace-local-viewer-independent-design-review"]
reviewer_os: WINDOWS
review_scope: CODE_REVIEW
test_policy: "STATIC_ONLY"
execution_status: COMPLETED
limitations: ["static review by an automatically started Claude Code process; no package code was executed", "knowledge files were delivered as the REQUEST pinned them; which parts were actually read is reported by the reviewer in the text", "reviewer host is Windows; Linux, in-house LLM and MCP behaviour are not verified by this review"]
---

# 리뷰 결과

# REQ-L1-WORKSPACE-LOCAL-VIEWER-DESIGN-R1-20261118 — 독립 설계 리�이 결과

## 0. 범위와 판정

읽은 9개 패키지 파일(90,120 bytes, FILE_INDEX.txt 기준) 전부를 검토했다. r0002 Delta(`06_FULL_WORKSPACE_TREE_VIEWER_DESIGN_DELTA_r0002.md`)를 최신 요구로 우선 적용하고, 상충 시 r0001(`01_SAFE_TRANSITION_DESIGN.md`)보다 r0002를 우선했다.

**판정: `ACCEPT_WITH_CHANGE`.** 전체 Workspace 기본 열람 + 사후 렌더링(전량 HTML 사전 변환 금지) 방향은 타당하고, P0~P6/G0~G6 게이트 구조와 fail-closed 원칙도 일관되게 설계돼 있다. 다만 아래 BLOCKING 항목은 G2(링크/보안) PASS 전에 반드시 구체화돼야 한다.

이 리뷰는 **코드·호스트 실행이 아닌 문서 정적 검토**이며, `review_request_gate.py`/`approve_request.py`/실제 Linux G0는 실행하지 않았다. 범위는 `PARTIAL_SCOPE`가 아니라 **문서 전체를 커버**했지만, T-테스트의 실제 실행 결과는 애초에 이 패키지에 없으므로(=설계 단계) 모두 `NOT_RUN`으로 남는다.

---

## 1. BLOCKING findings (G2/G3 진행 전 해결 필요)

### B1. Path containment 알고리즘이 구체화되지 않음 (R10, T09/T10/T16/T31 관련)
- **위치**: `06_FULL_WORKSPACE_TREE_VIEWER_DESIGN_DELTA_r0002.md` 2장(33행)·3장(38행), `01_SAFE_TRANSITION_DESIGN.md` 4장(90행), T09/T10/T16/T31.
- **실패 조건**: "`../`, encoded path, symlink/hardlink, casefold/NFC 탐지하고 거부"라고만 서술되어 있고, 정확히 *어떤 시점에* *어떤 함수로* canonicalize하는지 명시가 없다. 문자열 패턴 매칭(예: `..` 문자열 차단)만으로 구현하면 URL-encoding 이중 인코딩, Windows/Linux 혼용 경로 구분자, NFC/NFD 정규화 전 비교, 그리고 **검사-후-서빙 사이의 TOCTOU**(symlink가 요청 처리 중 교체되는 경우)로 우회될 수 있다. 전량 공개(allowlist 제거)로 블라스트 레이디어스가 커진 상태(R24)에서 이 구멍은 치명적이다.
- **증거**: 설계 문서 전체에서 "resolve" "realpath" "commonpath" 등 실제 구현 수준 용어가 한 번도 등장하지 않음. T31 기대 결과는 "403/404"만 명시, 검증 **방법**은 비어 있음.
- **제안 최소 변경**: T31/R10 수용 기준에 "요청 경로를 서빙 직전 1회 `realpath`로 완전히 canonicalize하고, 그 결과가 `WORKSPACE_ROOT`의 하위인지 `commonpath`로 확인하며, 경로상 모든 중간 컴포넌트가 symlink가 아님을 확인한다"는 구체 알고리즘을 명문화. open 후 재검증(open-then-verify, 즉 fd 기준 비교)으로 TOCTOU 제거.
- **검증 계획**: G0 이후 실제 서비스 선택이 끝나면, 위 알고리즘을 해당 서비스(OpenCode Web/Caddy/MkDocs 등)가 기본 제공하는지 또는 뷰어 계층에서 추가해야 하는지 G2에서 실측하고 T09/T10/T16/T31을 자동화된 fuzz 세트로 실행.

### B2. 전체 기본공개 전환에 따른 콘텐츠 내부 비밀 탐지가 한 줄 서술로만 존재 (R24)
- **위치**: `06_...r0002.md` 38행 "콘텐츠 내부에 embedded token 등 비밀이 있는 경우 검사/차단 우선".
- **실패 조건**: r0001의 Work별 allowlist(사람이 선별 승인)를 제거하고 "업무망 허용 계정은 기본적으로 전체 열람"으로 바뀌면서, 유일한 안전망이 path/extension 기반 denylist와 이 한 줄짜리 "검사" 요구뿐이다. 스캐너의 룰셋, false-negative 처리, 스캔 실패 시 fail-open/fail-closed 여부, 소유자 서명(sign-off) 절차가 전혀 정의되지 않았다.
- **제안 최소 변경**: G2/G4 수용 기준에 "비밀 스캔(denylist 패턴 + 룰 기반)이 실패하거나 미실행인 파일은 기본 403(fail-closed)", "스캔 통과 실패 파일 목록은 사람 리뷰 전까지 전체공개 대상에서 제외"를 명시적으로 추가. Work별 allowlist를 없애는 대신 "비밀 스캔 통과 allowlist"로 책임을 이전한 것이므로 그 대체 메커니즘의 명세가 필요.
- **검증 계획**: T12(비밀 문자열/제한 로그/고객자료)에 실제 스캔 도구명·룰·실패처리 정책을 채워 재시험.

### B3. MSC HTML sandbox의 "별도 origin"이 구현 수준에서 정의되지 않음 (R08/R09, T29)
- **위치**: `06_...r0002.md` 41행, `01_SAFE_TRANSITION_DESIGN.md` 89행.
- **실패 조건**: "별도 격리 origin/sandbox + 엄격한 CSP"라고만 쓰여 있다. 같은 도메인의 다른 path(`/workspace/msc/...`)로 서빙하면 쿠키 scope가 기본적으로 공유되어 "별도 origin" 요건이 깨진다. 서브도메인 분리 여부, 리버스 프록시가 쿠키 `Path`/`Domain` 속성을 어떻게 다룰지에 대한 결정이 없다.
- **제안 최소 변경**: 섹션 2/4와 T29 수용 기준에 "MSC HTML은 반드시 별도 서브도메인(또는 iframe sandbox + 인증 쿠키 `HttpOnly`+`SameSite=Strict`+`Path` 제한) 중 하나를 G0에서 확정"을 명시. 경로 기반 분리만으로는 origin 분리로 인정하지 않음을 문서에 추가.
- **검증 계획**: 실제 브라우저에서 MSC 페이지의 요청 헤더에 업무 인증 쿠키가 실려가지 않는지 확인(T29 자체가 이미 요구하는 바이나, "어떻게" 구현했는지 기록 요구).

---

## 2. Non-blocking 제안 (차단 아님, 개선 권고)

1. **캐시 무효화/회수 정책 누락** (섹션 1, T34): 정적 캐시 방식을 "대안으로 허용"한다면서도, 소스 수정·회수(retraction) 시 캐시된 HTML을 언제 폐기하는지 규정이 없다. T27/T34 수용 기준에 "원본 변경 또는 민감 재분류 시 캐시 무효화는 on-demand 렌더와 동일 수준으로 즉시 반영"을 추가 권고.
2. **PREVIEW/UNVERIFIED 배지가 전체공개 UI 요구사항에 반영되지 않음** (R17 vs 06 섹션 2): 전체 트리 기본 열람으로 바뀌면서 동료가 승인 전 개인 draft Work를 그룹 정본으로 오인할 위험이 r0001 대비 커졌는데, T28/T30 수용 기준에 "draft/PREVIEW 상태는 화면에 명시적 배지로 구분" 조항이 빠져 있다. 추가 권고.
3. **r0002 신규 파일들의 provenance pin 부재**: `FILE_INDEX.json`(source_commit `84b9f74...`)은 r0001의 5개 파일만 `source_blob_sha`/`sha256`로 고정하며, `06_...r0002.md`/`README_R0002_LATEST_FIRST.md`/`README.md`/`FILE_INDEX.json` 자신은 개별 blob/sha 핀이 패키지 내에 없다. 이는 설계 자체의 결함은 아니지만, 차후 재리뷰 시 r0002 파트의 바이트 불변성을 독립적으로 검증할 수단이 약하다. r0002용 manifest 항목(각 파일 `source_blob_sha`+`sha256`)을 추가하는 것을 권고.
4. **ZIP 컨테이너 크기와 멤버 바이트 합의 불일치 가능성**: REQUEST_TEXT가 명시한 ZIP 크기 91,324 bytes는 `FILE_INDEX.txt`가 보여주는 9개 파일 원문 바이트 합(90,120)보다 1,204 bytes 크다. ZIP 로컬/중앙 디렉터리 헤더 오버헤드로 설명 가능한 차이지만, 나는 압축 ZIP 자체를 받은 것이 아니라 이미 펼쳐진 파일만 봤으므로 이 차이가 정상적인 오버헤드인지 직접 검증하지 못했다. GPT/watcher 측에서 실제 ZIP의 `unzip -l`/CRC 결과로 확인 권고.

---

## 3. R01~R27 상태표

| R | 판정 | 비고 |
|---|---|---|
| R01 | PASS | 3개 정본(개인 Ledger/그룹 Knowledge/웹 파생) 소유 구분 명확 (01장 2절) |
| R02 | PASS | synthetic export PASS를 "실제 호스트 지원"으로 과장하지 않고 매 문서에서 구분 명시 |
| R03 | PASS | docs_sync의 origin/clean tree 요건을 local-mode에서 무단 제거하지 않음, 최소 diff로 분리 제안 |
| R04 | RISK | 동등 실패/동시성 보호 "설계"는 있으나 구체 lock/CAS 메커니즘은 G0 이후로 전부 유보 — 설계 단계에서는 정상이나 구체성 부족 |
| R05 | NOT_VERIFIED | Kernel 1000-Work/5MiB 한계 대응은 "G0에서 확인" 수준, 실제 완화책 없음 |
| R06 | PASS | LEDGER_ROOT/VIEWER_STAGING 권한 분리 표로 명시 |
| R07 | PASS | Updater WRITE/Workflow READ_ONLY 유지 명시 |
| R08 | RISK → **B3** | CSP/sandbox는 언급되나 origin 분리 구현 수준 미정 |
| R09 | PASS | Work-root 링크 vs Converter 상세 링크 별도 검증·HOLD 원칙 명확 |
| R10 | RISK → **B1** | 알고리즘 미구체화 |
| R11 | PASS | 조직 승인 없는 포트/SSL/방화벽 오픈 금지 명시 |
| R12 | PASS | private/shared viewer의 docroot·색인 분리 명시 |
| R13 | PASS | 개인 PC 가용성과 동료 URL 가용성 분리, C안(상시 호스트) 대안 제시 |
| R14 | PASS | viewer는 export 복사본만 열람, 원본 불변 명시 |
| R15 | PASS | 두 진입(Updater/Workflow) 모두 Work ID/Evidence 보존, 중복 분석 금지 명시 |
| R16 | PASS | CAS/readback 불명확 시 재게시 금지 명시 |
| R17 | RISK (비차단) | 설계 문서상 구분은 있으나 전체공개 UI 요구사항에 배지 요건 누락 (비블로킹 제안 2) |
| R18 | PASS | P0~P6/G0~G6 각 단계 명시적 승인·STOP 조건 |
| R19 | PASS | dirty/diverged 시 auto reset/rebase 금지 명시 |
| R20 | NOT_VERIFIED | 오프호스트 백업/RPO/RTO 요건은 있으나 수치·SLA는 G0 이후로 유보(설계 단계에서 기대되는 수준) |
| R21 | PASS | REUSE 우선, MkDocs/신규 DB 등은 "G0 미충족 입증 시"로 제한 |
| R22 | PASS | A/B/C 트레이드오프 비교표 존재 (01장 3절) |
| R23 | PASS | 전량 HTML 사전변환 불필요 판정이 설치 서비스 renderer 재사용과 양립, 선택적 정적 캐시만 예외로 구분 |
| R24 | RISK → **B2** | ACL 제거의 보완책(콘텐츠 비밀 스캔)이 한 줄 서술로만 존재 |
| R25 | PASS | 신규 custom server/generator/index를 기본 설치 대상으로 삼지 않음 명시 |
| R26 | NOT_VERIFIED | 성능/신규 Work 증가 시 검증은 T34에 위임되어 있고 수치는 전부 NOT_RUN (설계 단계에서는 정상) |
| R27 | PASS | Local authority 전환이 viewer 전환과 분리, Group writer 승인·CAS 불변 유지 명시 (06장 4절 표) |

T01~T34는 전체를 훑었고, 모두 **설계상 기대 결과만 정의된 상태(NOT_RUN)**이며 이 패키지 안에 실제 실행 증거는 없다. T09/T10/T16/T31(B1), T12(B2), T29(B3)를 우선순위로 지적했고, 나머지(T01~T08, T13~T28, T30, T32~T34)는 문서 내 자체 모순은 발견하지 못했다(=비차단).

---

## 4. 지식 교정 제안 (GPT 판정 대상)

- T31/R10 수용 기준에 구체적 path-canonicalization 알고리즘(realpath + commonpath + TOCTOU 대응) 명문화.
- T12/R24 수용 기준에 비밀 스캔 실패 시 fail-closed 원칙과 룰셋 소유자를 명시.
- T29/R08 수용 기준에 origin 분리의 구현 방식(서브도메인 vs 쿠키 scope)을 양자택일로 확정하도록 명시.
- 섹션 1/T34에 캐시 무효화-on-retraction 요구 추가.
- FILE_INDEX.json에 r0002 추가 파일(06/README/README_R0002/FILE_INDEX.json 자신)의 `source_blob_sha`+`sha256` 핀을 추가.

---

## 5. 메타 정보

- **읽은 pinned knowledge 파일**: 없음 (이 REQUEST에 pinned knowledge 미지정).
- **읽은 package 파일**: `__SKILL_COLLAB_CONTEXT__/FILE_INDEX.txt`, `README_R0002_LATEST_FIRST.md`, `06_FULL_WORKSPACE_TREE_VIEWER_DESIGN_DELTA_r0002.md`, `01_SAFE_TRANSITION_DESIGN.md`, `02_CLAUDE_REVIEW_R01_R22.md`, `03_PREP_EVIDENCE_AND_GAPS.md`, `04_WORK_TO_GROUP_KNOWLEDGE_FLOW.md`, `05_BUSINESS_PROPOSAL_DRAFT.md`, `README.md`, `FILE_INDEX.json` (9개 패키지 파일 전부).
- **판단 대상 consumer profile**: `l1-workspace-local-viewer-independent-design-review`.
- **검증하지 못한 것**: 실제 Linux 호스트 G0(설치 버전, 웹서비스 능력, ACL/백업), `review_request_gate.py`/`approve_request.py`/Windows live config의 실제 select/check/서명/READY 동작, ZIP 자체의 CRC/바이트(펼쳐진 파일만 봄), `source_commit 84b9f74...`의 원격 readback, 패키지 내 모든 SHA-256/Git blob 해시값의 재계산(문자열 길이만 육안 확인, 실제 재해시 안 함). Windows에서 이 파일들을 읽은 것이 Linux 동작을 검증한 것은 아니다.
