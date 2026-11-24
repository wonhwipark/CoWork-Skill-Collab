# CoWork 리뷰 등급 / 토큰·비용 예산 계약 V1

## 현행 해석 보충 — 2026-11-24 KST

- **최신 사용자 결정:** 독립 리뷰는 단일 유형이며 리뷰별 USD3/가격 상한·비용 정책 재승인·실제 과금 여부 확인을 신규 REQUEST 게시, GPT 판정, 재개 판단의 선행 조건으로 사용하지 않는다.
- **실행 후 관측과 실행 전 차단을 분리:** 모델 응답의 `usage`/영수증은 추적용이며 외부 과금 조회가 아니다. 과거 불확실 실행은 claim 보존·중복 호출 금지로 처리한다.
- **소스와 운영 구분:** GitHub Actions GPT Runner의 금액 차단 제거는 확인됨. Windows watcher 설치본의 과거 비용 게이트는 실제 호스트 readback 전까지 **적용 여부 미검증**으로 둔다. 가격 이외의 신뢰·서명·SOURCE_PIN·READY·scope·만료·중복 보호는 유지.
- **아래 r0004 및 2026-11-19 이하 USD3·등급·금액·CLI 예산 문구는 레거시 이력/호환 설명으로만 해석**하며 신규 정책 또는 필수 사용자 비용 승인으로 적용하지 않는다. 기존 고정 REQUEST/영수증은 수정하지 않는다.

---

## 현행 우선 r0005 — 독립 리뷰 단일화 (2026-11-22 KST)

- 사용자 최신 요청: '유료 리뷰' 별도 유형·리뷰별 금액 제한·비용 정책 선택과 내부 자동 가격 판단 제거. **한 유형 '독립 리뷰'**로 명명. 새 GPT 게시기에는 `unified USD3` 금액 검사를 더 이상 적용하지 않는다. 구형 검사와 계약은 과거 고정 요청의 이력·진단 호환으로 남긴다.
- **실제 Windows v0.2.29 LIVE**의 비용·allowlist 승인 게이트는 이 문서만으로 변경되지 않았다. 운영 코드·보호 정책 전환을 검증할 때까지 기존 비용 검증은 실효. 이 규칙을 근거로 무단 서명·READY·유료 모델 호출 금지.
- 다음 보호 모델은 가격 속성이 아니라 **인증된 독립 리뷰 실행 권한 + 고정 입력 + 서명·READY + 동일 요청 1회·중복/UNCERTAIN 방어**다. 사용자 지시만으로 무제한 비용을 승인한 것으로 보지 않으며, 기존 계정 과금은 여전히 발생할 수 있다. [최신 변경 및 호스트 전환](../../projects/COWORK-AUTO-APPROVAL-20261115-001/GPT_INDEPENDENT_REVIEW_COST_GATE_SIMPLIFICATION_RESULT_r0001_20261122_KST.md).

---

## 2026-11-22 r0004 — 정식 REQUEST 출판과 Windows 실행 승인 분리 (현행 우선)

- Claude 아키텍처 R1 및 GPT `ACCEPT_WITH_CORRECTIONS__OPTION_B` 수용. 사용자 명시 리뷰 요청의 GPT 게시 단계에는 **Windows LIVE `reviewer.config.json` 사전 조회를 필수로 요구하지 않는다**. GPT는 현재 Work·요청 형식·정적 unified `POLICY-STATIC-V1` USD3·ZIP SHA/크기/CRC·SOURCE_PIN 두 커밋·중복을 검증해 정식 REQUEST를 게시한다. 단, 실제 LIVE 등록 금액이나 자동 위임 적합성을 주장하지 않는다.
- Windows 운영 watcher/보호 signer에서 실제 정책·건당 예산·위임 범위·enabled_at·만료·서명·READY·중복/UNCERTAIN 검증은 그대로 유지하며, 부적합한 REQUEST가 게시돼도 **READY 및 모델 호출 0**. 공개 GitHub 문서는 유료 사용 권한이 아니다.
- 아래 2026-11-17 `REQUEST 게시 전 정책 호환성 필수 게이트`는 **이전 설계 이력으로서 신규 게시 필수조건에 적용하지 않는다**. `review_request_gate.py select/check --live-config`는 호스트 진단용. 운영 v0.2.29 `POLICY-STATIC-V1=USD3` 호스트 확인과 ZIP에 포함된 과거 예제 USD1의 차이를 혼동하지 않는다. [r0006 최신 제출 계약](PRE_READY_SOURCE_PIN_PREFLIGHT_V1.md)과 [GPT 판정](../../projects/COWORK-AUTO-APPROVAL-20261115-001/GPT_ARCH_REVIEW_DISPOSITION_r0001_20261122_KST.md)을 우선한다.

