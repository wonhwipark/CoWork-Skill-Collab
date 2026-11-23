# v0.2.32 후속 보완 원샷 결과 (Windows Claude Code)

- 작성: 2026-11-22 KST. Work: `COWORK-AUTO-APPROVAL-20261115-001`. 지시: `WINDOWS_V032_CORRECTIONS_ONE_SHOT_HANDOFF_r0001_20261122_KST.md`. 판정 입력: GPT `GPT_V032_PRELIVE_3_TO_9_DISPOSITION_r0001_20261122_KST.md`.
- **STATUS: 부분 완료. LIVE_READY=NO, LIVE_APPLY=NOT_RUN, 신규 리뷰·모델 호출·REQUEST/READY/서명 0.**
- **차단의 핵심:** 차기 후보 폴더(`v0_2_33`) 생성용 폴더 복사 명령이 권한 계층에서 두 번 거부되었다(§7). 우회하지 않았으므로 승인 경로 연결, 신규 시험 추가, 차기 ZIP 생성은 수행하지 못했다. 코드 변경 0.

## 1. 입력 고정

| 항목 | 값 | 판정 |
|---|---|---|
| v0.2.32 ZIP SHA-256 | `cbf95d1141cbed6973d6cace2950065b4ed5eb36e988ecf522a9fc3ab087fa94` | 실물 재확인 PASS |
| 크기/항목 | 295,885 B / 106 | 이전 결과와 일치 |
| v0.2.30·v0.2.31 구 ZIP | `541cd3f1…`, `1df85457…` | 변경 없음 |
| 라이브 | v0.2.29 Running, 설정·위임 SHA 불변(직전 검증) | 변경 없음 |

## 2. 단계별 결과

