---
schema: SKILL_COLLAB_REVIEW_RESULT_V1
review_id: "REQ-COWORK-V0219-R2-20261114|1|6e7fee3340cc6d0282d1c18fe3db42a90360259dd73fa6d7c0a7698af7afe5c0|1"
responds_to_request_id: "REQ-COWORK-V0219-R2-20261114"
responds_to_request_revision: "1"
package_sha256: "6e7fee3340cc6d0282d1c18fe3db42a90360259dd73fa6d7c0a7698af7afe5c0"
skill_id: "cowork-review-watcher"
run_policy_ref: "POLICY-STATIC-V1-LARGE"
knowledge_refs: [{"path": "/SKILL-COLLAB/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/review-inputs/REV-COWORK-V0219-20261114/REVIEW_MANIFEST.md", "sha256": "a67d4bd346f1afc0e1d01171e8565470c21c387ed1101010a5373007c00e1657"}, {"path": "/SKILL-COLLAB/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/review-inputs/REV-COWORK-V0219-20261114/diff_v0_2_17_to_v0_2_19.patch", "sha256": "8a194eb0d1363a4d93f1763b1503ff59683be5674837a778f14b70c640dfa4f4"}]
consumer_profiles: ["windows-single-user-watcher"]
reviewer_os: WINDOWS
review_scope: CODE_REVIEW
test_policy: "STATIC_ONLY"
execution_status: COMPLETED
limitations: ["static review by an automatically started Claude Code process; no package code was executed", "knowledge files were delivered as the REQUEST pinned them; which parts were actually read is reported by the reviewer in the text", "reviewer host is Windows; Linux, in-house LLM and MCP behaviour are not verified by this review"]
---

# 리뷰 결과

## Review Report — CoWork watcher v0.2.19 (R2, request REQ-COWORK-V0219-R2-20261114)

### Scope actually read
`skill_collab_watcher/orchestrator.py` (`_check_approval`, `_remote_result_published`, `_reserve_dispatch`, `_check_ceilings`, dispatch body of `run_scan_cycle`/`_dispatch_group` lines ~420–930), `state_store.py` (`claim`, `record_claim`, `seal_interrupted`, `get_job`, `create_job`, `update_job_state`, `find_dispatched_logical_job`, `dispatches_since`, `spend_since`), `github_transport.py` (full `_get`/`_raise_for`/`list_folder*`/`download*`/`get_metadata`/`upload`/`repository_id`), `transport_base.py` (contract + exceptions), `shadow_guard.py`, `review_runner.py` (taskkill/timeout section), `watch_loop.py`, `cli.py` (`_build_transport`, watch-loop wiring), `tests/test_v019_crash_matrix.py`, `tests/test_v018_gates.py`, and the diff/manifest. I did not re-read `approval.py`, `validator.py`, `zip_safety.py`, or the remaining test files beyond what's quoted above — those are unchanged by this patch per the diff and out of the stated scope.

---

### Q1 — Atomicity of the reservation
`GitHubTransport.upload()` (github_transport.py:286-307) does a client-side `get_metadata` pre-check, then PUTs with no `sha` (create-only), and treats **both** HTTP 409 and 422 as `UploadConflict`. The real atomicity guarantee is not the client-side pre-check (which is racy, as the code itself acknowledges in the `_reserve_dispatch` comment) but GitHub's server-side behaviour on a create PUT: a second create for a path that already exists on the branch tip is rejected (422/409), because GitHub serializes commits onto one branch ref. `_reserve_dispatch` correctly treats the pre-check as a fast path only and falls back to `download_latest` + content comparison after a conflict. Given GitHub's documented ref-update semantics, **no finding** for two processes reserving the same `(request_id, revision)` — but this is a claim about GitHub server behaviour that cannot be verified from a static Windows-only review; it is inherited, not re-derived (flagged as unverified below).

### Q2 — Duplicate keys / binding
The reservation record embeds `processing_key` and `package_sha256`, and `_reserve_dispatch`'s "ours" test requires both to match plus `job.attempt_count >= 2`. A different package under the same `request_id`+`revision` is intercepted earlier by the `CONFLICT` branch (orchestrator.py:662-667) before reservation is even attempted, so it can't silently share a slot. Approval binding itself (`expected` dict in `_check_approval`, lines 465-476) separately hashes `request_sha256`/`ready_sha256`/`package_sha256`, so a re-signed approval or resubmitted request is still bound to exact bytes via `verify_approval`, independent of the dispatch reservation. **No finding.**

