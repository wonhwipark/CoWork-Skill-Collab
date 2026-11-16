# 리뷰 완료 자동 감지 — 최소 보완 구현 및 검증 (r0001)

- 기준 일자: 2026-11-17 KST
- 정본: PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`
- 기존 Work: `COWORK-DROPBOX-TO-GITHUB-MIGRATION`. 신규 Work/원장/서명/READY/모델 호출 없음.
- 사용자 추가 확정: **리뷰 요청 → Claude 독립 리뷰 1회 → GPT 판정 = 한 작업의 1사이클**. 보완/자체시험은 기존 Work에서 진행하되 자동 재리뷰·무한반복 없음.

## 1. G0 기존 기능과 확인된 gap

- 기존 `collab/dashboard/review_chain.py`가 REQUEST/READY/REVIEW_RESULT/RECEIPT 필드의 링크 정합성을 읽기 전용 검사하고, 기존 `.github/workflows/cowork-dashboard.yml`은 PRIVATE main의 `collab/requests/**`, `collab/reviews/**`, `collab/receipts/**` 변경에 반응해 상태를 재생성하고 있었음. 새 watcher 필요 없음.
- 기존 시스템은 검출된 리뷰를 대시보드에서 `GPT_NOT_OBSERVED`로 표시하지만, **새로 완료된 리뷰의 1회성 판정 필요 이벤트**를 별도 표시하지 않고, 실제 GPT가 프로젝트 문서로 판정했더라도 `GPT_DISPOSITION.json`이 없으면 같은 요청이 계속 판정 대기로 보이는 gap이 있었음.
- Windows Notifier 실제 소스/Task/Telegram 수신은 이번 모바일 GPT 환경에서 직접 확인하지 못함. 기존 Notifier 변경·실제 발송을 주장하지 않음.

## 2. 최소 변경 (PRIVATE main, PR 없음)

| 경로 | 변경 | 최종 UTF-8 bytes / SHA-256 |
|---|---|---|
| `collab/dashboard/review_completion.py` | 기존 PRIVATE `state.json` 이전 스냅샷과 갱신본의 차이에서 신규 리뷰·영수증 연결 완료 1회만 검출; 정합성 불일치 fail-closed, GPT 판정 종료 시 재통지 0, GitHub Actions job summary에만 표시 | 4928 B · `4754a81e55e3651d30dc366bcd0e4f4258004aba6bc3301a857aa84442e1d401` |
| `collab/dashboard/tests/test_review_completion.py` | 신규 완료, 결과/영수증 분리 도착, 중복, 최종 GPT 판정 후 종료, 변조·형식 오류 11회 회귀 | 3140 B · `d1f524a14d1cb5fba9a5ce512372a0324b595476c2f6fa8001e32995a58e690d` |
| `collab/dashboard/review_chain.py` | 기존 GPT 판정 finding의 `m-1`·`m02` 등 소문자/하이픈 없는 ID 표시만 허용 범위 확대; 검증 없는 PASS 승격 금지 | 11028 B · `10cc0bd2bea900f1f94f31f61c142a013030d66a54df34ffc95df1dec17c6e61` |
| `collab/dashboard/tests/test_review_chain.py` | 7개 지적 등 비표준 MINOR ID 누락 방지 회귀 1건 | 5337 B · `2e2ba055fccceae1d2654de908d0fb9e84646a432f061ada4e9baed71b42481c` |
| `.github/workflows/cowork-dashboard.yml` | 기존 대시보드 Action에 이전 상태 복사→새 상태 생성→델타 판정→PRIVATE Action 요약 출력 연결. 모델·외부 API·Telegram 호출 0 | 2883 B · `7b8c3abd7da16aa0b47c64cefe0fe2069efe24abf2699bdd6ece82ab62f1d06c` |
| `collab/reviews/REQ-L1-WORK-KNOWLEDGE-FIXED-R1-20261116/GPT_DISPOSITION.json` | **이미 끝난** R1 리뷰의 기존 GPT 판정(`ACCEPT_WITH_CHANGE`)을 현행 대시보드의 기구현 메타 형식으로 등록. 새 GPT 판정이나 재리뷰 아님. 원본 판정 문서 Git blob `4bbc28d770e831ef9df2a6fd0ab74e252699c890` 연결 | 1510 B · `cbd5132e8fd04cb206497f645b60154c2612d3c11e893d405d1ea8806368b086` |

- 관련 commit: `cd25bb6d4af6`(detector), `6a247795d05b`(11 tests), `b84a9f7b6d2f`(Actions), `8c347912394a`(기존 GPT 판정 등록), `568286448416`(finding), `53eaa530e11c`(finding test).
- 위 6개 파일 모두 PRIVATE `main` 원격 재조회·본문 일치 확인. SHA-256은 원격 UTF-8 실제 바이트 기준.

## 3. 실제 시험

- 로컬 격리 단위시험 신규 detector **11/11 PASS**, 모델/API/Windows 호출 0.
- GitHub PRIVATE Actions [run #43902428499](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/43902428499) **completed/success**, 기존+신규 대시보드 unittest **77/77 PASS**, PUBLIC preview 격리 unittest **8/8 PASS**, PRIVATE 리뷰 완료 summary 스크립트 실제 실행 PASS.
- GitHub `collab/dashboard/state.json` 원격 readback: `REQ-L1-WORK-KNOWLEDGE-FIXED-R1-20261116`의 `request/ready/review/receipt/gpt=true`, 단계 `GPT_RECORDED_UNAUTHENTICATED`, 지적 7건, GPT verdict `ACCEPT_WITH_CHANGE`. **서명과 Windows 호스트 직접 검증은 이 PRIVATE 대시보드의 책임이 아님.**
- 가짜 신규 리뷰/READY를 PRIVATE main에 만들지 않았으므로 **신규 실제 결과 도착에 대한 1회성 Actions 알림 E2E는 미관측**. 합성 상태 전이 시험 11건과 Actions 실행 확인을 합격 범위로 한정.

## 4. 미실행·경계

- `PRIVATE_ACTIONS_SUMMARY=IMPLEMENTED_PASS` / `REVIEW_RESULT_DETECTION=IMPLEMENTED_AND_SYNTHETIC_TEST_PASS`.
- `TELEGRAM_REAL_RECEIPT=NOT_VERIFIED` / `WINDOWS_NOTIFIER_SOURCE_AND_HOST_TEST=NOT_RUN` / `CHATGPT_AUTO_WAKE_OR_AUTOMATIC_GPT_JUDGMENT=NOT_IMPLEMENTED`.
- `NEW_REQUEST_READY=0`, `NEW_CLAUDE_REVIEW=0`, `NEW_LLM_CALLS=0`, `WATCHER_OPERATIONAL_CHANGE=0`, `PUBLIC_DEPLOY_CHANGE=0`.
- Actions 요약은 GitHub PRIVATE에서 확인하는 알림 성격의 기록이지 휴대폰 푸시/Telegram 전달이 아님. 비용 없는 인계 자동 실행·비판적 R0~R3·USAGE_RECEIPT 개선은 별도 기존 범위로 보류. 기존 LIVE 서명/승인/비용/중복 정책은 건드리지 않음.

## 5. 다음 한 동작

Windows Claude Code의 **기존 Notifier**를 읽기 전용으로 확인하여 `REVIEW_RESULT + RECEIPT` 완료 이벤트가 실제 Telegram 수신으로 이어지는지, 이벤트 워터마크가 중복·재기동을 막는지 점검할 것. **실제 새 유료 리뷰 요청을 만들지 않고** 기존 완료 건 및 비발송/허용된 테스트만 사용. 확인되지 않으면 `NOT_VERIFIED`로 유지. 본 문서 GitHub 게시만으로 Windows 호스트 실행은 시작되지 않음.
