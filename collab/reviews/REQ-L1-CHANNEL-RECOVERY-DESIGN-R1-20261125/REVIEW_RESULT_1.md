---
schema: SKILL_COLLAB_REVIEW_RESULT_V1
review_id: "REQ-L1-CHANNEL-RECOVERY-DESIGN-R1-20261125|1|6b0803091be6ae0272ca4b5d909fa0869d65297611f158dea919dc6a4d4a44a7|1"
responds_to_request_id: "REQ-L1-CHANNEL-RECOVERY-DESIGN-R1-20261125"
responds_to_request_revision: "1"
package_sha256: "6b0803091be6ae0272ca4b5d909fa0869d65297611f158dea919dc6a4d4a44a7"
skill_id: "l1-channel-recovery"
run_policy_ref: "POLICY-STATIC-V1"
knowledge_refs: []
consumer_profiles: ["code-analyzer", "doc-converter", "work-ledger-kernel"]
reviewer_os: WINDOWS
review_scope: CODE_REVIEW
test_policy: "STATIC_ONLY"
execution_status: COMPLETED
limitations: ["static review by an automatically started Claude Code process; no package code was executed", "knowledge files were delivered as the REQUEST pinned them; which parts were actually read is reported by the reviewer in the text", "reviewer host is Windows; Linux, in-house LLM and MCP behaviour are not verified by this review"]
---

# 리뷰 결과

# L1 Channel Recovery r0003 독립 설계 리뷰 결과

## 전체 판정: **조건부 승인** (MAJOR 1건 수정 권장, 그 외 MINOR 다수)

r0003은 기존 r0002/r0002(계약)/11월 24일 인계의 핵심 원칙(판정 4분류, V0~V6, Edge 미확정 표시, 두 스킬 실제 호출, 보존·재조회)을 일관되게 계승하고 있고, 요청에서 지정한 두 중요 사례도 명확히 다룹니다. 다만 소스 폴더 사전 확인 표의 한 문장이 "경로 불일치"와 "revision 불일치"를 섞어 서술해 구현 시 질문 예산(1회) 위반 위험이 있어 MAJOR로 지적합니다.

---

## BLOCKING

없음. 읽은 범위 안에서 수락을 전면 막을 결함을 찾지 못했습니다.

---

## MAJOR

### M1. 소스 폴더 사전 확인 표의 "경로 불일치"와 "revision 불일치" 혼용 (2절, 23행 vs 29행)

- **위치**: `L1_RECOVERY_...r0003...md` 2절 표 1행(23행) "지정 경로를 읽을 수 없거나 프로젝트·요청 revision이 맞지 않으면 이유를 알려 주고 올바른 경로를 한 번 물어요" vs 29행 "지정 revision이 있으면 일치 여부를 별도로 확인하고, 같은 폴더에서 HEAD가 바뀌었으면 새 revision이 영향을 주는 근거만 갱신해요."
- **실패 조건**: 지정 경로는 유효하고 대상 프로젝트도 맞는데, 지정 revision만 현재 HEAD와 다른 경우. 23행만 보면 "경로가 맞지 않다"고 판단해 사용자에게 **"제품 소스 폴더 경로가 어디인가요?"**를 묻게 되는데, 사용자는 경로가 맞다고 답할 뿐 질문의 취지(어떤 revision을 쓸지)에 답하지 못합니다. 이 경우 재질문이 필요해져 6절의 수락 기준("질문 1회, 재질문 0회")을 위반할 수 있습니다.
- **반례**: 요청에 `path=/src/l1, revision=CL123`이 명시됨. `/src/l1`은 존재·읽기 가능·대상 프로젝트 일치하지만 현재 HEAD는 `CL130`. 23행의 "프로젝트·요청 revision이 맞지 않음" 조건에 해당해 "올바른 경로"를 묻게 되지만, 29행의 절차(일치 여부 별도 확인, HEAD 변경 시 근거만 갱신)와 모순되는 지시가 됩니다. 사용자가 "경로는 맞다, CL130을 써라"고 답하면 질문·답변 흐름이 표 1행이 예정한 "경로 재질문"과 들어맞지 않아 구현자가 둘 중 어느 것을 따를지 불명확합니다.
- **최소 수정**: 2절 표 1행을 다음처럼 분리. "① 경로를 읽을 수 없거나 대상 프로젝트가 다르면 → 올바른 경로를 한 번 물음. ② 경로·프로젝트는 맞지만 지정 revision과 실제 revision이 다르면 → 어느 revision을 쓸지 한 번 물음(경로 재입력 요구 아님). ③ revision 미지정 상태에서 같은 경로의 HEAD만 바뀌었으면 → 질문 없이 새 revision 근거만 갱신."
- **확인 시험**: 지정 경로=유효, 지정 revision≠현재 HEAD인 입력으로 실행 → 질문 문구가 "경로"가 아니라 "revision 선택"을 묻는지, 질문 횟수 1회, 답변 후 재질문 0회인지 확인.

