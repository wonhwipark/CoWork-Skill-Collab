# Recovery R1 보호 승인·알림 장애 정산 및 재발방지 — Windows 실행 인계 r0001

- 기준: 2026-11-25 KST. 기존 Work COWORK-AUTO-APPROVAL-20261115-001 재사용.
- 저장소: 실제 운영 GitHub PUBLIC wonhwipark/CoWork-Skill-Collab, branch main. 업무 제한 자료·원본 운영 로그·키·토큰 게시 금지.
- 대상 RID: REQ-L1-CHANNEL-RECOVERY-DESIGN-R1-20261125, rev 1. 기존 L1 Work L1-WORKSPACE-RAG-20261111-001.
- 입력: [REQUEST](../../requests/REQ-L1-CHANNEL-RECOVERY-DESIGN-R1-20261125/REQUEST.md), [PIN](../../requests/REQ-L1-CHANNEL-RECOVERY-DESIGN-R1-20261125/SOURCE_PIN.json), A=53ced35a2b095422560e34d5828d2efca6a6d01b, ZIP 16878 B, SHA-256 6b0803091be6ae0272ca4b5d909fa0869d65297611f158dea919dc6a4d4a44a7.
- GPT 직접 조회: REQUEST/PIN만 존재, APPROVAL_SIG/READY/REVIEW_INTENT 및 원격 dispatch/review/receipt 미존재. 실제 호스트 로그·정책·호출 여부는 UNKNOWN. 원격 부재가 과거 로컬 실행 0의 증거는 아님.

## 1. 원인 가설과 확인 대상

v0.2.35 공개 독립 리뷰 ZIP 내부 소스에서 확인: auto_approval.py L369–420, L588–615에서 보호 scope 거절 시 요청별 서명 REVIEW_INTENT를 검증하며, 유효한 intent가 없으면 SCOPE 거절 유지. orchestrator.py L577–596에서 WAIT_INPUT의 실제 auto 처리 결과 기록, notify_events.py L18–23, L89–109, L150–156에서 기존 WAIT_INPUT 알림 지원. 이 기능은 이미 존재하므로 동일 기능 재구현 금지. 실제 활성화/호출/Notifier 전달은 호스트에서 확인. 11/24 설치 기록에는 설정·위임·키·Notifier가 그대로 유지됐음.

가능한 직접 원인: 요청 감지 누락, 보호 scope 또는 프로젝트 범위 불일치, 승인 비활성/만료, 입력/신뢰 검사 실패, 서명 불확실, Notifier 전달 누락. 정확한 원인 하나를 실제 감사 로그·설치본·원격 증거로 확정. SCOPE라고 추정해 위임이나 키를 먼저 변경하지 말 것.

## 2. 읽기 전용 진단 먼저

최신 main을 승인된 로컬 경로에서 읽고 실제 설치 root, DB, 요청 root를 확인. 기존 WINDOWS_READONLY_AUDIT.ps1과 pending_requests_audit.py를 재사용.

```powershell
python collab/ops/pending_requests_audit.py --watcher-root "<실제 설치 root>" --db "<실제 DB>" --requests-root "<검증한 로컬 REQUEST root>" --scope github --request-id REQ-L1-CHANNEL-RECOVERY-DESIGN-R1-20261125
```

- --request-id는 pending 누락도 대상화. auto_seen, 마지막 SCAN_START, 요청별 감사 이벤트/정형화 차단 코드, 기존 jobs/auto_claims를 읽음. 원본 REQUEST 로컬 신선도·provider 귀속은 별도 검증. ID_ONLY 감사 이벤트를 현재 rev/ZIP 실행의 확정 증거로 해석 금지. 진단 결과 전체를 공개 게시하지 말고 승인된 비민감 코드만 요약.
- 최신 실제 watcher/provider/Task/Notifier 프로세스와 last scan, live config에서 자동 승인 enabled, 위임 만료 및 project/skill 적합성, signer/trust root 활성 목적 및 권한만 확인. 키·토큰·설정 전문·로컬 경로·raw audit 출력 금지.
- 정확한 RID/rev/ZIP의 claim, dispatch, receipt, result 및 UNCERTAIN 상태를 우선 대조. 원격 파일 부재만으로 과거 실행 0 단정 금지.
- Qwen 정상 완료 R1과 Recovery R1의 승인/감지/알림 이벤트 차이 대조. 별도 리뷰 호출 없이 기존 기록만 읽음.
- 기존 Notifier가 WAIT_INPUT 및 차단 코드 실제 전달을 지원하는 버전인지, watermark/전달 기록/실패 상태/Task 연결을 확인. 역사 알림 재생 또는 watermark 초기화 금지.

## 3. 같은 R1의 정상 연결

