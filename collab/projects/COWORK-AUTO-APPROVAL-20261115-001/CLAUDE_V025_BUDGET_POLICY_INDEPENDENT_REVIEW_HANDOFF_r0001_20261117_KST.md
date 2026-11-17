# Windows Claude Code 독립 리뷰 인계 — 비용 정책 v0.2.25

- CoWork PRIVATE: `wonhwipark/CoWork-Skill-Collab`, 정본 `main`.
- Work: `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/` (새 Work 생성 금지).
- 사용자 최신 요청·GPT 판정: `GPT_AUTO_REVIEW_BUDGET_POLICY_r0002_20261117_KST.md`.
- 개발 브랜치: `dev/auto-review-budget-policy-20261117`.
- 고정 검토 ZIP: `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/candidates/skill-collab-watcher_v0_2_25_1117.zip`, **283930 bytes**, SHA-256 **`26d63c8a03290499b13b2ceb8ff0b70c06eb1b1bcc1a25fe3d8f65fcc213d228`**.
- 이전 고정 ZIP: 같은 Work/dev/auto-quota-cost-only-20261117의 `skill-collab-watcher_v0_2_24_1117.zip`, SHA-256 `3c78699b734d88202a34ef5fd430f5f278ab1692a437b6affb6b6c64d24ca360`.
- 빌더·테스트: `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/dev/build_v025_review_budgets.py`, `patch_v025_budget_tests.py` (개발 branch).
- 개발 자체시험: [CI #44011874422](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/44011874422), **29 PASS/2 SKIP targeted, 582 PASS/30 SKIP/1 제외 Linux suite**, `REMOTE_BYTE_READBACK_PASS`; 독립 Windows 리뷰로 취급 금지.

## 검토할 결함 위험과 기대 동작

1. **보호된 위임/로컬 정책 책임:** 기본 `POLICY-STATIC-V1` 건당 **USD 1.50**, 디자인 `POLICY-STATIC-V1-DESIGN` 건당 **USD 3.00**. REQUEST는 정책명만 선택하며 임의 숫자로 직접 금액 지정 금지. `run_budgets_usd`의 로컬 등록과 보호 위임 `max_request_usd`가 모두 유효해야 허용. 기존 `max_request_usd: 1.0`이면 1.5/3 모두 차단되는지; 디자인 이름 미등록·보호 위임 1.5인 상황에서 디자인 3이 거부되는지; project/skill scope·만료·서명·SOURCE_PIN 정확히 검증되는지 확인.
2. **누적 상한 제거 완전성:** `auto_policy.assess`, `state_store.auto_claim`, `orchestrator._check_ceilings`, `state_store.claim`, `Config.load`에서 일일 횟수/비용·월간 횟수/비용이 실제로 신규 요청을 차단하지 않는지. KST 이전에 생긴 `UNCERTAIN` 예약도 다른 request_id를 차단하지 않으며 원 요청 재시도는 계속 `EXISTS`/fail-closed인지. 비용·호출 텔레메트리는 이력으로 보존.
3. **건당 비용 실제 제어:** 런타임이 선택한 로컬 설정 금액을 Claude CLI의 `--max-budget-usd`에 전달하는지, 예산 초과는 `FAILED`·재호출 금지로 처리하는지, 비용 추정과 실제 청구가 다를 수 있음을 결과가 표시하는지. CLI 본체 유료 호출로 시험하지 말고 fake runner/인자 단위시험 사용.
4. **경합·중복 보호:** `BEGIN IMMEDIATE`, 요청별 SQLite 고유키, 기존 N1/READY LAST, 원격 게시 실패 후 결과만 재전송, 위조·만료·repo_id mismatch·불확실 실행·중복 0 재호출 확인. 레거시 DB/WAL/SHM 정정·삭제·마이그레이션 없음.
5. **미래 가격 수정·승인 범위:** 기존 `reviewer.config.json`의 `known_run_policy_refs` 맵을 통해 1.5/3 값을 변경할 수 있는지. 로컬 정책 보호·위임 변경 시 백업/검토/서명 범위·만료 유지. 이전 REQUEST는 기존 고정 금액·SHA·영수증 보존, 기존 REVIEW 재큐잉 금지.
6. **Windows 실행검증:** Windows 전용 잠금·Shadow/CLI·Windows 3.11 운영 인터프리터 테스트를 **LIVE 미변경 격리 임시 디렉터리**에서 실제 실행. 기사용 로컬 환경·권한과 충돌하지 않도록 격리. 테스트는 모델 호출 0·원격 게시 0·운영 알림 0.
7. **릴리스 정합성:** 소스 ZIP SHA/CRC·내부 필수파일·버전 명세·개발 diff·보호 파일 미포함·rollback/symlink/path traversal 체크. 프라이빗 후보를 PUBLIC/호스트 설치 완료로 승격 금지.

## 결과 기록 형식

개발 세션과 독립 리뷰는 구분. 가능하면 명시적 independent 리뷰 세션에서 본 ZIP·commit·바이트로 판단. 유료 리뷰 실행은 기존 유효한 별도 사전 위임/승인/실제 비용 게이트가 확인된 경우에만 유효 REQUEST/READY를 이용; **이 문서 자체가 서명/READY/유료 실행 트리거가 아님**.

결과: 동일 Work의 `CLAUDE_V025_BUDGET_POLICY_INDEPENDENT_REVIEW_RESULT_FOR_GPT_20261117.md`, 증거·PASS/FAIL/SKIP/NOT_RUN·판정/지적·SHA/bytes·Windows 실행 결과·잔여 승인·다음 한 조치 포함. 허용된 PRIVATE main 게시 후 원격 본문과 실제 ZIP 바이트 재조회. Windows LIVE 설치·보호 위임/Task·Notifier 변경은 **별도 유효 운영 승인 및 재난 복구/단일 provider 안전 조건이 확인된 범위에서만**. 보류 시 `HOST_APPLIED=NOT_RUN` 및 `INDEPENDENT_REVIEW=NOT_RUN/PENDING`을 정확히 보고.

원래 요청 `REQ-L1-WORK-KNOWLEDGE-GUARD-CODE-R1-20261117`와 MSC 요청, 과거 불확실 서명·예약/완료 이력은 무손실 보존·자동 재큐잉 금지.
