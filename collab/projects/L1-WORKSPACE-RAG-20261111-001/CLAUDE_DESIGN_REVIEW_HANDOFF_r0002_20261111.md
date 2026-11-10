# Claude Code — L1 Workspace RAG r0002 변경분 독립 설계 리뷰 인계

- Date: 2026-11-11 KST
- Task ID: `L1-WORKSPACE-RAG-20261111-001`
- Source: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch **`main`**
- Input **r0002**: `collab/projects/L1-WORKSPACE-RAG-20261111-001/L1_WORKSPACE_RAG_DESIGN_r0002_20261111.md`
- r0002 creation commit: `2fdfea75e981a75243d185013a1b7e7ce4cff844`
- r0002 Git blob SHA (readback verified): `44d7bc056f203b1c7d82b44532ef7be410e82d33`
- Baseline **r0001**: `collab/projects/L1-WORKSPACE-RAG-20261111-001/L1_WORKSPACE_RAG_DESIGN_r0001_20261111.md`
- Previous handoff: `collab/projects/L1-WORKSPACE-RAG-20261111-001/CLAUDE_DESIGN_REVIEW_HANDOFF_r0001_20261111.md`
- Expected non-sensitive result: `collab/projects/L1-WORKSPACE-RAG-20261111-001/CLAUDE_DESIGN_REVIEW_RESULT_FOR_GPT_20261111.md` (생성 전 경로이며 현재 게시 확인되지 않음)
- Mode: **SEMI_AUTO / INTERACTIVE_STATIC_REVIEW_PREPARED / NOT_QUEUED**
- Operating transport: **MIGRATION_NOT_CUTOVER / DROPBOX_LIVE**, GitHub watcher **NOT_ACTIVE**
- **게시 자체로 Claude Code 호출/예약/비용/정식 watcher REQUEST·READY는 발생하지 않음.**

## 리뷰 목적 (delta 우선)

기존 RAG 설계의 실제 누락인 **개별 브랜치의 현재 코드 분석(AS-IS MSC)**을 누가, 어떤 기준으로, 어느 Work·지식 항목에 보관하고, RAG 답변에서 revision 충돌 없이 검색/소비하는지 검증한다. 새로운 RAG 엔진이나 DB 재개발을 권하지 말 것.

## 입력·선행 검증

1. `main`의 r0002 입력 blob/commit readback, r0001 대비 추가·수정 델타를 검증.
2. PUBLIC `wonhwipark/L1Work`의 `l1-fix-workflow_v1_6_67_1110.zip`, `l1-github_v0_3_56_1110.zip`, 이용 가능한 `work-ledger-kernel_v0_7_37_1103.zip` 코드·계약과 대조. 존재 확인과 실제 설치/실행 확인을 엄격히 구분.
3. 사내 `l1-workspace`는 외부 GitHub MCP에 연결되지 않음. 가능할 경우 사내 승인된 `l1-github` 역할(`work_docs`)과 Git CLI로 **읽기 전용** 실제 branch/tree/installed versions 확인; 접근 불가 시 `E0 / NOT_VERIFIED`.
4. Dropbox LIVE review/receipt가 존재한다면 해당 작업 ID/revision과 실제 결과를 확인해 구분. 임의 REQUEST/READY 생성·watcher 실행은 금지.

## 집중 리뷰 항목

