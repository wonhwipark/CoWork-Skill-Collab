# Windows Claude Code 원샷 실행 인계 — Dropbox LIVE 감시기 안전 Disable·아카이브
2026-11-12 KST / r0001
Repository: GitHub PRIVATE **`wonhwipark/CoWork-Skill-Collab`**
Branch: **`main`**
Exact relative path: **`collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/WINDOWS_DROPBOX_WATCHER_SAFE_DISABLE_ONE_SHOT_r0001_20261112.md`**
WORK_ID: `COWORK-DROPBOX-TO-GITHUB-MIGRATION`
**USER_APPROVED**: Dropbox reviewer watcher의 기존 예약작업 **Disable + 안전 중지 + 원본/이력 보존만** 승인.
**EXECUTION AT POSTING**: NOT_RUN. 문서 업로드 자체로 Windows 명령은 실행되지 않는다.

## 0. 최신 정본·실행 전 조건
1. 이 PRIVATE main의 `collab/START_HERE.md`, 이 작업 `CURRENT.md` **최상단 최신 상태**, `USER_DROPBOX_WATCHER_SAFE_DISABLE_APPROVAL_r0001_20261112.md`, `GPT_ETW_RESULT_AND_DROPBOX_LIVE_REEVALUATION_r0001_20261112.md`, 최근 Claude 운영 복구/ETW 결과, 운영 계약을 읽는다. 최신 실측과 문서 주장 구분.
2. 직전 Claude 관측에서는 기존 Dropbox LIVE watcher v0.1.5가 프로세스/스캔 진행 중, 신규 reviewer 모델 호출 0, notifier/Bridge/updater 정상, C/ETW=PARTIAL. 사용자는 Dropbox를 더 이상 사용하지 않는다고 알리고, **기존 watcher만 Stop+Disable, DB/요청/영수증 보존**을 명시 승인. 이 작업은 **GitHub LIVE cutover가 아니다**.
3. **정확한 예약 작업 식별을 실측**한다. 작업 이름을 추정하거나 느슨한 접두어로 여러 작업을 중지하지 말 것. Task Scheduler action, command-line, 서비스 연결, PID 및 런처-자식 관계를 대조해 **1개 watcher task**만 식별. Dashboard updater, Telegram notifier, Bridge, Dispatcher가 다른 업무에도 쓰이는지 전후 영향 확인.
4. 실행자가 Windows 운영 승인된 권한을 갖지 못하면 권한 우회 금지. 관리자 셸이 필요하면 **검증된 최소 명령 한 묶음**만 제공하고 사용자가 안전하게 직접 실행하도록 안내. 중간 반복 요구 금지. 토큰/운영 경로/사용자 계정 비밀이 결과 MD에 출력되지 않도록 한다.

## 1. Gate A — 중지 전 무손실·중복 실행 안전 점검 (READ-ONLY)
- TaskScheduler 현재 State/Triggers/Actions/RunAs/RestartCount/LastResult, watcher v0.1.5 실제 PID(런처·자식 포함), lock 소유자 및 관련 프로세스 상태 확인. 자동 시작/별도 supervisor/bridge 재실행 경로가 해당 watcher를 되살리는지 함께 확인.
- 요청별 현재 pending, WAIT_INPUT/F1, `READY`/review receipt, in-progress, `REVIEW_UNCERTAIN`, 비용/서명/중복 실행 상태를 **서로 구별**. 이미 완료됐다고 기록된 항목을 다시 실행하지 않는다. 읽기 전용 쿼리로도 원본 SQLite `-shm`가 변할 수 있으므로 가능하면 기존 안전 리포트나 격리 사본을 읽고, 운영 DB를 직접 sqlite 연결로 열지 않는다.
- 조건부: 진행 중 reviewer/결과 게시/중복 확인 불능/미정산 유효 READY가 있다면 **중지로 손실이 발생하지 않는 안전한 종료점까지 보존**. 임의 대기 요청 REJECT, HOLD, READY 삭제/생성, 리뷰 호출, 운영 DB 직접 수정은 불가. 정합성 미확인이면 `BLOCKED_INFLIGHT_OR_UNCERTAIN`으로 후속 변경 없이 종료; 사전 점검 결과 게시.
- **모델 새 호출 0** 기준을 잠재적 부작용과 분리 기록. 원래 task가 정상 기승인 요청을 dispatch하는 것이 관찰되면 임의 중지로 작업 손실을 만들지 말고 안전 경계 확인 전 차단.
- Dropbox 신규 사용은 없다는 **사용자의 운영 의도**만 근거로 하되 실제 요청자/외부 dispatcher에서 새 Dropbox 요청을 게시하는지 관찰. 감시기를 중단하면 새 요청을 자동으로 처리하지 못한다는 점을 결과에 명시.

