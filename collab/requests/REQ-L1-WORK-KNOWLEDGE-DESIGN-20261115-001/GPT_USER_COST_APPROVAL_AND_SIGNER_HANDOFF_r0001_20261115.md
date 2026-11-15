# Work→Knowledge 독립 설계 리뷰: 사용자 비용 승인 + Windows LIVE 서명·READY 원샷 인계

- 작성: 2026-11-15 KST / r0001
- GitHub PRIVATE: `wonhwipark/CoWork-Skill-Collab` / branch `main`
- **정확한 파일 경로:** `collab/requests/REQ-L1-WORK-KNOWLEDGE-DESIGN-20261115-001/GPT_USER_COST_APPROVAL_AND_SIGNER_HANDOFF_r0001_20261115.md`
- Work ID: `L1-WORKSPACE-RAG-20261111-001`
- 대상: `REQ-L1-WORK-KNOWLEDGE-DESIGN-20261115-001`, `request_revision=1`
- **사용자 명시 승인(본 채팅):** "REQ-L1-WORK-KNOWLEDGE-DESIGN-20261115-001의 독립 설계 리뷰 1회, 최대 $1 비용을 승인해. 기존 Windows 서명자로 APPROVAL_SIG를 생성·검증하고 READY를 마지막에 게시해줘. GitHub LIVE Watcher의 자동 리뷰 결과와 영수증을 확인한 뒤 GPT 판정까지 진행해줘. 추가 유료 호출은 금지해줘." 이후 "끝까지 진행해줘".
- **승인 범위:** 이번 요청/revision/고정 ZIP에 대한 `POLICY-STATIC-V1`, **최대 USD $1.00, Claude 독립 리뷰 모델 호출 총 1회**. 이전 승인/남은 예산의 타 요청 전용, 자동 재리뷰, 정책 상향은 불허.
- **중요:** 이 MD는 사용자 의사 기록 및 실행 인계이며 정식 암호학적 `APPROVAL_SIG.json`이 아니다. GitHub 문서 게시만으로 자동 실행되지 않는다. Windows의 **기존 신뢰 서명자/키**와 운영 v0.2.20 verifier가 서명·검증해야 한다.

## 고정 입력 및 사전 검증 — 변경 금지

- REQUEST: `collab/requests/REQ-L1-WORK-KNOWLEDGE-DESIGN-20261115-001/REQUEST.md`, `state=REQUESTED`는 기존 Validator에서 PASS. 사용자 원본 서술·revision·bytes 변경 금지.
- 원시 REQUEST SHA-256 (기존 호스트 게시 영수증): `a7a1b461a515cfe1d033e2072fd2015999a5ef22ec4bdcb24ab30eb03a28cfb7`, 3974 B로 호스트 보고(서명 시 **실제 바이트 재확인**; 불일치면 fail closed).
- ZIP: `collab/packages/work-to-knowledge-design_r0001_1115_REVIEW_INPUT.zip` (논리 경로 `/SKILL-COLLAB/packages/work-to-knowledge-design_r0001_1115_REVIEW_INPUT.zip`), 28,805 B, `SHA-256=4ccede070d03e497a8d821fcabc8092c0d46045b245b64dabf023abc83daa417`. 문서 5개 설계 입력. `SKILL.md` 추가 금지.
- Commit A: `0a46fea5f7f63c68c5cb12cfa35bfaed00c2c1a3`; 기존 `collab/requests/REQ-L1-WORK-KNOWLEDGE-DESIGN-20261115-001/SOURCE_PIN.json` repo ID `1451933830` (**변경·재게시 금지**).
- Windows 운영 Watcher v0.2.20의 read-only 격리 Validator preflight PASS 보고 및 GPT 판정: `collab/projects/L1-WORKSPACE-RAG-20261111-001/CLAUDE_REQUEST_VALIDATOR_PREFLIGHT_RESULT_FOR_GPT_20261115.md`, `GPT_REQUEST_VALIDATOR_PREFLIGHT_DISPOSITION_r0001_20261115.md`.
- GitHub LIVE `ACTIVE_PROVIDER=GITHUB` Windows 호스트 보고. 운영 Watcher는 READY 없음으로 `WAIT_INPUT` 확인. 별도 watcher/reviewer 기동 금지.

## Windows Claude Code 원샷 절차 — 실제 모델은 LIVE watcher만 1회 호출

