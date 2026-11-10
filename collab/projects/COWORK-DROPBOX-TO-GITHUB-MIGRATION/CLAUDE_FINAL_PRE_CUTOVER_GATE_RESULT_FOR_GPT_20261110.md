# CLAUDE FINAL PRE-CUTOVER GATE 결과 (GPT 확인용) 2026-11-10

- 작업 ID: COWORK-DROPBOX-TO-GITHUB-MIGRATION
- 인계서: GPT_C4_ADJUDICATION_AND_REMAINING_GATES_r0001_20261110.md (PRIVATE main에서 읽음)
- 처리 방식: NO_PR, 격리 복사본에서만 수정. 운영 watcher, 운영 DB, 예약 작업, Telegram, Bridge, Dashboard 변경 없음.
- 증거 수준: SELF_TEST_REPORTED. 정식 독립 리뷰가 아님. INDEPENDENT_REVIEW=NOT_RUN.
- 모델 리뷰 호출 0회. 실제 Telegram 발송 0회. 운영 신뢰키·개인키·토큰 발급 0회. 운영 DB 변경 0건.
- 현재 LIVE: Dropbox 그대로. GitHub 전환(LIVE)은 실행하지 않았다.

PRE_CUTOVER_STATUS: PARTIAL
사유: 코드·정책·격리 시험은 완료. 운영 신뢰키 발급, 호스트 SHADOW 설치, 정식 독립 리뷰, 운영 DB 이행, LIVE 전환은 승인 대상이라 미실행. 읽기 전용 조사로 미정산 요청은 분실이 아님을 확인했다.

## 1. 미정산 요청 1건과 불완전 폴더 2개 (읽기 전용, 식별자 비게시)
접근 범위: 감시기 전송 계층의 목록 조회와 다운로드, 운영 DB는 mode=ro 연결. 업로드·삭제·이동·DB 쓰기 없음. 출력은 익명 라벨과 집계만 사용했다.

| 라벨 | 상태 | 모델 호출 | 연결 | 판정 |
|---|---|---|---|---|
| F1 | REQUEST 1개 + 기타 1개 파일, READY 없음. 2026-11-09부터 대기. 작업 기록 없음. 감사 이벤트는 WAIT_INPUT 1건 | 0 | **미정산 대기 1건과 동일 (TRUE)** | HOLD. READY를 기다리는 정상 대기이며 분실도 중복도 아님 |
| F2 | REQUEST만 있음. 작업 1건이 COMPLETED. READY는 완료 후 제거된 것으로 보임 | 1 (완료됨) | 대기와 무관 (FALSE) | SETTLED. 논리 중복 규칙이 재실행을 막음 |
| G1~G3 | REQUEST+READY 쌍이지만 작업 기록 없음 | 0 | 대기와 무관 (FALSE) | SETTLED as REJECTED. 사유: READY 필수 필드 누락 1건, 지식 참조 해시가 자리표시자 2건. 각 1회 기록 후 종료 |

집계: 요청 폴더 65 = 정상 쌍 중 작업 있음 60 + 작업 없음(G) 3 + 불완전 2. 작업 61건은 폴더 61개에 대응(F2 포함). 분실 0, 미설명 0.

무손실 정산 방안
1. F1은 이관하지 않는다. 전환 시 `switch_provider(..., hold_pending=True)`로 보존하고 감사 로그에 PENDING_HELD로 ID를 남긴다 (알림 1회).
2. 전환 후에도 Dropbox 범위의 대기 목록은 GitHub 스캔이 건드리지 않는다 (제공자별 범위 분리, 시험 및 사본 리허설로 확인).
3. F1을 GitHub에서 리뷰하려면 새 REQUEST/READY와 서명 승인이 필요하다. 자동 이관·재큐잉 없음.
4. 정산 없이 전환하면 거부된다. `reconcile` 명령(읽기 전용)이 같은 집계를 언제든 출력한다.
5. 실제 hold·requeue·삭제·READY 발행은 하지 않았다.

실데이터 차이 시험 (65개 폴더 전부, 읽기 전용): 운영 v0.1.5 대비 후보 v0.2.4의 판정과 처리키가 64개 동일. 1개 차이는 이미 CONFLICT로 종료된 작업의 요청이며, 지식 참조 해시가 63자리 오타였다. v0.1.5는 파일 내려받기 뒤 ContextMismatch로, 후보는 검증 단계에서 같은 이유로 거부한다 (모델 호출 없음, 결과 동일).

