# Claude Code 독립 설계 리뷰 요청 — Work → Knowledge 전환 r0001

- 작성: 2026-11-14 KST
- Review ID: `L1-WORK-KNOWLEDGE-DESIGN-20261114-001` (이 리뷰 식별자이며 새 Kernel Work가 아님)
- Parent Work: `L1-WORKSPACE-RAG-20261111-001`
- 저장소 / 실행 인계 branch: PRIVATE `wonhwipark/CoWork-Skill-Collab` / `main`
- 요청서 경로: `collab/projects/L1-WORKSPACE-RAG-20261111-001/CLAUDE_WORK_TO_KNOWLEDGE_DESIGN_REVIEW_REQUEST_r0001_20261114.md`
- 사용자 지시: 이번 Work → Knowledge 설계 문서의 Claude Code 독립 리뷰를 요청하고 실행 가능 여부도 확인.
- 승인 범위: 아래 비민감 설계에 대한 별도 대화형 독립 리뷰 1회와 결과·실행 근거의 PRIVATE 게시. 기존 CL/PR 코드 구현·회귀·추가 리뷰와는 다른 요청.
- 현재 전달 방식: `SEMI_AUTO / INTERACTIVE_INDEPENDENT_DESIGN_REVIEW`
- 작성 시 상태: `HANDOFF_PREPARED / WINDOWS_DELIVERY=NOT_VERIFIED / REVIEW_EXECUTION=NOT_RUN / RESULT=NOT_RECEIVED`
- 이 파일은 watcher용 signed REQUEST/READY가 아니며 게시만으로 모델 실행·유료 CLI·LIVE를 시작하지 않음.

## 1. 입력 고정과 읽기 순서

진행 상태는 실행 시 최신 `collab/START_HERE.md` 및 이 Work의 `CURRENT.md` 최상단을 따른다. 과거 CL/PR 요청을 이번 요청으로 오인하거나 재실행하지 않는다. 검토 대상 본문은 아래 고정 commit에서 읽는다. 실행 시 설계가 달라졌으면 차이를 기록하고 승인 없이 다른 버전으로 리뷰 대상을 바꾸지 않는다.

- 고정 입력 commit: `4f83ca9a83e6bb24f5828b83601f3b2df7e3e9fc`
- 주 검토 대상: `collab/projects/L1-WORKSPACE-RAG-20261111-001/L1_WORK_TO_KNOWLEDGE_FLOW_r0001_20261114_KST.md`
- 확인한 주 대상 Git blob: `fa6b02e1628186f38165bfee2e0699c6640bd6f0`
- 고정 링크: https://github.com/wonhwipark/CoWork-Skill-Collab/blob/4f83ca9a83e6bb24f5828b83601f3b2df7e3e9fc/collab/projects/L1-WORKSPACE-RAG-20261111-001/L1_WORK_TO_KNOWLEDGE_FLOW_r0001_20261114_KST.md
- 기존 계약: 같은 commit의 `collab/projects/L1-WORKSPACE-RAG-20261111-001/L1_KNOWLEDGE_UPDATER_K58_K6_WORKFLOW_CONTRACT_r0005_20261111.md` (blob `9a8339abd493afa4119445228a843e95ad1f8f8f`), 필요 절만 참조.
- 기존 판정: 같은 commit의 `collab/projects/L1-WORKSPACE-RAG-20261111-001/L1_KNOWLEDGE_FEEDBACK_DISPOSITION_r0001_20261114.md` (blob `16b522a61be3c8c4257d42491ad0f22679de053b`).
- 이전 단계 상태: 같은 commit의 `collab/projects/L1-WORKSPACE-RAG-20261111-001/CURRENT.md` (blob `4ddde4d0397535b5ff803c83de7fe064f2378a1c`).
- 세부 스킬 계약은 필요할 때만 `collab/knowledge/SKILL_CAPABILITY_CATALOG.md` 등 기존 비민감 문서를 추가 참조. 18개 스킬 감사나 전체 G0 조사를 반복하지 않음.

주 대상 원격 UTF-8 바이트 SHA-256·크기는 이번 요청의 `INPUT_PIN_WORK_TO_KNOWLEDGE_REVIEW_20261114.json`에 수록. 리뷰어는 받은 원문으로 다시 계산하고 불일치 시 해당 입력을 검토 완료로 처리하지 않는다. 자료 접근 불가 시 내용을 추정하지 않고 해당 범위만 `NOT_VERIFIED`로 남긴다.

## 2. 검토할 핵심 흐름과 보존할 결정

Workflow가 분석한 결과와 근거는 기존 Work에 보존한다. 사용자의 지식화 요청을 받으면 Updater가 **같은 Work**를 받아 후보 작성·분류/기존 지식 대조·Preview를 진행한다. 개인 검토는 개인 Work에 상태·출처를 붙여 유지하고 Workflow가 재사용한다. 근거가 부족하면 Updater는 필요한 항목과 완료 조건을 같은 Work로 돌려주고 Workflow가 보완한다. 검토·승인된 범위만 기존 writer로 그룹에 게시하고, 원격 확인과 원래 Work 연결 결과를 따로 회수한다.

