# CoWork 대시보드 — HTML Pages 기본 운영 및 공개 허용 목록

**정책 적용:** 2026-11-12 / **기본 URL:** https://wonhwipark.github.io/L1Work/cowork-dashboard/

## 2026-11-15 B안 상태 정합성 보완 — 고정 비식별 라벨만 허용

- 사용자 지시: B안 공개 대시보드의 오래된 `NONE/정식 전환 전` 표시를 PRIVATE 최신 이관 판정에 맞춰 수정하고, 기존 GitHub Actions 자동 갱신을 검증.
- **허용된 상태의 최소 확장:** 최신 이관 CURRENT와 PRIVATE generated state에서 `ACTIVE_PROVIDER=GITHUB` **및** `CUTOVER=LIVE`가 동시에 확인되는 경우에만 `GitHub 리뷰 운송 LIVE (호스트 보고 수용)` / `GitHub LIVE (호스트 보고 수용)` 고정 문구를 PUBLIC에 사용. 신규 유료 리뷰 실행이나 장기 운영 PASS를 의미하지 않음.
- 모순·미확인 provider/phase, 출처 변조 및 미승인 라벨은 계속 fail-closed. 기존 5개 공개 범주, 인계 최근 3건, 승인된 공개용 수치·문구 외 PRIVATE Work/TODO/REQUEST ID, 결과·Receipt 원문, 토큰, 회사 코드/MSC/링크 공개 불가. 자동 출력 경로는 기존 `status.json` 단 하나.
- `generated_at`은 공개 상태 **마지막 변경** 시각이지 원본 데이터 **마지막 검증** 시각이 아니므로 브라우저가 6시간 이상 무변경을 무조건 실패로 표시하지 않음. 단순 JSON 수신은 PRIVATE 최신 확인 완료의 근거 아님.
- 이전 절의 전환 전 값은 당시 기록. 신규 공개 코드·실제 Actions 실행·독립 리뷰 판정은 관련 Work에 따로 기록.

## 인계·리뷰 추적 확장 — 공개 승인 범위 (2026-11-14 KST)
- **분리된 사용자 흐름:** Work 카드는 업무 목적·진행을, 인계 카드는 문서 게시 → 리뷰 요청 → 결과 접수 → GPT 판정 → 후속 반영을 표시. 단계를 완료율이나 실행/독립 리뷰 PASS로 해석하지 않음.
- **승인된 공개 인계 1건:** L1Work PUBLIC `main/handoffs/L1_KNOWLEDGE_MSC_B_VIEWER_GPT_REVIEW_HANDOFF_r0001_20261114_KST.md` (MSC B 뷰어 설계 리뷰). 초기 단계 `PUBLISHED`, 독립 리뷰 미실행. 이 문서는 실제 Work ID가 아니며 별도 Work를 자동 생성하지 않음.
- **정본과 갱신:** PRIVATE `collab/dashboard/handoff_registry.json`의 승인된 식별자·정형 단계·기준일을 PUBLIC exporter가 엄격 검증하여 `status.json.handoffs`에 고정 제목·문서 URL·상태 라벨·후속 조치만 출력. Registry 변경 → PRIVATE Action → 기존 allowlist PUBLIC sync → Pages; 브라우저 120초/복귀 갱신 재사용. 등록 내용은 실제 인계/리뷰 결과 증거를 확인한 뒤 명시적으로 수정해야 하며 원문 스캔만으로 리뷰 완료를 추정하지 않음.
- **안전:** 새 PUBLIC 링크는 미리 승인된 정확한 L1Work PUBLIC 문서 주소만 허용. 자유 입력 URL/문서 내용/PRIVATE 작업 ID/리뷰 원문/영수증/고객정보는 미출력. 알 수 없는 ID·단계·필드·중복·날짜·변조된 URL이면 fail-closed. 미등록 인계는 PUBLIC로 자동 노출하지 않음.
- **독립 상태:** `ACTIVE_PROVIDER=NONE`, `CUTOVER=MIGRATION_NOT_CUTOVER`; 이번 변경은 watcher/운영 DB/REQUEST/READY/모델 호출/ZIP 게시·LIVE 승인과 무관. 코드 정적/합성시험과 GitHub 원격 readback의 증거는 `COWORK-GITHUB-DASHBOARD-20261111-001/CURRENT.md`에 기록. 실제 모바일 브라우저 시각 시험은 별도.

