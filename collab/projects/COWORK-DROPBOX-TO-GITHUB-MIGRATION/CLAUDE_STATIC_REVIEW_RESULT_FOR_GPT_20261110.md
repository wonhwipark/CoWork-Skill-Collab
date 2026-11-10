# GitHub adapter 설계 독립 정적 리뷰 결과 (Windows Claude Code, 2026-11-10)

- 대상: PR #1 `[DRAFT] Dropbox 동일 REQUEST/READY 리뷰 계약 — GitHub adapter 설계 검토` (`wonhwipark/CoWork-Skill-Collab`, 브랜치 `review/github-adapter-design-20261110`).
- **검토 고정 커밋:** `1a251966e1ed10e9a7ff9a541050dded0812b874` (base `main` `17c587366f`). 이후 브랜치가 움직여도 이 커밋의 바이트를 검토했다.
  - 인계서 `CLAUDE_STATIC_REVIEW_HANDOFF_r0001_20261110.md` sha256 `72787b1c…cf2d` (4,763 B)
  - 설계 `GITHUB_ADAPTER_AND_REVIEW_FLOW_DESIGN_r0001_20261110.md` sha256 `c7d27bf5…a7a3` (11,356 B)
- 성격: **대화형 정적 설계 검토**다. 감시기를 통한 정식 비용·영수증 있는 독립 리뷰가 아니다(그쪽은 `NOT_RUN` 유지). 판정은 GPT가 한다.
- 실측 대상: 이 PC에 설치된 감시기 v0.1.5 소스. **정독:** `validator`, `state_store`, `models`, `lock`, `config`, `transport_base`, `orchestrator`(전반부 110줄과 265~624줄; 111~264줄의 컨텍스트·프롬프트 구성부는 건너뜀). **부분 읽음:** `cli.py`(90~220줄과 검색 결과), `watch_loop.py`(함수 목록과 일부 검색). **키워드 검색만:** `dropbox_transport`, `review_runner`. **읽지 않음:** `zip_safety`. 소스·설정·인증 값은 이 문서에 넣지 않았다.
- 보강 방법: 위 모듈을 **격리된 임시 폴더에서 합성 입력으로 실제 실행**해 가설을 재현했다(가짜 전송·가짜 실행기·임시 DB, 네트워크 0, 모델 호출 0, 운영 DB·설정·작업 무변경). 실행한 시험은 §7에 적었다.

## 0. 판정
**ACCEPT_WITH_CHANGE** — 방향(전송 계층만 교체, 실행·검증·비용·중복 방지 엔진 재사용, 서명과 신뢰 키 외부 고정)은 타당하다. 다만 **설계가 현재 코드에서 그대로 동작하지 않는 지점이 확인됐고**, 보안 핵심 통제(서명 검증)를 구현할 도구가 호스트에 없다. 아래 BLOCKING 7건을 해소하기 전에는 SHADOW도 시작하지 않는 것을 권한다.

## 1. 협업 semantics 보존 여부 (인계서 질문 1)
Dropbox와 GitHub 설계의 10단계 표는 단계, 책임, 불변조건이 서로 맞는다. 누락으로 본 것:
1. **`REVIEW_UNCERTAIN` 봉인 주장이 코드와 다르다**(B-3). 설계 §4는 중단 시 `REVIEW_UNCERTAIN`으로 봉인한다고 쓰지만 실제는 `REVIEW_RUNNING`이 영구히 남는다.
2. 설계의 `review_attempt`가 처리키에 대응하지 않는다(B-5).
3. Telegram은 "완료 1회"만 보존 항목으로 적었는데 실제 알림기는 DB 이벤트 기반이라 provider를 구분하지 못한다(R-2).
4. GPT finding별 판정, SEMI_AUTO, 모바일 재개 UX는 전송 계층과 무관해 영향이 없다.

## 2. BLOCKING (무제한 보고)

