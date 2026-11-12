# COWORK-GITHUB-DASHBOARD-20261111-001 — CURRENT

## 대시보드 현대화 HTML 시안 3종 — 선택 대기 (2026-11-12)
- **사용자 요청:** 현재 GitHub Pages 대시보드의 그림 표현·모던한 UI를 개선해 서로 다른 HTML 시안 3종으로 보여주고 사용자 선택 후 최종 적용.
- **DESIGN_OPTIONS=POSTED_FOR_USER_SELECTION / DEFAULT_PAGE=UNCHANGED**. 공개 Pages `L1Work/main/docs/cowork-dashboard/concepts/` 아래 비교 랜딩과 3개 별도 시안을 게시. 기존 `L1Work/main/docs/cowork-dashboard/index.html`의 기본 대시보드 HTML은 이 작업에서 변경하지 않음.
- **시안 01 — Executive Flight Deck**: `concepts/01/index.html`. 밝은 카드형 운영 현황, 4 KPI, 가로 프로세스 7단계, 게이트 상태.
- **시안 02 — System Topology**: `concepts/02/index.html`. 다크 UI, 고정 인라인 SVG로 현재 LIVE 운송과 GitHub 목표 경로, 신뢰·승인 게이트를 토폴로지 구성도로 표시.
- **시안 03 — Process Journey**: `concepts/03/index.html`. 에디토리얼 UI, 7단계 세로 경로 타임라인, 역할·검증 상태·다음 조치.
- **3개 비교 웹페이지:** `https://wonhwipark.github.io/L1Work/cowork-dashboard/concepts/`; 각 링크 `.../concepts/01/`, `.../02/`, `.../03/`. L1Work PUBLIC 루트 README에 미리보기 바로가기 등록.
- **검증된 공개 데이터 경계:** PRIVATE `state.json` 관측은 2026-11-12 기준 프로젝트 CURRENT 4개/REQUEST 0/REVIEW 0/RECEIPT 0; `WINDOWS_STAGE1_EXECUTION=NOT_RUN`, `INDEPENDENT_REVIEW=NOT_RUN`, `CUTOVER=MIGRATION_NOT_CUTOVER`. 수치는 GitHub 문서 관측 수일 뿐 완료 건수가 아님. PUBLIC 시안에는 개인별·사내 자료 원문, 내부 프로젝트 ID, REQUEST/READY 상세, 영수증, 토큰/키 등 미포함.
- **시험:** 세 시안 및 비교 HTML의 PRIVATE 링크/JS/자동 데이터 네트워크 미포함 사전 검사 PASS, 공개 원격 fetch_file 원문 일치 PASS. L1Work Pages 시안별 Actions 01: #43192319771 SUCCESS, 02: #43192585272 SUCCESS, 03: #43192851849 SUCCESS. 비교 페이지 최종 run은 별도 확인. 실브라우저 렌더링·픽셀 일치·모바일 실제 기기 시험은 NOT_RUN, HTML/CSS 반응형 규칙 포함. Claude 독립 리뷰 NOT_RUN.
- **권한/운영:** 정적 시안 공개 범위 외 PRIVATE 자료 게시 없음. Windows watcher/기존 LIVE/운영 DB/GitHub LIVE 전환 변경 없음. 향후 기본 화면으로 채택할 시 **사용자가 01/02/03 중 하나를 선택한 후** 교체하고 실제 배포 및 README를 검증.
- **다음 한 동작:** 사용자가 3개 HTML을 모바일/PC에서 보고 **1, 2, 3**으로 선택.


