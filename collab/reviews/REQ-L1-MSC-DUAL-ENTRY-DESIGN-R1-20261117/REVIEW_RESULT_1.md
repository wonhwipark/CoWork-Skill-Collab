---
schema: SKILL_COLLAB_REVIEW_RESULT_V1
review_id: "REQ-L1-MSC-DUAL-ENTRY-DESIGN-R1-20261117|1|e5c2da38fda253781b2cf0179c46d3cd6dbefdc5f5efb3f0603ddaaf7d03b91c|1"
responds_to_request_id: "REQ-L1-MSC-DUAL-ENTRY-DESIGN-R1-20261117"
responds_to_request_revision: "1"
package_sha256: "e5c2da38fda253781b2cf0179c46d3cd6dbefdc5f5efb3f0603ddaaf7d03b91c"
skill_id: "l1-knowledge-updater"
run_policy_ref: "POLICY-STATIC-V1"
knowledge_refs: []
consumer_profiles: ["l1-msc-dual-entry-independent-design-review"]
reviewer_os: WINDOWS
review_scope: CODE_REVIEW
test_policy: "STATIC_ONLY"
execution_status: COMPLETED
limitations: ["static review by an automatically started Claude Code process; no package code was executed", "knowledge files were delivered as the REQUEST pinned them; which parts were actually read is reported by the reviewer in the text", "reviewer host is Windows; Linux, in-house LLM and MCP behaviour are not verified by this review"]
---

# 리뷰 결과

# REQ-L1-MSC-DUAL-ENTRY-DESIGN-R1-20261117 — 독립 설계 리뷰 결과

## 결론: **ACCEPT_WITH_CHANGE**

두 독립 진입(Updater 직접 지식화 / Workflow 이슈 AS-IS·TO-BE)의 책임 분리, 공통 기능 재사용 구조, HTML 최소 보완안은 구조적으로 타당하고 근거(소스 발췌)와 일치합니다. 차단 결함은 발견하지 못했습니다. 다만 아래 비차단 개선 2건은 다음 리비전에 반영을 권고합니다.

---

## 1. 설계 이해 및 타당성 판단 (Q1, Q9)

- **Q1 (독립성)**: `02`/`01` 섹션 2의 다이어그램에서 A(`Updater`)→`C1`→`M`→`knowledge/`, B(`Workflow`)→`C2`→`E`→`works/`는 실선 경로가 서로 분리되어 있고, `C1 -.-> C2`(동일 계약, 호출 아님)와 `R -.-> M`(명시적 opt-in, 자동 아님)만 점선으로 연결됩니다. 숨은 강제 호출은 코드 근거(E01~E05) 상에서도 발견되지 않았습니다. 단, "Work ID 없이 출처/revision 보존"이 실제로 기존 Updater 계약으로 가능한지는 `02`/`03`(E06)에서 스스로 G0로 솔직하게 유보하고 있어, 문서가 미확인 사항을 확정된 기능으로 승격하지 않은 점은 적절합니다.
- **Q9 (과잉 설계 여부)**: 섹션 2, 5, 7에서 신규 엔진/Kernel 상태기계/Evidence enum/Work profile 확장을 명시적으로 기본안에서 제외했습니다. 재사용 우선 원칙이 실제로 지켜지고 있습니다.

## 2. 확인된 결함과 근거 (Q2, Q4, Q6)

**차단급 결함 없음.** 다음은 "확인된 사실"로서 설계가 스스로 식별한 gap이며, 코드 라인 근거와 일치함을 직접 대조 확인했습니다.

- **(확인) HTML opt-in gap (Q4)**: `03_SOURCE_EVIDENCE.md` E02 (`scenario_msc.py` 50~73행)에 `--view-mode`/`PROCEDURE_FEATURE` 전달이 없고, E04 (`msc_tool.py` 293, 861, 922, 928행)는 `view_mode=="PROCEDURE_FEATURE"`이고 렌더 성공일 때만 B HTML을 생성합니다. 따라서 현재 Workflow 이슈 경로는 모던 HTML을 받을 수 없다는 주장은 제시된 발췌로 뒷받침됩니다. 제안된 opt-in 플래그는 ISSUE 본문 의미(293행 `procedure_mode` 판정)와 HTML 생성 트리거(922행)를 분리하는 최소 변경으로, 기존 두 호출자의 기본 동작을 바꾸지 않는 설계입니다. 대안 B("단순히 PROCEDURE_FEATURE로 강제")를 "이슈 설명을 잃는 방식"으로 명시적으로 배제한 점도 타당합니다.
- **(확인) 동명 MSC_VIEW.md 두 역할 (Q2)**: E03(`work_ux.py` 903~904, 1075행)의 Work-root 안내 파일과 E04(`msc_tool.py` 1053행)의 Converter 상세 파일은 서로 다른 경로에 쓰이므로 덮어쓰기 충돌은 코드상 없습니다. 다만 두 파일이 **동일한 파일명**으로 서로 다른 트리에 존재하며, 사람이 링크 텍스트("MSC 보기")만 보고 어느 쪽인지 구분하기 어렵습니다. 문서는 "역할이 다름"이라고만 서술하고 구분 규칙(파일명/링크 문구)을 못박지 않았습니다. → 비차단 개선 1.

## 3. 비차단 개선 (Q5, Q7)

