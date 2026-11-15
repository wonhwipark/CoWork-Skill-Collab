# GPT v0.2.21 static disposition and one-shot corrective handoff

- Date: 2026-11-15 KST; revision r0001
- Repository: GitHub PRIVATE wonhwipark/CoWork-Skill-Collab; branch main
- Exact path: collab/projects/COWORK-AUTO-APPROVAL-20261115-001/GPT_V0221_STATIC_DISPOSITION_AND_SINGLE_FIX_HANDOFF_r0001_20261115.md
- Work ID: COWORK-AUTO-APPROVAL-20261115-001
- Input: CLAUDE_AUTO_APPROVAL_ONE_SHOT_RESULT_FOR_GPT_20261115.md and artifacts/v0_2_21/CANDIDATE_MANIFEST.md, diff_v0_2_20_to_v0_2_21.patch, skill-collab-watcher_v0_2_21_1115_DEV_NOT_FOR_DEPLOYMENT.zip
- Disposition: **REVISE_BEFORE_INDEPENDENT_REVIEW**. Static review BLOCKING 2 / MAJOR 2. No paid model, signer, READY, task modification or LIVE auto-signing is authorized by this document.

## I. Evidence and status

Windows Claude Code reported DEVELOPMENT=PASS and SELF_TEST_REPORTED=PASS: Windows Python 3.11.9 test venv and operating interpreter each 817 PASS / 12 SKIP, isolated SHADOW CLI 8/8, mutation 16/17, rollback isolation PASS. One first-run intermittent failure remains unidentified (later repeats passed). The pre-existing v0.2.20 GitHub LIVE watcher, original DB/Task/keys/Notifier remain unchanged; AUTO_SIGNING=OFF and new paid calls=0. **INDEPENDENT_REVIEW=NOT_RUN**.

GPT directly fetched the PRIVATE candidate ZIP as base64, decoded the **actual 272839 bytes**, and independently computed SHA-256 **16921bf4021714345cabc78de5e2e8a6882891615f90b5747622570ca4465d8b**, matching the Windows report; Git blob 4cf3a70109fad07fe546b4ab9304193a67e70926. Actual ZIP CRC/full Windows execution was host-reported, not separately reproduced here. GPT also read the 2409-line patch and inspected the code locations below. The two findings are code-path and simple integer-state reproductions; actual Windows paid-call/cost violation was not tested.

## II. Blocking corrections

### B1 — Blocker: max-of-two-counters can undercount disjoint reservations and dispatches

- Patch line approximately 1042; skill_collab_watcher/state_store.py auto_claim.
- Existing: day_calls, day_cents, month_cents = max(day_calls, extra_day_calls), max(day_cents, extra_day_cents), max(month_cents, extra_month_cents).
- Counterexample (same calendar day): **A** pending auto-sign reservation 1 call/$1, **B** separate manually dispatched review 1 call/$1, **C** new candidate auto approval. max(1,1)=1 admits C with limit 2, while the union of distinct requests after C is 3. This violates the local delegation call/count protection even if the existing Watcher later stops actual model dispatch. No evidence that the existing Watcher charged beyond its separate limit.
- Fix: count deduplicated union of auto reservation identities and existing job/dispatch/receipt identities, in a transactionally coherent reservation decision. For a temporary safe fallback use conservative sum (overcount/fail-closed acceptable, but not a final unusable behavior). Check day and month costs too; use the stricter of the Watcher and delegation ceilings.
- Regression: A reserved + separate B manual dispatched + C must DENY; A both auto-reserved and dispatched counts only once; same-day 2-call/$3, monthly $10, concurrent requests, restart and ledger recovery, KST rollover. Prove old candidate FAIL and patched candidate PASS.

### B2 — Blocker: current protected delegation narrowing not revalidated at sign/publish boundaries

- Patch lines approximately 625–641; skill_collab_watcher/auto_approval.py _still_allowed used by _sign_and_post and _publish.
- Currently re-reads enabled/expiry/repo_id only. Does not recheck project and skill allowlist, limit changes, enabled_at or same delegation/policy identity.
- Scenario: owner initially permits project A, candidate A reserved; owner changes protected local policy to permit B only while enabled=true and repo_id unchanged. Existing _still_allowed returns TRUE, allowing A to be signed or READY to be posted after the scope restriction.
- Fix: bind claim to approved immutable delegation hash/revision or fully revalidate current delegation + candidate/limits before signing and before each remote publication; narrowed or changed policy must fail closed, never silently use old scope. Preserve previously published remote bytes and REVIEW_UNCERTAIN/no additional calls.
- Regression: remove project/skill, lower per-request/day/month limits, change enabled_at/expiry, disable policy, change policy identity after RESERVE, SIGNED_LOCAL and APPROVAL_POSTED; subsequent SIGN/READY zero unless current delegation still explicitly allows exact candidate. Existing unchanged delegation remains PASS.

## III. Major items and original product goal

### M1 — Intermittent regression failure needs accurate characterization