| ID | 검토 질문 | 부정 회귀 / 완료 증거 |
|---|---|---|
| R1 | `CODE_ANALYSIS`를 별도 Work 유형으로 두는 것이 Kernel의 `profile`, `work_purpose`와 충돌 없는가? | ISSUE Work의 MSC_AS_IS를 CODE_ANALYSIS Work로 오분류하지 않음 |
| R2 | `work_category` 신규 필드가 없어도 기존 Work/Snapshot/Index/Resume이 유지되는가? | 과거/타 호스트 snapshot 읽기, UNKNOWN=UNCLASSIFIED, machine index schema 불변 |
| R3 | Branch/commit 고정 MSC가 다른 branch·리베이스·force-push·dirty/untracked로 오적용되지 않는가? | A의 SHA로 B 질의 응답 불가, HEAD drift 시 STALE, dirty는 VERIFIED 금지 |
| R4 | Git source pin과 P4 haveRev/CL 증거를 구분하는가? | source authority 불명에서 PREVIEW_ONLY/차단 |
| R5 | Kernel `WorkUX.export_docs()`가 루트 README/시스템 인덱스를 재생성하므로 수동 수정이 유실되는 문제는 없는가? | exporter에서만 파생 뷰 갱신; 문서안내/기존 index 보호 |
| R6 | `module-library` 스캐너/기존 `knowledge_input` 및 `github_docs`와 신규 `by-type` 인덱스가 중복·충돌하지 않는가? | 필요 없는 파생 JSON/MD는 DEFER, 기존 마커/frontmatter/ID 재사용 |
| R7 | AS-IS MSC는 코드 사실의 증거인가, 그 결과의 가독형 표현인가? | Source CODE_FACTS/anchor/revision 없이 MSC를 독립 정본으로 확정 금지 |
| R8 | RAG 입력 본문·anchor·scope·root·owner·digest의 최종 검증을 누가 수행하는가? | 단순 검색 결과와 Provider 자기 보고 digest는 실소비 PASS 아님 |
| R9 | `MSC_AS_IS/MSC_TO_BE`와 실제 모듈 경계 participant가 가독성과 추적성을 함께 충족하는가? | TxMngr/DRX/BCH/RF_BLOCK 대표 폴더 매핑은 코드 근거 기준 검증 |
| R10 | 기존 G0/M1와 7대 차단 게이트 회피가 생기는가? | F-B1-01/02, F-N1-01, F-N3-01, F-N2-01/02, F-VERS-01 미검증 시 BLOCKED 유지 |

## 리뷰 결과 요구 형식

```text
REVIEW_STATUS: COMPLETED | PARTIAL | NOT_RUN
REVIEW_KIND: INDEPENDENT_STATIC | SELF_REVIEW | NOT_RUN
REVIEW_SCOPE: DELTA_R0001_TO_R0002
INPUT_COMMIT / INPUT_BLOB_SHA
EVIDENCE_LEVEL: E3(real host) / E2(actual code) / E1(document) / E0(no evidence)
CURRENT_TREE / INSTALLED_VERSION / MCP_MAPPING: VERIFIED | NOT_VERIFIED
ISSUES: [id, BLOCKING|MAJOR|MINOR, grounded evidence, impact, minimal fix, negative test]
DECISIONS: REUSE / CONNECT / EXTEND / DEFER per skill
G0, M1, SECURITY_STATUS / UNRESOLVED_GATE
INHOUSE_WRITES=0 / PROVIDER_CALLS=0 / WATCHER_CALLS=0
RESULT_REMOTE_POST: POSTED_VERIFIED | NOT_POSTED | UNVERIFIED
RESULT_COMMIT / REMOTE_READBACK: actual only
GPT_DISPOSITION_REQUESTED
```

- 리뷰가 불가능하면 `NOT_RUN/PARTIAL`로 기록하고 **PASS 소급 금지**.
- 개발자가 스스로 구현·시험한 동일 세션은 독립 리뷰 증거가 아님.
- 내부 소스코드, 내부 상세 경로, 특허/고객 자료, 토큰/키/로그/민감 MSC 원문은 GitHub PRIVATE에도 게시 금지. 반출 가능 여부 불명 시 `NOT_POSTED`.
- 허용된 비민감 결과 MD만 위 지정 경로에 PR 없이 직접 게시하고 원격 재조회로 commit/bytes 검증.

## 금지·운영 경계

**정적 설계 리뷰만** 수행. 소스·ZIP·설치본 변경, 사내 Git 쓰기, Job-list 활성화, Provider 실호출, 운영 DB/WAL/SHM·watcher·Telegram 변경, 신규 유료 모델 리뷰/REQUEST/READY, PUBLIC 게시, LIVE 전환 금지. `/AI-CONTINUITY/` 접근·변경 금지.

**실제 실행 시작 조건:** Windows Claude Code 독립 세션에서 **사용자가 이 정확한 GitHub repo/branch/path를 지정하여 대화형 리뷰를 수행**하거나, 별도 승인된 Dropbox LIVE 유효 REQUEST/READY가 접수될 것. 이 문서는 그 어느 실행도 수행하지 않는다.
