# L1 Review Accumulation — Step 2 통합 스키마 및 회귀 계약 설계 r0001

- Date: 2026-11-11 KST
- Workstream: L1-WORKSPACE-RAG-20261111-001
- Design status: `STEP2_CONTRACT_DESIGN_COMPLETE / SYNTHETIC_TEST_17_PASS / G0_NOT_VERIFIED`
- Review type: `GPT_DESIGN_CHECK`. `CLAUDE_INDEPENDENT_REVIEW=NOT_RUN`.
- Boundaries: `MIGRATION_NOT_CUTOVER / DROPBOX_LIVE`, 기존 스킬·Kernel 원장·사내 Git/MCP/DB/Job/Watcher·REQUEST/READY·PUBLIC 배포·LIVE 전환 변경 없음.
- This is an **abstract, non-sensitive, proposal**. No actual inhouse review, product code, Jira body, P4 depot path, or model/Provider response is included.

## 1. 근거, 기존 기능과 정확한 확장 한계

입력은 PRIVATE main의 `CURRENT.md`(Step 1 최신), `L1_REVIEW_ACCUMULATION_SKILL_IO_CONTRACT_AUDIT_r0001_20261111.md`, RAG r0002 및 GPT_SELF_REVIEW(5 BLOCKING/8 MAJOR/3 MINOR). PUBLIC `L1Work` code-analyzer v0.15.2, p4-code-owner v0.6.7, l1-github v0.3.56의 계약과 사용자 첨부 Kernel v0.7.37 코드를 참고했다. 사내 실제 설치본/호스트는 G0 미확인.

**새로 리뷰 엔진을 개발하지 않는다.** 기존 `l1-github pr-code-analysis`가 PR URL/번호를 정확한 base/head SHA, changed files/diff/handoff로 변환하고 `code-analyzer git-pr-range`가 그 범위의 의미 분석/AS-IS MSC를 담당. `p4-code-owner jira-fix-cl-scan`은 Jira 전체 댓글/Mango P4 근거를 바탕으로 L1 코드 수정 관련성만 `INCLUDED_L1 / EXCLUDED_NON_L1 / PENDING`으로 분류한다. 각각 실제 Root Cause와 테스트 PASS/공식 Owner 판정이 아니다.

**Kernel 실제 코드 제약:** `kernel.py::new()`는 `record.json` schema `1.0.1`에 Work 상태 및 `evidence_index`를 보유. `record_evidence(work_id, source_path, kind, stage, provider, provider_version, code_rev, ...)`는 등록된 provider/kind/stage/profile 슬롯과 원장 쓰기 가드를 확인한 뒤 Evidence를 복제/해시/기록한다. 새로운 CODE_REVIEW/ISSUE_REVIEW Evidence kind를 즉시 허용한다고 가정하지 않는다. `work_ux.py::export_docs` 및 `work_docs_navigation.py`가 `README.md`, `works/<work_id>/...`, `문서안내.md`, `index/{active,latest}.json`을 생성/보호하므로 **생성파일을 리뷰 원장 정본으로 덮어쓰지 않는다**.

## 2. 논리 객체 5종과 책임

| 객체 | 필수 논리 필드 | 의미·소유권 |
|---|---|---|
| `ReviewSession` | `review_id, review_thread_id, review_revision, review_kind, work_id, target, source_snapshot_id, collection_state, tool_run_refs, observed_at, review_state` | 1개 기준 source·revision의 코드/이슈 리뷰. Work 라이프사이클 SSOT는 Kernel 유지 |
| `Finding` | `finding_id, review_id, rule_id, scope_id, fingerprint, severity, claim_state, evidence_ref_ids, disposition, resolution_state, verification_state` | 각 리뷰 지적의 판정/해결/재검증. 동일 fingerprint라도 원본 Finding 삭제·병합 금지 |
| `SourceSnapshot` | `source_snapshot_id, product_id, root_id, source_system, build_scope, captured_at, scope_digest, workspace_state, owner_authority_status, root_authority_status` | Git/P4 코드 시점 및 scope의 immutable identity. 기존 실권한 출처를 참조 |
| `EvidenceRef` | `evidence_ref_id, source_snapshot_id, origin, artifact_kind, confidence_state, digest_sha256, verified_link_state, kernel_evidence_id?` | 원본 Kernel Evidence/Analyzer Run/PR/Jira/P4의 출처와 내용 해시. 본문 이중 정본 금지 |
| `FindingEvent` | `event_id, finding_id, review_id, seq, event_type, actor_id, occurred_at, prev_event_digest, event_digest` | 판정·수정 링크·테스트 PASS·재오픈·지식 Preview의 append-only 변화 기록 |

