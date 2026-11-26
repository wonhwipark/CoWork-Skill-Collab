---
schema: SKILL_COLLAB_REVIEW_RESULT_V1
review_id: "REQ-L1-SOURCE-MAP-DESIGN-R1-20261127|1|ec953eb4a92512a3e8d8d74b4f56e72fd8e91b7fddca5ef748cc30744c025eeb|1"
responds_to_request_id: "REQ-L1-SOURCE-MAP-DESIGN-R1-20261127"
responds_to_request_revision: "1"
package_sha256: "ec953eb4a92512a3e8d8d74b4f56e72fd8e91b7fddca5ef748cc30744c025eeb"
skill_id: "l1-knowledge-updater"
run_policy_ref: "POLICY-STATIC-V1"
knowledge_refs: []
consumer_profiles: ["code-analyzer", "l1-channel-recovery", "work-ledger-kernel"]
reviewer_os: WINDOWS
review_scope: CODE_REVIEW
test_policy: "STATIC_ONLY"
execution_status: COMPLETED
limitations: ["static review by an automatically started Claude Code process; no package code was executed", "knowledge files were delivered as the REQUEST pinned them; which parts were actually read is reported by the reviewer in the text", "reviewer host is Windows; Linux, in-house LLM and MCP behaviour are not verified by this review"]
---

# 리뷰 결과

읽은 파일은 패키지 전체(`DESIGN_REVIEW_INPUT.md`, 1개 파일, 핀 지식 없음)이며, 아래는 그 전문에 대한 독립 정적 리뷰입니다.

---

# REQ-L1-SOURCE-MAP-DESIGN-R1-20261127 — 독립 설계 리뷰

## BLOCKING

**B1. "사실 왜곡 없음/안정적 식별" 보장의 근거(기존 Analyzer 추출 품질)가 본 문서 안에서 미확정 상태**
- 위치: Goal 섹션 4행 "Existing discovery outputs are reported but their contents and approval scope are not established." / §2 "no fabricated edges... Stable symbol identity must disambiguate namespace, overload, translation unit and variant"
- 실패 조건: Source Map의 모든 심볼/엣지(call, msgID→handler, 오버로드, 조건부 빌드 변형)는 "existing Analyzer supplies bounded code facts"에서 공급받는다고 가정하지만, 그 Analyzer 추출이 실제로 clang/AST 수준 도구인지, LLM 단독 추론인지 문서 자체가 밝히지 않음. C++ 오버로드/템플릿/매크로/조건부 빌드 구분은 파서 없이 안정적으로 보장하기 매우 어려운 영역이며, "no fabricated edges"·"stable identity" 같은 강한 보장을 LLM 전용 추출로 충족한다고 전제하면 반례(동일 시그니처 오버로드 2개를 하나로 합치거나, `#ifdef` 변형 중 하나만 보고 전체로 일반화하는 경우)가 쉽게 발생.
- 반례: §3에서 "Updater alone may refresh"라 하지만, Updater가 쓰는 추출 방법이 Analyzer와 동일한지/다른지도 불명확 — 두 컴포넌트가 서로 다른 신뢰도의 사실을 같은 스키마에 섞어 쓸 위험.
- 최소 수정: ① Source Map 레코드는 반드시 "extracted(도구/파서 근거) / inferred(LLM 추론) / unknown" 3단 신뢰도 필드를 필수로 가지고, Updater는 "inferred" 레코드를 "extracted"로 승격할 수 없다는 규칙을 명시. ② 현재 Analyzer가 실제로 어떤 방법(파서 유무)으로 사실을 추출하는지 한 문장으로 확정해 설계에 박아 넣을 것.
- 수락 시험: 알려진 오버로드 쌍/조건부 빌드 변형이 있는 샘플 모듈 1개를 골드셋으로 만들어, Source Map 산출 레코드가 신뢰도 필드를 정확히 구분해 표기하는지, "inferred" 레코드가 "no fabricated edges" 주장 없이 노출되는지 확인.

## MAJOR

