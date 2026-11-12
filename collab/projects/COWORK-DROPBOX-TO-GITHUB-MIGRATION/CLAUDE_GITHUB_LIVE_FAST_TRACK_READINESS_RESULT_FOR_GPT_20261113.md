# CLAUDE GitHub LIVE 최소 반복 통합 실행 결과 (GPT용) 2026-11-13

실행 기준: `GPT_GITHUB_LIVE_MINIMUM_REWORK_MASTER_r0001_20261113.md` 하나. 성격: Windows Claude Code **자체 시험·실측 보고(SELF_TEST_REPORTED)**, 독립 리뷰 아님. 관리자 셸 실행 0회, 새 ETW 추적 0회, 운영 DB 열기 0회.

## 1. 필수 필드

| 필드 | 값 |
|---|---|
| ACTIVE_PROVIDER | **NONE** (감시기·Bridge·갱신기 Disabled, 알림기만 Running; 읽기 전용 재확인 §2) |
| CURRENT_BASELINE | v0.2.10 로컬 ZIP 174745 B / 70항목 / SHA-256 `67ea7fc63ccc1de77a28025b7c4f1b701ee6f4fa387311bca3f3d2bc7432b108` (이번 세션에서 로컬 재해시 일치, 원격 미게시) |
| EVIDENCE_REUSED | §3 |
| DELTA_TESTS_RUN | §4 (ETW 사전검증 r0002 신규 20 PASS, 롤백 리허설 v0.2.10 재실행, 게이트별 기존 시험 집계) |
| C_ETW | **FAIL_UNTRUSTED_MEASUREMENT 유지** (새 측정 0회). 코드 결함 수정은 완료(§4-1), 호스트 해석 실패(시간 열)는 미해결 |
| C_ALT_EVIDENCE | **PROPOSED_ONLY** (§6). 계약 변경 승인 전 C PASS로 승격하지 않음 |
| B_OPERATING_SIGNER | **BLOCKED_SIGNER_DEVICE** (운영 키 생성·개인키 수령·root 설치 0) |
| D_EXPORT | **BLOCKED_EXPORT_CLASSIFICATION** (ZIP 게시 0) |
| E_INDEPENDENT_REVIEW | **NOT_RUN** (REQUEST/READY 0, 모델 호출 0) |
| CLEANUP_CANDIDATES | Bridge·갱신기는 이미 별도 승인으로 Disabled(2026-11-13 결과 참조). 이번 세션 추가 중지 0 |
| LIVE_HOST_INSTALL | NOT_RUN / NOT_APPROVED |
| ROLLBACK | **PASS_SYNTHETIC_ON_SNAPSHOT_COPY** (§5). 실운영 롤백은 NOT_RUN |
| MODEL_NEW_CALLS | 0 |
| USD_SPEND | 0 |
| HARD_GATE_APPROVALS_NEEDED | §7 한 묶음 |
| NEXT_ONE_ACTION | §7 승인 패킷에 대한 사용자 응답(우선 B 서명자 기기 지정과 D 반출 확인 두 가지) |
| CUTOVER | MIGRATION_NOT_CUTOVER |

## 2. 증거 ledger (재검증 포함)

