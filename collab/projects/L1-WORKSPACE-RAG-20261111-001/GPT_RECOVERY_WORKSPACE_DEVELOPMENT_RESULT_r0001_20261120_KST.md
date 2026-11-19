# Recovery Workspace 연결 — 관리 스킬 개발 결과 r0001

- 작성: 2026-11-20 KST / 기존 Work: L1-WORKSPACE-RAG-20261111-001
- 사용자 요청: 업무 GPT에서 다룰 l1-channel-recovery와 별개로, 접근 가능한 나머지 스킬의 구현·시험을 계속 진행
- 판정: **DEVELOPMENT_COMPLETE / PRIVATE_CANDIDATE / NEW_REGRESSIONS=0**
- 실제 변경: Kernel·Workflow 2종. l1-github·code-analyzer·P4·issue-analyzer·converter는 기존 기능 재사용, 이번 변경 없음
- 독립 코드 리뷰·업무 호스트 설치·생산자 실제 연결·Viewer API 통합·제품 recovery 시험·PUBLIC 게시: NOT_RUN

## 1. 현재 결과

같은 Work에 l1-channel-recovery 보고서를 부가 Evidence로 등록하고, 원본 hash를 확인하는 조회 및 Recovery 파생 보기를 구현했어요. Work를 새로 만들거나 기존 profile/schema/FSM을 바꾸지 않아요.

업무 호스트의 실제 생산자 결과 연결은 준비된 HO로 업무 GPT가 설계해요. MCP 확인 자료를 사용자에게 다시 요구하는 절차를 두지 않아요.

| 스킬 | 개발 후보 | 구현 |
|---|---|---|
| work-ledger-kernel | 0.7.46 | 부가 보고서 슬롯·preview/원본 등록·중복/동시성 검사·메타 조회·Work/전체 Recovery 보기 |
| l1-fix-workflow | 1.6.75 | 기존 attach-evidence에 Recovery 제공자 연결, 기존 로컬 writer·preview/apply 사용 |
| l1-github 등 | 변경 없음 | 기존 work_docs 목적지·Git 게시·수집·분석·변환 재사용 |

## 2. 고정 입력·기존 개발 보존

- Kernel 입력은 기존 PRIVATE 0.7.43 SHA-256 `80c955790aaa65f695c061f7ec2664bd1c7c5ba7e0a7534045960eea7fe2d5f6`에서 기존 main builder로 0.7.45를 재구성. 실제 재구성 ZIP SHA-256 `1bccbbffeaafcefda27b75ca8f430e502bc8c2b475b63bd76425ca7ee1c5d7f8` 일치. 기존 Knowledge 경로 보호·MSC Work-root HTML 링크 개발 변경 보존.
- Workflow 입력은 PUBLIC 1.6.74 ZIP SHA-256 `b810ce0cf072609431737c58b0ef2b7a0a8ec0701a0746e6a94283c374224989`.
- patch SHA-256: `1649d8e7288134a7044f5ccede87ae974f707c7db6888707bde03d3fe724f60a`.
- 기존 파일 삭제 0. Kernel 163→166파일, Workflow 311→313파일. 시험한 source tree와 최종 ZIP 모든 파일의 bytes 일치.
- 로컬 소스 commit: `fc85238740dbc57e9f5618d82f0113148d113a3c`. 원격 정본은 아래 PRIVATE 파일/게시 commit으로 확인.

| PRIVATE 후보 위치 | bytes | SHA-256 |
|---|---:|---|
| candidates/work-ledger-kernel_v0_7_46_1120.zip | 330715 | dabd412847354c77ca105da3ed686924f676f5f3c67428a2b984e68f2998076e |
| candidates/l1-fix-workflow_v1_6_75_1120.zip | 753864 | d13259cd0c9359dee2cddcb1c622fce5d98b663f9bc6eaea48c8a1c3b46b9ce4 |

두 파일은 development_not_for_deployment예요. PUBLIC ZIP 또는 설치본이 아니며 기존 미충족 배포 게이트를 해제하지 않아요.

## 3. 구현 계약

### 원본 등록과 책임

