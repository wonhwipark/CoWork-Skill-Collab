# ACE × PEC-HOP × ACON 적용 — CoWork 협업·L1 지식 통합 스킬 최소 변경 설계 r0001

- 작성: GPT / 2026-11-18 KST
- 기존 Work: COWORK-SKILL-DISCOVERY-20261112-001, L1-WORKSPACE-RAG-20261111-001 연계
- 상태: DESIGN_FOR_REVIEW / 코드·호스트·정책 변경 없음
- 입력 근거: [개별 ZIP·SKILL 원문 감사](ACE_PEC_HOP_ACON_SKILL_SOURCE_AUDIT_r0001_20261118_KST.md), [공통 브리프](../../CONTEXT_BRIEF.md), [기존 L1 두 진입·Work 보존](../L1-WORKSPACE-RAG-20261111-001/L1_WORK_TO_KNOWLEDGE_FLOW_r0002_20261115_KST.md)
- 논문: ACE (ICLR 2026) https://openreview.net/pdf?id=eC4ygDs02R / PEC-HOP·MCE-Compass (EMNLP 2026) https://aclanthology.org/2026.emnlp-main.849/ / ACON (ICML 2026) https://proceedings.mlr.press/v306/kang26b.html
- 범위: 세 논문의 설계 원리만 기존 기능에 적용. 논문 벤치마크 수치는 업무 실측 성과로 사용하지 않는다.

## 1. 해결할 문제와 우선순위

1. CoWork: 새 창·Work 재개 중 최신 결정/근거 누락, 과거 결정을 현행 승인으로 오독, 반복된 지침 전체 재요약의 누락을 줄인다.
2. L1 업무: CL·PR·P4/Jira·코드 분석·MSC/HLD 간 정확한 식별자·출처·조건을 보존한다. 근거가 없는 주장을 확인된 CODE FACT 또는 원인으로 승격하지 않는다.
3. 업무 GPT: 접근 불가능한 GitHub/로컬 파일에 대해 링크만 전달하면 실제 원문을 읽었다고 가정하지 않는다.
4. 장기: 실패가 실증된 압축 지침만 고치고, 기존 Worker/로그·공용 원장/업무 스킬을 변경하지 않는다.

우선순위: CoWork ACE, L1 PEC-HOP, 이후 ACON. 전체 구현 우선순위는 ① 기존 동작 재사용 ② 근거 보존 표시 ③ 제한적 압축 회귀이며 자동 RAG/학습/쓰기 엔진은 필요성 입증 전 DEFER.

## 2. 상위 흐름 (읽기·파생 표현·쓰기 경계)

사람/업무 요청
→ 기존 Work 확인 및 원본 source revision pin
→ ACE: 고정 지침 + 현재 Work 상태 + 선택된 검증 교훈만 읽기
→ PEC-HOP: CODE FACT/원문 발췌·출처 위치·조건을 근거별 파생 묶음으로 구성
→ 기존 업무 GPT/Agent/분석·문서 스킬 처리
→ 기존 Kernel·업무 writer가 허용된 Work/Evidence/결정 기록
→ 기존 Updater가 필요할 때 지식 후보·기존 정본 대조·Preview
→ 승인된 그룹 writer/readback 및 원 Work 연결(각각 별도 검증)
→ ACON: 재현된 실패가 있는 경우에만 압축 지침의 보존 규칙 제안
→ GPT 판정 및 기존 Work의 피드백/현재 요약 갱신

설계상의 화살표는 호출/설치 검증이 아닌 책임이다. CoWork PRIVATE reviewer transport와 업무 L1 Workspace/Knowledge 정본을 합치지 않는다. 유효 승인·비용·원본 결속·중복 방지는 결정형 기존 gate를 항상 우선한다.

## 3. ACE 적용 상세 — 새 메모리 DB를 만들지 않는다

### 3.1 유일한 기존 정본

