# Windows Claude Code — 위키 UI 시각 리뷰 1건 USD3 수동 부트스트랩·완료 원샷 r0002

- 날짜: 2026-11-19 KST
- PRIVATE 정본: `wonhwipark/CoWork-Skill-Collab` / branch `main`
- 대상 Work: `collab/projects/L1-WORKSPACE-RAG-20261111-001`
- 요청 ID: `REQ-L1-WORKSPACE-WIKI-UI-UX-R1-20261119`, revision `1` (동일 ID 신규 REQUEST가 존재한다면 중복 생성·재호출 금지)
- **r0001 제출 원샷 대체**: `WIKI_UI_UX_R1_WINDOWS_SUBMIT_ONESHOT_r0001_20261119_KST.md`의 `--intent unified` 단일 경로가 현재 Windows LIVE STATIC=$1.50 때문에 BLOCKED라는 실제 호스트 결과(commit `29ede587f09f850ea636195f8b608936c26f4c14`)를 인정. r0001 원본/결과를 삭제하거나 완료 처리하지 않음.
- 사용자 이전 승인: 이 위키 UI 완성본의 화면 구성·가독성·스타일·시인성에 대한 **정식 독립 리뷰 1회, 최대 USD3**. 사용자 최신 “개선해줘” 실행 지시를 근거로 **이번 요청만 이미 운영 등록된 `POLICY-STATIC-V1-DESIGN=$3`을 수동 서명 transport로 사용할 수 있도록 사전검증 경로를 정정**. **장기 비용 등급 구분을 복원하거나 다른 REQUEST의 권한을 확대하는 결정은 아님**.
- 중요한 신뢰 경계: 사용자/정본의 $3/1회 지시와 **실제 Windows 로컬의 유효한 수동 signer 권한·승인 검증은 별개**. GitHub 문서·채팅 주장을 승인 서명으로 취급 금지. 관리자 PIN/보호 자격이 없으면 그 단계만 BLOCKED 보고; 정책 우회·키 생성·JSON 직접 수정 없음.
- **현재 Windows LIVE는 v0.2.25**, 보호된 자동 위임 max_request_usd=$1.00, STATIC=$1.50, DESIGN=$3, LARGE=$3 (2026-11-19 호스트 마지막 확인). **v0.2.27은 DEV 후보**이므로 이번 UX 리뷰를 위해 watcher 배포 또는 unified 정책 활성화 금지. 모델 호출 총 1회 최대 USD3, 실행 재시도/유료 smoke/부속 agent 생성 0.

## Windows에서 한 번에 실행: 조건 충족 시 정식 리뷰 결과까지

