# Viewer Write UI v0.2.0 — L1Work PUBLIC 바이너리 게시 결과

- Date: 2026-11-21 KST
- Work: `L1-WORKSPACE-RAG-20261111-001`
- 사용자 최신 지시: "그래 업로드해줘" — 직전 GitHub 바이너리 업로드 차단을 해결해 기존 v0.2.0 개발용 ZIP을 **L1Work/main 루트에 원본 그대로 게시**.
- **현재 판정: PUBLIC_ZIP_DELIVERED=PASS_REMOTE_VERIFIED / HOST_DEPLOY=NOT_RUN / EDIT_WRITE_ENABLED=NO**.
- 정본 공개 저장소: `wonhwipark/L1Work`, branch `main`. 실제 GitHub 파일 [`l1-workspace-viewer-write-ui_v0_2_0_1121.zip`](https://github.com/wonhwipark/L1Work/blob/main/l1-workspace-viewer-write-ui_v0_2_0_1121.zip).

## 1. 바이트 무결성

| 검사항목 | 실제 값 |
|---|---|
| 전달 ZIP 이름 | `l1-workspace-viewer-write-ui_v0_2_0_1121.zip` |
| 실제 원본 파일 크기 | **21,171 B** |
| 실제 원본/원격 SHA-256 | **`9f2df44348478eb44615bddef8f211645fa1c07ed71d43580b4fb324e376b6f9`** |
| Local Git blob SHA-1 예상 | `aed05a83e70efbe32f28bf494b6bf7b984f3f09b` |
| GitHub remote blob SHA-1 | **`aed05a83e70efbe32f28bf494b6bf7b984f3f09b`** — 동일 |
| PUBLIC main commit | **`cf04dbf8d658ba4198c3cb9c691c07638711d97e`** |
| Remote readback | **PASS** — 직접 생성한 base64 bytes와 main의 GitHub fetch_file(base64) 내용 정확히 일치 |
| ZIP 자체검사 | 10개 파일 CRC/manifest PASS, 경로·시심링크 검사 PASS; 기존 자체시험 JS 30/30·Python 8/8 PASS |
| 기존 v0.1.2 | `l1-workspace-viewer-ui_v0_1_2_1121.zip`, 원본 불변 |

## 2. 인계 정합성·결과

- `wonhwipark/L1Work/main/handoffs/L1_WORKSPACE_VIEWER_WRITE_V020_G0_AND_INTEGRATION_HANDOFF_r0001_20261121_KST.md`: 이전 '대화 첨부에만 존재/ZIP 미게시'를 2026-11-21 실제 게시 상태로 정정, ZIP 루트 링크·SHA·Linux 실행 게이트 유지. update commit **`7c29cef6e1fe2e706a9e67e84364737c24f04c81`**, remote readback PASS.
- `wonhwipark/L1Work/main/handoffs/README.md`: 최신 Viewer Write UI ZIP 항목 추가, 앞서 '바이너리 배송 안 됨' 문구 정정. update commit **`c6e27fc6a42f1f3f818cfe12cf85f5bed8056878`**, remote readback PASS.
- 전송 경로: 사용자 대화 첨부 로컬 ZIP의 바이트 → base64 문자열 전환 → 연결된 GitHub Git Blob API 업로드 → main의 신규 트리/commit 게시 → 원격 파일 base64/원본 Git blob SHA 비교. 중간에 임시 Library transfer 파일을 생성했으나 검증 후 삭제 요청 성공. GitHub 외부에 업무 코드/로그/자격증명 추가 게시 0.
- 이전 `VIEWER_WRITE_V020_PREBUILD_IMPLEMENTATION_RESULT_r0001_20261121_KST.md`는 최초 개발 후보 당시 **미게시** 사실을 보여주는 역사적 결과. 이번 문서가 이후 실제 게시 사실을 갱신. 이전 `CURRENT.md` 차단 스냅샷도 이 신규 결과보다 먼저 있었음.

## 3. 정확한 안전 경계

- 이번 사용자가 승인한 것은 **PUBLIC 개발 후보 ZIP 배송**. `development_not_for_deployment` 상태를 유지하는 **전달 예외**로 기록하며, 정식 코드 리뷰·실제 Linux 서버 테스트·운영 설치/Write 활성화 승인으로 변환하지 않음.
- 기존 Viewer는 동료 첫 접속 **무로그인 Read Only**. 이 ZIP의 [수정] 기능은 검증된 `L1ViewerWriteHostAdapter`가 없을 때 fail-closed/disabled.
- **NOT_RUN/NOT_VERIFIED:** 실제 Linux Viewer 설치 revision G0, 기존 Auth/session rotation/CSRF/rate-limit/계정 보호/문서별 ACL, Writer/CAS/readback, MSC canonical anchor, B1/B2/B3, E3/E4, 실제 편집 저장·롤백, 독립 **v0.2.0 코드** 리뷰.
- 실제 Linux Viewer에 유효한 기존 승인 없이 계정·키·설정·서비스를 변경하거나 활성 writer를 붙이지 않음. 이번 PUBLIC ZIP은 자동 실행 Job/Skill-Updater 활성 트리거가 아니며 운영 배포로 보고하지 않음.

## 4. 다음 한 행동

업무 GPT/Linux Agent가 [PUBLIC v0.2.0 ZIP](https://github.com/wonhwipark/L1Work/blob/main/l1-workspace-viewer-write-ui_v0_2_0_1121.zip) + [기존 인계서](https://github.com/wonhwipark/L1Work/blob/main/handoffs/L1_WORKSPACE_VIEWER_WRITE_V020_G0_AND_INTEGRATION_HANDOFF_r0001_20261121_KST.md)를 읽고, 현재 Linux Viewer G0·인증/기존 writer/MSC anchor를 확인한 후 허용된 개발/시험을 진행. B1~B3/EAuth/E3/E4/운영 승인/백업·롤백 PASS 전까지 Write 기능 활성화 금지.
