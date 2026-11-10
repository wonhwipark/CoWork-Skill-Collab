# CLAUDE 로그온 없는 시작 방식 호환성 점검 결과 (GPT 확인용) 2026-11-11

- 작업 ID: COWORK-DROPBOX-TO-GITHUB-MIGRATION
- 인계서: WINDOWS_NO_LOGON_START_COMPAT_HANDOFF_r0001_20261111.md (PRIVATE main에서 읽음)
- 범위: 읽기 전용 조사와 격리 시험만. 운영 감시기, 예약 작업, DB, Telegram, 인증 설정 변경 없음. 재부팅, 자동 로그인, 새 예약 작업 등록, 모델 호출 없음.
- 증거 수준: SELF_TEST_REPORTED. 정식 독립 리뷰가 아님. INDEPENDENT_REVIEW=NOT_RUN.
- 게시 내용에서 사용자명, 로컬 경로, 계정 식별자, 인증 값은 제거했다.

COMPAT_STATUS: PARTIAL
REAL_LOGONLESS_BOOT_E2E=NOT_RUN ; PRODUCTION_CHANGED=false ; MODEL_CALLS=0
사유: 작업 구조와 환경 의존성은 증거로 확인했다. 그러나 (1) Claude Code가 로그인 정보를 어디에 어떻게 저장하는지, (2) 이 계정의 로그인 비밀번호가 비어 있는지는 비밀 영역을 읽지 않고는 확인할 수 없어 UNKNOWN이다. 두 가지 모두 실제 선택(B 또는 C)을 좌우한다.

## 요약표
| ID | 항목 | 결과 | 증거 종류 |
|---|---|---|---|
| R01 | 현재 트리거·계정 컨텍스트 | PASS | REAL_READ_ONLY |
| R02 | 비대화형 컨텍스트와 Claude 인증 의존성 | PARTIAL | REAL_READ_ONLY + 문서화된 동작 (미실측) |
| R03 | 합성 XML·런처 환경 시험 | PASS | SYNTHETIC (Task Scheduler 실제 스키마 검증 + 샌드박스 9건) |
| R04 | 보안 분석 (자동 로그인, 비밀번호 저장, S4U) | 분석 완료 | 분석 (실측 아님) |
| R05 | 운영 무변경·호출 0 | PASS | REAL_READ_ONLY (전후 스냅샷) |
| R06 | 준비 상태와 승인·롤백·게이트 | 계획 제시 | 계획, 호스트 시험 NOT_RUN |

## R01 현재 상태 (PASS, REAL_READ_ONLY)
SKILL-COLLAB 예약 작업 4개를 읽기 전용으로 조회했다. 등록·수정·실행·중지는 하지 않았다.

| 작업 | 트리거 | 로그온 방식 | 실행 | 인스턴스 | 재시작 | 시간 제한 |
|---|---|---|---|---|---|---|
| 리뷰 감시기 | 사용자 로그온 | InteractiveToken | python.exe (콘솔), 작업 폴더 지정됨 | 새 인스턴스 무시 | 5분 간격 3회 | 없음 |
| 알림(Notifier) | 사용자 로그온 | InteractiveToken | pythonw.exe (콘솔 없음), 작업 폴더 지정됨 | 무시 | 5분 간격 3회 | 없음 |
| Dashboard Updater | 사용자 로그온 | InteractiveToken | python.exe | 무시 | 5분 간격 3회 | 없음 |
| Dashboard Bridge | 주기(시간) 트리거 | InteractiveToken | python.exe, 1회 실행 후 종료 | 무시 | 없음 | 4분 |

- 부팅 트리거는 없다. 4개 모두 대화형 토큰이며 권한 수준은 기본(최소 권한)이다. 서비스 계정 작업은 없다.
- 프로세스는 모두 세션 1(대화형 데스크톱)에서 실행 중이다.
- 따라서 **재부팅 후 그 사용자가 로그온하기 전에는 4개 모두 실행되지 않으며, 로그오프하면 중단된다.** Bridge와 Updater도 같은 제약이라 감시기만 바꾸면 대시보드가 먼저 멈춘다.
- 운영 notifier는 이미 pythonw(콘솔 없음)로 안정적으로 동작 중이다. 콘솔 없는 실행의 실제 선례다.

