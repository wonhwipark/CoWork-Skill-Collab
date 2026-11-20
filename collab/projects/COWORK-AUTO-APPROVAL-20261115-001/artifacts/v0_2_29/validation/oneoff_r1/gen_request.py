import hashlib, pathlib

root = pathlib.Path(__file__).parent
zip_b = (root / "skill-collab-watcher_v0_2_29_1120.zip").read_bytes()
diff = pathlib.Path(r"D:\User\whpark\cowork-phase1\v029\diff_v0_2_28_to_v0_2_29.patch").read_text(encoding="utf-8")
manifest = pathlib.Path(r"D:\User\whpark\cowork-phase1\v029\CANDIDATE_MANIFEST_v029.json").read_text(encoding="utf-8")
sha = hashlib.sha256(zip_b).hexdigest()
assert sha == "c67bc342fe77547b000fc42e1b886396cbef035c0d265dbcd124947e267ed83f" and len(zip_b) == 310753
RID = "REQ-COWORK-V029-ONEOFF-R1-20261120"

front = f"""---
schema: SKILL_COLLAB_REVIEW_REQUEST_V1
state: SUBMITTED
request_id: {RID}
request_revision: 1
project_id: COWORK-AUTO-APPROVAL-20261115-001
work_id: COWORK-AUTO-APPROVAL-20261115-001
skill_id: cowork-review-watcher
package_path: /SKILL-COLLAB/packages/skill-collab-watcher_v0_2_29_1120.zip
package_file_id: github:{RID}
package_rev: v0.2.29
package_sha256: {sha}
package_size_bytes: {len(zip_b)}
baseline_package_ref: skill-collab-watcher_v0_2_28_1119.zip SHA256=9e6ee6d30170f0a2890237c7d1b9184e5c423213a18146926b848c5269b8c00c
knowledge_refs: []
consumer_profiles: [windows-single-user-watcher]
reviewer_os: WINDOWS
test_policy: STATIC_ONLY
run_policy_ref: POLICY-STATIC-V1-DESIGN
output_contract: SKILL_COLLAB_REVIEW_RESULT_V1
goal: one independent code and security review of watcher v0.2.29 (cost-refused requests excluded for good) before any Windows LIVE install, one call, max USD 3
---
"""