### B-1. 서명 검증에 필요한 암호 라이브러리가 호스트에 없다
- 근거: `requirements.txt`는 `dropbox`, `PyYAML`, `pytest`뿐이고, 감시기 venv에서 `cryptography`와 `nacl`은 모두 미설치다(`find_spec`으로 확인, 설치는 하지 않았다). 설계 §3의 Ed25519 detached signature 검증은 표준 라이브러리만으로 구현할 수 없다(표준 `hashlib`/`hmac`에는 비대칭 서명이 없다).
- 영향: 설계 보안 모델의 핵심(위조 READY 차단)을 현재 환경에서 시험·구현할 수 없다. 의존성 추가는 운영 venv 변경이라 별도 승인과 독립 점검이 필요하다.
- 최소 수정: (a) 의존성 추가를 사용자 승인 항목으로 분리하고 고정 버전·해시로 설치, 또는 (b) 대칭 키 HMAC로 대체하는 안은 키 유출 시 위조 가능하므로 권하지 않는다(신뢰 루트를 감시기 PC에 둬야 해서 서명자와 검증자의 분리가 사라진다).
- 필수 시험: S01~S10을 실제 라이브러리로 재현, 라이브러리 부재 시 fail-closed(모델 0).

### B-2. 설계의 `READY_APPROVAL.json`이 현재 요청 그룹화 코드에서 요청을 영구히 대기시킨다
- 근거: `orchestrator.group_request_entries`는 파일명에 `READY`가 들어가면 READY 후보로, `REQUEST`가 들어가면 REQUEST 후보로 분류한다. `READY.md`와 `READY_APPROVAL.json`이 한 요청 폴더에 있으면 READY 후보가 둘이 되고, 코드는 "추측하지 않는다"며 **그 역할을 비운다**.
- **재현:** 합성 요청에 `READY_APPROVAL.json`을 추가한 경우 `dispatched=0 pending=1 runner_calls=0 job_state=None`(요청이 영원히 대기). 사이드카가 없는 경우와 `REVIEW_EXECUTION_MODE.json`만 있는 경우는 정상 `COMPLETED`(모델 1회). 즉 `READY_APPROVAL.json`이라는 **이름 하나**가 원인이다.
- 영향: 안전하게 실패하지만(모델 0) 설계가 지정한 이름대로는 동작하지 않는다. 승인 사이드카를 `READY` 문자열이 없는 이름(예: `APPROVAL_SIG.json`)으로 바꾸거나, 사이드카를 `requests/<id>/` 밖에 두거나, 그룹화 규칙을 명시적 파일명(`READY.md`/`REQUEST.md`)으로 고쳐야 한다.
- 최소 수정: 설계에서 사이드카 이름을 `REQUEST`/`READY` 부분 문자열이 없는 이름으로 확정하고 그 제약을 계약 문서(REVIEW_TRANSPORT_V1)에 명시한다. 어댑터가 이름 규칙을 바꿀 경우 기존 Dropbox 쪽 동작 회귀를 시험한다.
- 필수 시험: 사이드카 이름 조합 매트릭스(위 재현을 시험으로 승격).

### B-3. 중단 시 `REVIEW_UNCERTAIN` 봉인이라는 설계 주장이 실제와 다르다
- 근거: 코드의 `REVIEW_UNCERTAIN`은 **실행기가 타임아웃을 보고했을 때만** 설정된다. 감시 프로세스 자체가 모델 호출 중 죽으면 작업은 `REVIEW_RUNNING`에 남는다.
- **재현:** 가짜 실행기에서 호출 중 중단(KeyboardInterrupt) 후 재시작: `runner_calls=0`(재호출 없음, 안전), 작업 상태 `REVIEW_RUNNING` 유지, `pending=0`.
- 영향: 재호출은 막히지만 작업이 `REVIEW_RUNNING`으로 영구히 남고 `pending`에서도 빠져 **아무도 모르게 정체**된다. 알림기는 `REVIEW_UNCERTAIN` 이벤트만 알리므로 알림도 없다. 복구는 사람이 `recover --requeue`로 해야 하고, 이 명령은 모델을 다시 부를 수 있다.
- 최소 수정: 시작 시 `CLAIMED`/`REVIEW_RUNNING` 잔존 작업을 `REVIEW_UNCERTAIN`으로 봉인하고 알림을 낸다(어댑터 범위 밖의 기존 감시기 보완). 설계 §4의 문구는 "현재 구현은 REVIEW_RUNNING 잔존, 봉인은 신규 보완 항목"으로 정정한다.
- 필수 시험: T12/T13 대응으로 "호출 중 사망 후 재시작: 모델 0, 상태 봉인, 알림 1회".

