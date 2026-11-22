# CoWork REVIEW REQUEST/PIN/ZIP 게시 전 필수 정합성 검증 V1

## 현행 결정 r0009 — 금액을 리뷰 자격에 사용하지 않음 (2026-11-23 KST)

- 사용자 비용 제한 제거 지시를 수용. 건당/일/월 비용, 고정USD3 일치, legacy 가격 인수/필드의 존재·형식이 신규 독립 리뷰 접수·승인 자격을 결정하지 않는다. 비용 제거 의사에 대한 같은 승인을 반복 요청하지 않는다. 실제 운영 적용 상태는 [자동 승인 CURRENT](../../projects/COWORK-AUTO-APPROVAL-20261115-001/CURRENT.md)에서 조회한다.
- 접수기 `required_budget`와 CLI `--required-budget-usd`는 deprecated/ignored. 금액을 파싱·비교하거나 넘겼다는 이유만으로 거부하지 않음. legacy 의도 표기도 가격 비교 없이 정책 identity/원본 호환만 확인. 현행 독립 리뷰 기본은 POLICY-STATIC-V1.
- 비용 사후 사용량/청구 기록은 보존. 보호된 실행 권한·서명·만료·scope·REQUEST/ZIP/PIN SHA·CRC·READY 마지막·중복/UNCERTAIN 봉인은 유지. GitHub 본문 가격/승인 주장은 권한 근거가 아니다.
- 운영 코드·설치본 확인 없이 소스 수정을 운영 해제 완료로 보고하지 않는다. 비용 제거 요청이 후보 전체 LIVE 설치·DB 이행·키/위임 확대·최종 컷오버 승인은 아니다. 기존 frozen 요청/서명/READY/영수증을 소급 변경하거나 재실행하지 않는다.
- 아래 r0008/r0007의 금액 승인 대기·가격 인수 거부·USD3 비교 지시는 이 결정으로 대체. 과거 실행 결과는 해당 시점의 이력으로 보존.
- 구현·직접 시험: [비용 제한 제거 결과](../../projects/COWORK-AUTO-APPROVAL-20261115-001/GPT_COST_GATE_REMOVAL_IMPLEMENTATION_RESULT_r0001_20261123_KST.md).

---


## 결정 r0008 — 요청 ID 단위 단일 실행 / 비용 상한 제거 후속 구현 (2026-11-22 KST)

- 사용자가 `--max-budget-usd` 제거에 동의하고, 독립 리뷰의 재실행 위험은 **요청 ID별 1회 디스패치, 원자적 중복 방지, 실행 불확실 시 재디스패치 금지**로 통제하도록 결정. `max_calls=1`은 watcher에서 Claude CLI 작업을 1회 넘게 시작하지 않는 보호장치이며 단일 실행 안의 모델 턴 수/청구 금액 상한으로 오해하지 않는다.
- **전환 목표(아직 운영 사실 아님):** 신규 독립 리뷰의 비용 기반 실행 허가·CLI 예산 인자를 제거하되, 신뢰되는 사용자 의도·실제 실행 권한, 원본 SHA/PIN/ZIP, 보호 서명, READY 마지막 게시, 과거 이력/중복·UNCERTAIN 봉인을 보존. 적법한 승인 없는 GitHub REQUEST 게시만으로 서명·모델 호출을 시작하지 않는다.
- **상태:** Windows v0.2.30 격리 후보는 `PER_REQUEST_COST` 및 수동 `--max-usd` 금액 일치 부분만 제거, CLI `--max-budget-usd`는 **여전히 후보에 남음**. Windows LIVE는 마지막 호스트 보고상 v0.2.29, 변경 미적용. 실제 Windows 변경·무모델 호출 회귀·운영 적용은 **NOT_RUN**. 위임 skill SCOPE 개선은 인증·권한 검증 설계를 전제로 별도 시험/승인.
- **구현·시험 지시:** [동일 Work의 r0001 인계](../../projects/COWORK-AUTO-APPROVAL-20261115-001/INDEPENDENT_REVIEW_IDEMPOTENCY_COST_REMOVAL_HANDOFF_r0001_20261122_KST.md). 기존 frozen REQUEST/승인/영수증 소급 수정·재모델 호출 금지. LIVE 변경은 별도 승인·백업·검증.
- 기존 r0007/r0006의 과거 구현 설명은 당시 상태 이력이며, 전환 목표가 설치된 것으로 해석하지 않는다.

