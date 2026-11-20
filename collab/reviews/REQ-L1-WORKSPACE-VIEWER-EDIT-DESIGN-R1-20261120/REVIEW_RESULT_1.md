---
schema: SKILL_COLLAB_REVIEW_RESULT_V1
review_id: "REQ-L1-WORKSPACE-VIEWER-EDIT-DESIGN-R1-20261120|1|764477880d6b6b6b4bb468f4bb9ccaf6802e5561944ec89569030d69c7080975|1"
responds_to_request_id: "REQ-L1-WORKSPACE-VIEWER-EDIT-DESIGN-R1-20261120"
responds_to_request_revision: "1"
package_sha256: "764477880d6b6b6b4bb468f4bb9ccaf6802e5561944ec89569030d69c7080975"
skill_id: "l1-knowledge-updater"
run_policy_ref: "POLICY-STATIC-V1"
knowledge_refs: []
consumer_profiles: ["l1-workspace-viewer-auth-edit-independent-design-review"]
reviewer_os: WINDOWS
review_scope: CODE_REVIEW
test_policy: "STATIC_ONLY"
execution_status: COMPLETED
limitations: ["static review by an automatically started Claude Code process; no package code was executed", "knowledge files were delivered as the REQUEST pinned them; which parts were actually read is reported by the reviewer in the text", "reviewer host is Windows; Linux, in-house LLM and MCP behaviour are not verified by this review"]
---

# 리뷰 결과

# REQ-L1-WORKSPACE-VIEWER-EDIT-DESIGN-R1-20261120 — 독립 설계 검토 결과

(두 패키지 파일만 정적으로 읽었음: `01_VIEWER_EDIT_DESIGN.md`, `02_REVIEW_README.md`. 코드 실행·설치·네트워크 접근 없음.)

## 판정
**ACCEPT_WITH_CHANGE** — 방향(REUSE 우선, G0 게이트, Work/Knowledge writer 분리, UNKNOWN 표시 원칙)은 건전하나, 아래 BLOCKING 1건을 해소하고 MAJOR 2건을 설계문에 명시적 게이트로 추가해야 D2 착수 가능.

---

## BLOCKING

### B-1. §8 B3 iframe 격리 원칙과 §4 메시지 선택 플로우의 구조적 모순 (R02)
- **위치**: §8 B3 "iframe에 ... 임의 JS bridge를 열지 않음 ... iframe DOM 직접 수정 금지" vs §4 "MSC 화살표 선택 → stable source anchor와 실제 원본 일부 확인".
- **실패 조건**: MSC B HTML/SVG가 별도 origin/sandbox iframe으로 격리된다면, 부모 Viewer는 사용자가 iframe 내부에서 "몇 번째 화살표"를 클릭했는지 DOM 접근 없이는 알 수 없음. 설계는 이 매개 경로(postMessage? 사전 enumerate된 anchor 목록 UI를 부모 DOM에 별도로 렌더?)를 명시하지 않음.
- **반례**: 구현팀이 이 간극을 "임시로" iframe에 postMessage 전역 리스너를 열어 임의 payload를 수신하는 방식으로 메우면, 그 자체가 B3가 막으려던 cross-origin bridge 공격면이 됨(악성/변조된 MSC 콘텐츠가 위조 anchor를 부모에 주입 → 잘못된 대상에 write).
- **최소 수정**: 선택 가능한 메시지/participant 목록은 부모 Viewer가 서버에서 별도로 받은 canonical anchor 리스트(§5의 immutable ID)로 "부모 소유 DOM" 안에서만 렌더하고 선택하게 하거나, iframe→parent 통신을 쓴다면 (a) 고정 origin 검사, (b) 스키마 고정(anchor id만, 좌표/자유 텍스트 금지), (c) 서버 재검증을 필수 조건으로 설계문에 명문화.
- **검증법**: 변조된 origin에서 postMessage를 보내는 네거티브 테스트, anchor id가 서버 enumerate 목록에 없는 경우 write 거부 테스트(T06/T14 확장).

---

## MAJOR

### M-1. 세션/인증 보안 게이트가 "G0 대조 후 최소 보완"으로만 서술되어 하드 스톱이 없음 (R01)
- **위치**: §3 "재인증 세션 사용 범위·TTL·rate limit·계정 잠금·CSRF·SameSite/HttpOnly/Secure·TLS·클릭재킹 방어는 기존 서비스 정책을 G0 대조 후 최소 보완."
- **실패 조건**: G0 확인 결과 기존 호스트 인증에 CSRF 방어나 계정 잠금이 없을 경우, 현재 문구는 "최소 보완"만 요구하고 D2 착수를 막는 명시적 게이트가 없어, 구현이 보완 없이 진행될 위험이 있음.
- **최소 수정**: "G0에서 CSRF/rate-limit/계정 잠금/세션 고정 방어 중 하나라도 미확인·부재로 확인되면 해당 보완이 설계·구현에 반영되기 전에는 EDIT_AUTHORIZED 상태로 전환하는 코드를 머지하지 않는다"는 명시적 정지 조건을 §9 D2 입구 조건에 추가.
- **검증법**: G0 보고서에 각 항목 존재/부재를 체크리스트로 받고, 부재 항목이 있으면 d2 착수 보류.

