# CoWork GitHub Actions — GPT 자동 판정 + Telegram 실연동 원샷 실행 인계
- 작성: 2026-11-23 KST
- 정본: `wonhwipark/CoWork-Skill-Collab`, branch `main` (**실제 GitHub 공개 저장소; 민감 정보 게시 금지**)
- Work: `COWORK-DROPBOX-TO-GITHUB-MIGRATION`, 연계 `COWORK-AUTO-APPROVAL-20261115-001`
- 사용자 최신 지시: **기존 비용·지출 상한 게이트 재승인 요구 없이 GPT API 자동 판정 활성화 및 Telegram까지 E2E 진행**. 허용된 유효 API 인증/모델/키를 재사용. 새 API 키 생성/키 교체, 유료 호출의 무제한 반복, Windows watcher LIVE 변경까지 승인한 것은 아님.
- GPT ↔ Windows 경계: 이 문서 게시만으로 Windows Claude Code나 GitHub Actions가 실행되지는 않음. **이 문서를 Windows Claude Code 실제 세션에 전달/실행해야 함**.

## 최신 기술 근거
- 전 회차 비용 제한 제거 결과: [GPT_ACTIONS_COST_GATE_REMOVAL_RESULT_r0001_20261123_KST.md](GPT_ACTIONS_COST_GATE_REMOVAL_RESULT_r0001_20261123_KST.md). `COWORK_GPT_API_ENABLED` 명시 ON, OPENAI API Secret, 모델 명시·보호 키 검증, 원격 claim을 유지.
- 추가 결함: GPT 판정 `preflight`가 Work의 **역사적인 별도 REQUEST**를 무조건 거부하여 v0.2.35 최초 판정을 차단하는 문제 발견. 수정 `479cc207ea85e07e953685f744a246b6ad214a79`: 완료된 REVIEW_RESULT/RECEIPT 및 보호 서명 검증 후 GPT 판정에서는 과거 요청 목록을 판정 자격의 차단 조건으로 쓰지 않음. **신규 리뷰 REQUEST에 대한 엄격한 동일-Work 중복 사전검사는 유지**. 실제 실행 직전 Work `ONE_CYCLE_CLAIM.json` 및 request `GPT_API_EXECUTION_CLAIM.json` CREATE_ONLY 중복 봉인은 유지.
- 신규 시험 `10148b6e5b05f3c0bff7bdf52e60942ab79737c3` 최초 Run `45195890869`은 테스트 mock `inspect` 속성 누락으로 1 ERROR; 수정 `38e63ceab97ed387317b7139144953fd5c7003ec` 최종 [Run 45196080268](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/45196080268): `offline-selftest=SUCCESS`, Python **31 tests OK**, `gpt-disposition=SKIPPED`, `telegram-smoke=SKIPPED`. 기존 실패 기록 보존, 재실행 금지.
- 기존 Claude 리뷰 `REQ-COWORK-V035-WATCHER-REVIEW-20261123` 완료. v0.2.35 package SHA256 `658a6f3da8bd018b96b64453892aec77d96868e19bc5788745c1591b1729a740`; **Claude 재리뷰하지 않음**. GPT 판정은 최초 1회만 허용.
- GitHub 원격 조회(2026-11-23): 이 Review의 `GPT_DISPOSITION.json`, `GPT_API_EXECUTION_CLAIM.json` 및 Work `ONE_CYCLE_CLAIM.json` **404 (미생성)**. 실행 직전에 재확인 필수.
- Telegram Bot Token/Chat ID 기존 GitHub secrets는 이전 2026-11-21 Smoke 전송 성공 결과로 보고됨. 실제 현재 상태는 호스트에서 이름 존재만 재조회. 기존 Windows Notifier 그대로 유지.

