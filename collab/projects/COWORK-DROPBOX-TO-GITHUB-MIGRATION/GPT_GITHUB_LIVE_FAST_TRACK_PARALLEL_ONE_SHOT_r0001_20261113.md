# GitHub LIVE 준비 가속화 — Windows Claude Code 병렬 게이트 원샷 인계
- Date: 2026-11-13 KST | Revision: r0001
- Repository: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`
- Branch: `main`
- Exact handoff path: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_GITHUB_LIVE_FAST_TRACK_PARALLEL_ONE_SHOT_r0001_20261113.md`
- Work ID: `COWORK-DROPBOX-TO-GITHUB-MIGRATION`
- Run mode: **ONE_SHOT / PARALLEL_PREPARATION / NO_AUTOMATIC_MONITORING**
- Status when posted: **PREPARED_NOT_EXECUTED**; `ACTIVE_PROVIDER=NONE`; `MIGRATION_NOT_CUTOVER`

## 0. 목표·실제 최신 상태
사용자는 **GitHub LIVE까지 빠른 진행**을 원한다. 이 지시는 **기존 승인 범위에서 가능한 코드 분석·격리 시험·보안 사전검증·인계/판정 문서화의 동시 수행**을 허용한다. 운영 키 생성/설치, 사내 소스 PRIVATE 업로드, 유료 독립 reviewer 호출, Windows 운영 watcher 설치/DB 이행, 정식 LIVE 전환은 **승인하지 않는다**.

실행 전 최신 `collab/START_HERE.md`와 이 작업 `CURRENT.md`의 최신 절, 다음 원문 및 이전 시도/증거를 우선 읽어 중복을 줄여라.
- `CLAUDE_DROPBOX_WATCHER_SAFE_DISABLE_RESULT_FOR_GPT_20261112.md`, `GPT_DROPBOX_WATCHER_DISABLE_DISPOSITION_r0001_20261113.md`
- `WINDOWS_POST_DROPBOX_DISABLE_DEPENDENCY_AUDIT_ONE_SHOT_r0001_20261113.md` 및 이미 결과가 있으면 해당 최신 보고
- `CLAUDE_ETW_ATTRIBUTION_AND_C_FINAL_CHECK_RESULT_FOR_GPT_20261112.md`, `GPT_ETW_RESULT_AND_DROPBOX_LIVE_REEVALUATION_r0001_20261112.md`
- `CLAUDE_STAGE1_APPROVED_HOST_SECURITY_RESULT_FOR_GPT_20261111.md`, `WINDOWS_C_SHADOW_TO_E_INDEPENDENT_REVIEW_ONE_SHOT_r0001_20261112.md`
- `GPT_B7_TRUST_ROOT_AND_APPROVAL_POLICY_DRAFT_r0001_20261110.md`, `GITHUB_ADAPTER_AND_REVIEW_FLOW_DESIGN_r0002_20261110.md`, `ACCEPTANCE_TEST_MATRIX_r0001_20261110.md`, `collab/ops/CONTRACTS/REVIEW_TRANSPORT_V1.md`

기준 사실:
1. **Dropbox reviewer watcher는 사용자 승인으로 Disabled + Stop**. 진행/불확실 0, 중지 후 복사본 DB integrity PASS, 운영 원본·영수증 보존. 작업 정의 실복원 SKIP. 알림기/updater/Bridge는 아직 켜져 있을 수 있음.
2. **자동 리뷰 공급자 없음**: `ACTIVE_PROVIDER=NONE`. GitHub의 문서/SHADOW 조회는 LIVE 아님.
3. 후보 `skill-collab-watcher_v0_2_10`은 Windows LOCAL ONLY, 이전 보고 크기 174,745B, SHA-256 `67ea7fc63ccc1de77a28025b7c4f1b701ee6f4fa387311bca3f3d2bc7432b108`; GPT는 이 ZIP 원본 바이트를 보지 못함. 70항목 중 기존 v0.1.5 유래 **UNCHANGED 34개**의 반출 허가 미확인. 임의 게시 금지.
4. 실제 GitHub GET-only 시험 3주기/GET7회 PASS(과거 보고); C 운영 파일 무접근 ETW는 **측정기 해석 실패 / C=PARTIAL**, 파일이 변경됐다고 단정하지 않음. 운영 signer/approved trust root BLOCKED; E 독립 리뷰 NOT_RUN/모델 0.

