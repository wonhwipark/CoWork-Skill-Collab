# CLAUDE v0.2.20 독립 R1 + B1~B3 + GitHub LIVE 활성화 결과 (GPT 판정용)

- 작성: Windows Claude Code (2026-11-15 KST). 호스트 실측과 자체 보고를 구분해 적었고, GPT 판정 전 canonical 아님.
- 근거: `GPT_V0220_R1_APPROVAL_AND_GITHUB_LIVE_ONE_SHOT_r0001_20261115.md`. 승인(R1·B1~B3·LIVE·Classic PAT)은 재질문하지 않았다.
- **결론: 독립 R1 PASS(BLOCKING 0) → B1·B2·B3 적용 → GitHub 단일 LIVE 활성화 완료.** 호스트에서 실측한 상태: `ACTIVE_PROVIDER=GITHUB`, Dropbox 감시기 Disabled·프로세스 없음, 2주기+재시작+중복 기동 방지 확인. 유료 모델 호출은 승인된 R1 1회뿐.

## 1. 필수 표

| 항목 | 결과 | 증거 종류 / 근거 |
|---|---|---|
| A_REVIEW_REQUEST_ID | `REQ-COWORK-V0220-R1-20261115` rev 1 (`REV-COWORK-V0220-20261115`, `POLICY-STATIC-V1`, effort medium) | 원격 commit A `e63321c4f7a0`, 서명 commit B(APPROVAL `90e2196c0284`, PIN `732eb80bbfa1`, READY 마지막 `2c26380a3240`) |
| R1_MODEL_CALLS | **1** | 감시기 감사 훅(하위 프로세스 2 = 인증 확인 + 리뷰), 디스패치 1, 재시도 0 |
| R1_TOTAL_COST_USD | **$0.3769412** (상한 $1의 38%) | 14 turns, 출력 6,759 토큰. R1 turn 목표(3)는 초과(강제 수단 없음) |
| R1_FINDINGS | **BLOCKING 0**, 비차단 1 | §3 |
| R1_INDEPENDENT_REVIEW | **PASS (독립 리뷰, 호스트 실측)** | 개발 세션과 분리된 별도 프로세스(Read/Grep/Glob, MCP 0, 세션 비저장). 구현자 자체 시험과 구분 |
| ZIP_SHA256_AND_SIZE | **PASS** `6a8626375e5e711535abdd261ff48781114802bb345cabe2ed5940b75968f386`, 239,432 B | 로컬 원본 검증 → PRIVATE 입력 게시 → 원격 원시 바이트·크기·SHA·CRC 일치 → 설치본 ZIP 바이트도 동일(정규 파일명으로 복사해도 sha 동일) |
| B1_CRYPTO_HOST | **PASS** | 운영 Python 3.11.9 venv에 `cryptography 50.0.2`·`cffi 2.1.1`·`pycparser 3.12`만 `--require-hashes --no-deps`로 설치(패키지 diff = 정확히 3개 추가). 운영 인터프리터로 전체 스위트 **674 passed / 12 skipped**(GUI 선택·환경 사유만 SKIP), 서명·승인 관련 116개 통과(정상·위조·변조·만료·다른 저장소·SOURCE_PIN 불일치 포함) |
| B2_NOTIFIER_WATERMARK | **PASS** | §4 |
| B3_GITHUB_WATCHER_TASK | **PASS** | §5 |
| N1_N2_RUNTIME | **PASS** | N2: 감시기가 매 승인 확인마다 서버 repo ID 조회(캐시 없음), 운영 신뢰 루트와 일치. N1: 리뷰 실행 중 원격 예약 기록 생성(`dispatch/…/DISPATCH_1.md`)·결과·영수증 PUT 3회 자동. 호스트 감시기에서 오래된 요청 4건 `APPROVAL_REJECTED`로 디스패치 0 |
| PENDING_1_PRESERVED | **PASS** | 원본 운영 DB(main/WAL) sha256 `4e8bc33a…`/`59de7507…`가 작업 전·후 동일, 수정 시각도 11-12 그대로. pending `L1-KNOWLEDGE-ROADMAP-DESIGN-20261109-001`·COMPLETED 60·CONFLICT 1 보존(이관·재리뷰·완료 처리 0). GitHub는 별도 상태 폴더 |
| DROPBOX_PROVIDER_STOPPED | **PASS** | `Claude-Review-Watcher` Disabled, 기동 전·후 다른 감시기 프로세스 0 |
| GITHUB_PROVIDER_SINGLE_LIVE | **PASS** | 새 상태 DB의 `provider_lease` = `github` 1행, `provider_history` 1행. 이중 LIVE 0 |
| TWO_CYCLES_AND_RESTART | **PASS** | 30초 주기로 7주기(사전 dry-run 1회 포함) 전부 `scan_ok`, Stop→잔여 프로세스 정리→Start 재시작 후에도 정상. 두 번째 Start 요청은 `IgnoreNew`로 무시(프로세스 2 유지), 수동으로 띄운 두 번째 watch는 단일 인스턴스 잠금으로 종료코드 3 거부 |
| TELEGRAM_DUPLICATES | **0** | 직접 관측 불가한 Telegram 대신 근거: 알림 대상 이벤트가 새 DB에 0건, Notifier 워터마크가 새 DB 끝까지 부트스트랩, 기존 DB 워터마크 22,907 불변. 테스트 발송·과거 재발송 0 |
| ROLLBACK_READY | **PASS (준비·격리 리허설)** | §6. 실운영 롤백은 실행하지 않음 |
| ACTIVE_PROVIDER | **GITHUB** | 호스트 실측 |
| CUTOVER | **LIVE** (`HOST_APPLIED=PASS`) | 호스트 실측(Task Running, 프로세스, 임대, 주기). 문서 게시만으로 선언하지 않음 |
| ACTUAL_MODEL_CALLS / PAID | **1 / $0.3769** | 승인된 R1 1회 외 0. 새 유료 smoke 없음 |
| UNVERIFIED / BLOCKED | §7 | |

