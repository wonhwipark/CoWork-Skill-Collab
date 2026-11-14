# CLAUDE Classic PAT 실제 쓰기·게시 E2E + LIVE 준비 결과 (GPT 판정용)

- 작성: Windows Claude Code (2026-11-14 KST). **Claude 자체 보고**, GPT 판정 전 canonical 아님.
- 근거 인계서: `GPT_CLASSIC_PAT_REAL_WRITE_AND_LIVE_PREFLIGHT_ONE_SHOT_r0001_20261114.md`
- 인증 계약: 사용자 확정에 따라 기존 Classic PAT를 감시기 기본 인증으로 사용. fine-grained 전환·만료 강제는 이번 판정 조건으로 삼지 않음. 토큰 값·접두·길이·해시·경로·계정 정보는 어디에도 출력/게시하지 않음.
- 실행하지 않은 것: 기존 리뷰 재실행, 추가 유료 모델 호출, 운영 DB·Task·Notifier 변경, 실제 Telegram 발송, 운영 인터프리터 설치, PUBLIC 배포, LIVE 전환.

## 1. 구분별 결과

| 항목 | 결과 | 한 줄 근거 |
|---|---|---|
| PAT_CLASSIC_ACCEPTED | **CLASSIC_PER_USER_DECISION** | 형식·무기한을 FAIL로 보지 않고 실제 동작으로 판정. 엔진 토큰 판독기는 classic JSON을 형식만으로 거부하지 않아 **코드 수정 불필요** |
| PAT_GITHUB_READ | **PASS** | 서버가 반환한 저장소 숫자 ID `1451933830` = 신뢰 루트 라벨, 비공개 저장소 |
| PAT_BRANCH_WRITE_READBACK | **PASS** | 임시 브랜치에서 create→readback→update→readback 모두 HTTP 201/200, 바이트·SHA 일치 |
| BRANCH_CLEANUP | **PASS** | 임시 브랜치 2개(쓰기 프로브, 게시 E2E) 모두 삭제 후 404, 원격 브랜치 목록에서 사라짐, `CLEANUP_PENDING` 없음 |
| WATCHER_INITIAL_UPLOAD_E2E | **PASS** | 실제 GitHub 임시 브랜치에서 감시기(v0.2.17 고정 바이트)가 `UPLOAD_PENDING`→`COMPLETED`. PUT 정확히 2회(결과+영수증) |
| IDEMPOTENT_PUBLISH | **PASS** | 재실행·재시작: 쓰기 0, 모델 0, 원격 불변. 이미 게시됨: GET readback만으로 완료. 내용 충돌: `CONFLICT`로 fail-closed, 덮어쓰기 0 |
| N1 (승인 재사용) | **수정·재시험 PASS (v0.2.18, 자체 시험)** | v0.2.17에서 재현 → v0.2.18 원격 결과 가드 |
| N2 (repo ID 결합) | **수정·재시험 PASS (v0.2.18, 자체 시험)** | 서버 숫자 ID와 신뢰 루트 비교, fail-closed |
| Q8 (복합) | **PASS(합성)**, 실 CLI 한도 문자열 **NOT_VERIFIED** | §5 |
| CRYPTO_TEST_VENV | **PASS** | 실서명 관련 68개 시험 통과 |
| CRYPTO_OPERATING | **NOT_RUN / BLOCKED(운영 설치 승인 필요)** | 운영 인터프리터 `cryptography` 없음, fail-closed 확인 |
| NOTIFIER_READ_ONLY_AUDIT | **PASS(분석)**; 이전 보고 **정정** | §7 |
| SHADOW_ACCOUNT_ENFORCE | **NOT_RUN** | 관리자·별도 계정 필요 |
| OPERATING_DB_INVARIANTS | **PASS** | 운영 DB main/WAL 해시가 이전 복구 리허설 시점과 동일, 쓰기 0, Task 상태 불변 |
| PAID_CALLS_DELTA | **0** | 모델 호출 0, 신규 유료 리뷰 0, Telegram 0 |
| ACTIVE_PROVIDER | **NONE / MIGRATION_NOT_CUTOVER** | 유지 |