---

## 2026-11-19 KST — 최신 승인: 신규 독립 리뷰 단일 건당 USD 3.00 (r0003)

- **사용자 명시 승인:** 기존 일반/설계 비용 분할 대신 모든 신규 정식 Claude Code 독립 리뷰에 **동일한 건당 최대 USD 3.00**, 일·월 호출 횟수 및 누적 비용 제한 **없음**. R0~R3 리뷰 깊이는 참고·범위 선택만 가능하며 유료 등급·자동 승급의 근거 아님.
- **신규 요청 단일 참조:** 기존 `POLICY-STATIC-V1`을 **건당 USD 3.00**으로 등록해 공통 사용. 별도 새 정책 ID/원장/승인 스키마 생성 없음. 기존 `-LARGE`, `-DESIGN` 등은 역사·고정 REQUEST 호환 이력으로만 보존. 새 요청의 승인 경로는 `--intent unified`, 결과 `selected_run_policy_ref=POLICY-STATIC-V1`, `expected_max_budget_usd=3.00`.
- **사용자 승인 ≠ 호스트 보호 정책 설치:** Windows watcher v0.2.25 운영 설정은 마지막 호스트 보고상 STATIC $1.50/DESIGN $3, 보호된 `auto_delegation.json`은 건당 $1.00. 현재 **신규 $3 자동 서명=NOT_OPERATIONAL**. 보호 위임은 Windows 호스트가 원본·서명 권한·ACL·만료·허용 프로젝트/스킬·레거시 pending 소급 실행 방지와 롤백을 확인해 **유효한 보호 경로에서만** 최소 변경. GitHub MD가 서명 승인 자체를 대체하지 않음.
- **요청마다 1회** `max_model_calls=1`, 기존 고정 입력 SHA/크기·SOURCE_PIN·서명·READY 마지막·중복·불확실/만료·scope fail-closed **유지**. 하루·월간 집계는 관측값일 수 있으나 실행 제한으로 쓰지 않음. `--max-budget-usd=3`은 플랫폼 청구액 절대 보장 아님.
- **과거 완료/대기 요청** 재서명·재큐잉·다른 예산으로의 소급 자동 승인 금지. Windows 적용 전 기존 pending/Guard 정산·선별·보존 조건 확인. 무허가 재실행 가능성이 있으면 **활성화 BLOCKED**. 기존 v0.2.25 LIVE watcher는 별도 적용 성공 전 계속 유지.
- **정본 실행 인계:** [통합 비용 조건부 적용](../../projects/COWORK-AUTO-APPROVAL-20261115-001/GPT_UNIFIED_REVIEW_USD3_CONDITIONAL_APPLY_r0001_20261119_KST.md). 신규 REQUEST 자체는 생성하지 않으며 유료 모델 호출 0.

> 아래 2026-11-17 r0002의 $1.50/$3.00 설명 및 이전 R0~R3 표·가격은 **당시 결정/기술 참조 이력**. 이 절이 신규 요청의 단일 정책에 우선한다.

## 2026-11-19 KST — 미설치 통합 정책의 순환 의존성 해소: UI/UX R1 *한 건만* 수동 부트스트랩

