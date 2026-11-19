---
schema: SKILL_COLLAB_REVIEW_RESULT_V1
review_id: "REQ-L1-WORKSPACE-WIKI-UI-UX-R1-20261119|1|411553e74e76bb82237fd2ebef65169769e4dbe4cfd2231afb5afd38559b10a9|1"
responds_to_request_id: "REQ-L1-WORKSPACE-WIKI-UI-UX-R1-20261119"
responds_to_request_revision: "1"
package_sha256: "411553e74e76bb82237fd2ebef65169769e4dbe4cfd2231afb5afd38559b10a9"
skill_id: "l1-knowledge-updater"
run_policy_ref: "POLICY-STATIC-V1-DESIGN"
knowledge_refs: []
consumer_profiles: ["l1-workspace-wiki-ui-visual-ux-review"]
reviewer_os: WINDOWS
review_scope: CODE_REVIEW
test_policy: "STATIC_ONLY"
execution_status: COMPLETED
limitations: ["static review by an automatically started Claude Code process; no package code was executed", "knowledge files were delivered as the REQUEST pinned them; which parts were actually read is reported by the reviewer in the text", "reviewer host is Windows; Linux, in-house LLM and MCP behaviour are not verified by this review"]
---

# 리뷰 결과

# REQ-L1-WORKSPACE-WIKI-UI-UX-R1-20261119 독립 시각 리뷰

## 1. 상태

- `REVIEW_STATUS=COMPLETE`
- `REVIEW_KIND=INDEPENDENT_VISUAL_UX`
- `request_id=REQ-L1-WORKSPACE-WIKI-UI-UX-R1-20261119` / `revision=1`
- `package_sha256=411553e74e76bb82237fd2ebef65169769e4dbe4cfd2231afb5afd38559b10a9` (REQUEST 명시값, 재해시 안 함 — watcher가 이미 검증했다는 전제를 그대로 수용)
- `VISUAL_INSPECTION=PASS`
- 실제로 이미지 도구로 직접 연 파일: `screenshots/wiki-1440.jpg`, `screenshots/wiki-390.jpg`, `screenshots/wiki-320.jpg`, `screenshots/msc-12.jpg` (4개 전부)
- 브라우저 사용: **안 함**. 정적 이미지 뷰어로만 검사했고 `L1_Workspace_Wiki_UI_v0_1_0_20261119_KST.html`도 열지 않았습니다. 코드(`index.html`, `assets/style.css`, `assets/app.js`, `fixtures/demo-data.js`)는 텍스트로만 읽었습니다.
- 미검증 범위: 실제 클릭/키보드 상호작용, 포커스 이동, 줌/폭맞춤 버튼의 실제 동작, 스크린리더, 실기기, 색 대비 수치 측정(육안 판단만).

## 2. 전체 판정

- **ACCEPT_WITH_CHANGE**
- **업무 GPT 전달 전 필수 보완: 있음 (P0 아님, P1 2건)** — 전달 자체를 막을 정도의 결함은 못 찾았지만, 전달 전에 고치는 편이 싼 항목이 있습니다.
- 이 판정은 정적 이미지 4장 + 코드 열람 기준이며, TEST_REPORT.md의 "PASS 56/56·정적 19/19"는 개발자 자체시험이지 이 리뷰가 재확인한 것이 아닙니다. 기존 Linux 운영/공유 승인 PASS와는 무관하며, B1/B2/B3 호스트 게이트는 이 리뷰로 해결되지 않았습니다(요청에서 지시한 대로 보존).

## 3. 4축 평가