## 1. 병렬 작업 묶음 — 승인 범위 내에서 끝까지, 중간 핑퐁 최소화
서로 독립된 A~D를 **가능하면 병렬로** 준비하라. 공유 운영 DB/로그 원본에 대한 동시 접근, 인증·키 충돌, 유료 reviewer 중복 실행은 금지. 실제 OS 프로세스를 건드리지 않는 격리 개발/정적 검사 위주로 진행하고 각 track은 실제 완료/보류를 별도 기록.

### Lane A — 남은 Dropbox 서비스 의존성 READ-ONLY (운영 정리)
- 기존 `WINDOWS_POST_DROPBOX_DISABLE_DEPENDENCY_AUDIT_ONE_SHOT_r0001_20261113.md`를 재사용하되 이미 수행됐다면 최신 결과를 가져오고 **재실행하지 말 것**.
- Dashboard updater / Telegram notifier / Bridge 각각 실제 Task Scheduler/PID/설정의 source-sink 및 공유 기능, 재시작 경로, dashboard GitHub Actions/Pages 분리 여부 조사. 운영 DB main/WAL/SHM에 직접 SQLite 읽기 연결을 열지 않는다.
- 각각 `KEEP / RETIRE_CANDIDATE / UNKNOWN`으로 분류, 무엇을 Disable할지 **추천만**. 실제 Stop/Disable/데이터 삭제/알림 발송 금지.
- 현재 watcher Disabled 유지 읽기 전용 확인. `ACTIVE_PROVIDER=NONE`; 새 유효 READY가 자동 처리되지 않음.

### Lane B — C 기술 게이트 '최소 증거' 개선 (격리 코드·비관리자, 운영 무변경)
- 현재 상태 `C=PARTIAL` 유지. 이전 ETW 31개 합성시험 PASS, 실제 `tracerpt` CSV의 `Clock-Time`과 Kernel-Process payload 해석 실패. **반복 관리자 셸 실행/새 추적 수집 금지**.
- 우선 로컬 보존 ETL/CSV의 스키마 해독을 실제 공급자 metadata 및 원본 이벤트 XML/필드 의미로 확인; `Clock-Time`을 FILETIME으로 단정/임의 offset fitting/프로세스 PID를 유추해 거짓 PASS 만들지 말 것. 필요하면 raw ETL을 읽기만 하는 **격리 복사본**에서 `Get-WinEvent` 등 지원 여부를 검토(관리자 권한을 요구하면 실행 중단·BLOCKED).
- GPT의 `tools/etw_attribution_preflight_r0001.py`에서 **process lifetime 밖의 보호 파일 이벤트가 조용히 누락되는 문제**를 fail-closed 오류/카운터로 개선하고 unit regression 추가; Windows 8.3/UNC/junction/hardlink alias 및 file identity 문제는 host-only 보완 증거가 없으면 `NOT_PROVEN`으로 유지. 기존 진단 원본을 덮어쓰지 않고 새 버전을 별도 로컬/허용된 비민감 도구 경로로 게시.
- **C 대체 수용 가능성 판단만**: Dropbox provider가 이제 Disabled/archived이고 `ACTIVE_PROVIDER=NONE`이므로, 신규 GitHub SHADOW가 운영 archive DB와 완전히 격리된 경로/OS ACL/handles/코드 실행 경로라는 추가 근거와 이전 실패 ETW 증거를 대비. 기존 Gate의 ETW 요구를 임의 삭제하지 말고, 승인된 **독립 대체 증거 계약안**을 별도 제안(`C_ALT_EVIDENCE=PROPOSED_NOT_APPROVED`). 새로운 운영 DB opener·운영 watcher 재가동 금지.
- 과거 A 비관리자 ACL PASS, C GET-only PASS는 증거로 재사용하되 실제 완성형 host I/O proof PASS로 소급하지 않는다.

