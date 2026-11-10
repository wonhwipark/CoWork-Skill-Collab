# CLAUDE PHASE2 통합 개발·시험 결과 (GPT 확인용) 2026-11-10

- 작업 ID: COWORK-DROPBOX-TO-GITHUB-MIGRATION
- 인계서: PHASE2_END_TO_END_ONE_SHOT_HANDOFF_r0001_20261110.md (PRIVATE main에서 읽음)
- 처리 방식: NO_PR. 격리 복사본에서만 수정. 운영 watcher, 운영 SQLite DB, 예약 작업, Bridge, Dashboard, Telegram 설정은 변경하지 않음.
- 독립 리뷰: INDEPENDENT_REVIEW=NOT_RUN. 이 문서는 개발 세션의 자체 시험 보고(SELF_TEST_REPORTED)이며 정식 독립 리뷰가 아님.
- 모델 리뷰 호출: 0회 (시험은 FakeReviewRunner만 사용)
- 유료 리뷰 실행, LIVE 전환, PUBLIC 배포: 없음

PHASE2_STATUS: PARTIAL
사유: 실제 Ed25519 서명 시험(라이브러리 설치 권한 거부로 미실행), Dropbox 실샘플 B-6 대조(로컬 조회 권한 거부로 미실행), 인수시험 T 38건 중 12건 NOT_RUN과 3건 PARTIAL, 운영 적용 게이트 미충족.

## 1. 시작 기준 대조
- Phase1 후보 ZIP v0.2.0: 로컬 SHA-256 1003c1ab…7b24ba52, 108,936 bytes로 일치. 작업 종료 시에도 동일 (불변 보존).
- Phase1 결과 원문(commit a3f30d85) 및 GPT 판정 문서, CURRENT.md를 PRIVATE main에서 읽고 판정 항목을 이번 작업 범위로 채택.
- 운영 DB는 조회 전후 mtime 2026-11-10 16:43:51, 1,478,656 bytes로 동일. 실행 중인 기존 워처가 갱신하는 DB로 보이며 이번 작업은 쓰지 않음.

## 2. B-1 ~ B-7 추적표
| ID | 판정 | 이번 변경 요지 | 근거 시험 | 잔여 |
|---|---|---|---|---|
| B-1 | 구현 PARTIAL | Ed25519Backend 추가 (cryptography 지연 import, 없으면 NotConfigured, 기본은 fail-closed). | test_phase2_ed25519 (모듈 전체 NOT_RUN), 테스트 더블 S01~S10 | 실 라이브러리 설치와 실 서명 검증 미실행 |
| B-2 | PASS (합성) | 사이드카는 APPROVAL_SIG.json, SOURCE_PIN.json. 정확한 basename만 REQUEST/READY. REQUEST/READY 유사 이름이 남은 폴더(예: READY_APPROVAL.json)는 자동 차단, 모델 0, 대기 목록에서 제거. | test_B2_* 3건 | 차단 정책의 운영 영향(과거 폴더 개수)은 운영 DB/Dropbox 실측 필요 |
| B-3 | PASS (합성) | 봉인은 워처 잠금을 보유한 watch에서만 수행. 자기 프로세스가 claim한 작업은 제외. claim 소유자 테이블(job_claims) 추가. 읽기 전용은 봉인 안 함. recover --requeue 비활성. | test_B3_* 5건, T12 | 운영 DB 적용 시 스키마 추가 승인과 백업 필요 |
| B-4 | PARTIAL | provider_lease 단일 LIVE, provider_history, epoch 증가, 전환은 진행 중 작업이 없을 때만 허용. SHADOW는 읽기 전용. | test_B4_* 4건, test_T29, T19 교차 프로세스 잠금 | lease 만료 자동 탈취 미구현 |
| B-5 | PASS (합성) | 처리키 형식 유지. 같은 request_id·revision·패키지의 완료/진행 작업을 정책 revision과 무관하게 조회해 재호출 0. | test_B5, test_T21 | 명시적 재리뷰는 신규 revision으로만 |
| B-6 | PASS (합성), 실샘플 NOT_RUN | 해시는 저장된 원본 바이트 기준. v0.1.5의 해시 방식(UTF-8 엄격 decode 후 encode)은 유효한 UTF-8에서 원본 바이트와 같으므로 Dropbox 호환 유지. BOM은 양쪽 모두 거부. CRLF는 원본 그대로 해시. | test_B6_* 3건, GitHub 실 blob sha가 git 해시와 일치 | Dropbox 실제 REQUEST/READY 샘플 대조는 권한 거부로 미실행 |
| B-7 | PARTIAL | trust root를 다중 키·ACTIVE/RETIRED 상태·지문 검증 형식으로 확장. 폐기 키 거부. | test_S08_* 2건 (테스트 더블), test_trust_root_fingerprint_* | 실 신뢰키 발급·회전·폐기 정책은 미승인 |

