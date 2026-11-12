# CoWork GitHub LIVE 전환 — 최소 반복 통합 실행 마스터
작성 2026-11-13 KST | r0001
Repository: GitHub PRIVATE **`wonhwipark/CoWork-Skill-Collab`**
Branch: **`main`**
정확한 상대 경로: **`collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_GITHUB_LIVE_MINIMUM_REWORK_MASTER_r0001_20261113.md`**
Work ID: `COWORK-DROPBOX-TO-GITHUB-MIGRATION`
Status: **MASTER_HANDOFF_PREPARED / WINDOWS_NOT_YET_EXECUTED / NO_PROVIDER_ACTIVE / MIGRATION_NOT_CUTOVER**

## 1. 목적과 우선순위
목표는 **사용자 재지시·관리자 셸 실행·중복 시험·모델 비용을 최소화**하여 검증된 GitHub LIVE까지 가는 것. 안전·반출·서명·독립 리뷰 승인을 우회해 빠른 완료를 주장하지 말 것. 이전 인계와 독립된 새로운 병렬 작업을 추가하지 않고, **기존 작업의 단일 후속 인덱스**로 본 마스터를 사용한다.

**최신 기본 사실 (각 세션 시작 시 CURRENT 최상단 및 결과 근거로 재검증):**
- 기존 Dropbox reviewer watcher 예약 작업 Disabled + PID 0, DB·요청·영수증은 로컬 아카이브 보존. `ACTIVE_PROVIDER=NONE`. 2026-11-12 보고 기준이며 재부팅/재로그인 이후 호스트 재확인은 미실행.
- 잔여 의존성 감사 PASS(Claude 자체 보고): Bridge=RETIRE_CANDIDATE, Dropbox updater=RETIRE_CANDIDATE, Telegram notifier=KEEP(노트 알림이 공용 모듈·비밀 공유). Bridge/updater **아직 실제 Disable 승인·실행되지 않음**. **잔여 Dropbox 작업 종료는 LIVE 전환의 선행 필수 게이트가 아님**. 별도 승인 전 중지 금지.
- GitHub SHADOW의 실제 Contents GET-only 3주기/7회 PASS(이전 호스트 보고); C 운영 DB/lock 무접근 ETW 측정기는 시간/PID 매핑 실패로 `C=PARTIAL / ETW=FAIL_UNTRUSTED_MEASUREMENT`.
- Windows 로컬 후보 `v0.2.10`: 174,745 bytes, reported SHA-256 `67ea7fc63ccc1de77a28025b7c4f1b701ee6f4fa387311bca3f3d2bc7432b108`; 70 items = new 24 + changed 12 + unchanged **34 company-origin items**. GPT는 ZIP 실제 바이트 미검증. 아직 외부 반출 허가 없는 항목을 PRIVATE에도 업로드 금지.
- B 운영 승인자 Ed25519 root/key BLOCKED; D 34개 코드 외부 반출 분류 BLOCKED; E 정식 별도 Claude 리뷰 NOT_RUN; 실제 LIVE 설치/DB 이행/운영 롤백 NOT_RUN.
- GitHub PRIVATE 대시보드는 별도 Actions이고 Windows Dropbox updater와 독립. Public Pages는 승인된 경로만 적용하며 민감정보 공개 금지.

## 2. 재실행 금지·단일 정본 규칙
1. PRIVATE `collab/START_HERE.md`, 작업 `CURRENT.md` **최상단**, `TRACKER.json`, 아래 기존 결과/인계 및 최신 remote commit을 읽고 **증거 ledger 표를 먼저 작성**. 같은 작업의 기존 RESULT가 있으면 해당 완료/실패와 원격 readback부터 재사용.
2. 기존 문서 `GPT_GITHUB_LIVE_FAST_TRACK_PARALLEL_ONE_SHOT_r0001_20261113.md`, `WINDOWS_POST_DROPBOX_DISABLE_DEPENDENCY_AUDIT_ONE_SHOT_r0001_20261113.md`, `GPT_RESIDUAL_DROPBOX_DEPENDENCY_DISPOSITION_AND_DISABLE_PLAN_r0001_20261113.md`는 참고/과거 인계. **이 마스터 하나를 실행 진입점**으로 사용. 중복 Windows 세션·중복 프롬프트 실행 금지.
3. **재사용 증거**: Dropbox watcher Disable 결과, Bridge/updater/notifier READ_ONLY 감사, test key S 보안시험, 비관리자 운영 ACL, 실제 Contents GET-only, 기존 31 synthetic ETW 관련 시험, v0.2.10 사용자/Claude 보고. 개별 시험은 `PASS_REUSED`, `PASS_SELF_TEST_REPORTED`, `FAILED`, `NOT_RUN`을 구분. 현재 코드/환경이 바뀌어 결과 유효성이 깨질 때만 영향을 받은 tests 재실행.
4. 각 gate마다 `InputArtifact/Exact SHA/Environment/Evidence/Test ID/Result/Blocking Reason/Owner/Next Action`를 1행으로 기록. 모호한 반복을 피하기 위해 **같은 실패에서 동일 명령 반복 = 0회**. 실패하면 원인·차이를 특정해 해당 테스트만 새로 실행.
5. Windows 운영 DB의 새로운 SQLite `mode=ro` 연결조차 WAL/SHM에 영향이 있을 수 있으므로 금지. 원본 신뢰키·토큰/로그/ZIP은 PRIVATE GitHub에도 반출 금지. 게시 자료는 비식별 상태·집계·허용된 source-free 코드/테스트뿐.