| Gate | InputArtifact | Evidence | Result | Blocking reason | Owner | Next |
|---|---|---|---|---|---|---|
| 기준선 | v0.2.10 ZIP (로컬) | 이번 세션 재해시 174745 B/70항목 일치 | PASS_REUSED+재확인 | - | Claude | - |
| 호스트 상태 | 작업 4개 + DB 파일 메타데이터 | 읽기 전용 재조회: 감시기·Bridge·갱신기 Disabled, 알림기 Running, 시험 계정 비활성. 운영 DB는 열지 않고 메타데이터만 확인 | PASS(HOST_REAL) | 재부팅/재로그인 후 지속은 여전히 NOT_RUN | Claude | 사용자 시점 재확인 |
| A 비관리자 ACL | Stage 1 결과 | 재실행 안 함 | PASS_REUSED (HOST_REAL) | - | - | - |
| 실GitHub GET-only | 이전 호스트 보고 | 재실행 안 함 | PASS_REUSED (HOST_REAL_REPORTED) | - | - | - |
| C ETW | GPT r0001 코드, 호스트 보고 | 코드 결함 수정(r0002)+시험. 호스트 측정은 새로 하지 않음 | PARTIAL | 시간 열 해석·PID 귀속 미해결 | GPT 판정 | §6, §7 |
| B | 시험키 시험 | 서명·root 도구 시험 reuse | PASS_SELF_TEST_REPORTED(시험키) | 실운영 키 BLOCKED | 사용자 | §7 |
| D | ZIP 70항목 | 출처 매트릭스 §8 | BLOCKED | 34개 유래 코드 반출 확인 없음 | 사용자/조직 | §7 |
| E | 합성 dry-run | §4-3 | NOT_RUN(실 리뷰) | B·D·runner·비용 승인 | 사용자 | §7 |
| 롤백 | 스냅샷 격리 사본 | v0.2.10으로 재실행 §5 | PASS_SYNTHETIC | 실운영 NOT_RUN | Claude | LIVE 승인 후 |

## 3. 재사용한 증거 (재실행하지 않음)
Dropbox 감시기 Disable 결과, Bridge·갱신기 정리 결과, 의존성 감사, A 비관리자 ACL·시험키 보안시험, 실GitHub GET-only 3주기/7회 보고, 이전 31개 ETW 보조 시험 보고, v0.2.10 전체 시험(venv 527 passed/12 skipped, 운영 인터프리터 492 passed/14 skipped; 이번 세션 앞부분 실행). v0.2.10 코드는 이번에 바뀌지 않았다(변경은 패키지 밖 진단 도구뿐).

## 4. 이번에 수정·시험한 delta

### 4-1. ETW 사전검증 `etw_attribution_preflight_r0002` (GPT 원본 r0001 보존, 별도 파일)
GPT 원본 코드와 시험 9개는 SHA 일치 확인 후 **그대로 9 PASS**. 호스트 보고가 지적한 결함을 신규 r0002에서 수정:
1. **수명 밖 이벤트 침묵 제외 → 오류화**: 탐침 계통 PID의 이벤트가 그 프로세스 수명 밖이면 `EVENT_OUTSIDE_PROCESS_LIFETIME`(사전검증 실패). 탐침 구간 밖의 계통 이벤트는 개수를 세고 보호 경로 적중도 검사.
2. **8.3 짧은 이름**: 확장 후 비교(`GetLongPathNameW`, 존재하는 가장 가까운 상위로 확장). 확장 불가한 짧은 이름이 보이면 격리 결과 `NOT_PROVEN`. 이 호스트 볼륨은 8.3 이름이 켜져 있어 실제 Windows 시험이 건너뛰지 않고 PASS.
3. **파일 identity**: `events[].file_id`와 `protected_file_ids`로 하드링크·junction 별칭 적중 검출(실제 NTFS 하드링크 시험 PASS). 모든 파일 이벤트에 identity가 없으면 최상위 결과를 `NO_ACCESS_EVENTS_BY_PATH_ONLY_ALIAS_NOT_PROVEN`으로 낮춰 별칭 안전을 주장하지 않는다.
- 시험: r0002 **20 PASS**(기존 9 동작 유지 + 신규 9 + 실Windows 2). 변환기(tracerpt → 정규화)는 포함하지 않으며 호스트 검증이 필요하다. 게시 파일은 `tools/`에 신규 추가(add-only).

### 4-2. TRACKER.json 값 오류 수정 (이전 세션 결함)
기존 값 `phase=DROPBOX_BRIDGE_UPDATER_DISABLED`, `self_test=SELF_TEST_REPORTED`는 대시보드 검증기 허용 enum(phase: REQUIREMENT/DEVELOPMENT/REVIEW/DISPOSITION/COMPLETE/BLOCKED/UNKNOWN, self_test: PASS/FAIL/SKIP/NOT_RUN/NOT_VERIFIED) 밖이라 등록 전체가 무시되고 CURRENT 카드로만 표시되었을 가능성이 크다. 실제 검증기(`work_tracker._registered`)로 수정 전 거부·수정 후 수락을 확인하고 `phase=BLOCKED`, `self_test=PASS`(개발자 자기 신고, 독립 리뷰 아님), `independent_review=NOT_RUN`으로 정정했다.

