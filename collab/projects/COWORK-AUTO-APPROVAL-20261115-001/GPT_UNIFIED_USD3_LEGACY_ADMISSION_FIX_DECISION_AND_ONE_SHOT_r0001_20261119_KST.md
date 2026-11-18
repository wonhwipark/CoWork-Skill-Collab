# GPT 판정 및 Windows Claude Code 원샷 — 단일 USD 3 신규 리뷰 / 레거시 자동 승인 차단
- 일자: 2026-11-19 KST
- PRIVATE 정본: wonhwipark/CoWork-Skill-Collab, branch main
- 기존 Work: collab/projects/COWORK-AUTO-APPROVAL-20261115-001
- 근거: 동일 Work의 CLAUDE_UNIFIED_REVIEW_USD3_HOST_RESULT_FOR_GPT_20261119.md, CLAUDE_LEGACY_DESIGN_R1_CLOSEOUT_AND_USD3_RESULT_FOR_GPT_20261119.md, CURRENT.md 및 완료된 LARGE R2 리뷰/영수증.
- 사용자 기존 승인: 신규 리뷰 공통 USD 3/건, 일·월 횟수·누적비용 제한 없음, 동일 요청 1회, 서명·SOURCE_PIN·READY·원본/재실행 보호 유지. 추가 유료 독립 리뷰/새 watcher 운영 설치까지 포괄하는 승인으로 해석 금지.

## 1. GPT 판정
**선택 1 — 기존 watcher 자동 승인 엔진의 최소 코드 수정.** 새 reject CLI·DB terminal/denylist·신규 승인 스키마는 기본 구현하지 않음.

- 기존 소스의 auto_policy.assess는 POLICY-STATIC-V1과 POLICY-STATIC-V1-DESIGN을 모두 자동 허용하는 것으로 확인됨(Windows 호스트 소스 확인). **신규 자동 리뷰는 POLICY-STATIC-V1/$3 한 종류만 허용**하도록 자동 승인 입구를 최소 수정. 새 REQUEST의 사전검증 review_request_gate.py --intent unified도 이미 POLICY-STATIC-V1/$3을 선택함. 과거 DESIGN/기타 ref는 기록·호환성을 위해 남겨도, 신규 위임을 통해 자동 서명되지 않아야 함.
- 문제 요청 REQ-COWORK-BUDGET-V025-DESIGN-R1-20261117, revision 1, ZIP SHA 26d63c8a03290499b13b2ceb8ff0b70c06eb1b1bcc1a25fe3d8f65fcc213d228 는 완료된 REQ-COWORK-BUDGET-V025-LARGE-R2-20261117과 동일 ZIP이며 업무상 SUPERSEDED/DO_NOT_EXECUTE 판정. 이력과 원격 bytes 보존. 정식 watcher terminal 경로가 없는 것으로 확인됐으므로 '종결 완료'라는 허위 표시 금지.
- **선택 2 (protected delegation의 project/skill 전체 제외) 기각**: watcher 자체의 신규 정상 리뷰까지 차단할 수 있고 현재 scope 포맷이 개별 REQUEST 예외를 표현할 수 있는지 미확인. 기존 프로젝트·스킬 허용 범위 확대·축소 회피.
- STATIC-only 한 줄 변경만으로 **그 밖의 구 STATIC REQUEST 소급 위험까지 차단했다고 가정 금지**. 새 USD3 위임 활성화 이전 REQUEST/Commit A가 새 가격으로 처리되지 않도록 기존 보호된 earliest_request_at/activation epoch 검증 경로를 실제 소스로 조사. 기존 계약으로 입증 가능하면 REUSE; 불가능하면 정확한 발생 근거로 최소 보완하여 안전 검증. 임의 DB 조작·REQUEST/SOURCE_PIN 변조·새 서명키/명목상 UNCERTAIN은 금지.