`ReviewThread`는 안정적인 Work+target+review_kind의 **묶음 개념**이며 별도 신규 Work가 아니다. 같은 PR에 새 HEAD가 올라오면 thread는 유지하고 새 ReviewSession을 만들고, 원본 리뷰 ID를 보존한다. ISSUE Work에서 발생한 CODE_REVIEW도 Work category를 임의 CODE_ANALYSIS로 변경하지 않는다.

## 3. Git/P4 SourceSnapshot 변종과 정확성

Git 변종은 `repository_id, requested_ref(branch label), pinned_commit_sha(전체 SHA), worktree_id`를 포함해야 한다. HEAD drift/dirty/untracked/scoped-file digest 불일치 때 VERIFIED와 Knowledge 게시를 차단한다. branch label만으로 '현재 코드'를 나타내지 않는다. 두 branch의 SHA가 동일해도 branch provenance와 요청 scope를 별도 보존한다.

P4 변종은 `depot_id, client_id, files[]{file_id, have_rev, submitted_cl?}`를 포함한다. 하나의 CL로 모든 파일 haveRev를 대체하지 않는다. integration 원본 수정 CL과 현재 branch 반영 CL, 코드 저자와 공식 조직 Owner를 구분한다. 파일 이동/복사 추정은 공식 lineage와 분리한다.

Git과 P4 자료를 하나의 무형식 `revision` 필드로 병합하지 않는다. SourceSnapshot과 Finding의 scope, Evidence의 source_snapshot_id가 불일치하면 그 리뷰 Finding을 CODE_CONFIRMED로 승격할 수 없다.

## 4. Work/Review 상태 축 분리

- `work_category=ISSUE/FEATURE/REFACTOR/DESIGN/CODE_ANALYSIS/UNCLASSIFIED`: 사용자 Work의 주목적(**제안 필드**, Kernel 설치본 미구현).
- `review_kind=CODE_REVIEW/ISSUE_REVIEW`: Work 안에서 발생한 리뷰 활동.
- `artifact_kind=CODE_FACTS/MSC_AS_IS/MSC_TO_BE/PR_DIFF/JIRA_RECORD/P4_CL_EVIDENCE/TEST_RESULT/REVIEW_COMMENT/OTHER`: 산출물/증거 종류.
- Kernel `profile/work_purpose/lifecycle`: 기존 실행 및 권한. 이 값과 리뷰 종류를 혼동하지 않는다.
- `claim_state=CODE_CONFIRMED/INFERENCE/QUESTION/CONTRADICTED/UNKNOWN`는 기술 주장 신뢰도, `disposition=PENDING/ACCEPT/ACCEPT_WITH_CHANGE/REJECT/HOLD/MORE_INFO`는 검토자 판단, `verification_state=PASS/FAIL/SKIP/NOT_RUN`은 회귀시험의 실제 결과. 별개로 기록한다.
- `resolution_state=OPEN/IN_PROGRESS/FIXED_UNVERIFIED/VERIFIED_CLOSED/REOPENED/WONT_FIX/DUPLICATE_LINKED`. `FIXED_UNVERIFIED`를 `VERIFIED_CLOSED`와 합치지 않고 결함 반복 시 새 이벤트로 REOPEN한다.

기존 Kernel confidence는 `AUTO_CANDIDATE/HUMAN_CONFIRMED/REJECTED/SUPERSEDED`가 공식이다. 외부 논리 스키마의 `UNKNOWN`은 adapter 표시 fallback일 뿐 기존 Kernel 원장에 추가하지 않는다.

## 5. ID, 중복·재시도·이력 보호 (후보 계약)

`target_identity=(authority_id,target_type,target_id)`; PR 번호 단독은 전역 ID가 아니다.