---

## MINOR

### N1. 5.3절 "변환 전·후 검증" 실패 시 등록 차단 여부 미명시 (76행)
- **내용**: "변환 전 의미 검증과 변환 후 결과 대조가 모두 필요해요"라고만 되어 있고, 검증 실패 시 Work 등록/링크를 막는지 명시하지 않음. 5.5절(78행)의 재개 분기(렌더러 누락/저장 충돌/링크 누락)에 "순서 역전이 사후 검출된 경우"가 포함되지 않음.
- **제안 문구**: "변환 후 대조에서 순서·방향 불일치가 발견되면 해당 결과를 Work에 등록·링크하지 않고 4절 마지막 행의 재입력 절차로 되돌림."
- **시험**: 역순 MSC를 Converter에 투입해 형식 검증은 통과하되 의미 대조에서 불일치가 나는 입력 → Work에 링크가 생성되지 않는지 확인.

### N2. Workflow v1.6.75 ZIP 이원화 처리의 종료 조건 부재 (80행)
- **내용**: "ZIP 내용이 다른 기존 후보가 둘이어서 설치본의 실제 소스·해시·지원 경로로 매핑해요"라고만 되어 있어, 매핑이 불가능할 때(설치 호스트 접근 불가 등) 분석을 어떻게 중단·보류하는지 없음.
- **제안**: "매핑이 확인되지 않으면 해당 버전의 Recovery 실행을 보류하고 이유를 Work에 남김"을 추가.
- **시험**: 설치본 해시 확인이 불가능한 상태를 가정해 Recovery가 보류 상태로 멈추는지 확인(실제 실행 환경 필요, 이번 리뷰로는 미검증).

### N3. Edge 의미 미확정 시 Converter 호출 차단 범위 불명확 (75행)
- **내용**: "미확정 Edge는 그 상태를 표시해요"는 있으나, Edge 의미가 끝까지 미확정인 채로 MSC AS-IS/TO-BE 생성 자체를 계속 진행해도 되는지(생성은 하되 표시만 미확정) 또는 생성을 보류하는지 불명확.
- **제안**: "Edge 의미가 업무 GPT 계약으로 확정되기 전에는 Edge를 포함하는 출력 요소만 '미확정'으로 표시하고, 노드·발신/수신/순서 등 Edge와 무관한 MSC 요소는 정상 생성."
- **시험**: Edge 정의가 비어 있는 입력으로 Converter를 호출해 비-Edge 요소는 생성되고 Edge 관련 요소만 미확정 표시되는지 확인.

---

## 두 중요 사례의 판정 이유

