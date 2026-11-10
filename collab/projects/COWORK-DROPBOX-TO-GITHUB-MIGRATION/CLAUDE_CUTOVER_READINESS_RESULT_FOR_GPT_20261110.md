# CLAUDE CUTOVER READINESS 결과 (GPT 확인용) 2026-11-10

- 작업 ID: COWORK-DROPBOX-TO-GITHUB-MIGRATION
- 인계서: GPT_V0_2_2_DISPOSITION_AND_CUTOVER_READINESS_ONE_SHOT_r0001_20261110.md (PRIVATE main에서 읽음)
- 처리 방식: NO_PR. 격리 복사본에서만 수정. 운영 watcher, 운영 DB, 예약 작업, Telegram, Bridge, Dashboard는 변경하지 않음.
- 증거 수준: SELF_TEST_REPORTED. 같은 개발 세션의 자체 시험이며 정식 독립 리뷰가 아님. INDEPENDENT_REVIEW=NOT_RUN.
- 모델 리뷰 호출: 0회 (FakeReviewRunner만 사용). 실제 Telegram 발송: 0회 (가짜 발송기만 사용).
- 이전 보고와의 관계: PRIVATE main의 CLAUDE_PHASE2_END_TO_END_RESULT_FOR_GPT_20261110.md는 v0.2.1 기준이며 그대로 보존. v0.2.2의 상세 리허설 보고는 게시된 적이 없어 §2에 통합.

CUTOVER_READINESS_STATUS: PARTIAL
사유: C-1, C-2, C-3, C-5는 해결·검증. C-4(Dropbox 실샘플 대조)는 NOT_RUN. 실 Telegram, 호스트 SHADOW, 독립 리뷰, 운영 LIVE 승인은 범위 밖이라 미실행.

## 1. 시작 기준 대조
- v0.2.2 ZIP 실측: 126,729 bytes, SHA-256 7ec4f63e175b582ceec1f809281fba003f4248331a3f296689e7e19981323410. GPT가 받은 보고값과 일치.
- v0.2.0 (1003c1ab…, 108,936 B), v0.2.1 (d1e612fe…, 125,653 B), v0.2.2는 작업 종료 시점에도 원래 해시 그대로 (불변 보존).
- 환경: Windows 11, CPython 3.11. 시험은 격리 가상환경(운영 venv 아님)에서 실행.

## 2. v0.2.2 리허설에서 발견·수정한 결함 (이전에 미게시된 내용 통합)
1. 읽기 전용(SHADOW) 조회가 DB 메인 파일을 바꿈. 원인: WAL 상태 DB를 일반 연결로 열고 닫으면 체크포인트가 메인 파일을 씀. 수정: mode=ro URI로 열고 query_only 유지. 회귀 시험: test_shadow_open_leaves_the_database_file_unchanged_while_wal_is_pending.
2. 제공자 간 커서 공유. 원인: GitHub 조회 후 Dropbox 커서 자리에 커밋 SHA가 저장되어 롤백이 깨짐. 수정: 제공자별 커서 키 (github:<repo>:<branch>), Dropbox는 기존 키 유지. 회귀 시험: test_cursor_is_scoped_per_provider.

