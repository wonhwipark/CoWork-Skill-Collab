# CoWork 독립 리뷰 단일 실행·비용 게이트 제거 — Windows 후속 구현 지시 r0001

- 결정: 2026-11-22 KST, 사용자 명시 요청. 기존 Work `COWORK-AUTO-APPROVAL-20261115-001`에서 이어서 수행.
- 정본: `wonhwipark/CoWork-Skill-Collab` `main`, 이 Work의 `CURRENT.md` 및 `CLAUDE_COST_GATE_REMOVAL_CANDIDATE_RESULT_FOR_GPT_20261122.md`.
- 기준 후보: Windows 격리 후보 v0.2.30, ZIP SHA-256 `541cd3f1a973fd2869ca3759a2987105a682189ecd81f78752c6e4c32dcbf121` / 288,594 bytes. 후보의 실제 바이트와 테스트 결과는 Windows 호스트에서 재확인할 것.
- 범위: Windows 격리 개발·시험·패키징 및 결과 게시. **이번 문서 게시만으로 운영 LIVE 설치, 실행 권한 확대, 신규 서명/READY, 유료 모델 호출을 승인하지 않음.** 과거 요청 재처리 금지.

## 확정 의도

1. 리뷰 유형은 **독립 리뷰 한 종류**로 통일. '유료 리뷰'를 별도 워크플로·분류·실행 결정으로 취급하지 않음.
2. 새 독립 리뷰의 **비용 기반 실행 허가 판단**과 `--max-budget-usd` 하드 상한을 제거. 요청·위임의 `--max-usd`, `max_request_usd`, USD3 등 과거 값은 새 리뷰 실행 자격 판정에 사용하지 않음. 실제 사용량/청구 금액의 사후 영수증·회계 기록은 유지. 비용 상한 제거는 **무과금 실행을 뜻하지 않으며**, 단 한 번의 CLI 실행에도 여러 유료 모델 호출이 발생할 수 있음.
3. **동일 요청 ID는 한 번만 독립 리뷰를 디스패치.** 이미 완료·실패·청구/호출 발생·불확실한 요청은 자동 재실행하지 않음. 다시 리뷰하려면 **새로운 유효한 요청 ID와 사용자 의도**가 필요.
4. 기존 원본·권한 보호(인증된 요청자/유효 승인, 신뢰 루트, 보호 서명, REQUEST/ZIP/SOURCE_PIN SHA·CRC·repo_id, READY 마지막 게시, 만료 검사)는 유지. GitHub에 REQUEST를 올렸다는 사실만으로 자동 승인·서명하지 않음.
5. **SCOPE/skill allowlist의 구조 개선은 후속 보호 정책 변경**으로 취급. 서명된·검증 가능한 사용자 독립 리뷰 의도와 실행 권한을 기준으로 설계·격리 시험하되 **wildcard 허용, 위임 무단 확대, 기존 대기 요청 소급 디스패치 금지**. 인증된 권한 근거가 없으면 FAIL-CLOSED.

## Windows Claude Code에 요청하는 변경

- 실제 설치본과 후보 v0.2.30을 대조하고 후보 **원본에서 연속 개발**. 구버전 디렉터리에서 다시 시작하거나 동일 Work를 새로 만들지 말 것.
- `review_runner.py` 및 `orchestrator.py`의 `--max-budget-usd` 전달, 값 생성, 실행 실패 처리, 검증 로직을 추적해 **신규 독립 리뷰 경로**에서 완전히 제거할 것. SDK/CLI 실행 옵션 및 legacy 사용자 지정 경로를 확인하고 무작정 문자열 치환하지 말 것.
- `auto_policy.py`, `auto_approval.py`, `approve/approve_request.py`, Windows 복사본 `tools/review_request_gate.py`, `state_store.py`, `notify_events.py`, 관련 문서/시험에서 아직 금액 때문에 서명·READY·디스패치가 거부되는 모든 경로를 추적. 금액이 **회계 관측/기록** 용도인지 **실행 허가** 용도인지 구분하고 후자만 제거. 사용되지 않는 조건·오해를 부르는 운영 문구 정리. 기존 frozen 요청, DB schema, 서명 검증 호환성을 깨지 말 것.
- 요청 ID의 원자적 claim/lease, terminal/UNCERTAIN 봉인, `max_calls=1`, 완료 영수증 우선 인식 유지. 동일 ID가 다른 PIN/ZIP/revision으로 들어오면 새 리뷰로 해석하지 말고 CONFLICT/REJECT. 병렬 watcher 및 네트워크 재시작에도 디스패치 최대 1회.
- **모델/CLI 실행 전** crash 또는 통신 실패의 재개와, **실행 여부가 불확실한 후** 재디스패치를 구분. 후자는 자동 재시도 금지. 이미 COMPLETED 상태인 `REQ-COWORK-P1P2-CONTEXT-CODE-R1-20261122` 등 과거 이력을 보존하고 재실행하지 말 것.
- 모델 호출 횟수와 단일 CLI 실행 내부의 모델 턴 수를 구분. `max_calls=1`은 **watcher의 CLI 리뷰 디스패치 횟수** 보호로 명시하고, 단일 작업 자체의 비용 무상한 리스크를 숨기지 말 것. 기존 타임아웃·프로세스 종료/취소 보호는 금액 규칙과 독립적으로 유지.
- 인증된 사용자 의도 기반 SCOPE 개선 설계안과 실제 실행 권한 검증 근거를 별도 제시. 임시로 `cowork-context-design`를 허용 목록에 넣거나 전체 skill wildcard를 쓰지 말 것.