`review_thread_id = stable_id("thread-v1", work_id, review_kind, target_identity)`.

`source_snapshot_id = stable_id("snapshot-v1", product, root, VCS authority, build, pinned Git full SHA / P4 sorted file#rev manifest, scoped file digest, workspace state)`.

`review_id = stable_id("session-v1", review_thread_id, source_snapshot_id, explicit_review_iteration)`. 동일 모델/Tool 재시도로 run_id만 바뀌면 같은 review_id; 사용자 승인된 별도 재리뷰면 iteration 증가. `finding_id = stable_id("finding-v1", review_id, finding_local_id)`.

`fingerprint`는 `rule_id + normalized mechanism + module/symbol/scenario + product/scope`의 **후보 중복 검색키**다. 동일 hash라도 같은 사실/해결책을 의미하지 않는다. 서로 다른 리뷰 원본과 Evidence는 삭제하지 않고 `DUPLICATE_LINKED` 또는 supersession 관계만 추가한다. Canonical ID 계산 규약(필드 순서, 길이 prefix, UTF-8 정규화, scope ID)은 G0/M0에서 확정해야 하며, 시간/표제만으로 생성 금지.

Event는 append-only `seq=1..N`, 이전 digest 참조, actor/occurred_at를 기록. 동일 event_id와 동일 bytes를 재수신하면 idempotent no-op, 동일 event_id와 다른 bytes는 `IDEMPOTENCY_CONFLICT`. 동시 호스트 수정은 최신 버전과 마지막 digest 기준 compare-and-swap 실패 시 `CONFLICT_PENDING`으로 보존. 단순 hash chain은 **서명·검증된 actor·원자적 CAS를 대체하지 않는다.** 이번 합성 테스트의 local event hash는 운영 인증 기제가 아니다.

## 6. 저장·표시 구조에서 하지 말아야 할 일

`record.json`의 Work/Evidence SSOT와 Kernel Journal을 유지한다. 제안 Review Ledger는 기존 Kernel에서 지원 가능한 등록 Evidence 슬롯과 실제 Work Docs exporter/sidecar 책임을 확인하기 전 **논리 모델**이며, `record.json`에 임의 키를 넣거나 물리적 `works/<work_id>/reviews` 경로를 생성하지 않는다.

기존 `README.md`/`문서안내.md`/`index/active.json`/`index/latest.json`은 **파생 표시**만. 기존 Snapshot/Resume, 수동 파일 보호, PC 간 sync/dirty/diverged, Git Push Guard 및 code-analyzer Run-retention 보호는 별도 회귀시험 대상이다.

RAG `module-library`로 이동할 경우 `KnowledgeCandidate`에 source revision/evidence/review ID를 걸고, `NEW/ENHANCEMENT/DUPLICATE/CONFLICT/RECHECK` Preview+owner/source authority+승인 후 사내 Git 게시/readback. `REVIEWED`나 AI Finding의 `ACCEPT`만으로 승격하지 않는다. 사외 PRIVATE는 회사 코드/MSC/Jira 원문 반출 허가 대상이 아니다. RAG Provider input M1는 기존 7대 게이트가 풀릴 때만 PASS 가능.

## 7. 직접 실행한 합성 계약검증

이 세션에서 **임시 Linux 작업 디렉터리에서 Python 3 + jsonschema 4.26.0**을 사용해 JSON Schema Draft 2020-12의 schema 유효성을 검사하고, 추가 cross-object 의미 검증을 수행했다. 완전 합성 `PRODUCT-A`/`PR-123`/`FILE-1`만 사용했다.

**17 PASS / 0 FAIL.** 정상 Git/P4(2 ACCEPT), 동일 review_id 재입력, 없는 source snapshot/evidence, 불량 SHA, Git-P4 필드 혼용, 증거 없음/깨진 링크, NOT_RUN인데 VERIFIED_CLOSED, CREATED 누락, 임의 승인 필드, event 내용 digest 변조, 댓글 PARTIAL의 거짓 완료, owner EXPIRED, 추론을 CODE_CONFIRMED로 오인, 동일 P4 파일을 두 revision에 중복 등록 등 **15개 REJECT**가 의도대로 처리됨.

