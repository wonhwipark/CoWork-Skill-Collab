# PEC-HOP·ACE 2스킬 독립 코드 리뷰 → L1Work 최종 ZIP 릴리스 원샷 r0001

## 2026-11-19 KST 사용자 최신 명시 리뷰 요청 — Windows 실행 대기

- **신규 지시:** 사용자 “리뷰 요청해줘”. 이 파일 자체를 **Windows Claude Code 독립 코드 리뷰를 위한 명시적 요청 인계**로 갱신. 리뷰 대상은 `code-analyzer_v0_15_4_1119.zip` (PEC-HOP)과 `l1-fix-workflow_v1_6_74_1119.zip` (ACE), **한 번의 결합 R1 신규 코드 리뷰**. ACON·Kernel·Knowledge Updater 제외.
- **고유 요청 후보 ID(아직 정식 게시 아님):** `REQ-COWORK-PEC-ACE-TWO-SKILLS-CODE-R1-20261119`. 이름만 예약한 **INTENT**, `collab/requests/<ID>/REQUEST.md` 및 `collab/packages`·`SOURCE_PIN.json`·`APPROVAL_SIG`·`READY` **미게시**. 기존 설계 R1 및 다른 요청/영수증 재사용·재큐잉 금지.
- **Windows Claude Code에 대한 작업 지시:** 이 PRIVATE 저장소 `main` 최신 CURRENT와 이 문서, 정확한 코드 4종 및 2026-11-19 run `44453442652`의 두 실제 ZIP 바이트를 확인. 이후 **설치된 Windows LIVE 설정 및 유효 보호 위임을 직접** 확인해 정책 `--intent unified --required-budget-usd 3.00` preflight → 리뷰 입력 원문·패키지 생성 및 SHA/크기 고정 → user approval scope·서명권한/만료·기존 pending/UNCERTAIN 중복 검사 → 허용된 계약에서만 신규 REQUEST/패키지 commit A → 원격 readback/SOURCE_PIN → 승인/서명 및 READY 마지막 게시 → 유효 요청 1회 독립 리뷰 → 리뷰 결과·비용 영수증 PRIVATE main readback, CURRENT/기존 TRACKER 갱신. **단순 텍스트 게시로 Windows 작업이 자동 실행됐다고 주장하지 않음**.
- **차단 조건:** 마지막 관측 Windows STATIC $1.50 / 보호 위임 $1.00과 신규 USD3가 불일치. 실제 호스트 preflight `PASS` 확인 전에는 정식 REQUEST/READY/유료 호출 금지. 다른 요청용 수동 USD3/DESIGN 예외·호스트 보호 정책/키/운영 설정 강제 변경·소급 승인 금지. 미충족이면 `REVIEW_REQUEST=HOST_PREFLIGHT_BLOCKED`, `INDEPENDENT_CODE_REVIEW=NOT_RUN`으로 결과를 이 Work에 기록.
- **최종 회신:** 새 코드 리뷰 결과/영수증 URL, 실제 독립 reviewer 판정, 지적사항의 최소 보완·재시험, L1Work 최종 ZIP 공개 릴리스 게이트/실제 게시 여부를 구분. 업무 Linux 설치/실증은 NO_EXPORT와 무관하게 **업무 환경 내부 전용**, 외부 PASS 추정 금지.

---