## 2. Classic PAT 실제 쓰기 (원격 증거)

- 대상: PRIVATE `wonhwipark/CoWork-Skill-Collab`의 **임시 브랜치만**. 고정 비민감 fixture 1개를 PAT 자체로 쓰고 읽음: v1 sha256 앞 12자 `9a5b80a6a7ba`, v2 `f7be5f3c5029`. `main`에는 fixture가 없고(404), 프로브 전후 `main` 헤드 불변.
- 기존 REQUEST/READY/리뷰 결과/영수증/ZIP/대시보드/운영설정은 변경하지 않음. 개발자 `gh` 로그인은 이 검증에 쓰지 않음(감시기 토큰 파일만 사용).
- 구분: 이번 쓰기 검증은 "토큰이 실제로 쓸 수 있다"까지이며, 토큰 범위가 넓은 classic이라는 사실 자체는 사용자 정책으로 수용된 상태로 기록할 뿐 재논의하지 않는다.

## 3. 감시기 게시 경로 E2E (모델 호출 0)

- 방법: 임시 브랜치를 `main`에서 만들고 그 브랜치에서만 R2 결과·영수증을 지워 "아직 게시 안 됨" 상태를 재현. 이전 R2 격리 원장의 **사본**(`UPLOAD_PENDING`)으로 실제 엔진 `scan` 실행. `claude` 경로는 존재하지 않게 설정(모델 시작 구조적 불가), 프로세스 내부 감사 훅으로 하위 프로세스·HTTP 메서드·호스트 기록.
- 첫 자동 게시: `UPLOAD_PENDING`→`COMPLETED`, HTTP `GET 23 / PUT 2`, 다른 쓰기 메서드 0. 올라간 결과 파일은 실제 게시본과 **바이트 동일**(sha256 `a740ba59363d…`), 영수증은 식별 필드 동일(`watcher_version`만 엔진 버전 `0.2.17`).
- 멱등: 같은 원장 재실행·재시작 각 1회 → 쓰기 0, 상태 `COMPLETED` 유지, 하위 프로세스 0.
- `ALREADY_PUBLISHED`: 새 원장 사본(`UPLOAD_PENDING`)이 이미 파일이 있는 브랜치를 만나면 GET readback만으로 `COMPLETED`, 쓰기 0.
- 충돌 fail-closed: 원격 영수증을 다른 job 식별자로 바꿔 놓으면 `CONFLICT` 상태 + `CONFLICT` 이벤트, 쓰기 0, 원격 영수증 **덮어쓰기 0**.
- 증거: `MODEL_CALLS=0`, `PAID_COST_DELTA=0`, `TELEGRAM_SENDS=0`(호스트는 `api.github.com`뿐), `OPERATING_DB_WRITES=0`(라이브 폴더 파일 열기 0·SQLite 연결 0, main/WAL 해시 불변). 원본 격리 원장은 여전히 `UPLOAD_PENDING`(사본만 사용).
- 이전 R2 실물 3개: 원격에서 `main`의 현재 바이트가 보관본과 동일함을 이미 확인(직전 보고)했고, 이번 E2E는 `main`을 건드리지 않았다(실행 후에도 결과·영수증 바이트 동일).
- 의미: 자동 업로드 E2E가 **실제 GitHub 쓰기**로 처음 검증됨. 단, 이는 R2 결과를 재료로 한 복구/게시 경로이며 새 리뷰 디스패치는 하지 않았다.

## 4. 수정·재시험: 후보 v0.2.18 (격리, `development_not_for_deployment`)

v0.2.17 리뷰 PASS를 소급 적용하지 않음. 독립 리뷰 상태 **NOT_RUN**.

