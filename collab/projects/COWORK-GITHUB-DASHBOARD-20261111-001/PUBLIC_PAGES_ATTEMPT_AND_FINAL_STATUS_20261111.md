# CoWork GitHub Dashboard — 공개 샘플 Pages 게시 시도 및 최신 최종 현황
기준: 2026-11-11 23:49 KST  
저장소: `wonhwipark/CoWork-Skill-Collab` PRIVATE / `main`  
Work ID: `COWORK-GITHUB-DASHBOARD-20261111-001`

## 1. 현재 상태 — 실측
- **사용자 승인:** 기존 합성 샘플 HTML의 GitHub Pages 외부 공개 및 게시 시도 승인. 승인 범위는 샘플 페이지 1개에 한정; 실제 내부 협업 데이터·운영 통계 공개 및 LIVE 전환은 제외.
- **배포 워크플로 게시:** `PASS`. 신규 `.github/workflows/cowork-public-preview-pages.yml`, 커밋 `7b251a336ed1184e90682495e5d79652260d22a2`, PRIVATE `main`. 원격 파일 readback `PASS`.
- **GitHub Actions 실행:** [run #43042181335](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/43042181335) — 전체 `FAIL` (**Pages 설정 미활성**). Checkout `PASS`, 승인 HTML SHA·바이트 검사 및 공개용 1개 파일 스테이징 `PASS`, Configure GitHub Pages `FAIL` (GitHub Pages site 조회 HTTP 404 / Not Found); Pages artifact upload `SKIPPED`; deploy `SKIPPED`.
- **실제 외부 공개:** `BLOCKED_NOT_PUBLISHED`; 웹페이지 배포 완료·외부 URL 응답 `NOT_VERIFIED`. 설정이 미완료인데 URL이 작동한다고 주장하지 않는다.
- **최종 전환:** `CUTOVER=MIGRATION_NOT_CUTOVER`. 기존 Dropbox LIVE 운영 및 Windows watcher/운영 DB/예약 작업/Telegram 변경 없음.

## 2. 승인된 콘텐츠·출력 무결성
- 승인된 PRIVATE 후보 `collab/dashboard/public_preview/index.html`: 4,754 bytes, SHA-256 `6acf4bc151dc292e32d97a03479784b26f0384c61aef59f99120867c1d239786`. Actions에서 정확한 크기·원본 SHA를 대조하고 불일치 시 종료.
- 공개 대상 HTML은 **샘플 단계 3개만 포함**. 워크플로에서 승인 전 상태 문구 4곳만 공개 샘플 문구로 고정 치환. 이번 실행 로그의 스테이징 출력은 4,765 bytes, SHA-256 `40a33950e4fc37ed643522ed06b73ea89afdd9b4c0447417d67bc19501c82779`.
- 배포 아티팩트는 `index.html` **1개만** 스테이징하며, PRIVATE 저장소의 CURRENT/REQUEST/READY/REVIEW/RECEIPT/state.json/VIEW.md 등은 호스팅 출력 경로로 복사하지 않는다. 외부 URL·스크립트·PRIVATE 경로는 차단한다.
- 전 단계에서 원본 공개 후보의 보안회귀 8 PASS / 기존 PRIVATE 대시보드 회귀 18 PASS가 보고되었음. 이번 실행에서는 SHA·격리 스테이징 `PASS`; 실제 Pages E2E는 `NOT_RUN`.
- 독립 Claude 리뷰 `NOT_RUN`; 실제 REQUEST→REVIEW→RECEIPT 연계 E2E `NOT_RUN`.

## 3. 차단 원인·필요한 단 한 번의 사용자 설정
개인 계정의 PRIVATE 저장소에서 Pages가 사용 가능한 GitHub 요금제인지 확인한 뒤, 저장소 `Settings → Pages → Build and deployment → Source`에서 **GitHub Actions**를 선택하고 저장해야 한다. Pages가 허용되지 않는 요금제라면 별도 PUBLIC 저장소/호스팅 설계가 필요하므로 PRIVATE 소스 전체 공개나 `wonhwipark/L1Work` 임의 게시로 우회하지 않는다.

- 설정 화면: https://github.com/wonhwipark/CoWork-Skill-Collab/settings/pages
- 이후 GitHub `Actions → CoWork public synthetic-only Pages release → Run workflow` 수동 1회 실행.
- 실행 성공 이후에만 웹페이지의 실제 `page_url`과 HTTP 200/본문 SHA-256을 검증하고 `PUBLICATION=PASS`로 승격한다.
- 사용자 설정 전 자동 무한 재시도·Pages 자동 활성화용 추가 키 생성·새 유료 서비스 연결은 하지 않는다.

## 4. PRIVATE 대시보드·협업 전환의 현재 구분
- PRIVATE 대시보드: `collab/dashboard/VIEW.md` (GitHub 로그인 후 직접 렌더링), `index.html`, `SUMMARY.md`, `state.json` 및 `.github/workflows/cowork-dashboard.yml` 구현·기존 Actions 자체시험 PASS.
- GitHub 리뷰 파일 실제 이관은 미완료. GitHub에 관측되는 REVIEW/RECEIPT 0은 Dropbox LIVE의 과거 리뷰 0건을 뜻하지 않는다.
- Windows 감시기의 Claude 독립 리뷰 운송은 별도 전환 프로젝트 관리, SHADOW/보안·신뢰 게이트와 LIVE 승인 전이므로 기존 Dropbox LIVE 유지.
- 공개 샘플 Pages 작업은 **대시보드 프레젠테이션만** 다루며, Windows watcher/provider 전환 승인이 아니다.

## 5. 판정
`PUBLIC_SAMPLE_SOURCE=VERIFIED`, `PUBLIC_WORKFLOW_POSTED=PASS`, `ACTIONS_STATIC_BUILD=PASS`, `PAGES_SETUP=BLOCKED_DISABLED_OR_UNAVAILABLE`, `PUBLIC_URL=NOT_AVAILABLE`, `PUBLIC_HOST_E2E=NOT_RUN`, `INDEPENDENT_REVIEW=NOT_RUN`, `CUTOVER=MIGRATION_NOT_CUTOVER`.

**다음 한 동작:** GitHub 저장소의 Settings → Pages에서 Source=GitHub Actions 설정. 가능하면 그 뒤 승인된 고정 샘플 배포 워크플로를 한 번만 재실행하고 실제 URL 검증. 새로운 PRIVATE 협업 데이터의 자동 공개는 계속 금지.

## 6. 최종 재조회 보강 — 기존 PRIVATE 자동화 영향 없음
- 이번 상태 문서·배포 게이트 갱신으로 트리거된 PRIVATE 대시보드 Actions [#43042614707](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/43042614707), [#43042707103](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/43042707103)은 모두 `completed/success`로 원격 확인. PRIVATE 대시보드 자동 갱신 기능에 대한 이번 변경의 직접적인 실패 증거는 없음.
- 공개 Pages 별도 배포 워크플로 #43042181335는 `failure`이고 `PUBLIC_URL=NOT_AVAILABLE`을 유지. 두 Actions의 판정은 서로 독립.
