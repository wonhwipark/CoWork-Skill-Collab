# Windows Claude Code 실행 인계 — v0.2.35 기존 독립 리뷰 최초 GPT 판정 + Telegram (2026-11-24 KST)

## 범위·권한
- 저장소: **GitHub PUBLIC** `wonhwipark/CoWork-Skill-Collab`, branch `main`. CoWork 외의 실제 Windows 운영 설정·watcher 설치·키/신뢰 루트 변경 금지.
- 기존 Work 재개: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md`와 연계 `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/CURRENT.md`. 절차 기본은 `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_API_TELEGRAM_ACTIVATION_ONE_SHOT_r0001_20261123_KST.md`.
- **사용자 최신 승인:** 기존 완료 Claude 독립 리뷰 1건의 GPT 최초 판정 및 Telegram E2E를 유효한 사전 검증 후 1회 실행. 사용자가 이미 승인한 동일 작업으로, 기존 승인된 비용 정책을 되묻지 않음. 새 Claude 독립 리뷰/새 REQUEST·READY 발행·키/토큰 생성/교체·보호 signer 변경·Windows watcher LIVE 적용은 범위 밖.
- **고정 대상:** `REQ-COWORK-V035-WATCHER-REVIEW-20261123` (`COWORK-AUTO-APPROVAL-20261115-001`, package SHA-256 `658a6f3da8bd018b96b64453892aec77d96868e19bc5788745c1591b1729a740`).

## GPT 직접 검증된 새 근거 (재시험/재호출하지 않고 재사용)
- 사용자 승인 `GET /v1/models` 1회: [Run 45212536082](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/45212536082) SUCCESS; 기존 `OPENAI_API_KEY` GitHub Secret으로 인증된 메타데이터 목록에서 `gpt-6.2-sol` 실제 확인. OpenAI 공식 문서 `https://developers.openai.com/api/docs/models/gpt-6.2-sol`: Responses API와 Structured Outputs 지원. **모델 생성 권한·실제 Schema 통과는 아직 미확인**; 같은 요청을 별도 Smoke 모델 호출로 중복 검증하지 말 것.
- 대용량 ZIP 근거 입력 보완: [Run 45208515737](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/45208515737) offline-selftest **35 PASS, 0 FAIL**.
- **신규 서명 포함 full preflight PASS**: [Run 45215858291](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/45215858291) (job signed-preflight-once). `PREFLIGHT=PASS`, `SIGNATURE_AND_ZIP_CHECK=PASS`, `MODEL_INPUT_BYTES=42915`, `MODEL_INPUT_SHA256=5bd39fa0a8300d597c1f7a794286b21d92bb54423937135caa0cc8b850dde294`, `MODEL_CALLS=0`, `CLAIM_WRITES=0`. 입력 제한 `140000` bytes 미만. 이 결과는 **GitHub Linux Runner** 검증이며 Windows host 자체 PASS의 근거로 대체하지 않음.
- GPT가 2026-11-24 KST에 원격 `GPT_DISPOSITION.json`, `GPT_API_EXECUTION_CLAIM.json`, `GPT_TELEGRAM_NOTIFICATION_CLAIM.json`, Work `ONE_CYCLE_CLAIM.json` **4건 404** 확인. 실행 직전 다시 확인할 것; 과거 404만 믿고 재실행하지 말 것.

