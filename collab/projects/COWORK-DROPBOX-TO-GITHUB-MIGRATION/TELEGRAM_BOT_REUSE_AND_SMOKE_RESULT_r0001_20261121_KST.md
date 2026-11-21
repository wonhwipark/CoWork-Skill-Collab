# 기존 Telegram Bot 재사용 · GitHub Actions 연결 · 무료 Smoke 결과

- 작성: Windows Claude Code, 2026-11-21 KST. Work: `COWORK-DROPBOX-TO-GITHUB-MIGRATION`. 정본: PUBLIC `wonhwipark/CoWork-Skill-Collab`, `main`. 기준 commit `1dcb576d333e`(기존 봇 재사용 결정).
- **비밀값(Bot Token, Chat ID)은 이 문서·로그·commit 어디에도 없다.** 값은 Windows의 보호된 로컬 파일에서 메모리로만 읽어 `gh`의 표준입력으로 등록했고 평문 임시 파일은 만들지 않았다.

## 1. 현재 상태

```
BOT_REUSE=PASS (새 Bot 생성 0, 토큰 재발급 0, 기존 Windows 알림 변경 0)
G0_WINDOWS_NOTIFIER=PASS
GITHUB_SECRETS=PASS (COWORK_TELEGRAM_BOT_TOKEN, COWORK_TELEGRAM_CHAT_ID 등록, 값 비노출)
SMOKE_TEST=PASS (Run 44910683694, attempt 1)
GPT_DISPOSITION_JOB=SKIP (예상대로)
TELEGRAM_SEND_ACK=PASS (SEND_ACKNOWLEDGED, telegram_message_id 59)
CLAIM_RECEIPT_READBACK=PASS
SMOKE_VARIABLE_RESET=PASS (COWORK_TELEGRAM_SMOKE_ENABLED=false)
MOBILE_RECEIVE=PENDING_USER_CONFIRMATION
WINDOWS_NOTIFIER_KEPT=PASS (Task Running, 설정·자격정보 불변)
PAID_CALLS=0 (Claude 리뷰 0, GPT API 0), GPT_API=OFF, GPT_TELEGRAM_NOTIFY=OFF(미설정)
```

## 2. 기존 Bot 재사용 (G0)

- **발송 모듈:** Windows의 알림 모듈 `notify_reviews.py`. 감시기 DB의 감사 로그를 읽기 전용으로 추적하다가 리뷰 완료·실패·UNCERTAIN·업로드 실패·충돌·인증 필요·거부 이벤트에서 Telegram `sendMessage`로 보낸다. 작업 `SKILL-COLLAB-Notifier`가 로그인 시 상시 실행 중.
- **자격정보 저장:** 알림 모듈 전용 로컬 폴더의 JSON 파일(키 `bot_token`, `chat_id`). 파일 ACL은 운영자 계정만 접근. 평문이지만 ACL로 보호된다(DPAPI는 아님).
- **같은 봇인지·유효한지:** 형식이 Actions의 검증 정규식과 일치. Telegram `getMe`가 `ok=true, is_bot=true`. 수신 대상은 개인 채팅 형태의 숫자 ID. 이 확인에서 메시지는 보내지 않았다.
- **Actions에서 같은 봇 사용 가능:** 가능(같은 HTTPS API, 웹훅 충돌 없음). 알림 모듈은 `sendMessage`만 쓴다.
- **중복 가능성:** 낮음. Windows 알림은 감시기 감사 이벤트(Claude 리뷰)가 발생할 때만, Actions 알림은 GPT 판정이 원격에 게시·재확인된 뒤에만(별도 변수가 켜졌을 때) 보낸다. 이벤트·문구·발송 주체가 다르고, 이번 시험 동안 Windows 쪽 알림 진행 표식에는 발송 흔적이 없었다.

## 3. GitHub Secrets 등록 (값 제외)

- 권한 확인: 저장소 admin, `gh` 토큰 범위 `repo`·`workflow`. 이 작업 지시에 따른 등록이다.
- 충돌 확인: 기존 시크릿은 `COWORK_PUBLIC_DASHBOARD_WRITE_TOKEN` 하나뿐이고 같은 이름 없음. 이 이름을 쓰는 워크플로는 `cowork-gpt-disposition.yml` 하나뿐. 덮어쓰기 없음.
- 등록: `COWORK_TELEGRAM_BOT_TOKEN`(2026-11-21T13:47:57Z), `COWORK_TELEGRAM_CHAT_ID`(2026-11-21T13:47:58Z). 목록에서는 이름과 시각만 보인다.

## 4. Smoke Test

- Run: https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/44910683694 (workflow_dispatch, `telegram_smoke=true`, `request_id` 비움, attempt 1, 실행자 소유자 계정).
- 작업: `offline-selftest` success(unittest 29건 실행), `telegram-smoke` success, `gpt-disposition` **skipped**.
- 로그: `PASS: isolated model-free Telegram smoke acknowledged, run=44910683694`. 토큰 형태 문자열 0건.
- 원격 영수증: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/telegram-smoke/RUN-44910683694-CLAIM.json`(`ONE_SEND_RESERVED_NO_AUTO_RETRY`), `RUN-44910683694-RECEIPT.json`(`SEND_ACKNOWLEDGED`, `telegram_message_id` 59).
- 변수: 시험 전 없음 → 시험 동안만 `COWORK_TELEGRAM_SMOKE_ENABLED=true` → 종료 후 `false`로 복귀 확인. 재실행·재발송 없음.

## 5. 모바일 수신

`PENDING_USER_CONFIRMATION`. Telegram API는 발송 수락(ACK)까지만 알려 주고 폰 도착은 알 수 없다. 사용자가 "CoWork Telegram 연결 시험" 고정 메시지 1건이 도착했는지 확인해야 한다.

## 6. 미검증 · 차단 · 필요 승인

- **실제 GPT 판정 후 Telegram 알림 E2E:** NOT_RUN. `COWORK_GPT_API_ENABLED`·비용 승인·지출 상한·`COWORK_GPT_TELEGRAM_NOTIFY_ENABLED`는 켜지 않았고 별도 승인과 검증이 필요하다.
- **Windows 리뷰 게시 `push`가 Actions를 실제로 시작시키는지:** NOT_VERIFIED(게시 인증 주체에 따라 달라짐).
- **[보안 주의] 저장소가 PUBLIC이다.** 이전 세션에서 이 저장소에 올린 운영 산출물(컷오버·사전검증 결과 JSON, 스크립트)이 인증 없이 읽힌다(확인: 비인증 요청 HTTP 200). 거기에 호스트 이름, 운영자 계정 이름, 로컬 경로, 위임 범위가 들어 있다. 비밀키나 토큰은 없다. 되돌리려면 저장소를 다시 비공개로 하거나 해당 파일을 정리해야 하며(이력에는 남음) 사용자 판단이 필요하다. 이 문서의 시험은 이 점을 바꾸지 않았다.
- 이번 시험 메시지 외 추가 발송 없음. 실패하거나 불확실하면 같은 Run 재실행 금지.

## 7. 다음 한 동작

사용자가 폰에서 시험 메시지 도착 여부를 확인. 도착 확인 후, GPT API 비용 승인과 게이트 변수를 별도로 승인하면 판정 후 알림 E2E를 한 번 시험한다.