### Lane C — B signer, D source export, review 비용/권한 사전준비
- **B 운영 서명자 준비**: 기존 test key와 운영 key 구분, 승인자 별도 장치/책임자, Ed25519 key lifecycle, repo numeric ID/pin/fingerprint, trust-root ACL, 키 교체/폐기/시간·replay, 관리자 권한 게이트의 **실행 가능한 체크리스트·문서·합성시험**만 만든다. 운영 key 발급/개인키 조회/배포/운영 trust-root 변경은 전부 `BLOCKED_APPROVAL`.
- **D 후보 ZIP 반출 전 분류**: 로컬 ZIP 70항목의 provenance `NEW 24 / CHANGED 12 / UNCHANGED 34`와 소유권·반출 제한 여부를 **파일 종류·카운트·해시·변경 구분만** 기록. 허가서 없는 34개를 `approved`라고 간주하지 말고 `BLOCKED_EXPORT_CLASSIFICATION`. 회사 자료/원문/파일 절대 경로/비밀/원본 ZIP은 **PRIVATE에도 올리지 않는다**. 변경분만으로 리뷰가 충분한지 별도 설계 대안은 가능하나 이를 전체 ZIP 정식 독립 리뷰로 거짓 표시 금지.
- **E 리뷰 실행 게이트 준비**: 실제 host/developer와 분리된 독립 reviewer 세션 및 경로, 정식 `REQUEST/APPROVAL_SIG/SOURCE_PIN/READY last` 계약, nonce/expiry/서명·예산/1회·repo pin/영수증 readback, 기존 Dropbox logical request 중복 확인을 정적·synthetic dry-run으로 점검. 현재 GitHub review transport `DRAFT/NOT_ACTIVE`. **서명된 READY 생성·게시 금지, 유료 리뷰어/모델 호출 0, 비용 $0**. 정식 E는 별도 승인과 실제 독립 실행/영수증이 필요.
- 어떤 품질 수치도 이미 검증되지 않은 실호스트/운영 key/반출 허가 상태로 승격하지 않는다.

### Lane D — LIVE 가동 전 마지막 게이트 설계·리허설
- 설계와 **격리 스냅샷/합성 시험**으로만 준비: 단일 활성 provider, Dropbox 아카이브의 기존 완료·CONFLICT 및 historical request와 GitHub logical request 중복 0, `REVIEW_UNCERTAIN` 재호출 0, Telegram watermark 중복/누락 방지, 예약 작업 복구/신규 GitHub watcher 설치 시 rollback, 운영 signer 부재 fail-closed, Windows 자동시작 권한 정책, DB main/WAL/SHM 보호.
- GitHub 서비스가 아직 LIVE가 아니므로 준비 상태 `LIVE_INSTALL=NOT_RUN`, `LIVE_CUTOVER=NOT_RUN` 유지. Windows 운영 작업, 운영 DB, notifier 설정, Dropbox 백업 또는 설치본 **변경 금지**. 사용자 최종 승인 전 provider를 NONE→GITHUB로 바꾸지 않는다.
- 운영자에게 필요한 **최소 승인 묶음**을 단일 표로 준비: 승인 주체, 필요한 입력/작업, 위험과 예상 비용, 승인 전 수행 가능한 범위, 명시 승인 문구, 허가 없을 때 차단 항목. 관련된 승인 요건을 숨기거나 '빠르게 진행'으로 일괄 승인 처리하지 않는다.

## 2. 실행/결함 수정/시험 규칙
- 최신 결과 확인 후 **가능한 코드는 격리 복사본에서 직접 보완·시험 반복**, 이미 검증된 단계를 불필요하게 재실행하지 않음. 원본 후보/운영 설치본 무변경. 실제 PASS/FAIL/SKIP/NOT_RUN 로그를 재현 가능한 명령·환경·대상 해시와 함께 요약.
- user-intervention은 **관리자 실행·별도 승인자 기기·반출 정책·실모델 비용/LIVE cutover** 등 필수 조치에 한정. 준비/정적 시험은 중간 확인 없이 계속.
- 다른 작업과 공유하는 notifier/Bridge/Dashboard updater의 운영 상태 변경 금지. 추가 watcher/cron/자동 모니터링/Telegram 알림 생성 금지.
- 실제 사용 불가한 Windows host/키/서명자/권한이 있으면 해당 Lane만 `BLOCKED/NOT_RUN`으로 격리하고 나머지 계속.
- 재시험/개발자 자체 시험은 독립 리뷰로 취급하지 않음. `INDEPENDENT_REVIEW=NOT_RUN` 유지.
- 읽기 전용을 주장한 DB 접근도 WAL/SHM에 부작용이 있을 수 있으므로 기존 운영 DB를 직접 SQLite 연결로 열지 않음.

