# GitHub Runner GPT 판정 — 비용 게이트 제거 원샷 결과
- 날짜: 2026-11-23 KST
- 정본: `wonhwipark/CoWork-Skill-Collab` `main` (원격 확인 시 PUBLIC)
- 기존 Work: `COWORK-DROPBOX-TO-GITHUB-MIGRATION`; 연계 `COWORK-AUTO-APPROVAL-20261115-001`
- 사용자 지시: 이전에 폐기한 건당 금액·비용 정책 승인·프로젝트 지출 상한을 GPT 판정 Runner에서도 제거. 별도의 비용 승인 반복 요구 금지.
## 현재 판정
**SOURCE_CHANGE=PASS / REMOTE_READBACK=PASS / STATIC_SAFETY_CHECK=11/11 PASS / PYTHON_UNIT_TEST=NOT_RUN / ACTIONS_PUSH_RUN=NOT_VERIFIED / GPT_API_ENABLED=UNCHANGED(최근 호스트 보고 OFF) / ACTUAL_API_CALLS=0_THIS_CHANGE / GPT_TELEGRAM=UNCHANGED / WINDOWS_LIVE=UNCHANGED**
## 수정 내용
| 경로 | 실제 변경 | GitHub commit / Git blob |
|---|---|---|
| `collab/tools/gpt_disposition_actions.py` | `budget_preflight` 및 `Decimal`, 비용 승인·프로젝트 상한·가격/단가 체크 제거; 신규 claim/disposition의 `budget_upper_usd` 제거; 모델 API 응답 usage·실행 영수증 보존 | `805728033acdd58000ad1a46086951b2001be7d3` / `0713c9c4b8bbde158c71378413887286e689a759` |
| `collab/tools/tests/test_gpt_disposition_actions.py` | 구 비용 거절 테스트를 레거시 비용 플래그가 false여도 유효한 명시적 실행 경로는 통과하는 모의 시험으로 전환, 기존 claim 선점·OFF 시험 유지 | `957c54c6be0da379989db40b8ba6b6ca4bb9d345` / `782d9bf3d56dad58368362ec435edcfa625b3d4c` |
| `.github/workflows/cowork-gpt-disposition.yml` | `gpt-disposition` Job의 비용 정책 승인·지출상한 확인 if 조건 2개와 예산/단가 관련 env 5개 삭제. `vars.COWORK_GPT_API_ENABLED == 'true'` 필수조건은 유지 | `96e839e7afcd4d0a0ff0193d9d9cd06311b61c3e` / `b9fea6a788e133e91626d2de982e7e7b011385f2` |
## 유지된 보호
1. `COWORK_GPT_API_ENABLED` 명시적 ON과 실제 `OPENAI_API_KEY` 존재 없이는 모델 호출 불가.
2. 고정 저장소·브랜치·PUBLIC·`repo_id` 검사, REQUEST/PIN/ZIP 원본·보호 승인 Ed25519, 기존 REVIEW_RESULT/RECEIPT 정합성 검증, 명시 모델명 제한 불변.
3. Work 단위 `ONE_CYCLE_CLAIM.json`, 요청 단위 `GPT_API_EXECUTION_CLAIM.json`을 API 호출 전에 CREATE_ONLY로 선점. 재시도 자동 금지/UNCERTAIN 이력 보존; 모델 출력 `OUT_TOKENS=3000`, 입력 크기 `MAX_SOURCE` 상한 불변.
4. GPT 판정 `GPT_DISPOSITION.json` 원격 게시·readback 이후에만 기존 알림 경로 사용(별도 OFF 유지).
5. 구 버전의 기존 claim/disposition에 들어 있던 `budget_upper_usd`는 **삭제/수정하지 않고 보존**. 새 문서에만 해당 비용 추정 필드 미생성; 실제 API usage는 기록.
## 실제 검증
- 원본 GitHub `main` 세 파일 fetch → 최소 변경 → 각 파일 `update_file` → 해당 원격 파일 재조회 내용 바이트 일치 **PASS**.
- 코드·workflow 정적 보존 검사 **11/11 PASS**: 레거시 금액 차단 제거, opt-in 스위치, API key, 워크/요청 claim, no-retry, 보호 승인 preflight, 사용량 기록, 모의 테스트 보존 등.
- 신규 Python 실제 unittest/CI Run ID는 현 실행 환경에서 확인하지 못함. 기존 Actions Push Runner 실증은 v0.2.35 완료 이벤트 Run `45132178582`/`45132184098`(그 당시는 GPT job SKIP)이므로 **이번 코드의 Python PASS 또는 GPT 실제 호출을 의미하지 않음**.
- 신규 Claude 리뷰 REQUEST/READY, GPT API 호출·과금, Windows LIVE 설치·DB/키/Task/Notifier 변경, Telegram 발송 **0**.
## 명확한 후속
- **추가 비용 승인 필요 없음**: 변경된 코드에서 비용 정책 승인 변수를 더 이상 사용하지 않음. 다만 `COWORK_GPT_API_ENABLED`는 별도 실제 API 실행 활성화 스위치로 남음. 사용자 이 원샷 지시는 *코드 변경 및 무과금 검증* 범위이며 ON 전환이 아님.
- 미검증: Actions Runner 최신 offline-selftest 실행 결과 및 보호 환경 API 키·모델 설정. 실제 API E2E/Telegram은 별도 운영 활성화·실행 권한을 확인한 뒤만.
- 현재 CoWork watcher: 마지막 Windows 보고 v0.2.29 LIVE; v0.2.35 컷오버 조건(실제 GitHub 동시 경합 시험) 별도 유지. Runner 소스만 수정했으므로 watcher ZIP 신규 버전·재리뷰 불필요.
- 이번 변경은 비용을 회계상 0으로 가정하거나 OpenAI 플랫폼의 기존 결제·한도 설정을 삭제한 것이 아님. 실행 후 응답 usage 기록은 유지.
