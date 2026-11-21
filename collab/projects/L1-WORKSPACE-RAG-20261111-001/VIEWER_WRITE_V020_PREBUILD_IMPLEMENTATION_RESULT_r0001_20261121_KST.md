# Viewer Write v0.2.0 선행 개발 — 구현·자체시험 결과

- 일자: 2026-11-21 KST
- 기존 Work: `L1-WORKSPACE-RAG-20261111-001`
- 사용자의 최신 동작 지시: "진행" — 1차 Viewer PUBLIC 전달 이후 2차 Write 기능 개발 진행
- **CURRENT_VERDICT=DEVELOPMENT_CANDIDATE_CREATED / REAL_WRITER_NOT_CONNECTED / NOT_FOR_DEPLOYMENT**
- CoWork 저장소 visibility는 **PUBLIC** (2026-11-21 CONTEXT_BRIEF 최신 근거), 회사 제한 코드·로그·MSC·계정/키·토큰 신규 게시 0.

## 1. 수행 범위

기존 읽기 Viewer v0.1.2의 CSS·Work 제목 기능을 유지하고 **별도 프런트엔드 편집 확장**만 개발. 기존 첫 접속/읽기/검색·문서/MSC는 **무로그인 Read Only**, 사용자가 [수정] 버튼을 누를 때만 편집자 인증을 시도한다. 실제 Linux 편집용 host adapter가 연결되어 있지 않으면 **[수정] 버튼 비활성·서버 호출/쓰기 0**.

| 구현 | 세부 내용 | 안전 경계 |
|---|---|---|
| `assets/write-client.js` | 상태기계 READ_ONLY → AUTH_PENDING → EDIT_AUTHORIZED/EDIT_DIRTY → DIFF_PREVIEW → DRAFT_SAVED / COMMIT_PENDING → COMMITTED, stale/uncertain 처리 | 서버 응답 인증/권한·source revision·writer 확인 전 저장 불가. 기존 문서별 writer 재검사 의무는 현장 연결 전 미확인 |
| `assets/write-ui.js`, `write-ui.css` | 기존 `#doc-actions`의 [수정] 버튼, 클릭 이후 ID/PW 모달, 본문/MSC 수정 요청·Diff/Preview·초안·확정 UI; 390/320 모바일 화면 대응 | 사용자 열람 진입 로그인 0. 비밀번호 localStorage/URL/GitHub 저장·메시지 원문 로깅 0. 연결 코드 미구현이면 버튼 disabled |
| MSC 변경 요청 | server canonical anchor 목록이 검증돼 있으면 **부모 DOM** 선택. 목록 없으면 문서 수준 자연어 변경 요청 초안만 | 격리 iframe DOM 직접 조작·postMessage 신규 브리지·MSC 구조 canonical commit 금지 |
| 저장/충돌 보호 | verified source base revision, 서버 preview/draft readback, TEXT만 명시적 commit, writer receipt verified/newRevision 요구, conflict 또는 WRITE_UNCERTAIN은 재시도 0 | 프로덕션 서버 권한/CSRF/ACL/rate-limit/session rotation/Writer·readback 구현은 Linux G0 미확인 |
| 패치 유틸리티 | `tools/apply_to_v012.py`가 정확한 v0.1.2 ZIP SHA 검증 후 프런트 자산·HTML script/style 세 곳만 추가; manifest/CRC·경로 이탈·symlink·중복 차단 | 기존 v0.1.2 원본 ZIP 불변. 실제 v0.2.0 **완성 전체 ZIP 생성/브라우저 회귀 NOT_RUN** (이 개발 환경에서 v0.1.2 원본 ZIP의 로컬 다운로드 차단) |
| 인계·샘플 | `HOST_INTEGRATION.md`, `README.md`, `preview.html` | 사용자/회사 자료 없는 **가상** UI 정적 샘플, 실제 인증·저장 성공 아님 |

## 2. 시험 결과 (자체시험과 실제 Linux 분리)

