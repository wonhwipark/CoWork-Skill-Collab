# v0.2.29 실제 ZIP 5개 창 복구 검증 — GPT 사전 결과 및 Windows 원샷 수행서 r0001

- 일자: 2026-11-20 KST
- 정본: PRIVATE `wonhwipark/CoWork-Skill-Collab`, `main`
- 기존 Work: `collab/projects/COWORK-AUTO-APPROVAL-20261115-001`
- 사용자 지시: 기존 5개 창(설계 요청 2건, 동일 스킬 수정 3건)의 충돌을 **차단만 하지 말고 자동 해결**하고, 실제 v0.2.29 ZIP에서 5회 격리 시험·확인된 gap만 최소 보완. **유료 리뷰와 LIVE는 하지 않음**.
- 읽기 기준: 해당 Work `CURRENT.md`, `GPT_V029_FIVE_WINDOWS_AUTO_RECOVERY_DISPOSITION_r0001_20261120_KST.md`, 실제 v0.2.29 개발 결과 `CLAUDE_AUTO_REVIEW_FOLLOWUP_RESULT_FOR_GPT_20261120.md`.

## 1. GPT 실행 결과 / 한계

| 항목 | 실제 결과 | 증빙 |
| --- | --- | --- |
| PRIVATE 실제 ZIP 바이트 재조회·SHA-256 | **PASS** | `artifacts/v0_2_29/skill-collab-watcher_v0_2_29_1120.zip`, 310753 B, SHA-256 `c67bc342fe77547b000fc42e1b886396cbef035c0d265dbcd124947e267ed83f` — connector binary base64 → JS SHA-256 직접 계산 및 manifest 일치 |
| 실제 ZIP 내부 테스트 파일/픽스처 정적 확인 | **PASS (static)** | ZIP 114 entries, `tests/conftest.py`, `tests/auto_helpers.py`, `tests/bundle.py`, `tests/test_auto_approval_e2e.py`, `tests/test_v029_cost_refused_exclusion.py` 확인. 기존 fake Github/throw-away Ed25519/CLI stub 재사용 |
| 새 5개 창 실물 패키지 pytest 4건 작성 | **PASS (문법 및 정본 게시)** | 테스트 파일 `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/artifacts/v0_2_29/validation/test_five_windows_actual_zip.py`, SHA-256 `687e16e78bba45684f61a9275dd0bb1db33097b471c7c8538b0b56589068ea61`, GitHub blob SHA `a4dfaebebe1d5e06a9237ac24177fe64d65b596e` |
| SHA/CRC/경로 검증 + 5회 새 임시 추출·pytest 반복 도구 작성 | **PASS (문법 및 정본 게시)** | 실행 파일 `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/artifacts/v0_2_29/validation/validate_v029_five_windows.py`, SHA-256 `416427f09ce4c2f61b0a2e2a8c5cc10c713b8b741fa30f7f7884d3ef8a9450d2`, GitHub blob SHA `608ca9dc3766e797ba8047439aa9027b609b7098` |
| runner 안전 실패 시험 | **PASS** | 없는 ZIP을 주면 `BLOCKED_OR_FAIL`, exit code 2, 0 rounds, actual paid 0. 실제 LIVE 경로는 참조하지 않음 |
| 기존 5창 SQLite 격리 mock 복구 시험 재실행 | **PASS_MODEL_ONLY** | `cowork_5windows_auto_recovery_model_20261120.py` 5회: 4회 정상 5/5, 한 회 UNCERTAIN 1·dependent 2 HOLD, 중복 runner 0 |
| **실제 v0.2.29 ZIP Python 전체 회귀 5회** | **NOT_RUN** | GitHub connector의 PRIVATE ZIP 바이너리를 이 Python 실행 컨테이너로 바이트 전송하는 지원 경로 없음. 실제 WINDOWS 호스트에 직접 실행하는 도구도 없음 |
| 실제 Windows 5개 창 Work source rebase / GitHub CAS 자동 복구 | **NOT_RUN** | 기존 Windows writer 설치·연결 구현을 아직 직접 실행/확인하지 못함 |
| 독립 유료 리뷰 / REQUEST·READY / Windows LIVE / 보호 위임 USD3 | **NOT_RUN / HOLD** | 신규 유료 호출 0, 운영 LIVE v0.2.25 / 위임 USD1 불변 |

**중요:** 스크립트 문법 PASS + SQLite 모델 PASS는 실제 v0.2.29의 5회 통합 PASS가 아님. 추가 pytest 파일은 고정 원본 ZIP에 넣지 않으며 **임시 추출본에만 복사**. 원본 SHA 그대로 유지. 테스트가 실패하면 FAIL로 보고, 마치 완료한 것처럼 승인/배포하지 않음.

## 2. PRIVATE 게시 테스트 산출물

- [실제 ZIP 보조 테스트](artifacts/v0_2_29/validation/test_five_windows_actual_zip.py) — 4개 시험:
  1. 설계 2 + 스킬 수정 3 = 고유 5개 REQUEST를 통합 STATIC으로 순차 READY, 반복 제출 서명 0.
  2. 구 `-DESIGN` 정책의 설계 2건 거절, 독립 스킬 3건 진행.
  3. `PER_REQUEST_COST` 기존 요청을 `POLICY_STOPPED`로 영구 제외, 상향 후 신규 5건 정상.
  4. **실제 watcher CLI subprocess** (다만 localhost fake GitHub + counting Claude stub + 임시 키/DB만)로 순차 5건에 대해 mock dispatch 5회, RESULT/RECEIPT/READY, 재시작 후 추가 호출 0.