## 최신 상태 — GitHub Pages HTML 기본화 및 공개 상태 요약 게시 (2026-11-12)
- **사용자 최신 지시:** `page 에 게시해서 링크클릭후 바로 볼 수 있도록, 항상 default`. 앞으로 CoWork 대시보드 기본 경로는 **`https://wonhwipark.github.io/L1Work/cowork-dashboard/`** (GitHub Pages HTML). Markdown/PRIVATE HTML blob 직접 열기를 기본값으로 삼지 않음.
- **PUBLIC_HTML=POSTED, PRIVATE_TO_PUBLIC_FILTER=ALLOWLIST**: `wonhwipark/L1Work` PUBLIC `main/docs/cowork-dashboard/index.html`을 기존 합성 샘플에서 검증된 상태 요약·7단계 흐름·역할별 환경·검증 상태표로 교체. 직접 PRIVATE 파일 ID/원문/영수증/개인정보/토큰/비밀정보 반출 없음.
- **페이지 원격 게시:** PUBLIC HTML commit `9d08be675cd0ee929e3305cbbc4bd44750423ffc`, Git blob SHA `4b67f5afa107b8420100a5be11f2d9f611b43d2d`, 원격 본문 일치 검증 PASS. 공개 README commit `6652b3001ddf4261685c1805c3be53f017c7d9e5`, Pages 진입 `docs/index.html` commit `5633f7b1ee21ea3027e9006cb7019faccc731907`, 각 readback PASS.
- **실제 배포 증거:** GitHub Pages Actions #43054416940 (HTML 교체 자체, SUCCESS), #43054544105 (최종 진입 페이지 변경, SUCCESS). 최신 run의 build/deploy/report-build-status 모두 SUCCESS, 배포 로그 `Reported success!` 및 `https://wonhwipark.github.io/L1Work/` URL 발급 관측. 직접 HTTP GET/served body SHA는 네트워크 제한으로 `NOT_VERIFIED`.
- **게시한 사실 상태:** 2026-11-12 기준 PRIVATE `state.json`에서 3개 프로젝트 문서, GitHub REQUEST/REVIEW/RECEIPT 각 0개 관측, `WINDOWS_STAGE1_EXECUTION=NOT_RUN`, `INDEPENDENT_REVIEW=NOT_RUN`, `CUTOVER=MIGRATION_NOT_CUTOVER`. 기존 Dropbox LIVE 운송 유지(운영 변경 미실시). 공개 HTML에는 업무 IDs 대신 상위 범주로 표시.
- **공개·보안 계약:** `collab/dashboard/PUBLIC_PAGES_DEFAULT_POLICY.md` 신규. CoWork PRIVATE 루트 README, 대시보드 README 및 `collab/START_HERE.md`에 Pages 기본 경로와 예외 범위 명시. PUBLIC L1Work에는 허용된 상위 상태만 표시, 내부 원문·PRIVATE 링크·민감 메타데이터는 미게시.
- **중요 제한:** `PAGES_AUTO_DEPLOY=PASS`는 PUBLIC 저장소에 커밋될 때의 자동 재배포. `PRIVATE_STATUS_AUTO_SYNC=NOT_IMPLEMENTED`로 유지. 공개 상태는 마지막 검증 시점의 스냅샷이며 최신 PRIVATE 결과를 자동 반영하지 않음. 공개 동기화 자동화에는 별도 권한·보안 설계·승인 필요.
- **독립 리뷰·운영:** Claude Code `INDEPENDENT_REVIEW=NOT_RUN`, Windows 실제 호스트 SHADOW `NOT_RUN`, LIVE 전환 `MIGRATION_NOT_CUTOVER`. 기존 watcher/운영 DB/예약 작업/Telegram 및 PUBLIC 스킬 ZIP 무변경.
- **다음 한 동작:** 사용자에게 Pages HTML URL을 기본 제공. 향후 PRIVATE 상태가 바뀔 때 공개 허용 목록 검토 후 PUBLIC HTML을 업데이트하고 Pages 배포 성공을 재검증. 자동 동기화는 승인 전 구현하지 않음.


## 최신 게시 상태 — HTML 스냅샷 PRIVATE 업로드 (2026-11-12)
- **사용자 지시:** 이전에 제공한 `CoWork_협업흐름_STATUS_20261112.html`을 GitHub에 업로드.
- **UPLOAD=PASS / GITHUB_REMOTE_READBACK=PASS**: `collab/dashboard/snapshots/CoWork_협업흐름_STATUS_20261112.html`을 PRIVATE `main`에 새 파일로 게시. 원본/원격 본문 정확히 일치.
- **실제 파일:** 20,943 bytes, SHA-256 `e2530c1062540e93191ca62bcf9dd0ece1d8cdac35e0903d8e6079c047f5d9e1`. Git blob SHA `df233dd31404735f2d41bdc0a6b0059a97d49494`. 원격 게시 commit `b7fe8f9342a355d6516296d62f0ecbb238c8a5df`.
- **진입점:** PRIVATE 루트 `README.md`와 `collab/dashboard/README.md`에 HTML 스냅샷 바로가기 등록 및 원격 내용 재조회 PASS.
- **구분:** 이 파일은 **고정 스냅샷**이며, 실제 자동 생성 정본은 `collab/dashboard/index.html`. GitHub PRIVATE의 HTML 링크는 소스를 표시하므로 다운로드하여 브라우저에서 열어야 함. L1Work PUBLIC 샘플은 미변경.
- **운영 안전:** Dropbox LIVE/Windows watcher/운영 DB/예약 작업/Telegram 및 Claude 리뷰 호출 변화 없음. `INDEPENDENT_REVIEW=NOT_RUN`, `CUTOVER=MIGRATION_NOT_CUTOVER` 유지.
- **다음 한 동작:** GitHub PRIVATE 루트 README에서 HTML을 다운로드해 화면 확인. 이후 자동 HTML을 기본으로 계속 사용.