| 축 | 점수 | 근거 |
|---|---|---|
| 화면 구성 | 8/10 | Work/Knowledge/전체 파일 탭, breadcrumb, 트리 선택 강조(`.tree-row:has(a[aria-current="page"])`), 중앙/우측 역할 분리가 1440px에서 명확함(`wiki-1440.jpg`). 모바일은 본문 우선 + 드로어로 전환(`index.html:20,28,52`, CSS `@media(max-width:760px)`). 트리 깊이 3단계(Work>NR L1 Tx>DEMO-TX-001>문서)까지는 들여쓰기(`tree-level .tree-level{margin-left:15px}`)로 구분되나, 4단계 이상이 되면 258px 사이드바 폭에서 가독성이 빠르게 나빠질 구조.
| 가독성 | 8/10 | 본문 16px/줄간격 1.75 적용 확인(`style.css` 12행 "Readability baseline"), H2 22px/H3 17px 위계 뚜렷, 표/코드 블록은 자체 스크롤 영역(`.table-scroll`, `.prose pre`)로 본문 레이아웃 붕괴 방지. 다만 메타 정보(byline, metadata dd)가 11~12px로 매우 작아 보조 정보 다수가 밀집(`wiki-1440.jpg` 우측 "문서 정보" 영역).
| 화면 스타일 | 8/10 | 보라 강조색 하나로 선택/링크/버튼을 일관되게 사용, 장식 최소화. PREVIEW 배지는 색+점+텍스트 조합이라 색맹에도 읽힘(`badge:before`, `states` 객체 — `assets/app.js:24`). 과도한 카드형 장식 없이 문서 위계 중심이라 장시간 사용 피로가 낮을 것으로 보임.
| 사용자 시인성·사용성 | 7/10 | PREVIEW/미확인 라벨이 텍스트로 명시돼 색 의존이 아님. MSC 12명 화면에서 확대/축소/폭맞춤 버튼은 잘 보이나(`msc-12.jpg`), 우측 끝 레인이 안내 없이 잘려 보여 "더 있다"는 신호가 약함(§4-1).

유지할 장점: 상태 배지의 텍스트+색 병기, 본문/탐색/메타의 타이포 위계, 모바일에서 본문 우선 배치, MSC 화면의 원본-아님 안내 문구(`msc-notice`)가 명확함.

## 4. 문제 목록

| # | 화면/viewport | 사용자 영향 | 근거 위치 | Severity | 최소 수정안 | 확인 방법 |
|---|---|---|---|---|---|---|
| 1 | MSC 12명, 1440px (`msc-12.jpg`) | 레인이 7개째 "확장 A"에서 안내 없이 잘려 보임. `.msc-scroll{overflow:auto}`(`style.css`)로 스크롤은 가능하나 스크린샷상 스크롤바/페이드 신호가 없어, 처음 보는 동료가 숨은 참가자가 더 있다는 걸 못 알아챌 수 있음 | `assets/style.css` `.msc-scroll` 규칙, `screenshots/msc-12.jpg` 우측 끝 | P1 | `.msc-scroll` 우측에 `mask-image`/그라데이션 페이드 또는 "→ 더 보기 N명" 텍스트 힌트 추가 | 12명 fixture를 열고 컨테이너 우측 끝에서 시각적 "더 있음" 신호가 보이는지 재확인 |
| 2 | `assets/style.css` 전체 (코드 레벨, 화면엔 안 보임) | 당장 사용자 영향은 없으나 유지보수 리스크. 11행 "Readability baseline" 주석 이후의 비-미디어쿼리 override 블록(12행)이 그 앞에 먼저 쓰인 `@media(max-width:1180/1040/760/360px)`(3~10행)의 동일 선택자·속성을 specificity 동률로 무조건 덮어씀. 이후 13~16행에서 같은 브레이크포인트를 다시 열어 재보정하는 이중 레이어 구조. 지금 스크린샷 결과는 일관돼 보이지만, 앞으로 누군가 3~10행의 옛 미디어쿼리만 고치면 효과가 전혀 반영되지 않는 "조용한 무효화" 함정이 있음 | `assets/style.css` 1~16행 (예: `.prose` 가 7행 `font-size:13px`로 설정됐다가 12행에서 무조건 `16px`로 재정의되어 7행 규칙이 사실상 죽은 코드) | P1 | 두 레이어를 병합해 브레이크포인트별로 한 번만 선언(디자인 토큰 하나로 정리), 또는 최소한 "line X의 규칙은 line Y가 덮어쓰므로 편집 금지" 주석 추가 | CSS를 브레이크포인트별로 재구성한 뒤 1440/390/320 스크린샷을 다시 비교해 값이 바뀌지 않는지 확인 |
| 3 | 320px 문서 메타 (`wiki-320.jpg`) | byline(예시·담당A·날짜·합성예시·읽기전용)과 배지 줄이 좁은 폭에서 2줄 이상으로 밀집해 첫 화면 스캔 시 정보 과밀감이 있음. 치명적이진 않음 | `assets/style.css` `.doc-byline{flex-wrap:wrap}` 관련 `@media(max-width:360px)` 블록, `wiki-320.jpg` 상단 | P2 | 320px 전용으로 byline 항목 중 "읽기 전용"을 배지/아이콘 하나로 축약하거나 `·` 구분자 간격을 줄임 | 320px로 다시 캡처해 byline이 1줄 또는 보기 좋은 2줄로 줄었는지 확인 |
| 4 | 사이드바 트리 깊이 (코드 추론, 실제 화면엔 3단계만 보임) | fixture는 3~4단계지만, Module→Feature→Scenario/Procedure처럼 더 깊은 Knowledge 트리가 늘어나면 258px 폭(`--sidebar:258px`)에서 들여쓰기(`margin-left:15px` 누적)가 겹쳐 텍스트 폭이 급격히 줄 수 있음. 스크린샷으로는 재현되지 않아 반례 추정만 가능 | `assets/style.css` `.tree-level .tree-level{margin-left:15px;padding-left:10px}` | P2 | 일정 깊이(예: 4단계) 이상에서 들여쓰기 증가를 멈추거나 가로 스크롤 허용 | 실제 Knowledge M→F→S 깊이의 긴 제목으로 fixture를 늘려 320/1440에서 재캡처 |

