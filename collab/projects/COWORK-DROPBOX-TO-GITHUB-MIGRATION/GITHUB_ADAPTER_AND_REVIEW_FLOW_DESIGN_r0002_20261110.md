# CoWork GitHub adapter 설계 r0002 — Claude Code 원문 반영
2026-11-10 KST | DESIGN_REVISED / IMPLEMENTATION_NOT_RUN / PR_FREE
근거: 동일 프로젝트 CLAUDE_STATIC_REVIEW_RESULT_FOR_GPT_20261110.md (Windows Claude Code가 watcher v0.1.5 일부 소스 및 합성시험 검토), 이전 설계 r0001, main의 NO_PR_COLLABORATION_V1.

## 1. 최종 운영 흐름
사용자 → GPT 요구사항/코드 수정/회귀시험/후보 ZIP → GitHub PRIVATE에 ZIP·기존 V1 REQUEST·REVIEW_EXECUTION_MODE.json·knowledge refs 게시(commit A) → 원격 raw SHA-256/size 및 pin 검증 → 서명된 READY를 마지막 게시(commit B) → Windows Python watcher 승인·중복·정책·비용 확인 → Claude Code 독립 리뷰 1회 → GitHub PRIVATE REVIEW_RESULT/RECEIPT readback → Telegram 완료 통지 → GPT 지적별 판정·수정·재시험 → 별도 승인된 최종 ZIP만 PUBLIC L1Work 기존 경로.
일반 협업에서 PR 생성/병합은 하지 않는다. 기존 Dropbox LIVE watcher는 GitHub 파일럿 검증까지 그대로 유지한다. 기본 SEMI_AUTO, AUTO_PENDING_SETUP 미검증 유지.

## 2. Claude Code BLOCKING 7건 판정과 수정 계약
### B-2 — 파일명 충돌: ACCEPT_WITH_CHANGE
실제 group_request_entries는 파일명에 READY 또는 REQUEST 부분 문자열이 있으면 해당 역할 후보로 분류함. READY.md + READY_APPROVAL.json은 두 READY 후보가 되어 영구 pending(합성 실측 runner=0).
**수정:** 신규 승인 sidecar 명은 APPROVAL_SIG.json, source pin은 SOURCE_PIN.json으로 고정; 둘 다 READY/REQUEST 부분 문자열 금지. 기존 REVIEW_EXECUTION_MODE.json 그대로. 장기적으로 정확한 basename(READY.md/REQUEST.md) 분류로 변경 시 기존 Dropbox 회귀시험 필수. 아직 코드 미변경.

### B-5 — 실제 처리키 불일치/정책 재실행: ACCEPT_WITH_CHANGE
실제 키는 request_id|revision|package_sha256|local_policy_revision(설정 schema_version), review_attempt가 아님. schema_version 변경만으로 동일 요청이 신규 키가 되어 재리뷰될 위험 있음.
**수정:** 기존 key 형식과 local_policy_revision 의미는 유지하면서 별도 불변 logical_request_id = request_id|revision|package_sha256의 완료/진행 이력을 정책개정·provider 이관과 무관하게 조회한다. 새 요청/개정에 대한 승인 없이 policy revision만 바뀐 중복은 모델 0. 서명 payload에 local_policy_revision 및 policy hash를 포함, review_attempt를 처리키로 오인하지 않음. 역사적 완료 처리키 reconcile 전 schema_version 변경 금지. 명시적 재리뷰는 새 승인된 request/revision으로만.

### B-3 — 프로세스 사망시 봉인 실패: ACCEPT_WITH_CHANGE
실제 watcher는 timeout에서만 REVIEW_UNCERTAIN을 만들고, 모델 호출 중 watcher 사망은 REVIEW_RUNNING을 영구 잔존시켜 재호출은 막지만 알림도 없음.
**수정:** 재시작 시 실행 프로세스가 더 이상 살아있지 않은 CLAIMED/REVIEW_RUNNING job을 SQLite 원자 트랜잭션으로 REVIEW_UNCERTAIN 봉인. 영속 이벤트 키로 불확실 알림 1회, 완료 통지는 0. 관리자 복구 전 재실행 없음. 기존 recover --requeue 같은 명령으로 임의 재호출되지 않도록 별도 운영 승인·근거 게이트 필요. 실제 코드 미변경.

### B-4 — provider/epoch 부재: ARCHITECTURE_DECISION
현재 jobs DB에 provider/epoch 열 없음. **선택: 단일 공유 SQLite DB**에 provider, epoch, logical_request_id, active_provider 및 전환 기록을 추가하되 운영 DB 백업과 스키마 이행 시험 후 적용. 단일 OS 실행 잠금 + provider lease/epoch를 함께 적용하고 Dropbox/GitHub 이중 LIVE 방지. GitHub SHADOW에서는 jobs/원격/Claude/Telegram 쓰기 0. 두 watcher 동시기동 실측은 아직 NOT_RUN.

