# GPT_SELF_REVIEW — L1 Workspace RAG r0002 구조적 심층 리뷰 (r0001)

- 작성일: 2026-11-11 KST
- Workstream: L1-WORKSPACE-RAG-20261111-001
- **REVIEW_KIND: GPT_SELF_REVIEW** (GPT의 설계·코드 자체 리뷰; Claude Code 독립 리뷰 아님)
- **REVIEW_STATUS: COMPLETED_WITH_GAPS** (접근 가능한 설계/Kernel E2 기반 구조 검토 완료, 사내 설치·실환경 검증 미수행)
- **DISPOSITION: DESIGN_ACCEPT_WITH_REQUIRED_CHANGES / IMPLEMENTATION_BLOCKED_AT_G0_M1**
- **INDEPENDENT_CLAUDE_REVIEW: NOT_RUN**, signed REQUEST/READY/reviewer receipt: NOT_RUN
- 기존 운영: `MIGRATION_NOT_CUTOVER / DROPBOX_LIVE` 변동 없음
- 작업 제한: 신규 코드 수정·ZIP·사내 Git 쓰기·MCP/Provider 실행·운영 watcher/DB/Job/Telegram/READY/PUBLIC 배포/LIVE 전환 **0**

## A. 입력·근거 및 실제 실행 범위

| 근거 | 식별·검증 | E수준 및 한계 |
|---|---|---|
| PRIVATE `main`의 `CURRENT.md` | 2026-11-11 r0002 최신 섹션 확인, 기존 Claude REVIEW `NOT_RUN` | E1 원격 문서 |
| `L1_WORKSPACE_RAG_DESIGN_r0002_20261111.md` | Git blob `44d7bc056f203b1c7d82b44532ef7be410e82d33`, 문서 원문 열람 | E1 |
| `CLAUDE_DESIGN_REVIEW_HANDOFF_r0002_20261111.md` | Git blob `c4e44280875dbce5a01d6fc465f0cc5299e8332c`, r0002 R1~R10 검토 범위 | E1 |
| `GPT_ASSESSMENT_AND_DELTA_r0001_20261111.md` 및 r0001 baseline | 판단·미검증 항목 대조 | E1 |
| 사용자 첨부 `work-ledger-kernel_v0_7_37_1103.zip` | **318845 byte**, SHA-256 `8cf53c9ba14aed97b9be7b00db39ca5458ba0127ba00b9a1eef3533aba3a06a5`. ZIP 실제 파일 추출, Python 소스와 테스트 확인 | **E2 실제 배포 ZIP 코드**; 설치본 아님 |
| PUBLIC `L1Work` ZIP 인벤토리 | Workflow `v1.6.67`, l1-github `v0.3.56`, code-analyzer `v0.15.2`, doc-converter `v0.2.21`, hld-composer `v0.4.32`, job-list `v0.4.34`의 파일/구성 명칭 확인 | E1 package manifest/ZIP entry 수준; 사내 설치·실 API 미확인. Workflow/Analyzer 전체 코드를 실행해 검증한 것으로 주장 금지 |
| PUBLIC `L1_MCP_Wrapper_RAG_U01_U15_Verification_OneShot_v1_2_1107.md`, `L1_KNOWLEDGE_ROADMAP_INHOUSE_GPT_HANDOFF_20261109.md` | RAG 본문 소비, owner/root/Job 7개 Gate 원문 확인 | E1 |
| 사내 `l1-workspace`·source checkout·MCP·Job | **NOT_VERIFIED**: 외부 GitHub.com은 사내 Git 서버가 아님 | E0, E3 실호스트 증거 0 |

**격리 코드/합성 시험(이 회차 직접 실행):**