### M-2. 변경(mutating) 엔드포인트별 재검사 지점이 열거되지 않음 (R01)
- **위치**: §3 "화면 표시만으로 권한 허용 금지"는 원칙만 서술, §6 플로우(EDIT/DIFF/COMMIT)에 "어느 단계에서 ACL+세션을 재검사하는지"가 단계별로 명시되지 않음.
- **실패 조건**: 구현 시 "로그인 성공 시 1회 검사"로 축소 구현될 위험 — 권한 회수나 세션 만료가 draft 저장/commit 사이에 발생해도 막지 못함.
- **최소 수정**: §6에 "draft 저장, diff 생성, commit 각각의 서버 호출에서 독립적으로 ACL+세션 유효성을 재검사한다"를 단계별로 명시.
- **검증법**: T03(권한 회수/세션 만료) 시나리오를 draft 저장 중, diff 생성 중, commit 직전 세 시점으로 나눠 개별 테스트.

---

## MINOR

- **초안(draft) TTL/정리 정책 부재** (R06): §7에 초안 폐기와 확정 rollback 분리는 언급되나, 방치된 개인 초안의 만료/정리 정책이 없음. 최소 수정: 기존 writer에 TTL 기능이 있으면 재사용, 없으면 G0 gap으로 명시.
- **세션 고정(session fixation) 미언급** (R08): §8 EAuth 목록에 CSRF/브루트포스/이중 제출은 있으나 세션 고정이 빠짐. 재인증 성공 시 세션 ID 재발급 요구를 EAuth 항목에 추가 권장.
- **Agent 호출 비용/횟수 한도 미수치화** (R08, §8): "요청 비용/호출 횟수 제한"은 선언적이며 세션당 상한이 없음. code-analyzer 호출 폭주 방지를 위해 세션당 최대 N회 명시 권장.
- **UI 회귀 의존 순서** (R07): P1/U01/U02와 편집 패널 작업을 "같은 회귀 계획"에 포함한다고만 서술. D2 입구 조건에 "P1/U01/U02 회귀 통과 후 편집 패널 머지" 순서를 명문화하면 혼선 감소.

---

## 분류 재검토 (§2 표에 대한 독립 평가)

| 구성 요소 | 설계 분류 | 검토 의견 |
|---|---|---|
| Linux Viewer | CONNECT/G0 | 동의. 실제 API 미확인 상태에서 과잉 확정 없음. |
| l1-fix-workflow | REUSE | 동의, 설계 서술과 일관. |
| work-ledger-kernel | REUSE/G0 writer | 동의하나 CAS/3-way/멱등키 실제 지원 여부가 R06의 핵심 미확인 — G0 필수. |
| l1-knowledge-updater | REUSE/G0 | 동의. 개인 draft writer 실존 여부가 전체 §6 EDIT 단계의 전제. |
| doc-converter | REUSE | 동의. canonical/파생 HTML 상태 분리 서술 적절. |
| code-analyzer/Agent | CONDITIONAL_CONNECT | 동의하되 호출 한도 수치화 필요(위 MINOR). |
| l1-github/Git writer | REUSE/G0 | 동의. |

새 API/DB/schema를 과잉 확정한 부분은 발견되지 않음(§5 필드 목록은 스스로 "새 schema 아님"으로 명시) — R09 관점에서 설계는 적절히 보수적.

---

## G0 추가 확인 필요 항목 (D2 착수 전)
1. 기존 호스트 인증 서비스의 CSRF/rate-limit/계정 잠금/세션 고정 방어 실존 여부.
2. work-ledger-kernel/Updater 실제 writer의 CAS(revision 비교), 3-way merge, 멱등키 지원 여부.
3. MSC B HTML iframe이 postMessage 등으로 안전하게 anchor를 부모에 전달할 기존 메커니즘이 있는지(B-1 해소 전제).
4. 개인 Knowledge draft 저장 경로(개인 writer)의 실존 여부.
5. doc-converter가 canonical 변환 실패를 성공과 분리해 반환하는지.

## 1차 최소 범위 제안 (R10)
설계 자체의 보수적 원칙(§5 anchor 없으면 HOLD, T05 Agent 미호출)과 일치하는 축소안: **첫 증분은 이슈 본문/코멘트/MSC 설명의 텍스트 편집(draft→diff→commit, 기존 writer 재사용)만 포함**하고, 메시지/participant 구조적 수정과 Agent 자동 검증 호출은 B-1·G0-2/3 해소 후 2차 증분으로 미룬다.

## 후속 한 동작
요청자는 r0002에서 (a) B-1 선택 메커니즘 해법과 (b) §3/§6의 명시적 보안 게이트를 보완한 뒤, 위 "1차 최소 범위"로 D2를 좁게 착수한다. 이번 R1 재실행은 금지.

---

## 메타 정보

**읽은 지식 파일**: 없음(이번 REQUEST에 고정 지식 pin 없음). 패키지 파일 `01_VIEWER_EDIT_DESIGN.md`, `02_REVIEW_README.md`만 전체 읽음.

**검토 대상 consumer profile**: `l1-workspace-viewer-auth-edit-independent-design-review` (REQUEST 명시값) 외 추가 프로파일 없음.

**미검증 항목**: 실제 Linux Viewer repo/branch/handler, 실제 host 인증 서비스의 CSRF/세션/잠금 구현, work-ledger-kernel/Updater/doc-converter의 실제 writer API, iframe-parent 통신 기존 메커니즘 — 전부 설계 문서 서술에 대한 정적 평가일 뿐 실제 호스트 동작 확인 아님. 이 리뷰는 Linux/실제 LLM/MCP 동작을 검증하지 않음.

**knowledge 수정 제안**(GPT 판정용): 향후 유사 "인증 후 편집" 설계 리뷰 시 체크리스트에 "cross-origin iframe 격리 원칙과 선택(click-to-select) UX 간 매개 경로 명시 여부"를 표준 점검 항목으로 추가할 것을 제안.
