# CoWork Approval Bridge — 수동 Windows 서명 호출 제거 최소 개선 설계

- r0001 / 2026-11-15 KST
- GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab` / `main`
- 정확한 상대 경로: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_APPROVAL_BRIDGE_MINIMAL_DESIGN_r0001_20261115.md`
- 역할: **설계/격리 프로토타입**. 기존 운영 변경·사용자별 실행권한 확대·새 유료 리뷰 호출 승인 문서가 아님
- 기존 최신 운영: `ACTIVE_PROVIDER=GITHUB`, Watcher `v0.2.20` LIVE(Windows 호스트 보고). 기존 Ed25519 signer·approval verifier·REQUEST/READY·N1 원격 예약·중복 게이트·비용 정책 모두 유지
- 문제: GPT가 REQUEST/ZIP·사용자 승인 의사를 GitHub에 게시해도 Windows signer를 직접 자동 호출할 **인증 가능한 승인 이벤트 경로가 없음**. `APPROVAL_SIG.json` 없으면 READY가 올라도 감시기는 모델 0을 유지. 서명키를 GPT·GitHub에 제공하거나 GitHub에 쓰인 '사용자 승인' 텍스트 자체를 권한으로 삼는 것은 금지

## 1. 기본 해법 — 기존 Telegram으로 *1회 승인 탭*, Windows는 자동 서명

```text
GPT → PRIVATE REQUEST/ZIP + commit A/SOURCE_PIN ─┐
                                                  │ (후보 정보, 실행권한 아님)
Windows 기존 승인 처리기(읽기·검증 전용) ◀──────────┘
      │ ZIP/hash/repo ID/policy/중복/키 준비 검증
      │ 사용자가 확인할 고정 요청 요약 + 15분 이하 난수 challenge 전송
      ▼
Telegram 사용자 지정 대화: [승인 1회 최대 $1] [거절]
      │ (사용자가 직접 승인 버튼 선택)
      ▼
Windows 단일 Telegram 입력 소비자
      │ 실제 Telegram 서버의 callback_query;
      │ 고정 owner user ID + chat ID + bot이 발송한 message ID + 난수 + 만료/중복 검증
      ▼
기존 Windows signer (Ed25519 개인키는 운영 PC에만)
      │ 요청 ID/revision/REQUEST SHA/ZIP SHA/Commit A/repo ID/정책/$1/1회/만료 결속
      ├─ APPROVAL_SIG.json create-only → remote readback → 검증
      └─ READY.md 마지막 create-only → remote readback
      ▼
기존 GitHub LIVE Watcher 자동 리뷰 1회 → 기존 RESULT/RECEIPT/Telegram 알림 → GPT 판정
```

**승인을 실제로 수행하는 유일한 사용자 동작은 Telegram의 승인 탭이다.** ChatGPT 대화에서 "승인"이라고 말한 사실은 GitHub 문서만으로 진위를 인증할 수 없으므로, 별도 신뢰된 연결 앱의 실행 권한이 검증되기 전까지 그 문서만으로 signer를 자동 호출해서는 안 된다. 사용자가 GPT에서 요청을 작성한 후 Telegram 승인 한 번을 누르는 방식이며 Windows Claude Code의 매번 수동 실행은 사라진다. 향후 승인 권한을 제공하는 별도 신뢰 ChatGPT connector가 생기면 Telegram 탭 대신 그 **인증된 이벤트**를 받을 수 있도록 입력부만 교체 가능. 비용 승인을 2회 반복하는 설계가 아니라, 모바일 탭이 공식 인증된 승인이다.

## 2. 구현 경계 / 기존 기능 재사용

