# Viewer v0.5.1 게시본 재검증 — 2026-11-23 KST

- Work: `L1-WORKSPACE-RAG-20261111-001`
- 사용자 요청: v0.5.0 보존 → 도우미 기본 숨김 새 버전 ZIP → 이전 인계 내용 전량을 포함한 신규 업무 GPT 인계 업로드까지 완료.
- 판정: **PUBLIC_DELIVERY=PASS_REMOTE_BYTE_VERIFIED**. 이미 동일 범위로 게시된 v0.5.1을 발견해 그 고정 게시본을 재검증. 별도 로컬 후보는 정본으로 게시하지 않았고 기존 공개 ZIP·인계서를 덮어쓰지 않음.
- 공개 게시 commit: `4dd8cfe691f9d18f658c8f23f0da5ed5d8d6d129`. 새 모델 리뷰/호스트 실행 없음.

## 최종 전달 두 파일

| 자료 | 정확한 L1Work main 경로 | Bytes | SHA-256 |
|---|---|---:|---|
| 신규 ZIP | `l1-workspace-viewer-wiki-integrated_v0_5_1_1123.zip` | 349332 | `0bc0240261e29c863c541e9650e9f99271b2b924ffd52be753598889f66cf290` |
| 완결 업무 GPT 인계 | `handoffs/L1_WORKSPACE_VIEWER_V051_TODAY_ASSISTANT_HANDOFF_r0001_20261123_KST.md` | 15747 | `8a76eeca399abca261d55faae3b51aef3b8a8e109338f011ebc7498edd975e05` |
| 단독 HTML | `handoffs/L1_Workspace_Viewer_v0_5_1_20261123_KST.html` | 156149 | `308249168e73475c2d0fd4a2807b321b8bd87743bd7d1e24a25767057447e59d` |

ZIP Git blob `90616a432879f9f253a31b54ad51ed0a79283626`。인계 Git blob `902e804d7d907a4bfb1fe42bf1c68e10275f7933`。
기존 v0.5.0 ZIP Git blob `6f62820eef5dace0950f3cf75ccd3c5d35612b5c` 및 SHA-256 `a133d8703cc36a7f74cce8de1fd37db757052ed6a44030bc05fea89a05c253fa` 보존.

## GPT 직접 확인

- GitHub connector로 공개 ZIP 전체 base64 취득 후 실제 bytes/SHA-256/CRC/34개 엔트리 중복·경로 이탈/manifest 33개 해시 PASS.
- ZIP의 standalone-preview.html과 공개 HTML 전체 동일 PASS. 공개 HTML·인계 bytes SHA는 체크섬 정본과 일치 PASS.
- 모든 source JS와 공개 standalone inline JS를 Node --check로 구문 확인 PASS. CSP inline script/style SHA 전량 일치 PASS.
- 게시된 v0.5.1 ZIP에서 기존 regression.cjs **10 PASS**, assistant-client.cjs **15 PASS**, 합계 **25 PASS**. 이번 재검증은 이전 버전 결과의 복사가 아니라 게시본에 대한 실제 실행.
- 기존 Write 3파일 바이트 불변 PASS.
- 이전 v0.5.0 인계의 버전·경로·날짜·ZIP bytes/SHA를 신판 기준으로 정규화해 비교: 모든 비어 있지 않은 줄이 신규 인계에 포함됨. 단 **2개 시험 근거 문장**은 신판에서 과거 버전 시험임을 명시한 문장으로 수정됨. 스킬 책임·서버 bridge·보안·미확인·복구·A01~A10 전체 계승, H01~H05 추가.
- L1Work handoffs/README.md의 v0.5.1 최상단 색인, CoWork CURRENT의 동일 공개 commit/ZIP/인계 기록 직접 확인.

## 검증 한계·진행 중 후보 정산

- 이 세션이 별도로 만들던 로컬 v0.5.1 후보의 **91 PASS는 공개 정본의 시험 결과로 사용하지 않음**. 동일 버전 동시 게시 발견 후 정본 ZIP을 덮어쓰지 않고 후보를 미게시로 종료.
- 최초 개발 stream의 active_change는 공개된 동일 사용자 범위로 정산. 공개 v0.5.1은 오늘의 업무 **목록·메뉴를 유지**하고 도우미 대화만 기본 숨김. 별도 후보의 추가 메뉴 숨김·route 변경은 채택하지 않음.
- Chromium 실행 시 환경의 socket 제한으로 브라우저가 시작되지 않았음. **BROWSER_E2E=NOT_RUN**. 모의 DOM/Python/정적 확인을 브라우저 PASS로 승격하지 않음.
- **FORMAL_INTEGRATION_GATE/LINUX_G0/REAL_LLM_AGENT/REAL_WRITE/HOST_DEPLOY=NOT_RUN**. 독립 리뷰는 기존 사용자 생략 결정 유지, 신규 REQUEST/READY/리뷰 호출 없음.
- `development_not_for_deployment`, `deployment_approved=false`. 실제 Linux 설치·LLM 연결·Write 활성화와 공개 전달은 별도.
- 원래 공개 인계의 Node NOT_RUN은 그 작성 당시 상태. 이후 이 재검증의 25 PASS로 보완하며 원래 문서·체크섬은 불변.

다음 한 동작: 업무 GPT에 위 v0.5.1 ZIP과 완결 인계서 두 파일만 전달해 실제 설치본 G0 및 A01~A10/H01~H05를 기존 승인 범위에서 검증. 이전 v0.5.0 별도 전달 불필요.
