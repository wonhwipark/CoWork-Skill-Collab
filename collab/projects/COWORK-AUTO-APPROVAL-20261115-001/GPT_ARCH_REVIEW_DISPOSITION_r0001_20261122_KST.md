# GPT 판정 — CoWork 정식 리뷰 접수 구조·간소화 독립 리뷰 R1

- 판정: 2026-11-22 KST / GitHub `wonhwipark/CoWork-Skill-Collab`, `main` (현재 PUBLIC)
- Work: `COWORK-AUTO-APPROVAL-20261115-001`
- 정식 리뷰: `REQ-COWORK-REVIEW-ARCH-DESIGN-R1-20261122`, revision 1, skill `cowork-review-watcher`
- **GPT_DISPOSITION=`ACCEPT_WITH_CORRECTIONS__OPTION_B`**
- **구현 승인/운영 적용과 구분:** `DESIGN_DIRECTION=ACCEPTED`, `CODE_CHANGE=NOT_RUN`, `WINDOWS_LIVE_CHANGE=NOT_RUN`, `INDEPENDENT_RE_REVIEW=NOT_REQUESTED`

## 1. 실제 결과·영수증 정합성

- [독립 리뷰 원문](../../reviews/REQ-COWORK-REVIEW-ARCH-DESIGN-R1-20261122/REVIEW_RESULT_1.md): `execution_status=COMPLETED`, `review_scope=CODE_REVIEW`, `test_policy=STATIC_ONLY`, `run_policy_ref=POLICY-STATIC-V1`, `skill_id=cowork-review-watcher`, SHA-256 `c67bc342fe77547b000fc42e1b886396cbef035c0d265dbcd124947e267ed83f`. Claude 자체 판정 **BLOCKING 0, MAJOR 2(F1/F2), MINOR 2**; 실행시험 **NOT_RUN**.
- [영수증](../../receipts/REQ-COWORK-REVIEW-ARCH-DESIGN-R1-20261122/RECEIPT_1.md): `ok=true`, `request_id`/revision 1/`package_sha256`/processing_key 일치, `watcher_version=0.2.29`. 원격 결과 1건과 영수증 1건 존재 확인. 사용자 제공 Windows Telegram 알림의 비용은 **USD 0.77**이며, 영수증 JSON에는 달러 사용량이 없어 DB·usage 별도 비용 검증은 **NOT_VERIFIED**.
- [정식 REQUEST](../../requests/REQ-COWORK-REVIEW-ARCH-DESIGN-R1-20261122/REQUEST.md)·[SOURCE_PIN](../../requests/REQ-COWORK-REVIEW-ARCH-DESIGN-R1-20261122/SOURCE_PIN.json)·승인/READY와 동일 요청임을 대조. Commit A `1c9ff4448813c4c974d366ef82d25235781a3376`, B `cc84fa7c522ebfc8ffe3a938dbffe07ca8efdcd7`. 기존 ZIP 310753 bytes. 실제 Windows 호스트 DB 내부 모델 호출 횟수/서명 Ed25519 별도 재검증 **NOT_RUN**.
- **새 유료 E2E가 실제 발생한 증거:** 기존 v0.2.29 LIVE 이후 이 신규 요청의 A/B → 승인/READY → 리뷰/영수증 전체 GitHub 원격 체인이 확인됨. `LIVE_REAL_REVIEW_CHAIN=PASS_REMOTE_EVIDENCE`; 호스트 DB·사용액의 독립 정산까지 `PASS`로 승격하지 않음.

## 2. 핵심 설계 판정

**Option B — GPT 정식 REQUEST 게시와 Windows 유료 실행 승인 분리: 수용(조건부).**

- 현재 `collab/ops/submit_review_request.py`는 **GitHub 쓰기 전** 실제 Windows `reviewer.config.json`을 `review_request_gate.check_request(..., intent='unified', budget=3)`로 읽게 만들어 ChatGPT GitHub 연결에서 제출을 차단. 그러나 리뷰어는 운영 `skill_collab_watcher/validator.py`와 `auto_approval.py`가 등록 정책·PIN·scope·서명·비용·중복을 **호스트에서 다시 독립 검증**한다고 정적 근거를 제시함. 출판 단계의 LIVE 설정 접근은 실제 신뢰 게이트의 요건이 아님.
- **GPT의 명시적 사용자 요청 → 현재 대화의 Work/최신 변경·근거 확정 → 자체 형식·ZIP SHA/CRC·중복·commit pin 검증 → Commit A REQUEST+ZIP, Commit B PIN 원격 readback**을 기본 제출 단계로 하고, 실제 signer/READY/모델 호출 권한·정책은 기존 Windows watcher에 남김. 공개 저장소의 임의 텍스트나 GPT 승인 주장만으로 서명/READY를 만들지 않음.
- **중요 조건:** 출판 자체가 승인 권한은 아니지만, 자동 위임 범위 내 요청은 호스트 승인 후 **실제 비용**이 발생할 수 있으므로 *사용자의 명시적 리뷰 실행 지시*와 해당 Work/범위/원본을 반드시 확인한다. 임의 일정/일반 문서 갱신/초안 게시를 유료 모델 호출 신호로 바꾸지 않음. 자동 재큐잉, 이전 UNCERTAIN 복구 모델 재실행, scope 위장 금지.
- **입증된 이번 사례:** GPT에서 실제 GitHub A/B를 게시한 후 기존 Windows 처리 경로에 승인/READY와 리뷰/영수증까지 나타남. “새 상주 Windows 인입 watcher가 반드시 있어야 한다”는 가정은 이번 실례에 한해 **기각**. 다만 미래 모든 ChatGPT 채팅·미허용 skill에서 무조건 자동 리뷰를 보장한다는 주장은 하지 않음.