## 2. 운영 신뢰키(B-7) 수명주기 정책 — 설계 + 구현 + 격리 시험
키 발급·설치는 하지 않았다. 정책 전문은 패키지의 docs/CUTOVER_RUNBOOK.md.

| 항목 | 정책 | 구현 상태 |
|---|---|---|
| 역할 분리 | 서명 개인키는 승인자 기기에만, 신뢰 루트는 호스트 관리자만 수정. 감시기는 공개키만 보유. 저장소 커밋은 승인이 아님 | 설계 + 구조적 보장(감시기에 개인키 경로 없음) |
| 보관 위치 | 저장소 밖, 동기화 폴더 밖. 광범위 그룹(Everyone, Users, Authenticated Users, Domain Users)에 쓰기 권한이 있으면 거부 | 구현: Windows 보안 설명자 조회(프로세스 생성 없음). 실제 파일에서 동작 확인 |
| 무결성 고정 | 로컬 설정의 trust_root_sha256으로 파일 바이트 고정. 고정값이 없으면 거부 | 구현 + 시험 |
| 버전 래칫 | 수락한 최고 버전보다 낮으면 거부(롤백 방지). 복구는 항상 더 높은 버전 | 구현 + 시험 (읽기 전용 저장소는 비교만) |
| 키 상태 | ACTIVE, RETIRED, REVOKED. 각각 다른 거부 사유. 키별 유효 기간(not_before/not_after), 용도(review-approval) | 구현 + 시험 |
| 회전 | 버전 N+1: 구 키 RETIRED, 새 키 ACTIVE, 핀 갱신 | 시험(실서명): 새 키 수락, 구 키 거부 |
| 폐기·유출 | 버전 N+1: 해당 키 REVOKED + 새 키 | 시험 |
| 비상 정지 | `frozen: true` 한 줄로 모든 승인 거부. 키 조작 불필요 | 구현 + 시험 |
| 승인 수명 | 기본 24시간 상한(루트에서 60초~7일로 조정). 초과하면 거부 | 구현 + 시험 |
| 시계 | 제공자(GitHub) Date 헤더와 로컬 시계 차이가 5분 초과이거나 헤더가 없으면 승인 대기. 승인 자체의 시계 편차 허용은 5분 | 구현 + 시험 |
| 서명 검증 장애 | 라이브러리 없음, 신뢰 루트 없음, 파일 손상, 핀 불일치, ACL 문제는 모두 fail-closed. 모델 호출 0 | 시험 |
| 롤백 | 신뢰 루트는 되돌리지 않고 상위 버전으로 복구. 제공자 롤백은 대기·커서 보존. DB 롤백은 백업 복원(바이트 동일 검증) | 설계 + 사본 시험 |
| 운영자 도구 | tools/trust_root_tool.py: 공개키만 받아 신뢰 루트 생성, 핀 출력, 점검. 덮어쓰기 거부, 개인키 취급 없음 | 구현 + 시험 11건 |

실서명 시험 (격리 가상환경, 해시 고정 cryptography 50.0.2, 시험마다 메모리에서 만든 시험 키, 개인키 비저장): test_phase2_ed25519 19건 전부 통과. S01~S10 전체와 만료·변조·재생·폐기·회전·시계 편차 포함.
NOT_RUN: 운영 키 부트스트랩, 승인 서명 도구(승인자 기기용), 운영 신뢰 루트의 실제 ACL 설정.

## 3. SHADOW 준비 (호스트 설치·가동은 하지 않음)
설계: provider_mode=SHADOW. 운영 DB는 SQLite mode=ro로만 연다. 실행 산출물과 단일 인스턴스 잠금은 `<state_dir>-shadow` 형제 폴더에 둔다. 따라서 운영 폴더에 쓰지 않고 운영 감시기 잠금과 충돌하지 않는다. 승인 요구·디스패치·알림·GitHub 쓰기는 모두 꺼진다.

