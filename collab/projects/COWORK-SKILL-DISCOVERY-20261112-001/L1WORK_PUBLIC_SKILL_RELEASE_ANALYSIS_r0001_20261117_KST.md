# L1Work 공개 스킬 패키지 분석·협업 재개 인덱스 — r0001 / 2026-11-17 KST

- **목적:** L1Work에 이미 공개된 스킬, CoWork PRIVATE 후속 개발 후보, 연동 책임·차단 게이트를 한 문서에서 찾도록 하는 **조회용 스냅샷**. 새 Work·런타임 registry·자동 로더 아님.
- **기존 Work:** `COWORK-SKILL-DISCOVERY-20261112-001`. 새 창 기본 경로: `collab/CONTEXT_BRIEF.md` → 본 Work의 `CURRENT.md` 최상단 → **이 보고서** → 필요한 개별 SKILL/관련 Work CURRENT.
- **PUBLIC 고정 원본:** `wonhwipark/L1Work` / `main` 조회 commit `33d959f3376a495875eed59b79b292c0f8f9cfe0`; GitHub contents API 기준 루트 125개 항목 중 ZIP **39개**, 관리 목록 18종 중 루트 ZIP이 있는 스킬 **17종**, 독립 `skillsilent` ZIP **미발견**, 기타/보조 파일 **17개**. 숫자는 해당 commit의 루트 스냅샷이며 전체 설치·사용 스킬의 완전성 아님.
- **PRIVATE 조회 근거:** `collab/knowledge/SKILL_CAPABILITY_CATALOG.md` r0008, [18종 과거 정적 패키지 감사](SKILL_18_PACKAGE_AUDIT_20261112.md), [MSC 릴리스 결과](../L1-WORKSPACE-RAG-20261111-001/GPT_MSC_PUBLIC_L1WORK_RELEASE_RESULT_r0001_20261116_KST.md), [Knowledge Guard 후보 QA·배포 차단](../L1-WORKSPACE-RAG-20261111-001/GPT_KNOWLEDGE_GUARDS_CANDIDATE_QA_PUBLIC_GATE_r0001_20261117_KST.md).
- **검증 구분:** 이번에는 GitHub 원격 루트 파일의 **이름·파일 크기·Git blob SHA-1**을 재조회. 39개 ZIP 전량의 실제 바이트/CRC/SKILL 원문 및 설치본을 이번에 재감사하지 않았으며, 아래 SHA-256 값은 인용한 릴리스/후보 결과의 실측값. Git blob은 ZIP SHA-256이 아님.

## 1. 가장 먼저 확인할 릴리스·개발 경계

| 스킬 | 공개 또는 후보 버전 | 위치·판정 | 실제 bytes / ZIP SHA-256(확인된 원문 기록) |
|---|---|---|---|
| `doc-converter` | v0.2.25 / 2026-11-16 | [`doc-converter_v0_2_25_1116.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/doc-converter_v0_2_25_1116.zip) / PUBLIC POSTED, readback PASS | 162,642 / `97cbdf6747b2632035a56fd0ecb792115cdd35e0a202caa3555991422544f181` |
| `work-ledger-kernel` | v0.7.42 / 2026-11-16 | [`work-ledger-kernel_v0_7_42_1116.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/work-ledger-kernel_v0_7_42_1116.zip) / PUBLIC POSTED, readback PASS | 320,083 / `ece2bce143ef35a1c8cc3bc12ddf6a73e27e0f218fc69fec87844759d9dfc164` |
| `l1-fix-workflow` | v1.6.70 / 2026-11-17 | PRIVATE `dev/l1-knowledge-guards-20261117` / `development_not_for_deployment` / **PUBLIC BLOCKED** | 758,117 / `1e08302b6a533d2894101427f5a7bb94b43102e00a98f2c6e0b19f534a885ceb` |
| `l1-github` | v0.3.58 / 2026-11-17 | PRIVATE `dev/l1-knowledge-guards-20261117` / `development_not_for_deployment` / **PUBLIC BLOCKED** | 566,777 / `cad08cba93a147b08b3a1b8a940397cced840fe21d600c5e904e8c597a754ced` |
| `work-ledger-kernel` | v0.7.43 / 2026-11-17 | PRIVATE `dev/l1-knowledge-guards-20261117` / `development_not_for_deployment` / **PUBLIC BLOCKED** | 319,793 / `80c955790aaa65f695c061f7ec2664bd1c7c5ba7e0a7534045960eea7fe2d5f6` |

