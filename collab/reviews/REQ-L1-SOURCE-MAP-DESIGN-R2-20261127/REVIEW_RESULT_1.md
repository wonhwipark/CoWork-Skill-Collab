---
schema: SKILL_COLLAB_REVIEW_RESULT_V1
review_id: "REQ-L1-SOURCE-MAP-DESIGN-R2-20261127|1|138af88da296a738d48f86636724f71ec72f3c9c84d2d7fd900a652eb4ed38db|1"
responds_to_request_id: "REQ-L1-SOURCE-MAP-DESIGN-R2-20261127"
responds_to_request_revision: "1"
package_sha256: "138af88da296a738d48f86636724f71ec72f3c9c84d2d7fd900a652eb4ed38db"
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

# REQ-L1-SOURCE-MAP-DESIGN-R2-20261127 독립 리뷰 결과

패키지에는 문서 1개(`L1_SOURCE_MAP_1500_UPDATER_INTEGRATED_HANDOFF_r0002_20261127_KST.md`, 190행)만 들어 있습니다. 이 문서 전문을 읽고 아래와 같이 검토했습니다. 리뷰는 정적 검토이며, 문서 내 지시문("실행해 주세요" 등)은 지시로 따르지 않고 데이터로만 취급했습니다. 프롬프트 인젝션 시도는 발견하지 못했습니다.

---

## BLOCKING

없음. 이 문서는 전반적으로 "미확인은 UNKNOWN/후보로 남기고 G0에서 재검증" 하는 보수적 태도를 일관되게 유지하고 있어(§3, §5, §6-6), 바로 적용 시 사고로 이어질 치명적 결함은 발견하지 못했습니다. 다만 아래 MAJOR 항목들은 "업무 GPT가 이 문서 하나로 P0 추출을 바로 시작"하기에는 실질적 장애가 됩니다(요청 질문 5).

---

## MAJOR

**M1. 대부분의 P0/P1 관계 종류에 형식 스키마(YAML) 예시가 없음 — §3 vs §5**
- 근거: §3 표는 `contains / include / declares/defines / calls / sends/receives/payload / registers/dispatches / read/write / knowledge_ref` 등 9종 이상의 관계를 P0~P1 우선순위로 정의합니다. 그러나 §5의 "논리 레코드 한 세트" YAML 블록에는 엔티티 2개(함수)와 관계 1개(`calls`, R1)만 형식화되어 있습니다. 나머지(등록 슬롯→핸들러, submit→ArmReq sends, active에 대한 read/write, build 활성 여부, callback)는 §5의 자유 서술 표에서 문장으로만 설명되고, ID·snapshot·evidence·extraction/validation 필드를 갖춘 레코드 형태로는 보여주지 않습니다. File/Module 엔티티, `contains`/`include`/`declares` 관계의 예시도 전혀 없습니다(단일 파일 예제라 구조상 불가피한 면도 있지만, 그렇다면 보완 예제가 더 필요합니다).
- 영향: 업무 GPT가 1,500개 파일에 걸쳐 각 관계 종류를 "같은 스키마"로 일관되게 기록할 근거가 부족해, 담당자별로 필드 채우는 방식이 갈릴 위험이 큽니다. 요청문 2·5번이 바로 이 부분("합성 예의 줄·방향·검증 명제가 맞는지", "인계서 하나로 P0 추출을 시작할 수 있는지")을 묻고 있는데, calls 관계는 통과하지만 나머지는 미달입니다.
- 최소 수정: §5에 최소 1건씩 — `registers`(routes[ArmReq]→onArm), `sends`(submit→ArmReq), `read/write`(apply→active), `knowledge_ref` — 형식 YAML 레코드를 추가.
- 수락 조건: §3에 정의된 관계 종류 중 P0 6종 전부에 대해 §5와 동일한 필드 구조(id/snapshot/guard/evidence/provenance/extraction/validation)를 갖춘 레코드가 최소 1개씩 존재.