- 현재 Windows LIVE에서 `POLICY-STATIC-V1`은 USD 1.50, 공통 USD 3 설정 및 v0.2.27은 미설치. 통합 USD 3을 먼저 설치해야만 그 설치 전에 필요한 코드/UX 독립 리뷰를 할 수 있다는 순환 의존성은 **운영 가격 변경이 아닌, 이미 등록된 정책의 유효한 수동 승인 경로**로만 해소.
- 이번 **정확한 한 요청 `REQ-L1-WORKSPACE-WIKI-UI-UX-R1-20261119` rev 1**은 이미 승인된 한 건 USD 3 상한 안에서 현재 LIVE의 `POLICY-STATIC-V1-DESIGN` USD 3을 **수동 부트스트랩 transport**로 선택 가능. 사용자 “개선해줘”의 현재 차단 해소 요청을 적용. 신규 공통 비용 정책 `unified/STATIC=$3`과는 **별개**이며 일반/설계 가격 분리의 복원이 아님. 이전 UI Work의 `unified` 비실행 초안은 보존, 실제 수동 후보는 [r0002](../../projects/L1-WORKSPACE-RAG-20261111-001/WIKI_UI_UX_R1_REQUEST_MANUAL_BOOTSTRAP_DRAFT_r0002_20261119_KST.md). [Windows r0002 원샷](../../projects/L1-WORKSPACE-RAG-20261111-001/WIKI_UI_UX_R1_WINDOWS_SUBMIT_ONESHOT_r0002_20261119_KST.md)을 이 요청의 최신 지시로 사용.
- **필수 선행 검증**: 설치된 로컬 config로 `select/check --intent design --required-budget-usd 3.00` 및 실제 ZIP·REQUEST bytes 고정 PASS, 이어서 호스트 기존 `approve_request.py check`와 **실제로 유효한 수동 서명/승인 자격** PASS. `POLICY_COMPATIBLE_NOT_APPROVED`는 승인 자체가 아니다. 호스트 허가/비용 범위가 부족하면 REQUEST/READY/모델 0. 보호 위임 USD 1, 운영 watcher/config/키/DB/Task 변경 0. 다른 요청·ID·revision은 이 예외로 승인하지 않음.
- Commit A 실제 원격 readback/SOURCE_PIN(repo_id 문자열)/보호 서명/READY 마지막·중복·UNCERTAIN·모델 호출 1회·영수증 원칙 유지. 새 POLICY-STATIC-V1 통합 기본은 **실제 별도 배포가 검증되기 전까지 LIVE라고 주장하지 않음**.

## [과거 설계·신규 제출 비적용] REQUEST 게시 전 정책 호환성 필수 게이트 (2026-11-17 이력)

**모든 신규 CoWork 정식 리뷰 REQUEST는 게시 이전에 Windows 설치 LIVE의 실제 reviewer.config.json 기준으로 `collab/ops/review_request_gate.py`를 실행해 호환성을 확인한다.** GPT는 현행 설치 상태를 추정하거나 개발 후보에만 존재하는 정책명을 선택하지 않는다. 코드·문서 배포만으로 이 단계가 자동 실행됐다고 표시하지 않는다.

1. GPT는 리뷰 목적(`skill` / `design`)과 건당 금액(현행 기본 $1.50/$3.00)을 고정하고 Windows Claude Code에 `select --live-config <실제 Windows 로컬 reviewer.config.json> --intent design` 형태의 **읽기 전용 호스트 정책 조회**를 요청한다. `POLICY_COMPATIBLE_NOT_APPROVED`인 선택명만 사용할 수 있다. `design`은 LIVE에 DESIGN 등록 시 DESIGN, 없고 기존 LARGE $3이 실제 등록돼 있으면 LARGE를 선택한다. 모델/자동 리뷰 비용 승인 아님.
2. GPT가 작성한 신규 REQUEST 초안(필요 시 기존 Work의 비실행 draft 문서로 호스트에 전달) 및 고정 ZIP 실제 바이트로 `check --live-config <실제 로컬 config> --intent design --request <신규 REQUEST.md> --package <원본 ZIP>` 실행. 결과가 `PASS_PREPUBLICATION_ONLY`이거나 Windows 격리 검증 근거가 동일하게 확인된 경우에만 REQUEST와 ZIP을 commit A로 게시. `MISSING / UNVERIFIED / POLICY_* / SHA 오류`는 **NOT_POSTED / BLOCKED**; 임의 정책 변경·구두 확인·경험칙으로 PASS 대체 금지.
3. commit A의 실제 원격 ZIP 바이트·REQUEST 본문이 preflight가 출력한 `request_sha256`와 정확히 일치함을 확인한 후 기존 `source_pin.py`로 문자열 repo_id의 SOURCE_PIN을 생성·검증하고 마지막 원격 읽기 확인. Windows에서 기존 `approve_request.py check`와 유효 보호 위임/정상 승인 범위를 **별도 필수 검증**하고, 해당 승인에서만 서명·READY를 마지막으로 게시. 사전 게이트는 **정책 호환성**이며 서명·READY·금액 권한을 부여하지 않는다.