1. `collab/START_HERE.md`, migration `CURRENT.md`, 이 문서, `REQUEST.md`, `SOURCE_PIN.json` 확인. 실행 직전 `APPROVAL_SIG.json`, `READY.md`, dispatch/review/receipt, 운영 DB 격리 바이트 복사본, 기존 수동 리뷰 `L1-WORK-KNOWLEDGE-DESIGN-20261114-001`의 완료/불확실 여부를 **중복 검사**. 이미 실행·정산/실행 중/불확실하면 새 서명·호출 0, 결과만 회수.
2. 현재 GitHub repo ID, commit A, REQUEST raw sha, ZIP raw bytes/size/SHA/CRC, 정책·일일 상한·기존 신뢰 루트·사용자 $1/1회 승인, active baseline·만료·모드 검증. 실패하면 해당 항목만 BLOCKED, 모델 0. 개인키/토큰/회사자료 원격 게시 금지.
3. **사용자 비용 승인 재질문 없이** 기존 Windows 승인 서명자로만 이번 ID, revision, 요청 SHA, ZIP SHA, commit/repo binding, `POLICY-STATIC-V1`, 예산 `USD 1`, 호출 1회, 만료에 묶인 `APPROVAL_SIG.json`을 생성. 유효한 서명 자체를 운영 verifier로 확인하고 GitHub PRIVATE `main`의 `collab/requests/REQ-L1-WORK-KNOWLEDGE-DESIGN-20261115-001/APPROVAL_SIG.json`에 게시·원격 재조회. **SOURCE_PIN.json을 도구가 덮어쓰려 하면 중지**하고 기존 핀을 사용하는 지원되는 sign-only 경로를 확인. 승인 문서 자체를 서명으로 간주 금지.
4. 승인 서명 PASS 뒤에만 정식 `SKILL_COLLAB_READY_V1`의 `READY.md`를 해당 요청 폴더에 **마지막으로** 게시. request_path, request SHA, package SHA, 실제 운영 baseline의 바이트/정합성을 다시 검증하고 재조회. 빈/더미 READY 금지.
5. 이미 기동 중인 **GitHub 단일 LIVE watcher**가 READY를 확인하여 유효한 검증 뒤 독립 Claude 리뷰를 **최대 한 번** 자동 디스패치하도록 둔다. Windows에서 두 번째 watcher/수동 `claude` review/독립 서브에이전트를 따로 실행하지 말 것. 비용 $1를 넘길 가능성이 확인되면 시작하지 말 것. model uncertainty → REVIEW_UNCERTAIN 봉인; 추가 호출 0.
6. `collab/dispatch/REQ-L1-WORK-KNOWLEDGE-DESIGN-20261115-001/DISPATCH_1.md`, `collab/reviews/REQ-L1-WORK-KNOWLEDGE-DESIGN-20261115-001/REVIEW_RESULT_1.md`, `collab/receipts/REQ-L1-WORK-KNOWLEDGE-DESIGN-20261115-001/RECEIPT_1.md` 및 실제 사용량 receipt을 원격 readback. 요청 ID/rev/ZIP SHA, 실제 model_calls, 실제 cost, 독립성, 결과 파일·hash 및 Telegram 알림(관측된 경우만) 확인. 게시 장애는 publish-only; 모델 재호출 금지.
7. `SUBMISSION_STATUS.json`, 해당 프로젝트 `CURRENT.md` 최상단/Tracker의 **이번 요청 부분만** 실제 PASS/FAIL/BLOCKED/NOT_RUN으로 갱신. 실측 Windows 결과 `collab/projects/L1-WORKSPACE-RAG-20261111-001/CLAUDE_WORK_KNOWLEDGE_DESIGN_LIVE_REVIEW_RESULT_FOR_GPT_20261115.md`에 게시·remote byte/SHA readback. GPT가 그 실제 리뷰 원문과 receipt을 대조해 항목별 최종 판정. CLPR/Knowledge 배포·운영 Task/DB/Notifier/설정 불변.
8. 위 각 단계는 **기존 승인 범위에서 중간 승인을 다시 묻지 않고** 수행. 서명키·운영 호스트 접근 실패면 임의 우회하지 않고 해당 실패를 BLOCKED로 기록, 나머지 무비용 검증 및 결과 보고까지 마친다. 유료 Claude 리뷰 0~1회 외 호출 금지.

## 현재/다음 한 동작

- 승인: **YES** (비용/대상 범위 명시), 사전입력 검증: **PASS** (호스트 보고).
- 본 GPT 게시 시점: `APPROVAL_SIG=NOT_POSTED`, `READY=NOT_POSTED`, `REVIEW=NOT_RUN` (GitHub 원격 확인), 운영 Windows 실시간 검증/서명 **NOT_RUN**.
- **NEXT_ONE_ACTION:** Windows Claude Code가 이 문서에 정의된 기존 signer와 LIVE watcher 흐름을 실행해 서명→READY→독립 리뷰 결과/receipt을 게시.

### Windows Claude Code 복사용 원샷 명령

```text
GitHub PRIVATE wonhwipark/CoWork-Skill-Collab/main의 collab/requests/REQ-L1-WORK-KNOWLEDGE-DESIGN-20261115-001/GPT_USER_COST_APPROVAL_AND_SIGNER_HANDOFF_r0001_20261115.md를 읽고 사용자 승인(이번 설계 독립 리뷰 1회, 최대 USD1)을 그대로 실행해줘. 해당 REQUEST/ZIP/Commit A/SOURCE_PIN은 v0.2.20 Validator PASS이므로 변경하지 마. 먼저 중복/불확실/비용한도를 확인하고 기존 Windows 서명자로 이번 요청의 APPROVAL_SIG 생성·실검증·remote readback, READY를 마지막에 게시해줘. ACTIVE_PROVIDER=GITHUB 단일 LIVE watcher가 자동으로 리뷰 최대 1회만 수행하게 두고 두 번째 reviewer나 watcher는 기동하지 마. 결과/receipt/사용량을 원격 조회해 이번 요청의 SUBMISSION_STATUS, 프로젝트 CURRENT/TRACKER, CLAUDE_WORK_KNOWLEDGE_DESIGN_LIVE_REVIEW_RESULT_FOR_GPT_20261115.md까지 원샷 게시·검증해줘. 모델 추가 호출/재시도 0. signer가 없거나 미검증이면 READY 없이 BLOCKED로 정직하게 보고하고 운영은 변경하지 마.
```
