# 팀 위키형 UI 설계 · v0.1.0

2026-11-19 KST · 합성 프런트엔드 구현 설계

## 1. 사용자와 읽기 흐름

공동 담당자가 문서 제목과 현재 상태를 먼저 파악하고, 왼쪽 계층에서 관련 업무·지식을 찾으며, 중앙 문서를 읽고 오른쪽 목차와 근거를 확인하는 구조예요. 팀 위키의 일반적인 정보구조를 독자 구현했어요.

| 영역 | 표시·동작 | 목적 |
|---|---|---|
| 상단 | 제품명, fixture 검색, 합성 데모 표기 | 위치·데이터 범위 인지 |
| 왼쪽 | Work / Knowledge / 전체 파일, 계층 펼침·접기, 현재 문서 강조 | 기존 전체 파일 접근과 지식 분류 동시 유지 |
| 중앙 | 실제 제목, 짧은 설명, 상태, 문서·원문, 관련 문서 | 독서와 다음 탐색 연결 |
| 오른쪽 | H2/H3 목차, Work·Evidence·경로·revision·미확인 | 읽는 중 근거 확인 |
| 모바일 | 본문 우선, 좌우 드로어, 닫기·Esc·초점 복귀 | 좁은 화면에서도 동일 본문 크기 유지 |
| MSC | 넓은 단일 본문, 합성 6/12명, 확대·폭맞춤·설명 접기·복귀 | 실제 B형 HTML 연동 전 레이아웃 검증 |

브라우저 hash route는 `#/work/<doc-id>`, `#/knowledge/<doc-id>`, `#/files/<doc-id>`예요. 목차는 `?section=section-N`으로 공유·재열람할 수 있어요. 상대 파일 경로를 URL에 직접 결합하지 않아요.

## 2. 시각 체계

- 흰색 독서 화면, 옅은 회색 탐색 영역, 보라색 선택 강조. 과도한 카드·요약 숫자 대신 문서 위계에 집중.
- 본문 16px·줄 간격 1.75, H1 약 25~34px, H2 22px, H3 17px. 보조 메타는 11~12px, 핵심 메뉴는 14px. 설치 호스트에 있는 시스템 한글 글꼴 사용.
- 본문 열 최대 960px, 데스크톱에서 좌측 약 258px·우측 정보 약 205px. 좁아지면 우측부터 드로어로 전환.
- 표·코드·MSC는 자체 영역만 스크롤. 문서 제목·메타 경로는 줄바꿈.
- PREVIEW·DRAFT·PUBLISHED·미확인은 텍스트와 색을 함께 사용. 알 수 없는 입력은 항상 미확인.
- PUBLISHED fixture는 반드시 `PUBLISHED · 예시`로 표시. 실제 서비스에서는 업무 GPT가 검증된 게시 상태·고정 revision을 확인한 후 표현을 매핑해야 해요.

## 3. 코드 경계

`fixtures/demo-data.js` → `adapters/adapter.js` → `assets/app.js` → DOM.

adapter의 반환 객체는 UI용 임시 DTO예요. 실제 원장·메타데이터 스키마·API를 정의하지 않아요. 상태 관리·저장·게시 책임은 기존 Knowledge Updater/Workflow/Kernel에 있어요. Viewer에는 writer·DB·동기화 엔진이 없어요.

| 파일 | 책임 |
|---|---|
| index.html | 의미 있는 영역, 버튼·대화상자·ARIA, CSP |
| assets/style.css | 위키형 레이아웃·반응형·초점·인쇄 스타일 |
| assets/app.js | 읽기 탐색·검색·메타·목차·현재 route·오류/로딩/빈 상태 |
| assets/markdown.js | 데모용 제한 Markdown의 안전한 DOM 생성 |
| adapters/adapter.js | 합성 읽기 메서드·명시된 capability |
| fixtures/demo-data.js | 합성 13문서·3종 탐색 트리 |

이 데모의 Markdown은 H1~H3·리스트·인용·표·코드·강조·`doc:` 링크만 처리해요. 임의 HTML은 문자로 표시하고 일반 URL은 차단해요. 이미지·PDF·SVG·CSV 등은 현장 기존 renderer/handler 연결 대상이며, 이 구현에서 지원 완료로 표시하지 않아요. JSON은 textContent로 렌더, 바이너리는 미지원 안내를 표시해요.

## 4. 보안·접근성

DOM은 createElement/textContent로 만들며 원문·제목·메타를 innerHTML로 넣지 않아요. 문서 ID는 adapter로 조회하며 파일시스템 경로로 사용하지 않아요. 기본 CSP는 connect-src/frame-src/object-src를 none으로 제한해요. 외부 CDN·서체·데이터 호출은 없어요.

실제 MSC URL/iframe을 활성화하는 코드는 없어요. `getMscTarget()`이 반환하는 URL을 자동으로 열지 않으며, 합성 placeholder만 허용해요. 기존 doc-converter의 참가자 의미·원문·변환 규칙은 재구현하지 않아요. 데모 SVG는 위치·확대 시험용이며 실제 MSC renderer 대체물이 아니에요.

모바일 드로어의 초점 진입/순환/복귀, 검색 dialog의 기본 초점 관리, skip link, 명시적 버튼 이름, 표·코드 스크롤 영역, reduced-motion을 지원해요. 색 대비 전체 인증·스크린리더 실기·OS 고대비·실기기 터치 검증은 NOT_RUN이에요.

기존 독립 설계 리뷰의 B1 경로 canonicalization·symlink/TOCTOU, B2 파일내용의 비밀·제한자료 검사, B3 MSC 별도 origin·쿠키·sandbox·CSP는 서버 책임이며 **실제 호스트에서 미해결 BLOCKING**으로 유지해요. 이 프런트엔드의 합성 XSS 시험은 이 서버 게이트를 해결한 근거가 아니에요.

## 5. 범위 판정

합성 데모의 UX 구현은 COMPLETE. 실제 Linux API·서비스 revision·동료 계정·권한·접속·성능은 미확인. 실제 사용자 5초 인지·3회 이내 MSC 접근의 수락은 현장 관찰로 확인해요. 독립 코드 리뷰·호스트 설치·운영 전환·그룹 게시를 UI 완성에서 추론하지 않아요.
