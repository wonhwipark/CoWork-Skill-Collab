# Viewer Wiki 최종 정합성 통합 v0.4.0 — 개발·L1Work 전달 결과 r0001

- 일자: 2026-11-21 KST, Work `L1-WORKSPACE-RAG-20261111-001`.
- 사용자 요청: 기존 GitHub 전체 Viewer 설계 대조 후, 확정 2안 팀 위키형 UI의 정합성을 맞춰 최종 ZIP/HTML 제공. L1Work 게시 및 업무 GPT HO 갱신까지 실행.
- 결론: **통합 개발 패키지 제작 + GitHub 공개 전달 + 원격 바이트 readback PASS**, **업무 Linux 실제 적용·브라우저 통합 E2E/Write 저장 NOT_RUN**. `development_not_for_deployment`.

## 1. 원본·변경 범위

| 입력 | 정확한 L1Work/main ZIP | SHA-256 |
|---|---|---|
| 확정 2안 팀 위키/Blue Gray | `l1-workspace-viewer-ui_v0_1_2_1121.zip` | `9be14c4c34c2a7d923d8b11c01fb0249d41e820861721f275001f0f7d499d9e3` |
| Write 프런트 v0.2.0 | `l1-workspace-viewer-write-ui_v0_2_0_1121.zip` | `9f2df44348478eb44615bddef8f211645fa1c07ed71d43580b4fb324e376b6f9` |
| 사용자 환경설정 v0.3.0 | `l1-workspace-viewer-preferences_v0_3_0_1121.zip` | `228c60bada8a92591f7ae855dfabe206e018d9e59970cf2d1b773d4d00072812` |

- 새 전체 개발 패키지: **[`l1-workspace-viewer-wiki-integrated_v0_4_0_1121.zip`](https://github.com/wonhwipark/L1Work/blob/main/l1-workspace-viewer-wiki-integrated_v0_4_0_1121.zip)** / **236,326 B** / SHA-256 **`474db38255de06540b888241c0ee96f94feb09e48d9ee767768f50469d5ee7b3`**, 20 entries, Git blob `f20fcc97d14afad2274d35fba620727cd78b2aa9`.
- 새 [standalone HTML preview](https://github.com/wonhwipark/L1Work/blob/main/handoffs/L1_Workspace_Viewer_Wiki_Integrated_Preview_v0_4_0_20261121.html) / **114,175 B**, Git blob `1a378141e37ecbddc17144192e7e697ca8a98858` — **가상 자료와 인라인 JS가 포함된 독립 시연**으로 운영 배포 금지.
- 첫 ZIP + HTML 커밋 `0cd3b2d36a79d939babfe73b3e7be716d47e1069`. 원격 ZIP 원본 bytes/full Base64/SHA 및 HTML full readback 직접 검증 PASS.
- 업무 GPT 인계: [L1Work HO r0001](https://github.com/wonhwipark/L1Work/blob/main/handoffs/L1_WORKSPACE_VIEWER_WIKI_INTEGRATED_V040_G0_AND_E2E_HANDOFF_r0001_20261121_KST.md), commit `9d5f17f9b8e4eae828a6de36bd2410f4d9dd820f`, Git blob `fab99f7d159149eb52559d09dc2924fbb18ca333` / 원격 본문 readback PASS. `handoffs/README.md` 색인 commit `689fb53b8e70adbb356d4b7b41edb803aa24775a`, blob `7f2ba40d952452a9aa0f7c0c865311e269f0814f` / readback PASS.
- 기존 세 ZIP 및 Work/Evidence/Workflow v1.6.75/Kernel v0.7.43/이전 HO·리뷰·영수증 불변.

## 2. 개선 사항(원본 소스 실제 연결, 단 운영 시험 아님)

1. 기존 확정 2안 Wiki 데스크톱 3영역·모바일 드로어/검색/MSC ·Blue Gray 스타일·SOC 대표 이슈번호/Work ID 표시 유지.
2. 기존 Write UI `write-client.js`, `write-ui.js`, `write-ui.css` 추가. 기존 검증된 Linux host adapter 없으면 Edit Disabled; 기본 무로그인 Read Only.
3. 사용자 환경설정 v0.3.0 JS/CSS 추가·보완. `#doc-actions`는 매 문서 이동시 지워지므로 환경설정 버튼을 **고정 `.topbar`로 이동**하여 문서 이동 중 소멸 위험 제거.
4. 표시 메뉴: Work/Knowledge 기본 표시·전체 파일 기본 감춤; index/transfers 기술 폴더 기본 숨김·쉼표 구분 추가 폴더, 테마/밀도/폰트·저장/취소/초기화·브라우저 localStorage. 프런트 필터는 **문서 권한 검증이 아니므로** Linux read/search/raw/cache/download/API 접근 게이트와 별개.
5. 탭별 마지막 문서·읽던 위치 메모리 복원, 동일 세션 검색어 유지, 고정 MSC 대상 `msc-six` 대신 related MSC의 ID 연결. 실제 Knowledge/MSC canonical owner·현장 API는 미검증.
6. `viewer-wiki-ui/standalone-preview.html`: asset을 1개 파일로 넣은 synth-only HTML. `viewer-wiki-ui/index.html`: 기존 데모 CSP fail-closed 유지(`connect-src none/frame-src none`)하여 운영 서버 adapter 연결 없는 상태 명시.

## 3. 실제 시험·미완료

| 시험/작업 | 결과 |
|---|---|
| 원본 ZIP 3종 실제 바이트 SHA-256 · 각 ZIP 엔트리 CRC | PASS |
| anchor 유일성/기존 원본 보존, ZIP 생성 후 전체 20 엔트리 CRC 및 SHA manifest 검증 | PASS |
| GitHub ZIP · HTML 원격 바이트 readback 및 HO/README 문서 | PASS |
| 신규 JS/HTML 실제 Chromium 1440/720/390/320 실행·기능 클릭·접근성 | **NOT_RUN** |
| 기존 전체 Viewer 테스트/신규 prefs+Write 호환 Node test 재실행 | **NOT_RUN** |
| Linux Viewer 실제 서비스·소스/branch/revision G0·B1/B2/B3·EAuth/E3/E4 | **NOT_RUN** |
| 실제 편집 인증/기존 Workflow/Kernel/CAS writer 저장·Evidence readback·rollback | **NOT_RUN** |
| 독립 코드 리뷰/운영 배포/Write 활성화 | **NOT_RUN** |

보안·원본 소유권 불확실성을 임의 PASS로 승격하지 않음. 기존 CSS Readability 중복 구간 완전 정리·실제 computed-style 최종 검증은 추가 확인 대상. 기존 파일 기반 샘플은 실제 팀 사용성 시험 아님.

## 4. NEXT_ONE_ACTION

업무 GPT/Linux Agent가 L1Work/main `handoffs/L1_WORKSPACE_VIEWER_WIKI_INTEGRATED_V040_G0_AND_E2E_HANDOFF_r0001_20261121_KST.md` 및 통합 ZIP의 고정 SHA를 확인해 기존 Linux Viewer에서 **UI/adapter 연결 및 실제 통합 브라우저 시험**을 먼저 시행. 미확인 Writer/인증·보안 게이트가 있을 때 Write disabled 유지, 운영 설치는 실제 호스트 유효 승인·백업/롤백/게이트 통과 이후에만.
