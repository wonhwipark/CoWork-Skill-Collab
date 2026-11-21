# Viewer 환경설정 v0.3.0 — 구현·시험·L1Work PUBLIC 배송 결과

- 날짜: 2026-11-21 KST
- Work: `L1-WORKSPACE-RAG-20261111-001`
- 대상: 기존 Linux L1 Workspace Viewer 재사용. 기존 업무용 writer·Kernel/Updater·MSC 원본은 이 릴리스에서 변경하지 않음.
- **종합 판정:** `PUBLIC_DEV_ZIP_DELIVERY=PASS_REMOTE_VERIFIED` / `LOCAL_SYNTHETIC_QA=PASS` / `LINUX_HOST_DEPLOY=NOT_RUN` / `development_not_for_deployment`.

## 1. 원본 상태와 변경 내용

- 원본 Viewer v0.1.2 ZIP `l1-workspace-viewer-ui_v0_1_2_1121.zip` SHA-256 `9be14c4c34c2a7d923d8b11c01fb0249d41e820861721f275001f0f7d499d9e3` (기배포).
- Write source v0.2.0 ZIP `l1-workspace-viewer-write-ui_v0_2_0_1121.zip`, **21,171 B**, SHA-256 `9f2df44348478eb44615bddef8f211645fa1c07ed71d43580b4fb324e376b6f9` (기배포). 편집용 인증·Writer host adapter는 실제 Linux에서 미확인.
- 본 개발 ZIP `viewer-preferences-v030/`: 독립 `assets/preferences.js`, `assets/preferences.css`, 고정 Write ZIP SHA를 검사하는 `tools/apply_to_viewer.py`, JS/Python 회귀, 가상 미리보기, `README.md`·`HOST_INTEGRATION.md`·해시 manifest. 기존 Write v0.2.0 UI JS/CSS 수정 0.
- **사용자별 표시:** 유효 `data-l1-section` 9개 중 선택 표시(overview/work-meta/issue/analysis/msc/history/evidence/comments/debug). **문서 필터:** `data-l1doc-type` 6개(issue/msc/hld/analysis/design/other). 등록되지 않은 요소는 기본 유지하여 권한/UI를 숨기지 않음.
- **화면:** 시스템/밝음/어두움 테마, 기본/촘촘 밀도, 작은/기본/큰 글자. 저장·취소·초기화, storage 이벤트와 프로필 변경 이벤트 반영. 비밀번호/토큰·Writer CAS 데이터는 로컬 설정에 기록하지 않음.
- **사용자 ID:** `window.L1ViewerPrefsIdentity`의 안정적 비밀 아닌 opaque id(허용 문자/길이 한정)만 사용; 없으면 anonymous 브라우저 저장. 공유 PC의 계정 전환과 실제 서버 사용자 인증 소유자는 Linux G0 확인 대상. 브라우저 간 동기화·계정 정책 지원을 주장하지 않음.

## 2. 검사 결과

| 점검 | 결과 | 한계 |
|---|---|---|
| JavaScript 로직 `node --test tests/preferences.test.cjs` | PASS 16/16 | 합성 상태/Mock |
| Python ZIP patch `unittest discover` | PASS 14/14 | 합성 Viewer fixture/부정 경로 검증 |
| JS syntax, Python compile | PASS | 실제 브라우저 렌더 제외 |
| ZIP CRC/path/manifest, 실제 PUBLIC blob | PASS | 9 entries, 20,661 B; 원격 Base64 바이트 일치 |
| 브라우저 Chromium 실제 페이지 접근 | BLOCKED/NOT_RUN | 테스트 환경의 네트워크/file 프로토콜 정책 차단 |
| 정확한 v0.1.2 → v0.2.0 → v0.3.0 전체 ZIP 조립 | NOT_RUN | 원본 2 ZIP의 동일 실행 환경 전체 빌드/검증 미실행 |
| Linux Viewer DOM/CSP/원본 writer/Write 회귀/호스트 적용 | NOT_RUN | 호스트 실제 코드·권한/로그 접근 없음 |
| 별도 독립 코드 리뷰 | NOT_RUN | 사용자 요청에 유료 리뷰 자동 추가하지 않음 |

## 3. L1Work 배송·SHA-256

- **공개 루트 ZIP:** [`wonhwipark/L1Work/main/l1-workspace-viewer-preferences_v0_3_0_1121.zip`](https://github.com/wonhwipark/L1Work/blob/main/l1-workspace-viewer-preferences_v0_3_0_1121.zip).
- **20,661 bytes / SHA-256:** `228c60bada8a92591f7ae855dfabe206e018d9e59970cf2d1b773d4d00072812`.
- **정확한 Git blob:** `6798f08a2780c9313f10af12669d5cec2016f14a`. Git 원격 Base64 readback == 원본 export Base64: PASS.
- **L1Work 최초 배송 커밋:** `08c4c216d82ad89bc9958daccd44247b74cf2d02`. 이후 원격 `main` HEAD는 동시 작업으로 이동할 수 있으며 ZIP blob/내용 자체는 재조회로 검증.
- **정확한 G0 인계:** `wonhwipark/L1Work` / `main` / `handoffs/L1_WORKSPACE_VIEWER_PREFERENCES_V030_G0_INTEGRATION_HANDOFF_r0001_20261121_KST.md`.
- `handoffs/README.md` 인덱스 추가·원격 readback PASS.
- 기존 v0.1.2·v0.2.0 파일 교체·삭제·Linux 운영 설치 0.

## 4. 차단/다음 한 행동

업무 GPT/Linux Agent가 고정 SHA ZIP·공개 인계서로 **기존 Linux Viewer 설치 원본 G0**, DOM 섹션/문서 유형 매핑·CSP·사용자 식별·Write UI 충돌 및 실 브라우저 1440/720/390/320·동료 무로그인·세션/권한·백업/롤백 검증. 이 단계가 실제로 통과하고 유효한 운영 승인 범위를 확인하기 전에는 호스트 운영 적용/Write 활성화 금지. 결과는 같은 Work의 비민감 Evidence로 회신하고 회사 제한 코드/로그/키를 PUBLIC으로 반출하지 않음.