- 실제 제공자 l1-channel-recovery, kind recovery_analysis, 기존 utility stage의 attach-recovery-report 슬롯으로 보존.
- utility는 부가 보고서 첨부 의미이며 기술 분석 완료를 대신하지 않아요. 기존 7종 profile에 보존할 수 있고 어떤 profile의 분석 준비 조건도 이 보고서만으로 충족되지 않아요.
- 실제 코드 사실은 해당 analyzer의 기존 Evidence로 유지. 다른 analyzer 제공자로 사칭하지 않아요.
- UTF-8 MD/JSON object·5 MiB 한도, 알려진 JSON provenance와 선언 불일치·잘못된 형식·symlink 차단.
- 제공자 버전·code_rev는 호출자의 출처 선언이에요. 이 API가 설치본이나 source revision 의미를 독립 검증했다는 주장은 하지 않아요.

### 기존 writer와 재시도

- Kernel recovery_report_preview → record_recovery_report. 기존 record_evidence가 원본을 복사하고 hash·Evidence ID를 기록.
- 고정 보고서 bytes와 preview hash를 대조하고 기존 Work lock 안에서 Evidence 개수 revision을 검사.
- Work/본문 hash/생산자 버전/code_rev가 같으면 기존 E-12hex ID와 원본/출처를 대조해 재사용. 같은 요청 재시도로 Evidence·journal을 중복 작성하지 않음.
- 다른 source revision/내용은 별도 Evidence 보존. 동일 identity에서 summary/원본이 달라지면 충돌. 이전 confidence·기각 상태를 재시도로 승격하지 않음.
- 기존 record schema·Evidence metadata schema·FSM·profile 정책은 byte 단위 불변.

### 조회·분류

- Kernel work_recovery_reports 및 recovery-list --work-id는 저장 메타정보와 현재 파일 SHA 무결성을 반환. 보고서 본문 자동 반출·분석기 실행 없음.
- 기존 docs export에 Work RECOVERY.md·state/recovery_reports.json, 루트 RECOVERY.md·index/recovery.json을 파생.
- 등록된 실제 artifact mapping/SHA에서 보고서 링크를 만들며 미게시·무결성 미확인은 링크 성공으로 표시하지 않음.
- 교차 호스트 Work projection 보존, Work identity·경로 위조 방어, 반복 export 멱등, 수동 수정 문서 보존.
- 이 읽기 projection은 새 Work 원장이나 Knowledge 정본이 아니에요. 기존 Module→Feature→Scenario와 함께 쓰는 목적별 탐색이에요. 실제 Viewer/Updater 연결은 업무 GPT 인계 범위예요.

### Workflow

- 기존 attach-evidence 명령과 preview/apply·인증된 Linux PC writer 경계를 사용.
- l1-channel-recovery / recovery_analysis만 새 연결. 기존 analyzer 첨부는 변경하지 않음.
- 기존 Kernel이 새 API를 제공하지 않으면 RECOVERY_KERNEL_UNSUPPORTED. MCP read-only 환경에서는 파일을 읽기 전에 로컬 첨부 거부.
- Git 게시·Knowledge 쓰기·분석 재실행·자동 lifecycle 전이 없음.

## 4. 실제 시험

| 구분 | 결과 |
|---|---|
| 신규 Kernel Recovery | 18 PASS |
| 신규 Workflow Recovery 연결 | 5 PASS |
| 기존 Kernel 관련 회귀 | 66 PASS |
| 기존 Workflow 관련 회귀 | 8 PASS, 2 FAIL, 1 ERROR |
| 합계 | **100건: 97 PASS, 2 FAIL, 1 ERROR** |
| 새 회귀 실패 | 0 — 실패 3건은 수정 전 원본에서 같은 형태로 재현 |
| 패키지 QA | 두 ZIP CRC/경로/manifest 전집합/버전·CLI 실제 버전 PASS |
| 재현 빌드 | 두 ZIP 각각 연속 재패키징 bit-for-bit 일치 PASS |
| 소스·schema 검증 | compile PASS, git diff --check PASS, 기존 source 파일 삭제 0, authority schema/FSM 불변 |