## 2. Windows Claude Code 단일 개발 원샷 (유료 모델 호출 0)
A. **실제 원본 확인**: 본 문서/최신 CURRENT, 설치된 v0.2.25와 개발 후보 v0.2.26의 auto_policy/auto_approval/signing/claim 및 기존 테스트, 실제 사용자 허용 범위·만료/기간을 읽기 전용 대조. 기존 v0.2.26의 pin 타입 선차단/READY 뒤 WAIT 억제/CRLF fixture 보완을 신규 후보에서 퇴행시키지 않음. 이미 후속 고정 후보가 있으면 그보다 오래된 ZIP에 기능을 되돌리지 말 것.
B. **최소 패치 및 신규 버전 후보**: 실제 후보 소스에서 자동 서명 경로의 허용 policy를 POLICY-STATIC-V1 하나로 제한. DESIGN 과거 REQUEST는 위임 USD3·등록 정책 USD3·허용된 project/skill·원본 pin 모두 맞아도 서명 이전의 REVIEW_POLICY 또는 동등한 fail-closed 결과. 기존 history, REQUEST, SOURCE_PIN, jobs/auto_claims 무변경. 활성화 컷오프가 기존 신뢰 경로에 없는 사실이 확인되면 최소 대안에 대한 근거/회귀를 마련하되 새 기능 확장을 무리하게 진행하지 않음. 새 버전 ZIP 이름·SHA·CRC·민감정보 및 경로 이탈 검증; 기존 v0.2.25/v0.2.26 ZIP 덮어쓰기 금지. 후보는 development_not_for_deployment.
C. **반례·전체 회귀**: (1) 구 DESIGN R1의 실제 ID/rev/SHA에 USD3 위임을 가정해 signer/READY/model 0, (2) 완료 LARGE R2 재호출 0, (3) Guard UNCERTAIN 재시도 0, (4) 위임 전 first-seen 3건 실행 0, (5) 신규 POLICY-STATIC-V1/USD3은 합성 평가만 정상 허용, (6) 과거 POLICY-STATIC-V1 요청이 있으면 새 가격으로 소급 서명 0, (7) 변조/만료/허용 scope/비용 초과/소스 SHA/동시성 중복 모두 fail-closed, (8) 일·월 한도 무효화 지속 PASS, (9) Windows 전용/기존 전체회귀 및 rollback 격리 시험. 실제 유료 모델 호출·실제 서명/READY·Telegram 발송·운영 설정 수정 0.
D. **독립 리뷰와 운영 게이트 분리**: 개발자 자체시험 PASS를 독립 리뷰 PASS로 쓰지 않음. 추가 유료 Claude 독립 리뷰는 기존 유효한 별도 승인/사전위임 범위를 확인한 후 정식 신규 REQUEST/READY 1회로 처리. 승인 범위가 불명확하면 INDEPENDENT_REVIEW=NOT_RUN/PENDING. 신규 ZIP을 Windows LIVE에 설치하거나 보호된 위임 USD1을 USD3로 변경하지 않음. 해당 부분은 이후 실제 승인/독립 리뷰/백업·SHADOW·롤백·소급 0 검증이 충족된 경우에만 조건부 진행.
E. **정본 원격 결과**: 같은 Work에 CLAUDE_UNIFIED_USD3_ADMISSION_FIX_DEV_RESULT_FOR_GPT_20261119.md 및 새 후보 ZIP/SHA·시험 결과를 PRIVATE main에 게시하고, CURRENT/TRACKER의 현행 필드만 업데이트 후 commit·원격 원본 bytes SHA 확인. 최소 ENGINE_POLICY_FIX, OLD_DESIGN_R1_USD3_DENIED, LEGACY_STATIC_RETROACTIVE_DENIED, TEST_WINDOWS, INDEPENDENT_REVIEW, HOST_CONFIG_APPLY, MODEL_CALLS, NEW_REQUEST_READY 상태를 개별 PASS/FAIL/BLOCKED/NOT_RUN으로 표기. 완료·불완전·미실행 구분.

## 3. 현 운영 판정
- GPT_DECISION=MINIMAL_STATIC_ONLY_AUTO_POLICY, AUTO_ADMISSION_FIX=DEV_HANDOFF, HOST_CONFIG_APPLY=BLOCKED, AUTO_SIGNING_USD3=NOT_APPLIED.
- Windows LIVE v0.2.25 / protected max_request_usd=1.00 유지, 모델/신규 REQUEST/READY 0. 기존 불확실 이력 재큐잉 없음.
- **NEXT_ONE_ACTION**: Windows Claude Code에서 이 한 문서 A~E를 실행하여 신규 개발 후보·회귀·원격 영수증을 게시. 별도 신규 유료 리뷰·운영 설치는 실제 승인 및 게이트 전 시작하지 않음.
