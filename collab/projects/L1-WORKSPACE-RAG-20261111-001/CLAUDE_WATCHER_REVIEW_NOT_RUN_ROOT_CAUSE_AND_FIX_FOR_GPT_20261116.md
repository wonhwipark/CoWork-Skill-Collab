# CLAUDE 감시기 리뷰 미실행 원인 분석과 개선 결과 (GPT 판정용)

- 작성: Windows Claude Code (2026-11-16 KST). 호스트 실측과 자체 시험을 구분한다. GPT 판정 전 canonical 아님.
- 사실: 감시기(GitHub LIVE v0.2.20)는 정상 동작 중이었다(Running, 약 30초 주기 스캔, 오류 없음). 이 요청은 `WAIT_INPUT: REQUEST present but no matching READY yet`에서 멈춰 있었다.
- 현재 같은 상태로 대기 중인 요청 4건(모두 APPROVAL_SIG·READY 없음, 결과 없음): `REQ-L1-WORK-KNOWLEDGE-DESIGN-20261115-001`, `REQ-COWORK-DASHBOARD-PRESENTATION-20261115-001`, `REQ-COWORK-AUTO-APPROVAL-V023-R2-20261115`, `REQ-L1-MSC-MD-LINK-STRUCTURE-20261115-001`. 이번에는 MSC 요청만 읽기 전용 점검했고, 나머지 3건은 존재와 파일 목록만 확인했다.

## 원인 (연쇄)
1. **승인 서명·READY가 없었다.** GPT는 서명키가 없어 READY를 만들 수 없고(요청서에도 명시), 이 요청의 USD 1 비용 권한은 미확인으로 남아 있었다. 감시기는 설계대로 기다렸다.
2. **대기 사실을 사용자에게 알리는 경로가 없었다.** Notifier는 완료·실패 등만 알렸고 "승인 대기"는 알리지 않았다. 4건이 대기하는 동안 아무도 몰랐다.
3. **기존 요청을 승인으로 바꾸는 고정 도구가 없었다.** 지금까지 승인은 요청마다 이전 파이프라인 스크립트를 복제해 손으로 만들었다(예: r19→r20). GPT가 올린 요청을 그대로 서명·READY하는 경로가 없었다.
4. **호스트 쪽 응대 실수.** 사용자의 "리뷰해줘"는 비용 승인이 아니다. 그런데 승인 질문 없이 대화형 검토를 먼저 수행했다. 대화형 검토 결과는 감시기 결과(`REVIEW_RESULT_1.md`)를 대신하지 않는다.
5. 자동 승인(v0.2.23)은 GPT 판정과 R2 전이라 미설치이고 `AUTO_SIGNING=OFF`다. 이 요청에 소급 적용되지 않는다. 원인이 아니라 정상 상태다.

## 개선 (실제 적용, 자체 시험)
- **승인 도구**(신규, 운영 경로 미변경): `D:\User\whpark\cowork-phase1\approve\approve_request.py`.
  - `check <id>`: 읽기 전용. 배포된 검증기에 메모리상 READY를 넣어 VALIDATED 여부, 패키지 SHA·CRC, SOURCE_PIN(repo_id, 커밋이 main에 있음, 핀 커밋의 REQUEST 바이트 동일), 승인 키 복호화, 원격 dispatch·receipt·review 없음, DB job 없음, 기존 승인·READY 없음을 확인하고 비용 상한을 출력한다. 서명·쓰기 없음.
  - `approve <id> --max-usd <상한> --execute`: check 재실행 후, 입력한 비용이 정책 상한과 같을 때만 서명(2시간)하고 APPROVAL_SIG.json 다음 READY.md를 마지막에 create-only로 게시하고 원격 바이트를 대조한다. 모델 호출 없음.
  - 시험: MSC 요청 `check` 16/16 PASS(상한 USD 1.0, `APPROVABLE`). 이미 처리된 id, 없는 id는 `NOT APPROVABLE`. 플래그 누락·상한 불일치(`--max-usd 3`)는 서명 없이 거부. **`approve`의 실제 서명·게시 경로는 이번에 실행하지 않았다(미검증).** 이전 `commit_b`와 같은 서명 호출을 쓰지만 새 코드다.
- **Notifier 승인 대기 알림**(운영 적용): `WAIT_INPUT` 중 "READY 없음"인 요청마다 한 번 `[승인 대기] <id>`와 "Claude Code에 보낼 문구: <id> 승인 점검해줘"를 텔레그램으로 보낸다. 다른 사유의 대기는 보내지 않는다. 비발송 시험 17건 전부 PASS(이전 12건 포함). 적용 전 설치본·워터마크를 백업했고(`aa\ops_backup_notifier\`), 적용 후 작업 Running, 프로세스 2개, 워터마크 유지(Dropbox DB 22907 그대로, GitHub DB 정상 전진). 기존 대기 4건은 과거 이벤트라 재전송하지 않는다. 설치본 sha256 `03748fe21507a31d`.
- 변경하지 않은 것: 감시기·DB·키·설정·Task, 자동 승인 설계, 요청·READY·APPROVAL 게시, 유료 모델 호출 0.

## GPT에게 제안
- 요청 게시 후 사용자에게 보낼 안내에 "승인이 필요하다. Claude Code에 `<id> 승인 점검해줘`라고 말하면 읽기 전용 점검 뒤 비용 상한(USD)을 알려주고, 사용자가 그 금액을 확인하면 서명·READY를 게시한다"는 한 줄을 넣는다.
- `HOST_SUBMIT_ONESHOT.md`의 5단계(승인 경로)를 위 도구로 교체한다. 현재는 호스트가 매번 직접 구성해야 한다.
- 대기 4건의 처리 순서와 어떤 요청이 실제 독립 리뷰를 필요로 하는지는 사용자가 정한다. 호스트는 사용자가 비용을 확인한 요청만 승인한다.

## 한계
`approve` 실행 경로 미검증, Notifier 알림의 실제 텔레그램 수신 미확인(비발송 시험만), 대기 3건의 내용은 점검하지 않았다.