## 3. 한 세션 내 단계 — 조건부 진행, 불가 항목만 BLOCKED
### Phase 0: 증거 정산과 변경 범위
- 보고서 `CLAUDE_GITHUB_LIVE_FAST_TRACK_READINESS_RESULT_FOR_GPT_20261113.md` 존재 여부를 먼저 확인. 이미 존재하면 달라진 요구/테스트 결과만 갱신하거나 새로운 증거 블록으로 이어서 기록. 진행 중인 다른 세션/동일 모델 호출이 있으면 중복 실행 없이 결과를 대기/정산.
- `CURRENT.md`, `TRACKER.json`의 최신 실제 상태를 우선. 오래된 DRAFT 문서의 당시 Dropbox LIVE 진술은 현 상태로 소급 금지.
- T01~T38, S01~S10 수락시험은 기존 시험에서 실제 매핑된 ID만 증거로 표시; 오래된 원장에 일괄 NOT_RUN이라도 새로운 로컬 실측을 자동 PASS로 변환하지 않음.

### Phase 1: 이미 승인된 비운영 준비·격리 수정 (중간 확인 불필요)
- **C**: 기존 ETL/CSV parser 원본을 로컬 보존본/격리 복사본에서 **비관리자 읽기만** 이용. Provider manifest/이벤트 XML/clock domain/PID·TID·자식 수명 확인. 양성 대조 정확히 귀속되지 않으면 `C=PARTIAL`. 시간 offset 임의 fitting 금지. 기존 GPT ETW preflight에서 수명 밖 파일 이벤트 silent drop을 fail-closed로 수정하고 8.3/junction/hardlink alias 위험을 방어 또는 `NOT_PROVEN` 처리. 합성 테스트/회귀 증거 작성. **관리자 ETW 새 trace·운영 DB 직접 I/O 재실행 없음**. 대체 계약(독립 state dir + Windows ACL + file identity + 정적 call path + isolated runtime)도 **`C_ALT_EVIDENCE=PROPOSED_ONLY`**로 준비, 계약 변경 승인 전 실제 C PASS로 승격 금지.
- **B**: 별도 서명자 기기 운영자·공개키 설치·root ACL/Ed25519 payload/정책 서명·nonce/replay/시계/키 폐기/비용 가드를 정리한 **운영자 실행용 승인 체크리스트**와 시험키 synthetic 검증 준비. **운영 key 생성·개인키 수령·root 설치 금지**.
- **D**: 파일 단위 provenance matrix 정리. 34 unchanged 유래 소스의 소유자·반출 승인 기준 미확정이면 **ZIP 전량 PRIVATE 업로드 금지**. 허가된 안전한 요약/코드 없는 설계 자료로 가능한 독립 검토 범위와 한계만 정의. '코드 없이 전체 ZIP independent review PASS'로 표시 금지.
- **E**: 독립 reviewer input 범위·세션 독립성·유효 REQUEST/APPROVAL_SIG/SOURCE_PIN/READY last·유료 비용 상한·중복 차단·receipt readback을 시험키/합성 데이터로 dry-run. 실제 `READY`·모델 호출·결제·의도치 않은 provider 시작 **0**. 개발 Claude 자체 테스트 != 독립 리뷰.
- **Dropbox 잔여 정리**: 이미 수행한 Bridge/updater/notifier 의존성 감사 **재실행 금지**. Bridge → updater Stop+Disable은 **별도 사용자 명시 승인 전 보류**, notifier 모듈·secret·note publisher 유지. Dropbox 정리의 남은 선택은 필수 C/B/D/E 게이트와 병렬 준비할 수 있다.
- **LIVE 롤백**: 원본 DB·이력·작업 XML을 건드리지 않는 격리 사본으로 동일 요청 재처리 0, REVIEW_UNCERTAIN 봉인, provider one-live, 알림 워터마크, 설치/복원 시나리오를 구성. 원본 watcher 또는 예약작업 재활성화/운영 DB migration 금지.

