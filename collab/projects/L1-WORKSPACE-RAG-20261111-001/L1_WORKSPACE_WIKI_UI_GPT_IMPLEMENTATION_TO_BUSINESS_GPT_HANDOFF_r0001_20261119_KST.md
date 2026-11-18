# L1 Workspace — 2안 팀 위키형 UI: GPT 프런트엔드 구현 → 업무 GPT 현장 연동 핸드오프 r0001

- 작성: 2026-11-19 KST
- 정본: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`
- 기존 Work: `L1-WORKSPACE-RAG-20261111-001`; 본 문서는 같은 Work의 후속 **작업 지시·설계 기준**이며 신규 Work/운영 승인 아님.
- **최신 사용자 결정 (우선):** 이전 GPT 잠정안 ‘B안: Work 중심 홈 → 독서 화면’보다, 사용자 직접 선택한 **상용 팀 위키 패턴 4종 중 ‘2안 — Confluence 계열 팀 위키형’**을 UI 기준으로 삼는다. Confluence의 상표·에셋/코드를 복제하지 않고 일반적인 정보구조만 차용.
- **작업 방식 (최신):** GPT가 설계만 전달하는 방식 대신, **설계 + 실제 작동하는 독립 HTML/CSS/JavaScript UI 구현 + 테스트 + 통합 가이드**까지 제작. 업무 GPT는 실제 Linux의 별도 L1 Workspace Viewer 서비스와 원본/권한/API를 조사하여 기존 서비스에 최소 변경으로 적용한다. 업무용 저사양 LLM/Agent는 처음부터 UI를 설계·재개발하지 않고 **연동·필요 보완·현장시험**에 집중.
- **별도 서비스 근거:** 사용자가 2026-11-19 대화에서 현재 웹 뷰어는 업무용 Linux PC에 구현된 **별도 서비스**라고 직접 명시. OpenCode Web의 하위 UI로 간주하거나 새 호스트 서비스 설치를 기본 요구하지 않는다. 단 실제 설치본 소스/서비스 이름/프레임워크/API/revision/보안 구성은 여기에서 직접 접근 검증한 것이 아니므로 `HOST_SERVICE_FACT=USER_CONFIRMED`, `HOST_SOURCE/REVISION/API=NOT_VERIFIED`.
- **현재 단계:** `HANDOFF_DESIGN=POSTED`; `FRONTEND_CODE_PACKAGE=NOT_BUILT`; `FRONTEND_BROWSER_TEST=NOT_RUN`; `HOST_INTEGRATION/INSTALL/SHARING=NOT_RUN`. 새 창은 이 문서로 구현을 **시작**할 것. 다른 문서의 과거 “UX 논의 대기”·구 B안 잠정 추천보다 최신 사용자 확정 지시를 우선.

## 1. 새 창 재개 순서

1. PRIVATE `collab/CONTEXT_BRIEF.md` → `collab/projects/L1-WORKSPACE-RAG-20261111-001/CURRENT.md` 상단 현재 요약 → **이 인계**를 읽는다.
2. 필요 근거만 추가: 동일 Work의 `L1_WORKSPACE_FULL_TREE_WEB_RENDER_VIEWER_DESIGN_DELTA_r0002_20261118_KST.md`, `L1_WORKSPACE_VIEWER_PERSONAL_KNOWLEDGE_TOBE_DELTA_r0003_20261118_KST.md`, `L1_WORKSPACE_KNOWLEDGE_UPDATER_OWNERSHIP_AND_VIEWER_UX_DELTA_r0004_20261118_KST.md`, `VIEWER_R0004_UX_READABILITY_PROPOSAL_r0001_20261119_KST.md`. 원본은 수정하지 않고 변경 델타로 연결.
3. **중복 확인:** 기존 r0002 Claude R1 `REQ-L1-WORKSPACE-LOCAL-VIEWER-DESIGN-R1-20261118`는 `COMPLETED/ACCEPT_WITH_CHANGE` (BLOCKING B1~B3). r0004 델타 리뷰 후보 `REQ-L1-WORKSPACE-VIEWER-UX-OWNER-R1-20261119`는 마지막 확인 기준 사전자료만 게시, **정식 REQUEST/서명/READY 미게시·유료 독립 리뷰 NOT_RUN**. 신규 리뷰의 실제 상태와 최신 유효 승인 여부는 해당 CURRENT/요청 경로로 재확인. 완료된 R1 재큐잉/재과금 금지. 새 유료 리뷰가 불가해도 **허용된 UI 개발과 시험은 진행**.
4. GPT가 아래의 **독립 프런트엔드**를 만들어 실제 브라우저 시험한 후, 결과/미검증/소스 revision/SHA-256을 같은 Work에 게시. 사용자가 최종 파일을 요청할 경우 사용 가능한 ZIP 다운로드 링크도 제공.
5. 업무 GPT가 **기존 Linux 별도 Viewer 소스와 데이터 계약을 읽기 전용 조사**하여 adapter만 실제 API에 연결. 미확인 API를 GPT가 추측해 확정·구현하지 않으며, 사업장 제한 정보는 PRIVATE/PUBLIC으로 반출하지 않는다.

## 2. 현재 확정된 디자인·정보 구조 (2안 팀 위키형)

**데스크톱 화면:** 위쪽 제품명/위치·검색(실제 지원 범위 표시)·문서 breadcrumb; **왼쪽** 단계형 페이지 트리와 Module/Feature/Scenario 및 Work 구분; **중앙** 문서 제목/짧은 개요/Markdown·HLD·상세설계·이슈/MSC 렌더; **오른쪽** 목차/Work ID/Evidence/원본 경로/검증 상태/고정 revision (근거가 있는 값만, 미확인은 `미확인`).

- 상단 진입 메뉴: `Work` / `Knowledge` / `전체 파일`. `Work`는 기존 Workflow·Kernel의 Issue/Work/Evidence를 **읽기만**, `Knowledge`는 **Module → Feature → Scenario**(Procedure 교차 링크 포함), `전체 파일`은 기존 Viewer r0002의 **전체 업무 콘텐츠 트리**를 보존. 사용자 요구가 ‘위키형’이라는 이유로 기존 전체 트리 접근을 없애지 않는다.
- 중앙 독서 화면은 실제 문서 제목 우선(작은 보조 경로), 본문 폭 약 880~960px, 줄 간격 약 1.65~1.75, H1/H2/H3 시각적 위계와 목차 앵커, 긴 코드/표 **영역 내부** 가로 스크롤. 링크는 현재 문서와 관련 Work/Knowledge 맥락 및 뒤로 가기 유지.
- 모바일 390px/320px에서는 **본문 우선**, 좌측 트리와 우측 메타 패널을 접는 드로어. 키보드 탐색/초점 표시/스크린리더 레이블과 명암대비 기본 준수.
- 개인 Knowledge의 `DRAFT/PREVIEW/NOT_VERIFIED`와 실제 승인된 그룹 정본의 `PUBLISHED`를 혼동시키지 않음; 실제 스키마/메타 필드는 업무 GPT가 확인하기 전 hardcode 금지. UNKNOWN 상태를 완료/PASS로 표시하지 않는다.
- MSC는 기존 `doc-converter`가 만든 **B형 HTML+SVG**를 되도록 원본 링크/별도 넓은 문서 화면으로 표시. Viewer가 MSC 변환기 자체를 재구현하거나 participant 의미/원본 데이터를 바꾸지 않음. 6명/12명 participant, 장문 phase 확대·접기·복귀 UX를 시험.
- 디자인은 기존 2안 *팀 위키 정보구조*를 독자적으로 구현. 과거 4개 샘플의 ChatGPT 대화 `sandbox:` 경로는 **GitHub 정본 자료가 아니며 새 창에서 자동 접근된다고 가정 금지**. 현재 PRIVATE의 `VIEWER_CURRENT_DESIGN_LAYOUT_REVIEW_SAMPLE_r0001_20261119_KST.html`도 이전 **원시 3영역 축약 시안**으로 이 신규 2안 완성본과 혼동 금지.

## 3. GPT가 다음 창에서 제작할 독립 프런트엔드 패키지

권장 논리 구조(파일명은 기존 실제 서비스와 충돌하면 구현 시 조정):
```text
viewer-wiki-ui/
  index.html              # UI 진입점; 합성 데이터 데모를 실제로 탐색 가능
  assets/style.css        # 위키형 화면과 1440/390/320 반응형
  assets/app.js           # 문서탐색, 검색 UI, 선택/목차/탭/브레드크럼, 에러/빈 상태
  adapters/adapter.js     # 아래의 읽기 전용 추상 인터페이스; 기본은 합성 데이터
  fixtures/demo-data.js   # 실 데이터/회사 코드/제한 메타정보 없는 예시만
  DESIGN.md               # 정보구조, 렌더 정책, 보안/접근성, 화면 상태
  INTEGRATION.md          # 업무 GPT→Linux Viewer 현장 연결 절차 및 차이 매핑표
  TEST_REPORT.md          # 실제 수행 테스트와 NOT_RUN·증거
  manifest.sha256         # 실제 완성 bytes에 대한 SHA-256 목록