## R02 비대화형 컨텍스트와 Claude 인증 의존성 (PARTIAL)
관측한 사실 (값·이름·경로 비게시):
| 항목 | 관측 | 의미 |
|---|---|---|
| 계정 종류 | 로컬 계정, 사용 가능 | Microsoft 계정이 아니므로 '비밀번호 저장' 방식에서 Microsoft 계정 암호 특수성이 없다 |
| 로그인 비밀번호 | 암호 필수 설정이 꺼져 있고(PasswordRequired=False), 정책 'Accounts: Limit local account use of blank passwords to console logon only'이 켜져 있음. 암호가 비어 있는지는 **UNKNOWN** | 암호가 비어 있으면 B(저장 암호)와 C(S4U) 모두 시작이 거부될 수 있다. 확인하려면 로그인 시도가 필요해 하지 않음 |
| 관리자 여부 | 이 사용자는 로컬 관리자 그룹 소속이고, 현재 세션 토큰은 상승됨 | 등록 권한은 있으나, 상시 실행 계정은 비관리자 권장 (R04) |
| 자동 로그인 | 꺼져 있음 | 사용자 결정과 일치 |
| 빠른 시작(Fast Startup) | 꺼짐 | 부팅 트리거가 매 부팅에서 정상 의미를 가짐 |
| 절전·최대 절전 | 전원 연결·배터리 모두 '없음' | 무인 실행에 적합 |
| 저장된 네트워크 자격 증명 금지 정책 | 꺼짐 (허용) | 저장 암호 방식에서 네트워크 자격 사용 가능 |
| Claude CLI 위치 | 사용자 프로필 안(.exe), **사용자 PATH에만 있고 시스템 PATH에는 없음** | 사용자 환경이 로드되지 않거나 PATH가 다르면 못 찾음. 감시기 설정의 claude_executable은 null(PATH 의존) |
| Claude 로그인 | 로그인됨, 방식 claude.ai(구독), 제공자 firstParty | 환경 변수 방식(API 키, 토큰)은 모두 미설정 → 프로필에 저장된 로그인 사용 중 |
| 환경 변수 | USERPROFILE, APPDATA, LOCALAPPDATA, TEMP 설정됨. HOME, CLAUDE_CONFIG_DIR 미설정 | CLI는 프로필의 기본 위치를 사용 |

`claude auth status` 호출은 단 1회, 모델 호출 없이 수행했다. 출력에서 계정 정보는 사용하지 않았다.

방식별 인증 의존성 (문서화된 동작이며 이 점검에서 실측하지 않음):
- A(로그온 시): 사용자 프로필과 DPAPI 비밀에 모두 접근 가능. 현재 동작 중.
- B(저장 암호): 사용자 프로필 로드, 사용자 암호 기반 DPAPI 키 사용 가능, 네트워크 자격 사용 가능.
- C(S4U): 사용자 프로필은 로드되지만 암호 자격이 없어 **암호화된 파일(EFS), DPAPI 보호 데이터, Credential Manager, 네트워크 자격에는 접근할 수 없다**.
따라서 Claude Code 로그인이 프로필의 일반 파일에 있으면 C도 동작하고, DPAPI나 Credential Manager에 있으면 C는 CLAUDE_NOT_LOGGED_IN으로 실패한다. 어느 쪽인지는 **UNKNOWN**이다(확인하려면 보호된 프로필 데이터를 읽어야 하므로 하지 않음). 이 프로젝트의 다른 비밀(Dropbox, GitHub 토큰, Telegram)은 일반 파일에 있어 C에서도 읽힌다는 점은 설계상 확인되나 실측은 아니다.
좋은 점: v0.2.5의 로그인 사전 점검이 이 실패를 **요청을 소모하지 않는 대기 + 알림**으로 바꾼다. 따라서 실제 호스트 시험은 모델 호출 없이 안전하게 할 수 있다.