1. **MSC_VIEW.md 명칭 구분 규칙 추가**: Work-root 안내 파일과 Converter 상세 파일에 대해 (a) 서로 다른 파일명(예: 안내 파일을 `MSC_VIEW.md` 대신 `MSC_INDEX.md` 등으로) 또는 (b) 링크 문구에 "상세/원본" vs "작업 안내"를 명시하는 최소 규칙을 다음 리비전에 추가 권고합니다. 비용은 문자열/상수 변경 수준으로 낮고, 기존 writer 동작을 바꾸지 않습니다.
2. **수동 편집/마커 메커니즘의 소유자 명시**: T08(사람 수정 MD·마커 누락/충돌)이 수락 시나리오에 등장하지만 `01_DESIGN.md` 본문에는 마커/앵커 메커니즘 자체가 설명되지 않고 "기존 계약"으로만 위임되어 있습니다. 부분 실패·수동 편집은 가장 회귀 위험이 큰 영역이므로, 다음 리비전에서 이 메커니즘의 소유 스킬(Updater writer vs Kernel writer)과 충돌 시 기본 동작(Preview/HOLD)을 한 줄로라도 명시할 것을 권고합니다. 이는 구조 변경이 아니라 기존 결정을 문서에 드러내는 수준입니다.

이 두 개선 모두 구조 대안이 아니라 "최소 보완" 수준이며, 구현 비용과 호환성에 영향을 주지 않습니다.

## 4. G0 / 미검증 목록 (Q3, Q8)

- Updater/그룹 writer의 실제 설치 원문·API, 개인 knowledge 폴더 구조, Work-ID-less 출처 보존 방식 — `02`(확인한 사실과 미확인), `03`(E06)에서 동일하게 미확인으로 일관되게 표기됨.
- Kernel/Updater 두 writer의 링크 재매핑 지원 여부 — "기능 없음으로 단정하지 않음"이라고 올바르게 유보.
- 회사 호스트의 HTML 렌더/Pages 접근(E3) — 범위 밖으로 명시.
- **Q8 답**: HTML opt-in(Workflow 경로)은 Converter/Workflow/gateway 변경만 필요하고 Updater/그룹 writer G0와 분리되어 있어, Updater G0가 미해결이어도 HTML 보완은 독립적으로 진행 가능합니다. 설계가 이 분리를 올바르게 유지하고 있습니다.

## 5. 다음 구현 순서 제안 (문서가 이미 제시한 순서에 동의)

1. Converter: HTML opt-in 플래그 추가 (parser/allowed_flags) — 기존 ISSUE/PROCEDURE_FEATURE 기본 동작 불변 확인 (T05, T06).
2. Workflow: MSC handoff에 opt-in 플래그 전달 경로 추가, 양쪽 caller 회귀 시험.
3. (독립) Updater/그룹 writer G0 확인 — 완료되는 대로 Work-ID-less 출처 보존·링크 재매핑 가능 여부 판정.
4. 위 1~2의 완료 게이트와 3의 완료 게이트는 서로 차단하지 않음(Q8).

---

## 읽은 지식 파일
- 패키지 6개 파일 전부 읽음: `README.md`, `01_DESIGN.md`, `02_CONTEXT_AND_SKILL_RELATIONSHIPS.md`, `03_SOURCE_EVIDENCE.md`, `04_ACCEPTANCE_AND_REVIEW_QUESTIONS.md`, `REVIEW_MANIFEST.json`.
- REQUEST에 핀된 별도 지식 파일 없음(0건).

## 판단에 사용한 consumer profile
- `l1-msc-dual-entry-independent-design-review` (REQUEST에 지정된 유일한 프로필).

## 검증하지 않은 것
- `03_SOURCE_EVIDENCE.md`의 코드 발췌(E01~E05)는 패키지에 포함된 "읽은 결과"만 신뢰했고, 원본 저장소(`wonhwipark/CoWork-Skill-Collab`)에 직접 접근해 해당 라인을 재확인하지 않았습니다 — 패키지의 SHA-256 주장과 발췌 내용의 일치는 제 자신의 실행 검증이 아니라 패키지 저자의 주장입니다.
- Converter 0.2.26 "공개 전달 및 96 PASS" 등 개발 자체시험 결과는 패키지의 보고를 그대로 인용했을 뿐, 제가 직접 실행한 PASS가 아닙니다.
- 업무 호스트(OpenCode/로컬 Agent), 실제 L1 소스, Updater/그룹 writer 설치본은 범위 밖으로 전혀 조회하지 않았습니다.
- Windows 리뷰이므로 Linux 호스트/사내 LLM/MCP 동작은 검증 대상이 아니었습니다.

## 공통 지식(common knowledge)에 대한 제안 (GPT 판단 필요)
- 제안 1: "동일 파일명(MSC_VIEW.md)이 Work-root 안내와 Converter 상세 산출물 양쪽에 쓰일 수 있다"는 점을 스킬 간 공통 명명 규칙 문서에 명시해 향후 다른 요청에서도 재발하지 않도록 반영 검토.
- 제안 2: HTML opt-in 플래그 설계가 승인되면, "문서 목적(mode)과 렌더 출력 여부(opt-in)는 분리된 축"이라는 원칙을 Converter 공통 계약 문서에 일반 규칙으로 추가할 가치가 있음 — 현재는 이번 요청 범위의 개별 제안으로만 존재.
