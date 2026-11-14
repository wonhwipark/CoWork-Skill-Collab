# JOBLIST-SMOKE-20261114-001 — CURRENT
- Date: 2026-11-14 KST
- Goal: 새 One-shot ID로 MCP → Skill-Updater → Job-list Activation/Registry → Runner/Worker → Result/Receipt → MCP readback 검증.
- State: CANDIDATE_PREPARED. **전체 설치 가능 ZIP 미생성 / PUBLIC 미게시 / 호스트 설치·실행 NOT_RUN**.
- PUBLIC baseline: `wonhwipark/L1Work/main` `job-list_v0_4_36_1112.zip`; 과거 배포/설치와 호스트 E2E 성공을 구분.
- New Work ID: `JOBLIST-SMOKE-20261114-001`
- New Job ID: `JOB-20261114-JOBLIST-E2E-SMOKE-01`; old `JOB-20261112-NR-L1TX-KNOWLEDGE-MSC-EXEC-01` **재실행 금지**.
- Proposed package: `job-list_v0_4_37_1114.zip` (**NOT_BUILT / NOT_POSTED**)
- Profile: `joblist-e2e-smoke-linux`; single Linux request, params={}, retry=0, expires 2026-11-17 23:59:59 KST.
- Requested no-LLM smoke Worker: `scripts/joblist_e2e_smoke.py` within a future isolated candidate package; no code analysis, no Knowledge writes, no external exports.
- Local isolated Worker tests: `3 PASS / 0 FAIL`, manifest identity, absent runner identity blocks, unique Run ID receipt, duplicate refusal. No live Job-list core integration test.
- Old current evidence: v0.4.36 Catalog active vs Registry absent; queue DONE/SUCCESS but Run ID and Worker start absent; MCP result RESULT_UNSUPPORTED. Latest in-house GPT/MCP debugging fix, installed diffs/versions **NOT independently verified** in this task.

## Packaging gate
1. On-host debugging patch/diff & actual MCP/Job-list call contracts independently verify; if absent, BLOCKED.
2. Build from pinned original v0.4.36 in an isolated workspace, updating VERSION, all package identity fields, manifest/SHA and `scripts/job_core.py` builtin profile; exactly one active Job `JOB-20261114-JOBLIST-E2E-SMOKE-01`. Do not hand-install loose files or overwrite prior ZIP.
3. Preserve existing Registry/Queue/Receipt/Run, old Job IDs, production DB and scheduler. Never requeue or reactivate the consumed v0.4.36 Job.
4. Run package CRC/manifest/path/secret scans, compile, profile validate, targeted regression and non-model duplicate safety test. `SELF_TEST` is not independent review.
5. PUBLIC `L1Work/main` root deployment and in-house install/activation are **separate approval gates**; PRIVATE docs do not trigger them. Only authorized final new ZIP may be posted PUBLIC, with SHA-256/size and remote readback verified.

## Host E2E PASS proof — same new Job ID end to end
- Updater actual archive SHA and installed version agree.
- Catalog active and Registry contains the new ID.
- Queue entry → Runner `run_id` → actual Worker start recorded.
- New Worker output `SMOKE_WORKER_REACHED`, `llm_invoked=false`, `analysis=NOT_RUN`.
- Receipt/Run Catalog/result semantics reconcile for same ID and Run ID.
- MCP result readback returns the same original result; `RESULT_UNSUPPORTED` is not PASS.
- Exactly-once: duplicate activation causes no second execution, old Job receipts unchanged.
- Do not treat queue DONE or result JSON alone as full E2E PASS.
- On Smoke E2E PASS only, plan a **separate newly approved Job ID** for NR L1 Tx 4 scenarios.

## Status and next
- DEVELOPMENT: CANDIDATE_REQUEST_ONLY
- SELF_TEST: 3 PASS synthetic Worker tests, no complete package test
- INDEPENDENT_REVIEW: NOT_RUN
- PUBLIC_RELEASE: NOT_POSTED
- HOST_E2E: NOT_RUN
- USER_APPROVAL_NEEDED: PUBLIC ZIP deployment / operational activation
- NEXT: inspect actual in-house debug changes, build + self-test installable candidate in isolation; release/execute only with appropriate approval.
