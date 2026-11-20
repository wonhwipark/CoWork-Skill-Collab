# GPT 판정 — v0.2.29 보안 경합 / CAS 재시도 / 독립 리뷰 / writer 실연결

- 판정: 2026-11-20 KST
- 정본: PRIVATE wonhwipark/CoWork-Skill-Collab, branch main
- Work: COWORK-AUTO-APPROVAL-20261115-001 (기존 Work 사용)
- 고정 후보: artifacts/v0_2_29/skill-collab-watcher_v0_2_29_1120.zip
- ZIP SHA-256: c67bc342fe77547b000fc42e1b886396cbef035c0d265dbcd124947e267ed83f / 310753 bytes. 바이너리 변경 없음.
- 선행 증거: CLAUDE_V029_SU_L1_AND_FIVE_WINDOW_RECOVERY_RESULT_FOR_GPT_20261120.md 및 이전 GPT_V029_SU_L1_RACE_AND_FIVE_WINDOWS_RECOVERY_DISPOSITION_r0001_20261120_KST.md

## 1. 증거와 상태

Windows 개발자 자체시험 보고: 실제 v0.2.29 ZIP을 매회 독립 임시 폴더/DB/키·fake Github에서 5회 실행하여 전회 전체 회귀 1038 PASS, 12 SKIP, 0 FAIL, 5개 창 동반 시험 전회 PASS. 설계 2/스킬 수정 3의 READY 각 1회, 재처리 추가 서명·PUT 0, CLI 가짜 runner 총 5회, 재시작 재호출 0. 이는 독립 reviewer 결과나 LIVE 운영 검증이 아님.

과거 round 1 su_l1 FAIL과 약 31회 중 2회 실패 이력은 유지. 실패 회차의 실제 원인 출력이 없어 SU_L1_OBSERVED_ROOT_CAUSE=UNRESOLVED. Windows 무잠금 anchor read vs os.replace 경합에서 PermissionError 296/40000 재현, 주입 10/10 안전 불변식 검증은 원인 가설·안전성 보강 근거일 뿐 관측 실패와 직접 인과 증명은 아님.

writer mock: 19 unit PASS, 5개 창/5회 mock PASS, 실제 GitHub·실제 스킬 저장소·운영 DB E2E NOT_RUN. watcher 운영 LIVE v0.2.25, 보호 위임 USD1, 신규 유료 모델 호출/실제 REQUEST/READY/서명 0.

## 2. 결정 ① SECURITY_RACE

**SECURITY_RACE=CONDITIONALLY_ACCEPTED_FOR_INDEPENDENT_REVIEW_ONLY.**

su_l1은 watcher 운영 DB를 사용하는 경로가 아닌 별도 로컬 계약 실험. 주입/경쟁 시험에서 수락 1회, nonce 재사용 차단, 로그·앵커 정합성, 신규 nonce 처리, 임시 파일 정리가 보존된 근거가 있음. 잔여 위험은 *일시적 가용성 저하 가능성*으로 등록. 단, 관측 실패 직접 원인은 미확정이므로 안전성/원인 해결을 단정하지 않고, 독립 reviewer가 LIVE 차단급 보안 영향인지 판단해야 함.

원래 su_l1 원본 시험의 기대값 완화/삭제/skip/xfail 금지. 기존 FAIL 이력 보존. 추가 반복 계측을 독립 리뷰 이전의 무한 게이트로 만들지 않음. 리뷰어가 실제 불변식 위반 또는 운영 영향이 있는 보안 취약점을 재현할 경우 RELEASE HOLD, 정확한 최소 패치 + 관련 시험으로 복귀. SECURITY_RACE는 LIVE 수용이나 ROOT_CAUSE_FIXED가 아님.

## 3. 결정 ② CAS 호출자 재시도

**CAS_RETRY=BOUNDED_IDEMPOTENT_CALLER_RETRY_ACCEPTED.**