---

## 현행 규칙 r0007 — 독립 리뷰만, 게시자 가격·스킬 선검사 제거 (2026-11-22 KST)

- 상위 최신 사용자 결정. **독립 리뷰 단일 유형**을 사용하며 GPT REQUEST 게시자는 비용 상한·가격 정책 선택·스킬별 위임 목록을 검증하지 않는다. `check_request_for_publication(intent="independent")` 기본값; `required_budget`를 넘기는 신규 독립 요청은 거부. `submit_review_request.py`는 실제 가격 설정을 읽지 않으며 AUTO 인자는 **실행 권한이 아닌 요청 메타**다.
- 출판 과정에서 남는 게이트: USER 명시 독립 리뷰 요청, Work/입력 고정, 기존 결과/READY/영수증/UNCERTAIN 중복 확인, REQUEST schema, ZIP 크기/SHA/CRC/경로, 정적 `run_policy_ref` 호환, REQUEST+ZIP Commit A → PIN Commit B → 원격 바이트 검증.
- **아직 Windows LIVE는 변경하지 않음**: 기존 호스트에서는 스킬별 위임·USD3 비용·승인/서명·READY·중복·실행 방어가 계속 동작하므로 GPT 출판 개선만으로 `AUTO_NOT_ELIGIBLE:SCOPE`가 해결되었다고 주장하지 않는다. Windows 가격·allowlist 제거는 별도 설치본 수정/격리 회귀/유효 승인 절차가 필요한 후속 구현. 공개 저장소의 REQUEST를 임의 사용자가 실행하게 만드는 무권한 자동 승인 대체는 불가.
- [실제 코드 변경 및 Windows 전환 경계](../../projects/COWORK-AUTO-APPROVAL-20261115-001/GPT_INDEPENDENT_REVIEW_COST_GATE_SIMPLIFICATION_RESULT_r0001_20261122_KST.md). 아래 r0006의 `unified USD3` 및 게시자 AUTO skill 검사는 과거 규칙으로 대체되지만, LIVE 보호 검사에 대한 기술은 **호스트가 바뀔 때까지 현재 사실**로 유지한다.

---

## 현행 규칙 r0006 — GPT REQUEST 출판과 Windows 실행 승인 분리 (2026-11-22 KST)

**적용 우선순위:** Windows Claude Code 독립 리뷰 R1 `REQ-COWORK-REVIEW-ARCH-DESIGN-R1-20261122`과 GPT 판정 `ACCEPT_WITH_CORRECTIONS__OPTION_B` 반영. **이 절이 아래 r0005 및 이전 2026-11-17 'Windows LIVE 선검사 필수' 문구보다 우선**. 기존 완료·고정 요청을 소급 수정하거나 READY를 재큐잉하지 않는다.

