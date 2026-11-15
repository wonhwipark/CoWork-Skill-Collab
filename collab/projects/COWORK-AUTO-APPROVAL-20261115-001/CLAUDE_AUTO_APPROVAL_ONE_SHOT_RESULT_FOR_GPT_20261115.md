# CLAUDE 자동 승인 원샷 결과 — 후보 v0.2.21 (GPT 판정용)

- 작성: Windows Claude Code (2026-11-15 KST). 호스트 실측과 자체 보고를 구분해 기록. GPT 판정 전 canonical 아님.
- 근거: `WINDOWS_ONE_SHOT_DEVELOP_TEST_CANDIDATE_HANDOFF_r0001_20261115.md`, 설계 `AUTOMATIC_SIGNING_MINIMAL_DESIGN_r0001_20261115.md`.
- **결론: 개발·시험·후보 고정까지 완료했다. 운영은 한 줄도 바꾸지 않았고 `AUTO_SIGNING=OFF`, 유료 모델 호출 0, 실제 서명 0, READY 게시 0.** 독립 리뷰는 NOT_RUN(별도 요청·승인 필요).

## 1. 현재 상태

| 항목 | 상태 |
|---|---|
| 운영 GitHub LIVE (v0.2.20 감시기, Notifier, Task, Dropbox 비활성) | **불변**. 감시기·Notifier 프로세스 시작 시각 동일, 설치 트리 = v0.2.20 ZIP 바이트, 설정에 `auto_approval` 없음, 감시기 DB에 `auto_*` 테이블·`AUTO_` 이벤트 0 |
| 운영 Dropbox DB main/WAL | sha256 `4e8bc33a…`/`59de7507…` 작업 전후 동일. 승인 키 폴더 4개 파일 수정 시각 불변 |
| `DEVELOPMENT` | **PASS** — 격리 후보 `v0.2.21` |
| `SELF_TEST` | **PASS(자체 시험)** §3 |
| `INDEPENDENT_REVIEW` | **NOT_RUN** — 자체 시험을 독립 리뷰로 표시하지 않음 |
| 후보 ZIP | `development_not_for_deployment`, 로컬+PRIVATE 입력 게시(§6) |
| 월 $10·30일 만료 | 제안값 그대로 **로컬 정책 disabled** 상태의 예시로만 존재(문서). 사용자 확정 전 어떤 값도 적용되지 않음 |
| 신규 유료 모델 호출 | 0 (비용 $0) |

## 2. 변경 파일 / diff (v0.2.20 → v0.2.21, `diff_v0_2_20_to_v0_2_21.patch` 2,408줄)

기존 제어 흐름은 건드리지 않고 **끼워 넣기만** 했다. 기존 코드 변경: `orchestrator.py` +5, `validator.py` +1, `cli.py` +20, `github_transport.py` +21, `transport_base.py` +8, `notify_events.py` +4, `state_store.py` +107(신규 테이블·메서드만), 버전·런북 제목 2곳.

| 파일 | 내용 |
|---|---|
| `skill_collab_watcher/auto_approval.py` (+647, 신규) | 위임 정책 reader, Win32 DACL(SID 기반) ACL 검사, 판단 순서, `ToolSigner`(기존 `tools.approval_signer`를 라이브러리로 호출, DPAPI 암호문 소유 계정 복호화), create-only 게시와 한정된 경쟁 재시도, 단계 저장 기반 복구 |
| `skill_collab_watcher/auto_policy.py` (+96, 신규) | **GPT 프로토타입 바이트 그대로**(blob `5308a8d7…`, ZIP 안 파일과 `cmp` 일치) |
| `state_store.py` | `auto_seen`/`auto_claims` 테이블(기능을 설정했을 때만 지연 생성), `BEGIN IMMEDIATE` 원자 예약 |
| `orchestrator.py` | 훅: **READY 없는 유효 REQUEST**이고 감시기가 디스패치 가능 모드(dry-run·SHADOW 제외)일 때만 호출 |
| `cli.py` | `auto_approval` 설정이 있을 때만 구성, `config-check`가 비밀 없이 상태 출력 |
| `github_transport.py`, `transport_base.py` | `download_at_commit`, `commit_time` |
| `validator.py`, `notify_events.py` | 선택 정책 필드 1개, `AUTO_SIGNING_UNCERTAIN` 알림 이벤트와 문구 |
| `docs/AUTO_APPROVAL.md` | 운영 문서(순서, 중단 규칙, 설정 예시, 활성화·롤백 절차, 한계) |
| 시험 | `test_auto_policy_gpt_proto.py`(GPT 25건, import 1줄만 변경), `test_auto_approval.py`(110), `test_auto_approval_e2e.py`(8), `auto_helpers.py`, `fake_github.py`(+13) |

