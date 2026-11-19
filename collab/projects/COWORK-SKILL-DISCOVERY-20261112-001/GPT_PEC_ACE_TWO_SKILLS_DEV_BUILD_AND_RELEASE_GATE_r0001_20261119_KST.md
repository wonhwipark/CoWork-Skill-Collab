# PEC-HOP Code Analyzer + ACE Workflow 2종 최소 수정 개발 ZIP·배포 게이트 판정 r0001

- 작성: 2026-11-19 KST / 기존 Work: `COWORK-SKILL-DISCOVERY-20261112-001`
- 최신 사용자 명시 지시: **“상위 두개만 스킬변경후 패키지 배포해줘”** → `code-analyzer` PEC-HOP(P1), `l1-fix-workflow` ACE(P2)만 개발·패키징·시험·L1Work 정식 최종 ZIP 게시까지 승인된 범위에서 진행. 기존 전체 ACE/PEC/ACON v1.6.73 개발 결과와 구별. `ACON=DEFER`; `work-ledger-kernel`, `l1-knowledge-updater`, `skill-updater` 변경 0.
- **현재 판정:** `TWO_DEV_ZIPS=BUILT_VERIFIED`, `SYNTHETIC_PACKAGED_TEST=22_PASS`, `BASE_SOURCE_PRESERVATION=PASS`, `REPRODUCIBLE_ZIP=PASS`, `INDEPENDENT_NEW_CODE_REVIEW=NOT_RUN`, `ACTIVE_BUSINESS_HOST_G0=NOT_EXTERNALLY_OBSERVABLE`, `PUBLIC_FINAL_SKILL_ZIP=BLOCKED_NOT_POSTED`.
- 업무 Linux의 코드·Evidence·로그·설치·시험·결과는 **NO_EXPORT**. 실제 활성본/효과를 추정하지 않음. 업무 GPT의 현장 평가/영수증은 업무 환경에서 보존. 외부 비민감 요약 자동 회신 요구 0.

## 1. 실제 두 스킬 수정

| 스킬 | 기반 source pin | 버전·수정 내용 | 기존 동작 및 호환 |
|---|---|---|---|
| `code-analyzer` | PRIVATE `collab/projects/L1-WORKSPACE-RAG-20261111-001/candidates/code-analyzer_v0_15_3_1114.zip`, SHA-256 `dbbd0f9fd4d5173b8f445aa2fabd9f7417593ecd996ac0e2f0ad10278f3626c2` | **v0.15.4**: `scripts/ca_core/pec_hop_excerpt_readonly.py` 새 순수 모듈; `reuse_validator.validate(manifest,resolution,requested_baseline=None,pec_claims=None)`에서 **명시적 opt-in** `pec_excerpt_integrity`를 결과에 추가 | 기본 reuse 판정/기존 JSON output schema 무변경. 검증된 원본 권한·revision/sha256·raw byte offset/length/발췌를 모두 받았을 때 PASS. stale/미확인 HOLD, 변조 FAIL. 파일/SCM/모델/Knowledge write 0 |
| `l1-fix-workflow` | PRIVATE `collab/projects/L1-WORKSPACE-RAG-20261111-001/candidates/l1-fix-workflow_v1_6_70_1117.zip`, SHA-256 `1e08302b6a533d2894101427f5a7bb94b43102e00a98f2c6e0b19f534a885ceb` 및 MSC v1.6.72 선행 패치 보존 | **v1.6.74**: `l1_fix_workflow/ace_resume_readonly.py` 새 순수 모듈; `work_inspection.inspect_work`에 `ace_scope`/`ace_subject`가 명시된 경우에만 `ace_latest_decision_candidate` 추가 | 기본 Work 조회 결과에 새 키 없음. 원본 journal·권한·source/order/범위 불충족 때 HOLD; 현재 결정을 사용자 승인으로 자동 확정하지 않음. Work/Kernel/지식·Git writer 변경 0, 기존 MSC opt-in 보존 |

**주의:** Code Analyzer의 `pec_claims`는 신뢰된 업무 host producer가 raw byte/권한을 확인해 전달할 때만 의미가 있는 **선택적 Python API**. Workflow ACE도 원문 decision journal에 scope/subject/verified authority/append-index가 있을 때만 선택 후보를 제시. 현장 기존 Agent가 실제 선택적 인자를 넘기고 정확한 원문 근거를 제공하는지 아직 미실측. 따라서 **개발 ZIP에 함수가 연결된 것과 실업무 통합 E2E/효과 개선은 다르다**.

## 2. GitHub Actions 직접 수행·재현 결과