## 3. 새 blocking C-1 ~ C-5 처리
| ID | 판정 | 조치 | 증거 |
|---|---|---|---|
| C-1 | 해결 (합성 + 실제 DB 사본 리허설) | 원인: GitHub 스캔이 Dropbox 대기 요청 ID를 같이 훑고, GitHub에 폴더가 없자 삭제된 것으로 보고 제거. 수정: 대기 목록을 제공자별 범위로 분리 (스키마 변경 없음, Dropbox는 기존 무접두 ID, 그 외는 "<제공자>:<ID>"). 전환은 이탈 제공자에 미정산 대기가 있으면 거부, hold_pending=True일 때만 허용하며 보류한 ID를 PENDING_HELD로 감사 로그에 기록. reconcile 명령(읽기 전용)과 reconciliation_manifest 추가. | 시험 7건 (test_C1_*). 리허설: 정산 없이 전환 거부, 보류 전환 후 GitHub 스캔·롤백 뒤에도 Dropbox 대기 ID 동일, 롤백 후 Dropbox 스캔이 보류 요청을 정확히 1회만 처리 |
| C-2 | 해결 (합성 + 실제 DB 사본 리허설) | 알림 위치를 제공자+epoch별 워터마크로 관리. 초기화(bootstrap) 없이는 아무것도 보내지 않음(NotifyNotInitialized). 운영 notifier가 이미 도달한 last_id를 시작점으로 이어받을 수 있어 이미 보낸 과거는 재전송하지 않고, 그 이후 미발송분은 건너뛰지 않음. 건마다 상태 저장, 발송 실패 시 워터마크 불변. | 시험 14건. 리허설: 사본 이력에 알림 대상 66건, bootstrap 후 첫 실행 재전송 1건 (그 1건은 리허설이 만든 PENDING_HELD), 초기화 안 한 상태는 발송 거부 |
| C-3 | PASS (REAL, 시험 키) | 격리 가상환경에만 cryptography 50.0.2를 해시 고정(--require-hashes) 설치. 시험용 Ed25519 키쌍은 시험마다 메모리에서 생성하고 개인키는 어디에도 저장하지 않음 (신뢰 루트 파일에는 공개키만, pytest 임시 폴더). 운영 신뢰 루트·키 미생성. | test_phase2_ed25519.py 19건 전부 통과 |
| C-4 | NOT_RUN | 로컬 Dropbox 동기화 폴더에 SKILL-COLLAB 사본이 없음 (원격 API 전용). 원격 읽기는 보호된 운영 자격 증명 파일이 필요해 우회하지 않음. 대체 근거: (a) v0.1.5 해시 방식이 엄격 UTF-8 decode 후 encode이므로 유효 UTF-8에서는 원본 바이트와 같음을 코드로 확인, (b) 무작위 2,000개 문서 속성 시험 통과 (CRLF, BOM 문자, NUL, 이모지 포함), (c) 유효하지 않은 UTF-8은 두 방식 모두 호출 전에 거부. | test_B6_legacy_text_hash_equals_stored_byte_hash_for_any_valid_utf8_document 외 3건. 실제 샘플 대조 스크립트는 준비되어 있음 |
| C-5 | PASS (사본) | 운영 DB는 SQLite 온라인 백업 API로 읽기 전용 연결에서 사본 확보 (백업 전후 메인 파일 해시·크기·mtime 불변). 사본에서만 이행·검증. 백업은 운영 데이터를 담아 로컬에만 보관, 게시하지 않음. | 아래 §6 |

## 4. 실제 변경 (diff 요지, v0.2.2 → v0.2.3, 파일 11개 변경 / 추가 0 / 삭제 0)
- state_store.py: pending_scope와 범위별 add/remove/list_pending, reconciliation_manifest, switch_provider(hold_pending), 읽기 전용 mode=ro.
- transport_base.py / github_transport.py: provider_name 속성 (dropbox 기본, github 재정의).
- orchestrator.py: 스캔 시작 시 pending_scope를 전송 계층 이름으로 설정.
- cli.py: 읽기 전용 reconcile 명령 추가, 커서 키를 전송 계층에서 가져옴.
- notify_events.py: 워터마크 모델, bootstrap, read_legacy_last_id, 건별 persist, PENDING_HELD 알림.
- __init__.py: 0.2.2 → 0.2.3.
- 시험: test_phase2_cutover, test_phase2_notify (재작성), test_phase2_ed25519 (확장), test_phase1_blocking_fixes (B-6 속성 시험).

