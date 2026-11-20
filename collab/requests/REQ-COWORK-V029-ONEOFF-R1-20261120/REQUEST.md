---
schema: SKILL_COLLAB_REVIEW_REQUEST_V1
state: SUBMITTED
request_id: REQ-COWORK-V029-ONEOFF-R1-20261120
request_revision: 1
project_id: COWORK-AUTO-APPROVAL-20261115-001
work_id: COWORK-AUTO-APPROVAL-20261115-001
skill_id: cowork-review-watcher
package_path: /SKILL-COLLAB/packages/skill-collab-watcher_v0_2_29_1120.zip
package_file_id: github:REQ-COWORK-V029-ONEOFF-R1-20261120
package_rev: v0.2.29
package_sha256: c67bc342fe77547b000fc42e1b886396cbef035c0d265dbcd124947e267ed83f
package_size_bytes: 310753
baseline_package_ref: skill-collab-watcher_v0_2_28_1119.zip SHA256=9e6ee6d30170f0a2890237c7d1b9184e5c423213a18146926b848c5269b8c00c
knowledge_refs: []
consumer_profiles: [windows-single-user-watcher]
reviewer_os: WINDOWS
test_policy: STATIC_ONLY
run_policy_ref: POLICY-STATIC-V1-DESIGN
output_contract: SKILL_COLLAB_REVIEW_RESULT_V1
goal: one independent code and security review of watcher v0.2.29 (cost-refused requests excluded for good) before any Windows LIVE install, one call, max USD 3
---

# CoWork watcher v0.2.29 independent review R1 -- cost-refused requests are excluded for good

## Purpose and separation
One independent, static code and security review of the exact v0.2.29 ZIP below. It decides whether these bytes may later replace the Windows LIVE v0.2.25 watcher, and whether the protected delegation may later be raised from USD 1 to USD 3 for the single unified tier `POLICY-STATIC-V1`. This REQUEST authorizes nothing by itself: it is not an install, not a delegation change, not a policy change. The review is paid through the already installed manual `POLICY-STATIC-V1-DESIGN` USD 3.00 tier, used only as a one-call transport for this one ID/revision/SHA; the candidate's own unified policy is not used to review itself. Developer self tests quoted below are claims for context, not an independent result.

## Frozen inputs (everything the reviewer needs is in this file and the ZIP)
- Exact ZIP: `collab/packages/skill-collab-watcher_v0_2_29_1120.zip`, **310753 bytes**, SHA-256 `c67bc342fe77547b000fc42e1b886396cbef035c0d265dbcd124947e267ed83f`, 114 members, CRC clean, two builds byte-identical.
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
{
  "skill": "skill-collab-watcher",
  "version": "0.2.29",
  "status": "development_not_for_deployment; independent review NOT_RUN for this exact SHA",
  "baseline": {
    "version": "0.2.28",
    "sha256": "9e6ee6d30170f0a2890237c7d1b9184e5c423213a18146926b848c5269b8c00c",
    "size_bytes": 309367
  },
  "candidate": {
    "name": "skill-collab-watcher_v0_2_29_1120.zip",
    "size_bytes": 310753,
    "sha256": "c67bc342fe77547b000fc42e1b886396cbef035c0d265dbcd124947e267ed83f",
    "members": 114,
    "rebuild_sha256_identical": true
  },
  "changed_files": [
    "docs/AUTO_APPROVAL.md",
    "docs/BUDGET_POLICY_CONFIGURATION.md",
    "docs/CUTOVER_RUNBOOK.md",
    "skill_collab_watcher/__init__.py",
    "skill_collab_watcher/auto_approval.py",
    "skill_collab_watcher/state_store.py"
  ],
  "inherits_review_pass_from": null
}
```

## Unified diff v0.2.28 -> v0.2.29 (verbatim)
```diff
--- a/docs/AUTO_APPROVAL.md
+++ b/docs/AUTO_APPROVAL.md
@@ -21,8 +21,10 @@
 4. Package: size and sha256 equal the REQUEST, ZIP CRC, the engine's credential scan, `safe_extract`, size limit 5 MiB.
 5. Commit A: the REQUEST and the package bytes at the pinned commit equal the bytes on `main` today.
 6. No earlier history: no APPROVAL_SIG/READY/dispatch/receipt/result on the remote, no local job, no earlier reservation.
