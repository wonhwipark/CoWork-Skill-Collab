# L1 Knowledge 3종 스킬 후보 ZIP QA 및 L1Work PUBLIC 배포 게이트 판정
- 날짜: 2026-11-17 KST / 기존 Work: `L1-WORKSPACE-RAG-20261111-001`
- 사용자 요청: `l1-fix-workflow`, `l1-github`, `work-ledger-kernel` 최신 패키지 작업 후 `wonhwipark/L1Work/main` 루트 게시
- 소스/후보: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `dev/l1-knowledge-guards-20261117`
- CI 실행 증빙: [GitHub Actions 43905367017](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/43905367017), `SUCCESS` (2026-11-17 KST)
- 원본 위치: `collab/projects/L1-WORKSPACE-RAG-20261111-001/candidates/`의 workflow/github, PUBLIC `L1Work/main`의 Kernel v0.7.42
- 이 문서는 비민감 QA/게이트 보고서. 호스트 설치·그룹 지식 생성·운영 권한 수정/모델 재호출 0.

## 1. 개발 패키지 생성·검증

| 스킬 | 기존 버전 → 후보 | 실제 패키지 크기 | 후보 ZIP SHA-256(원격 바이트 직접 대조) |
|---|---|---:|---|
| l1-fix-workflow | v1.6.69 → **v1.6.70** | 758,117 B | `1e08302b6a533d2894101427f5a7bb94b43102e00a98f2c6e0b19f534a885ceb` |
| l1-github | v0.3.57 → **v0.3.58** | 566,777 B | `cad08cba93a147b08b3a1b8a940397cced840fe21d600c5e904e8c597a754ced` |
| work-ledger-kernel | v0.7.42 → **v0.7.43** | 319,793 B | `80c955790aaa65f695c061f7ec2664bd1c7c5ba7e0a7534045960eea7fe2d5f6` |

후보 경로(모두 PRIVATE 개발 브랜치 `dev/l1-knowledge-guards-20261117`):
- `collab/projects/L1-WORKSPACE-RAG-20261111-001/dev/output/l1-fix-workflow_v1_6_70_1117.zip`
- `collab/projects/L1-WORKSPACE-RAG-20261111-001/dev/output/l1-github_v0_3_58_1117.zip`
- `collab/projects/L1-WORKSPACE-RAG-20261111-001/dev/output/work-ledger-kernel_v0_7_43_1117.zip`
- `collab/projects/L1-WORKSPACE-RAG-20261111-001/dev/output/BUILD_RESULT.json`

개발 빌더는 원본 SHA-256 pin, ZIP CRC, 경로 이탈/심링크/중복 검사, Python compile, 후보 스킬 메타데이터(version/archive/channel) 및 기존 manifest digest 재계산을 수행. 후보 3종 원격 파일 전체 바이트를 다시 읽어 보고된 SHA-256과 일치함을 GPT가 재검증. 모든 후보의 `.skill-release.json` 채널은 **`development_not_for_deployment`**이며 최종 배포본 아님.

## 2. 실제 시험 성적과 구분

- CI `build` 전체 SUCCESS. PIN/source 일치, ZIP CRC, Python 컴파일, 기존 digest manifest 대조: PASS.
- `l1-fix-workflow`: `knowledge/` / 대소문자 변형 / `../` / 절대 경로 / symlink 별칭의 Workflow changed-path 거부 표적시험 PASS. group READ/전체 기존 업무 회귀 미검증.
- `l1-github`: Work-docs 경로에서 Git status의 staged/unstaged/untracked `knowledge/` 감지 거부 표적시험 PASS. **미커밋 변경만 검사하므로 이미 커밋된 보호 파일을 raw Git 경로로 push하는 반례를 현재 시험·코드에서 차단 입증하지 못함.** 인증된 writer/권한 분리/직렬화·중복/경합/실제 writer 전체 우회는 NOT_RUN.
- `work-ledger-kernel`: 실제 `WorkLedgerKernel.work_docs_export` 대상에 `knowledge/README.md` 및 개인 수정 문서를 만든 후 exporter 2회 실행, 파일 SHA 보존/루트 링크 존재 확인 **T01/T02 PASS (격리 synthetic)**.
- **미실행:** T03 실제 raw Git/credential 차단, T04 전체 경로 우회/host, T05 동시 writer 경합, T06 허용 Kernel Work-side 역링크, T07~T10 3-way/승인/CAS/원격 게시 실패 복구. 실제 Linux 호스트 G0/E3, 업무 GPT Updater/group writer 실제 계약, 독립 코드 리뷰 1회 결과 없음. Claude 2026-11-16 R1은 **설계 전용**, 코드 독립 리뷰 PASS 아님.
- QA 성공은 격리 개발 시험이며 실제 업무 호스트 접근/설치/게시·그룹 Knowledge write 성공을 의미하지 않음.

## 3. 게이트 판정

**`CANDIDATE_BUILT=PASS` / `TARGETED_QA=PASS_SCOPE_LIMITED` / `INDEPENDENT_CODE_REVIEW=NOT_RUN` / `HARD_GUARD=NOT_VERIFIED` / `PUBLIC_RELEASE=BLOCKED_NOT_POSTED`.**

- PUBLIC L1Work 루트 확인 결과 신규 ZIP `l1-fix-workflow_v1_6_70_1117.zip`, `l1-github_v0_3_58_1117.zip`, `work-ledger-kernel_v0_7_43_1117.zip` **3개 모두 없음**. 기존 PUBLIC 파일 변경/덮어쓰기 0.
- 현 후보에는 단순 Workflow/Git 호출 경로 가드만 있으므로 같은 credential의 raw Git 우회와 **이미 commit된 `knowledge/` diff의 push**를 기술적으로 보장하지 못함. 실질적 구현 gap 존재. `l1-github`에 전체 outbound commit diff 검사/신뢰된 writer 경계/lock/atomic CAS를 우선 검증하고 최소 패치·회귀 필요.
- 후보 메타데이터가 `development_not_for_deployment`이므로 PUBLIC 최종 ZIP으로 이름만 바꿔 배포하면 [PUBLIC 릴리스 게이트](../../ops/CONTRACTS/PUBLIC_RELEASE_GATE.md) 위반. 사용자 PUBLIC 목적지 지시는 확인되지만 미충족 필수 안전·회귀·독립 코드 검증 게이트의 자동 면제는 아님.
- 사용자가 이미 완료한 Claude 설계 리뷰 1회는 유지. **신규 REQUEST/READY/유료 독립 리뷰 호출 0**. PUBLIC 배송 승인과 별개로 실제 설치/Job/그룹 writer 실행 0.

## 4. 다음 한 동작

기존 개발 후보에 대해 먼저 보호된 Git outbound diff/동시 writer fail-closed 반례를 코드 수준에서 보완·회귀시험하고, 업무 GPT READ_ONLY G0로 실제 writer 자격·그룹 Knowledge 인터페이스를 확인. 그 후 필수 코드 리뷰·보안/호환 게이트를 통과한 **신규 최종 버전 ZIP만** `wonhwipark/L1Work/main` 루트에 게시·원격 SHA-256 검증. 리빌드 없이 개발 후보를 그대로 PUBLIC으로 복사하지 말 것.