- 고정 지도: collab/CONTEXT_BRIEF.md. 구조/책임/Work 진입 경로만, 일반 운영 상태와 최신 blob 미복사.
- 현재 상태: 관련 Work CURRENT.md의 짧은 현재 요약/열린 메모/마지막 검증/미해결/다음 한 행동.
- 결정·증거·실패: 기존 Work의 원문 결정/notes/REVIEW_RESULT/RECEIPT 및 L1 Kernel Work/Evidence.
- 그룹 Knowledge: 검증·승인된 별도 정본; 개인 Work·임시 후보와 별개.

Generator: 요청 범위에 필요한 기존 사실을 선택하여 조회용 맥락 묶음으로 구성(전체 기록 덤프 금지).
Reflector: 완료된 작업의 원래 목표·실제 결과·상충 근거·재발 원인을 구분하고 검증이 필요한 교훈 후보만 작성.
Curator: 사용자 최신 지시·기존 승인 범위와 원본 결정 대조 후 수용/수정 수용/보류/거절; 기존 CURRENT/notes만 갱신.
세 역할은 논문의 원리 설명이며 신규 Agent 세 개, 백그라운드 모델 호출, 자동 스킬 실행 지시가 아니다.

### 3.2 읽기용 경량 Context Packet

아래 항목은 새 DB 필드/원장/Kernel schema가 아니라 기존 자료의 사람이 읽는 파생 view다.

- 요청 목적 / 기존 Work ID / 현재 사용 branch·source revision / 확인 시점
- 무조건 지켜야 할 안전·승인 규칙(원본 위치 포함)
- 최신 검증 결과 및 과거 판정과의 차이, confidence·미확인
- 관련 Evidence ID와 실제 원문 위치, 원문 접근 여부
- 열린 문제, 실패해도 재실행하지 않아야 할 요청/Job
- 이번 요청에 필요한 최대 1~3개 검증된 기존 교훈
- 다음 한 행동 및 필요 승인 범위

읽기 전용 출력과 개인/그룹 실제 쓰기 경로를 분리. 명령/승인/READY/게시 사실은 Context Packet 문구로 대체되지 않는다. 내부 사용자 데이터나 private 키 내용은 Context Packet에 넣지 않는다.

### 3.3 기존 스킬별 ACE 책임

| 스킬·구성 | 판정 | 필요한 연결/금지 |
|---|---|---|
| CoWork 지도/CURRENT/notes | REUSE | 기존 피드백 판정에 검증 교훈을 연결. 전체 playbook 새 파일·자동 갱신 제외 |
| l1-fix-workflow 1.6.70 후보 | REUSE / CONNECT 후보 | Work 재개·Checkpoint read-only, 기존 Evidence 유효성 검토 후 선택만. 원문 대체/자동 분석 금지 |
| work-ledger-kernel 0.7.43 후보 | REUSE | append-only 결론·Evidence 원본 유지. 새 profile/record/context DB 금지 |
| l1-github 0.3.59 후보 | REUSE | source ref, repo role, 원격 readback. 기존 Knowledge 보호 우회 및 raw Git 직접 push 금지 |

## 4. PEC-HOP 적용 상세 — 복사가능한 근거를 보존

이 설계는 PEC-HOP 완전 구현 또는 MCE-Compass의 소형 모델별 offline prompt calibration을 뜻하지 않는다. 초기 단계는 논문의 copy-preserving 증거 유지 원리만 사용한다.

### 4.1 입력 패키지의 논리적 항목(현재 writer 포맷과 매핑)

| 필수 내용 | 기대 원본 | 검증 |
|---|---|---|
| 근거 참조 | 기존 Work/Evidence ID, Code Analyzer Fact ID 또는 문서 위치 | ID 존재·원본 위치/권한·파일 SHA |
| 고정된 source | Git commit/P4 CL·필요 시 실제 origin/landed CL, 파일·함수/라인 또는 문서 revision | 서로 다른 revision 자동 병합 금지 |
| 최소 원문 발췌 | 허용된 정확한 원문과 앞뒤 해석 문맥 | 원문 발췌/식별자 byte-level 동일성, 정보 반출 정책 |
| 의미 분류 | CONFIRMED_FACT / OBSERVED / HYPOTHESIS / DESIGN_PROPOSAL / UNKNOWN (설명용) | 실제 기존 record enum을 변경하지 않고 문서 표현으로 구분 |
| 적용 범위/조건 | RAT/Stack/Module/Procedure/Scenario, version·branch·조건 | 조건 누락 때 일반화 금지 |
| 분석 연결 | Problem→Cause→Solution/AS-IS→TO-BE 중 해당 주장과 실제 근거 pointer | 원인·수정·시험을 각각 다른 근거로 구분 |
| 반례/미확인 | 누락·충돌·stale·접근 불가·미검증 API | 본문에서 명시, 강행/추측 금지 |
| 출력 대상 | 업무 GPT 텍스트 패킷 또는 기존 HLD/MSC 보고서 링크 | 링크 접근 불가 시 승인된 발췌 포함; 공개 유출 차단 |