- Kernel v0.7.37 추출본의 5개 관련 테스트 모듈 `tests/test_code_rev.py`, `test_github_docs_layout_v077.py`, `test_work_docs_navigation_v0724.py`, `test_cross_host_context_v076.py`, `test_feature_stage4_export.py`: **11 PASS / 1 FAIL** (`pytest`, 이 환경 Python 3.13). 실패 항목은 `test_v2_layout_is_immutable_work_id_and_human_first`로, 테스트가 README의 `**지금 상태:**`·`**다음 할 일:**`을 요구하는 반면 현재 exporter는 `**결론:**`·`**상태:**`·`**다음:**`을 렌더함. **기존 패키지의 기대문구 불일치이며 r0002 코드 회귀로 단정 금지**.
- 별도 임시 Work 생성/Export 합성: `profile=MAINT`, `work_purpose=ENGINEERING`, `work_category` 스냅샷 필드 **MISSING**; Feature 기록이 없는 Work에서 `CODE_FACTS.md`/`MSC_VIEW.md` 생성되지 않음. 추출본 수정·사내 Work 변경 없음.
- `worktree_digest` 경로 합성: 허용 glob `src/*.cpp` 아래 심볼릭 링크가 코드 root **밖의 파일**을 참조할 때 바깥 파일 변경에 digest가 바뀌는 현상 재현. 빈 결과 집합과 빈 glob의 digest 같음. `validate_code_rev`은 `wrong:<64hex>` 모양도 통과함. 이는 **형식 체크가 source authority 검증이 아님**을 보여줌. 모두 임시 경로/합성 데이터.
- 위는 Kernel 일부 동작의 코드·합성 결과일 뿐 사내 원본/현장 Provider/E2E, Workflow/Analyzer 통합 시험이 아님.

## B. 총평 및 핵심 설계 판단

**수용:** Work SSOT(`record.json` + Kernel Work), GitHub `works/<immutable-work-id>`·`index/` 기존 생성기 보존; 개인 `module-library`와 그룹 `l1sw-dev-knowledge` 분리; `work_category` / `artifact_kind` / knowledge tags / Kernel profile의 **4축 분리**; Git 전체 commit/P4 실제 haveRev 증거; `MSC_AS_IS`는 코드 사실의 파생 표현이고 `MSC_TO_BE`는 미구현 설계; CODE_ANALYSIS Work를 독립 생성하더라도 다른 ISSUE Work의 AS-IS MSC로 Work 유형을 바꾸지 않음.

**수정 수용:** CODE_ANALYSIS 사용자 시나리오를 실제 exporter/provider 연결로 구현할 방법, typed SourceSnapshot 불변성·dirty 범위·source authority, Evidence→MSC 출처 연쇄, source 검증 본문→pre-call payload 보증, 기존 코드/문서 생성기의 정합성 계약을 구체화해야 구현 가능.

**보류:** `module-library/index/by-type` 등 새 인덱스, 별도 RAG skill/vector DB, 자동 게시·자동 승격. 사내 현재 트리·기존 스캐너·원격 동기화의 중복 여부 미확인.

**전체 구현 판정:** G0 E3(실환경 설치·권한·root·tools) 없음, M1 provider body consume 게이트 실현 증거 없음. 이 문서가 정적 설계 ACCEPT를 넘어 구현 승인/운영 PASS를 의미하지 않음.

## C. 리뷰 지적 — 심각도별 구체 판정

### BLOCKING (5건; 해당 기능의 구현·PASS·사외 게시 게이트)

**B-01 — 실제 RAG 본문 공급/신뢰 드라이버가 검증되지 않음 [E1, 기존 G0/M1 gate; 설계 게이트]**

- **근거:** r0002 `5`는 검색→본문→scope/owner/root→Provider input→Receipt를 제시하지만, 실제 reader/tool ID/driver identity/typed payload의 집행 지점과 호출 경로가 구현·설치됐다는 E2/E3 근거 없음. 2026-11-09 로드맵의 `F-B1-01/02`, `F-N2-01/02`, `F-N1-01`, `F-N3-01`, `F-VERS-01`는 해제되지 않음.
- **영향:** 제목/링크 검색만 수행하거나 Provider 자체 보고 digest를 신뢰하면 다른 revision의 지식을 근거로 잘못된 CODE_ANALYSIS 답변을 '검증됨'으로 표시.
- **권고:** 사내 기존 MCP/Workflow/Job/Provider 호출 드라이버에서 **최종 전달 직전** trusted reader의 `file_sha256`, canonical `body_sha256`, `D_retrieve`, `D_call`, `D_payload`, `canon_spec_id`, source/owner/root authority, 실제 input assembly reference를 한 묶음으로 기록. 승인된 Job-list pre-enqueue 및 direct pre-call 가드를 구분하고 검증 불가 경로는 fail-closed. 기존 검증기를 재사용하고 새로운 독립 엔진 도입 금지.
- **부정시험:** 검색 성공·원문 소비 누락, 다른 body/CRLF/BOM, Provider 자기보고 hash 위조, 만료 owner, 미등록 source root, sentinel job_id 우회, 미승인 DIRECT; 모두 `M1 PASS` 거부, 호출/Queue 증가 0.

