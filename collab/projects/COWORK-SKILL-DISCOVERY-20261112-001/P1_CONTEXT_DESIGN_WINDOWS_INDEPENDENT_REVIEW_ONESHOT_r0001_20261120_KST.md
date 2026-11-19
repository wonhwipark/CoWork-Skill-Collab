# CoWork P1 설계 — Windows Claude Code 정식 리뷰 1회 실행 인계 r0001

- 작성: 2026-11-20 KST / **단일 요청·단일 실행 인계**
- 저장소: PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`
- 기존 Work: `collab/projects/COWORK-SKILL-DISCOVERY-20261112-001`
- **실제 수신자:** Windows Claude Code (실제 보호된 운영 정책/서명 도구 사용 가능한 Windows PC). 문서 게시만으로 실행 시작하지 않음.
- 사용자 지시: P1 계층 조회/근거 검증/한 화면 요약 설계 뒤 **Claude 협업 독립 리뷰 정식 요청 1회**. 이미 승인된 리뷰당 USD3 이하, 모델 호출 1회만. 중간 승인 반복 요청보다 유효한 현행 보호 승인 우선.

## 0. 기존 상태 확인 / 중복·소급 호출 방지
1. `collab/CONTEXT_BRIEF.md` 및 이 Work `CURRENT.md` 상단, `COWORK-AUTO-APPROVAL-20261115-001/CURRENT.md`, `REVIEW_TIER_TOKEN_BUDGET_V1.md`, 실제 Windows LIVE config/보호 승인 자격 읽기.
2. ID `REQ-COWORK-P1-CONTEXT-RETRIEVAL-DESIGN-R1-20261120`의 `collab/requests/`, `collab/reviews/`, `collab/receipts/` 및 Windows 처리 DB의 기존 ID/revision/source hash/processing key/UNCERTAIN 확인. 이미 유효한 결과가 존재하면 **게시·재호출 중단하고 그 결과만 회수**.
3. 기존 완료된 PEC·ACE·wiki UX·기타 리뷰, `GUARD UNCERTAIN`·legacy DESIGN 요청은 절대 재서명·재큐잉하지 않음.
4. 이 설계 리뷰는 업무 회사 소스·로그·지식·토큰/개인키를 열람/업로드하지 않음. 스킬 릴리스·Windows 운영변경·Linux Job 실행·PUBLIC 배송 0.

## 1. 입력 자료 (정확한 위치)
- 설계: `collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/P1_PROGRESSIVE_CONTEXT_EVIDENCE_DASHBOARD_DESIGN_r0001_20261120_KST.md`.
- 리뷰 질문: `collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/P1_PROGRESSIVE_CONTEXT_INDEPENDENT_REVIEW_QUESTIONS_r0001_20261120_KST.md`.
- **호스트 prepublication 입력 REQUEST 초안**: `collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/P1_CONTEXT_DESIGN_REQUEST_UNPOSTED_DRAFT_r0001_20261120_KST.md` (frontmatter와 본문을 정식 REQUEST의 정확한 후보 바이트로 사용; 실제 게시 전 PREPUBLICATION_PASS 요구).
- PRIVATE ZIP `collab/packages/cowork_p1_context_retrieval_design_r0001_1120_REVIEW_INPUT.zip`
- ZIP **24,410 bytes**, SHA-256 **`3ab8e1a4e5b59e6eea0fa2bd90dc044bb86289cd569cafdbed6158f19dda3327`**, Git blob **`79da67d0831cb1dde89f901d946f048fc0ef3af2`**; 4개 안전한 상대경로(01_DESIGN.md, 02_REVIEW_QUESTIONS.md, 03_SOURCE_MANIFEST.json, README.md). 입출력 SHA/CRC·source manifest 확인.
- 원본 기준 commit `b719b7355597e7027a53d7c6a3c0f0f8117b11f3`, ZIP 게시 commit `4f8183f6592c5d970e01c63c3c2e6ba61dad47e5`; 정식 REQUEST Commit A는 신규 commit이며 SOURCE_PIN은 A를 참조.

## 2. Windows LIVE 정책 사전검증 (필수, 아직 GPT 측 NOT_RUN)
1. Windows 로컬 **실제 LIVE** `reviewer.config.json`의 설치 버전·등록 정책과 적용 중인 보호된 위임을 읽기 전용 확인. 정책이 변경됐다고 추정하지 않음.
2. `collab/ops/review_request_gate.py select --live-config <WINDOWS_LIVE_CONFIG> --intent unified --required-budget-usd 3.00` 수행.
3. 반드시 `selected_run_policy_ref=POLICY-STATIC-V1` 및 그 정책의 **실제 USD3 호환**을 확인. 이어 `review_request_gate.py check --live-config <WINDOWS_LIVE_CONFIG> --intent unified --required-budget-usd 3.00 --request <EXACT_REQUEST_DRAFT_BYTES> --package <ACTUAL_PINNED_ZIP>`를 실제 실행하여 `PASS_PREPUBLICATION_ONLY` 확보. CLI 옵션은 설치된 도구 `--help`와 대조하고 미지원/불일치 시 강제 옵션이나 우회 금지.
4. **보호된 실제 승인**의 allowlist(프로젝트/skill_id/`cowork-context-design`), 한도·만료·신뢰 root·실제 signer 경로를 `approve_request.py check` 등 기존 로컬 정상 도구로 별도 확인. `PASS_PREPUBLICATION_ONLY`는 서명 허가가 아님.
5. STATIC=$1.50 또는 위임=$1인데 USD3 보호 서명/유효 수동 경로가 없으면 **`HOST_PREFLIGHT_BLOCKED / MODEL_CALLS=0 / REQUEST=NOT_POSTED`**. 이전 특정 wiki UX R1의 수동 DESIGN 예외를 이번 P1에 소급 사용하지 않음. 기존 LIVE/키/DB 수정 없음. 오류 근거만 별도 결과로 게시.

## 3. 모든 게이트 PASS 시, 정식 REQUEST + 1회 Claude 리뷰까지 연속 수행
1. 호스트 검증에 사용한 **정확히 동일한 REQUEST draft bytes**를 `collab/requests/REQ-COWORK-P1-CONTEXT-RETRIEVAL-DESIGN-R1-20261120/REQUEST.md`에 **create-only** 게시 (이미 있으면 중복 확인 후 중단). 원본 ZIP은 이미 PRIVATE `collab/packages/`에 있으므로 bytes 변경·중복 덮어쓰기 금지. Commit A의 정확한 SHA 기록, 원격 request 텍스트 SHA와 패키지 ZIP SHA/크기/CRC 검증.
2. SOURCE_PIN V1 생성: `collab/ops/source_pin.py create --repo-id 1451933830 --commit <COMMIT_A>`. JSON `"repo_id": "1451933830"` **문자열** 강제, `source_pin.py check --expected-repo-id 1451933830`, 원격 readback.
3. 기존 유효 보호 승인 도구로 **정확한 요청·revision·source pin·policy·max USD3**에만 서명. `APPROVAL_SIG.json`은 실제 signer가 생성해야 하며 GPT/문서로 위조하지 않음.
4. 해당 요청의 `READY.md`를 **마지막으로** 게시 (승인/원본/중복 검사 PASS 시). REQUEST만 생성돼도 READY 없으면 모델 호출 0이 정상.
5. 승인된 기존 LIVE watcher로 **이 ID만** 독립 Claude 설계 리뷰 `STATIC_ONLY` 1회 수행. 1회 이상/서브에이전트/자동 재리뷰 없음.
6. REVIEW_RESULT + RECEIPT + 고정 ID/rev/package SHA/처리키·실제 비용·중복 0을 GitHub PRIVATE로 readback. 비용/중단/게시 응답 UNCERTAIN이면 모델 **재실행하지 말고** 호스트 이력·영수증 보존/게시 전용 복구만.
7. 독립 리뷰 결과에 `ACCEPT/ACCEPT_WITH_CHANGE/REVISE/PARTIAL_SCOPE`·severity·Q01~Q10·미검증과 최소 변경/시험을 담고 GPT 최종 판정 대기. 개발 세션의 자체평가로 대신하지 말 것.

## 4. 결과 제출·정본 정리
- 결과 문서(차단돼도 한 건): `collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/CLAUDE_P1_CONTEXT_DESIGN_REVIEW_SUBMISSION_RESULT_FOR_GPT_20261120.md`.
- 실제 완료 시: `collab/reviews/REQ-COWORK-P1-CONTEXT-RETRIEVAL-DESIGN-R1-20261120/REVIEW_RESULT_1.md`, `collab/receipts/REQ-COWORK-P1-CONTEXT-RETRIEVAL-DESIGN-R1-20261120/RECEIPT_1.md`.
- 상태표: `LIVE_POLICY_PREFLIGHT`, `PROTECTED_SIGNER_CHECK`, `INPUT_SHA_CRC`, `DUPLICATE_CHECK`, `REQUEST_POSTED`, `SOURCE_PIN_STRING`, `APPROVAL_SIG`, `READY_LAST`, `INDEPENDENT_REVIEW`, `RECEIPT`, `MODEL_CALLS`, `COST_USD`, `GPT_DISPOSITION`, `BLOCKERS`, `NEXT_ONE_ACTION`.
- 해당 Work `CURRENT.md` 최상단에 짧은 실제 결과, 기존 `TRACKER.json` 현행 필드만 갱신. PRIVATE `main` 게시 commit·원격 SHA·본문 검증. `CONTEXT_BRIEF`·공통 카탈로그·PUBLIC 변경 불필요.
- 리뷰 실패/불가 시에도 **가능한 결과 기록까지** 마무리. Windows 호스트 보호 정책이 나중에 바뀌어도 이 비실행 인계/옛 요청의 소급 자동 실행을 허용하지 않음.

## 5. 최종 상태 구분
- 현재 이 문서의 게시: `P1_DESIGN=POSTED`, `REVIEW_INPUT_ZIP=POSTED`, `WINDOWS_PREFLIGHT=NOT_RUN_BY_GPT`, `FORMAL_REQUEST=NOT_POSTED`, `INDEPENDENT_REVIEW=NOT_RUN`, `NEW_MODEL_CALLS=0`.
- Windows의 **실제 성공**은 유효 보호 승인·READY·별도 reviewer 결과/영수증이 존재할 때만 인정. 문서 작성 자체를 '정식 리뷰 완료'로 표시 금지.
- 사용자 요청은 P1 설계·독립 리뷰까지. 구현·PUBLIC 배포·업무 GPT/LLM/Knowledge 실제 실행은 범위 밖이며 별도 판정 필요.

**다음 한 동작:** Windows Claude Code가 §0~4를 **한 번의 독립 리뷰 신청 실행**으로 조건부 연속 처리하고 결과 원문을 PRIVATE main에 게시. GPT는 receipt를 확인한 후 P1 설계 최종 판정.