## 최신 표시 방식 — HTML 우선 (2026-11-12)
- **사용자 요청:** "앞으로는 대시보드는 HTML로 확인". 기본 화면은 `collab/dashboard/index.html` (PRIVATE), GitHub `VIEW.md`는 보조. 루트 `README.md` 및 `collab/dashboard/README.md`에 HTML 기본 표시로 갱신. GitHub 파일 화면은 HTML 소스가 보이므로 파일 다운로드→브라우저로 열기 방식이며, PRIVATE HTML의 익명 공개 URL은 제공하지 않음.
- **HTML 단일파일 스냅샷 별도 제공:** `CoWork_협업흐름_STATUS_20261112.html` (현재 대화 첨부) 20,943B, SHA-256 `e2530c1062540e93191ca62bcf9dd0ece1d8cdac35e0903d8e6079c047f5d9e1`; 프로젝트 CURRENT 3, GitHub REQUEST/REVIEW/RECEIPT 관측 각 0, Windows Stage1 NOT_RUN, Claude 독립 리뷰 NOT_RUN, CUTOVER=MIGRATION_NOT_CUTOVER, L1Work 합성 샘플 Pages 배포 PASS 기록. 협업 관리 환경 / 업무 실행 환경 용어 사용.
- **정본 구분:** 위 대화 첨부 HTML은 2026-11-12 기준 **고정 스냅샷**이며 PRIVATE GitHub `main`에 같은 바이트의 신규 파일을 게시한 것으로 보고하지 않음. 자동 최신 생성의 정본은 `collab/dashboard/index.html` (Actions 관리)이고 별도로 GitHub `VIEW.md`가 있다.
- **파일 자체 정적 검사:** HTML DOM 구조, 7개 흐름 카드, 8개 STATUS 테이블 항목, 3개 프로젝트 카드, 4 KPI 및 허용된 links/CSP 확인 PASS. 실제 Chromium 렌더링은 브라우저 바이너리 부재로 **NOT_RUN**. GitHub Actions의 기존 합성 회귀 35 PASS는 별도 실측 기록이며 새 별도 스냅샷의 브라우저 시험 PASS로 대체하지 않음.
- **보안:** 실제 PRIVATE 현황을 L1Work PUBLIC Pages 또는 Dropbox로 게시하지 않음. L1Work 공개 주소는 계속 실제 협업 정보 없는 합성 샘플 전용. `WINDOWS_HOST_E2E=NOT_RUN`, `INDEPENDENT_REVIEW=NOT_RUN`, `CUTOVER=MIGRATION_NOT_CUTOVER` 유지.
- **다음 한 동작:** 사용자가 내려받은 HTML을 브라우저에서 열고 도식·상태 가독성을 확인. 실시간 웹 URL로 실제 PRIVATE 상태를 볼 필요가 있으면 별도 접근 통제/공개 범위 설계와 승인 필요.