**B-02 — Branch/P4 SourceSnapshot 계약과 코드 분석 실제 입력의 원자적 바인딩 미완성 [E1+Kernel E2]**

- **근거:** r0002 `3`의 `requested_ref` / `pinned_source_revision` / `tree_state`는 논리 필드. Kernel `kernel.py`의 `_git_workspace_identity`와 `code_rev.py::make_code_rev`은 Git branch/HEAD 및 파일 범위 digest 메커니즘을 일부 보유하지만, CODE_ANALYSIS→MSC→문서 검색까지 같은 고정 source snapshot을 전달하는 구현 증거 없음.
- **영향:** 브랜치 이동/force-push/다중 worktree/P4 mixed haveRev, CODE_FACTS 생성 후 HEAD 변경으로 AS-IS MSC가 다른 기준의 '현재' 코드로 오표시.
- **권고:** `SourceSnapshot` typed contract(`product_id, VCS, repo/depot authority ID, root_id, requested_ref, pinned full Git SHA 또는 P4 file#haveRev set, tree/root status + scoped files digest, capture time, analysis tool/version, evidence IDs`) 도입; **source read → pin → analyze → write candidate → retrieval→ pre-call**의 단계에서 동일 snapshot 재검증. Git의 같은 commit을 공유하는 서로 다른 branch는 **코드 내용 동등**으로 처리 가능하나 branch 표시/요청 범위와 변경 여부는 별도 확인. P4 CL 하나를 모든 파일 revision으로 가정 금지.
- **부정시험:** Branch A/B 서로 다른 SHA, 같은 브랜치 HEAD drift, dirty/untracked, 다른 worktree/제품/RAT, P4 mixed haveRev, checkout 바뀐 뒤 재사용 시 verified→STALE/PREVIEW_ONLY. 의도된 동일 SHA 재사용은 scope/권한 조건에서 허용.

**B-03 — Kernel의 source scope digest가 symlink 경계를 넘을 수 있음 [E2 + 격리 재현]**

- **근거:** 첨부 Kernel `work_ledger_kernel/code_rev.py::worktree_digest`는 `workspace.rglob("*")` + `x.is_file()` + `sha256_file(x)`를 사용하여 source root 밖을 가리키는 파일 symlink를 필터하지 않음. 합성 `src/link.cpp`가 root 밖 파일을 가리키는 경우 밖 파일의 변경에 digest 변화 **재현**. `validate_code_rev`은 trailing 64-hex+prefix 형식 검증에 국한.
- **영향:** 사용자/등록된 scope 외 파일 바이트를 의도치 않게 읽거나, 권한·반출 경계를 넘은 digest가 RAG 검증 근거로 오인될 위험. 대규모 checkout의 지연·TOCTOU도 남음.
- **권고:** 기존 `code_rev`를 무조건 버리지 말고 **root resolve/identity**, 개별 경로의 non-symlink·root 내 containment, 허용된 file manifest, 빈 매칭 거부, metadata + content hash를 안전하게 고정. Git tree object hash 및 scoped Worktree snapshot의 역할을 구분. 외부 링크 발견 시 `OUT_OF_SCOPE_PATH` 실패. 이 수정은 이번 리뷰에서 실행하지 않음.
- **부정시험:** symlink로 root 이탈, 부모 디렉터리 symlink, 빈 glob, 삭제/추가 untracked, 작업 중 파일 변경, 동일 내용 다른 repo/root. 바깥 경로 접근 0, VERIFIED 금지.

**B-04 — 기술 지식의 사외 반출 경계가 자동 파생 문서에 의해 우회될 수 있음 [E2 코드 + 위험 조건부]**

- **근거:** Kernel `work_ux.py::export_docs`는 Ledger Evidence 중 정합성·확장자·크기 가드를 만족하면 `artifacts/{analysis,design,verification}` 등으로 텍스트/HTML/JSON을 복제함. 기존 preflight·symlink/해시/TL_REVIEW 차단은 있지만, **개별 RAG 본문/MSC의 사외 반출 승인**이 자동으로 이뤄진다는 증거는 없음. 이는 사내 `l1-workspace`로의 승인된 이동과 사외 PRIVATE 문서 게시를 구분해야 하는 이유.
- **영향:** 회사 코드/고객/상세 제품 흐름 또는 민감 MSC를 외부 협업 repo로 잘못 동기화할 경우 보안 위반. PRIVATE는 반출 허가 근거가 아님.
- **권고:** `destination trust boundary`를 typed classification으로 정의: 사내 work_docs/인가된 지식 검색과 사외 협업 결과 MD를 분리, 외부 이동에는 명시된 export-authority + allowlist + redaction review가 선행되어야 함. 사외에는 `issue ID / severity / abstract evidence / hashes of non-sensitive docs`만 게재. 공유 경로를 도구명에 암묵 연동하지 말 것.
- **부정시험:** source snippet, 제품 log, 상세 MSC, 토큰/내부 경로, HTML embedded sensitive payload 포함 시 사외 게시 거부. 격리된 사내 source read는 외부 원격 업로드 0. 현재 이 보고서에는 사내 제품 원문 없음.