**강제 범위:** 이 게이트는 협업 REQUEST 작성자의 표준 절차 및 자동화 진입 코드에 적용한다. GitHub PRIVATE `main`에 브랜치 보호/필수 status check가 현재 설치·확인되지 않았으므로 임의 직접 API 쓰기 전체를 기술적으로 차단한다고 주장하지 않는다. 이를 보완하는 최종 fail-closed 안전장치는 기존 Windows 보호된 서명/READY 검증. 과거 고정 REQUEST/영수증·불확실 이력은 수정/재실행하지 않는다.


> **2026-11-17 최신 정책(r0002):** 일반 스킬 독립 리뷰 `POLICY-STATIC-V1` **USD 1.50/건**, 디자인 독립 리뷰 `POLICY-STATIC-V1-DESIGN` **USD 3.00/건**. **일·월 호출 횟수 및 누적 비용 상한 모두 폐기**. 보호 위임에서 승인한 요청별 금액·프로젝트/스킬/만료·중복 방지·서명/READY는 유지. 두 비용은 로컬 `review_policy.known_run_policy_refs`에서 향후 조정 가능. [결정·개발 후보·실제 시험](../../projects/COWORK-AUTO-APPROVAL-20261115-001/GPT_AUTO_REVIEW_BUDGET_POLICY_r0002_20261117_KST.md). LIVE 적용은 미실행. 아래 2026-11-14 R0~R3 기존 표와 사용자별 과거 $1/$3/$6 승인 사실은 **역사적 정책/특정 리뷰의 계약**이며 신규 자동 리뷰 기본 정책으로 사용하지 않음.
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
아래 수치는 **추천 입력 컨텍스트·응답 토큰 목표 예산**이며 **CLI가 보장하는 실제 hard token cap이 아님**. 각 레벨 비용은 **등급별 상한**이다. 사용자가 **사전 운영 예산 정책을 한 번 승인**했다면 이후 그 허용 범위의 신규 리뷰는 매 건 별도 비용 승인을 요구하지 않는 것을 목표로 한다. 단, 사전 정책은 아직 신규 승인을 받지 않았으므로 지금 자동으로 효력이 발생하지 않는다.

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

## 2.1 비판적 평가·개선 제안 (독립 리뷰 품질 기준, 2026-11-15 보강)
- **독립 리뷰는 결함 개수 경쟁이 아니다.** 최소 결함 수나 반드시 반대 의견을 내도록 요구하지 않는다. 실제 근거가 없으면 `CONFIRMED_FINDINGS=NONE` 또는 '확인된 결함 없음'으로 보고할 수 있다. 근거가 약한 추정은 확정 결함이나 BLOCKING으로 승격하지 않는다.
- **비판적 관점은 필수, 비판적 결론은 강제하지 않는다.** 입력으로 주어진 설계·구현·테스트의 핵심 가정, 놓친 반례, 단순화 가능성, 숨은 유지보수 비용, 보안·상태·호환성·복구 위험을 검토한다. 합리적인 설계면 그 판단 근거도 명시한다. 개발자의 주장·자체시험 PASS를 무비판적으로 재진술하지 않는다.
- **개선안은 증거와 비용을 함께 제시한다.** 유의미한 개선이 있다면 (A) 기존 구조를 최대한 재사용하는 최소 수정, (B) 구조적 대안(필요할 때만)을 비교한다. 장단점·도입 위험·회귀 범위·유지보수성·실현 난도를 적고, 과도한 리팩터링을 강요하지 않는다. 근거 없는 대안 채우기 금지.
- **확인된 결함과 개선 제안은 분리한다.** BLOCKING/MAJOR/MINOR는 재현 가능한 결함·실질 위험에 적용하고, 비차단 구조 개선과 향후 검증 제안은 별도 구획에서 우선순위·기대효과·검증 방법을 서술한다. 기존 코드/운영에 즉시 적용하거나 승인되지 않은 설계 변경을 진행하지 않는다.
- **독립성 표시:** 개발자 자체시험과 별도 독립 리뷰 요청·입력 revision·실행 결과·영수증을 구분한다. 같은 개발 세션의 자기 점검을 독립 검토라고 표기하지 않는다. 직접 확인하지 못한 부분은 `NOT_VERIFIED` 또는 `PARTIAL_SCOPE`로 표시한다.