## R03 합성 시험 (PASS, SYNTHETIC)
### XML 구조 (Windows Task Scheduler의 실제 파서, 메모리에서만 검증, 등록 없음)
| 시험 | 결과 |
|---|---|
| A 로그온 트리거 + 대화형 토큰 | 수락 |
| B 부팅 트리거(지연 1분) + 저장 암호 | 수락 (LogonType=Password) |
| C 부팅 트리거(지연 1분) + S4U | 수락 (LogonType=S4U) |
| 알 수 없는 로그온 방식 / 잘못된 지연 형식 / 빈 동작 / S4U+그룹 주체 / 깨진 XML | 5건 모두 거부 |
| 등록 여부 | 시험 전후 SKILL-COLLAB 작업 4개, 전체 작업 312개 그대로 (등록 0) |
의미 한계: 파서가 받아들이는 것은 구조일 뿐이다. 로그온 권리(batch logon right), 암호 일치, S4U의 접근 제약 같은 의미 검사는 실제 등록 때만 일어나므로 **NOT_RUN**이다.

### 비대화형 환경 (합성 샌드박스 9건 모두 PASS, 운영 폴더 미사용)
| 시험 | 관측 |
|---|---|
| T1 작업 환경(프로필 변수 있음, PATH에 사용자 경로 없음, 작업 폴더 지정) | 정상 실행 |
| T2 작업 폴더 미지정(작업의 기본값) | `No module named` 로 실패. **WorkingDirectory는 필수** (감시기는 패키지로 설치되어 있지 않고 작업 폴더에서 모듈을 찾음) |
| T3 LOCALAPPDATA 없음, 프로필 변수 있음 | 프로필 아래 기본 위치로 대체되어 정상 |
| T4 프로필이 로드되지 않음(USERPROFILE·LOCALAPPDATA 없음) | 홈 디렉터리를 결정하지 못해 **실패(fail-closed)**, 어디에도 쓰지 않음 |
| T5 pythonw(콘솔 없음, 표준 출력 없음) | 정상 |
| T6 pythonw watch, 자격 증명 없음 | 종료 코드 4(AUTH_REQUIRED), WATCH_START·AUTH_REQUIRED·WATCH_END 감사 기록 |
| T7 python.exe 콘솔 창 없음 | 동일 결과, 출력 수집 가능 |
| T8 사용자 PATH에만 있는 claude, 작업 PATH에는 없음 | 사전 점검이 CLAUDE_CLI_NOT_FOUND 반환 → 요청 소모 없이 대기 |
| T9 claude_executable을 절대 경로로 지정(합성 스텁, 실제 CLI 아님) | PATH 의존성 제거, 정상 |
또한 패키지의 단일 실행 잠금(msvcrt)은 세션과 무관하게 동작하며 두 번째 프로세스를 거부한다(기존 시험으로 확인). 구버전 로그온 작업과 신규 부팅 작업이 동시에 있어도 한 쪽만 실행된다.
`windows/run_watch.cmd`는 수동용(pause 포함)이라 작업 동작으로 쓰면 안 된다. 운영 작업처럼 python.exe를 직접 지정해야 한다.

## R04 보안 분석
### 자동 로그인을 권장하지 않는 이유
비밀번호가 레지스트리나 LSA 비밀에 평문에 가깝게 저장되고, 부팅하면 잠금 없는 데스크톱이 열려 물리 접근자가 Claude 로그인, Dropbox, GitHub 도구 등 사용자 세션 전체를 얻는다. 화면 잠금이 무력화되고 재시작 후 항상 같은 계정이 열린다. 사용자의 선택(권장하지 않음)과 일치한다.

### 방식 비교
| 항목 | A 로그온 시 (현재) | B 부팅 + 저장 암호 | C 부팅 + S4U |
|---|---|---|---|
| 재부팅 후 로그온 없이 시작 | 불가 | 가능 | 가능 |
| 로그오프 후 계속 실행 | 아니오 | 예 | 예 |
| 암호 저장 | 없음 | Windows가 LSA 비밀로 저장 | 없음 |
| 암호 변경 시 | 영향 없음 | 작업이 실패, 재등록 필요 | 영향 없음 |
| 물리 접근·관리자 권한 위험 | 낮음 | 로컬 관리자가 저장 암호를 추출할 수 있음 (BitLocker 상태는 이 점검에서 미확인) | 저장할 암호 자체가 없음 |
| Claude 로그인 접근 | 가능 | 가능 | 로그인 저장 위치에 따라 불가능할 수 있음 (UNKNOWN) |
| 네트워크 자격 사용 | 가능 | 가능 | 불가 (HTTPS 호출은 별도 자격 없이 가능) |
| 세션 | 1 (대화형) | 0 (비대화형) | 0 (비대화형) |
| 필요한 권리 | 없음 | '배치 작업으로 로그온' 권리 | 동일 |
| 적합성 | 현재 요구(로그온 없이 시작)를 충족하지 못함 | 충족, 암호 관리 부담 | 충족, 인증 호환 검증이 관건 |