토큰이 부족하면 중복 설명을 우선 제거한다. 안전 규칙·검증 등급·함수/API/IPC 이름·수치·대상 revision·예외 조건·source pointer를 삭제해서는 안 된다. 입력이 미충족이면 컴팩트한 완성본을 위조하지 않고 PARTIAL_EVIDENCE/HOLD로 표시한다.

### 4.2 스킬 책임과 최소 연결

- code-analyzer: 정확한 CODE FACT·procedure·source metadata와 저장된 기존 분석 결과를 producer로 사용. 동일 CODE FACT를 얻기 위한 자동 재실행 금지.
- issue-analyzer: 실제 로그 인용/증상과 확인 원인·과거 사례 참조를 분리한다. 과거 지식/예상 Flow만으로 이번 장애의 근본 원인을 확정하지 않는다.
- p4-code-owner, l1-github: P4 actual modifier/CL·Git PR·source revision·integration/landing 구분. 권한 있는 provider만 조회.
- hld-composer: 제한된 model packet, SOURCE_MAP, HLD trace를 재사용. context-only Issue와 CODE FACT는 근거 수준을 달리한다.
- doc-converter: 기존 scenario_trace/participant policy/MSC Manifest를 보존한 표현 소비자. Render·HTML 링크 존재와 사실 승인/Knowledge 게시를 구별한다.
- Workflow/Kernel: 기존 Evidence·published path·원본 digest/원래 Work의 영속 기록. 문서 복사나 새 index 대신 기존 writer/readback.
- Updater: 공개 스킬 원문이 아니므로 ① 기존 producer의 근거 view를 읽는 후보 조정자 ② 그룹 writer G0 확인 전 저장/게시 구현 요구 금지. 별도 설계 적용 제안서를 업무 GPT에 전달.

### 4.3 저사양 업무 GPT용 전달 원칙

패킷은 (A) 결정/요청, (B) 핵심 근거별 원문 발췌, (C) 정확한 미확인/추가 검색 요청의 3부분으로 먼저 구성한다. 출처 링크만 보내고 업무 GPT가 PRIVATE 또는 업무 호스트 문서를 자동 열었다고 가정하지 않는다. 원문 발췌를 공유할 때도 권한·정보등급을 먼저 확인하고, 비허가 원문은 전달하지 않고 관련 작업 호스트에서 확인하도록 명시한다.

## 5. ACON 적용 상세 — 실패 기반 보존 규칙만 시험

1. 기존 Evidence/Work에 보존된 동일 질문의 full-context baseline, 기존 압축판, 새로운 압축안을 동등 조건에 놓는다.
2. full-context는 통과하지만 압축판만 실패한 사례인지 먼저 판단한다. 모델/환경/설치/출처 버전 차이로 인한 실패를 context compression 결함으로 단정하지 않는다.
3. 실패 근거의 누락 형태(결정 우선순위, 식별자, branch/source revision, 부정조건, 미확인 표시, 승인경계)를 기록한다.
4. 기존 피드백 문서에 보존 규칙의 수정 제안을 남기되 사용자/검증 판정 전 공통 지침이나 모델 system prompt를 자동 변경하지 않는다.
5. 개선에 사용하지 않은 별도 사례로 재시험. 정확성·근거 보존을 통과한 경우에만 토큰 감소/사용자 편의 평가.