## 5. 시험 결과
### 5.1 전체 pytest
- 명령: 격리 가상환경의 python -m pytest tests -q (캐시·바이트코드 미생성)
- 결과: 348 PASS / 0 FAIL / 12 SKIP. 후보 ZIP을 풀어 낸 사본에서도 동일 (348 / 12).
- 이전 보고(314 PASS / 13 SKIP) 대비: PASS +34, SKIP -1.
  - SKIP 감소 1건 = 이전에 cryptography 미설치로 모듈째 건너뛰던 test_phase2_ed25519가 실행됨 (19건 전부 통과).
  - 남은 SKIP 12건: GUI 실창 시험 8건 (SKILL_COLLAB_GUI_TESTS=1 옵트인), Windows 스크립트 시험 4건 (프로젝트 .venv 폴더가 있을 때만 실행). 기준 236/8과의 차이도 이 4건으로 설명됨.
- 변이 시험과 커버리지 측정은 수행하지 않음.

### 5.2 실제 GitHub 읽기 전용 (PRIVATE 저장소, GET만)
- ensure_auth, 커밋 ETag 조건부 읽기, 고정 커밋의 목록(12개 파일)과 파일 다운로드, 없는 경로의 fail-closed, 과거 커밋 기준 변경 목록 5건, 모두 정상. 쓰기 호출 없음. github_readonly_real = PASS.
- 점검 스크립트의 하드코딩된 CURRENT.md blob 해시 비교만 False였음: 그 사이 CURRENT.md가 갱신되어 상수가 낡았기 때문이며 어댑터는 매 읽기마다 blob 해시를 직접 검증함.

### 5.3 인수시험 T01~T38, S01~S10 (PASS(REAL) / PASS(SYNTH) / PARTIAL / NOT_RUN)
| ID | 상태 | 근거 |
|---|---|---|
| T01 | PASS(SYNTH) | 패키지만 있음, 호출 0 |
| T02 | PASS(SYNTH) | REQUEST만 있음, 호출 0 |
| T03 | PASS(SYNTH) | READY가 패키지보다 먼저 보임, 재시도, 호출 0 |
| T04 | PASS(SYNTH) | READY.request_sha256 불일치, 호출 0 |
| T05 | PASS(SYNTH) | 크기/SHA/CRC 손상 3건 |
| T06 | PARTIAL | 해시 누락·형식 오류·고정본 불일치. revision 필드는 V1에 없음 |
| T07 | PASS(SYNTH) | 새 request_id는 자체 승인 필요 |
| T08 | PASS(SYNTH) | 같은 ID+revision에 다른 ZIP, CONFLICT, 기존 보존 (Dropbox 형식 모의 전송) |
| T09 | PARTIAL | 측면 ref의 READY는 읽지 않음. PR/포크/이슈/태그는 모델링하지 않음 |
| T10 | PASS(SYNTH) | 승인된 READY 1회 호출 |
| T11 | PASS(SYNTH) | 반복 조회·재시작 후 호출 1회 유지 |
| T12 | PASS(SYNTH) | 봉인 후 재호출 0, 불확실 알림 1회 |
| T13 | PASS(SYNTH) | 게시 503 후 업로드만 재시도 |
| T14 | PASS(SYNTH) | RECEIPT 누락, UPLOAD_PENDING, 완료 알림 0 |
| T15 | PASS(SYNTH) | 다른 작업의 영수증, CONFLICT |
| T16 | PASS(SYNTH) + 실 GitHub 읽기 | 고정 커밋 읽기, 변조 blob 탐지(합성). 실제 고정 읽기는 §5.2 |
| T17 | PASS(SYNTH) | add-only, 422 충돌, 덮어쓰기 0 |
| T18 | PASS(SYNTH) | 자격 없음/403/404/429/네트워크/401 |
| T19 | PASS(SYNTH) | 자식 프로세스로 실제 교차 프로세스 잠금, 스캔 중첩 시 호출 0 |
| T20 | PASS(SYNTH) | SHADOW: 모델 0, DB 메인 파일 불변(실제 WAL DB 사본), 원격 쓰기 0, 알림 0. 호스트 SHADOW는 NOT_RUN |
| T21 | PASS(SYNTH) + 사본 리허설 | 전환 뒤 완료 작업 재호출 0, 보류 대기 요청 보존 |
| T22 | PASS(SYNTH) | 완료 알림 1회. 실제 휴대폰 수신은 미확인 |
| T23 | NOT_RUN | 워처가 mode를 읽지 않음 (정적 확인만) |
| T24 | PASS(SYNTH) | 기존 예산 단계 회귀 시험 |
| T25 | PASS(SYNTH) | 경로 이탈, 심볼릭 링크, 자격증명 형태 텍스트 |
| T26 | NOT_RUN | 공개 게시 경로 없음 |
| T27 | NOT_RUN | Dashboard 소스가 복사본에 없음 |
| T28 | NOT_RUN | 공개 게시 경로 없음 |
| T29 | PASS(SYNTH) + 사본 리허설 | 롤백 후 활성 lease 1건, 이력 3행, 커서 보존 |
| T30 | NOT_RUN | 플랫폼 속성, 범위 밖 |
| T31 | NOT_RUN | 공개 게시 경로 없음 |
| T32 | NOT_RUN | 공개 배포 경로 없음 |
| T33 | NOT_RUN | 공개 배포 경로 없음 |
| T34 | NOT_RUN | 공개 배포 경로 없음 |
| T35 | NOT_RUN | 공개 배포 경로 없음 |
| T36 | NOT_RUN | 공개 배포 경로 없음 |
| T37 | NOT_RUN | 권한 환경 필요 |
| T38 | PARTIAL | 빌드 비밀 검사 60파일 0건. 공개 게시 차단 장치 없음 |
| S01 | PASS(REAL) | 승인 파일 없음 + 빈 서명 (MISSING_SIGNATURE) |
| S02 | PASS(REAL) | 위조 서명, 서명 후 페이로드 수정 (BAD_SIGNATURE) |
| S03 | PASS(REAL) | 다른 저장소 ID |
| S04 | PASS(REAL) | 만료, 경계, 시계 편차 5분 |
| S05 | PASS(REAL) | 고정 커밋 불일치 |
| S06 | PASS(REAL) | 서명은 유효하나 REQUEST 바이트와 불일치 |
| S07 | PASS(REAL) | 서명은 유효하나 패키지와 불일치 |
| S08 | PASS(REAL) | 폐기 키, 미등록 key_id, 회전 후 새 키 수락/구 키 거부, 다른 키로 서명한 가장 |
| S09 | PASS(REAL) | 정책 revision 변경 재사용, 다른 request_id 재사용, 완료 후 재시작·재생 시 호출 0 |
| S10 | PASS(REAL) | 승인/핀 쌍의 일부만 있음, 대기, 호출 0 |
요약: T 38건 = PASS(SYNTH) 23, PARTIAL 3, NOT_RUN 12. S 10건 = PASS(REAL) 10 (시험 키, 개인키 비저장).

