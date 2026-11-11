# L1 Knowledge Updater K5.8 / K6 및 l1-fix-workflow 연계 계약 — 개정 설계 r0003

- Date: 2026-11-11 KST
- Kind: `GPT_DESIGN_REVIEW + INHOUSE_G0_HANDOFF`; **설계 제안**. 사내 기존 Updater 원문/K5.8/K6/설치본을 직접 읽은 결과가 아님
- Change driver: 그룹 합의에 따라 그룹 `l1sw-dev-knowledge`는 코드 기준 HLD, detailed design, 확인된 AS-IS MSC, 설계 변경과 재사용 가능한 기술적 이슈 히스토리까지 관리
- Preserved: 기존 공개 r0002 인계서, private RAG/Workflow 설계, Work Ledger 기록, 운영 스킬 및 그룹 정본은 변경하지 않음
- Gate: `G0_AS_IS_K58_K6=NOT_VERIFIED`, `INHOUSE_E2E=NOT_RUN`, `GROUP_PUBLISH=NOT_RUN`, `RAG_M1=BLOCKED`, `MCP_EXPORT=NO_EXPORT`.

## 0. 검토 증거 및 미확인 경계

**확인한 자료(E1/E2):** 공개 사내 인계용 `L1_KNOWLEDGE_UPDATER_WORKFLOW_INHOUSE_HANDOFF_r0002_1111.md`, private `L1_E2E_INHOUSE_OFFSITE_ARCHITECTURE_r0002_20261111.md`, `L1_INHOUSE_GPT_OPENCODE_HANDOFF_r0002_20261111.md`, `L1_REVIEW_ACCUMULATION_G0_PARTIAL_AUDIT_r0001_20261111.md`, 프로젝트 `CURRENT.md`. G0 보고서에 따르면 공개 Kernel dev 패키지의 등록된 `code-analyzer/analyze/asis_msc` 슬롯은 실소스·격리시험에서 확인되었으나 `code_review`, `issue_review` Evidence kind 및 `p4-code-owner` direct provider 등록은 **미지원**이다. 이는 회사 설치본 E3 검증이 아니다.

**확인하지 못한 실제 AS-IS:** 사내 개발 `l1-knowledge-updater`의 `K5.8 tier`의 현행 tier 목록/조건/예외, `K6 MSC` 원문, 그룹 writer 권한, 실제 Workflow/Kernel 연결 구현, 사내 릴리스 버전. 따라서 아래 K5.8/K6 수정 사항은 **목표 정책(TO-BE)**이며 원래 tier 명칭을 새 명칭으로 덮어쓰거나 기존 사용 동작이 곧바로 실패라고 단정하지 않는다. 사내 GPT/OpenCode가 G0에서 원문/entrypoint/테스트로 `AS_IS → TO_BE` 차이를 작성해야 한다.

## 1. 책임과 지식 정본