기존 Work 산출물 artifacts/v0_2_29/validation/work_writer/work_writer.py 에서 cas_update(max_retries=3)는 실제 1호출당 최초 1회 + 내부 충돌 재시도 최대 3회 = 총 최대 4회의 PUT 시도. 완전 동시 5창에서 소진 4회(5라운드 합계) 후 호출자 멱등 재호출로 정상 복구한 Windows mock 증거 수용.

호출자는 CasExhausted stale blob SHA일 때에 한해 **같은 Work ID/논리 변경/멱등 merge를 최대 1회 추가 호출**. 두 wave의 총 시도 상한 최대 8, 각 wave에서 remote 최신 SHA fetch, bounded jitter/backoff 및 readback. remote 결과가 이미 반영됐다면 두 번째 put 없이 성공 처리. last-writer-wins, force push, 무한 재시도 금지. auth 실패·내용 해시 불일치·readback mismatch·의미 충돌에서는 자동 재호출 금지. 두 wave 소진시 POST_CONFLICT_PENDING + 증거 기록, 다른 Work만 진행. 모델/리뷰/Job 재실행 0.

동일 Work에 서로 상충하는 phase/next_action 갱신이 들어오면 단순 덮어쓰기 금지. 최신 근거/Work 상태로 병합하고 의미 충돌 시 NEEDS_DECISION.

## 4. 결정 ③ 유료 독립 리뷰 진입

**V029_TECHNICAL_READY_FOR_PAID_INDEPENDENT_REVIEW=YES_WITH_DISCLOSED_SU_L1_EXCEPTION.**
**REVIEW_TRANSPORT=HOST_PREFLIGHT_REQUIRED, INDEPENDENT_REVIEW=NOT_RUN.**

범위: 정확한 위 v0.2.29 ZIP SHA에 대한 신규 독립 리뷰 R1 한 건. v0.2.28 MAJOR 소급 비용 거절 차단, 실패 지속성, 5창 중복 서명/READY, 재시작/UNCERTAIN, su_l1의 미해결 경합/운영 영향 여부를 명시적 평가 항목으로 포함. Work-only writer helper는 ZIP 밖의 별도 개발 내용이므로 독립 watcher 리뷰 입력과 무단 혼합 금지.

기존 REVIEW_TIER_TOKEN_BUDGET_V1.md의 일반 정책은 신규 리뷰당 USD3 / 모델 호출 최대 1회 사용자 승인으로 기록되어 있으나 Windows LIVE 운영 STATIC USD1.5, 보호 위임 USD1이므로 unified STATIC USD3 자동 승인·서명은 미설치. **사용자 일반 예산 승인과 유효한 개별 host 실행/서명 범위를 구별**. 실제 설치 정책을 먼저 read-only preflight (review_request_gate select/check, source zip sha, scope, PIN repo_id 문자열, signer ACL, legacy pending/UNCERTAIN, rollback) 수행. 등록되지 않은 unified 정책이나 과거 특정 UI Work용 DESIGN3 수동 예외를 우회 사용 금지.

정식 REQUEST 게시, SOURCE_PIN, protected SIGN, READY 마지막 게시 및 유료 reviewer 1회/최대 USD3은 실제 사전 승인·정책/서명 자격이 모두 확인된 경우에만. 유효 경로가 없으면 REVIEW_REQUEST=NOT_POSTED, REVIEW_TRANSPORT=BLOCKED_HOST_POLICY, 모델 0. 비용 자체를 다시 무조건 승인 요청하는 것이 아니라 현행 호스트 경계의 부족한 항목만 정확히 보고.

독립 리뷰에서 BLOCKING/MAJOR가 재현되면 RELEASE HOLD 후 입력/원인/최소 수정과 관련 시험으로 처리. MINOR/추후 개선 제안을 자동 신규 버전·재유료 리뷰의 원인으로 만들지 않음. PASS라고 해도 운영 설치·위임·SHADOW/롤백·소급 차단 검증은 별도 host gate.

## 5. 결정 ④ writer·정산 실제 연결

**WRITER_INTEGRATION=PROCEED_IN_EXISTING_WORK_AS_SEPARATE_DEV_LANE, WATCHER_ZIP_UNCHANGED.**

