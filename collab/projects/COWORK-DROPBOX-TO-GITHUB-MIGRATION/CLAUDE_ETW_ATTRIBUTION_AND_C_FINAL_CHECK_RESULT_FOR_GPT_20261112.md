# ETW 귀속 보정 · C 최종 검증 · 운영 지속성 읽기 전용 확인 — 결과 (Claude 자체 보고)

- 작성: Windows Claude Code (감시기 PC), 2026-11-12 KST 23:0x–23:3x 실측
- 근거 인계서: `GPT_ETW_ATTRIBUTION_C_FINAL_CHECK_ONE_SHOT_r0001_20261112.md`
- 성격: **자체 시험·실측 보고(`SELF_TEST_REPORTED`)**, 독립 리뷰 아님. 관리자 권한이 필요한 실행은 사용자가 관리자 셸에서 직접 했고, Claude는 출력 기록을 읽어 판정했다. 원본 추적·PID/TID·로컬 경로·프로세스 목록은 **LOCAL_ONLY**이며 게시하지 않았다(집계와 불리언만).

## 1. 필수 판정 요약
| 항목 | 값 |
|---|---|
| ETW_TRACE_REANALYSIS | **DONE** — 기존 C 추적은 헤더/스키마 집계, 보존된 사전검증 추적은 분류기 수정 전후로 2회 재분석 (§4) |
| PROCESS_TREE_ATTRIBUTION | **NOT_ESTABLISHED** — 시험 프로세스 계통은 WMI 샘플로 확인(자기 포함 2개)했으나 ETW 이벤트와의 귀속은 입증하지 못함 |
| PID_TID_EVENT_FIELD_MAPPING | **PARTIAL / UNVERIFIED** — PID·TID 열 위치와 이벤트 ID 의미는 확인. `Clock-Time`은 FILETIME 가정이 성립하지 않아 시간 상관 불가. 프로세스 시작 payload의 pid/ppid 위치는 WMI 교차 확인 실패 |
| POSITIVE_CONTROL_PREFLIGHT | **FAIL_UNTRUSTED_MEASUREMENT** — 시험 프로세스가 직접 연 마커(양성 대조)가 계통에 귀속된다는 증거를 얻지 못함. 원인은 **측정 도구의 시간·필드 해석 실패**로, "이벤트가 실제로 없음"과 구분할 수 없음 |
| ETW_MEASUREMENT_PREFLIGHT | **FAIL_UNTRUSTED_MEASUREMENT** (GPT 진단 코드 판정 기준 오류: `ETW_PROVIDERS_NOT_VERIFIED`, `PID_FIELD_MAPPING_UNVERIFIED`, `POSITIVE_CONTROL_NOT_ATTRIBUTED_TO_PROBE_TREE`) |
| C_FINAL_RERUN | **NOT_RUN_PREFLIGHT_FAILED** — 인계서 규칙대로 사전검증 실패 시 C 실측과 관리자 추적 반복을 하지 않음 |
| C_READ | 이번 인계서에서 새 실GitHub 실측은 **미실시**. 이전 `PASS(HOST_REAL_REPORTED)`(2회, 3주기, GET 7회, 200×5/304×2, 쓰기 0) 유지. 별도로 제 계정 비관리자 리허설에서 새 프로브 래퍼가 GET 8회(200×7/304×1)·쓰기 0·모델 0으로 동작함을 확인했으나 이는 C 시험이 아님 |
| C_ETW_OPERATING_FILE_ISOLATION | **NOT_PROVEN** (운영 `state.sqlite3`/`-wal`/`-shm`/`watch.lock` 무접근은 증명하지 못했고, 접근했다는 뜻도 아님) |
| C_OVERALL | **PARTIAL** |
| WATCHER_LAST_SCAN_PROGRESS | **PASS_SHORT_TERM** — 두 관측 사이 신규 스캔 10회, 프로세스 불변 (§6) |
| DASHBOARD_LOG_PROGRESS | **PASS_SHORT_TERM** — 로그 증가, 마지막 기록 갱신, 프로세스 불변 (§6) |
| LONG_RUN | **PENDING** — 재시작 후 감시기 약 55분, 갱신기 약 50분 관측. 24시간 안정으로 주장하지 않음 |
| MODEL_CALLS_NEW | **0** (`review_dispatch_count` 61 → 61, `model_calls` 61 → 61) |
| USD_SPEND | **0** |
| ACTIVE_PROVIDER | Dropbox LIVE v0.1.5 유지(단일 LIVE) |
| INDEPENDENT_REVIEW | NOT_RUN |
| CUTOVER | MIGRATION_NOT_CUTOVER |

