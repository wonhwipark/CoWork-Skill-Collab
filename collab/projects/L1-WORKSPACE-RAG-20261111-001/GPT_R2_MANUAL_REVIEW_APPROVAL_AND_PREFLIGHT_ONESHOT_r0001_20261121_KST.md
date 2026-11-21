# Windows Claude Code 원샷 — Knowledge Preflight v0.2.0 R2 수동 승인 리뷰 1건 + SOURCE_PIN 재발 방지

- 작성/사용자 승인: 2026-11-21 KST, 이번 대화에서 GPT가 **R2 1회 최대 USD 3 수동 리뷰 진행 여부**를 질문했고 사용자가 “그래, 그리고 이 문제 발생에 대한 재발 방지대책”으로 명시 동의.
- **사용자 의도**: R2 고정 패키지 1회의 정식 수동 독립 리뷰 처리와 동일 문제의 생성 단계 예방. 이 문서 자체가 보호된 승인 서명·READY/모델 호출 권한 또는 실제 운영 호스트 실행임을 뜻하지 않음.
- **정본 저장소:** `wonhwipark/CoWork-Skill-Collab`, branch `main`, 이 파일 `collab/projects/L1-WORKSPACE-RAG-20261111-001/GPT_R2_MANUAL_REVIEW_APPROVAL_AND_PREFLIGHT_ONESHOT_r0001_20261121_KST.md`.
- **기존 Work:** `L1-WORKSPACE-RAG-20261111-001`. R1 원문·PIN·WAIT_INPUT/COMMIT_UNREADABLE·DB/감시 기록을 무손실 보존.

## 고정 요청

| 필드 | 값 |
|---|---|
| Request ID | `REQ-L1-KNOWLEDGE-PREFLIGHT-V020-R2-20261121` |
| Request revision | 1 |
| `skill_id` | `knowledge_analysis_preflight` — **다른 이름으로 변경 금지** |
| 정책 | `POLICY-STATIC-V1`, 현재 정본 Windows LIVE 보고 기준 **USD 3.00 이하**. 실제 현장 로드 값 재검증 |
| 고정 SOURCE_PIN commit | `50a8b5d9e832b1fbf9095c729c813e83134b1fd8` |
| Repo ID | 문자열 `"1451933830"` |
| ZIP 경로 | `collab/packages/knowledge_analysis_preflight_v0_2_0_1121_REVIEW_INPUT.zip` |
| ZIP SHA-256 | `90a0d55842138d4c813f0dbc3a5c8e4625e84a110afe68035348297ffedad1f3` |
| ZIP size | `16138` bytes |
| 고정 요청 진입 | `collab/requests/REQ-L1-KNOWLEDGE-PREFLIGHT-V020-R2-20261121/REQUEST.md`, `SOURCE_PIN.json` |
| 승인 범위 | **한 ID / revision 1 / 동일 고정 SHA / 모델 최대 1회 / 최대 USD 3**. 반복 승인·다른 ID·그룹 게시·운영 LIVE/키/위임 변경은 포함하지 않음 |

## Windows Claude Code / 공식 보호 signer 실행

1. 현재 `collab/CONTEXT_BRIEF.md`, Knowledge Work `CURRENT.md`, AUTO-APPROVAL Work `CURRENT.md`, R1 장애·R2 전송 정정 결과, [기본 원칙](../../ops/CONTRACTS/PRE_READY_SOURCE_PIN_PREFLIGHT_V1.md) 확인. 원격 `main`과 Windows DB/Job/claim, REQUEST/READY/APPROVAL_SIG/REVIEW_RESULT/RECEIPT를 **먼저** 조회. R1 또는 R2에 이미 완료/불확실/모델 과금 기록이 있으면 **중단/보존**, 재큐잉 금지.
2. Git 원격 최신 `main` 전체 SHA를 실제로 확인하고 허용된 로컬 CoWork 체크아웃에 `git fetch`(READ-only remote, 로컬 ref update)하여 해당 SHA와 고정 commit의 객체 확보. 전체 소스·운영 설정을 수정하거나 백업 삭제하지 말 것.
3. 다음 **읽기 전용 Git-tree 사전검사**를 실제 코드에 대해 실행. `<MAIN_40HEX_SHA>`는 실제 원격에서 방금 읽은 값으로 대체하고 더 오래된 값을 재사용하지 말 것.

   ```powershell
   python collab/ops/review_pin_preflight.py --repo-root . --main-commit <MAIN_40HEX_SHA> --request-id REQ-L1-KNOWLEDGE-PREFLIGHT-V020-R2-20261121 --package-repo-path collab/packages/knowledge_analysis_preflight_v0_2_0_1121_REVIEW_INPUT.zip --expected-repo-id 1451933830 --approval-mode manual
   ```

   `status=PASS_PINNED_INPUTS_ONLY`과 PIN commit/REQUEST 해시/ZIP SHA·크기 정합성 확인. FAIL이면 **어떤 서명/READY도 작성하지 않고 BLOCKED**. 이 단계의 PASS는 **사용자 승인·보호 signer 자격·READY PASS가 아님**.
