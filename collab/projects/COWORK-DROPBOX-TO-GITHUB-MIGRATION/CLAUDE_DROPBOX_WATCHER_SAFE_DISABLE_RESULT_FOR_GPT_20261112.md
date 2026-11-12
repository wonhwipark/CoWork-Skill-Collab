# Dropbox 리뷰 감시기 안전 Disable·보존 — 결과 (Claude 자체 보고)

- 작성: Windows Claude Code (감시기 PC), 2026-11-12 KST 23:3x–00:0x 실측
- 근거: `WINDOWS_DROPBOX_WATCHER_SAFE_DISABLE_ONE_SHOT_r0001_20261112.md`, `USER_DROPBOX_WATCHER_SAFE_DISABLE_APPROVAL_r0001_20261112.md`
- 성격: **자체 실측 보고(`SELF_TEST_REPORTED`)**, 독립 리뷰 아님. 작업 정의 변경(Disable)과 프로세스 중지는 **관리자 권한이 필요해서 사용자가 관리자 셸에서 검증된 스크립트 1개를 직접 실행**했고, Claude는 사전 점검·보존·사후 검증·게시를 맡았다.
- 게시하지 않은 것: 작업 정의 XML, DB·WAL·SHM, 백업, 로컬 경로, PID, 요청 ID, 계정·토큰. 집계와 불리언만 적었다.
- 이 작업은 **GitHub LIVE 전환이 아니다.**

## 1. 필수 판정 요약
| 항목 | 값 |
|---|---|
| PREFLIGHT_INFLIGHT_REVIEW | **PASS** — 진행 중·불확실·실패 작업 0, 리뷰어(claude) 자식 프로세스 0, 감시기 자체 status 리포트 기준 |
| PENDING_REQUEST_PRESERVATION | **PASS** — 대기 요청 1건(이미 CLOSED_SUPERSEDED, READY 없음)과 READY·영수증 없는 4건(모두 종결: REJECTED 3, CONFLICT 1) 모두 변경·삭제·재실행 없음. Dropbox 원본 요청·결과·영수증은 건드리지 않음 |
| TASK_IDENTITY_VERIFIED | **PASS** — `skill_collab_watcher.cli ... watch --longpoll`을 실행하는 예약 작업은 정확히 1개. 서비스·Run 키·시작 폴더·다른 작업에 재시작 경로 없음. Bridge는 다른 작업 이름만 대상으로 하며 실행 전 작업 내용을 검사함 |
| ARCHIVE_BACKUP | **PASS** — 중지 후 정지 상태에서 DB main·WAL·SHM 복사, main·WAL은 원본과 SHA-256 일치. 중지 전에는 작업 정의·설치 목록·인벤토리 보존. 로컬 보호 폴더(현재 사용자만 접근), 동기화·원격 업로드 없음 |
| RESTORE_COPY_TEST | **PASS (DB 복사본)** / **SKIP (작업 정의 복원)** — DB는 별도 복사본에서 `integrity_check=ok`·`quick_check=ok`, 작업 COMPLETED 60·CONFLICT 1·진행 중 0. 작업 정의 XML은 형식 검증과 해시 기록까지만 했고 실제 재등록 시험은 새 작업을 만들게 되어 하지 않음 |
| WATCHER_TASK_DISABLED | **PASS** — 작업 상태 `Disabled`, 설정 `Enabled=False`, 두 관측 지점 모두 유지 |
| WATCHER_PROCESS_STOPPED | **PASS** — 런처·자식 프로세스 0, 락 파일 소유자 없음, 두 관측 지점 모두 0. 마지막 결과 코드 `267014`(사용자 요청에 의한 작업 종료) |
| MODEL_CALLS_NEW | **0** — `review_dispatch_count`·`model_calls`·`claude_process_start_count` 모두 61 유지(복사본 기준), 감사 로그 마지막 이벤트가 중지 전 `SCAN_END` |
| USD_SPEND | **0** |
| QUEUE_INTEGRITY | **PASS** — 중지 후 새 스캔·WATCH_START 0(감사 최대 id 22907 유지, 알림기 last_id 22907 고정), 복사본 무결성 정상, 중복 처리·유실 없음 |
| DASHBOARD_UNCHANGED | **PASS** — 작업 정의 해시 불변, 같은 프로세스, 로그 계속 갱신 |
| NOTIFIER_UNCHANGED | **PASS** — 작업 정의 해시 불변, 같은 프로세스. 새 이벤트가 없어 새 알림이 오지 않는 것이 정상 |
| BRIDGE_UNCHANGED | **PASS** — 작업 정의 해시 불변, 5분 주기 실행과 결과 0 유지 |
| ACTIVE_PROVIDER | **NONE** (자동 리뷰 없음) |
| ETW_GATE | 변경 없음: `C_ETW=FAIL_UNTRUSTED_MEASUREMENT`, `C_OVERALL=PARTIAL` (이 작업으로 소급 PASS 없음) |
| INDEPENDENT_REVIEW | NOT_RUN |
| CUTOVER | MIGRATION_NOT_CUTOVER |
| ROLLBACK_READY | **PASS (관리자 권한 필요)** — 작업 정의 XML·설치 목록·DB 일관 백업 보존. 복구 수단은 작업 Enable 후 Start이며 둘 다 관리자 권한 필요 |
| HOST_OPERATION_STATUS | `DROPBOX_WATCHER=DISABLED_ARCHIVED` |