CoWork SOURCE_PIN repo_id의 숫자/문자열 타입 불일치는 압축 정책의 대체 해결 대상이 아니다. 기존 결정형 pin preflight와 approval/signing의 fail-closed 검사는 그대로 유지한다. 압축 도입은 승인·서명·READY·비용·중복 검증을 느슨하게 할 수 없다.

## 6. 기존 운영 원칙 충돌 방지

- REUSE→CONNECT→입증된 최소 EXTEND 순서. 미확인 API/필드나 source path를 실제 구현 명세로 승격 금지.
- 새 model 호출·자동 Watcher/Job·LLM subagent·RAG 엔진·지속 기억 DB·새 Kernel profile/schema 추가 없음.
- 개인 knowledge/는 Updater만 수정, Workflow read-only. 현재 개발 후보의 raw Git/이미 commit된 보호 diff 및 동일 인증 우회 문제는 별도 기존 보안 Work에서 해결해야 함.
- Updater는 Workflow의 모든 실행을 선행할 필요가 없고, 기존 Work 기반 지식화는 동일 Work의 Evidence를 재사용. 그룹 Knowledge 확정은 Preview→유효 승인→기존 writer→readback→Work 역링크를 별도 확인.
- 회사 소스/상세 MSC/로그/고객자료/토큰을 CoWork PRIVATE/PUBLIC으로 전달 금지. 공개 handoff는 비민감 책임·제안·호스트 검사 문구만 허용.
- 독립 리뷰/CI/자체시험/업무 실제 E2E/그룹 지식 게시의 PASS 상태를 혼동하지 않는다.

## 7. 수용 시험 계획 (현재 설계만, 전 항목 NOT_RUN)

| ID | 범위 | 합격 조건 |
|---|---|---|
| ACE-01 | 5회 연속 동일 Work 변경 | 원래 필수 승인/결정/미해결 보존 100%, 폐기 결정 재등장 0 |
| ACE-02 | CURRENT에 과거 성공·최신 실패 공존 | 최신 판정과 과거 이력 구별, 실제 증거가 우선 |
| ACE-03 | 읽기 전용 재개 | Work/원장/Job/READY 변경 0, 모델/분석 자동 재실행 0 |
| PEC-01 | CL·Jira·PR·코드 Evidence 각 1개 이상 | API/IPC/함수/상태/수치/Source pin 식별자 왜곡·누락 0 |
| PEC-02 | 근거 없는 Cause 또는 stale source | 확정 원인 승격 0, HOLD/미확인 정확히 표시 |
| PEC-03 | MSC/HLD·원본-파생 링크 및 권한 | 원본 해시·source trace 유지, 손상/접근불가 시 성공 표시 0 |
| PEC-04 | 업무 GPT 링크 미접근·텍스트 전용 | 전달 가능한 승인 발췌만 첨부, 미접근 링크를 실제 읽었다고 주장 0 |
| ACON-01 | 원본 성공/압축본 실패 사례 | 압축 때문임이 재현된 경우만 보존 규칙 변경 후보로 채택 |
| ACON-02 | 개선에 사용하지 않은 독립 사례 | 정확성·근거 보존 기준 먼저 PASS, 토큰 절감은 그다음 평가 |
| SAFE-01 | 원격 지침 게시 vs 모델/호스트 | 문서 게시만으로 READY/리뷰/호스트/Knowledge 쓰기 0 |
| SAFE-02 | 같은 Work 지식 후보와 별도 그룹 게시 | 원 Work 불변, 미승인 그룹 게시 0, 실패한 역링크만 복구 |
| SAFE-03 | 불확실 실행/리뷰 | receipt/history 선 정산, 중복 호출·재큐잉 0 |

측정 기준은 요구 품질 게이트이지 논문 성능 수치나 업무 E2E의 이미 달성된 성적이 아니다. 첫 실제 적용은 기존 승인된 비민감 합성 사례로 수행. 실패한 시험은 FAIL, 환경 때문에 못 돌린 시험은 NOT_RUN으로 분리한다.

## 8. 보수적 구현 계획 및 소유자

