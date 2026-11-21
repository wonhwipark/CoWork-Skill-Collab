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

---

## 2026-11-21 KST 후속 G0 — Runner 오프라인 시험·봇 연결 진단

- **무과금 Actions 시험 보완 게시:** `.github/workflows/cowork-gpt-disposition.yml` 의 `offline-selftest`에 GPT 실행기와 Telegram 발송기 두 Python 파일의 `py_compile`을 추가. 기존 `unittest discover -s collab/tools/tests -v`는 GPT 15건 + Telegram 7건, 총 22건을 발견하도록 연결. source blob `0635ac8fdd53c2ee2401ec9f6196d62536b64438`, commit `72ae8c50d94acd66460ac04673d7038d6bbdd741`.
- **직접 확인:** main 소스 파일 5개 원격 재조회 성공, 단위시험 정의 15+7=22 확인, 실행 순서 및 OFF/claim/run_id/결과 게시 후 발송 등 소스 정적 게이트 11/11 확인. 이 **정적 검사**를 Python 시험 22 PASS나 GitHub Actions Runner PASS로 바꿔 보고하지 않음.
- **Actions 실행 기록:** 연결된 GitHub 상태 조회는 `statuses=[]`, commit workflow 조회는 PR-triggered run으로 제한되어 `workflow_runs=[]`; 이 응답들은 `push` Runner 성공/실패의 증거가 아님. 해당 workflow runs 조회가 현재 지원되지 않아 `ACTIONS_RUN=NOT_VERIFIED`, `22_TESTS_RUN=NOT_VERIFIED`로 보존.
- **Telegram 연결:** 이 세션에서 GitHub Actions Secrets/Variables 존재 여부 및 실제 Windows Bot 자격정보 조회 권한이 제공되지 않음. `COWORK_TELEGRAM_BOT_TOKEN`, `COWORK_TELEGRAM_CHAT_ID`의 존재, 봇의 해당 Chat 접근, 수신자 모바일 알림 설정은 **NOT_VERIFIED**. 토큰/Chat ID를 문서·응답에 붙이지 않으며 임의 새 봇을 만들지 않음.
- **운영 미변경:** GPT API OFF, Telegram Runner 전송 기본 OFF, 새로운 유료 호출·Telegram 실제 `sendMessage`·Windows watcher/Notifier·기존 리뷰/READY 재실행 = 0.
- **NEXT_ONE_ACTION:** GitHub Actions [해당 workflow 실행 기록](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/workflows/cowork-gpt-disposition.yml)에서 최신 `offline-selftest`의 실행 ID 및 성공/실패를 확인하고, 기존 Bot 자격정보를 안전한 Windows 실행 환경에서 조회하여 GitHub Actions secret의 **존재만** 검증. 미설정이면 관리자 권한과 범위 확인 후 secret을 별도 등록하고 발송은 계속 OFF. 이후 실제 Telegram 시험은 승인된 단일 비유료 발송으로 분리하여 수행.


---

## 2026-11-21 KST 추가: 모델 0회, 수동 1회 Telegram 연결 Smoke 게이트