## 2. 실제로 한 일과 횟수 (그대로 기록)
- **GPT 진단 코드:** 두 파일 모두 SHA-256과 Git blob 해시가 인계서와 일치. GPT의 9개 시험을 격리 프로세스에서 재실행해 9 PASS.
- **호스트 측정기 보완(로컬 보존, 미게시):** 추적 CSV와 WMI 프로세스 샘플을 GPT 코드가 받는 정규화 형식으로 바꾸는 도구와 시험 22개를 추가해 합계 **31 PASS**. 관리자 없이 전체 호출 흐름을 합성 데이터로 확인하는 `-SelfCheck` 모드 포함(양성 PASS, 음성 `FAIL_UNTRUSTED_MEASUREMENT`).
- **관리자 셸 실행 3회(사용자가 실행):**
  1. 1회차: P0 게이트에서 중단. **제 스크립트 버그**(PowerShell 5.1에서 `Stop` 상태의 `2>&1`이 정상 stderr 로그를 오류로 처리). 추적·시험 계정 활성화·측정 없음.
  2. 2회차: **새 ETW 추적은 이 1회뿐.** 시험 계정이 직접 만든 마커 파일을 여는 양성 대조 사전검증. 추적 자체는 정상 수집(행 86,034, 수집 손실 0, 프로세스 이벤트 포함)이었으나 **제 정규화 분류기가 이벤트를 하나도 인식하지 못해**(`events_kept=0`) FAIL.
  3. 3회차: 새 추적 없이 **보존된 사전검증 원본을 분류기 수정 후 재분석** — 여전히 FAIL(§4). 사전검증 실패로 C 실측은 실행하지 않음.
  - 인계서의 "관리자 ETW 재시험 1회" 한도는 지켰지만(새 추적 1회), 관리자 셸 실행 자체는 3회였음을 명시한다.
- 시험 계정은 매 실행 후 비활성으로 복구, 토큰 사본은 만들지 않았거나 삭제됨(P3 미실행).

## 3. GPT 진단 코드에 대한 관찰 (판정은 GPT)
- 코드는 의도대로 동작하고 fail-closed다. 호스트 적용 시 다음을 발견했다.
  1. 트리 PID 이벤트가 프로세스 기록의 수명 밖이면 **조용히 제외**된다(오류 없음). 마지막 구간 이벤트나 호스트 시계 오차가 있으면 보호 파일 접근이 가려질 수 있어, 호스트 도구는 이를 `tree_events_outside_process_lifetime`으로 따로 집계했다. 코드에서 오류로 승격하는 것을 권한다.
  2. `match_path`는 문자열 정규화라 8.3 짧은 이름·junction·UNC·하드링크를 처리하지 못한다. **이 호스트의 운영 볼륨은 8.3 이름 생성이 켜져 있고(상태 0), 운영 경로에 reparse point는 0개**다. 따라서 경로 별칭 위험은 이론이 아니라 실재한다. 이번 도구에도 완전한 파일 identity 정규화는 없다(미검증).
  3. `process_provider_verified`가 호스트에서 "프로세스 시작 이벤트가 실제로 파싱되고 WMI와 일치"해야 참이 되도록 구현했다. 입력 형식이 맞지 않으면 플래그가 거짓이 되어 사전검증이 실패한다(이번 경우).

## 4. ETW 추적 재분석 결과 (집계만)
### 4-1. 기존 C 추적(실패한 1차 측정)
- tracerpt CSV 구조: 열 위치 PID=9, TID=10, `Clock-Time`=16. `Event Name`은 **공급자 이름**, `Type`은 **숫자 manifest 이벤트 ID**(Kernel-File: 12=Create, 15=Read, 16=Write, 13/14=Cleanup/Close, 24=OperationEnd 등).
- 행 54,580, 서로 다른 PID 129. **Kernel-Process 이벤트가 없어** 프로세스 계통은 이 추적에서 복원할 수 없다.
- 미끼 파일 열기 1건과 SHADOW 폴더 이벤트는 시험 프로세스가 아닌 PID들에서 관측되었고, 미끼 열기의 스레드 ID는 **1**이었다(시험 프로세스의 실제 스레드 ID와 자릿수가 다름, 원인 미확정). 서로 다른 PID에서 같은 TID가 4건 관측됨.
### 4-2. 보존된 사전검증 추적(2차 측정, 보강된 수집)
- 행 86,034, Kernel-File 이벤트 대부분(예: Create 10,135, Read 3,205, Write 1,557), **Kernel-Process 시작 8건·종료 7건**. 수집 손실 0건(tracerpt 요약 기준). 시험 프로세스는 WMI 샘플에서 자기 포함 2개 프로세스 계통으로 확인됨(자식 1개의 정체는 미확인).
- **시간 해석 실패:** `Clock-Time`을 FILETIME으로 해석할 수 있는 행이 86,034행 중 7,196행(약 8%)이고 추적 시간대(±60초)에 들어오는 것은 2행뿐이다. 파일 이벤트 26,643건이 시간 해석 불가로 제외됐다. `logman -ct system` 지정에도 이 열이 FILETIME이 아니다. (프로세스 시작 payload에는 ISO 형식 생성 시각이 있어, 이를 기준으로 열을 보정할 수 있는 가능성이 있다. 미시도.)
- **프로세스 시작 payload:** 이름 없는 위치 기반 값(숫자, 따옴표 ISO 시각, SID, 이미지 경로, 16진수 값). 제 위치 가정(1번째=pid, 3번째=ppid)은 WMI의 (pid, ppid) 쌍과 일치하지 않아 채택하지 못했다.
- 결론: 이 추적에서 마커 열기가 시험 프로세스에 귀속되는지는 **도구가 해석하지 못해 판정 불가**다. "프로세스가 이벤트를 안 남겼다"도, "다른 프로세스가 대신 남겼다"도 입증하지 못했다.