## 6. 운영 DB 읽기·이행 검증 (C-5, 사본 기준)
- 백업: SQLite 온라인 백업, 원본은 읽기 전용 연결. 백업 전후 원본 메인 파일 SHA-256·크기·mtime 불변.
- 백업 무결성 ok. 행 수: jobs 61, audit_log 17,877, counters 8, cursors 1, pending_requests 1. 새 테이블 3개는 없음.
- 사본 이행: integrity_check ok, 기존 5개 테이블 행 수와 jobs 내용 동일, 새 테이블 3개 (provider_lease, provider_history, job_claims) 생성.
- 재개방: 스키마 해시와 행 수 불변 (idempotent).
- 구버전 호환: 운영 v0.1.5 코드가 이행된 사본을 오류 없이 열어 대기 목록과 감사 로그를 읽음.
- 롤백: 백업 파일을 되돌려 놓으면 바이트 동일 (해시 일치), v0.1.5 코드가 정상으로 엶.
- 운영 무변경: 운영 소스 버전 0.1.5 그대로, 운영 DB 테이블 6개 그대로 (새 테이블 없음), 작업 상태 COMPLETED 60 / CONFLICT 1, 예약 작업 4개(Watcher·Notifier·Dashboard Updater 실행 중, Bridge 대기) 상태 변화 없음.

