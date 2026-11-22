# CoWork 독립 리뷰 단일화·비용/게시 선검사 분리 — 구현 및 운영 전환 경계

- 기준: 2026-11-22 KST / GitHub PUBLIC `wonhwipark/CoWork-Skill-Collab` branch `main`.
- 기존 Work: `COWORK-AUTO-APPROVAL-20261115-001` (신규 Work 생성하지 않음).
- 사용자 결정: 독립 리뷰 한 유형만 사용. CoWork가 리뷰를 가격으로 선택·분류·거부하지 않도록 내부 금액 사전 판단·USD3 고정을 없애고, 스킬별 allowlist가 일반 리뷰 접수를 막는 불합리도 단순화. 실제 Claude 제공자 청구 자체가 없어지거나 무제한 자동 실행이 승인되었다는 뜻은 아님.
- 실제 범위: **GPT REQUEST/PIN 게시기의 개발 코드·회귀 소스 GitHub 게시**. **Windows LIVE 보호 signer/watcher/승인 위임·모델 실행·운영 설정 변경 없음**.

## 1. 확인된 문제와 수정

| 레이어 | 종전 | 이번 변경 | 잔여 |
|---|---|---|---|
| `review_request_gate.check_request_for_publication` | `unified`와 `required_budget=3` 필수 | 신규 `independent`를 기본으로 가격 매개변수 없이 유효 REQUEST·ZIP·정적 `POLICY-STATIC-V1` 확인. `required_budget` 제공 시 명시 거부 | 오래된 `unified/skill/design` 비용 검증 함수는 **고정 이력 호환/호스트 진단용** 유지 |
| `submit_review_request` | 비용 `Decimal(3)` 및 선택적 Windows LIVE 가격 자문 | 게시 단계에서 가격·설정 파일 읽기 모두 제거. `--live-config`는 이전 CLI 호환만 위해 받아도 사용 안 함 | Windows 활성 정책은 **변경 안 됨** |
| `submit_review_request` 스킬 자동 preflight | `--delegated-skill`에 없으면 GitHub Commit A 전 `AUTO_NOT_ELIGIBLE_SCOPE` | 게시자는 스킬 허용 여부를 판정하지 않음. `approval_route=auto`는 희망 경로 표시일 뿐. PIN 검사도 읽기 전용 manual 경로로 고정 | **실제 Windows signer의 scope 검사는 여전히 그대로** |
| 불변 보호 | source pin, ZIP SHA/CRC, 원격 두 커밋, 동일 요청 중복·READY 금지 | 유지 | 운영 보호 signer·권한·모델 호출 자체 미변경 |

- 코드 게시: commit `a21bab69dcf1bd2f4f2525fe36e6b6235be567cf`; 과거 가격 진단 CLI에서 신규 독립 모드가 잘못 노출되는 문제 보완 commit `ea3a4811e5208618fcb714786086b596fdf86f99`. 파일별 원격 Git blob 재조회 확인.
- 변경 코드 2개·회귀 소스 2개: `collab/ops/review_request_gate.py`, `collab/ops/submit_review_request.py`, `collab/ops/tests/test_review_request_gate.py`, `collab/ops/tests/test_submit_review_request.py`.
- 테스트 추가: 가격 설정 손상/유무와 무관한 게시, 명시 가격 인수 거부, 미등록 policy 거부, 잘못된 자동 scope·미제공 scope라도 REQUEST 게시 가능/서명 및 READY 불가. 기존 고정 입력·중복 회귀 보존.
- 판정: `SOURCE_EDIT=PASS`; `REMOTE_READBACK=PASS`, `STATIC_CONTRACT_ASSERTIONS=20/20 PASS`(실제 Python 단위시험 아님); `PYTHON_TEST=NOT_RUN`(이 GPT 연결에서 GitHub 소스를 Python 컨테이너로 내려받는 네트워크 미제공); `WINDOWS_LIVE=UNCHANGED`; `INDEPENDENT_REVIEW=NOT_REQUESTED`; `MODEL_CALLS_THIS_CHANGE=0`.

## 2. Windows 전환 목표 — 아직 구현/설치 아님

요구 체계는 **한 종류의 독립 리뷰**: GPT 사용자 지시 → GitHub REQUEST/ZIP Commit A·SOURCE_PIN Commit B → Windows 검증/권한 확인 → 유효 승인·서명 후 READY → Windows Claude Code 독립 리뷰 **한 번** → 결과·영수증 → GPT 판정.

- 새로운 요청에 대한 Windows 가격 기반 정책 선택, 건당 USD3 일치·가격 기준 거부, 리뷰 등급별 모델/금액 판단은 **제거 목표**. 구형 REQUEST와 증거의 `run_policy_ref`는 해석 이력 및 포맷 호환을 위해 훼손하지 않음. 기존 설치본의 Validator/Signer/Watcher 소스와 호출 사슬을 Windows에서 확인한 후 한 변경으로 이관.
- `skill_id`는 역할/추적용 메타데이터로 유지하되 **새 리뷰 승인 판단의 스킬별 allowlist**는 일반 독립 리뷰 capability로 대체하는 후보. 단, GitHub는 현재 PUBLIC이므로 **공개 REQUEST 문구나 GPT가 쓴 승인 주장 자체를 실행 권한으로 신뢰하지 않음**. 실제 승인된 실행 주체와 고정된 원본에 결속된 보호 signer 자격/위임이 필요. 서명 또는 인증된 사용자 리뷰 의도 검증 없이 단순히 allowlist를 삭제하는 것은 불수용.
- 제거하면 안 되는 장치: PIN SHA/크기/내용 검증, 비밀·허용 소스 범위, 정식 권한, Ed25519 서명·READY 마지막, 동일 Work·ID·revision 중복/UNCERTAIN 봉인, `max_model_calls=1`, 영수증·실패 시 재호출 금지. 내부 건별 가격 제한 제거는 비용 청구 여부와 별개이므로 실제 계정 청구·사용량의 사후 관찰은 가능하나 **실행 자격 판정에 다시 섞지 않음**.
- 전환 시 원본 보존: 기존 서명/READY/REQUEST/영수증·DB/WAL/SHM·설치 패키지 원본은 그대로; 구요청 소급 재평가 금지. 격리 dev 후보·모의 signer/expired/unauthorized/tampered/duplicate/replay/permission 회귀→독립 검토 필요시 별도 유효 지시→호스트 백업·롤백→실제 승인 범위에 따라 LIVE 적용→readback.
- LIVE 기존 v0.2.29를 GPT 코드 게시만으로 바꿀 수 없음. `SCOPE`로 대기했던 `REQ-COWORK-P1P2-CONTEXT-CODE-R1-20261122`나 미정산 legacy를 조용히 재서명/READY/재디스패치해서는 안 됨.

## 3. 다음 실행 한 가지

Windows Claude Code가 현 LIVE v0.2.29의 보호 signer/validator/watcher 호출 경로를 먼저 **읽기 전용** 확인하고, 그 결과에 근거해 기존 Work에서 수정 가능한 격리 소스·무과금 시험·개발 후보 패키징까지 진행. 운영 설치/위임/서명·READY 변경은 유효 승인 및 실호스트 검증 전 **NOT_RUN**. 이 과정에서 새로운 유료 리뷰는 요청하지 않음.
