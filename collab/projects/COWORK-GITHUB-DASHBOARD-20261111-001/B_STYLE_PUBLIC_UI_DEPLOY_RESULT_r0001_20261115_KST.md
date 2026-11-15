# B안 공개 대시보드 GitHub Pages 반영 결과 r0001

- 기준: 2026-11-15 KST.
- Parent Work: `COWORK-GITHUB-DASHBOARD-20261111-001`.
- 사용자 명시 지시: 확정된 B안으로 현재 대시보드를 교체하고 GitHub PUBLIC 갱신·검증까지 이 창에서 진행.
- 입력: [B안 선택·공개 게이트](B_STYLE_SELECTION_AND_IMPLEMENTATION_r0001_20261115_KST.md), [발표용 기존 설계](PRESENTATION_DASHBOARD_DESIGN_r0001_20261115_KST.md), 현재 PRIVATE CURRENT 및 [기존 공개 허용 정책](../../dashboard/PUBLIC_PAGES_DEFAULT_POLICY.md).
- **배포 판정:** B안 UI·기존 범주로 제한된 PUBLIC 게시 `POSTED`, 원격 본문 `PASS`, Pages build/deploy `SUCCESS`. 실제 GitHub Pages URL HTTP 본문·모바일 사용자 브라우저 E2E는 본 도구에서 직접 검증되지 않아 `NOT_VERIFIED`.

## 1. 실제 PUBLIC 변경·원격 검증

- 저장소: `wonhwipark/L1Work`, branch `main`, 기존 URL `https://wonhwipark.github.io/L1Work/cowork-dashboard/`.
- 신규 `docs/cowork-dashboard/board.js`: commit `5a80688019a98f6bfeb73a9f83a6392bd8146530`, 원격 Git blob `94b38b2f10fad2887467c082d6fed27adf2bc194`, raw UTF-8 **9,662 B**, SHA-256 `35da73bc86422b77fe50d337a6d4a3f8a250c0eaef2079bd15fbff5911c976ce`.
- 기존 `docs/cowork-dashboard/index.html` 교체: commit `31ac017d56fecca6522469d790891909a2d5eea8`, 원격 Git blob `f07b745974adf5e526b622b2efe4edaa695c9d23`, raw UTF-8 **14,606 B**, SHA-256 `604330b13c438bfc5a487a2ede65fe5b1e6518e788279d850391cc4159a78b75`.
- 두 파일은 local tested bytes를 등록 후 GitHub `fetch_file`로 원격 본문 완전 일치 확인.
- Pages: `https://github.com/wonhwipark/L1Work/actions/runs/43706148759`, target commit `31ac017...`, `completed/success` 확인. JS 선행 commit의 취소된 Pages 중간 빌드는 index 최종 빌드 성공으로 대체됨.
- 기존 `status.json`, `status.js`, `handoffs.json`, 기존 Actions/exporter/PUBLIC 허용 정책·GitHub README/URL **불변**. 부가 Site·DB·서명/READY·모델 호출·호스트 작업 없음.

## 2. 구현 기능