**B-05 — 사내 설치본/Job-list 우회 가드·권한 정본 미검증 [E0/E1, 배포 차단]**

- **근거:** PUBLIC zip 존재는 내부 설치 승인/실행 증거가 아니며 현재 `CURRENT.md`도 E3 부재. 설치 Worker/Job Profile/RAG MCP tool ID·provider invocation, owner authority, code-root registry의 적용이 확인되지 않음.
- **영향:** 개발 후보를 운영 호환 버전으로 오인하거나, 실패한 호출을 새 Job ID로 반복하고, 비담당 모듈을 개인 지식 정본에 확정할 수 있음.
- **권고:** G0 격리 read-only inventory: installed path/hash/release status, 실제 role/mapping, 모든 MCP tool ID/host, job-list pre-enqueue guard, owner/root 신뢰원천 신선도 확인. 실검증 실패면 `BLOCKED`, 운영 변경 금지.
- **부정시험:** 설치 0.4.32 vs 후보 0.4.34, 다른 Job ID로 sentinel 우회, expired owner, null tool mapping, wrong product root, review-candidate 릴리스. 어떤 경우도 운영 M1 또는 배포 PASS 아님.

### MAJOR (8건; M0/기능별 구현 전 반드시 보완)

**M-01 — CODE_ANALYSIS-only Work의 CODE_FACTS 문서 경로가 기존 Kernel과 불일치 [E2+합성 재현]**

- **근거:** `work_ux.py::export_docs`에서 `CODE_FACTS.md` 생성은 `has_feature = bool(feature['items'] or feature['legacy_unnumbered'])` 하위에 있고, `HUMAN_CONFIRMED` + `provider=code-analyzer` evidence만 summary로 표시. Feature 이벤트 없는 새 MAINT 기반 분석 Work 생성 후 Export 시 `CODE_FACTS.md`와 `MSC_VIEW.md` 둘 다 없음 확인.
- **영향:** 사용자가 요구한 독립 `CODE_ANALYSIS` Work는 분석 Evidence가 있어도 기존 exporter 규칙만으로 별도 CODE_FACTS 요약/링크를 얻는다고 보장할 수 없음.
- **권고:** 기존 Feature 조건을 깨지 않는 **정본 Evidence 기반 보조 summary projector**를 별도 경량 분기로 추가하는 설계안 작성; 원본 Evidence 없으면 '검증된 코드 사실 없음'으로 표시, 전체 code-analyzer 결과를 무검증 사실로 승격 금지. 기존 Work 문서 및 수동 문서 충돌 규칙 유지.
- **시험:** Feature 없음+confirmed analyzer evidence, feature 있음 기존 문서 결과, rejected/unconfirmed evidence, 다른 branch evidence 혼재, 수동 `CODE_FACTS.md` collision.

**M-02 — MSC_AS_IS/TO_BE 산출물 명명·탐색 호환이 미정 [E2]**

- **근거:** `work_ux.py`에서 `msc_artifacts`는 `'MSC_VIEW' in src.stem.upper()`일 때만 수집, 기본 `MSC_VIEW.md` 안내문은 '변경 전후 MSC' 표현. `artifact_publish_map.json`은 `evidence_id / published_path / sha256`만 관리. r0002 `MSC_AS_IS`와 `MSC_TO_BE`는 아직 메타데이터 제안.
- **영향:** `MSC_AS_IS.md`로만 저장한 새 분석 MSC가 기존 `MSC_VIEW.md` 및 문서탐색에 나타나지 않거나, TO-BE와 혼합되면서 사용자가 설계안을 현재 코드로 오인할 위험.
- **권고:** 기존 안정 artifact map과 Evidence ID는 유지, `artifact_kind`를 **정본 Evidence 메타데이터/manifest**에서 판별하여 기존 문서 안내/MSC renderer에 파생 연결. 파일명 substring 감지는 호환용 fallback만. AS-IS/TO-BE 상태·source revision/approval·CODE_FACTS anchor를 사용자 화면에 표시.
- **시험:** MSC_AS_IS-only, TO_BE-only, BOTH, 구형 MSC_VIEW, 동일 이름 다른 Evidence ID, map mismatch/rename/dirty/legacy; 파일 복제와 링크·render 성공 별개.

