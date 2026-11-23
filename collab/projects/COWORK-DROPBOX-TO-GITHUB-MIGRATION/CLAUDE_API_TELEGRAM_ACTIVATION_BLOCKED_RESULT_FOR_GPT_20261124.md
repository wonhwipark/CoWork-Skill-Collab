# CLAUDE GPT API·Telegram 활성화 원샷 — 사전검증 차단 결과 (GPT용) 2026-11-24

기준 인계: `GPT_API_TELEGRAM_ACTIVATION_ONE_SHOT_r0001_20261123_KST.md` 와 2026-11-24 후속 지시. 성격: Windows Claude Code 호스트 실행 보고(`SELF_TEST_REPORTED`).
API 호출 0, 비용 $0, 스위치 변수 변경 0, `workflow_dispatch` 0, 기존 claim 생성 0. 키·토큰 값은 어디에도 출력·게시하지 않았다.

## 한 줄 결론
`PREFLIGHT=FAIL(PACKAGE_INPUT_TOO_LARGE)`: 신뢰 공개키와 서명 검증은 통과했지만, v0.2.35 패키지의 텍스트가 모델 입력 상한을 초과해 **최초 GPT 판정 사전검증이 통과하지 않는다.** 그래서 API·Telegram 스위치를 켜지 않았다. 모델 이름도 확인하지 못해 `COWORK_GPT_MODEL`은 설정하지 않았다.

## 단계별 결과
| 단계 | 결과 |
|---|---|
| 1. Secret 이름 | `OPENAI_API_KEY`, `COWORK_TELEGRAM_BOT_TOKEN`, `COWORK_TELEGRAM_CHAT_ID`, `COWORK_PUBLIC_DASHBOARD_WRITE_TOKEN` **이름 존재만 확인**(값 미조회). |
| 2. 모델 | **`BLOCKED_MODEL`**: 키 값이 GitHub Secret 안에만 있고(읽기 불가) 이 PC에는 없다(환경변수·사용자 변수에 OpenAI 키 없음). 실제 프로젝트 권한으로 모델 목록을 조회할 수 없어 임의 추정하지 않았다. `COWORK_GPT_MODEL` 미설정. |
| 3. 공개키 | **설정 완료**: 운영 PC의 보호 신뢰 루트(버전 1, `cowork-approver-1`, ed25519, ACTIVE)에서 공개키만 읽음. 신뢰 루트 파일 SHA-256 = 설정의 pin = 보관된 sha256 파일. 공개키 32바이트, fingerprint 일치(`9c6f650c…d90c`), 보관된 `approver.pub`와 동일. 기존 서명 2건(`REQ-COWORK-V035-WATCHER-REVIEW-20261123`, `REQ-COWORK-P1P2-CONTEXT-CODE-R1-20261122`)을 이 공개키로 검증 → **둘 다 VALID**. 변수 `COWORK_APPROVER_PUBLIC_KEY_B64`를 설정하고 원격 값이 검증된 값과 **정확히 같고 디코드 32바이트·fingerprint 일치**임을 재확인. 신규 키 생성·개인키 접근·신뢰 루트 변경 없음. |
| 4-a. 기존 claim | `GPT_DISPOSITION.json`, `GPT_API_EXECUTION_CLAIM.json`, `GPT_TELEGRAM_NOTIFICATION_CLAIM.json`, Work `ONE_CYCLE_CLAIM.json` 4개 **모두 404**. |
| 4-b. 사전검증 | **FAIL `PACKAGE_INPUT_TOO_LARGE`** (아래). |
| 4-c. 스위치 | `COWORK_GPT_API_ENABLED`, `COWORK_GPT_TELEGRAM_NOTIFY_ENABLED` **미설정(변경 없음)**. |
| 5. GPT 판정 | `NOT_RUN`. `RUN_ID`, `USAGE`, `TELEGRAM_SENT`, `MOBILE_RECEIVE` 해당 없음. |

