# Windows Claude Code 원샷 인계 — ACE·PEC-HOP·ACON 통합 스킬 설계 독립 리뷰

- 작성 2026-11-18 KST / 기존 Work: COWORK-SKILL-DISCOVERY-20261112-001
- 고정 저장소: GitHub PRIVATE wonhwipark/CoWork-Skill-Collab, branch main
- 목적: 통합 맥락/증거 전달/피드백 설계에 대한 독립 Windows Claude Code 설계 리뷰 1사이클만 요청. 업무용 l1-knowledge-updater의 실제 설치본 검토는 별도 업무 GPT 공개 인계로 분리.
- 상태: REVIEW_PREFLIGHT_HANDOFF_ONLY, FORMAL_REQUEST_NOT_POSTED, WINDOWS_LIVE_POLICY_NOT_VERIFIED.
- 실행 지시의 한계: GitHub 문서 게시만으로 Windows Claude Code·watcher·서명·READY·유료 모델이 자동 기동되지 않음.
- 승인 경계: 사용자 이번 대화의 "협업 리뷰요청까지"는 독립 리뷰 의도와 범위를 승인한 요청. 비용/모델 호출·LIVE 정책은 기존 유효 위임과 실제 Windows 보호 승인 범위를 추가로 만족해야 함. 이 인계 문구를 APPROVAL_SIG로 인정 금지.

## 1. 이미 게시된 원본 — 수신 때 실제 바이트 및 현행 결과 검증

| 원본 | 정확한 repo/ref/경로 | 직접 게시 commit / Git blob |
|---|---|---|
| 8종 스킬 원문 정적 감사 | CoWork PRIVATE main, collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/ACE_PEC_HOP_ACON_SKILL_SOURCE_AUDIT_r0001_20261118_KST.md | c5e9a3995c45eaf47c6ca1db589d1584823f0782 / e815a0be20a5028b68e31eb8dd7d55a319c81ecb |
| 통합 설계 r0001 | CoWork PRIVATE main, collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/ACE_PEC_HOP_ACON_INTEGRATED_SKILL_DESIGN_r0001_20261118_KST.md | d34f20bea719d98d534e30dbec3dc86a8bf4dca1 / 11b3680be92fb12734f2fa998dc57674716a59b8 |
| 업무 GPT Updater 별도 제안 | PUBLIC wonhwipark/L1Work/main, handoffs/L1_KNOWLEDGE_UPDATER_ACE_PEC_HOP_ACON_DESIGN_APPLICATION_PROPOSAL_r0001_20261118_KST.md | 7b028cc4e9ff2423d407ba6d0a44d7942ce0d37e / 085a3c53b51a1a6fe70b7e3dbc162201169bc310 |

원본이 갱신되었다면 임의로 최신 내용을 새 리뷰 고정 패키지에 섞지 않는다. 위 pin commit에서 실제 내용을 확보하고 source SHA/size 계산·원본 위변조 확인. 공개 업무 인계는 비민감 설계 제안으로만 읽고 실제 Updater 설치본·회사 코드/로그/상세 MSC를 가져오지 않는다. 최근 같은 기존 Work의 다른 설계 리뷰는 결과·영수증이 이미 종료된 사안; 새 범위의 새 요청과 중복 검사 결과를 명시한다.

## 2. Windows 정책 사전검증 — 공식 REQUEST 게시 이전 필수