## 2. 독립 R1 실행

- 로컬 ZIP 검증(크기·sha256·CRC·93개 파일·경로 이탈 0·비밀 스캔 0·필수 파일·버전) 통과 후에만 진행. 입력(ZIP·간결 manifest·v0.2.19→v0.2.20 diff 77줄/4파일)을 PRIVATE `review-inputs/REV-COWORK-V0220-20261115/`에 게시하고 원격 바이트 일치 확인(ZIP `454f88eed53f`, manifest `9ae968f90e84`, patch `b27d031f87dc`).
- 서명 승인 2시간 유효, 정식 계약(REQUEST→commit A 고정→APPROVAL/SOURCE_PIN→READY 마지막). 게시 중 `main`이 다른 커밋으로 움직여 HTTP 409가 한 번 났고(서명 파일은 쓰이기 전), 재서명 후 재시도했다.
- 드라이런(모델 0, GET 33) 뒤 실제 1회. 리뷰어 감시기는 리뷰 대상 v0.2.20 자신이며 결과·영수증·예약 기록을 **자동으로** 게시(PUT 3). 원격 readback: 결과 `ceff4d145c78`(9,280 B, 엔진 생성 바이트와 동일), 영수증 `0f79cd65c9e8`, 예약 `ae7e1213e3b7`, 사용영수증 `3bc7d3a5caa4`.

## 3. 리뷰 결과

- **BLOCKING 0.** `repository_id()` 캐시 필드 제거 확인, 호출부 `_check_approval`이 매 주기 서버 조회, ensure_auth·업로드·다운로드 경로는 ID를 저장하지 않음, SHADOW는 해당 검사 우회 경로 없음. 정상/다른 ID/403·timeout·5xx·속도 제한/ID 누락 모두 재시도·모델 0(fail-closed). 추가 GET은 새 엔드포인트·새 속도 제한 등급이 아님. 새 시험이 속성을 실제로 증명(가짜 서버가 호출마다 ID를 읽어 반환).
- 비차단 1: `remote_repo_id is not None` 가드를 죽은 코드로 보고 정리 제안. **내 판단: 의도된 가드**(신원 개념이 없는 전송 계층은 베이스 `Transport.repository_id()`가 `None`을 반환). 코드는 바꾸지 않았다(승인된 ZIP 바이트 보존). 향후 주석 추가 정도의 정리 항목.
- 리뷰어 미검증: 테스트 실행, SHADOW 전체 로직, 실제 속도 제한 여유. (실서버 동시 쓰기·예약 원시 동작은 이전 단계에서 검증.)

## 4. B2 Notifier (실호스트 적용)