**M1. Q5(평가 설계)에 구체적 수치·골드셋·정지 기준이 전혀 없음**
- 위치: §Q5 전체
- 실패 조건: "recall/precision", "measurable acceptance and stop criteria" 요구만 나열되고 실제 숫자(예: recall ≥ X%), 골드 관계 수, 네거티브 케이스 구성, 정지 조건이 본문에 없음. 이 상태로 승인되면 "invented performance gains 없음"을 검증할 기준 자체가 없어 Q5가 요구한 바를 설계가 자답하지 못함.
- 최소 수정(제안 시험): 동일 소스/빌드/모델/예산 고정 후 baseline vs map-only vs procedure-only vs both 4조건 비교, 모듈당 최소 30개 골드 관계 + 10개 네거티브(존재하지 않는 관계) 세트, 수락 기준 예: 정확한 관계 recall ≥ 90%, 허위 긍정(fabricated edge) 0건, stale/빌드 변형 입력 시 반드시 "stale/unknown" 표기율 100%. 정지 기준: 2회 연속 fabricated edge 발견 시 그룹 게시 중단.
- 검증 방법: 위 수치를 실제 1개 RAT 모듈에 시범 적용한 결과를 다음 리뷰에서 재확인.

**M2. Aider Repo Map 재사용과 "신규 인덱싱 엔진 도입 금지" 원칙의 긴장**
- 위치: §3 "Consider Aider-style relevance ranking only if simple lookup is insufficient." / Goal "Do not assume a new... indexing engine... is necessary."
- 실패 조건: Aider의 그래프 랭킹은 ctags/tree-sitter 기반 저장소 전역 태그 그래프 구축을 전제로 하며, 이는 그 자체로 인덱싱 인프라임. "필요시 고려"라고만 적으면 나중에 이 비용을 "기존 재사용"으로 오인해 별도 승인 없이 인덱서를 들여올 위험.
- 최소 수정: Aider식 랭킹을 도입하는 순간 그 그래프 구축 비용·소유자·승인 절차가 신규 컴포넌트 도입과 동일하게 취급된다는 문구를 명시.
- 검증: 단순 exact-match lookup으로 실패하는 실제 질의 사례를 먼저 수집해, 그 사례 수가 Aider 도입을 정당화하는지 확인.

**M3. 저사양 모델 대상 토큰/레코드/파일 예산의 구체적 수치 부재**
- 위치: §1, §3 "token/record/file budget" (숫자 없음), Goal "low-resource Qwen3.6-27B"
- 실패 조건: "최소 효과적 선택"을 주장하려면 실제 컨텍스트 창 크기 대비 예산 수치가 있어야 하는데 전혀 없음. "Qwen3.6-27B"라는 모델명도 공개된 Qwen 네이밍(1/1.5/2/2.5/3, .5B~72B 계열)과 불일치해 실제 컨텍스트 길이를 특정할 수 없음(오타/내부 포크 가능성 — MINOR로도 연결).
- 최소 수정: 실제 사용 모델의 확정 컨텍스트 길이를 먼저 확인하고, 그 대비 N토큰/M레코드/K파일 상한을 수치로 박아넣을 것.
- 검증: 실제 모델 설정값(컨텍스트 윈도우) 확인 후 예산표 1줄 추가.

**M4. Recovery V3 시딩이 Source Map 신뢰도 문제를 그대로 흡수할 위험**
- 위치: §4 "V3 uses map to seed alternate paths... without narrowing away uncovered paths"
- 실패 조건: B1이 해결되지 않은 상태에서 V3가 map 기반 대안 경로를 "verified" 수준 신뢰로 제시하면, 미검증 추론 엣지가 복구 절차에 암묵적 권위를 얻게 됨.
- 최소 수정: V3가 소비하는 모든 map 레코드는 원본 신뢰도 필드(B1)를 그대로 노출/전파해야 하며, 신뢰도 격상 금지 규칙을 Recovery 쪽에도 명문화.
- 검증: V3가 "inferred" 태그가 붙은 경로를 제시할 때 그 태그가 사용자/후속 단계까지 유지되는지 시범 케이스로 확인.

