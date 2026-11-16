# L1 Knowledge 확정 ①~④ — Claude R1 결과·영수증 GPT 판정
- 날짜: 2026-11-17 KST
- 기존 Work: `L1-WORKSPACE-RAG-20261111-001`
- 요청: `REQ-L1-WORK-KNOWLEDGE-FIXED-R1-20261116` revision 1
- 원본 리뷰: `collab/reviews/REQ-L1-WORK-KNOWLEDGE-FIXED-R1-20261116/REVIEW_RESULT_1.md`
- 원본 영수증: `collab/receipts/REQ-L1-WORK-KNOWLEDGE-FIXED-R1-20261116/RECEIPT_1.md`
- 원본 dispatch: `collab/dispatch/REQ-L1-WORK-KNOWLEDGE-FIXED-R1-20261116/DISPATCH_1.md`
- 고정 입력 ZIP SHA-256: `58d39bcf884d9fbd22d03a14e5fffde5e1b69a8ecec482d2e9c8b2b125add7bb`

## 1. 원격 결과/실행 근거
- PRIVATE main에서 REVIEW_RESULT_1.md 원격 읽기 확인. `execution_status: COMPLETED`, 원판정 `ACCEPT_WITH_CHANGE`, BLOCKING 1/MAJOR 4/MINOR 2.
- RECEIPT_1.md 원격 읽기 확인. `ok:true`, `watcher_version:0.2.23`, `processing_key` 및 request ID/rev/package SHA가 결과와 일치.
- DISPATCH_1.md도 동일 processing_key, `reserved_at:2026-11-16T15:07:14.506070+00:00` 포함.
- 비용 `$0.27`은 사용자에게서 전달된 금액이며 위 339-byte RECEIPT_1.md에는 비용·토큰·provider 세부가 없음. **비용 세부 실측=NOT_VERIFIED**, 외부 비용 원장/Windows watcher DB가 필요. 영수증 존재로 비용 세부를 추정하지 않음.
- 기존 `REQ-L1-WORK-KNOWLEDGE-DESIGN-20261115-001`의 receipt 디렉터리 조회는 404(조회 시점); reviewer 자신도 선행 실행 이력을 직접 검증하지 못했다고 명시. 고정 구버전 요청을 재호출·취소·수정하지 않고 watcher 현장 DB 중복 검사는 별도 보존.
- 본 리뷰 입력은 비민감 설계 MD 3개뿐. **스킬 소스 코드 검토/실행·Linux MCP·업무 호스트·Knowledge 게시와 E2E 시험 전부 NOT_RUN/NOT_VERIFIED**.

## 2. GPT 종합 판정
**`REVIEW=ACCEPT_WITH_CHANGE` / `DESIGN_DIRECTION=KEEP` / `IMPLEMENTATION_READY=BLOCKED_PENDING_G0_AND_GUARDS`.**
리뷰 1회는 완료; 이번 설계 보완은 **새 리뷰/유료 호출 없이** 기존 Work에서 수행. 사용자 고정 방향 ①~④ 유지. 원래 R1 문서는 고치지 않음.

| 지적 | GPT 판단 | 최소 설계 보완·소유 |
|---|---|---|
| BLOCKING B01 Work 역링크 계약 모순 | **수용** | 기존 `work_refs.REF_TYPES`에 지식 타입 없음. `alias/code_root` 오용 금지. 필수 origin 링크는 **개인 Knowledge 쪽에 Work ID/근거 링크로 보존**, 기존 Work 쪽 구조화 역링크는 실제 허용 기록 API가 검증될 때만 추가. 미지원이면 `WORK_BACKLINK=PENDING`으로 남기고 지식→Work 링크와 그룹 게시 결과를 보존. `knowledge` ref_type이나 새 Kernel 원장 선제 추가 금지. 단 개인 metadata 표현·게시 제외 동작은 업무 호스트 G0 필요. |
| MAJOR M01 Workflow write protection | **수용·원칙/강제 구분** | Workflow READ_ONLY/Updater WRITE_ONLY 정책 고정. 실제 강제는 raw Git 우회 불가를 입증하는 OS 사용자/credential 분리 + 권한 제한된 checkout 또는 동등하게 검증된 단일 전용 writer가 필요. 기존 동일 자격증명의 raw git 가능하면 `HARD_GUARD=NOT_VERIFIED` 및 보호된 게시 차단. `l1-fix-workflow` 자체 path deny는 심층 방어만. |
| MAJOR M02 공통 clone 경합 | **수용** | `l1-github`/기존 Git writer의 staged-path allowlist, 인증된 actor, lock/직렬화, HEAD 재조회/CAS를 우선 확인. 없으면 실제로 입증된 최소 보완만. 격리 checkout/worktree 활용 가능 여부 확인; 임의 독립 writer/DB 추가 금지. |
| MAJOR M03 구조 변경 | **수용** | 그룹 측 rename/move/delete, 경로·ID/variant 변경, 파생 링크 영향은 Git의 자동 merge 성공 여부에 무관하게 `CONFLICT/HOLD`. 사용자 재승인 + 최신 HEAD 확인 전 게시 금지. |
| MAJOR M04 exporter 보존 | **수용** | `work_ux.export_docs` 동작 T01/T02 격리 회귀를 **필수 선행 게이트**로 승격. knowledge 해시 보존·README 유효 링크 검증. |
| MINOR m01 revision 단위 | **수용** | **그룹 전체 commit SHA**를 CAS 기준; **파일별 원격 blob/content SHA-256**과 불변 Base 내용 위치를 3-way 입력으로 명시. Base 복원 불가 시 HOLD. |
| MINOR m02 retry 한도 | **수용** | 개인 상태·링크 복구 **최대 3회**, 짧은 지수 backoff 이후 `PENDING_MANUAL_RECONCILIATION`; 그룹 게시 재시도 0. 유효 기존 공통 retry 정책이 확인되면 이를 우선. |

## 3. 검증 및 실행 경계
- Claude 제안 T01~T10은 **시험 계획이며 실행 PASS 아님**. 사용자 확정 결정 ① 물리 mirror, ② Updater 소유/Workflow READ, ③ optional Work ID, ④ Base/Ours/Theirs/승인/CAS/readback은 유지.
- 스킬 설계 개정: [`L1_KNOWLEDGE_UPDATER_SKILL_DESIGN_r0002_20261117_KST.md`](L1_KNOWLEDGE_UPDATER_SKILL_DESIGN_r0002_20261117_KST.md).
- 실제 회사 지식의 그룹 폴더 구조·Updater 및 그룹 writer API·호스트 설치 권한은 현 시점 미조회. 따라서 `KNOWLEDGE_WRITE=NOT_RUN`, `SKILL_PATCH=NOT_RUN`, `HOST_E3=NOT_VERIFIED`, `NEW_PAID_REVIEW=0`.
- PRIVATE 문서 게시가 실행·승인·그룹 수정·PUBLIC 전달이나 스킬 설치를 의미하지 않음.

**NEXT_ONE_ACTION:** 업무 GPT가 실제 설치본과 현재 그룹 구조·Git writer 권한/API를 READ_ONLY G0 매핑하고, 이 r0002 설계의 필수 게이트를 입증한 뒤 최소 패치 대상 확정.