- 공개 2종: doc-converter `83 PASS`, Kernel `244 PASS + 39 subtests` (Python 3.10/3.11 각각, 관련 원문 보고 기준); MSC B HTML 및 SVG export의 **격리 시험** 근거. 실제 OpenCode/업무 호스트 설치·`l1-workspace`/그룹 writer·HTML URL E2E는 `NOT_RUN/NOT_VERIFIED`.
- 개발 3종: 기존 PRIVATE Work에 후보 ZIP과 CI 근거 존재, 표적 시험만 PASS. 이미 commit된 `knowledge/` 변경의 raw Git push, 동일 credential/공통 writer 우회, 경합/하드 권한, 전체 회귀·코드 독립 리뷰·G0 미검증. **PUBLIC 공개 전 차단 유지**. 최신 파일이 있다는 이유로 최신 공개 릴리스라고 처리하지 않음.
- 공개 릴리스와 실제 호스트 설치/활성화·Job 수행은 다른 상태. `skillsilent` 런타임 검사는 OpenCode 사용자 실행 경로에 해당하지 않아 2종 MSC 릴리스에서 `SKIP_BY_USER_SCOPE`였고, 설치/호출 PASS를 의미하지 않음.

## 2. 관리 스킬 18종 — 기능·PUBLIC 최신 파일·연결 포인트

아래 '공개 파일'은 **해당 스냅샷의 L1Work 루트에서 이름상 가장 최신인 파일**이며, 버전/설치/기능 검증의 최종 정본은 각 관련 CURRENT·실제 원문임. 2026-11-12 감사의 지원 기능은 역할 수준에서 재사용했으며, 모두 2026-11-17에 재시험했다는 뜻이 아님.