### 사례 1: 잘못된 명시 경로가 유효한 저장값과 함께 있는 경우 — **적절히 설계됨**
23행 "저장된 다른 경로로 자동 전환하지 않아요"는 명시적 요청을 우선하는 안전한 선택입니다. 사용자가 특정 경로를 지정했다면 그 의도(예: 다른 브랜치/스냅샷 검증)가 있을 가능성이 높고, 저장된 과거 경로로 조용히 대체하면 잘못된 소스에 대해 분석하고도 사용자는 알아채지 못할 위험이 있습니다. 따라서 "이유 설명 + 1회 질문, 자동 대체 금지"는 정확성과 투명성을 질문 1회 비용으로 교환하는 합리적 설계입니다. 단, M1에서 지적한 대로 "경로 불일치"와 "revision 불일치"를 같은 조항으로 뭉친 점은 분리해야 합니다.

### 사례 2: HAL 결과 판단 전 성공 통지 — **적절히 설계됨**
59행에서 두 실패 경로 모두 자원은 반납하지만 한 경로만 HAL 결과를 판단하기 **전에** 성공을 통지한다고 명시했고, 63행 해결안은 "반환을 판정한 뒤 성공/실패로 분기 → 성공은 한 번, 실패는 소유자가 획득분만 정리하고 한 번"으로, 정확히 순서 결함(판단 전 통지)을 구조적으로 제거합니다. 65행(이미 상위 전이가 끝난 경우)은 "예방 우선, 안전한 정정 수단이 없으면 상위 이관 또는 보류"로 사후 패치보다 원인 수정을 우선시해 중복 종료를 피합니다. 64행(비동기 접수/완료 분리)도 "완료 근거 확보 후 성공 확정 + 기존 세대 식별 규칙으로 지연/중복 구분"을 요구해 정상 지연을 오판하지 않도록 설계되어 있습니다. 세 조항이 서로 보완적으로 중복 종료·과잉 복구를 가려낼 수 있는 구조입니다.

---

## 읽은 지식 파일
- 핀 지식 파일: 없음 (REQUEST에 핀 지식 없음)
- 패키지 파일 전체 읽음: `REVIEW_SCOPE.md`, `SHA256SUMS.txt`, `L1_RECOVERY_POINT_ANALYSIS_DETAILED_DESIGN_AND_IMPLEMENTATION_HANDOFF_r0003_20261125_KST.md`(심사 대상 전문), `PRIOR_HANDOFF_EXCERPTS.md`(r0002/r0002계약/11월24일 인계 발췌, 대조용)

## 대조한 consumer profile
code-analyzer(진입점 오류·focus 옵션 결함 대응), doc-converter(역순 MSC 수용 결함·의미 검증 대응), work-ledger-kernel(기존 Work/Evidence 재사용·중복 등록 방지 계약). Viewer는 REQUEST 범위에 언급돼 있어 5절 열람 단계만 함께 확인했으나 별도 consumer_profile로는 지정되지 않음.

## 미검증 (이번 정적 리뷰로 확인 못함)
- Qwen3.6-27B가 업무 호스트에서 실제로 이 지침을 따랐을 때의 실행 결과(질문 횟수, 판정 정확도 등)
- code-analyzer v0.15.5 / doc-converter v0.2.26의 실제 바이너리 동작(문서에 적힌 결함 재현 여부) — r0003의 "직접 관찰값" 주장 자체는 신뢰하되 제 자신이 재실행한 것은 아님
- 업무 호스트의 실제 소스 폴더 구조, Git/P4 설정, Workflow v1.6.75의 실제 설치본 해시
- Kernel v0.7.47 / Viewer v0.5.3의 실제 Work/Evidence 쓰기·읽기 동작과 HTML/SVG 실제 열람
- 제품(C++) 상의 실제 복구 효과 — 합성 시험 결과만 문서에 기재되어 있고 이번 리뷰로 독립 재현하지 않음

## 공통 지식에 대한 제안 수정 (GPT 결정)
- 2절 "소스 폴더 사전 확인" 표의 1행을 M1 제안대로 "경로 무효/프로젝트 불일치"와 "경로 유효/revision만 불일치"로 분리해 공통 지식(향후 유사 가이드)에도 반영 권장.
- 5.3절/5.5절에 "변환 후 의미 대조 실패 시 Work 등록 차단"을 명시적 재개 분기로 추가해 둘 것을 공통 패턴으로 제안.