### B-4. provider 구분이 없는 단일 SQLite로는 Dropbox↔GitHub 이중 실행을 막을 수 없다
- 근거: `jobs` 테이블 열은 `processing_key, request_id, request_revision, package_sha256, state, created_at, updated_at, attempt_count, last_error, result_path`뿐이며 provider나 epoch 열이 없다. 처리키는 `request_id|revision|package_sha256|local_policy_revision`이다.
- **재현(실행으로 확인한 부분):** 한 DB에 이미 `COMPLETED`인 키를 다시 `create_job`하면 `INSERT OR IGNORE`라 상태가 `COMPLETED`로 남는다. 그리고 `jobs`에 provider를 구분하는 열이 없음을 `PRAGMA table_info`로 확인했다.
- **추론(실행으로 확인하지 않음):** DB를 provider별로 분리하면 같은 처리키가 서로 보이지 않으므로 같은 요청을 두 번 리뷰할 수 있다고 판단한다. 두 감시기를 실제로 동시에 띄워 확인한 것은 아니다. 공유 DB로 가면 키 충돌 동작은 안전할 것으로 보이나, 그 경우에도 provider 소유권과 전환 시점은 기록되지 않는다.
- 영향: 설계 §4의 `ProviderEpochGuard`가 무엇을 기준으로 하는지 정의돼 있지 않다.
- 최소 수정: (a) 하나의 상태 DB를 공유하고 `jobs`에 `provider` 열과 전환 epoch를 추가하거나, (b) provider별 DB를 쓰되 단일 LIVE를 OS 수준 잠금(`SingleInstanceLock` 확장)으로 강제한다. 어느 쪽이든 "SHADOW 상태에서는 `jobs`에 쓰지 않는다"를 시험으로 고정한다. 현재 `SingleInstanceLock`은 `watch` 프로세스 하나만 막고 provider 전환을 모른다.
- 필수 시험: T19~T21 대응 + "두 provider 동시 기동 시 하나만 LIVE".

### B-5. 설계의 처리키(`review_attempt`)가 실제 처리키와 다르고, 정책 개정이 바뀌면 같은 요청이 재실행된다
- 근거: 실제 처리키 마지막 요소는 `review_attempt`가 아니라 `local_policy_revision`(= 설정의 `schema_version`)이다. `attempt_count`는 별도 열로 처리키에 들어가지 않는다.
- **재현:** 같은 요청·같은 ZIP이라도 정책 개정만 1→2로 바꾸면 처리키가 달라진다(`…|1` → `…|2`).
- 영향: 설계 §3의 서명 대상에 `review_attempt`가 있고 §4가 "승인된 처리키"를 언급하는데 실제 코드와 필드 의미가 달라, 서명 대상과 중복 방지 키가 어긋난다. 더 중요하게는 `schema_version`을 올리면(예: GitHub 전환 때 설정을 바꾸면) **이미 끝난 모든 요청이 새 키로 다시 리뷰 가능**해진다. 전환 작업 중 설정을 손대는 순간 모델 비용이 발생할 수 있다.
- 최소 수정: 서명 payload에 `local_policy_revision`을 명시하고 `review_attempt`를 삭제하거나 정의를 분리한다. 전환 전에 "`schema_version` 변경 금지 또는 기존 처리 이력과의 reconcile"을 체크리스트로 둔다.
- 필수 시험: T22 계열 "정책 개정 변경 시 기존 완료 요청 재실행 0"(현재 코드는 이 시험을 통과하지 못한다).

