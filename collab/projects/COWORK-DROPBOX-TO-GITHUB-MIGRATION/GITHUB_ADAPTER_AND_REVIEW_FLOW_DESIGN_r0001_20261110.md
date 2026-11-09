# CoWork GitHub Transport Adapter — 기존 Dropbox 협업 계약 1:1 보존 설계 r0001

- 날짜: 2026-11-10 KST
- 상태: `DESIGN_CANDIDATE` / `NOT_ACTIVE`
- 대상: PRIVATE `wonhwipark/CoWork-Skill-Collab`
- 기존 운용 원본: Dropbox `/SKILL-COLLAB/`의 REQUEST/READY → watcher → Claude Code → REVIEW_RESULT/RECEIPT → GPT 판정
- 원칙: **협업 방식은 동일하고, 전달 계층(Dropbox → GitHub)만 교체**한다.
- 이 문서 및 PR은 정식 `REQUEST.md`/`READY.md`가 아니고 Claude 모델 실행 신호가 아니다.

## 1. 계약 비교 — 유지해야 하는 사용자 동작

| 단계 | 기존 Dropbox | 목표 GitHub | 책임 및 불변조건 |
|---|---|---|---|
| 1 후보 준비 | GPT 소스 수정·회귀시험·ZIP/SHA | GPT 동일, PRIVATE 후보 ZIP | GPT 정본 책임, 과거 ZIP 불변 보존 |
| 2 리뷰 요청 | `requests/<id>/REQUEST.md` + mode sidecar | `collab/requests/<id>/REQUEST.md` + `REVIEW_EXECUTION_MODE.json` | **기존 V1 YAML frontmatter 유지** |
| 3 실행 승인 | 검증된 `READY.md` 마지막 게시 | 검증된 `READY.md` 마지막 커밋 B에 게시 | READY 없으면 호출 0, 승인 서명 추가 |
| 4 요청 감지 | Dropbox watcher longpoll | Windows watcher GitHub API poll | 모델 실행 엔진 재사용, 활성 provider 단일 |
| 5 검증 | SHA, knowledge refs, policy, 중복키, mode | 동일 + Git commit A pin + 저장소 ID + 서명 검증 | 실패 시 `BLOCKED`/모델 0 |
| 6 리뷰 | Claude Code 독립 STATIC_ONLY | 같은 Claude Code runner | 비용 정책 유지, 재호출 금지 |
| 7 결과 기록 | `reviews/<id>/REVIEW_RESULT_<rev>.md`, `receipts/<id>/RECEIPT_<rev>.md` | PRIVATE `collab/reviews`, `collab/receipts` | 원격 읽기/해시 재검증 뒤 완료 판정 |
| 8 사용자 통지 | Telegram 완료 알림 | Telegram 동일 | 요청 ID/접근 가능한 링크·상태, 완료 1회 |
| 9 GPT 판정 | finding별 ACCEPT/ACCEPT_WITH_CHANGE/REJECT/DEFER/NEED_INFO | 동일 | 수정→재시험→신규 ZIP, 필요시 신규 정식 리뷰 |
| 10 공개 배포 | 별도 배포판정 | 승인 ZIP만 PUBLIC `L1Work` 기존 호환 경로 | reviewer에게 PUBLIC write 권한 없음 |

`SEMI_AUTO` 기본, `AUTO_PENDING_SETUP`은 아직 자동 GPT Work 연동 증거 없음. 기존 비용정책 STATIC $1, LARGE $3, XLARGE $6 유지.

## 2. 어댑터 최소 변경 경계

- 교체: `GitHubEventSource`(main 커밋의 신규 READY 탐색), `GitHubArtifactFetcher`(고정 commit SHA에서 bytes), `GitHubResultPublisher`(CAS·no-overwrite), `GitHubAuth`(최소권한)
- 추가: `ApprovalVerifier`(서명된 READY 승인), `SourcePinVerifier`(repo ID·commit·개별 SHA), `ProviderEpochGuard`(Dropbox↔GitHub 중복 실행 방지)
- 최대한 재사용: 기존 REQUEST V1 파서·정책/비용 검사·ZIP 검증·SQLite 처리키·Claude runner·Telegram notifier·영수증 schema
- 메서드 계약(설계): `list_new_ready(after_commit)`, `read_bytes_at_commit(path, sha)`, `validate_request(bundle)`, `claim_once(processing_key)`, `run_reviewer_once(validated_bundle)`, `publish_if_absent(path, bytes, expected_head)`, `verify_readback(path, expected_sha)`
- 실제 Windows watcher 소스·설치 버전 확인 전까지 모듈/함수명은 구현 확정값이 아닌 설계 인터페이스다.

## 3. 브랜치 보호 불가를 보완하는 승인 검증

