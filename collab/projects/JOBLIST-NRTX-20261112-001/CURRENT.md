# JOBLIST-NRTX-20261112-001 — CURRENT

- Date: 2026-11-12 KST
- Goal: new Linux `job-list` One-shot for NR L1 Tx Init RACH and UL SCell configuration/activation/deactivation investigation; `l1-knowledge-updater` orchestrates `code-analyzer` and `doc-converter`; stage candidate AS-IS MSC & reusable NR Tx group-knowledge updates.
- Current release: **`development_not_for_deployment`**; PUBLIC ZIP `NOT_POSTED`, `ACTIVE_JOBS=0`; existing PUBLIC `job-list_v0_4_34_1109.zip` intact; in-house source `NOT_ACCESSED`; no host install/Job execution/group knowledge write.
- CoWork baseline: `MIGRATION_NOT_CUTOVER / DROPBOX_LIVE`. Independent review has not run. This is unrelated to Dropbox reviewer REQUEST/READY.

## Implemented candidate

- Base: `wonhwipark/L1Work` `main` `job-list_v0_4_34_1109.zip`, 1,551,031 bytes, Git blob `13353c5db1d09752507b865fe3d4e5fc456f495c` pinned and verified.
- New package: **`job-list_v0_4_35_1112.zip`**, 1,562,969 bytes; SHA-256 **`3061be176932ed145554b583624a96f0c2bbb22533c5fed8635c1acc2101779c`**, created in isolated GitHub Actions; ZIP CRC, all-file manifest, package identity and static profile pass.
- PRIVATE review artifact: [GitHub Actions run 43058706135 artifact 13872392048](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/43058706135/artifacts/13872392048) (14-day artifact retention; artifact zip wrapper SHA-256 `343f4e8d5a0c1c508f6eda90b531a112b767a0299affabc26729b92ea06039ba` is distinct from the inner package ZIP SHA above).
- Builder and source (PRIVATE `main`): `collab/tools/joblist_nrtx/build_candidate.py`, `nr_tx_knowledge_linux_job.py`, `NR_TX_KNOWLEDGE_RESEARCH_ORCHESTRATION_v0435.md`, `test_v0435_nrtx_candidate.py`.
- Host source root: resolved inside approved Linux environment from `$HOME/Project/smp1900`; no exact employee-specific absolute path, source code, corporate logs or credentials are embedded in the publicly deployable package.
- Candidate new Profile: `nr-l1tx-knowledge-research-linux` with `scripts/nr_tx_knowledge_linux_job.py`; staged request `requests/staged/one-shot-v0.4.35-nr-l1tx-knowledge-research.json`; **`requests/one-shot-jobs.json` remains `{"schema_version": 1, "jobs": []}`**. Baseline requests, runtime data, queues, receipts and old revisions remain unchanged.
- Runtime default: needs host-local owner-approved `data/config/nr_tx_knowledge_research.json`, pinned clean Git HEAD, valid existing Work ID and approved local OpenCode provider; confirms installed `l1-knowledge-updater`/`code-analyzer`/`doc-converter` SKILL contracts; no arbitrary external parameters, source patches or shared knowledge publication. If any gate is missing, emits a locally recorded BLOCKED semantic result and does not invoke a model. Actual in-house G0 not performed.
- Tasks: (1) `L2_L1_TX_REQ` → PHY IPC Init RACH; (2) `PHY_CONFIG_REQ` → UL SCell config; (3) `SCELL_STATUS_IND` → Activation; (4) same indication → Deactivation. Code Fact evidence and source-pinned AS-IS only; Doc Converter `SOURCE_PARENT_DIR_V1`, BCH/DRX/TxMngr participant remapping; four separate MSC, generated artifacts and group update candidates. Existing group knowledge write requires separate owner approval.

## Actual tests and independent review