```

- **필수 구현 범위:** Work/Knowledge/전체파일 탭 전환, 좌측 트리 및 현재 위치, 목록/문서 선택, Markdown 샘플 읽기, 목차/앵커, 메타 패널, 상태(PREVIEW/미확인), 문서 링크/뒤로가기, 좁은 화면 드로어, MSC HTML을 위한 안전한 **placeholder 및 외부 연결 지점**. 샘플 검색은 **fixture 한정**임을 명시하고 호스트 전체검색으로 오인시키지 않는다.
- **데이터 계약(예시 인터페이스, 실제 API 계약 아님):** `listRoots()`, `listChildren(nodeId)`, `getDocument(docId)`, `getDocumentMeta(docId)`, `getMscTarget(docId)`. 실제 Linux API/경로/권한 확인 후 업무 GPT가 매핑, 프런트엔드에서는 이를 직접 가정하지 않음.
- **보안 설계:** 실제 파일/Markdown/메타/HTML은 비신뢰 입력으로 취급, 무작위 HTML 삽입 없이 안전한 Markdown sanitizer/escape 사용. `innerHTML`에 파일 원문/메타를 직접 대입 금지. iframe sandbox와 별도 origin은 실제 서비스의 B3 구현 계약을 현장에서 확인한 후만 활성화. 정적 fixture 데모 성공을 실제 운영 보안 PASS로 승격 금지.
- **의존성:** 가능하면 프레임워크 없는 정적 JS/CSS, 외부 CDN·추가 서버·인증·새 DB 없이 동작. 기존 Viewer가 이미 프레임워크를 쓰면 동작·디자인과 API 경계만 살리고 최소 연결.
- **완료 정의:** 2안 UI가 독립 데모에서 실제 동작, 1440/390/320 화면/키보드/문서 렌더 자가시험, 산출물 코드+해시+ZIP, 현장 연동에 필요한 미확인 매핑 포인트를 문서로 완전히 정리. **독립 데모 완성**과 **Linux 별도 Viewer 설치·서비스에 통합 완료**는 별도 판정.

## 4. 업무 GPT가 수행할 현장 연결·업무 LLM 위임

1. 별도 Linux Viewer의 **실제 서비스/소스/버전/UI 구조/빌드·시작 방법/기존 인증·파일루트·읽기 API**를 기존 Work·인계와 대조하여 READ_ONLY G0로 확인. 호스트 세부 경로/제한 자료는 업무 환경에 보존.
2. 기존 화면을 단순 교체할 수 있는지, 기존 template/renderer에 스타일·컴포넌트만 이식해야 하는지 **REUSE→CONNECT→입증된 최소 EXTEND**로 판정. 새로운 서비스나 스킬 신설을 기본 해법으로 삼지 않음.
3. 업무용 LLM/Agent에게는 **일회성 좁은 구현 작업**만 전달: adapter 실제 계약 연결, 기존 로그인/파일 접근/렌더링 존치, 필요 마이너 CSS 수정, 롤백 가능한 변경. 직접 업무 데이터·Work 원본·Group Knowledge를 업로드/게시하거나 API를 재정의하지 않음.
4. 그룹 Knowledge/개인 Knowledge 메타정보는 **Knowledge Updater 책임**, 업무 GPT가 실제 설치본과 그룹 정본을 확인해 매핑. Viewer는 **읽기 전용 presentation**만 하며 Updater/Workflow/Kernel/doc-converter를 UI 적용을 이유로 수정 금지.
5. **호스트 변경/설치/서비스 재시작·공유**는 기존 유효 승인·위임과 변경 전 백업·롤백 확인 후 허용 범위에서만. 범위 밖이면 `BLOCKED`로 분리하고 UI 데모·자체시험은 계속.
6. HTML/URL에 접근 가능한 동료 수, 조회 권한 범위, 실제 배포 가능성은 host E3/E4 별도 증거 전 `NOT_VERIFIED`.

## 5. 보안 게이트·수락/회귀 테스트

- 기존 Claude r0002 정식 리뷰 `ACCEPT_WITH_CHANGE`의 **B1** path containment/canonicalization·symlink/TOCTOU, **B2** 제한자료/비밀 문자열 선별 fail-closed, **B3** MSC HTML active content의 origin·cookie·iframe sandbox 분리 문제는 **미해결 BLOCKING**. 프런트엔드 스타일 교체로 해결됐다고 간주하지 않음.
- `U01` 5초 안에 Work/Knowledge/전체파일 진입 구별(실제 사용자 관찰은 업무 호스트에서 수행).
- `U02` 대표 Work에서 Problem/Cause/Solution→관련 MSC를 3회 이내 주요 조작으로 탐색(합성 데모 후 현장 실증).
- `U03` 1440/390/320 레이아웃: 본문 잘림·의도치 않은 페이지 overflow 0, 표/코드 자체 가로 스크롤 허용.
- `U04` Markdown H1~H3/TOC/표/코드/문서 간 링크/원본 경로/deep link/뒤로가기, XSS 악성 fixture 안전 처리.
- `U05` MSC 6/12명 참가자 긴 시나리오에서 확대/폭맞춤/메뉴 복귀 및 기존 B형 HTML의 원문 불변 (호스트 실행 전 NOT_RUN).
- `U06` 개인 초안/그룹 게시 revision/미확인 구분, 원본 파일·SHA 불변, 신규 write API 0.
- `U07` 보안 B1~B3 악성 입력·경로 이탈·HTML 실행·제한자료 노출 부정 시험은 **실제 Linux 서비스 검증** 필요. 미검증이면 `HOST_SECURITY=NOT_VERIFIED`, 공개·동료 공유 금지.
- `U08` 기본 접근성: 키보드 탭·초점, 열기/닫기 버튼 라벨, 200% 확대, 모바일 패널 우선순위.
- 테스트 값 `PASS/FAIL/SKIP/NOT_RUN`로 구분, 실제 수행한 코드/브라우저/호스트, 스크린샷·리포트의 합성/실자료 구분.

## 6. 협업 리뷰·승인·보존

- 기존 Viewer r0002 정식 독립 리뷰는 **이미 완료**, 결과 `collab/reviews/REQ-L1-WORKSPACE-LOCAL-VIEWER-DESIGN-R1-20261118/REVIEW_RESULT_1.md`; 같은 요청 재호출 금지.
- 신규 r0004 소유권/UX 델타는 리뷰용 사전자료 `VIEWER_R0004_UX_REVIEW_HOST_PREFLIGHT_HANDOFF_r0001_20261119_KST.md`가 있지만 **최신 확인 시점 새 REQUEST/승인서명/READY와 실제 리뷰가 미완료**. 변경된 UI 구현물을 새 독립 리뷰에 넣을지는 기존 유효 요청·승인 범위·중복/비용/정책 사전검증 결과를 보고 판정. 미승인 유료 호출 없이 허용된 개발·자체시험 진행.
- 코드/설계/합성 fixture·시험 결과는 PRIVATE에 게시 가능(비민감 검토 후). **최종 ZIP을 PUBLIC `wonhwipark/L1Work/main` 루트로 게시**하는 것은 별도의 유효한 공개 전달 승인과 민감정보 검사 후. 업무 Linux 호스트 설치·LIVE·공유/운영전환과 구분.
- 기존 `CURRENT.md`, r0002/r0003/r0004 원본, 이미 완료된 리뷰·영수증·개인 Work/Evidence, 그룹 지식 revision은 무손실 보존. 다른 스킬/DB/실제 Viewer 동작은 이 인계 작성 단계에서 수정하지 않음.

## 7. 다음 창의 첫 실행 지시 (복사 없이 바로 재개)

> PRIVATE `wonhwipark/CoWork-Skill-Collab` `main`에서 `collab/CONTEXT_BRIEF.md` → `collab/projects/L1-WORKSPACE-RAG-20261111-001/CURRENT.md` → `collab/projects/L1-WORKSPACE-RAG-20261111-001/L1_WORKSPACE_WIKI_UI_GPT_IMPLEMENTATION_TO_BUSINESS_GPT_HANDOFF_r0001_20261119_KST.md`를 읽고 기존 Work를 재개해줘. 사용자 확정 2안(팀 위키형)을 기준으로, GPT가 실제 작동하는 독립 HTML/CSS/JS UI와 adapter fixture, 테스트·SHA-256·ZIP을 제작해줘. 업무 GPT/저사양 LLM은 기존 Linux 별도 웹뷰어 구조 확인 후 연동/현장 시험만 맡도록 INTEGRATION.md까지 작성해줘. 기존 Reviewer r0002 BLOCKING B1~B3 보존, 새 유료 독립 리뷰/운영 설치/공개 배포는 승인·게이트를 별도로 판정해줘. 실제 하지 않은 부분은 NOT_RUN/NOT_VERIFIED로 구분하고, 완료 산출물은 같은 PRIVATE Work와 CURRENT에 게시·원격 재조회·해시 확인해줘.

**NEXT_ONE_ACTION:** 새 창의 GPT가 이 정본을 바탕으로 **2안 UI 독립 구현물 제작 및 자체시험**에 착수.
