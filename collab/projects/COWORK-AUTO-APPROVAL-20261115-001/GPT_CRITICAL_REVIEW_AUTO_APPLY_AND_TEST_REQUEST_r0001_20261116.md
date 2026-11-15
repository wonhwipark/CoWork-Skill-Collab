# CoWork Claude 자동 리뷰 — 비판적 평가 기준 실제 적용·검증 요청

- r0001 / 2026-11-16 KST
- 정본: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`
- 상대 경로: `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/GPT_CRITICAL_REVIEW_AUTO_APPLY_AND_TEST_REQUEST_r0001_20261116.md`
- 기존 Work: `COWORK-AUTO-APPROVAL-20261115-001`. 별도 Work/원장/정식 R2 REQUEST 추가 생성 금지
- 사용자 지시: 현재 R0~R3 독립 리뷰에 비판적 검증·개선안 평가를 부각하고, **실제 자동 리뷰 경로에 적용 및 검증하는 작업까지 요청**
- **이 문서는 코드/설정 적용과 검증을 위한 작업 요청**. 여기 게시만으로 Windows 실행이나 Claude 모델 호출은 발생하지 않음. 임의 `READY.md`·유료 리뷰는 금지
- **새 유료 호출 승인 아님.** 기존 v0.2.23 독립 R2의 `POLICY-STATIC-V1-LARGE`, 최대 USD 3/모델 1회와는 구분

## 1. 확인된 기준 및 원래 동결 요청 보존

- 공통 품질 정본: `collab/ops/CONTRACTS/REVIEW_TIER_TOKEN_BUDGET_V1.md`의 **§2.1 비판적 평가·개선 제안**. 문서 수정 commit `1b7ab2175da7bace4d9dced5e01c31087a2bfe73`, 원격 읽기 검증 완료.
- 리뷰 타입 R0/R1/R2/R3 및 기존 정책 `POLICY-STATIC-V1` ($1), `-LARGE` ($3), `-XLARGE` ($6), 기존 요청/READY/서명/중복/비용 계약은 **불변**. R0는 설계상 후보이므로 실제 Windows 호스트에 등록·배포된 것으로 가정하지 않음.
- 이미 고정된 기존 R2 `REQ-COWORK-AUTO-APPROVAL-V023-R2-20261115`: `REQUEST.md`/`SOURCE_PIN.json`/검증된 v0.2.23 ZIP과 승인 비용은 변경·재생성하지 않는다. 최신 GitHub 조회 시 `READY.md`·`APPROVAL_SIG.json`·결과·영수증은 아직 **NOT_FOUND**였다. **기존 R2 재큐잉·동일 모델 재호출 절대 금지**.
- 기존 개발 후보 v0.2.23 자동 승인 기능은 아직 설치 LIVE라고 입증되지 않음. 사용자 요청을 더 단순하게 처리하더라도 host 상태/영수증으로 실제 동작을 검증하기 전에는 `AUTO_REVIEW_ACTIVE=UNVERIFIED`.

## 2. Windows Claude Code / 리뷰 실행 환경의 원샷 작업 (중간 핑퐁 최소)

**우선 REUSE/CONNECT 확인, 검증된 기능 부재에만 최소 EXTEND:**

1. 실제 Windows 설치본·개발 후보의 기존 review prompt 생성 경로(예: REQUEST 본문 전달/템플릿 결합/runner)를 **설치 원본과 콜사이트 근거로 확인**. `REQUEST.md`의 내용이 그대로 전달되는 구조라면 새 스키마·모듈·정책을 만들지 않고, 향후 GPT 신규 REQUEST 작성 규칙에 §2.1을 넣는 방식부터 검증할 것.
2. 향후 **새로 생성되는** 독립 리뷰에서 아래 평가 기준이 실제 최종 Claude 입력에 포함되도록 연결한다. 리뷰 타입별 깊이는 R0=문서 가정, R1=변경 반례·최소 수정, R2=구조·신뢰/상태 가정·대안, R3=운영·복구/장기 아키텍처 비교. 이미 고정된 R2 입력은 건드리지 않음.
3. 원칙: 결함 수 강제 0, 반드시 반론할 의무 0. 설계 타당성 확인도 근거와 함께 허용. 개발 세션 자체시험을 독립 PASS로 주장 금지. 결함(BLOCKING/MAJOR/MINOR)은 재현 근거와 심각도를 요구하고, **개선 기회는 별도 섹션**에서 (A) 최소 수정, (B) 필요 시 구조적 대안 및 비용·리스크·호환성 비교. 비차단 제안은 자동 코드 수정/운영 적용 트리거가 아님. `NOT_VERIFIED`·`PARTIAL_SCOPE` 표기.
4. 비용/토큰 초과를 유발하지 않도록 기존 리뷰 타입별 목표 예산을 유지하고, 기존 리뷰 텍스트에 짧은 평가 문구만 추가. 임의 새 등급 승격, R0 활성화, 별도 모델 호출/서브에이전트 금지.
5. **모델 호출 없는 격리 시험**: 실제 prompt-builder 혹은 fake runner dry-run을 사용해 R1/R2/R3(그리고 지원하는 경우 R0)의 생성 입력을 캡처하고 §2.1의 필수 평가 요소가 들어가는지 확인. 확인된 결함 없음/근거 불충분/결함+개선 혼합/설계가 합리적인 경우/승인 범위 밖 제안 등 반례를 정적 스냅샷·테스트로 검사한다. 입력 revision·SHA가 동결된 기존 R2는 변경 전후 동일한지 비교. self-test vs independent-review 라벨 구분.
6. **REUSE로 충분하면 코드·ZIP 변경 없이** 결과·시험과 신규 REQUEST 템플릿 개선만 기록. 실제 연결이 없다면 `CONNECT` 또는 입증된 최소 코드 수정으로 한정하고 신규 개발 후보/테스트/ZIP SHA·CRC를 작성. 그 후보는 새 독립 리뷰·최종 판정 전 설치·LIVE 변경 금지.
7. 신규 리뷰 요청이 필요하다면 **작업 대상/후보 ZIP/승인 비용을 고정한 별도 신규 REQUEST**만 가능. 현재 승인된 `POLICY-STATIC-V1` 자동 위임은 실제 Windows 활성화·유효 scope 검증 전에는 사용 불가. 이미 고정된 R2 $3를 이 새 목적에 재사용하거나 임의 추가 유료 호출하지 않는다. 가능한 생성 테스트는 전부 무료·격리 수행.
8. 독립 리뷰 요청을 실행할 수 있는 유효한 자동 경로가 실제로 준비되고 비용 위임도 유효하면, **그때만** 신규 요청을 정상 기존 절차로 연결하고 결과/영수증을 확인한다. 그렇지 않으면 `AUTOMATED_REVIEW_REQUESTED_PENDING_HOST` 또는 `BLOCKED_APPROVAL_OR_ACTIVE_POLICY`로 명확히 기록. 이 문서 자체나 CURRENT/TRACKER 수정으로 watcher 작업을 실행했다고 주장하지 않음.

## 3. 결과 및 완료 기준

- 결과 예상 경로: `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/CLAUDE_CRITICAL_REVIEW_AUTO_APPLY_VALIDATION_FOR_GPT_20261116.md`
- 입력 근거: 실제 설치본/후보 버전, 리뷰 프롬프트 조합 지점과 캡처한 final input의 범위, 기존 정책/요청 경계
- 판정: `REUSE/CONNECT/EXTEND`, **PROMPT_INJECTION_TEST=PASS/FAIL/NOT_RUN**, `R0=NOT_ACTIVE` 해당 시 표시, `INDEPENDENT_REVIEW=NOT_RUN` 또는 실제 증거로 구분
- 검증: 각 등급별 평가 항목 포함 여부, false finding 강제 회피, 결함/개선 분리, 입력 고정 불변, prompt 길이/추가 비용, 같은 요청 중복 모델 0
- 필요한 경우 최소 개발 후보만 생성·격리 자체시험. **실제 Claude 호출은 유효한 독립 승인·정식 READY가 있고 고정 패키지에 대한 중복 검사에 합격할 때만**
- `CURRENT.md`에는 최신 요약·미검증·다음 한 동작, `TRACKER.json`에는 기존 Work의 현재 필드만 갱신. 허용된 비민감 결과를 PRIVATE main에 PR 없이 게시하고 commit·remote bytes/SHA readback 확인. 과거 리뷰/영수증·v0.2.23 R2 입력 보존.
- **금지:** 무단 유료 모델 실행, 기존 v0.2.23 R2 수정/재큐잉, 운영 설치·Notifier·Task·DB·token/key·provider 설정 변경, PUBLIC 게시, 새로운 자동 감시 설치.

## 4. 한 번에 전달할 Windows 실행 프롬프트

GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`의
`collab/projects/COWORK-AUTO-APPROVAL-20261115-001/GPT_CRITICAL_REVIEW_AUTO_APPLY_AND_TEST_REQUEST_r0001_20261116.md`
를 읽고 §2~3의 실제 자동 리뷰 프롬프트 적용·격리 dry-run 검증을 한 회차로 수행해. 기존 R2 `REQ-COWORK-AUTO-APPROVAL-V023-R2-20261115`의 고정 입력과 승인·READY를 손대지 말고, R0~R3가 실제 요청/runner에서 어디서 전달되는지 확인해 REUSE→CONNECT→필요한 최소 EXTEND로 처리해. 결함 개수 강제 없이 근거 중심 비판·최소 수정·대안 비교·개선 제안 분리가 실제 생성 프롬프트에 들어갔는지 테스트해. 모델 유료 호출/새 READY/운영 설치 없이 가능한 자체시험을 마친 다음 결과를 `CLAUDE_CRITICAL_REVIEW_AUTO_APPLY_VALIDATION_FOR_GPT_20261116.md`에 기록하고, 같은 Work의 CURRENT/TRACKER를 갱신해 PRIVATE main 게시·원격 재조회해. 유효한 자동 리뷰 실행이 불가하면 그 사실만 BLOCKED/NOT_RUN으로 구분해 보고해.