- 대상 저장소: `wonhwipark/CoWork-Skill-Collab` PRIVATE, branch `main`
- 기존 Work: `collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/`
- 실행 담당: Windows Claude Code **독립 리뷰 세션** (개발/자체시험과 분리); GPT는 판정·최종 PUBLIC 게시.
- 사용자 최신 지시: `code-analyzer` PEC-HOP, `l1-fix-workflow` ACE **두 스킬만 수정하여 L1Work에 배포**. ACON·Kernel·Knowledge Updater·skill-updater 변경 금지. 업무 Linux 원본·로그·Work ID·호스트 테스트 결과는 **NO_EXPORT**; 비민감이라고 추측하여 외부 회신시키지 않음.
- 검증된 실제 개발 패키지(최종 릴리스 아님):
  - `code-analyzer_v0_15_4_1119.zip` **515271 bytes / SHA256 `ca1e4cd2d89afd5bf35ce49cab4d2034e93650ffb50a3e713db28eb65b758d21`** / PEC 내부 12 PASS
  - `l1-fix-workflow_v1_6_74_1119.zip` **760040 bytes / SHA256 `546936c3856ef19e212ecea3076446d7c75d89db6fcb5ff34df77981024edcd6`** / ACE 내부 10 PASS
  - [GitHub Actions run 44453442652](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/44453442652) `success`, source commit `cc28d9e5d46b2ff6035de23fae49a307fad5092b`: 2회 byte-identical build, CRC/all-manifest/version/compiler/scope preservation PASS, 각각 기존 파일 삭제 0·뜻밖의 기존 코드 변경 0
  - 해당 run의 PRIVATE 기한부 artifact: `pec-ace-two-skill-development-1119`, ID `14496641478`, 2026-11-26 UTC 만료. 원본 ZIP pin과 빌더가 PRIVATE main에 유지되므로 재현 가능.
- 개발 코드: `dev/pec_hop_excerpt_readonly.py`, `dev/ace_resume_readonly.py`, `dev/build_pec_ace_two_skills_v1_1119.py`, `dev/test_pec_ace_two_skill_integration_r0001.py` 및 `.github/workflows/cowork-skill-release-quality.yml`.
- 상세 실제 QA/릴리스 판정: [GPT 2스킬 DEV 빌드 결과](GPT_PEC_ACE_TWO_SKILLS_DEV_BUILD_AND_RELEASE_GATE_r0001_20261119_KST.md).

## 0. 사전 정합성 (유료·호스트 보존 게이트)

1. 최신 `collab/CONTEXT_BRIEF.md`, 이 Work `CURRENT.md`, 두 스킬 개발·CI/원본 근거를 읽되 유효한 동일 목적의 리뷰/영수증 중복·불확실 항목을 먼저 확인. 과거 ACE/PEC/ACON **설계 R1 CLOSED**는 이 코드의 독립 리뷰가 아님.
2. Windows LIVE `collab/ops/review_request_gate.py select/check --intent unified --required-budget-usd 3.00`에 필요한 실제 로컬 `reviewer.config.json`·실행자의 보호 위임·승인/서명 만료·소급 요청 안전성을 **읽기 전용으로 확인**. 마지막 확인 기준 `STATIC` USD1.5·보호 위임 USD1, 단일 USD3는 미설치. `POLICY_COST_MISMATCH`, 보호 위임 미적용, 승인 불명확, 토큰 만료, 중복이면 **새 REQUEST/SOURCE_PIN/APPROVAL_SIG/READY/모델 호출 0**. 정책/비용/키/DB/Watcher를 이 리뷰 때문에 우회 수정하지 않음.
3. 실 LIVE와 사용자 기존 유효 승인 범위가 일치할 때만 **신규 요청**을 고정 원본·패키지 해시·저장소 repo_id 문자열로 만들고, 기존 독립 리뷰 승인·서명 보호 정책을 준수. REQUEST→원격 raw hash→PIN→기존 승인/서명→READY 마지막→watcher 실행/영수증 1회. 기존 R1 재사용·소급 서명·모델 재호출 금지.

## 1. 새 코드 독립 리뷰 범위 (2스킬 변경만)