P0(전달 전 필수)는 없음. 위 1,2번은 P1로 전달 전 처리를 권장하되, 전달 자체를 막을 수준은 아닙니다.

## 5. 개선 우선순위 (효과 대비 비용)

1. **MSC 스크롤 신호 추가(#1)** — CSS 몇 줄로 끝나는 변경 대비, "참가자가 더 있는데 못 봤다"는 가장 흔한 오해를 막아 효과가 큼.
2. **CSS 이중 레이어 정리(#2)** — 지금 당장 화면엔 안 보이지만, 다음 반복에서 누군가 옛 미디어쿼리를 고치고도 반영이 안 되는 상황을 막아 장기 유지보수 비용을 줄임. 전체 재작성이 아니라 중복 선택자 병합 수준.
3. **320px byline 압축(#3)**, **깊은 트리 대비(#4)**는 선택 개선으로, 현재 fixture 범위에선 급하지 않음.

전체 재구현/새 프레임워크는 필요하지 않다고 판단합니다. 근거 없는 취향(예: 보라색 대신 다른 색, 폰트 선호 등)은 결함으로 보고하지 않았습니다.

## 6. 명시적 미검증

- 실제 클릭/키보드/포커스 이동, Esc 닫기, 줌·폭맞춤 버튼의 실제 동작 — TEST_REPORT.md의 자체시험 주장일 뿐 제가 재현하지 않음.
- 5초 인지, 완료 시간, 클릭 수 — 정적 이미지로 측정 불가, PASS로 단정하지 않음.
- 색 대비 수치(4.5:1 등) — 육안 판단만 했고 계산 도구로 측정하지 않음.
- 스크린리더, 실기기, 터치, Firefox/Safari — TEST_REPORT.md도 NOT_RUN으로 명시, 이 리뷰에서도 NOT_RUN.
- `L1_Workspace_Wiki_UI_v0_1_0_20261119_KST.html` 정적 브라우저 렌더링은 열람하지 않음(스크린샷 4장만으로 충분하다고 판단).
- Windows 리뷰이므로 Linux 실제 운영 화면과의 동일성은 검증 불가.

## 7. 기록

- **읽은 지식 파일**: 없음 (이 REQUEST에 pinned knowledge 없음)
- **대상 소비자 프로필**: `l1-workspace-wiki-ui-visual-ux-review`
- **공통 지식 수정 제안**: 없음. 다만 GPT 판단용 참고: `TEST_REPORT.md`의 "PASS 56/56"이 독립 시각 수락을 보장하지 않는다는 REQUEST의 우려는 타당했고, 실제로 코드 레벨(#2)과 MSC 스크롤 신호(#1)에서 자체시험이 못 잡는 문제를 발견했습니다. 이는 향후 "자체 Chromium 시험 PASS"와 "독립 시각 리뷰 PASS"를 분리 기록하는 현재 관행이 유효함을 재확인하는 선례로 남기면 좋겠습니다.
