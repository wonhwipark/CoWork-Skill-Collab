# GPT 자동 승인 정책 격리 테스트 증거 — 2026-11-15 KST

- GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab` / `main`
- 상대 경로: `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/GPT_AUTO_APPROVAL_PROTO_TEST_RESULT_r0001_20261115.md`
- 범위: Python 순수 정책 판정(Windows/GitHub/Telegram/API I/O 없음), 외부 reviewer 호출 0
- 설계/본격 인계: `AUTOMATIC_SIGNING_MINIMAL_DESIGN_r0001_20261115.md`, `WINDOWS_ONE_SHOT_DEVELOP_TEST_CANDIDATE_HANDOFF_r0001_20261115.md`
- **시험 명령(실행 환경 Linux Python):** `cd /mnt/data/cowork_autoapproval_proto && python -m unittest discover -s . -v`
- **실측 결과:** `Ran 25 tests in 0.001s — OK`, **PASS 25 / FAIL 0 / SKIP 0**. 정상 허용·기본 disabled·만료·소급 요청·장래 시각·다른 repo/branch/project/skill·빈 allowlist·정책 상향·2회 시도/호출·잘못된 state/pin·$1 초과·위임 자체의 한도 완화·완료/불확실 중복·CRC·키·atomic ledger·일/월 예산 위반.
- 실측 로컬 소스 `auto_policy.py` 3451 bytes, SHA-256 `26cfe6abe6d74361c0d64270cc3c6ca9f1e0da5f3761814df4fea2ca73ac333c`, Git blob `5308a8d71703fe65bc5eb7bbe7e71267d9588d88`.
- 실측 로컬 회귀 `test_auto_policy.py` 4291 bytes, SHA-256 `64f816b111c169cc1460a03c48d291b6b8e9b88dd51be50c1d1bd59be53d3c87`, Git blob `8adc334322807585a5460c770fe62c4c7aa1a4c2`.
- **원격 정확성:** PRIVATE `main`에 게시된 두 소스의 blob SHA가 실행 파일에 대해 실제 `git hash-object`로 산출한 값과 일치하며 GitHub fetch 내용도 동일 확인. 이 사실은 **시험한 Python 소스가 원격에 일치한다**는 증거이며 **Windows 통합에 대한 증거는 아니다**.
- 각 코드 위치: `prototype/auto_policy.py`, `prototype/test_auto_policy.py`. 모두 참고 코드, 운영 watcher 구성 요소 아님. 로컬 Python 임시 파일은 대화 작업 디렉터리; Windows Claude Code는 GitHub 정본을 읽으면 충분하고 파일 전송 불필요.
- **엄격한 미검증:** `WINDOWS_PYTHON311=NOT_RUN`, `ACTUAL_SIGNER_INTEGRATION=NOT_RUN`, `APPROVAL_SIG/READY_BYTES_CONTRACT=NOT_RUN`, `ATOMIC_DB_IO=NOT_RUN`, `GITHUB_REMOTE_CREATE_ONLY=NOT_RUN`, `WINDOWS_SHADOW=NOT_RUN`, `FULL_V0220_REGRESSION=NOT_RUN`, `INDEPENDENT_REVIEW=NOT_RUN`, `OPERATING_DEPLOYMENT=NOT_RUN`, `AUTO_SIGNING=OFF`, `PAID_CLAUDE_CALLS=0`.
- 다음 한 동작: Windows Claude Code가 원샷 인계에서 실제 v0.2.20 코드로 재사용/최소 연결을 구현하고 실제 기존 signer/Watcher 계약과 전체 회귀·SHADOW·candidate ZIP/rollback을 확인한 후 PRIVATE 결과/receipt readback.