1. `main`의 READY 생성 이벤트만 **발견 후보**로 취급하고 승인으로 신뢰하지 않는다. PR/issue/fork/ZIP 갱신은 실행 신호가 아니다.
2. Commit A에 immutable 후보 ZIP·REQUEST·sidecar·지식근거를 반영한 뒤, 각 raw bytes SHA-256·크기·ZIP CRC·schema를 원격에서 재검증한다.
3. `READY.md`의 기존 내용/키는 보존한다. GitHub 전용 `GITHUB_SOURCE_PIN.json` 및 `READY_APPROVAL.json`은 별도 sidecar로 관리한다(정확한 최종 파일 형식은 실 watcher 호환 검증으로 확정).
4. 승인 서명 대상(정규화된 canonical payload): `repo_id`, `request_id`, `request_revision`, `review_attempt`, `source_commit_A`, `request_sha256`, `package_path`, `package_sha256`, `package_size_bytes`, `knowledge_refs_hash`, `execution_mode`, `policy_ref/hash`, `expires_at`, `ready_payload_hash`. 예: Ed25519 detached signature.
5. 서명 개인키·토큰은 GitHub 밖 승인된 비밀저장소에서 관리하고, 감시기에는 **별도로 고정한 신뢰 공개키와 저장소 ID**를 배포한다. 단순 repo 파일 속 공개키 교체로 신뢰를 변경할 수 없게 한다. 키 관리·발급은 별도 사용자 승인 사항이다.
6. 승인 후 Commit B에서 READY + 필요한 서명 sidecar를 마지막에 원자적으로 게시한다. 감시기는 B가 main의 승인된 이력인지, A pin의 원본과 서명이 일치하는지, 만료·중복·비용·policy·mode가 모두 유효한지 확인한다.
7. 서명만으로 충분하지 않다. 처리키의 SQLite 원자 선점, 단일 LIVE provider, 운영상 권한 제한, 신뢰키 외부 고정도 **동시에** 요구한다. 서명 부재·키 회전 불일치·인증 오류는 fail-closed/모델 0.
8. Git commit SHA, blob SHA, ZIP raw SHA-256, Dropbox content_hash는 **서로 다른 검증값**이다.

## 4. watcher 운용 상태와 중복 방지

```text
Dropbox LIVE (기존 watcher)
          └── 기존 REQUEST/READY → 기존 Claude Runner → Dropbox RESULT/RECEIPT → Telegram
GitHub SHADOW_READ_ONLY (후보, 독립 격리)
          └── GitHub READY/bytes 읽기·검증만 수행 (Claude=0, write=0, 알림=0)

[명시적 cutover 승인 후에만]
GitHub LIVE (정확히 1개)
          └── 승인 READY → 동일 Claude Runner → GitHub RESULT/RECEIPT → Telegram → GPT 판정
Dropbox READ_ONLY_ARCHIVE
```

- 처리키: `request_id|revision|package_sha256|review_attempt`, provider 전환 이전 처리 이력 reconcile. 과거 리뷰 원장 복사로 새 리뷰가 시작되어서는 안 됨.
- 실행 직전 durable claim. `RUNNING` 중 중단·PC 재부팅은 `REVIEW_UNCERTAIN`으로 봉인하고 자동 모델 재호출 금지.
- 결과 게시 장애는 로컬 검증된 결과만 재게시; 모델 재실행 없음.
- 기존 Windows 예약 작업/실행 인스턴스는 설치·전환 승인 전 변경 금지. 단일-process lock + provider epoch/lease 필요.
- Branch 보호가 없는 동안 PR merge와 승인 서명은 서로 다른 통제. PR 승인 또는 GitHub write 자체를 리뷰 실행 허가로 사용하지 않는다.

## 5. REQUEST → 결과 → 판정의 정확한 상태 계약

```text
GPT PACKAGE_TESTED
  -> GPT REQUEST_PUBLISHED
  -> GPT READY_APPROVED + SOURCE_PINNED (commit A)
  -> GPT READY_PUBLISHED (commit B)
  -> watcher DISCOVERED/VALIDATED
  -> watcher RUNNING (1회)
  -> Claude Code STATIC_ONLY review
  -> watcher RESULT_PUBLISHED + RECEIPT_PUBLISHED
  -> watcher REMOTE_READBACK_VERIFIED
  -> watcher COMPLETED + Telegram 알림
  -> GPT finding-by-finding disposition
  -> 필요한 수정/재시험 -> 새 버전 후보
```

- 유효한 REQUEST/READY 외에는 모델 0. 같은 요청 중복 polling·재시작에도 0 추가 호출.
- `REVIEW_RESULT` 와 `RECEIPT`에서 request_id/revision/package_sha256/processing_key/status/비용의 정합성 확인.
- REVIEW_RESULT 문서만 존재하거나 RECEIPT 실패면 `PUBLISH_PENDING`; Telegram 완료 알림 금지.
- GPT 판정은 실제 Claude 리뷰와 별도 상태. `REVIEW_COMPLETED`가 `GPT_ACCEPTED`를 뜻하지 않음.
- 동일 건 재리뷰는 자동 재시도가 아니라 사용자가 명시한 새 REQUEST/revision/attempt로 진행.