- GitHub Actions final run: [43058706135](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/43058706135), **SUCCESS**.
- ZIP CRC = **PASS**; all package file SHA manifest = **PASS**; byte-for-byte original baseline Git blob verification = **PASS**; source/secret/path policy static scan = **PASS**; static skill/Job profile validation = **PASS**.
- Targeted pytest regression: **33 PASS / 0 FAIL**, including old staged Knowledge bridge and new v0.4.35 fail-closed tests; new Worker Python compile PASS. Whole-suite = NOT_RUN; actual Linux Provider/Updater/Code Analyzer/Doc Converter/MSC rendering = NOT_RUN.
- **`INDEPENDENT_REVIEW=NOT_RUN`**: developer self tests are not independent review. `HOST_G0=NOT_RUN`; `GROUP_WRITE=NOT_RUN`; `RAG_M1=BLOCKED`; `PUBLIC_RELEASE=NOT_POSTED`; `SKILL_UPDATER_INSTALL=NOT_RUN`; `JOB_EXECUTION=NOT_RUN`.
- Existing baseline v0.4.34 itself is STAGED/zero-active and has unresolved Run Catalog, provider entrypoint and host compatibility gates. Do not treat updating metadata as release approval.

## Blocking items before PUBLIC automatic delivery

1. **Installed Updater contract unknown**: user reports existing in-house `l1-knowledge-updater`, but no independently measured CLI/tool invocation, exact installed version or owner-approved group publication contract. Candidate uses native OpenCode integration and must be site-validated.
2. **Host G0 not proven**: owner-approved config, current immutable source SHA, existing Work/Evidence, `skill-updater` post-update activation behavior, Code Analyzer and Doc Converter actual installed packages/permissions.
3. **Activation vs consumption**: if `jobs: []` were changed to an active request without above gates, the scheduled runner could prematurely consume the one-shot and lose the overnight request. Do not promote just by copying the staged JSON.
4. **Quality and release gates**: actual emitted MSC/receipt, Run Catalog readback, independent review, trust/integrity checks, rollout/rollback and group writer permissions. No automatic publication or source modifications.
5. **PUBLIC auto-update risk**: `wonhwipark/L1Work` root new ZIP is discovered by in-house Skill-Updater. For this reason only a PRIVATE review artifact was made; it has not been published to the root.

## One next action

Use the already-built candidate for an approved, read-only in-house G0 check of the installed `l1-knowledge-updater` invocation and host source/approval/Skill-Updater activation contracts, then independent review. Only after the gates are satisfied, create a **new approved active One-shot version** (rather than silently reusing or overwriting the staged v0.4.35) and publish to `wonhwipark/L1Work` root with actual package hash and remote readback. User has requested public release, but currently unverified runtime and independent review prevent classifying this candidate as deployable.

## 2026-11-12 — Candidate ZIP committed to PRIVATE (latest)

- **PRIVATE_ARTIFACT_ARCHIVED=PASS**: `collab/candidates/joblist_nrtx/job-list_v0_4_35_1112.zip`; GitHub main remote directory readback size **1,562,969 bytes**, Git blob **`26c4276eb3912a7f09feddbb5fc12bd20f42ea03`**, Actions push commit prefix **`283307b`**.
- **Real inner package SHA-256 (Actions actual bytes):** `3061be176932ed145554b583624a96f0c2bbb22533c5fed8635c1acc2101779c`. After commit, GitHub blob SHA matches the Actions-reported `git hash-object`; remote directory readback PASS.
- **FINAL_SELF_TEST:** GitHub Actions run `43059239712` completed SUCCESS: baseline byte pin, ZIP CRC/manifest, Python compile, `job_core validate`, 33 pytest PASS/0 FAIL, unsupported-OS BLOCKED test, zero active jobs. This is a **development candidate**, NOT host E2E or independent review.
- **PUBLIC_RELEASE=NOT_POSTED / INHOUSE_SKILL_UPDATER=NOT_RUN / JOB_ACTIVATION=NOT_RUN / GROUP_KNOWLEDGE_WRITE=NOT_RUN**. The requested automatic analysis has **not started**. This restriction avoids unwarranted auto-install/one-shot consumption while host approval, Knowledge Updater CLI and independent review remain unverified.
- **NEXT_ONE_ACTION:** verify in-house installed Knowledge Updater invocation, owner-approved Work/SourceSnapshot and Skill-Updater activation contract, then request independent review and build a new explicitly active deployable release. Do not overwrite candidate ZIP, create a fake PASS, or treat GitHub PRIVATE posting as an in-house execution signal.
