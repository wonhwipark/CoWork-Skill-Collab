# GPT 판정 — CL/PR → 이슈 분석 → l1-workspace 축적 설계 리뷰 r0001

- Date: 2026-11-14 KST
- Parent Work: `L1-WORKSPACE-RAG-20261111-001`
- Review report: `CLAUDE_CL_PR_ISSUE_ANALYSIS_DESIGN_REVIEW_RESULT_FOR_GPT_r0001_20261114.md` (Git blob `1426308b751e056eec6bc8d88b3aeef229c61540`)
- Baseline: `CL_PR_ISSUE_ANALYSIS_DESIGN_BRIEF_r0001_20261114.md`
- Review status: `CLAUDE_INDEPENDENT_DESIGN_REVIEW=REPORTED_COMPLETE`, source/version E2 and synthetic tests, receipt not independently attested; actual installed host E3 unverified.
- GPT disposition: `ACCEPT_WITH_CHANGE` / `REUSE_EXISTING_SKILLS` / `MINIMAL_CONNECTOR_AND_EXTENSIONS`
- User instruction: **no additional independent review request**; implement/repair and regress where source tools and privileges allow, aim for PUBLIC L1Work validated final ZIP only. No false PASS or unauthorized host changes.

## 1. 항목별 GPT 판정

| Finding | GPT 판단 | 구현·판정 / 소유 |
|---|---|---|
| F-R01 P4 CL-only 불가 | **수용** | `p4-code-owner`에서 Jira 비의존 CL Evidence 입력 단계 추가. Mango MCP가 이미 수집한 submitted/describe/files/integration 입력을 기존 `validated_change`와 L1 scope guard로 검증. Jira 가상 생성 금지. |
| F-R02 Merged PR landing SHA 없음 | **수용** | `l1-github`에 `merged`, `merged_at`, `merge_commit_sha`, 목표 브랜치 적용/확인 상태를 추가. base/head diff와 landing tree를 동일하다고 간주 금지. |
| F-R03 이슈 그룹핑 부재 | **수정 수용** | Workflow 측 통합 규칙을 최소 도입. 공통 Jira 키·명시적 CL/PR 교차참조·공식 integration 계보를 근거로 *후보 그룹* 생성, 다대다 원본 보존. 근거 약하면 UNLINKED, 사용자 승인 없는 자동 합병 금지. 새 영속 원장 금지. |
| F-R04 P4 과거 CL before/after | **수정 수용** | P4 파일별 `rev/from_rev` 등 실제 Mango 제공 근거 보존. 파일별 revision 불일치에서 VERIFIED 차단. 과거 코드 내용에 접근 불가하면 INFERENCE. read-only snapshot 구현은 실제 필요할 때 후속. |
| F-R05 claim state 부재 | **수용** | Root Cause 근거수준을 기존 Work artifact의 정형 내용으로 표시. CODE_CONFIRMED/INFERENCE/UNKNOWN, 수정반영·테스트·현재성 각각 독립. Kernel Evidence schema 임의 확장 금지. |
| F-R06 issue-analyzer 조건부 | **수용** | CL/PR-only 요청에서는 기본 호출하지 않음. 실제 로그/증상 증거가 있을 때 선택 연결. |
| F-R07 delivery 우회 위험 | **수용 / 안전 필수** | 과거 PR/P4 출처를 `delivery`, `change_provenance`, 가짜 provider로 저장 금지. 등록된 code-analyzer Evidence kind만 해당 사실에 사용. 필요 증거 종류는 테스트에서 실제 gap 확인 후 별도 설계. |
| F-R08 Work 중복 및 참조 표기 | **수정 수용** | CL은 `p4:<authority>:<number>`, PR은 정규화한 `https://<host>/<owner>/<repo>/pull/<number>`로 식별. Work 재검색 후 연결; 기존 Work 여러 개 발견 시 합병하지 않음. **원본 목록 집합의 hash를 영구 이슈 ID로 간주하지 않음**(CL 추가시 변동 위험). |
| F-R09 Knowledge 연결 | **수용 / 후속 유지** | Work가 업무·Evidence SSOT, Knowledge가 검증 기술 지식 SSOT. 후보분류와 범위 참조만 준비. 게시·역링크·Provider RAG M1는 별도 승인 후 시험. |
| F-R10 반출 정책 | **수용** | 회사 소스·로그·MSC·MCP 상세는 PRIVATE에도 업로드 금지. 공개 기술 계약/합성 예제만 외부 저장소 사용. |
| R11 시험 우선순위 | **수용** | T02/T09/T10 → T05/T06/T07 → T03/T04 → 전체 T01~T14. 합성 / 실제 호스트를 분리한 영수증만 인정. |
| R12 새 엔진 불필요 | **수용** | 기존 5개 스킬 최소 변경. 신규 RAG·Review Ledger·업무 원장 엔진 금지. |
| N1 Python 호환성 | **수용** | Kernel `work_ux.py`, code-analyzer `share_export.py`의 3.10/3.11 구문 호환. 선언한 최소 버전부터 py_compile, 기동·기존 회귀 필요. 코드 한 줄 시험 우회는 배포 PASS 아님. |
| N2 임시 PR worktree 재사용 | **수용** | 동일 저장소에서 PR 메타데이터 조회/분석/증거 보존 후 다음 PR. 분석 직전 head/snapshot 재검증; 병렬 분석 금지. |
| N3 P4 접근 정책 충돌 | **수정 수용** | CL/PR 흐름에서 허가된 Mango MCP Evidence 우선. code-analyzer의 임의 로컬 p4 실행 금지; `EVIDENCE_FILE` 호환 확인 후 연결. 허가·실제 스키마 없는 새 MCP 호출 금지. |