- B안 단독(보드 우선, 표·검색·선택형 상세). A/B 전환 없음.
- `01 협업 전체`: 기존 5개 공개 업무 범주만 `status.json`에서 읽고, 상태 위치별 보드와 표·검색·상세(기존 정형 test/review/next_action) 제공. 전체 협업 주체/전달 **개념도** 포함.
- `02 L1 지식 설계`: Module→Feature/Procedure→Scenario 분류와 Workflow/Kernel→분석→Evidence→Updater 후보/Preview→보완·승인→그룹 게시/readback→역링크·재사용의 7단계 선택형 구조도. 실제 실행 성공 상태 아님을 명시.
- `03 TODO / 후속 업무`: 승인된 **5개 공개 업무 범주**의 다음 행동만 제공. PRIVATE `TD-001~004` ID/우선순위/Work/Request ID/PRIVATE 링크는 **미공개**, 정확한 GPT TODO 정본은 PRIVATE `collab/GPT_TODO.md`. 기존 PUBLIC `handoffs.json`의 최근 3건 인계 이력도 유지(개별 리뷰 완료 추정 금지).
- 동기화: 같은 출처 `status.json`/`handoffs.json`을 최초 로딩·120초 주기·focus/visibility 복귀 시 읽음. PUBLIC data 스키마/5개 category/title/enum/문자열 길이 검증, 변조·알 수 없는 category는 카드 전체 미출력. DOM textContent 사용, HTML 주입 금지. CSP `default-src 'none'; script-src 'self'; connect-src 'self'` 유지.
- P0 운영 표시 안전장치: 기존 PUBLIC `status.json`의 `generated_at=2026-11-14T16:20:47Z`는 PRIVATE GitHub/LIVE 최신 판정과 불일치. **실제 상태값을 임의 보정하거나 구형 `NONE`을 현행으로 표시하지 않고**, 수신 JSON이 6시간 초과 시 “공개 상태 자료 오래됨/운영·리뷰 판단 보류” 안내. 기존 PRIVATE→PUBLIC provider/Tracker mapping 결함은 미수정·별도 남은 문제.

## 3. 직접 시험

| 시험 | 결과 |
|---|---|
| HTML/JS 구문·CSP·개인 식별/PRIVATE ID 정적 스캔 | `PASS` |
| Chromium Playwright viewport 1440×900, 1366×768, 390×844 | `PASS` |
| 3개 탭·보드↔표·검색·상세 열기/닫기(Escape) | `PASS` |
| L1 설계 7단계·Module→Feature→Scenario · TODO 공개 5건·인계 2건 합성 입력 | `PASS` |
| 모바일 가로 overflow 0 / runtime error 0 | `PASS` |
| allowlist unknown category·HTML 입력·인계 경로 조작 차단 | `PASS` |
| GitHub PUBLIC 두 파일 원격 본문 readback | `PASS` |
| GitHub Pages action complete/success | `PASS` |
| 공개 URL 실제 HTTP 페이지/body 검사·실 사용자 브라우저 검증 | `NOT_VERIFIED` |
| 기존 PRIVATE→PUBLIC 데이터의 P0 최신 provider/Tracker 정합성 수정 | `NOT_RUN` |
| B안 변경의 Windows Claude Code 독립 리뷰 | `NOT_RUN` |
| 실제 업무 L1 host/Knowledge/RAG E2E | `NOT_RUN` |

로컬 브라우저 시험은 GitHub 원격 내용과 일치하는 정적 원본을 제공했을 때의 테스트이며 GitHub Pages CDN 실제 수신의 직접 확인이 아님.

## 4. 남은 검증·조치

1. **운영 서비스 단일화:** `GITHUB/LIVE` 호스트 판정을 구형 PUBLIC `NONE`과 안전하게 정합화하려면 기존 exporter/Tracker enum의 P0 최소 수정, 관련 독립 리뷰·공개 allowlist 판정·동기화 E2E가 별도로 필요. 이번 UI 변경으로 자동 해결됐다고 보고하지 않음.
2. **PUBLIC TODO 범위:** PRIVATE 상세 TD를 공개하려면 별도 허용 판정이 필요. 이번 B안은 공개 업무 요약으로 제한.
3. **독립 리뷰:** 기존 고정 요청 `REQ-COWORK-DASHBOARD-PRESENTATION-20261115-001`은 설계 리뷰이며 B안 UI 구현을 리뷰했다고 취급할 수 없음. 기존 REQUEST/ZIP/SOURCE_PIN·서명·READY 그대로 보존, 유료 호출 0.
4. **실제 Pages HTTP 검증:** GitHub Actions 성공을 확인했지만 실행 중인 공개 URL은 웹 수신 도구 제한으로 본문 직접 확인 불가. `NOT_VERIFIED` 유지.

**NEXT_ONE_ACTION:** 동일 Work의 기존 P0 상태 데이터 연결 문제를 별도 검토·시험하고 유효 독립 리뷰/공개 승인 범위를 충족한 후 기존 `status.json` 갱신을 복구. 이미 승인된 B안 선택·HTML 배포는 반복하지 않음.