## 7. 후보 ZIP
- 파일명: skill-collab-watcher_v0_2_3_1110.zip
- 크기: 131,400 bytes
- SHA-256: 9a4201295156ea93b572f4a7d0f8bc6b566130c31c1cae72c55d6c8c8489cf41
- 항목 60, ZIP 무결성 OK, 경로 이탈 0, 디렉터리 항목 0, 금지 파일 0, 필수 파일 누락 0, 비밀 검사 60파일 0건 (로컬 자격 값 2개 대조, 값은 비공개)
- 패키지에서 푼 사본에서 시험 재실행: 348 PASS / 12 SKIP
- v0.2.2 대비: 변경 11, 추가 0, 삭제 0
- 로컬 보관, 공개 게시 없음. 분류: development_not_for_deployment.

## 8. 미검증 및 운영 전환 차단 요건
1. C-4 Dropbox 실샘플 B-6 대조 NOT_RUN. 운영 Dropbox 읽기 권한(보호된 자격 증명)이 필요. 승인 시 준비된 스크립트로 개수·불리언만 산출.
2. 운영 신뢰 루트 생성·키 수명주기·시계 신뢰 실패 정책(B-7), 최소 권한 토큰: 미승인.
3. 실 Telegram 발송, 운영 notifier의 문구 교체(N-2): 미적용. bootstrap 시작점은 운영 notifier의 last_id를 이어받는 설계이며 운영 적용은 별도 승인.
4. 호스트 SHADOW 설치·가동, 실제 GitHub REQUEST/READY 발행, 독립 리뷰와 영수증: NOT_RUN.
5. 운영 DB에 테이블 3개를 추가하는 실제 이행은 미수행. 사전 조건: 백업, watcher 정지 시점 확인, 대기 요청 정산.
6. 현재 운영 Dropbox에는 정산되지 않은 대기 요청 1건이 있음. 전환 전에 처리하거나 hold_pending으로 보존 사유를 기록해야 함.
7. lease 만료 자동 탈취 미구현. 비정상 종료 후 수동 확인 필요.
8. 변이 시험·커버리지 미측정.

## 9. 판정에 필요한 설계 선택 (기록)
- 대기 범위를 새 컬럼 대신 ID 접두로 구현: 운영 스키마 변경을 줄이고 구버전이 같은 테이블을 읽을 수 있게 하기 위함. 대안: provider 컬럼 추가 (이행 위험 증가).
- 알림 시작점을 운영 notifier last_id에서 이어받음: 증거 없이 과거를 건너뛰지 않기 위함. 대안: 항상 현재 최신으로 시작 (미발송 중요 이벤트 유실 가능).
- hold_pending 전환은 허용하되 감사 로그와 알림을 남김: 전환 때문에 대기 요청이 조용히 사라지는 것을 막기 위함.

## 10. 다음 한 동작
GPT가 §8의 차단 요건 1~6을 판정한다. 승인되면 (a) Dropbox 실샘플 B-6 대조, (b) 호스트 SHADOW 설치 승인, (c) 정식 REQUEST/READY 독립 리뷰 순으로 진행한다. 운영 전환(LIVE)은 그 뒤 사용자의 명시 승인이 있을 때만 수행한다.

CUTOVER_READINESS_STATUS: PARTIAL ; tests: 348_PASS/0_FAIL/12_SKIP ; acceptance: T 23_PASS_SYNTH/3_PARTIAL/12_NOT_RUN, S 10_PASS_REAL ; crypto_real: PASS_TEST_KEYS ; github_readonly_real: PASS ; dropbox_b6_sample: NOT_RUN ; db_copy_migration: PASS ; model_review_calls: 0 ; telegram_real_sends: 0 ; production_changed: false ; candidate_zip: skill-collab-watcher_v0_2_3_1110.zip ; candidate_size: 131400 ; candidate_sha256: 9a4201295156ea93b572f4a7d0f8bc6b566130c31c1cae72c55d6c8c8489cf41 ; independent_review: NOT_RUN
