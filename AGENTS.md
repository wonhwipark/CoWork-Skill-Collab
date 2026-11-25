# CoWork 작업 시작 지침

이 저장소의 새 작업은 다음 순서로 진행한다.

1. [공통 맥락 브리프](collab/CONTEXT_BRIEF.md)를 먼저 읽어 협업 운용·L1 지식·관리 스킬의 공통 방향을 파악한다.
2. 브리프에서 요청 목적에 맞는 프로젝트를 고른 뒤 해당 `CURRENT.md`의 현재 요약·열린 메모·최신 결과/영수증을 실제 조회한다. Work ID뿐 아니라 그 안의 설계·구현·시험 등 이어갈 작업 흐름도 확인한다. 최신 조회에 실패하면 마지막 확인 시점과 미확인을 표시하고 과거 상태로 실행 여부를 확정하지 않는다.
3. 브리프에서 기존 스킬 후보를 선택하고 필요한 상세 I/O는 `collab/knowledge/SKILL_CAPABILITY_CATALOG.md`와 해당 스킬 원문만 확인한다. 사용자에게 스킬명을 다시 묻거나 18개 감사를 반복하지 않는다.
4. 실제 작업에 적용되는 `collab/START_HERE.md`의 계약을 필요한 범위에서 확인하고 REUSE / CONNECT / 입증된 최소 EXTEND / DEFER를 판단한다. 이미 읽은 브리프를 링크 때문에 반복 조회하지 않는다. 정확한 절차는 `collab/ops/CONTRACTS/SKILL_DISCOVERY_AND_REUSE_V1.md`를 따른다.
5. 작업 결과·피드백 원문은 해당 결과/결정/notes에 보존하고, 현재 상태·근거 링크·미해결·승인 범위·다음 한 행동은 해당 CURRENT에 갱신한다. 보완은 같은 목적의 Work와 작업 흐름을 이어간다. 기존 TRACKER는 필요한 현행 필드만 맞추고 별도 상태 정본으로 삼지 않는다.
6. 공통 브리프는 역할·정본 위치·요청별 경로가 바뀔 때, 카탈로그는 스킬 책임·입출력·연결 계약이 바뀔 때만 갱신한다. 일반 진행·버전·리뷰 상태를 브리프에 복사하지 않는다. 작업한 GPT/Agent가 CoWork main 게시와 원격 재조회까지 확인하며 사용자 최신 지시와 최신 실제 근거를 우선한다.

## 자연어 협업 Claude 독립 리뷰 — 현행 실행 진입 (2026-11-25)

- 사용자의 실행 지시 **“협업 클로드리뷰 요청해줘”**, “협업 Claude 리뷰 요청해줘”, “클로드 협업 리뷰 요청해줘”, “정식 독립리뷰 요청해줘”, “리뷰요청해줘”는 동일한 정식 Windows Claude Code 독립 리뷰 워크플로를 의미한다. 예시·인용·절차 질문은 실행이 아니다. 일반 “검토해줘”는 독립 리뷰로 확대하지 않는다.
- 어느 CoWork 대화창이든 최신 CONTEXT_BRIEF 및 해당 CURRENT에서 기존 Work·마지막 확정 입력·중복/불확실 이력을 확인하고 [현행 계약](collab/ops/CONTRACTS/PRE_READY_SOURCE_PIN_PREFLIGHT_V1.md)을 적용. Work/원본/입력이 이미 제공됐으면 반복 질문하지 않는다.
- 표준 제출기 또는 동등한 GitHub API 절차로 REQUEST+ZIP/PIN을 게시한 뒤 반드시 같은 RID의 보호 승인·READY·dispatch·결과/영수증 상태를 다시 조회한다. 표준 제출기의 post_submission/--status-request-id 또는 동일 고정 원격 스냅샷 읽기를 재사용. 기존 RID의 보류는 신규 제출하지 않고 회수한다.
- 기존 유효 권한이면 실제 보호 signer 경로를 연결한다. 스킬 범위 밖이면 실제로 지원되는 보호된 일회성 승인/서명 REVIEW_INTENT 경로를 사용하며, 자격이 없거나 호스트 접근 불가이면 정확한 차단을 보고한다. GitHub 공개 REQUEST나 자연어 기록 자체는 실행 권한이 아니며 --approval-route auto는 표시일 뿐이다. 기존 위임·키·scope 임의 변경 금지.
- 완료 표현: REQUEST/PIN 원격 검증은 **정식 제출 완료(승인 대기)**; 보호 서명·READY 정합성 실제 검증은 **실행 준비 완료**; 실제 dispatch 증거는 **리뷰 실행 확인**; 결과/영수증 정합성 검증은 **독립 리뷰 완료**. 파일 존재만으로 검증 PASS 금지. 원격 snapshot만 읽을 수 있으면 HOST_ACK=UNKNOWN이며 미실행/실패를 단정하지 않는다.
- 자동 승인이 가능한 기존 보호 경로는 재사용하되, 해당 경로가 실제 운영에서 미연결이면 같은 Work에 차단·담당·다음 한 동작을 기록한다. 새 리뷰 요청이나 별도 수동 프롬프트를 기본 동작으로 만들지 않는다. 본 지침은 실제 자동 로딩·호스트 접속·권한 변경을 보장하지 않는다. 아래 구형 게시/비용/완료 표현보다 이 현행 진입과 최신 계약이 우선한다.