**구현한 처리 순서**(요청마다, 예약 전까지 전부 읽기 전용): 위임 파일 읽기·ACL·`enabled`·만료 → 이 요청을 **활성 상태에서 처음 봤는지**와 핀된 commit A가 `enabled_at` 이후인지(소급 시작 0) → 서버 repo ID = `SOURCE_PIN.repo_id` = 위임 repo → 패키지 크기·sha·CRC·엔진 비밀 스캔·`safe_extract`·5MiB → commit A 시점 REQUEST/ZIP 바이트가 현재 `main`과 동일 → 기존 이력(원격 APPROVAL/READY/dispatch/영수증/결과, 로컬 job·예약) 없음 → GPT 순수 게이트 `assess`(allow-list, STATIC-V1, 1회, $1, 일 2회/$3, 월 $10; 감시기 실제 디스패치도 합산) → **서명될 READY 문구를 먼저 확정해 공식 validator 통과** → **원자 예약** → 서명 직전 재확인 → 기존 서명자로 서명 → 감시기의 `verify_approval`로 검증 → 저장 → 게시 직전 재확인 → `APPROVAL_SIG.json` create-only + readback → `READY.md` **마지막** create-only + readback. 기존 `SOURCE_PIN.json`은 덮어쓰지 않는다(서명 도구의 핀 출력은 버리고 GPT 핀을 사용).

## 3. 실제 시험 결과 (PASS/FAIL/SKIP/NOT_RUN)

