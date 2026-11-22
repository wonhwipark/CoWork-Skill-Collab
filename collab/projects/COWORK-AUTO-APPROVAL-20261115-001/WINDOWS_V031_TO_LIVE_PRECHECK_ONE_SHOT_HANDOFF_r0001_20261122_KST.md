# CoWork v0.2.31 → LIVE 직전(3~9단계) Windows 통합 실행 지시 r0001

- 작성: GPT / 2026-11-22 KST
- 사용자 최신 실행 지시: **3~9단계를 한 묶음으로 진행**; **10단계의 비용 위험 수용 및 LIVE 컷오버는 별도 사용자 승인**, 11~12단계는 그 후
- 원본: `wonhwipark/CoWork-Skill-Collab`, **branch `main`**
- 기존 Work: `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/`
- 정본 시작 순서: `collab/CONTEXT_BRIEF.md` → 본 Work `CURRENT.md` 맨 위 → `CLAUDE_INDEPENDENT_REVIEW_IDEMPOTENT_CANDIDATE_RESULT_FOR_GPT_20261122.md` → `GPT_V031_INDEPENDENT_IDEMPOTENCY_DISPOSITION_r0001_20261122_KST.md` → 필요 시 본문 연결 계약
- 소스: Windows 격리 작업 폴더 `D:\User\whpark\skill-collab-watcher-dist\candidates\v0_2_31_independent_idempotent\`, 기존 후보 `D:\User\whpark\skill-collab-watcher-dist\candidates\v0_2_31_independent_idempotent_candidate.zip`
- **Windows 호스트가 보고한 후보 식별:** SHA-256 `1df85457ec01eaaa1a63022777f40b658732355e9d4f016a92b07076da950ea3`, 291484 B, ZIP 103 entries, CRC 정상, 시험 960 PASS/0 FAIL/12 SKIP. GPT가 Windows 원본 ZIP을 직접 읽거나 시험한 것은 아님
- 현행 LIVE **마지막 Windows 보고 기준** v0.2.29; 설치본/키/위임/설정/DB/Task/Notifier 불변. 호스트에서 실행 직전 재확인할 것
- `v0.2.30`/ `v0.2.31` 구 ZIP 불변 보존. 기존 `REQ-COWORK-P1P2-CONTEXT-CODE-R1-20261122` 등 요청·기존 영수증/결과 재실행 0

## 0. 한 번에 처리할 범위와 보호 경계

**목표:** 중복 리뷰 무재실행·비용 하드 게이트 제거·인증된 사용자 의도에 따른 SCOPE 설계/후보 구현을 교차 검증하고, 정식 독립 리뷰 및 읽기 전용 SHADOW까지 실증한 **LIVE 직전 최종 후보**를 만들 것. 단계별 허용 범위가 다르므로 불가한 단계는 BLOCKED/NOT_RUN으로 남기고 앞 단계 가능한 개발·시험·비민감 게시를 계속한다.

- 개발·격리 무모델 테스트·후보 패키징·문서/원격 검증은 진행. 운영 설치·LIVE 정책/위임/키/DB/Task/Notifier 변경, 현행 watcher 종료/재시작, 새 토큰/키 생성, 기존 REQUEST/READY 재큐잉, 비용 없는 척하는 유료 모델 호출, 자동 승인 범위 임의 확장 **금지**.
- **독립 리뷰는 실제 승인된 기존 보호 서명·REQUEST/READY 경로에서 1건만** 수행. 현재 사용자 지시는 3~9단계 개발·검증의 목적과 리뷰 진행 의도를 나타내지만 GitHub 문구만으로 신뢰 서명·실행 권한을 발급하지 못함. 실제 유효한 운영 위임/한정 승인, 실제 입력 ZIP 배포 허용, 승인 만료 및 기존 진행 이력을 확인. 없으면 새 유료 호출·서명·READY 없이 `INDEPENDENT_REVIEW=BLOCKED_AUTH`, 준비·정적 검토는 계속.
- **SHADOW는 읽기 전용**: 모델 0, GitHub/DB 업무 레코드 쓰기 0, Telegram 0, 단일 LIVE 보존. 호스트에서 별도 운영 SHADOW 설치/Task/보호 설정 변경을 요구하면 현재 승인 권한을 먼저 확인하고 미확인 시 그 항목만 BLOCKED; 오프라인 격리 SHADOW 시뮬레이션으로 대체하되 실운영 SHADOW PASS로 표시하지 말 것.
- 비용 하드 상한 제거의 위험: 외부 CLI 1회는 Claude CLI **내부의 모델 턴/청구액 상한이 아님**. `timeout_sec`·watcher `max_calls=1`은 유지하되 실제 제한없는 LIVE 위험 수용은 **10단계 사용자 별도 결정**.

## 1. 실행 및 시험 — 단계 3·4

Windows v0.2.31 원본과 패키지 SHA/CRC 재검증 후 **기존 테스트 재사용 및 아래 누락 시나리오만 최소 추가**. 처음부터 전체 기능을 다시 만들지 말 것. 모든 신규 테스트는 fake runner, stubbed Claude CLI, 격리 temp DB와 인메모리/테스트용 원격 claim을 사용; 유료 모델 0. 단순 순차 watcher 두 개가 아니라 **두 독립 watcher가 정확히 동시에 같은 REQUEST/PIN/ZIP을 획득하는 barrier/latch 동시 경합**이 핵심.

| ID | 시나리오 | 반드시 관찰할 PASS 기준 |
|---|---|---|
| G3-01 | 서로 다른 프로세스와 **서로 다른 DB**의 watcher A/B가 동일 ID/revision/PIN/ZIP으로 동시 remote create-only `DISPATCH_<rev>.md` 경쟁 | 원격 claim 원자성, 실제 mock runner 실행 합계 **1회 이하**; 지는 쪽 0회, 기존 기록/원본 덮어쓰기 0 |
| G3-02 | 실패 응답/타임아웃 직후 원격 claim 기록 여부 불명 | UNKNOWN→재확인 또는 봉인, 모델 자동 재디스패치 **0** |
| G3-03 | 동일 ID, 다른 ZIP/SHA/revision; 이미 완료 또는 terminal인 ID | `CONFLICT` 또는 terminal 보존, 외부 모델 디스패치 0 |
| G4-01 | claim 이후 시작 전/시작 후 crash, watcher 재시작, 부팅 시 `CLAIMED`/`RUNNING` 잔존 | 위험한 시작 여부가 불확실하면 `REVIEW_UNCERTAIN` 봉인, 추가 CLI 호출 0 |
| G4-02 | timeout 이외 CLI 비정상 종료/신호/장애/취소/호스트 재시작 | terminal `FAILED` 또는 `UNCERTAIN` 명시, 자동 재모델 호출 0 |
| G4-03 | 모델 완료 후 결과 또는 영수증 게시 중 네트워크 429·5xx·프로세스 중단 | 동일 완료 artifact **게시만 재시도**, 새 Claude CLI 호출 0, 원격 결과·영수증 충돌 안전 |
| G4-04 | 과거 terminal 기록·수동 승인/서명·old budget 필드/회계 ledger 로드 | 신/구 입력 호환, 새로운 가격 조건 차단 0, 기존 수행 이력/회계 유지 |
| G4-05 | 위조 서명/만료/리포지터리 불일치/변조된 원본 SHA·CRC/READY 순서 위반 | fail-closed, 모델 호출 0 |

- `CLAIMED` 단계에서 모델 시작 여부를 확증할 근거가 없다면 성급한 자동 복구 대신 봉인. 외부 요청의 전역 exactly-once는 단순 테스트 문자열이 아니라 **원격 claim 원자성+동시 테스트 결과**로 입증할 것.
- 모든 시험은 `TEST_ID / ENV / BUILD_SHA / INPUT_SHA / COMMAND / EXPECTED / OBSERVED / RESULT / EVIDENCE / EXECUTOR / UTC` 형태로 결과에 기록. 테스트나 실제 디스패치로 기존 REQUEST ID를 이용하지 말고 격리 ID를 사용.
- G3/G4 시험 실패 시 수정·동일 범위 회귀를 반복해 후보를 안정화하되 **유료 호출 0/운영 쓰기 0** 유지.

## 2. SCOPE 설계 확정·후보 구현 — 단계 5·6

**사용자 목표:** 리뷰는 하나의 `independent` 유형으로 유지, 금액/등급/스킬별 기본 가격 판단 제거. 단 사용자/호스트 권한 없이 PUBLIC GitHub 파일만 올려 실행시키는 자동 승인 확대는 금지. 기존 자동 위임이 valid한 범위는 그대로 재사용하고, 범위 밖 요청은 **인증된 사용자 의도(또는 명시적 유효 위임)로만** 진행.

현행 SCOPE 리터럴 allowlist를 단순 `*`로 치환하지 않는다. 새 별도 PC/키를 당연한 필수로 만들지 말고 Windows에 실제 설치된 signer/trust root와 유효한 승인 범위를 **읽기 전용 확인 후 최소 변경(REUSE → CONNECT → gap EXTEND)**.

**의도 매니페스트 후보 계약(설계 가정, 기존 구현 API로 확정하지 말 것):**
- 별도의 신뢰된 승인 이벤트에서만 생성·서명하는 `REVIEW_INTENT_V1` 또는 기존 승인 envelope 확장. **watcher와 GitHub 작성 내용만으로 자체 발급·자체 승인 불가**.
- 검증 대상은 정확한 `repo_id`, `request_id`, `revision`, `skill_id`, `source_commit`, REQUEST/ZIP SHA256과 크기(또는 이와 동등한 기존 원본 pin binding), `issued_at`, `expires_at`, 서명 키 ID 및 필요시 nonce/재사용 차단. 저장 필드/서명 canonicalization은 기존 검증 함수와 호환 여부를 확인해 중복 필드 최소화.
- 사전 위임이 있는 경우 실제 로드된 위임의 issuer/허용 범위/만료/활성 시점을 사용, 없으면 해당 요청에 대한 보호 사용자 승인 필요. 매번 돈을 승인하게 하는 `max_usd`나 새 비용 등급은 다시 넣지 않음.
- 요청 대상 skill ID를 정확 비교, 와일드카드 금지. 잘못된 패밀리/권한·위조/만료·key revocation·manifest replay·서명자 자기발급·소급 REQUEST는 모델 0. GitHub의 요청 본문 내 승인 문구만으로 권한 인정 불가.
- signer의 요청 승인 증거와 watcher의 `SOURCE_PIN`·`READY`·원격 디스패치 선점 단계 모두 기존 보호 경계를 유지. 이전 위임 목록을 임의로 전체 확장하거나 `cowork-context-design`을 몰래 추가하는 우회 금지.
- 서명 사용자 의도 자체를 자동으로 신뢰할 수 없는 경우에는 **신규 signer 생성이나 프로세스 자체서명 없이 `SCOPE=BLOCKED_AUTH_DESIGN`**로 보고. SCOPE 단계가 막혀도 G3/G4의 안전성 시험·기타 후보 패키징·SHADOW 준비는 이어 갈 것.

**필수 SCOPE 테스트:** valid trusted review intent + exact skill PASS; missing/forged/expired/replayed/revoked/wrong repo/wrong skill/wrong input SHA/unapproved future request/old request all fail-closed; auth verification precedes READY; false claim `approved_by_user` in GitHub 0 calls. 모델/운영 자격/DB 쓰기 0.

## 3. 후보 확정 — 단계 7

- 기존 v0.2.31 후보의 최소 delta만 새 `v0.2.32` 또는 검증된 충돌 없는 차기 버전 작업 폴더에 반영. `v0.2.31` ZIP 덮어쓰지 말 것.
- 변경 코드·개발자 자체시험·권한 테스트·새 동시성/부팅 테스트를 통합하여 전체 회귀 실행. PASS/FAIL/SKIP/NOT_RUN과 SKIP 사유 기록.
- ZIP path traversal, symlink, 중복, CRC, manifest, 민감정보/credential, 크기, 전체 SHA256, 원본 file sha/tree hash 기록. 패키지 최종 SHA 동결 이후 코드 수정 시 **새 후보 revision**으로 다시 패키징.
- GitHub 현재 CoWork repo는 PUBLIC. 코드 ZIP 공개 게시나 별도 외부 전달은 **허용 범위를 검증한 경우에만** 실행; 불명확할 경우 Windows 로컬에 보존하고 GitHub에는 비민감 SHA/경로/결과 요약만 게시. PUBLIC L1Work 배송은 이번 단계에 포함하지 않음.

## 4. 정식 독립 리뷰 — 단계 8 (보호 승인 충족 시)

- 개발자 세션 자체시험은 독립 리뷰가 아니다. 개발 세션과 **분리된 별도 Windows Claude Code 리뷰 실행**을 기존 CoWork 공식 reviewer 경로로 요청할 것.
- 실제 코드 ZIP을 입력으로 하는 최초 유효한 신규 REQUEST만 검토; 기존 v0.2.31의 G3/G4 결함 검토를 위해 임의 과금 재요청하지 말 것. 같은 Work·동일 고정 버전의 `SOURCE_PIN`/REQUEST/ZIP SHA 검증, **REQUEST+ZIP commit A → SOURCE_PIN commit B → 보호 서명/READY 마지막 게시 → watcher 1회 디스패치** 순서 유지.
- 현재 저장소 PUBLIC 가시성 및 패키지 반출/모델 전송 허용, 실제 Windows 승인 유효성을 먼저 검증. GitHub 문서 게시만으로 보호 승인 발생하지 않음. 유효 권한이 없으면 `INDEPENDENT_REVIEW=BLOCKED`로 두고 임의 서명/READY/모델 호출 0.
- 리뷰어는 race/remote claim 원자성, 불확실 후 재모델 금지, 서명 의도 위조·소급·scope 우회, ledger/schema 호환성, 코드 ZIP 내용, rollback/shadow 위험에 집중. 실 리뷰가 실행되었을 때만 독립 `REVIEW_RESULT` + `RECEIPT` + 사용량 증거를 읽고 GPT 판정. 리뷰 부정적이면 같은 Work에서 최소 수정·자체 재시험 후 **사용자/보호 승인 없이 자동 2회 리뷰 요청 금지**.
- GPT가 자동으로 review 완료를 인지하거나 무인 판정 API가 켜져 있다고 가정하지 말 것. Windows 독립 리뷰 결과를 결과 문서에 정확히 연결하여 사용자가 현재/다른 ChatGPT 창에서 조회할 수 있게 할 것.

## 5. SHADOW / 운영 전 복원 준비 — 단계 9

- 실제 최신 Windows LIVE 버전·provider 1개·설정/위임 키 검증 상태·DB WAL/SHM·작업 예약/Notifier/Telegram 수신·watcher 서비스 버전·기존 request/receipt 처리 상태를 읽기 전용으로 고정. 이전 보고의 v0.2.29가 현재도 LIVE라고 추정만 하지 말 것.
- **SHADOW_READ_ONLY** 모드로 동일 새 후보의 실제 입력 검증/분류를 호스트에서 점검하되 모델 0, GitHub remote write 0, 운영 DB job write 0, Telegram 0, 현행 provider 1개 유지. 격리 simulation과 실제 host SHADOW은 구분. SHADOW 설치/Task 추가에 새 운영 승인 필요하면 기존 허용 범위를 확인하고 BLOCKED로 분리.
- 변경 전 백업 계획: Windows LIVE 설치본과 config/위임/보호키 참조, 기존 DB(main/WAL/SHM) 일관된 스냅샷, Task/Notifier/Bridge 설정, cursor/lease, provider 단일성, Telegram 중복 watermark를 **실제 운영에 영향을 주지 않는 방식으로 복구 가능한지 확인**. 10단계 승인 전에는 필요 범위 밖의 DB 정지/교체/키 수정/예약 Task 변경 또는 watcher restart 금지.
- 복원 시나리오와 fail-closed 전환 게이트 문서화. 실제 LIVE 실패 시 단일 provider 복원·기존 DB 이력 보존·과거 요청 재큐잉 및 알림 중복 0을 판정할 체크리스트를 제공. 구 이력/미정산 요청 모두 보존.
- 검증 결과 PASS 아니면 `LIVE_READY=NO` 유지. SHADOW 예비 시험 PASS만으로 운영 컷오버/실제 유료 reviewer E2E 성공이라 표현하지 말 것.

## 6. 결과·게시·인계 (중간 확인 최소화)

위 3~9단계를 **한 세션의 기존 Work**에서 가능한 범위 끝까지 수행. 동일 시험 불합격은 관련 부분만 수정·재시험. 불가한 항목은 정확히 `BLOCKED/NOT_RUN`으로 구분하고 남은 비허가 동작을 억지로 진행하지 말 것.

결과 문서 1개(비민감, 신규 파일)와 기존 `CURRENT.md` 최상단 요약, 필요한 기존 TRACKER 현행 필드만 갱신 후 **`wonhwipark/CoWork-Skill-Collab/main` 직접 게시(PR 없음)**. commit + 원격 본문 + 정확한 파일 SHA256/readback 확인. `collab/CONTEXT_BRIEF.md` 및 스킬 카탈로그는 정본 구조/책임 변경 시에만 갱신.

최종 보고 순서:
1. `STATUS` 및 `LIVE_READY=YES|NO|BLOCKED`
2. `G3_RACE` / `G4_RECOVERY` / `G5_SCOPE_DESIGN` / `G6_SCOPE_CODE` / `G7_PACKAGE` / `G8_INDEPENDENT_REVIEW` / `G9_SHADOW`
3. `TEST_PASS/FAIL/SKIP/NOT_RUN` 및 테스트 명령/증거
4. `AUTH_APPROVAL` / `NEW_MODEL_CALLS` / `DISPATCH_COUNT` / `UNCERTAIN_COUNT` / `LIVE_APPLY=NOT_RUN` / `OPERATING_VERSION`
5. `FINAL_PACKAGE_PATH`/`SHA256`/`SIZE`, `GIT_COMMIT`/`REMOTE_READBACK`, `BLOCKER`
6. **`NEXT_ONE_ACTION`: GPT가 실증 결과·인증된 리뷰 판정을 검토해 사용자에게 비용 무상한 위험 수용과 10단계 LIVE 컷오버 승인을 한 번에 제시**

**이 파일은 Windows 작업용 실행 지시이며, 게시 자체는 watcher/Claude Code 자동 호출 트리거 또는 운영 변경 권한이 아니다.** 모든 검증은 실제 호스트 수행 증거가 있어야 PASS.