- **GPT 단계 ②**: 동일 대화의 마지막 확정 Work·설계/구현 입력 revision·실제 ZIP/문서·이미 존재하는 REQUEST/READY/결과·영수증/UNCERTAIN을 직접 확인한다. 사용자가 **“리뷰요청해줘”**라고 명시한 경우에만 제출. 초안·handoff만 만들고 종료하지 않는다.
- **GPT 단계 ③**: `collab/ops/review_request_gate.py:check_request_for_publication`으로 schema, `unified` 정적 `POLICY-STATIC-V1` 및 USD3 표준, ZIP 크기/SHA-256/CRC/경로/중복 필드 검사. 실제 LIVE config 조회 없이 **Commit A(REQUEST+정확한 ZIP 같은 트리) → SHA/바이트 원격 확인 → Commit B(SOURCE_PIN이 A를 지시, repo_id JSON 문자열) → PIN/REQUEST/ZIP 원격 재조회**. `submit_review_request.py --publish` 또는 동등 게이트를 충족한 GitHub connector/API 두 커밋 게시. 외부 호스트 설정이 없어서 차단하지 않는다.
- `submit_review_request.py --live-config`는 **선택적 참고 검사**이며 PASS/FAIL이 GitHub 접수 권한·모델 실행 권한을 부여하거나 REQUEST 출판을 차단하지 않는다. Windows `review_request_gate.py select/check`는 로컬 정책 진단용으로 보존. 과거 packaged `tools/review_request_gate.py`와 현재 GPT `collab/ops/review_request_gate.py`는 버전이 달라 운영 ZIP 원본을 직접 동일하게 고치지 않는다. GPT 게시기 기준 정본은 `collab/ops/`, 차기 watcher 후보 packaging 시 gate 의미/테스트 정합성을 확인한다.
- **Windows 운영 보호 게이트 불변**: validator, 실제 LIVE policy, 위임 allowlist/만료/enabled_at·단일 USD3 한도, source pin 고정, 공식 서명·READY 마지막, 중복·UNCERTAIN 및 비용 검증 통과 시에만 Claude 모델 호출. 공개 GitHub REQUEST·GPT 주장·문서 게시만으로 AUTO signer 권한을 만들지 않는다. 잘못된 정책/비용/범위는 REQUEST를 보존하되 READY/모델 호출 0.
- **완료 판정 분리**: `SUBMITTED_AWAITING_PROTECTED_SIGNER` = Commit A/B 및 원격 검증 완료일 뿐 승인/READY 아님. `READY_POSTED`와 `REVIEW_RESULT/RECEIPT_VERIFIED`는 각각 실제 근거로 확인. 원격 게시 중단·충돌 또는 미확인은 자동 재게시 금지·부분 상태 정산. 사용자 명시 리뷰 지시 없이 문서 변경/Actions로 새 유료 요청 생성 금지.
- **F1/F2 현행 근거 구분**: Windows v0.2.29 LIVE `POLICY-STATIC-V1=USD3`는 11/20 호스트 보고 및 이번 정식 리뷰 결과 체인으로 확인. v0.2.29 ZIP 내부 `config/reviewer.config.example.json`의 USD1은 이전 예제이지 현행 운영값이 아님. `collab/ops/tests/test_review_request_gate.py`에는 unified $3 및 구 값 거부 테스트가 존재하므로 시험 없었다는 주장은 부정확. 두 코드 사본 드리프트는 차기 packager 정합성 과제이며 운영 ZIP 불변.

---

- 제정: 2026-11-21 KST
- 직접 원인: `REQ-L1-KNOWLEDGE-PREFLIGHT-V020-R1-20261121`의 SOURCE_PIN이 **ZIP만 있는 커밋**을 참조했고, 해당 커밋에 REQUEST가 없어서 Windows watcher가 `COMMIT_UNREADABLE / WAIT_INPUT`으로 정지.
- 추가 원인: `skill_id=knowledge_analysis_preflight`가 실제 자동 위임 허용 집합에 없음. 자동 signer가 허용되지 않는 요청을 수동 승인 없이 실행할 수 없음.
- 효력: **신규 리뷰 요청을 게시·서명·READY 처리하는 GPT/Windows Claude Code의 절차 계약**. 이 MD와 Python helper의 게시만으로 Windows 운영 watcher의 실제 preflight 로더/호출 경로가 변경되는 것은 아님. 운영 자동 연동 여부는 별도 G0 검증.

## GPT 책임 ② 대상 확정 → ③ 정식 제출, 완료 게이트 (r0005 / 2026-11-22 KST)

**실제 사용 명령:** 진행 중인 GPT 설계 대화창에서 **“리뷰요청해줘”**, **“리뷰체계 최신버전 확인후 다시 리뷰요청해줘”** = 그 창의 마지막 확정 설계/구현물을 **Windows Claude Code 정식 독립 리뷰로 접수하라는 실행 지시**. 설명·미리보기·입력 후보만 요구한 게 아니다. 이 문구를 인용·정책 논의 중 언급한 경우는 트리거가 아니다. `AGENTS.md`와 본 계약을 해당 창에서 최신 readback 후 바로 적용하며 사용자가 Work ID·파일명·긴 프롬프트를 반복 입력하지 않게 한다.

**② 대상 확정 — GPT 직접 검증 필수**