## 3. 실제 변경 (diff 중심, 격리 src 기준)
- approval.py: 서명 메시지는 canonical(payload). payload에 schema, ready_sha256, nonce(16자 이상) 바인딩 추가. 키 상태 ACTIVE/RETIRED.
- signature_backend.py (신규): Ed25519Backend, default_backend() (없으면 None).
- orchestrator.py: 승인 게이트에 ready_sha256 추가. BOM 거부. 패키지 자격증명 형태 텍스트 검사(호출 전 REJECTED). 결과 재검증(download_latest, 영수증 필드 비교) 실패 시 CONFLICT. 세부 변경 사항은 아래 6번 행동 변화 참조.
- state_store.py: job_claims, provider_history 테이블. seal_interrupted(exclusive). switch_provider(). record_claim().
- zip_safety.py: package_secret_findings() 추가 (ZIP 내용 검사, 추출 전).
- validator.py: knowledge_refs sha256이 64자리 16진수인지 검사.
- cli.py: default_backend 연결, watch만 exclusive=True, recover --requeue 거부(EXIT_REFUSED).
- notify_events.py (신규): 알림 대상 선택, 1회 발송, 제공자별 문구(Dropbox/GitHub). 발송기는 주입 방식이라 실제 Telegram 호출 없음.
- transport_base.py / github_transport.py: download_latest() 추가 (Dropbox는 download와 동일, GitHub는 pin을 무시).
- __init__.py: 0.2.0 -> 0.2.1.
- tools/build_release.py: requirements-crypto-test.lock을 패키지에 포함.
- tests: fake_github.py 재작성(측면 ref 커밋 지원), bundle.py(신규), 테스트 파일 5개 재작성/신규.
- 운영 환경 변경 없음. 운영 venv에 설치한 것 없음.

## 4. 시험 결과
### 4.1 전체 pytest (격리 복사본, 설치 없이 기존 인터프리터의 읽기 전용 사용, 캐시 미생성)
- 312 PASS / 0 FAIL / 13 SKIP
- SKIP 13개의 내역:
  - test_phase2_ed25519.py 모듈 전체 1건: cryptography 미설치 (NOT_RUN, 개별 시험 12개 포함)
  - test_secret_prompt.py GUI 옵트인 8건: SKILL_COLLAB_GUI_TESTS=1 필요
  - test_windows_scripts.py 4건: 프로젝트 .venv 존재 시에만 실행. 이 복사본에는 .venv가 없음
- Phase1 수치 차이 설명: 기준 236 PASS/8 SKIP은 .venv가 있는 원본 프로젝트에서 나온 값으로, 차이 4건은 test_windows_scripts 4건과 정확히 일치 (232+4=236, 12-4=8). 원인 확정.
- 이번 신규 시험 수치는 테스트 함수 기준으로 집계. 기존 Dropbox 회귀 파일은 전부 PASS.
- 변이 시험(mutation test)과 커버리지 측정은 수행하지 않음.

