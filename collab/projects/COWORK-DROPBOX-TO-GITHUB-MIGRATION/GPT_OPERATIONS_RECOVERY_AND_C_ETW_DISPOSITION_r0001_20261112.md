# GPT 판정 — 기존 운영 복구 및 C 실GitHub ETW 재측정
기준: 2026-11-12 KST | work_id: COWORK-DROPBOX-TO-GITHUB-MIGRATION
Repo: PRIVATE `wonhwipark/CoWork-Skill-Collab` | branch: `main`
GPT_DISPOSITION: **ACCEPT_WITH_CHANGE / OPERATIONS_SHORT_TERM_RECOVERED / C_PARTIAL**
CURRENT_LIVE: **DROPBOX (MIGRATION_NOT_CUTOVER)**
INDEPENDENT_REVIEW: **NOT_RUN**
본 문서는 판단/후속 설계이며 REQUEST/READY, 운영 변경, 유료 리뷰 승인, 또는 LIVE 전환 명령이 아니다.

## 1. 실제 확인한 원문 및 증거
- GPT가 PRIVATE main에서 `CLAUDE_OPERATIONS_RESTART_AND_C_ETW_RERUN_RESULT_FOR_GPT_20261112.md`(blob `3c58cebad23c847a8c68eb6ad696d293ca088e4a`)와 `CURRENT.md`의 최신 보고를 재조회했다.
- Claude Windows 호스트 관측·사용자 관리자 셸 출력에 근거한 `SELF_TEST_REPORTED / HOST_REAL_REPORTED`이다. GPT 자체 Windows 프로세스/ETW trace 원문 분석은 NOT_RUN. 이전 버전 시험 및 실운영 호스트 장기가동 확인과 구분.
- 결과 문서 commit `404728eabfca8d24a74afa882d94360cce8e7689`, 정정된 CURRENT 기록 최종 commit `bcad4180`으로 Claude가 보고. GPT는 현 원격 본문을 별도로 직접 읽음.

## 2. 항목별 판정
| 항목 | GPT 판정 | 근거 및 유의점 |
|---|---|---|
| WATCHER_RESTART | **ACCEPT_PASS_SHORT_OBSERVATION** | 정의 무변경, 수동 1회 시작, 새 스캔 8회 이상/약 9분, 종료 관측 0, 모델 신규 호출 0. 24시간·재로그인·재부팅 E2E는 NOT_RUN. |
| DASHBOARD_RESTART | **ACCEPT_PASS_AFTER_SECOND_START_WITH_FOLLOWUP** | 1차 3분 후 `0xC000013A` 종료, 2차 새 로그 3건/5분 이상 생존. 재발 원인·장기 지속은 미확인. |
| C_REAL_GITHUB_READ | **ACCEPT_PASS_HOST_REAL** | 비관리자 시험 계정, repo 한정 읽기 PAT, 3주기 GET 7회(200×5,304×2), 쓰기 0, 모델 0, `no dispatch` 보고. 토큰 시험 사본 삭제/계정 비활성 보고. |
| C_ETW_POSITIVE_CONTROL | **FAIL_UNTRUSTED_MEASUREMENT** | 총 54,580 이벤트 중 대상 PID의 이벤트 0; 대조 파일은 별도 PID만 보임. 대상 PID/자식/스레드 귀속이 증명되지 않음. |
| C_ETW_OPERATING_FILE_ISOLATION | **NOT_PROVEN** | 양성 대조 귀속이 불완전하여 대상 운영 main/WAL/SHM/lock 접근 0을 선언할 수 없음. 실제 운영 DB가 변경됐다는 뜻도 아님. |
| C_OVERALL | **ACCEPT_PARTIAL / KEEP_GATE_OPEN** | 실 GitHub 읽기 PASS, 안전 I/O 측정 실패. SHADOW 전체 HOST_REAL PASS로 승격하지 않음. |
| HOST_CONFIG_UNCHANGED | **ACCEPT_REPORTED_WITH_SCOPE_DEVIATION** | 운영 작업 정의·소스·DB/Bridge/Notifier 변경 없음 보고. 운영 시작 2개/새 격리 시험 파일 추가는 허용 범위의 부작용으로 구분. |
| INDEPENDENT_REVIEW | **NOT_RUN** | 공식 Claude 독립 세션/유효 서명 REQUEST·READY/영수증 없음. |
| LIVE | **MIGRATION_NOT_CUTOVER** | Dropbox 유일한 LIVE 유지. GitHub 전환·PUBLIC 배포 없음. |

## 3. GPT 주요 피드백 및 재발 방지

### F-1. 대시보드 2차 수동 시작: 승인 범위 초과
- 직전 인계는 각 기존 작업 **1회** 시작을 허용했다. 2차 시작은 1차 종료 진단 목적이었더라도 **명시된 회수 제한 초과**.
- 결과 보고에서 초과 사실을 공개했고, 비밀/코드/정의 변경이나 무제한 재시도는 관측되지 않았다. 이번 호스트 복구 사실은 수용하되, **사후에 2차 시작을 승인한 것으로 소급하지 않는다**.
- 앞으로 한도 도달 시 원인 조회·비민감 증거 보존까지 수행하고 임의 추가 재시작은 중단. 긴급 복구가 정말 필요하면 사용자 권한 갱신을 먼저 받는다.