### Q3 — Classification / double start / permanent refusal
Traced the `attempt_count` lifecycle: it is bumped only inside `StateStore.claim()`'s single `UPDATE ... WHERE state IN (...)` (state_store.py:255-259), i.e. once per successful claim transition, and nowhere else by default (`update_job_state` only bumps if `bump_attempt=True`, which the dispatch path never passes). The `BEFORE_START` usage-limit path resets the job to `VALIDATED` without bumping attempt further, so the *next* claim (attempt 2) is what makes `ALREADY_OURS` legitimately fire on retry — this matches the manifest's intended "usage-limit retry" story and is exercised by `test_q8_...` in test_v018_gates.py. A **lost/reset local row** makes `store.get_job(...)` return `None`, which forces `ours=False → FOREIGN` (orchestrator.py:548-551) — fail-safe, confirmed by `test_a_foreign_reservation_seals_the_request_as_uncertain_without_a_model_call`. I did not find a path where `attempt_count` reaches ≥2 without the job having actually been claimed+dispatched at least once, so I found no state where a paid review starts twice or a legitimate retry is permanently FOREIGN. **No finding** beyond what the manifest already flags as accepted.

### Q4 — Crash / restore
The crash matrix (`before_reservation`, `after_reservation`, `during_model`, `before_result_saved`, `before_publish`, `publish_fails`, `completed`) × (state kept / lost / old backup restored) is asserted to produce ≤1 model start and no vanished job, and `seal_interrupted` (state_store.py:275-316) converts any `CLAIMED`/`REVIEW_RUNNING` row not owned by the current process into terminal `REVIEW_UNCERTAIN` *before* any dispatch in the same process, which is the mechanism that makes the invariant hold even when the remote reservation was written but the local row survives in `CLAIMED`. I traced this logic directly (not just the test assertions) and it is internally consistent: a crash strictly between claim and a successful reservation write leaves no remote trace and reclaims cleanly after state loss; a crash after a successful reservation write always leaves a remote FOREIGN/ALREADY_OURS marker that blocks a second model start even after total local loss. **No finding** — this is the one part of the patch I'd call solidly verified from first principles, not just trusted test output.

### Q5 — Remote errors / fail-closed
`_raise_for` (github_transport.py:128-139) maps 401/403→`AuthRequired`, 404→`RemoteNotFound`, 429/5xx/rate-limited-403→`TransientTransportError`, everything else→`TransportError`. `_reserve_dispatch` and `_remote_result_published` both catch `(TransportError, AuthRequired)` and fail closed (`ERROR`/retry, never "proceed"). I could **not verify** GitHub's actual read-after-write visibility window for Contents API (the "eventual visibility of a just-written record" part of Q5) from a static review — this is an assumption the design depends on (see Q1) and is explicitly out of reach of this review.

### Q6 — N2 repository-id binding — **BLOCKING finding**
**File/function:** `skill_collab_watcher/github_transport.py:158-169` (`GitHubTransport.repository_id`), consumed by `orchestrator.py:440-451` (`_check_approval`).

**Failure condition:** `repository_id()` caches `self._repo_id` for the lifetime of the `GitHubTransport` object. `cli.py:_build_transport` is called **once** before the watch loop (`cli.py:288`, `rt = ...`), and `run_cycle=lambda: _one_cycle(rt)` (`cli.py:538`) reuses that same transport object for every scan cycle for the entire life of a `run_watch` process (confirmed in `watch_loop.py:72-110`, which loops calling `run_cycle()` repeatedly without rebuilding the transport). So in the real CLI, `repository_id()` is fetched from GitHub **exactly once per watch-process lifetime**, not once per cycle.

Consequently, if the underlying GitHub repository behind `owner/name` is swapped during a long-running watch session (e.g. the repo is deleted and a new repo is created under the identical `owner/name`, which GitHub assigns a new numeric id to), every subsequent N2 check still compares the **stale, first-observed** id against `trust.repo_id` and will keep reporting success (or keep reporting the *original* mismatch/match outcome) even though all the live Contents-API calls (`list_folder`, `download`, `get_metadata`, `upload`) are now hitting the new repository. N2's own docstring states "fail closed" as its purpose; this caching defeats that purpose for the remainder of a long-running process.

**Evidence this is untested:** The test suite's `run()` helper in `tests/bundle.py:21-22` does `transport or make_transport(env.http)`, i.e. it builds a **fresh** `GitHubTransport` (with `_repo_id=None`) on every single call unless a transport is explicitly passed in. All of `test_v018_gates.py`'s N2 tests (`test_n2_another_repository_id_blocks_the_review`, etc.) therefore only ever exercise the "first fetch" path; none of them keep one transport alive across multiple cycles while `http.repo_id` changes, so this gap in the real CLI is not covered by any test I read.

**Minimal fix:** drop the cache (or scope it to one scan cycle, e.g. clear `self._repo_id` at the top of `run_scan_cycle`/each `ensure_auth()` call) so `repository_id()` re-verifies against the live server on every approval check, matching the per-cycle re-verification already done for `server_time()`/clock checks in the same function.

**How to verify:** add a test using `tests/bundle.py`'s `run(env, transport=shared_transport)` with one transport instance reused across two `run()` calls, where `env.http.repo_id` is changed between the two calls; assert the second call also raises `APPROVAL_REPO_ID_REMOTE_MISMATCH` (it currently will not, with a cached transport).