- **GPT**: 입력 ZIP/REQUEST 검토·고정, 사용자에게 상태 표시, 리뷰 후 판정. PRIVATE의 임의 서류를 작성할 수 있다는 이유만으로 서명 권한 없음.
- **Approval Intake**: Windows에서 기존 Telegram Bot 알림 설정 활용 가능 여부부터 확인. `getUpdates`와 webhook 상호배타 및 기존 inbound 소비자 커서 충돌 여부를 읽기 전용 조사. 이미 다른 소비자가 업데이트를 소모한다면 병렬 `getUpdates` 추가 **금지**; 기존 단일 소비자와 연동할 수 없으면 `BLOCKED_TELEGRAM_INTAKE_CONFLICT`. <https://core.telegram.org/bots/faq>
- **Telegram 인증**: 허용 사용자 numeric ID, 허용 개인 채팅 numeric ID를 **Windows 전용 관리자 설정**에서 읽음. GitHub/요청 문서에서 가져오지 않음. 동일 Bot이 보낸 메시지의 message ID와 호스트 자체 발급 난수(128비트 이상, 예: `approve:<opaque>`, 64 UTF-8 bytes 이하), expires_at≤15분, callback update_id의 재처리 여부를 반드시 검증. 사칭/재전송/다른 대화방·사용자/오래된 버튼/변조된 승인 데이터는 모두 서명 0. Telegram API의 callback_data 크기 제한은 공식 API 기준 1~64 bytes. <https://core.telegram.org/bots/api>
- **요청 고정/요금**: callback 전후 실제 GitHub repo ID, pinned commit A, REQUEST 원시 SHA, ZIP SHA·크기·CRC, SOURCE_PIN, 정책·일일 총액·기존 디스패치/receipt를 **최신 상태로 다시 조회**. 화면에 표시된 요청 ID/revision, ZIP SHA prefix/full 조회 링크, 비용 상한·1회·만료, 과거 결과 존재 여부와 **서명 payload의 바이트 동일성**. $1 초과·다른 request/ZIP·다른 정책·만료·비용 상한 감소·불명 리뷰 상태는 모두 fail-closed.
- **기존 signer/READY 작성**: 기존 Windows v0.2.20의 승인 서명 검증 도구/신뢰 루트/원본 SOURCE_PIN 및 GitHub create-only 기록·remote readback을 재사용. signer 개인키, Telegram token·숫자 사용자 ID를 PRIVATE/PUBLIC/로그/프롬프트에 게시하지 않음. SOURCE_PIN·REQUEST·ZIP 원본 덮어쓰기 금지.
- **중복/장애**: 승인 클릭 update_id와 요청 `(request_id,revision,package_sha256,attempt)`를 로컬 영속 상태에서 **원자적으로 1회 선점**. 로컬 재시작/원격 409/네트워크 timeout/서명 중단/READY 게시 시각 불명에서 기존 원격 APPROVAL_SIG/READY를 조회하고 **정확한 일치에 한해 publish-only/정산**. 새로운 서명·READY·유료 호출 반복을 금지. 모델 디스패치는 항상 기존 Watcher에 맡기며 Approval Bridge가 직접 Claude 실행하지 않음.
- **정책 상한**: 첫 후보는 `POLICY-STATIC-V1`, 단일 리뷰/최대 $1만 허용. LARGE/XLARGE/AUTO 또는 다른 업무는 별도 범위 승인·검증 전 차단. 비용 지출은 기존 Watcher daily ceiling + 모델 max budget에 추가로 종속.
- **운영 보호**: 현재 GitHub LIVE watcher는 계속 단일 제공자. Dropbox Task·DB(WAL/SHM)·Notifier watermark·예약 작업·키/토큰 보호 폴더는 허용된 개발 단계에서 수정 금지. Telegram 입력 소비자는 기존 Notifier를 훼손하지 않는 단일 소비자로 계획; 배포 전 사용자 승인 및 실제 호스트 백업·롤백 필요.

## 3. 실패/크래시 상태 표

| 조건 | 행동 | 모델 호출 |
|---|---|---|
| GitHub REQUEST만 게시 / 승인 MD만 존재 | Telegram 승인이 없으므로 WAIT_APPROVAL | 0 |
| 다른 Telegram user/chat/message/nonce | REJECTED, 원격 서명/READY 생성 없음 | 0 |
| 만료/2회 탭/소진된 update_id/비용 >$1 | REJECTED, 만료 또는 기존 결과만 조회 | 0 |
| REQUEST/ZIP/Commit A/repo ID 변경 | INVALID_BINDING, 기존 승인 무효 | 0 |
| 승인 탭 후 signer 전 크래시 | 로컬 영속 승인 기록만 남김; 자동 재실행 조건은 명시된 원자성/시간유효성 정책으로 제한 | 0 |
| 서명 생성·게시 성공 후 READY 전 크래시 | 기존 서명 동일성 검증 후 READY만 게시(실제 서명 생성 재호출 금지) | 0 (서명 단계) |
| READY 게시 응답 유실 | 원격 READY 원시 바이트 조회 후 일치면 게시 완료 정산; 불명/충돌은 차단 | 중복 신규 호출 0 |
| 리뷰 중 크래시·사용량 한도·영수증 업로드 실패 | 기존 Watcher N1 원격 예약/REVIEW_UNCERTAIN/결과 publish-only에 위임 | 최대 1 |
| Telegram 업데이트 소비자 충돌/봇 인증 불확실 | 신규 listener 시작/토큰 변경 없이 BLOCKED, 운영 유지 | 0 |

