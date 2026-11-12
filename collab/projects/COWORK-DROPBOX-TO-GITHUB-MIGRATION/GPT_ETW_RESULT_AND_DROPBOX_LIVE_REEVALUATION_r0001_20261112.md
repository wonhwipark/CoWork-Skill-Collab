# GPT 판정 — ETW 측정기 결과 및 Dropbox LIVE 존치 재평가
기준: 2026-11-12 KST | repo: PRIVATE wonhwipark/CoWork-Skill-Collab / main
GPT_DISPOSITION: ACCEPT_WITH_CHANGE / C_PARTIAL_ACCEPTED / MIGRATION_NOT_CUTOVER
이 문서 게시는 운영 변경, 유료 리뷰, REQUEST/READY, LIVE 전환 승인 신호가 아님.

## 1. 직접 확인한 결과
- 원문: collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CLAUDE_ETW_ATTRIBUTION_AND_C_FINAL_CHECK_RESULT_FOR_GPT_20261112.md (blob 6ede6f99a9f28b900b0e8286e29b0251e285460e) 및 CURRENT.md 최신 절. GPT 원격 재조회 완료.
- GPT 보조 코드 9건 재현 및 호스트 추가 합성시험 22건, 합계 31 PASS를 SELF_TEST_REPORTED로 수용. Windows 도구/원본 ETW의 독립 검증은 수행하지 않았음.
- 신규 추적 86,034행, drop 0 보고. Clock-Time의 FILETIME 가정이 불일치했고 7,196행만 해석, 해당 추적 시간 구간 내 2행. Kernel-Process 시작 payload PID/PPID 위치가 WMI 대조와 불일치. 미끼 이벤트의 시험 프로세스 귀속 미확인.
- ETW=FAIL_UNTRUSTED_MEASUREMENT, C_FINAL_RERUN=NOT_RUN, 운영 state.sqlite3/WAL/SHM/watch.lock 무접근=NOT_PROVEN, C_OVERALL=PARTIAL. 실제 접근이 있었다는 증거로도 해석하지 않음.
- 기존 실제 GitHub GET 3주기/7회 read-only PASS는 이전 보고치이며 이번 최종 C 실측으로 소급하지 않음.
- 운영 watcher 스캔 +10, updater 로그 증가, 같은 프로세스 약 50~55분 유지, 종료코드 0xC000013A 재발 미관측. LONG_RUN=PENDING, 모델 새 호출 0, 비용 $0.
- 사용자 관리자 셸 총 3회 실행(추적 1회, 사전 중단 1회, 재분석 1회). 불필요한 셸 반복은 개선 대상. 추가 관리자 실행을 요청하지 않음.

## 2. GPT 후속 기술 판정
- 원인 미확정: 수집되지 않은 이벤트와 파서가 이해하지 못한 이벤트를 구분하지 못함. 공급자/manifest event ID/ETW clock domain 및 PID/PPID 필드 정의를 호스트 로컬 원본으로 확인해야 함. 임의 timestamp offset으로 허위 PASS를 만들지 않음.
- GPT 보조 코드에서도 수명 밖 이벤트를 조용히 제외할 수 있는 점은 수정 대상. 해당 이벤트의 잠재적 운영 파일 접근은 fail-closed 집계·거부가 필요.
- 문자열 match_path는 8.3/junction/UNC/NT path/hardlink를 해결하지 못함. 호스트 8.3 활성 보고를 고려해 원본 파일 identity 확인 없이 C ETW PASS 금지.
- 관찰 중 실제 운영 DB를 SQLite mode=ro로 열었고 WAL/SHM 영향을 측정하지 않았으므로 이를 완전한 운영 무쓰기 증거로 수용하지 않음. 향후 원본 DB를 직접 여는 관찰은 피할 것.
- ACL 접근거부 및 SHADOW 독립 state 코드 경로는 보완 근거로만 수용하며 ETW PASS나 실제 운영 무접근의 입증을 대체하지 않음.
- 추가 C 실제 계측은 당분간 보류. 필요한 경우 보존한 local-only 원본을 먼저 신뢰 가능한 parser로 오프라인 해독 및 양성 대조 사전 검증 후 별도 명시 승인으로 1회 실시.

## 3. Dropbox LIVE 불필요 의견에 대한 운영 제안
- 사용자는 Dropbox 협업을 더 이상 사용하지 않는다고 명시함. 단 현 Windows 보고에서 watcher v0.1.5는 최근 실제 실행 중이었고, 새 리뷰 호출 0은 '프로세스 중지'와 다름.
- 권고: 즉시 삭제 아닌 사용자 별도 승인에 따른 안전한 Stop + Scheduled Task Disable + ARCHIVE/ROLLBACK 보존.
- 전제: 새 리뷰를 받을 계획 없음 재확인, 활성/불확실 reviewer 작업 및 READY/비용/영수증 무손실 보존, 운영 DB 및 작업 정의 백업·복원 확인, watcher 중단 후 모델 실행 0, 단일 provider 명확화.
- Dropbox watcher만 기본 대상. Dashboard updater, Telegram notifier, Bridge가 공용일 수 있으므로 각 실제 의존성 확인 없이 함께 종료하지 않음.
- Disable 후 GitHub LIVE 승인 전 상태는 ACTIVE_PROVIDER=NONE(자동 리뷰 중단)일 수 있음. GitHub SHADOW는 LIVE가 아님. 운영 전환 게이트 C=PARTIAL, 정식 독립 리뷰=NOT_RUN 유지.
- 사용자 최종 Disable 승인 받기 전에는 예약 작업·운영 DB·키·토큰·작업자 프로세스를 변경하지 않음. 원본 이력/ZIP/DB 삭제 금지.

## 4. 판정과 다음 행동
GPT_DISPOSITION=ACCEPT_WITH_CHANGE; C_OVERALL=PARTIAL_ACCEPTED; ETW=FAIL_UNTRUSTED_MEASUREMENT; WINDOWS_LONG_RUN=PENDING; INDEPENDENT_REVIEW=NOT_RUN; DROPBOX_DISABLE=PROPOSED_NOT_EXECUTED; CUTOVER=MIGRATION_NOT_CUTOVER.
다음 사용자 결정: Dropbox LIVE watcher의 안전한 중지와 예약 작업 Disable을 명시 승인할지 확인. 승인 시 읽기 전용 현장 사전점검→보존/백업→정지/Disable→단일 LIVE 없음과 새 모델 호출 0 검증→PRIVATE 결과 게시까지 원샷. GitHub LIVE 활성화는 승인 범위 밖.