## 원샷 수행 — Windows Claude Code 책임 (추가 확인 질문 없이 사전 허용 범위 내에서 진행)
1. 최신 `main` fetch 및 `collab/CONTEXT_BRIEF.md`, 현재 두 Work의 CURRENT, 기존 운영 계약 및 실제 결과 확인. 본문보다 최신 원격 결과·사용자 지시가 있으면 우선. 정확히 1개의 GPT 판정 대상은 완료된 `REQ-COWORK-V035-WATCHER-REVIEW-20261123`. 이미 claim/판정 존재 시 **재실행 금지**.
2. 인증된 GitHub CLI `gh`로 `gh secret list -R wonhwipark/CoWork-Skill-Collab`에서 `OPENAI_API_KEY`, `COWORK_TELEGRAM_BOT_TOKEN`, `COWORK_TELEGRAM_CHAT_ID` **존재만** 확인. `gh variable list -R ...`로 `COWORK_GPT_MODEL`, `COWORK_APPROVER_PUBLIC_KEY_B64`, `COWORK_GPT_API_ENABLED`, `COWORK_GPT_TELEGRAM_NOTIFY_ENABLED` 유효성 확인. **키·토큰·모델 Secret 원문을 채팅/로그/문서에 출력 금지.** 사용 가능한 기존 프로젝트 키·지원 모델·신뢰 공개키가 없다면 각각 `BLOCKED_KEY`/`BLOCKED_MODEL`/`BLOCKED_TRUST`로 멈춤. 별도 승인 없이 신규 키/토큰 발급 금지.
3. API ON 전에 실제 패키지/서명/리뷰 입력을 **모델 0회·원격 쓰기 0회**로 사전검증. `collab/tools/gpt_disposition_actions.py`의 `preflight(ROOT, RID, repo_id='1451933830', public_key_b64=<Windows에서 검증된 보호 공개키>)` 직접 사용; 결과는 `PREFLIGHT=PASS` 및 SHA만 로깅하고 모델 입력·서명 비밀값 출력하지 않음. 해당 프리플라이트에는 `review_chain.inspect`, PIN/APPROVAL/READY 바인딩·서명·ZIP 크기/SHA/CRC/경로·입력·민감패턴 검증이 포함. 과거 Work HISTORY는 최종 수정 코드로 확인.
4. REQUEST 단위 GPT disposition/claim 2개와 Work claim 1개가 **모두 404**인지 원격 readback. 기존 `GPT_DISPOSITION.json` 또는 미해결/UNCERTAIN claim이 있으면 재실행하지 않고 `BLOCKED_ALREADY_CLAIMED` 기록. Code/Actions runner 31 PASS 상태를 재확인.
5. 준비 상태가 모두 유효하고 API 호출 1회 권한이 확인된 경우에만 기존 GitHub repo **variable** `COWORK_GPT_TELEGRAM_NOTIFY_ENABLED=true`를 설정(기존 Bot 재사용)하고 **마지막으로** `COWORK_GPT_API_ENABLED=true`를 설정; 두 값을 이름/true 여부만 readback. `COWORK_GPT_COST_POLICY_APPROVED`, `COWORK_GPT_PROJECT_SPEND_CAP_CONFIRMED`, USD3/월 상한·단가를 새 게이트로 요구하지 않음. 단, OpenAI 플랫폼 자체 결제 가능 여부를 보장하지 않음.
6. 새로운 Claude 독립 리뷰를 만들지 말고 **기존 완료된 리뷰의 최초 GPT 판정만** 승인된 `workflow_dispatch`로 1회 수행: `gh workflow run cowork-gpt-disposition.yml -R wonhwipark/CoWork-Skill-Collab --ref main -f request_id=REQ-COWORK-V035-WATCHER-REVIEW-20261123 -f telegram_smoke=false`. 실제 Run ID/actor/commit/Jobs를 조회해 새 실행과 다른 Runs를 구분. **새 유료 모델 호출은 1회까지**. 인증·선점·서명·원본검증 차단/호출 불확실이면 멈추고 재디스패치·재호출 금지.
7. 성공하면 `collab/reviews/REQ-COWORK-V035-WATCHER-REVIEW-20261123/GPT_DISPOSITION.json`, `.../GPT_API_EXECUTION_CLAIM.json`, `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/ONE_CYCLE_CLAIM.json`의 원격 바이트·바인딩·한 번 처리 여부를 확인. 비용은 API `usage` 사후 기록만 확인.
8. 같은 Run에서 판정 게시 후 Telegram `COWORK_GPT_TELEGRAM_NOTIFY_ENABLED` 단계가 1회 실행되고, `GPT_TELEGRAM_NOTIFICATION_CLAIM.json`/영수증·Run ID·발송 ACK가 확인되는지 검증. 기존 Windows Claude 리뷰 완료 알림과 구분. 모바일 실제 수신 확인이 없으면 `MOBILE_RECEIVE=NOT_VERIFIED`로 유지. Telegram 실패 또는 응답 불확실을 이유로 GPT 판정을 재실행 금지.
9. 실패/불확실 모델 호출·Secret/권한 오류나 자동화 루프 위험이 확인되면 새 모델 호출 없이 `COWORK_GPT_API_ENABLED=false`로 안전 복귀(단, 이미 claim이 있으면 유지/영수증·로그 확인). 알림은 전송 이력/중복 방지를 고려해 처리. 기존 Windows 운영 v0.2.29·설치 트리/DB/Task/Notifier/키 변경 금지.
10. 결과는 **기존** `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md`, `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/CURRENT.md` 최상단 요약 및 기존 결과/영수증 경로에 기록. GitHub `main`에 게시하고 SHA·원격 바이트 readback 확인. 개인키/토큰·원문 L1 코드·민감 데이터 공개 저장소에 게시 금지.

## 보고 형식
`HOST_ACK` / `SECRETS_PRESENT` / `MODEL_APPROVED` / `PREFLIGHT` / `PREEXISTING_CLAIMS` / `API_SWITCH` / `TELEGRAM_SWITCH` / `RUN_ID` / `GPT_DISPOSITION` / `USAGE` / `TELEGRAM_SENT` / `MOBILE_RECEIVE` / `LIVE_WATCHER_VERSION` / `POSTED_COMMIT` / `NEXT_ONE_ACTION`.
성공하지 않은 단계를 완료로 표시하지 않음. GitHub 문서 게시만으로 Windows 호스트 실행을 주장하지 않음.