## 4. 최소 회귀/수용 기준

- **격리 합성**: 정상 1회, 다른 from.id/chat.id/message_id, challenge 오류, TTL 만료/미래 시각, 중복 update_id/버튼 재탭, 입력 변조, 정책·비용·호출 수 변경, repo ID 변경, local ledger 상태중복. 이후 Windows 실제 signer와 mock Telegram 콜백으로 생성·검증·create-only·readback·READY LAST/승인없는 0회.
- **장애 매트릭스**: crash-before-claim / after-claim / after-sign-before-put / after-PUT-before-readback / after-SIG-before-READY / after-READY-before-dispatch / after-dispatch-before-receipt, 원장 손실·백업 복원; **상태 보존 및 모델 호출 <=1**.
- **보안**: 임의 GitHub 작성자만으로 서명 0, 숨김 키/토큰/ID 외부 게시 0, 관리자 ACL 유효성, idempotency, GitHub 생성 전용 충돌, 최근 사용자 이벤트 확인.
- **Windows 호스트 SHADOW**: Telegram 실제 **발송과 서명/원격 쓰기를 모두 금지**한 모의 이벤트·fake signer로 검증, 원본 운영 DB/키·Task 불변, 기존 GitHub LIVE 정상 상태 유지.
- **실제 설치 전 게이트**: 정확한 변경 파일/기존 운영 코드 실제 diff, 회귀 명령·결과, 후보 ZIP/SHA/CRC/기밀 스캔, 독립 리뷰 수행 여부 별도 표시, 서명/Telegram 입력 충돌·원장 백업/복원·롤백 리허설, 비용 재확인. **운영 Notifier/Task/DB/서명자 변경 및 실제 Telegram 승인 이벤트를 통한 유료 호출 활성화는 별도 승인 및 현장 검증 전 NOT_RUN.**

## 5. 개발용 순수 함수 프로토타입

- 동일 프로젝트 아래 `approval-bridge-prototype/approval_gate.py` 및 `test_approval_gate.py`는 **로컬 합성 판정 로직 예시**. Telegram API·GitHub IO·Ed25519 서명·READY·상태 DB/Task 직접 접근을 하지 않으며 운영 코드가 아님. `python -m unittest -v test_approval_gate.py`로 17개 mock 시험을 작성/검증.
- 이 프로토타입의 `eligible()`가 true여도 바로 signer 호출하면 안 된다. 반드시 Windows 실행 계층의 영속 원자적 claim + callback 진위 + 운영 v0.2.20 verifier + 서버 입력 재검증을 수행한 뒤 signer/READY 처리.

## 6. 현재 판정과 다음 단일 작업

`DESIGN=PREPARED`, `PROTOTYPE_SELF_TEST=17_PASS`, `INDEPENDENT_REVIEW=NOT_RUN`, `WINDOWS_INTEGRATION=NOT_RUN`, `HOST_SHADOW=NOT_RUN`, `OPERATING_APPLIED=NOT_RUN`, `AUTO_SIGNING_ENABLED=NO`, `MODEL_CALLS=0`.

**NEXT_ONE_ACTION**: Windows Claude Code가 정확한 [구현 원샷 인계](WINDOWS_APPROVAL_BRIDGE_IMPLEMENTATION_HANDOFF_r0001_20261115.md)에 따라 실제 현재 Notifier·signer·Watcher 코드/설정과 격리 사본을 대조, 최소 구현 및 합성/SHADOW·보안·롤백 시험/후보 정리를 수행하고 PRIVATE 결과/실바이트 readback. 사용자 기존 `REQ-L1-WORK-KNOWLEDGE-DESIGN-20261115-001` $1 리뷰 승인 범위를 **Approval Bridge 운영 변경 승인**으로 확대 해석 금지. 현재 요청은 별도 기존 signer 절차로 계속 수행 가능, 승인 창/자동 서명 개선을 기다리기 위해 지연시키지 않음.