1. 현재 창에서 최근 사용자 수정/결정·확정 범위·최신 설계/구현물을 채택하고, 관련 기존 Work의 CURRENT 최상단·기존 설계·구현·시험·열린 메모를 대조한다. 다른 창의 Work를 추측·혼합하지 않는다. 이전에 사용자가 생략한 리뷰와 새로운 명시 요청은 구분한다.
2. 동일 Work의 현재 원본 repo/branch/commit/path·ZIP 정확한 바이트/size/SHA-256·리뷰 목적·포함/제외·근거/시험을 **실물 조회**해 고정한다. 과거 정적 인계/후보가 최신과 다르면 최신 확정본 기준으로만 요청한다. README·MD 이름이나 ZIP 후보의 주장만으로 고정 PASS를 만들지 않는다.
3. 기존 `collab/requests/<RID>`, `collab/reviews/<RID>`, `collab/receipts/<RID>`, 승인/서명/READY/불확실 이력과 remote HEAD를 먼저 조회한다. 기존 유효한 REQUEST/READY/영수증이 있으면 신규 요청을 만들지 않고 진행 상태를 회수하며, 확인되지 않은 재시도/재서명을 금지한다. 이전에 비트리거 초안만 게시된 경우 해당 실제 원본을 재검증해 재사용하되 새 Work·ZIP·RID를 불필요하게 생성하지 않는다.

**③ 정식 제출 — GPT의 완료 판단 필수**

4. 요청 형식·실제 ZIP 구조/CRC/경로 및 SHA·크기·Git 원본과 정적 정책 참조/요청 상한을 사전검사한다. Windows LIVE 정책 적합성은 보호 signer/READY 단계에서 별도 확인한다. 사용할 실제 제출 API/CLI·권한을 검증한다. 현행 `review_request_gate.py`, `submit_review_request.py`, `review_pin_preflight.py`를 **REUSE**한다. Base64 ZIP·REQUEST 초안이 이미 게시된 경우 `review_staged_submission.py` 경로를 재사용하되 이를 요청 접수로 오인하지 않는다.
5. **조건을 충족하고 실제 게시 권한이 있는 경우** GitHub `main`에 Commit A: 정확한 `REQUEST.md` 및 패키지 ZIP **같은 트리** → 원격 바이트·size/SHA/요청 필드 검증 → Commit B: `SOURCE_PIN.json`이 A를 정확히 지시하고 `repo_id`가 **문자열** → 검증기로 PIN 검사 및 원격 readback을 수행한다. 해당 단계에 필요한 정책/보호 권한 미검증이면 **실행하지 않고 정확한 경계에서 fail-closed**한다. GitHub API 직접 게시도 같은 게이트를 만족해야 하며, GPT가 읽을 수 없다는 이유로 Windows 보호 정책을 정적 GitHub 문서로 대신할 수 없다.
6. 결과 **`SUBMITTED_AWAITING_PROTECTED_SIGNER`를 말할 수 있는 유일한 근거**는 실제 `collab/requests/<RID>/REQUEST.md` + `SOURCE_PIN.json` 원격 존재, A 고정 ZIP 포함·정합성/바이트 SHA·두 커밋 검증 PASS이다. `REQUEST DRAFT` front matter의 `state: SUBMITTED`, `collab/projects/` 초안·Base64 ZIP·CURRENT/TRACKER 게시, Windows 원샷 지시서만으로는 절대로 `REQUEST_POSTED`/정식 리뷰 접수 PASS로 판정하지 않는다.
7. GitHub 제출 도구·원본·Git commit A/B 검증·원격 쓰기 권한이 **불가능한 경우**, GPT는 `FORMAL_REQUEST=NOT_POSTED` 또는 실제 부분 상태(예: `POST_CONFLICT`/`UNCERTAIN`)와 막힌 **정확한 단계**만 보고한다. ②③ 가능한 검증은 마친 후 차단을 짧게 보고하며, 새로운 리레이/daemon/스킬/워크플로 발명이나 반복적인 인계서 게시를 후속 기본 작업으로 확장하지 않는다. 이미 승인된 범위의 실행은 중간마다 재승인 질문 없이 진행하되 유료 리뷰·서명·READY·운영 변경은 기존 실제 보호 정책과 승인 범위를 유지한다.

**GPT의 사용자 보고:** `Work ID / 리뷰 대상·원본 revision / 검증된 요청 ID / FORMAL_REQUEST=SUBMITTED|NOT_POSTED|BLOCKED / GitHub 정식 REQUEST·PIN 실제 링크·커밋(있을 때만) / 실제 차단 한 가지` 순서. ②③의 검증/실제 GitHub 게시 여부와 ④ Windows 보호 signer/READY 및 Claude 리뷰 완료는 서로 별개로 기록한다. 동일 창에서 정식 리뷰 지시를 받고 **단순 일반 검토로 되돌리지 않는다**. 기존 이력·불확실 재실행 금지를 그대로 유지한다.