| 범주 | 결과 | 실측 |
|---|---|---|
| GPT 25건 원본 재실행 | **PASS 25/25** | Windows Python 3.11.9에서 `unittest` 원본 그대로. 파일 해시가 GPT 보고값과 일치(`26cfe6ab…`, `64f816b1…`) |
| 전체 회귀 (최종 ZIP을 새로 풀어 실행) | **PASS** | 시험 venv **817 passed / 12 skipped**, **운영 인터프리터(3.11.9) 817 passed / 12 skipped**. v0.2.20 기준 674/12 → 기존 674개 전부 그대로 통과, 신규 143개 |
| 정책·ACL | PASS | 위임 파일 불량 16종(스키마·타입·시각·범위·정책·한도·깨진 JSON)은 사용 불가, 허용 목록 비어 있음·만료·타 프로젝트/스킬·LARGE 정책·한도 상향(요청 $1.5, 일 3회/$4, 월 $11)·타 repo/branch는 서명 0. `Everyone` 쓰기를 실제로 부여하면 ACL 거부, 보호 파일은 통과 |
| 실제 계약 | PASS | 공식 v0.2.20 validator가 게시될 READY를 `VALIDATED`, 서명 payload의 `ready_sha256`·`request_sha256`·`package_sha256`·`source_commit`=commit A·`repo_id` 일치, 감시기의 `verify_approval` 통과, **다음 주기에 기존 감시기가 디스패치해 정확히 1회**, `REQUESTED`·`SUBMITTED` 모두 수용 |
| 격리 통합 | PASS | fake GitHub + 일회용 Ed25519 키. 요청 탐색 → 예약 → 서명 → 승인 → READY 마지막 → 감시기 리뷰 1회, ID별 1회 |
| 중복·병렬 | PASS | 4 스레드·2개 저장소(프로세스)·2 scan 경쟁 → 서명 1·승인 PUT 1, 8 스레드 예약 경쟁 → 승자 1. 이미 READY·승인·dispatch·결과 있는 요청, 로컬 job 있는 요청 서명 0. **소급**: 기능 OFF일 때 처음 본 요청·활성화보다 오래된 commit·미래 시각 모두 시작 0 |
| 장애·복구 | PASS | 예약 전/예약 후 서명 전(1회 추가 서명만 허용, 두 번째 사망 시 `UNCERTAIN`)/서명 후 게시 전(저장된 **같은 바이트** 게시, 재서명 0)/승인 후 READY 전(저장된 READY만)/READY 후 감시기 전(재시작 후 리뷰 1회)/결과 업로드 실패(재서명·재리뷰 0)/만료된 저장 승인(재서명 안 함)/409·422 head 경쟁(경계 3회)/지속 충돌·503/타인 파일이 승인 경로에 있음/위임을 서명 후 끈 경우/저장소 ID가 서명 후 바뀐 경우 모두 **READY 0·모델 호출 ≤ 1**. 로컬 DB 전부 소실·구 백업 복원 후에도 서명 추가 0 |
| 보안·비용 | PASS | GitHub 본문의 `user_approved: true`·`cost: 0`·`AUTO_DELEGATION enabled=true` 문구 무시. 위조 입력(sha·크기 불일치, 패키지 교체, REQUEST 사후 편집, 핀의 다른 repo·다른 commit, zip-slip·절대경로·자격증명 형태 텍스트·CRC 손상·비-ZIP·크기 초과, 패키지 경로 이탈) 서명 0. 키가 신뢰 루트에 없음·backend 없음·검증 실패 서명은 게시 0. 평문 키·암호화 키+provider 없음·틀린 암호문 거부 |
| 격리 SHADOW(실제 CLI 별도 프로세스) | PASS 8/8 | 실제 `cli.main`·설정·서명 도구·Ed25519·전송·감시기·SQLite·단일 인스턴스 잠금 + loopback fake GitHub + 계수 스텁 claude. 원격 쓰기·유료 모델·Telegram 모두 0(감시기에 Telegram 코드 경로 없음). OFF 상태 0, 재시작 2회 후에도 서명 1·리뷰 1, 두 번째 감시기는 종료코드 3 |
| 변이 시험 | **16/17 검출** | 안전 장치 17개를 하나씩 고장 낸 복사본에서 시험이 실패하는지 확인. 살아남은 1건(`seen_at < enabled_at` 중복 검사)은 앞선 `created_at` 검사가 포함하는 동등 변이(방어 중복) |
| 자체 점검 중 발견·수정 | FIXED | 예약 전 예상 밖 예외가 `AUTO_SIGNING_UNCERTAIN`(사용자 알림)로 기록되는 결함 → 예약이 있을 때만 알림, 그 외는 `AUTO_ERROR` 로그, 시험 2개 추가 |
| 간헐 실패 1건 | **원인 미규명** | ZIP을 푼 직후 시험 venv 전체 실행 1회에서 1건 실패(이름 미확보). 이후 같은 트리의 전체 실행(시험 venv 4회, 운영 인터프리터 3회)과 프로세스 타이밍 시험 부분 집합 3회 반복이 모두 통과, 최종 ZIP은 두 인터프리터 모두 통과. v0.2.20부터 있는 프로세스 타이밍 시험의 간헐 가능성을 배제하지 못함 |
| 모델 호출 경계 | PASS | `review_runner.py` 밖 `subprocess` 금지 시험을 약화하지 않았다(ACL 검사를 `icacls` 대신 Win32 DACL로 구현) |

## 4. Windows ACL / Signer / SHADOW / 롤백 (호스트 실측, 서명 0)

- **서명 경계(읽기 전용)**: 후보 코드 경로로 운영 신뢰 루트 로드(핀 sha256 일치, repo_id `1451933830`), `ToolSigner`가 키 ID `cowork-approver-1`을 ACTIVE로 신뢰, **DPAPI 암호문 → 운영 키를 메모리에서만 복호화(32바이트), 서명은 하지 않음**, 키 파일은 암호화 형식. 승인 키 폴더 4개 파일은 `Everyone/Users/Authenticated Users` 쓰기 권한 없음(Win32 DACL).
- **실행 계정**: 감시기 프로세스 소유자 = 현재 사용자 = 키 소유자이므로 **같은 감시기 프로세스가 서명 가능**(설계의 1순위 경로가 실제로 가능). 키 ACL 완화·복제 불필요, 한 줄도 변경하지 않음.
- **롤백 리허설(격리 복사본)**: 설치본을 복사 → v0.2.21 ZIP을 덮어써 업그레이드(모든 파일이 ZIP 항목과 일치) → `config-check` 0.2.21, 기능 미설정=`not configured` → 설정만 켠 상태(`enabled=False`, signer 없음 → 서명 불가) → v0.2.20 ZIP으로 되돌려 **복사본이 v0.2.20 ZIP과 바이트 동일**(남은 파일 0) → 복사본 삭제. 실제 설치 트리·운영 DB 불변. 롤백 절차 = `auto_approval` 설정 제거(또는 `enabled:false`)·재시작, 필요 시 이전 ZIP 바이트 복원.
- **참고**: 위 리허설 중 "상태 폴더에 운영 DB 없음" 항목은 무의미한 검사라 증거로 세지 않는다.

