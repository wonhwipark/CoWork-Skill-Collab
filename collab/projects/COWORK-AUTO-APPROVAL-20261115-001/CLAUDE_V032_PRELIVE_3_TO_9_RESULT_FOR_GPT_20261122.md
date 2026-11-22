# v0.2.32 LIVE 직전 3~9단계 결과 (Windows Claude Code)

- 작성: 2026-11-22 KST. Work: `COWORK-AUTO-APPROVAL-20261115-001`. 지시: `WINDOWS_V031_TO_LIVE_PRECHECK_ONE_SHOT_HANDOFF_r0001_20261122_KST.md`.
- 출발 후보: v0.2.31 ZIP `1df85457…`(CRC/entries 재검증 PASS). v0.2.31 폴더·ZIP 불변, v0.2.32 작업 폴더에서 연속 개발.
- **STATUS: LIVE_READY=NO.** 개발·시험·패키징·읽기 전용 SHADOW(사본)·백업 복원 시험은 완료. 독립 리뷰는 보호 승인 부재로 BLOCKED, 운영 SHADOW 설치와 SCOPE 활성화 키는 승인 전이라 NOT_RUN/BLOCKED.

## 1. 단계별 결과

| 단계 | 항목 | 결과 | 근거 |
|---|---|---|---|
| G3_RACE | 두 독립 watcher(서로 다른 DB)가 같은 DISPATCH 기록에 정확히 동시 진입 | PASS | `test_two_watchers_racing…`: barrier 동시 진입, 실제 runner 합계 1, 지는 쪽 REVIEW_UNCERTAIN 봉인. 5회 반복 전부 PASS |
| G3_RACE | 응답 유실 후 같은 DB 재스캔 | PASS | `test_lost_reservation_response_retries_once…`: 불명 상태 중 모델 0, 이후 생애주기 모델 호출 정확히 1 |
| G3_RACE | 응답 유실 기록을 새 DB watcher가 봄 | PASS | `test_lost_reservation_seen_by_a_fresh_watcher…`: 모델 0, REVIEW_UNCERTAIN 봉인 |
| G3_RACE | 원격 claim 확인 자체 실패 | PASS | `test_reservation_that_could_not_be_written…`: 모델 0 |
| G3_RACE | 동일 ID 다른 ZIP / 이미 완료 ID | PASS | 기존 `test_same_revision_with_another_package…`(CONFLICT), `test_result_already_published…`(재리뷰 0) |
| G4_RECOVERY | 클레임 후 crash → 재시작 → 봉인 | PASS | `test_crash_after_the_claim…`: `seal_interrupted` 후 REVIEW_UNCERTAIN 1, 재실행 0 |
| G4_RECOVERY | 시간 초과·신호 종료·exit 1 (모델 시작 후) | PASS | 파라미터 3건: 터미널 FAILED/UNCERTAIN, 3회 스캔 모델 1회 |
| G4_RECOVERY | 결과 업로드 실패 후 게시만 재시도 | PASS | v0.2.31 시험 PASS, 모델 재호출 0 |
| G4_RECOVERY | 과거 레코드·구 필드 호환 | PASS | 전체 스위트 내 `test_phase4_unattended`(구 `max_budget_usd` 행) PASS |
| G4_RECOVERY | 위조·만료·repo 불일치·변조 | PASS | 기존 승인 시험군 PASS, 신규 의도 검증 시험 25건 PASS |
| G5_SCOPE_DESIGN | 사용자 의도 계약 | PASS(설계) | `REVIEW_INTENT_V1`: 전용 키 목적 `REVIEW_INTENT`, repo/request/revision/skill/commit/REQUEST·ZIP SHA/크기 바인딩, 최대 7일, 1회용 nonce, 와일드카드 금지, GitHub 본문 승인 불인정 |
| G6_SCOPE_CODE | 격리 검증 구현 | PASS(격리) | `skill_collab_watcher/review_intent.py` + 시험 25건 PASS. 승인 경로 `assess`에는 **연결하지 않음**(입장 규칙 불변) |
| G6_SCOPE_CODE | 활성화 | BLOCKED_AUTH_DESIGN | 현재 trust root에 `REVIEW_INTENT` 목적 키가 없음. 키 생성·trust root 변경은 승인 필요, 이번에 생성하지 않음 |
| G7_PACKAGE | 전체 회귀 | PASS | 994 PASS / 0 FAIL / 12 SKIP (v0.2.31 960 + 신규 34) |
| G7_PACKAGE | 패키징·무결성 | PASS | 아래 §4 |
| G8_INDEPENDENT_REVIEW | 보호 승인 기반 독립 리뷰 1회 | BLOCKED_AUTH | v0.2.32 패키지에 대한 유효 보호 승인·위임 없음. 신규 REQUEST는 코드 ZIP을 PUBLIC 저장소에 올려야 하는데 이는 허용되지 않음. 유료 호출·서명·READY 0 |
| G9_SHADOW | 읽기 전용 SHADOW(라이브 DB 사본, 모델 0, 쓰기 차단 전송) | PASS(사본 한정) | 아래 §5 |
| G9_SHADOW | 호스트 실운영 SHADOW(설치·Task 추가) | NOT_RUN | 새 설치·Task 승인 필요. 사본 시뮬레이션을 실운영 PASS로 표시하지 않음 |
| BACKUP | DB·설정·위임 백업 번들 + 복원 시험 | PASS | `backup_v0_2_29_precheck_20261122\`, integrity ok, 작업 12, 감사 최대 id 22804 |
| BACKUP | 설치 트리 사본(v0.2.29) | NOT_DONE | 복사 명령이 권한 계층에서 거부됨. 우회하지 않음. LIVE 전 필수 |

## 2. 동시성·복구 설계 메모

- 원격 디스패치 기록(`dispatch/<id>/DISPATCH_<rev>.md`, create-only)이 원자적 claim 역할을 한다. 승자만 모델을 시작하고 패자는 봉인된다.
- 응답 유실 후 같은 DB의 재시도는 `ALREADY_OURS`로 1회 디스패치될 수 있다. 이 경우 첫 시도는 모델 시작 전에 `ERROR`로 끝났으므로 생애주기 모델 호출은 1회다. 다른 DB watcher가 같은 기록을 보면 봉인된다.
- **한계:** 모의 전송의 create-only 원자성은 잠금으로 흉내 냈다. 실제 GitHub의 원자성은 서버 측 규칙이며 이번 단계에서 원격 쓰기로 재검증하지 않았다(쓰기 금지).

## 3. 검증 기준 정직성

- 개발 세션의 자체 시험은 독립 리뷰가 아니다.
- 시험은 가짜 runner와 인메모리 전송만 사용. 실제 `claude` 호출 0.
- 실제 원격 쓰기 0, 운영 DB 쓰기 0, Telegram 0.

## 4. 패키지

- 작업 폴더: `D:\User\whpark\skill-collab-watcher-dist\candidates\v0_2_32_live_precheck\`
- ZIP: `D:\User\whpark\skill-collab-watcher-dist\candidates\v0_2_32_live_precheck_candidate.zip`
- **SHA-256 `cbf95d1141cbed6973d6cace2950065b4ed5eb36e988ecf522a9fc3ab087fa94`**, **295,885 B**, 106 항목
- 트리 SHA-256 `644eaf61e33c1430fa7d90b18df9d5cc28eacf24f955c5acb916a2e9d253e9cd`
- 검사: CRC 정상, 중복 없음, 경로 탈출 0, 심볼릭 링크 0, 민감정보 패턴 0
- 이전 v0.2.31 ZIP(`1df85457…`)과 v0.2.30 ZIP(`541cd3f1…`)은 변경 없음.
- 코드 ZIP은 PUBLIC 저장소에 게시하지 않았다.

## 5. SHADOW(사본) 결과

- 라이브 DB를 백업 API로 **읽기 전용 복제**하여 사본에 기록. 전송은 쓰기 계열 호출을 차단하는 래퍼. `allowed=False`, 모델 실행기는 호출 시 예외.
- 결과: `dispatched=0`, `pending=8`, 모델 호출 0, 쓰기 차단 0건 발생.
- 라이브 감사 최대 id: 실행 전 22803 → 실행 후 22803 (라이브 쓰기 없음). 백업 시점 22804.

## 6. 라이브 현황(읽기 전용 검증, 2026-11-22 16:39)

- 설치본 v0.2.29, 트리 SHA `b0134258…` 불변. 설정 `2ead4007…`, 위임 `6d826672…` 불변.
- Task: `SKILL-COLLAB-GitHub-Watcher` Running, `SKILL-COLLAB-Notifier` Running, 나머지 Disabled. pythonw PID 30904/31848.
- 기준선 이후 디스패치 2→3(우리 R1 1건). 검증기 `model_calls_new` 4→6은 리뷰 1건당 카운터 2증가로 설명됨. 추가 모델 호출 없음.
- `FINAL_LIVE_STATE_OK=false`는 기준선 이후 새 이벤트와 요청 폴더 변화 때문이며 운영 이상은 아니다.

## 7. LIVE 준비 판정과 남은 승인 항목

LIVE_READY = **NO**. 막힌 항목:
1. 보호 승인 기반 독립 리뷰 1회(G8) 미실행 — 승인·위임 필요.
2. `REVIEW_INTENT` 목적 키 생성과 trust root 변경(G6 활성화) — 별도 승인.
3. 설치 트리(v0.2.29) 백업 사본 — 권한 거부로 미생성, LIVE 전 필수.
4. 호스트 실운영 SHADOW — 설치·Task 승인 필요.
5. 비용 무상한 위험 수용 — 사용자 결정(10단계).

## 8. 롤백 절차(초안)

1. 후보 설치 시 Task 중지 → 기존 설치 트리 복원(3번 백업 선행) → `state.sqlite3`는 워처 정지 상태에서 백업 번들로 교체 → 설정·위임 해시 확인 → Task 시작 → 버전 0.2.29, `WATCH_START` 확인.
2. 과거 요청 재큐잉 금지, 알림 중복 0 확인.

## 9. NEXT_ONE_ACTION

GPT 판정 후 사용자에게 다음 4개를 한 번에 제시: (a) 비용 무상한 위험 수용 여부, (b) 설치 트리 백업 생성 승인, (c) `REVIEW_INTENT` 키 생성·trust root 변경 승인 여부, (d) 독립 리뷰 1회를 위한 보호 승인 발급 여부. 이 중 하나라도 불승인이면 LIVE는 진행하지 않는다.