| 항목 | 필수 확인 |
|---|---|
| PEC opt-in 검증 | `ca_core.reuse_validator.validate(...,pec_claims=...)` 기존 무인자 동작 및 `reuse_status` 보존. `source_access_verified=True`는 **caller 자체 선언일 뿐 실제 권한/출처 인증은 host 책임**. 무단 외부 입력·이미 변경된 원본과 동일하게 조작된 발췌로 잘못 PASS하지 않는지 점검 |
| PEC raw 바이트 | source revision pin, 전체 SHA256, offset/length, excerpt raw bytes 1-byte 변조·Unicode·CRLF·stale/누락·권한 거부가 각각 FAIL/HOLD. 바이트/원문을 외부 로그·output에 복제하지 않음 |
| ACE work inspector | 기존 `inspect_work` 기본 결과·Work 조회·기존 MSC 기능 무퇴행. `ace_scope/ace_subject` 명시 opt-in에서만 후보 파생. 요약에 원문 ref/순서 없으면 HOLD, 승인/철회/중복 append·타 Work/다른 scope 판별 정확 |
| 외부/업무 경계 | 기존 Git/P4/Kernel/Knowledge writer, 예약 작업·모델/Job/READY 호출·외부 반출 0. 현장 실제 수행 결과를 외부 GPT에 요구하지 않음. 공유된 공개 코드가 회사 원본에 의존하지 않는지 비민감 diff와 ZIP만으로 감사 |
| 호환·배포 | 전체 ZIP 이전 파일 보존/버전·메타데이터·CRC·manifest·ZIP path escape·심링크/비밀정보. 빌드의 `development_not_for_deployment`을 리뷰 없이 최종 채널로 변경 금지. 기존 PUBLIC 원본 및 v1.6.72 MSC patch 보존 |

- 리뷰어는 구체적 실패·변경량·재현 가능한 결함/반례와 PASS/FAIL/NOT_RUN을 분리하고, 자체 CI 22 PASS를 독립 리뷰로 취급하지 않음.
- 결과·영수증은 기존 Work에 반환; GPT가 minimal fix 및 가능하면 동일 범위 회귀, 승인된 전체 릴리스 게이트를 판정. 실제 Windows review가 불가해도 현재 코드·시험·기존 HISTORY는 보존.

## 2. 최종 L1Work/main 루트 배송 (리뷰 및 릴리스 게이트 전부 충족 시에만)

1. 두 스킬을 새 독립 코드 리뷰 판정에 따라 필요한 최소 수정·전 범위 회귀/보안/호환·민감정보 확인. 최종 bytes/channel/source SHA·size/CRC/파일명 고정. 개발 ZIP 바이트를 이름/채널만 바꿔 정상 릴리스라 주장하지 않음.
2. 사용자가 이미 허용한 PUBLIC 패키지 배송은 **추가 확인 질문 없이** 수행 가능. 단 해당 최종 범위와 실제 유효 승인·필수 게이트 PASS가 성립해야 함. `wonhwipark/L1Work`, branch `main`, **루트**에 신규 고유 파일 2개를 게시, 기존 ZIP 덮어쓰기 0. GitHub 공개 bytes 재다운로드 SHA256·크기·commit/Git blob을 대조하고 `CURRENT.md`/`TRACKER.json`에서 각 스킬별 `PUBLIC_POSTED` 정산.
3. 업무 Linux의 `skill-updater` 설치·활성화·실업무 이득 검증은 업무 GPT/Agent 내부 전용. 외부 정본은 `HOST_E2E=NOT_EXTERNALLY_OBSERVABLE`로 유지하며, PUBLIC ZIP 존재를 업무 설치 PASS로 승격하지 않음.
4. 리뷰/권한/호환 게이트 하나라도 실패 또는 미검증이면 `FINAL_PUBLIC_ZIPS=BLOCKED_NOT_POSTED`와 정확한 사유를 남김. 개발 후보 아티팩트를 PUBLIC에 밀어 넣거나 기존 활성 설치를 추정·우회하지 않음.

**최종 실행 프롬프트:** PRIVATE `wonhwipark/CoWork-Skill-Collab` `main`의 이 인계서를 기준으로 단 한 번 Windows 독립 코드 리뷰 가능성을 조회→유효할 때만 정식 신규 리뷰→GPT 최종 판정·최소 보완/회귀→허용된 최종 두 ZIP만 PUBLIC `wonhwipark/L1Work` `main` 루트 배송·원격 해시 검증. 접근 불가 단계는 `NOT_RUN/BLOCKED`만 분리, 기존 Work/영수증 및 실업무 보안 경계 보존.
