# 협업 리뷰 결과 자동 감지 — Claude 운영 평가 반영 및 최소 보완 설계 (r0001)

- 일자: 2026-11-17 KST
- 정본: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab` / `main`
- 기존 Work: `COWORK-DROPBOX-TO-GITHUB-MIGRATION` (리뷰 운송·watcher·Notifier 책임). 대시보드 표시는 기존 `COWORK-GITHUB-DASHBOARD-20261111-001`에서 처리.
- 성격: 사용자 제공 Windows Claude Code의 협업구조 8/10, 자동화 7/10 평가를 검토·통합한 **설계 및 수락 기준**. 평가 점수는 리뷰어 의견이며 독립 운영 계측이 아님.
- 변경 경계: 이 문서는 **실행 트리거 아님**. 신규 REQUEST/READY·유료 호출·서명·watcher 설치/설정·DB 이행·운영/Notifier 변경·PUBLIC 게시 없음.

## 1. 검토 판정

| 리뷰 지적 | 판정 | 감지 기능에 반영할 기준 |
|---|---|---|
| 역할/권한 분리, GitHub 본문은 승인 근거가 아님 | 수용·유지 | 완료 감지와 실행 승인 분리. 리뷰 결과 파일이 생겨도 모델 호출/자동 승인/호스트 명령 금지 |
| 원격 readback·SHA, 자체/독립 검증 분리 | 수용·유지 | 고정 입력·리뷰·영수증 상호 대조, 불일치 시 `UNVERIFIED`/수동 정산. 알림이 독립 검증 PASS는 아님 |
| 사용자 복사·붙여넣기 병목과 WAIT_INPUT | 수용 | 결과 **수신 후** 알림은 무인·무LLM 처리. 비용 없는 인계의 자동 실행 권한은 별도 연구·허용 범위 검증 전 보류 |
| GPT↔호스트 검증 비대칭 | 수용 | GitHub 원격 증거와 호스트 실제 Task/Notifier 수신은 따로 보고. 서명 파일 존재만으로 로컬 보호정책 실행을 직접 검증했다고 표기 금지 |
| 단일 Windows PC/동일 신뢰 도메인 | 수용 | PC 오프라인·감지 지연을 상태로 표시, 재시작 시 누락 복구·중복 0. 자동 서명 권한 확장 금지 |
| 문서 축적 부담 | 수정 수용 | 동일 Work 내 단일 검토 문서+CURRENT 상단 단문/기존 TRACKER 활용. 새 원장/새 Work/새 템플릿 생성을 기본으로 하지 않음 |
| 30초 watcher·자동 서명·READY·결과 게시 | 현행 구현 수용, 실전 증빙은 분리 | 기존 GitHub LIVE v0.2.23 재사용; 결과 수신 감지는 별도 읽기/표시 기능으로만 추가 |
| 소급 금지·한도·서명·중복 fail-closed | 수용·필수 | 기존 원격 dispatch/로컬 중복 금지를 건드리지 않음. 게시 실패·불확실 리뷰 재실행 금지 |
| 문구 존재 확인만 하는 시험의 놓친 BLOCKING | 수용 | JSON/MD 파싱, 실제 Git 이벤트·중복·부분 게시·불일치·재기동의 상태 전이 시험 필수 |
| USAGE_RECEIPT 수동 보충, 비객체 JSON MINOR #2 | 개선 후보 | v0.2.24 등 **별도 변경 후보**로 유지. 결과 자동 감지 선행 조건으로 추가하지 않음 |
| 비용 없는 인계 자동 실행 확장 | 보류 | 기존 보호 위임을 무제한 호스트 명령에 재사용하지 않음. 별도 allowlist/권한·비용 0·명시적 범위 승인 필요 |

## 2. 최신 실증에 따른 리뷰 작성 시점 정정

- 2026-11-16 호스트 평가의 `FIRST_LIVE_AUTO_SIGNED_REQUEST=NOT_OBSERVED`는 당시의 관찰. **현재까지 미관측이라고 일반화하지 않음**.
- 2026-11-17 PRIVATE 원격 확인: `REQ-L1-WORK-KNOWLEDGE-FIXED-R1-20261116` revision 1에 대해 `APPROVAL_SIG.json` 존재, `READY.md` 원본 SHA 일치, `DISPATCH_1.md` 같은 processing_key, `REVIEW_RESULT_1.md` `execution_status=COMPLETED`, `RECEIPT_1.md` `ok=true`/watcher `0.2.23`. 실제 GPT 판정도 `L1-WORKSPACE-RAG-20261111-001/GPT_FIXED_KNOWLEDGE_R1_REVIEW_DISPOSITION_r0001_20261117_KST.md`에 게시됨.
- **판정:** 첫 신규 요청의 원격 승인/READY→dispatch→result/receipt→GPT 판정 연계 증거 **OBSERVED_REMOTE**. GPT가 Windows 로컬 키 서명 과정·Task·Notifier 실송신/수신을 직접 재현하지 않았으므로 `HOST_DIRECT_E2E=NOT_VERIFIED`, `TELEGRAM_DELIVERY=NOT_VERIFIED`. 추가 유료 시험 요청을 만들지 말고 기존 사례로 비유료 정산.
- 비용 액수는 일반 `RECEIPT_1.md`에서 확인되지 않을 수 있으며, 금액 없는 영수증에서 사용료/토큰 추정 금지.

## 3. 최소 자동 감지 계약 (신규 구현 전 G0 확인)

1. **입력:** CoWork PRIVATE `main`의 리뷰 결과/영수증 Git 변경을 기존 GitHub Actions/Notifier로 수신 가능한지 먼저 확인. 이벤트 누락 대비 동일 GitHub 상태에서 회수하는 비유료 reconciliation 고려. Actions `push` 경로·자격 주체에 따라 실제 트리거가 발생하는지 검증.
2. **정식 watcher 리뷰:** `REVIEW_RESULT_<rev>.md` `execution_status=COMPLETED` + `RECEIPT_<rev>.md` `ok=true` + 동일 request ID/revision/패키지 SHA/processing_key를 REQUEST·SOURCE_PIN·DISPATCH와 대조. 결과만 있을 때는 `PARTIAL/WAIT_RECEIPT`; mismatch나 불확실은 `UNVERIFIED`. 인증/서명 검사는 승인 권한을 가진 Windows watcher의 별도 책임.
3. **대화형 Claude Code 리뷰:** 해당 요청서의 고정 RESULT MD + 실행 근거 JSON + 입력 revision/readback을 대조. 이 경로는 watcher RECEIPT를 필수로 요구하지 않되 `INDEPENDENT_REVIEW=NOT_VERIFIED`와 리뷰 완료를 엄격히 구분.
4. **중복/재시작:** 기존 ID·revision·attempt·파일 blob/commit 조합으로 이미 통지한 완료는 재통지하지 않음. 이벤트 순서가 뒤바뀌거나 Actions 재실행, PC 오프라인 후 복구에도 누락/중복 0. 결과 미확실 시 **모델·분석·Job 재실행 0**.
5. **출력:** 기존 CURRENT/TRACKER의 **허용된 현재 필드**만 갱신하고 리뷰 대상 Work에 연결. 실제 GPT 판정 전에는 대시보드에 'GPT 판정 필요' 라벨만; 임의 새 schema/enum 추가 금지. PUBLIC 대시보드는 기존 공개 허용목록의 비민감 요약만; PRIVATE 원문/서명/영수증 상세 공개 금지. 기존 Telegram Notifier에 완료/대기 1회 알림을 재사용.
6. **GPT 경계:** 자동 감지는 순수 GitHub API/파서/Actions/Notifier로 수행하며 리뷰나 GPT 판정을 자동 호출하지 않음. 따라서 **LLM 토큰 0**(GitHub Actions/API 및 알림 서비스 자원은 별도). GPT 판정은 실제 대화·승인된 별도 실행 수단에서만 수행.

## 4. 우선순위와 수락 시험

- **P0 결과 수신/상태 반영:** 기존 watcher/Notifier/대시보드 현재 기능을 먼저 G0 읽기 확인; 누락 연결만 최소 보완. 비유료 실제 GitHub 테스트에서 (a) 결과+영수증 정합, (b) 결과 먼저/영수증 나중, (c) SHA 불일치, (d) 중복 push/재시작, (e) 대화형 리뷰의 실행 JSON 누락/도착, (f) 지연·PC 오프라인 복구를 PASS/FAIL/SKIP/NOT_RUN 기록. Telegram 실제 수신은 별도 계측.
- **P1 문서/시험 품질:** 문자열 존재 시험 대신 파서·상태 전이·실행 경로 검증, 동일 Work CURRENT 요약과 기존 TRACKER 정합화.
- **P2 watcher 후보:** `_auto_usage_locked`의 비객체 JSON 오류 회귀와 USAGE_RECEIPT 자동 생성 필요성은 별도 작은 변경으로 평가. 감지와 무관한 버전 업·독립 유료 리뷰를 이번 범위에 묶지 않음.
- **P3 사용자 인계 병목:** 비용 없는 일반 작업의 보호된 전달/기동은 기존 GitHub 문서가 실행 신호가 아닌 원칙을 유지하는 별도 설계·사용자 승인 항목. 새 Windows 실행 경로/신뢰 루트 확대를 이번 감지 변경에 포함하지 않음.

## 5. 이번 작업 판정 및 다음 한 동작

- `REVIEW_FEEDBACK=ACCEPT_WITH_SCOPE_CORRECTION`
- `DETECTION_DESIGN=DOCUMENTED_ONLY`
- `DETECTION_IMPLEMENTATION=NOT_RUN`
- `WINDOWS_HOST_TEST=NOT_RUN`, `TELEGRAM_REAL_RECEIPT=NOT_VERIFIED`, `NEW_LLM_CALLS=0`
- **NEXT_ONE_ACTION:** 기존 `dashboard/.github workflows` 및 Windows Notifier/리뷰 파일 파서의 현행 기능을 G0 읽기 전용 대조하여 **이미 있는 검출과 누락 연결을 구분**하고, 입증된 gap만 최소 수정·비유료 상태 전이 시험 수행. 새 감시기/스키마/자동 실행 권한 추가 금지.