| 스킬 | 공개 ZIP(해당 루트 내 선택) | 주요 입력→출력·책임 | 주의 / 현재 연계 |
|---|---|---|---|
| `issue-analyzer` | [`issue-analyzer_v0_11_50_1102.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/issue-analyzer_v0_11_50_1102.zip) | 로그·SDM 분석 → 원인 근거·보고·수정 인계 | issue-analyzer CURRENT/업무 원본 확인 |
| `code-analyzer` | [`code-analyzer_v0_15_2_1107.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/code-analyzer_v0_15_2_1107.zip) | 고정 코드 분석 → CODE FACT·call flow·MSC/HLD 입력 | PRIVATE v0.15.3 별도 후보; 공개본과 구분 |
| `code-fix` | [`code-fix_v0_4_19_20260928.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/code-fix_v0_4_19_20260928.zip) | 승인된 코드 수정·shelve·as-built | submit 별도 승인 |
| `l1-fix-workflow` | [`l1-fix-workflow_v1_6_67_1110.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/l1-fix-workflow_v1_6_67_1110.zip) | Work 선택·진행·분석/결정/Evidence 연결 | PRIVATE v1.6.70 개발 후보 공개 차단 |
| `work-ledger-kernel` | [`work-ledger-kernel_v0_7_42_1116.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/work-ledger-kernel_v0_7_42_1116.zip) | Work/Evidence 원장·MSC SVG/MD export | v0.7.42 정식 공개; v0.7.43 개발 후보 차단 |
| `hld-composer` | [`hld-composer_v0_4_32_1008.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/hld-composer_v0_4_32_1008.zip) | SRS·분석 근거 → HLD·설계 게이트 | 합성/호스트 검증 별도 |
| `doc-converter` | [`doc-converter_v0_2_25_1116.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/doc-converter_v0_2_25_1116.zip) | MSC/문서 변환 → B형 HTML+SVG·manifest | v0.2.25 정식 공개·격리 회귀 PASS |
| `hld-code-compare` | [`hld-code-compare_v0_10_15_0825.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/hld-code-compare_v0_10_15_0825.zip) | HLD ↔ 코드 비교 → gap report | MSC 근거 등급 구분 |
| `hld-code-implement` | [`hld-code-implement_v0_5_14_0815.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/hld-code-implement_v0_5_14_0815.zip) | 승인된 gap → 수정 기록·shelve | G1/G2 승인/실호스트 검증 별도 |
| `l1-github` | [`l1-github_v0_3_56_1110.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/l1-github_v0_3_56_1110.zip) | Git/GitHub 근거·안전 작업·journal | PRIVATE v0.3.58 개발 후보 공개 차단 |
| `p4-code-owner` | [`p4-code-owner_v0_6_7_1012.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/p4-code-owner_v0_6_7_1012.zip) | P4 수정 이력·수정자/CL 근거 조회 | 읽기 전용; module owner 추정 금지 |
| `l1-cl2git-merge` | [`l1-cl2git-merge_v0_3_5_1017.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/l1-cl2git-merge_v0_3_5_1017.zip) | CL 기반 PR 충돌 검증·해결 | SKILL 내부 0.3.4 표기 불일치 이력 |
| `l1-sam-fixer` | [`l1-sam-fixer_v0_2_85_0929.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/l1-sam-fixer_v0_2_85_0929.zip) | SAM LOC/MCD 분석·수정 제안 | 옛 provider/제목 표기 불일치 이력 |
| `skill-updater` | [`skill-updater_v0_5_44_1027.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/skill-updater_v0_5_44_1027.zip) | 승인 공개 ZIP 설치·격리 검증·롤백 | 설치와 Job 실행 구분 |
| `skillsilent` | **없음** | 등록 Action/policy 기반 실행 게이트 | 독립 PUBLIC ZIP 미발견; OpenCode 경로 시험과 구분 |
| `job-list` | [`job-list_v0_4_38_1115.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/job-list_v0_4_38_1115.zip) | 승인 One-shot Job 전달·Runner·영수증 | PUBLIC 전달 완료 ≠ Linux MCP 실행 |
| `autotask-builder` | [`autotask-builder_v0_4_24_0918.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/autotask-builder_v0_4_24_0918.zip) | OS 예약 작업 생성·상태 | Job queue 소유 아님 |
| `l1-cleanup` | [`l1-cleanup_v0_13_6.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/l1-cleanup_v0_13_6.zip) | 보존·정리 audit/plan·격리 복구 | 파괴적 정리는 별도 승인 |

**별도 연동 스킬:** `l1-knowledge-updater`는 이 18종 공개 ZIP 감사 범위의 19번째(업무 GPT/그룹 공용 연동)로, **L1Work 루트 ZIP 미확인**. 실제 설치/원문·업무 `l1-workspace` 및 `l1sw-dev-knowledge` writer/승인 계약은 업무 GPT G0/실행 근거에서 확인. 루트에 남아 있는 `l1-knowledge-manager_v0_5_4_0830.zip`을 현행 Updater라고 간주하거나 자동 대체·설치하지 않음.

## 3. 실제 연결 방식 — 재사용·검증 경계

```text
모바일 Agent / 업무 GPT → Linux MCP 또는 승인된 Job-list
   ├─ 기존 Work 조회·재개 → l1-fix-workflow → work-ledger-kernel (works/, Evidence)
   ├─ 코드/로그 → issue-analyzer·code-analyzer (+ P4/Git 근거)
   │     ├─ CODE FACT / source revision → hld-composer·hld-code-compare
   │     └─ MSC 근거 → doc-converter(B형 HTML+SVG) → Kernel Evidence/export
   └─ l1-knowledge-updater (업무 설치 원본 G0 필요)
         ├─ 직접 Procedure/Feature 분석 또는 기존 Workflow Work 재사용
         ├─ 개인 l1-workspace: 원래 Work/Evidence 보존 + knowledge/ 탐색
         └─ 후보·그룹 정본 대조·Preview/승인 → 기존 그룹 writer
                       → l1sw-dev-knowledge revision/readback → Work 역링크
```

- `code-analyzer`는 **코드 사실**, `doc-converter`는 **MSC 표현/문서 변환**, Kernel은 **Work/Evidence/export**, Workflow는 **업무 흐름**, Updater는 **지식 후보/Preview/게시 연결**. 제작·조회·승인/실제 그룹 게시를 혼동하지 않음.
- 개인 `knowledge/`는 그룹 지식 구조를 탐색하기 위한 설계이며 WRITE 권한은 Updater 전용; Workflow는 READ_ONLY 설계. 실제 OS/Git 자격·하드 보호 강제는 현재 G0/보완 미확인. Kernel `works/` 보존, 단일 writer, 그룹 CAS/readback, HTML/SVG URL 호스팅 실제 E2E는 별도 확인.
- `skill-updater`는 승인 ZIP 설치·롤백, `job-list`는 승인 One-shot Job/Runner·영수증, `autotask-builder`는 OS 예약. PACKAGE_POSTED, HOST_INSTALLED, JOB_RUN, RESULT_RECEIVED, GROUP_KNOWLEDGE_PUBLISHED를 개별 기록.

## 4. 관리 범위 밖 공개 루트 ZIP 17개 — 이름만 확인

- [`L1_Workflow_Release_Preflight_20261013.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/L1_Workflow_Release_Preflight_20261013.zip)
- [`MCD_handoff_20260908_v2.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/MCD_handoff_20260908_v2.zip)
- [`cl-ait-dev-orchestrator_v0_1_11_0919.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/cl-ait-dev-orchestrator_v0_1_11_0919.zip)
- [`integration_candidate_v1_6_12.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/integration_candidate_v1_6_12.zip)
- [`l1-crash-check_v0_8_3_0930.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/l1-crash-check_v0_8_3_0930.zip)
- [`l1-defect_v0_1_2.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/l1-defect_v0_1_2.zip)
- [`l1-fla_v0_3_47_1029.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/l1-fla_v0_3_47_1029.zip)
- [`l1-issue-ut_v0_2_10_1009.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/l1-issue-ut_v0_2_10_1009.zip)
- [`l1-knowledge-manager_v0_5_4_0830.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/l1-knowledge-manager_v0_5_4_0830.zip)
- [`l1-part-evaluation_v0_4_4_1106.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/l1-part-evaluation_v0_4_4_1106.zip)
- [`l1-skill-benchmark_v0_3_1_0815.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/l1-skill-benchmark_v0_3_1_0815.zip)
- [`l1-study-runner_v0_2_13_0901.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/l1-study-runner_v0_2_13_0901.zip)
- [`l1sw-dispatcher-bundle_v0_3_13_1011.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/l1sw-dispatcher-bundle_v0_3_13_1011.zip)
- [`l1sw_dev_feature_v0_3_design_bundle_0819.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/l1sw_dev_feature_v0_3_design_bundle_0819.zip)
- [`p4-crash-check_v0_7_0_0825.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/p4-crash-check_v0_7_0_0825.zip)
- [`p4-fix-kb_v0_2_4_0817.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/p4-fix-kb_v0_2_4_0817.zip)
- [`vscode-source-insight-theme_v0_7_0_0915.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/vscode-source-insight-theme_v0_7_0_0915.zip)