## 동일 스킬·Viewer 병렬 개발 통합 게이트 — 새 창의 필수 진입 (2026-11-21)

- **공통 정본:** [병렬 변경 통합 게이트 V1](collab/ops/CONTRACTS/PARALLEL_CHANGE_INTEGRATION_GATE_V1.md), 코드 `collab/ops/integration_gate.py`, 기존 Work CURRENT. 새 창에서 UI·Write·환경설정 등 **같은 Work/단일 ZIP을 수정**하면 시작 전에 기존 `integration/streams/<stream_id>.json` 등록 여부와 각 작업의 기준 revision·필수 파일·원본 ZIP SHA를 확인하고, 같은 Work를 재개한다. 다른 창의 진행을 대화 메모리만으로 추측하지 않는다.
- **최종 통합본 제출 전 필수:** Work에 등록된 모든 stream을 최종 ZIP 한 개에 합치고, 명시된 소스 ZIP 및 필수 엔트리 SHA·동일파일 충돌 해결·`regression`과 `cross_stream` 실제 시험 근거를 확인한다. `python collab/ops/integration_gate.py --work-dir <STAGED_WORK_DIR> --repo-root . --branch main --expected-head <FROZEN_REMOTE_MAIN_HEAD>`의 **exit 0 `INTEGRATION_PRECHECK_PASS`**가 없거나 HEAD가 갱신되면 **최종 릴리스 완료/운영 배포로 판정 금지**. 같은 줄 충돌·변경 누락은 새 후보/rebase 후 전체 재시험.
- **승인·자동화 경계:** PASS는 소스/로그·핀 사전 일치 검증이며 독립 리뷰/운영 호스트 설치·실제 브라우저 E2E PASS가 아님. 이 지침은 CoWork를 읽은 개발/게시 주체의 **수동 게시 전 절차**이며 모든 GitHub API 직접 쓰기를 기술적으로 차단하지 않는다. 자동 Actions 시험은 사용자 지시에 따라 재활성화하지 않음.

확인되지 않은 원본·API·설치 기능을 구현 대상으로 확정하지 않는다. 문서 기록·패키지 검토·호스트 설치 사실·실제 호출·독립 리뷰는 서로 구분한다. 기존 제공자 재사용을 먼저 확인하고 새 엔진/schema는 입증된 gap의 최소 범위로 제한한다.

이 지침은 스킬 원문·상위 사용자 지시·프로젝트 CURRENT를 대체하지 않는다. 문서 게시만으로 Claude/Job/자동 감시를 실행하지 않으며, 운영 변경·PUBLIC 게시·LIVE 전환에는 해당 승인과 게이트가 필요하다. 제한 자료는 PRIVATE에도 게시하지 않는다.

**표현 규칙:** [용어·저장소·실행 환경 표기 원칙](collab/ops/CONTRACTS/TERMINOLOGY_AND_ACCESS_SCOPE_V1.md)을 따른다. 장소/망 접두어 없이 **GitHub PRIVATE/PUBLIC**, 업무용 Git 역할, 작업 PC, Linux 실행 호스트 등 실제 대상을 지칭한다. 파일명·기존 경로·과거 감사·보안 권한은 바꾸지 않는다. 신규 문서와 응답부터 적용한다.