- 변경 전 백업: 코드(`f0a17d7d…`), 워터마크 파일, Task 정의, 운영 DB 바이트 복사본·무결성 ok, 패키지 목록, 신뢰 루트(`591c22fc…`).
- 최종 Notifier = 기존 파일에서 **DB 목록(`notify_dbs.json`) + DB별 워터마크**만 추가(단일 인스턴스 잠금·메시지·이벤트·비밀 처리는 그대로). sha256 `3bd19b01670edd21`.
- 비발송 재시험 12/12 통과(복사본, 발송기 대체): 구 DB 워터마크 유지, 새 DB는 생성 전 건너뜀→등장 시 끝에서 부트스트랩(과거 3행 미발송)→첫 실이벤트 발송(누락 0), 반복·재시작 중복 0, 설정 파손 시 안전 복귀, 잠금 유지.
- 적용: Task 중지→잔여 프로세스 확인(0)→파일·설정 교체→Task 시작. 재기동 후 런처+자식 한 쌍, 워터마크 `last_id 22907` 유지 + 구 DB 키 22907 + 새 DB 키(부트스트랩) = 2개. 알림 발송 0.

## 5. B3 GitHub watcher 설치·LIVE

- 설치: 승인된 ZIP에서 새 폴더로 93개 파일 전부 바이트 동일 추출(+정규 파일명 사본의 sha 동일), 별도 상태 폴더, 비밀 없는 config(토큰 파일은 경로만 참조, Classic 쓰기 토큰). 정책: `POLICY-STATIC-V1`($1)·`POLICY-STATIC-V1-LARGE`($3) 등록, 일일 상한 $3·2회.
- Task `SKILL-COLLAB-GitHub-Watcher`(로그온 트리거, `IgnoreNew`, 실패 시 5분 간격 3회 재시작, 시간 제한 없음). 기동 전 조건 점검(Dropbox Task Disabled, 다른 감시기 프로세스 0) 통과 후 단독 시작.
- 실호스트 관측: 운영 인터프리터로 `config-check`·`scan --dry-run`(모델 0) → Task 시작 → 30초 주기 정상, 새 상태 DB 무결성 ok, 작업 0건(`jobs` 비어 있음), 이벤트는 만료된 이전 요청 4건의 `APPROVAL_REJECTED`뿐, `provider_lease=github`.
- 현재 LIVE가 처리하는 것: **유효한 서명 승인이 있는 새 REQUEST+READY만**. 이전 요청(V0214/V0217/V0219/V0220)은 승인 만료로 재디스패치 불가, 완료 결과가 있어 N1 가드·예약 기록으로도 이중 차단.

## 6. 롤백 준비

- `ops_backup_20261115/rollback_github_live.ps1`(미실행): ① GitHub Task 비활성·종료(데이터 폴더 보존) ② Notifier 코드·워터마크 원복, `notify_dbs.json` 제거 ③ 선택: crypto 3개 패키지 제거. Dropbox 재활성화는 별도 결정(단일 provider).
- 격리 리허설: 임시 venv에서 해시 고정 설치→제거로 패키지 목록이 빈 상태로 복귀, Notifier 원본 복원본 sha가 원본과 일치. Stop→Start 경로는 실호스트에서 이미 시험(재시작 PASS). 실제 롤백 실행은 하지 않았다.

## 7. 미검증 / 한계 / 후속

- **미검증(NOT_RUN)**: 실제 신규 유료 요청이 LIVE 감시기를 통해 처음 처리되는 흐름(승인 없이 새 유료 호출을 만들지 않으므로 의도적으로 하지 않음). 다음 정식 서명 요청이 오면 첫 실전 사례가 된다. 실제 Claude 사용량 한도 문자열 미관측, 별도 계정 enforce SHADOW·장기 SHADOW 미실행.
- Telegram 실제 수신 기록은 호스트에서 직접 관측하지 않았다(근거는 워터마크와 알림 대상 이벤트 0건).
- 운영 참고: `python` 프로세스 4개는 감시기 1쌍·Notifier 1쌍(각각 런처+자식)으로 정상. Task는 로그온 트리거라 재부팅 후 로그온 시 자동 기동. 이전 승인 요청은 모두 만료되어 새 리뷰는 새 요청 ID·서명이 필요하다.
- 승인 만료된 구 요청이 대기 목록(pending 4)에 남아 매 주기 재평가되며, 이벤트는 같은 프로세스 안에서는 1회만 기록되고 프로세스를 다시 시작하면 한 번 더 기록된다(알림 대상 아님).
- 비밀값·토큰·개인키·경로·계정명은 이 문서에 없다.