## 최신 업데이트 — 협업 흐름·현재 STATUS 도식화 (2026-11-12)
- **DEVELOPMENT=IMPLEMENTED, SELF_TEST=PASS, PRIVATE_ACTIONS=PASS, GITHUB_PAGES_DEPLOY=PASS(기존 합성 샘플에 한정).** 샘플 웹페이지가 PRIVATE 협업 현황이라는 뜻은 아님.
- **CUTOVER=MIGRATION_NOT_CUTOVER.** 기존 LIVE 운송은 변경하지 않았고, Windows 호스트 STAGE1_EXECUTION=NOT_RUN / INDEPENDENT_REVIEW=NOT_RUN은 별도 전환 CURRENT 최신 근거. 실제 운영 호스트 시험과 구분.
- **협업 화면:** GitHub PRIVATE의 collab/dashboard/VIEW.md에서 Mermaid 도식(기존 LIVE 경로 / GitHub 목표 경로), 6개 운영 STATUS 항목, 근거 CURRENT 링크 확인. 기존 REQUEST→READY→REVIEW→RECEIPT→GPT 판정 및 피드백 유지.
- **표현 교체:** ‘사내/사외’ 대신 협업 관리 환경(GPT·GitHub) / 업무 실행 환경(Windows watcher·Claude Code). 구성 요소의 책임과 검증 증거를 기준으로 분류.
- **HTML 개선:** index.html의 7단계 반응형 흐름 카드, 관측 수·운영 상태표. 현재 GitHub REQUEST/REVIEW/RECEIPT 관측은 각 0개지만 미이관/미확인과 실제 완료 수를 혼동하지 않음.
- **구현/정본:** flow_view.py 신규, generate.py 및 tests/test_flow_view.py 갱신. state.json schema COWORK_GITHUB_DASHBOARD_SHADOW_V3에 operations 추가. PRIVATE의 README 2곳 업데이트. PUBLIC L1Work 샘플/배포본 변경 없음.
- **실제 시험:** GitHub Actions #43050678544 및 #43050925086 모두 completed SUCCESS, 27 dashboard tests + 8 public sample safety tests = **35 PASS / 0 FAIL**. GitHub 원격 index.html/VIEW.md/state.json 최신 파일 재조회 PASS. 실제 Windows 독립 리뷰·LIVE 전환·브라우저 픽셀 E2E = NOT_RUN.
- **전체 보고:** FLOW_STATUS_VISUAL_UPDATE_20261112.md (이 프로젝트 경로, 원격 게시 및 readback 확인).
- **다음 한 동작:** 사용자가 PRIVATE GitHub VIEW.md에서 Mermaid 도식/STATUS 가독성 확인; 실제 Windows 호스트 증거는 승인된 별도 인계와 CURRENT 업데이트 후 재판정.