**M-03 — 새 work_category의 권위/이력/타 호스트 병합 계약 불명 [E2+E1]**

- **근거:** `work_ux.py::create`는 `profile=MAINT`와 `work_purpose=TRACKING_ONLY/ENGINEERING`, `context_meta.json` 및 Kernel `record.json schema_version=1.0.1`에만 현행 상태를 저장. `work_docs_export`의 snapshot에는 `work_category` 없음(합성 확인), `index/latest.json`/`active.json`은 layout v2·schema 1.
- **영향:** 분류 필드를 README/새 인덱스에만 추가하면 다음 Export 시 유실. 다른 PC의 구버전 exporter가 새 분류를 지우거나 두 호스트가 서로 다른 category를 제공할 수 있음.
- **권고:** category의 trusted owner, 명시적 update event/actor/old/new/revision/충돌 정책을 결정. Kernel SSOT와 분리된 표시용 metadata는 **동기화·권한 규약**을 통해 보존. 이전 snapshot에서 `UNCLASSIFIED` fallback; 원본 schema 변경 없이 additive + old/new reader contract를 시험한 뒤 승인. 같은 Work에서 ISSUE/FEATURE 변경은 사용자 확인 필요.
- **시험:** legacy snapshot, old/new exporter roundtrip, cross-host A/B category conflict, 재생성, rollback, unknown fields 보존, 기존 last-work index byte-compat.

**M-04 — MSC source/evidence 식별자 및 provenance 체인 부족 [E1+E2]**

- **근거:** r0002의 source metadata는 제안이며, Kernel 공개 artifact map은 `evidence_id/path/sha256` 중심. `MSC_AS_IS`는 source file/line/condition/commit의 verified chain을 자동 보장하지 않음.
- **영향:** branch A/B 같은 시나리오의 파생 MSC가 코드/증거 앵커 없이 '검증됨'으로 중복 축적됨.
- **권고:** `artifact_id, work_id, evidence_id, analysis_revision, artifact_kind, source_snapshot_id, source_anchor_ids, claim_state`를 별도 구조화 contract로 정의. 동일한 content hash라도 서로 다른 적용 scope는 별개 적용 판정. `MSC_TO_BE`가 `MSC_AS_IS`로 자동 승격되는 경로 금지.
- **시험:** 동일 파일명 다른 Evidence, missing source anchor, source code change, unverified inference, AS_IS/TO_BE 혼합, backward reader 호환.

**M-05 — Git worktree/P4 고정·sync·dirty/diverged 경합 보호의 end-to-end 부재 [E1]**

- **근거:** Git branch name은 mutable. 이미 Kernel source write gate에는 branch/HEAD 검사가 있지만, **읽기 분석→module-library→RAG 검색/게시**는 해당 source-write lease와 다른 경로. l1-github `work_docs`는 사내 호스트에서 확인 필요.
- **영향:** 사용자가 두 고정 worktree를 전환하거나 upstream merge/force-push를 수행할 때 stale MSC가 의도치 않게 갱신/게시될 위험. 아울러 워크트리 수천 untracked 상황에서 무차별 재검색 부하.
- **권고:** source checkout과 docs repo의 branch/ref 분리; fast HEAD/status snapshot → approved scope map → staged manifest → 다시 HEAD/status 검증. 변경된 branch에 대한 지식은 기존 문서 덮어쓰기 대신 `STALE/RECHECK` 버전 연결. Git read-only 분석과 Push Guard는 별도.
- **시험:** 두 worktree 같은 repo 다른 HEAD, upstream merge 리베이스, dirty/diverged docs repo, force push, P4 haveRev 파일 혼합, git root 중첩, rollback.

**M-06 — Participant 표시명 = 폴더명 규칙만으로는 충돌·책임분리 불가 [E1]**

