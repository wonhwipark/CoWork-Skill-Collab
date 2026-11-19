# GPT v0.2.29 — 서로 다른 5개 창의 연속 요청 격리 시뮬레이션 r0001

- 날짜: 2026-11-20 KST
- 정본: PRIVATE `wonhwipark/CoWork-Skill-Collab` branch `main`
- 기존 Work: `collab/projects/COWORK-AUTO-APPROVAL-20261115-001`
- 후보: dev `v0.2.29` (310753 B, 114 entries), ZIP SHA-256 `c67bc342fe77547b000fc42e1b886396cbef035c0d265dbcd124947e267ed83f`
- 입력 시나리오: **서로 다른 5개 채팅 창에서 설계 요청 2건, 스킬 수정 3건이 순차 발생**. 각 Work ID, 리뷰 REQUEST ID, revision, 패키지 SHA가 개별인 것을 기본으로 가정. 3개의 스킬 수정이 **같은 스킬/같은 구버전**을 기반으로 시작하는 반례도 별도 시험.
- **실제 실행 범위**: GPT가 직접 Python 격리 SQLite와 가짜 GitHub 파일·서명·runner 상태기를 사용해 모델 9종을 실행 및 assert 검증. 기 검토한 v0.2.29 ZIP 변경 diff, `auto_policy.py`의 STATIC-only, `auto_claims` 고유 키, `POLICY_STOPPED` 전이를 모사했음. 실제 ZIP Python import/Windows watcher 실행 **NOT_RUN**. 결과는 `PASS_MODEL_ONLY`이지 제품 E2E PASS가 아님.
- **비용/보호 상태**: 실제 모델 호출 0, 실제 서명 0, PRIVATE REQUEST/READY 생성 0, 운영 LIVE v0.2.25 / 보호 위임 USD1 유지, 신규 독립 리뷰 NOT_RUN.

## 1. 5개 창 정상 경로 — 후보 v0.2.29와 실제 LIVE를 구분

가정: *미래의* 보호 정책이 유효하게 설정된 `POLICY-STATIC-V1` 요청당 USD3, 해당 5개 Work/skill이 scope 안에 있고, ZIP SHA·SOURCE_PIN·서명 자격·개별 승인 모두 유효하며, 첫 요청의 소급 cutoff도 통과.

| 창 | 작업 | 새 Work/REQUEST 별도 | 모델 상태 |
| --- | --- | --- | --- |
| 1 | 임의 설계 A | 예 | COMPLETED |
| 2 | 임의 설계 B | 예 | COMPLETED |
| 3 | 스킬 수정 A | 예 | COMPLETED |
| 4 | 스킬 수정 B | 예 | COMPLETED |
| 5 | 스킬 수정 C | 예 | COMPLETED |

- 모의 runner 호출 5회, 각 요청별 REQUEST → SOURCE_PIN → APPROVAL_SIG → READY → DISPATCH → RECEIPT → REVIEW_RESULT 순서 보존. 동일 ID 재투입 5건 모두 `DUPLICATE_BLOCKED`. 실제 호출/서명/게시 0.
- *이론상 승인 예산* USD3 × 5건 = **USD15**이며 **일/월 누적 한도가 없음**. 이는 실제 청구/보장 상한을 의미하지 않으며 신규 유료 호출 승인도 아님.
- **자연어로 설계·스킬 변경을 요청한 순간에는 모델 유료 리뷰를 실행하면 안 됨.** 작업/문서/ZIP 게시 자체는 트리거가 아니고, 별도 고정 REQUEST·유효 승인 서명·READY가 필요한 점은 불변.
- 현실은 LIVE `v0.2.25`, STATIC 등급 USD1.50, 보호 위임 USD1이므로 위의 정상 처리 결과를 현재 운영에 대입할 수 없음.

## 2. 네거티브·교차 창 시험 (모두 격리 모델, 제품 동작 검증 아님)

| 시험 | 조작 | 관찰 |
| --- | --- | --- |
| B | 설계 2건에 구 `POLICY-STATIC-V1-DESIGN` 부착 | 설계 2 `REVIEW_POLICY` 차단 / 스킬 3 통과. 향후 자동 설계 리뷰도 유효한 통합 STATIC 정책 선택이 필수. 과거 REQUEST의 정책을 재작성해선 안 됨 |
| C | v0.2.29 모델에 현재와 유사한 cap USD1, tier cost USD1.50 설정 | 5건 `PER_REQUEST_COST` 차단 / `POLICY_STOPPED` 영구 보존 / 모델 호출 0. **현재 v0.2.25 엔진 자체를 실행한 실측이 아님** |
| D | 스킬 3건이 같은 skill, 같은 base SHA에서 출발 + 최신 HEAD 대조 게이트 | 첫 건만 처리, 후속 2건 `STALE_SKILL_BASE` 차단 |
| D2 | 위와 같지만 최신 HEAD 게이트 제거 | 모의 리뷰 자체는 3건 모두 완료될 수 있음. **리뷰/서명/중복 방지 PASS가 패키지 병합 안전까지 의미하지 않음** |
| E | 세 번째 리뷰 DISPATCH 이후 결과 불확실 | 세 번째 `UNCERTAIN` 보존·재투입 0, 나머지 4건 완료. 실제 host lease/recovery는 NOT_RUN |
| F | 설계 2건의 새로운 Work ID가 보호 위임 scope에서 제외 | 설계 2 `OUT_OF_SCOPE`, 나머지 스킬 3 통과 |
| G | 창 5가 창 3과 같은 REQUEST ID/revision 재사용(패키지 SHA는 다름) | 마지막 요청 `DUPLICATE_BLOCKED`; 실제 요청 ID는 전 창에서 유일해야 함 |
| H | 5개 창 모두 동일한 오래된 글로벌 TRACKER SHA를 기준으로 쓰기 | 1건 UPDATE_OK, 나머지 4건 SHA_CONFLICT. 최신 HEAD 재조회→병합→CAS 갱신을 하면 5건 모두 유지; 자동 복구 없는 채 단순 재시도는 불허 |

