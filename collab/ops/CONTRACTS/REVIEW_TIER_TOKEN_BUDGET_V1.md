# CoWork 리뷰 등급 / 토큰·비용 예산 계약 V1
2026-11-14 KST · USER_REQUESTED_DESIGN · CONFIG_NOT_DEPLOYED
Applies to: CoWork watcher 독립 Claude 리뷰 및 L1Work PUBLIC ZIP·handoff MD 링크 리뷰
Canonical repo: PRIVATE `wonhwipark/CoWork-Skill-Collab`, `main`
Exact path: `collab/ops/CONTRACTS/REVIEW_TIER_TOKEN_BUDGET_V1.md`

## 1. 목적·적용 경계
- 사용자 1인 협업에서 검토할 때마다 전체 ZIP을 전부 읽는 비효율을 피하고, **검토 목적에 맞게 입력·출력 토큰 예산과 최대 비용을 분리**한다.
- 기존 예산 정책 `POLICY-STATIC-V1` ($1), `POLICY-STATIC-V1-LARGE` ($3), `POLICY-STATIC-V1-XLARGE` ($6)는 **후방 호환** 유지. 신규 R0 저비용 등급은 후보이며 배포/활성화 후 실제 사용 가능하다.
- **등급 설정·상한 정의 = 무기한 유료 리뷰 실행 승인 아님.** 요청마다 승인된 review ID, target immutable commit/ZIP hash, 리뷰 횟수·정책·비용 상한이 필요.
- 이번 `REV-COWORK-V0214-20261114`은 사용자 승인한 **R1 / 기존 `POLICY-STATIC-V1` / 최대 $1 / 1회 / effort medium**. 키/신뢰 루트는 동일 Windows PC에서 A안에 따라 보호하고 `trust_root_independence=warn` 허용; B 토큰 교체·LIVE는 미승인.

## 2. 리뷰 레벨과 예산
아래 수치는 **추천 입력 컨텍스트·응답 토큰 목표 예산**이며 **CLI가 보장하는 실제 hard token cap이 아님**. 각 레벨의 비용은 **정식 개별 실행 승인 시 요청할 최대 금액**, 기본 무인 실행 허용 아님.

| 레벨 | 기본 리뷰 종류 | 권장 입력 토큰 목표 | 출력 토큰 목표 | 최대 agent turns | 비용 정책 상한(USD) | 기존 정책 매핑 |
|---|---|---:|---:|---:|---:|---|
| **R0** | 단순 정합성: MD 형식, 링크, 이름·버전·설정값, ZIP manifest 간 비교 | 4,000 | 1,000 | 1 | **0.25** | 신규 `POLICY-CONSISTENCY-V1` (후보, 실제 등록 전 사용 금지) |
| **R1** | 변경·결함 영향: 파일 diff, 원인·수정, 주변 연동과 핵심 회귀 | 16,000 | 3,000 | 3 | **1.00** | 기존 `POLICY-STATIC-V1` |
| **R2** | 구조 리뷰: 호출 체인·모듈 경계·상태기계·Windows/GitHub 계약 | 40,000 | 6,000 | 5 | **3.00** | 기존 `POLICY-STATIC-V1-LARGE` |
| **R3** | 심층 통합/전환 설계: 여러 모듈·상태 이행·복구·롤백·운영 회귀 | 75,000 | 9,000 | 8 | **6.00** | 기존 `POLICY-STATIC-V1-XLARGE` |

기본 선택: 단순 Handoff MD 확인 → R0; 구체 결함/diff 수정 → R1; 모듈/설계 리뷰 → R2; 독립적인 운영 전환 구조 종합 검토 → R3.
- 사용자가 **리뷰 목적**을 지정하면 그 목적을 우선. ZIP 전체 크기만으로 최고 등급 승격 금지. 대상 파일이 커도 요청한 변경 diff와 필요한 call-site/테스트를 먼저 추려서 예산 내 review.
- R1에서 정책 버전/논리 키/일일 비용 경쟁 등 **인접 핵심 구조 위험**을 보는 것은 가능; 한 번의 리뷰 중 R2로 자동 승급·재호출·추가 과금 금지. 충분한 분석이 불가능하면 `PARTIAL_SCOPE`와 추가 심층 검토 후보만 보고.
- 레벨이 낮으면 PASS 근거 범위도 좁음. R0 문서 정합성 PASS = 전체 제품 구조·안전성 PASS가 아님.