| 기준 (T20) | 실측 (운영 상태 폴더의 복사본 + 실제 GitHub PRIVATE 읽기, 3사이클) |
|---|---|
| 모델 호출 | 0 (디스패치 0 x 3, 러너 미기동) |
| GitHub 쓰기 | 0 (사용한 HTTP 메서드는 GET뿐, 9회) |
| 운영 DB 메인 파일 | 바이트 동일 |
| WAL 파일 | 바이트 동일 |
| SHM 파일 | 변경됨. SQLite가 읽기 표시를 기록하는 파생 색인이며 데이터가 아니다. 이미 운영 중인 notifier도 같은 방식으로 읽는다. 기준을 "메인+WAL 동일"로 정의할 것을 제안 |
| 운영 폴더에 새 파일 | 없음 (형제 폴더에만 생성) |
| 미이행(v0.1.5 스키마) DB에서 시작 | 가능 (아래 결함 수정 후) |
| Telegram | 0 (알림은 SHADOW에서 구동되지 않음) |
| 단일 LIVE 제공자 | SHADOW는 lease에 쓰지 않음 |
| 커서 | 제공자별 키, 롤백 시 Dropbox 커서 불변 (사본 리허설) |
| 알림 시작점 | 운영 notifier의 last_id를 이어받음. 초기화 없는 상태는 발송 거부. 리허설: 과거 알림 대상 66건 중 재전송 0 (1건은 리허설이 만든 PENDING_HELD) |

호스트 SHADOW 차단 요건(승인 필요): 별도 폴더에 후보 설치, 읽기 전용 토큰 생성, 운영 Dropbox 감시기 무영향 확인 기간 합의.

## 4. 이번에 찾아 고친 결함
1. SHADOW가 미이행 DB에서 중단 (provider_lease 테이블 없음). 호스트 SHADOW의 실제 시작 조건에서만 나오는 결함. 수정 + 회귀 시험(v0.1.5 스키마 DB에서 SHADOW 실행, 새 테이블 미생성 확인).
2. 신규 정책 코드가 프로세스 생성 금지 정적 시험(모델 호출 경계)에 걸림. 시험을 완화하지 않고 ACL 점검을 Windows API 호출로 다시 구현.
3. 시험 설계 오류 2건(단언 오류, 이전 단계에서 확인된 공유 경로 덮어쓰기) 수정. 제품 결함 아님.

## 5. 시험 결과
- 전체 pytest: **410 PASS / 0 FAIL / 12 SKIP** (격리 가상환경, 캐시·바이트코드 미생성). 후보 ZIP을 풀어 낸 사본에서도 동일.
- 이전 보고(348 PASS / 12 SKIP) 대비 PASS +62, SKIP 불변. SKIP 12건: GUI 실창 시험 8건(옵트인), Windows 스크립트 시험 4건(프로젝트 .venv가 있을 때만 실행). 원인 불명 SKIP 없음.
- 신규 시험 62건 = 정책 게이트 51건(test_phase3_gates) + 신뢰 루트 도구 11건(test_phase3_trust_tool). 이전 대비 PASS 증가분 62와 일치.
- 리허설(실제 운영 DB 사본): 전환·롤백, 백업·이행·재개방·구버전 호환·복원, SHADOW, 실데이터 차이 시험, 실제 GitHub 읽기. 전부 통과.
- 인수시험 48건: T 38건 = PASS(SYNTH) 23, PARTIAL 3, NOT_RUN 12 (변동 없음, T19·T20은 사본 리허설로 보강). S 10건 = PASS(REAL, 시험 키) 10.
- 변이 시험·커버리지 측정은 하지 않았다.

## 6. 후보 ZIP
- 변경 사유: 위 2·3절의 코드 변경이 있어 신규 버전 필요. 이전 후보는 그대로 보존.
- 파일명: skill-collab-watcher_v0_2_4_1110.zip
- 크기: 146,879 bytes
- SHA-256: 854d2d324033dac77771ed7145feabf0a659b3450d7b7579c54f487ae3f6ed20
- 항목 64, ZIP 무결성 OK, 경로 이탈 0, 디렉터리 항목 0, 금지 파일 0, 비밀 검사 64파일 0건(로컬 자격 값 대조 포함)
- 운영 v0.1.5 대비: 변경 10, 신규 18, 동일 36. 소스(패키지+도구) 추가 1,605줄 / 삭제 66줄
- 이전 후보 해시 불변: v0.2.0 1003c1ab…, v0.2.1 d1e612fe…, v0.2.2 7ec4f63e…, v0.2.3 9a420129…
- 로컬 보관, 게시하지 않음. 분류: development_not_for_deployment.

## 7. 독립 리뷰 입력 자료
별도 파일로 게시: REVIEW_INPUT_MANIFEST_v0_2_4_FOR_GPT_20261110.md (실행 요청 아님). 내용: 후보 식별, 우선 검토 영역과 질문 9개, 알려진 한계 7개, 재현 방법, 소스 전달 조건, 정식 리뷰 시작 체크리스트, ZIP 항목 64개의 파일별 SHA-256·크기·v0.1.5 대비 변경 분류와 변경 줄 수.
소스 ZIP 게시는 반출 분류와 사용자 승인 전이라 NOT_APPROVED. 실제 REQUEST/READY, 독립 reviewer 실행, 영수증은 발행하지 않았다.

