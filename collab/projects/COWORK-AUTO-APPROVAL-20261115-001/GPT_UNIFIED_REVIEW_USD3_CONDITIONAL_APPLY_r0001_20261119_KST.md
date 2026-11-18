# Windows Claude Code 원샷 — 단일 USD 3 리뷰 자동 승인 정책 정합화 (r0001)
- 일자: 2026-11-19 KST
- 정본: **GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`**
- 기존 Work: `collab/projects/COWORK-AUTO-APPROVAL-20261115-001`
- 요청 근거: 사용자가 일반/설계 비용 구분 및 하루 건수 제한의 필요성을 질의한 후, GPT가 **모든 신규 리뷰 건당 $3, 일/월 건수·비용 상한 없음, REQUEST당 1회·기존 승인 보호 유지** 정책과 Windows 자동 승인 정합화를 제안했고 사용자가 “그래”로 실행을 승인.
- 작업 유형: 기존 v0.2.25 watcher/사전검증 도구를 **REUSE→CONNECT→검증된 최소 CONFIG 변경**. 별도 Work·인증 스키마·새 watcher/Notifier 추가 불가.
- 비용/호출: **신규 유료 독립 리뷰 REQUEST/READY=0, 실제 모델 호출=0** (실호출을 시험 목적으로 만들지 않음).
- 현재 상황: Windows 2026-11-18 호스트 보고에서는 단일 GitHub LIVE watcher v0.2.25 설치·Task Running, reviewer 정책맵 `POLICY-STATIC-V1=$1.50`, DESIGN=$3, LARGE=$3, 보호 위임 `max_request_usd=$1.00`. GPT는 Windows 파일/DB에 직접 접근하지 못하므로 이 원샷 게시 자체는 호스트 적용이 아님.

## 1. 목표 불변 조건
1. 신규 **일반 스킬·설계** Claude 독립 리뷰는 구분 없는 **`run_policy_ref=POLICY-STATIC-V1`, 요청당 최대 USD 3.00**. R0~R3의 검토 깊이는 프롬프트 참고일 뿐, 과금 등급으로 사용하지 않음.
2. **일/월 총 호출 횟수 및 누적 비용 상한 없음**. 단, `max_model_calls=1` / `attempt=1` / 중복 영구 차단 / UNCERTAIN 자동 재시도 0 / 실제 실행 결과·비용 영수증 필수.
3. 현재 허용 프로젝트 family `COWORK-`·`L1-WORKSPACE-` 및 현행 정확한 skill allowlist·보호 위임 유효기간·서명/인증 신뢰 루트·SOURCE_PIN·고정 ZIP SHA/크기·READY LAST를 **변경하지 않음**. 새 프로젝트·스킬/기간·사용자·키/토큰 추가 승인이 아님.
4. **과거 고정 REQUEST/READY/영수증/Guard UNCERTAIN은 무손실 보존.** 이 신규 금액 승인을 옛 미완료 건에 소급 적용해 자동 서명·재디스패치 금지.
5. 단일 provider는 GitHub뿐. 기존 Windows Notifier/Telegram·DB/Task/키/다른 provider 건드리지 않음. 기존 watcher v0.2.25 ZIP SHA `26d63c8a03290499b13b2ceb8ff0b70c06eb1b1bcc1a25fe3d8f65fcc213d228` 불변. v0.2.26 DEV ZIP 미설치.

## 2. Windows Claude Code 조건부 일괄 수행

**A — G0 읽기 전용 검증.** 이 Work의 CURRENT 최상단과 이 문서, `collab/ops/CONTRACTS/REVIEW_TIER_TOKEN_BUDGET_V1.md`, 이관 CURRENT를 읽어 최신 요청/중복 여부 확인. 실제 v0.2.25 설치본·`reviewer.config.json`·보호된 `auto_delegation.json`·signer/approval 버전·권한/만료·자동 승인 enable·lease/provider·Notifier를 READ_ONLY 조회. 요청당 $1, 보존된 하루 2회/$3·월 $10 값이 **현재 v0.2.25에서 실제로 무시되는지** 코드+격리 반례로 확인; 이미 무시되면 보호 파일의 낡은 필드는 무리하게 삭제/고쳐 쓰지 않음.

**B — 레거시 승인/재실행 위험 차단.** 과거 pending 9건과 Guard의 `AUTO_SIGNING_UNCERTAIN`, `pending_requests`, 승인 claim/서명·READY·dispatched·비용·원격 영수증을 **읽기 전용** 대조하고, 현재의 정책 변경으로 이전 REQUEST가 신규 자동 서명 대상에 들어오지 않도록 운영 측 최소 차단을 증명. 최소한 기존 `request_id/revision/package_sha256`의 무손실 보존, 완료 재호출 0, 현재 기록된 미완료/불확실 내역의 소급 서명 0. 제품의 요청 적격 판단을 바꾸지 않고 증명이 불가하면 **CONFIG_APPLY=BLOCKED**, 권한·원인만 보고. Guard 불확실 상태 임의 해제·예약 재큐잉/삭제 금지.

**C — 독립 사전검증 도구 시험.** PRIVATE main `collab/ops/review_request_gate.py`와 `collab/ops/tests/test_review_request_gate.py`를 받아서 새 `--intent unified` 경로 확인. 독립 Python 3.11.9 격리 시험 실행:
`python -m unittest discover -s collab/ops/tests -p test_review_request_gate.py -v`.
합성 local config를 통해 `POLICY-STATIC-V1=$3` + `unified` PASS, $1/$1.50·잘못된 참조·비용 override·호스트 미설치·기존 pin 거부 PASS, 기존 historical skill/design 회귀도 PASS. 이 단계는 모델/서명/REMOTE_WRITE 0. 소스 변경점: 커밋 `f0a11fee`, `52769ffd`, `2187dd99`, `9e148408`; 최종 main 파일 SHA와 교차 검증.

**D — 안전한 보호 경로에서만 운영 정합화.** A~C PASS이고 사용자 본 승인 범위·**Windows 로컬 신뢰된 사용자/서명 권한**이 실제로 허용되며 새 $3 보호 위임을 정당하게 생성·설치할 수 있을 때만 진행. 보호 위임·설정·Task·DB/WAL/SHM/설치본·rollback 자료를 백업하고 바이트/SHA·ACL 확인한 후 watcher를 안전 정지. 기존 승인 도구가 제공하는 보호된 정책 갱신 수단으로 **요청당 max_request_usd=$3.00** 및 현행 `POLICY-STATIC-V1`에만 유효한 동일 프로젝트/스킬/만료의 최소 변경을 적용. `review_policy.max_budget_usd=3.0`, `known_run_policy_refs["POLICY-STATIC-V1"].max_budget_usd=3.0`. 과거 `-LARGE`/`-DESIGN` 정책명·고정 REQUEST를 삭제/재작성하지 않음. 일·월 숫자는 적용/승인 로직에 실질 영향이 없도록 검증하되 불필요한 키 재서명/수정은 하지 않음. **단순 JSON 직접 편집·키 위조·GitHub 문구만으로 보호 권한 승인 주장·새 서명키 생성·정책 우회 금지**. 유효한 보호된 갱신 수단이나 사용자 인증이 없으면 변경 0·BLOCKED.

**E — SHADOW·롤백·LIVE 검증.** 재시작 전후 동일 SHA·provider 단일 lease·보호된 정책 load PASS, 정확 프로젝트/스킬·만료/변조/중복/소급 요청의 fail-closed PASS, 정상 신규 합성 $3 정적 요청 **모델·원격 게시 없이** 적격성 평가 PASS, 요청당 비용 초과·무단 확대 FAIL_CLOSED, 일·월 횟수/비용 누적이 높아도 새 정책이 더 이상 차단하지 않음 PASS. Task 2주기+재시작을 관찰하되 자동으로 돈 드는 과거 요청이 발생할 가능성이 없어야 함. 안전 불확실 시 즉시 정지/보존·원복 (불확실 리뷰는 재큐잉 금지). **시험용 유료 리뷰 생성 금지**.

**F — 동일 Work에 결과 게시·원격 재조회.** `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/CLAUDE_UNIFIED_REVIEW_USD3_HOST_RESULT_FOR_GPT_20261119.md` (실제 결과, 누락이면 `NOT_RUN`)를 작성, 관련 CURRENT·TRACKER 현행 요약만 갱신. 실제 bytes SHA-256/commit/readback·백업 롤백 경로(민감정보 배제), 변경 전후 protected scope/expiry/hash(비밀 내용 제외), Windows CLI 회귀 건수, SHADOW, 소급 0건, 실제 model_calls=0, 신뢰된 승인 수단, `HOST_CONFIG_APPLY`, `AUTO_SIGNING_USD3`, `DAILY_MONTHLY_LIMITS_DISABLED`를 개별 PASS/BLOCKED/NOT_RUN으로 구분. 정보 없으면 PASS 추정 금지.

## 3. 실패 시 처리 및 범위
- A~D 중 하나가 실패하면 운영 변경을 하지 않고 READ_ONLY 진단·자체시험·문서 결과를 먼저 게시. **기존 $1 보호 위임/현재 LIVE 계속 사용**; 새 $3 REQUEST는 자동 승인 차단이 정상이므로 임의 수동 READY 우회·소급 자동 승인 금지.
- 설치 성공 여부와 관계없이 **새로운 Claude 독립 리뷰·추가 유료 요청·PUBLIC 배포·v0.2.26 설치·기존 pending 재실행 0**.
- 서명/READY는 향후 실제 정식 사용자가 새로운 리뷰를 요청할 때만 현재 보호된 검증을 통과한 입력으로 게시.
- 기존 같은 목적 Work를 그대로 재개. 독립 리뷰를 위한 새 REQUEST를 만들지 않으며 운영 CONFIG 검증을 유료 코드 리뷰로 바꾸지 않음.

**NEXT_ONE_ACTION:** Windows Claude Code에서 이 파일의 A~F를 **한 번** 수행하고 결과를 PRIVATE main에 게시·실제 원격 재조회. GPT는 반환된 실제 결과를 보고 유효 적용/부분 보류를 종결 판정.