body = f"""
# CoWork watcher v0.2.29 independent review R1 -- cost-refused requests are excluded for good

## Purpose and separation
One independent, static code and security review of the exact v0.2.29 ZIP below. It decides whether these bytes may later replace the Windows LIVE v0.2.25 watcher, and whether the protected delegation may later be raised from USD 1 to USD 3 for the single unified tier `POLICY-STATIC-V1`. This REQUEST authorizes nothing by itself: it is not an install, not a delegation change, not a policy change. The review is paid through the already installed manual `POLICY-STATIC-V1-DESIGN` USD 3.00 tier, used only as a one-call transport for this one ID/revision/SHA; the candidate's own unified policy is not used to review itself. Developer self tests quoted below are claims for context, not an independent result.

## Frozen inputs (everything the reviewer needs is in this file and the ZIP)
- Exact ZIP: `collab/packages/skill-collab-watcher_v0_2_29_1120.zip`, **{len(zip_b)} bytes**, SHA-256 `{sha}`, 114 members, CRC clean, two builds byte-identical.
- Baseline: v0.2.28, 309367 bytes, SHA-256 `9e6ee6d30170f0a2890237c7d1b9184e5c423213a18146926b848c5269b8c00c`, reviewed earlier (BLOCKING 0 / MAJOR 1 / MINOR 2). v0.2.29 differs from it in exactly 6 changed files and 1 new test file. The full unified diff and the manifest are embedded verbatim at the end of this REQUEST.
- The ZIP contains `skill_collab_watcher/`, `tools/` (`review_request_gate.py`, `source_pin.py`, `approval_signer.py`, `trust_root_tool.py`, `build_release.py`), `su_l1/`, all tests and docs. `tools/approve_request.py` is a host-side manual approval script and is NOT in this ZIP. Review only what is in the ZIP and in this REQUEST. The separate Work-side writer helpers (CAS, rebase, reconciliation) are NOT part of this input.

## What v0.2.29 changes relative to v0.2.28 (the single behavior change)
v0.2.28 MAJOR finding: `auto_policy.assess` returned `PER_REQUEST_COST` before any claim row existed, so a request refused only by the per-request cap stayed `NEW` forever; raising `max_request_usd` later (without refreshing `enabled_at`) admitted it retroactively.
v0.2.29: `auto_approval.py::_process` now calls `store.auto_exclude(...)` when `assess` returns `PER_REQUEST_COST`, writing an `auto_claims` row with `stage=POLICY_STOPPED` and `reserved_cents=0` (`INSERT OR IGNORE`, one row per request and revision). The existing `_resume` path treats `POLICY_STOPPED` as terminal. `state_store.py::_auto_usage_locked` now counts only rows with `reserved_cents > 0`, so exclusion rows are not telemetry calls. Docs: `AUTO_APPROVAL.md` (stale day/month ceilings removed, cap-raise behavior described), `BUDGET_POLICY_CONFIGURATION.md` (exclusion rule, `approve_request.py` is outside the package), `CUTOVER_RUNBOOK.md` title version. New test file `tests/test_v029_cost_refused_exclusion.py` (3 tests).

## Developer self-test evidence (context only, not independent, not executed by you)
- Windows full suite on the extracted ZIP, five independent rounds (own temp directory, DB, throw-away keys, fake GitHub each): 1038 passed / 12 skipped / 0 failed in every round; the five-window companion tests (two design requests and three skill requests in sequence: each READY once, no second signature, old `-DESIGN` tier refused, cap-refused request stays stopped, CLI watch with a counting stub: exactly 5 model-stub calls, none after restart) passed 5/5. The 12 skips are opt-in GUI tests and tests that need the project virtualenv.
- **Known intermittent failure (must be judged by you):** `su_l1/test_local_only_contract_r0003.py::Race::test_the_same_nonce_in_six_processes_is_accepted_exactly_once` failed in about 2 of about 31 runs. The cause of the observed failures is UNRESOLVED (the raw error of the failing run was not captured). Reproduced mechanism: an unlocked anchor read racing `os.replace` gives `PermissionError errno 13` on Windows (296 of 40000 reads in a tight loop), which `_read_anchor` turns into `ANCHOR_UNREADABLE_FAIL_CLOSED`. Injected `ANCHOR_UNREADABLE` in one of six racing workers kept the invariants in 10 of 10 trials (exactly one OK, replay refused, nonce and log counts 1/1, anchor and DB consistent, a new nonce still accepted, no temp file left). Unlocked `_verify()` callers: `Ledger.open()`, `review_state()`, `counts()`; `_mutate` verifies inside `_FileLock`. The test expectation was NOT relaxed. These measurements are not in the ZIP.

## Review questions
1. **Exclusion correctness.** Is `POLICY_STOPPED` written exactly when intended (cap refusal), never for a transient problem (unreadable pin, missing SOURCE_PIN, unreadable commit bytes, clock check, package invalid)? Walk `_process` in order and state which refusals return before `assess`. Can a request be excluded while a different, still-fixable reason also applies?
2. **Side effects of permanent exclusion.** `estimated` comes from the registered tier cost, not the request. If the registry cost of a tier is raised before the delegation cap is raised, are requests that arrive in between excluded for good and only manually approvable? Is this documented accurately and is it acceptable?
3. **Concurrency and atomicity.** `auto_exclude` is a plain `INSERT OR IGNORE` outside `BEGIN IMMEDIATE`. Can it race with `auto_claim` for the same (request, revision) from a second process, and can that admit a request that was refused or hide one that was admitted? What does `_resume` do afterwards?
4. **Retroactive admission, residual paths.** With v0.2.29, state exactly which retroactive paths are closed by code (seen while disabled, cap refusal, finished or uncertain history, `enabled_at` comparison) and which still depend on the operator.
5. **Telemetry integrity.** Does `reserved_cents > 0` change any other consumer of `auto_claims` or `window_usage`? Could a zero-cent row break claim-count, duplicate, or recovery logic?
6. **Five windows and restart.** From the code, is exactly one APPROVAL_SIG and one READY possible per (request, revision) across five sequential windows and across a watcher restart, including after an UNCERTAIN stage? Any path that signs twice?
7. **`su_l1` classification.** Does the watcher runtime import or depend on `su_l1`? Classify the intermittent failure as one of: test-only availability issue, runtime availability issue, or safety defect, with the evidence you used. State whether it must block a LIVE install and what minimal fix (if any) you would require.
8. **Carry-over from v0.2.28 review.** Confirm that the two documentation MINOR findings are actually fixed in these bytes. List anything in the docs that is still inaccurate.
9. **Release label.** The ZIP labels itself `development_not_for_deployment` in `docs/CUTOVER_RUNBOOK.md`. What must be recorded outside the ZIP so that an install of exactly these bytes is traceable?

## Boundaries
- STATIC_ONLY. Do not execute package code, tests, builders or servers; do not run the watcher; no network beyond reading this pinned input; no sub-agents.
- Report only verified BLOCKING / MAJOR / MINOR findings with file and function, failure condition, evidence, minimal fix and verification. No quota for the number of findings. Separate PASS / FAIL / NOT_RUN. List the files you actually read. Do not claim a test PASS you did not run. Linux, in-house LLM and MCP behavior are not verified by this review.
- No install, no delegation change, no second review. GPT's final disposition is a separate authority.

## Manifest (verbatim)
```json
{manifest}```

## Unified diff v0.2.28 -> v0.2.29 (verbatim)
```diff
{diff}```
"""
data = (front + body).encode("utf-8")
assert b"\r" not in data
(root / "REQUEST_v029.md").write_bytes(data)
print(RID, len(data), hashlib.sha256(data).hexdigest())
