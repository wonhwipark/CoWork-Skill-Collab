# B안 대시보드 — 상태 정합성 및 자동 갱신 검토 r0001

- 기준: 2026-11-15 KST / 기존 Work: `COWORK-GITHUB-DASHBOARD-20261111-001`.
- 대상: PUBLIC `wonhwipark/L1Work/main/docs/cowork-dashboard/`와 PRIVATE `wonhwipark/CoWork-Skill-Collab/main`의 읽기 전용 상태 생성·동기화 계약.
- 성격: **현재 원격 소스·상태 직접 대조 + 정적 코드 경로 검토**. 별도 자동화·코드 패치·운영/공개 정책 변경·유료 독립 리뷰를 실행하거나 성공으로 주장하지 않는다.
- 사전: [B안 배포 결과](B_STYLE_PUBLIC_UI_DEPLOY_RESULT_r0001_20261115_KST.md) 및 [기존 발표 정합성 설계](PRESENTATION_DASHBOARD_DESIGN_r0001_20261115_KST.md) 재사용.

## 1. 실제 확인한 데이터 및 상태

| 대상 | 직접 확인한 원격 상태 | 근거 Git blob |
|---|---|---|
| 이관 운영 정본 `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md` | 최신 섹션 `ACTIVE_PROVIDER=GITHUB`, `CUTOVER=LIVE`; Windows 호스트 보고·GPT 판정 수용, 장기 운영/첫 신규 실전 이벤트는 별도 | `400a58c29ed29bace8b627275da2cd2c8598c4b1` |
| PRIVATE `collab/dashboard/state.json` | `live_provider=GITHUB`, `operations.active_provider=GITHUB`, `operations.cutover=LIVE` **동시에** `phase=MIGRATION_NOT_CUTOVER` | `a6b2bfd6cf04bff957d0cec53faf282dbde5275d` |
| PUBLIC `docs/cowork-dashboard/status.json` | `checks.active_provider=활성 리뷰 제공자 없음`, `cutover=정식 전환 전`, `generated_at=2026-11-14T16:20:47Z`(11/15 01:20:47 KST); 5개 허용 Work 카드 | `23538934ab6a9af55c337a0893fe803041e811ff` |
| PUBLIC B안 HTML/JS | `index.html` 및 `board.js` 게시·원격 확인, 120초 JSON 폴링·복귀 갱신 구현, 6시간 이상 구형 자료 경고 | `f07b745974adf5e526b622b2efe4edaa695c9d23` / `94b38b2f10fad2887467c082d6fed27adf2bc194` |
| PUBLIC Pages 빌드 | B안 대상 `#43706148759` `completed/success`(기존 배포 검증); Pages URL의 실제 HTTP 본문 수신은 이번 도구에서 확인 불가 | [Pages Actions](https://github.com/wonhwipark/L1Work/actions/runs/43706148759) |

정적 대조: `PRIVATE GITHUB/LIVE`와 `PRIVATE phase=MIGRATION_NOT_CUTOVER`, `PUBLIC NONE/전환 전`의 상호 모순 **확인**. PUBLIC 생성 시각은 기준 시점(11/15 20:16 KST) 약 18.9시간 경과하여 B안 경고 기준 6시간 초과.

## 2. 자동 갱신 실제 설계·결함

| 구간 | 구현된 동작 | 검토 판정 |
|---|---|---|
| PRIVATE `main`의 Work/REQUEST/REVIEW/RECEIPT 갱신 | `.github/workflows/cowork-dashboard.yml` 경로 필터 → 표준 unittest/생성기 → `collab/dashboard/state.json` 등 생성 → 비강제 push | **트리거·코드 존재 확인**. 최신 실제 Actions run 성공은 조회 불가 |
| PRIVATE 생성 → PUBLIC 반영 | `cowork-public-status-sync.yml`의 `workflow_run`/수동 트리거 → 최신 trusted main checkout → 단위시험/`generate.py`/`public_sync.py prepare` → PUBLIC 전용 토큰으로 승인된 `status.json`만 갱신·readback | **코드 경로상 차단 결함**. 현재 run 로그를 직접 읽어 특정 실패 로그로 확정하지 않음 |
| 공개 업무용 JSON 생성 | `generate.py:build_state`가 `phase=MIGRATION_NOT_CUTOVER` 고정; `public_sync._read_active_provider`가 NONE/DROPBOX만 허용하고 GITHUB에 `SafetyBlock`; `build_payload`도 구형 `MIGRATION_NOT_CUTOVER`/전환 전 상태만 수용 | **P0 BLOCKING**. GITHUB/LIVE 상태에서는 소스 수정 없이는 최신 운영 상태를 정상 표현할 수 없음 |
| TRACKER 상태 매핑 | `work_tracker._registered`는 `self_test`/ `independent_review`를 enum으로 검사; 불일치시 fallback, `next_action` 165자 제한 | **P1 정합성 결함**. L1 RAG Tracker의 긴 설명 필드와 비표준 리뷰값 때문에 정형 단계·담당·후속정보가 오독될 수 있음 |
| 브라우저 수신 | B안 `board.js`가 `status.json`/`handoffs.json` 최초/120초마다/탭 복귀 시 읽고 allowlist 검사. 새로운 PRIVATE API/계정/모델 호출 없음 | **POLLING 구현 확인**. JSON 생성이 막히면 화면 새로고침으로 복구 불가능 |
| 시각 최신성 | `public_sync.publish_public`는 의미 있는 필드가 같으면 `generated_at`만 바뀌어도 `UNCHANGED` 반환. 반면 B안 `fresh()`는 `generated_at` 6시간 초과 시 경고 | **P1 의미 충돌**. 마지막 데이터 변화 시각과 성공적으로 상태를 재점검한 시각은 다름 |
| TODO·인계 갱신 | PUBLIC TODO 화면은 **5개 비식별 업무 범주의 다음 행동** 재사용; `GPT_TODO.md`는 PRIVATE 정본이며 그 원문은 PUBLIC exporter에 없음. `handoffs.json`은 PUBLIC `handoffs/*.md` 변경 시 별도 워크플로로 최근 3건 생성 | 기존 계약에 부합. 실제 `TD-001~004` 자동 공개로 과장 금지. 새 PUBLIC 필드 추가는 별도 승인 범위 |

추가로 `PUBLIC_WORKS`의 `next_action`은 현재 정해진 정적 허용 문구다. CURRENT의 변경을 모두 실시간 상세 조치로 반영하는 기능이 아님. `phase_index` 역시 단계 위치이지 실제 완료 비율이 아니다.

## 3. 최소 수정 방향과 시험 게이트

**P0 — 동일 소스의 상호 일치하는 상태 매핑**

1. PRIVATE generator는 최신 이관 CURRENT의 **명시적 운영 판정·근거**만 읽어 `GITHUB/LIVE` 또는 유효한 구형 상태를 생성. 과거 `MIGRATION_NOT_CUTOVER`를 상수로 유지하지 않는다. 운영 호스트 보고 수용과 실제 신규 유료 리뷰 완료를 구분.
2. PUBLIC exporter는 특정 확인된 `GITHUB/LIVE` 조합만 **고정 비식별 한글 라벨**로 매핑하도록 기존 정책 승인/리뷰 후 최소 확장. NONE/GITHUB·LIVE/DROPBOX·미확인 상충, 조작된 CURRENT/예상치 못한 값은 **fail-closed**. `ACTIVE_PROVIDER`만 따로 발견됐다고 전체 CUTOVER 승인으로 간주하지 않음.
3. `work_tracker`/L1 `TRACKER.json`의 필드 타입과 enum을 실제 현행 계약으로 정리. 시험 세부사항과 후속 액션의 긴 문단은 CURRENT에 보존, TRACKER에는 `PASS/FAIL/SKIP/NOT_RUN/NOT_VERIFIED`와 정형 단계·짧은 다음 한 행동만 유지. 상세 히스토리 무손실.
4. PUBLIC `status.json`은 기존 **5개 허용 업무 범주**만, 기존 URL·`handoffs.json` 최근 3건 보존. PRIVATE ID/TODO·승인/READY/Receipt·비용/키/링크/원문은 내보내지 않음.

**P1 — 마지막 상태변경 시각과 마지막 점검 시각 분리**

- `generated_at`은 현재 의미를 명확히 규정(실제 해당 PUBLIC snapshot 생성 시각); `last_verified_at` 등 점검 근거는 별도 허용 필드/고정 정책·출처·검증이 준비된 경우에만 도입. 단순 화면 폴링을 원본 점검 성공으로 표기하지 않는다.
- 정기 heartbeat를 무분별하게 게시하지 말고, 기존 Action의 검증 성공·게시 여부와 화면 데이터의 마지막 변화/최종 근거 시각을 **서로 다르게** 표시. 스냅샷이 오래됐다는 이유만으로 운영 provider가 OFF라고 판정하지 않는다.
- 별도 신규 cron/watcher/알림 생성은 현재 요청 범위가 아니므로 **DEFER**.

**P2 — 자동 동기화 수용 시험(실 실행 이전엔 NOT_RUN)**

- 정상 `GITHUB/LIVE`, 유효 구형 NONE/전환 전, 서로 모순되는 판정·미지 provider, 변조/만료 입력, 잘못된 Tracker enum, 유효 Reviewer/호스트 미실행, 6시간 무변경 등 합성 회귀.
- PRIVATE unit test + 공개 allowlist/정적 보안 스캔 PASS 후 **기존** GitHub Actions 1회 정상 변경 이벤트 → PUBLIC 상태 JSON 새 commit/내용/readback → Pages build SUCCESS → 실제 Pages HTTP/PC·모바일 브라우저 본문·120초 반영 확인.
- `REQUEST/READY` 등록·서명·유료 독립 리뷰/운영 DB/Watcher/Job/Knowledge 변경 없음. UI 수정의 독립 리뷰는 기존 설계 리뷰와 별도 결과·영수증이 확인되어야만 PASS로 기록.

## 4. 이번 판정

- `STATUS_CONSISTENCY=FAIL` (동일 원본의 세 레이어 충돌 직접 관측).
- `AUTOMATION_TRIGGER_DESIGNED=PASS_STATIC`, `BROWSER_POLLING=PASS_STATIC`.
- `PUBLIC_STATUS_END_TO_END_CURRENT=NOT_VERIFIED`, 최근 정상 공개 JSON 반영은 구형 전환 상태만 관측.
- `ROOT_CAUSE_CODE_PATH=IDENTIFIED_STATIC`; **최신 PRIVATE Actions run 실패 로그 조회 불가**이므로 실제 run 오류 메시지로 확정하지 않음.
- `CODE_PATCH=NOT_RUN`, `NEW_PUBLIC_POLICY=NOT_APPROVED/NOT_RUN`, `PAGES_DATA_REFRESH=NOT_RUN`, `NEW_PAID_REVIEW=0`; 기존 GITHUB LIVE 운영 변경 없음.

**NEXT_ONE_ACTION:** 기존 대시보드 Work에서 P0 `generate.py` + `public_sync.py` + 관련 회귀시험을 PRIVATE 후보로 최소 보완하고, L1 Tracker enum을 현행 근거에 맞춰 최소 정규화. 공개 허용목록·독립 리뷰 계약을 확인한 뒤 **기존 PUBLIC status.json만** 안전하게 게시·원격/화면 E2E 확인. B안 HTML을 다시 교체하거나 별도 포털·Watcher를 신설하지 않음.