| 시스템 | 단일 소유권 | 구체적 책임 | 권한 범위 |
|---|---|---|---|
| `l1-fix-workflow` | **요청/Work 라이프사이클 조정** | ISSUE/FEATURE/REFACTOR/DESIGN/CODE_ANALYSIS intent(후보), 기존 Work 탐색, 수행 계획, 코드 분석 호출, Evidence 접수와 Updater handoff | 그룹 지식 본문을 직접 덮어쓰지 않음. 분류 후보를 Kernel 실행 profile로 임의 전환하지 않음 |
| `work-ledger-kernel` | **Work ID/Work 상태/Evidence 원장** | Work ID 발급·재개, 허용 registry slot의 Evidence, 원본·SourceSnapshot, 원장/파생 README/index | 새 K5.8/K6 정보를 `record.json`/Evidence 임의 필드에 삽입하지 않음 |
| `code-analyzer` 및 Git/P4 보조 스킬 | **분석 근거 생성** | CODE_FACTS, 코드 revision 고정, AS-IS/TO-BE MSC 후보, 이슈/코드리뷰 근거 | 게시 권한 없음. 분석 성공 자체가 현행 검증·수정 완료를 뜻하지 않음 |
| `l1-knowledge-updater` | **기술 지식 후보 평가와 갱신 오케스트레이션** | 기술 분류(module/feature/scenario), tier/지식 종류, 기존 지식 차이, 중복·충돌, K6 MSC 검증, preview, 그룹 소유자 승인 요청, 게시·readback·Work 역링크 조정 | 유효 게시 권한/승인 없는 그룹 write 금지. Kernel Work ID 자체 발급·상태 원장 대체 금지 |
| 개인 `l1-workspace` | **작업 진행·개발 이력 정본** | 임시 분석/실험/미해결/코드 변경 과정, 이슈·리뷰·시험 히스토리, Evidence/Work ID, 그룹 게시 지식 포인터 | 그룹에서 승인된 같은 상세 지식을 별도 ‘최신 기술 정본’으로 중복 유지하지 않음. Work 이력은 삭제하지 않음 |
| 그룹 `l1sw-dev-knowledge` | **공유 기술 지식 정본** | 현행 HLD/상세설계/AS-IS MSC, 기술적으로 검증된 이슈 분석과 해결 패턴, 승인된 설계 변경 및 버전 계보 | 상태·제품/RAT/브랜치/revision 분명히 표시. TO-BE를 AS-IS로 위장 금지. 그룹 owner 게시 정책 준수 |

## 2. K5.8 tier 정책 개정 권고 (AS-IS 원문 확인 필요)

### 2.1 분리해야 할 **세 축**

**기존 K5.8 tier는 유지하되**, 해당 tier가 '개요냐 상세냐'를 기준으로 GROUP/PERSONAL을 바로 결정한다면 그 조건을 바꿀 것을 권고한다. 내부 tier 이름·번호는 원문 확인 후 매핑하며 현 단계에서 변경·삭제하지 않는다.

1. `knowledge_kind` — 기술 콘텐츠 분류: `OVERVIEW / HLD / DETAILED_DESIGN / CODE_FACTS / MSC_AS_IS / MSC_TO_BE / DESIGN_CHANGE / ISSUE_HISTORY / REVIEW_FINDING` (논리 예시; 실제 스키마 필드가 아님).
2. `validation_state` — 신뢰·실행 현재성: `DRAFT / CODE_VERIFIED / DESIGN_APPROVED / FIX_INTEGRATED / TEST_VERIFIED / STALE / SUPERSEDED / UNKNOWN` (상호 배타적 단일 상태라기보다 필요한 경우 설계 승인/구현/시험 축을 별도 필드로 분리).
3. `publication_decision` — 정본 위치/권한: `WORKSPACE_ONLY / GROUP_CANDIDATE / GROUP_APPROVAL_PENDING / GROUP_PUBLISHED / REJECTED / LINK_PENDING`.

**결정식:** *기술 상세도는 저장소 선택 조건이 아니다.* 그룹 게시 여부는 재사용 가능한 기술 지식인지, 근거·적용 범위가 충분한지, 중복/충돌 및 그룹 소유자 승인이 해결됐는지로 결정한다. 진행 중 Work 원장은 개인에 남는다. 그룹에도 ‘진행 중인 사실’(검증된 원인 등)을 게시할 수 있지만 **미해결/미적용 상태를 명시**해야 한다.

### 2.2 권고 라우팅 판정표