I judged this BLOCKING because it silently defeats a security control (N2) that the manifest explicitly describes as "fail closed," for an attacker capability (repo-identity takeover under the configured owner/name) that is plausible for a GitHub repo over the lifetime of a long-running unattended watcher, even though it requires some namespace control the reviewer cannot fully characterize from static code alone.

### Q7 — Cost/gates, reservation vs. ceilings, SHADOW
`claim()`'s ceiling SQL (state_store.py:242-254) counts `CLAIMED`/`REVIEW_RUNNING` rows with no `REVIEW_DISPATCHED` audit entry as "reserved" toward the ceiling — this correctly prevents two processes both seeing "room" before either logs a dispatch. A reservation that is written remotely but never followed by paid work (crash between reservation and `REVIEW_RUNNING`) does **not** permanently consume ceiling capacity: once `seal_interrupted` reclassifies the stuck row to terminal `REVIEW_UNCERTAIN`, it drops out of the `CLAIMED`/`REVIEW_RUNNING` set and the ceiling frees up, and `dispatches_since`/`spend_since` only count `REVIEW_DISPATCHED`/`REVIEW_COST` audit events, which were never written. Matches the manifest's accepted gap #1 (new revision needed, fail-closed, not reported as paid). SHADOW is blocked twice independently: `StateStore.claim()` calls `self._skip_write(...)` and returns `"LOST"` immediately for a read-only store (never reaching `_reserve_dispatch`), and even if it did, `GitHubTransport.upload()` raises `TransportError("READ_ONLY_TRANSPORT...")` for `read_only=True` (github_transport.py:287-288). **No finding.**

### Q8 — Interaction with v0.2.18, locking, seal_interrupted, publish-only retry
`seal_interrupted` runs only when `exclusive=True` (the watcher lock is held) and only once per `StateStore` instance (`sealed_at_open`), before any dispatch in that process — this is exactly the ordering the N1/N2 reservation logic depends on to avoid sealing rows another live process still owns. `_retry_publish_only` (orchestrator.py:840-875) is structurally prevented from calling the runner (it has no `ReviewRunner` parameter at all) and reuses the stored `existing.processing_key`/`package_sha256`, so a publish-only retry can't trigger a second reservation or model call; it only re-attempts `_publish_result`. I traced this and it's consistent with `test_v018_gates.py`'s Q8 composite scenario (usage-limit hold → restart → policy-revision change → rollback → lost cursor → second process → full state loss → exactly one `COMPLETED` review). **No finding**, other than the Q6 caching issue above, which is orthogonal to locking/seal_interrupted but shares the "lives across cycles" root cause.

---

### Findings summary

**BLOCKING**
1. **N2 repository-id check uses a process-lifetime cache** — `github_transport.py:158-169` / `orchestrator.py:440-451`. See Q6 above for failure condition, evidence, fix, and verification steps.

**Non-blocking**
1. Q1/Q5's atomicity and read-after-write-visibility guarantees rest entirely on documented GitHub Contents-API server behaviour (serialized branch commits, 409/422 on conflicting creates, prompt visibility of a just-committed file to the same credential). This is architecturally sound and matches the design in `_reserve_dispatch`, but is unverifiable from a static Windows review and was not independently exercised against real GitHub by me (the manifest's "on real GitHub (throw-away branch)" results are the author's claim, not mine).
2. `review_runner.py` S2 `taskkill` exit-status logging (`review_runner.py:193-197`) is a sound, low-risk addition; confirmed by reading, not retested live.

---

### What I could not verify
- Live GitHub Contents-API atomicity/visibility semantics under concurrent writers (requires a real two-writer test against GitHub, out of scope/budget for a static review).
- The author's reported test run (673 passed/12 skipped; 606 passed/17 skipped without `cryptography`) and the real-GitHub throw-away-branch results — these are claims in the manifest, not reproduced by me.
- Any Linux, in-house-LLM, or MCP behaviour — explicitly out of scope per the manifest and REQUEST; this review is Windows-only as instructed.
- Whether a real-world repo-id swap (Q6) is actually reachable by a plausible threat actor for this `windows-single-user-watcher` profile — I verified the code path and cache lifetime, not the practical likelihood of a GitHub repo-identity takeover under a fixed owner/name.

### Consumer profiles judged against
`windows-single-user-watcher` (the only profile given). All code paths read (cli.py, watch_loop.py, orchestrator.py, state_store.py, github_transport.py) are the Windows/single-watcher paths; I did not examine Dropbox-transport or multi-tenant assumptions beyond confirming they're not what's reused across the watch loop.

### Proposed corrections to common knowledge (GPT to decide)
- The REVIEW_MANIFEST's "known gaps" list (items 1–4) are all confirmed accepted/handled by the code as described — no correction needed there.
- Suggest adding a fifth "known gap" entry for future reviewers: **the `repository_id()` cache lifetime spans the whole watch process**, not one scan cycle, which the current N2 tests (all using a fresh `make_transport()` per call) do not exercise. This should be called out explicitly so a future R3 doesn't re-discover it by accident or, worse, assume the existing N2 tests cover the long-running-process case.