## 진행 중인 설계 창의 단축 명령 (r0003 / 2026-11-21 KST)

- 사용자가 **현재 설계·개발을 이어 온 동일 대화창**에서 단독으로 **“리뷰요청해줘”** 또는 “리뷰 요청해줘”라고 실행 지시하면 **바로 앞까지 확정·갱신한 해당 작업의 정식 Windows Claude Code 독립 리뷰 요청**으로 해석한다. “정식”, Work ID, 스킬명, 파일명, 긴 프롬프트를 재입력하도록 요구하지 않는다. “○○ 설계하고 정식 리뷰까지 진행해줘”는 설계+리뷰 일괄 요청으로 동일 계약을 적용한다. 이 문구들을 *예시·인용·규칙 논의*로 언급한 경우에는 실행 지시로 간주하지 않는다. 단순한 “리뷰해줘”·“검토해줘”는 기존 설계의 일반 검토 요청일 수 있으므로 자동으로 유료 정식 리뷰 접수라고 확대 해석하지 않는다.
- **대상 결정 우선순위:** (1) 현재 창에서 사용자가 마지막으로 승인·수정·확정한 설계/구현 범위와 바로 연결된 Work 및 artifact/revision, (2) 같은 Work의 최신 CURRENT·열린 메모·후보/시험 증거, (3) GitHub main 실제 원격 HEAD·REQUEST·RESULT·RECEIPT·승인/중복 기록 순으로 대조한다. 대화 내 이미 확정한 범위를 사용자에게 반복 질문하지 않는다. 관련 Work가 여러 개면 현재 대화의 **가장 최근 작업 대상**을 선택하고 무관한 다른 Work는 포함하지 않는다. 유일한 대상 또는 고정 원본이 실증 불가능할 때만 해당 차단 사유를 명시하고 임의 제출하지 않는다.
- **리뷰 입력 준비:** 현재 창의 최신 설계·변경 내역을 실제 GitHub 정본/고정 source revision과 일치시키고 리뷰 범위·완료 기준·증거를 준비한다. 설계 리뷰라면 검토할 설계 문서를, 스킬 코드 리뷰라면 실제 코드를 포함한 유효 패키지 ZIP을 고정한다. 기존 해당 Work의 승인된 후보·설계·시험/패키지를 재사용하고, 제출 규칙의 필수 입력 REQUEST+ZIP·정책 게이트를 충족할 때만 정식 제출한다. 무관한 확대 구현이나 근거 없는 ZIP·자료를 자동 생성하지 않는다.
- **실행 단계:** 신규 요청·기존 요청·완료/불확실 이력을 먼저 대조해 중복을 차단한다 → 현재 Windows 보호 위임의 skill_id·예산·만료에 따라 AUTO/MANUAL을 분류한다 → 단일 `submit_review_request.py`의 사전검사 PASS 후 허용된 범위에서 Commit A(REQUEST+ZIP), Commit B(SOURCE_PIN) 원격 readback까지 수행한다 → 공식 signer의 승인/서명·READY 마지막 게시 여부를 별도 확인한다 → 실제 watcher·Claude 결과·영수증은 확인된 경우에만 완료 판정한다. 기존 유효 승인 내 처리는 반복 동의 요구 없이 진행하되 새 유료 호출·운영 변경·보호 위임 확장 등은 승인 게이트를 그대로 유지한다.
- **결과 표현:** `PREPUBLICATION_PASS_NOT_SUBMITTED`, `SUBMITTED_AWAITING_PROTECTED_SIGNER`, `BLOCKED`, `READY`, `REVIEW_RESULT/RECEIPT_VERIFIED`를 실증대로 구분한다. 현재 창의 단축 지시는 **새 자동 실행 권한이나 무조건 승인**을 생성하지 않는다. Telegram 리뷰 알림은 기존 Windows notifier가 실제 이벤트에 따라 발송하며, GitHub 문서 게시만으로 알림·자동 GPT 판정을 약속하지 않는다.
- **효력 경계:** GPT와 Windows Claude Code가 이 계약을 읽고 적용할 때의 **자연어 의도 해석/워크플로 진입 규칙**이다. 모든 새 ChatGPT 창의 무조건적 자동 문서 로딩, Windows watcher 자동 수정, 새로운 trigger/parser 설치, 호스트 E2E 성공을 뜻하지 않는다.