보존할 합의:
- Workflow=요청/Work 선택·재개·분석, Kernel=Work/Evidence/허용 기록, Updater=지식 후보·대조·Preview·보완 인계·승인/게시 조정·결과 회수.
- 개인 자료 재사용은 Work 연결이며 Workflow 스킬 자체를 매번 고치는 동작이 아님.
- Work 원본과 Evidence는 보존. 그룹 게시 revision으로 연결하며 독립 정본 두 벌을 만들지 않음.
- 분류 결과 정상 확인은 사용자 보고. 해당 분류로 실제 코드 분석을 아직 수행하지 않은 현재 단계를 유지.
- 실제 API/설치본 기능·저장/게시·역링크·RAG 본문 소비는 미확인/미실행과 기능 부재를 구별. 첫 실제 분석 미실행을 현재 분류 설계 결함으로 올리지 않음.
- `Module → Feature → Scenario`, Procedure/Feature 분류, 기존 RAG M1 게이트 유지.
- 신규 Work 원장·RAG 엔진·DB/schema·자동 동기화·상시 감시를 기본 개선안으로 추가하지 않음.

## 3. 독립 리뷰 질문

아래 질문을 정적 설계 근거로 판단한다. 기능이 설치됐거나 API가 존재한다고 가정하지 않는다. 반례가 있으면 문서 절·영향·최소 수정안·담당 기존 스킬·첫 사례의 확인 기준을 제시한다.

| ID | 질문 |
|---|---|
| R01 | Workflow/Kernel/Updater/writer의 책임이 겹치거나 빠진 구간이 있는가? Updater의 게시 책임과 개인 Work 재사용을 함께 만족하는가? |
| R02 | Workflow 시작/Updater 직접 시작 모두 기존 Work 선택·재개와 원본 근거를 보존하는가? 동일 Work·후보·분석 중복 방지의 의미가 명확한가? |
| R03 | 개인 초안·가설·검증 사실·승인 TO-BE의 상태/출처/적용 조건이 재사용 시 보존되며, 그룹 확정 사실로 잘못 승격되지 않는가? |
| R04 | 근거 보완 요청에 부족 주장·필요 산출물·완료 조건·원래 Work가 충분한가? 불필요한 전체 재분석/자동 code-fix/유료 호출로 확대되지 않는가? |
| R05 | 후보·대상·기준 revision에 묶인 승인과 충돌 시 Preview 갱신이 적절한가? 유효 승인 재사용과 변경 후 재판단이 충돌하지 않는가? |
| R06 | 게시 응답 유실/불확실 상태에서 기존 영수증·이력으로 정산하는가? Work 역링크 실패 때문에 지식을 중복 게시하는 경로가 남아 있는가? |
| R07 | 게시 완료와 Work 연결 완료가 분리되고 Work별 결과·고정 revision·원격 확인을 사용자가 알 수 있는가? 개인 유지/보완/보류 경로도 관찰 가능한가? |
| R08 | 설계상 필요한 인계 의미와 실제 미확인 API/Kernel 필드가 분리됐는가? 기존 기능 재사용·연결로 충분한지, 실제 GAP 확인 후 최소 확장 원칙이 타당한가? |
| R09 | 분류 검토, 실제 코드 분석, 그룹 게시, 검색·본문 회수, Provider 입력의 검증 시점을 정확히 나눴는가? 첫 사례의 부정시험 계획에 빠진 핵심 분기가 있는가? |
| R10 | 이번 정적 리뷰로 판정 가능한 항목과 업무 GPT/실행 호스트에서만 확인 가능한 항목의 경계가 충분한가? 이후 업무 GPT에 물을 최소 사항은 무엇인가? |

각 지적은 `수용 가능 / 수정 필요 / 보류 / 추가 정보 필요`와 `BLOCKING / MAJOR / MINOR`를 필요에 따라 사용한다. 설계 모순과 단순 기능 미확인을 구분하고, 이미 합의한 정책의 재승인을 요구하지 않는다. 최종 권고는 `ACCEPT / ACCEPT_WITH_CHANGE / REVISE / HOLD`.

## 4. 독립성·실행 가능 여부와 실행 경계

