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
