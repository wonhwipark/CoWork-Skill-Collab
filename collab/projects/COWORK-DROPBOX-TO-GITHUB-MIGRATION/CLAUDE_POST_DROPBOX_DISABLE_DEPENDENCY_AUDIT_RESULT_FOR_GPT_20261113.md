# Dropbox 감시기 Disable 이후 잔여 구성요소 의존성 감사 — 결과 (Claude 자체 보고)

- 작성: Windows Claude Code, 2026-11-13 KST 00:1x–00:2x 실측
- 근거: `WINDOWS_POST_DROPBOX_DISABLE_DEPENDENCY_AUDIT_ONE_SHOT_r0001_20261113.md`
- 성격: **읽기 전용 감사(`SELF_TEST_REPORTED`)**. 정리 판정이며 **정리 실행이 아니다.** 독립 리뷰 아님.
- 증거 표기: `HOST_REAL_READ_ONLY`(이번 실측) / `HISTORICAL_REPORTED`(이전 보고) / `NOT_VERIFIED`
- 게시하지 않은 것: 로컬 경로 원문, 계정·토큰·chat ID, 커맨드라인 원문, 로그 원문, DB 내용. 구성요소 이름과 집계만 적었다.

## 1. 필수 필드
| 필드 | 값 | 증거 |
|---|---|---|
| DASHBOARD_DEPENDENCY | `DROPBOX_REVIEW_ONLY` — Dropbox의 요청·리뷰·영수증 폴더를 읽어 Dropbox 정적 HTML 1개를 게시. 감시기 DB는 읽지 않음. 감시기 구성·인증 파일과 공용 venv만 빌려 씀 | 코드 확인 + 작업 정의 + 로그 집계 (HOST_REAL_READ_ONLY) |
| DASHBOARD_RECOMMENDATION | **RETIRE_CANDIDATE** (Bridge 다음 순서) | 아래 §3 |
| NOTIFIER_DEPENDENCY | 프로세스는 `DROPBOX_REVIEW_ONLY`(감시기 감사 로그 소비). **Telegram 채널·전송 모듈은 `SHARED_OTHER_WORK`**(Dropbox 노트 알림 경로와 공유) | 코드 + 호출처 검색 (HOST_REAL_READ_ONLY) |
| NOTIFIER_RECOMMENDATION | **KEEP**(보류). 프로세스 중지는 가능하나 GitHub 알림 경로 결정 전에는 이득이 작음. 채널·모듈·비밀 파일은 삭제 금지 | §3 |
| BRIDGE_DEPENDENCY | `DROPBOX_REVIEW_ONLY` — 대시보드 갱신기 v0.1.4→v0.1.9 **1회 설치용** 수신기. 이미 완료. 대상은 갱신기 작업 이름 하나로 고정 | 코드 + 정책 + 상태 파일 (HOST_REAL_READ_ONLY) |
| BRIDGE_RECOMMENDATION | **RETIRE_CANDIDATE** (가장 먼저) | §3 |
| SHM_WRITER_ATTRIBUTION | **`CORRELATED_NOTIFIER` (확정 아님)**. `SHM_WRITER=UNKNOWN`에서 한 단계만 올림 | §2 |
| WATCHER_DISABLED_PERSISTENCE | 감사 시점 **Disabled·프로세스 0·새 자동 재시작 경로 없음**. 재부팅·재로그인 후 유지는 NOT_VERIFIED (마지막 부팅 11-03, 이후 재부팅 없음) | HOST_REAL_READ_ONLY / NOT_VERIFIED |
| ACTIVE_PROVIDER | **NONE** | HOST_REAL_READ_ONLY |
| MODEL_CALLS_NEW | **0** (감시기 프로세스 없음, 리뷰어 프로세스 없음, DB main·WAL 수정 시각 11-12 23:55 이후 불변, Bridge 기록 `model_calls=0`). DB 카운터는 열지 않아 직접 읽지 않음 | 간접 (HOST_REAL_READ_ONLY) |
| HOST_CHANGES | **0** | §5 |
| ROLLBACK_PREREQS | §4 | — |
| GITHUB_DASHBOARD_INDEPENDENCE | **독립 확인**. GitHub 대시보드는 저장소 Actions 산출물이고, 세 구성요소 코드에는 GitHub 참조가 0건이며 서로 읽고 쓰는 경로가 없다. Pages도 Windows 갱신기를 필요로 하지 않음 | 코드 검색 (HOST_REAL_READ_ONLY) + 저장소 문서 읽기 |
| CUTOVER | MIGRATION_NOT_CUTOVER | — |