| 단계 | 결과 | 근거·한계 |
|---|---|---|
| 1. 시험 증거 연결 | PASS(재사용) / G3 프로세스 증거 NOT_RUN | 이전 Windows 결과의 race 시험은 **같은 OS 프로세스 안의 두 스레드**와 서로 다른 임시 DB를 사용했다. 서로 다른 OS 프로세스를 쓰는 시험은 없다. 모의 전송은 잠금으로 create-only를 흉내 냈다. 실제 GitHub 경합은 NOT_RUN(쓰기 금지) |
| 2. 승인 경로 연결(REUSE→CONNECT) | **BLOCKED_PERMISSION** | 차기 폴더 생성 거부. 코드 변경 없음. 연결에는 `REVIEW_INTENT` nonce 저장소(`review_intent_nonces`)가 필요하며, 설치 시 DB 테이블 추가 이행이 생긴다 |
| 3. 의도 검증 시험(보완) | 기존 범위만 PASS / 일부 **NOT_COVERED** | 기존 `review_intent` 시험 25건이 정확 바인딩, 위조, 변조, 만료, 미래 시점, 수명, 해지 키, 승인용 목적 키, 와일드카드, 본문 승인 주장, 재사용 nonce(동일 프로세스)를 다룬다. **미포함:** 재시작 후 nonce 재사용, 동시 nonce 소비, 소급 요청(통합 경로 없음). 모델 시작 불명 재시작은 기존 `test_lost_reservation…`/`test_crash…`가 봉인을 확인 |
| 4. 설치 트리 백업 | **BLOCKED_PERMISSION** | 필요 작업: `D:\User\whpark\skill-collab-watcher-github`(라이브 v0.2.29 읽기) → `D:\User\whpark\skill-collab-watcher-dist\backup_v0_2_29_precheck_20261122\install_tree_v0_2_29`. 계정 `ME`. Bash 복사 명령 2회 거부(첫 시도 전체 스크립트, 이번 세션 복사 명령). 다른 수단으로 재시도하지 않음. **필요 권한:** 이 복사 작업 허용 또는 허용된 읽기 전용 복사 방식 지정 |
| 4a. DB·설정·위임 백업 | PASS(이전) | `backup_v0_2_29_precheck_20261122\`: state.sqlite3(백업 API, integrity ok, 작업 12, 감사 최대 id 22804), reviewer.config.json SHA `2ead4007…`, auto_delegation.json SHA `6d826672…`, MANIFEST.json |
| 5. 롤백 준비 | **BLOCKED_PRESERVE / 복구 BLOCKED** | 기존 2026-11-20 번들은 **v0.2.25 설치 트리**(SHA `f691bcf8…`)이고 v0.2.29 트리 백업이 아니다. 2026-11-20 이후 완료 작업이 있어 과거 DB(작업 9)로 교체하면 이력이 유실된다. 따라서 DB 교체 금지. 코드 복원은 v0.2.29 트리 백업(단계 4)이 필요하다. 사본 복원 시험은 이전에 integrity ok, 최신 이력 유지 확인 |
| 6. 차기 후보 v0.2.33 | **BLOCKED_PERMISSION** | 단계 2와 동일 원인. ZIP 생성 없음 |
| 7. 독립 리뷰 | **BLOCKED_AUTH** | 이 패키지에 대한 유효 보호 승인·전달 허용 없음. 신규 REQUEST는 코드 ZIP을 PUBLIC 저장소에 올려야 하므로 불가. 기존 R1 재실행 없음. 유료 호출·REQUEST·READY·서명 0 |
| 8. 읽기 전용 SHADOW(사본) | PASS(사본 한정) | 재실행 결과 `dispatched=0`, `pending=8`, 모델 0, 쓰기 차단 래퍼. 라이브 DB는 읽기 전용 URI로만 접근. 라이브 감사 최대 id: 실행 전 22998 → 실행 후 22999. 증가분은 실행 중인 라이브 watcher가 남긴 자체 기록이다(SHADOW는 쓰지 않음). 설치·Task 기반 호스트 SHADOW는 NOT_RUN |

## 3. 시험 기록 (재실행 없음)

- 전체 후보 시험 994 PASS / 0 FAIL / 12 SKIP (v0.2.32, 이전 Windows 결과).
- 관련 신규: race·복구 9건, 의도 검증 25건(이전 수행).
- 이번 단계에서 새 시험을 실행하지 않았다(코드 변경 없음).

## 4. 운영 전후 상태

- 라이브 watcher 2개 Running(pid 30904/31848 기준, 직전 검증), 설치·설정·위임 SHA 불변.
- 운영 DB 쓰기 0, GitHub 업무 레코드 쓰기 0, Telegram 0, 신규 모델 호출 0, 디스패치 0.
- 키·trust root·위임·LIVE 설정 변경 0.

## 5. 공개 게시 판단

- 코드 ZIP은 PUBLIC 저장소에 게시하지 않는다. 이 결과 문서는 비민감 상태·SHA·경로 요약만 포함한다.
- 자격정보, 개인키, 운영 DB 사본, 백업 본문은 게시하지 않았다.

## 6. LIVE 판정

LIVE_READY = **NO**. 막힌 항목:
1. 차기 후보 생성과 승인 경로 연결(단계 2, 6) — 폴더 생성 권한 필요.
2. v0.2.29 설치 트리 백업(단계 4) — 복사 권한 필요. 현재 존재하는 번들은 v0.2.25 기준이다.
3. 독립 리뷰(단계 7) — 보호 승인 필요.
4. 호스트 실운영 SHADOW(단계 8) — 설치·Task 승인 필요.
5. 비용 무상한 위험 수용(10단계) — 사용자 결정.

## 7. 권한 거부 기록

- 대상: 폴더 복사 명령(라이브 설치 트리 읽기 → dist 백업 경로, 또는 candidate 폴더 → v0_2_33).
- 계정: `ME`. 호스트: Windows 11, Git Bash 도구.
- 현상: 도구 권한 계층이 명령을 거부. 우회하지 않음, 다른 복사 도구(PowerShell 포함)로 재시도하지 않음.
- 필요 권한: 위 두 복사 작업을 허용하거나, 허용된 읽기 전용 복사 방식을 지정.

## 8. NEXT_ONE_ACTION

사용자에게 복사 권한(v0_2_33 생성, v0.2.29 트리 백업) 허용 여부를 묻는다. 허용되면 단계 2·3·4·6을 이어서 수행한다. 10단계 비용 위험 수용과 LIVE는 별도 승인 전까지 진행하지 않는다.

---

## 9. 후속 실행 (2026-11-22, 최신 지시 1~3단계)

- **사전 확인:** 원격 `main`에 `759de9b87b6f`가 포함됨(`identical`, behind_by 0). 최신 지시서 `WINDOWS_V032_CORRECTIONS_ONE_SHOT_HANDOFF_r0001_20261122_KST.md` 재독.
- **§1 두 복사 — PASS:**
  - A. `cp -r .../candidates/v0_2_32_live_precheck .../candidates/v0_2_33` 성공. 파일 수 일치(소스 26, 테스트 58).
  - B. `cp -r D:\User\whpark\skill-collab-watcher-github .../backup_v0_2_29_precheck_20261122/install_tree_v0_2_29` 성공. `diff -rq`로 원본과 **IDENTICAL**. 파일 143개. 매니페스트 `INSTALL_TREE_v0_2_29_SHA256SUMS.txt`(143줄, 매니페스트 SHA `4bf920cd…`).
  - 이전 세션의 두 복사 거부는 이번 최신 지시 이후 재시도에서 허용되어 해소됨. 거부 원문 기록은 §7 참고.
- **§2 SCOPE 격리 연결 — PASS(격리):**
  - `review_intent.verify_review_intent`는 nonce를 콜백(`consume_nonce`)으로 받는다.
  - `StateStore.consume_review_intent_nonce`: `review_intent_nonces` 기본키 INSERT 한 번. 재시작과 여러 OS 프로세스에서도 1회만 성공.
  - `AutoApprover._intent_scope`: 커밋 A의 `REVIEW_INTENT.json`만 읽음. 검증 통과 시 **이 요청의 스킬 한 개**만 위임 범위에 추가.
  - 재검증(`_revalidate`): 후보 기록의 `intent_nonce`가 **이 요청 ID에 대해 소비되어 있을 때만** 범위를 인정. 그 외 `INTENT_NOT_CONSUMED_FOR_THIS_REQUEST`로 중단.
  - 순서: 서명 검증 → repo/request/revision/skill/commit/REQUEST·ZIP SHA·크기 바인딩 → 만료/미래 시점 → 소급(의도 발급 시각 < 요청 생성) 거부 → nonce 소비 → 기존 assess·서명·READY·원격 claim.
  - 수정 중 발견·보완: (a) 의도 발급 시각 비교를 초 단위로 맞춤(마이크로초 때문에 같은 초 내 "아직 유효하지 않음" 오거절). (b) 재검증이 확장 범위를 몰라 `POLICY_STOPPED`가 나던 문제를 nonce 소비 기록 기반 재검증으로 해결.
  - 신규 DB 테이블 `review_intent_nonces`는 **후보 코드와 temp DB에서만 검증**. 운영 DB 적용 시 `ensure_auto_tables`가 테이블을 만들므로 **운영 이행 요구로 기록**(이번 범위 밖, 미실행).
- **§3 누락 시험·회귀·패키징:**
  - `tests/test_v033_nonce_store.py` 3건: 재시작 후 재사용 거부, 읽기 전용 소비 불가, **두 OS 프로세스 경합 → 소비자 1명**(PID 2개 서로 다름, `nonce_worker.py`).
  - `tests/test_v033_intent_wiring.py` 10건: 정확한 의도 승인 → READY_POSTED·서명 1회, 의도 없음 → SCOPE, 본문 승인 주장 → SCOPE, 위조 → SCOPE, 다른 스킬 의도 → SCOPE, 만료 → SCOPE, 해지 키 → SCOPE, 승인 목적 키 → SCOPE, 요청보다 이른 의도 → SCOPE, 동일 nonce 재소비 거부.
  - `tests/test_v032_scope_intent.py` 25건은 새 콜백 시그니처로 갱신, 전부 PASS.
  - **최종 전체 회귀 1회: 1007 PASS / 0 FAIL / 12 SKIP** (v0.2.32 994 + 신규 13).
  - **v0.2.33 ZIP:** `D:\User\whpark\skill-collab-watcher-dist\candidates\v0_2_33_intent_wired_candidate.zip`, zip SHA-256 `4dc3c701a83c22b2615e244a9dfeca8bd07ef89e9456c1b182a7ec3c01293cda`, 297,249 B, 109 항목, CRC 정상, 중복 0, 경로 탈출 0, 심볼릭 링크 0, 민감정보 패턴 0, 트리 SHA `ab80c9f7d9c163a5d130076e7c0d502891cabb4e6248d958073b83ef7da8103c`. v0.2.32 ZIP(`cbf95d11…`)은 변경 없음.
- **시험 증거 한계(정직 기록):**
  - 두 OS 프로세스 경합은 **nonce 소비**에 대해서만 실증. **디스패치 claim 경합은 여전히 같은 프로세스 두 스레드 + 별도 DB** (NOT_RUN for cross-process dispatch, 실제 GitHub 경합 NOT_RUN).
  - 재시작 후 재사용·동시 소비는 저장소 시험으로 확인, 통합 경로 전체 재시작 시험은 **NOT_COVERED**.
  - 모델 시작 불명 ALREADY_OURS 봉인은 기존 `test_lost_reservation…`/`test_crash…`로 확인(이번 변경 무관, 회귀에 포함).
- **§4 설치 트리 백업 — PASS:** 위 B 항목. 백업 경로는 `backup_v0_2_29_precheck_20261122\install_tree_v0_2_29`. 이전 v0.2.25 번들은 v0.2.29 백업으로 취급하지 않음.
- **§5 롤백 — 판정 유지(BLOCKED_PRESERVE):** 현재 DB 이력이 2026-11-20 번들 이후 진행되었으므로 과거 DB로 교체하지 않음. 코드 롤백 원본은 이제 §4 트리 백업으로 존재. 운영 DB 복원·이행 0.
- **§6 독립 리뷰 — BLOCKED_AUTH:** v0.2.33 패키지에 대한 유효 보호 승인·전달 허용 없음. 신규 REQUEST·READY·서명·모델 호출 0. 기존 R1 재실행 없음. 키·trust root·위임·LIVE 활성화 0.
- **§7 도구 거부 기록:**
  - 이전 세션: 원본 복사 명령이 권한 계층에서 2회 거부됨(원문은 명령 실행 결과로 "Permission to use Bash with command … has been denied"). 우회하지 않음.
  - 이번 세션: 최신 지시 이후 A·B 복사 명령은 거부되지 않고 성공.
- **운영 상태:** 운영 DB·GitHub 업무 레코드·Telegram 쓰기 0, LIVE 설치·Task·Notifier 변경 0, 호스트 SHADOW 설치 0. 이번 단계에서 watcher/Notifier 프로세스를 종료·재시작하지 않음.
- **LIVE_READY = NO.** 남은 승인: 독립 리뷰 보호 승인, 운영 DB 이행 승인(review_intent_nonces), 비용 무상한 위험 수용(10단계), LIVE 컷오버 승인.

---

## 10. 기술 마무리 원샷 (2026-11-22, 최신 지시서 범위: 시험→보완→패키징→독립 리뷰 조건→SHADOW·복구→게시)

- **입력:** 후보 `v0_2_33`, 이전 ZIP `v0_2_33_intent_wired_candidate.zip`(SHA `4dc3c701…`) 보존. 이번 시험 보완으로 소스가 바뀌어 **새 리비전 ZIP `v0_2_33_r2_intent_wired_candidate.zip`** 생성.

### 10.1 시험·보완 (PASS, 실제 OS 프로세스 사용)
- **다른 DB 두 watcher, 같은 ID/revision/PIN/ZIP, 원자적 공유 디스패치 기록:** `tests/test_v033_process_dispatch.py::test_two_os_processes_…` **PASS**. 두 OS 프로세스(서로 다른 PID, 서로 다른 DB), 공유 디렉터리 `O_CREAT|O_EXCL`을 디스패치 기록으로 사용, barrier 도달 후 경합. 모델 호출 합계 1, 디스패치 1, 패자는 REVIEW_UNCERTAIN, 원격 기록 1개. *원격 GitHub 실경합은 NOT_RUN(쓰기 금지).*
- **모델 호출 중 프로세스 강제 종료 → 재기동:** `test_a_process_killed_…` **PASS**. 종료 코드 3(모델 진입 직후 `os._exit`), 재기동 프로세스에서 봉인 후 모델 호출 0, UNCERTAIN 1.
- **nonce 소비:** 재시작 후 재사용 거부, 읽기 전용 소비 불가, 두 OS 프로세스 경합 시 소비자 1명 — **PASS**(`test_v033_nonce_store.py`).
- **재검증(_revalidate)이 소비 기록으로 권한·만료·키·바인딩을 대체하지 않음:** **PASS**. 변경 없음 상태는 통과. 의도 키 해지 → `INTENT_KEY_NOT_ACTIVE`, 위임 비활성 → `DELEGATION_DISABLED`, 소비되지 않은 nonce → `INTENT_NOT_CONSUMED_FOR_THIS_REQUEST`로 중단. 이를 위해 재검증에 신뢰 루트 전달 경로를 추가하고 전 호출 지점을 맞춤(누락된 `_sign_and_post` 호출 1건을 시험으로 발견·수정).
- **rev1 의도로 rev2 요청 승인 시도:** 거부(`SCOPE`), 서명 0 — **PASS**.
- **전체 회귀:** **1014 PASS / 0 FAIL / 12 SKIP** (이전 1007 + 신규 7).
  - SKIP 8: `test_secret_prompt.py` 실창 시험. `SKILL_COLLAB_GUI_TESTS=1`로만 실행하도록 설계된 옵트인.
  - SKIP 4: `test_windows_scripts.py`. Windows 호스트 `.venv` 필요 조건.

### 10.2 패키지 (r2 동결)
- 파일: `D:\User\whpark\skill-collab-watcher-dist\candidates\v0_2_33_r2_intent_wired_candidate.zip`
- **zip SHA-256 `23579a5c8c6690b5831116410fc623e3a8bbc5c659cb6fdea8628e765fa7c206`, 301,136 B, 111 항목**, CRC 정상, 중복 0, 경로 이탈 0, 링크 0, 민감정보 패턴 0.
- **트리 SHA-256 `e4ecdc4c9d141ec76be922410dcd0ea1eb8e3598c6df01a80908ccfadf4cd0e0`**
- 구 ZIP 보존: v0.2.33 `4dc3c701…`, v0.2.32 `cbf95d11…`, v0.2.31 `1df85457…`, v0.2.30 `541cd3f1…`.

### 10.3 독립 리뷰 — **BLOCKED_AUTH**
- 원격 `collab/requests`에 이 후보(v0.2.32/v0.2.33 명칭·INTENT·CORRECTION)와 연결된 요청 폴더 없음 — 확인 명령 exit=1, 결과 없음.
- 이 ZIP은 공개 저장소에 올려야 검토 요청이 가능하고, 그 전달 허용이 확인되지 않았음. 게시·전달을 하지 않았음.
- REQUEST·READY·APPROVAL·모델 호출 0. 기존 R1 재실행 없음. 개발 세션과 분리된 리뷰는 **사용자의 보호 승인 확인 후에만 가능**.

### 10.4 SHADOW·복구 리허설
- **호스트 SHADOW(라이브 DB 사본, 읽기 전용 URI, 쓰기 차단 전송, 모델 실행기 차단):** 디스패치 0, 대기 8, 모델 0. 라이브 감사 최대 id `23349 → 23350`. 증가 원인은 **실행 중인 라이브 watcher 기록으로 추정**(SHADOW 쓰기 경로 없음, 대조는 미확인). 설치·Task 기반 호스트 SHADOW는 **NOT_RUN**(설치 승인 필요).
- **복구 리허설(백업 DB 임시 사본):** 백업 파일 불변(`BACKUP_UNCHANGED True`). 사본 무결성 ok. 이력 유지: 작업 12/12 완료, 자동 클레임 5, 감사 22804. `review_intent_nonces` 테이블은 **사본에만** 생성되고 두 번 적용해도 idempotent. 같은 nonce 두 번째 소비 거부.
- **이행 계획(운영 미적용):** 첫 기동 때 `ensure_auto_tables`가 테이블을 만든다. 구 코드는 추가 테이블을 무시하므로 역호환. 롤백은 테이블 삭제 또는 구 코드 복원. **운영 승인 전 적용 금지.**

### 10.5 운영 상태 전후
- 라이브 설치 트리 `b0134258…`(v0.2.29) 불변. 설정·위임 해시 불변(이전 검증 기준). GitHub watcher·Notifier 둘 다 Running(읽기 전용 확인).
- LIVE 설치·활성화 0, 운영 DB 쓰기·이행 0, Task/Notifier 변경 0, 키·정책·위임 변경 0, 신규 모델 호출 0.

### 10.6 차단·미실행 (정직 기록)
| 항목 | 상태 | 사유·필요 조치 |
|---|---|---|
| 독립 리뷰 1회 | BLOCKED_AUTH | 유효 보호 승인·코드 ZIP 전달 허용 없음 |
| 실제 GitHub 경쟁 쓰기 | NOT_RUN | 쓰기 금지 |
| 호스트 SHADOW(설치·Task) | NOT_RUN | 설치 승인 필요 |
| 운영 DB 이행(review_intent_nonces) | BLOCKED | 운영 이행 승인 필요 |
| 비용 무상한 위험 수용(10단계) | BLOCKED | 사용자 결정 |
| LIVE 컷오버 | BLOCKED | 최종 승인 필요, 이번 범위 밖 |

- **LIVE_READY = NO.**

---

## 11. r2 정식 REQUEST·독립 리뷰 실행 (2026-11-22, 사용자 "r2 ZIP PUBLIC 게시 허용")

### 11.1 실물 검증
- 입력 ZIP `v0_2_33_r2_intent_wired_candidate.zip`: SHA-256 `23579a5c8c6690b5831116410fc623e3a8bbc5c659cb6fdea8628e765fa7c206`, 301,136 B, 111 항목. 재확인 PASS.
- 원격 게시 파일 `collab/packages/v0_2_33_r2_intent_wired_candidate.zip`: 바이트 SHA-256 동일, 크기 301,136. PASS.
- 기존 요청 대조: 이 후보에 연결된 요청 없음(목록 대조 PASS). 중복 없음.

### 11.2 정식 제출 (공식 `collab/ops/submit_review_request.py`, 깨끗한 main 클론 `publish_clone` 사용)
- 드라이런 `PREPUBLICATION_PASS_NOT_SUBMITTED`(manual, auto 두 경로) 후 `--publish`.
- 요청 ID `REQ-COWORK-V033-R2-WATCHER-REVIEW-20261122` rev 1, `skill_id=cowork-review-watcher`, `POLICY-STATIC-V1`, STATIC_ONLY, WINDOWS.
- Commit A `dbcfccac2d8552e9aa536a8ffd61671b6488ff40`: REQUEST + ZIP. 원격 readback 일치.
- Commit B `9e8175a3c6f135be778eaffe065ae2d3027959be`: SOURCE_PIN(`repo_id` `"1451933830"` 문자열, commit = A). 원격 readback 일치.

### 11.3 보호 승인·READY (기존 감시기 자동 경로, 사람의 수동 서명 없음)
- 감사: `AUTO_RESERVED` 300 cents → `AUTO_SIGNED_LOCAL` → `AUTO_APPROVAL_POSTED` → `AUTO_READY_POSTED`(2026-11-22 13:55 UTC).
- `APPROVAL_SIG.json` 커밋 `3036e4a8de`, 서명 키 `cowork-approver-1`, 만료 2시간, 요청·ZIP·PIN 바인딩 일치.
- `READY.md` 커밋 `4539852c7e`(승인 다음, 마지막). 순서 PASS.

### 11.4 독립 리뷰 1회 (감시기 디스패치)
- `DISPATCH_1.md` 커밋 `6781f02` (2026-11-22 22:57 KST).
- 감사: `VALIDATED` → `CLAIMED` → `REVIEW_DISPATCHED`(1회) → `REVIEW_COST` → `COMPLETED`.
- **실제 비용 USD 1.0571709999999999**(감사 DB, 상한 3.0 이내), 내부 턴 36, 디스패치 **모델 호출 1회**(max_calls=1), 중복 0, UNCERTAIN 0.
- `REVIEW_RESULT_1.md` 커밋 `f2d05a3`, 크기 9,479 B, SHA-256 `bf6f299dc5d192d04a0f0c19e73775e03040748c5f9a342b70672c5684c3ffe6`, `execution_status=COMPLETED`, STATIC_ONLY.
- `RECEIPT_1.md` 커밋 `5854d37`, SHA-256 `52cfd63bd71fe90ebd431316233dc09520e7411762a1f748576960a6662ca163`, `ok=true`, `watcher_version=0.2.29`, 패키지 SHA 일치.

### 11.5 리뷰 결과 요약 (GPT가 판정, 이 문서는 통합 판정 아님)
- **BLOCKING: 0.**
- 비차단 1: 의도 nonce는 전체 검증 뒤에만 소비됨 — 정상 설계로 확인.
- 비차단 2: `package_size`를 문자열로 비교하는 바인딩 — 발행 도구가 정수 10진수만 쓰는지 확인 필요(후속 확인 항목).
- 비차단 3: 예산 인자 제거와 금액 상한 제거 확인, 서명자 게이트(`max_day_*`, 재검증 window) 유지 확인.
- 비차단 4: 크로스 프로세스 디스패치 원자성은 **원격 전송의 create-only 실제 구현에 의존**. 리뷰어는 실제 GitHub/Dropbox 전송 원자성을 읽지 않았다고 명시. → **실제 전송 원자성 검증은 여전히 NOT_RUN.**
- 비차단 5: `seal_interrupted`/`exclusive` 연결 확인.
- 리뷰가 지적한 사항은 이번 단계에서 코드 변경하지 않음. 같은 Work 후속 범위로 남김. 수정 후 새 SHA는 이번 리뷰 완료로 승격하지 않음.

### 11.6 미수행·경계
- 개정 코드 재리뷰 없음(자동 2회 리뷰 금지). LIVE 설치·활성화 0, 운영 DB 이행 0, 위임·키·정책·Task·Notifier 변경 0.
- 원격 실제 전송 원자성 NOT_RUN.
- 호스트 설치 SHADOW NOT_RUN.
- 10단계 비용 위험 수용 BLOCKED(사용자 결정), LIVE 컷오버 BLOCKED.

- **LIVE_READY = NO.**

---

## 12. Windows 최종 기술 마무리 — QA28·F1/F2/F3·신규 ZIP v0.2.34 (2026-11-23 KST)

**판정 요약:** Windows에서 실행한 결과만 PASS로 기록. F1·F2 수정 완료, F3는 설계 결함으로 **BLOCKED**(기능 미발행, fail-closed 유지). 신규 독립 리뷰 미실행. LIVE 미적용.

### 12.1 착수 대조 (REUSED_WITH_EVIDENCE)
- 원격 `main` 최신 `cbb1019224fd`(2026-11-22T14:37Z) 확인. r2 보고 §11(정식 요청 `REQ-COWORK-V033-R2-WATCHER-REVIEW-20261122`, 보호 승인 `3036e4a8de`, READY `4539852c7e`, DISPATCH `6781f02`, RESULT `f2d05a3`, RECEIPT `5854d37`) **재사용**. r2 리뷰는 재실행하지 않음.
- GPT 판정 `GPT_V033_R2_INDEPENDENT_REVIEW_DISPOSITION_r0001_20261122_KST.md`의 보완 대상 F1/F2/F3 확인. 보완 입력: `cost_gate_removal_r2_r0001.patch` SHA `28d6b6db…`(39,061 B), 매니페스트 `cost_gate_removal_r2_r0001.json`, 실패 기록 `cost_gate_tests_r0001.json`(28 노드). 모두 원격에서 내려받아 SHA 확인.

### 12.2 비용 기반 차단 제거 패치 적용 (PASS)
- 입력 기준 r2 ZIP `23579a5c…` 폴더 `v0_2_33`의 12개 대상 파일이 매니페스트 before 해시와 **12/12 일치** 확인 후 `v0_2_34` 복사본에 `git apply`.
- 적용 후 8개 파일이 CRLF 혼재 상태였음. CRLF→LF 정규화 시 매니페스트 after 해시와 **정확히 일치**(GPT replay 바이트 기준). 정규화 후 12/12 after 일치.
- 패치 대상: auto_approval, auto_policy, cli, config, state_store, review_request_gate(tools), 관련 시험 6개, 신규 `test_cost_gate_removal.py`.
- 잔여 참조(의도적 유지, 신규 독립 경로 아님): `tools/review_request_gate.py`의 `required_budget` 인자는 레거시 unified/skill/design 호환 경로. `notify_events.py`의 `PER_REQUEST_COST` 문구는 죽은 문자열. `auto_policy`의 `max_request_cents`는 0 고정 비활성 필드. 신규 `independent` 접수 경로의 금액 게이트는 없음(게시·시험으로 확인).

### 12.3 Windows QA28 (실제 실행, PASS 28/28)
- 명령: `.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider <28 노드>` in `v0_2_34`. 노드 목록은 `cost_gate_tests_r0001.json`의 정확 28개.
- 결과: **exit 0, PASS 28, FAIL 0, SKIP 0**, 70.8초. 요약 `windows_qa28_summary.json` SHA `8491f540…`(F1 수정 후 재실행 값). 최초 실행(F1 수정 전)도 28/28 PASS.
- GPT의 Linux 환경 실패 28건은 **Windows 실행에서 통과**. Linux 환경 차이로 판단(원인 세부는 미분석).
- 실행 호스트: 본 Windows Claude 세션(인계서 수신·실행 확인, HOST_EXECUTION=CONFIRMED_THIS_SESSION).

### 12.4 F1 — 소비 후 의도 만료 재검증 (PASS, 수정)
- 원인: 재검증이 현재 위임만 확인하고 의도의 서명·만료·바인딩을 다시 보지 않았음.
- 수정: 후보 기록에 `intent_envelope`(서명된 의도 원문)·`intent_expected`(바인딩 값)를 보존. 재검증은 **같은 서명 검증을 현재 시각·현재 신뢰 루트로 재수행**하며, nonce는 **새로 소비하지 않고** 소유자만 확인. 실패 사유는 `CURRENT_POLICY:INTENT_<코드>`.
- 신규 시험: `test_revalidation_refuses_after_the_consumed_intent_itself_expires` PASS(만료 전 통과, 만료 후 `INTENT_EXPIRED`). 기존 재검증 시험(키 해지·위임 비활성·미소비 nonce)도 PASS.

### 12.5 F2 — 릴리스 매니페스트 (PASS, 재생성)
- `docs/RELEASE_MANIFEST.json`을 실제 파일 기준으로 재생성: version `0.2.34`, baseline `0.2.33-r2`(sha `23579a5c…`), 자기 파일만 제외(`self_excluded_path`), **112개 파일** 목록(바이트·SHA-256).
- 신규 시험 `test_release_manifest_v034.py` 3건 PASS: 버전, 모든 항목 크기·해시 일치, 목록과 실물 집합 일치.
- ZIP 내부 파일도 매니페스트와 **112/112 일치**, 여분 파일 0.

### 12.6 F3 — Commit A 자기 참조 (BLOCKED, 미구현)
- 문제: 의도 파일을 Commit A 안에 넣을 수 없다(A는 서명 전에 이미 생성). 현재 `_intent_scope`는 A에서만 읽으므로 **실제 발행 흐름에서 의도 경로는 성립하지 않는다.** 보안 우회가 아니라 기능 미발행이며, 항상 `SCOPE`로 거절된다(fail-closed 유지).
- 필요한 구현: A 이후 고정 스냅샷(커밋 C)에 의도를 두고, 최초 검증 시 C를 고정·기록하여 이후 교체로 권한이 바뀌지 않게 함. 이를 위해 전송 계층에 **경로별 커밋 이력 조회**(GitHub `commits?path=`)와 시험용 가짜 GitHub의 이력 지원이 필요한데 현 코드에 없음.
- 상태: **BLOCKED**. 다음 후보에서 전송 API 추가 후 로컬 실제 Git 시험(A→C 생성, 정확 revision/재시작/만료/경합) 필요.

### 12.7 전체 Windows 회귀 (PASS 1065 / FAIL 0 / SKIP 12)
- 명령: `pytest tests -q -rs` in `v0_2_34`. **1065 passed, 12 skipped, 15 subtests passed, 104.6초.**
- SKIP 12: `test_secret_prompt.py` GUI 실창 8건(`SKILL_COLLAB_GUI_TESTS=1` 옵트인), `test_windows_scripts.py` 4건(후보 폴더 안 `.venv` 필요 — 환경 조건이며 이번에는 미실행, NOT_RUN).
- 보안·중복·만료·원본 검증은 전체 회귀에 포함: 위조 서명·변조·만료 위임·중복/UNCERTAIN 봉인·재실행 방지 시험 포함(전체 PASS).

### 12.8 신규 ZIP v0.2.34 (구버전 보존)
- 파일: `D:\User\whpark\skill-collab-watcher-dist\candidates\v0_2_34_intent_scope_candidate.zip`
- **zip SHA-256 `ecb071c4a57b48d9d3ff00e713df35fc086db7c1127b5dc31ef00c358f4f2160`, 304,880 B, 113 항목**(매니페스트 112 + 자기 매니페스트 1)
- CRC 정상, 중복 0, 경로 탈출 0, 심볼릭 링크 0, 민감정보 패턴 0. 매니페스트 대비 불일치 0.
- 트리 SHA-256 `bc705c744d8ad14027886b7c400d9e6338a5bf10e2dfe85d5e12bb1d361346da`
- 구버전 보존: v0.2.33 r2 `23579a5c…`, v0.2.33 `4dc3c701…`, v0.2.32 `cbf95d11…`, v0.2.31 `1df85457…`, v0.2.30 `541cd3f1…`.
- 코드 ZIP은 공개 저장소에 게시하지 않음(r2 허용 범위 밖).

### 12.9 정책 동기화 매트릭스 (코드 근거, 실운영 미실행)
| 단계 | 현행 신규 독립 리뷰 경로 | 금액 차단 |
|---|---|---|
| 접수(게시자) | `check_request_for_publication(intent="independent")`, 가격 매개변수 없음 | 없음 |
| 서명(보호 signer) | 위임·의도·원본 검증 후 서명, 상한 `max_request_cents`는 0 비활성 | 없음 |
| READY | 서명 뒤 마지막 게시 | 없음 |
| watcher 디스패치 | `max_calls=1`, `--max-budget-usd` 인자 미전달 | 없음 |
| 알림·표시 | 완료 알림은 독립 리뷰로 표기(비용 기록은 사후 영수증) | 없음 |

### 12.10 LIVE 적용 준비 판정
- **LIVE_READY = NO.** 이유: (1) F3 미구현, (2) 호스트 설치 SHADOW NOT_RUN, (3) 실제 GitHub 전송 원자성 NOT_RUN, (4) 운영 DB 이행(`review_intent_nonces`) 미승인, (5) 비용 무상한 위험 수용 미결정(10단계), (6) 최종 LIVE 승인 미수령.
- **LIVE 변경 범위(예정, 미실행):** 설치 트리 v0.2.29 → v0.2.34(112 파일), 설정 변경 없음(기존 `reviewer.config.json` 유지), 위임·키·trust root 변경 없음, Task/Notifier 변경 없음, 운영 DB는 `review_intent_nonces` 추가 테이블만(추가 전용, 기존 이력 불변).
- **백업:** 설치 트리 v0.2.29 `backup_v0_2_29_precheck_20261122\install_tree_v0_2_29`(143 파일, 원본과 IDENTICAL, 매니페스트 `INSTALL_TREE_v0_2_29_SHA256SUMS.txt`). DB 스냅샷 `backup_v0_2_29_precheck_20261122\state.sqlite3`는 2026-11-22 시점이므로 **컷오버 직전 새 백업 필수**. 키·위임 사본은 게시 금지, 로컬 보존.
- **롤백:** 설치 트리를 백업으로 복원 → 워처 정지 상태에서 DB 교체 없이 현재 DB 유지 → 설정·위임 해시 확인 → Task 시작 → 버전 0.2.29, `WATCH_START` 확인. 새 nonce 테이블은 구 코드가 무시하므로 역호환. 과거 DB 교체·테이블 DROP 금지.

### 12.11 차단·미실행 요약
| 항목 | 상태 |
|---|---|
| QA28 | PASS 28/28 (Windows 실행) |
| F1 | PASS (수정·시험) |
| F2 | PASS (재생성·시험) |
| F3 | BLOCKED (전송 이력 API·가짜 GitHub 확장 필요) |
| 전체 회귀 | PASS 1065 / FAIL 0 / SKIP 12 (SKIP: GUI 8, .venv 스크립트 4 NOT_RUN) |
| 신규 독립 리뷰 | NOT_RUN (GPT 판정 후 새 고정 입력에서만, 보호 승인 필요) |
| 호스트 설치 SHADOW | NOT_RUN |
| 실제 GitHub 전송 경쟁 | NOT_RUN |
| 운영 DB 이행 / LIVE 설치 / Task·Notifier·키·위임 변경 | NOT_RUN (최종 승인 전) |

- **LIVE_READY = NO.**

---

## 13. F3 커밋 고정 구현 + 최종 Windows 검증 + LIVE 준비 (2026-11-23 KST)

**요약:** F3 구현·시험 PASS. v0.2.35 ZIP 생성. **독립 리뷰 BLOCKED_AUTH**(ZIP 공개 게시 허용 없음). **LIVE 활성화 BLOCKED**(최종 승인 없음). LIVE=OFF 유지, LIVE_READY=NO.

### 13.1 F3 구현 (커밋 고정 방식)
- 전송 계층 최소 확장: `commits_touching(path, limit)`(GitHub `commits?path=&sha=`), `is_ancestor(A, C)`(GitHub `compare`의 `ahead`/`identical`). 기반 클래스는 기본 거절.
- 승인기 `_intent_scope`: 의도 파일을 커밋 A에서 찾지 않고, 경로별 커밋 이력에서 **정확히 1개** 커밋 C를 찾는다. 조건: C ≠ A, A가 C의 조상, C에서 REQUEST·패키지 바이트가 A와 동일, 그 뒤 서명·바인딩·만료·nonce 검증. 실패는 모두 fail-closed.
- 고정: 후보 기록에 `intent_commit`(C), `intent_raw_sha`(원문 해시), `intent_path`, 원문 `intent_envelope`, 바인딩 `intent_expected`를 저장.
- 재검증: 저장된 C에서 의도 원문을 다시 읽어 **해시·원문이 기록과 같아야** 통과. 이후 HEAD에 새 의도를 올려도 기존 승인은 바뀌지 않는다(시험 확인).
- nonce 소비는 기존 원자적 저장(기본키 INSERT) 유지, 재검증은 소비하지 않고 소유자만 확인.

### 13.2 F3 시험 (Windows PASS)
- `tests/test_v035_commit_pinned_intent.py` 6/6 PASS: 정상 고정, 승인 후 교체해도 기존 승인 유지, A보다 이전 커밋의 의도 거절, 의도 커밋 2개(모호) 거절, 커밋의 REQUEST 바이트가 A와 다르면 거절, 사이드 커밋(main 이력 밖)은 보이지 않아 거절.
- `tests/test_v033_intent_wiring.py` 15/15 PASS(커밋 방식으로 재배선), `test_v033_nonce_store.py` 3/3, `test_v032_scope_intent.py` 25/25 PASS.
- **실제 Git CLI 의미 검사** `real_git_semantics_check.py` 6/6 PASS(임시 저장소): 경로별 커밋 최신순 목록, A가 C의 조상, C가 A의 조상 아님, 사이드 커밋이 main 이력 밖, 이른 의도 커밋이 A의 후손 아님. → 가짜 GitHub 계약과 실제 Git 의미 일치 확인.
- **한계:** 실제 GitHub 원격 쓰기 경합은 NOT_RUN(쓰기 금지). 가짜 GitHub는 선형 브랜치 모델.

### 13.3 F1 / F2 / QA28 / 전체 회귀
- F1 PASS(§12.4 보존). F2 PASS(v0.2.35 매니페스트 113 파일 재생성, `.venv` 제외, 시험 3건 PASS).
- **QA28 Windows 재실행: 28/28 PASS**(exit 0).
- **Windows 미실행 시험 4건 해결 PASS:** `test_windows_scripts.py` 4/4. 후보 루트에 `.venv`가 필요해 기존 watcher venv를 가리키는 **임시 junction**을 만들어 실행한 뒤 junction만 제거(원본 venv 무결 확인).
- **전체 회귀: 1075 PASS / 0 FAIL / 8 SKIP.** SKIP 8은 `test_secret_prompt.py` GUI 실창 시험(옵트인 `SKILL_COLLAB_GUI_TESTS=1`). 실제 창을 띄우고 사용자 입력을 요구하므로 무인 세션에서 실행하지 않음(NOT_RUN, 사유 기록).

### 13.4 신규 ZIP v0.2.35
- 파일: `D:\User\whpark\skill-collab-watcher-dist\candidates\v0_2_35_intent_scope_candidate.zip`
- **zip SHA-256 `658a6f3da8bd018b96b64453892aec77d96868e19bc5788745c1591b1729a740`, 307,418 B, 114 항목**(매니페스트 113 + 자기 매니페스트 1)
- CRC 정상, 중복 0, 경로 탈출 0, 링크 0, 민감정보 0. 매니페스트 대비 불일치 0. 트리 SHA `fac132f3ceaa8e4065267d6fa08f88695ad15bf33ebbc82e7e18d16267c56816`. `.venv` 제외 확인.
- 구버전 보존: v0.2.34 `ecb071c4…`, v0.2.33 r2 `23579a5c…`, v0.2.33 `4dc3c701…`, v0.2.32 `cbf95d11…`.

### 13.5 독립 리뷰 — BLOCKED_AUTH
- 리뷰 흐름은 REQUEST+ZIP을 PUBLIC 저장소에 올려야 한다. v0.2.35 ZIP 공개 게시 허용은 기록에 없다(r2 ZIP 한 건 허용만 존재). 지시서도 "코드 ZIP PUBLIC 게시는 별도 승인 없이 금지"로 명시.
- 따라서 게시·REQUEST·승인·READY·모델 호출 **모두 0**. 기존 r2 리뷰는 재실행하지 않음.
- 필요한 사용자 조치: v0.2.35 ZIP 공개 게시 1회 허용 여부.

### 13.6 LIVE 준비 점검 (읽기 전용·사본)
| 항목 | 결과 | 근거 |
|---|---|---|
| 설치 버전 비교 | 운영 **v0.2.29** / 후보 **v0.2.35** | 운영 tree `b0134258…`, 설정 `2ead4007…`, 위임 `6d826672…` 불변 확인 |
| Task·Notifier | GitHub watcher **Running**, Notifier **Running**, 나머지 Disabled | 읽기 전용 검증 |
| provider 단일성 | lease `github` 1행 | 읽기 전용 검증 |
| DB 무결성 | integrity ok | 읽기 전용 |
| 새 DB 백업 | `backup_live_db_20261123\` 생성·검증 | 작업 13(완료 13), claims 6, 감사 최대 id 24873, 복구 사본 integrity ok, 설정·위임 SHA 일치 |
| 설치 트리 백업 | 2026-11-22 `install_tree_v0_2_29`(143 파일, 원본과 IDENTICAL) | 설치 직전 재검증 필요 |
| 사본 SHADOW(v0.2.35) | PASS(사본 한정) | 디스패치 0, 대기 9, 모델 0, 쓰기 차단. 라이브 감사 증가 원인은 **미확인**(상수 출력 주의) |
| 호스트 설치 SHADOW | NOT_RUN | 설치·Task 승인 필요 |
| 실제 GitHub 전송 경합 | NOT_RUN | 쓰기 금지 |
| `review_intent_nonces` 이행 | 필요(F3·의도 경로가 사용) | 추가 전용 테이블. 구 코드는 무시해 역호환. 이행은 승인 필요, 미실행 |
| 비용 추적 | REVIEW_COST 기록 유지(사후 영수증) | 코드 경로 확인. 상한 없는 단일 실행 위험은 사용자 수용 필요 |

### 13.7 LIVE 활성화 — BLOCKED (최종 승인 필요)
- 기존 운영 승인은 **v0.2.29 컷오버**에 대한 것이며 v0.2.35 설치를 포함하지 않음. 지시서 역시 설치·DB 이행·Task/설정/키/위임 변경은 최종 승인 전 금지.
- 변경 범위(승인 요청 대상): (1) watcher 작업 안전 정지, (2) 설치 트리 v0.2.29 → v0.2.35(113 파일), (3) DB에 `review_intent_nonces` 추가(추가 전용), (4) watcher 작업 재시작. 설정·위임·키·trust root·Task 정의·Notifier·Bridge는 변경하지 않음.
- 위험: 단일 실행 모델 비용 상한 없음(외부 CLI 1회, 시간 제한만). F3 경로는 실제 GitHub에서 아직 미검증.
- 롤백: watcher 정지 → 설치 트리를 백업(2026-11-22 트리)으로 복원 → DB는 교체하지 않음(현재 이력 유지, 신규 테이블은 구 코드가 무시) → 설정·위임 해시 확인 → watcher 시작 → 버전 0.2.29, `WATCH_START` 확인.
- 실운영 검증(정상 요청의 승인→READY→DISPATCH→RESULT, 실제 모델 호출)은 **유효한 실행 권한과 최종 승인 후에만** 수행.

### 13.8 차단·미실행 요약
| 항목 | 상태 |
|---|---|
| F3 커밋 고정 구현·시험 | PASS(Windows, 가짜 GitHub + 실제 Git 의미 검사) |
| F1 / F2 | PASS |
| QA28 | PASS 28/28 |
| Windows 스크립트 시험 4 | PASS 4/4 (임시 junction) |
| 전체 회귀 | PASS 1075 / FAIL 0 / SKIP 8 (GUI 실창 옵트인, NOT_RUN) |
| v0.2.35 ZIP | 생성·검증 완료 |
| 독립 리뷰 | BLOCKED_AUTH (ZIP 공개 게시 승인 필요) |
| 실제 GitHub 경합 | NOT_RUN |
| 호스트 설치 SHADOW | NOT_RUN |
| DB 이행·LIVE 설치·Task 변경 | BLOCKED (최종 승인 필요) |
| 실운영 모델 검증 | NOT_RUN (실행 권한 필요) |

- **LIVE_READY = NO. LIVE = OFF(변경 없음).**
- **사용자 최종 승인 1회 요청 항목:** (a) v0.2.35 ZIP 공개 게시 1회(독립 리뷰용), (b) 위 §13.7 LIVE 변경 범위 설치·DB 추가 테이블·watcher 재시작, (c) 상한 없는 단일 실행 모델 비용 위험 수용.

---

## 14. v0.2.35 승인 원샷: 공개 게시·독립 리뷰·게이트·LIVE 판정 (2026-11-23 KST)

**요약:** (1) 승인된 ZIP 정확히 공개 게시 PASS. (2) 독립 리뷰 COMPLETED, BLOCKING 0. (3) 필수 게이트 중 **실제 GitHub 두 프로세스 동시 경합 NOT_RUN** → 지시서 규칙에 따라 **LIVE 전환 미실행**. 운영은 v0.2.29 그대로(LIVE=OFF 상태 유지, Task 두 개 Running). LIVE_READY=NO.

### 14.1 공개 게시 (PASS)
- 입력 ZIP `v0_2_35_intent_scope_candidate.zip`: SHA-256 `658a6f3da8bd018b96b64453892aec77d96868e19bc5788745c1591b1729a740`, 307,418 B, 114 항목 — 승인값과 일치 확인.
- 저장소 실제 visibility 재조회: PUBLIC. 동일 버전 기존 요청 없음.
- 공식 `collab/ops/submit_review_request.py`(깨끗한 main 클론 `49629ba`), 드라이런 PASS 후 `--publish`.
- 요청 `REQ-COWORK-V035-WATCHER-REVIEW-20261123` rev 1, `skill_collab_watcher`=`cowork-review-watcher`, `POLICY-STATIC-V1`, STATIC_ONLY, WINDOWS.
- Commit A `f8ad29b1037f07716b6ff0de2dd26c72170061e9`(REQUEST+ZIP), Commit B `b2f186fb7de55638983ad6a057f9204e0c4aed9c`(SOURCE_PIN, A 고정, repo_id 문자열 `"1451933830"`). 원격 ZIP 바이트 SHA 일치.

### 14.2 보호 승인·READY·디스패치·독립 리뷰 (PASS)
- 기존 감시기 자동 경로(기존 보호 위임 범위), 수동 서명 없음. APPROVAL_SIG 및 READY 원격 게시 확인.
- 감사: `REVIEW_DISPATCHED` 1회(2026-11-23 07:32 UTC), `REVIEW_COST` 기록, `COMPLETED`. jobs COMPLETED 1, 중복 0.
- 실제 비용 USD 0.8444 (상한 3.0 이내), 내부 턴 24 (디스패치 1회).
- `REVIEW_RESULT_1.md`: `execution_status: COMPLETED`, SHA-256 `67547d03fe189e72107b1fa04aa0570badd764bb8fbe28c22173b08f40c7bdbf`, 7,001 B. **BLOCKING: None.** 비차단 관찰 4건(F3 고정 설계 확인, F1 재검증 nonce 비소비 확인, 디스패치 1회 확인, F2 매니페스트 일부 확인).
- 영수증 `RECEIPT_1.md`: `ok: true`, watcher 0.2.29, 패키지 SHA 일치.
- 리뷰어 미검증 항목(매니페스트 113 해시, 런타임 GitHub API, 테스트 재실행)은 본 세션에서 대신 확인(§14.3).

### 14.3 필수 게이트 검증
| 게이트 | 결과 | 근거 |
|---|---|---|
| 리뷰 BLOCKING 0 | PASS | §14.2 |
| 매니페스트 113 해시 vs ZIP | PASS | 패키지 검사 불일치 0 |
| 실제 GitHub API: 경로별 커밋 조회 | PASS | `commits_touching(REQUEST.md)` → 커밋 A 정확 반환, 없는 의도 파일 → 0건 (GET 전용) |
| 실제 GitHub API: 조상 관계 | PASS | A가 main HEAD의 조상 `true`, 역방향 `false`, 동일 `true` (GET 전용) |
| 실제 GitHub 원자성(create-only) | PASS(단일 시도) | 기존 `DISPATCH_1.md`에 **동일 바이트** create-only 쓰기 → `UPLOAD_CONFLICT` 거부, 내용 불변 (sha `0ae6bc8d…` 전후 동일) |
| **실제 GitHub 두 프로세스 동시 경합** | **NOT_RUN — 필수 게이트 미충족** | 새 경로에 동시 생성은 운영 저장소에 산출물을 남기는 쓰기. 승인된 범위(ZIP 공개·리뷰·LIVE)에 없음 |
| Windows 호스트 SHADOW(사본) | PASS | 최신 상태 사본: 디스패치 0, 대기 9, 모델 0, 쓰기 차단 래퍼. 라이브 DB 읽기 전용 |
| 호스트 설치형 SHADOW | NOT_RUN | 설치·Task 변경 필요(LIVE 범위 전) |
| 구 코드 롤백 호환 | PASS | v0.2.29 코드가 `review_intent_nonces`가 있는 사본에서 정상 스캔(디스패치 0, 무결성 ok, 작업 14 유지) |
| 컷오버 직전 DB 백업 | PASS | `backup_live_db_20261123_precut`: 무결성 ok, 작업 14(진행 중 0), 클레임 7, 감사 최대 25310, 복구 사본 무결성 ok, 설정·위임 SHA 라이브와 일치 |
| 설치 트리 백업 대조 | PASS | 2026-11-22 `install_tree_v0_2_29`의 Python 파일 25개 = 라이브 25개(SHA 일치) |
| 설정·위임·키·Task·Notifier 불변 | PASS | 설정 `2ead4007…`, 위임 `6d826672…`, Task 정의 미변경(조회만), Notifier Running |
| provider 단일성·중복 방지 | PASS | lease `github` 1행, 진행 중 작업 0, 대기 클레임 0 |

### 14.4 LIVE 전환 — 미실행 (필수 게이트 미충족)
- 지시서 4번: "실제 GitHub 전송 경합/원자성 ... 실행 불가한 필수 검증은 NOT_RUN/BLOCKED로 두고 LIVE 강행 금지."
- 두 프로세스 동시 경합은 **NOT_RUN**. 따라서 설치(watcher 정지·설치 트리 교체·테이블 추가·재시작)를 **수행하지 않았습니다.**
- 현재 운영: **v0.2.29 Running** (작업 `SKILL-COLLAB-GitHub-Watcher`, `Running`), Notifier Running, 설치 트리·DB·설정·위임 변경 없음.
- 롤백 자산은 이미 준비됨(§14.3 백업·호환 PASS). 설치 자체는 실행 전.

### 14.5 운영 검증(§5 항목 6~7)
- LIVE 미전환이므로 v0.2.35 운영 검증·실모델 E2E·Task/Notifier 중복 검증은 **NOT_RUN**. 무권한 유료 요청 생성 금지 규칙에 따라 테스트용 요청도 만들지 않음.

### 14.6 필요한 사용자 조치 (최소 1건)
- 실제 GitHub 동시 경합 시험 경로 승인: 예) `collab/ops/race-tests/<run-id>/` 아래 synthetic 파일을 두 클라이언트가 같은 새 경로에 동시에 create-only로 쓰는 1회 시험(산출물 1개가 저장소에 남음, 이후 삭제는 별도 쓰기 필요). 또는 전용 격리 저장소 허용.
- 이 승인이 나면 경합 시험 → 통과 시 LIVE 설치(§13.7 범위) → 운영 검증 순서로 진행합니다.

- **LIVE_READY = NO. LIVE = OFF(변경 없음).**

---

## 15. v0.2.36 Runner 완료 감지 E2E 판정 (2026-11-23 KST)

**판정: v0.2.36 ZIP 미생성 (FORMAL_REQUEST=BLOCKED_SOURCE). 신규 독립 리뷰 미요청. 기존 완료 리뷰 재실행 없음.**

### 15.1 Runner 자동 감지 — 기존 실행 증거로 PASS
- 워크플로 `cowork-gpt-disposition.yml`은 `main`에 대한 `push` 중 `collab/reviews/**/REVIEW_RESULT_1.md`, `collab/receipts/**/RECEIPT_1.md` 경로 변경에 자동 실행.
- v0.2.35 결과·영수증 게시로 생성된 Run:
  - `45132178582` (push, head `45e20834c9`, 트리거 actor `wonhwipark`): offline-selftest **success**, gpt-disposition **skipped**, telegram-smoke **skipped**.
  - `45132184098` (push, head `98c6813705`): offline-selftest **success**, gpt-disposition **skipped**, telegram-smoke **skipped**.
- 해석: 결과 게시 → Runner 자동 시작은 **확인됨**. 두 skipped는 설계상 게이트 때문(GPT API 변수 `COWORK_GPT_API_ENABLED` 등 미설정, 원격 변수 목록에 `COWORK_TELEGRAM_SMOKE_ENABLED`만 존재).

### 15.2 v0.2.36 필요성 판단
- 지시서 2번: Runner 자동 시작을 위한 **실질적 최소 변경만** 반영. 위 증거상 워치독 코드·워크플로 변경은 **불필요**.
- 단순 버전 올림은 지시서가 금지한 무의미 변경. 실제 신규 소스가 없으므로 지시서 4번에 따라 `FORMAL_REQUEST=BLOCKED_SOURCE`로 종료하고 가짜 ZIP·SHA·REQUEST를 게시하지 않음.
- 같은 v0.2.35 ZIP으로 리뷰를 다시 여는 것은 완료된 리뷰 재실행에 해당하므로 하지 않음.

### 15.3 상태 구분
| 항목 | 상태 | 근거 |
|---|---|---|
| 결과 게시 → Runner 자동 시작 | PASS | Run 45132178582 / 45132184098 (push, actor wonhwipark) |
| offline 무모델 검증 | PASS | offline-selftest success (두 Run) |
| 모델 실행(신규 리뷰) | NOT_RUN | 신규 리뷰 없음 |
| GPT 판정(GitHub GPT API) | NOT_RUN | `COWORK_GPT_API_ENABLED` 미설정, 비용 정책 미승인 |
| Telegram(GitHub Actions 경로) | NOT_RUN | `COWORK_GPT_TELEGRAM_NOTIFY_ENABLED` 미설정 |
| v0.2.36 ZIP·독립 리뷰 | BLOCKED_SOURCE | 실질 변경 없음 |
| LIVE 설치 | NOT_RUN | 이번 범위 밖, 기존 게이트 미충족 유지 |

### 15.4 다음 한 가지 결정
- GPT 판정까지 실제로 검증하려면 `COWORK_GPT_API_ENABLED`·비용 정책 승인·지출 상한 확인이 필요합니다. 이는 별도 비용 승인 범위이므로 사용자 결정이 필요합니다.
- 실질 변경을 원하면 구체 요구(예: 워처가 결과를 올린 뒤 Runner 다시 트리거 등)를 주시면 그때 v0.2.36을 만듭니다.

- **LIVE_READY = NO. LIVE = OFF.**

---

## 16. v0.2.35 최초 GPT 판정 원샷 — 사전검증 FAIL로 중단 (2026-11-24 KST)

**판정: HOST_PREFLIGHT=FAIL, 안전 중단. GPT API·Telegram 스위치 미변경, workflow dispatch 0, 모델 호출 0, 원격 쓰기 0.**

- HOST_ACK: 실제 Windows Claude Code 세션에서 인계서 수신·실행(CONFIRMED_THIS_SESSION).
- 대상: `REQ-COWORK-V035-WATCHER-REVIEW-20261123`(완료된 기존 리뷰). 재리뷰 없음.
- 신뢰 루트: 로컬 `trust_root_file`이 설정의 고정 SHA와 일치, 키 `cowork-approver-1` ACTIVE, 로컬 공개키가 GitHub 변수 `COWORK_APPROVER_PUBLIC_KEY_B64`와 일치(키 값은 출력하지 않음).
- SECRETS_PRESENT: `OPENAI_API_KEY`, `COWORK_TELEGRAM_BOT_TOKEN`, `COWORK_TELEGRAM_CHAT_ID` 이름 존재 확인(값 미열람).
- MODEL_VARIABLE: `COWORK_GPT_MODEL` 미설정.
- 사전검증 1차 FAIL(`APPROVAL_FIELD_READY_SHA256`): 클론의 `core.autocrlf=true`가 READY.md를 CRLF로 변환한 것이 원인. 원격 blob `d30f6f24…`는 승인 필드와 일치. 클론 설정을 false로 바꾸고 요청 폴더를 저장소 바이트로 복원한 뒤 재검증.
- 사전검증 2차 PASS_RETURNED(모델 0)였으나 입력 기대값과 불일치: 기대 `5bd39fa0…`/42,915 B, 실제 `cda7110a…`/42,979 B(main `8a95f3f` 기준). 기준 Run `45215858291`은 커밋 `557297e`에서 측정되었고 이후 문서 커밋이 추가됨. 지시서 규칙에 따라 HOST_PREFLIGHT=FAIL.
- PREEXISTING_CLAIMS: 미확인(사전검증 FAIL로 claim 조회 전 중단, claim 생성 없음).
- API_SWITCH=UNCHANGED, TELEGRAM_SWITCH=UNCHANGED, RUN_ID=없음, GPT_DISPOSITION=NOT_RUN, USAGE=0, TELEGRAM_SENT=0, MOBILE_RECEIVE=NOT_VERIFIED.
- LIVE_WATCHER: v0.2.29 Running 유지. 설치·DB·Task·Notifier·키 변경 없음.
- NEXT_ONE_ACTION: 기준 커밋을 고정하거나 현재 main 기준 기대값을 재측정한 뒤 사전검증을 다시 수행. 먼저 추가된 문서 커밋이 입력에 들어가는지 확인.



---

## 17. v0.2.35 GPT 최초 판정 재개 — 게이트 버그로 호출 전 차단, 스위치 안전 복귀 (2026-11-24 KST)

- **HOST_ACK:** 실제 Windows Claude Code 세션(CONFIRMED_THIS_SESSION).
- **클론:** 새 클론 `publish_clone_lf`, `core.autocrlf=false`, 워킹트리 clean, HEAD `dd98fd7`. READY.md `d30f6f24…` 저장소 바이트와 일치.
- **사전검증 PASS(모델 0, 원격 쓰기 0):** 입력 SHA `5bd39fa0a8300d597c1f7a794286b21d92bb54423937135caa0cc8b850dde294`, 42,915 B — 기대값과 정확히 일치. work_id `COWORK-AUTO-APPROVAL-20261115-001`.
- **미실행 확인:** claim·결과 4개(`GPT_DISPOSITION.json`, `GPT_API_EXECUTION_CLAIM.json`, Work `ONE_CYCLE_CLAIM.json`, `GPT_TELEGRAM_NOTIFICATION_CLAIM.json`) 모두 404. 최근 `cowork-gpt-disposition` Run 전부 `gpt-disposition`·`telegram-smoke`가 skipped였음 → 과거 GPT 판정 실행 없음.
- **지출 상한 변수:** `COWORK_GPT_PROJECT_SPEND_CAP_CONFIRMED`는 설정하지 않음(워크플로에서 조건 제거 확인).
- **스위치 설정:** `COWORK_GPT_MODEL=gpt-6.2-sol`, `COWORK_GPT_TELEGRAM_NOTIFY_ENABLED=true`, `COWORK_GPT_API_ENABLED=true`(마지막). 각각 readback 확인.
- **1회 디스패치:** `workflow_dispatch` Run `45268991482`(request_id=REQ-COWORK-V035-WATCHER-REVIEW-20261123, telegram_smoke=false). 결과: `gpt-disposition` **failure**, `offline-selftest` success, `telegram-smoke` skipped.
- **실패 원인:** 로그 `BLOCKED: REPOSITORY_NOT_PUBLIC`. 저장소는 실제로 공개(`private=false`). 원인은 `collab/tools/gpt_disposition_actions.py`의 `github_json`이 URL을 `repos/<repo>/`(끝 슬래시)로 만들고, GitHub이 이 형식에 404를 반환해 `code == 200` 검사가 실패한 **게이트 코드 버그**. 저장소 조회에서 끝 슬래시 없이 `200`/`private=false` 확인.
- **모델·Telegram 상태:** claim이 생성되기 전 차단. 모델 호출 0, GPT 판정 0, Telegram 발송 0, `MOBILE_RECEIVE=NOT_VERIFIED`.
- **안전 복귀:** `COWORK_GPT_API_ENABLED=false`, `COWORK_GPT_TELEGRAM_NOTIFY_ENABLED=false`로 되돌리고 readback 확인(이렇게 두면 결과 push 시 자동 GPT 호출을 막음).
- **다음 필요 조치:** 게이트 버그 수정은 `collab/tools/gpt_disposition_actions.py` 변경과 `main` push가 필요합니다. 이 push는 워크플로 경로 필터에 걸려 Actions를 자동 실행하므로, 수정 범위 승인과 push 허용을 받은 뒤 진행합니다. 수정 후 기존 Run 재사용이 아니라 새 workflow_dispatch 1회로 재시도합니다.
- **LIVE:** 변경 없음. LIVE=OFF, LIVE_READY=NO.