### 최소 권한·자격 증명 보관 권고
1. 상시 실행 계정은 **비관리자 전용 로컬 계정**(예: 리뷰 실행 전용)을 권장한다. 현재 사용자는 관리자다. 이 경우 Claude 로그인, 비밀 파일, 설정 파일을 그 계정 프로필에 별도로 구성해야 하므로 사용자 작업이 늘고, 이 구성은 이번 범위에서 하지 않았다.
2. 비밀 파일(Dropbox, GitHub 토큰, 신뢰 루트, notifier)은 실행 계정만 읽고 쓰게 ACL을 제한한다. v0.2.4의 파일 권한 점검(광범위 그룹 쓰기 금지)을 같은 방식으로 적용할 수 있다.
3. 어느 방식이든 `claude_executable`을 절대 경로로 설정한다 (T8·T9).
4. S4U를 먼저 시도하고, Claude 로그인 접근이 실패하면 B로 가되 전용 비관리자 계정을 쓴다.

## R05 안전성 (PASS, REAL_READ_ONLY 전후 스냅샷)
점검 전후를 비교한 결과 **작업 4개의 정의 해시, 상태, 프로세스 목록, 감시기 버전(0.1.5), 설정 파일 해시, 운영 스크립트 해시, DB 테이블 6개, 작업 상태(COMPLETED 60 / CONFLICT 1), 리뷰 디스패치 수(61), 모델 호출 카운터(61)가 모두 동일**했다. 유일한 차이는 Bridge 작업의 마지막 실행 시각이 자체 5분 주기로 5분 앞선 것이다(정의 해시는 동일).
- 운영 폴더에 새 파일·SHADOW 폴더 없음. 점검은 DB를 읽기 전용(mode=ro)으로만 열었다.
- 작업 등록 0 (메모리 검증만 사용), 실행·중지 0, 재부팅 0, 자동 로그인 변경 0, 인증 변경 0.
- 모델 호출 0, Telegram 0, GitHub 원격 쓰기는 이 결과 문서와 CURRENT 갱신뿐.
- 롤백 자료: 현재 작업 4개의 정의를 PC 로컬에만 내보냈고(게시하지 않음, 경로·계정 포함), 메모리에서 다시 가져올 수 있고 텍스트가 동일함을 확인했다.

## R06 실제 호스트 시험 준비 (실제 호스트 시험은 NOT_RUN)
### 필요한 사용자 승인 (한 번에 묶음)
1. 시험 방식 선택: **C(S4U)를 먼저**, 실패 시 B(전용 비관리자 계정). 자동 로그인은 사용하지 않음.
2. 이 계정의 로그인 비밀번호 상태 확인과, 필요하면 설정(사용자 작업).
3. v0.2.5 후보를 별도 폴더에 설치하고 설정에서 `claude_executable`을 절대 경로로 지정, 일일 상한값 설정.
4. 새 작업을 **사용 안 함 상태로 등록**한 뒤 기존 로그온 작업을 비활성화하고 새 작업을 활성화, 재부팅 1회.
5. 무인 구성에 필요한 알림 연결(notifier 갱신).

### 롤백
- 기존 4개 작업의 정의가 로컬에 보존되어 있고 다시 가져오기가 가능함을 확인했다. 새 작업을 비활성화하고 기존 로그온 작업을 다시 활성화하면 이전 상태로 돌아간다.
- DB는 건드리지 않는다(감시기 설치만 바뀜). 필요하면 이전에 만든 온라인 백업 사본으로 복원한다.

