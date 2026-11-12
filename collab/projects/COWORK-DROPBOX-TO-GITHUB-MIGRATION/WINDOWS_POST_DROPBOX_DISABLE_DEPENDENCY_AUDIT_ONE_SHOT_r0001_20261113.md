# Windows Claude Code 원샷 인계 — Dropbox 감시기 중지 후 잔여 구성요소 의존성 감사
작성: 2026-11-13 KST | rev: r0001
저장소: **GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`**
브랜치: **`main`**
인계서 정확한 경로: **`collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/WINDOWS_POST_DROPBOX_DISABLE_DEPENDENCY_AUDIT_ONE_SHOT_r0001_20261113.md`**
작업 ID: `COWORK-DROPBOX-TO-GITHUB-MIGRATION`
상태: **READ_ONLY_AUDIT_AUTHORIZED / WINDOWS_EXECUTION_NOT_YET_OBSERVED**
**운영 변경·Disable/Stop·DELETE·설치·재부팅·ETW 관리자 재시험 승인 아님.**

## 0. 목적과 기준
사용자는 Dropbox 기반 리뷰를 더 이상 사용하지 않아 reviewer watcher의 안전한 Stop + Task Disable을 명시 승인했고, Windows에서 성공 보고됐다. 새로운 후속 지시는 **남아 있는 Dashboard updater, Telegram notifier, Bridge의 사용처/의존성 확인 및 정리 대상 판정**이다. 다음 사용자 판단을 한 번에 할 수 있도록 각 구성요소의 실제 유지 필요성, 안전 중지 범위, 위험/복구 조건을 근거별로 제시하라.

시작 시 PRIVATE `collab/START_HERE.md`, 이 프로젝트 `CURRENT.md` 최상단, `GPT_DROPBOX_WATCHER_DISABLE_DISPOSITION_r0001_20261113.md`, `CLAUDE_DROPBOX_WATCHER_SAFE_DISABLE_RESULT_FOR_GPT_20261112.md`, `TRACKER.json`, `collab/dashboard/README.md`, `collab/projects/COWORK-GITHUB-DASHBOARD-20261111-001/CURRENT.md`를 읽고 현재 사실/오래된 역사적 기록을 구분한다.

이미 확인된 사실:
- Windows Dropbox reviewer task는 Disabled, 런처·자식 PID 0, 신규 모델 호출 0, 운영 DB 복사본 무결성 PASS(작업정의 실복원 SKIP); **ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER**. 재부팅/재로그인 이후 상태 유지와 24시간 무인 안정은 미검증.
- 갱신기/알림기/Bridge는 watcher 중지 시 변경하지 않았다. 갱신기는 Dropbox 상태를 게시하지만 요청 내용은 더 이상 새로 갱신되지 않는다. Notifier는 DB를 읽는 것으로 보이며 SHM 수정시각 변화 가능성이 있으나 원인 미확정. Bridge는 5분 스케줄을 정상 실행하는 것으로 보고.
- **GitHub 기반 CoWork PRIVATE 대시보드**는 별도의 GitHub Actions(`.github/workflows/cowork-dashboard.yml`, `collab/dashboard/`)이며 Windows Dropbox updater와 동일 프로세스가 아님. PUBLIC Pages 상태갱신은 별도 허용목록/Secret/승인 규칙으로 운용. 이 둘을 '같은 대시보드'로 합쳐서 종료 판단하지 말 것.
- GitHub SHADOW/C ETW는 PARTIAL이고 정식 리뷰 NOT_RUN. 별도 LIVE가 아직 없으므로 자동 리뷰 공급자는 NONE.

## 1. READ_ONLY 호스트 인벤토리
아래 세 구성요소 **각각**의 Windows 작업 스케줄러 설정, 실제 PID/커맨드라인, 실행 계정, 트리거·재시작 정책·부모/자식, 폴더/구성파일의 입력·출력 경로, 네트워크 호출 대상 종류(도메인/토큰 값 제외), 최근 처리 시간·실패/종료·처리량과 관련 작업/서비스를 조회한다:
A. **Dashboard updater**: Dropbox 운영 watcher DB·requests/reviews/receipts를 읽는지, Dropbox 정적 HTML 게시 목적만 있는지, 새 GitHub PRIVATE Action/Pages와 무관한지. 현재 새 데이터가 없는데도 계속 실행해 무엇을 쓰는지, 실패시 구형 대시보드 정체가 되는지.
B. **Telegram notifier**: watcher 상태 DB `-shm` 공유 index 및 `last_id`/커서를 실제 사용 중인지, Dropbox 리뷰 알림 **전용인지** 혹은 Job List/배포 Bridge/다른 자동화 알림과 **공유**하는지. 알림기 중지가 다른 서비스의 Telegram 메시지 누락을 만들지 확인. 종료 후 재기동 시 워터마크 소급 재발송/중복 위험.
C. **Bridge**: 5분 주기가 Windows 실행/Dispatcher/대시보드 배포 등 **다른 기능**에 꼭 필요한지, Dropbox reviewer watcher의 재시작 여부를 감시하는지, 감시기 Disable을 변경/해제할 가능성이 있는지. Heartbeat/대상 경로/Task Scheduler 설정을 현장 기준으로 확인.

특히 아래 사항 준수:
- **운영 DB 메인·WAL·SHM을 새 SQLite 연결(`mode=ro` 포함)로 열지 않는다.** Windows Task Scheduler/WMI/proc handler/실제 로컬 설정 및 비민감 기존 로그·코드 읽기만 사용. 필요하면 이미 승인된 별도 사본에서 조회하고 그 시점을 정확히 적는다.
- 토큰·키·Telegram chat ID·업무 기밀·개인 로컬 경로/프로세스 커맨드 내 secret의 원문을 출력/기록/게시하지 않는다. GitHub PRIVATE에도 반출 금지. 설정 값 열람 시 민감 문자열은 **처음부터 메모리 안에서 마스킹**.
- Windows 파일 핸들/프로세스 경로에서 운영 DB `-shm` 접촉 주체를 **읽기 전용**으로 추적하되, ETW/PID attribution 실패 이력이 있으므로 소유 PID/핸들 오픈과 SHM 파일 쓰기 causality를 구분. 확정할 수 없으면 `SHM_WRITER=UNKNOWN`.
- 기존 상태를 해치지 않는 관찰만 수행. **새 ScheduledTask/자동화/모니터링 작업 생성**, 서비스/작업 Stop/Disable/Enable, 운영 설정·DB·토큰/키 수정, 재부팅/로그오프/유료 reviewer 호출/Telegram 발송/모델 재시도 전부 금지.
- Dropbox reviewer Disabled 상태가 여전히 유지되고 자동 재시작 경로가 추가되지 않았는지 확인. 사전 확인과 종료 전 확인에서 다르면 `SINGLE_PROVIDER=UNKNOWN`으로 보고 원인만 조사, 자동 수정 금지.

## 2. 공용/전용 의존성 판정
각 구성요소를 다음 중 하나로 분류하고 코드·실제 설정·처리 로그 중 2가지 이상 교차 근거를 명시:
- `DROPBOX_REVIEW_ONLY`: watcher·Dropbox 전용 작업만 소비/게시, 다른 승인된 서비스 사용하지 않음. 사용 목적 종료라면 향후 별도 승인 후 **Stop + Disable 후보**.
- `SHARED_OTHER_WORK`: Telegram, Bridge, 별도 대시보드/Job List 등 다른 활성 기능과 공유. **유지** 또는 최소 분리 설계 필요.
- `INDEPENDENT_REQUIRED`: Dropbox와 무관하게 독립 필수 기능이 있음. **유지**.
- `UNKNOWN`: 증거 미확보. **변경 보류**, 필요한 정보/시험 지정.

관련 **의존성 그래프**를 Markdown Mermaid 또는 표 1개로 제공. 의존성이 없는 대상은 '없음 실측'과 '확인 못함'을 분리. 기존 Dropbox 감시기와 GitHub Actions/Pages는 **별도 배포 경로**로 표현.

## 3. 정리 제안과 향후 중지 승인 범위
- 이번에는 **정리 실행이 아닌 정리 판정**. 구성요소별 권장 `KEEP / RETIRE_CANDIDATE / BLOCKED_UNKNOWN`, Stop/Disable 시 데이터 유실·재전송/중복·Dashboard/Telegram/Bridge 서비스 중단 영향, 필요한 보존본 및 되돌리기 조건/관리자 권한을 제시.
- 먼저 **Dropbox 전용 Dashboard updater**를 후보로 검토하되, GitHub Pages가 Windows updater를 실제로 필요로 하지 않는지 확인할 것. Notifier가 여러 경로를 공유하면 함부로 중지하지 말 것. Bridge는 **다른 Dispatcher 작업의 연결 의존성** 확인 전 유지.
- SHM 파일 시각 변경이 updater/notifier의 DB 폴링 때문이라는 가설은 실측 근거가 없으면 확정 금지. 운영 데이터 수정 0을 주장하는 경우 반드시 증거 수준 명시.
- 중지 후보에게는 백업/rollback/서비스 연쇄효과/데이터 보존 및 중지 후 재기동 방지까지 구체적 체크리스트를 제시. **중지 명령은 실행하지 않음**.
- `C=PARTIAL` 기술 게이트는 유지하며, Dropbox watcher 중지 사실을 GitHub LIVE/독립 리뷰 PASS로 해석하지 않는다.

## 4. 결과 직접 게시 (사용자 원샷, PR 없음)
- 신규 결과 파일: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CLAUDE_POST_DROPBOX_DISABLE_DEPENDENCY_AUDIT_RESULT_FOR_GPT_20261113.md`.
- 필수 필드: `DASHBOARD_DEPENDENCY`, `DASHBOARD_RECOMMENDATION`, `NOTIFIER_DEPENDENCY`, `NOTIFIER_RECOMMENDATION`, `BRIDGE_DEPENDENCY`, `BRIDGE_RECOMMENDATION`, `SHM_WRITER_ATTRIBUTION`, `WATCHER_DISABLED_PERSISTENCE`, `ACTIVE_PROVIDER`, `MODEL_CALLS_NEW`, `HOST_CHANGES`, `ROLLBACK_PREREQS`, `GITHUB_DASHBOARD_INDEPENDENCE`, `CUTOVER`.
- 각 주장 증거 `HOST_REAL_READ_ONLY / HISTORICAL_REPORTED / NOT_VERIFIED` 표시. 민감경로/구성원·코드/자격증명/원본 로그/DB는 절대 게시 금지.
- 결과 `CURRENT.md`에 **최상단 새 절**로 추가, `TRACKER.json`은 계약 허용 `phase`, `self_test`, `independent_review`, `next_action` 값만 사용(phase 예: DISPOSITION, self_test=NOT_VERIFIED). 과거 이력 불변.
- PRIVATE main에 직접 게시(PR 불필요), **원격 UTF-8 원문·Git Blob SHA·commit readback** 확인. 결과 게시 실패면 `NOT_POSTED`로 남기며 운영 변경·자동 retry/reviewer 호출 금지.
- 이 문서 자체는 Dropbox watcher 재시작이나 Windows Claude Code 자동 실행을 유발하지 않는다. 사용자 Windows Claude Code 1회 실행 요청으로 수행.

최종 1행: `DEPENDENCY_AUDIT=PASS|PARTIAL|BLOCKED; DASHBOARD=KEEP|RETIRE_CANDIDATE|UNKNOWN; NOTIFIER=KEEP|RETIRE_CANDIDATE|UNKNOWN; BRIDGE=KEEP|RETIRE_CANDIDATE|UNKNOWN; ACTIVE_PROVIDER=NONE|UNKNOWN; HOST_CHANGES=0`.