## 2. 구성요소별 실측
### A. Dashboard updater
- 작업: 로그온 트리거, 현재 사용자·제한 권한, 실행 중. 재시작 3회/5분. 부모-자식 2프로세스(런처+파이썬).
- 입력: Dropbox `requests/reviews/receipts` 목록·본문(읽기). 출력: Dropbox `dashboard/index.html` 1개(CAS 게시, 외부 수정 시 덮어쓰기 거부). 로컬 출력은 운영 로그와 규칙 파일뿐.
- **감시기 DB를 열지 않는다**(코드에 SQLite 사용 없음). 따라서 감시기 Disable이 입력에 영향을 주지 않으며, 입력 Dropbox 파일이 더 늘지 않는 한 결과도 바뀌지 않는다.
- 로그 집계(최근 3,000줄): UNCHANGED 2,818, PUBLISHED 5, 연결 오류 177. 마지막 상태 요청 65·결과 60으로 고정. 원격 index.html 마지막 수정은 11-09 12:13 KST(마지막 리뷰 시점)로 이후 게시 없음. 즉 **지금은 같은 값을 반복 확인만 한다.**
- 실패 시: 게시가 멈추면 구형 화면이 남는다. 지금도 사실상 구형 상태가 고정이다.
- 소비자: index.html에 파일 단위 공유 링크 없음. 상위 공유 폴더 접근자(사용자 계정 등)가 볼 수 있음. **실제로 누가 보는지는 NOT_VERIFIED.**
- 다른 기능과의 연결: Bridge가 이 작업 이름을 대상으로 한다(설치 시에만). 공용 파이썬 venv·감시기 구성/인증 파일 의존.

### B. Telegram notifier
- 작업: 로그온 트리거, `pythonw`(창 없음), 11-06부터 연속 실행, 재시작 3회/5분.
- 30초마다 감시기 DB를 **읽기 전용 연결로 열었다 닫고**, 알림 대상 이벤트(완료·실패·불확실·업로드실패·인증·충돌·거부)가 있을 때만 Telegram 전송. 워터마크(`last_id`)는 로컬 상태 파일에 보존 중이며 감시기 마지막 이벤트 시점에서 고정.
- 공유 여부: 알림 프로세스는 감시기 전용. 그러나 **전송 모듈과 비밀 파일을 `notify_note`(노트 게시 알림, `publish.ps1` 호출)도 import해서 쓴다.** 이 경로는 프로세스와 독립이라 프로세스를 멈춰도 노트 알림은 영향이 없다. 반대로 모듈·비밀 파일을 지우면 노트 알림이 깨진다. Job List·Bridge·다른 자동화에서의 참조는 검색 범위 안에서 0건.
- 재기동 시 중복 위험: 워터마크가 유지되므로 소급 재발송 없음. 상태 파일이 없어지면 최초 실행 규칙상 현재 최대 id로 초기화해 역시 재발송 없음. DB를 다른 DB로 교체하면 id 체계가 달라 알림이 누락/지연될 수 있음(이행 시 별도 설계 필요).

### C. Bridge
- 작업: 5분 주기, 1회 실행 후 종료, 실행 제한 4분, 재시작 정책 없음.
- 기능: 승인 정책과 해시가 일치하는 갱신기 v0.1.9 설치 1회. 상태는 `HOST_APPLIED`, 보고 게시 완료. 이후 매 주기 `ALREADY_COMPLETED`로 즉시 반환하며 **Dropbox 요청을 보내지 않는다**(원격 읽기는 미완료 상태 분기에만 있음). 최근 기록 결과 0, 모델 호출 0.
- 설치 승인은 2026-11-14 00:00 KST 만료.
- 제어 대상: 정책의 작업 이름 하나(갱신기)에 한정, 코드가 이름 불일치를 거부한다. **감시기 작업을 Enable/Start/Stop 하는 경로 없음.** 감시기 재시작 감시 기능 없음. Dispatcher/Job List 작업은 이 Bridge를 참조하지 않음(검색 범위 내).
- 공용 의존: 감시기 구성·인증 파일과 venv.

### SHM 수정 시각 (읽기 전용 실측)
- 파일 메타데이터만 70초간 5초 간격으로 관측(DB 연결 없음): `-shm` 수정 시각이 **정확히 30초 간격**(:20.3, :50.3 …)으로 갱신. `-wal`·main은 불변.
- 알림기의 폴링 주기 30초와 일치하고, 갱신기·Bridge 코드에는 DB 접근이 없으며 감시기는 없다 → **알림기가 원인일 가능성이 높다(상관 증거).**
- 핸들 소유·쓰기 인과(알림기가 연결을 열 때 읽기 표시를 갱신하는지)는 증명하지 못했다. 열린 상태가 순간적이라 핸들 열거 불가, ETW 귀속 실패 이력도 있어 시도하지 않았다. 따라서 `CORRELATED_NOTIFIER`로만 보고하며, 운영 데이터(main/WAL) 수정 0은 **파일 시각 기준 증거(간접)**이다.