## 3. 실제 호출 제어: 토큰 한계의 정직한 표현
Claude Code CLI 공식 `-p` 모드에는 `--max-budget-usd`, `--max-turns` 제어가 있으나 **해당 조합만으로 전체 호출 input/output token 총량의 절대 하드 캡이 성립한다고 선언하지 않는다**. 비용은 CLI의 **추정**이므로 실제 청구와 다를 수 있고 모델 응답 과정에서 임계치를 넘어갈 수 있음.
- **모델 호출 이전**: review manifest에서 대상 버전/고정 SHA·정확 파일/정확 diff/필요 테스트를 한정; local estimator 또는 실제 사용 가능한 토큰 계산기(외부 호출/비용이 생기지 않는 방법 우선)로 **예상 입력 토큰**을 추정해 레벨 목표 이상이면 더 압축/파일 선택. 계산법/오차를 영수증에 명시. 무관한 history·대형 문서·중복 배포본 투입 금지.
- **실행 중**: 호출 wrapper 또는 Claude runner가 지원하는 `--max-budget-usd`와 `--max-turns`를 적용. 단일 요청 `max_model_calls=1`, 별도 서브에이전트 추가 생성/자동 재시도 금지. CLI 비용 추정 상한 초과 가능성을 감안해 **정책 비용 한도보다 낮은 내부 stop threshold** (예: R1 $0.85, 조건·호스트 검증 뒤 조정) 적용을 우선 고려; 플랫폼 제공상 수치가 실제 결제의 완벽한 차단을 보장하는 것으로 주장 금지.
- **출력 제어**: 필요한 판정 결과(근거 위치·Severity·수용/보류·후속 재현)만 요청; 요청한 출력 목표를 프롬프트 계약에 기재. 실제 출력 토큰을 CLI 결과/usage로 측정해 보고하되 CLI print mode 전체 출력에 hard token cap이 **있는 것처럼 표기하지 않음**. SDK/API가 검증된 별도 출력 토큰 제한을 지원하더라도 검증 없이 자동 적용하지 않음.
- **실행 후**: `input_tokens`, `output_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`, `total_cost_usd`, `max_budget_usd`, `max_turns`, `selected_review_tier`, `target_sha256/commit`, `token_estimation_method`, `limit_reached`, `scope_partial`를 확보 가능한 만큼 영수증에 기록. unavailable 값을 0으로 채워 성공으로 표시하지 않음.
- 실제 CLI `--help`, 설치 버전, `RealReviewRunner` 인자 지원을 Windows에서 확인하고 **지원되지 않는 CLI 옵션을 임의로 통과시키지 말 것**. 기능 없으면 `BUDGET_ENFORCEMENT=PARTIAL`로 기록하고 출력 크기·입력 범위/승인 비용을 더 보수적으로 제한.

## 4. 자동 등급 선택·승급 방지
- 기본은 **R0 또는 R1**. 사용자 '구조 리뷰' 요청이 명백할 때 R2를 추천할 수 있으나 실제 유료 호출은 해당 레벨 예산 개별 승인 필요.
- 범위를 초과하면 모델을 먼저 실행하지 말고 입력을 압축하거나 `BUDGET_SCOPE_TOO_LARGE`로 종료. 자동으로 비용/레벨 상승 금지.
- 동일 논리 리뷰 요청의 **중복 호출 0**, 상태 불명 `REVIEW_UNCERTAIN`에서 무승인 재시도 0. 재리뷰는 변경된 ZIP 해시·신규 명시적 요청에 한정.
- GitHub PRIVATE에는 허용된 CoWork 자체 코드/ZIP/manifest를, PUBLIC L1Work에는 이미 공개된 스킬 및 `handoffs/` 문서 링크만 일반 리뷰 입력으로 사용. 회사 L1 코드·고객자료·자격정보는 제외.

## 5. 구현·배포 단계
- **현재 v0.2.14 ZIP에 위 4개 등급의 실행 제어가 모두 구현되어 있다고 가정하지 않음.** 기존 $1/$3/$6 정책은 선행 계약상 존재, 신규 R0 및 토큰 추적·입력 사전 예산 검사는 추가 구현/검증 후보.
- 이번 A안 독립 리뷰 1회는 **v0.2.14 아티팩트 변경 없이 R1**로 실시, prompt/manifest 범위 제한과 기존 비용 게이트 사용. 향후 reviewer tier 정책을 watcher 제품에 코딩한다면 신규 버전으로 별도 발행·관련 시험·독립 리뷰/배포 게이트를 거침. 리뷰 중 후보를 바꾸고 옛 아티팩트 PASS를 소급하지 않음.
- 정식 등급 분류·비용·사용량 지표가 실제 Windows runner에 연동되었는지는 **host test PASS**로 따로 입증; 본 문서 게시만으로 활성화 완료가 아님.

References: `collab/ops/CONTRACTS/REVIEW_TRANSPORT_V1.md`, `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_V0214_PREFLIGHT_DISPOSITION_AND_APPROVAL_GATE_r0001_20261114.md`.
