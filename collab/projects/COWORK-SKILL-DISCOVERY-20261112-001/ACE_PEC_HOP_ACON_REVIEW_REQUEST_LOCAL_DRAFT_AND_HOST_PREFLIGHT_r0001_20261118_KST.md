# ACE·PEC-HOP·ACON 독립 설계 리뷰 — Windows 실호스트 정식화 이전 입력 초안 및 사전검증 원샷

- 개정: r0001 / 2026-11-18 KST
- **비실행 초안**: DRAFT_ONLY, 실제 정식 REQUEST 아님. 이 문서의 게시는 watcher 실행 신호가 아니며 Windows/Claude Code 자동 기동·새 유료 모델 호출 0.
- 저장소·브랜치: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab` / `main`
- 기존 Work: `COWORK-SKILL-DISCOVERY-20261112-001`
- 리뷰 ID 후보: `REQ-COWORK-ACE-PEC-HOP-ACON-DESIGN-R1-20261118`. **중복/원격·로컬 예약 체크 후에만** 신규 확정.
- 검토 범위: CoWork/L1 ACE 맥락 재개·PEC-HOP 근거 보존·ACON 실패 검증의 최소 변경 통합 설계 **1회 독립 리뷰**. 업무 설치본 `l1-knowledge-updater`는 실제 G0 미접근, 별도 업무 GPT의 설계 적용 제안/READ_ONLY 조사로 유지.
- 이전 Windows 실제 보고: 2026-11-18의 운영 watcher v0.2.23, protected delegation `max_request_usd=1.0`, v0.2.25 미설치. 이번 작업에서 재측정하지 않았으며 현재 값이라고 단정하지 않음.
- 현행 문서상 설계 리뷰 정책 기준: `POLICY-STATIC-V1-DESIGN` 또는 실제 LIVE에 등록된 후방 호환 `POLICY-STATIC-V1-LARGE` **USD 3.00**. 코드 계약 `collab/ops/review_request_gate.py`의 `intent=design` 기준. 유효 위임 $1 상태이면 **정식 게시·서명·READY·모델 호출 모두 0**. 사용자 "그래"는 기존 조치를 진행하라는 뜻이며 무제한 비용/보호 위임 상향 승인으로 취급하지 않음.

## 1. 원격 입력 고정

| 패키지 내부 제안 경로 | 실제 원문 | 이미 원격 검증된 SHA-256 / bytes |
|---|---|---|
| `01_SKILL_SOURCE_AUDIT.md` | PRIVATE main `collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/ACE_PEC_HOP_ACON_SKILL_SOURCE_AUDIT_r0001_20261118_KST.md` | `743d7b3c40b6eecb0cf3633e1276ad7ffae3b7d34d314741fb67e755245c2cff` / 8122 |
| `02_INTEGRATED_DESIGN.md` | PRIVATE main `collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/ACE_PEC_HOP_ACON_INTEGRATED_SKILL_DESIGN_r0001_20261118_KST.md` | `aa69b2e6bba529d09609d8c6c7b1ead0d4b3d744208361ce447c87ad57b41303` / 16874 |
| `03_BUSINESS_UPDATER_APPLICATION.md` | PUBLIC `wonhwipark/L1Work/main` `handoffs/L1_KNOWLEDGE_UPDATER_ACE_PEC_HOP_ACON_DESIGN_APPLICATION_PROPOSAL_r0001_20261118_KST.md` | `b8273c33392370b93945b370679d670b5ddbc6ae0a4b9abaa12118bc41dae368` / 10707 |
| `04_REVIEW_INSTRUCTIONS.md` | 아래 §2 (리뷰 범위·질문만 포함, 실호스트에서 실제 ZIP에 동봉) | 생성한 실제 바이트·해시를 기록할 것 |

서명/요청 고정 패키지는 **검증된 위 세 원문 + §2**의 비민감 스냅샷만 포함. CoWork PRIVATE 문서에 회사 소스·고객 로그·상세 MSC 또는 키/토큰을 섞지 않는다. 미래 변경분을 묵시적으로 섞지 않는다. 내용이 기준 digest와 달라지면 정확한 원본 commit 고정·차이 재검토 전 멈춘다. ZIP 파일명 후보: `ace_pec_hop_acon_design_r0001_1118_REVIEW_INPUT.zip`.

## 2. 리뷰 패키지 `04_REVIEW_INSTRUCTIONS.md` 내용

독립 Windows Claude Code 리뷰어는 01~03 문서를 읽고 다음을 비판적으로 검토:
1. ACE: CoWork `CONTEXT_BRIEF→CURRENT→Work/Evidence` 및 L1 Kernel을 재사용하면 새 메모리/원장이 실제로 불필요한가? 정본 충돌과 최신 결정의 우선순위가 타당한가?
2. PEC-HOP: CODE FACT/CL·PR/원본 위치·source revision·모듈/시나리오 조건·부정조건을 무손실 보존할 수 있는가? Issue/Fact/HLD/MSC 원본과 출력 owner가 섞이지 않는가?
3. ACON: full-context 성공/압축본 실패의 재현·반례/통제와 기존 피드백/회귀 경로 연결이 충분한가? 압축률보다 정확성을 먼저 판정하는가?
4. 현재 개발 후보 `l1-fix-workflow`, `l1-github`, `work-ledger-kernel`의 `development_not_for_deployment`, raw Git 우회/G0, 실제 Updater 미확인, 그룹 Knowledge 승인/충돌·writer 경계가 설계에서 보존되는가?
5. 공개 전달/업무 보안·기존 리뷰 승인/서명·READY·중복/비용 fail-closed를 위반하지 않는가?
6. 각 기능에 REUSE/CONNECT/증명된 최소 EXTEND/DEFER를 판정하고 실제 누락/과도한 신규 시스템 제안의 반례를 제시해라.

요청 판정: ACCEPT / ACCEPT_WITH_CHANGE / REVISE / HOLD. 확정 결함과 구조 개선 기회 분리. 결함 0건도 허용; 근거·심각도·최소 수정·미확인·수용 시험을 명시하고 **1회 독립 리뷰** 후 결과/영수증을 게시. 임의 다중 유료 재리뷰·모델 전환·추가 서브에이전트 금지.

## 3. Windows Claude Code가 해야 할 원샷 순서

1. `main` 최신 readback 후 본 문서/선행 [공식 인계](ACE_PEC_HOP_ACON_WINDOWS_INDEPENDENT_DESIGN_REVIEW_PREFLIGHT_HANDOFF_r0001_20261118_KST.md), 계약 `collab/ops/CONTRACTS/REVIEW_TIER_TOKEN_BUDGET_V1.md`, `collab/ops/review_request_gate.py`를 확인. 기존 리뷰 요청 ID/논리 중복과 Windows 예약 상태 확인. 이 작업을 지난번 MSC 완료 리뷰나 Guard UNCERTAIN 요청에 붙이지 않는다.
2. 실제 **Windows 로컬 LIVE** `reviewer.config.json`을 운영 호스트에서 찾아 읽기 전용으로 확인하고, GitHub의 **현행** `collab/ops/review_request_gate.py`를 로컬에 안전하게 확보. `python collab/ops/review_request_gate.py select --live-config <실제 Windows 설정 경로> --intent design --required-budget-usd 3.00` 실행. `POLICY_COMPATIBLE_NOT_APPROVED`가 아닌 결과는 실패. 보호 위임의 1회 비용/프로젝트/스킬/기한/잔여 한도도 실제 승인 검증 도구로 확인. 정책 등록과 승인 유효성은 별도.
3. 정책·위임 미충족 또는 비용 범위가 실제 max $1이면 **새 REQUEST/ZIP/APPROVAL_SIG/READY 게시/유료 호출 0**. 새 위임 생성·정책 수정·$1 정책으로 의도 바꿔 우회 금지. 기존 Work에 blocker 코드·실제 읽기만 수행한 결과/기존 승인 범위와 필요한 정확한 승인 항목을 게시하고 종료.
4. 모두 유효할 때만 §1 세 원본을 원격 digest/byte 기준으로 가져오고 §2를 담아 로컬 ZIP 생성·CRC/경로/민감정보 검사. `REQUEST.md` 로컬 초안은 아래 §4의 값을 실제 ZIP 바이트, 선택한 등록 정책, 기존 보호 범위에 맞게 채운다.
5. 로컬에서 `python collab/ops/review_request_gate.py check --live-config <실제 Windows 설정 경로> --intent design --required-budget-usd 3.00 --request <신규 로컬 REQUEST.md> --package <동일 로컬 ZIP>` 실행, **`PASS_PREPUBLICATION_ONLY`** 필수. 정책 select/check가 실제 LIVE config에 대해 성공하기 전에 formal `collab/requests/<id>/REQUEST.md` 및 `collab/packages/<zip>` 게시 금지. 합성 config PASS로 대체 금지.
6. 실제 PASS + 유효 별도 승인이 함께 확인되었을 때 정확한 ZIP·REQUEST 바이트만 commit A로 PRIVATE main 게시→원격 bytes/SHA/revision/원문 재검증→`collab/ops/source_pin.py create --repo-id 1451933830 --commit <commit A> --output <로컬 파일>`로 문자열 repo_id pin 생성→`source_pin.py check`로 검증→기존 Windows signer/approve의 진짜 보호 정책과 유효 위임 별도 검사→서명 검증 후 READY **마지막** 게시.
7. 기존 watcher/runner가 유효 신규 요청만 단 1회 실행하도록 하고, REVIEW_RESULT·RECEIPT·실제 호출 수/비용/디스패치 및 GPT 판정 대기 상태를 기존 경로에 게시·원격 검증. 불확실/이미 호출됨/게시 실패 시 모델 재호출 0. 결과 게시 실패는 게시/영수증만 정산.
8. 기존 `COWORK-SKILL-DISCOVERY-20261112-001/CURRENT.md` 상단에 실제 결과/차단·승인·경로·hash·NEXT_ONE_ACTION을 갱신. 기존 TRACKER의 현행 필드만 정합화. MAIN PR 없이 직접 게시·readback. 운영 DB·LIVE·키·토큰·회사 지식·PUBLIC ZIP은 변경하지 않음.

## 4. 로컬 REQUEST.md 초안의 필드 (정식 게시 금지)

```yaml
---
schema: SKILL_COLLAB_REVIEW_REQUEST_V1
state: SUBMITTED
request_id: REQ-COWORK-ACE-PEC-HOP-ACON-DESIGN-R1-20261118
request_revision: 1
project_id: COWORK-SKILL-DISCOVERY-20261112-001
work_id: COWORK-SKILL-DISCOVERY-20261112-001
skill_id: cowork-context-design
package_path: /SKILL-COLLAB/packages/ace_pec_hop_acon_design_r0001_1118_REVIEW_INPUT.zip
package_file_id: github:REV-COWORK-ACE-PEC-HOP-ACON-DESIGN-R1-20261118
package_rev: ace-pec-hop-acon-design-r0001
package_sha256: REPLACE_WITH_ACTUAL_LOCAL_PACKAGE_SHA256
package_size_bytes: REPLACE_WITH_ACTUAL_LOCAL_ZIP_BYTE_COUNT
baseline_package_ref: null
knowledge_refs: []
consumer_profiles: [cowork-context-evidence-feedback-design-review]
reviewer_os: WINDOWS
test_policy: STATIC_ONLY
run_policy_ref: REPLACE_WITH_ACTUAL_POLICY_SELECTED_BY_LIVE_GATE
output_contract: SKILL_COLLAB_REVIEW_RESULT_V1
goal: independent one-cycle scoped ACE PEC-HOP ACON integration design review
---
```

**경고:** 위 scope `skill_id=cowork-context-design`은 논리적 초안 이름이며, Windows 보호 위임의 허용 스킬 ID 목록과 실제 비교 후 유효한 정확한 ID로만 확정. 허용 스킬명을 바꿔 권한을 우회하거나 승인 범위를 넓히지 않음. 위 REPLACE 값이 남아 있는 초안은 불완전하며 **정식 REQUEST가 아니다**.

정식 본문은 §2 및 선행 설계의 확정 source pin, READ_ONLY G0 한계, reviewer 결과 위치, 예산/호출 최대 1회를 적고 기존 동일한 `SKILL_COLLAB_REVIEW_REQUEST_V1` 계약을 준수.

## 5. 실제 이번 GPT 작업 상태

- 원격 검사: `collab/requests/` 및 `collab/reviews/`의 목록과 신규 ID 조회 결과 해당 정식 요청/결과 미발견(확인 시점 2026-11-18 KST). Windows 로컬 pending/claims·운영 DB는 미접근.
- 계약/코드 정적 검증: `review_request_gate.py`에 `--intent design`, `--required-budget-usd`, `select/check`, `POLICY_COMPATIBLE_NOT_APPROVED/PASS_PREPUBLICATION_ONLY` 구현 확인.
- 최신 Windows 운영 설정/위임 실측 이번 GPT 세션에서는 NOT_RUN. 마지막 보고 v0.2.23 보호 위임 $1과 설계 정책 $3의 차이는 **KNOWN_POLICY_DELEGATION_GAP**이며 현재 해소 여부 미확인.
- `FORMAL_REQUEST_NOT_POSTED` / `READY_NOT_POSTED` / `MODEL_CALLS=0` / `INDEPENDENT_REVIEW=NOT_RUN`.
- 검증 가능한 한도에서 문서·정책·원본 readback만 진행. 실제 Windows 실행을 문서 게시로 대신 주장하지 않음.

**NEXT_ONE_ACTION:** Windows Claude Code가 실제 LIVE config + 보호 위임 select/check를 수행해 유효하다면 §3을 같은 1사이클로 끝까지 처리, 불가하면 이유/호스트 근거만 기존 Work에 보고.
