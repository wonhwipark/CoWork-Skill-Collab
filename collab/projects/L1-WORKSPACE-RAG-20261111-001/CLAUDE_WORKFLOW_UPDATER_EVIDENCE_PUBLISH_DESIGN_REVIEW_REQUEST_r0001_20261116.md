# Windows Claude Code 독립 설계 리뷰 요청 — Workflow × Knowledge Updater 인계·그룹 게시 연결 (r0001)

- 작성: 2026-11-16 KST
- REVIEW_ID: `L1-WORKFLOW-UPDATER-EVIDENCE-PUBLISH-DESIGN-20261116-001` (CoWork 리뷰 식별자, 신규 Kernel Work 아님)
- PARENT_WORK: `L1-WORKSPACE-RAG-20261111-001` — 기존 설계·개발·시험 Work 그대로 재개
- CANONICAL: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`
- REVIEW_KIND: `INDEPENDENT_DESIGN` / 대상: 책임·인계 데이터·게시/역링크 실패 처리의 설계 검토
- REVIEW_MODE: `WINDOWS_CLAUDE_CODE_INTERACTIVE_HANDOFF`; **watcher 정식 REQUEST/READY가 아님**
- REQUEST_DOCUMENT=POSTED (게시·원격 재확인 후에만), WINDOWS_DELIVERY=NOT_VERIFIED, INDEPENDENT_REVIEW=NOT_RUN, RESULT=NOT_RECEIVED
- 작성 GPT는 검토 대상 설계안을 정리했으므로 **동일 세션 자기 검토를 독립 리뷰로 보고하지 않음**.
- 이번 문서 자체는 유료 모델 실행·새 감시·서명·운영 변경의 트리거가 아님. 이미 유효한 승인 범위의 별도 실행 수단이 있을 때만 실행할 것.

## 1. 배경·사용자 최신 피드백 (2026-11-16 KST)

구현 GPT에 전달한 결과에 대해 사용자가 다음과 같이 보고했다.

1. Updater에서 `Work ID` 연계는 기존 `l1-fix-workflow`의 Work 검색·선택·재개를 통해 가능하다고 확인받음.
2. Workflow와 Updater 모두 기존 `code-analyzer`를 사용하므로 **별도 코드 분석 엔진 개발 불필요**라는 방향을 확인받음.
3. **미확인:** 두 진입점 모두 동일 `Work ID / Code Evidence / MSC 원본 / Source Revision`을 동일 Work에 보존하고, 다른 진입점이 재사용하는가?
4. **미확인:** Updater의 기존 후보·Preview·승인 과정 이후 그룹 `l1sw-dev-knowledge` 게시와 원래 Work 역링크를 실제 기존 스킬이 어떻게 처리할 것인가?

1·2는 **사용자 전달 구현 GPT 보고(직접 호스트/API 영수증 아님)**로 기록. 리뷰어는 설계상 REUSE/CONNECT가 타당한지 비판적으로 검토하되 호스트 구현 완료로 승격하지 말 것. 3·4의 실제 호출·writer/permission은 확인된 API와 설치본 없이는 단정 금지. **이번 요청은 ①~④ 설계 리뷰이며 구현·코드 패치 요청 아님.**

## 2. 기존 결정·핵심 자료 (필요 부분만)

아래 파일은 현재 PRIVATE main에서 직접 확인된 파일과 Git blob이다. 리뷰어는 읽은 실제 commit/blob·가능하면 원문 SHA-256을 기록하고, 읽기 실패를 추정으로 대체하지 말 것. 단일 실행 입력 고정은 이 요청 문서 게시 commit 및 아래 열거한 blob을 기준으로 기록하며, **기존 정식 REQUEST의 고정 SOURCE_PIN/ZIP을 변경하지 않는다**.

- `collab/projects/L1-WORKSPACE-RAG-20261111-001/L1_WORK_TO_KNOWLEDGE_FLOW_r0002_20261115_KST.md` — blob `ba546d265511e7fafb1073c1d63472f57cd3f51b`. 두 진입, 두 저장 주체, Workspace 보존, 그룹 writer·역링크 경계
- `collab/projects/L1-WORKSPACE-RAG-20261111-001/L1_KNOWLEDGE_FEEDBACK_DISPOSITION_r0001_20261114.md` — blob `16b522a61be3c8c4257d42491ad0f22679de053b`. G0 부분 보고·첫 실제 분석 후 검증 범위
- `collab/knowledge/SKILL_CAPABILITY_CATALOG.md` — blob `14fd7352814d0f54751b0e2e03f205d60024a188`. Workflow/Kernel/Analyzer/Converter/Updater 역할
- `collab/projects/L1-WORKSPACE-RAG-20261111-001/GPT_MSC_PUBLIC_L1WORK_RELEASE_RESULT_r0001_20261116_KST.md` — MSC 최종 두 ZIP PUBLIC 게시·자체시험 성공과 업무 E3 미검증의 구분
- `collab/ops/CONTRACTS/REVIEW_TIER_TOKEN_BUDGET_V1.md` §2.1 — 근거 기반 비판·결함 강제 0·최소수정/구조대안 비용 비교
- `collab/projects/L1-WORKSPACE-RAG-20261111-001/CURRENT.md` 상단 최신 실행 이력. 과거 절의 “미게시”를 최신 공개본 완료 사실보다 우선하지 말 것

기존 별도 정식 요청 `REQ-L1-WORK-KNOWLEDGE-DESIGN-20261115-001`는 **이미 1회 USD $1 비용 승인·Validator PASS**인 상태지만, 이번 작성 시점 GitHub에는 `READY.md` / `REVIEW_RESULT_1.md` / `RECEIPT_1.md`가 없음. 해당 요청의 고정 r0001 입력은 수정하거나 재핀하지 말고, **서로 다른 리뷰가 중복 실행되지 않도록 동일 목적·실행 여부를 먼저 조회**한다. 그 요청이 실행 중/완료/불확실하면 기존 결과·영수증을 우선 회수하고 중복 리뷰는 시작하지 않는다. 이번 추가 쟁점이 기존 고정 입력에 포함되지 않으면 이를 별도 **후속 설계 범위**로 기록하고 별도 유료 승인·위임 없이 모델을 추가 호출하지 않는다.

## 3. 검토할 권장 설계 (비판 대상이지 확정 구현 아님)

### A. 두 진입점과 Work ID

- A: `l1-knowledge-updater` 직접 Procedure/Feature 분석 요청 → 기존 `l1-fix-workflow`의 Work 선택/재개 계약(또는 검증된 공통 Kernel 진입)을 사용 → 동일 Work 보존.
- B: `l1-fix-workflow`에서 분석한 기존 Work → Updater가 해당 Work를 받아 지식 후보화.
- 두 진입 모두 `code-analyzer`를 코드 사실 제공자로 재사용. 기존 분석의 적합한 Evidence가 있으면 재분석 금지. 새 분석이 필요할 경우 source revision/scope pin 확인.
- 양 스킬이 Work 저장·갱신 주체라는 기존 사용자 결정 유지. Updater의 개별 기록에 Workflow 전체 파이프라인을 매번 실행하도록 강제하지 않음. Kernel의 실제 허용 write API를 확인한 뒤 연결.

### B. 공통 분석 결과 인계: 정보 4종

- Work ID: 기존 Work 식별자를 유지하고 Work 재개/중복 생성 방지.
- Code Evidence: 분석 근거의 **기존 Evidence ID/실제 원본 참조** 유지. 문서 요약만으로 source fact로 승격 금지.
- MSC 원본: 원본 PUML/MD 및 생성 근거·Artifact ID/해시·보관 위치를 보존; HTML/SVG 등 표현 산출물은 별도 참조. 무단 재작성/덮어쓰기 금지.
- Source Revision: 분석 사용 repository/source revision/범위를 고정. 같은 Work라도 revision 불일치 시 기존 Evidence를 현재 사실로 자동 사용 금지; Kernel의 staleness/기존 gate 적용.
- 새 필수 필드나 schema를 선제 도입하지 말고 **기존 Kernel Evidence/Artifacts/Work/SCM 기록에 매핑**. 정확한 실제 field·method 이름은 설치 계약에서 확인.

### C. Updater 후보→Preview→승인된 그룹 게시→Work 역링크

1. 동일 Work/Evidence를 기반으로 Updater가 후보를 만들고 기존 Module→Feature→Scenario 지식 ID·중복/충돌·Tier·대표 MSC 선택 정책을 대조; Procedure는 교차 탐색.
2. 기존 Preview로 변경 대상/근거/적용 조건/목표 revision을 보여줌. 승인 전 그룹 write 금지.
3. 유효 승인·scope·대상 revision/permission·충돌 보호를 확인. 비확정·개인 초안·민감 원문은 승인만으로 무조건 그룹 공개하지 않음.
4. **기존 `l1sw-dev-knowledge` writer/게시 계약**으로 승인된 부분만 기록; 실제 commit/revision 및 원격 readback을 확인하기 전 `POSTED` 금지.
5. 같은 Work에 게시 대상/고정 revision/상태/근거를 **기존 Kernel/Workspace writer**로 역링크. 원본 Work/Evidence는 그대로 보존.
6. 게시 실패→Work 후보 유지; 게시 성공/역링크 실패→**그룹 재게시 금지**, 기존 게시 결과를 확인하고 역링크만 복구; 응답 유실·성공 불확실→실제 remote history/receipt를 먼저 정산.

### D. 검증 시나리오 (설계 기준, 아직 실행 아님)

- V01 Workflow 기존 Work 분석→Updater 재사용: Work ID·Code Evidence·MSC 원본·Source Revision이 조회 후 일치하는가, 적합한 기존 분석 중복 호출 0인가?
- V02 Updater 직접 분석→Workspace 저장/readback: Workflow Work 선택·Kernel Evidence 저장과 교차 재조회가 가능한가?
- V03 같은 Work ID, 다른 source revision: staleness/재분석 조건 및 덮어쓰기 차단
- V04 MSC 원본/HTML/SVG 표시물 간 해시·source/Evidence 근거 연결 및 원본 불변
- V05 Preview 승인 범위·기준 revision 변경·동시 게시 충돌: fail-closed, 승인 자동 확대 0
- V06 그룹 게시 실패 또는 응답 유실: 기존 이력/영수증 우선 정산, 중복 게시 0
- V07 그룹 게시 성공 후 역링크 실패: 게시 revision 유지, Work 링크만 복구, 재게시 0
- V08 개인 유지·보완 요청·승인 대기: 개인 Work 원본 보존, 그룹 미게시, 이후 같은 Work에서 재개

## 4. 독립 리뷰 핵심 질문

| ID | 검토 질문 |
|---|---|
| R01 | Workflow를 Work ID 진입으로 재사용하면서 Updater의 독립 저장 주체성을 보장하는 책임 경계는 일관적인가? 숨은 순환 호출/Work 중복 위험은 없는가? |
| R02 | 두 스킬이 `code-analyzer`를 호출한다는 사실만으로 동일 Evidence 포맷·중복 분석 방지·Source Revision 정합성이 보장되는가? 아닌 경우 필요한 **최소 연결 계약**은? |
| R03 | Work ID·Code Evidence·MSC 원본·Source Revision의 기존 원본/Artifact/Evidence 참조 매핑에서 누락된 핵심 의미가 있는가? 새 필드 없이 가능한 범위와 실제 미확인을 구분했는가? |
| R04 | Source Revision·scope 달라질 때 동일 Work 재사용과 staleness의 안전한 경계는? 분석 오류/MSC 변경 시 기존 원본 덮어쓰기·재승격 위험은? |
| R05 | 두 진입 모두 Workspace writer를 사용하는 설계에 단일 writer/충돌 보호·저장 후 readback 책임이 명확한가? |
| R06 | Updater의 Preview·승인이 실제 그룹 writer가 요구하는 상태·revision·권한 계약과 연결되는가? 검증 전 무엇을 BLOCKED로 남겨야 하는가? |
| R07 | 그룹 게시 후 readback·원래 Work 역링크를 분리하여 판정하고, 불확실/재시도에서 그룹 지식 중복 게시를 막는가? |
| R08 | 기존 Module→Feature→Scenario·Procedure 교차 탐색·AS-IS/TO-BE·Tier/MSC 정책, 팀 지식 상세 설계 허용 범위를 유지하는가? |
| R09 | 실제 설치본/API 미확인을 결함으로 단정하지 않고 REUSE/CONNECT/증명된 최소 EXTEND/DEFER를 구별하는가? |
| R10 | V01~V08 중 첫 승인된 실분석 **이전** 설계로 결정할 내용과 첫 실제 분석 **이후** 확인할 실행 게이트를 올바르게 구분하는가? |
| R11 | 실제 근거가 있으면 단순한 대안(A: 기존 경로 연결 최소)과 구조 대안(B: 입증된 필요 시에만)을 회귀 비용·유지보수성·권한 리스크로 비교해줘. 발견할 결함 개수를 강제하지 말 것. |

## 5. 범위·독립 리뷰 산출물

- 이번 리뷰는 **설계의 비판적 검토**. 코드 수정·기능 구현·스킬 패키징/설치·Job/LLM 분석 재실행·그룹 Knowledge 실제 쓰기·PUBLIC 신규 ZIP·운영 설정/DB/LIVE 변경 요청이 아님.
- Windows Claude Code 별도 **독립 리뷰 세션**에서 결과를 작성. 단, 사용자에게서 확인되지 않은 새 유료 CLI/모델 호출·watcher 신규 REQUEST/READY는 실행하지 말 것. 기존 정식 요청/영수증과 중복 여부를 먼저 정산.
- 리뷰 문서에는 확인된 사실/사용자 보고/설계 가정/추가 검증을 구분하고, 지적별 근거 문서·절/반례·영향·최소 수정안·소유 스킬·검증 방법 작성. BLOCKING/MAJOR/MINOR와 단순 개선 제안을 분리, 결함 강제 0.
- 최종 `ACCEPT / ACCEPT_WITH_CHANGE / REVISE / HOLD` 및 R01~R11 판정, V01~V08 coverage, REUSE/CONNECT/최소 EXTEND/DEFER 매핑 표 제공.
- 원격 결과 경로 (PRIVATE `main`, PR 없이):
  - `collab/projects/L1-WORKSPACE-RAG-20261111-001/CLAUDE_WORKFLOW_UPDATER_EVIDENCE_PUBLISH_DESIGN_REVIEW_RESULT_FOR_GPT_r0001_20261116.md`
  - `collab/projects/L1-WORKSPACE-RAG-20261111-001/CLAUDE_WORKFLOW_UPDATER_EVIDENCE_PUBLISH_DESIGN_REVIEW_EXECUTION_EVIDENCE_r0001_20261116.json`
- 실행 근거에는 독립 세션 구분·입력 file/blob/commit·실제 검토 근거·실행 결과·출력 실제 SHA-256·Git commit·remote readback·모델/비용 확인 상태를 담되 확인 불가값 추정 금지.
- 해당 CURRENT 상단 현재 상태/결과 링크와 TRACKER 현행 상태만 최소 반영. 구버전·기존 정식 REQUEST/영수증 및 다른 실행 이력 무손실 보존.
- 결과 게시 실패로 리뷰 자체를 다시 호출하지 말 것. 사용 중지·불확실 여부는 `NOT_RUN / PENDING / REVIEW_UNCERTAIN`으로 보고. 실제 읽기/결과 없으면 독립 리뷰 `PASS` 금지.

## 6. Windows Claude Code에 전달할 단일 실행 문구

PRIVATE `wonhwipark/CoWork-Skill-Collab`의 `main`에서 `collab/projects/L1-WORKSPACE-RAG-20261111-001/CLAUDE_WORKFLOW_UPDATER_EVIDENCE_PUBLISH_DESIGN_REVIEW_REQUEST_r0001_20261116.md`를 읽어줘. 기존 `REQ-L1-WORK-KNOWLEDGE-DESIGN-20261115-001`의 실행·결과·영수증 및 비용 승인 범위를 먼저 확인하고 중복 유료 호출을 막아줘. ① Workflow Work ID 재사용, ② 공통 code-analyzer 재사용, ③ 네 가지 분석 Evidence 공통 보존, ④ Updater Preview·승인→그룹 Knowledge 게시·Work 역링크에 대한 **독립 설계 리뷰**를 기존 Work에서 수행해줘. Windows 별도 리뷰 권한/비용 계약이 유효한 범위만 실행하고, 결과 MD·실행 근거 JSON을 지정 경로에 PRIVATE main PR 없이 게시·원격 SHA/readback 검증해줘. 미접근 API·실행 미검증은 `NOT_VERIFIED`로 남기고 코드/스킬/Job/Knowledge/운영 변경은 하지 마.