이 `PASS`는 합성 데이터의 **허용/거부 예측 일치**일 뿐 실제 운영 검증이 아니다. JSON Schema만으로 교차 객체 링크·CAS·실제 content digest·Owner signature·PR/Jira MCP pagination·RAG provider payload를 증명할 수 없다. 이 회차의 의미 검사는 별도 합성 reference checker다. 실제 Kernel provider slot·실환경/Windows 시험 `NOT_RUN`.

## 8. 반드시 남길 문제 및 회귀 요구

| Issue | Severity | Change / regression requirement |
|---|---|---|
| RL-B01 | BLOCKING | Kernel `record_evidence`의 provider/kind/stage/profile registry G0 확인 전 임의 review kind 저장 금지. 미지원 슬롯에서 기록 0 |
| RL-B02 | BLOCKING | Owner/root authority, trusted pre-call digest, Job-list pre-enqueue/direct guard, 실제 설치·버전 미검증. M1 `BLOCKED` 유지 |
| RL-B03 | BLOCKING | 사내 리뷰 Evidence와 사외 협업/외부 저장소의 보안 분리. 반출금지 원문 외부 전송 0 |
| RL-M01 | MAJOR | GitHub 실제 PR review/comment/approval/dismissed 및 댓글 pagination API 인벤토리 필요. 일부 수집은 PARTIAL |
| RL-M02 | MAJOR | 안정 ID/event chain/CAS/retry cross-host 저장소·writer 미선정. 동일 요청 중복 0, 충돌 시 이력 손실 0 |
| RL-M03 | MAJOR | Analyzer Run-retention과 영구 Work evidence 링크 보호 미검증. 오래된 Run compact 전 원본 ID/해시 확인 |
| RL-M04 | MAJOR | Git A/B drift/P4 file#rev/MSC_AS_IS·MSC_TO_BE/Work type 축 분리와 legacy export 호환성 실제 시험 필요 |
| RL-m01 | MINOR | Work/review/findings/verdict/test status의 사용자 UI 구분 및 breadcrumb |

## 9. 후속 G0 read-only 및 실제 시험 게이트

| Gate | 직접 확인할 사내 입력 | 완료/거부 기준 |
|---|---|---|
| H01 | Kernel 설치버전·registry 슬롯·record JSON/Evidence/Journal | 기존 Work/수동문서/schema 무손실, 새 종류 불허면 쓰기 0 |
| H02 | l1-github PR base/head/handoff와 PR review+comment tool | exact SHA와 모든 댓글·approval 상태, 미수집을 COMPLETE로 오표시 금지 |
| H03 | code-analyzer run/evidence index/MSC/source scope | scoped SourceSnapshot 일치, inference와 code fact 구분 |
| H04 | Jira/Mango 실제 MCP, P4 submitted/files/origin | 불완전 댓글/미확정 integration은 PENDING |
| H05 | Git A/B rebase+worktree, dirty/untracked/symlink, P4 mixed haveRev | stale/다른 범위를 CODE_CONFIRMED로 자동 사용 금지 |
| H06 | 재리뷰·재오픈·동시 호스트 이벤트 | finding_id/이력 보존, duplicate 0, CAS 충돌 안전 |
| H07 | Export/old Snapshot/manual docs/Resume/Run-retention | Work root/index/기존 링크 호환성 |
| H08 | 승인된 Knowledge Preview/사내 Push Guard/외부 DLP | 승인 없이 지식/사외 게시 0 |
| H09 | 실제 Provider input/owner/root/Job gate | 제목 검색만 성공할 때 M1 PASS 금지 |

**Outcome:** `STEP2_DESIGN_COMPLETE / SYNTHETIC_TEST_17_PASS / IMPLEMENTATION_NOT_RUN / INHOUSE_HOST_NOT_VERIFIED / RAG_M1_BLOCKED / CLAUDE_REVIEW_NOT_RUN`.

**Next one action:** 사내 G0 H01–H04 **읽기 전용** 기존 설치 스킬·tool/action·Kernel 등록 슬롯 인벤토리 확보 후 `ReviewSession + Finding` 최소 connector 구현/회귀 범위를 확정한다. 기존 스킬·운영 환경·REQUEST/READY·LIVE 변경 없음.