### 4-3. E 합성 dry-run (실제 READY·모델 호출·결제 0)
기존 시험 매핑(이번 세션 v0.2.10 현재 코드로 실행, 전부 PASS): 서명 도구 17, 비용·예산·상한 41, nonce·replay·만료 12, 승인 철회·롤백·버전 래칫·동결 6, 논리적 중복 요청 3, REVIEW_UNCERTAIN 봉인 3, 제공자 단일 LIVE·lease 23, 알림 워터마크·부트스트랩 3. 이는 합성·시험키 증거이며 독립 리뷰가 아니다.

## 5. LIVE 롤백 설계 시험 (격리 스냅샷 사본, 원본 불변)
v0.2.10으로 재실행(스냅샷은 운영 DB의 일관된 사본 하나이며 현재 운영 DB와는 시점이 다르다):
- 이행: 새 테이블 3개 추가, integrity ok, 기존 행 보존. 두 번째 LIVE 제공자 거부, 미정산 백로그에서 전환 거부, 전환 시 PENDING_HELD 기록.
- 실GitHub GET으로 스캔(모델 0, 디스패치 0): Dropbox 백로그·커서 불변. 완료 이력은 새 정책 revision에서도 재처리되지 않음(동일 요청 재처리 0).
- 롤백: epoch 증가, Dropbox 백로그 동일, 제공자 lease 정확히 1개. 알림기는 부트스트랩 전 발송 거부, 부트스트랩 후 중복 0. 두 번째 열기 멱등.
- 복원: 이전 버전(v0.1.5)이 이행본·복원본을 모두 열 수 있음, 스냅샷 바이트 해시 복원 동일, 스냅샷 원본 불변.
- 한계: 운영 DB·예약 작업·원본 감시기는 건드리지 않았으므로 **실운영 설치/복원은 NOT_RUN**.

## 6. C 처리 방안
- **C_ETW (엄격 계약)**: 남은 장애는 도구가 아니라 호스트 추적의 시간 열 해석이다. 가능한 경로: 보존된 원본 ETL을 `Get-WinEvent -Path`로 해독하거나 프로세스 시작 payload의 ISO 시각으로 시간열을 보정해 1회 재분석(새 추적 없음). 이 재분석은 관리자 셸 1회가 필요하므로 이번에는 요청하지 않았다.
- **C_ALT_EVIDENCE=PROPOSED_ONLY**: ETW 대신 독립 증거 4종 — ①SHADOW 전용 state dir와 경로 가드 ②Windows ACL(비관리자 계정이 운영 폴더에 들어갈 수 없음, Stage 1 HOST_REAL) ③파일 identity(가드의 identity 비교, 호스트 결함 2건 수정) ④정적 호출 경로. 한계: 코드가 열지 않는다는 증명이 아니라 OS가 열 수 없게 막는다는 증명이다. 수락 기준 변경으로 보이므로 GPT와 사용자의 최종 승인 전에는 C PASS로 쓰지 않는다.

## 7. 사용자 승인 패킷 (무응답은 승인 아님, 항목은 서로 독립)

| gate | 승인에 필요한 입력·행동 | 승인 전 상태 |
|---|---|---|
| B | 감시기 PC와 **다른 기기**를 승인자 장치로 지정, 그 기기에서 사용자가 직접 Ed25519 키 생성(§9 체크리스트). 공개키+pin만 이 PC 관리자 전용 폴더에 설치하는 것을 별도 승인 | BLOCKED_SIGNER |
| C | 다음 중 택1: (a) 보존 ETL 재분석 1회 + 통과 시 실측 1회(관리자 셸 1회) (b) ETW 없이 C_ALT_EVIDENCE를 수락 기준으로 승인 | PARTIAL |
| D | 34개 유래 파일(§8)의 소유·외부 반출 가능 여부 확인. 불가하면 대안 선택: (i) 신규 24개만 게시 (ii) 요약·설계 자료만 | BLOCKED_EXPORT |
| E | B·C·D 충족 후 독립 runner·STATIC $1 상한·REQUEST/READY·receipt 승인 | NOT_RUN |
| 읽기 전용 토큰 | 이 저장소 전용 Contents:Read-only 토큰을 사용자가 직접 발급해 시험 계정 전용 위치에 설치(채팅 금지). 이전 요청에서 보류됨 | BLOCKED_CREDENTIAL |
| Cleanup | Bridge·갱신기는 이미 완료. 알림기의 GitHub 알림 경로 이행·유지 결정 | 사용자 결정 |
| LIVE | Windows GitHub 감시기 설치, DB·알림 이행, 운영 롤백 준비, 단일 제공자 활성화 | NOT_APPROVED |