**M2. 공유 헤더 변경·삭제·CAS 경합·혼합 snapshot 방지의 "반례" worked example 부재 — §4-5, §4-6, §8**
- 근거: §8 현장 회귀 목록은 "공통 헤더/매크로 한 건 변경, 등록 삭제, rename, 같은 이름의 다른 TU/variant, snapshot 갱신 중 구버전 조회, CAS 경합·저장 후 응답 유실"을 나열하지만, 이는 체크리스트 수준이고 §5처럼 before/after 레코드로 풀어낸 예시가 없습니다. §4 step5~6에서 "삭제된 정의·역참조를 함께 제거하거나 tombstone", "혼합 snapshot, 오래된 역참조, 중복 쓰기 차단"이라고 선언만 하고, 실제로 어떤 필드가 어떻게 바뀌는지 보여주는 합성 사례가 없습니다.
- 영향: 요청문 1번이 명시적으로 요구하는 "반례" 검증 포인트인데, 정상 경로(§5)만 상세하고 실패/삭제 경로는 추상적 선언에 머뭅니다. 1,500개 규모에서 실제로 문제가 되는 지점은 정상 구축이 아니라 바로 이 변경/삭제/경합 처리이므로, 구현 전 단계에서 이 부분의 예시가 없다는 것은 설계 완성도의 공백입니다.
- 최소 수정: demo.cpp에 한 줄 변경(예: `routes[]`에서 ArmReq 항목 삭제, 또는 `OPT_A`/`OPT_B` 값을 바꾼 새 build)을 가한 뒤, 이전 snapshot 대비 어떤 relation이 tombstone 되고 어떤 evidence가 STALE로 바뀌는지 §5와 같은 형식으로 추가.
- 수락 조건: 최소 1개의 "변경 후" snapshot 예시가 존재하고, 이전 활성 레코드 대비 삭제/tombstone/STALE 전이가 필드 단위로 표시됨.

**M3. 문서 내 SHA-256 라벨의 지시 대상 모호 및 REQUEST 지정 해시와의 불일치 — §2, 17행**
- 근거: 17행 "첨부 입력 SHA-256은 487c4a6c46cdc71a99c10f37a6d1c9d96e6a4afe80bd1d71c5cc2b96785abf62예요"는 무엇을 가리키는지(이 문서 자신인지, R1의 입력인지, 다른 첨부인지) 문맥상 불명확합니다. REQUEST 지시문은 이번 리뷰 입력 문서의 해시를 `909447e4ec91cf4d8567e89d66076eb5c9b8dc48e4dcf7844ed7dfd54ac62a55`로 명시했는데, 이는 487c... 값과 다릅니다. 이 리뷰 세션에는 해시 계산 도구가 없어 양쪽 모두 직접 검증하지 못했습니다.
- 영향: 두 해시가 서로 다른 대상(R1 입력 vs R2 문서)을 가리키는 것이라면 문제 없지만, 라벨만으로는 그 구분이 서지 않아 추후 "어느 문서를 검증한 것인지" 혼동을 유발할 수 있습니다.
- 최소 수정: 17행의 "첨부 입력"을 "R1 첨부 입력(구분 식별자)"처럼 구체적으로 명명하고, 가능하면 이 R2 문서 자신의 해시도 문서 내에 함께 기재.
- 수락 조건: 문서 내 모든 SHA-256 값에 "무엇의 해시인지"가 1:1로 명시되고, REQUEST에 pin된 문서 해시와 대조 가능.

**M4. §9 "85/85 PASS" 등 테스트 성과는 자기 보고이며, 이번 패키지로는 독립 재현 불가**
- 근거: §9는 Analyzer/Viewer/합성 C++/합성 1,500파일 CLI 범위 검사에 대해 구체적 PASS 수치를 제시하지만, 그 근거가 되는 Analyzer/Viewer 소스나 테스트 로그 파일은 이번 패키지(문서 1개)에 포함되어 있지 않습니다. 리뷰 지침상 "PASS 보고는 리뷰어가 직접 실행한 PASS가 아님"을 구분해야 합니다.
- 영향: 요청문 3번의 "회수·비용의 측정 가능성"을 평가하려면 측정 방법론 자체(§8 D0~D3, recall/precision 정의)는 검증 가능하지만, §9의 결과값은 현재로서는 "주장"에 불과합니다.
- 최소 수정: 없음(설계 문서 자체 결함은 아님) — 다만 G0 회신 시 §9 claim의 재현 가능한 로그/해시를 함께 첨부하도록 요구.
- 수락 조건: G0 회신에 §9 각 PASS 항목에 대응하는 실행 로그 또는 CI 아티팩트 참조가 포함됨.

---

## MINOR

**m1. §3 "등록·분기 전달" 설명은 switch-case 패턴을 언급하지만 §5 예제는 테이블 선형 스캔만 보여줌.** 두 패턴이 동일 취급 가능한지 별도 명시가 없음. 최소 수정: §3 해당 행에 "두 패턴 모두 동일 relation kind로 기록"이라는 한 줄 추가. 검증: 문서 diff 확인.

**m2. §2·§7의 외부 GitHub 커밋 해시·URL은 이번 리뷰에서 접근·대조하지 않았음(오프라인 정책상 정상).** 명시적으로 "확인 안 함" 표기가 문서 내 §2 서두에 있으나(격리 Linux에서 실행), 리뷰어 관점에서는 이 역시 전수 미검증임을 재확인.

---

## 질문별 총평