| 입력 유형 | Workspace | 그룹 지식 업데이트 | 그룹 게시 내용의 상태 |
|---|---|---|---|
| 현재 분석 중인 이슈의 메모/가설/미검증 로그 | Work·Evidence 보존 | 아직 미게시 | `DRAFT / NOT_VERIFIED` |
| 기존 소스에 존재하는 코드 흐름이 고정 revision/anchor로 확인됨 | 분석 Work 유지 | HLD/상세설계/AS-IS MSC 후보 | `CODE_VERIFIED` + 제품·브랜치·revision |
| 승인된 기능/설계 변경이나 새 설계 HLD, 구현 전 | 설계 Work·승인 이력 유지 | **설계 상태가 표시된** 변경 이력 게시 후보 | `DESIGN_APPROVED / NOT_IMPLEMENTED` (AS-IS 아님) |
| 이슈 원인이 기술적으로 검증, 수정은 진행 중 | ISSUE Work·가설/시험 이력 유지 | 재사용 가능한 이슈 증상·원인·회피 조건 후보 | `CAUSE_VERIFIED / FIX_PENDING` |
| 수정 반영 및 회귀시험 확인 | ISSUE Work/PR/CL/Evidence 유지 | 이슈 히스토리 및 영향받은 HLD/상세설계/MSC 개정 후보 | `FIX_INTEGRATED / TEST_VERIFIED` (각각 독립 증거) |
| TO-BE MSC 추정, 해당 코드 미구현 | Work 설계 후보 유지 | 승인된 설계 절로만 별도 후보, **현재 AS-IS로는 미게시** | `PROPOSED/APPROVED_DESIGN; NOT_AS_IS` |
| 다른 브랜치의 MSC, 소스 drift, 검증 누락 | 기존 Work 근거 유지 | 현 요청 scope에 대한 VERIFIED 게시 차단 | `STALE / SCOPE_MISMATCH` |

승인 대상/편집 권한/게시 시점은 그룹 운영 정책에 따른다. 시스템의 단일 `tier`값에 모든 진척 상태를 과적하지 말고 독립 metadata 또는 관리된 sidecar/manifest를 검토한다. 현행 tier 라벨은 기존 reader 호환을 위해 유지하고 새 분류는 점진 도입한다.

## 3. K6 MSC 정책 개정 권고 (AS-IS 원문 확인 필요)

### 3.1 핵심 변경

- **기존 정책이 상세 MSC를 개인 Workspace 전용으로 고정했다면 해당 제약을 제거**한다. AS-IS MSC는 그룹 기술지식의 정식 게시 후보가 될 수 있다.
- 게시 전 `MSC_AS_IS`와 `MSC_TO_BE`를 명시적으로 구분한다. HLD/설계 변경 과정에서 작성한 TO-BE는 코드 실체와 혼합하지 않는다.
- 실제 코드의 소스 스냅샷을 고정한다: Git full commit SHA + branch(표시 정보) + dirty/untracked + 제품/RAT/module scope 또는 P4 실제 file#rev/haveRev + client/CL(단서). Branch 이름이나 CL 번호 하나만으로 모든 파일 revision을 대표한다고 가정하지 않는다.
- MSC의 중요한 메시지/상태 변화는 CODE_FACTS 함수/문장 anchor 및 EvidenceRef와 추적 가능해야 한다. 정적 분석으로 확인되지 않는 타이밍/런타임 동작은 `INFERRED/UNVERIFIED`로 표시한다.
- participant는 기존 표시 가독성 정책을 **재사용**한다. 마지막 의미 있는 폴더 단위의 alias 예: TxCfgMngr/TxCmdMngr → `TxMngr`, BCH_CTRLR → `BCH`, DRX_CTRLR → `DRX`, RF_BLOCK → `RF_BLOCK`. 사람이 보는 alias와 정규화 participant ID(전체 소스/모듈 범위)는 별도 관리해 동명 충돌을 피한다.
- 그룹의 기술 탐색은 `module → feature → scenario → MSC`로 연결하되, 기존 문서 구조와 ID를 우선 사용한다. 같은 MSC를 개인과 그룹에 독립 정본 2개로 유지하지 않고 **Work→그룹 게시 revision**을 참조한다.
- 그룹에 과거 버전 MSC가 남는 것은 허용하되 `HISTORICAL/SUPERSEDED` 및 해당 pinned source와 적용 조건을 명시한다. 신규 질문에서 임의로 현행 AS-IS로 승격하지 않는다.