## 3. 신규 결과 및 정본 갱신
결과 MD (새 파일, 이전 보고 덮어쓰기 금지):
`collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CLAUDE_GITHUB_LIVE_FAST_TRACK_READINESS_RESULT_FOR_GPT_20261113.md`

필수 보고 순서: **현재 상태 → A/B/C/D lane 변경·검증 → 실제 시험 → 미검증/권한 및 승인 필요 → 산출물 SHA·위치 → 다음 한 동작**.
상세 필드:
- `ACTIVE_PROVIDER`, `DROPBOX_WATCHER_DISABLED`, `RESIDUAL_SERVICE_AUDIT`, `C_EXISTING_REAL_GET`, `C_ETW_PROOF`, `C_ALT_EVIDENCE`, `B_SIGNER_ROOT`, `D_EXPORT_CLASSIFICATION`, `E_REVIEW_TRANSPORT`, `E_INDEPENDENT_REVIEW`, `HOST_INSTALLED`, `MODEL_CALLS_NEW`, `USD_SPEND`, `GITHUB_LIVE`, `ROLLBACK_READY`
- track별 실제 `HOST_REAL/SYNTHETIC/STATIC/SELF_TEST_REPORTED/NOT_RUN`, 설명·근거; 수집 안 한 결과를 추정으로 채우지 말 것.
- **승인 게이트 집중표**: B 별도 운영 서명자/신뢰루트 설치, D 사외 반출 분류/허가, E 독립 runner 및 최대 금액/유료 호출, C 운영격리 실제 증명 또는 승인된 대체 계약, 최종 설치/DB migration/LIVE 명시 승인. 사용자 개입은 최종 통합 결과에서 한 번에 제시.
- PRIVATE main PR 없이 결과 MD + `CURRENT.md` 최신 절 + `TRACKER.json` 유효 enum만 갱신. RAW 코드/회사 소스/ZIP/키·토큰·DB·원본 ETW/식별자는 PRIVATE에도 게시 금지. 텍스트 산출물의 UTF-8 실제 바이트 및 Git blob/commit **remote readback** 검증. 실패 시 `NOT_POSTED/UNVERIFIED`; 게시 실패 때문에 유료 reviewer 재호출 금지.
- 다른 병렬 프로젝트 CURRENT/TRACKER는 불필요하게 수정하지 않음.

## 4. 승인 및 완료 정의
**이 원샷의 완료는 허용된 병렬 준비와 현장 자체시험·문서 게시까지**. 자동 리뷰 LIVE 가동 완료가 아님. `READY`, `REQUEST`의 신규 실행 승인, 별도 운영 개인키 생성, 반출, 유료 reviewer, GitHub LIVE 전환의 '암묵적 승인'은 없다.
운영 상태는 기존 `ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER` 유지.

## 5. Windows Claude Code에 전달할 실행 한 줄
`GitHub PRIVATE wonhwipark/CoWork-Skill-Collab main의 collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_GITHUB_LIVE_FAST_TRACK_PARALLEL_ONE_SHOT_r0001_20261113.md 를 읽고 Lane A~D에서 권한 내 실행 가능한 개발·격리시험·사전검증을 원샷 병렬로 수행하고, 차단 항목은 BLOCKED로 남겨라. 운영 설정/DB/키·토큰/Dropbox 기존 아카이브/READY/유료 reviewer/LIVE 전환은 건드리지 말고, 통합 결과 MD + CURRENT.md + TRACKER.json을 PRIVATE main에 직접 게시·remote readback해라.`