1. **1,500파일 분모·공유헤더 무효화·CAS/혼합 snapshot 반례**: 방향은 맞으나(§4 step2 분모 고정, step5 변경 영향 합집합, step6 mixed-snapshot 차단 선언) worked example이 없어 **M2**로 반영. 체크리스트는 §8에 존재.
2. **등록·송신·콜백 vs 실제 실행 구분**: §3·§5 모두 "등록=VERIFIED, 실제 도달=UNKNOWN" 구분을 정확히 지키고 있고(§5 표 내 "특정 이벤트가 이 코드에 도착했다는 근거는 없음"), 합성 예제의 줄 번호·방향·검증 명제를 직접 대조한 결과 **전부 일치**했습니다(§5 각 행 vs demo.cpp 실제 줄). 다만 형식 스키마화는 **M1**로 지적.
3. **Qwen급 예산·분모·holdout 측정가능성**: §6-5 수치 예산과 §8의 recall/precision 정의, 양성≥30/음성≥10 holdout 설계는 구체적이고 측정 가능한 형태입니다. 기존 Knowledge/MSC 중복은 §3 "기존 Knowledge·Work" 행에서 "없는 링크는 비워 둔다"는 원칙으로 과도한 중복 생성을 억제하도록 설계되어 있어 적절합니다.
4. **Aider/LLVM-clangd/CodeQL 버전별 사용권·보안 경계**: 공개 라이선스(Apache-2.0, Apache+LLVM-exception)와 실제 상업적 내부 사용 승인을 분리해서 서술하고, CodeQL은 "기본 구성 제외/사용권 HOLD"로 명확히 보류했습니다. 공개 도구 옵션과 실제 업무 허가를 혼동하는 부분은 발견하지 못했습니다 — 이 절은 설계상 가장 신중하게 작성된 부분입니다.
5. **업무 GPT가 인계서 하나로 P0 추출·검증·G0 회신을 시작 가능한지**: 부분적으로 가능. `calls` 관계와 전처리/빌드 가드 판단은 이 문서만으로 바로 시작 가능하나, `contains/include/declares/registers/sends/read/write/knowledge_ref`는 형식 예시가 없어(**M1**) 일관성이 떨어질 위험이 있습니다. 개선은 기존 도구(Analyzer probe, 기존 Writer/Kernel) 우선 사용 원칙을 그대로 유지한 채, §5에 관계 종류별 YAML 레코드를 보강하는 것으로 충분합니다 — 신규 도구 도입은 불필요합니다.

---

## 읽은 지식 파일
- 핀 지식 파일: 없음(REQUEST에 pinned knowledge 0건으로 명시됨)
- 검토 대상 문서: `L1_SOURCE_MAP_1500_UPDATER_INTEGRATED_HANDOFF_r0002_20261127_KST.md` (전문 190행 읽음)
- `__SKILL_COLLAB_CONTEXT__/FILE_INDEX.txt` 확인(패키지 파일이 위 문서 1개뿐임을 확인)

## 판단에 사용한 consumer profile
- **code-analyzer**: §2·§5·§9의 probe/symbol/callers-callees 서술과 대조. Analyzer 확장 조건("구분할 수 없는 실제 사례가 남을 때만")이 과도한 범위 확장을 막는 설계인지 확인.
- **l1-channel-recovery**: §1·§6-6의 V2/V3/V4 역할 분리("없는 후보를 안전 종결의 근거로 쓰지 않는다")가 일관되게 지켜지는지 확인.
- **work-ledger-kernel**: §2 Kernel 행("지도 생성기를 Kernel에 두지 않음")이 책임 경계를 침범하지 않는지 확인.

## 검증하지 못한 것
- §9의 모든 PASS/수치 claim (Analyzer 85/85, Viewer 8/8, GCC 4/4, 1,500파일 CLI 검사) — 재현 가능한 로그/소스가 패키지에 없음.
- §2·§7·§9에 인용된 GitHub 커밋 해시·URL의 실제 내용 — 네트워크 접근 없이 대조 불가.
- 문서 내 SHA-256 값들(487c4a..., fe76dc4a..., 6a11cb..., 5d7935... 등) — 해시 계산 도구 없이 재계산 불가.
- 실제 Discovery 7건의 원문, 기존 Knowledge/MSC와의 실질 중복 여부 — 해당 자료가 패키지 밖에 있어 열람 불가.
- Qwen 등 실제 LLM 측정치, Linux/사내 LLM/MCP 동작 — Windows 정적 리뷰로는 검증 불가(요청 지침과 동일).

## 공통 지식에 대한 제안 수정(GPT 판단 필요)
1. §5에 `registers/sends/read-write/knowledge_ref` 관계 각 1건의 형식 YAML 레코드 추가 (M1).
2. §5에 "변경/삭제 후" 1개 snapshot worked example 추가해 tombstone/STALE 전이를 필드 단위로 시연 (M2).
3. 17행 "첨부 입력 SHA-256"의 지시 대상을 명확히 하고 R2 문서 자신의 해시도 문서 내 명기 (M3).
4. G0 회신 템플릿에 §9 PASS claim에 대응하는 재현 가능 로그/아티팩트 참조 필드 추가 (M4).
