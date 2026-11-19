---
schema: SKILL_COLLAB_REVIEW_REQUEST_V1
state: SUBMITTED
request_id: REQ-L1-WORKSPACE-WIKI-UI-UX-R1-20261119
request_revision: 1
project_id: L1-WORKSPACE-RAG-20261111-001
work_id: L1-WORKSPACE-RAG-20261111-001
skill_id: l1-knowledge-updater
package_path: /SKILL-COLLAB/packages/l1-workspace-wiki-ui_v0_1_0_1119.zip
package_file_id: github:REQ-L1-WORKSPACE-WIKI-UI-UX-R1-20261119
package_rev: l1-workspace-wiki-ui-v0.1.0
package_sha256: 411553e74e76bb82237fd2ebef65169769e4dbe4cfd2231afb5afd38559b10a9
package_size_bytes: 267140
baseline_package_ref: null
knowledge_refs: []
consumer_profiles: [l1-workspace-wiki-ui-visual-ux-review]
reviewer_os: WINDOWS
test_policy: STATIC_ONLY
run_policy_ref: POLICY-STATIC-V1
output_contract: SKILL_COLLAB_REVIEW_RESULT_V1
goal: one independent visual usability review of implemented team wiki UI before business GPT handoff
---

# 2안 모던 팀 위키 UI v0.1.0 — 화면 구성·가독성·스타일·시인성 독립 R1

## 사용자 요청·승인·현재 게시 단계

- 사용자 최신 지시: **업무 GPT에 전달하기 전에**, 위 작업의 화면 구성, 가독성, 화면 스타일, 사용자 관점의 시인성을 협업 리뷰 요청.
- 기존 유효 승인 재사용: 2026-11-19 신규 정식 독립 리뷰 공통 **최대 USD 3.00/건·이 요청 1회**. 새 비용 승인을 반복 요청하지 않음. 추가 호출·재시도·자동 R2·운영 설정 변경을 포함하지 않음.
- 이 파일은 **기존 Work에 게시하는 비실행 REQUEST 초안**. frontmatter는 호스트가 그대로 검증할 후보 바이트이며, `state: SUBMITTED`만으로 정식 접수된 것이 아님. 실제 Windows LIVE `--intent unified` select/check PASS 전에 `collab/requests/<ID>/REQUEST.md`로 게시 금지. READY/서명은 아직 없음.
- 기존 r0002 리뷰는 설계·보안 검토로 완료된 별도 입력. 이 구현물의 시각 리뷰를 완료했다고 소급하지 않으며 기존 리뷰 재큐잉·재과금 0. 과거 UX-OWNER 후보 문서와 이번 완성본 UI 리뷰를 혼동하지 않음.

## 정확한 고정 입력

PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`에서 수신하되, 실제 검토 대상은 **content commit `17ac2b39ad01dc3e01df467ada698fbac8b5c399`**에 고정.

- ZIP: `collab/packages/l1-workspace-wiki-ui_v0_1_0_1119.zip`
- size 267140 bytes / SHA-256 `411553e74e76bb82237fd2ebef65169769e4dbe4cfd2231afb5afd38559b10a9`
- 소스: `collab/projects/L1-WORKSPACE-RAG-20261111-001/ui/viewer-wiki-ui_v0_1_0/`
- 압축 해제 루트: `viewer-wiki-ui/`, 23개 파일. manifest는 자기 자신 제외 22개.
- 이 입력은 GPT가 구현·자체시험한 **합성 독립 데모**, 실제 업무 Linux 화면·데이터·설치본 아님. 실제 공동 사용자 수락은 아직 미검증.

### 먼저 볼 자료와 순서

1. `screenshots/wiki-1440.jpg`, `screenshots/wiki-390.jpg`, `screenshots/wiki-320.jpg`, `screenshots/msc-12.jpg`를 **이미지로 직접 열어** 시각 평가. 코드를 읽은 것만으로 VISUAL_INSPECTION=PASS를 쓰지 말 것.
2. `index.html`, `assets/style.css`, `assets/app.js`에서 관찰한 화면의 원인·최소 수정 지점을 확인. 필요 시 `L1_Workspace_Wiki_UI_v0_1_0_20261119_KST.html`은 승인된 정적·격리 브라우저 표시만 허용. ZIP의 Python/JS 테스트·빌드 스크립트/서버는 실행하지 않음(STATIC_ONLY).
3. `DESIGN.md`, `TEST_REPORT.md`는 설계 의도와 자체시험 한계 확인용. 자체시험 PASS 56/56·정적 19/19를 독립 시각 수락으로 재진술하지 말 것.
4. `fixtures/demo-data.js`는 화면 상태·문서 밀도·긴 제목/표의 예시 범위를 판단할 때만 참고. 전체 과거 Work/스킬·정책 감사를 반복하지 않음.

## 핵심 검토 4축

| 축 | 사용자 관점의 질문 | 확인할 구체 항목 |
|---|---|---|
| 화면 구성 | 처음 보는 동료가 위치·현재 문서·다음 탐색을 쉽게 찾는가? | Work/Knowledge/전체 파일 구분, M→F→S/Procedure, 선택 상태, 트리 깊이, breadcrumb, 중앙/우측 역할, 중요 버튼 우선순위, 모바일 본문 우선 |
| 가독성 | 긴 기술 문서를 오래 읽고 필요한 근거를 찾기 편한가? | 제목/H2/H3 위계, 본문 폭·글자·줄간격, 표/코드/경로, 메타·상태·보조 글자 크기/대비, 내용 밀도·공백·한국어 줄바꿈, 320px 가림/내부 스크롤 |
| 화면 스타일 | 여러 담당자가 계속 쓰는 업무 위키에 맞게 모던하고 일관적인가? | 색·아이콘·버튼·여백·배지·선택 강조의 일관성, 장식/색의 과다·부족, 기본/선택/hover/focus의 구별, 장시간 사용 시 피로 |
| 사용자 시인성·사용성 | 중요한 문서·상태·행동이 바로 눈에 들어오고 오해 없이 쓰이는가? | PREVIEW/DRAFT/PUBLISHED 예시/미확인 구분, 버튼 발견성, 원문/본문·검색·뒤로가기, 모바일 닫기/목차·초점, 읽기 전용 인지, 색에만 의존하지 않는 의미 전달 |

### 실제 작업을 가정한 보조 검토

- 새로운 동료가 Work에서 문제·원인·해결을 읽고 관련 MSC로 넘어가는 흐름.
- Knowledge에서 Module→Feature→Scenario를 찾고 Work/Evidence·Procedure로 이동하는 흐름.
- 1440px PC와 390/320px에서 긴 제목·보조 메타·표·코드·목차가 보이는 방식.
- 6/12명 MSC의 확대·폭 맞춤·접기·복귀 버튼이 찾아지며, placeholder와 실제 기술 정본을 혼동하지 않는지.
- 문서가 늘거나 실제 문구가 길어지면 현재 트리·레이아웃에서 혼란/가림이 생길 구체적 반례. 실제 큰 데이터 성능은 정적 이미지로 판정하지 않음.

## 결과 계약

한국어로 다음 순서의 간결한 독립 리뷰를 제출:

1. `REVIEW_STATUS`, `REVIEW_KIND=INDEPENDENT_VISUAL_UX`, 고정 request/revision/ZIP SHA, **VISUAL_INSPECTION=PASS/PARTIAL/NOT_RUN**, 실제로 열어 본 이미지 목록, 브라우저 사용 여부와 미검증 범위.
2. 전체 판정 `ACCEPT / ACCEPT_WITH_CHANGE / REVISE / PARTIAL_SCOPE`. **업무 GPT 전달 전 필수 보완 여부**를 별도로 제시. 기존 Linux 운영/공유 승인 PASS와 구분.
3. 4축별 10점 평가 + 짧은 근거, 유지할 장점. 이미지를 실제로 보지 못했으면 시각 점수는 `N/A`.
4. 확인된 문제는 **화면/viewport·사용자 영향·근거 위치·Severity·최소 수정안·확인 방법** 표로 보고. 코드 근거가 있으면 CSS selector/값이나 파일 위치를 제시. P0 전달 전 필수/P1 우선 개선/P2 선택 개선을 구분하되 결함 개수를 강제하지 않음.
5. 가장 효과가 큰 개선 순서와 기대 효과·변경 비용. 필요할 때만 대안을 비교하고 전체 재개발/새 프레임워크를 기본 해법으로 삼지 않음. 근거 없는 취향은 확정 결함과 분리.
6. 실제 사용자 관찰·실기기·브라우저 상호작용·접근성 미검증은 명시. 정적 이미지로 실제 5초 인지·완료 시간·클릭 수·스크린리더·성능을 PASS로 단정하지 않음.

결함이 없으면 없다고 보고. 비판적 검토는 하되 반대 결론이나 최소 지적 수를 강제하지 않음. 56개 자체시험 PASS가 사용자의 시인성 만족을 보장하지 않는지 독립적으로 판단해 주세요.

## 범위·실행 경계

- 검토 대상은 **이 UI 완성본의 화면/스타일/사용성**. 기존 Updater/Workflow/Kernel·RAG·자동 승인 엔진·운영 설치를 다시 설계하는 리뷰가 아님.
- 기존 B1 경로 containment/B2 파일내용 비밀 검사/B3 MSC origin 격리는 미해결 호스트 게이트로 보존. 이 시각 리뷰에서 해결/PASS로 변경하지 않음.
- 이미지 읽기 기능이 없으면 `VISUAL_INSPECTION=NOT_RUN / PARTIAL_SCOPE`. 이미지 없는 CSS 추론을 시각 리뷰 완료로 대체하지 않음. 승인되지 않은 추가 모델/Agent 호출·외부 이미지 전송 금지.
- `max_model_calls=1`, 최대 USD 3, 출력 목표 약 3500 tokens. 사용자 요청 1회→독립 리뷰 1회→GPT 판정 1사이클. 과금/실행 불확실 시 임의 재큐잉 없음.
- 실제 호스트/인증·키/위임·LIVE/Notifier/DB·PUBLIC 게시·원본 코드/Knowledge/Work/Evidence 쓰기·업무 GPT 전달은 이 리뷰로 시작하지 않음.