## 현행 결정 r0007 — 독립 리뷰 단일 유형·게시기 비용 게이트 제거 (2026-11-22 KST)

- 일반 신규 요청은 **독립 리뷰 한 유형**. GPT 게시기 `check_request_for_publication(intent="independent")`는 Windows 가격 파일·금액·스킬별 위임 허용 목록을 조회하지 않는다. 기존 `unified USD3` 선검사와 `--delegated-skill` 출판 선차단은 현행 신규 게시 경로에서 사용하지 않음. `run_policy_ref=POLICY-STATIC-V1`은 기존 Windows 포맷과의 원본 호환을 위해 유지.
- 게시자의 AUTO 표시는 보호 signer 권한이 아니다. **Windows 설치 LIVE는 아직 USD3 및 skill allowlist를 계속 검증**. 해당 게이트가 실제로 제거됐다는 주장 금지. 새 제안은 [동일 Work 적용/전환 기록](collab/projects/COWORK-AUTO-APPROVAL-20261115-001/GPT_INDEPENDENT_REVIEW_COST_GATE_SIMPLIFICATION_RESULT_r0001_20261122_KST.md)과 [PRE_READY r0007](collab/ops/CONTRACTS/PRE_READY_SOURCE_PIN_PREFLIGHT_V1.md) 기준. 위험한 무승인 모델 호출을 열지 않도록 승인된 reviewer capability·서명·READY·원본/중복 보호는 필수.
- 구형 유료 리뷰/정책 문구는 그 시점의 이력. 새 사용자 의도와 비용 통제를 별개 리뷰 유형으로 분류하지 않음. 이 결정으로 이전 READY나 실행 중 요청을 다시 큐에 넣지 않는다.

 — “리뷰체계 최신버전 확인 후 다시 리뷰요청해줘” (2026-11-22)

## GPT 정식 리뷰 실행 책임 — 이전 r0006 원칙(일부 r0007로 대체)

**과거 r0006 기준(2026-11-22):** GPT는 사용자 명시적 리뷰 요청을 받으면 **Windows LIVE 설정 없이** REQUEST/ZIP 형식·실제 바이트 SHA/CRC·기존 ID/결과 중복과 Git source pin을 검증하여 정식 Commit A/B를 직접 게시한다. Windows 정책/위임/비용·서명·READY는 실제 Windows 보호 signer/watcher가 검증한다. 아래 과거 사전 정책 확인 필수·호스트 위임 문구는 **REQUEST 게시 전 필수조건으로 적용하지 않는다**. 제출·실행 승인 경계를 혼동하지 말고 [정본 r0006](collab/ops/CONTRACTS/PRE_READY_SOURCE_PIN_PREFLIGHT_V1.md)을 따른다.