신규 시험에는 preview/조회 무변경, 임시 run 정리 뒤 원본 유지, 동일 결과 재시도·동시 등록, source revision 변경 이력, stale hash/revision, 원본 변조, 잘못된 provenance/format/path, 7종 lifecycle 비승격, Work/루트 링크 SHA·멱등·수동 수정 보존, 교차 호스트 projection/경로 위조, CLI·로컬 권한·MCP 모드 차단을 포함했어요.

### 기존 실패를 숨기지 않음

test_personal_github_docs_v150.py의 아래 3건이 후보와 원본에서 동일하게 실패했어요.

- test_auto_sync_false_skips_implicit_but_not_explicit: 기존 explicit sync fixture에서 changed 미반환(KeyError).
- test_docs_push_local_git_commit_push_and_remote_sha_readback: 기존 unowned README 수동 편집 보호로 WORK_DOCS_MANUAL_EDIT_REVIEW_REQUIRED.
- test_docs_push_migrates_tracked_legacy_layout_in_one_commit: 같은 수동 문서 보호/legacy fixture의 기대 불일치.

원본 Kernel 0.7.45 + Workflow 1.6.74로 같은 Git helper를 사용해 **2 FAIL + 1 ERROR**를 재현했어요. 이번 기능의 결함으로 단정하거나 이를 PASS/SKIP으로 바꾸지 않았어요. 기존 보호를 약화해 시험을 통과시키지도 않았어요.

초기 개발 시험에서 신규 ID가 기존 게시 파일명 규칙에 맞지 않는 오류 2건을 발견해 기존 E-12hex 형식을 재사용하도록 수정했고, 이후 export 시험을 통과했어요. 초기 sibling fixture 경로 부재는 격리 시험 레이아웃을 공급해 해결했어요. 전체 스킬 시험이나 실제 업무 호스트 E2E PASS를 주장하지 않아요.

## 5. 재생성·리뷰 입력

기존 Work의 dev/recovery-workspace-20261120/ 아래에 다음을 보존해요.

- build_candidate.py: 고정 Kernel .43→.45 재구성, Workflow .74 추출, patch 적용, compile·CLI 버전·재현 ZIP/QA.
- recovery_workspace.patch: 실제 source·문서·새 시험·package metadata 변경.
- verify_candidate.py: 관련 회귀와 기존 실패 비교. helper는 명시 입력.
- TEST_RESULTS.json, kernel_test_log.txt, workflow_test_log.txt, baseline_workflow_test_log.txt.
- BUILD_RESULT.json: 실제 ZIP 크기·hash·재현성·입력 pin·schema 불변 확인.
- [업무 GPT 연결 계약 인계](L1_RECOVERY_WORKSPACE_IMPLEMENTED_CONTRACT_HANDOFF_r0001_20261120_KST.md).

개발 빌더는 기존 dev의 보호/MSC 빌더·deterministic ZIP writer·quality gate를 재사용해요. 스킬 ZIP은 이 CoWork 경로나 인증에 의존하지 않아요. 공유 업무 자료·실제 회사 코드·로그·상세 MSC는 포함하지 않아요.

## 6. 미검증·다음 한 동작

- 신규 코드의 독립 리뷰: NOT_RUN. 과거 설계 리뷰/개발 세션 자체시험으로 대체하지 않아요.
- l1-channel-recovery 실제 출력 adapter, 실제 설치 Kernel/Workflow와의 호환·승인된 host 호출, Viewer API/개인 Knowledge 연결: NOT_RUN/업무 GPT 담당.
- 실제 제품 recovery 코드·runtime·로그 분석·그룹 지식 게시·Job·호스트 설치·PUBLIC 게시·새 유료 호출: NOT_RUN.
- 다음: 고정 후보/patch·회귀 결과를 기준으로 독립 코드 리뷰를 진행하고, 준비된 구현 계약 HO로 업무 GPT의 생산자·Viewer/Updater 최소 연결 설계를 이어가요. MCP 확인 자료 제공은 그 선행 조건이 아니에요.