### B-6. 요청 본문의 줄바꿈·BOM이 GitHub 체크아웃에서 해시를 깨뜨린다
- 근거: 검증기는 REQUEST를 **문자열로 디코드한 뒤 `encode("utf-8")`로 다시 인코딩해** SHA-256을 계산하고 READY의 `request_sha256`과 비교한다. 원본 바이트를 쓰지 않는다. 디코드는 BOM을 제거하지 않는다(`utf-8`).
- **재현:** LF로 고정된 READY와 CRLF로 읽은 REQUEST는 `CONFLICT`. BOM이 붙은 REQUEST는 front matter 시작 검사에서 `CONFLICT`.
- 영향: GitHub API의 `contents`는 저장 바이트를 그대로 주지만 Windows `git clone`은 `core.autocrlf` 설정에 따라 CRLF로 바꿀 수 있다. 어댑터가 clone을 쓰면 전송 도중 해시가 바뀌어 요청이 영구 `CONFLICT`가 된다(모델 0, 안전). 반대로 설계 §3의 "raw bytes SHA-256"은 이 코드의 계산 방식과 다르다.
- 최소 수정: 어댑터는 clone/checkout 없이 `contents`/`git blob` API로 바이트를 받는다. 또는 검증기가 원본 바이트로 해시하도록 바꾸되 이는 Dropbox 쪽 회귀 영향이 있는 변경이므로 기존 요청 전체의 해시 일치 시험이 필요하다. `.gitattributes`로 `*.md -text`를 강제하는 보조 통제도 둔다.
- 필수 시험: LF/CRLF/BOM 매트릭스(위 재현을 시험으로 승격), 기존 Dropbox 요청 샘플 해시 회귀.

### B-7. 신뢰 루트(고정 공개키·저장소 ID)의 배포·갱신 경로와 키 유출 대응이 설계에 없다
- 근거: 설계 §3-5는 "감시기에 별도로 고정한 신뢰 공개키와 저장소 ID를 배포한다"고만 적었다. 현재 감시기에는 이를 둘 설정 항목이 없고(`config` 키는 `schema_version … review_policy`뿐), `ReviewPolicy`/`LocalPolicy`에도 해당 필드가 없다. 키 회전(S08)과 폐기(revocation) 절차, 서명 만료 시계(PC 시계 신뢰)가 정의돼 있지 않다.
- 영향: 서명이 있어도 신뢰 루트를 바꿀 수 있는 사람이 누구인지 정하지 않으면 보안이 설정 파일 접근 통제로 환원된다(이 PC의 설정은 사용자 계정 쓰기 가능). 만료(`expires_at`)는 PC 시계에 의존하므로 시계 조작으로 우회 가능하다.
- 최소 수정: 신뢰 키의 보관 위치(설정이 아닌 별도 읽기 전용 위치와 해시 고정), 폐기 목록, 시계 허용 오차를 설계에 명시한다. 키 생성·발급은 별도 사용자 승인으로 분리(설계에도 있음) 하되 그 승인 전까지 어댑터의 서명 경로는 NOT_RUN임을 계약에 적는다.
- 필수 시험: S02, S08, 만료 경계, 키 폐기 후 기존 승인 거부.

