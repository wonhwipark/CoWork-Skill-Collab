# 2안 위키 UI 시각·사용성 리뷰 고정 입력 manifest r0001

- Request: REQ-L1-WORKSPACE-WIKI-UI-UX-R1-20261119 / revision 1
- 기존 Work: L1-WORKSPACE-RAG-20261111-001
- 작성: 2026-11-19 KST
- 승인 범위: 신규 독립 리뷰 1회·최대 USD 3, POLICY-STATIC-V1 / intent unified. 실제 Windows 정책·보호 서명 게이트 별도.
- 신규 고정 대상: 완성 UI v0.1.0, 화면 구성·가독성·스타일·사용자 시인성 4축. 이전 설계 리뷰 재실행 아님.
- Source commit: 17ac2b39ad01dc3e01df467ada698fbac8b5c399
- Source UI tree: 6282918d60fed523dba2ec0868866eb502ef08b5
- ZIP: collab/packages/l1-workspace-wiki-ui_v0_1_0_1119.zip
- ZIP bytes: 267140
- ZIP SHA-256: 411553e74e76bb82237fd2ebef65169769e4dbe4cfd2231afb5afd38559b10a9
- ZIP Git blob: c590c3e18813eff5db7cc9b6da4c6abf8ae5660c
- 23개 파일. 기존 패키지 바이트·버전 불변 재사용, 새 ZIP 중복 제작 없음.
- INPUT_TYPE=SYNTHETIC_DEMO. 실제 Linux 화면·업무 자료·로그·코드 미포함.

## 시각 검토 필수 이미지

| ZIP 내부 상대 경로 | bytes | SHA-256 |
|---|---:|---|
| viewer-wiki-ui/screenshots/wiki-1440.jpg | 92791 | `0f08ee0452f38f2630f4fc0ddbcf0df639ba7fe6c8cf3e9053cdda4fa206b6be` |
| viewer-wiki-ui/screenshots/wiki-390.jpg | 39502 | `95ba117bd434968f3eff91986d4c6fe1412ec9e5f174f5a856f92a695c65637b` |
| viewer-wiki-ui/screenshots/wiki-320.jpg | 33480 | `17af8f4337c48a839ab94282b8e56d2b018aff75d60eec7e35253c2ffe85e663` |
| viewer-wiki-ui/screenshots/msc-12.jpg | 80061 | `046428eb97e4fdcf8d5651a4a157ea3afa36ea51520ab9c49003c618ba1f75d4` |

## REQUEST·사전검증

- 후보의 정본 파일: 같은 Work `WIKI_UI_UX_R1_REQUEST_DRAFT_r0001_20261119_KST.md`
- 후보 bytes: 8361
- 후보 SHA-256: `460bce9b3724d82dd3d59f0a68abdae970ee3afcd55466ade2f43935e6b00192`
- 줄끝: UTF-8 LF. 호스트에서 CRLF 변환·본문 수정 없이 그대로 검증·게시할 것.
- 합성 게이트 2/2 PASS: STATIC/USD3 fixture에서는 후보 문법·고정 ZIP/size/SHA·CRC PASS; 마지막 보고 STATIC/USD1.50 fixture에서는 예상대로 POLICY_COST_MISMATCH 차단 PASS.
- **HOST_LIVE_PREFLIGHT=NOT_RUN**, SIGNER/APPROVAL_SIG/READY/MODEL=NOT_RUN. 이 합성시험은 실제 Windows LIVE 호환성이나 서명·승인 PASS가 아님.

## 필요한 출력과 전달 보류

REVIEW_KIND=INDEPENDENT_VISUAL_UX. 실제 이미지 열람 목록·4축 평가·우선 보완·근거/최소수정안·업무 GPT 전달 전 필수 보완 여부. 이미지 못 읽으면 VISUAL_INSPECTION=NOT_RUN/PARTIAL_SCOPE. 운영 B1/B2/B3는 본 시각 리뷰의 해결 범위가 아님.

정식 REQUEST 이전 호스트 게이트가 필요한 상태로 후보만 게시. 완료·수락으로 표시하지 않으며 업무 GPT 전달은 리뷰 및 GPT 판정 후로 HOLD.
