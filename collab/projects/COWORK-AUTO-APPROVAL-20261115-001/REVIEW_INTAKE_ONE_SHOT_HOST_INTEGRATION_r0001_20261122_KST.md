# CoWork 단축 리뷰 요청 → Windows 정식 제출 연결 r0001

- 작성: 2026-11-22 KST
- 기존 Work: `COWORK-AUTO-APPROVAL-20261115-001`
- 참조 Work: `COWORK-SKILL-DISCOVERY-20261112-001` (P1/P2 실제 입력 후보)
- 정본: GitHub PUBLIC `wonhwipark/CoWork-Skill-Collab`, branch `main`
- **상태:** `STAGED_INPUT_ADAPTER=CODE_PUBLISHED_TESTED`, `WINDOWS_RELAY_HOOK=NOT_INSTALLED`, `FORMAL_REQUEST=NOT_POSTED`, `MODEL_CALLS=0`

## 1. 사용자 목표·확인된 연결 공백

- 동일 설계 대화창에서 사용자 **“리뷰요청해줘”** → 해당 Work 최신 설계·소스·시험을 선택 → **정식 Windows Claude Code 리뷰 요청**. 긴 프롬프트와 Windows 수동 명령을 반복 요구하지 않는 것이 최종 목표.
- 현재 GPT가 정상적으로 GitHub에 후보 ZIP(Base64)·REQUEST 초안·인계를 게시할 수 있으나, 기존 Windows v0.2.29 LIVE watcher는 유효한 REQUEST/서명/READY 기반 처리기다. **후보에서 실제 Windows 정책 사전검사 → Git Commit A/B 요청 게시**를 자동 실행하도록 연결된 host-side 접수 단계는 확인되지 않았다.
- 등록된 자동 위임 허용 목록 외 `skill_id`는 기존 정책상 공식 수동 signer 검증이 필요하다. 새 연결이 생겨도 **GitHub 게시/ChatGPT 지시/문서의 승인 주장으로 보호 서명을 대신할 수 없다**.

## 2. 구현: 기존 제출기 재사용, 기본 읽기 전용

- [새 보조 진입 코드](../../ops/review_staged_submission.py): 실제 Windows checkout의 **클린 main·원격 HEAD 일치**를 기존 `submit_review_request.require_clean_main`으로 확인 → 기존 Work 하위 **커밋된 REQUEST 초안·Base64 ZIP**만 Git object에서 읽음 → 일반 파일 모드·크기·path 탈출·YAML Work·ZIP 경로/크기/SHA-256 확인 → 격리 임시 폴더로 바이트 복원 → 기존 `submit_review_request.submit` 재사용.
- `--publish`가 없으면 **기본 dry-run**. `--publish`가 있어도 기존 LIVE `review_request_gate.check_request`와 제출기 게이트가 성공할 때만 Commit A(REQUEST+ZIP), Commit B(SOURCE_PIN), 원격 readback을 수행. **서명/READY/모델 호출·알림·호스트 설정 변경 없음.**
- [시험 원문](../../ops/tests/test_review_staged_submission.py): 임시 실제 Git repository를 사용한 11건 격리 단위시험 PASS. `submit`과 보호 signer/네트워크는 mock. 테스트한 로컬 코드 파일과 GitHub main 원격 **Git blob SHA 완전 일치**.
- 코드 SHA-256: `review_staged_submission.py` = `5d4dfffe0f1fd92d543a7a352d60d3d5aed5196d6e7f2e5b2183d9605276b518`, Git blob = `d33b3b5a4669cfb1e25a9c78d0b92209b0ffdbe7`.
- 테스트 SHA-256: `test_review_staged_submission.py` = `3fb6a9dd0937a3b14ccc08b537b4784179bfff944a1ca7c5c234ba16b1c2c1e2`, Git blob = `ebe467de726048f223c94a92336ae4f4d7ed1c60`.
- **제약:** 이 코드는 기존 제출기로 연결하는 로컬 진입점이며 Windows에 자동 설치·호출된 watcher hook이 아니다. 호스트 환경에서 실제 CLI 및 다른 기존 회귀 전체 실행은 `NOT_RUN`. P1/P2 94,843B ZIP의 Windows 새 독립 재검증도 `NOT_RUN`.

## 3. 기존 P1/P2의 정확한 입력과 검증 경로

입력은 다음 기존 **동일 Work**에 이미 고정되어 있으며 새 ZIP이나 REVIEW ID를 만들지 않는다.

- Work: `COWORK-SKILL-DISCOVERY-20261112-001`
- Request 후보: `REQ-COWORK-P1P2-CONTEXT-CODE-R1-20261122` (새 재큐잉 금지)
- Draft: `collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/P1_P2_FORMAL_REVIEW_REQUEST_UNPOSTED_DRAFT_r0001_20261122_KST.md`
- Candidate: `collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/P1_P2_REVIEW_CANDIDATE_r0001_1122.zip.base64`
- ZIP 고정 94,843 bytes, SHA-256 `35de54934944807518e0141daaedde1888a42c08c1d264584e9b341f65dcd5f3`
- Skill ID `cowork-context-design` **변경 금지**. 과거 위임 허용 목록 밖 → 공식 signer의 실제 AUTO 갱신 여부 또는 유효한 수동 승인 확인.