## 3. 비차단 제안 (5건)
- **N-1. 호출 한도·변경 감지:** GitHub 변경 감지는 ETag/`If-None-Match` 조건부 요청이 실제로 동작한다(합성 시험 아님, 호스트에서 실측: 304 응답). 그러나 `contents` API 목록은 디렉터리 단위라 `requests/` 아래 폴더가 늘면 비용이 커진다. 변경 확인은 `commits/main`의 ETag로 먼저 걸러 목록 호출을 줄이는 구조를 권한다.
- **N-2. Telegram 알림 문구·대상:** 알림기는 감시기 DB를 읽기만 하므로 provider 개념이 없다. 문구의 "Dropbox reviews/…"는 코드에 박혀 있어 GitHub LIVE 후에는 틀린 안내가 된다. 코드 변경이 아니라 문구 템플릿을 provider별로 분기하는 정도이며, 알림이 두 DB를 보면 이중 알림이 날 수 있으므로 한 DB만 보게 한다.
- **N-3. 결과 게시 경합(CAS):** 설계는 `publish_if_absent(path, bytes, expected_head)`를 말한다. GitHub `contents` PUT은 파일이 있으면 `sha` 없이는 실패하므로 `mode=add` 의미는 구현 가능하다. 같은 브랜치에 GPT와 감시기가 동시에 커밋하면 충돌이 나므로 감시기용 결과는 별도 브랜치 또는 별도 경로에 쓰는 편이 안전하다.
- **N-4. 큰 ZIP:** `contents` API는 1MB까지 인라인이며 그 이상은 blob API가 필요하다(문서 한도, 이번에 대형 파일로 시험하지 않았다). 현재 후보 ZIP 크기 분포(최대 수백 KB, 100KB대 다수)에서는 문제없을 가능성이 높으나 확인이 필요하다.
- **N-5. 시험 수의 정의:** 인계서의 T01~T38과 S01~S10은 이 PC에서 본 적이 없다(PR 두 문서에는 번호만 있고 본문이 없다). 시험 목록 원문이 어디에 있는지(`COWORK_DROPBOX_TO_GITHUB_MIGRATION_HANDOFF_r0002_20261110.md`로 보이나 이 PR에는 없다) 확인이 필요하다.

## 4. 보안·중복 실행 위험 요약
| 위험 | 현재 코드가 막는가 | 판정 |
|---|---|---|
| READY 없는 모델 호출 | 막음. 검증기가 READY를 요구, 합성 시험에서 `runner_calls=0` | 안전 |
| 같은 처리키 재호출(재시작) | 막음. `CLAIMED` 이후 상태가 영속, 합성 시험 재호출 0 | 안전 |
| 모델 호출 중 PC 중단 | 재호출은 막음, 그러나 `REVIEW_RUNNING` 정체·무알림 | B-3 |
| 정책 개정 변경 시 재실행 | **막지 못함**(처리키에 포함) | B-5 |
| Dropbox와 GitHub 동시 리뷰 | **막지 못함**(provider 개념 없음, 단일 프로세스 잠금만) | B-4 |
| 위조 READY | 현재는 Dropbox ACL에 의존. 서명 검증은 미구현이고 라이브러리 없음 | B-1, B-7 |
| 결과 중복 게시 | 막음. 존재하면 업로드 생략(`get_metadata` 후 `add`) | 안전 |
| 게시 실패 후 모델 재호출 | 막음. `_retry_publish_only`는 실행기 인자가 없음 | 안전 |
| 자격증명 노출 | `dropbox_transport.py`와 `review_runner.py`를 키워드(`token`, `secret`, `app_key`, `refresh_token`)로 검색했고, 값이 생성자와 인증 호출에만 쓰이며 `log_event`나 출력으로 가는 경로는 찾지 못했다. 두 파일을 정독한 것은 아니다. 이 문서와 이번 점검 어디에도 값은 넣지 않았다 | 키워드 검색 범위 |
| PUBLIC 유출 | 이 PC의 `gh` 로그인은 PUBLIC `L1Work`와 소유 저장소 21개에 push 가능(§사전점검). 감시기용 최소 권한 토큰이 아직 없다 | 별도 승인 필요 |