### B-6 — CRLF/BOM 및 SHA: ACCEPT_WITH_CHANGE
현 validator는 text decode→UTF-8 재encode로 REQUEST hash 계산. Git checkout의 autocrlf가 원본 바이트를 바꿀 수 있음. **어댑터는 clone/checkout이 아니라 고정 Git commit/blob API 바이트를 사용**, raw byte SHA와 크기를 검증한다. LF/CRLF 원본을 무단 정규화하지 않는다. BOM 등 미지원 형식은 사전 차단. 해시 검증기 자체를 바꿀 경우 Dropbox 원본 요청 회귀 필요.

### B-1 — 서명 라이브러리 미설치: REQUIRED_APPROVAL
Windows watcher venv에서 cryptography/nacl 미설치 관찰. Ed25519 detached signature 검증은 운영 라이브러리 추가 승인·버전/해시 고정 후 구현. 승인 전 실제 S01~S10 PASS를 주장하지 않음. 라이브러리 없음/서명 검증 실패 시 fail-closed, 모델 0. HMAC으로 자의적 대체하지 않음.

### B-7 — 신뢰키/폐기/시계: REQUIRED_APPROVAL
신뢰 루트(approved repo ID, 공개키 fingerprint)는 GitHub 밖 Windows 승인 보호 위치에 고정하고 저장소의 문서 변경으로 교체 불가. key ID/회전·폐기·재발급 정책, clock skew와 신뢰 가능한 시계 실패 처리를 정의한다. 개인 서명키나 토큰은 GitHub·프롬프트·로그에 저장하지 않는다. 신뢰키 발급과 최소권한 토큰 생성은 별도 사용자 승인 후.

## 3. 재사용/변경 경계 (Claude 원문 실측 근거)
REUSE: transport_base.Transport 7개 추상 메서드, lock.SingleInstanceLock 기본, models 상태, 기존 비용·정책 검증 흐름, SQLite idempotency 기초.
WRAP: validator의 Dropbox 경로 가정/해시, orchestrator의 부분문자열 파일분류·재시작 봉인, state_store(provider/epoch), cli의 DropboxTransport 하드코딩, watch_loop의 GitHub ETag poll, notify_reviews의 provider별 링크·알림.
REPLACE: 전송 계층 dropbox_transport → 신규 github_transport, 기존 dropbox_transport는 삭제하지 않음.
NEW: ApprovalVerifier(Ed25519), SourcePinVerifier(repo ID/commit/raw SHA), ProviderEpochGuard.
review_runner, zip_safety, dropbox_transport, watch_loop 일부는 Claude가 정독하지 않아 REUSE 가정의 추가 확인이 필요하다.
사용자 PC에 설치된 실제 Windows watcher와 SQLite/예약 작업은 변경하지 않는다.

## 4. PR 없는 GitHub 승인/실행 게이트
1) Commit A에 후보 ZIP·기존 YAML REQUEST/모드/지식 refs를 게시하고 실제 바이트 SHA-256·크기·CRC·정책 스냅샷, A full commit을 검증한다.
2) Commit B에서 새 APPROVAL_SIG.json, SOURCE_PIN.json, READY.md를 함께 마지막 게시한다. self-reference commit hash 순환을 만들지 않는다.
3) 승인 서명의 canonical payload에는 repo ID, request ID/revision, source commit A, request SHA, package SHA/size/path, knowledge refs, execution mode, local_policy_revision, policy hash, 만료/nonce, READY payload hash, signature schema version을 고정한다.
4) watcher는 main의 신규 READY만 후보로 발견하고, GitHub 외부 고정 trust root로 signature와 모든 pin을 확인한 뒤 단일 LIVE provider·logical duplicate·비용·정책·승인 유효성·SQLite durable claim을 만족하는 경우에만 Claude 1회 호출.
5) 통신 실패, 결과 게시 실패·409/422/429는 기존 결과의 원격 확인/재게시만 시도. 모델 재호출 0. 원격 RESULT와 RECEIPT readback 일치 후만 COMPLETED/Telegram 완료 1회.
6) GitHub fork/PR/Issue/문서만으로 reviewer 기동 0. GitHub write 접근자에게 자동 리뷰 실행 권한이 생기지 않는다. PUBLIC에 리뷰 문서 전송 금지.

## 5. 적용 순서와 현재 상태
현재 단계: r0002 설계·시험표 준비, GPT가 Claude 원문 7건을 설계 차원에서 수용. Windows 어댑터 구현/변경/통합 시험 NOT_RUN, 서명키/토큰/라이브러리 준비 NOT_RUN, GitHub 정식 독립 리뷰 NOT_RUN, SHADOW/LIVE/CUTOVER NOT_RUN.
다음: Windows Claude Code가 PRIVATE main의 r0002와 ACCEPTANCE_TEST_MATRIX_r0001_20261110.md를 읽고 **격리 작업 복사본**에서 최소 변경 구현·오프라인 회귀시험을 설계/진행. 운영 watcher 변경, 신규 토큰/키/암호 라이브러리 설치, READY 게시, LIVE 운영 전환은 별도 승인.
회사 반출 금지 자료·토큰·개인키 PRIVATE GitHub 업로드 금지. /AI-CONTINUITY/ 수정 금지.
