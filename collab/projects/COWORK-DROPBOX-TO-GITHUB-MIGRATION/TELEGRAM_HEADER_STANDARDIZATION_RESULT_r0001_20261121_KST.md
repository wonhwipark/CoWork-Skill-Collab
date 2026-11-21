# Telegram 메시지 머릿말 표준화 결과 (Claude · GPT · 연결 시험)

- 작성: Windows Claude Code, 2026-11-21 KST. Work: `COWORK-DROPBOX-TO-GITHUB-MIGRATION`. 정본: PUBLIC `wonhwipark/CoWork-Skill-Collab`, `main`.
- **결론: 머릿말 4종을 적용하고 시험했다.** 발송 조건, Bot Token, Chat ID, 승인 정책, 중복 방지 로직은 바꾸지 않았다. 신규 리뷰·GPT API·유료 호출 0.

## 1. 머릿말

| 알림 | 머릿말 | 발송 주체 |
|---|---|---|
| Claude 리뷰 완료 | `🔵 [Claude 리뷰 완료]` | Windows Notifier |
| Claude 리뷰 실패 | `🔴 [Claude 리뷰 실패]` (하위: `· 상태 불확실`, `· 결과 게시 실패`) | Windows Notifier |
| GPT 최종 판정 완료 | `🟢 [GPT 최종 판정 완료]` | GitHub Actions (`gpt_disposition_telegram.py`) |
| 연결 시험 | `🔔 [CoWork 연결 시험]` | GitHub Actions (`telegram_smoke.py`) |

Work ID는 GPT 판정과 연결 시험 메시지에 포함된다. Windows Notifier는 감시기 감사 DB만 읽고 Work ID를 저장하지 않으므로 Claude 메시지에는 Work ID를 넣지 않았다(요청 ID, 비용, 결과 위치·링크는 포함). 연결 시험 메시지에는 Run 링크를 추가했다.

## 2. 변경 파일

| 대상 | 변경 | 위치 |
|---|---|---|
| `collab/tools/gpt_disposition_telegram.py` | 판정 머릿말 1줄 | main, commit `506ed738019a` |
| `collab/tools/telegram_smoke.py` | 연결 시험 머릿말 + Run 링크 | main, commit `37dc103b735e` |
| `collab/tools/tests/test_gpt_disposition_telegram.py` | 머릿말·Claude 문구 부재 검사 추가 | main, commit `b7635a007195` |
| `collab/tools/tests/test_telegram_smoke.py` | 머릿말·Run 링크·문구 검사 추가 | main, commit `77be3f42ae49` |
| Windows `notify_reviews.py` (운영) | 완료·실패 3종 머릿말만 변경, 나머지 함수 원문과 동일 | 운영 파일 교체, 백업 `backup_notifier_20261121\notify_reviews.py` |

Windows 운영 파일 SHA-256(앞 16자): 원본 `7ac3eb85bae050e2` → 적용본 `8ea17bbd8dd63d2e`.

## 3. 시험 결과

- **로컬 단위 시험:** Telegram 판정·연결 시험 14건 PASS(모의 네트워크, 실제 발송 0).
- **Notifier 오프라인 시험 6건 PASS:** 완료 머릿말·비용·GitHub 링크, Dropbox 위치 문구, 실패 3종 빨간 머릿말과 구분 라벨, Claude 머릿말이 GPT 머릿말과 다름, 나머지 이벤트(충돌·자동 서명 불확실·자동 승인 정책 중지·인증·자동 승인·거부·승인 대기)가 원본과 글자 단위로 동일, 발송·상태·중복 방지 함수 원문 동일.
- **GitHub Actions 푸시 실행(run `44911302355`, 최종):** `offline-selftest` success(단위 시험 29건), `telegram-smoke` skipped, `gpt-disposition` skipped. 텔레그램 발송 흔적 없음.
- **Windows 운영 dry-run:** `--dry-run --replay 3`로 실제 감사 DB 확인, 메시지 출력만, 상태 파일 변경 없음.

## 4. 운영 적용 여부

- **Windows Notifier: 적용 완료.** 운영 파일을 백업 후 교체하고 작업 `SKILL-COLLAB-Notifier` 한 개만 재시작했다. 재시작 후 작업 Running, 실행 프로세스 2개(런처 + 자식), 코드 해시 일치, 전송 위치(marks, last_id 22907) 유지.
- **GitHub main 반영: 완료.** 발송기 4개 파일은 원격 바이트 일치로 확인했다.
- **GPT API·GPT 판정 알림 활성화: 미적용**(`COWORK_GPT_API_ENABLED`, `COWORK_GPT_TELEGRAM_NOTIFY_ENABLED` 미설정). 실제 GPT 판정 알림 머릿말은 판정이 발생해야 확인할 수 있다.

## 5. 미검증·한계

- 실제 휴대폰 수신 확인(Claude 머릿말 및 연결 시험): 연결 시험은 이전 단계에서 사용자 확인 완료. 실제 Claude 완료·실패 알림 수신은 다음 리뷰 이벤트에서 관측해야 한다. NOT_RUN.
- Windows Notifier 새 머릿말을 실제 이벤트로 발송한 적은 없다(`--dry-run`만). 새 이벤트가 생길 때 한 건을 관측해 기록한다.
- 저장소가 PUBLIC이며 이전 운영 산출물이 인증 없이 읽힌다는 점은 이번 작업과 무관하게 남아 있다(이전 보고 참조).