## GitHub 보관 후보의 Windows 접수 보조 (r0004 / 2026-11-22)

- GitHub `collab/projects/<WORK_ID>/` 하위에 **REQUEST 비실행 초안과 `.zip.base64` 후보**가 이미 있고 Windows 보호 환경에서 실제 제출기를 실행해야 하는 경우, [보조 CLI](../../ops/review_staged_submission.py)를 사용해 커밋된 원본을 동일 바이트로 복원한 뒤 **기존** `submit_review_request.py`를 재사용한다. 별도 신규 watcher·READY/서명 엔진을 만들지 않는다.
- **기본 동작은 dry-run**: `--work-id`, `--draft-path`, `--candidate-path`, `--live-config`를 제공하고 `--publish` 없이 먼저 실행. 클린 원격 main·Git blob 타입·Work·ZIP SHA/크기와 Windows LIVE 정책을 검사한다. 이후 원격 중복·보호 signer/승인 범위를 실증했을 때에만 같은 명령에 `--publish`를 추가해 Commit A/B를 제출한다. 정상 제출은 `SUBMITTED_AWAITING_PROTECTED_SIGNER`이며 승인/READY가 아니다.
- Windows watcher가 이 보조 CLI를 **자동 실행하도록 하는 기존 호스트 hook은 NOT_APPLIED/NOT_VERIFIED**. 실제 설치본에서 승인된 기존 watcher run_cycle로 연결할 수 있는지 G0 검사 후, 별도 유효 운영 승인·백업·SHADOW·중복 차단을 거쳐 적용한다. 이 절의 문서/코드 게시만으로 새 창의 리뷰 1회 E2E가 자동 완료되지는 않는다. [실행 경계·해당 Work](../../projects/COWORK-AUTO-APPROVAL-20261115-001/REVIEW_INTAKE_ONE_SHOT_HOST_INTEGRATION_r0001_20261122_KST.md).

## 자연어 정식 리뷰의 표준 제출 명령 (r0002 / 2026-11-21)

**신규 요청 기본 경로:** Windows LIVE config 접근 없이 `collab/ops/submit_review_request.py`를 사용한다. 이 제출기는 `review_request_gate.check_request_for_publication`, `source_pin.dumps_source_pin`, `review_pin_preflight.inspect`를 **연속 호출**하고, 요청 생성에 필요한 Commit A/B를 안전하게 `git push`한다. `--publish`가 없으면 원격/로컬에 쓰지 않는 드라이런이다. 안전성 위해 클린 `main`·신뢰 `origin`·원격 최신 SHA·새 REQUEST ID를 강제한다. 인증 토큰·보호 서명·READY는 절대 생성하지 않는다.

예시(Windows, 실제 설치 LIVE 설정 경로는 호스트 확인 후 지정):

```powershell
python collab/ops/submit_review_request.py --repo-root . --request-draft <OUTSIDE_REPO>\\REQUEST.md --package <OUTSIDE_REPO>\\skill.zip
# 모든 게이트 검증 성공한 경우에만, 동일 인자로 --publish 추가
python collab/ops/submit_review_request.py --repo-root . --request-draft <OUTSIDE_REPO>\\REQUEST.md --package <OUTSIDE_REPO>\\skill.zip --publish
```

### 요청 대상과 보호 위임 범위의 분리 (2026-11-21 보완)

