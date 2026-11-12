# CoWork PUBLIC Pages 자동 상태 게시 구축·시험 결과

**기준:** 2026-11-12 KST · 사용자 지시 "public page 로 자동으로 해줘"

## 1. 현재 상태

| 항목 | 결과 | 직접 확인 근거 |
|---|---|---|
| PUBLIC HTML 기본 화면 | **PASS** | L1Work Pages Executive HTML |
| PUBLIC 상태 JSON 클라이언트 | **PASS (파일 게시/배포)** | status.js, status.json, index.html 원격 readback |
| PRIVATE 허용목록 exporter | **PASS (합성시험)** | PRIVATE Actions 47개 테스트 |
| PRIVATE→PUBLIC 자동 트리거 | **PASS (실행 확인)** | workflow_run 실제 호출 |
| PUBLIC 게시 자격증명 | **BLOCKED_MISSING_SECRET** | 공개 PUT Step SKIPPED |
| PRIVATE→PUBLIC 실제 PUT/원격 readback | **NOT_RUN** | 자격증명 설정 전 안전 차단 |
| GitHub Pages 배포 | **PASS** | PUBLIC Actions #43243668745 |
| 실제 브라우저 JSON 동적 렌더링/HTTP E2E | **NOT_RUN** | Github Pages 파일·빌드까지만 검증 |
| Dropbox/GitHub 협업 LIVE 전환 | **MIGRATION_NOT_CUTOVER** | 기존 운영 변경 없음 |

## 2. 변경 산출물 · 위치

### PRIVATE `wonhwipark/CoWork-Skill-Collab` main

- `collab/dashboard/public_sync.py` (Git blob `46679b784b640a6c779fb2d9d0d4fcee858cc5b7`): PRIVATE state.json 재생성·비교 후 고정된 상위 업무 범주/상태/숫자만 PUBLIC JSON으로 내보냄. 새 미허용 Work는 상세 공개하지 않음. URL/경로/권한을 고정한 GitHub contents 단일 파일 PUT, 재조회·정확 바이트 검증, 멱등.
- `collab/dashboard/tests/test_public_sync.py` (blob `b5704d99a4830efb05c68f9c556633c4f6b0df04`): 보안 범위, 무단 새 Work, 상태 PASS 오인, cutover 차단, stale 소스, 인증 부재 0회 호출, 지정 경로만, API readback 등에 대한 합성시험.
- `.github/workflows/cowork-public-status-sync.yml` (blob `a71bd8c4c0b45f626d6af248036668191d553d1e`): PRIVATE 대시보드 성공 `workflow_run` 후 독립 sync 실행. `workflow_dispatch` 수동 재실행 지원. 운영 watcher·Claude 호출 없음.
- `collab/dashboard/PUBLIC_PAGES_DEFAULT_POLICY.md`: 사용자 추가 승인된 PUBLIC 상태 자동화의 공개 필드 게이트.
- `collab/dashboard/PUBLIC_AUTO_SYNC_SETUP.md`: 토큰 생성/Secrets 설정/검증/취소/회전 지침. 비밀 자체 미포함.
- README 및 `collab/START_HERE.md`는 공개 Pages를 기본 확인 화면으로 계속 유지하되 PRIVATE→PUBLIC 인증 전에는 BLOCKED로 판정.

### PUBLIC `wonhwipark/L1Work` main

- `docs/cowork-dashboard/index.html` (blob `3c6fc6747a9c2e3a357431899b11998dd9a5a110`): Executive 기존 화면 보존, same-origin 상태 JS 허용 CSP, 최신 자동 상태 연결 여부 표시.
- `docs/cowork-dashboard/status.js` (blob `be47cd8c8613e4d501e0b1c71c5ccf8782d3b5c7`): PUBLIC status.json만 `fetch`하고 textContent/DOM 생성으로 Work 카드 및 KPI 갱신. 공개 스키마·데이터 타입·개수·용어 검증, 오류 시 정적 기본 화면 유지.
- `docs/cowork-dashboard/status.json` (blob `afb84106e8d2b5684535c8ad1dc1e035a949cef7`): 안전한 초기 공개 스냅샷. `sync_mode=BOOTSTRAP_NOT_AUTO`, 5개 공개 업무 범주, PRIVATE Work ID·원문·영수증/민감내용 없음.
- PUBLIC README 설명 보완. 기존 ZIP·시안 2/3·타 파일 불변.

## 3. 실제 실행·검증 증거

- PRIVATE `CoWork PRIVATE dashboard` #43242260965 SUCCESS: Python **47 PASS/0 FAIL** (기존 35+신규 public sync 12), 공개 샘플 **8 PASS/0 FAIL**. 총 **55 PASS/0 FAIL**.
- PUBLIC 자동 동기화 Action #43243087542 및 #43243862993: PRIVATE 성공 이후 `workflow_run` 자동 호출 성공. `ALLOWLIST_BUILD=PASS`; 검증·비밀 존재 확인 PASS, **PUBLIC 게시 Step SKIPPED**. 후자의 자격증명 Secret 부재가 확인되며 PUBLIC HTTP PUT은 호출하지 않음.
- PRIVATE 액션 #43243918416 성공 이후 #43243965078 연쇄 실행 성공으로 트리거 재현.
- PUBLIC Pages #43243668745 SUCCESS: HTML+JS+초기 JSON+README 배포·정적 파일 원격 재조회 PASS. **실제 인증된 PRIVATE→PUBLIC 게시 및 HTTP 응답/시각적 렌더링은 검증되지 않음**.
- 모델 리뷰·유료 호출·운영 호스트 시험을 실행하지 않음.

## 4. 남은 사용자 1회 설정

1. GitHub 계정에서 **Fine-grained PAT**, 소유자 `wonhwipark`, repository **Only select → L1Work**, permission **Contents Read/Write**만 발급 (Metadata 기본). 이 토큰은 PUBLIC 저장소 전체 Contents에 쓸 수 있어 **파일 단위로 GitHub ACL을 제한하지 못함**을 인정해야 함.
2. PRIVATE `https://github.com/wonhwipark/CoWork-Skill-Collab/settings/secrets/actions` → `New repository secret`, Name **`COWORK_PUBLIC_DASHBOARD_WRITE_TOKEN`**, Value는 위 토큰을 직접 입력. **채팅·문서·로그에 토큰 전송 금지.**
3. PRIVATE Actions `CoWork PUBLIC Pages status sync (allowlist only)` → `Run workflow` 수동 1회 실행. `PUBLIC_SYNC=POSTED_READBACK_PASS` 및 이어지는 L1Work Pages 성공, 브라우저 HTML 새 상태 반영 확인. 이후 CURRENT/TRACKER 변화 시 자동 체인 재작동.

## 5. 종합 판정

**개발 및 합성시험 PASS / PUBLIC 초기 페이지 게시 PASS / 자동 트리거 PASS / 인증된 cross-repo PUB 게시 BLOCKED_MISSING_SECRET / AUTO_PUBLISH_E2E NOT_RUN / 독립 리뷰 NOT_RUN.**

비밀 설치 전 새 PUBLIC 게시 성공으로 주장하지 않음. LIVE 운송·Windows watcher·운영 DB·스킬 ZIP·Telegram·Claude 리뷰 실행 불변. PUBLIC 자동화는 새 비용을 유발하는 모델 호출이나 별도 자동 감시 서비스가 아닌 GitHub Actions 이벤트 기반.

**다음 한 동작:** 사용자의 PUBLIC 범위 최소 fine-grained token을 PRIVATE Actions Secret에 직접 등록하고 sync workflow를 1회 실행.