- **근거:** r0002의 `TxMngr/DRX/BCH/RF_BLOCK`은 가독용 participant 이름. doc-converter `v0.2.21`에 parent-directory participant 테스트 파일 존재; **정확한 실제 설치 매핑은 검증되지 않음**. 동일 폴더명이 제품/stack/owner마다 반복 가능.
- **영향:** 다른 제품의 같은 `DRX`가 한 MSC 노드로 병합되거나 조직 owner와 혼동될 수 있음.
- **권고:** `participant_id=(source_system, product/stack, module_id or source-path-id)`는 안정 식별자로 보관, 표시명만 마지막 의미 있는 폴더. 사용자 지정 alias map의 버전/우선순위, 모호성 거부, ownership=separate field. HTML/PlantUML render 전후 동일 ID 검증.
- **시험:** 동명 폴더 서로 다른 제품/모듈, parent-dir naming, Windows/Linux path separator, TxCfgMngr+TxCmdMngr 하나의 TxMngr, 내부 상세 code anchor와 viewer 역링크.

**M-07 — 대규모 코드 checkout에서 root 전체 rglob 해시·인덱싱 비용 계획 부족 [E2]**

- **근거:** `code_rev.py::worktree_digest`는 `workspace.rglob("*")`로 전체 subtree를 순회하고 glob 매칭 후 해시. 수정 전 원본에서 대상 scope에 맞는 allowlist·증분 캐시·timeout 정책이 이 루틴에 명시되어 있지 않음.
- **영향:** 수만 개 파일의 SMP1900 worktree, PC 전환·RAG 질의마다 재해시하면 지연·비용·사용성 악화. 해시 계산 중 파일 변경으로 TOCTOU 가능.
- **권고:** 최소 G0 read-only manifest 재사용 + whitelist scoped files, pinned Git tree object/SCM APIs 우선, 파일 범위 digest는 정확성 검사에 한정. 벤치마크 후 캐시/증분 기능 결정; stale cache는 신뢰 근거로 사용하지 않음.
- **시험:** 소규모/대규모 fixture, symlink/untracked, 파일이 검사 도중 변경되는 race, 동일 snapshot 반복, Windows/Linux 경로 case, timeout fail-closed.

**M-08 — Kernel 기존 패키지의 회귀시험 기대문구와 실제 렌더 불일치 [E2+격리 실행]**

- **근거:** 12 tests executed, 11 PASS / 1 FAIL. `tests/test_github_docs_layout_v077.py` 기대 `**지금 상태:**`/`**다음 할 일:**` vs 현재 exporter `**결론:**`/`**상태:**`/`**다음:**`. 기존 첨부 ZIP에 이미 포함된 불일치이며 이번 r0002의 신규 코드 변화가 아님.
- **영향:** UI/exporter 변화 검출 신뢰도 저하; CI에서 baseline red를 새 CODE_ANALYSIS 회귀와 혼동.
- **권고:** 기존 요구 UI 문구의 실제 기준을 확정한 뒤 **test expectation 또는 renderer 중 한쪽을 최소 수정**하고 원본 v0.7.37은 보존. 이 회차 어떤 파일도 수정하지 않음.
- **시험:** 최초 baseline 전체, 생성 root+Work README golden snapshot, human navigability, old format compatibility, 신규 category 표시 on/off.

### MINOR (3건; 후속 개선)

**m-01 — Work와 기술지식 검색 화면의 통합 UX가 아직 구체적이지 않음 [E1].** Work 대시보드와 개인 module-library 탐색을 별도 SSOT로 두면서 양방향 breadcrumb/근거/branch badge를 같은 탐색 표면에 표시하는 최소 가이드 필요. 지식 인덱스를 두 개 생성하지 않음.

**m-02 — `UNCLASSIFIED`·`UNKNOWN`·`STALE`·`PREVIEW_ONLY` 용어의 축이 다름 [E1].** `UNCLASSIFIED=Work intent 모름`, `UNKNOWN=증거/적용상태 불명`, `STALE=기준 이탈`, `PREVIEW_ONLY=사용/게시 제한`으로 스키마·UI·로그의 의미를 고정.

**m-03 — Branch 동일 SHA/멀티 scope 중복 비용 [E1].** 동일 immutable Git commit+검증된 scope는 분석 결과를 공유해도 되지만 branch label은 provenance로 기록. P4는 product/client/file haveRev가 다르면 단일 CL 같아도 재사용 금지.

## D. 컴포넌트별 중복 방지 / 실제 구현 분담