## 5. 재사용 매트릭스 (실측 모듈 기준)
| 모듈(파일) | 판정 | 근거 |
|---|---|---|
| `validator.py` (`validate`, `parse_front_matter`) | **WRAP** | 로직은 재사용. 경로 접두어 `/SKILL-COLLAB/…` 가정(`_safe_remote_path`)과 대소문자 무시 비교는 Dropbox 규칙이라 GitHub 경로 모델에 맞게 설정값으로 분리해야 한다. 해시 계산 방식(재인코딩)은 B-6 |
| `models.py` | REUSE | 상태 열거는 provider 무관. 단 `REVIEW_UNCERTAIN` 설정 시점은 B-3 |
| `state_store.py` | **WRAP** | 스키마 재사용. `provider`/epoch 열 추가 필요(B-4). `cursors` 테이블은 GitHub용 이름만 추가하면 됨 |
| `lock.py` (`SingleInstanceLock`) | REUSE | 프로세스 잠금은 그대로. provider 전환 잠금은 별도 |
| `orchestrator.py` (`process_request_group`, `_publish_result`, `_retry_publish_only`, `run_scan_cycle`) | **WRAP** | 흐름·순서(READY 후 검증, 지식 해시는 CLAIM 전, 게시만 재시도)는 안전해 재사용. `group_request_entries`는 Dropbox 폴더 모델과 부분 문자열 규칙이라 B-2. 커서 수집 `_collect_delta`는 Transport에 맞춘 어댑터가 필요 |
| `transport_base.py` (`Transport` 추상 클래스) | **REUSE(핵심)** | 7개 메서드의 얇은 경계. `EntryMeta.content_hash`·`file_id`는 Dropbox 개념이라 GitHub blob/commit SHA를 어떻게 채울지 정의 필요 |
| `dropbox_transport.py` | **REPLACE** | `github_transport.py`로 대체. Dropbox 쪽은 그대로 보존 |
| `cli.py` | **REPLACE(일부)** | `DropboxTransport`를 직접 import·반환형으로 고정(`Runtime.transport: DropboxTransport`, `_build_transport`). provider 선택 지점으로 바꿔야 한다 |
| `watch_loop.py` | **WRAP** | `longpoll`을 콜백으로 받으므로 GitHub는 ETag 폴링 콜백을 넘기면 된다 |
| `review_runner.py` | **REUSE(미정독, 추정)** | 어댑터는 이 모듈을 호출만 하고 전송과 무관하다는 점은 `orchestrator`의 호출부(`runner.run(snapshot_dir, prompt, …)`)에서 확인했다. 내부 구현은 읽지 않았으니 UNKNOWN에 가깝다 |
| `config.py` | **WRAP** | `transport` 값이 이미 있으나 `cli.py`가 읽지 않는다. 신뢰 키 위치·repo ID 항목 추가 |
| `zip_safety.py` | **UNKNOWN(미독)** | `orchestrator`가 `safe_extract`로 호출하는 것만 확인했다. 전송과 무관할 것으로 보이나 읽지 않았으므로 판정을 보류한다 |
| 알림기 `notify_reviews.py` | **WRAP** | 이벤트 기반이라 재사용 가능. provider 구분과 문구 분기 필요(N-2) |
| 서명 검증(`ApprovalVerifier`)·`SourcePinVerifier`·`ProviderEpochGuard` | **신규** | 현재 코드에 대응물이 없다. B-1, B-4, B-7 |

## 6. 기존 계약과의 차이 (정확한 대응)
| 항목 | 설계 가정 | 실제 코드 |
|---|---|---|
| 처리키 | `request_id|revision|package_sha256|review_attempt` | `request_id|revision|package_sha256|local_policy_revision`(B-5) |
| 중단 시 상태 | `REVIEW_UNCERTAIN` 봉인 | 타임아웃일 때만. 프로세스 사망은 `REVIEW_RUNNING` 잔존(B-3) |
| READY 사이드카 | `READY_APPROVAL.json` 병존 | 이름의 `READY` 부분 문자열 때문에 요청 영구 대기(B-2) |
| 요청 해시 | raw bytes | 디코드 후 UTF-8 재인코딩 바이트(B-6) |
| 확장 필드 | `source_commit_A`, 서명 참조를 READY/REQUEST에 병기 가능 | 기존 파서가 **알 수 없는 필드를 무시**하고 통과시킴(재현 P3). 하위 호환은 되지만 서명 검증을 우회하려면 파서가 모르는 필드로는 막을 수 없다 |
| provider | 단일 LIVE + epoch | provider 개념 없음(B-4) |