Windows의 **승인된 기존 세션**에서 다음 명령은 첫 단계 `--publish` 없는 사전검사다. `<ACTUAL_WINDOWS_LIVE_CONFIG_PATH>`는 운영 PC에서 실제 경로 확인 후 대체하며 토큰·설정 본문 공유 금지.

```powershell
python collab/ops/review_staged_submission.py --repo-root . --work-id COWORK-SKILL-DISCOVERY-20261112-001 --draft-path collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/P1_P2_FORMAL_REVIEW_REQUEST_UNPOSTED_DRAFT_r0001_20261122_KST.md --candidate-path collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/P1_P2_REVIEW_CANDIDATE_r0001_1122.zip.base64 --live-config "<ACTUAL_WINDOWS_LIVE_CONFIG_PATH>" --approval-route manual
```

`PREPUBLICATION_PASS_NOT_SUBMITTED` 이후에도 **Windows official signer의 정책/대상/권한·과거 기록**을 확인해야 한다. 기존 유효 승인과 권한이 확인될 때만 동일 명령에 `--publish`를 추가하고, `SUBMITTED_AWAITING_PROTECTED_SIGNER` 이후 승인·서명·READY 마지막 게시·리뷰 1회를 기존 계약대로 별도 처리한다.

## 4. 진짜 원샷을 위한 Windows 기존 watcher 연결 (아직 미적용)

- 권장: **기존 watcher/정기 run_cycle에 후보 접수 단계 1개를 안전하게 연결**. 별도 상주 watcher, 새로운 예약 작업, 유료 GPT/Claude 자동 승인 엔진을 만들지 않는다. v0.2.29 실제 설치본과 운용 중인 `orchestrator`·`watch_loop` 인터페이스를 Windows에서 실측한 뒤 기존 Task의 승인된 업데이트 절차로만 연결한다.
- 입력 발견은 **사용자가 리뷰 요청한 동일 Work의 고정 후보**에 한정. SOURCE_PIN 없는 초안/ZIP 및 일반 `CURRENT.md` 변화 자체는 watcher **리뷰 실행 트리거가 아니다**. 별도 사용자 리뷰 요청의 출처·단일 Work·commit pin을 확인한 후 사전검사만 연결한다.
- 이미 있는 REQUEST/PIN, APPROVAL_SIG/READY, REVIEW/RECEIPT, 감사 DB/UNCERTAIN이 발견되면 **중복 제출·재서명·재큐잉 없이 기존 건 정산**. 멀티창 HEAD 충돌/미확인/승인 범위 밖은 fail-closed, 오류 후 무조건 재시도 없음.
- Windows 기존 설치 파일·Task·DB/WAL/SHM·보호 signer/키/위임·Notifier 및 유료 운영 설정 수정은 **현재 이번 코드 게시에서 하지 않았음**. 호스트 hook 설치·재시작·롤백은 해당 유효 운영 승인/백업/실측이 확인될 때만 진행.
- **남은 직접 검증:** Windows에서 `--publish` 없는 정확한 P1/P2 사전검사와 11건 회귀 소스를 실제 실행 → 보호 수동 signer 권한 여부·비용·중복 확인 → 기존 run_cycle에 안전한 후크 위치와 비승인 우회 여부 독립 검토 → 허용 범위의 설치·SHADOW→실제로 새 user-intent 1건 E2E. 그 전에는 `AUTO_FORMAL_REVIEW_INTAKE=NOT_APPLIED`.

## 5. 상태 및 다음 한 행동

- `CODE_PUBLISHED=PASS`, `GIT_BLOB_REMOTE_READBACK=PASS`, `ISOLATED_LOCAL_TEST=10_PASS`
- `REAL_SUBMITTER_INTEGRATION_TEST=NOT_RUN`, `WINDOWS_HOST_PREFLIGHT=NOT_RUN`, `WATCHER_INTAKE_HOOK=NOT_APPLIED`
- `P1P2_REQUEST=NOT_POSTED`, `APPROVAL_SIG/READY=NOT_POSTED`, `INDEPENDENT_REVIEW=NOT_RUN`, `PAID_MODEL_CALLS=0`.
- **NEXT_ONE_ACTION:** Windows Claude Code가 기존 호스트의 실제 권한·설정·watcher hook 가능성을 무과금 G0 점검하고 위 코드 `--publish` 없는 dry-run과 11개 회귀 시험을 1회 수행. 통합 설치가 승인 범위 밖이면 필요한 운영 변경 승인만 요청하고 기존 Work에 BLOCKED/NOT_RUN 게시. 기존 P1/P2 유료 리뷰는 보호 승인 확인 전 절대 실행하지 않음.