4. **정식 Windows 보호 signer의 수동 승인 자격을 별도 검증**: 실제 설치된 `approve_request.py` 또는 호스트 승인 도구의 정확한 `help`·loaded config를 확인하고, 이번 사용자 1건 승인 의도에 대한 공식 서명 권한/expiry/scope/policy/ref/SHA/budget를 확인. `skill_id=knowledge_analysis_preflight`는 자동 위임 미허용이므로 **`AUTO_NOT_ELIGIBLE`이 정상**; `l1-knowledge-updater`로 대상을 바꾸거나 위임 allowlist·USD 정책·보호 키/ACL·Windows LIVE 변경 금지. **현재 서명 도구가 수동 권한을 인정하지 않으면 `BLOCKED_MANUAL_AUTHORITY` 기록만 게시하고 모델 0**. GitHub에 쓴 사용자 승인 주장을 정식 서명으로 대신하지 말 것.
5. 호스트 정식 signer에서 수동 승인 범위를 실제 확인하고 서명이 유효할 경우에만 해당 R2에 **공식 보호 `APPROVAL_SIG.json`**, 최종 remote readback, **`READY.md` 마지막 게시**를 수행. 자격이 없으면 그 후 단계를 절대 시도하지 않음. 이미 READY가 존재하면 모델 중복 가능성 확인 전 재실행 금지.
6. watcher가 기존 유효 처리 경로로 실행한 **정식 Windows Claude Code 독립 코드 리뷰 최대 1회**의 `REVIEW_RESULT_1.md`·`RECEIPT_1.md`, 실제 policy 비용·모델 호출수·Job DB 처리키를 확인. 불확실 실행은 UNCERTAIN 보존, 결과 게시 실패 때문에 모델 재호출하지 않음. 요청 수정/비용 초과/중복도 차단.
7. CoWork PRIVATE `collab/projects/L1-WORKSPACE-RAG-20261111-001/` 기존 Work에 **하나의 비민감 결과** 및 CURRENT 현행 상태를 게시하고 commit/remote bytes 확인. GPT가 실제 결과·영수증 판정 후에만 최종 패키지 `L1Work/main` 공개 배포와 그 다음 업무 GPT `l1-knowledge-updater` 구현 핸드오프 r0002 발행. 이 순서는 사용자 최신 지시이며 절대 역전하지 말 것.

## 재발 방지 적용 범위

- GPT가 직접 구현·정적 시험/게시한 `collab/ops/review_pin_preflight.py`: 고정 ZIP SHA/크기, PIN repo_id, **PIN commit의 REQUEST와 ZIP 동일 존재**, main 대비 바이트 drift, 자동 delegated skill 적격성/미제공, READY·SIG 선존재 재큐잉 차단.
- `collab/ops/tests/test_review_pin_preflight.py`: 실제 임시 Git 저장소를 이용한 **15/15 합성 PASS**, 그중 잘못된 R1 commit의 `COMMIT_UNREADABLE_REQUEST_ABSENT` 차단 포함. GitHub 원격 코드 blob과 로컬 시험 바이트 동일.
- 새 절차 [PRE_READY_SOURCE_PIN_PREFLIGHT_V1](../../ops/CONTRACTS/PRE_READY_SOURCE_PIN_PREFLIGHT_V1.md) 채택. 그러나 **운영 Windows signer의 자동 필수 연결은 아직 적용/검증되지 않음**. 이 Windows 실행 시 수동으로 게이트를 호출하고, 추후 별도 유효한 운영 승인/시험을 거쳐서만 자동 연동.
- 테스트는 입력 무결성에 한정. 모델 리뷰 정확도/업무 C++ 접근/실제 MSC·Knowledge write 통과를 뜻하지 않음.

## 반드시 반환할 결과

| 필드 | 필수 보고 |
|---|---|
| R2 preflight | 원격 HEAD, pinned commit, `PASS/BLOCKED`, reason |
| 승인/권한 | 한정 사용자 승인 인지, **실제 signer authority PASS/BLOCKED**, scope, budget |
| READY/리뷰 | `READY` 게시/미게시, review 결과/영수증, 모델 실제 호출 횟수 |
| 비용·중복 | USD 실청구, R1/R2 중복 0 또는 UNCERTAIN |
| 신규 예방 | helper 15개 테스트 및 Windows 실제 호출 PASS/FAIL/NOT_RUN |
| 결과 게시 | 기존 Work의 정확한 commit·readback 및 후속 GPT 판정 상태 |
| NEXT_ONE_ACTION | 차단 중 최초 한 항목 |

**실행 경계:** 본 인계는 사용자의 수동 유료 리뷰 1회 진행 의사를 전달하는 수단이고 **Windows 호스트/정식 signer의 신뢰·권한·실행을 대신하지 않는다**. 유효 조건 실패 시 서명·READY·유료 호출 0.
