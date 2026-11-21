# CoWork PUBLIC · Claude 리뷰 → GitHub Actions → GPT API 독립 판정 구현 기록

- 기록 시점: 2026-11-21 KST
- 정본: `wonhwipark/CoWork-Skill-Collab`, `main` / 기존 [Issue #2](https://github.com/wonhwipark/CoWork-Skill-Collab/issues/2)
- 사용자 최신 지시: CoWork PUBLIC으로 전환하고 기존 Claude 리뷰 뒤 Actions 기반 자동 판정을 구현. **신규 Telegram GPT 판정 알림은 만들지 않음**. 기존 Claude 리뷰 완료 Telegram은 유지.
- 상태: **REPO_PUBLIC=CONFIRMED / EXECUTOR_CODE=POSTED / LOCAL_OFFLINE_TEST=PASS(9) / GITHUB_RUN=NOT_VERIFIED / API_SECRET=NOT_VERIFIED / PAID_API_CALL=NOT_RUN / GPT_AUTO_DISPOSITION=NOT_RUN / API_AUTO_ENABLE=OFF**.
- 기존 Windows watcher v0.2.29와 Claude 리뷰 호출/서명/READY/LIVE 설정은 변경하지 않았음.

## 게시 산출물

| 역할 | 경로 | 실제 Git blob SHA |
|---|---|---|
| 이벤트 구독·Runner·안전 게이트 | [Actions workflow](../../../.github/workflows/cowork-gpt-disposition.yml) | `b3c70fe66938dc217b64a8f0d3e262a38b691b48` |
| GPT API 판정 실행기 | [executor](../../tools/gpt_disposition_actions.py) | `7e83fdf4cca6424f9d68e3961fc94851bde8040f` |
| 독립 오프라인 회귀 | [tests](../../tools/tests/test_gpt_disposition_actions.py) | `77fbf351b39b36cdfdf7e4c6c1207efb628333f7` |

원격 파일을 재조회하여 위 Git blob SHA 일치 확인. 각 파일의 개발 원본 SHA-256: workflow `7181246e966bf3115183e87c7d1efc83c1a02a93ef7b0f09dc2f027595dba344`, executor `610979f9f5a3eb8e01bbd7473d01814f51641c3338f07f8a4e74430aefd265c9`, tests `5b62d55d1350bfb6ec96ecf4dc8a519c00cc616dd50e73c51a2321dce4739ee0`.

## 플로우와 안전 게이트

1. Windows Claude Code의 기존 리뷰 결과·영수증이 GitHub `main`에 게시됨.
2. `push` 경로 필터가 `collab/reviews/*/REVIEW_RESULT_1.md` 또는 `collab/receipts/*/RECEIPT_1.md`의 변경을 감지. **실제 게시 자격이 GitHub Actions `GITHUB_TOKEN`이면 일반 push로 다른 workflow를 다시 시작시키지 못하므로 G0 검증 필수.** 사용자 수동 `workflow_dispatch`는 별도 수단.
3. Runner가 기존 `review_chain.inspect`로 REQUEST→READY→RESULT→RECEIPT 필드 일치, 기존 `GPT_DISPOSITION.json` 없음 확인. SOURCE_PIN `repo_id`, 서명 payload, Windows 승인자 공개키 Ed25519 검증, 원본 ZIP 크기·SHA-256·CRC·멤버 경로, 입력 크기·민감 패턴 검사. 실제 서명 canonical 방식과 공개키는 Windows 호스트 G0 확인 전 PASS가 아님.
4. 승인된 GPT 모델·별도 API 비용 승인·프로젝트 한도·모델 단가·건당 보수적 비용 상한을 모두 확인한 뒤 **모델 호출 전에** 기존 리뷰 폴더의 `GPT_API_EXECUTION_CLAIM.json` CREATE_ONLY로 중복 실행을 선점. 결과 게시 불확실 또는 API 타임아웃이라도 자동 재호출 금지.
5. OpenAI Responses API를 1회만 호출하고, Claude 지적별 독립 수용/변경/거절/보류·근거·미검증·다음 행동을 구조화 JSON으로 받음. `store=false`, 출력 토큰 제한, 자동 재시도 없음.
6. 기존 `collab/reviews/<request_id>/GPT_DISPOSITION.json` CREATE_ONLY 게시 + 원격 바이트 readback. **신규 Telegram GPT 알림 없음.** 모바일 ChatGPT에서 사용자가 공개 GitHub 판정을 조회하고 후속 대화 가능. API 실행 결과를 기존 ChatGPT 대화에 자동 삽입하지 않음.

## 현 상태의 비과금 안전장치

- `gpt-disposition` Job은 `vars.COWORK_GPT_API_ENABLED == 'true'` 및 `vars.COWORK_GPT_COST_POLICY_APPROVED == 'true'`, `vars.COWORK_GPT_PROJECT_SPEND_CAP_CONFIRMED == 'true'`, 저장소 PUBLIC/main을 동시에 충족해야 Runner에 배정됨. 기본 미설정이므로 자동 GPT 호출 불가.
- `offline-selftest` Job은 API 키를 전달받지 않고 Python 구문 검사·9개 오프라인 시험만 실행하도록 구성. GitHub Runner의 **실제 실행 성공 여부는 아직 NOT_VERIFIED**.
- 단위시험: **9 PASS / 0 FAIL** (로컬 Python). 배포 환경·실제 GitHub workflow job·실제 승인자 서명 검증 E2E·OpenAI 모델 응답 E2E는 각각 NOT_RUN/NOT_VERIFIED.
- 사전 비용 계산은 UTF-8 바이트 기반 **보수적 추정**이며 OpenAI 청구액 보증이 아님. 외부 OpenAI 프로젝트의 실제 비용 예산 제한과 사용자 승인 확인이 필수. 기존 Claude `POLICY-STATIC-V1` USD3 정책이 GPT API 호출 승인이 되지는 않음.
- 리스크: `GPT_API_EXECUTION_CLAIM.json`이 생겼는데 결과 기록 실패 시 유료 호출 여부가 불확실할 수 있음. 기존 영수증/실행 이력과 이 claim을 보존하고 임의 재큐잉·재호출 금지. 원격 commit/Actions 로그 대조 후 수동 결정.

## 향후 활성화에만 필요한 별도 설정 (지금 미수행)

GitHub Repository → Settings → Secrets and variables → Actions에서 관리자만 다음을 설정:
- Secret `OPENAI_API_KEY`: 별도 승인된 OpenAI 프로젝트 키. **채팅·저장소·Actions 로그에 값 출력 금지**.
- Variables `COWORK_APPROVER_PUBLIC_KEY_B64`: Windows 실제 신뢰 루트 공개키(개인키 금지).
- Variables `COWORK_GPT_MODEL`, `COWORK_GPT_INPUT_RATE_USD_PER_1M`, `COWORK_GPT_OUTPUT_RATE_USD_PER_1M`, `COWORK_GPT_MAX_CALL_USD`: 승인된 정확한 모델·정확한 요금·한도. 실행기 자체 건당 상한 최대 USD3이고 더 낮은 값 지정 가능.
- `COWORK_GPT_PROJECT_SPEND_CAP_CONFIRMED=true`: 해당 OpenAI 프로젝트의 실제 월 지출 제한 확인 후에만 설정.
- `COWORK_GPT_COST_POLICY_APPROVED=true`: 새 GPT API 과금에 대한 사용자 별도 승인 후에만 설정.
- **마지막으로만** `COWORK_GPT_API_ENABLED=true` 설정. 사용자 별도 승인 전 변경 금지.

G0: GitHub 실제 Actions 실행 결과·Windows 리뷰 게시 트리거의 인증 주체·승인 서명 canonical/공개키·기존 GPT 판정 중복을 읽기 전용 검증. G1: MOCK으로 비용 0 검증. G2: 사용자 별도 API 비용·실제 실시간 동작 승인 후 **새로 완료된 리뷰 1건**으로 제한한 유료 E2E. 과거 리뷰 재리뷰·무인 소급 처리 금지.

## 사용자/운영 판단

CoWork PUBLIC 설정은 **실제 GitHub 메타데이터로 확인**. 이로 인해 기존 문서의 `CoWork PRIVATE` 표현은 작성 당시 이력. 향후 L1 업무 제한 원본·토큰을 PUBLIC에 게시하지 않는 원칙은 유지.

**NEXT_ONE_ACTION:** 현재 Actions 페이지에서 `offline-selftest`의 실제 실행 상태와 Windows 리뷰 게시 토큰에 따른 `push` 이벤트 발생을 확인. 이 단계에서는 새 API 비용을 승인하거나 키를 설정할 필요 없음.

## 구현 보완 (같은 범위)
- 추가 발견: ZIP CRC 검사 전에 모든 멤버를 해제하면 압축 폭탄에 노출될 수 있어 **멤버 개수·각 해제 크기·전체 해제 크기를 CRC 검사보다 먼저 제한**. 신규 회귀 1개를 추가해 로컬 9 PASS; 실제 GitHub Runner 시험은 별도 미확인.