1. CoWork PRIVATE main의 collab/ops/CONTRACTS/REVIEW_TIER_TOKEN_BUDGET_V1.md 및 collab/ops/review_request_gate.py의 실제 현재 계약을 재조회.
2. Windows Claude Code 실제 운영 호스트 설치 LIVE의 reviewer.config.json(실제 로컬 파일을 호스트가 탐색; 값·비밀을 PRIVATE/PUBLIC으로 게시하지 말 것)으로 review_request_gate.py select --live-config <검증된 실제 로컬 설정> --intent design 호출. 대상 정책명/정책금액/보호 위임·현재 설치 상태를 read-only로 확인. 설정이나 위임을 임의 수정·격상/대체 금지.
3. 디자인 리뷰는 현재 정책 계약상 DESIGN $3이 우선이나 실제 LIVE에 등록·유효 승인된 정책만 선택. DESIGN 미등록이고 LARGE가 실제 등록돼 있을 때만 기존 LARGE 허용. 동일 사용자 명시 요청이라도 Windows 운영 유효 비용 승인 범위를 넘으면 POLICY_NOT_AUTHORIZED/HOLD로 종료, 호출 0. 구형 운영 $1 수준을 근거 없이 $3으로 승격 금지.
4. 리뷰 입력에 꼭 필요한 위 두 PRIVATE 파일 + 허용된 PUBLIC 설계 제안 + 최소 책임·수락 기준만 가진 임시 고정 ZIP과 정식 REQUEST의 로컬 초안을 작성(회사 자료/토큰/키 제외). 사전 스킬 목적/비용·패키지 SHA-256/크기/CRC/path·Request 정확 SHA를 Windows review_request_gate.py check --live-config <실제 로컬 config> --intent design --request <로컬 DRAFT REQUEST> --package <로컬 후보 ZIP>으로 검증. select/check 모두 PASS_PREPUBLICATION_ONLY 또는 실제 계약의 동일 PASS가 확인되지 않으면 ZIP/REQUEST를 GitHub 정식 경로에 게시 금지. 단순 synthetic PASS는 대체 근거 아님.
5. 사용자 지시로 독립 설계 리뷰 1회가 요청됐더라도, 별도 필요한 유료 비용 승인/정책/위임이 유효하지 않으면 진행 중지: REQUEST_NOT_POSTED / READY_NOT_POSTED / MODEL_CALLS=0 / BLOCKED_REASON을 해당 Work에 기록하고 GPT에 전달.

## 3. 사전검증 PASS와 유효 승인 범위가 모두 확인된 경우에만

1. 중복/기존 완료 요청 존재 여부를 실제 원격 및 Windows reservation/audit에서 확인. 기존 완료/UNCERTAIN 요청 재큐잉 금지. 논리 요청 ID 신규 예시 REQ-COWORK-ACE-PEC-HOP-ACON-DESIGN-R1-20261118 (기존 중복없음 검증 후 확정); request_revision=1, work_id/project_id=COWORK-SKILL-DISCOVERY-20261112-001. 사용자 비용 위임을 새로 만들거나 임의 상한 상향 금지.
2. Windows preflight가 PASS한 동일 ZIP/REQUEST 바이트만 PRIVATE main의 collab/packages/ 와 collab/requests/<확정 ID>/REQUEST.md 경로로 commit A에 게시. source 원본·ZIP SHA256/size/CRC/비밀 검사·패키지 manifest·commit A 실제 바이트를 독립적으로 remote readback.
3. collab/ops/source_pin.py create/check를 사용하여 실제 repo ID 1451933830을 SOURCE_PIN.json에 **문자열 "1451933830"**로 입력, pin commit A의 40자리 SHA 정확 결속. SOURCE_PIN과 원본 byte/readback PASS.
4. 기존 Windows approval/signing 도구로 승인 가능 여부·변조·만료·중복/실행 여부·호출 budget 검증. 승인 불가/불확실/이미 처리 시 signer/READY/모델 호출 0.
5. 유효 승인/서명이 검증되면 APPROVAL_SIG 및 READY를 정상 보호 도구로 **마지막에** 게시. GPT가 승인 서명/READY 직접 게시하지 않는다.
6. 승인된 watcher/runner가 1회만 Windows Claude Code 독립 리뷰. 인증·원본·정책 실패는 fail-closed. 실행 중/결과 게시 실패 때문에 모델/Job을 재호출하지 않음.
7. 결과/영수증/실제 비용을 기존 collab/reviews, collab/receipts, collab/dispatch에 게시, 원격 내용 SHA/영수증/정확 processing key와 호출 1회 증거를 검증. 현재 Work CURRENT 상단 상태/링크·필요한 TRACKER만 업데이트. 비민감 내용만 게시.