## 최신 확정 — 자동 갱신 E2E 성공 (2026-11-13)

- **PAGES_DEFAULT=ENABLED / AUTO_PUBLISH_E2E=PASS**. 사용자가 공개 Pages HTML을 열어 둔 상태에서도 `status.js`가 `status.json`을 120초 간격과 포커스 복귀 시 확인. 실제 JSON 상태 변경의 UI 동적 표시가 목표이며 브라우저 실화면 E2E 자체는 `NOT_RUN`.
- **SOURCE_TRIGGER=ENABLED:** PRIVATE `CURRENT.md`, `TRACKER.json`, `collab/projects/**` 내 인계·피드백, `collab/requests/**`, `collab/reviews/**`, `collab/receipts/**` 등의 변경 시 GitHub Actions 자동 검증. 상위 공개 허용 상태 변경이 없는 경우에는 `PUBLIC_SYNC=UNCHANGED`로 중복 게시하지 않음.
- **PUBLIC_SYNC=POSTED_READBACK_PASS 실측:** PRIVATE Work 단계 2→4 입력 `88135a754efa8af2970127013aae879c82ae1431` → PRIVATE Actions [#43251843321](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/43251843321) SUCCESS → PUBLIC sync [#43251880632](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/43251880632) `POSTED_READBACK_PASS` → L1Work Pages [#43251906090](https://github.com/wonhwipark/L1Work/actions/runs/43251906090) SUCCESS. PUBLIC JSON `dashboard.phase_index=4` 원격 재조회 확인. [상세 검증](../projects/COWORK-GITHUB-DASHBOARD-20261111-001/AUTO_PUBLIC_HTML_REFRESH_E2E_20261113.md).
- **연속 갱신 보완:** 과거 stale PRIVATE state 검사 오류를 차단하기 위해 PUBLIC sync Action이 신뢰된 현재 PRIVATE `main`을 checkout한 뒤 `generate.py`를 로컬 실행하고, 그 결과를 공개 허용목록으로 검증. 기존 인증·단일 파일 목적지·원격 readback·불일치 차단 계약 유지.
- **보안 게이트 그대로:** PUBLIC에 추가되는 데이터는 기존 비식별 고정 범주·상태 enum·집계 수치에 한정. 새 미승인 스킬/문서 원문/내부 Work ID/리뷰 영수증/비밀 정보는 공개 금지. 토큰 범위는 L1Work Contents 권한뿐; 공개 `status.json` 단일 파일만 자동 갱신. 자격 증명 만료·삭제·API 실패 시 fail-closed.
- **이하 2026-11-12 이전 섹션의 `BLOCKED_AUTH_PENDING`, `MANUAL_ALLOWLIST_ONLY`, `BOOTSTRAP_NOT_AUTO` 등은 당시 관측 이력**. 현재 자동 게시 판정은 이 최신 섹션을 우선하며, 인증 갱신이 실패하면 다시 BLOCKED로 판정.

## 2026-11-12 갱신 — PUBLIC 자동 요약 승인·인증 게이트

**사용자 최신 지시:** PUBLIC Pages 자동 갱신 요청. 기존의 수동 게시 정책은 아래 **선별된 허용 정보에 한해** 자동 갱신 구현으로 보완. 이 승인으로 PRIVATE 전체 공개·운영 LIVE 전환·유료 리뷰/토큰 임의 발급을 허용하지 않음.

- **AUTO_EXPORTER=IMPLEMENTED:** PRIVATE `public_sync.py`로 `state.json` 재생성 정합성·상태 스키마·전환 상태를 검증한 뒤, 승인된 업무 범주명·정형 phase/검증 요약·집계 수치만 출력한다.
- **AUTO_TRIGGER=IMPLEMENTED:** 성공한 PRIVATE dashboard GitHub Actions 실행 뒤 `workflow_run`으로 별도의 `cowork-public-status-sync.yml` 시작. 독립 수동 재실행도 가능하다. SECRET 누락·정책 불일치 시 PUBLIC 쓰기 차단.
- **PUBLIC_STATUS_JSON=BOOTSTRAP_POSTED:** `L1Work/main/docs/cowork-dashboard/status.json`은 현재 초기 스냅샷(`sync_mode=BOOTSTRAP_NOT_AUTO`)으로 게시됨. `status.js`가 same-origin JSON만 읽고 안전한 DOM API로 KPI·Work 카드를 갱신. GitHub Pages 자동 배포는 동작 중.
- **AUTO_PUBLISH_E2E=BLOCKED_AUTH_PENDING:** 사용자 제공 최소 범위의 SECRET `COWORK_PUBLIC_DASHBOARD_WRITE_TOKEN`이 아직 설치·검증되지 않으면 PRIVATE→PUBLIC 자동 게시가 실행되지 않는다. [인증 설치·검증 인계](PUBLIC_AUTO_SYNC_SETUP.md) 참조. 모델 호출이나 무한 재시도로 우회 금지.
- **승인된 출력 범위:** 기존 다섯 개 비식별 업무 범주 + 이미 공개한 스킬명 예시 `l1-fix-workflow`/`l1-github` (실제 등록된 Work일 때만). 추가 스킬과 내부 Work ID, 직접 FREE-TEXT next_action, PRIVATE 링크, 개인·고객정보, 영수증 등은 무조건 차단. 저장소 `L1Work`의 `status.json` 이외 경로 자동 쓰기는 금지.
- **토큰 권한 제한:** PUBLIC `L1Work` 하나만 선택한 fine-grained token의 Contents read/write. PRIVATE Actions Secret에만 설치. GitHub의 repo 단위 권한이므로 단일 파일만 허용하는 **플랫폼 차원의 ACL은 불가능**하며, exporter 코드의 경로 고정과 원격 readback은 별도 방어 장치.
- **상태 판정 원칙:** 문서에 표시된 `PASS`는 PUBLIC에 실운영 완료로 그대로 표기하지 않는다. 독립 검증·영수증/운영 판정은 별도 게이트. `MIGRATION_NOT_CUTOVER`에서 이탈하면 새 승인까지 PUBLIC 자동 게시 실패 차단.
- **정식 전환 영향:** 기존 Dropbox LIVE/Windows watcher/운영 DB/예약 작업/Telegram/모델 리뷰 호출/협업 LIVE 전환에는 영향 없음.

## 현재 운영 결론

- **PAGES_DEFAULT=ENABLED:** 사용자가 대시보드를 확인할 때 기본으로 열어야 할 화면은 위 GitHub Pages HTML이다. GitHub PRIVATE HTML 소스 링크나 Markdown VIEW를 기본 UI로 제시하지 않는다.
- **PAGES_DEPLOY=PASS:** L1Work PUBLIC `main/docs/cowork-dashboard/index.html` 업데이트 후 GitHub Pages 배포 성공. 실제 PUBLIC 파일 GitHub readback PASS.
- **PUBLIC_DATA_SYNC=MANUAL_ALLOWLIST_ONLY:** PRIVATE 데이터와 공개 상태가 자동 연결된 것으로 보고하지 않는다. GitHub Pages 자동 빌드/배포는 **L1Work PUBLIC 파일이 바뀔 때만** 동작한다.
- **SOURCE_OF_TRUTH=PRIVATE_CURRENT_AND_VERIFIED_EVIDENCE:** 실제 진행 상태는 PRIVATE `CURRENT.md`, 리뷰·영수증 및 Actions 증거를 확인해 반영한다. 이전/미관측 정보는 PASS로 승격 금지.
- **CUTOVER=MIGRATION_NOT_CUTOVER:** 기존 LIVE Windows watcher, DB, 예약 작업, Telegram, Claude 독립 리뷰 운송 및 GitHub 전환에는 변경이나 승인을 부여하지 않는다.

## Executive Work Tracker 공개 적용 (2026-11-12)

- 사용자 선택: 디자인 시안 **01 Executive**. 기본 공개 URL은 `https://wonhwipark.github.io/L1Work/cowork-dashboard/` 그대로 유지하며, 공개 HTML의 상단 KPI → 개별 Work Tracker → 협업 7단계 흐름 → 검증·다음 조치 순서.
- **PUBLIC 승인 정보는 비식별·상위 범주만:** PRIVATE `CURRENT.md`가 존재하는 다섯 개 업무 범주(협업 운송, 대시보드, 스킬 탐색, 업무 자동화 후보, 지식 구조 설계)를 별도 카드로 표현한다. 내부 Work ID, PRIVATE 파일 링크, 상세 사내 환경/개발 소스/리뷰 요청 원문/영수증/토큰/고객 자료 공개 금지.
- `l1-fix-workflow` 및 `l1-github`는 사용자가 예시로 든 공개 스킬명으로서 **미등록·상태 미확인 예시**로만 표시. 실제 진행·리뷰 대기·완료로 추정하거나 활성 Work 수에 합산하지 않는다.
- GitHub PRIVATE `collab/dashboard/work_tracker.py`는 Work ID별 상태를 읽어 PRIVATE HTML/상태 JSON/VIEW를 갱신한다. 여기서 PUBLIC으로 자동 동기화하는 쓰기 권한/토큰/Actions는 추가하지 않는다.
- `phase`, `self_test`, `independent_review`의 문서 기재는 자기 신고 수준이고, REVIEW/RECEIPT 무결성 검증 또는 실제 실행 완료를 뜻하지 않는다. 공개 단계 막대는 완료율이 아닌 등록된 단계 위치다.
- PAGES 배포는 PUBLIC HTML 커밋 시 GitHub Pages가 자동 실행. `PAGES_AUTO_DEPLOY=PASS`와 `PRIVATE_STATUS_AUTO_SYNC=NOT_IMPLEMENTED`는 계속 분리 판정.

## 공개 허용 필드 (2026-11-12 사용자 Pages 게시 승인 범위)

- 업무 흐름의 일반적인 **단계명·주체 역할** (GPT / GitHub 협업 관리 환경 / Windows watcher·Claude Code 업무 실행 환경).
- 전환 여부의 상위 상태 (기존 LIVE 경로 유지 / GitHub 정식 전환 전).
- 독립 리뷰 및 호스트 Stage1 실검증의 상위 상태 (`NOT_RUN`을 미실행으로 표시).
- GitHub PRIVATE 추적 파일의 **비식별 합계 수치** (프로젝트 CURRENT 3 / REQUEST 0 / REVIEW 0 / RECEIPT 0, 2026-11-12 기준). 파일 관측 수는 완료 횟수가 아니다.
- 공개 HTML 제공·배포 성공 여부 및 날짜 기준. 페이지가 스냅샷이며 PRIVATE 자동 동기화가 없다는 고지.
- 개인·조직·업무 원문이 없는 공개 가능한 일반 프로젝트 범주 요약.

## 기본 공개 금지 및 강제 차단

- PRIVATE 내부 문서 원문, 기업 반출금지 코드, 고객정보, 사내 네트워크 주소·로컬 경로, 작업 ID/리뷰 요청 ID, ZIP 원본 및 실제 SHA, GitHub PRIVATE 링크, 토큰/키/서명, 운영 DB·로그 내용, 사람 이름, 상세 피드백, 리뷰 비용·실행 정책 구체 값.
- 공개 허용 목록에 없는 정보는 안전하다고 추정하지 않는다. 새 항목은 별도 반출 판단 및 승인 후 반영.
- PRIVATE Action의 `contents:write` 범위를 PUBLIC 쓰기 권한으로 확대하거나 별도 개인 토큰을 저장하지 않는다.
- 자동 PUBLIC 동기화는 **추가 구현/권한/승인 필요**. '항상 기본 Pages'는 표시 형식의 기본값이지 무인 실무 데이터 유출 승인이 아니다.

## 공개 페이지/인계

- PUBLIC 소스: `wonhwipark/L1Work` `main/docs/cowork-dashboard/index.html`.
- **기본 바로가기:** `https://wonhwipark.github.io/L1Work/cowork-dashboard/`
- PRIVATE 내부 상세: `collab/dashboard/index.html` (GitHub 코드 파일은 브라우저 실행 아님), `collab/dashboard/VIEW.md` (GitHub Markdown).
- 새 작업 시 사용자에게 HTML Pages 링크를 먼저 제공하고 `최종 상태 확인 일자` 및 `배포 성공/미검증`을 함께 알린다.
- PUBLIC 새 게시 후 GitHub 원격 readback, Pages Actions 빌드/배포 PASS, 가능 시 실제 HTTP 200/본문 해시 확인. 실패/검증 불가면 해당 항목만 NOT_VERIFIED로 기록.