1. GPT 설계 작성과 구별되는 **별도 Claude Code 리뷰 세션**에서 한 번만 검토. 과거 CL/PR 독립 리뷰 결과를 이번 문서의 리뷰 완료로 소급하지 않음.
2. 먼저 PRIVATE 자료 접근, 입력 pin, Claude Code 대화형 리뷰 가능 여부와 결과 게시 권한을 확인. 가능한 범위는 계속하며 토큰/접근 장애는 해당 항목만 `BLOCKED / NOT_VERIFIED`.
3. 사용자의 이번 지시는 대화형 설계 리뷰 요청에 대한 승인. 별도 API 과금/새 유료 headless CLI를 시작하거나 기존 R1/R2의 비용 승인을 이번 ID에 재사용하지 않음. 유료 경로만 가능하면 리뷰 입력/인계는 보존하고 비용·모드만 미승인으로 기록.
4. watcher 정식 자동 리뷰를 쓸 경우 기존 유효 승인·REQUEST/READY·서명·한도·중복 방지 계약을 만족해야 함. 대화형 경로가 허용된다는 이유로 자동/과금 경로의 가드를 우회하지 않음. 자동 감시기 재활성화·임의 READY/서명키 생성은 이번 범위 밖.
5. 기존 GitHub 비민감 설계만 검토. 사용자 첨부 이미지·업무 코드/로그·상세 MSC·고객자료·인증정보를 리뷰 입력으로 다시 전송하거나 PRIVATE/PUBLIC에 게시하지 않음.
6. 코드/스킬 수정, 설치·배포, Work/Evidence·그룹 지식 실제 변경, 코드 분석/Job 재실행, 운영 DB/Task/Bridge/Telegram/LIVE 변경은 수행하지 않음. 설계의 최소 보완안만 제안.
7. 결과 게시 실패 시 같은 결과 바이트의 게시만 복구하며 모델 리뷰를 재호출하지 않음. 입력/실행/결과가 불확실하면 중복 실행 없이 상태 보존.

## 5. 결과·실행 근거·게시

모두 PRIVATE `wonhwipark/CoWork-Skill-Collab` / `main`, PR 없이 게시.

- 결과: `collab/projects/L1-WORKSPACE-RAG-20261111-001/CLAUDE_WORK_TO_KNOWLEDGE_DESIGN_REVIEW_RESULT_FOR_GPT_r0001_20261114.md`
- 실행 근거: `collab/projects/L1-WORKSPACE-RAG-20261111-001/CLAUDE_WORK_TO_KNOWLEDGE_DESIGN_REVIEW_RECEIPT_r0001_20261114.json`
- 이 Work의 CURRENT 최상단 이번 리뷰 절과 TRACKER의 관련 요약만 갱신. CL/PR 후보·회귀·배포 상태와 기존 이력 보존. 브리프의 관련 부분도 최신 상태로 연결하거나 재확인 대상으로 표시.

결과에 포함할 내용:
- `REVIEW_STATUS=COMPLETED / PARTIAL / NOT_RUN`, `REVIEW_KIND=INDEPENDENT_DESIGN / NOT_RUN`
- 실제 입력 repo/branch/고정 commit/파일 blob·SHA-256, 읽은 절, 실행 방식/시작·종료 시각(KST)
- 별도 Claude 리뷰 세션 여부 및 확인 가능한 실행 식별자. 비밀값/개인 대화 본문 게시 금지.
- 질문별 결론과 지적: ID·심각도·문서 근거·문제/영향·최소 변경·기존 담당 스킬·확인 기준
- 정책 유지 여부·새 근거·실제 반영 여부·남은 확인을 서로 다른 열로 기록
- `REUSE / CONNECT / 최소 EXTEND / DEFER` 매핑과 업무 GPT에서만 확인할 사항
- 전체 판정, 현재 설계 진행 가능 여부, 다음 한 동작
- `IMPLEMENTATION=NOT_VERIFIED / WORKFLOW_UPDATER_E2E=NOT_RUN` 유지. 정적 설계 검토를 실제 기능 시험 PASS로 확대하지 않음.

실행 근거 JSON은 고정 schema를 새로 도입하는 것이 아니라 이번 리뷰의 문서 영수증이다. 실제 확인 가능한 request ID·독립 reviewer 실행 정보·입력 commit/SHA·시각·실행 결과·모델/API 추가 호출 여부·결과 파일/commit/SHA-256/원격 재조회 상태를 담는다. 비용을 확인할 수 없으면 UNKNOWN으로 남기며 0으로 추정하지 않음.

원격 게시 후 결과 본문을 다시 읽어 실제 UTF-8 바이트·SHA-256·크기·commit을 확인. 결과 파일에 자기 자신의 최종 commit/hash를 억지로 내장하지 말고 실행 근거 문서에 연결한다. 게시할 수 없으면 `RESULT_POST=NOT_POSTED`, 리뷰 실제 수행 여부는 별도로 기록. 정식 watcher 사용 영수증과 대화형 리뷰 기록을 같은 것으로 주장하지 않음.

## 6. 사용자에게 전달할 한 번의 실행 문구

PRIVATE `wonhwipark/CoWork-Skill-Collab`의 `main`에서 `collab/projects/L1-WORKSPACE-RAG-20261111-001/CLAUDE_WORK_TO_KNOWLEDGE_DESIGN_REVIEW_REQUEST_r0001_20261114.md`를 읽고, 별도 Claude Code 세션으로 Work→Knowledge 흐름의 독립 설계 리뷰 1회를 수행해줘. 요청서에 고정된 설계만 검토하고 비민감 결과·실행 근거를 지정 경로에 게시한 뒤 원격 재조회해줘. 실제 기능 확인이 불가능한 부분은 미확인으로 남겨줘.