| ID | 판정 | 내용 |
|---|---|---|
| N1 | **재현 후 수정** | v0.2.17에서 상태 DB 전부 소실 후 같은 승인 번들로 다시 스캔하면 **2차 모델 호출**이 재현됨(합성). v0.2.18은 디스패치 전에 원격에 같은 request_id·revision·package_sha256의 영수증 또는 결과가 이미 있으면 `REMOTE_RESULT_EXISTS`로 중단(영수증 없이 결과만 있는 중간 크래시 경우도 포함). 원격 조회 실패 시 대기(`TRANSPORT_ERROR`, 리뷰 없음). 별도 nonce 저장소는 **추가하지 않음**: 재사용 방지는 로컬 DB 대신 원격에 이미 있는 결과를 기준으로 하고, 승인 유효기간(2시간 사용)은 그대로 한계로 둔다 |
| N2 | **구현** | 승인 확인 전에 서버가 알려주는 저장소 숫자 ID를 읽어 신뢰 루트 `repo_id`와 비교. 불일치→`APPROVAL_REPO_ID_REMOTE_MISMATCH`, 조회 실패·ID 없음→`APPROVAL_REPO_ID_UNVERIFIABLE`(둘 다 대기, 모델 0). 신뢰 루트·서명·키는 변경하지 않음. 실제 서버(읽기 전용 GET): 서버 ID가 운영 신뢰 루트의 repo_id와 **일치**(`True`) |
| S1 | 적용 | 호출처 없던 `find_logical_job` 제거 |
| S2 | 적용 | `taskkill` 비정상 종료 코드를 경고 로그로 남김 |

- **N1의 한계(정직)**: 원격에 결과가 아직 없는 상태(업로드 전에 DB가 소실)에서는 로컬 상태 없이 2차 호출을 막을 방법이 없다. 이 경우는 기존대로 승인 유효기간에 의존한다.
- 시험(v0.2.18 전용 `tests/test_v018_gates.py` 9개): N1 3(상태 소실, 영수증 없는 결과, 원격 조회 실패), N2 5(일치, 다른 ID, ID 없음, 403, timeout), Q8 1. **N1·N2 시험 7개는 v0.2.17 바이트에서 실패**(회귀 증명; 일치 ID 정상 경로 1개는 양쪽 통과), Q8 시험도 v0.2.17에서는 마지막 상태 소실 단계에서만 실패(§5).
- 수정 중 발견: 처음 N1 가드가 `MockTransport`의 "없는 파일" 오류를 전송 오류로 오인해 기존 시험 49개가 깨짐 → 존재 여부를 `get_metadata`로 먼저 묻도록 수정해 해결. 또 repo ID 도입으로 서명 도구 시험 1개의 가짜 서버 ID와 런북 제목 버전을 갱신.
- 전체 시험(고정 ZIP을 새로 풀어 실행): 시험 venv **653 passed / 12 skipped**(v0.2.17: 644/12), 운영 인터프리터 **587 passed / 17 skipped**(v0.2.17: 578/17). FAIL 0.
- v0.2.18 산출물: `skill-collab-watcher_v0_2_18_1114_DEV_NOT_FOR_DEPLOYMENT.zip` 235,650 B, sha256 `519c70e3eabbe9722621afa5bf6365b93d99803c76fee2fe078722a0835522cd`, 92개 파일, ZIP CRC/무결성 OK, 경로 이탈 0, 비밀 스캔 findings 0, 재빌드 바이트 동일. 변경 파일 10개(소스 6, 런북 제목, 시험 3). **로컬 보관, PRIVATE·PUBLIC 모두 게시하지 않음**(리뷰 게시는 새 리뷰 승인과 함께). v0.2.17 ZIP(`824f26c4…`) 바이트 불변.

## 5. Q8 복합 합성 시험

- 시나리오(모델 없음, 서명된 승인 사용): usage-limit 거부(작업 시작 전) → 재시작 → 다른 policy revision 승인으로 전환 → 원래 revision으로 롤백(새 nonce) → 커서 유실 → 같은 DB를 쓰는 두 번째 프로세스 스캔 → 한도 해제 → 실제 리뷰 1회 → 상태 전부 소실 후 재스캔.
- 결과: v0.2.17에서도 **마지막 단계 전까지는 모두 통과**(호출 수가 한도 해제 전까지 1로 유지, 완료 job 정확히 1). 마지막 상태 소실 단계에서만 2차 호출 → N1과 동일 원인. v0.2.18은 전 단계 통과, 총 호출 2(첫 번째는 시작 전 거부, 두 번째가 유일한 실제 리뷰).
- **NOT_VERIFIED 유지**: 실제 Claude CLI의 사용량 한도 메시지는 한 번도 관측하지 않았고, 일부러 유료 한도를 소진하지 않았다.