## 3. 판정과 중지 영향
| 구성요소 | 판정 | 근거 | 중지 시 영향 |
|---|---|---|---|
| Bridge | **RETIRE_CANDIDATE** | 1회 설치 완료, 이후 작업 없음, 대상은 갱신기뿐, 승인 만료 임박 | 데이터 유실 0. 다른 기능 영향 없음(검색 범위). 향후 갱신기 재설치가 필요하면 새 승인으로 재설치 |
| Dashboard updater | **RETIRE_CANDIDATE** | Dropbox 전용, 입력이 더 늘지 않음, 결과 고정, GitHub 대시보드와 독립 | Dropbox 화면이 마지막 값(요청 65/결과 60)에서 **갱신 중이라고 오해될 수 있는 정지 화면**으로 남음(알림 문구는 GPT 결정). 사용자가 해당 화면을 실제로 쓰는지는 미확인이라 **사용자 확인 필요** |
| Notifier | **KEEP**(보류) | 프로세스는 감시기 전용이나 채널·모듈이 노트 알림과 공유되고 GitHub 알림 재사용 가능성이 있음. 중지 이득은 SHM 접촉 제거뿐 | 중지해도 노트 알림은 유지. 새 감시기 이벤트가 없어 알림 손실 0. 모듈·비밀 삭제는 금지 |

권고 순서(실행 아님): Bridge → 갱신기 → (GitHub 알림 경로 결정 후) 알림기. 어느 단계든 공용 venv·감시기 구성·인증 파일은 보존해야 한다(삭제하면 남은 구성요소가 깨짐).

## 4. 중지 후보의 체크리스트와 되돌리기 (실행하지 않음)
- 사전: 해당 작업 정의 XML과 해시 보존, 현재 상태/마지막 결과 기록, 다른 두 작업 정의 해시 불변 확인, 운영 DB는 열지 않음.
- 중지 방식: Stop은 일반 사용자 권한으로 가능하지만 **재시작 방지(Disable)는 관리자 권한이 필요**(이전 실측: Disable·Register 액세스 거부). Stop만 하면 로그온/재시작 정책으로 되살아날 수 있다.
- Bridge는 5분 트리거이므로 Disable 없이는 다음 주기에 다시 실행됨(기존 제공된 비활성화 스크립트 있음).
- 되돌리기: 관리자 셸에서 Enable 후 Start. 작업 정의 XML 보존본 필요. 갱신기는 재시작 시 게시 상태를 Dropbox 현재 값에서 재계산(CAS)하므로 중복 게시 위험이 작음.
- 보존: 로그, 규칙, 상태 파일, 워터마크 파일은 삭제하지 않음.
- 중지 후 확인: 작업 Disabled·프로세스 0, 감시기 Disabled 유지, 나머지 작업 해시 불변, 재부팅/재로그인 후 유지 확인(NOT_VERIFIED, 사용자 승인 하에).

## 5. HOST_CHANGES=0 근거
- 사용한 것: 작업 스케줄러 조회, 프로세스 조회, 파일 메타데이터, 코드·설정·상태 파일 읽기(비밀 값은 키 이름만 확인), Dropbox 메타데이터·공유 링크 목록 조회(읽기).
- 하지 않은 것: 작업 생성/Stop/Disable/Enable/Start, 운영 DB·WAL·SHM 연결, 설정·비밀 수정, Telegram 발송, 모델 호출, 재부팅/재로그인, ETW/관리자 실행, Dropbox 쓰기.
- 한계: 의존성 검색은 이 PC의 사용자 작업 폴더·알려진 자동화 폴더 범위이며 전 디스크 검색이 아니다. 해당 범위 밖 참조는 **확인 못함**으로 남는다.

## 6. 의존성 표 (Mermaid 대체: 표)
| 소비자 → 자원 | 상태 |
|---|---|
| 갱신기 → Dropbox 요청·리뷰·영수증(읽기), Dropbox index.html(쓰기) | 있음 |
| 갱신기 → 감시기 DB | **없음 실측**(코드) |
| 갱신기·Bridge·알림기 → 공용 venv, 감시기 구성/인증 파일(알림기는 DB 경로만) | 있음 |
| Bridge → 갱신기 작업 이름 | 있음(설치 시에만) |
| Bridge → 감시기 작업 | **없음 실측**(코드) |
| 알림기 → 감시기 DB(30초 읽기) | 있음 |
| 노트 알림(`notify_note`) → 알림기 모듈·Telegram 비밀 | 있음 |
| 세 구성요소 → GitHub 대시보드/Actions/Pages | **없음 실측**(코드 참조 0) |
| Dispatcher/Job List 등 다른 작업 → 세 구성요소 | 검색 범위 내 없음, 범위 밖 **확인 못함** |
| 기존 Dropbox 경로(위 전부) ↔ GitHub Actions/Pages | 별도 배포 경로 |

## 7. 사용자 확인이 필요한 한 가지
- Dropbox `dashboard/index.html`을 지금도 열어 보는가? 아니라면 Bridge → 갱신기 순서로 별도 승인 하에 Stop+Disable(관리자 셸 필요)을 검토할 수 있다.

최종 1행:
`DEPENDENCY_AUDIT=PASS; DASHBOARD=RETIRE_CANDIDATE; NOTIFIER=KEEP; BRIDGE=RETIRE_CANDIDATE; ACTIVE_PROVIDER=NONE; HOST_CHANGES=0`