## 최신 상태 — L1Work GitHub Pages 실제 배포 성공 (2026-11-12)
- 사용자 GitHub Pages 설정 화면 확인: `Deploy from a branch`, `main /docs`, 'GitHub Pages source saved'; 사용자가 직접 활성화 완료.
- **GITHUB_PAGES_DEPLOY=PASS**: PUBLIC `wonhwipark/L1Work` GitHub Actions [run #43046422145](https://github.com/wonhwipark/L1Work/actions/runs/43046422145) `completed/success`. 독립 build/report-build-status/deploy jobs 모두 SUCCESS. Deploy 로그에 `Reported success!` 및 발급된 `Evaluated environment url: https://wonhwipark.github.io/L1Work/`가 존재.
- **웹페이지:** GitHub가 발급한 사이트 루트 `https://wonhwipark.github.io/L1Work/`는 `docs/index.html`에 의해 샘플 폴더 `https://wonhwipark.github.io/L1Work/cowork-dashboard/`로 리다이렉션하도록 구성됨. PUBLIC repository `docs/cowork-dashboard/index.html` 원격 재조회 `PASS` (4765B, SHA-256 `40a33950e4fc37ed643522ed06b73ea89afdd9b4c0447417d67bc19501c82779`).
- **검증 한계:** GitHub가 Pages 성공을 보고했지만 GPT 실행 환경에서는 직접 HTTP GET이 불가능했음. `PUBLIC_HTTP_200=NOT_VERIFIED`, `REMOTE_SERVED_BODY_SHA256=NOT_VERIFIED`, 브라우저 실사용 표시 `NOT_RUN`. 사이트 정상 열림은 사용자가 URL 클릭으로 확인 가능.
- 이번 업데이트는 화면 게재 확인 및 상태 문서 갱신에 한정. `PUBLIC_DATA=SYNTHETIC_ONLY`, 실제 GitHub REVIEW/RECEIPT E2E `NOT_RUN`, `CLAUDE_INDEPENDENT_REVIEW=NOT_RUN`, `CUTOVER=MIGRATION_NOT_CUTOVER`. 기존 Dropbox LIVE/Windows watcher/운영 DB는 변경하지 않음.
- 상세 업로드 이력: `L1WORK_PUBLIC_HTML_UPLOAD_20261112.md`. 이전에 기록된 `PAGES_WEB_DEPLOY=NOT_VERIFIED`는 이 최신 배포 로그로 **PASS로 갱신**하며, HTTP 본문 검증은 구분하여 미검증 처리함.


## 최신 상태 — L1Work PUBLIC HTML 파일 게시 완료 / Pages 웹사이트 활성화 미검증 (2026-11-12)

- **사용자 최신 지시:** 공개 샘플 HTML의 저장·확인 위치를 `wonhwipark/L1Work` PUBLIC로 지정. 이전 PRIVATE Pages 제한을 우회하기 위한 무단 반출이 아니라, 사용자가 지정한 고정 공개 샘플에 한정한 게시.
- `PUBLIC_HTML_FILE=PASS`, `GITHUB_REMOTE_READBACK=PASS`: `L1Work/main/docs/cowork-dashboard/index.html`, 4,765B, SHA-256 `40a33950e4fc37ed643522ed06b73ea89afdd9b4c0447417d67bc19501c82779`, commit `0a92951c114b014b40353c3351870e731ef55cb7`.
- `PAGES_ROOT_ENTRY=PASS`: `L1Work/main/docs/index.html`에서 `cowork-dashboard/`로 이동하는 정적 진입 페이지, commit `f2957b91da454c3d218c2837e4fb897b48c35076`.
- `PAGES_WEB_DEPLOY=NOT_VERIFIED`, `PUBLIC_HTTP_E2E=NOT_RUN`: L1Work에는 Pages Actions 실행 이력 없음. GitHub Pages 설정 UI `L1Work/settings/pages`에서 `Deploy from a branch → main /docs` 선택 필요. 설정 전 예상 도메인을 동작 완료로 보고하지 않음.
- `DATA=SYNTHETIC_ONLY` 승인된 3단계 샘플만 공개. PRIVATE 협업 정보, 실제 REVIEW/RECEIPT/상태 JSON, Windows watcher·Dropbox LIVE·운영 DB·PUBLIC ZIP 배포 변경 없음.
- **최신 결과:** [L1WORK_PUBLIC_HTML_UPLOAD_20261112.md](L1WORK_PUBLIC_HTML_UPLOAD_20261112.md) 원격 게시 및 내용 readback `PASS`.
- **다음 한 동작:** GitHub Pages `main /docs` 활성화 후 실제 공개 URL·HTTP 200·HTML 본문 검증. `CUTOVER=MIGRATION_NOT_CUTOVER` 유지.


## 최신 상태 — 공개 샘플 Pages 업로드 시도 및 실제 차단 (2026-11-11 23:49 KST)
- **사용자 승인:** 기존 합성 샘플 HTML GitHub Pages 공개 업로드 승인. 실제 협업/업무·리뷰 데이터 공개 승인은 아님.
- **PUBLIC_SAMPLE_SOURCE=VERIFIED**: 원본 `collab/dashboard/public_preview/index.html` 4,754 bytes, SHA-256 `6acf4bc151dc292e32d97a03479784b26f0384c61aef59f99120867c1d239786`. 고정 SHA 일치일 때만 게시 후보로 허용.
- **PUBLIC_PAGES_WORKFLOW=POSTED / REMOTE_READBACK=PASS**: 신규 `.github/workflows/cowork-public-preview-pages.yml`, commit `7b251a336ed1184e90682495e5d79652260d22a2`. 기존 PRIVATE dashboard Actions와 역할 분리, PUBLIC `L1Work` 불변.
- **PUBLISH_RUN=FAILED_ON_PAGES_CONFIGURATION**: [GitHub Actions #43042181335](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/43042181335). Checkout PASS, 승인 후보 해시 검증·정적 HTML 단일 파일 스테이징 PASS; Pages `configure-pages`에서 404 `Not Found` (Pages 미설정/사용 불가); Pages artifact 업로드 SKIP, 실제 배포 SKIP.
- **스테이징 출력:** 공개 상태 안내 문구만 4개 고정 치환한 4,765 bytes HTML, SHA-256 `40a33950e4fc37ed643522ed06b73ea89afdd9b4c0447417d67bc19501c82779` (Actions 로그 실측). PUBLIC에 **실제로 발행된 바이트가 아님**.
- **PUBLICATION=BLOCKED_NOT_PUBLISHED; PUBLIC_URL=NOT_AVAILABLE; HOST_E2E=NOT_RUN**. URL 생성·외부 접속 성공을 선언하지 않음.
- **PRIVATE 대시보드:** VIEW.md/HTML/SUMMARY/state.json 및 PRIVATE 자동 갱신 기존 구현 유지. 기존 공개 후보 자체시험 8 PASS, PRIVATE 대시보드 기존 18 PASS; 실제 GitHub REQUEST→REVIEW→RECEIPT E2E NOT_RUN, Claude 독립 리뷰 NOT_RUN.
- **CUTOVER=MIGRATION_NOT_CUTOVER**. Dropbox LIVE, Windows Claude Code watcher/Bridge/운영 DB/예약 작업/Telegram 및 운영 신뢰키 미변경.
- **최종 결과 정본:** `PUBLIC_PAGES_ATTEMPT_AND_FINAL_STATUS_20261111.md` (이번 업데이트에 앞서 PRIVATE main 게시)와 `collab/dashboard/public_preview/PUBLIC_RELEASE_GATE.md`.
- **다음 한 동작:** [GitHub 저장소 Pages 설정](https://github.com/wonhwipark/CoWork-Skill-Collab/settings/pages)에서 **Source=GitHub Actions**로 활성화(계정 요금제에 따라 PRIVATE Pages 제한 가능). 그 후 `CoWork public synthetic-only Pages release` 수동 재실행 1회 → 실제 공개 URL/바이트 검증 → 상태 갱신. 설정 불가 시 임의 PUBLIC L1Work 게시로 우회하지 않는다.


## 공개용 HTML 독립 후보 — 설계·구현·시험 (2026-11-11 KST)
- **사용자 요청 범위:** 민감정보를 제거한 별도 공개용 HTML 설계·구현·시험. 실제 공개 게시/Pages/PUBLIC 배포는 별도 승인. 이번 작업은 PRIVATE `main`에서만 후보 제작 및 검증.
- **현재 판정:** `DEVELOPMENT=IMPLEMENTED`, `SELF_TEST=PASS`, `ACTIONS_PRIVATE_RUN=PASS`, `INDEPENDENT_REVIEW=NOT_RUN`, `PUBLICATION_APPROVAL=NOT_GRANTED`, `PUBLIC_HOST_E2E=NOT_RUN`, `CUTOVER=MIGRATION_NOT_CUTOVER`.
- **후보:** `collab/dashboard/public_preview/index.html` — **4754 bytes**, SHA-256 **`6acf4bc151dc292e32d97a03479784b26f0384c61aef59f99120867c1d239786`**. GitHub blob SHA `a83dab85bf7dbf6d98722b64d34d826b0d613660`; GPT가 만든 로컬 파일의 Git blob SHA-1과 원격 blob ID 일치 → 후보 실제 바이트 일치.
- **개발:** `collab/dashboard/public_preview/build.py`는 `STATIC_SYNTHETIC_ONLY` 문구만 이용하는 정적 HTML 생성기. 실제 `CURRENT.md`, REQUEST/READY/REVIEW/RECEIPT, Work ID, 운영 이력/통계, 계정/경로/링크, 자격증명을 입력으로 사용하지 않음. 샘플 3단계와 `NOT_APPROVED` 표시.
- **보안 게이트:** `collab/dashboard/public_preview/PUBLIC_RELEASE_GATE.md`; 실제 PUBLIC/Pages/외부 URL에 배포하는 단계는 명시 승인 전 금지. `collab/dashboard/public_preview/README.md`에 운영 범위 기록.
- **시험:** PRIVATE GitHub Actions run `43039501201` `completed/success`, workflow 로그 **기존 18 PASS + 후보 보안 8 PASS = 26 PASS / 0 FAIL**. 후보 4754B; Action이 PRIVATE `main`에만 생성 파일 게시(commit `c764932`). GitHub 원격 fetch_file·blob SHA 검증 PASS. 보안 테스트는 외부 URL/스크립트/네트워크 요청, PRIVATE 파일 유출 sentinel, 실행 시각/결과 결정성, CSP 및 식별자 누출 방지를 포함.
- **브라우저 시험:** 로컬 Chromium desktop 1280px 및 mobile 390px에서 HTML 렌더링, 카드 3개, 수평 overflow 0 확인. 실제 외부 공개 호스트/인증/브라우저 E2E는 `NOT_RUN`.
- **기존 구성 불변:** PRIVATE 대시보드 `collab/dashboard/index.html`/VIEW/요약 유지, Dropbox LIVE, Windows watcher/Bridge/예약 작업/SQLite main·WAL·SHM/Telegram, Claude 모델 호출, PUBLIC `wonhwipark/L1Work`, GitHub Pages 및 LIVE 전환 변경 없음.
- **다음 한 동작:** 사용자가 공개할 **정확한 후보 SHA 및 대상 호스팅 방식**을 승인하고 보안/반출 범위를 확정한 뒤에만 별도 공개 게시. 실제 정보 연동은 별도의 허용목록 데이터 계약과 추가 승인 필요.


## 클릭 한 번으로 보기 — PRIVATE GitHub 렌더링 (2026-11-11 KST)
- 사용자 요청: GitHub HTML을 다운받지 않고 링크 클릭만으로 진행 현황을 보고 싶음. GitHub PRIVATE HTML blob은 브라우저 실행 화면이 아니므로, 공개 Pages를 열지 않고 **GitHub Markdown native VIEW**로 제공.
- **직접 보기:** `collab/dashboard/VIEW.md` — PRIVATE 로그인 권한을 가진 사람에게 GitHub 화면에서 즉시 렌더링됨. 기존 `index.html`과 `SUMMARY.md`는 보존.
- 구현: `collab/dashboard/generate.py`에 `render_direct_view` 및 `VIEW.md` 출력 추가, `collab/dashboard/tests/test_direct_view.py` 2개 합성 회귀시험 추가, `.github/workflows/cowork-dashboard.yml`에서 `VIEW.md` 자동 commit 대상 등록. `collab/dashboard/README.md`에 바로 보기 진입점 추가.
- 원격 자체 검증: GitHub Actions **#43036400263** `completed/success`; Checkout, Build/Test, PRIVATE Publish 각각 success; bot commit `85ec2330d42933e44a5b967711c6d4d2332d2c88`에서 VIEW.md 원격 생성. GitHub 원격 `VIEW.md` 재조회로 title, 요약, 5단계, REQUEST 미이관 표기 확인. 기존 16개 + 신규 2개로 **18개 테스트 수행 설계**, Actions 전체 test 단계 SUCCESS (개별 테스트 숫자는 로그 검증 시 확정).
- **경계:** 새 VIEW는 GitHub가 렌더링하는 Markdown이며 원본 HTML을 사이트로 호스팅하는 기능은 아님. GitHub Pages 및 PUBLIC 공개 미실시; 외부 익명 접근 불가. Windows 감시기, Claude Code 호출, GitHub 리뷰 실제 E2E, 기존 Dropbox LIVE와 운영 SQLite/예약 작업 변경 없음. `CUTOVER=MIGRATION_NOT_CUTOVER`; 독립 리뷰 `NOT_RUN`.
- 사용자 다음 동작: PRIVATE 로그인 상태에서 [대시보드 바로 보기](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/dashboard/VIEW.md) 클릭. 운영 LIVE 전환 승인은 별개.


## 2차 GitHub 리뷰 연결·항목별 피드백 및 Actions 검증 (2026-11-11 KST)

- 사용자 실행 지시: GitHub Actions SHADOW 대시보드에 GitHub REQUEST → READY → REVIEW → RECEIPT → GPT 판정 연결, 항목별 피드백·다음 담당을 추가.
- **현재 상태:** DEVELOPMENT=IMPLEMENTED / SELF_TEST=PASS / ACTION_RUN=SUCCESS / INDEPENDENT_REVIEW=NOT_RUN / GITHUB_REAL_REVIEW_E2E=NOT_RUN / CUTOVER=MIGRATION_NOT_CUTOVER.
- **수정 파일:** collab/dashboard/review_chain.py (신규 연결기), generate.py (연결 데이터·HTML·MD에 통합), tests/test_review_chain.py (신규 9개 synthetic regression), .github/workflows/cowork-dashboard.yml (collector *.py 변경 감지), collab/dashboard/README.md (입력·보안 계약).
- **출력:** collab/dashboard/state.json (SHADOW_V2 및 review_chains[]), index.html (요청별 5단계·비차단 피드백·다음 담당), SUMMARY.md (모바일 읽기용 연결 표).
- **실제 Actions 실행:** GitHub run #42998956812 (commit 549ed2b38f31b9974b6490d25e3a36fe4a895bd2) completed=SUCCESS, Checkout/Build and test/Publish 각 단계 SUCCESS. 기존 7개 + 신규 9개 = 16개 unittest (workflow의 build/test step 성공). 이는 **합성시험**이며 실제 GitHub reviewer/영수증 실 API 시험 아님.
- **원격 직접 재조회:** state.json schema COWORK_GITHUB_DASHBOARD_SHADOW_V2, review_chains 길이 0, 3개 CURRENT 프로젝트; SUMMARY.md와 index.html에 새 연결 섹션 표시됨. GitHub 실제 요청/리뷰/영수증 0개는 **미이관**이며 Dropbox에서 완료가 0건이라는 뜻이 아님.
- **검증 안전성:** request ID/revision/ZIP digest + READY request raw SHA + REVIEW COMPLETED + RECEIPT ok/processing key + GPT JSON 결정이 일치할 때만 단계 상승. 실패/불일치 시 완료 처리 금지. GPT_DISPOSITION.json은 동작 승인 파일이 아니라 표시용 후속 판정 기록.
- **미검증:** 운영 신뢰 서명·고정 repo ID/commit pin·권한·중복 방지는 Windows watcher/승인 게이트의 별도 사항. 실제 GitHub REVIEW/RECEIPT 입력 E2E, 정식 독립 Claude 리뷰, 모바일 브라우저 E2E, Pages 운영: NOT_RUN.
- **미변경:** 기존 Dropbox LIVE, Windows watcher v0.1.5/Bridge/Dashboard/운영 SQLite·WAL·SHM, Telegram, PUBLIC L1Work, 클로드 모델 호출 0, LIVE 전환 승인 없음.
- **다음 작업:** 정식 승인된 실제 GitHub 리뷰 데이터가 PRIVATE에 안전하게 게시되면 1건 E2E를 검증한다. 검증 전까지 샘플 REQUEST/READY/RECEIPT를 main에 게시하거나 리뷰 실행으로 승격하지 않는다.

## GitHub Actions SHADOW 대시보드 1차 구현 (2026-11-11 KST)

- **현재 상태:** `DEVELOPMENT=IMPLEMENTED`, `SELF_TEST=PASS`, `ACTION_RUN=SUCCESS_OBSERVED`, `INDEPENDENT_REVIEW=NOT_RUN`, `LIVE_CUTOVER=MIGRATION_NOT_CUTOVER`.
- **담당:** GPT 개발·시험·최종 판정 / GitHub Actions 대시보드 빌드·PRIVATE 게시 / Windows Claude Code 독립 리뷰는 별도 유효 요청 시 진행.
- **대상 저장소/브랜치:** `wonhwipark/CoWork-Skill-Collab` PRIVATE `main`.
- **소스:** `collab/dashboard/generate.py`.
- **워크플로:** `.github/workflows/cowork-dashboard.yml` (push: 관련 CURRENT/requests/reviews/receipts/생성기/워크플로 변경; 수동 workflow_dispatch).
- **실제 생성물:** `collab/dashboard/index.html`, `SUMMARY.md`, `state.json`.
- **테스트:** `collab/dashboard/tests/test_generate.py` 7개 로컬 PASS; GitHub Actions 42954499889의 Build/Test 및 PRIVATE Publish 단계가 모두 SUCCESS.
- **원격 관측:** HTML 2개 CURRENT 프로젝트 및 GitHub 파일 관측 수(REQUEST 0/REVIEW 0/RECEIPT 0), 상태 `MIGRATION_NOT_CUTOVER`. Dropbox에서 미이관된 데이터는 완결 0건이 아니라 UNKNOWN.
- **비용·권한:** Actions는 GitHub 자체 런타임 사용; Claude 리뷰 모델 호출 없음. `GITHUB_TOKEN`의 `contents:write`는 PRIVATE 대시보드 산출물 자동 갱신에만 사용, 외부 API/Pages/PUBLIC 발행 없음. 실행 권한은 소스·기본 브랜치 접근 통제에 종속.
- **보안:** 검증되지 않은 리뷰 파일을 승인 증거로 승격하지 않음. 템플릿 HTML 이스케이프/프로젝트 경로 검증/대상 파일 크기 상한; 내용의 원본 전체 복제 금지. push는 비강제/동시성 제한, 결과가 동일하면 no-op.
- **한계:** GitHub에 REQUEST/REVIEW/RECEIPT 원본은 아직 이관되지 않았으며, GitHub watcher LIVE·Windows 호스트 SHADOW·독립 Claude 정적 리뷰·Private Pages 노출 검토·모바일 브라우저 E2E = NOT_RUN. 이전 Dropbox LIVE 및 Windows 운영 감시기/DB/Bridge/Telegram에 변화 없음.
- **표시 방식:** PRIVATE GitHub `SUMMARY.md`는 모바일/웹에서 즉시 읽기 가능. `index.html`은 GitHub 소스 미리보기에서 실행되지 않으므로 브라우저로 다운로드해 열어야 함. GitHub Pages는 게시하지 않음.
- **다음 한 동작:** 이후 GitHub 협업 자료가 실제로 PRIVATE에 이관되면 상태별 파일 집계를 확대하고, 검증된 영수증/승인 레이어를 별도 구현한다. 기존 LIVE cutover 승인과는 분리.