- **목적**: GPT API가 계속 OFF여도 기존 Telegram Bot → 모바일 푸시 수신을 **리뷰/판정과 분리**해 수동으로 시험할 수 있도록 준비. 자동 리뷰·GPT 호출·가짜 REVIEW_RESULT/READY/지출 없음.
- 새 코드: `collab/tools/telegram_smoke.py` (blob `bd7988790d784e59958f7e8b5512f1d5c11085a3`), `collab/tools/tests/test_telegram_smoke.py` (blob `35b9ebecb49b0f0f3ac812c571bffc735bae22ab`), workflow `cowork-gpt-disposition.yml` (blob `ab463774e4e1e89f77f501d6019166760923936b`).
- **분리 보호**: 수동 `workflow_dispatch`에서 `telegram_smoke=true`, `COWORK_TELEGRAM_SMOKE_ENABLED=true`, 실행자 `wonhwipark`, `main`, 최초 `run_attempt=1`일 때만 수행. GPT job은 `telegram_smoke=true`에서 **명시적으로 제외**. 신뢰 검증·모델 호출·리뷰 경로에 접근하지 않음.
- 발송 전 `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/telegram-smoke/RUN-<id>-CLAIM.json` CREATE_ONLY·원격 readback, 고정 문자열 메시지 1회, ACK 후 `RUN-<id>-RECEIPT.json` 기록. 실패·응답 불확실 시 자동 재발송/재실행 금지.
- **실제 로컬 시험:** GitHub 원격 4개 Python 파일과 로컬 바이트의 Git blob hash가 일치하는 것을 확인하고, Python 문법 검사 및 Telegram 판정 알림 7건 + 수동 연결 7건 = **14/14 PASS** (모두 모의 API, 유료 호출/실제 Telegram 발송 0). 기존 GPT 단위시험 15건은 본 세션에서 실행 못 함. 전체 소스 기준 unittest 함수 15+7+7 = **29개**. Actions Runner 실제 29건/모바일 실제 수신 = **NOT_VERIFIED**.
- 로컬 파일 SHA-256: `gpt_disposition_telegram.py` `404b4c54f69a3dcfd579e38af6a2d617c54941ec2727f0d02ede95e666323f16`; `test_gpt_disposition_telegram.py` `615046440714680a867020f471cffd036ea9cf06f158a42a8ce7ffc0f1eced21`; `telegram_smoke.py` `d9c18e70787a1fb261d85e0dc829aa1a93bb9493803d3e2dc5071d72b8dcaba9`; `test_telegram_smoke.py` `615c834f9b647292741c67b781f05d827730253f0f904a0e7af0e8034ca25e61`.
- **운영 미실시:** 사용자 계정의 Actions Secrets/Variables 설치 여부를 현재 도구가 조회 불가. 기존 Bot token/Chat ID를 반환·복사하지 않았으며, 새 발송 경로와 GPT API 모두 OFF 유지. 수동 workflow_dispatch 버튼 실행은 실제 수행하지 않음.

### 연결 시험 실행 순서 (비밀값 비노출)
1. `Settings → Secrets and variables → Actions`에서 **Repository secrets** `COWORK_TELEGRAM_BOT_TOKEN`, `COWORK_TELEGRAM_CHAT_ID`의 **존재 여부** 확인. 없으면 권한 있는 관리자가 기존 Bot 설정에서 안전하게 추출해 직접 등록(값을 채팅/저장소에 게시 금지). 봇 대화에서 `/start` 확인, 모바일 Telegram 알림 허용.
2. **Repository variables** `COWORK_TELEGRAM_SMOKE_ENABLED=true`를 **수동 시험에 한해** 활성화. 이것은 GPT API `COWORK_GPT_API_ENABLED`와 무관.
3. [Actions workflow](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/workflows/cowork-gpt-disposition.yml) → Run workflow → branch `main` → `telegram_smoke=true`, `request_id` 비움 → 1회 실행. `offline-selftest`와 `telegram-smoke`가 별도 job으로 실행되며 `gpt-disposition` job은 SKIP이어야 함.
4. 사용자 모바일 Telegram에 `CoWork Telegram 연결 시험` 고정 메시지가 1회 도착하는지 확인. GitHub Actions run log + `telegram-smoke/RUN-<id>-CLAIM.json`·RECEIPT readback으로 판정. 실패/불확실 실행은 같은 Run 재실행 금지.
5. 연결 확인 후 `COWORK_TELEGRAM_SMOKE_ENABLED=false` 복귀. 실제 GPT 판정 후 자동 Telegram은 **별도** `COWORK_GPT_TELEGRAM_NOTIFY_ENABLED` 운영 게이트와 GPT API 비용 승인 후에만 활성화.