위 17개는 **파일 존재만 확인**. 일부는 보조 번들·과거 설계·다른 스킬일 수 있어 이름으로 최신 정식 스킬, 동작, 승인·설치 여부를 추정하지 않음. 구버전 5개(`doc-converter` 0.2.21, `work-ledger-kernel` 0.7.37, `job-list` 0.4.34/0.4.36, Workflow/Kernel 호환 패치 ZIP)는 부록에 보존. 공개 루트에서 삭제·변경하지 않음.

## 5. 이 시점에 해결하지 않은 사항·사용자 요청과 다음 행동

1. **현재 차단:** PRIVATE 개발 3종은 `PUBLIC_RELEASE=BLOCKED_NOT_POSTED` 유지. outbound commit diff에서 `knowledge/` 보호, 인증된 writer/경합/회귀/승인된 리뷰 게이트를 실제 증빙할 때만 최종 릴리스로 변경.
2. **미검증:** 실제 업무 호스트 설치 SHA, OpenCode/Skill-Updater, Linux MCP/Job readback, 개인 `knowledge/` writer G0, 그룹 지식 승인·CAS/readback, MSC B형 링크/HTML URL E2E. 문서·ZIP QA로 승격 금지.
3. **과거 부채:** `skillsilent` 독립 패키지 미발견(설치 부재 단정 금지), CL2Git ZIP/내부 버전 불일치, SAM legacy provider 표기, `l1-knowledge-manager` 잔존. 기존 Work에서 필요한 범위로만 점검.
4. **이번 작업 범위:** GitHub READ_ONLY 조회 + PRIVATE 비민감 분석/진입 링크 게시. ZIP/소스 수정·PUBLIC 쓰기·호스트 설치·Job/그룹 writer·REQUEST/READY/유료 리뷰 실행 **없음**.
5. **NEXT_ONE_ACTION:** 3종 Knowledge Guard 후보의 보호 diff·단일 writer 미검증 반례와 업무 G0를 기존 L1 RAG Work에서 해소하여 배포 게이트 충족 시만 신규 최종 ZIP 공개. 스킬 **조회 요청**이라면 먼저 본 문서와 `COWORK-SKILL-DISCOVERY.../CURRENT.md`, 해당 스킬의 Work CURRENT 및 실제 PUBLIC HEAD를 대조.