### Phase 2: 승인 불가 항목은 하나의 패킷으로
**Phase 1 종료 후 사전 정보가 모두 갖춰진 시점에만** 아래 항목을 **중복 질문 없이 하나의 승인 표**에 묶어 제시. 무응답은 승인 아님:
| gate | 승인에 필요한 실제 입력·행동 | 명시 승인 전 |
|---|---|---|
| B | 별도 승인자 기기/관리자 공개키·서명자 지정, trust-root 설치·검증 및 서명 승인 | `BLOCKED_SIGNER` |
| C | ETW 기준 충족 재측정 1회 또는 동등한 독립 증거·변경된 수락 기준에 대한 최종 승인 | `PARTIAL` |
| D | 원본 34개 코드/ZIP의 외부 반출 가능 여부에 대한 소유자·조직 정책 확인(불가하면 대안 설계) | `BLOCKED_EXPORT` |
| E | B/C/D 충족 후 정식 독립 Claude runner/입력·원샷 비용 상한 및 REQUEST/READY·receipt 승인 | `NOT_RUN` |
| Cleanup | Bridge와 Windows Dropbox 갱신기 두 task만 순서대로 Stop+Disable할지 | `PROPOSED` |
| LIVE | Windows GitHub watcher 정식 설치, DB/알림 이행, 운영 호스트 rollback & 단일 provider 활성화 | `NOT_APPROVED` |

**주의**: 사용자에게 위 여러 항목을 *같은 메시지/승인 패킷*으로 묻는 것은 가능하나, 각 항목의 승인 경계·비밀키 보호·사내 코드 반출 허가 및 최종 LIVE 승인은 서로 독립이다. 운영 서명 개인키를 GPT/Claude 대화·GitHub 파일·로그에 첨부하지 말 것. 비용과 서명 단계를 검증했다고 별도 회피하지 말 것.

### Phase 3: 후속 승인 후 실행 계획만 준비
- 권한 게이트가 실제 충족된 경우에 한해 정식 Claude 독립 리뷰 `PASS` + 서명/영수증 readback, GitHub watcher host live 설치, 최종 DB 보존/이행/복구·provider one-live/restart 테스트, notifier 중복 방지 검증 → 사용자 마지막 명시 LIVE 승인으로 cutover.
- 지금 세션에서는 **Windows 운영 watcher/DB/task/Bridge/notifier·인증·토큰 변경 0**. 관리자가 필요한 명령을 매 단계 무의미하게 요청하지 않음; 필요 시 필수 실측 1회에 한해 검증된 하나의 스크립트/정확한 승인 요청을 작성.
- 자동 백그라운드 모니터링/재시도·임의 리뷰 모델 호출 금지. 사용자 불참 시 단순히 진행 중이라고 보고하지 말고 `BLOCKED`를 기록해 종료.

## 4. 한 개의 통합 결과 파일·작업 정본 갱신
Windows Claude가 실제로 실행한 후 결과 파일은 기존 예정 경로 한 개만:
**`collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CLAUDE_GITHUB_LIVE_FAST_TRACK_READINESS_RESULT_FOR_GPT_20261113.md`**

기록 항목: `ACTIVE_PROVIDER`, `CURRENT_BASELINE`, `EVIDENCE_REUSED`, `DELTA_TESTS_RUN`, `C_ETW`, `C_ALT_EVIDENCE`, `B_OPERATING_SIGNER`, `D_EXPORT`, `E_INDEPENDENT_REVIEW`, `CLEANUP_CANDIDATES`, `LIVE_HOST_INSTALL`, `ROLLBACK`, `MODEL_NEW_CALLS`, `USD_SPEND`, `HARD_GATE_APPROVALS_NEEDED`, `NEXT_ONE_ACTION`. 합성/자체시험/실호스트/독립리뷰 증거 명확히 구별.

`CURRENT.md` 최상단과 `TRACKER.json` 유효 enum도 같은 작업에서 갱신하되 최신 파일 원격 재조회·commit·실제 UTF-8 원문 일치 검증. 한 번의 원샷 실행이 여러 버전의 인계서를 생성하는 루프가 되지 않도록 차단. **개발/검증 결과가 다 나올 때까지 새 프롬프트를 요구하지 않는다.**

## 5. 실행 완료 기준
**이번 원샷의 완료:** 최신 실측 근거 재사용 + 사전승인 범위의 delta 개발·시험·비밀 제외 문서·최종 게이트 승인 패킷 + GitHub remote readback.
**LIVE 전환 완료 아님:** `ACTIVE_PROVIDER=NONE`, `MIGRATION_NOT_CUTOVER`, `INDEPENDENT_REVIEW=NOT_RUN` 등 실제 미진행 항목 그대로.

User-facing one-line invocation:
`GitHub PRIVATE wonhwipark/CoWork-Skill-Collab main의 collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_GITHUB_LIVE_MINIMUM_REWORK_MASTER_r0001_20261113.md 하나만 기준으로 실행해줘. 기존 결과를 재사용하고 미해결 차이만 수정·시험해; 승인 항목은 한 번에 모아 최종 보고하고 허가 없는 운영 변경/반출/유료 리뷰/LIVE 전환은 하지 마. 결과는 기존 예정 결과 MD 한 개와 CURRENT/TRACKER만 PRIVATE main에 게시·readback해.`