## 8. D — 파일 출처 매트릭스 (이번 세션 해시 비교)
v0.2.10 ZIP 70항목을 운영 v0.1.5 폴더와 SHA-256으로 비교: **UNCHANGED 34 / CHANGED 12 / NEW 24**.
- UNCHANGED 34 = `skill_collab_watcher` 8(auth_flow, dropbox_transport, lock, mock_transport, models, secret_prompt, secrets_store, watch_loop) + `tests` 17 + `windows` 5 + `config` 1 + `prompts` 1 + `tools` 1(빈 `__init__`) + 루트 1(requirements). **v0.1.5 유래, 반출 승인 필요.**
- CHANGED 12 = `skill_collab_watcher` 10 + `tests` 1 + `tools` 1. v0.1.5를 수정한 파생물이라 원 소유권이 그대로 적용될 수 있어 반출 승인 필요 대상으로 취급.
- NEW 24 = `tests` 15 + `skill_collab_watcher` 5 + `tools` 2 + `docs` 1 + 루트 1. 이 협업에서 AI 세션이 작성한 파일. 단, 소유·반출 정책 확인은 사용자 몫.
- 자동 secret·개인정보 스캔 0건은 반출 허가가 아니다. 허가 없이는 ZIP 전량 PRIVATE 업로드 금지.
- 독립 리뷰 가능 범위 제안(허가 전): 허가된 NEW 24개와 설계·시험 결과 요약만으로 "부분 검토"가 가능하나, 이는 전체 ZIP 독립 리뷰 PASS가 아니다.

## 9. B — 운영자 실행 체크리스트 (운영 키 생성 금지, 실행은 사용자 장치에서)
1. 승인자 기기 지정(감시기 PC가 아님). 개인키는 그 기기 밖으로 나가지 않는다(GitHub·채팅·로그·이 PC 금지).
2. 그 기기에서 이 ZIP의 `tools/approval_signer.py keygen`으로 키 생성. 출력의 **공개키·지문**만 옮긴다.
3. `tools/trust_root_tool.py`로 trust root(버전 1, 키 ACTIVE) 작성 → 파일 SHA-256 pin 계산.
4. 이 PC 관리자 전용 폴더(상속 제거, 관리자만 쓰기)에 root·pin·config 배치. 비관리자 시험 계정이 읽기만 가능함을 A와 같은 방법으로 실측(`TRUST_ROOT_LOADED` 대 `NOT_INDEPENDENT` 대조).
5. 서명 계약: 승인은 요청 ID·ZIP SHA·고정 커밋·정책·비용 상한·nonce·만료를 모두 서명 대상에 포함. 문장 텍스트를 그대로 신뢰하지 않는다. 시계 역행·replay·폐기 키·버전 롤백은 시험으로 거부 확인됨(§4-3).
6. 시험키는 운영 서명으로 쓰지 않는다. 키 분실·유출 시 폐기는 root 버전을 올려 대응.

## 10. 보호 범위와 한계
- 운영 watcher·DB·작업·Bridge·알림기·인증·토큰 변경 0, 새 모델 호출 0, USD 0, Telegram·REQUEST/READY 게시 0. 추가된 것은 로컬 시험 도구·이 결과·ETW 진단 도구 사본뿐. 시험 계정 비활성·샌드박스 보존 유지.
- 이 결과는 자체 보고이며 독립 리뷰가 아니다. LIVE 전환은 하지 않았고 `ACTIVE_PROVIDER=NONE`, `MIGRATION_NOT_CUTOVER`다.