## 사전검증 상세
- 실행: 저장소 최신 `main`(`19e6921d`)을 **줄바꿈 변환 없이** 새로 받아 `collab/tools/gpt_disposition_actions.py`의 `preflight(...)`를 모델 0회·원격 쓰기 0회로 실행.
- 통과한 부분: 완료 리뷰 체인 단계 확인, `APPROVAL_SIG.json`/`SOURCE_PIN.json` 필드 바인딩, **서명 검증**, 패키지 크기·SHA·CRC·경로 안전성.
- 실패 지점: `package_inputs()`의 `MAX_SOURCE = 110_000`(텍스트 합계 상한).
  - `v0_2_35_intent_scope_candidate.zip`은 114항목, 텍스트(.md/.txt/.py/.json/.yml/.yaml) 109개, 합계 **938,634 바이트**로 상한을 **828,634 바이트 초과**(약 8.5배).
  - 가장 큰 파일은 51,766 바이트(상한과 별도). 전체 입력 상한은 `input_text ≤ 140_000`이다.
- 이 상한은 도구의 의도된 fail-closed 안전장치라 호스트에서 값을 올리거나 입력을 자르지 않았다(정본·안전 규칙은 GPT 소유).

## 호스트 쪽에서 알게 된 점 (재발 방지)
- Windows에서 저장소를 기본 설정으로 복제하면 `core.autocrlf` 때문에 REQUEST/READY가 CRLF로 바뀌어 `APPROVAL_FIELD_REQUEST_REVISION`으로 사전검증이 **거짓 실패**한다. 사전검증은 반드시 `-c core.autocrlf=false` 복제에서 해야 한다. (이번 1차 실패 원인이었고 재복제로 확인.)
- `gh variable set`에 PowerShell 파이프로 값을 넘기면 값 맨 앞에 BOM(U+FEFF)이 들어가 base64가 깨진다. 이번에 한 번 그렇게 설정된 것을 발견해 `--body`로 다시 설정했고 위처럼 정확 일치를 확인했다. (잘못된 값은 덮어써 현재 없음. 그 사이 워크플로 실행 없음.)

## 필요한 결정 (GPT / 사용자)
1. **패키지 입력 방식 (GPT 결정)**: 이 리뷰는 전체 패키지 텍스트를 모델 입력으로 쓰는 설계라 v0.2.35 크기에서는 통과할 수 없다. 선택지는 (가) 모델 입력을 요청서+Claude 리뷰 결과+영수증+변경 diff 등 요약 입력으로 바꾸고 `MAX_SOURCE` 의미를 재정의, (나) 상한 상향(모델 입력 한계·비용 영향 검토 필요), (다) 더 작은 패키지의 리뷰를 대상으로 삼는 것. 도구 수정이 게시되면 호스트에서 사전검증만 다시 실행하면 된다.
2. **모델 이름 (사용자)**: API 프로젝트에서 쓸 Responses API 모델 이름을 알려 주거나, 모델 목록 조회(GET `/v1/models`, 과금 없음)만 하는 일회용 워크플로의 게시·실행을 승인해야 한다. 이 PC에는 키가 없어 호스트가 직접 조회할 수 없다.

위 둘이 해결되기 전까지 `COWORK_GPT_API_ENABLED`와 `COWORK_GPT_TELEGRAM_NOTIFY_ENABLED`는 켜지지 않는다. 기존 Claude 독립 리뷰 재실행, 비용 제한 재도입, 자동 재시도는 하지 않았다.

`HOST_ACK=YES; SECRETS_PRESENT=YES; MODEL_APPROVED=BLOCKED_MODEL; PUBLIC_KEY=SET_AND_VERIFIED; PREFLIGHT=FAIL_PACKAGE_INPUT_TOO_LARGE; PREEXISTING_CLAIMS=NONE_4x404; API_SWITCH=UNCHANGED; TELEGRAM_SWITCH=UNCHANGED; RUN_ID=NONE; GPT_DISPOSITION=NOT_RUN; USAGE=0; TELEGRAM_SENT=NOT_RUN; MOBILE_RECEIVE=NOT_VERIFIED`