### 3.2 MSC 게시/갱신 조건(모두 필요한 게이트)

`CANDIDATE → PINNED_SOURCE → EVIDENCE_VERIFIED → DIFF_PREVIEW → OWNER_APPROVED → PUBLISHED_READBACK → WORK_LINKED`.

- 대상 코드가 없으면 생성할 수 있는 것은 `DESIGN_MSC`/`MSC_TO_BE` 초안뿐. 기존 코드의 현행 동작이라고 표시하지 않는다.
- 그룹 기존 지식과 충돌하면 자동 승격/덮어쓰기 금지. `CONFLICT`에 원인과 비교 대상 revision을 남기고 검토한다.
- 읽기만 확인된 분석 결과와 실제 그룹 Git 게시(readback 검증)를 서로 다른 상태로 기록한다.
- 게시 성공 뒤 Workspace 링크 실패 시 **그룹 게시를 반복하지 않고** `PUBLISHED_LINK_PENDING`으로 정산.

## 4. 기술 이슈 히스토리 구조 — 그룹과 Work 관계

그룹에 재사용 가능한 **한 건의 issue knowledge**에는 다음 의미 필드가 필요하다(실제 파일 저장 형식은 G0 후 결정):

- `scope` : product/RAT/module/feature/scenario 및 관련 source revision.
- `symptom` : 어떤 조건에서 무엇이 관측됐는가(확인된 사실 vs 추정 구분).
- `root_cause` : 확인된 원인/가설/미확인 사항 및 근거 수준.
- `design_change` : 적용 예정/승인/실제 반영 여부, 변경 이유, 영향 범위.
- `fix` : Git commit/P4 revision 등 실제 수정 확인 여부, 미적용/미검증 상태.
- `verification` : 실제 재현/회귀시험과 범위, PASS/FAIL/NOT_RUN을 독립 표시.
- `reusability` : 적용 조건, 재발 방지 규칙, 관련 HLD/MSC/다른 issue 지식 ID.
- `provenance` : origin Work ID(s), EvidenceRef(s), source revision, published knowledge ID, publication revision, 승인/읽기 검증 영수증.

이슈 자체의 진행·토론·시험 로그는 개인 Work 원장에 남고, **기술적으로 재사용 가능한 결론과 변경 상태**만 그룹 지식으로 정리한다. `CAUSE_VERIFIED`와 `FIX_INTEGRATED`, `TEST_VERIFIED`를 하나의 `RESOLVED` 필드로 뭉개지 않는다.

## 5. Workflow ↔ Updater ↔ Kernel 연계 계약(논리 API, 실제 구현 아님)

### 5.1 메시지의 최소 공통 필드

```text
WorkContext {
  work_id?              // 있으면 재사용; Kernel 발급을 Workflow가 조정
  request_id            // 호출 계층 멱등키, 재시도에도 동일
  work_category?        // ISSUE | FEATURE | REFACTOR | DESIGN | CODE_ANALYSIS (제안)
  execution_profile?    // 기존 Kernel profile/work_purpose와 별개
  source_snapshot       // source_system, product/RAT, module scope, pinned revision, tree state
  tool_contract_version?
}
ArtifactRef {
  artifact_id, work_id, artifact_kind, evidence_ids[], source_snapshot_ref,
  content_digest, validation_state
}
KnowledgeCandidate {
  candidate_id, work_id, artifact_refs[], knowledge_kind, module/feature/scenario,
  target_knowledge_id?, target_revision?, content_delta_digest,
  source_snapshot_ref, conflict_state, publication_decision
}
PublicationReceipt {
  candidate_id, knowledge_id, publication_revision, approved_actor_ref,
  approval_receipt_ref, write_commit, remote_readback_digest, status
}
```