- 제출기의 기본값은 `--approval-route manual`: 이는 **보호 서명자 수동 승인 필요**를 표시할 뿐, 승인·서명·READY가 아님. 대상 스킬이 자동 위임 밖에 있어도 이 경로로 REQUEST/PIN *후보* 게시 가능하며, 유효한 일회성 수동 승인 전 리뷰는 실행하지 않는다.
- 자동 처리를 기대할 때는 **실제 Windows 보호 signer의 현재 로드 위임에서 읽은** 허용 스킬 각각을 `--delegated-skill <skill-id>`로 전달하고 `--approval-route auto`를 지정. 누락은 `AUTO_DELEGATION_SCOPE_NOT_SUPPLIED`, 미허용은 `AUTO_NOT_ELIGIBLE_SCOPE`로 **Commit A 이전 차단**. 프로그램에 허용 목록을 임의 입력했다고 해서 signer 권한이 증명되는 것은 아니다. 실행 시 signer가 원본 위임/만료/repo_id/비용/승인 범위를 다시 검증해야 한다.
- 예시: `knowledge_analysis_preflight`는 2026-11-21 호스트 보고 허용 목록에 없어 R2 자동 처리가 불가능. `skill_id`를 `l1-knowledge-updater`로 위장하거나 scope를 임의 추가하지 않는다. **R2는 이미 게시된 신규 요청이므로 제출기를 재호출하거나 PIN/READY를 다시 만들지 않는다.** R2 유효한 보호 수동 1회 승인은 사용자/기존 위임 계약으로 별도 확인할 때만 진행한다.
- 신규 CLI 게이트는 게시자 측 예방책이며 Windows signer 또는 watcher 설치 변경이 아님. **CLI의 manual 선택은 REQUEST의 서명 정책을 바꾸지 않으며**, signer가 다른 유효 자동 위임을 검증할 경우 자동 처리 가능성 자체를 강제 차단하는 표시도 아니다. 대상이 자동 범위 밖이면 실제 수동 권한 검사가 필요하다. PIN 검증은 ZIP basename이 아닌 `collab/packages/<filename>` 전체 정규 경로를 검사한다. 임의 GitHub API 직접 게시를 막는 호스트·저장소 수준 강제는 별도 설치 검증 필요. 기존의 자동 위임 allowlist는 유지.

**성공 판정 경계:** `PREPUBLICATION_PASS_NOT_SUBMITTED` = 미게시, `SUBMITTED_AWAITING_PROTECTED_SIGNER` = REQUEST+ZIP·PIN 원격 게시/검증까지, 정식 실행/서명 아님. 프로그램이 `FORMAL_REVIEW_SUBMISSION_BLOCKED`를 출력하면 명시적으로 실패, **자동 재시도 금지**, 원격 Commit·보호 signer·DB·중복/UNCERTAIN 판정 후 새 revision을 선택. 자동 위임 허용 여부는 게시기의 `approval_mode=manual` 형식 무결성 검사로 입증되는 것이 아니며 **Windows 공식 보호 signer가 별도 확인**한다.

**중요 제한:** 신규 보조 코드는 GitHub 저장소에 게시됐지만 Windows PC에서 실행/설치 확인 전이다. 단일 명령을 우회한 GitHub API 직접 게시·다른 GPT/Agent에 대해 저장소 수준 강제 브랜치 보호를 활성화한 것은 아니다. 실제 운영 signer 연결/강제 status check는 운영 변경 승인과 실측 후에만 PASS로 판정한다. 기존 R1/R2의 서명·READY·실행 상태는 그대로 보존한다.

## 예방 조치와 담당

| 항목 | 필수 행위 | PASS 기준 | FAIL/불확실 |
|---|---|---|---|
| 0. 시작 전 승인 분류 | 대상 skill_id, 실제 로드된 delegation scope, 비용 정책·만료 확인 | AUTO 허용 여부 또는 MANUAL 한정 분류 | 자동 전환/스킬 명의 우회 금지 |
| 1. 고정 패키지 | 안전한 ZIP의 CRC/경로/파일 SHA·크기 검증 | exact package sha256, bytes, Git blob | 게시 중지 |
| 2. Commit A | **같은 commit tree**에 정확한 REQUEST.md와 패키지 ZIP이 존재하도록 게시 | A에서 REQUEST/ZIP 둘 다 READBACK, REQUEST 실제 바이트 고정 | PIN 만들지 말 것 |
| 3. SOURCE_PIN | **A를 commit으로 지정**하고 repo_id를 **문자열**로 직렬화 | `source_pin.py check` / main readback | READY·서명 금지 |
| 4. Commit B와 READBACK | PIN은 뒤 커밋 B에 게시. 확인된 최신 main과 **PIN이 가리킨 A**를 비교 | A의 REQUEST와 B/current REQUEST 동일 바이트, ZIP SHA/크기 일치 | `COMMIT_UNREADABLE` / `REQUEST_BYTES_CHANGED` 등 BLOCK |
| 5. 승인 | AUTO=실제 로드 scope 적합 여부 / MANUAL=정식 보호 signer 자격·예산·사용자 범위 | signer의 실제 APPROVAL 검증 | 사용자 발화/MD만으로 서명 PASS 불가 |
| 6. READY | 유효 서명·중복/UNCERTAIN·정책 검사 후 **맨 마지막 새 파일로** 게시 | watcher가 1회 처리/결과+영수증 | fail-closed, 모델 0 |
| 7. 사후 | 결과·영수증·비용·모델 호출·중복 원격 대조 | GPT 판정 후 승인된 배포 | 미검증은 NOT_RUN |

