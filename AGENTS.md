# CoWork 작업 시작 지침

이 저장소의 새 작업은 다음 순서로 진행한다.

1. [공통 맥락 브리프](collab/CONTEXT_BRIEF.md)를 먼저 읽어 협업 운용·L1 지식·관리 스킬의 공통 방향을 파악한다.
2. 브리프에서 요청 목적에 맞는 프로젝트를 고른 뒤 해당 `CURRENT.md`의 현재 요약·열린 메모·최신 결과/영수증을 실제 조회한다. Work ID뿐 아니라 그 안의 설계·구현·시험 등 이어갈 작업 흐름도 확인한다. 최신 조회에 실패하면 마지막 확인 시점과 미확인을 표시하고 과거 상태로 실행 여부를 확정하지 않는다.
3. 브리프에서 기존 스킬 후보를 선택하고 필요한 상세 I/O는 `collab/knowledge/SKILL_CAPABILITY_CATALOG.md`와 해당 스킬 원문만 확인한다. 사용자에게 스킬명을 다시 묻거나 18개 감사를 반복하지 않는다.
4. 실제 작업에 적용되는 `collab/START_HERE.md`의 계약을 필요한 범위에서 확인하고 REUSE / CONNECT / 입증된 최소 EXTEND / DEFER를 판단한다. 이미 읽은 브리프를 링크 때문에 반복 조회하지 않는다. 정확한 절차는 `collab/ops/CONTRACTS/SKILL_DISCOVERY_AND_REUSE_V1.md`를 따른다.
5. 작업 결과·피드백 원문은 해당 결과/결정/notes에 보존하고, 현재 상태·근거 링크·미해결·승인 범위·다음 한 행동은 해당 CURRENT에 갱신한다. 보완은 같은 목적의 Work와 작업 흐름을 이어간다. 기존 TRACKER는 필요한 현행 필드만 맞추고 별도 상태 정본으로 삼지 않는다.
6. 공통 브리프는 역할·정본 위치·요청별 경로가 바뀔 때, 카탈로그는 스킬 책임·입출력·연결 계약이 바뀔 때만 갱신한다. 일반 진행·버전·리뷰 상태를 브리프에 복사하지 않는다. 작업한 GPT/Agent가 CoWork main 게시와 원격 재조회까지 확인하며 사용자 최신 지시와 최신 실제 근거를 우선한다.

## 동일 스킬·Viewer 병렬 개발 통합 게이트 — 새 창의 필수 진입 (2026-11-21)

- **공통 정본:** [병렬 변경 통합 게이트 V1](collab/ops/CONTRACTS/PARALLEL_CHANGE_INTEGRATION_GATE_V1.md), 코드 `collab/ops/integration_gate.py`, 기존 Work CURRENT. 새 창에서 UI·Write·환경설정 등 **같은 Work/단일 ZIP을 수정**하면 시작 전에 기존 `integration/streams/<stream_id>.json` 등록 여부와 각 작업의 기준 revision·필수 파일·원본 ZIP SHA를 확인하고, 같은 Work를 재개한다. 다른 창의 진행을 대화 메모리만으로 추측하지 않는다.
- **최종 통합본 제출 전 필수:** Work에 등록된 모든 stream을 최종 ZIP 한 개에 합치고, 명시된 소스 ZIP 및 필수 엔트리 SHA·동일파일 충돌 해결·`regression`과 `cross_stream` 실제 시험 근거를 확인한다. `python collab/ops/integration_gate.py --work-dir <STAGED_WORK_DIR> --repo-root . --branch main --expected-head <FROZEN_REMOTE_MAIN_HEAD>`의 **exit 0 `INTEGRATION_PRECHECK_PASS`**가 없거나 HEAD가 갱신되면 **최종 릴리스 완료/운영 배포로 판정 금지**. 같은 줄 충돌·변경 누락은 새 후보/rebase 후 전체 재시험.
- **승인·자동화 경계:** PASS는 소스/로그·핀 사전 일치 검증이며 독립 리뷰/운영 호스트 설치·실제 브라우저 E2E PASS가 아님. 이 지침은 CoWork를 읽은 개발/게시 주체의 **수동 게시 전 절차**이며 모든 GitHub API 직접 쓰기를 기술적으로 차단하지 않는다. 자동 Actions 시험은 사용자 지시에 따라 재활성화하지 않음.

확인되지 않은 원본·API·설치 기능을 구현 대상으로 확정하지 않는다. 문서 기록·패키지 검토·호스트 설치 사실·실제 호출·독립 리뷰는 서로 구분한다. 기존 제공자 재사용을 먼저 확인하고 새 엔진/schema는 입증된 gap의 최소 범위로 제한한다.

이 지침은 스킬 원문·상위 사용자 지시·프로젝트 CURRENT를 대체하지 않는다. 문서 게시만으로 Claude/Job/자동 감시를 실행하지 않으며, 운영 변경·PUBLIC 게시·LIVE 전환에는 해당 승인과 게이트가 필요하다. 제한 자료는 PRIVATE에도 게시하지 않는다.

**표현 규칙:** [용어·저장소·실행 환경 표기 원칙](collab/ops/CONTRACTS/TERMINOLOGY_AND_ACCESS_SCOPE_V1.md)을 따른다. 장소/망 접두어 없이 **GitHub PRIVATE/PUBLIC**, 업무용 Git 역할, 작업 PC, Linux 실행 호스트 등 실제 대상을 지칭한다. 파일명·기존 경로·과거 감사·보안 권한은 바꾸지 않는다. 신규 문서와 응답부터 적용한다.


## 자연어 정식 리뷰 요청 — 표준 생성 경로 (2026-11-21)