1. **최신 상태/중복 선조회.** `collab/CONTEXT_BRIEF.md` → 위 Work `CURRENT.md` 상단 최신 결과 → `CLAUDE_WIKI_UI_UX_R1_SUBMISSION_RESULT_FOR_GPT_20261119_KST.md` → 본 문서·실제 정책/서명 계약 확인. 기존 완료 `REQ-L1-WORKSPACE-LOCAL-VIEWER-DESIGN-R1-20261118` 및 UX-OWNER 후보/운영 DB·UNCERTAIN/REMOTE READY/receipt를 다시 확인. 이번 ID의 REQUEST/READY/RESULT가 이미 있으면 그 처리키·영수증을 우선 정산하고 재호출 0.
2. **고정 리뷰 패키지 그대로 사용.** PRIVATE `collab/packages/l1-workspace-wiki-ui_v0_1_0_1119.zip`, source commit `17ac2b39ad01dc3e01df467ada698fbac8b5c399`, 267140 bytes, SHA-256 `411553e74e76bb82237fd2ebef65169769e4dbe4cfd2231afb5afd38559b10a9`. ZIP CRC/경로/4개의 필수 screenshot 존재·JPEG SHA를 기존 [manifest](WIKI_UI_UX_R1_REVIEW_MANIFEST_r0001_20261119_KST.md)와 검사. 코드·ZIP·기존 리뷰 결과 변경 없음.
3. **유효한 현행 수동 $3 정책 선택 (핵심 수정).** 실제 Windows 로컬 `reviewer.config.json`으로 `collab/ops/review_request_gate.py select --live-config <WINDOWS_CONFIG> --intent design --required-budget-usd 3.00` 실행. `POLICY_COMPATIBLE_NOT_APPROVED`이고 `selected_run_policy_ref=POLICY-STATIC-V1-DESIGN`/expected `3.00`인지 확인. 단, DESIGN 미등록이고 이미 등록된 LARGE $3을 선택하면 **후보의 `run_policy_ref`만 같은 값으로 고정한 새 비실행 draft**를 만들어 해당 selected ref에 재검증; 임의 가격 하향·상향 금지. `--intent unified`/STATIC=$3은 이번 예외에서 사용 금지(운영에 미등록). **STATIC $1.50 대체·비용 변경·자동 위임 $3 상향 금지**.
4. **리뷰 초안과 승인 경로 검증.** 신규 비실행 후보 `WIKI_UI_UX_R1_REQUEST_MANUAL_BOOTSTRAP_DRAFT_r0002_20261119_KST.md`를 UTF-8 LF **원시 바이트**로 가져와 `review_request_gate.py check --live-config <WINDOWS_CONFIG> --intent design --required-budget-usd 3.00 --request <EXACT_DRAFT> --package <EXACT_ZIP>` → `PASS_PREPUBLICATION_ONLY`/ZIP SHA/request SHA 기록. 로컬 `approve_request.py check`/기존 신뢰 루트/실제 signer 자격·본 건의 $3 수동 승인 사용 범위·만료·scope를 별도 확인. **Gate 통과는 실제 사용 승인과 다름**; signer 권한이 없다면 REQUEST·READY를 게시하지 않고 `MANUAL_SIGNER=BLOCKED`로 정확히 종료. 종전 지침의 수동 `-DESIGN/-LARGE` 사용 금지는 **이 특정 ID에 한해 최신 r0002가 대체**, 타 ID/프로젝트에는 확대 적용 금지.
5. **정식 REQUEST 게시/고정 SOURCE_PIN/수동 승인.** 1~4 PASS와 승인 자격 확인 시에만 `collab/requests/REQ-L1-WORKSPACE-WIKI-UI-UX-R1-20261119/REQUEST.md`를 EXACT_DRAFT 바이트로 CREATE-ONLY 게시. GitHub remote readback으로 request_sha256/ZIP SHA·size·Commit A의 정확한 source_commit 확인. `collab/ops/source_pin.py`로 repo_id JSON **문자열**과 Commit A를 고정하여 `SOURCE_PIN.json` CREATE-ONLY 게시·재조회. 정식 Windows 로컬 수동 signer의 유효한 서명을 받아 `APPROVAL_SIG.json` 게시. `READY.md`는 **마지막**에만 게시하고 원격 값/해시/동일 request_ID/revision·처리키 확인. token/키/PIN GitHub 업로드 금지, 임의 재서명·READY 없는 유료 실행 금지.
6. **독립 Claude reviewer 1회만 실행.** READY가 유효할 때 기존 GitHub watcher v0.2.25의 승인/중복 검증 경로로 유료 모델 최대 1회·USD3 상한 실행; 개발 대화형 세션이 별도 유료 호출하지 말 것. 리뷰어는 ZIP 내부 `screenshots/wiki-1440.jpg`, `wiki-390.jpg`, `wiki-320.jpg`, `msc-12.jpg` **4장 직접 열람** 후 화면 구성·가독성·스타일·사용자 시인성 네 축 평가. 이미지 열람 불가/정적 snapshot 한계는 `VISUAL_INSPECTION=NOT_RUN/PARTIAL_SCOPE` 정직하게 남기기. 비민감 합성 UI 외 업무 자료 추가 없음.
7. **결과+회수+후속 최소 보완 한 번에.** `collab/reviews/<ID>/REVIEW_RESULT_1.md`, `collab/receipts/<ID>/RECEIPT_1.md`, dispatch 등 실제 영수증의 source/request/ZIP SHA·reviewer version/비용/호출 횟수 대조. 결제·호출 불확실/게시 실패면 재호출 없이 publish-only 또는 UNCERTAIN 보존. 사용자 중간 질문 없이 같은 Work `CLAUDE_WIKI_UI_UX_R1_RESUME_RESULT_FOR_GPT_20261119_KST.md` + `CURRENT.md`/기존 `TRACKER.json` 현행 필드 갱신 후 PRIVATE main commit·원격 bytes SHA 검증. 독립 리뷰에서 개선 사항이 발견되면 동일 UI Work에 CSS/HTML 보완 후보·자체 회귀까지 가능한 범위 진행하되, **검토된 고정 ZIP을 수정하거나 새 유료 리뷰를 자동 실행하지 말 것**. GPT 최종 리뷰 판정과 공개 재전달/실제 업무 Linux 배포는 별도 게이트.

## 기존 공개 전달과 충돌 방지
- 사용자 지시로 `wonhwipark/L1Work/main`에 UI ZIP·HTML·업무 GPT 인계 MD는 **이미 PUBLIC 게시 완료**(content commit `c9e9be9e84629bcdba07c1045384dac6bfd9bc93`). 이번 시각 리뷰는 그 이후의 **추가 검증**이며 이미 완료한 전송을 `NOT_POSTED`로 되돌리지 않음.
- `BUSINESS_GPT_REVIEW_FEEDBACK=WAIT_REVIEW_RESULT`와 `PUBLIC_HANDOFF=ALREADY_POSTED` 구분. 기존 업무 GPT 통합 호스트 G0/API/B1~B3 BLOCKED는 이번 UX 리뷰만으로 해제되지 않음.

## 강제 범위
- 신규 REQUEST는 **이번 한 ID/revision만**. 사용자 승인된 $3 한 건 외 유료 재리뷰·새 유료 smoke 0.
- v0.2.27 설치, watcher 정책/위임/키/DB/Task/Notifier 변경 0. 기존 과거 DESIGN R1/LARGE R2/Guard UNCERTAIN 재서명·재큐잉 0.
- `REVIEW_STATUS`, `HOST_POLICY_SELECTED`, `PREFLIGHT`, `MANUAL_SIGNER`, `REQUEST_POSTED`, `SOURCE_PIN`, `READY`, `REVIEW_RESULT`, `RECEIPT`, `VISUAL_INSPECTION`, `MODEL_CALLS`, `COST`, `GPT_DISPOSITION=PENDING`, `NEXT_ONE_ACTION` 각각 PASS/FAIL/BLOCKED/NOT_RUN으로 분리.
- 이 문서·비실행 후보 게시 자체는 signer/READY/모델 호출을 시작하지 않음. **NEXT_ONE_ACTION:** Windows Claude Code가 이 r0002 단일 파일 1~7을 한 번 수행하고 본 Work에 결과 게시, GPT가 실제 결과 최종 판정.
