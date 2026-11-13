# CoWork Executive v2 — 가독성·운영 정확성 개선 통합 결과

- 기준: 2026-11-13 KST
- 사용자 승인: 현재 Executive 기본 대시보드를 유지한 채 P0 운영 정확성, P1 Work별 가독성·시각적 우선순위, P2 모바일·검색·필터 개선
- PUBLIC 기본 HTML: https://wonhwipark.github.io/L1Work/cowork-dashboard/
- **현재 결론:** DEVELOPMENT=IMPLEMENTED / SELF_TEST=PASS / PUBLIC_PAGES_DEPLOY=PASS / INDEPENDENT_REVIEW=NOT_RUN / LIVE_CUTOVER=MIGRATION_NOT_CUTOVER
- **운영 리뷰 제공자:** PRIVATE 이관 CURRENT 최신 섹션 `ACTIVE_PROVIDER=NONE` 근거; Dropbox watcher/Bridge/Updater 비활성화 자체보고가 있으며 **리뷰 ACTIVE_PROVIDER=NONE**, Pages 상태 자동 업데이트와 분리

## 변경 내역

1. **P0 운영 상태 정확성:** PUBLIC JSON의 `checks.active_provider`를 PRIVATE 이관 `CURRENT.md` **최신 섹션**에서 제한적으로 추출. `NONE` → `활성 리뷰 제공자 없음`, 누락 → `기록 미확인`, 미승인/상충 값 → fail-closed. 이전 `기존 운영 경로 유지` 오표기 제거. `MIGRATION_NOT_CUTOVER` 유지.
2. **P0 공개 범위 명확화:** PRIVATE Work 전체 6개와 승인된 PUBLIC 카드 5개의 차이를 `전체 Work 6 / 공개 5 / 비공개·미승인 1`로 표시. 비공개 Work 이름·ID·원문은 공개하지 않음.
3. **P1 사용자 조치 우선:** 기존 운송 전환의 차단·승인 항목만 검증된 고정 분류 `action_kind=USER`로 표시, 상단 `내 조치 1` 및 카드 첫 순위에 배치. 그 외 리뷰/차단/일반 작업은 서로 다른 `action_kind`로 정렬·필터; 원문 자유 텍스트를 직접 복제하지 않음.
4. **P1 검색·필터:** 공개 카드의 작업명/단계/공개 다음 조치로 검색, 전체/내 조치/리뷰 대기/차단 필터, 필터 결과 0건 메시지와 초기화. 필터·검색은 HTML 클라이언트의 same-origin JSON에서만 수행.
5. **P1 시간 구분:** 실행 한 번의 고정 UTC `generated_at`를 PRIVATE workflow environment로 전달해 공개 JSON에 반영, 화면은 KST 데이터 생성시각과 최근 웹 수신시각을 각각 표시. **시각만 변경된 경우는 내용 동일 처리**하여 PUBLIC 재게시/Pages 불필요한 재배포를 차단.
6. **P2 시각·모바일:** Executive 헤더 유지, 상단 운영/내 조치/갱신 시각 3패널, 카드 우선순위, 44px 터치 컨트롤, 더 큰 보조 글자, 모바일 단일 컬럼. 7단계 흐름도를 키보드 접근 가능한 기본 `details/summary`로 접기/펼치기. 단계 막대의 과거 구간 음영을 제거해 검증된 PASS로 오해하지 않도록 함.
7. **방어:** PUBLIC `status.js`는 DOM `textContent`/노드 생성만 사용, 제3자/PRIVATE API 호출·토큰 노출 없음. 오류 시 마지막 공개 상태/정적 기본 화면 유지. `COWORK_PUBLIC_DASHBOARD_WRITE_TOKEN`의 기존 권한과 PUBLIC 단일파일 경로 유지.

## 원격 소스 및 검증

- PRIVATE exporter: `wonhwipark/CoWork-Skill-Collab` `main/collab/dashboard/public_sync.py`.
- PRIVATE 테스트: `main/collab/dashboard/tests/test_public_sync.py`. `ACTIVE_PROVIDER` 최신 섹션·상충/미승인 값, GENERATED_AT 검증, 허용 분류와 PRIVATE 원문 누출 차단, 시각만 변경 시 `UNCHANGED` 회귀 추가.
- PRIVATE Action [#43414643041](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/43414643041): **Python 51 PASS**, 공개 합성 보안 **8 PASS**; 합계 **59 PASS / 0 FAIL**.
- PRIVATE → PUBLIC Action [#43414352955](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/43414352955): PUBLIC 상태 실제 게시 PASS; 이후 [#43414675245](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/43414675245)에서 `PUBLIC_SYNC=UNCHANGED` 정합성 확인(중복 게시 생략).
- PUBLIC `L1Work/main/docs/cowork-dashboard/index.html`: Git blob `19d48b9915ce70a95dbe867ab3cf390ee788d93c`, 원격 readback PASS.
- PUBLIC `L1Work/main/docs/cowork-dashboard/status.js`: Git blob `3255ec6f84dfff782473f8008801a44db4391cf4`, 원격 readback PASS.
- PUBLIC `L1Work/main/docs/cowork-dashboard/status.json`: `schema=COWORK_PUBLIC_STATUS_V1`, `generated_at=2026-11-13T11:06:32Z`, `active_provider=활성 리뷰 제공자 없음`, WORK=6/PUBLIC_CARD=5, Work 확인 필요=1. Git blob `ec00b5c58450e196e69ef9c966630a4c9ac65fed`, readback PASS.
- GitHub Pages [#43414793161](https://github.com/wonhwipark/L1Work/actions/runs/43414793161) `completed/success`.
- 실행 JavaScript 구문검사 PASS, HTML 노드 열림/닫힘·ID 대응 검사 PASS. 별도 synthetic DOM 스모크에서 PUBLIC 카드 5개 로드, 내 조치 필터 1, 리뷰 대기 0, `dashboard` 검색 결과 1, 초기화 5 복구 및 `ACTIVE_PROVIDER=NONE` 표시 확인.
- **미실행:** 실제 웹페이지에서 Chromium/모바일 실기기 렌더링 및 터치·HTTP served-body E2E. Actions Pages 배포 성공과 브라우저 화면 시험을 동일하게 주장하지 않음.

## 보안·운영 불변

- 새 승인 범위 없이 PUBLIC Work ID, 내부 피드백, 사내 자료, 검증 키, 비밀, 운영 DB, ZIP 코드 반출 없음.
- Windows watcher/Dropbox LIVE(현재 REVIEW ACTIVE_PROVIDER=NONE)/운영 DB(WAL 포함)/예약 작업/Notifier/Telegram, Claude 독립 리뷰 호출/비용, 협업 GitHub LIVE 전환 **변경 없음**.
- `ACTIVE_PROVIDER=NONE`은 최신 PRIVATE 운영 기록의 상태이며, `live_provider=DROPBOX` 같은 오래된 운송 기본 라벨과 구분해서 표시함.
- `CUTOVER=MIGRATION_NOT_CUTOVER` 유지. 별도 운영/보안 승인 전 새로운 스킬명 공개 허용목록 확대 금지.

## 다음 한 동작

사용자는 PUBLIC 기본 HTML에서 ① 상단 `활성 리뷰 제공자 없음`, ② `전체 Work 6 / 공개 5 / 비공개 1`, ③ `내 조치 1`, ④ 필터/검색 및 7단계 접기·펼치기를 모바일로 확인. 추후 개선은 실제 모바일 렌더링 피드백만 받아 묶어서 보완.
