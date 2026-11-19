# Windows Claude Code — 완성 위키 UI 시각·사용성 리뷰 1회 제출 원샷

- 작성: 2026-11-19 KST
- 저장소: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`
- Work: `collab/projects/L1-WORKSPACE-RAG-20261111-001/`
- 이 문서 최종 경로: `collab/projects/L1-WORKSPACE-RAG-20261111-001/WIKI_UI_UX_R1_WINDOWS_SUBMIT_ONESHOT_r0001_20261119_KST.md`
- 신규 ID: `REQ-L1-WORKSPACE-WIKI-UI-UX-R1-20261119`, revision 1
- REQUEST 후보: 같은 Work의 `WIKI_UI_UX_R1_REQUEST_DRAFT_r0001_20261119_KST.md`
- 사용자 지시: 업무 GPT 전달 전에 완성본 화면 구성·가독성·스타일·시인성 독립 리뷰 요청. **신규 최대 USD 3/1회 사전 승인 재사용**, 같은 승인을 다시 물을 필요 없음.

## 현재 사실과 목표

GPT가 비민감 실제 UI 코드/4장 캡처/설계/시험을 포함한 ZIP을 PRIVATE에 이미 게시·원격 bytes 확인했어요. 이 원샷은 구 설계 리뷰를 재실행하지 않고 **완성본 UI 시각 리뷰**를 신규 1회 제출하는 경로예요.

최신 자동 승인 Work에 따르면 `POLICY-STATIC-V1` 단일 USD 3 적용은 구 DESIGN 소급 실행 위험으로 보류됐고, v0.2.27은 개발 후보예요. **사용자 USD 3 승인 사실과 Windows LIVE 정책/보호 위임 적용은 별개**예요. 실제 설치본을 확인하기 전 이 요청을 정식 REQUEST/READY로 게시하거나 v0.2.27을 설치하지 마세요. 이 원샷 자체는 운영 설정·위임·기존 pending을 변경할 권한을 추가하지 않아요.

## 한 번에 실행할 절차

1. `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/CURRENT.md`에서 최신 호스트 적용 결과 확인. 실제 운영 service/config·보호 서명 경로·유효 위임/allowlist/expiry를 READ_ONLY로 대조. 승인 재요청 대신 기존 USD 3/1회 사용자 지시를 재사용하되 문서의 승인 주장을 서명으로 취급하지 않음.
2. 위 신규 ID의 원격 REQUEST/PIN/SIG/READY/DISPATCH/RESULT/RECEIPT와 Windows DB 중복·UNCERTAIN 확인. 이전 `REQ-L1-WORKSPACE-LOCAL-VIEWER-DESIGN-R1-20261118`은 완료·재호출 금지. `REQ-L1-WORKSPACE-VIEWER-UX-OWNER-R1-20261119`는 과거 설계 후보와 이번 범위의 중복을 대조하되 자동 종결/취소/재실행하지 않음. 동일 완성본 리뷰가 이미 있으면 신규 게시 없이 기존 결과만 회수.
3. 정확한 ZIP `collab/packages/l1-workspace-wiki-ui_v0_1_0_1119.zip`을 고정 content commit `17ac2b39ad01dc3e01df467ada698fbac8b5c399`에서 읽고 267140B / SHA-256 `411553e74e76bb82237fd2ebef65169769e4dbe4cfd2231afb5afd38559b10a9` / CRC·경로·manifest 검사. REQUEST 후보를 CRLF 변환 없이 UTF-8 원시 bytes로 로컬 복사.
4. 현행 `collab/ops/review_request_gate.py`의 `select --live-config <실제 config> --intent unified --required-budget-usd 3.00` 실행. 실제 LIVE에서 `POLICY_COMPATIBLE_NOT_APPROVED`, STATIC/USD3일 때만 `check --live-config <실제 config> --intent unified --required-budget-usd 3.00 --request <후보> --package <검증 ZIP>`으로 `PASS_PREPUBLICATION_ONLY` 확인. **과거 skill/$1.50 또는 DESIGN/LARGE 선택으로 우회 금지.** GPT의 합성 사전시험은 호스트 select/check를 대체하지 않음.
5. 게이트가 막히면 config/위임/키/엔진·DB를 이 작업에서 수정하지 않고 **BLOCKED_LIVE_POLICY** 또는 실제 오류코드로 결과 게시. 신규 정책 설치는 관련 자동 승인 Work의 기존 승인/독립 리뷰/운영 게이트에서 처리. GPT에게 같은 비용 승인을 다시 요구하지 않음. 부분 결과/검토 대상 고정까지는 마무리.
6. 호스트 게이트 PASS와 유효 보호 승인 경로가 모두 확인되면, 후보의 **원시 bytes 그대로** `collab/requests/REQ-L1-WORKSPACE-WIKI-UI-UX-R1-20261119/REQUEST.md`에 게시. 이 파일과 고정 ZIP이 함께 조회되는 실제 Commit A를 확인하고 원격 bytes/SHA 재검증. `collab/ops/source_pin.py`로 신뢰된 실제 repo numeric ID를 **JSON 문자열**로, Commit A를 실제 값으로 SOURCE_PIN 생성·검증·게시. 예상 repo ID 1451933830은 실제 보호 신뢰 루트와 대조.
7. 실제 설치본의 공식 `approve_request.py check`와 유효 수동 signer 또는 설치·활성 위임 범위에서만 APPROVAL_SIG 생성. 보호 위임 미활성이라도 유효한 공식 수동 USD3 경로가 있으면 이를 사용할 수 있으나 signer 권한·정책 검증을 생략하지 않음. 임의 키·서명·보호 JSON 편집 금지. 승인 후 **READY 마지막 게시**. 기존 단일 LIVE watcher 1회만; 개발 Claude가 별도로 유료 리뷰/Agent를 중복 호출하지 않음.
8. 리뷰어에게 REQUEST 본문의 4축과 **실제 JPEG 열람 필수**를 전달. 정적 읽기 전용 리뷰, ZIP 스크립트/테스트/서버 실행 0. 이미지 미지원이면 시각 리뷰 PARTIAL_SCOPE로 기록, 임의 추가 이미지 모델/전송 0.
9. 결과/영수증을 `collab/reviews/REQ-L1-WORKSPACE-WIKI-UI-UX-R1-20261119/REVIEW_RESULT_1.md`, `collab/receipts/REQ-L1-WORKSPACE-WIKI-UI-UX-R1-20261119/RECEIPT_1.md`에 게시·readback. 완료·불확실 실행 이력을 보존. 결과 게시 실패만으로 모델 재호출 금지.
10. 같은 Work `CLAUDE_WIKI_UI_UX_R1_SUBMISSION_RESULT_FOR_GPT_20261119_KST.md`에 아래 상태/근거를 게시하고 CURRENT/TRACKER 현행 필드만 맞춤. GPT 판정까지 **업무 GPT 전달=HOLD**. 실제 전달 이후로 자동 간주하지 않음.

## 반드시 남길 결과

`HOST_SELECT_CHECK / DUPLICATE_CHECK / FORMAL_REQUEST / SOURCE_PIN / APPROVAL_SIG / READY / DISPATCH / REVIEW_RESULT / RECEIPT / VISUAL_INSPECTION / MODEL_CALLS / ACTUAL_COST / BLOCKER / NEXT_ONE_ACTION`

미실행은 NOT_RUN, 직접 읽지 않은 것은 NOT_VERIFIED. CURRENT/영수증에 원격 commit·REQUEST/ZIP 해시·실제 바이트 확인을 남겨요. BLOCKED라면 최초 실패 게이트와 기존 권한 내 다음 한 조치를 짧게 보고해 주세요. 자동화 코드나 LIVE를 바꾸기 위한 신규 Work/스키마/예산 예외를 만들지 않아요.
