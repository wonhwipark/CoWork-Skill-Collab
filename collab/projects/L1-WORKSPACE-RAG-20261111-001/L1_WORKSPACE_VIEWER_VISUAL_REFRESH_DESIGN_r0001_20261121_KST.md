# L1 Workspace Viewer — 동료용 색상·가독성 개선 설계 R1

- Version: r0001 / 2026-11-21 KST
- Existing Work: `L1-WORKSPACE-RAG-20261111-001`
- Purpose: 기존 위키 UI의 보라색/데모 분위기를 차분한 팀 기술문서 도구로 정리. **동작·원본·호스트 설치는 변경하지 않는 독립 정적 설계 리뷰 입력**
- Baseline: `ui/viewer-wiki-ui_v0_1_0/assets/style.css` Git blob `5d3e1e88b5ff3553ea94f745cd52c431457ca2e3`, 기존 screenshots `wiki-1440.jpg` / `wiki-390.jpg`; 기존 UI v0.1.0 ZIP 267140B/SHA-256 `411553e74e76bb82237fd2ebef65169769e4dbe4cfd2231afb5afd38559b10a9`.
- 1st phase work-title prebuild v0.1.1 candidate SHA-256 `20e635802b3480c5b3c9888e3599316e158ee0aa0c50deeac6b53098459ce9f8`; standalone candidate, **real v0.1.0 integration NOT_RUN**.
- Preview: `VIEWER_STYLE_A_B_COMPARISON_r0001_20261121_KST.html`, synthetic static HTML; actual Viewer runtime and Linux screenshots NOT_VERIFIED.

## 1. 사용자 요구·변경 불가

1. 현재 Viewer가 전체 로그인 없이 Read Only로 운영되는 것은 **사용자 결정**. 동료의 첫 접속·Work 검색·문서·MSC 열람에 ID/PW를 요구하지 않는다. 2차 [수정] 때만 편집 인증하는 별도 기능이며 **이번 1차 시각 리뷰 범위 밖**.
2. 현재 좌측 Work/Knowledge 트리·중앙 본문·우측 목차, 문서/MSC handler·검색·deep link·모바일 드로어를 유지한다. 새 서비스·프레임워크·DB·AI 챗 UI 만들지 않는다.
3. 검증된 대표 이슈번호(예: `SOC-1234`)가 있으면 **표시 제목 맨 앞**, 이어 Module/제목·설명. 제목에 중복된 번호 제거, 대표 번호가 없는 경우 안전 폴백. 실제 Work ID·폴더·링크·Evidence·원본 SHA는 **절대 변경하지 않고 보조 행에서 ID 제공**. 번호/제목을 임의 추정하지 않는다.
4. 보안 B1(경로 containment), B2(title/search/raw/download/cache 제한정보), B3(별도 origin MSC 격리) 및 실제 Linux E3/E4 게이트는 아직 미검증이며 시각 디자인 검토로 해제되지 않는다.
5. 합성 `PUBLISHED`, `fixture-r1`, `합성 데모` 등을 실제 업무 사실로 바꾸지 않는다. 운영에서는 원본 확인된 상태만 표시하되 source/provider 연동 완료 전 해당 요소를 숨기거나 '미확인'으로 다룬다.

## 2. 원본 CSS 관측과 변경 제안

현재 CSS `--purple:#5145cd`, `--purple-soft:#eeecff`, `--ink:#202739`, `--muted:#606b7e`, `--line:#e7eaf0`, `--soft:#f6f7fb`. 선택된 Work 탭/링크/로고/TOC에 보라색이 반복되고, 일부 9~11px 메타/보조 문자열·연보라 배경이 업무용 위키보다 프로토타입을 연상시킬 수 있다. 넓은 흰 독서 공간, 3단 구조, 표/코드/MSC 탐색은 유지할 가치가 크다.

**추천 A — Blue Gray / 공통 색상 토큰 (색상은 디자인 후보이며 실제 코드 반영 전 리뷰 판정 필요)**

| 의미 | A안 | 구현·검증 주의 |
|---|---|---|
| 기본 강조, 링크, 선택 상태 | `#1E40AF` | 기존 보라색 selector 좁게 변경, 활성 메뉴에 3px 선/aria-current 등 색 외 차별 |
| 활성 배경 | `#EFF6FF` | 텍스트 대비 유지 |
| 탐색 패널 | `#F8FAFC` | 본문 백색과 명확한 구조 분리 |
| 본문·제목 | `#334155` / `#1E293B` | 16px 본문·22px H2·17px H3 유지 |
| 테두리 | `#E2E8F0` | 카드/테두리 과장·그림자 축소 |
| 보조 텍스트 | `#475569` | 저대비 `#8D97A7` 등 교정, 12px 이상 우선 |
| 브랜드 | slate 계열 단순 L1 표식·`L1 Workspace` | TEAM KNOWLEDGE·원형 avatar 등 장식 단순화, 링크 기능 보존 |
| Badge / 상태 | 중립 Slate + 실제 의미 있을 때 상태색 | 'AI 생성/합성'과 실제 검증·공유 상태 혼동 금지 |