| 항목 | 판정 / 근거 |
|---|---|
| JavaScript 상태기계·서버 실패 주입 | **PASS 30/30** Node `node --test tests/write-client.test.cjs`: auth 실패·ACL gate, revision stale/충돌, draft/preview/commit readback·uncertain, MSC 구조 commit 0, close/busy 동시 처리 |
| Python patch/ZIP 부정 경로 | **PASS 8/8** `python -m unittest discover -s tests -p 'test_*.py'`; fail-closed base ZIP SHA 불일치, 이중 anchor, ZIP path traversal/중복 파일, manifest/deterministic pack |
| JS syntax / Python compile | PASS (`node --check` 2개 JS, `python -m py_compile` 1개 patch script) |
| 패키지 자체 검증 | PASS: 10 files, zip CRC PASS, manifest 9개 파일, 경로 이탈/구성 검사 |
| **기존 PUBLIC v0.1.2 원격 HTML 실제 anchor** | PASS: `<link rel="stylesheet" href="assets/professional-theme.css">`, `<script defer src="assets/app.js"></script>`, `v0.1.2 · 합성 데이터` **각 1회**; 이미 L1Work PUBLIC에 있는 고정 v0.1.2 원격 ZIP 바이트 읽기로 확인 |
| 실제 v0.1.2 전체 ZIP + v0.2.0 적용 통합·전체 Viewer 56/19 회귀·브라우저 렌더 | **NOT_RUN**. 로컬 빌드의 patch mock 시험으로 실배포/브라우저 성공을 주장하지 않음 |
| Linux host/G0 인증·CSRF·session·doc ACL·Kernel/Updater writer·canonical anchor·B1/B2/B3·E3/E4·실제 수정/복구 | **NOT_RUN / BLOCKED_HOST_ACCESS** |
| 독립 **코드** 리뷰/운영 배포 | **NOT_RUN**; 앞서 진행했던 Viewer 인증 **설계** R1 완료와 별개. 스타일 R1 사용자 waiver가 Write 보안 코드 리뷰/게이트까지 면제하는 근거 아님 |

## 3. 작성된 파일과 바이트(현재 대화 다운로드, ZIP 원격 미게시)

- 개발 후보 ZIP: **`l1-workspace-viewer-write-ui_v0_2_0_1121.zip`** / **21,171 bytes**, SHA-256 **`9f2df44348478eb44615bddef8f211645fa1c07ed71d43580b4fb324e376b6f9`** / 10 files.
- UI 가상 미리보기: `l1-workspace-viewer-write-ui-preview_20261121.html` / 5,088 bytes / SHA-256 `56fb8467d7cc90115488c753b702d89dc63adcd62c579e6b94735238a431243c`.
- 핵심 파일 `write-client.js` 10,037 bytes / SHA-256 `2f466fc3dbe24a9864ac259ed4b45bbf87398e222bc07e8555a78e02078c59da`; `write-ui.js` 10,998 bytes / SHA-256 `05f37773cb166c563516ab74bdb8923f83e5dfb69762339328e357b895bf64f1`; `write-ui.css` 2,485 bytes / SHA-256 `b391a6f542ac3d1e6e0f86ac5163a70cd018ea2e59a6eec9108e6f919eb5f181`.
- **이번 ZIP·preview는 이 대화의 사용자 다운로드 파일. GitHub CoWork/L1Work에 바이너리 게시되거나 업무 GPT/호스트로 자동 전송된 것이 아님.** 향후 다른 세션이 SHA만으로 ZIP을 다시 받을 수 있다고 주장하지 않음. 공개 저장소에는 비민감 결과 문서만 기록.
- 1차 v0.1.2는 기존 PUBLIC ZIP `wonhwipark/L1Work/main/l1-workspace-viewer-ui_v0_1_2_1121.zip`·74,940 bytes/SHA `9be14c4c34c2a7d923d8b11c01fb0249d41e820861721f275001f0f7d499d9e3`. 본 작업에서 변경 0.

## 4. 업무 GPT 인계·다음 한 행동

- PUBLIC `wonhwipark/L1Work/main/handoffs/L1_WORKSPACE_VIEWER_WRITE_V020_G0_AND_INTEGRATION_HANDOFF_r0001_20261121_KST.md` 게시/remote readback 완료(해당 문서에서 현장 권한/실행 분리).
- 다음: 업무 GPT/Linux Agent가 **기존 Viewer Work/실제 Linux G0**로 인증·CSRF·세션 회전·rate-limit/계정 보호/ACL·기존 Work/Evidence/Knowledge writer·canonical anchors 확인 후, 개발 ZIP의 실제 파일 전달이 승인된 경우에만 정확한 SHA로 연결·시험. 모호하거나 미확인 부분은 EDIT_DISABLED/BLOCKED로 두고 동료 Read Only 유지. 별도 운영 승인/백업/롤백/보안 B1~B3/E3/E4 PASS 전에 실제 호스트 Write 활성화 불가.