`content_digest`/`source_snapshot_ref`는 포인터·해시일 뿐 원본의 사외 반출 승인이 아니다. Kernel 필드와 registry를 무단 확장하지 않고 **별도 연결 manifest/sidecar** 또는 설치본의 이미 허용된 기능을 우선 검토한다. 문자열/ENUM/필드 타입과 명칭은 G0의 실제 설치 계약으로 최종 매핑한다.

### 5.2 요청·응답 단계 계약

| 단계 | 호출/책임 | 필수 입력 | 출력/멱등성 | 실패 시 |
|---|---|---|---|---|
| 0. 기존 Work 탐색 | Workflow → Kernel | request_id, 사용자 의도/기존 work_id | **한 개** `work_id`, resume/new 판정 | 모호하면 사용자 확인, 중복 생성 금지 |
| 1. Work 분류 | Workflow | request + source scope | work_category 후보, work 목적/현행 profile 별개 | `UNCLASSIFIED` 보존; 전권 분류 금지 |
| 2. 분석 지시 | Workflow → code-analyzer/Git/P4 | work_id, 고정 소스 revision | ArtifactRefs + 기존 허용 Evidence ID | 허용 registry/provider/kind 불일치면 거부 |
| 3. 지식 후보 생성 | Workflow 또는 사용자 진입점 → Updater | `WorkContext + ArtifactRef[]` | KnowledgeCandidate, K5.8 기술 분류/게시 후보 | 원본 근거/적용범위 누락이면 Workspace-only |
| 4. K6 MSC 게이트 | Updater | MSC_AS_IS/MSC_TO_BE, code anchors, revision | AS-IS verified 여부/TO-BE 분리 | `SCOPE_MISMATCH`, `STALE`, `PREVIEW_ONLY` |
| 5. 중복·충돌 Preview | Updater → 그룹 기존 reader | knowledge_id, expected_revision, 후보 diff | NEW/UPDATE/NO_CHANGE/CONFLICT 및 preview digest | CAS 충돌 시 재검토; 승인 무효화 |
| 6. 게시 승인 | 그룹 Owner 승인 채널 | candidate_id, target_revision, preview digest | 단일 approval receipt | 승인 없으면 그룹 write 0 |
| 7. 그룹 게시 | 권한 있는 기존 writer(Updater 조정) | 승인 받은 불변 candidate 및 expected revision | commit + **원격 readback** + receipt | 네트워크/uncertain 상태에서 중복 게시 금지 |
| 8. Work 역링크 | Workflow/Kernel의 허용된 저장 계약 | receipt + work_id + knowledge_id | link receipt 또는 PUBLISHED_LINK_PENDING | 그룹 다시 게시하지 않음, 링크 정산 |
| 9. RAG 조회 | 기존 검증된 RAG driver | question scope + published knowledge revision | 실제 본문 anchor/권한/Provider payload 검증 | 링크 검색만으로 M1 PASS 선언 금지 |

### 5.3 호출 소유권/경쟁조건

- **지식 업데이트로 진입:** Updater가 module/feature/scenario를 질문하더라도 Work 원장이 필요한 코드/이슈 분석 단계는 Workflow의 기존 Work 연결 기능을 사용한다. **Updater가 Work ID를 별도로 직접 발급하지 않는다.**
- **이슈·코드 분석으로 진입:** Workflow는 Work/Evidence를 먼저 보존하고 Updater에 게시 후보를 인계한다. Updater가 코드 분석기를 다시 실행해 새 Work를 만들지 않도록 `work_id + artifact_id + source_snapshot_ref`를 넘긴다.
- **동시 호출/재시도:** `request_id` 기반 request dedupe와 `candidate_id + expected target_revision + preview_digest` 기반 publication dedupe. 승인 당시와 현재 지식 revision이 다르면 승인 재취득.
- **반쪽 성공:** `PUBLISHED_LINK_PENDING`, `REVIEW_REQUIRED`, `INTEGRATION_BLOCKED` 등의 복구 상태를 분리해 기록하고 거짓 `COMPLETE` 금지.
- **Profile/Work category:** Kernel 기존 profile/Work purpose는 실행 정책. 제안 work_category를 새 Evidence kind/provider처럼 직접 사용하지 않음.