## 2. 구현 및 회귀시험 순서 (추가 독립 리뷰 0)

1. PUBLIC L1Work 기존 5종 ZIP 실제 바이트 및 스킬 설정·릴리스 메타 확인. 원본/오래된 ZIP 보존.
2. Python 구문/기동 N1 수정 → Py3.10/3.11 minimum compatibility regressions.
3. P4 CL-only(F-R01), GitHub merge(F-R02), 기존 Git/P4 scope guard(F-R04/N3) 변경 후 각각 합성 정상/차단 시험.
4. Workflow connector(F-R03/F-R05/F-R07/F-R08/N2): 안정 ref, 후보 그룹, 단일 PR 순차 분석, Work 재사용, 안전한 Evidence 등록 경계.
5. 전체 T01~T14, 기존 각 스킬 자체 회귀, 반복 입력, missing object/revision, bad enum/registry, no Jira, Work export, ZIP CRC/ZipSlip/secret check.
6. 별도 새 버전 ZIP 및 SHA-256/bytes/test matrix/rollback manifest 작성. 스킬별 `development_not_for_deployment` 상태에서 충분한 검증·정식 게시 게이트를 평가.
7. 검증·배포 게이트 충족한 **최종 ZIP만** 사용자 승인된 PUBLIC `wonhwipark/L1Work/main` 루트에 신규 파일명으로 게시하고, 실제 바이트 재다운로드·SHA256·원격 commit readback. 미충족 패키지는 PUBLIC 배송본으로 표시하거나 PRIVATE ZIP으로 대체하지 않음.

## 3. 완료 판정이 별개인 항목

| Axis | 현재 판정 |
|---|---|
| DESIGN_REVIEW | ACCEPT_WITH_CHANGE (Claude 별도 세션 보고 E2, source/host 제한) |
| GPT_DISPOSITION | COMPLETED (본 문서) |
| CODE_IMPLEMENTATION | NOT_RUN (검증된 수정 ZIP 없음) |
| POST_PATCH_REGRESSION | NOT_RUN |
| WORKSPACE_PILOT_E3 | NOT_VERIFIED/NOT_RUN |
| CODE_INDEPENDENT_REVIEW | NOT_RUN (사용자가 추가 리뷰를 요청하지 않음) |
| PUBLIC_SKILL_ZIP_RELEASE | NOT_POSTED (기술 게이트 충족 전) |
| HOST_SKILL_UPDATER / JOB_EXECUTION | NOT_RUN |
| KNOWLEDGE_PUBLISH / RAG_M1 | NOT_RUN/BLOCKED |

**주의:** 사용자의 '추가 리뷰 없이'는 새 리뷰 요청을 하지 않는 범위 지시이며, 미수행 독립 리뷰를 PASS로 소급하거나 배포 안전·릴리스 계약을 임의 해제한다는 의미로 취급하지 않는다.

## 4. CoWork 협업 구조와의 관계 (작업 종료 시 재감사)

- 업무 요청 1회 → GPT 판정 → 가능한 직접 수정·시험 → 미지원 호스트 항목만 BLOCKED → PRIVATE 결과·상태·고정 경로 게시/readback → 공개 허용 최종 ZIP만 L1Work root 배포 → 호스트 설치/실행은 별도 증거. **협업 구조와 일치**.
- Windows Claude Code의 추가 리뷰는 요청하지 않음. 필요시 코드 구현 담당 세션을 열어도 자기시험은 `SELF_TEST_REPORTED`, 독립 리뷰가 아니다.
- PRIVATE 설계 MD와 PUBLIC 인계 MD는 저장소별 책임을 유지. 공개 인계 MD의 존재는 ZIP 배포 완료가 아니다.
- 무인가 회사 코드/토큰 반출, 운영 Work/DB/Job/Watcher 변경, LIVE 전환, 그룹 Knowledge 정본 변경 없음.
- 검토 후 추가로 확인된 결함은 같은 수정 작업에서 보완·회귀시험. 미수행을 완료로 표시하지 않음.

## 5. 다음 한 동작

공개 패키지의 원본 소스와 Python 시험 실행 환경이 확보된 승인 호스트에서 **신규 리뷰 없이** 구현·재시험·신규 ZIP 후보 생성까지 한 작업으로 실행. PUBLIC 게시가 차단되면 원인과 후보 상태를 하나의 비민감 결과로 보고한다.