First extracted-test venv run had one FAIL whose test name is missing; subsequent repeats (venv 4, operating interpreter 3, targeted timing 3) all PASS. Obtain failing test identity/stack if logs remain or record NOT_REPRODUCIBLE and run timing stress/cross-version comparison. Do not misstate as a confirmed new regression or a universally clean 100% environment.

### M2 — Exact project/skill allowlist may force manual action for every new Work

The pure policy requires exact membership in projects and skills. The caller sets project from project_id or work_id, and if both differ it sets project empty. Confirm real REQUEST V1 permits distinct project_id/work_id. Even when security gate works, a brand-new project ID outside allowlist cannot auto review; this may violate the user goal of no per-REQUEST human action.

Define how to delegate a **stable, preapproved scope** (skill/profile/category/explicit project family) rather than requiring each new Work ID, without silently granting a wildcard. The exact allowed scope and limits must remain in the protected local owner policy and are NOT yet approved. If real project IDs are stable across repeated reviews, explain when exact mode is sufficient. Include explicit safe negative tests for foreign projects, skills, policy escalation, and arbitrary GitHub document statements. Do not widen scope in a live policy.

## IV. Other gates

- v0.2.21 adds around 900 lines to Windows trust-sensitive signer/ledger code; the developer's 817 PASS is SELF_TEST, not independent validation. After the two blockers are corrected, recommend one **independent Claude review** of the frozen patched candidate and its diff: POLICY-STATIC-V1-LARGE, R2, **maximum USD $3, one call**, **not yet approved**. Do not request model usage before GPT confirms fix and user cost authorization.
- Operating Notifier must support AUTO_SIGNING_UNCERTAIN if enabled, but do not change it now.
- Existing Work→Knowledge and dashboard requests with READY absent are **not retrospectively auto-enqueued** by this candidate. The owner-approved $1 for one older request is NOT a blanket future auto-delegation approval.
- Status: CANDIDATE=development_not_for_deployment; GPT_STATIC=BLOCKING_2/MAJOR_2; INDEPENDENT_REVIEW=NOT_RUN; ACTIVE_PROVIDER=GITHUB_LIVE_v0.2.20; AUTO_SIGNING=OFF; NEW_PAID_CALLS=0.

## V. Single Windows Claude Code next action — development and tests only

Read this exact file from PRIVATE main and in a single session:
1. Reproduce/fix **B1 and B2** in an isolated copy of v0.2.21; add failing-on-old/passing-on-new targeted regressions and real signer/READY payload verifier tests.
2. Address M1/M2 without scope creep; record actual REQUEST compatibility and a usable safe stable-scope option if needed. Never auto-enable or broaden any operating policy.
3. Re-run baseline regression (v0.2.20), full new Windows Python 3.11.9 tests, cost/concurrency/restart/413/409/422/503/error and RESERVED/SIGNED_LOCAL/APPROVAL_POSTED/READY_POSTED/UNCERTAIN scenarios, fake GitHub/fake signer SHADOW, archive security and isolated rollback.
4. Publish a **new-version development_not_for_deployment ZIP** preserving v0.2.20/v0.2.21 originals, with raw byte SHA-256, size, ZIP CRC, path/symlink/secrets checks and evidence. A v0.2.22 filename is only an example; check for collisions before naming.
5. Write result to collab/projects/COWORK-AUTO-APPROVAL-20261115-001/CLAUDE_V0221_GPT_FINDINGS_FIX_RESULT_FOR_GPT_20261115.md; update this Work CURRENT.md and TRACKER.json, and verify each remote commit/content/ZIP SHA by readback. Developer self-tests stay SELF_TEST_REPORTED, independent review NOT_RUN.
6. **Do not perform any paid Claude model review, official REVIEW REQUEST/READY, Windows operating install, operating DB/Task/Notifier/key change, public release, or LIVE auto signing enable.** Do not ask user for intermediate approval while doing isolated fixes/tests. If one item is blocked, report it and continue remaining allowed work.

After this one-shot fix result is posted, GPT performs a single consolidated disposition: verify blockers cleared, then present one combined request for R2 cost authorization plus bounded owner-delegation scope and conditional operating installation/rollback approval. Never equate a GitHub document posting with Windows Claude Code automatic execution.

### Single prompt to paste into Windows Claude Code

GitHub PRIVATE wonhwipark/CoWork-Skill-Collab branch main: read collab/projects/COWORK-AUTO-APPROVAL-20261115-001/GPT_V0221_STATIC_DISPOSITION_AND_SINGLE_FIX_HANDOFF_r0001_20261115.md as the latest authoritative GPT disposition. Fix B1 (auto reserve/manual dispatch count union) and B2 (protected delegation policy narrowed between reserve/sign/READY) in the isolated v0.2.21 copy, add old-fail/new-pass tests, examine M1 intermittent failure and M2 stable permission scope/new Work compatibility, run full regression/SHADOW/rollback/security checks and build a distinct development ZIP. Publish CLAUDE_V0221_GPT_FINDINGS_FIX_RESULT_FOR_GPT_20261115.md + this Work CURRENT.md/TRACKER.json with remote readback. No operating modification, no real signer, no REVIEW REQUEST/READY, no paid call, no public release. Keep GitHub LIVE v0.2.20 unchanged.