### 레벨별 비판적 검토 깊이
| 등급 | 반드시 질문할 관점(승인된 입력·토큰 범위 안에서만) |
|---|---|
| R0 | 문서·매니페스트·링크의 모순, 설명이 전제하는 불명확한 가정. 코드/운영 안전성까지 확인했다고 주장하지 않음 |
| R1 | 변경 diff의 타당성, 놓친 반례와 회귀, 더 작은 수정으로 같은 효과를 달성할 여지 |
| R2 | 설계의 책임·경계·상태 전이·승인/신뢰 가정, 구조 단순화와 대안별 트레이드오프 |
| R3 | 통합 운용 가정, 장애·복구·롤백·확장성, 단기 보완 대 장기 아키텍처의 비용과 위험 |

### 신규 리뷰 요청에 넣을 간결한 평가 프롬프트 (기존 필드·정책 불변)
> 확인된 결함이 없으면 없다고 보고해. 결함을 일정 수 이상 찾아내도록 강제하지 않는다. 구현/설계의 핵심 가정과 반례를 독립적으로 검토하고, 타당한 결정은 근거를 제시해 인정해. 발견한 문제는 재현 근거와 심각도를 기록하고, 비차단 개선 기회는 별도로 분리해 최소 수정안과 필요 시 구조적 대안을 비용·위험·호환성 측면에서 비교해. 검증하지 못한 것은 명시해. 승인된 입력 범위·토큰/비용 한도를 넘기거나 추가 모델 호출을 실행하지 마.

**적용 경계:** 위 문구는 향후 **신규** 리뷰 REQUEST/프롬프트 작성 시 사용하는 품질 기준이다. 기존 `R0~R3`의 등급 매핑, `POLICY-STATIC-V1{,-LARGE,-XLARGE}` 비용 정책, 요청 스키마, 서명/READY·중복 방지·예산 게이트는 변경하지 않는다. 이미 고정된 `REQ-COWORK-AUTO-APPROVAL-V023-R2-20261115`의 입력·프롬프트·승인/실행은 소급 변경하지 않는다. 이 문서 변경만으로 Windows watcher/Claude runner의 실제 프롬프트가 자동 갱신되거나 유료 리뷰가 실행되지 않으며, 향후 운영 적용 여부는 별도 입력/호스트 증거로 확인한다.

## 3. 실제 호출 제어: 토큰 한계의 정직한 표현
Claude Code CLI 공식 `-p` 모드에는 `--max-budget-usd`, `--max-turns` 제어가 있으나 **해당 조합만으로 전체 호출 input/output token 총량의 절대 하드 캡이 성립한다고 선언하지 않는다**. 비용은 CLI의 **추정**이므로 실제 청구와 다를 수 있고 모델 응답 과정에서 임계치를 넘어갈 수 있음.
- **모델 호출 이전**: review manifest에서 대상 버전/고정 SHA·정확 파일/정확 diff/필요 테스트를 한정; local estimator 또는 실제 사용 가능한 토큰 계산기(외부 호출/비용이 생기지 않는 방법 우선)로 **예상 입력 토큰**을 추정해 레벨 목표 이상이면 더 압축/파일 선택. 계산법/오차를 영수증에 명시. 무관한 history·대형 문서·중복 배포본 투입 금지.
- **실행 중**: 호출 wrapper 또는 Claude runner가 지원하는 `--max-budget-usd`와 `--max-turns`를 적용. 단일 요청 `max_model_calls=1`, 별도 서브에이전트 추가 생성/자동 재시도 금지. CLI 비용 추정 상한 초과 가능성을 감안해 **정책 비용 한도보다 낮은 내부 stop threshold** (예: R1 $0.85, 조건·호스트 검증 뒤 조정) 적용을 우선 고려; 플랫폼 제공상 수치가 실제 결제의 완벽한 차단을 보장하는 것으로 주장 금지.
- **출력 제어**: 필요한 판정 결과(근거 위치·Severity·수용/보류·후속 재현)만 요청; 요청한 출력 목표를 프롬프트 계약에 기재. 실제 출력 토큰을 CLI 결과/usage로 측정해 보고하되 CLI print mode 전체 출력에 hard token cap이 **있는 것처럼 표기하지 않음**. SDK/API가 검증된 별도 출력 토큰 제한을 지원하더라도 검증 없이 자동 적용하지 않음.
- **실행 후**: `input_tokens`, `output_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`, `total_cost_usd`, `max_budget_usd`, `max_turns`, `selected_review_tier`, `target_sha256/commit`, `token_estimation_method`, `limit_reached`, `scope_partial`를 확보 가능한 만큼 영수증에 기록. unavailable 값을 0으로 채워 성공으로 표시하지 않음.
- 실제 CLI `--help`, 설치 버전, `RealReviewRunner` 인자 지원을 Windows에서 확인하고 **지원되지 않는 CLI 옵션을 임의로 통과시키지 말 것**. 기능 없으면 `BUDGET_ENFORCEMENT=PARTIAL`로 기록하고 출력 크기·입력 범위/승인 비용을 더 보수적으로 제한.