Work-only 개발 후보를 영구 방치하지 않고 같은 Work의 별도 DEV 경로로 연결. 다만 watcher github_transport.upload의 create-only 승인/READY 계약은 변경하지 않으며 writer CAS/3-way rebase를 watcher v0.2.29 ZIP에 혼합하지 않음.

1. 기존 Git API, Work/Kernel/Updater·기존 writer를 다시 확인하고 Work 산출물의 mock Contents adapter를 실제 GitHub GET content/blob sha, PUT with sha, remote byte readback에 연계. 먼저 read-only 대상/권한 점검. 유효 승인된 비민감 PRIVATE 테스트 경로만 실제 CAS 쓰기 시험 수행; CURRENT/TRACKER에 시험 마커 오염 금지.
2. 동일 스킬 3건 수정은 실제 허용된 test worktree/branch에서 base HEAD → 최신 HEAD 3-way rebase → 관련 회귀 → SHA pin → 게시 전 확인. 의미 충돌 NEEDS_DECISION은 코드 변경·리뷰 요청 금지. 회사 제한 소스/상세 로그 PRIVATE/PUBLIC 반출 금지.
3. UNCERTAIN 원격 결과 정산은 mode=ro, 정확한 DB processing_key / request revision / package SHA / policy revision, 원격 REVIEW_RESULT·RECEIPT·DISPATCH bytes 비교 및 readback. **현행 Work helper가 processing key 끝에 정책 리비전을 |1로 하드코딩한 점은 실제 DB 연결 전 수정/검증 필요**. 결과 증거가 발견되어도 운영 DB terminal 상태 강제 변경·동일 유료 모델 재호출 금지; SETTLED_BY_EVIDENCE는 읽기 전용 외부 판정으로만 표기.
4. 실제 GitHub/실스킬 저장소/호스트 DB는 아직 NOT_RUN이며, 기존 mock 시험 PASS를 자동 운영 PASS로 승격하지 않음. 이 개발 레인은 watcher 독립 리뷰 사전 준비를 막지 않지만, 완전 자동 교차창 복구 운영 완료를 주장하기 전에는 실제 연결 E2E PASS가 필요.

## 6. Windows Claude Code 다음 한 행동

PRIVATE wonhwipark/CoWork-Skill-Collab branch main, 기존 Work collab/projects/COWORK-AUTO-APPROVAL-20261115-001/CURRENT.md와 본 문서를 읽고 다음을 하나의 무과금 우선 원샷으로 처리.

A: v0.2.29 고정 ZIP의 신규 독립 리뷰 1건에 대한 실제 Windows 정책/승인/서명 가능 여부를 read-only 진단. 유효 승인 아래 policy preflight를 모두 통과하면 이 Work의 정식 REQUEST/READY 및 비용 상한 준수로 1회 리뷰 가능. 아직 불가하면 검증된 BLOCKED_HOST_POLICY 사유를 남기고 모델 호출 0. B: 기존 writer 인터페이스·실 GitHub GET/sha read-only 확인, 최대 2 wave CAS 호출자 규칙과 UNCERTAIN policy revision 동적 고정 DEV patch/mock 시험. 현재 승인된 허용 범위 밖 원격 쓰기/호스트 설치는 시행하지 않음.

독립 리뷰 결과가 나오기 전 LIVE=v0.2.25 / 보호 위임 USD1 불변, 이전 REQUEST·영수증 보존, ZIP 바이트 불변. 결과는 기존 Work 결과 파일 1건 및 CURRENT/TRACKER 필요한 현행 필드만 갱신하고 PRIVATE main 원격 SHA/바이트 readback 확인.

**현재 판정:** ZIP_5X=PASS_HOST_REPORTED, SECURITY_RACE=CONDITIONAL_REVIEW_ONLY, REVIEW_TECHNICAL_READY=YES, REVIEW_TRANSPORT=HOST_PREFLIGHT_REQUIRED, INDEPENDENT_REVIEW=NOT_RUN, LIVE=v0.2.25, AUTO_DELEGATION_USD3=NOT_APPLIED.
