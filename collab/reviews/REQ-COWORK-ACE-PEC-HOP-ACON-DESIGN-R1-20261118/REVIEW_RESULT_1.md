---
schema: SKILL_COLLAB_REVIEW_RESULT_V1
review_id: "REQ-COWORK-ACE-PEC-HOP-ACON-DESIGN-R1-20261118|1|5f56a23e8c962da273cd24ca2c64c4a6239f85ef588411633aa9c20b823b0431|1"
responds_to_request_id: "REQ-COWORK-ACE-PEC-HOP-ACON-DESIGN-R1-20261118"
responds_to_request_revision: "1"
package_sha256: "5f56a23e8c962da273cd24ca2c64c4a6239f85ef588411633aa9c20b823b0431"
skill_id: "cowork-context-design"
run_policy_ref: "POLICY-STATIC-V1-DESIGN"
knowledge_refs: []
consumer_profiles: ["cowork-context-evidence-feedback-design-review"]
reviewer_os: WINDOWS
review_scope: CODE_REVIEW
test_policy: "STATIC_ONLY"
execution_status: COMPLETED
limitations: ["static review by an automatically started Claude Code process; no package code was executed", "knowledge files were delivered as the REQUEST pinned them; which parts were actually read is reported by the reviewer in the text", "reviewer host is Windows; Linux, in-house LLM and MCP behaviour are not verified by this review"]
---

# 리뷰 결과

# 독립 설계 리뷰 결과 — ACE·PEC-HOP·ACON 통합 설계 (r0001)

**판정: ACCEPT_WITH_CHANGE**

01~03 문서를 모두 읽었다. 확정 결함(BLOCKING)은 발견하지 못했다. 설계는 전반적으로 보수적이며 "REUSE→CONNECT→입증된 최소 EXTEND" 원칙을 일관되게 유지하고, 미확인 항목(dev candidate 보안 우회, Updater G0, 그룹 writer 하드 권한)을 스스로 정확히 BLOCKED/NOT_VERIFIED로 표시하고 있다. 다만 구조적 개선 기회(비차단)가 여럿 있어 ACCEPT_WITH_CHANGE로 판정한다.

## BLOCKING 결함

없음. 세 문서 모두 신규 영속 저장소/신규 writer/자동 승인 변경을 제안하지 않으며, dev candidate(l1-fix-workflow, l1-github, work-ledger-kernel)의 raw Git 우회·보호 diff 문제를 "별도 기존 보안 Work"로 명시적으로 떠넘기고 있어(02_INTEGRATED_DESIGN.md §6) 이번 설계 범위 내에서 해결됐다고 과장하지 않는다. 공개 handoff(03번 문서)도 회사 코드·로그·토큰을 담지 않고 읽기 전용 G0 요청만 전달한다.

## 비차단 개선 제안 (구조 개선 기회)

**1. ACE 최신 결정 우선순위 판정 기준 미구체화**
- 파일: `02_INTEGRATED_DESIGN.md` §3.1, "Curator" 설명 — "사용자 최신 지시·기존 승인 범위와 원본 결정 대조 후 수용/수정 수용/보류/거절"
- 실패 조건: CURRENT.md와 Work 결정 레코드가 시점상 어느 쪽이 최신인지 판별하는 규칙(타임스탬프/리비전 번호 등)이 명시되지 않음. "실제 근거와 사용자 판정이 우선"(§6)은 원칙만 있고 결정형(deterministic) 판별 절차가 없음.
- 증거: 문서 어디에도 비교 연산자(예: Work decision timestamp > CURRENT.md 갱신시각)가 정의되어 있지 않다.
- 제안: ACE-02 수용 시험(§7)에 "최신 판정"을 결정하는 구체적 규칙(예: Work 결정 레코드의 append 순서 또는 revision 번호 비교)을 명문화해, LLM 판단이 아니라 기존 기록의 순서로 우선순위를 정하도록 한다.
- 검증 방법: ACE-02 시험에서 동일 Work에 상충 기록 2건을 인위적으로 넣고, 규칙이 정의된 순서대로 재현 가능하게 최신 건을 선택하는지 확인.

**2. PEC-HOP 원문 발췌의 "byte-level 동일성" 검증 수단 미지정**
- 파일: `02_INTEGRATED_DESIGN.md` §4.1 표, "검증" 열 — "원문 발췌/식별자 byte-level 동일성"
- 실패 조건: 여러 producer(code-analyzer, doc-converter 등)를 거치며 수동/서술적 비교만으로는 전사(transcription) 오류를 못 잡을 위험.
- 제안: 발췌 구간에 대한 해시(예: sha256) 비교나 원본 offset/length 대조 같은 구체적 자동 검증 단계를 PEC-01/PEC-03 수용 시험에 추가.
- 검증 방법: PEC-01 시험에서 발췌문 해시를 원본 파일의 해당 byte range 해시와 대조.

**3. ACON 모델 편차 vs 압축 결함 구분에 최소 재현 횟수 미지정**
- 파일: `02_INTEGRATED_DESIGN.md` §5, §9 (R5) — "모델/환경/설치/출처 버전 차이로 인한 실패를 context compression 결함으로 단정하지 않는다"
- 실패 조건: 원칙은 맞지만 "몇 회 재현해야 압축 결함으로 판정하는가"가 비어 있어, 단발성 실패를 과대/과소 해석할 위험이 남음. 문서 자체도 이를 R5로 미해결 질문으로 남겨둠 — 설계 결함이 아니라 열린 질문으로 인정.
- 제안: ACON-01 수용 시험에 최소 반복 횟수(예: baseline/compressed 각 ≥3회) 기준을 추가.
- 검증 방법: ACON-01 재현 시 반복 횟수와 분산을 수용 기준에 명시.

