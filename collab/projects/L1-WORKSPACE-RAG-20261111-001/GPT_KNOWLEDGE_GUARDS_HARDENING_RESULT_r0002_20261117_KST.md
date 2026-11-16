# L1 지식 보호 스킬 3종 추가 보완 결과 r0002 — PUBLIC 자동 게시 기본 지시 적용

- 날짜: 2026-11-17 KST
- Work: `L1-WORKSPACE-RAG-20261111-001`
- 사용자 최신 지시: **세 스킬 업로드 및 앞으로 최종 스킬 ZIP 자동 게시**
- 원본 사용: `l1-fix-workflow v1.6.69` / `l1-github v0.3.57` / `work-ledger-kernel v0.7.42`
- 개발 branch: `dev/l1-knowledge-guards-20261117`
- 최신 CI: [L1 knowledge guard hardening QA once, 43909570584](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/43909570584), **SUCCESS**
- 결과 상태: `BUILT=PASS`, `SOURCE_PIN=PASS`, `TARGETED_QA=PASS`, `PUBLIC_RELEASE=BLOCKED_NOT_POSTED`, `HOST_G0=NOT_VERIFIED`, `INDEPENDENT_CODE_REVIEW=NOT_RUN`

## 1. 최소 구현 변경

1. `l1-fix-workflow v1.6.70`: 개인 `knowledge/`에 대한 Workflow writer `changed_files`/`extra_paths`의 경로 이탈·symlink·상대경로·대소문자 변경 검사를 추가. Updater 단독 writer 경계는 실행 호스트에서 검증 필요.
2. `l1-github v0.3.59`: Work-docs commit/push의 staged/unstaged/untracked `knowledge/` 변경 거부에 더하여 **업스트림과 HEAD 사이 이미 커밋된 변경이 `knowledge/`를 수정하면 push 전 fail-closed**하도록 수정. tracking branch 부재·검증 실패도 거부. raw Git을 별도 credential로 실행하는 우회는 이 함수만으로 차단 불가.
3. `work-ledger-kernel v0.7.43`: exporter의 `knowledge/` 경로 보존·symlink 안전 조건, 개인 Knowledge README 존재 시 루트 README 탐색 링크 추가; Knowledge ref_type/profile 신규 확장 없음.

## 2. 패키지/빌드 근거

| 스킬 | 신규 후보 ZIP | 크기 | SHA-256 (CI, GitHub PRIVATE 개발 브랜치) |
|---|---|---:|---|
| Workflow | `l1-fix-workflow_v1_6_70_1117.zip` | 758117 B | `a3070d3cfd64d78da7a684f8d81fc35ea323c3667d539a61d16bf5ac6fe40878` |
| GitHub | `l1-github_v0_3_59_1117.zip` | 567266 B | `85f7e95372027a326a41b0d17e7df4d630115c468c0745236fb24ca68b19fcb0` |
| Kernel | `work-ledger-kernel_v0_7_43_1117.zip` | 319793 B | `0e178e651c2a53175a5ddce2dae68e07f11141b4a92a6b94be6126114c5ab95c` |

PRIVATE 경로: `collab/projects/L1-WORKSPACE-RAG-20261111-001/dev/output/` (branch `dev/l1-knowledge-guards-20261117`). `BUILD_RESULT.json`과 패키지 3종을 해당 branch에서 재조회해 존재를 확인. CI는 원본 baseline SHA 고정, Python compile, ZIP CRC·path/symlink/중복, manifest hash, 제한된 기능시험을 수행. 위 SHA는 `BUILD_RESULT.json`과 CI 로그 근거이며, 정확한 원격 바이트 해시가 필요한 최종 PUBLIC 게시에서는 **다시 다운로드하여 대조**할 것. 개발 후보 세 ZIP 모두 `.skill-release.json.channel=development_not_for_deployment`.

## 3. 시험 결과·한계

- GitHub CI 전체 SUCCESS(2026-11-17 KST), Workflow 경로 차단 smoke PASS.
- Git Work-docs staged/unstaged/untracked 차단 smoke PASS.
- **새 회귀시험:** tracking upstream 구축, 허용 Work commit 성공, 원격 push 후 **미커밋 변경이 없는 상태의 보호 Knowledge 변경 commit** 생성, outbound guard가 차단함을 확인: `GITHUB_COMMITTED_KNOWLEDGE_DENY_PASS`.
- 실제 `work_ledger_kernel.WorkLedgerKernel.work_docs_export`를 격리 임시 디렉터리에서 연속 2회 수행해 `knowledge/README.md` 및 개인 변경 문서 SHA-256 보존·루트 탐색 링크를 확인: T01/T02 PASS(격리).
- **여전히 NOT_RUN/NOT_VERIFIED:** 원격 동시 writer lock/실제 CAS/credential 분리, raw Git 우회 및 실제 설치본 G0, 그룹 writer 실제 승인·병합/게시·readback, Work-side origin link, 전체 기존 회귀, T03~T10, Windows Claude **코드** 독립 리뷰. 이전 Claude R1은 **설계** 정적 리뷰만 수행.

## 4. PUBLIC 자동 게시 기본 정책

사용자의 2026-11-17 최신 지시를 [PUBLIC 배송 계약](../../ops/CONTRACTS/JOBLIST_PUBLIC_DELIVERY_V1.md)에 반영. 앞으로 GPT의 스킬 개발 작업에서는 릴리스 게이트 PASS인 새 ZIP을 **별도 반복 질문 없이** `wonhwipark/L1Work/main` 루트로 게시 및 remote SHA-256 대조. 단 개발 후보/미검증 코드·정보 등급 위반/운영 하드 가드 미충족은 자동 게시 대상에서 제외하고 `BLOCKED_NOT_POSTED`를 보고. 별도 무인 에이전트나 스케줄러·신규 토큰 설치/활성화는 이번 사용자 지시로 이미 완료된 것처럼 처리하지 않음.

## 5. GPT 판정·다음 동작

**`CODE_CANDIDATE=PASS_TARGETED_QA` / `PUBLIC_RELEASE=BLOCKED_NOT_POSTED`.** 사용자 PUBLIC 게시 지시는 인정되지만, `development_not_for_deployment` ZIP을 자동 설치 경로에 릴리스로 게시하지 않음. 현 세 패키지의 PUBLIC 경로는 만들지 않음. 기존 PUBLIC ZIP 바이트는 유지.

다음 한 동작: 업무 GPT의 실제 writer/호스트 OS·Git credential 경계 G0 결과 및 기존 동시성/CAS 계약을 수령·검증하고, 검증 가능한 추가 최소 패치/회귀/코드 리뷰를 마친 신규 릴리스 ZIP만 승인된 자동 게시 흐름으로 업로드할 것.