## 부록. PUBLIC 루트 ZIP 39개 — 고정 HEAD의 경로·크기·Git blob

해시 열은 **GitHub blob SHA-1** (ZIP raw SHA-256 아님). 목록은 파일 존재/크기 증거이며 개별 ZIP 바이트·CRC 및 내용 재감사가 아님.

| # | 경로 (L1Work 고정 commit 링크) | bytes | Git blob SHA-1 |
|---:|---|---:|---|
| 1 | [`autotask-builder_v0_4_24_0918.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/autotask-builder_v0_4_24_0918.zip) | 116458 | `ab0a824b5024d3d8077d208bbb5aa73707c31b63` |
| 2 | [`cl-ait-dev-orchestrator_v0_1_11_0919.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/cl-ait-dev-orchestrator_v0_1_11_0919.zip) | 166614 | `c7872dadb10f44089fde2ae3c490964f6dc4dab1` |
| 3 | [`code-analyzer_v0_15_2_1107.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/code-analyzer_v0_15_2_1107.zip) | 513811 | `6017f81f51e9747286825648599fc13770cb8903` |
| 4 | [`code-fix_v0_4_19_20260928.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/code-fix_v0_4_19_20260928.zip) | 170699 | `02a3a556f526f997b5ba9b20e1049febac16a395` |
| 5 | [`doc-converter_v0_2_21_1106.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/doc-converter_v0_2_21_1106.zip) | 155012 | `bd5192c802fcc28d21f75ead81fb4cffc10d8470` |
| 6 | [`doc-converter_v0_2_25_1116.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/doc-converter_v0_2_25_1116.zip) | 162642 | `be847e46b8e47885e02b869391c3c9975574fd0c` |
| 7 | [`hld-code-compare_v0_10_15_0825.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/hld-code-compare_v0_10_15_0825.zip) | 160883 | `ff8405df122718326b0c8bcb3cc3f466ece970ee` |
| 8 | [`hld-code-implement_v0_5_14_0815.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/hld-code-implement_v0_5_14_0815.zip) | 121821 | `61698dd27d1232eea97ee59639bcf53e74e02521` |
| 9 | [`hld-composer_v0_4_32_1008.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/hld-composer_v0_4_32_1008.zip) | 267227 | `da0d969c0ce83b0244e87274d700a4fa136773d3` |
| 10 | [`integration_candidate_v1_6_12.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/integration_candidate_v1_6_12.zip) | 303349 | `207b1df12ffb63ec8046f0e4ff4c50b8c49aa56a` |
| 11 | [`issue-analyzer_v0_11_50_1102.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/issue-analyzer_v0_11_50_1102.zip) | 440609 | `f830b6bb561c0c3c1ac11ffd63625ccbf2fdfc13` |
| 12 | [`job-list_v0_4_34_1109.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/job-list_v0_4_34_1109.zip) | 1551031 | `13353c5db1d09752507b865fe3d4e5fc456f495c` |
| 13 | [`job-list_v0_4_36_1112.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/job-list_v0_4_36_1112.zip) | 1563658 | `4357594be4cdae26a4fd19788fb3a35d7de3b5d5` |
| 14 | [`job-list_v0_4_38_1115.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/job-list_v0_4_38_1115.zip) | 1570759 | `15416300e2f4cb0b29a43d4a965e21f57e41d0cb` |
| 15 | [`L1_Workflow_Release_Preflight_20261013.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/L1_Workflow_Release_Preflight_20261013.zip) | 582773 | `15be51c91bb5f60ef85090f627d4554ee0c070fd` |
| 16 | [`l1-cl2git-merge_v0_3_5_1017.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/l1-cl2git-merge_v0_3_5_1017.zip) | 39005 | `c8435e7ad831fc74343ba796e462a2ed4d6e6ce2` |
| 17 | [`l1-cleanup_v0_13_6.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/l1-cleanup_v0_13_6.zip) | 210536 | `7176c89151390f4a43122575c457025fce4d3862` |
| 18 | [`l1-crash-check_v0_8_3_0930.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/l1-crash-check_v0_8_3_0930.zip) | 64755 | `e6b21abb05268cd3c5dfbb8047b47878ca0c0d2a` |
| 19 | [`l1-defect_v0_1_2.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/l1-defect_v0_1_2.zip) | 29953 | `cfae3ec0d246a5f4b6dfe714745c0c64b7b60ea4` |
| 20 | [`l1-fix-workflow_kernel_v079_compat_patch_1013.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/l1-fix-workflow_kernel_v079_compat_patch_1013.zip) | 22644 | `9b690f5b3b6df2cf2d7ba7214d5a96861fbfd27d` |
| 21 | [`l1-fix-workflow_v1_6_67_1110.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/l1-fix-workflow_v1_6_67_1110.zip) | 749307 | `6a1dc5c85d63ee70a35ed3af024852879c7d33fd` |
| 22 | [`l1-fla_v0_3_47_1029.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/l1-fla_v0_3_47_1029.zip) | 335991 | `d0bf4a5ba60a66b2122bde48186ebe46b49304b1` |
| 23 | [`l1-github_v0_3_56_1110.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/l1-github_v0_3_56_1110.zip) | 572047 | `47f76743a6ca7ce20ecaaf943ef5aa634a77f66d` |
| 24 | [`l1-issue-ut_v0_2_10_1009.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/l1-issue-ut_v0_2_10_1009.zip) | 213723 | `56eb76e79b057f188cec4af29f95e2bf1ce6aa72` |
| 25 | [`l1-knowledge-manager_v0_5_4_0830.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/l1-knowledge-manager_v0_5_4_0830.zip) | 255802 | `9bdf0ac0d12581d63b948243544740cbb6191e43` |
| 26 | [`l1-part-evaluation_v0_4_4_1106.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/l1-part-evaluation_v0_4_4_1106.zip) | 37299 | `48ed76ca67c1a268c0d88aabddf8e24351dc85b3` |
| 27 | [`l1-sam-fixer_v0_2_85_0929.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/l1-sam-fixer_v0_2_85_0929.zip) | 648748 | `3248a16e60e5b3310d8edf719313e4f729561330` |
| 28 | [`l1-skill-benchmark_v0_3_1_0815.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/l1-skill-benchmark_v0_3_1_0815.zip) | 48011 | `a59aad198d6c496d9869087c2ad78a477c785a22` |
| 29 | [`l1-study-runner_v0_2_13_0901.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/l1-study-runner_v0_2_13_0901.zip) | 68032 | `9fc22e1bf91aa96fea4781c0c1d4262dce0f095a` |
| 30 | [`l1sw_dev_feature_v0_3_design_bundle_0819.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/l1sw_dev_feature_v0_3_design_bundle_0819.zip) | 24181 | `1ab0a87a8509318bdf970ce85e71c9ef98075370` |
| 31 | [`l1sw-dispatcher-bundle_v0_3_13_1011.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/l1sw-dispatcher-bundle_v0_3_13_1011.zip) | 83538 | `b28ff844a1405dcb3336e27137504243b3f09dc7` |
| 32 | [`MCD_handoff_20260908_v2.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/MCD_handoff_20260908_v2.zip) | 2007769 | `ff971e8bd069e9d6cf3e889fa149dee432fd9e6b` |
| 33 | [`p4-code-owner_v0_6_7_1012.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/p4-code-owner_v0_6_7_1012.zip) | 106017 | `ee5801e2d8021a54d224f18d321002a3f1742716` |
| 34 | [`p4-crash-check_v0_7_0_0825.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/p4-crash-check_v0_7_0_0825.zip) | 55278 | `3dc07cb9d41fd02c3615d597a127d936db0cd971` |
| 35 | [`p4-fix-kb_v0_2_4_0817.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/p4-fix-kb_v0_2_4_0817.zip) | 91626 | `ba54f1cfefe5f5cfa4b4c716302b4655938ae2ee` |
| 36 | [`skill-updater_v0_5_44_1027.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/skill-updater_v0_5_44_1027.zip) | 210717 | `d83faa021549835a40e3ddc134b8e936dc962e65` |
| 37 | [`vscode-source-insight-theme_v0_7_0_0915.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/vscode-source-insight-theme_v0_7_0_0915.zip) | 133860 | `c8cdf2c7f75c2f949eee32c9675b3b30da6844e3` |
| 38 | [`work-ledger-kernel_v0_7_37_1103.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/work-ledger-kernel_v0_7_37_1103.zip) | 318845 | `dd1fc06fb318be2072613839634a485faacb83a2` |
| 39 | [`work-ledger-kernel_v0_7_42_1116.zip`](https://github.com/wonhwipark/L1Work/blob/33d959f3376a495875eed59b79b292c0f8f9cfe0/work-ledger-kernel_v0_7_42_1116.zip) | 320083 | `7799e03fbfa5c95851c430a20f8df0da253cbf07` |

**참고:** [CoWork 공통 기능 카탈로그](../../knowledge/SKILL_CAPABILITY_CATALOG.md) / [CoWork 공통 시작 지도](../../CONTEXT_BRIEF.md) / [L1 RAG Work 최신 판정](../L1-WORKSPACE-RAG-20261111-001/CURRENT.md) / [PUBLIC L1Work](https://github.com/wonhwipark/L1Work). 보고서 게시만으로 다음 대화의 자동 선조회 설정이 바뀌는 것은 아님.
