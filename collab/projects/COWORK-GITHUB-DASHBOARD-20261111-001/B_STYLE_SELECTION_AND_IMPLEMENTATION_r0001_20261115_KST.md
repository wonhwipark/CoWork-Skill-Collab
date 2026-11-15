# B안 확정 — CoWork 통합 운영 화면 UI 선택·후속 구현 판정 r0001

- 기준: 2026-11-15 KST / 기존 Work `COWORK-GITHUB-DASHBOARD-20261111-001`.
- 사용자 결정: A/B 비교 후 **B안(GitHub Projects형 보드·표 우선)이 더 읽기 쉬우므로 B안으로 진행**.
- 관련 고정 설계: [발표용 대시보드 r0001](PRESENTATION_DASHBOARD_DESIGN_r0001_20261115_KST.md), [본 Work 최신 CURRENT](CURRENT.md).
- 이 문서는 **B안 선택·개발 시제품 및 PUBLIC 전환 게이트**를 기록하며, 기발행 독립 리뷰의 SOURCE_PIN/REQUEST/승인 범위를 수정하거나 실행시키지 않는다.

## 1. 사용자가 확정한 화면 구조

- **B안 단독 적용:** A/B 모드 전환은 운영 후보 화면에서 제거한다. 동일 목적의 2개 포털 신설 없이 기존 GitHub Pages CoWork 대시보드의 상호작용 패턴으로 적용할 방향.
- **서브화면 3개:** `01 협업 전체`(단계별 Work 카드, 보드/표, 검색, 현재 책임·다음 행동), `02 L1 지식 설계`(요청/분석/Work·Evidence/Updater/보완·승인/그룹 게시/역링크·RAG 7단계와 Module→Feature→Scenario), `03 GPT TODO`(TD-001~004의 실제 완료 범위와 다음 행동).
- **상세 패널:** 업무 또는 TODO 선택 시 검증된 완료, 현재 대기·차단, 담당, 다음 행동, PRIVATE 정본 근거(접근권 있는 사용자만) 표시. 페이지에서 개발·승인·READY·Job 등을 직접 실행하는 버튼은 두지 않는다.
- **표시 수준:** 문서 완료 ≠ 독립 리뷰 완료 ≠ PUBLIC 배포 ≠ Linux 코드 분석/지식 게시 ≠ RAG 활용. 검증 근거 없이 과거 완료 상태를 승격하지 않는다.

## 2. 독립 로컬 HTML 후보 — 직접 시험

- 파일명: `CoWork_B_Selected_r0003_20261115_KST.html` (**이번 대화 로컬 전달물, GitHub 미게시**).
- 46,101 bytes / SHA-256 `ea996809c470a84b115c1cf10a5adb1472e2fac9138bd329c5c7b3b4f1390414`.
- ZIP(로컬 전달물): `CoWork_B_Selected_r0003_20261115_KST.zip`, 14,271 bytes / SHA-256 `bf3e5708963d74072b92a1028742a726898bfca99e47f6d654b25ef2bd151b64`. **릴리스/스킬 패키지 아님**.
- Playwright 격리 브라우저 검증 1440×900, 1366×768, 390×844: 세 탭, 6개 Work, L1 7단계, TODO 4개, 보드/표, 검색, 상세 오버레이, Escape, 가로 넘침 없음 **PASS**. 이 결과는 로컬 샘플의 기능시험에 한정한다.
- 파일은 2026-11-15 PRIVATE 문서의 고정 스냅샷이며 **실시간 조회·PUBLIC Pages·실호스트 실행 아님**. PRIVATE ID/원문 링크가 있으므로 그대로 PUBLIC에 올릴 수 없다.

## 3. PUBLIC 도입 전제와 위험

- 기존 PUBLIC 기본 URL `https://wonhwipark.github.io/L1Work/cowork-dashboard/`와 `docs/cowork-dashboard/index.html`/`status.js`/`status.json` 및 기존 exporter/Actions/120초 폴링을 **REUSE**한다. 별도 Sites·DB·상시 watcher·GitHub Projects 중복 원장 신설 없음.
- **공개 허용 목록 유지:** 현재 PUBLIC은 기존 5개 비식별 범주·고정 정형 라벨만 허용. PRIVATE `TD-001~004` 작업 ID, Work/Request ID, PRIVATE URL, 리뷰 Receipt·비용·원문을 PUBLIC에 복사할 수 없다. TODO 공개 표시는 별도의 허용 범주·필드 심사 또는 PRIVATE 접근 전용 화면으로 분리해야 한다. 사용자의 B안 선택이 신규 PUBLIC 내용 반출 승인을 자동 포함하지 않는다.
- **P0 상태 연결:** 현재 PRIVATE 이관 CURRENT의 `ACTIVE_PROVIDER=GITHUB/CUTOVER=LIVE` 호스트 보고 수용과 기존 PUBLIC `status.json`의 구형 `NONE/전환 전` 표시가 불일치. 기존 `PRESENTATION_DASHBOARD_DESIGN_r0001`의 P0 안전 매핑·tracker enum·fail-closed를 먼저 해결해야 하며, 단순 HTML 교체로 최신 운영 표시를 보장하지 않는다.
- **독립 리뷰 게이트:** 이전 `REQ-COWORK-DASHBOARD-PRESENTATION-20261115-001` 고정 review input은 **B안 선택 전 설계**다. 요청/입력 ZIP·SOURCE_PIN을 변경하지 않는다. 그 리뷰가 진행되더라도 새 HTML 구현의 독립 리뷰 PASS라고 소급하지 않는다. 신규 리뷰/유료 호출은 현재 실행하지 않는다.
- **모바일/접근성:** 390px 최소 검증, 색과 글자 병용, 키보드 및 클릭 탐색, 스냅샷 시각 고지, 원본 확인 시각과 브라우저 수신 시각 분리.

## 4. 이번 결과 및 다음 행동

| 항목 | 실제 판정 |
|---|---|
| 사용자 디자인 선택 | B안 확정 |
| 로컬 HTML 구현 및 UI 시험 | `PASS` (위 범위) |
| PRIVATE 설계 결정 기록·원격 readback | 아래 게시 이후만 완료 |
| 기존 독립 리뷰 실행 | `NOT_RUN` (기존 REQUEST/READY 상태 유지) |
| PUBLIC 정책/코드 수정·Pages 교체 | `NOT_RUN` |
| GitHub LIVE·서명·Watcher/Job/Knowledge 변경 | `NOT_RUN` |

**NEXT_ONE_ACTION:** 같은 기존 대시보드 Work에서 B안 UI를 기존 PUBLIC 허용목록 전용 렌더링/PRIVATE 상세 뷰로 분리하는 최소 변경을 설계·구현한다. 먼저 P0 provider·Tracker 표시 정합성과 새 TODO 노출 범위를 확인하고, 유효한 독립 리뷰·PUBLIC 승인 범위 충족 전까지 실제 대시보드 교체를 하지 않는다. 사용자의 B안 선택을 반복 질의하지 않는다.