## 6. G0 읽기 전용 확인 사항 — K5.8/K6 원문을 최우선 확보

1. 실제 Updater 설치 위치/버전과 스킬 지침에서 **`K5.8` 전체 원문, tier 명칭·의미·우선순위·예외 및 tier→storage routing**을 확인한다.
2. **`K6` 전체 원문과 AS-IS/TO-BE MSC 생성·검증·저장·갱신·승격 조건**, participant/branch scope를 확인한다.
3. Updater의 자연어 entrypoint가 Workflow/Kernel Work ID 및 code-analyzer를 **현재 호출하는지**, 어느 시스템이 Work와 Evidence를 소유하는지 추적한다.
4. 그룹 Dev Knowledge의 현행 module/feature/scenario tree, HLD/detail design/issue history writer, owner 승인, revision conflict, readback 실제 경로·권한을 읽기 전용 확인한다.
5. Work Ledger Evidence registry의 기존 허용 slot(예: `code-analyzer / analyze / asis_msc`), `record.json`과 export 소유권, 설치본의 스키마 차이를 확인한다.
6. `l1-github` Git full SHA 및 `p4-code-owner` P4 file revision, code-analyzer CODE_FACTS/MSC 실제 output shape, 내부 정보 분류/반출 정책을 확인한다.
7. AS-IS K5.8/K6와 TO-BE를 **항목별 수용/수정/보류** 판정하고 `REUSE / CONNECT / EXTEND / DEFER` 및 예상 diff·역호환성·회귀시험 목록을 제시한다. 미실시 항목 `NOT_RUN`.

## 7. 필수 부정/회귀 시나리오

| ID | 시험 | PASS 기준 |
|---|---|---|
| T01 | 상세 HLD/MSC를 그룹 후보로 분류 | 상세도만으로 개인-only 강제 0; 유효성 검증/승인 기준 적용 |
| T02 | 미완료 이슈의 재사용 가능한 원인 분석 | `CAUSE_VERIFIED/FIX_PENDING`을 구분해 그룹 후보; 해결 완료로 위장 0 |
| T03 | 설계 승인되었으나 코드 미적용 | 그룹 design-change 이력은 별도 상태로 관리; AS-IS MSC 승격 0 |
| T04 | 현행 코드 AS-IS MSC (새 코드 변경 없음) | 고정 source/evidence/approval 후 그룹 후보 가능 |
| T05 | TO-BE 추정 MSC만 존재 | AS-IS 게시 0, 명시적 design-draft 판정 |
| T06 | Branch A MSC를 Branch B로 잘못 적용 | source pin/scope mismatch 탐지, VERIFIED 재사용 거부 |
| T07 | Updater·Workflow 각각에서 같은 요청 재시도 | Work ID 신규 중복 0, 후보/그룹 publication 중복 0 |
| T08 | 권한/승인 없음 또는 지식 revision CAS 변경 | 그룹 쓰기 0; 재승인 요구 |
| T09 | 그룹 게시 성공 후 Workspace 역링크 실패 | 영수증 유지, 중복 게시 0, `PUBLISHED_LINK_PENDING` |
| T10 | 기존 개인 Work/Kernel 구버전 데이터 | 원장·README/index/Evidence 무손실, `UNCLASSIFIED` fallback |
| T11 | 등록되지 않은 Evidence provider/kind | Kernel registry mismatch 차단, provider 위장 0 |
| T12 | 최신 지식 검색은 성공, 모델 본문 소비 미확인 | RAG 검색과 M1 분리, `M1=BLOCKED` |
| T13 | 동일 기술 지식이 두 Work/두 source branch에서 갱신 | N:M provenance, scope/version 구분, 최신본 무단 덮어쓰기 0 |
| T14 | 원본 code anchor 누락/유실, 변경된 dirty tree | `STALE/PREVIEW_ONLY` 처리; VERIFIED 게시 0 |