### 4.2 실제 GitHub 읽기 전용 점검 (PRIVATE 저장소, GET만, 토큰은 기존 gh 로그인 사용)
- gh CLI 직접 호출 8항목: commit 200 + ETag, 조건부 GET 304, 재귀 트리 (truncated=false, 38항목), 고정 ref 파일 조회, blob sha가 git hash-object와 일치, blob 엔드포인트, 없는 경로 404, compare 엔드포인트 — 전부 기대대로.
- 격리 복사본의 GitHubTransport 실행 점검 (실 HTTP): ensure_auth, head_sha 조건부 읽기, pin 목록 10개, 고정 파일 7,197 bytes와 blob sha 일치, 없는 파일 RemoteNotFound(fail closed), 과거 커밋 기준 list_folder_continue 3건. 쓰기 호출 없음.
- 상태: github_readonly_real = PASS (읽기 전용 범위에 한함).

### 4.3 인수시험 T01~T38 / S01~S10 (상세)
| ID | 상태 | 근거 (시험명 또는 근거) |
|---|---|---|
| T01 | PASS | test_T01 |
| T02 | PASS | test_T02 |
| T03 | PASS | test_T03 (READY만 있고 패키지 없음 → 재시도, CLAIM 없음) |
| T04 | PASS | test_T04 |
| T05 | PASS | test_T05 3건 (크기/SHA 불일치 → 호출 0, CRC 손상 ZIP → FAILED, 호출 0) |
| T06 | PARTIAL | test_T06 3건 (해시 누락/형식 오류 → 거부, 고정 내용 불일치 → CONFLICT). revision 필드는 V1 스키마에 없어 시험하지 않음 |
| T07 | PASS | test_T07 2건 (새 request_id는 자기 승인 없이는 검토 안 됨, 자기 승인이 있으면 1회 추가 검토) |
| T08 | PASS | test_T08_same_revision_with_another_package_is_conflict_and_original_kept (Dropbox 형식 모의 전송. GitHub 경로 전용 시험은 없음) |
| T09 | PARTIAL | test_T09 (측면 ref에만 있는 READY는 읽지 않음). PR/포크/이슈/태그는 모델링하지 않음 |
| T10 | PASS | test_T10 |
| T11 | PASS | test_T11 (반복 조회와 재시작 후 호출 1회 유지) |
| T12 | PASS | test_T12 (봉인 후 재실행 0, REVIEW_UNCERTAIN 1건), notify 불확실 알림 1회 |
| T13 | PASS | test_T13 (게시 503 → 업로드만 재시도, 호출 1회) |
| T14 | PASS | test_T14 (RECEIPT 누락 → UPLOAD_PENDING, COMPLETED 없음, 재시도 시 호출 추가 없음) |
| T15 | PASS | test_T15 (다른 작업의 영수증 → CONFLICT, COMPLETED 없음) |
| T16 | PASS | test_T16 2건 (고정 commit에서 읽음, 변조 blob 탐지) |
| T17 | PASS | test_T17 (add-only, 422 충돌, GET/PUT 외 호출 없음) |
| T18 | PASS | test_T18 5건 (자격 없음, 403/404, 429 재시도 힌트, 네트워크 오류, 401) |
| T19 | PASS | test_T19 2건 (자식 프로세스로 실제 교차 프로세스 잠금 확인, 진행 중 재스캔 시 디스패치 0) |
| T20 | PASS (합성) | test_T20 + notify의 SHADOW 시험 (DB 쓰기 0, 호출 0, 원격 쓰기 0, 알림 0). 실 Telegram 0은 미관찰 |
| T21 | PASS | test_T21 (제공자 전환 후 완료 작업 재호출 0) |
| T22 | PASS (합성) | test_T22 (완료 알림 1회, 재실행 시 추가 없음). 실제 휴대폰 수신은 미확인 |
| T23 | NOT_RUN | 워처는 mode를 읽지 않음. 정적 확인만 수행 (GPT Work 자동 실행 경로 없음) |
| T24 | PASS | 기존 test_v014_budget_tiers 회귀 PASS (예산 중단 시 게시 안 함, 요청이 금액을 지정할 수 없음) |
| T25 | PASS | test_T25 3건 (경로 이탈, 심볼릭 링크, 자격증명 형태 텍스트) |
| T26 | NOT_RUN | 공개 게시 경로가 워처에 없음 |
| T27 | NOT_RUN | Dashboard 소스가 이 복사본에 없음 |
| T28 | NOT_RUN | 공개 게시 경로 없음 |
| T29 | PASS | test_T29 (롤백 후 활성 lease 1건, 이력 보존) |
| T30 | NOT_RUN | Git 이력 복구는 플랫폼 속성이며 이번 시험 범위 밖 |
| T31 | NOT_RUN | 공개 게시 경로 없음 |
| T32 | NOT_RUN | 공개 배포 경로 없음 |
| T33 | NOT_RUN | 공개 배포 경로 없음 |
| T34 | NOT_RUN | 공개 배포 경로 없음 |
| T35 | NOT_RUN | 공개 배포 경로 없음 |
| T36 | NOT_RUN | 공개 배포 경로 없음 |
| T37 | NOT_RUN | 권한 환경 필요 |
| T38 | PARTIAL | build_release 비밀 검사 59파일 0건 (사전 검사로만 확인). 공개 게시 차단 장치는 없음 |
| S01 | PASS (테스트 더블) | test_S01; 실 Ed25519 NOT_RUN |
| S02 | PASS (테스트 더블) | test_S02 2건; 실 Ed25519 NOT_RUN |
| S03 | PASS (테스트 더블) | 다른 저장소 ID; 실 NOT_RUN |
| S04 | PASS (테스트 더블) | 만료, 경계, 시계 편차 5분; 실 NOT_RUN |
| S05 | PASS (테스트 더블) | 고정 커밋 불일치; 실 NOT_RUN |
| S06 | PASS (테스트 더블) | REQUEST 해시 바인딩; 실 NOT_RUN |
| S07 | PASS (테스트 더블) | 패키지 해시 바인딩; 실 NOT_RUN |
| S08 | PASS (테스트 더블) | 폐기 키, 미등록 key_id; 실 NOT_RUN |
| S09 | PASS (테스트 더블) | 정책 revision 변경 재사용, 다른 request_id 재사용; 실 NOT_RUN |
| S10 | PASS (테스트 더블) | 쌍의 일부만 있음 → 대기; 실 NOT_RUN |