대안 B — Slate monochrome: 더 절제되지만 선택 상태·링크의 발견성이 약해질 수 있어 평가용 비교 대안으로만 유지. 웹폰트/CDN, 무관한 애니메이션/그라디언트 추가 금지.

**대상 기존 CSS 선택자:** `:root`, `.brand-mark`, `.view-nav button[aria-current="page"]`, `.tree-row:has(a[aria-current="page"])`, `.eyebrow`, `#toc a.active`, `:focus-visible`, `.badge`, `.sidebar`, `.metadata`. 이미 진행 중인 UX R1 P1 항목 (12 participant MSC overflow 방향 힌트 및 CSS Readability override 충돌 정리)과 순서/중복을 확인하고 함께 최소 변경.

## 3. 1차 구현과의 연결·수락 기준

- 제목 표시: 목록/검색 결과/breadcrumb/현재 문서 제목은 같은 formatter. **가상** `SOC-1234 — NR L1 Tx — UL Tx Switching 분석` + `Work ID: DEMO-TX-001` 같은 두 단계 위계. 실제 번호가 없으면 검증된 title/module만, 그것도 없으면 ID 그대로. 원본 경로 rename/metadata DB 추가 0.
- 읽기 흐름: 로그인 없는 열람·키보드/모바일 탐색·주소/검색·탭/스크롤 복귀를 보존. 소스가 일부 fixture 직접 참조하고 CSS 데모 CSP는 `connect-src none/frame-src none`이므로 실제 Linux G0에서 adapter/handler 재사용을 먼저 확인.
- 대비: 일반 텍스트 AA **4.5:1 이상**, 큰 글자 **3:1 이상**, 아이콘/선택/포커스 대비·색상 비의존 표시. 기존 `#8D97A7`의 흰색 대비 약 **2.95:1**로 우려; 실제 화면과 computed style에서는 해당 요소에 대해 재검증.
- 화면: 1440/720/390/320 CSS px, 200% reflow, 키보드 focus, 워크 이름 1~4줄 줄바꿈, 긴 SOC 번호, 표/코드/MSC 6/12 participant, WCAG/색각, 최소 이동/최대화의 회귀 비교.
- **G0 미확인:** 실제 Linux Viewer 소스·revision·현재 CSS/프레임워크·renderer·Work issue/title API와 B1/B2/B3/E3/E4. 따라서 이 리뷰가 PASS여도 실서비스 배포 승인은 아니다.

## 4. Windows Claude Code 독립 R1에 요청할 판단

1. **A vs 기존 vs B**: 과연 A가 팀 엔지니어링 문서 화면에 적합한지, 현 디자인에서 유지할 강점과 바꿔야 할 최소 변경 경계는?
2. 색상 토큰·브랜드·상태 표현의 **실제 부작용**(링크/focus/selected 색 구별, 대비, 기존 CSS override·MSC 힌트 충돌, 320px 가독성)은?
3. `SOC-xxx` 앞번호·Work ID 보조, 동일 formatter가 탐색 구조를 읽기 쉽게 하는가? 대표번호 없는 Work·길고 중복된 title·모바일 반례는?
4. 별도 Viewer 읽기 서비스·기존 handler·B1/B2/B3 권한을 유지하면서 UX만 개선할 수 있는 최소 구현 순서는? 스킬 일괄 변경이 불필요하다는 판단에 반례는?
5. 리뷰 범위/검증 불확실성: 정적 합성 HTML을 **실제 Linux UI 시험/운영 승인**으로 혼동시키는 근거 없는 PASS 주장은 없는가? 예상 PC/mobile 시험을 구체화해 달라.
6. R1 결론은 `ACCEPT/ACCEPT_WITH_CHANGE/REVISE/HOLD`, 발견 사항별 **BLOCKING/MAJOR/MINOR**·해당 설계 절·사용자 영향·최소 수정·검증법·G0 추가 확인 한 행동. 지적 개수 강제 금지.

**리뷰는 이번 스타일 R1 한 건만.** 기존 Viewer 설계/편집/UX 완료 리뷰 재실행 0. 실제 2차 인증/편집 구현, 운영 배포, 스킬 수정, PUBLIC 업로드, 회사 자료/계정/토큰/실제 MSC 열람 금지. 유료 모델 1회 이내, 실제 보호된 정책/유효 승인·서명·READY 충족 때만 실행.

## 5. 후속 단계(리뷰 결과 도착 후)

GPT가 같은 PRIVATE Work에서 리뷰 결과·영수증을 원격 확인하고 지적을 수용/수정 수용/거절/보류 판정 → 1차 전용 CSS/레이블 통합 후보를 기존 v0.1.0+v0.1.1에 적용→ 자체시험/브라우저 캡처→ 수정된 candidate ZIP·SHA→ 실제 Linux G0/승인·B1~B3/E3/E4에 따라서 배포 판단. **이번 R1 요청 게시만으로 이 후속 구현/배포를 시작하지 않음.**