| 컴포넌트 | 판정 | 최소 실제 변경 위치 후보/금지 |
|---|---|---|
| `work-ledger-kernel v0.7.37` | **REUSE + bounded EXTEND** | 기존 record SSOT/`work_ux.py`/`work_docs_navigation.py`/`code_rev.py` 유지. category optional provenance, CODE_ANALYSIS evidence projection, source path guard·regression. 새 Work 엔진 구현 금지 |
| `l1-fix-workflow v1.6.67` | **REUSE + CONNECT** | 기존 `module_library.py`/`knowledge_input.py`/`github_docs.py`/code analysis orchestration 사용 가능성 조사. 입력 contract 구현 확인 전 기능 PASS 금지 |
| `code-analyzer v0.15.2 후보` | **REUSE + CONNECT** | 기존 `code_analyzer_msc_contract`/`knowledge_link` 참조 기능 inventory, source snapshot pin 및 CODE_FACTS/Evidence artifact_kind 연결; 분석 알고리즘 신규 중복 구현 금지 |
| `doc-converter v0.2.21 후보` | **REUSE** | 기존 `msc_tool.py`·`test_msc_participant_parent_dir_v0221.py` contract와 participant alias mapping 대조; MSC 렌더러 재구현 금지 |
| `hld-composer v0.4.32 후보` | **REUSE** | 설계 `MSC_TO_BE`/HLD만 기존 계약 내에서 재사용. AS-IS source fact로 자동 승격 금지 |
| `l1-github v0.3.56 후보` | **REUSE** | 실제 사내 `work_docs` 역할, Checkout/branch/status/readback, Push Guard 실측. GitHub.com PUBLIC 저장소를 사내 `l1-workspace`로 대체 금지 |
| `job-list v0.4.34 후보` | **CONNECT / BLOCKED** | 실제 설치 version/hash/profile/queue preflight 검증 전 Job/Provider 실행 금지 |
| 사내 MCP/RAG reader/driver | **CONNECT; G0 확인 필요** | 기존 tool ID/입력 조립 경계 확인 후 `D_call/D_payload` 최소 연결. 새 벡터 DB/별도 agent daemon 개발 보류 |
| `module-library` | **REUSE if exists; G0** | 실제 스캐너와 schema 확인 전 `index/by-type` 등 새 경로 생성 보류 |

**실현 가능성 판정:** 기존 구성 요소를 **연결하는 설계는 실행 가능성이 높음**(공용 계약·Kernel 기능 일부 존재). 하지만 `CODE_ANALYSIS-only Work의 문서 생성, MSC kind/provenance bridge, 실제 provider payload capture, owner/root/Job gate`에는 확인 또는 최소 개발이 필요. Windows/Linux 혼합 호스트 설치/성능·동시작업 실험은 별도 실행 게이트.

## E. 요구 회귀 시험 매트릭스 (착수 승인 전 설계)

| ID | 시나리오 | 실패 시 거부 / 성공 증거 |
|---|---|---|
| T01 | Legacy Work snapshot/index/resume v1/v2 읽기 | 과거 Work 원문/ID/수동문서/`index/latest.json` 유지 |
| T02 | CODE_ANALYSIS-only Work 생성, 한 개 AS-IS Evidence/MSC 생성 | category 분리, CODE_FACTS/MSC 안내/근거 링크 실제 노출 |
| T03 | ISSUE Work 안 AS-IS MSC | Work ISSUE 유지, artifact `MSC_AS_IS` |
| T04 | FEATURE Work의 미구현 MSC | `MSC_TO_BE`/Preview 표시, 현재 코드 사실 미승격 |
| T05 | Branch A vs B 상이한 HEAD SHA | A Evidence로 B 답변 거부 |
| T06 | Branch A/B 동일 SHA + scope 유효 | 안전한 재사용 허용, 두 requested_ref provenance 보존 |
| T07 | force-push/rebase/HEAD drift | `STALE` 또는 재확인, 기존 MSC 무단 덮어쓰기 0 |
| T08 | Dirty/untracked·symlink outside root·empty glob | VERIFIED 0, root 외 읽기/부적합 digest 거부 |
| T09 | P4 haveRev 다중 파일/다른 client | 파일별 revision 검증, 단일 CL로 동일성 오판 금지 |
| T10 | CODE_FACTS confirmation/rejected/inference 분리 | unconfirmed→fact 승격 0, 내부 anchor 추적 |
| T11 | MSC participant alias · 동명 경계 | TxMngr/DRX/BCH/RF_BLOCK 보기; ID와 owner 별도 |
| T12 | module-library 스캐너/중복 인덱스 | 기존 reader만 사용, 파생 view 재생성/충돌 탐지 |
| T13 | RAG 제목만 제공·body 미공급 | `M1 FAIL/PARTIAL`, PASS 금지 |
| T14 | canonicalization CRLF/BOM/Unicode/frontmatter·payload drift | D_retrieve/D_call/D_payload 검증 실패 시 사전 차단 |
| T15 | 다른 제품/RAT/owner/root or 만료 권한 | Provider 입력 및 지식 게시 거부 |
| T16 | direct 호출/Job ID 변경으로 정책 우회 | pre-enqueue/pre-call both fail-closed, Queue 소비 0 |
| T17 | 구버전 exporter / 동시 PC 수정 / manual doc | 충돌·dirty 보존, 의도치 않은 삭제·overwrite 0 |
| T18 | 생성 결과 Git readback/rollback | 원격 blob/bytes/commit 확인 전 완료 금지 |
| T19 | PUBLIC candidate vs actual installed release | installed version/hash/release status 미확인=BLOCKED |
| T20 | 대형 checkout performance/cancellation | 승인된 scope만 read, 중단 안전성·time budget 충족 |
| T21 | 사외 업로드 보안 경계 | 반출금지 원문 0; 비민감 status만 허용 |
| T22 | 기존 12개 Kernel 테스트 전체 rebaseline | 기존 FAIL 1건 원인·해소/승인 표시, regression green |
| T23 | 실 Agent→MCP→Provider E2E | input assembly evidence+source/owner scope+terminal Receipt(별도 승인 후) |
| T24 | 다른 Work에서 재사용/반례 거부 | 동일 scope 1건 PASS + 불일치 scope 1건 거부 |

