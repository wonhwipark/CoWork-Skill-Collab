# CoWork 리뷰 1사이클 → GPT 판정 → Telegram 알림 → 모바일 GPT 조회
- 작성: 2026-11-21 KST
- 기존 Work: `COWORK-DROPBOX-TO-GITHUB-MIGRATION`, 연계 Issue #2
- 정본: GitHub PUBLIC `wonhwipark/CoWork-Skill-Collab`, branch `main`
- 사용자 최신 지시: Runner에서 GPT 판정이 GitHub에 저장·원격 확인된 **이후에만** Telegram Bot으로 판정 결과를 모바일에 알림. Gmail은 대안으로 보류. 기존 Claude 리뷰 완료 Telegram 통지는 유지하되 GPT 판정 알림과 구분.

## 전체 실행 순서 및 주체
| 순서 | 주체 | 실행 및 공식 결과 | 차단/비용 경계 |
|---|---|---|---|
| 1 | GPT | 기존 Work·패키지·승인 확인 후 정식 REQUEST/SOURCE_PIN 게시 | 게시 자체가 유료 리뷰 승인은 아님 |
| 2 | Windows watcher | 실제 REQUEST/READY·승인/서명·SHA·중복·기존 Claude 예산 확인 | 검증 실패 시 Claude 호출 0 |
| 3 | Windows Claude Code | **독립 리뷰 최대 1회**, 원격 REVIEW_RESULT/RECEIPT 게시 | 기존 Windows notifier의 Claude 리뷰 완료 Telegram은 별개 |
| 4 | GitHub Actions Runner | 결과 파일 `push` 또는 승인된 `workflow_dispatch`로 시작, 원본·승인 서명·ZIP·비용 정책 검증 | watcher 게시 토큰이 Actions 이벤트를 실제 발생시키는지는 G0 미검증 |
| 5 | GitHub Actions → GPT API | Work 단위 CREATE_ONLY → 요청 단위 CREATE_ONLY → **GPT 판정 1회** | 별도 API 키·비용 승인·지출 상한 확인. 현재 **OFF** |
| 6 | GitHub Actions Runner | `collab/reviews/<request_id>/GPT_DISPOSITION.json` CREATE_ONLY 게시·원격 바이트 readback | 판정 게시 불확실 시 자동 재호출 0 |
| 7 | 동일 GitHub Actions job → Telegram Bot | 이번 Run에서 게시 확인된 ID만 읽고 GPT claim·Work claim·run_id 재검증 → 알림 선점 CREATE_ONLY → `sendMessage` 1회 → 응답 영수증 | 기존 Windows 알림과 별개, 새로운 봇 발송 **OFF**; 실패·응답 불확실 시 자동 재발송 0 |
| 8 | 모바일 사용자 / ChatGPT | Telegram 앱 푸시 알림 탭해 GitHub 판정 링크 확인. 또는 모바일 ChatGPT 어느 대화창에서든 “CoWork 최신 판정 확인해줘” 요청 | ChatGPT 대화 자동 생성/자동 삽입 기능은 아님 |

**엄격한 1사이클**: GPT 리뷰 요청 → Windows Claude 리뷰 1회 → GPT 독립 판정 1회 → 종료. Telegram은 결과 전달만 하며 재리뷰·재판정·보완요청을 자동 시작하지 않음.