사용자가 설계·구현을 이어온 **같은 창에서 단독으로 “리뷰요청해줘”** 또는 “리뷰 요청해줘”라고 지시하거나, 새 창에서 **“정식 리뷰 요청”, “Claude 협업 리뷰 요청”, “리뷰 올려줘”, “재리뷰 요청”** 등 자연어로 지시하면 기존 Work와 현재 요청·결과·영수증을 먼저 조회하고 이 절을 **필수 진입점**으로 사용한다. 문서만 생성하거나 ZIP만 게시하고 “정식 리뷰 제출 완료”라고 말하지 않는다.

- 정본: [두 커밋 생성 및 검증 절차](collab/ops/CONTRACTS/PRE_READY_SOURCE_PIN_PREFLIGHT_V1.md), 단일 게시기 `collab/ops/submit_review_request.py`, 정책 검사 `review_request_gate.py`, PIN 검사 `review_pin_preflight.py`.
- **Base64로 보관된 설계 후보의 Windows 접수 경로:** 동일 Work의 원격 고정 REQUEST 초안·Base64 ZIP이 이미 있으면 `collab/ops/review_staged_submission.py`의 **기본 dry-run**으로 원본/Work/크기/SHA·Windows 실제 LIVE 정책을 검사하고, 허용된 경우에만 `--publish`로 기존 단일 게시기를 호출한다. 정확한 절차는 [접수 보조 및 Windows 연결 게이트](collab/projects/COWORK-AUTO-APPROVAL-20261115-001/REVIEW_INTAKE_ONE_SHOT_HOST_INTEGRATION_r0001_20261122_KST.md). **호스트 자동 hook은 아직 미설치**이며 이 파일·일반 GitHub 후보/문서 게시만으로 Windows 접수나 signer/READY를 완료했다고 보고하지 않는다. 사용자가 긴 프롬프트를 반복 입력하도록 하지 않되, Windows host 접근이 실제로 없으면 HOST_BLOCKED로 분리한다.
- **정식 요청 생성은 단일 게시기 우선**: Windows LIVE 정책과 입력 ZIP으로 게시 전 검증 → 동일 Commit A에 REQUEST+ZIP → 원격 SHA/bytes 확인 → Commit A를 가리키는 PIN을 별도 Commit B에 게시 → 로컬 PIN 검사·원격 확인. 실패하면 `BLOCKED`, 새 ID 남발·이전 요청 재큐잉·수동 우회 금지. GitHub 파일 작성 도구로 직접 쓰는 경우에도 **동일 절차·각 게이트 실측** 없이는 정식 제출 판정 금지.
- 게시기의 `SUBMITTED_AWAITING_PROTECTED_SIGNER`는 **서명/READY/Claude 리뷰 완료가 아님**. Windows 보호 signer의 실제 승인·위임/비용/만료/중복 검사와 READY 마지막 게이트는 별도. 자동 대상 외라면 유효한 수동 승인만 사용; 스킬 ID 변경으로 우회 금지.
- GPT가 실제 Windows `reviewer.config.json` 및 보호 자격을 읽을 수 없으면 **해당 검증·게시 단계는 Windows Claude Code의 표준 게시기 실행으로 위임**하고, 이 대화/문서만으로 실행됐다고 주장하지 않는다. 현재 발화의 승인 범위보다 유료 호출·운영 변경을 확대하지 않는다.
- **새 창 적용 경계:** 이 저장소의 AGENTS/CLAUDE 및 ChatGPT 프로젝트가 읽는 CONTEXT_BRIEF로 진입을 안내하지만, 모든 GPT 세션의 자동 조회·Windows 설치·호스트 강제 hook은 별도 실측 전 `NOT_VERIFIED`. 기존 스크립트를 거치지 않는 GitHub API 쓰기까지 기술적으로 막힌 것은 아니다.

## CoWork 리뷰 REQUEST 사전 검증 (신규 요청만)

GPT가 새 REQUEST를 작성·게시하기 **전에** `collab/ops/CONTRACTS/REVIEW_TIER_TOKEN_BUDGET_V1.md`의 신규 'REQUEST 게시 전 정책 호환성 필수 게이트'를 따라야 한다. `collab/ops/review_request_gate.py`의 `select` / `check`에 Windows 실제 LIVE `reviewer.config.json` 및 신규 ZIP 바이트를 사용하고 `PASS_PREPUBLICATION_ONLY`를 확인한다. LIVE 설정 직접 조회가 불가능하면 Windows Claude Code에 읽기 전용 검증을 요청하고, 검증 전에는 REQUEST를 게시하지 않는다. GPT가 개발 예정 정책명을 선택해 기존 LIVE를 막는 자기 참조를 금지. SOURCE_PIN/서명/READY는 기존 계약대로 별도 검증하며 이 절차로 유료 모델을 호출하거나 운영 설정을 변경하지 않는다.

## 후속 조치가 있는 응답의 마무리

- 사용자 명시 요청(2026-11-18 KST): **다음 조치가 남아 있는 사용자 대상 최종 응답은 마지막 문장을 정확히 “조치에대해 처리 진행할까요?”로 마무리한다.** 문구의 공백·표기를 임의로 바꾸지 않는다. 다음 조치가 없으면 이 질문을 덧붙이지 않는다.
- 기존 유효 승인 범위의 작업은 끝까지 수행한 뒤 남은 조치에 이 응답 형식을 적용한다. 이 문구를 이유로 기승인 작업 중간에 반복 승인을 요청하지 않으며, 문구 자체를 새 유료 호출·운영 변경·설치·배포 승인으로 해석하지 않는다.