## 2. Gate B — 백업·복원 준비 (LOCALE_ONLY, 원본 불변)
- **중단 전** 기존 Scheduled Task XML/설정, 작업 실행 파일 버전/해시, 관련 서비스·재기동 경로, 현재 처리 중 요청/영수증 인벤토리 및 운영 DB 3종 이름/크기/상태를 **비밀 보호 로컬 위치**에 보존. 민감한 task XML에 account/token/경로가 있으면 PRIVATE GitHub에 게시 금지.
- 운영 데이터 백업은 **일관성 있는 방식으로** 수행하고 검증한다. 가동 중 `state.sqlite3` main/WAL/SHM을 임의 순차 파일 복사한 것을 SQLite 일관 백업이라고 하지 않음. 안전한 VSS/snapshot 기술 또는 watcher가 완전히 quiescent하고 타 writer가 없는 상태에서 동일 snapshot 기준 수집. 운영 DB를 열기 위한 SQLite mode=ro 연결이 SHM/WAL에 미치는 영향이 미검증이면, 별도 검증된 OS-level snapshot 또는 권한 승인된 격리된 일관 백업 방식을 쓸 것. 가능한 과정에서도 운영 DB 스키마/row 직접 변경 금지.
- **중지 전 기본 롤백 수단**: 기존 task XML/export + 원본 설치 폴더/설정 식별 + 데이터/요청/결과/receipt/hash 인벤토리 + 기존 snapshot 가용성. 중지 후 writer가 없는 상태를 증명할 수 있을 때에도 후속 데이터 보존과 restoration test를 **별도 복사본**에서 실시. 타 provider/notifier가 DB를 사용하는 경우 이 접근 자체가 무영향인지 확인.
- 백업 불가/복원 계획 불명/백업 데이터 유출 가능/미정산 위험 -> `BLOCKED_BACKUP_OR_ROLLBACK`으로 보고하고 Disable·Stop **미실행**. 단, 과거 승인된 기존 사본/백업을 검증해 충분하면 이를 재사용(재생성 불필요).
- 백업을 Dropbox, PRIVATE 또는 PUBLIC GitHub로 **업로드하지 않음**. 원본 ZIP/DB/WAL/SHM/로그·자격증명 모두 로컬 보존. 민감정보를 출력/README에 남기지 않음.
- 어느 시점에 어떤 파일을 백업했는지, backup SHA256·size 및 Restore-on-copy PASS/FAIL/SKIP/NOT_RUN을 개인 비밀 없이 집계한 증거만 PRIVATE로.

## 3. Gate C — 승인된 watcher 하나만 Disable + Stop
- **모든 안전 게이트가 PASS인 경우에만** 진행. 실제 task name/path를 다시 확인하고, watcher의 정상 종료 수단을 우선. 새 모델 실행을 유도하는 신규 READY 게시나 테스트 요청 생성 금지.
- 자동 재시작 경쟁이 없도록 **지정된 기존 reviewer watcher 예약 작업만 Disable**한 뒤 안전 중지. `Disable-ScheduledTask -TaskPath <실측> -TaskName <실측>` 및 `Stop-ScheduledTask` 등을 사용할 경우 대상 이름은 호스트에서 1:1 확인한 실제 문자열로만 대입. 멈춤 도중 active job이 생기면 손실 없는 처리·복구 경계 전 진행 중단. 수동 종료가 갑자기 프로세스를 강제 종료시키는 방식이면 reviewer in-flight 0와 journal 상태가 검증되기 전 실행하지 않는다.
- 기존 프로세스가 이미 멈춘 경우 실행하지 않고 예약 작업 Disable만. watcher 자식이 계속 살아있거나 별도 supervisor가 재시작하면 `DISABLE_PARTIAL`로 기록하고 임의 kill/추가 task disable/운영 설정 수정 금지.
- **운영 DB·정책·키·토큰·모델 호출·Telegram·github mode·기존 파일/로그/요청을 수정하지 않는다.** 이미 존재하는 watcher process를 종료하면서 발생한 정상 종료·잠금 해제·이력 로그만 변화로 취급.
- 원래 운영 watcher가 Windows 자동 복구/재부팅으로 다시 기동하는 트리거가 없는지(예약 작업만으로 충분한지) 실제 상태와 현재 설정을 확인. task disable이 모든 복구 메커니즘을 막는다는 추정은 하지 않는다.