**4. Generator/Reflector/Curator 역할 명명이 향후 리터럴 서브에이전트화로 이어질 위험**
- 파일: `02_INTEGRATED_DESIGN.md` §3.1 — "세 역할은 논문의 원리 설명이며 신규 Agent 세 개... 지시가 아니다"
- 실패 조건: 디스클레이머가 있지만, 세 역할이 논문 용어로 1:1 명명되어 있어 후속 구현 단계에서 실제 3개 서브에이전트/모델 호출로 literal하게 번역될 리스크가 있음(디스클레이머는 구현 티켓까지 안 살아남을 수 있음).
- 제안: SAFE 시험군에 "파일럿 중 서브에이전트/모델 호출 수가 증가하지 않음(0)"을 명시적 수용 기준으로 추가하거나, 역할명을 "기존 수동 프로세스의 단계"로 재명명.
- 검증 방법: CoWork read-only 파일럿(§8-2) 실행 전/후 모델 호출 횟수 로그 비교.

## 읽은 것 vs 문서가 주장하는 것 구분

- 내가 직접 읽은 것: 패키지 내 4개 문서(01~04)의 전체 텍스트, 비민감 역할/인터페이스 서술.
- 내가 직접 검증하지 **못한** 것(문서의 주장일 뿐): `01_SKILL_SOURCE_AUDIT.md`에 기재된 GitHub ZIP 실제 바이트/Git blob SHA/SKILL.md 압축해제 내용 — 이 세션은 GitHub·외부 시스템에 대한 읽기 권한이 없어 어떤 해시·blob도 재계산하지 않았다. 문서 자체도 dev candidate SHA-256은 "보고서 값이며 이번 독립 SHA256 재계산과 구분"이라고 명시해 자체적으로 구분하고 있다.
- Windows 환경에서 이 리뷰를 수행했으므로, Linux/실제 업무 호스트/MCP/그룹 Knowledge writer의 실제 동작은 어떤 식으로도 검증되지 않았다(G0 NOT_RUN, 문서가 정확히 이렇게 표시).

## 각 REQUEST 질문에 대한 요약 판정

- **R1 (ACE 신규 저장 필요성):** 문서가 제시한 근거(기존 Work 재개·append-only 결정·Evidence가 이미 존재)에 기반하면 신규 영속 저장은 불필요해 보인다. 다만 "최신 판정" 규칙이 결정형으로 명시되지 않은 점은 위 개선안 1 참고.
- **R2 (PEC 중복 생성 방지 경계):** §4.2에서 producer별 책임이 명확히 분리되어 있어 중복 생성 위험은 낮다.
- **R3 (식별자/조건 보존 가능성):** 표(§4.1)가 필요한 필드를 모두 열거하나, 검증 수단이 서술적이라 개선안 2 필요.
- **R4 (Updater writer 충돌):** §6, 03문서 §2·§6에서 "Updater만 지식 WRITE 요청자, Workflow read-only"로 명확히 분리하고 하드 권한 검증은 G0로 미룸 — 설계 자체는 일관되나 실제 집행은 미확인(의도된 것).
- **R5 (ACON 모델 편차 구분):** 원칙은 있으나 구체적 재현 횟수 기준 없음(개선안 3). 정확도 우선 게이트(ACON-01/02)는 유효하게 설계됨.
- **R6 (reviewer watcher 정책 보존):** 01문서 §2 마지막 행, 02문서 §8-6에서 기존 승인/서명/READY/예산/중복 방지를 변경 없이 유지한다고 명시 — 문서상 보존됨. 실제 watcher 설정 자체는 이 세션에서 재검증하지 않았다.
- **R7 (과도한 신규 시스템 반례):** 가장 위험한 후보는 Generator/Reflector/Curator 명명(개선안 4)이며, 그 외 신규 enum(의미 분류)은 "문서 표현일 뿐 실제 schema 아님"으로 scoped되어 있어 수용 가능.

## 지식 파일
- 이번 REQUEST에는 핀된 지식 파일이 없음(명시: "없음").

## 판단에 사용한 소비자 프로필
- `cowork-context-evidence-feedback-design-review` (REQUEST 메타데이터 지정).

## 확인하지 못한 것 (중요)
- 01문서의 GitHub ZIP/blob/SHA-256 주장 전체 — 외부 네트워크 접근 불가로 재검증 불가.
- 실제 l1-knowledge-updater 설치본, 그룹 Knowledge writer 권한, work-ledger-kernel append-only 보장의 런타임 동작 — G0 NOT_RUN으로 설계상 의도적으로 범위 밖.
- Linux/업무 호스트/MCP 환경에서의 어떤 동작도 Windows 세션에서는 검증 불가.
- 기존 Windows LIVE reviewer 정책 select/check의 사전 PASS 여부 자체(이 리뷰가 실행됐다는 사실 외에는 재확인 수단 없음).

## 공통 지식에 대한 수정 제안 (GPT 판단)
- ACE "최신 결정" 우선순위, PEC-HOP 발췌 무결성, ACON 재현 횟수에 대한 결정형 기준을 수용 시험 표(02문서 §7)에 구체 수치/절차로 보강할 것을 제안. 세 건 모두 설계 거부 사유가 아니라 수용 시험을 더 엄격하게 만들기 위한 보강 제안이다.