### 단일 LIVE·단일 실행 게이트
- 한 번에 하나의 시작 방식만 활성화한다. 새 작업과 기존 작업이 동시에 켜져도 감시기의 단일 실행 잠금이 두 번째를 거부한다(종료 코드 3).
- 제공자 LIVE는 여전히 Dropbox 하나다. GitHub LIVE는 별도 승인이며, 이 시험에서 활성화하지 않는다.
- 시험 중 모델 호출 0을 유지한다: 대기 중인 요청이 없으면 사전 점검조차 실행되지 않는다. 인증 호환만 보려면 아래 프로브를 쓴다.

### 모델 호출 없는 호스트 시험 순서 (승인 후)
1. (선택, 코드 변경 필요) 로그인 사전 점검만 실행해 결과 사유 코드를 한 줄 출력하는 `preflight` 명령을 추가한다. 현재 패키지에는 없다. 그 전에는 같은 효과를 내는 일회용 점검 작업을 쓴다.
2. 새 작업의 로그온 방식으로 `claude auth status`를 한 번 실행하게 하고 결과(loggedIn 여부)만 기록한다.
3. 통과하면 감시기를 같은 방식으로 실행하고, 재부팅 후 로그온하지 않은 채 SCAN_START가 쌓이는지 확인한다(데드맨 감지에도 사용).
4. 실패하면 사유 코드로 원인을 구분한다: CLAUDE_CLI_NOT_FOUND(경로), CLAUDE_NOT_LOGGED_IN(인증 저장소), 홈 디렉터리 오류(프로필 미로드).

### 합성 XML 참고 (C, 자리표시자만 사용)
```xml
<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <Triggers><BootTrigger><Enabled>true</Enabled><Delay>PT1M</Delay></BootTrigger></Triggers>
  <Principals><Principal id="Author"><UserId>HOST\RUNNER</UserId><LogonType>S4U</LogonType><RunLevel>LeastPrivilege</RunLevel></Principal></Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries><StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <StartWhenAvailable>true</StartWhenAvailable><RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit><Hidden>true</Hidden>
    <RestartOnFailure><Interval>PT5M</Interval><Count>10</Count></RestartOnFailure>
  </Settings>
  <Actions Context="Author"><Exec><Command>INSTALL\.venv\Scripts\python.exe</Command>
    <Arguments>-m skill_collab_watcher.cli --config INSTALL\config\reviewer.config.json watch --longpoll</Arguments>
    <WorkingDirectory>INSTALL</WorkingDirectory></Exec></Actions>
</Task>
```
B는 LogonType을 Password로 바꾸고 등록 시 암호를 입력하는 점만 다르다. 부팅 직후 네트워크가 아직 준비되지 않아도 감시기는 전송 오류로 처리하고 재시도한다(기존 감시 루프 시험으로만 확인, 부팅 E2E는 NOT_RUN).

## 미검증 (NOT_RUN)
- REAL_LOGONLESS_BOOT_E2E: 실제 부팅·로그온 없는 실행
- 실제 작업 등록 시의 의미 검사(배치 로그온 권리, 암호 일치, S4U 제약)
- Claude Code 로그인 저장 위치와 S4U에서의 접근 가능 여부
- 이 계정의 로그인 비밀번호가 비어 있는지 여부
- 디스크 암호화(BitLocker) 상태와 저장 암호 추출 위험의 실측
- 전용 비관리자 계정으로의 구성
- Bridge·Updater·Notifier를 같은 방식으로 전환했을 때의 동작

COMPAT_STATUS: PARTIAL ; R01: PASS(REAL_READ_ONLY) ; R02: PARTIAL(REAL_READ_ONLY) ; R03: PASS(SYNTHETIC) ; R04: ANALYSIS ; R05: PASS(REAL_READ_ONLY) ; R06: PLAN(NOT_RUN on host) ; REAL_LOGONLESS_BOOT_E2E: NOT_RUN ; PRODUCTION_CHANGED: false ; MODEL_CALLS: 0 ; scheduled_tasks_registered: 0 ; independent_review: NOT_RUN ; next_approval: C(S4U) 호스트 시험 + 로그인 비밀번호 확인 + claude_executable 절대 경로 + 후보 설치 (한 번에)