-7. The pure gate `auto_policy.assess` (GPT prototype, byte-identical): scope allow-lists, `POLICY-STATIC-V1` only, 1 call, attempt 1, per request <= $1,
-   day <= 2 calls / $3, month <= $10 (limits can only be equal to or stricter than the product ceilings), counting the watcher's own recorded dispatches.
+7. The pure gate `auto_policy.assess`: scope allow-lists, `POLICY-STATIC-V1` only, 1 call, attempt 1, per request <= `max_request_usd`.
+   There are no day or month count/cost admission gates; legacy `max_day_*` / `max_month_*` keys are accepted and ignored.
+   A request refused only by `PER_REQUEST_COST` is recorded as `POLICY_STOPPED` (zero reserved cents) and is never admitted automatically afterwards,
+   even if `max_request_usd` is raised later. Such a request needs an explicit manual approval.
 8. The official validator on the READY text that WILL be published (bytes fixed before signing).
 9. Atomic reservation (`BEGIN IMMEDIATE`, one row per request and revision, day/month ceilings inside the same transaction).
 10. Re-check (delegation still enabled and unexpired, repository id unchanged) -> sign with the existing `tools.approval_signer` -> verify with the
@@ -47,13 +49,15 @@
 {"schema": "AUTO_DELEGATION_V1", "enabled": false, "repo_id": "1451933830", "branch": "main",
  "projects": ["<explicit work ids>"], "skills": ["<explicit skill ids>"], "policy": "POLICY-STATIC-V1",
  "enabled_at": "2026-11-16T00:00:00+09:00", "expires_at": "2026-12-16T00:00:00+09:00",
- "max_request_usd": 1.0, "max_day_calls": 2, "max_day_usd": 3.0, "max_month_usd": 10.0}
+ "max_request_usd": 1.0}
 ```
 `config-check` prints the state without any path of a secret. `acl_check: "skip"` exists for isolated tests only and is printed as a warning.
 
 ## Enabling procedure (after an explicit user approval; not part of this candidate)
 install with `enabled: false` -> let one watch cycle pass (every pending REQUEST is recorded as "seen while off") -> set `enabled: true` and
 `enabled_at` to now. Revoke by setting `enabled: false` (takes effect at the next check, also between signing and publishing).
+Raising `max_request_usd` does not need an `enabled_at` change for requests already refused by the cap (they are excluded for good). Other
+requests seen while enabled stay eligible after a raise; set `enabled_at` to the raise time if they must be excluded too.
 
 ## Rollback
 Remove the `auto_approval` section (or keep `enabled: false`) and restart; the two new tables stay unused. Restore the previous package folder from
--- a/docs/BUDGET_POLICY_CONFIGURATION.md
+++ b/docs/BUDGET_POLICY_CONFIGURATION.md
@@ -1,4 +1,4 @@
-# Per-review budget policy (v0.2.28 development)
+# Per-review budget policy (v0.2.29 development)
 
 Unified default for every new independent review: USD 3.00, single `run_policy_ref=POLICY-STATIC-V1`.
 No daily/monthly cost or count ceilings. Do not auto-upgrade a request. The DESIGN/LARGE names below
@@ -19,6 +19,9 @@
   "policy": "POLICY-STATIC-V1",
   "max_request_usd": 3.0
 
+A request first seen while the per-request cap is too low is recorded as `POLICY_STOPPED` and stays excluded from automatic signing even after the cap is raised; it can only be approved manually.
+`tools/approve_request.py` is a host-side manual approval script and is not part of this package.
+
 The request names only run_policy_ref, never the price. `POLICY-STATIC-V1` requires the
 pre-existing permitted project/skill and valid SOURCE_PIN/signature/READY, same as before.
 `POLICY-STATIC-V1-LARGE` and `POLICY-STATIC-V1-DESIGN` are REVIEW_POLICY-refused by the
--- a/docs/CUTOVER_RUNBOOK.md
+++ b/docs/CUTOVER_RUNBOOK.md
@@ -1,4 +1,4 @@
-# Cutover runbook: Dropbox to GitHub (v0.2.28, development_not_for_deployment)
+# Cutover runbook: Dropbox to GitHub (v0.2.29, development_not_for_deployment)
 
 Status: a design with isolated test evidence. Nothing here installs, starts or switches anything on the
 operating host. Each step marked APPROVAL needs an explicit decision by the user.
--- a/skill_collab_watcher/__init__.py
+++ b/skill_collab_watcher/__init__.py
@@ -1 +1 @@
-__version__ = "0.2.28"
+__version__ = "0.2.29"
--- a/skill_collab_watcher/auto_approval.py
+++ b/skill_collab_watcher/auto_approval.py
@@ -538,6 +538,8 @@
                                   atomic_claim_available=True)
         ok, reason = auto_policy.assess(scoped, cand, ev)
         if not ok:
+            if reason == "PER_REQUEST_COST":
+                store.auto_exclude(rid, rev, cand.zip_sha256, now, "PER_REQUEST_COST: excluded for good; manual approval only")
             ev_name = "AUTO_DUPLICATE_BLOCKED" if reason == "DUPLICATE_OR_UNCERTAIN" else "AUTO_NOT_ELIGIBLE"
             self._once(ev_name, rid, reason)
             return AutoResult(reason)
--- a/skill_collab_watcher/state_store.py
+++ b/skill_collab_watcher/state_store.py
@@ -326,7 +326,7 @@
         month = KST calendar month. `exclude` removes the candidate's own identity when a stored candidate is re-checked."""
         day_start, month_start = kst_window_starts(now)
         window_rows = self.conn.execute(
-            "SELECT request_id, revision, reserved_cents, created_at FROM auto_claims WHERE created_at >= ?", (month_start,)).fetchall()
+            "SELECT request_id, revision, reserved_cents, created_at FROM auto_claims WHERE created_at >= ? AND reserved_cents > 0", (month_start,)).fetchall()
         dispatch_rows = self.conn.execute(
             "SELECT ts, event, processing_key, detail FROM audit_log WHERE event IN ('REVIEW_DISPATCHED', 'REVIEW_COST') AND ts >= ? ORDER BY id",
             ((datetime.fromtimestamp(month_start, KST) - timedelta(days=1)).astimezone(timezone.utc).isoformat(),)).fetchall()
@@ -402,6 +402,16 @@
             self.conn.execute("ROLLBACK")
             raise
         return "CLAIMED"
+
+    def auto_exclude(self, request_id: str, revision: str, package_sha256: str, now: int, detail: str) -> None:
+        if self._skip_write("AUTO_EXCLUDE", None, request_id):
+            return
+        day_key = datetime.fromtimestamp(now, KST).strftime("%Y-%m-%d")
+        month_key = datetime.fromtimestamp(now, KST).strftime("%Y-%m")
+        self.conn.execute(
+            "INSERT OR IGNORE INTO auto_claims (request_id, revision, package_sha256, stage, reserved_cents, day_key, month_key, detail, created_at, updated_at) "
+            "VALUES (?, ?, ?, 'POLICY_STOPPED', 0, ?, ?, ?, ?, ?)",
+            (request_id, revision, package_sha256, day_key, month_key, detail, now, now))
 
     def auto_update(self, request_id: str, revision: str, now: int, **fields) -> None:
         if self._skip_write("AUTO_UPDATE", None, request_id):
```
