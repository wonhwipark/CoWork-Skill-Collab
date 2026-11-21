# Viewer v0.1.2 1차 — 사용자 리뷰 생략·PUBLIC ZIP 전달 결과 (2026-11-21 KST)

- Work: `L1-WORKSPACE-RAG-20261111-001`
- 사용자 최신 실행 지시: **"리뷰없이 배포까지 진행해줘"**. 이번 변경 대상은 1차 Viewer 색상·Work ID/대표 이슈번호·읽기 UX이며, 2차 ID/PW/실제 편집/원본 writer 기능은 제외.
- 협업 저장소 최신 확인: GitHub PUBLIC `wonhwipark/CoWork-Skill-Collab`, branch `main`; L1Work 역시 PUBLIC.

## 1. 현재 판정

| 단계 | 판정 | 직접 확인한 근거 |
|---|---|---|
| 1차 개발·패치 코드 | PASS_DEVELOPMENT | 기존 v0.1.1 work-labels 단위 18 PASS, v0.1.2 first-phase 전용 patch mock 12 PASS 및 JS 구문/Python compile PASS |
| 1차 A안 테마·표시 정적 코드 | PASS_STATIC | v0.1.0 `index.html`/app/CSS/adapter/fixture Git blob 고정 입력, 문자열 exact anchor 변경 및 유일성 fail-closed 19곳; 블루그레이 색상, 이슈번호/검색/원본 ID 보조, MSC overflow hint |
| 1차 배송용 합성 Viewer ZIP | **PASS_PUBLIC_DELIVERY** | `wonhwipark/L1Work/main/l1-workspace-viewer-ui_v0_1_2_1121.zip`, 74,940 bytes, SHA-256 `9be14c4c34c2a7d923d8b11c01fb0249d41e820861721f275001f0f7d499d9e3`, Git blob `6b9b3cb718044565e0b99aea8ba38a2ed3fa29de`, commit `4abf877a75d36388f1f4409edaaca1822f019cec`, remote base64 readback PASS/ZIP 11 파일 CRC PASS |
| 버전/원본 | PASS_PRESERVATION | 이전 v0.1.0 ZIP 불변, 기존 Work ID·폴더·Evidence 수정 0. 모든 Work/이슈번호는 **합성 fixture**뿐, 실제 업무 데이터 연결 없음 |
| 1차 업무 GPT 인계 | **PASS_PUBLIC_HANDOFF** | `wonhwipark/L1Work/main/handoffs/L1_WORKSPACE_VIEWER_FIRST_PHASE_V012_G0_DEPLOY_HANDOFF_r0001_20261121_KST.md`, commit `01855470ac50aa2ab90e7f44fc7a0581e31ae7f5`, remote readback PASS, `handoffs/README.md` 색인 commit `66bf08fc2f6d3af10300043eca9e5dd5168fd6b6` readback PASS |
| 새로운 STYLE 독립 R1 | **USER_WAIVED** | 신규 `REQ-L1-WORKSPACE-VIEWER-STYLE-DESIGN-R1-20261121`은 서명·READY·결과/영수증 미관측. 최신 사용자 지시로 **새 유료 리뷰·GPT 별도 판정을 배포 선행 조건에서 제외**. 과거 UX/편집 R1 이력은 변경 없음 |
| Windows watcher 실행 취소 | **NOT_VERIFIED** | REQUEST/PIN은 불변. 사용자 waiver를 별도 [기록](../../requests/REQ-L1-WORKSPACE-VIEWER-STYLE-DESIGN-R1-20261121/USER_REVIEW_WAIVER_20261121.md), commit `1f86bf2f3d43af7bdd17414ffee346f97b52217c`, remote readback PASS. 해당 문서는 watcher의 하드 차단 기능 아님; Windows 운영자/보호 signer에서 실제 취소 확인 필요 |
| 전체 원본 v0.1.0 ZIP에 대한 완전 회귀 56/19 및 Chromium | **NOT_RUN** | 원본 ZIP의 실바이트를 로컬 런타임으로 다운로드하는 경로 차단. 이번 ZIP은 원본 GitHub v0.1.0 **소스 파일**로 합성 생성했으며 GitHub 바이트/CRC 확인만 수행 |
| 실제 Linux G0, B1/B2/B3, E3/E4, HOST_DEPLOY | **NOT_RUN/BLOCKED_BY_HOST_ACCESS** | 이 GPT 환경에는 업무 Linux viewer의 소스·서비스·원본 Work/이슈번호 메타와 운영 권한에 접근하는 연결이 없음. 원격 ZIP 게시 ≠ 실제 설치/동료 화면 확인 |
| 2차 edit/ID-PW/writer | **OUT_OF_SCOPE** | v0.1.2 UI ZIP에 편집 prototype 파일·로그인 요구·write API 0. 읽기용 viewer 시각 코드만 배송 |