## 5. C 단계 상태 (소급 PASS 없음)
- 실GitHub 읽기 PASS는 이전 보고 그대로이며 이번에 새로 추가한 PASS가 아니다.
- ETW 계측은 신뢰할 수 없어 운영 파일 격리를 **NOT_PROVEN**으로 유지한다. 인계서 §4에 따라 양성 대조 불검출·귀속 실패 시 접근 0 PASS를 선언하지 않는다.
- 보완 근거로 이전 Stage 1에서 확인된 "비관리자 계정의 운영 DB 접근 거부(ACL)"와 "SHADOW 코드 경로가 운영 DB를 열지 않는다"는 코드 근거가 있으나, 이는 보완 근거일 뿐 파일 I/O 무접근 ETW PASS를 대신하지 않는다.

## 6. 운영 지속성 읽기 전용 관측
| 항목 | 지점 1 (23:18:10) | 지점 2 (23:29:42) |
|---|---|---|
| 감시기 작업 / 프로세스 | Running, 런처+자식 1쌍 | 같은 PID, Running |
| 감시기 스캔 누적 | 10,809 | 10,819 (+10) |
| 감시기 `WATCH_START` / `WATCH_END` | 5 / 2 | 5 / 2 (재시작 없음) |
| 갱신기 작업 / 프로세스 | Running, 1쌍 | 같은 PID, Running |
| 갱신기 로그 크기 / 마지막 기록 | 1,001,837 B / 23:17:39 | 1,003,178 B / 23:29:30 |
| 알림기 last_id | 22,843 | 22,865 |
| Bridge | Ready, 마지막 결과 0 | Ready, 마지막 결과 0 |
| `0xC000013A` 재발 | 없음 | 없음 |
- 두 지점 사이에 관리자 시험(ETW 세션 생성, 시험 계정 활성화)이 있었으나 감시기와 갱신기는 영향받지 않았다. 이전에 보고한 "갱신기 1차 종료가 C 시험 시간대와 겹침"은 이번 관측으로 **약화**되지만 원인은 여전히 UNKNOWN이다.
- 재시작 후 경과: 감시기 약 55분(22:34:23 시작), 갱신기 약 50분(22:39:14 시작). 24시간·재로그인·재부팅은 NOT_RUN. 이 인계서에서 추가 재시작은 하지 않았다.
- **관측 방법의 부작용 고지:** 감시기 상태 DB를 `mode=ro`로 열어 읽었다(스캔·이벤트 조회). 읽기 전용 열기가 WAL/SHM 파일에 미치는 영향은 측정하지 않았다.

## 7. 보호·변경 범위
- 작업 정의·계정·인증·정책·운영 DB·Notifier/Bridge 변경 없음. 재시작·`pythonw.exe` 전환 없음. 새 모델 호출 0, 비용 0, Telegram 0, REQUEST/READY 게시 0.
- 샌드박스 작업 폴더에 새 파일을 추가했다(도구·시험·진단, 기존 파일 덮어쓰기 없음). 시험 계정 비활성 복구 확인. 원본 추적은 관리자 전용 폴더에 보존.

## 8. 한계와 다음 한 동작(제안, 미실행)
- 이 결과는 자체 보고이며 사용자가 실행한 관리자 셸 출력에 기반한다. ETW 해석 실패의 원인(시간 열의 의미)은 미확정이다.
- 승인이 필요한 선택지:
  1. **보강 도구 1회 재분석:** 보존된 원본을 새 추적 없이 다시 읽되, `Clock-Time`을 프로세스 시작 이벤트의 ISO 생성 시각으로 자동 보정(오프셋과 기울기 검증)하거나 `Get-WinEvent -Path`로 ETL을 직접 해독한다. 통과하면 같은 실행에서 C 실측 1회. 관리자 셸 1회 필요, **새 명시적 승인 전에는 요청하지 않는다.**
  2. **ETW 없이 보완 근거로 결론:** 비관리자 ACL 접근 거부와 SHADOW 코드 경로 증명을 근거로 두고 파일 I/O 무접근 ETW PASS는 보류한다. GPT 판단 사항.
- 이 문서는 REQUEST/READY가 아니며 운영 변경·유료 리뷰·LIVE 전환 승인이 아니다.
