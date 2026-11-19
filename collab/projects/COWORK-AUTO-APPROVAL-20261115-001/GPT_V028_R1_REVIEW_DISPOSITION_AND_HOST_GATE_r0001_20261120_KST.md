# GPT v0.2.28 독립 R1 결과·영수증 판정 및 Windows 후속 게이트 r0001

- 판정일: 2026-11-20 KST
- 정본: PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`
- 기존 Work: `collab/projects/COWORK-AUTO-APPROVAL-20261115-001`
- 독립 리뷰: `collab/reviews/REQ-COWORK-V028-AUTO-REVIEW-R1-20261120/REVIEW_RESULT_1.md`
- 영수증: `collab/receipts/REQ-COWORK-V028-AUTO-REVIEW-R1-20261120/RECEIPT_1.md`
- 통합 호스트 결과: `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/CLAUDE_AUTO_REVIEW_COLLAB_ONE_SHOT_RESULT_FOR_GPT_20261119.md`

## 1. GPT 확인 사실 / 최종 판정
- `REVIEW_EXECUTION=COMPLETED` (rev 1), `INDEPENDENT_REVIEW=COMPLETE_WITH_FINDINGS`, `BLOCKING=0, MAJOR=1, MINOR=2`. 리뷰 입력 고정 SHA = `9e6ee6d30170f0a2890237c7d1b9184e5c423213a18146926b848c5269b8c00c`, 패키지 309367 B, 113 members.
- 원격 `REVIEW_RESULT_1.md`, `DISPATCH_1.md`, `APPROVAL_SIG.json`, `READY.md`, `RECEIPT_1.md`의 request ID / rev / package SHA 일치. 원격 receipt `ok=true`, watcher `v0.2.25`. 이 receipt에는 **비용 필드가 없음**.
- Windows Claude Code의 운영 호스트 결과는 모델 호출 1회, `total_cost_usd=1.1914247` (표시 $1.19, USD3 상한 내) 및 원본·결과 정합을 보고. GPT는 해당 호스트 원장의 실제 데이터베이스와 CLI 청구액을 직접 열람하지 않았으므로 `COST_SOURCE=HOST_AUDIT_REPORTED`; 영수증의 비용값이라고 표시하지 않음.
- Windows 자체 회귀 `1031 PASS / 0 FAIL / 12 SKIP`, 패키지 E2E 가상 시험 PASS는 호스트 보고. 독립 reviewer는 **정적 코드 검토만** 했고 Windows 런타임 시험은 NOT_RUN. 새 LIVE 호스트 SHADOW/유료 E2E는 NOT_RUN.
- **`GPT_DISPOSITION=ACCEPT_WITH_CONDITIONS`**. MAJOR #1의 발생 조건과 영향은 수용. 해당 코드가 보호하는 `enabled_at/earliest_request_at` 메커니즘을 **검증된 호스트 실행 게이트**로 사용하는 운영 완화안 A 채택. MAJOR가 코드 차원에서 해결되었다고 판정하지 않음.
- **`RELEASE_GATE=HOLD_UNTIL_HOST_PROOF`, `HOST_DEPLOY=NOT_AUTHORIZED_BY_THIS_DOCUMENT`**. 단순한 문서 수용·GitHub 게시만으로 LIVE 설치, 보호 위임 증액, 서명 권한을 얻지 않음. 사용자 기존 조건부 원샷 승인 범위에서만 실제 호스트 게이트를 확인한 뒤 작업 가능.
- `REVIEW_R1=CLOSED_NO_RETRY`: 이 요청 재서명·READY 재게시·재큐잉·추가 유료 리뷰·유료 smoke 0.

## 2. 리뷰 지적별 판정
1. **MAJOR #1 / 수정 수용·호스트 조건부 완화**: `PER_REQUEST_COST`로만 거부되고 claim 없는 기존 요청은 `max_request_usd` 상향 시 `enabled_at`을 함께 새 시각으로 갱신하지 않으면 소급 자동 서명 위험. 코드 자체로는 완전 차단하지 않으므로 (a) 변경 전 모든 관련 pending/seen/claim/job/uncertain 원격 대조, (b) 새 `enabled_at`을 **실제 USD3 보호 위임 활성화 시각으로** 설정, (c) 실제 호스트에서 옛 요청 재평가와 가짜 signer/runner 모델 0 SHADOW 입증, (d) 보호된 정상 도구로 재서명·로드 확인을 **필수**로 지정. `enabled_at` 미갱신·권한/원자성 불명·구 요청 적격 가능성·시험 실패는 반드시 `BLOCKED`; 운영 우회 불허.
2. **MINOR #2 / 수용**: `approve_request.py`는 v0.2.28 ZIP 구성품이 아닌 **별도 Windows 호스트 수동 승인 도구**라는 호스트 확인을 채택. REQUEST에 ZIP 내부 포함이라고 쓴 문장은 오류. 고정 REQUEST·ZIP 원문은 수정하지 않고 이 판정에서 정정.
3. **MINOR #3 / 수용**: `docs/AUTO_APPROVAL.md`의 폐기된 일/월 상한 서술은 문서 불일치. 후속 문서 정리 대상으로 기록하되, 기존 ZIP의 단 1바이트도 수정하지 않음. 운영자에게 현행 상한은 요청당 USD3(설치 후), 일/월 상한 없음이며 레거시 키는 무시됨을 별도 인계.

## 3. Windows 조건부 재개: 순서 및 중단선
1. 기존 원샷과 실제 호스트 최신 상태/승인 권한을 재조회. 기존 서명·READY·결과·영수증은 재사용하고 절대 새 리뷰 요청/모델 호출을 만들지 않음.
2. **읽기 전용 선행 검증**: 고정 v0.2.28 ZIP SHA/크기/CRC, 기존 LIVE v0.2.25, 보호 위임 USD1과 실제 enabled_at, 업무상 폐기된 구 DESIGN R1·완료 LARGE R2·Guard UNCERTAIN·구 STATIC/pending 전체의 코드·DB·원격 상태/created_at/first_seen_at/claim/job을 대조. 구 DESIGN R1의 실제 ID/정책/해시 재현을 포함하여 signer/READY/model=0 검증. 이후 권한을 올릴 때 이미 봤던 요청과 오래된 원격 REQUEST가 예외 없이 탈락할지 확인.
3. **추가 무과금 격리시험**: 동일 코드/ZIP을 대상으로 두 반례를 직접 실행: (i) `PER_REQUEST_COST` 거절 후 cap만 올리면 위험하게 적격해지는 현 상태 재현(실제 서명·모델 호출 금지); (ii) cap과 enabled_at을 한 번에 변경하면 예전 요청이 `RETROACTIVE_OR_FUTURE_REQUEST`로 영구 거부됨을 증명. 현재/new STATIC 요청의 정상 처리, 이미 완료·UNCERTAIN 중복 0, 정책 DESIGN/LARGE 자동 거부, READY 마지막을 검사. 이 실험은 최종 ZIP **코드·시험·문서를 수정하지 않는** 독립 호스트 임시 시험으로 수행하고 결과를 Evidence로 보존. 하나라도 실패하면 중지.
4. 위의 근거와 보호된 권한·백업·롤백·단일 provider·작업 중 watcher 정지를 충족하면, 기존 원샷 계약 §4 범위에서만 **동일 리뷰 ZIP 바이트**를 조건부 설치. 보호된 지원 도구가 `STATIC/USD3` 가격·위임 `max_request_usd=3`·신규 `enabled_at`을 watcher 재가동 **전에 일관된 상태**로 적용하고 서명·load·legacy exclusion을 증명할 수 있어야 함. 별도 승인 없는 키/ACL/DB 직접 덮어쓰기 금지. 이 조건이 불가능하면 변경 0으로 BLOCKED.
5. 재가동 전후 실제 ZIP SHA, 2주기+재시작, auto signing SHADOW(가짜 signer·transport·runner; 유료 0), old REQUEST signer/READY/model 0, 누락/중복/불확실 영수증, single provider·rollback 확인. 실패 시 보호 위임 USD1/기존 LIVE v0.2.25로 **재가동 이전 안전 복원**하고 손실/불확실 이력 보존. 유료 신규 LIVE E2E는 다음 정상 요청 전까지 `NOT_RUN`.
6. 기존 Work의 단일 통합 결과에 각 게이트와 실제 `LIVE_VERSION`, `AUTO_SIGNING_USD3`, SHADOW/rollback, 설치 SHA/DB 백업/위임 설정(비밀 제외), HOST_AUTHORIZATION, 비용·모델 호출 변화, 잔여 BLOCKED를 기록. `CURRENT.md`, `TRACKER.json`만 필요한 현행 필드 갱신 후 PRIVATE main 원격 bytes readback. PUBLIC 게시/업무 호스트 배송/새 모델 호출 없음.

## 4. 판정 경계와 다음 한 행동
- 이 판정은 **리뷰 지적 MAJOR의 재발 방지 조건부 채택**이지 **릴리스 무조건 PASS**가 아님. Windows에서 무과금 호스트 증빙을 만족하면 `RELEASE_GATE=PASS_HOST_VERIFIED`와 실제 LIVE 결과를 기록할 수 있음. 불만족은 `HOLD/BLOCKED`와 구 운영 유지.
- 최종 패키지 변경이 필요하면 새 patch SHA/버전을 별도 생성하고 **기존 v0.2.28 리뷰를 새 ZIP의 독립 PASS로 소급하지 않음**. 이번 요청/비용으로 두 번째 리뷰 금지.
- **NEXT_ONE_ACTION**: Windows Claude Code가 기존 원샷 Work 안에서 §3을 조건부로 이어서 실제 결과·영수증을 게시. 먼저 호스트 검증만으로 해결 가능한 blocker를 닫고, 유료 재리뷰나 보호 권한 우회 없이 진행.