## 5. 미완료 / 사용자·GPT 승인 필요

| 항목 | 상태 |
|---|---|
| 새 후보의 **독립 리뷰** | `NOT_RUN` — 별도 REQUEST/서명/비용 승인 필요. 변경 규모(운영 코드 약 +910줄: 신규 모듈 743줄 + 기존 파일 변경 +166줄)와 서명 권한을 다루므로 `POLICY-STATIC-V1-LARGE`(R2, 최대 $3, 1회) 권고 — 결정은 GPT |
| 위임 범위 확정 | **사용자 1회 승인 필요**: 허용 Work/skill 목록, 요청당 $1, 일 2회/$3, 월 $10(제안), 만료 30일(제안), `enabled_at`. 현재 어떤 값도 승인·적용된 것 아님 |
| 운영 설치 | 미승인(`NOT_RUN`): 설치본 교체, 설정 `auto_approval` 추가, 위임 파일 배치(보호 ACL), 키 접근 경로 설정 |
| 운영 Notifier | `AUTO_SIGNING_UNCERTAIN`을 설치된 Notifier 이벤트 목록에 추가해야 알림이 감(미변경) |
| 활성화 절차 | 승인 후: 위임을 `enabled:false`로 설치 → 감시기 1주기(기존 대기 요청 전부 "OFF일 때 봄"으로 기록되어 영구 제외) → `enabled:true`+`enabled_at` 설정 → 2주기+재시작 확인 |
| 현재 대기 중인 요청 | Work→Knowledge·대시보드 요청은 **소급 자동 실행되지 않는다**(시험으로 입증). 수동 서명 경로는 그대로 유효 |

**설계 한계(정직)**: ① 서명 능력이 GitHub가 통제하는 입력을 읽는 감시기 프로세스 안에 있다(별도 신뢰 영역 아님). 방어는 위임 게이트와 fail-closed 순서이며, 파서 취약점이 있다면 위임 범위 안의 서명까지가 최대 피해다(요청당 $1·일 2회·월 $10). ② 요청 생성 시각은 핀된 commit의 committer date이며 API로 커밋하는 주체가 지정할 수 있다 → "활성 상태에서 처음 봄" 플래그가 두 번째 방어선. ③ GPT가 `SOURCE_PIN.json`을 올리지 않으면 서명하지 않는다(`PIN_MISSING`). ④ 일/월 키는 로컬 시계(KST 달력)이며 서버 시각과의 편차 검사는 기존과 동일.

## 6. 후보 ZIP

- `skill-collab-watcher_v0_2_21_1115_DEV_NOT_FOR_DEPLOYMENT.zip` **272,839 B**, sha256 `16921bf4021714345cabc78de5e2e8a6882891615f90b5747622570ca4465d8b`, 100개 파일, ZIP CRC/무결성 OK, 경로 이탈·심볼릭 링크 0, 비밀 스캔 findings 0, **재빌드 바이트 동일**.
- 위치: Windows 로컬 보관 + PRIVATE `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/artifacts/v0_2_21/` {ZIP commit `6f49c19aab6a`, `CANDIDATE_MANIFEST.md` `a483307293f2`, `diff_v0_2_20_to_v0_2_21.patch`(126,207 B, sha256 `e3a7aeb2…`) `8763271b12da`}. 원격 원시 바이트·ZIP CRC 재조회 일치. 기존 v0.2.20 ZIP·설치본 미변경, 이름 충돌 없음, 요청·READY·`packages/` 파일 없음(게시 자체가 리뷰 신호 아님).

## 7. 다음 한 동작

GPT가 단일 판정으로 (a) 위 후보의 독립 리뷰 요청(권고 R2/LARGE, $3, 1회)과 (b) 사용자에게 받을 **위임 범위 1회 확정**(허용 Work/skill, 요청당·일·월 한도, 만료)을 묶어 제시한다. 리뷰 PASS와 사용자 승인 후에 Windows가 `설치 → 위임 OFF로 1주기 → enabled 전환 → 2주기+재시작 확인`을 한 회차로 수행한다.