요약: T 38건 중 PASS(합성) 23, PARTIAL 3, NOT_RUN 12. S 10건은 테스트 더블 기준 PASS 10이며 실 Ed25519 기준은 전부 NOT_RUN.

### 4.4 실 Ed25519 시험 (NOT_RUN)
- 사유: 격리 가상환경에 해시 고정 cryptography 설치가 사용자 권한 거부로 실행되지 않음. 운영 venv에는 설치하지 않음.
- test_phase2_ed25519.py는 구문 검사(ast 파싱) 통과. 실행되지 않았으므로 동작은 미검증.
- 해시 고정 잠금 파일 requirements-crypto-test.lock (cryptography 50.0.2 외 전이 의존성 포함)은 준비됨. 설치는 별도 승인 후 실행.

## 5. 운영 무변경 증거
- 운영 DB 사본 인벤토리 (읽기 전용 복사본, 카운트만): jobs COMPLETED 60, CONFLICT 1, 진행 중 CLAIMED/REVIEW_RUNNING 0, audit_log 17,665행, pending 1, cursors 1행, provider_lease 테이블 없음 (v0.1.5 스키마).
  - 이 시점 기준 B-3 봉인 대상 행은 0건. 다만 운영 적용 시점에는 다시 확인 필요.
- 원본 DB는 조회 전후 mtime/size 동일 (16:43:51, 1,478,656 bytes). 복사본은 조회 후 삭제.
- 운영 venv, 예약 작업, Bridge, Dashboard, Telegram 설정: 변경 없음 (설치 없음, 실행 없음).
- 신규 스키마(provider_lease, provider_history, job_claims)는 v0.2.x를 운영 DB에 여는 순간 생성됨. 이는 운영 적용 게이트이며 이번에는 적용하지 않음.