시험 구분: (a) 논리 표/정적 점검, (b) 합성 schema/상태 전이 테스트, (c) 승인된 격리복사본 I/O 통합시험, (d) 사내 운영 호스트 실측. 수행하지 않은 시험을 PASS로 작성 금지.

## 8. 사내 GPT·OpenCode 원샷 실행 인계

> 이 설계 r0003을 기준으로 현재 설치된 `l1-knowledge-updater`의 **K5.8 tier 분류 전체 원문**과 **K6 MSC 정책 전체 원문**을 먼저 찾아 정적 분석해 줘. 기존 tier 값과 사용자 지식 경로를 훼손하지 말고 **AS-IS→TO-BE 항목별 매핑**을 작성해 줘. 그룹 `l1sw-dev-knowledge`는 현행 코드 기반 HLD/상세 설계/AS-IS MSC/승인된 설계 변경 상태/기술적 이슈 히스토리까지 관리하고, 개인 `l1-workspace`는 Work·진행 상태·수정·시험·리뷰/Evidence 이력의 정본이 되도록 재분류해 줘. Workflow는 요청 분류·Work ID/Kernel lifecycle 및 분석 호출, Updater는 기술 지식 후보 분류·K6 MSC 검증·그룹 게시 Preview·승인 조정의 역할을 제안하되, 실제 스킬 I/O가 다르면 확인된 구현에 맞춰 최소 연결안으로 조정해 줘. G0 READ_ONLY 범위에서 설치본 entrypoint/field/registry/승인 경로를 실측하고 REUSE/CONNECT/EXTEND/DEFER, 변경 파일 및 T01~T14 회귀시험 계획을 작성해 줘. 그룹 정본/운영 스킬/Work/DB/예약작업을 변경하거나 회사 자료를 사외로 전송하지 마. 미확인은 NOT_VERIFIED, 미실행은 NOT_RUN으로 기록해.

### 결과 문서 (사내 보관)

`L1_KNOWLEDGE_UPDATER_K58_K6_WORKFLOW_G0_INTERNAL_RESULT.md`:
- A. AS-IS K5.8 tier 실제 규칙(사내에서만 원문 관리), B. AS-IS K6 MSC 실제 규칙, C. 기능별 Reuse/Gap, D. Work ID/Evidence I/O 매핑, E. 그룹 게시 정책/승인 권한, F. 최소 수정안(diff 대상), G. T01~T14 상태와 시험 증거, H. 승인 필요와 차단, I. 다음 한 동작.
- 별도 승인된 비민감 추상 결과가 필요한 경우에도 사내 원문/코드/경로/로그/MSC 내용은 외부 반출하지 않는다.

## 9. 변경/실행/배포 상태

- `DESIGN_REVIEW=COMPLETE_WITH_ASIS_GAP`
- `K58_TIER_SOURCE=NOT_VERIFIED`, `K6_MSC_SOURCE=NOT_VERIFIED`
- `WORKFLOW_INTEGRATION_IMPLEMENTED=NOT_VERIFIED`, `GROUP_PUBLICATION=NOT_RUN`
- `G0_INHOUSE=NOT_RUN`, `TEST_T01_T14=NOT_RUN`, `RAG_M1=BLOCKED`
- `CLAUDE_INDEPENDENT_REVIEW=NOT_RUN`, `SOURCE_PATCH=NOT_RUN`, `PUBLIC_RELEASE=NOT_RUN`, `LIVE_CUTOVER=NOT_RUN`.
- 게시 문서가 승인/운영 전환/자동 리뷰 실행을 의미하지 않으며, 그룹의 상세 자료 등록 허용과 자동 게시 권한은 다르다.