## 4. Gate D — 실제 종료·영향·다중 구성요소 검증
- 최소 2회 분리된 관찰 지점에서 watcher 예약작업 `Disabled`, 기존 watcher 모든 관련 PID 0, 새 WATCH_START/SCAN 증가 0(활성 watcher 관점), 새로운 모델 실행/비용 0, 진행 중 job·receipt 유실/중복 0, 기존 DB/요청/receipt 보존을 확인.
- **최종 상태 정확한 표현**: `DROPBOX_WATCHER=DISABLED_ARCHIVED`, `ACTIVE_PROVIDER=NONE`, `GITHUB_PROVIDER=SHADOW_ONLY_OR_NOT_RUNNING`, `CUTOVER=MIGRATION_NOT_CUTOVER`. `DROPBOX_LIVE_DISABLED`라고 표시해도 GitHub LIVE가 된 것은 절대 아님.
- Dashboard updater, Notifier, Bridge, Windows Dispatcher는 변경하지 않고 처음과 같은 실행/대기 상태인지 확인. 해당 서비스가 Dropbox watcher에 의존하여 쓰기 실패·알림 오류를 내는지 읽기 전용 관측. 공용 서비스라도 실제 오류가 생기면 원인/영향을 기록하고 **추가 disable 금지**.
- 예약작업 Disabled만 보고 운영 완전 중단 PASS 선언 금지(PID 확인 필수). 모델 호출 0은 **테스트로 유발한 모델 호출이 없고 추가 실행이 없는 것**을 실제 원장/로그로 확인; 기존 검증되지 않은 WAL/SHM 조작 금지.
- 점검 실패 시 `PARTIAL/NOT_PROVEN` 및 현재 실측 상태를 기록. 임의 재활성화·무제한 restart 금지. 별도 복구 승인이 필요하면 실행하지 않고 제안.

## 5. 혼동 방지: ETW 및 GitHub C·E 상태
- ETW tracerpt/Clock-Time 파서 오류로 `C_ETW=FAIL_UNTRUSTED_MEASUREMENT`, `C_OVERALL=PARTIAL`은 **별개 기술 게이트**다. Dropbox Disable로 C를 PASS로 바꾸지 않는다.
- GitHub READ-SHADOW의 실GitHub GET 시험 PASS도 reviewer 자동실행·정식 독립 리뷰·LIVE 전환을 뜻하지 않는다. GitHub LIVE **승인되지 않음**; 전환 후 GitHub에 새 REQUEST/READY를 올려도 reviewer 자동 처리되지 않음.
- 현재 `INDEPENDENT_REVIEW=NOT_RUN`; 원본 운영 watchdog/DB 삭제, 비밀키 발급, 서명된 READY/비용, PUBLIC ZIP 게시 모두 제외.

## 6. 문서·대시보드·정본 갱신
- 신규 결과 경로 (새 MD, 과거 이력 보존): 
  `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CLAUDE_DROPBOX_WATCHER_SAFE_DISABLE_RESULT_FOR_GPT_20261112.md`
- 필수 항목: `PREFLIGHT_INFLIGHT_REVIEW`, `PENDING_REQUEST_PRESERVATION`, `TASK_IDENTITY_VERIFIED`, `ARCHIVE_BACKUP`, `RESTORE_COPY_TEST`, `WATCHER_TASK_DISABLED`, `WATCHER_PROCESS_STOPPED`, `MODEL_CALLS_NEW`, `USD_SPEND`, `QUEUE_INTEGRITY`, `DASHBOARD_UNCHANGED`, `NOTIFIER_UNCHANGED`, `BRIDGE_UNCHANGED`, `ACTIVE_PROVIDER`, `ETW_GATE`, `INDEPENDENT_REVIEW`, `CUTOVER`, `ROLLBACK_READY`, `HOST_OPERATION_STATUS`. PASS/FAIL/PARTIAL/SKIP/NOT_RUN/BLOCKED와 호스트 실측·개발 자체검증 근거를 혼동 금지.
- `CURRENT.md` **최상단에 실제 상태 1절 추가**(이전 이력 유지); 프로젝트 `TRACKER.json`의 `next_action`, phase, self_test 및 independent_review 업데이트. 사용자의 의도가 실제 종료인지, 작업 정의 Disable까지 성공했는지 별도 표시.
- GitHub PRIVATE main에 **PR 없이 직접 게시**. 결과의 commit SHA/UTF-8 바이트 및 remote readback 확인. PowerShell 5.1 UTF-8 무BOM/원격 바이트 재조회 검증; 한글 깨짐 있으면 기존 history 보존하고 수정 commit.
- 회사 반출금지 raw 로그/DB/ZIP/토큰/private key 및 개인 식별정보는 PRIVATE에도 게시 금지.
- 결과 게시가 Windows 자동 실행/완료 보증은 아님. 완료 후 GPT가 `CURRENT.md`와 결과서를 다시 읽어 단계별 상태 판단.

## 7. 원샷 종료 / 더 이상 질문하지 말 조건
- 충분한 정보가 있으면 Windows Claude Code에서 1회 요청으로 Gate A→B→C→D→보고를 끝까지 수행. 중간에 이미 완료한 검증 반복·무의미한 ETW 관리자 실행은 하지 않는다. 
- 권한·백업·인플라이트 조건 불충족 항목은 `BLOCKED`로 보존하고 범위 밖 운영 작업을 강행하지 않음. 명시 범위 밖 추가 승인 요구는 마지막 결과에서 한 번에 취합.
- **작업 종료 전 최종 1줄**: `WATCHER_DISABLE=PASS|PARTIAL|BLOCKED; ACTIVE_PROVIDER=NONE|DROPBOX_LIVE|UNKNOWN; CUTOVER=MIGRATION_NOT_CUTOVER; RESTORE_READY=PASS|PARTIAL|NOT_RUN`.