## 8. 운영 무변경 및 호출 수 증거
- 모델 리뷰 호출 0, 실제 Telegram 0, 운영 키·토큰 발급 0.
- 운영 소스 버전 0.1.5, 운영 DB 테이블 6개 그대로(새 테이블 없음), 작업 상태 COMPLETED 60 / CONFLICT 1, 대기 1행.
- 운영 상태 폴더에 새 파일·폴더 없음. 형제 SHADOW 폴더 없음(리허설은 임시 복사본에서 수행 후 삭제).
- 예약 작업 4개 상태 변화 없음: Watcher Running, Notifier Running, Dashboard Updater Running, Bridge Ready.
- 운영 DB는 감시기가 계속 기록하므로 행 수는 시간에 따라 늘어난다(감사 로그 17,877행 → 18,079행). 우리 쪽 접근은 mode=ro 읽기와 온라인 백업뿐이며, 백업 전후 메인 파일 해시가 동일했다.
- 운영 데이터가 담긴 로컬 백업 사본 1개는 격리 작업 공간에만 보관하고 게시하지 않았다.

## 9. 미해결 사항
1. 운영 신뢰 루트·승인 키 부트스트랩, 승인 서명 도구(승인자 기기용): 미구현·미승인.
2. 호스트 SHADOW 설치·가동과 관찰 기간: 미실행.
3. 정식 독립 리뷰와 영수증: NOT_RUN. 소스 전달 승인과 반출 분류 필요.
4. 운영 DB의 실제 이행(테이블 3개 추가): 미실행. 백업·정지 시점·정산 선행.
5. F1(READY 대기 요청)의 최종 처분: 사용자 결정 필요 (Dropbox에서 계속 대기, 또는 GitHub에서 새로 발행).
6. lease 만료 자동 탈취 미구현. 실 Telegram 문구 교체(N-2)는 운영 notifier에 미적용.
7. BOM·CRLF 실표본 0이므로 합성 시험으로만 검증. 공개 배포·Dashboard 관련 T 12건은 범위 밖.
8. 변이 시험·커버리지 미측정.

## 10. 사용자 승인 1회분 (제안, 한 번에 판단 가능하도록 묶음)
LIVE 전환은 포함하지 않는다. 다음 네 가지를 한 번에 승인하면 GPT가 정식 리뷰까지 진행할 수 있다.
1. 승인자 키 쌍을 승인자 기기에서 생성하고, 공개키로 신뢰 루트를 만들어 호스트에 핀과 ACL로 설치 (개인키는 호스트와 저장소에 두지 않음).
2. 후보를 별도 폴더에 설치하고 읽기 전용 토큰으로 호스트 SHADOW를 가동 (기간 합의, 운영 Dropbox 감시기 불변).
3. 소스 ZIP을 PRIVATE의 packages 폴더에 새 파일명으로 게시 (반출 분류 확인 후).
4. 정식 독립 리뷰 1회 (STATIC 상한 $1, 서명된 REQUEST/READY, 영수증 확인).
그 이후에 별도 승인으로: 운영 DB 이행(백업 선행), 정산 확인, LIVE 전환.

## 11. 다음 한 동작
GPT가 위 판정과 승인 묶음을 검토한다. 승인되면 1번(신뢰 루트)부터 순서대로 진행한다.

PRE_CUTOVER_STATUS: PARTIAL ; tests: 410_PASS/0_FAIL/12_SKIP ; acceptance: T 23_PASS_SYNTH/3_PARTIAL/12_NOT_RUN, S 10_PASS_REAL ; crypto_real: PASS_TEST_KEYS ; pending_accounting: F1_is_the_pending_request_HOLD ; unaccounted_folders: 0 ; shadow_copy_rehearsal: PASS(main+WAL identical, shm derived) ; b7_policy: DESIGNED_AND_IMPLEMENTED_NOT_DEPLOYED ; model_review_calls: 0 ; telegram_real_sends: 0 ; production_changed: false ; candidate_zip: skill-collab-watcher_v0_2_4_1110.zip ; candidate_size: 146879 ; candidate_sha256: 854d2d324033dac77771ed7145feabf0a659b3450d7b7579c54f487ae3f6ed20 ; independent_review: NOT_RUN