- [PRIVATE main Actions run 44453442652](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/44453442652), head commit `cc28d9e5d46b2ff6035de23fae49a307fad5092b`, job **SUCCESS**.
- 대상 두 버전은 `development_not_for_deployment`. **최종 PUBLIC 배송본으로 채널 변경·가장하지 않음**.
- `code-analyzer_v0_15_4_1119.zip`: **515,271 B**, SHA-256 **`ca1e4cd2d89afd5bf35ce49cab4d2034e93650ffb50a3e713db28eb65b758d21`**, ZIP 217 files / hash manifest 216 entries, **12 synthetic unit tests PASS**, 전체 ZIP CRC/manifest/version/compile PASS.
- `l1-fix-workflow_v1_6_74_1119.zip`: **760,040 B**, SHA-256 **`546936c3856ef19e212ecea3076446d7c75d89db6fcb5ff34df77981024edcd6`**, ZIP 311 files / hash manifest 310 entries, **10 synthetic unit tests PASS**, 전체 ZIP CRC/manifest/version/compile PASS.
- **원본 보존 추가 게이트 PASS:** Code Analyzer 원본 216 files 중 210개 완전 바이트 동일, 변경 6개는 기존 `reuse_validator.py`·SKILL/버전/릴리스/매니페스트만, 새 PEC Python 파일 1개. Workflow 원본 310 files 중 303개 완전 바이트 동일, 변경 7개는 기존 MSC `scenario_msc.py`, 새 Work inspector·SKILL/버전/릴리스/매니페스트, 새 ACE Python 파일 1개. 파일 유실 0·의도하지 않은 신규 파일 0·예외 범위 밖 기존 내용 변경 0.
- **2회 독립 재빌드에서 각각 ZIP byte-for-byte PASS** (2개 `cmp`), 입력 SHA pin 검사 PASS. code-analyzer candidate 원본 SHA 최초 예상값 오류는 빌드 preflight `PIN_MISMATCH`로 실패 차단됐고 실제 GitHub CI 산출 `dbbd0f9...`로 pin을 정정 후 PASS. Source pin 건너뛰기 0.
- PRIVATE GitHub Actions artifact `pec-ace-two-skill-development-1119`, ID `14496133294`, run `44453128562`는 초기 22 PASS 후보이며, **최종 source-preservation 추가검증까지 포함한 실행은 run 44453442652**. 최신 결과·패키지는 위 CI run의 같은 artifact 이름·해당 run id로 조회. 아티팩트는 기한부 개발 보존이지 L1Work 최종 전달 아님.

## 3. 실제 미완료·차단

- `INDEPENDENT_CODE_REVIEW=NOT_RUN`: 기존 ACE/PEC/ACON **설계** R1은 종료됐지만, 이번 새 두 스킬 코드와 builder는 Windows Claude Code의 별도 **독립 코드 리뷰 근거/영수증 없음**. 새 모델을 무단 호출하거나 과거 유료 리뷰를 재실행/소급하지 않음.
- `RELEASE_CHANNEL=development_not_for_deployment`, `PUBLIC_FINAL_ZIP=BLOCKED_NOT_POSTED`. 일반 릴리스 게이트는 원본·버전·보안·호환/회귀·독립 코드 리뷰·정보등급/채널, 정확한 PUBLIC SHA readback을 요구. 사용자 PUBLIC 배포 지시는 유효하지만 QA 면제 아님. **Job-list v0.4.38 한정 사후 리뷰 예외를 두 스킬로 확대 금지.**
- `HOST_G0=NOT_EXTERNALLY_OBSERVABLE`: 업무 자료·설치본·테스트 결과는 NO_EXPORT; 현장 자체 검증의 PASS를 GPT가 수신한 것처럼 주장하지 않음. 업무 GPT와 허용된 Linux Agent만 실제 설치·업무 사례 1건을 선택해 `PEC-P1~3/ACE-P1~2/SAFE-P1/VALUE-P1` 현장 기준으로 내부 검증 가능.
- `PUBLIC_L1WORK_ROOT=UNCHANGED`: 마지막 확인 시 공개 Workflow v1.6.67 / Code Analyzer v0.15.2. 개발 후보 ZIP을 최종 설치 트리거 경로에 게시하거나 기존 ZIP 덮어쓰기 0. 인증, DB/운영 감시기/키/READY/유료 리뷰/Job·Knowledge writer 변경 0.

## 4. 독립 코드 리뷰용 입력(Windows Claude Code 기존 운영 계약)

- 고정 개발 소스: 이 Work의 `dev/pec_hop_excerpt_readonly.py`, `dev/ace_resume_readonly.py`, `dev/build_pec_ace_two_skills_v1_1119.py`, `dev/test_pec_ace_two_skill_integration_r0001.py`, `.github/workflows/cowork-skill-release-quality.yml` 최신 `main`과 위 **run 44453442652** 패키지 바이트.
- 리뷰 초점: (a) Code Analyzer opt-in **raw bytes provenance**와 untrusted `source_access_verified` flag가 승인 판정으로 오용되지 않는지 (b) ACE raw context_events에서 origin/authority/append-index의 진위가 실제로 인증되는지, legacy decision summaries의 오승격이 없는지 (c) 기존 MSC·Work reader 부수 효과/Git writer·그룹 Knowledge 보호가 기존 스킬과 호환되는지 (d) 새 코드와 이전 배포 계보/SourceSnapshot CAS 및 전체 회귀·정보등급·공개 배송에 문제 없는지.
- Windows reviewer는 실제 LIVE 정책/서명/비용/위임 범위와 독립 코딩 리뷰를 분리. 원본 리뷰 영수증/REQUEST 재큐잉 금지. LIVE의 USD3 미적용/보호 정책 불일치가 해소되지 않았다면 `INDEPENDENT_CODE_REVIEW=NOT_RUN`와 차단 원인만 기록하고 신규 모델 호출·READY/자동 signer 0.
- 새로운 코드 리뷰가 실제 완료되고 차단 결함 해결, 필수 보안/회귀/채널 Gate PASS 뒤에만 **유일 신규 최종 릴리스 ZIP**을 `wonhwipark/L1Work/main` 루트에 게시·원격 raw ZIP SHA 검증. 정확한 최종 ZIP SHA는 개발 후보 SHA와 다르므로 추정하지 않음.

## 5. 다음 한 행동

**NEXT_ONE_ACTION:** 기존 CoWork Work의 Windows Claude Code 운영 계약을 통해 **두 패키지의 신규 코드 독립 리뷰·최종 공개 릴리스 게이트**를 검증한다. 통과하면 기존 사용자 공개 배송 지시를 재승인 없이 실행; 실패/NOT_RUN이면 `BLOCKED_NOT_POSTED` 유지·근거 보존. 현장 G0·실업무 수용 시험은 업무 환경에서만 수행·보존, 외부 완료 인식 불가.
