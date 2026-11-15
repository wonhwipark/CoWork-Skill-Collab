# ⑦ Updater → ⑥ Workspace 화살표 누락 수정 결과 — r0001

- 확인일: 2026-11-15 KST
- Work: `COWORK-GITHUB-DASHBOARD-20261111-001`
- 사용자 지적: 설명에는 Workspace 갱신을 적었지만 실제 플로우에 7 → 6 방향이 보이지 않음. **수용·수정 완료**.
- 원인: 이전 변경은 두 스킬의 역할/설명만 수정했고 렌더러는 영역 간 하향 화살표만 생성. Updater 결과 저장을 나타내는 역방향 연결선 미구현.

## 변경과 현재 상태

- ⑦ `l1-knowledge-updater` 카드 왼쪽에서 출발해 ⑥ `l1-workspace` 카드 왼쪽으로 들어가는 녹색 SVG 실선·도착 화살촉 추가.
- 두 영역 사이에 **⑦ → ⑥ 분석·초안·결정 저장/갱신** 라벨 추가. 선택 시 STEP 6 상세와 해당 저장 경로 설명 표시.
- 기존 ⑥에서 지식 후보 단계로 내려가는 흐름·13카드·5영역·3분기 유지.
- 실제 카드 좌표로 선을 배치하고 L1 화면 복귀/창 크기 변경 시 다시 계산. 모바일에는 좌측 선 공간과 라벨·하향 화살표 분리 CSS 적용.
- 스크립트 URL 개정 표시로 이전 `board.js` 캐시와 구분. 상태 JSON·공개 허용목록·기존 120초 갱신/협업·TODO 로직은 유지.
- PUBLIC commit: `41d151e54651cc030e6ef66c94a7d62f654aec2b`.
- Pages: [#43717660361](https://github.com/wonhwipark/L1Work/actions/runs/43717660361), `completed/success`.
- 실제 브라우저 열람 주소: https://wonhwipark.github.io/L1Work/cowork-dashboard/#l1

## 실제 시험과 근거

| 확인 | 판정 | 직접 확인한 범위 |
|---|---|---|
| JavaScript 구문 | PASS | VM Script 컴파일 |
| 연결선 좌표 함수 | PASS | desktop/mobile 좌표의 출발=7, 도착=6, 상향 방향 및 좌측 경유 합성 확인 |
| 기존 상태/갱신 제어 본문 | PASS | validateHistory 이후 controller 본문 바이트 동일 |
| PUBLIC 파일 readback·실제 SHA | PASS | 원격 UTF-8 본문 일치·Git blob SHA-1 재계산·아래 SHA-256 |
| 실제 Pages 브라우저 표시 | PASS | Cloud Chrome 1363×936. 녹색 선이 7에서 출발해 6으로 들어가는 화살촉과 라벨을 시각 확인 |
| 실제 출발/도착 좌표 | PASS | DOM path `M 224 617.1875 H 206 V 417.1875 H 224`; sourceError=0, targetError=0, upward=true |
| 라벨 클릭 | PASS | STEP 6 선택·Workspace 저장 경로 추가 설명 표시 |
| 다른 화면 → L1 복귀 | PASS | 협업 화면 왕복 후 선 표시 및 라벨 동작 확인 |
| 기존 노드/분기·화면 너비 | PASS | 13 cards / 3 branches, 실제 데스크톱 가로 overflow 없음 |
| 실제 모바일 viewport·창 크기 변경 E2E | NOT_RUN | CSS/합성 좌표만 확인. 실제 기기/모바일 화면 성공으로 확대하지 않음 |
| 업무 호스트 실제 Workspace 저장/readback | NOT_RUN / NOT_VERIFIED | 이번 수정은 흐름도 표시. 실제 스킬 저장 기능 완료로 해석하지 않음 |
| 새 독립 리뷰·설치·Job·그룹 게시 | NOT_RUN | 기존 범위 유지 |

## PUBLIC 실제 바이트

저장소 `wonhwipark/L1Work`, branch `main`:

| 경로 | bytes | SHA-256 |
|---|---:|---|
| `docs/cowork-dashboard/board.js` | 18895 | `2e948cf336b61ba86b8c7607c8bf25730758c9d715e8fda1aad750b0a2331169` |
| `docs/cowork-dashboard/index.html` | 20884 | `254d9faacfdb57b1b6a3a390f7f4d483f7393deca6d08c46c68e92a52e3f176b` |

## 다음 한 동작

기존 대시보드 주소를 새로고침해 ⑦ → ⑥ 녹색 연결선을 확인. 같은 Work에서 발견된 표시 문제만 보완.