## 4. 자동 등급 선택·승급 방지
- 기본은 **R0 또는 R1**. 사용자 '구조 리뷰' 요청이 명백할 때 R2를 추천할 수 있으나 실제 유료 호출은 해당 레벨을 포괄하는 **유효한 사전 승인 또는 해당 건 명시 승인**이 필요.
- 범위를 초과하면 모델을 먼저 실행하지 말고 입력을 압축하거나 `BUDGET_SCOPE_TOO_LARGE`로 종료. 자동으로 비용/레벨 상승 금지.
- 동일 논리 리뷰 요청의 **중복 호출 0**, 상태 불명 `REVIEW_UNCERTAIN`에서 무승인 재시도 0. 재리뷰는 변경된 ZIP 해시·신규 명시적 요청에 한정.
- GitHub PRIVATE에는 허용된 CoWork 자체 코드/ZIP/manifest를, PUBLIC L1Work에는 이미 공개된 스킬 및 `handoffs/` 문서 링크만 일반 리뷰 입력으로 사용. 회사 L1 코드·고객자료·자격정보는 제외.

## 4.1 리뷰마다 반복 승인하지 않는 단일 사용자 기본 정책(제안)
- 사용자 요청 **한 번으로 작업별 리뷰 의도·대상·품질 등급을 함께 확정**한다. 단일 사용자 기준 사전 운영 정책에 대해서 사용자가 **한 번 명시 승인**하면 `approved_tiers`, `per_review_cost_cap`, `repo_allowlist`, `valid_until` 안에서 각 작업의 새 리뷰를 자동으로 실행할 수 있게 설계. GitHub 임의 게시만으로 사용자의 승인된 업무 지시를 위조하거나 무제한 유료 호출하는 경로를 만들지 않는다.
- 상시 승인된 등급이라도 **예산 확대·등급 자동 상승·기존 리뷰 실패 후 새 유료 재리뷰·다른 저장소/범위 변경**은 예외로 보류하여 추가 명시 승인받는다. 정책이 만료되거나 불명확하면 새 모델 호출 0.
- **현재의 사용자 승인 사실**: `REV-COWORK-V0214-20261114`, R1 / `POLICY-STATIC-V1`, 최대 **$1**, 1회, 동일 Windows PC 서명키 A안은 이미 승인됨. **한 번 더 물을 필요 없음**. 미래의 R0/R1/R2/R3 전체에 대한 **상시 예산 승인은 아직 주어지지 않음**.
- 운영자가 유료 사용을 직접 승인한 명시 범위는 해당 단계에서 실행하되 실제 Windows host 토큰·운영 계정·LIVE 변경은 승인된 것으로 확대하지 않는다.

## 5. 구현·배포 단계
- **현재 v0.2.14 ZIP에 위 4개 등급의 실행 제어가 모두 구현되어 있다고 가정하지 않음.** 기존 $1/$3/$6 정책은 선행 계약상 존재, 신규 R0 및 토큰 추적·입력 사전 예산 검사는 추가 구현/검증 후보.
- 이번 A안 독립 리뷰 1회는 **v0.2.14 아티팩트 변경 없이 R1**로 실시, prompt/manifest 범위 제한과 기존 비용 게이트 사용. 향후 reviewer tier 정책을 watcher 제품에 코딩한다면 신규 버전으로 별도 발행·관련 시험·독립 리뷰/배포 게이트를 거침. 리뷰 중 후보를 바꾸고 옛 아티팩트 PASS를 소급하지 않음.
- 정식 등급 분류·비용·사용량 지표가 실제 Windows runner에 연동되었는지는 **host test PASS**로 따로 입증; 본 문서 게시만으로 활성화 완료가 아님.

References: `collab/ops/CONTRACTS/REVIEW_TRANSPORT_V1.md`, `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_V0214_PREFLIGHT_DISPOSITION_AND_APPROVAL_GATE_r0001_20261114.md`.