## Windows Claude Code 단일 실행 지시 (실제 PC 권한 보유 세션에서 수행)
1. `collab/CONTEXT_BRIEF.md`, 본 인계서 및 두 Work `CURRENT.md`를 최신 `main`에서 조회. 이미 최신이며 유효한 기존 근거를 재사용하고, 다른 Work나 신규 리뷰를 만들지 않는다. Git checkout은 `core.autocrlf=false`로 보존해 REQUEST/READY SHA 변조를 방지. 입력 zip 원본 바이트·`SOURCE_PIN`/APPROVAL/READY를 수정하지 않는다.
2. `gh secret list -R wonhwipark/CoWork-Skill-Collab` 및 `gh variable list -R wonhwipark/CoWork-Skill-Collab`로 이름만 재확인. 공개키 변수 `COWORK_APPROVER_PUBLIC_KEY_B64`는 기존 Windows 보호 신뢰 루트의 `cowork-approver-1`에서 이미 검증되어 설정된 값만 허용. `OPENAI_API_KEY`/Telegram Secret 값은 열람·로그/파일 게시 금지.
3. **Windows-local 무과금 preflight**: 현재 최신 소스 `collab/tools/gpt_disposition_actions.py`의 `preflight(ROOT, 'REQ-COWORK-V035-WATCHER-REVIEW-20261123', '1451933830', public_key_b64=<기존 검증 공개키>)`를 실제 Windows checkout에서 호출. `cryptography` 설치는 기존 의존성·승인 범위에 한정. 반환된 `input_sha256`, `len(input.encode('utf-8'))`, `work_id`만 비교/기록하고 입력 원문·키를 출력하지 말 것. 기대값: 입력 SHA `5bd39fa0a8300d597c1f7a794286b21d92bb54423937135caa0cc8b850dde294` / 크기 42915. 불일치/오류는 `HOST_PREFLIGHT=FAIL`로 안전 중단, 원인보고. 크기 제한 증설·입력 임의 절단 금지.
4. 동일 리뷰/Work의 위 **4개 claim·결과 파일이 모두 여전히 원격 404**인지 확인. 이미 claim/불확실 실행/판정 게시가 존재하면 **재디스패치 금지**, 해당 실행 영수증·기록만 추적. GitHub 현재 Runner git HEAD와 이번 검증 코드 sha가 일치하는지 확인.
5. 3·4 PASS 후 모델 변수 `COWORK_GPT_MODEL=gpt-6.2-sol`를 실제 호스트의 GitHub CLI로 설정. `gh variable set COWORK_GPT_MODEL --repo wonhwipark/CoWork-Skill-Collab --body gpt-6.2-sol` 사용 (PowerShell 파이프 입력 금지: BOM 위험). `gh variable get ...` 정확한 readback 확인. 목록 GET 및 공식 문서 확인만으로 결제/Schema E2E PASS를 주장하지 않는다.
6. 원래 원샷 인계의 안전 조건을 유지해 기존 `COWORK_TELEGRAM_BOT_TOKEN`, `COWORK_TELEGRAM_CHAT_ID` Secret 이름/설정 및 `COWORK_APPROVER_PUBLIC_KEY_B64` 유효성을 확인한 뒤, 승인 범위에서 `COWORK_GPT_TELEGRAM_NOTIFY_ENABLED=true`를 먼저, `COWORK_GPT_API_ENABLED=true`를 **마지막**으로 `gh variable set ... --body true`로 설정·readback. 중복 호출 위험이나 기존 claim이 있으면 스위치를 켜지 않는다.
7. **정확히 한 번만** `gh workflow run cowork-gpt-disposition.yml -R wonhwipark/CoWork-Skill-Collab --ref main -f request_id=REQ-COWORK-V035-WATCHER-REVIEW-20261123 -f telegram_smoke=false`. 기존 v0.2.35 완료 리뷰의 최초 GPT disposition만 호출. 새로운 리뷰·재리뷰·모델 smoke·임의 재호출 금지. HTTP 에러/응답 불확실/실행 불확실 시 재디스패치하지 않고 기존 Run·claim 조사. 실제 모델 output schema 오류가 나더라도 같은 Work 재호출 금지.
8. 완료 시 `GPT_DISPOSITION.json`, `GPT_API_EXECUTION_CLAIM.json`, Work `ONE_CYCLE_CLAIM.json`의 실제 bytes/binding/processing key 및 모델 usage·실제 Run ID·실행 횟수를 검증. GPT 결과 readback 후에만 해당 Run의 Telegram 결과 claim·영수증·발송 ACK 확인. 모델 호출 성공/실패와 알림 성공/실패를 별개 판정. 모바일 수신 확인 없으면 `MOBILE_RECEIVE=NOT_VERIFIED`.
9. 실패·불확실 호출/루프 위험 시 `COWORK_GPT_API_ENABLED=false` 안전 복귀(변수 쓰기 권한이 실제 있을 때만) 후 상태 재조회, 기존 claim 보존, 모델/GPT/Telegram **재실행 금지**. Windows watcher v0.2.29(마지막 호스트 보고), DB/WAL/SHM, 작업 스케줄러, notifier, 키·LIVE provider 등 변경 금지.
10. 결과 MD 및 두 Work `CURRENT.md` 최상단 요약을 PUBLIC main에 게시. 원격 readback/실제 commit 및 SHA-256 검증. 정책·원본·키·제한 L1 정보 공개 금지. 결과 형식은 `HOST_ACK / MODEL_VARIABLE / HOST_PREFLIGHT / CLAIMS_PRECHECK / API_SWITCH / TELEGRAM_SWITCH / RUN_ID / GPT_DISPOSITION / USAGE / TELEGRAM_ACK / MOBILE_RECEIVE / LIVE_WATCHER / POSTED_COMMIT / NEXT_ONE_ACTION`. PASS/FAIL/SKIP/NOT_RUN 분리.

## 실행 인계의 의미
이 파일은 Windows Claude Code의 **실제 사용자 실행 세션용 인계**. GitHub 문서 게시 자체로 Windows 코드·Secrets 변수 변경이나 GitHub workflow_dispatch를 자동 실행하지 않음. GPT GitHub 연결에서 Actions variable 쓰기·workflow_dispatch는 지원되지 않아 이 권한은 Windows Claude Code 또는 승인된 운영 주체가 필요. 유료 호출 및 호스트 실행은 위 실검증 게이트 후 기존 승인 범위에서만 허용.

## 이 실행의 다음 한 행동
Windows Claude Code 실제 세션이 이 인계서를 수신·Windows 로컬 preflight PASS를 확인한 다음, 안전 게이트를 유지한 단 한 번의 GPT disposition + Telegram 알림 결과를 같은 Work에 회수·게시.
