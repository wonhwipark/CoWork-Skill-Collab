# Viewer UI v0.1.1 선행 구현 개발 후보 — 결과 기록

- 시간: 2026-11-21 KST
- 목적: 사용자가 제기한 "기존 업무 Linux Viewer에서 업무 GPT보다 먼저 미리 구현할 수 있는 부분이 없나?"에 대한 GPT 직접 개발·시험.
- Work: `L1-WORKSPACE-RAG-20261111-001`
- **상태: DEVELOPMENT_CANDIDATE, NOT_FOR_DEPLOYMENT**
- 기존 확정: 본 업무 Viewer는 사용자 요청으로 전역 ID/PW 제거·동료 무로그인 Read Only. [수정] 클릭 때만 편집 전용 인증, 실제 writer/G0 보안 게이트 필요. 원본 Work ID/폴더 변경 금지. 검증된 SOC 등의 이슈번호는 제목 맨 앞.
- PUBLIC 업무 GPT 인계: `wonhwipark/L1Work/main/handoffs/L1_WORKSPACE_VIEWER_TWO_PHASE_IMPLEMENTATION_ONESHOT_HANDOFF_r0001_20261120_KST.md` (이전 게시 자료로 유지).

## 1. 작성한 실제 코드

- `assets/work-labels.js` — 검증된 `issueKey` 선두/기존 제목 정규화, 중복 prefix 제거, Work ID 폴백, 제목·번호·Work ID 검색용 공통 함수. 새 영속 스키마/API 아님. 임의 문서 문자열에서 대표 이슈번호 추출 금지.
- `assets/edit-prototype.js` + `assets/edit-prototype.css` — [수정]→수정 요청 UI 골격, 임시 브라우저 메모 입력. ID/PW 수집·실제 인증/ACL·Diff·save·LLM 호출·원본 쓰기는 **전부 비활성화**.
- `apply_to_v010.py` — 이미 L1Work PUBLIC에 있는 `l1-workspace-wiki-ui_v0_1_0_1119.zip`의 SHA256 `411553e74e76bb82237fd2ebef65169769e4dbe4cfd2231afb5afd38559b10a9` 고정 검사 후 4개 실제 소스 `index.html`, `assets/app.js`, `adapters/adapter.js`, `fixtures/demo-data.js`의 anchor 패치. 불일치/경로이탈/CRC 오류면 fail-closed. 원본 ZIP 덮어쓰기 금지.
- `preview.html` — 가상 `SOC-1234` 등으로 제목/ID와 [수정] 골격 화면을 설명하는 **합성** 자료. 실제 제품 코드·MSC·비밀자료 없음.
- `tests/work-labels.test.cjs`, `tests/patch.test.py`, `README.md`.

## 2. 실제 확인과 한계

| 항목 | 판정 |
|---|---|
| Work labels 18개 Node 단위시험 | PASS (18/18) |
| patch exact anchor 모의시험 7건 | PASS (7/7) |
| 실제 PRIVATE main 원본 v0.1.0의 소스 anchor 16개 일치 | PASS (16/16, GitHub 원문 조회) |
| JS syntax `node --check` + Python `py_compile` | PASS |
| 개발 후보 ZIP CRC, 8개 파일, 12,573 bytes | PASS |
| 실제 PUBLIC v0.1.0 전체 ZIP 다운받아 패치·기존 56+19 회귀 | NOT_RUN (container 외부 다운로드 차단) |
| 합성 브라우저 렌더 자동시험 | NOT_RUN (Chromium file/loopback 접근 관리자 차단) |
| 실제 업무 Linux Viewer G0·API/편집 인증·writer·B1/B2/B3·E3/E4 | NOT_RUN / NOT_VERIFIED |
| 독립 코드 리뷰/실서비스 운영 배포 | NOT_RUN |

## 3. 산출물과 전달 한계

- 이 GPT 응답에 **다운로드 가능한 ZIP 파일** 생성 완료: `l1-workspace-viewer-prebuild_v0_1_1_1121.zip`, 12,573 bytes, SHA-256 `20e635802b3480c5b3c9888e3599316e158ee0aa0c50deeac6b53098459ce9f8`.
- 이 GPT 응답에 **독립 미리보기 HTML** 생성 완료: `l1-workspace-viewer-prebuild-preview_20261121_KST.html`, 7,831 bytes, SHA-256 `f1d8d3a3ea077e505eed7cf096ac6a330e9855dd5bbf64ae14ccda3edf19602e`.
- **주의: 코드 ZIP 및 HTML은 현재 대화의 사용자 다운로드 첨부이며 GitHub PRIVATE/PUBLIC에 바이너리로 게시한 것은 아님.** 이 MD의 SHA만으로 다른 창에서 바이트를 다운로드할 수 있다는 뜻이 아님. 실제 호스트에 자동 배송·설치·활성화도 아님.
- 기존 본 Work 설계 r0001~r0004/R1 결과/영수증·L1Work PUBLIC 인계와 기존 ZIP은 불변.

## 4. 다음 한 행동

업무 GPT/Linux 로컬 Agent에서 기존 UI ZIP + 이 개발 후보 ZIP을 둘 다 이용해 정확한 원본 적용·회귀검사를 수행. 실제 Viewer source·branch/revision/Work issueKey metadata·보안/인증/원본 writer G0를 확인하고 가능한 UI 개선만 기존 service code에 통합. 별도 실제 호스트 승인과 B1~B3/E3/E4 게이트가 확인될 때만 운영 변경. 외부로 제품 코드/로그/자격증명/실제 MSC 반출 금지.