## 읽기 전용 개발/현장 검증 도구

- 코드: `collab/ops/review_pin_preflight.py`
- 회귀: `collab/ops/tests/test_review_pin_preflight.py` (합성 git 저장소 15건 직접 PASS; R1 잘못된 commit/REQUEST 변조/ZIP 변경/숫자 repo_id/미허용 자동 skill/READY 재큐잉 등 포함)
- Python 표준 라이브러리 + Git + 기존 `collab/ops/source_pin.py`; **네트워크/쓰기/승인/서명/READY/LLM 호출 없음**.
- **실행 전:** 로컬 Git 체크아웃에 최신 원격 main commit과 참조하는 A commit을 `git fetch`하여 확보. `--main-commit`에 **실제 원격 main에서 별도 조회·검증한 전체 SHA**를 입력. helper는 오프라인 검증이므로 로컬 HEAD가 원격 최신인지 스스로 입증하지 못함.

예시 (R2, 한정 MANUAL 승인 분류 — 명령은 읽기 전용):

```bash
python collab/ops/review_pin_preflight.py \
  --repo-root . \
  --main-commit <LIVE_REMOTE_MAIN_40HEX_SHA> \
  --request-id REQ-L1-KNOWLEDGE-PREFLIGHT-V020-R2-20261121 \
  --package-repo-path collab/packages/knowledge_analysis_preflight_v0_2_0_1121_REVIEW_INPUT.zip \
  --expected-repo-id 1451933830 \
  --approval-mode manual
```

- `status=PASS_PINNED_INPUTS_ONLY`은 **커밋·REQUEST·ZIP 바이트 정합성만 PASS**를 뜻함. `signer_authority=NOT_VERIFIED`, `ready_or_model_calls=0`은 의도된 보호 결과.
- 자동 승인은 반드시 **현장 보호 위임의 실 로드 allowlist**를 `--delegated-skill`로 전달하여 `--approval-mode auto`로 검사. 공백 allowlist나 skill 미허용은 BLOCK. 임의 allowlist 전달은 정식 signer 검증을 대체할 수 없음.
- EXIT 2/`REVIEW_PIN_PREFLIGHT_BLOCKED`이면 서명/READY/모델 호출 0. 기존 R1 또는 이미 서명·READY·결과가 있는 요청은 **새로 처리하지 말고 처리키·DB·영수증 상태를 재조회**. 실제 실패시 재실행하지 않음.
- 저장소 병합·branch SHA·원격 readback과 **Windows 운영 보호 signer, 실제 승인·정책·비용·중복 검증은 별도**다.

## 운영 반영 방법

- GPT/Claude 요청 게시자: **신규 요청마다 Commit A 검증·Commit B preflight를 필수**로 한다. 계열 작업의 기존 R1 실패 재발 방지.
- Windows signer/watcher: 다음 승인된 운영 변경 시 **실제 signer 직전의 필수 호출 게이트**로 연결하고, 원격/DB 상태와 일치하는지 SHADOW·실제 테스트로 검증. 현재 LIVE 설치·예약 작업·키·위임·DB·정책은 변경하지 않음.
- 이전 잘못된 요청을 조용히 고쳐 READY 처리하는 대신 새 ID/revision을 만들고 구 이력은 보존.

## 관련 Work

- `collab/projects/L1-WORKSPACE-RAG-20261111-001/CURRENT.md`
- `collab/projects/L1-WORKSPACE-RAG-20261111-001/KNOWLEDGE_PREFLIGHT_R1_PIN_FAILURE_R2_TRANSPORT_CORRECTION_r0001_20261121_KST.md`
- R2: `collab/requests/REQ-L1-KNOWLEDGE-PREFLIGHT-V020-R2-20261121/REQUEST.md` 및 `SOURCE_PIN.json`