- 기존 사용자 리뷰 의사에 해당하는 정확한 R1 입력만 대상으로, 실제 보호 signer의 유효한 권한 및 현재 중복/만료/입력 검증 PASS일 때 기존 승인 경로를 사용. 승인 범위가 확인되지 않으면 BLOCKED로 종료하며 필요한 승인 한 항목만 보고.
- 위임 범위 밖이면 기존 권한이 허용하는 공식 일회성 수동 승인 또는 보호된 요청별 REVIEW_INTENT 경로를 사용. 후자의 경우 정확한 RID/rev/skill/A/REQUEST SHA/ZIP SHA/size/repo 바인딩, 신뢰된 REVIEW_INTENT 목적 키, 유효기간, nonce, 단일 descendant C 및 동일 A 입력 확인. GPT 본문이나 GitHub 게시만으로 의도 서명 불가. 기존 키/신뢰 루트/위임 임의 확대 금지.
- 기존 claim 또는 서명/호출 UNCERTAIN, 이미 실행·완료 증거가 있다면 새 서명·READY·재디스패치 금지. 결과 게시만 실패한 경우 기존 산출물 게시 정산.
- 검증된 승인 서명 → READY 마지막 create-only → 기존 watcher가 한 번 실행. REQUEST/PIN/ZIP/RID를 재생성하거나 바꾸지 않음.
- 결과와 영수증 원격 readback 후에만 독립 리뷰 완료. 이 R1 자체를 실사용 E2E 사례로 활용. 별도 유료 시험 요청 생성 금지.

## 4. 시스템 재발방지 및 완료 기준

실제 확인된 gap만 기존 watcher/보호 signer/Notifier에 최소 수정. 새 watcher·예약 작업·중복 승인 엔진 금지.

- P0: 자연어 리뷰 요청의 제출 후 실제 호스트 ACK 또는 차단 코드 연결. 기존 watcher의 실제 설정된 scan 주기를 기준으로 정상 접수 확인 구간을 정의(권장 2회 정상 scan). 미감지/미접근/오류는 서로 분리.
- P0: 제출 PASS, 보호 승인/READY PASS, 실제 dispatch/result/receipt PASS 분리. 보호 위임이 유효하면 사용자에게 같은 승인 반복 질문하지 않음. 실패 시 정확한 코드·담당·다음 한 조치 표시.
- P1: 기존 WAIT_INPUT/UNCERTAIN/감시기 중단 Notifier 경로의 전달·중복 억제 검증. 필요하면 차단 사유 변경 시 한 번 알림, 복구 시 stale wait 억제. 사전 서명/권한 없이는 실행 0. 현 코드에 이미 있으면 변경하지 않음.
- P1: 승인 가능한 새 요청, scope 밖 unsigned intent, 변조/만료/중복, signer/READY 실패, 감지/Notifier 실패, 기존 R1 회수 등 무모델 합성 회귀 및 격리 SHADOW. 기존 claim·nonce·DB·설정 보호.
- 변경이 필요한 경우 실제 설치 원본 기준 diff/후보/회귀/독립 리뷰/유효 운영 승인/백업·롤백/설치 바이트 확인/실제 E2E 순서. 현재 인계 자체는 키 생성·위임 확대·임의 운영 설정 변경 승인 아님. 업무 제품 코드·상세 로그 반출 금지.
- 검증 결과는 이 Work에 기존 기록으로 연결. 호스트 확인 전 운영 PASS 금지. 새 요청의 자동 접수는 실제 검증 결과가 있을 때만 PASS.

## 5. GPT 직접 변경·시험 근거

- pending_requests_audit.py commit b1086c510b2625583149a130477048c4c517fbd7, 12345 B, SHA-256 8638cf6012fddb639f77ec821476c7288d438b88eb4ca780a326abbba019fed9.
- test_pending_requests_audit.py commit 12c6eca1e37c92b4266b0243120c73e30191b05d, 13930 B, SHA-256 c7de2a003057ede8dccbe57170aa11429b827c84d79f38e5a3696f91e932a775.
- GPT 격리 합성 SQLite helper 7 PASS. helper 원격/시험 원본 SHA-256 d2246f8083f7b22b9109156a0d52ff695bc04ed76f3b4f140407c97720c5a6ae 동일. 원격 파일 본문 readback PASS. CLI 통합/기존 전체 회귀/Windows 실제 DB/Notifier/독립 리뷰 NOT_RUN. 신규 모델 호출 0(이번 GPT 작업), 운영 변경 0.
- HOST_DIAG=BLOCKED_HOST_ACCESS, R1=SUBMITTED_AWAITING_PROTECTED_SIGNER, INDEPENDENT_REVIEW=NOT_CONFIRMED. 다음 한 동작: Windows 실제 설치 환경에서 §2–4를 승인 범위 내 실행하고 실제 차단 코드 및 결과/영수증 게시.