**이 문서의 T01~T24는 대부분 계획된 시험이며 이 회차 실행 PASS를 뜻하지 않음.** 직접 실행된 테스트는 `A`의 12건+별도 합성 관찰뿐. 운영 real-host 실행 테스트는 모두 `NOT_RUN`.

## F. 우선순위·승인 게이트·완료 정의

1. **P0/G0 read-only:** 사내 root/role, `module-library` tree, 실제 installed Work/Workflow/Kernel/Analyzer/GitHub/Job versions/approval, MCP tool mapping/owner registry, 기존 Work fields/샘플 artifact map 확인. 반출 가능한 적합성 요약만 공유.
2. **P0/M0 contract:** typed SourceSnapshot, new `work_category` authority, `artifact_kind`/Evidence bridge, AS-IS/TO-BE 전시, read-only security/path guard·legacy cross-host compatibility. 최소 patch 범위와 backward reader 시험 명세만 먼저 확정.
3. **P0/M1 integration:** 실제 승인된 도구·call path로 문서 body/anchor + scope/owner/root + trusted digest ↔ provider payload ↔ Receipt를 입증하고, 다른 branch/stale/dirty 차단 시험을 통과한 후에만 `RAG_PROVIDER_INPUT=PASS`.
4. **P1/M2~M3:** 개인 지식 Preview→owner 승인→사내 Git commit/readback→다른 Work 재사용+거부 1건. 그룹 지식 자동 승격·사외 게시 금지.
5. **P2/M4:** 검색 품질 평가셋으로 필요 입증 전 새 DB/embedding/deep indexing 보류.

- **이 보고서가 허용하는 변경:** GitHub PRIVATE에서 이 리뷰 MD 작성 및 해당 프로젝트 `CURRENT.md`에 결과 링크·상태 기록만.
- **DEVELOPMENT:** DESIGN_ONLY / SOURCE_PATCH=NOT_RUN / PACKAGE_BUILD=NOT_RUN
- **SELF_TEST:** `Kernel isolated 11 PASS / 1 FAIL` + separate synthetic probes; Workflow/CodeAnalyzer integration `NOT_RUN`
- **GPT_SELF_REVIEW:** COMPLETED_WITH_GAPS; **CLAUDE_INDEPENDENT_REVIEW:** NOT_RUN
- **INHOUSE_HOST:** NOT_VERIFIED; **RAG_M1:** BLOCKED; **EXTERNAL_PUBLISH_CONTENT:** non-sensitive abstract only; **LIVE:** unchanged.

**GPT 다음 판정:** `DESIGN_ACCEPT_WITH_REQUIRED_CHANGES`. G0 read-only inventory와 최소 connector/schema patch 설계가 다음 동작; 사용자 별도 승인 없는 기존 스킬·운영·Git 변경 및 reviewer 호출 금지.
