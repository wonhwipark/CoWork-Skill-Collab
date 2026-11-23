# GPT API 모델 목록 읽기 전용 조회 — 2026-11-24 KST

## 결과
- **MODEL_DISCOVERY=PASS_HOSTED_ACTIONS_VERIFIED.** 사용자 승인에 따라 기존 GitHub Repository Secret `OPENAI_API_KEY`를 GitHub Actions에서만 사용해 `GET https://api.openai.com/v1/models` 1회 실행. `POST /v1/responses` 및 기타 모델 생성 요청 **0회**, 신규 키 발급 0.
- 첫 Run [45212208881](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/45212208881): 새 파일 생성 이벤트의 추가 경로 조건 불일치로 **SKIPPED**, 모델 호출·GET 0. job 조건을 정확한 후속 commit message + `run_attempt==1`로 제한해 재게시한 후 두 번째 Run [45212536082](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/45212536082) **SUCCESS**, `list-api-models-once` job PASS, `MODEL_DISCOVERY=SUCCESS_METADATA_ONLY`, `MODEL_CANDIDATE_COUNT=86`.
- 86개는 `gpt-` 또는 `o[0-9]` 접두어를 갖는 모델 ID 개수로, 텍스트 전용 모델 86개라는 뜻이 아님(영상·음성·이미지 계열 일부 포함). 전체 모델 목록을 게시하거나 Secret 값을 출력하지 않고 정규식으로 검증된 ID만 워크플로 로그에 출력. 공개 상태인 저장소의 실행 로그에도 비밀값 출력을 금지함.
- 실제 확인된 후보: `gpt-6.2-sol`, `gpt-6.2-astra`, `gpt-6.1-sol`, `gpt-6-luna`. **권장 후보 `gpt-6.2-sol`** (API 모델 목록에서 실제 반환됨; 공식 모델 설명에서 Responses API·Structured Outputs 지원 명시). 단, 모델 목록 GET은 모델 호출 권한·개별 JSON Schema 성공을 실사용 검증하지 않음.
- 승인 범위의 READ_ONLY GET만 실행. 모델을 자동 선택해 원격 변수 `COWORK_GPT_MODEL`에 쓰지 않았고, `COWORK_GPT_API_ENABLED` 및 `COWORK_GPT_TELEGRAM_NOTIFY_ENABLED`, Windows LIVE, 키·서명, 기존 REQUEST/READY/claim·receipt, Claude 독립 리뷰는 **모두 변경 없음**.
- 기존 대용량 입력 개선 코드에 대한 무과금 GitHub Actions [Run 45208515737](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/45208515737) `offline-selftest` **35 PASS, 0 FAIL** 확인 (실제 v0.2.35 ZIP fixture 시험 포함); `gpt-disposition`/Telegram job SKIPPED. **Windows 서명 포함 `preflight` 재실행은 여전히 NOT_RUN**.

## 파일·원격 확인
- 1회용 워크플로 `.github/workflows/cowork-model-ids-once-20261124.yml`. 최초 commit `94223a1a1a651fa6eb3f0f05bd58f1f007a41ad9` (SKIPPED), 성공 commit `3ba18923e82d0f32aa2b1622c7f32c8cbd0aaf7e`; 원격 내용 readback PASS.
- 현재 workflow의 이벤트는 자기 파일 수정 `push`이며, 성공 동작에는 고정 commit 메시지 `chore: CoWork model discovery GET-only one-shot retry 20261124`, `main`, repo 확인, `run_attempt==1`이 모두 필요. 일반 push/재실행으로 모델 API를 반복 호출하지 않도록 제한됨. 새로운 GET이 필요하면 사용자 별도 지시 전까지 이 일회용 워크플로를 재사용하거나 활성화하지 않음.
- `MODEL_GENERATION_REQUESTS=0`는 워크플로 코드와 Run 45212536082의 실제 성공 로그에 근거. OpenAI 모델 생성 **토큰 과금 0**; 별도의 GitHub Actions 실행 시간 과금 여부는 확인 대상.
- 최신 공식 API 모델 문서: https://developers.openai.com/api/docs/models/gpt-6.2-sol (Responses 및 Structured Outputs 지원).

## 안전 재개 / 다음 한 행동
1. 승인된 Windows Claude Code 호스트에서 최신 `main`을 `core.autocrlf=false`로 가져온 후, 기 게시된 `gpt_disposition_actions.py`로 **완료된 v0.2.35 리뷰에 대해 서명 포함 무과금 실제 preflight를 재검증**. `PACKAGE_INPUT_TOO_LARGE` 재발·크기 초과·기존 claim 존재·서명/ZIP/원본 불일치 시 fail closed.
2. 호스트가 모델 ID `gpt-6.2-sol`의 실제 메타데이터 결과/공식 Responses·Structured Outputs 지원과 사용자 기존 GPT 판정 활성화 승인 범위를 대조해 `COWORK_GPT_MODEL` 변수를 `gh variable set ... --body ...`로 설정·readback. 값 앞 BOM 유입 금지. 현 문서 게시만으로 모델 변수 설정 완료 아님.
3. 원래 `GPT_API_TELEGRAM_ACTIVATION_ONE_SHOT_r0001_20261123_KST.md`의 원본 서명/claim 404/이중 처리 방지 게이트를 유지하고, 모든 사전검증 PASS 후 기존 v0.2.35 완료 리뷰의 최초 GPT 판정 1회/Telegram ACK만 실제 확인. 새로운 Claude 리뷰/유료 요청 자동 재실행 금지.

## 판정
`MODEL_DISCOVERY=PASS` / `SECRET_ENDPOINT_AUTH=PASS_FOR_GET` / `MODEL_RECOMMENDED=gpt-6.2-sol` / `MODEL_VARIABLE=NOT_SET` / `OFFLINE_SELFTEST=35_PASS` / `WINDOWS_PREFLIGHT=NOT_RUN` / `GPT_FIRST_DISPOSITION=NOT_RUN` / `TELEGRAM=UNCHANGED` / `WINDOWS_LIVE=UNCHANGED`.