## 3. GPT 판정 — 현재 그대로 문제없다고 선언 불가

- `SIMULATION=PASS_MODEL_ONLY` (정상 시나리오, 네거티브 예상 차단 및 충돌 재조회 동작은 **재구성 모델의 단언**으로 검증).
- `V029_ACTUAL_PACKAGE_5_WINDOW_TEST=NOT_RUN`; `WINDOWS_HOST_5_WINDOW_TEST=NOT_RUN`; `INDEPENDENT_REVIEW_V029=NOT_RUN`; `LIVE_SWITCH=HOLD`.
- **교차 창 주요 위험 1 — 같은 스킬 기준본 경합**: 새로운 수정 패키지 생성/리뷰 직전과 최종 게시 직전에 대상 스킬의 최신 HEAD·버전·원본 SHA를 재확인. 충돌이면 기존 Work에서 병합/재검증 후 다음 단계. watcher에 스킬별 HEAD 충돌 차단이 구현돼 있다고 검증하지 못했으므로 `UNVERIFIED`; 필요한 기존 Work/패키지 계약 우선 재사용.
- **교차 창 주요 위험 2 — 공유 CURRENT/TRACKER 쓰기 경합**: GitHub update의 blob SHA 기준 낙관적 잠금을 사용하되 409/422/부정합을 무시하지 않음. fetch latest, 개별 항목 무손실 병합, SHA 검증/원격 readback. 창마다 자체 상태를 유지하고 공통 정본은 순서대로 갱신해야 함.
- **승인/비용 위험**: 새 Work의 범위가 사전 위임 허용 목록에 포함된다는 가정 금지. 통합 STATIC이 실제 설치되기 전 구 DESIGN 또는 가격 변경을 우회하지 말 것. 승인된 5건이 실제 리뷰로 전환될 경우 요청당 1회/최대 USD3 수준의 **합산 계획 예산 USD15**에 주의; 추가 유료 호출은 사용자 명시 승인과 보호 서명 게이트에 의존.

## 4. 실제 v0.2.29 ZIP 검증에 추가할 단일 E2E 시나리오

기존 [5회 실제 ZIP 검증 게이트](GPT_V029_PRE_REVIEW_FIVE_SIMULATIONS_AND_HOST_TEST_GATE_r0001_20261120_KST.md)의 범위를 확장하지 않고 **한 회차에서 5개 독립 요청 연속 도착을 재현**:
1. 정확한 ZIP SHA/CRC와 Windows 호스트 개발 시험을 확인하고, 격리 임시 SQLite/가짜 transport/signer/runner만 사용. 실제 서명·네트워크·유료 모델 0.
2. `SIM-W1~W5` 서로 다른 request_id/revision/package SHA/Work로 설계 2·스킬 수정 3을 차례로 게시한 뒤 watcher scan/claim/READY 순서를 측정. 모든 사전검증·승인·scope는 테스트용 임시 입력으로만 구성.
3. unified `POLICY-STATIC-V1` 정상 5건, legacy `-DESIGN` 2건 차단, 허용 목록 누락, 동일 skill base HEAD 경쟁, ID 충돌, 한 건 UNCERTAIN 후 나머지 처리, 공통 CURRENT/TRACKER SHA 경합을 **별도 반례**로 측정. 실제 구현이 미지원이면 `NOT_RUN/FAIL`로 구분하고 정상으로 추정하지 않음.
4. 각 요청의 실제 모의 signer/READY/runner 횟수, remote mock 기록, 중복·비용·원격 readback·복구/거부 결과를 저장. 코드 결함이 확인되면 별도 신규 후보를 만들고 기존 v0.2.29 리뷰를 승계하지 않음.
5. 전부 PASS 및 기존 5회 게이트 충족 전까지 신규 리뷰 REQUEST/READY, 과금, LIVE 설치, USD3 위임 변경은 **HOLD**. 이전 `REQ-COWORK-V028-AUTO-REVIEW-R1-20261120` 재사용·재실행 0.

**NEXT_ONE_ACTION:** Windows Claude Code가 실제 후보 ZIP을 사용한 *5개 창 연속 요청 E2E*를 기존 사전 시험 회차에 합쳐 무과금 실행하고 `CURRENT.md` 및 결과 문서를 PRIVATE `main`에 원격 bytes 검증과 함께 게시. GPT는 이후 독립 리뷰 진행 여부 판정.