## 3. Claude 세부 발견 판정

| 리뷰 항목 | Claude | GPT 판정/근거 및 처리 |
|---|---|---|
| 두 커밋 A/B | SIMPLIFY | **유지(KEEP)**: SOURCE_PIN의 원본 커밋 자기참조를 안전하게 풀 수 있는 검증된 한-커밋 대안 없음. 중복 preflight 호출만 간소화 검토 |
| F1: `unified` USD3 vs 제공 예제 STATIC USD1 | MAJOR | **수정 수용(MINOR: 예제/호환 설명 정합성)**. 11/20 실제 Windows LIVE v0.2.29는 `POLICY-STATIC-V1=USD3`로 전환되었다는 호스트 보고와 이 완료된 신규 STATIC 리뷰가 존재함. `collab/ops/tests/test_review_request_gate.py`에는 USD3 정상·USD1/1.5 거부 회귀시험이 **이미 존재**. 예제 파일의 USD1을 현재 운영값으로 오인 금지. `POLICY-STATIC-V1-LARGE`로 정책 이름을 바꾸는 수정은 기존 자동 위임·단일 정책 계약과 충돌하여 **거절**. 운영 변경 없이 예제·설명/부정시험 기준만 최신 사실에 맞춰 정리 |
| F2: 패키지 `tools/review_request_gate.py`와 `collab/ops/review_request_gate.py` 차이 | MAJOR | **수정 수용(개발 정합성 우선)**. 서로 다른 생성 시점/역할로 보이는 두 게이트가 의미상 달라 장기 드리프트 위험이 있음. 단, 후자에 대한 `test_review_request_gate.py`가 실제로 unified 정상/거부 시험을 포함하고 `test_submit_review_request.py`도 직접 통합 경로를 검증하므로 “unified 경로 시험 전무”는 **사실 아님**. 보조 staged 11/11은 mock이라 E2E 증거가 아님. 패키지 빌드 시 어느 소스가 정본인지 확인 후 **필요한 의미/호환성 정합 시험만** 추가. 기존 v0.2.29 설치 ZIP 소급 수정·재배포 금지 |
| staged Base64 ZIP + 인계 문서 | SIMPLIFY | **수용**: 이미 정식 GitHub 바이너리/REQUEST를 쓸 수 있으면 직접 A/B 제출 우선. Base64는 진짜 바이너리 업로드 불가 시 선택적 보조, 초안 작성 후 중단 금지 |
| 자동 보호 위임·비용 한도·enabled_at·READY·UNCERTAIN | KEEP | **수용**: 보호 실행 경계 유지. 무단 변경/재서명/재모델 호출 금지 |
| PUBLIC 전환 뒤 PRIVATE 문구 / 옛 DRAFT | MINOR | **수용(필요한 현행 진입 문서만 최소 정리)**. 모든 과거 이력 삭제·새 STATUS 원장 발명 금지 |
| signer PIN 재생성 중복 | MINOR | **추가 확인 후 최소 수정**. 동일 SHA 재계산이 필요할 수 있으며 기존 승인 서명·원본 경로 보장을 깨는 단순 제거 금지 |
| 미검증 실제 host/API·브랜치 보호 | VERIFY_MORE | **그대로 유지**. 원격 GitHub 체인 PASS ≠ 설치 구조 변경 허용; 공개 main이 서명 권한을 대신하지 않도록 기존 호스트 검증 유지 |

## 4. 한정된 최소 후속 작업·시험

1. 기존 Work에서 `review_request_gate.py`의 **순수 REQUEST·ZIP 정합성 검사**를 Windows LIVE 정책 호환성 판단과 분리하고 `submit_review_request.py`의 게시 전 호스트 파일 필수 의존성을 제거. 실제 호스트 정책 검사는 계속 운영. 기존 `review_staged_submission.py`는 선택적 입력 복원 경로로만 둠.
2. `POLICY-STATIC-V1=USD3` 설치 실측/회귀와 오래된 예제 값의 관계를 표시해 F1을 정확히 정리. 패키지 빌드의 기존 gate source/정본 위치를 먼저 확인하고 F2에 대해서만 최소 일치/호환 시험. 과거 watcher ZIP 불변.
3. 무과금 테스트: GPT만의 실제 신규 요청 A/B 게시·소스 SHA/크기/CRC/pin repo_id 문자열·동일 Work 중복 차단; 보호 호스트의 미허용 scope/예산/만료/변조 입력은 READY·모델 0; 정상 승인 시 신규 요청 1회·영수증 1회; UNCERTAIN/기존 완료는 재실행 0. 신규 유료 시험만을 위해 실제 리뷰를 추가 요청하지 않음.
4. 수정 결과는 현재 Work 내 개발·시험·변경 승인 경계로 관리. 정식 독립 리뷰 1회는 **완료**이며 후속 자동 재리뷰 0, LIVE watcher 설치·키·위임·DB·Task·Notifier 변경 0.

**NEXT_ONE_ACTION:** 위 수용/수정 수용에 해당하는 **GPT 게시기 ②·③ 최소 패치와 무과금 회귀**를 기존 Work에서 구현·검증·GitHub `main` 원격 readback. 호스트 보호 정책·LIVE 운영 변경은 별도 유효 승인이 확인되지 않는 한 실행하지 않음. 새 독립 리뷰를 자동 요청하지 않음.