## 2. 최종 한 줄
`WATCHER_DISABLE=PASS; ACTIVE_PROVIDER=NONE; CUTOVER=MIGRATION_NOT_CUTOVER; RESTORE_READY=PARTIAL`
- `RESTORE_READY=PARTIAL`: DB 복원은 복사본에서 검증했으나, 작업 정의의 실제 재등록 복원은 새 작업 생성이라 시험하지 않았다.

## 3. 단계별 실측
### Gate A — 중지 전 점검 (읽기 전용)
- 운영 DB는 직접 열지 않았다. 대신 감시기 자체의 `status` 리포트를 1회 사용했다(실행 중인 감시기가 매 주기 쓰는 같은 코드 경로).
- 감시기 프로세스는 런처(부모는 작업 스케줄러 호스트)와 자식 파이썬 각 1개, `conhost` 1개. 리뷰어 자식 0.
- 마지막 리뷰 결과 파일은 11-09 12:13이고 이후 새 요청 없음.
- 호출 위험: READY는 있으나 영수증이 없는 4건은 모두 종결 상태이고 진행 중 작업은 0이어서, 작업이 살아 있어도 새 리뷰 호출을 유발할 경로가 없었다.
### Gate B — 중지 전 보존
- 4개 작업(대상 1, 비교용 3)의 정의 XML과 SHA-256, 설치 목록(v0.1.5, 패키지 18개 파일·설정 해시, `secrets.json`은 복사하지 않고 존재만 기록), 로컬 결과 60·전사 57·스냅샷 60 인벤토리, DB 파일 3종의 이름·크기·시각.
- 가동 중 WAL DB의 파일 복사는 일관성이 없어 하지 않았다. 인계서 조건대로 **중지 후 정지 상태**에서 복사했다.
### Gate C — Disable + Stop
- Claude 세션(비관리자)의 `Disable-ScheduledTask`는 **액세스 거부**였고 이 시도로 바뀐 것은 없었다(작업 정의 XML이 보존본과 동일함을 확인). 권한 우회는 하지 않았다.
- 사용자가 관리자 셸에서 스크립트 1개를 실행했다. 스크립트는 작업 이름·동작의 1:1 일치, 정의 불변, 프로세스 정확히 2개, 리뷰어 자식 없음, 마지막 DB 쓰기 후 유휴 구간(파일 수정 시각만 사용, DB는 열지 않음)을 확인한 뒤 Disable → Stop을 수행했다. 중지 시각은 23:55:59였고 마지막 감사 이벤트는 그 직전(23:55:34)의 `SCAN_END`였다.
- 감시기 v0.1.5에는 정상 종료 신호가 없어 `Stop-ScheduledTask`는 강제 종료다. 유휴 구간·진행 작업 0을 확인한 뒤 수행했고, 복사본 무결성 검사가 정상이다.
### Gate D — 사후 검증
- 관측 지점 1(23:57:12), 2(23:58:16), 3(23:59:21)과 Bridge 주기 확인(23:59:35): 감시기 작업 Disabled, 감시기 PID 없음, DB main·WAL 수정 시각·크기 불변(main 22:23:28, WAL 23:55:34), 갱신기·알림기·Bridge 프로세스와 작업 정의 불변.
- Bridge는 중지 후 첫 5분 주기(23:59:32)에도 정상 실행되어 결과 0, `model_calls` 0, 상태 `ALREADY_COMPLETED`를 기록했다.
- 감시기 작업 정의는 보존본과 **정확히 한 줄**(`Enabled=false`)만 다르다.
- 관측 간격은 중지 후 약 4분으로 짧다. **재부팅·재로그인 후에도 Disabled가 유지되는지와 장기 안정은 미검증(`LONG_RUN=PENDING`)**이다.

## 4. 알아 둘 점
- **새 Dropbox 요청은 자동으로 처리되지 않는다.** 이는 의도한 결과이며 `ACTIVE_PROVIDER=NONE`이다. GitHub SHADOW는 LIVE가 아니고 GitHub에 새 REQUEST/READY를 올려도 자동 리뷰되지 않는다.
- **DB 파일의 SHM만 중지 후에도 수정 시각이 바뀌었다(23:56:50).** 중지된 감시기가 아니라 실행 중인 알림기의 읽기 전용 폴링이 만든 변화로 보이며, main·WAL은 23:55:34 이후 변하지 않았다. 알림기는 이번 승인 범위 밖이라 변경하지 않았다.
- **관측 방식 고지:** 이 작업에서는 운영 DB를 직접 열지 않았다. 다만 이전 세션들의 관측에서는 `mode=ro`로 열었다(GPT 지적과 동일, 영향은 미측정).
- 대시보드 갱신기는 계속 Dropbox에 게시한다. 감시기가 멈췄으므로 대시보드의 요청 상태는 더 이상 갱신되지 않는다. 갱신기·Bridge·알림기를 어떻게 할지는 승인 범위 밖이다.
- 복구가 필요하면 사용자 승인 하에 관리자 셸에서 작업 Enable 후 Start. 이 작업에서 실행하지 않았다.

## 5. 다음 한 동작 (제안, 미실행)
- GPT: 결과 판정과 `CURRENT.md`·`TRACKER.json` 확인.
- 사용자 결정: 남은 Dropbox 의존 구성요소(대시보드 갱신기·Bridge·알림기)의 처리, GitHub 쪽 리뷰 경로(SHADOW 이후) 준비. 모두 별도 승인이 필요하다.