1. **문서 범위 완료 가능:** 기존 문서/스킬 I/O 매핑, 위험/반례 및 수용 시험 설계. 기존 CURRENT·notes/판정에 연결, 신규 원장 불필요.
2. **CoWork read-only 파일럿:** 기존 Work 5개 이력 기반 Context Packet 수동/결정형 생성; 추가 호출 없이 이전 판정과 누락 비교. 실제 기존 reader/formatter가 충분하면 코드 추가 안 함.
3. **L1 Evidence 파일럿:** 실제 업무 호스트에서 code-analyzer/issue-analyzer의 기존 출력에 PEC view를 연결 가능한지 확인. 필요 시 기존 출력 serializer 최소 수정; 새로운 근거 탐색 서비스 제안 금지.
4. **Updater G0 대조:** 업무 GPT에 별도 설계 적용 제안서 전달, 실제 Updater 설치본·group writer/승인·Kernel 경로를 읽기 전용 확인. 이후만 최소 코드 변경 범위 결정.
5. **ACON 시험:** 실패 사례가 실제 수집된 후 기존 피드백/회귀 경로에서 prompt guideline 후보를 검증; 자동 prompt 배포는 추가 승인·검증 전 보류.
6. **독립 설계 리뷰:** Windows Claude Code 1사이클로 책임/계약/비용·보안 반례 검토. 기존 Windows LIVE reviewer 설정 select/check 사전 PASS 없이는 REQUEST/ZIP commit A 및 SOURCE_PIN/서명/READY 게시 금지.

## 9. 독립 리뷰에서 판단해야 할 질문

- (R1) 기존 지도/CURRENT/Kernel을 ACE playbook으로 해석할 때 실제로 빠진 기능이 무엇이며 별도 영속 저장이 정말 필요한가?
- (R2) PEC view를 스킬별로 중복 생성하지 않고 CODE FACT·HLD·로그·SCM producer가 책임지는 최소 연결 경계는?
- (R3) source revision·Evidence ID·문서 line/함수 이름/조건·민감자료 경계를 정확하게 보존할 수 있는가?
- (R4) L1 Updater가 기존 Work를 쓰는 기능과 개인 knowledge/ 단일 writer를 충돌 없이 함께 유지하는가? 실제 설치 G0 이전에 제안하면 안 될 구현은 무엇인가?
- (R5) ACON 실패 분류/평가가 모델 편차와 실제 압축 누락을 구분하는가? 정확도 우선 gate가 유효한가?
- (R6) 계승해야 할 reviewer watcher 승인/서명/READY·예산·중복 방지가 변경 없이 보존되는가?
- (R7) 더 단순한 REUSE 안이 있는가? 확인 가능한 결함과 비차단 개선 제안을 분리하고 과도한 기능 확장 금지.

결과 형식: ACCEPT / ACCEPT_WITH_CHANGE / REVISE / HOLD. Finding별 Severity, 실제 파일/원본, 재현 가능한 반례, 최소 수정안, 추가 확인, 독립 리뷰 범위와 불확실 요소를 한국어로 보고. 결함 개수 강제 금지. 이미 종료된 타 주제 리뷰를 재개하거나 새로운 유료 재리뷰를 자동 시작하지 않는다.

## 10. 상태와 다음 한 동작

DESIGN=AUTHORED / SKILL_SOURCE_AUDIT=PASS_SCOPE_LIMITED / FUNCTIONAL_TEST=NOT_RUN / WORKSPACE_G0=NOT_VERIFIED / INDEPENDENT_REVIEW=NOT_RUN / PUBLIC_RELEASE=NOT_RUN / HOST_CHANGE=NOT_RUN.

NEXT_ONE_ACTION: 업무 GPT용 Updater 설계 적용 제안서를 비민감 전달 경로로 공유하고, Windows Claude Code가 현재 LIVE 정책을 읽기 전용 select/check한 뒤 조건을 충족할 경우에만 신규 고정 입력의 단일 독립 리뷰 REQUEST를 정식 게시한다. 사전 게이트가 막히면 이번 설계는 PRIVATE 게시 완료, 리뷰는 BLOCKED_PREFLIGHT로 정확히 보존.