## 6. 암호 검증

- 시험 venv(실제 Ed25519): 승인·서명·키 보호 관련 **68개 통과**. 포함: 위조 서명, 서명 후 변조, **다른 저장소용 승인 거부**, 만료 승인 거부, 소스 커밋/핀 불일치, 폐기·교체 키, 같은 ID의 다른 키, 빈 서명, 다른 요청·패키지 바이트에 대한 서명, 완료 후 재생, 시계 오차 경계.
- 운영 인터프리터(Python 3.11.9): `cryptography` **없음**. 이 경우 승인 검증은 fail-closed(모델 호출 0, 대기). 운영 설치는 미승인이라 **변경하지 않음**.

## 7. Notifier 읽기 전용 분석 — 이전 보고 정정

- 이전 보고("`notify_reviews.py --watch` 2개 동시 실행")는 **독립된 두 Notifier가 아니다**. PID A(venv 런처)가 PID B(기본 인터프리터)를 **자식으로** 실행한 쌍이며(같은 시각 시작), A의 부모는 Task Scheduler 서비스 쪽 `svchost`. venv 스크립트 실행 시 나타나는 정상 구조다.
- 작업: 로그온 트리거 1개, `MultipleInstances=IgnoreNew`. 코드: 단일 인스턴스 바이트 잠금(두 번째 인스턴스는 "already running"으로 종료), 워터마크 `last_id`(첫 실행 시 과거 이력 미전송), 운영 DB를 SQLite `mode=ro`로 주기 조회(→ `-shm` 약 30초 갱신의 원인), Telegram 전송은 지정 이벤트만.
- 중복 전송 경로 가능성: **낮음**(잠금+워터마크). 종료·설정 변경·실전송 0.
- 비발송 이전 계획(미실행): GitHub 이행 시 감시기 상태 DB 경로가 달라지므로 Notifier에 provider별 DB 경로와 `last_id`를 분리해 두고, 전환 시 새 DB의 현재 최대 id로 부트스트랩(과거 이력 미재전송), 기존 pending 1건은 영수증/워터마크 기준으로 중복 방지. 전환 전까지 Notifier는 기존 운영 DB만 본다.

## 8. 남은 LIVE 게이트

1. v0.2.18(또는 이후 후보)의 **독립 리뷰**: 새 승인 필요. 통과 전까지 운영 후보는 v0.2.17이며 N1·N2는 LIVE 게이트로 남음.
2. 운영 인터프리터 `cryptography` 설치 + 실호스트 서명 검증 E2E (운영 변경 승인).
3. 별도 계정 enforce SHADOW + 네이티브 I/O 추적(관리자), 장기 SHADOW.
4. Notifier GitHub 연동 이행(provider별 DB·워터마크), 비발송 리허설 후 실알림은 별도 승인.
5. 컷오버·롤백 리허설, 단일 ACTIVE_PROVIDER 확인, 그 후 사용자 **별도 최종 승인**. 현재 `ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER`.
6. 실제 Claude 사용량 한도 메시지 관측(발생 시 정규식 검증) — 의도적 유발 금지.

## 9. 한계

- N1/N2 수정과 v0.2.18은 **자체 시험 결과**이며 독립 리뷰 PASS가 아니다. 리뷰어는 정적 리뷰라 실행 재현을 하지 않았다.
- E2E는 R2 결과를 재료로 한 게시/복구 경로이며, 첫 게시가 새 리뷰 디스패치와 이어지는 완전한 LIVE 흐름은 검증하지 않았다.
- Windows 전용. 비밀값·토큰·경로·계정명은 이 문서에 없다.