## 필수 회귀 검증 (전부 무모델 호출)

- **IDEMPOTENT:** 동일 ID 재수집/중복 READY/동시 2개 watcher/재시작/완료 후 재도착 → 실제 CLI 디스패치 1회 이하.
- **UNCERTAIN:** claim 후 실행 결과 기록 실패, 영수증 업로드 실패, 비용 기록/네트워크 불확실 → 자동 2차 호출 0.
- **INPUT:** 동일 ID의 source SHA, REQUEST, PIN, ZIP, repo_id, revision 불일치 → REJECT, 호출 0.
- **AUTH:** 미인증/서명 위조/만료/승인 범위 밖/권한 취소 → FAIL-CLOSED, 호출 0.
- **COST:** 과거 `--max-budget-usd`·`PER_REQUEST_COST`·USD3 불일치가 신규 승인·실행을 막지 않으며 CLI에 비용 상한 인자가 전달되지 않음. 실제 소비 비용 영수증은 정상 기록.
- **LEGACY:** 이전 영수증·보호 서명·DB 기록과 신규 처리 호환, 기존 요청 소급 재실행 0.
- **SMOKE:** 가짜 CLI로 preflight→서명→READY→claim→결과/영수증 순서를 검증. 실제 Claude 유료 호출 0.

## 실행/게시 경계

1. 기존 설치본·DB(main/WAL/SHM)·설정·키/서명·Task·Notifier·watcher의 상태/바이트/유효 위임을 읽기 전용 기준선으로 기록.
2. 새 격리 후보 및 회귀 패키지 생성. 버전 충돌 확인 후 새 버전 발행(구 ZIP 덮어쓰기 금지), ZIP CRC/경로/파일 수/크기/전체 SHA-256 확인.
3. 변경 범위 자체시험과 별도 리뷰를 구분하여 보고. 독립 리뷰를 실제 요청하려면 신규 유효 REQUEST/권한이 있어야 하며 자동 유료 리뷰를 임의 생성하지 말 것.
4. 비민감 결과·시험표·후보 SHA·롤백 절차를 **같은 Work**의 결과 문서와 `CURRENT.md`에 갱신, `main`에 게시·원격 바이트 확인. 코드 후보 ZIP은 저장소 가시성/반출 허용을 확인하기 전 GitHub에 게시하지 말 것.
5. LIVE 교체·비용 상한 없는 모델 실행 활성화·위임/서명 정책 변경은 새 운영 승인 경계. 승인 없이 **LIVE_APPLY=NOT_RUN**, 유료 호출=0, 기존 요청 재큐잉=0. 운영 컷오버 승인 후에만 현행 설치본 및 DB를 백업하고 격리 검증→적용→실제 상태 검증, 실패 시 롤백.

## 보고 형식

`SOURCE_DIFF`, `REMOVED_COST_GATES`, `CLI_BUDGET_ARG`, `IDEMPOTENCY`, `UNCERTAIN_BLOCK`, `AUTH_SCOPE`, `TEST_PASS/FAIL/SKIP/NOT_RUN`, `LIVE_APPLY`, `NEW_MODEL_CALLS`, `PACKAGE_PATH/SHA256/SIZE`, `GIT_COMMIT/REMOTE_READBACK`, `BLOCKER`, `NEXT_ONE_ACTION`.

**완료 기준:** 가격이 신규 독립 리뷰 허가를 결정하지 않고, 유효 요청 ID당 watcher 디스패치 1회 이하, 재시작·불확실 상태에서도 자동 재실행 0, 인가·원본 보호 유지가 시험으로 입증된 격리 후보. 운영 LIVE 적용은 별도 결과로 판정.