- 사용자가 설계 중인 **해당 GPT 대화창**에서 “리뷰요청해줘” 또는 “리뷰체계 최신버전 확인후 다시 리뷰요청해줘”라고 실행 지시하면 **정식 Windows Claude Code 독립 리뷰 요청**이다. 계약 조회·문서 요약·자체 검토로 요청을 대체하지 않는다. 같은 대화에서 마지막으로 확정한 동일 Work/설계·구현 산출물만 대상으로 삼는다.
- **GPT 책임 ② — 대상 확정:** 최근 사용자 수정·확정 사항 → 해당 Work CURRENT/열린 결과·리뷰 이력 → 실제 GitHub 원본 revision·경로·SHA/크기·시험 증거를 순서대로 확인한다. 오래된 인계서나 이전 ZIP보다 마지막 확정 산출물 우선. 기존 REQUEST/READY/결과·영수증 및 불확실 이력부터 조회해 **동일 건 중복 접수·재모델 호출을 차단**한다. 정확한 Work·검토 목적/포함·제외 범위·소스 고정이 가능하면 사용자에게 같은 입력을 재요구하지 않는다.
- **GPT 책임 ③ — 실제 정식 제출:** 필요한 비민감 리뷰 입력이 이미 있으면 재생성하지 않고 검증·재사용한다. ZIP 실제 바이트·SHA-256·크기·CRC/경로·REQUEST 필수 필드·원본 고정을 사전검사한 뒤, 허용된 제출 수단으로 **Commit A(REQUEST.md와 정확한 ZIP 같은 커밋) → 원격 검증 → Commit B(SOURCE_PIN.json이 A를 가리킴) → 원격 readback**까지 진행한다. 가능한 API/도구와 승인 범위를 실제 조회·활용하며, **인계 MD·ZIP Base64 후보·REQUEST 초안·CURRENT/TRACKER 갱신만으로 종료하지 않는다**. 이 자료를 만든 후 즉시 실제 제출 가능 여부까지 판정한다.
- **실제 제출 불가능할 때:** GPT가 GitHub 정식 Commit A/B 원격 게시·원본 해시/중복 검증 자체를 수행할 도구·권한이 없으면, **정식 요청 미접수**로 정확히 판정하고 누락 게이트 한 가지를 보고한다. 별도 Windows 작업을 실행했다고 주장하거나 대체 제출/무단 서명·READY·비용 우회를 하지 않는다. 반복적인 인계서·새 후보·새 Work 생성으로 문제를 숨기지 않는다. 사용자가 요청한 ②③을 수행 가능한 범위에서 모두 끝낸 다음에만 이 차단을 보고한다.
- **최종 보고 필수:** 확인한 Work ID/대상·원본 SHA, 정식 `collab/requests/<RID>/REQUEST.md`와 `SOURCE_PIN.json` **원격 실재·commit A/B 확인 여부**, 상태 `SUBMITTED_AWAITING_PROTECTED_SIGNER` 또는 `NOT_POSTED/BLOCKED`, 이후 signer/READY/Claude 리뷰는 별도 판정. **“정식 제출 완료(승인 대기)”는 REQUEST·ZIP·SOURCE_PIN 원격 검증이 실제 PASS일 때만 사용**한다. 실행 준비/리뷰 완료는 위 현행 기준을 따른다. 상세 판단 기준은 [REQUEST/PIN 계약의 GPT ②③ 게이트](collab/ops/CONTRACTS/PRE_READY_SOURCE_PIN_PREFLIGHT_V1.md)를 따른다.

## 자연어 정식 리뷰 요청 — 표준 생성 경로 (2026-11-21)

사용자가 설계·구현을 이어온 **같은 창에서 단독으로 “리뷰요청해줘”** 또는 “리뷰 요청해줘”라고 지시하거나, 새 창에서 **“정식 리뷰 요청”, “Claude 협업 리뷰 요청”, “리뷰 올려줘”, “재리뷰 요청”** 등 자연어로 지시하면 기존 Work와 현재 요청·결과·영수증을 먼저 조회하고 이 절을 **필수 진입점**으로 사용한다. 문서만 생성하거나 ZIP만 게시하고 “정식 리뷰 제출 완료”라고 말하지 않는다.