## 2. 실제 변경 파일·연결

- 배송 ZIP의 `viewer-wiki-ui/index.html`: 기존 스크립트/레이아웃 유지, `work-labels.js` 및 `professional-theme.css` 추가, 버전·데모 메시지 보존. 
- `assets/work-labels.js`: **확인된** `issueKey`/Work ID/title만 조합; 중복번호 접두어 제거, missing title fallback, 검색 도우미. `issueKey`는 업무 Linux의 확정 API 필드가 아님.
- `assets/professional-theme.css`: 블루그레이 A안 선택 상태·본문 메타 글자색/크기·상태 구분; 원본 style.css 변경 0.
- `assets/app.js`: Work tree/group/title/breadcrumb/search·원본 Work ID 보조/MSC 방향 안내.
- `adapters/adapter.js`, `fixtures/demo-data.js`: 합성 예시의 issueKey/workId 연결만. 업무 Linux Viewer에 해당 fixture 설치 금지.
- `README_1ST_PHASE.md`, `manifest.sha256`: 원본/실서비스 경계·SHA·G0 게이트 기록.

**추가 사용자 다운로드용 별도 소스 패치 ZIP(이번 대화 sandbox):** `l1-workspace-viewer-first-phase_v0_1_2_1121.zip`, 10,685 B / SHA-256 `9f76166dd3a8e84755468e4e218c3ad429b84c3ec75d311c16228f94fe0c329a`, 7 files CRC PASS. 이 파일은 PUBLIC ZIP과 **다른 바이트/역할**이며 L1Work에 별도 게시하지 않았음; 개발용 오프라인 원본 SHA 고정 패치 도구.

## 3. 실제 Linux 배포를 완료하려면

업무 GPT 또는 기존 승인된 Linux Agent가 이미 PUBLIC에 게시된 ZIP과 [정확한 원샷 인계](https://github.com/wonhwipark/L1Work/blob/main/handoffs/L1_WORKSPACE_VIEWER_FIRST_PHASE_V012_G0_DEPLOY_HANDOFF_r0001_20261121_KST.md)를 읽어 기존 Linux Viewer source/branch/revision·API/이슈번호 title 메타·G0 검증→코드 이식/시험→보안 B1~B3·E3/E4→유효한 host 설치 승인/백업·롤백→사용자 접근 검증. 호스트 검증 전 배포 완료라 단정하지 않음.

**다음 한 행동:** 업무 GPT가 기존 Linux Viewer Work를 재개해 PUBLIC v0.1.2 + 위 인계로 **G0 읽기 전용 실체·권한/데이터 확인 및 1차 UI 이식**부터 실행하고, 승인된 실제 서비스 설치 결과 또는 BLOCKED 사유를 업무 Work에 남길 것. CoWork Windows 보호 signer는 최신 사용자 waiver를 확인하여 기존 STYLE R1에 서명/READY를 새로 만들지 않도록 운영 경로에서 확인.