## 6. 안전한 개발·독립 리뷰 부트스트랩

현재 GitHub watcher는 LIVE가 아니므로 **이 새 경로의 REQUEST/READY만으로 Claude가 리뷰했다고 표시하지 않는다.**

1. GPT가 설계·어댑터 후보를 PRIVATE 검토 브랜치/PR에 게시한다. **이 문서가 해당 단계이며 실제 실행 신호가 아니다.**
2. Claude Code는 인증된 개인 Windows PC에서 PR 자료를 읽고 독립 정적 설계 리뷰를 수행할 수 있다. 이 직접 대화형 정적 검토는 기존 watcher의 정식 REQUEST/READY 결과·영수증과 별도 상태로 남긴다.
3. 정식 Claude 리뷰 영수증이 필요하면 검증된 **기존 Dropbox REQUEST/READY watcher 경로**로 후보 ZIP을 요청해 리뷰한다. 신규 GitHub 경로의 E2E로 새 GitHub 경로를 자체 검증하는 순환 부트스트랩 금지.
4. GPT가 finding별 수용/수정/거절 판정→재시험→후보 ZIP 재발행.
5. 독립 리뷰/host 테스트/최소권한 인증 이후 GitHub `SHADOW_READ_ONLY` 동작. 이때도 Claude 호출 0.
6. 별도 LIVE 승인 후 **시험 request 1건**에 한해 GitHub 정식 REQUEST/READY → Claude 1회 → REVIEW_RESULT/RECEIPT → Telegram → GPT 판정 E2E.
7. 최종 cutover 이후에야 신규 요청의 GitHub 정본화. Dropbox 기존 기록·watcher는 안전 롤백까지 유지.

## 7. 필수 회귀시험 및 판정

- 기존 인계서 수락시험 T01~T38을 대상 목록으로 유지하되 실제 시험 상태는 별도 기록. 특히 T01/T02(무 READY), T04~T06(SHA/knowledge 불일치), T09(PR로 실행 금지), T10/T11(정상 1회/중복 0), T12/T13(중단·재게시), T19~T21(이중 프로세스/provider/기존 요청 재검출), T24(비용), T25(ZIP), T31/T37(PUBLIC 유출/권한).
- 서명 보강 시험 S01(서명 없음), S02(서명 위조), S03(다른 repo ID), S04(만료), S05(다른 source commit A), S06(다른 request bytes), S07(다른 ZIP bytes), S08(키 회전), S09(같은 승인 replay), S10(READY·승인 sidecar 분리 관찰): 모두 의도치 않은 Claude 호출 0.
- 이전 GPT 보고의 **보안 게이트 오프라인 합성 시험 41 PASS**는 보고된 범위로만 인용한다. 이 GitHub 문서 게시가 원본 후보 ZIP 바이트, Windows 통합 회귀, 기존 YAML V1 호환, 실제 GitHub API·Claude 리뷰 E2E의 PASS를 의미하지는 않는다.

## 8. 현 단계 증거와 금지 범위

- 확인된 사실: PRIVATE repo 생성·GPT 접근, main 기본 계약 문서, Windows 점검 요약 `HOST_AUDIT_STATUS: PARTIAL` (사용자 제공), 별도 GPT 보안 게이트 후보 개발/오프라인 시험 보고.
- 미검증: 현재 Windows watcher 정확한 설치 버전, 후보 ZIP raw byte readback, 기존 V1 실제 파서 연동, fine-grained 토큰/서명 키 운영, Claude 독립 검토, 실제 GitHub 처리·결과 게시, 기존 watcher 변경.
- 금지: 인증정보/GitHub 토큰·서명 개인키·회사 반출 금지 데이터 업로드, PUBLIC `L1Work`에 협업 파일 게시, Dropbox watcher 중지/재시작, 신규 watcher LIVE 활성화, 유효하지 않은 REQUEST/READY 게시, 임의 Claude 호출, 근거 없는 REVIEW_COMPLETED 표시.

## 9. 다음 한 동작

Windows Claude Code에서 이 PRIVATE 검토 브랜치와 `CLAUDE_STATIC_REVIEW_HANDOFF_r0001_20261110.md`를 읽고 설계·기존 watcher 경계에 대해 정적 리뷰 및 차단 사항을 보고한다. 초기에는 READ_ONLY로 확인하고, 어댑터 구현 및 별도 테스트/서명키 생성/LIVE/공식 게시에는 각 게이트를 적용한다.

참조: `collab/ops/CONTRACTS/REVIEW_TRANSPORT_V1.md`, `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md`, `COWORK_DROPBOX_TO_GITHUB_MIGRATION_HANDOFF_r0002_20261110.md`.