**M5. 그룹 게시 시 "기존 discovery outputs"와의 중복/충돌 해소 규칙 부재**
- 위치: Goal "existing discovery outputs are reported but ... approval scope are not established" vs §5 "group publication separate approval and existing conflict/CAS policy"
- 실패 조건: 기존(미확정) discovery 산출물과 신규 Source Map이 같은 영역을 다르게 기술할 경우 어느 쪽이 권위를 갖는지 규칙 없음 → 이중 진실 소스(dual source of truth) 위험.
- 최소 수정: 그룹 게시 승인 절차에 "기존 discovery outputs와의 교차 확인" 단계를 명시적 전제조건으로 추가.
- 검증: 동일 모듈에 대해 기존 discovery와 신규 map이 상충하는 가상 사례를 만들어, 설계가 명확한 우선순위/병합 규칙을 내놓는지 확인.

**M6. Q6(단계적 핸드오프 로드맵) 미제시**
- 위치: §Q6 — 본문은 "design GPT (packages/UI)"와 "business GPT (Updater, Recovery, host integration)" 역할만 언급하고 순서/게이트가 없음.
- 최소 수정(제안): 1단계 design GPT가 스키마 후보+Viewer 목업만 작성(설치 없음) → 2단계 business GPT가 샘플 모듈 1개로 실측 검증 → 3단계 게이트 승인 후 RAT 단위 점진 적용 → 4단계 그룹 게시는 M5 해소 후 별도 승인.
- 검증: 각 단계 경계에서 산출물(스키마 문서, 샘플 검증 리포트, 승인 로그)이 실제로 존재하는지 확인.

## MINOR

**m1.** "Qwen3.6-27B" 모델명이 공개된 Qwen 네이밍 체계와 불일치 — 오타 여부 확인 필요(예산 가정에 영향, M3와 연동).

**m2.** §2 "human MD derived from same validated data"에 재생성 트리거 미정의 — JSON/JSONL 게시와 MD 동시·원자적 재생성 규칙을 명시해 MD-JSON 드리프트를 막을 것.

**m3.** §5 "verify writer path/ACL, export preservation, read contract"는 검증을 리뷰어에게 요구하지만 본 패키지에는 해당 경로/ACL 정보가 전혀 포함되어 있지 않음 — 이번 리뷰에서는 검증 불가로 명시적으로 남김(아래 "미검증" 참조).

---

## 전체 판정: **REVISE**

핵심 이유: B1(기반 데이터 신뢰도 미확정)과 M1(평가 기준 부재)이 해결되지 않으면 "no fabricated edges"·"measurable acceptance"라는 이 설계의 핵심 주장 자체를 검증할 수 없음. ACCEPT_WITH_CHANGE로 가기엔 변경 사항이 세부 수정이 아니라 설계 결정(신뢰도 필드, 수치 예산, 평가 골드셋, 로드맵)이라 REVISE가 적절. 문서 자체는 전반적으로 보수적이고(신규 파서/DB/엔진 기본 도입 금지, 기존 컴포넌트 재사용 우선) 방향성은 타당함.

---

## 메타 정보

**실제로 읽은 지식 파일:** 핀 지식 없음(REQUEST에 "(none pinned)"). 패키지 파일은 `DESIGN_REVIEW_INPUT.md` 1개(전문 읽음)뿐.

**대조한 consumer profile:** code-analyzer(기존 사실 공급자 겸 읽기 전용 소비자 — 이중 역할 명확화 필요, B1), l1-channel-recovery(V2/V3, M4), work-ledger-kernel(원자적 게시/CAS 재사용 가정 — Kernel 코드가 패키지에 없어 검증 불가).

**미검증 항목(이번 리뷰로는 확인 불가):**
- 실제 설치된 Analyzer/Updater/Kernel/Viewer/MCP 구현 — 패키지에 코드 없음, 문서 주장만 존재.
- `source-map/` 작업공간 writer path/ACL, export preservation, read contract(§5) — 경로·권한 정보 자체가 패키지에 없음.
- Qwen 추론 환경(실제 컨텍스트 길이, Linux 호스트 동작) — Windows 정적 리뷰로는 검증 불가.
- 기존 discovery outputs의 실제 내용/승인 범위 — 문서가 스스로 "not established"라고 명시.

**공통 지식에 대한 수정 제안(채택 여부는 GPT 결정):**
- "Source Map 레코드는 extracted/inferred/unknown 3단 신뢰도 필드 필수"를 L1 설계 공통 규칙으로 등록 제안.
- "Aider식 랭킹 도입 = 신규 인덱싱 인프라 도입과 동일 승인 절차"를 공통 원칙에 추가 제안.
