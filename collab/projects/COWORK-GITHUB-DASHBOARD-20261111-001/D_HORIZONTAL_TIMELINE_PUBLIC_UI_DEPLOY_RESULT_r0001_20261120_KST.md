# D안 가로 타임라인 — 기존 CoWork PUBLIC 대시보드 최소 적용 결과
기준: 2026-11-20 KST / 사용자 요청: 기존 현재 대시보드만 먼저 정리하고 배포까지.

## 현재 판정
- `PUBLIC_SOURCE_POSTED=PASS`: `wonhwipark/L1Work/main/docs/cowork-dashboard/index.html`, `board.js` 원격 내용 재조회·정확 일치.
- `PAGES_BUILD_AND_SERVED_HTML=NOT_VERIFIED`: 현재 접근 가능한 GitHub connector는 workflow run 목록·서비스 HTTP 렌더를 직접 검증할 수 없음. 기존 URL은 유지됐지만 새 커밋의 Pages 서비스 완료를 과장하지 않음.
- `STATIC_JS_AND_SYNTHETIC_DOM=PASS`, `REAL_BROWSER_DESKTOP_MOBILE=NOT_RUN`, `INDEPENDENT_REVIEW=NOT_RUN`. 새 모델 리뷰/REQUEST/READY·Windows/LIVE/업무 Job 호출 0.

## 변경 범위
- 기존 3개 탭 중 **협업 전체**의 기본 업무 표시를 가로 타임라인으로 전환. 각 Work는 한 행; 진행 스킬·운영 3개, 설계·대시보드 2개 그룹.
- 표 머리글: 설계 → 개발·시험 → 리뷰 요청 → 독립 리뷰 → 게시·운영. 강조되는 점은 실제 완료가 아니라 **`status.json.phase_index`에 따른 기록 위치**. phase_index가 명확한 단계로 매핑되지 않으면 강조하지 않음. 이전 단계는 PASS로 추정하지 않음.
- 검색/현재 상세 drawer/보드·표 토글/L1 지식 설계 13단계/TODO/최근 인계3건/120초 재조회 유지.
- 공개 허용목록 5개, PRIVATE→PUBLIC exporter, `status.json` schema와 bytes, watcher·서명·승인·운영 DB·스킬 ZIP 변경 없음. PUBLIC에 개별 Work ID, REQ ID, PRIVATE 리뷰 본문·버전·영수증 신규 공개 0.

## PUBLIC 게시 근거
| 파일 | 원격 커밋 | Git blob SHA | UTF-8 SHA-256 |
|---|---|---|---|
| `docs/cowork-dashboard/board.js` | `03eb9ced1b0d7faf77285b8b10f2c9af980d674e` | `cb3f4cc96c2193d60f3900f3cc216f11a2f61303` | `553f55bf74c423fed68c5b9485855f3268ff8653b6f6bd505a69d2f31f951000` |
| `docs/cowork-dashboard/index.html` | `e92aec4529e13e0174379d33f8f2173692725480` | `c4f3fdab1fab32462e2015a19384069767df16a7` | `eed21579d61ea6c2fab081f91fb3c550edf8875cef6b81951755337e1392905d` |

- 기존 공개 데이터 `status.json` Git blob `983f2c88a72d88cbe0a2e15678693c47d7c2a46c` 내용 불변.
- 기존 URL: https://wonhwipark.github.io/L1Work/cowork-dashboard/
- HTML과 JS는 각 수정 후 PUBLIC main 최신 원문을 다시 읽어 게시 입력과 문자열 전체 일치 확인. ZIP 신규 생성 없음.

## 직접 확인한 시험
- V8 JavaScript 구문 PASS 및 공개 스키마와 5개 승인 범주 검증 PASS.
- 합성 DOM: 그룹 2 / 진행 스킬·운영 3행 / 설계·대시보드 2행 / 전체 5행 / 단계 셀 25개 / 표시 위치 4개·UNKNOWN 1개 PASS.
- 기존 탭 3개 보존, 모바일 그룹별 가로 스크롤 CSS, PRIVATE REQUEST ID 미노출, 다른 단계의 PASS 추정 없음. 총 9개 불변식 PASS.
- 실제 GitHub Pages build run·served HTML HTTP·PC/모바일 픽셀·상호작용 E2E는 `NOT_VERIFIED/NOT_RUN`.

## 공개 상태의 기존 한계
- `status.json`의 일부 운영 전환 표기가 PRIVATE CURRENT 최신 host 보고와 다를 수 있음. 이번 UI 변경만으로 데이터 정합성이 고쳐진 것은 아님.
- 개별 스킬 릴리스 버전/리뷰 요청 ID는 기존 PUBLIC JSON 계약에 없으므로 공개 화면에서 생성하지 않음. 필요 시 기존 PRIVATE 정본과 공개 허용범위를 별도 판정.
- `phase_index=5`도 '게시 완료' 증빙이 아니라 신고 위치임. drawer 내 자체시험·리뷰 라벨은 현재 공개 데이터를 그대로 사용.

## NEXT_ONE_ACTION
L1Work GitHub Pages 최신 배포 성공·서비스 화면을 PC/모바일에서 확인하고, 5건 전체 표시·2개 그룹·모바일 가로 이동·기존 3개 탭 회귀를 확인. 확인 전 `PAGES_RENDER=NOT_VERIFIED` 유지. 본 작업의 추가 리뷰 요청·운영 변경·공개 데이터 확대는 없음.