## 4. 독립 리뷰 평가 범위

- ACE: 현재 CoWork 지도→CURRENT→Work/Evidence·L1 Kernel이 이미 제공하는 맥락을 과장 없이 재사용하는가? 새 메모리 DB/원장 없이 충분한가?
- PEC-HOP: source revision·Fact ID·정확 인용·적용조건/부정조건·미확인 상태를 지키는 패킷과 producer/consumer 소유권을 어떻게 최소 연결하는가?
- ACON: 원본 성공/압축본 실패의 인과를 검증할 수 있는가? 기존 피드백·시험 경로와 사용자 승인 경계를 어떻게 보존하는가?
- L1 knowledge: 업무 Updater 설치본 접근 미확인 상태를 사실대로 표시했는가? 기존 Knowledge Preview/권한·단일 writer·그룹 CAS 및 개인 Work 저장 구분이 유지되는가? 새 ref_type/metadata/key/API를 추정하고 있지 않은가?
- 보안/운영: 소스 민감정보를 CopWork/PUBLIC에 반출하지 않는가? 승인·서명·READY·비용/중복 검사와 모델 출력을 혼동하지 않는가?
- 비용/단순성: 독립 모델 호출 수를 늘리거나 불필요 스킬 변경을 유도하는가? 최소 REUSE 안과 필요할 때 구조 대안 비교.

확인된 결함 없으면 NONE으로 보고. 지적은 BLOCKING/MAJOR/MINOR, 명확한 증거, 검증 불가능 항목, REUSE/CONNECT/입증된 GAP, 최소 수정/수용 시험, 판정(ACCEPT/ACCEPT_WITH_CHANGE/REVISE/HOLD)을 한국어로 기록. 단 한 사이클. 리뷰 입력 부족 시 PARTIAL_SCOPE, 임의 R2/R3 상향·서브에이전트/추가 유료 요청 금지. 독립 리뷰와 Windows Claude 자체 구현/시험을 혼동 금지.

## 5. 원샷 보고 계약

성공 시: REQUEST/ZIP/source pin SHA·크기·commit A, Windows policy select/check의 실제 상태, 서명/READY 검증, Windows dispatch/review/receipt URL·검증 SHA, 실제 모델 호출 횟수/비용, finding·상태, 관련 Work의 NEXT_ONE_ACTION.

차단 시: 수행된 읽기 전용 검증·정확 차단 단계/오류코드, 신규 REQUEST/READY/유료 실행 여부 각각 0 또는 미확인, 필요한 정확한 승인 항목, 다음 한 동작. 차단이라고 기존 배포·운영 설정·보호 위임을 변경하지 않는다.

## 6. 현재 전달 단계의 정확한 판정

SKILL_SOURCE_AUDIT=POSTED / DESIGN=POSTED / BUSINESS_UPDATER_PROPOSAL=PUBLIC_POSTED / WINDOWS_HOST_SELECT_CHECK=NOT_RUN_BY_GPT / FORMAL_REVIEW_REQUEST=NOT_POSTED / REVIEW_RESULT=NOT_RUN / HOST_OPERATION_CHANGE=0 / NEW_MODEL_CALLS=0.

NEXT_ONE_ACTION: 실제 Windows Claude Code가 이 PRIVATE main 인계서를 조회해 자신이 접근하는 현재 LIVE 정책을 읽기 전용 select/check로 사전 검증. 통과·유효 비용 승인/중복 조건을 입증하면 같은 1회 사이클의 REQUEST→서명/READY→실리뷰→영수증까지 완료; 미통과면 정확한 차단 근거만 게시.