## 구현된 변경
- [알림 발송기](../../tools/gpt_disposition_telegram.py): 현재 GitHub Actions Run의 판정·claim 일치/승인 검증된 판정만 발송. 민감 원문·모델 생성 요약은 보내지 않고 Work ID·Request ID·판정 등급·공식 GitHub 링크만 포함. GitHub 알림 시도 선점/영수증으로 중복 발송 보호.
- [판정 실행기](../../tools/gpt_disposition_actions.py): `GPT_DISPOSITION.json` 원격 readback 성공 뒤에만 Runner `GITHUB_OUTPUT`으로 `posted_request_id` 노출. 새 자동 모델 호출·재시도 기능 없음.
- [GitHub workflow](../../../.github/workflows/cowork-gpt-disposition.yml): 같은 GPT job의 후속 step에서만 `posted_request_id`를 받아 알림 처리. `vars.COWORK_GPT_TELEGRAM_NOTIFY_ENABLED == 'true'`일 때만 동작. 기본 OFF.
- [회귀시험](../../tools/tests/test_gpt_disposition_telegram.py): OFF·자격정보 누락·잘못된 ID·선점 우선·중복 영수증·run_id 불일치 등 7건 추가. 로컬 독립 후보 실행에서 **7 PASS**. 실제 게시된 전체 코드의 Actions Runner 통합시험 **NOT_VERIFIED**.
- 신규 Telegram Bot 비밀값 **저장소 게시 0**. Windows watcher/DB/Notifer LIVE 설정 변경 0. 유료 모델 호출 0. 기존 Windows 리뷰 완료 알림을 삭제/재설정하지 않음.

## 사용자에게 보일 Telegram 메시지 예시
> ✅ CoWork GPT 판정 완료
>
> Work: `<work-id>`
>
> Request: `<request-id>`
>
> 판정: 수정 수용
>
> 결과: `https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/reviews/<request-id>/GPT_DISPOSITION.json`
>
> 모바일 ChatGPT 어느 창에서든 “CoWork 최신 판정 확인해줘”라고 질문하세요.

## 운영 설정 · 승인 전제
- GitHub Actions Secrets: `COWORK_TELEGRAM_BOT_TOKEN`, `COWORK_TELEGRAM_CHAT_ID` (숫자 Chat ID). 채팅이나 GitHub 파일에 평문 게시 금지. **현재 존재/설치/실제 송신 미확인**.
- GitHub Actions Variable: `COWORK_GPT_TELEGRAM_NOTIFY_ENABLED=true`는 봇 수신 검증과 운영 승인 후 최종 활성화. 현재 기본 OFF.
- **GPT API는 별도**: `OPENAI_API_KEY`, 승인된 모델·건당 요금·프로젝트 지출 상한·세 가지 게이트 `COWORK_GPT_API_ENABLED`, `COWORK_GPT_COST_POLICY_APPROVED`, `COWORK_GPT_PROJECT_SPEND_CAP_CONFIRMED` 모두 충족 후에만 판정 Job 가동. 기존 Claude 리뷰 USD3 한도와 독립.
- 결과 게시 성공 후 Telegram만 실패하면 **리뷰/판정을 재실행하지 않음**. GitHub 결과는 보존; claim·로그·수신 여부를 확인해 수동 후속 처리.
- GitHub Actions 자체 트리거·Runner 22건(기존 15+신규 7) 전체 PASS, 실제 Telegram 푸시 수신, Windows Claude 호출 전 1사이클 게이트는 아직 NOT_VERIFIED/NOT_APPLIED. 문서나 코드 게시만으로 LIVE 완료로 승격하지 않음.
- **중요**: Windows 게시가 `GITHUB_TOKEN`으로 이뤄질 경우 그 `push`는 일반적으로 후속 GitHub Actions를 자동 시작시키지 않음. 원격 푸시 인증 주체와 workflow 실제 이벤트를 G0에서 확인할 것.

## 다음 한 동작
Actions `offline-selftest`의 실제 22건 결과·Windows 리뷰 게시 `push` 인증 주체를 먼저 읽기 전용 검증하고, 봇 자격정보는 해당 GitHub Actions secret에 별도 설치·비용 0 테스트를 확인. 이후 승인된 GPT API 설정으로 새 리뷰 1회 E2E에서 판정 게시→Telegram 수신을 확인. 실운영 확대·신규 유료 요청은 승인 범위 확인 전 금지.

## 근거
- [이관 Work CURRENT](CURRENT.md)
- [1사이클 게이트 구현](GPT_ONE_CYCLE_GUARD_IMPLEMENTATION_r0001_20261121_KST.md)
- [Actions GPT 판정 실행기 구현](GPT_ACTIONS_DISPOSITION_IMPLEMENTATION_r0001_20261121_KST.md)
- [Issue #2](https://github.com/wonhwipark/CoWork-Skill-Collab/issues/2)