## 7. 이번 검토에서 실제로 한 것 (시험 매트릭스 일부)
- **PASS(합성·격리 실행, 모델 0):** P1 정책 개정이 처리키를 바꿈(**결함 재현**), P2 LF/CRLF·BOM 해시 불일치(**결함 재현**), P3 확장 필드 무시 통과(하위 호환 확인), P4 사이드카 이름의 그룹화 영향(**결함 재현**), P5 공유 DB 키 충돌 시 기존 상태 유지(안전 확인), Q1 정상 흐름(모델 1회·게시 2건), Q2 `READY_APPROVAL.json` 영구 대기(**결함 재현**), Q3 `REVIEW_EXECUTION_MODE.json`은 영향 없음, Q4 호출 중 중단 후 재시작 재호출 0(안전 확인)과 `REVIEW_RUNNING` 정체(**결함 재현**).
- **호스트 실측(읽기 전용):** PRIVATE 저장소 읽기, `gh` 인증, ETag 조건부 요청 304, 호출 한도(5,000/h), 브랜치 보호·ruleset 사용 불가(HTTP 403, 무료 플랜), 암호 라이브러리 미설치.
- **T01~T38, S01~S10 번호별 상태:** 목록 원문을 읽지 못해 **번호별 PASS/FAIL을 부여하지 않았다.** 위 합성 시험이 T01/T02(무 READY 호출 0), T10/T11(정상 1회/중복 0), T12/T13(중단·재게시)의 **일부**에 대응하지만 번호 매핑은 GPT가 원문과 대조해야 한다. S01~S10(서명)은 라이브러리가 없어 전부 **NOT_RUN**이다.
- **NOT_RUN:** GitHub 쓰기·결과 게시·큰 파일, 실제 GitHub 전송 구현, 두 감시기의 동시 기동, 키 회전·폐기, 대형 저장소 성능, 정식 감시기 경유 독립 리뷰.

## 8. 필요한 회귀시험 (추가분)
1. 사이드카 이름 매트릭스(`READY_APPROVAL.json` 포함)가 요청을 막지 않을 것.
2. LF/CRLF/BOM에서 `request_sha256`이 안정적일 것(어댑터는 바이트 보존).
3. 정책 개정 변경 후 기존 `COMPLETED` 요청이 재실행되지 않을 것.
4. 호출 중 프로세스 사망 후 재시작: 모델 0, 작업이 `REVIEW_UNCERTAIN`으로 봉인, 알림 1회.
5. provider별 SHADOW가 `jobs`를 쓰지 않을 것, 두 provider 동시 LIVE 거부.
6. 서명 부재·위조·타 저장소·만료·타 커밋·타 바이트·키 회전·재사용: 전부 모델 0.
7. 기존 Dropbox 요청 샘플에 대한 기존 시험 17개 파일 전체 재통과(변경 후에도).
8. 결과 게시 중 GitHub 쓰기 충돌(409/422)에서 모델 재호출 0.

## 9. 다음 한 동작 (정확히 하나)
**최소 수정 설계 반영:** 위 BLOCKING 7건을 설계 r0002에 반영하되, 먼저 B-2(사이드카 이름), B-5(처리키·정책 개정), B-3(`REVIEW_UNCERTAIN` 봉인 보완)처럼 **기존 감시기 소스에 대한 사실 정정**부터 한다. 암호 라이브러리 설치와 신뢰 키 발급, 최소 권한 토큰 생성은 사용자 승인 후 별도로 진행한다.

## 10. 미검증과 한계
- 감시기의 `review_runner`·`dropbox_transport`·`zip_safety`·`watch_loop` 세부는 정독하지 않았다.
- 인계서 T/S 목록 원문과 이전 GPT의 "보안 게이트 오프라인 41 PASS" 후보 ZIP은 이 PC에서 본 적이 없다(재현·검증 불가).
- 합성 시험은 실제 GitHub·실제 Claude를 쓰지 않았다.
- Windows 읽기만으로 Linux나 다른 호스트 동작은 검증하지 못했다.
- 이 문서는 GitHub에 게시하지 않았다.