## 6. 행동 변화 (GPT 판정 필요)
1. B-2: READY/REQUEST 유사 이름의 사이드카가 있는 폴더는 이제 자동 차단 (구버전에서는 READY 모호성으로 영구 대기였음). 운영 전환 시 과거 대기 폴더가 활성화되지 않도록 차단 기록을 확인해야 함.
2. 패키지 내용에 자격증명 형태 텍스트가 있으면 호출 전 REJECTED. 정상 패키지 오탐 가능성 있음.
3. BOM이 있는 REQUEST/READY는 Dropbox 포함 전 제공자에서 거부 (v0.1.5도 front matter 파싱에서 같은 결과).
4. T15: 게시 후 원격 재검증 실패 시 COMPLETED가 되지 않고 CONFLICT. 재시도로 호출이 늘지 않음.
5. recover --requeue 비활성. 불확실/진행 중 작업은 새 revision으로만 다시 리뷰.
6. 봉인은 watch 잠금 보유 시에만. 단일 scan 명령은 봉인하지 않음.
7. 알림 문구는 제공자별로 생성되지만, 운영 notify_reviews.py는 변경하지 않음 (N-2 운영 적용 미완료).

## 7. 후보 ZIP
- 파일명: skill-collab-watcher_v0_2_1_1110.zip
- 로컬 보관: 격리 작업 공간 dist_phase2\ (공개 게시하지 않음)
- 크기: 125,653 bytes
- SHA-256: d1e612fe70b34ec6e10109be58f95dfb79c9c620ff85e076152ae6d631aa0fd2
- 항목 수 59, ZIP 무결성 OK, 경로 이탈 0, 디렉터리 항목 0, 금지 파일 0, 필수 파일 누락 0, 비밀 검사 59파일 0건 발견 (로컬 자격 값 2개 대조, 값은 비공개)
- v0.2.0 대비: 추가 7건, 삭제 0건, 내용 변경 15건
- 배포 분류: development_not_for_deployment (실 서명 미검증, 실 GitHub 쓰기 미검증, 운영 적용 게이트 미충족)
- 이전 후보 v0.2.0 ZIP은 원래 상태 그대로 보존 (SHA-256 1003c1ab…7b24ba52, 108,936 bytes)

## 8. 미해결 사항 / 남은 운영 게이트
1. 실 서명 라이브러리 설치 승인 (해시 고정된 잠금 파일 준비됨). 승인 후 실 Ed25519 S01~S10과 키 폐기·회전·만료·재생 시험 실행.
2. Dropbox 실제 REQUEST/READY 샘플의 바이트 해시 대조 (B-6). 권한 거부로 미실행. 코드 근거는 있으나 실측 필요.
3. 신뢰 루트 수명주기 정책 (발급, 회전, 폐기, 시계 신뢰 실패 처리) 확정 및 승인 (B-7).
4. 운영 DB 스키마 추가 시점의 백업과 승인 (provider_lease, provider_history, job_claims), 봉인 전 인벤토리 재확인.
5. lease 만료 자동 탈취 미구현 (B-4).
6. 실제 Telegram 발송 미검증 (fake sender만 사용). 운영 notifier 문구 교체 미적용.
7. 공개 배포 경로 (T26, T28, T31~T36)와 Dashboard (T27)는 이 작업 범위 밖이며 미구현.
8. 독립 정식 리뷰: 별도 유효 REQUEST/READY와 독립 reviewer 실행, 영수증 필요 (INDEPENDENT_REVIEW=NOT_RUN).

## 9. 권장 다음 한 동작
GPT가 6번의 행동 변화 1~4와 8번 항목 1~3을 판정한다. 실 서명 라이브러리 설치 승인을 받으면 격리 가상환경에서 실 Ed25519 시험을 실행한다. 운영 DB 적용은 별도 승인 전까지 보류한다.

PHASE2_STATUS: PARTIAL ; tests: 312_PASS/0_FAIL/13_SKIP ; acceptance: 33_PASS(23 T + 10 S synthetic)/3_PARTIAL/12_NOT_RUN ; crypto_real: NOT_RUN ; github_readonly_real: PASS ; model_review_calls: 0 ; production_changed: false ; candidate_zip: skill-collab-watcher_v0_2_1_1110.zip ; candidate_size: 125653 ; candidate_sha256: d1e612fe70b34ec6e10109be58f95dfb79c9c620ff85e076152ae6d631aa0fd2 ; independent_review: NOT_RUN