- [5회 검증 실행기](artifacts/v0_2_29/validation/validate_v029_five_windows.py) — 매회 새 임시 폴더에 **SHA/CRC 검증된 정확한 ZIP** 추출, pytest 보조 4건 필수 PASS, 전체 테스트 최소 `1038 passed` (기존 Windows 1034 + 4), 5회 반복. 암호화 의존성 부족으로 security tests가 SKIP이면 최소 통과 수 불충족으로 FAIL. `--focused-only`는 smoke이고 릴리스 게이트 PASS로 사용 불가. 위험 경로 누락을 막기 위해 테스트 고정 SHA 검사 후 수행.
- ChatGPT 세션 전달용 동일 스크립트 2종 압축: `cowork_v029_5window_host_gate_20261120.zip`, 5050 B / SHA-256 `c2e82e4cce32b048929b2acef3579cc41d839f2abc3336d6c020be86b729afb7` (사용자 대화 다운로드용, GitHub 정본은 상기 텍스트 두 파일).

## 3. Windows Claude Code 단일 원샷 (아직 NOT_RUN)

1. PRIVATE `wonhwipark/CoWork-Skill-Collab` branch `main`, 기존 Work `collab/projects/COWORK-AUTO-APPROVAL-20261115-001`에서 **최신 CURRENT + 기존 AUTO_RECOVERY_DISPOSITION + 이 문서** 조회.
2. 운영 변경 0 상태로 **설치된** Work writer/GitHub CAS/스킬원본 최신조회·rebase 지원, watcher `recover/reconcile` 기능과 실제 권한을 판별. 증거 없는 기능 존재 주장 금지.
3. 기존 허용된 Windows 로컬 경로에 DEV ZIP 하나를 내려받을 수 있으면 SHA `c67bc342fe77547b000fc42e1b886396cbef035c0d265dbcd124947e267ed83f`로 고정. 이전에 `gh api`/Python 다운로드 권한이 거부된 경로라면 같은 동작·경로 변경으로 거부 우회 금지, 정확한 BLOCKED 사유 기록. 운영 DB/키/Tasks/Notifier 접근 및 설정 변경 금지.
4. 두 보조 Python 파일을 함께 받은 뒤 명령 예:
   ```
   python validate_v029_five_windows.py --zip <approved-local-dev-zip-path> --companion-test test_five_windows_actual_zip.py --output v029_five_windows_result.json
   ```
   실제 Python 전체 pytest x5 + mock transport/signer/runner만 사용. CLI e2e의 `FakeGitHub`는 loopback 테스트 서버 사용, 외부 GitHub·실제 Claude 모델 호출 금지. 사용자 데이터/비밀키 미사용.
5. **별도의 기존 writer 실물 시험:** (a) 같은 skill의 구 base SHA를 본 수정 3건은 새 원본 HEAD/revision/rebase/시험 후 REVIEW 전에 SHA 고정, (b) 공통 CURRENT/TRACKER의 충돌 4건은 GitHub blob SHA CAS→원본 재조회→각 Work 무손실 병합→readback, (c) REQUEST ID는 게시 전만 재발급, (d) UNCERTAIN은 영수증·DB 근거로 **정산만** 하고 이미 시작된 paid job 재호출 0, 같은 skill 후속 의존 Work만 보류, (e) scope/구 DESIGN 거부/기존 cap 거절 영구 제외. 실제 writer가 이 기능을 지원하지 않으면 `GAP_CONFIRMED`로 원인 파일/함수 특정 후 관련 기존 Work의 최소 DEV 보완 후보, 새로운 SHA로 관련 시험 전체 재실행. watcher가 Work 원본을 임의 병합하는 확장은 금지.
6. 결과에 `ZIP_5X=PASS/FAIL/NOT_RUN`, `WRITER_CAS=PASS/FAIL/NOT_RUN`, `SKILL_REBASE=PASS/FAIL/NOT_RUN`, 5개 창별 mock reviewer 호출·서명·READY·UNCERTAIN·증거를 정직하게 기록. 사용자 5회 검증 게이트 충족 전 **신규 유료 독립 리뷰/실제 REQUEST·READY/모델 호출·LIVE/USD3 위임 변경 모두 HOLD**. 패키지 바이트 수정 시 v0.2.29를 덮어쓰지 말고 v0.2.30 DEV 등 후속 새 버전으로 보존, 별도 검증/독립 리뷰 조건 유지.
7. 기존 Work 안에 결과 1건·필요 최소 CURRENT/TRACKER 수정, PRIVATE `main` 원격 commit·bytes readback 및 SHA를 보고. 단순 GitHub 문서 게시가 Windows Claude Code를 자동 시작하지는 않음.

## 4. GPT 현재 판정 및 다음 동작

- `SOURCE_ZIP_SHA=PASS`, `HOST_TEST_CODE=PREPARED_STATIC_PASS`, `MODEL_5X=PASS_MODEL_ONLY`.
- `ACTUAL_V029_ZIP_5X=NOT_RUN`, `ACTUAL_WINDOWS_WRITER_RECOVERY=NOT_RUN`, `INDEPENDENT_REVIEW=NOT_RUN`, `LIVE=v0.2.25`, `AUTO_DELEGATION_USD3=NOT_APPLIED`.
- `NEXT_ONE_ACTION`: **Windows Claude Code가 위 3절 원샷을 수행**해 결과 원격 게시. GPT는 그 결과를 확인하고 유료 리뷰 진행 여부만 판단. 새 사용자 반복 승인이나 별도 유료 요청 자동 발행 금지.