- 정본: [두 커밋 생성 및 검증 절차](collab/ops/CONTRACTS/PRE_READY_SOURCE_PIN_PREFLIGHT_V1.md), 단일 게시기 `collab/ops/submit_review_request.py`, 정책 검사 `review_request_gate.py`, PIN 검사 `review_pin_preflight.py`.
- **Base64 보관 후보의 선택적 복원 경로:** 동일 Work에 이미 고정된 REQUEST 초안·Base64 ZIP이 있을 때만 `collab/ops/review_staged_submission.py`의 기본 dry-run으로 Work/원본/크기/SHA·ZIP 자체를 검증한다. **Windows LIVE 정책은 REQUEST 게시 필수조건이 아니며** `--live-config`는 선택적 참고. 사용자 명시 리뷰 요청·기존 중복 조회·GitHub 제출 권한이 확인된 범위에서만 `--publish`로 기존 단일 게시기를 재사용한다. **후보 게시만으로는 접수 완료가 아니며, 실제 REQUEST+PIN Commit A/B 원격 확인 시 접수 완료**. 서명·READY·리뷰 실행은 Windows 보호 경로에서 별도 검증한다. 이전 Windows 자동 인입 hook 미설치 여부는 이 출판 절차의 장애 조건이 아니다.
- **정식 요청 생성은 단일 게시기 우선**: Windows LIVE 설정이 아닌 입력 REQUEST·ZIP 자체 무결성을 게시 전 검증 → 동일 Commit A에 REQUEST+ZIP → 원격 SHA/bytes 확인 → Commit A를 가리키는 PIN을 별도 Commit B에 게시 → 로컬 PIN 검사·원격 확인. 실패하면 `BLOCKED`, 새 ID 남발·이전 요청 재큐잉·수동 우회 금지. GitHub 파일 작성 도구로 직접 쓰는 경우에도 **동일 절차·각 게이트 실측** 없이는 정식 제출 판정 금지.
- 게시기의 `SUBMITTED_AWAITING_PROTECTED_SIGNER`는 **서명/READY/Claude 리뷰 완료가 아님**. Windows 보호 signer의 실제 승인·위임/비용/만료/중복 검사와 READY 마지막 게이트는 별도. 자동 대상 외라면 유효한 수동 승인만 사용; 스킬 ID 변경으로 우회 금지.
- GPT는 실제 Windows `reviewer.config.json` 및 보호 자격을 읽을 필요 없이 **정식 REQUEST+PIN 게시까지 수행**한다. GitHub commit A/B 원격 readback이 되지 않으면 완료로 보고하지 않는다. Windows 실제 LIVE 정책·보호 서명·READY/유료 모델 실행은 호스트의 기존 보호 경로에서 별도로 검사하며 현재 승인 범위를 확대하지 않는다.
- **새 창 적용 경계:** 이 저장소의 AGENTS/CLAUDE 및 ChatGPT 프로젝트가 읽는 CONTEXT_BRIEF로 진입을 안내하지만, 모든 GPT 세션의 자동 조회·Windows 설치·호스트 강제 hook은 별도 실측 전 `NOT_VERIFIED`. 기존 스크립트를 거치지 않는 GitHub API 쓰기까지 기술적으로 막힌 것은 아니다.

## CoWork 리뷰 REQUEST 게시/실행 승인 분리 (r0006 / 2026-11-22)

- GPT 게시 전 필수: `review_request_gate.check_request_for_publication()`의 schema·정적 run_policy_ref(`POLICY-STATIC-V1`/USD3 unified)·실제 ZIP 크기/SHA-256/CRC·경로 검증, 기존 ID/영수증/UNCERTAIN·Git commit A/B 원본 고정. `submit_review_request.py`의 `--live-config`는 **선택적 참고**이며 생략해도 REQUEST+PIN 게시 가능. GitHub API 게시도 동일 입력/커밋/원격 readback을 만족해야 한다.
- Windows 승인 전 필수: 실제 LIVE reviewer.config/delegation/비용/승인 서명·READY·중복 검증은 **계속 강제**한다. GPT가 작성한 policy/status/문서만으로는 승인이나 서명을 대체할 수 없고, READY 없이는 모델 호출 0. 정식 REQUEST 게시 완료와 Claude 리뷰 완료는 별도 판정.
- 과거 `REVIEW_TIER_TOKEN_BUDGET_V1.md`의 2026-11-17 **REQUEST 게시 전 Windows LIVE 검증 의무 조항은 r0006에 의해 대체**. 호스트 자체 호환성 검사 CLI `review_request_gate.py select/check`는 삭제하지 않으며 읽기 전용 진단으로 유지. 새 리뷰/재큐잉/정책·키·위임/운영 변경에 대한 추가 권한을 이 문서가 부여하지 않음.

## 후속 조치가 있는 응답의 마무리

- 사용자 명시 요청(2026-11-18 KST): **다음 조치가 남아 있는 사용자 대상 최종 응답은 마지막 문장을 정확히 “조치에대해 처리 진행할까요?”로 마무리한다.** 문구의 공백·표기를 임의로 바꾸지 않는다. 다음 조치가 없으면 이 질문을 덧붙이지 않는다.
- 기존 유효 승인 범위의 작업은 끝까지 수행한 뒤 남은 조치에 이 응답 형식을 적용한다. 이 문구를 이유로 기승인 작업 중간에 반복 승인을 요청하지 않으며, 문구 자체를 새 유료 호출·운영 변경·설치·배포 승인으로 해석하지 않는다.