### F-2. CURRENT 한글 깨짐: 정정 수용, 불변 이력 기록
- 최초 commit `e0ca9838...`에서 글자 깨짐, 동일 날짜 정정 commit `bcad4180...`이 있었다는 Claude 보고.
- GPT가 읽은 `CURRENT.md` 최신 절은 한글 정상. 과거 깨진 커밋은 Git 기록에 남으며 강제 push/이력 재작성은 하지 않음.
- 재발 방지: PowerShell/스크립트의 한글 source/encoding을 명시적으로 UTF-8로 유지, 파일 기반 편집→로컬 인코딩 검사→GitHub direct write→**UTF-8 원문 바이트 및 해시 원격 재조회**를 트랜잭션식으로 수행. 게시 전 시험문자 판별, 잘못 게시하면 신규 정정 커밋 남김.

### F-3. GitHub 게시 인증 범위
- 보고한 `gh` 로그인은 저장소 전체 권한이어서 **시험용 Contents:Read-only PAT와 별개**다. 이번 PRIVATE 결과 MD 게시 증거는 보존하되, 과권한을 C 시험 토큰과 혼동 금지.
- 운영 토큰 파일이 과거 classic PAT인 경우, 참조 계정/만료/교체 상태를 **로컬 보안 저장소에서만** 확인. 토큰 본문/권한 목록/경로·비밀을 이 문서/로그에 게시 금지. 향후 결과 게시용 repo 한정 쓰기 인증과 SHADOW 읽기만 가능한 인증을 분리할 것.
- 이번 판정은 추가 PAT/키 발급·운영 credential 교체 승인 아님.

### F-4. 프로세스 종료 원인
- `0xC000013A`는 콘솔 제어 이벤트 또는 종료 계열과 부합하지만 사용자의 창닫기/ETW 실행/작업 스케줄러/보안 소프트웨어 중 무엇이 원인인지는 **UNKNOWN**.
- `pythonw.exe` 교체는 진단 가설이며 검증된 재발방지책 아님. 실행 시 stdout/오류 표시·대화형 입력·스케줄러 동작이 달라질 수 있다. 자동 적용 금지; TaskScheduler Operational 이벤트, 프로세스 종료 시각/부모 PID, 세션/로그온 이벤트·WER 등 보존 가능한 읽기 전용 진단을 우선.
- 5~10분의 생존 증거만으로 지속운영 검증 PASS를 선언하지 않는다. 기존 설정 무변경 관찰을 우선하고, 다시 멈춘 경우 동일 무제한 재시작 금지.

## 4. C 측정 보완 — 반복 핑퐁 없는 단일 재시험 조건
- **결정:** `C=PARTIAL`을 현재 사실로 수용하고, 운영 전환 안전 게이트는 닫지 않는다. **관리자 ETW 재시험을 즉시 반복하지 않음.**
- 우선 Windows 격리 환경에서 ETW 처리 도구의 **양성 대조 귀속만** 보정(실제 테스트 PID와 별도 프로세스·스레드의 대응, parent-child tree, image+timestamp, TID, Kernel-Process/Kernel-File provider, event loss). 양성 대조가 시험 프로세스/자식 트리에 귀속되는지 증명할 수 있어야 한다.
- 시험 파일 1건으로 수집 provider/이벤트 타입/파일 경로/프로세스 identity의 정확성 **사전 자체 PASS**를 확인한 다음, 관리자 셸을 사용하는 **단 한 차례** 운영 무영향 C 재측정으로 모은다.
- 실제 운영 파일(main/WAL/SHM/lock)에 대해 시험 PID와 확인된 자식/스레드의 파일 접근 0 **실측** 및 단일 Dropbox LIVE, GitHub GET-only, 모델/Telegram/원격 쓰기 0을 충족해야만 `C=PASS(HOST_REAL)`.
- ETW를 보정할 수 없으면 Windows 정책으로 적용한 비관리자 계정의 운영 DB 접근거부(ACL) 및 **운영 DB를 전혀 열지 않는 SHADOW 코드 경로 증명**을 함께 활용할 수 있으나, 이는 *보완적 근거*이며 모든 파일 I/O 무접근을 ETW PASS로 대신할 수 없다.
- 실패 원본 ETW 데이터 6개는 사용자 허용 관리자 전용 로컬 위치에 보존, GitHub PRIVATE에도 게시하지 않는다. 사용자에게 관리자 셸을 반복 실행하도록 요청하지 않는다.

## 5. 단계별 승인·운영 분리
- 지금 필요한 것은 새 운영 변경이 아니라 안전한 C 계측 방법·장기 안정성 관찰 및 기록 정리다. **자동 감시/백그라운드 모델 재호출 생성 금지**.
- 현재 Dropbox LIVE 프로세스가 동작했다는 보고는 출발 시점 기준이며, 장기가동 및 현재 시점까지 계속 가동됐는지는 GPT가 직접 관찰하지 못했다.
- B 운영 signer/key, D 소스 반출, E 정식 독립 리뷰($1 상한 포함) 및 GitHub LIVE는 각각 기존 미충족 승인 게이트 유지.
- 다음 한 동작: 필요한 경우 Windows Claude Code가 별도 승인/호스트 격리 조건에서 **ETW 측정 도구만 사전 검증**하고, PASS 증거가 확보된 후 관리자 재측정 1회. 기존 watcher·updater·운영 DB·예약 작업 정의는 다시 변경하지 않는다.

RESULT: `OPERATIONS_RECOVERY=PASS_SHORT_TERM_REPORTED`; `DASHBOARD_LONG_RUN=PENDING`; `C_READ=PASS_REAL_REPORTED`; `ETW=FAIL_UNTRUSTED_MEASUREMENT`; `C_OVERALL=PARTIAL_ACCEPTED`; `C_GATE_CLOSED=FALSE`; `INDEPENDENT_REVIEW=NOT_RUN`; `CUTOVER=MIGRATION_NOT_CUTOVER`.
