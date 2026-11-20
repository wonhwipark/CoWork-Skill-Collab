---
schema: SKILL_COLLAB_REVIEW_RESULT_V1
review_id: "REQ-COWORK-V029-ONEOFF-R1-20261120|1|c67bc342fe77547b000fc42e1b886396cbef035c0d265dbcd124947e267ed83f|1"
responds_to_request_id: "REQ-COWORK-V029-ONEOFF-R1-20261120"
responds_to_request_revision: "1"
package_sha256: "c67bc342fe77547b000fc42e1b886396cbef035c0d265dbcd124947e267ed83f"
skill_id: "cowork-review-watcher"
run_policy_ref: "POLICY-STATIC-V1-DESIGN"
knowledge_refs: []
consumer_profiles: ["windows-single-user-watcher"]
reviewer_os: WINDOWS
review_scope: CODE_REVIEW
test_policy: "STATIC_ONLY"
execution_status: COMPLETED
limitations: ["static review by an automatically started Claude Code process; no package code was executed", "knowledge files were delivered as the REQUEST pinned them; which parts were actually read is reported by the reviewer in the text", "reviewer host is Windows; Linux, in-house LLM and MCP behaviour are not verified by this review"]
---

# 리뷰 결과

I now have enough to confirm `su_l1` is standalone/not wired in. I have sufficient evidence for all questions. Let me write the final review.

## Review: skill-collab-watcher v0.2.29 (SHA ...b886396cbef035c0d265dbcd124947e267ed83f)

### Q1 — Exclusion correctness

Walking `_process` in `skill_collab_watcher/auto_approval.py:442-545` in order, these refusals return **before** `assess` is ever called (so `auto_exclude` cannot be reached for them): `POLICY_PROBLEM` (448-453), `DISABLED` (454-455), `PRE_EXISTING_REQUEST` (456-458), `PIN_MISSING`/`IDENTITY_UNREADABLE` (470-475), `PIN_MISMATCH` from pin parsing (476-481), `PROJECT_IDS_DIFFER`/`PROJECT_ID_MISSING`/`PROJECT_NOT_IN_SCOPE` (486-496), `COMMIT_UNREADABLE` (503-514), and the three "specific, honest reasons" `PIN_MISMATCH`/`PACKAGE_INVALID`/`COMMIT_A_MISMATCH` (526-534) — all of these are checked explicitly ahead of the call to `auto_policy.assess` at line 539, so none of these transient/structural problems can trigger `auto_exclude`.

`auto_exclude` (line 541-542) is reached only inside `if not ok:` after `assess` runs, and only `if reason == "PER_REQUEST_COST"`. Looking at `auto_policy.assess` (`auto_policy.py:61-91`), `PER_REQUEST_COST` (line 79-80) is checked after `DISABLED`, `DELEGATION_EXPIRED`, `RETROACTIVE_OR_FUTURE_REQUEST`, `REPOSITORY_OR_BRANCH`, `SCOPE`, `REVIEW_POLICY`, `REQUEST_FORMAT`, `INVALID_PIN_FORMAT` — all of which return a *different* reason string and would short-circuit before `PER_REQUEST_COST` is reached if any of them also apply. `assess` is a pure function that returns on the *first* failing check, so a request can only be excluded for the cap when it has already cleared every earlier (more fundamental) check. **This means a request cannot be excluded "while a different, still-fixable reason also applies" by this code path**, because `assess` returns only one reason and the earlier ones take priority. One subtlety: `UNSUPPORTED_DELEGATION_LIMIT` (line 81-82) is checked *after* `PER_REQUEST_COST`, so if `max_request_usd` is itself outside `[0.01, 100.00]`, a request whose cost exceeds the (invalid) cap will be excluded with `PER_REQUEST_COST` even though the delegation itself is also malformed. This is a MINOR ordering nit, not a correctness defect, since the delegation being out of range at all is an operator misconfiguration independent of this request.

### Q2 — Side effects of permanent exclusion (registry cost vs. cap ordering)

`estimated` is computed from `policy.run_budgets_usd.get(run_policy)` (line 499-500) — the *registered tier cost*, not anything from the request itself. So yes: if the tier's registered cost is raised (e.g. `POLICY-STATIC-V1` moved from $1 to $3 in the local reviewer policy config) *before* the delegation's `max_request_usd` is raised to match, any request that arrives in that window is evaluated against the old, lower cap, fails `PER_REQUEST_COST`, and is `auto_exclude`d — permanently, by design, per the v0.2.29 change. This is accurately documented in `docs/AUTO_APPROVAL.md:26-27` and `docs/BUDGET_POLICY_CONFIGURATION.md:22` ("excluded for good... can only be approved manually"). It is an intentional conservative fail-closed behavior (favors manual review over silent retroactive admission), which is acceptable for a `windows-single-user-watcher` profile, but it does create an operational footgun: **the operator must raise the registry cost and the delegation cap together**, or legitimate requests pile up needing manual approval. This is accurately documented, not a defect — I'd flag it as a MINOR operational note rather than a finding, since the docs already warn about it.

### Q3 — Concurrency and atomicity of `auto_exclude`

`auto_exclude` (`state_store.py:406-414`) is a bare `INSERT OR IGNORE`, not wrapped in `BEGIN IMMEDIATE` like `auto_claim` (`state_store.py:383-404`). However, `auto_claims` has `PRIMARY KEY (request_id, revision)` (`state_store.py:88-104`), and SQLite enforces primary-key uniqueness regardless of the explicit transaction wrapper — the `INSERT OR IGNORE` and the `INSERT` inside `auto_claim`'s `BEGIN IMMEDIATE`/`COMMIT` are both atomic single-statement operations against the same table in the same `sqlite3.Connection` (default `isolation_level=None` means each statement autocommits unless inside an explicit `BEGIN`). Since SQLite serializes writers (one writer at a time, `PRAGMA journal_mode=WAL`), whichever of `auto_claim`'s explicit transaction or `auto_exclude`'s single insert commits first will win the PK slot; the second will either be rejected (`auto_claim`'s `SELECT ... WHERE` check inside its `BEGIN IMMEDIATE` will see the row and return `"EXISTS"`) or silently ignored (`auto_exclude`'s `OR IGNORE`). So **no race can result in two rows, nor in overwriting a `CLAIMED`/`RESERVED` row with `POLICY_STOPPED`, nor vice versa** — whichever row is inserted first for a given (request, revision) stands, and the second writer's call is a no-op. This matches the intended "one row per request and revision, ever" invariant. It cannot admit a refused request nor hide an admitted one.

What it *can* do: if two processes race `_process` for the same request (e.g., after a restart with a stale process still running), one could reach `auto_claim` (admit) while the other reaches `auto_exclude` (exclude) for the same identity, and whichever SQLite write lands first wins — this is a true TOCTOU race only across process boundaries, not within one, since `AutoApprover._in_progress` (lines 413-416, 420-421) already guards against concurrent processing of the same `request_id` within one process. Given the single-watcher, single-user Windows deployment model, two watcher processes mutating the same DB file concurrently is already an unsupported configuration (the lock file / single-instance design elsewhere in the codebase presumably prevents it); I did not find evidence this is prevented *here* at the DB layer, but it is consistent with the stated single-process model.

`_resume` (lines 697-700) checks `claim["stage"]` and immediately returns `AutoResult(stage, claim.get("detail"))` for `POLICY_STOPPED` without further action — so once a `POLICY_STOPPED` row exists, `_resume` is a terminal no-op for it, matching intent.

### Q4 — Retroactive admission, residual paths

Closed by code in v0.2.29:
- **Seen while disabled**: `auto_note_seen` (`state_store.py:300-310`) is `INSERT OR IGNORE`, write-once; `_process` line 456-458 returns `PRE_EXISTING_REQUEST` permanently if `seen_enabled` was `False` at first sight. Closed.
- **Cap refusal**: now closed by `auto_exclude` + `_resume`'s terminal handling of `POLICY_STOPPED`, as described above. This is the new fix in this release.
- **`enabled_at` comparison** (retroactive start by request creation time): `_process` line 546-549 still checks `created_at < delegation.earliest_request_at or seen_at < delegation.earliest_request_at` → `RETROACTIVE_OR_FUTURE_REQUEST`. This is a per-request check evaluated every time (not persisted exclusion), so it remains correctly enforced each run as long as `earliest_request_at` doesn't change — but it is *not* excluded permanently in a stored row the way `PER_REQUEST_COST` now is; if `earliest_request_at` is itself lowered later (operator edits `enabled_at` backward), a previously-retroactive request could pass this check on a later run. That is a residual operator-dependent path, same as before v0.2.29 — not newly introduced, not fixed by this diff, and not claimed to be fixed by the docs.
- **Finished or uncertain history** (`UNCERTAIN`, `READY_POSTED`): `_resume` line 699 treats both as terminal, unchanged from v0.2.28.

Still depends on the operator: raising `max_request_usd` without raising the tier's registered cost in sync (Q2); lowering `enabled_at`/`earliest_request_at` retroactively; and the explicit manual-approval step for any `POLICY_STOPPED` row (by design, since `tools/approve_request.py` is outside this package).

### Q5 — Telemetry integrity

`_auto_usage_locked` (`state_store.py:323-371`) now filters `auto_claims` to `reserved_cents > 0` (line 329), so `POLICY_STOPPED` rows (`reserved_cents=0`) are excluded from `window_rows` and thus from `day_calls`/`day_cents`/`month_cents`. This is confirmed directly by `test_c_a_cost_refused_request_is_not_counted_as_a_call_in_the_usage_telemetry` in `tests/test_v029_cost_refused_exclusion.py:38-43` (I read this test; I did not execute it). I checked the other consumers of `auto_claims`/`window_usage`: `auto_claim`'s own duplicate check uses `SELECT 1 FROM auto_claims WHERE request_id=? AND revision=?` (no `reserved_cents` filter, line 385) so a `POLICY_STOPPED` row still correctly blocks a second `auto_claim` insert for the same identity (returns `EXISTS`), which is exactly the intended behavior — a zero-cent row still participates correctly in **existence/duplicate** checks, it's only excluded from **usage/cost aggregation**. `auto_get_claim` (line 312-321) returns the row regardless of `reserved_cents`, used by `_resume`/`_process` for stage dispatch — unaffected by the filter. I found no consumer that would be broken by a zero-cent row; the filter is scoped correctly to the one function (`window_usage`) it needs to affect, since day/month counts are "telemetry, not admissibility gates" per `auto_policy.py:89-90` — this matches the comment and intent.

### Q6 — Five windows and restart, double-signing

`_process` only reaches `auto_claim` reservation once per (request, revision) due to the PK; after that, every re-entry (restart, later cycle) goes through `claim = store.auto_get_claim(...)` → `_resume` (line 460-462). `_resume`:
- `RESERVED` with no remote files and `attempts < 2` → signs once, bumps `attempts` first (line 710) *before* signing — so a crash between bump and successful sign still caps at `attempts>=2` on the next retry (line 708), preventing unbounded retries, though it technically allows exactly 2 sign attempts if the first attempt's signature silently failed without publishing anything remotely. Both attempts still only publish `APPROVAL_SIG.json`/`READY.md` via `_post_create_only`, which is create-only and read-back-verified (lines 673-675, 689-691) — so even a double local `sign()` call cannot result in two different published signatures: the first `_post_create_only` that successfully creates the remote file wins, and a second publish attempt for the same path would see `EXISTS_SAME` (same bytes, since `_revalidate` + `_ready_for` deterministically reconstruct identical bytes from the stored candidate) and proceed, or `EXISTS_DIFFERENT` → treated as an error/uncertain path (implicit in `res not in ("POSTED","EXISTS_SAME")` at lines 674, 690). So two *different* valid signatures cannot both be published for the same (request, revision). I did not find a path that signs twice with different payloads.
- `SIGNED_LOCAL`/`APPROVAL_POSTED` → re-publish from stored bytes only (no re-sign), lines 724-732, expiry-checked.
- `READY_POSTED`/`UNCERTAIN`/`POLICY_STOPPED` → immediate terminal return (line 699-700), no action across any number of further windows or restarts.

This matches the "exactly one APPROVAL_SIG and one READY per (request, revision)" invariant from the code as read. I did not execute the five-window test; the developer's self-test claim of "5 model-stub calls, none after restart" is consistent with this code structure but I verified it by static reading only, not execution.

### Q7 — `su_l1` classification

Confirmed by `Grep` of `skill_collab_watcher/`: **no file in the watcher runtime package imports or references `su_l1`**. `su_l1/README.md:1,10` states explicitly "feature OFF, NOT wired into the watcher... not enabled by any setting of the watcher in this version." This is corroborated by the module design: `su_l1/local_only_contract_r0003.py` uses its "OWN private SQLite pair; never opens the watcher DB" (README line 6).

Classification: **test-only availability issue**, not a runtime availability issue and not a safety defect reachable from the watcher's LIVE code path, because:
1. The watcher process never calls into `su_l1` code, so the flaky test cannot affect a LIVE install of v0.2.29 as-is.
2. The failure mechanism described (unlocked `_verify()` reader racing `os.replace` on Windows, caught and converted to `ContractError("ANCHOR_UNREADABLE_FAIL_CLOSED")`) is itself a fail-closed outcome, not silent corruption — the developer's own reproduction (10/10 trials with injected `ANCHOR_UNREADABLE`) shows invariants hold (no double-accept, no lost nonce, no orphan temp file). I did not execute this myself; I'm relying on the developer's stated reproduction as context, consistent with the code's fail-closed design in `_read_anchor` (`local_only_contract_r0003.py:91-99`) and `_verify` (line 173-199) which only raises `ContractError` subclasses on any read/parse failure, never silently proceeds.

Should it block a LIVE install of v0.2.29? **No**, given `su_l1` is dormant and unreachable from the watcher runtime, this flaky test is irrelevant to whether these bytes are safe to install as the watcher. It *should* block `su_l1` itself from ever being wired in/enabled until the root cause of the `PermissionError` race is captured and understood (currently "UNRESOLVED," per the self-test note) — I'd require capturing the raw exception of a failing run before `su_l1` moves beyond "feature OFF," but that is a separate, future decision from this REQUEST's scope.

### Q8 — Carry-over from v0.2.28 review

The REQUEST states the v0.2.28 review found MAJOR 1 (retroactive admission via `PER_REQUEST_COST`, fixed per Q1-Q4 above) and MINOR 2 (unspecified in text given to me). I don't have the v0.2.28 review document itself (not in this package or pinned knowledge), so I can only confirm what's inferable from the diff and docs read:
- `docs/AUTO_APPROVAL.md` was updated to remove stale day/month ceiling language and accurately describe cap-raise/exclusion behavior (lines 24-27, 59-60) — reads internally consistent with the code (`auto_policy.py` has no day/month admission gates, matching line 89-90 comment "Day/month counts and costs are telemetry, NOT admissibility gates").
- `docs/BUDGET_POLICY_CONFIGURATION.md` now states `tools/approve_request.py is a host-side manual approval script and is not part of this package` (line 23), matching the manifest/REQUEST's own statement.
- I cannot independently confirm these are *the exact two* MINOR findings from v0.2.28 since that review's text wasn't provided to me — **this item is NOT_RUN** (I cannot verify against a document I never saw). What I *can* say: nothing I read in `docs/AUTO_APPROVAL.md` or `docs/BUDGET_POLICY_CONFIGURATION.md` is inaccurate relative to the current code (`auto_policy.py`, `auto_approval.py`, `state_store.py`).

### Q9 — Release label / traceability

`docs/CUTOVER_RUNBOOK.md` title still says `development_not_for_deployment` (confirmed by diff header, only version bumped 0.2.28→0.2.29). For a LIVE install of exactly these bytes to be traceable, outside the ZIP you (GPT/operator) need to record at minimum: the exact SHA-256 (`c67bc342fe77547b000fc42e1b886396cbef035c0d265dbcd124947e267ed83f`) and size (310753 bytes) being installed, the install/cutover date, an explicit operator decision overriding the `development_not_for_deployment` label (since nothing in the package itself flips that label), the prior installed version/SHA being replaced (v0.2.25 per the REQUEST), and confirmation that `tools/approve_request.py` (host-side, outside this ZIP) and the delegation file's `max_request_usd`/registry tier costs are reconciled per Q2 before enabling `auto_approval`. This record should live in whatever install/runbook log GPT maintains outside this package — not something this static review can create itself.

---

## Findings

**BLOCKING: none.**

**MAJOR: none.** The v0.2.28 MAJOR (retroactive admission via unrefreshed `enabled_at` after a cap raise) is fixed as designed and verified by static reading of `auto_approval.py:541-542`, `state_store.py:406-414`, and the schema PK at `state_store.py:103`.

**MINOR:**
1. **`auto_policy.py:79-82` — check-order nit.** `PER_REQUEST_COST` is evaluated before `UNSUPPORTED_DELEGATION_LIMIT`. If `max_request_usd` is itself out of the supported range, a request exceeding it is permanently excluded (`POLICY_STOPPED`) rather than surfaced as a delegation-configuration problem. *Fix:* swap the order of these two checks, or leave as-is since it's cosmetic (both are non-admitting outcomes) — I'd leave it, flagging for awareness only. *Verify:* unit test asserting reason order when both conditions hold.
2. **`docs/AUTO_APPROVAL.md` / `docs/BUDGET_POLICY_CONFIGURATION.md` — operational footgun, already documented.** Raising a tier's registered cost before the delegation cap permanently excludes in-between requests (Q2). Already documented accurately; no doc fix needed, but worth operator runbook emphasis (Q9) to always raise both together.
3. **Q8 not independently verifiable** — the two v0.2.28 MINOR findings' exact text wasn't available to me in this session; I can only confirm the docs I read are internally consistent with the code, not that they match the prior review's specific wording.

---

### Files read directly
`docs/AUTO_APPROVAL.md`, `docs/BUDGET_POLICY_CONFIGURATION.md`, `skill_collab_watcher/auto_approval.py` (full), `skill_collab_watcher/auto_policy.py` (full), `skill_collab_watcher/state_store.py` (schema + auto_* functions), `tests/test_v029_cost_refused_exclusion.py` (full, read not executed), `su_l1/README.md`, `su_l1/local_only_contract_r0003.py` (anchor/verify/mutate sections). Grepped (not fully read): `skill_collab_watcher/` for `su_l1` imports (none found); `auto_approval.py` for structural markers.

### Knowledge files read
None pinned in this REQUEST ("(none pinned)").

### Consumer profiles judged against
`windows-single-user-watcher`, as specified.

### Left unverified
- Did not execute any code, tests, or the watcher (per STATIC_ONLY boundary). All "PASS" statements above describing developer self-tests are reported as claims, not my own executed results.
- `docs/CUTOVER_RUNBOOK.md` full body (only diff hunk + title confirmed) and `docs/RELEASE_MANIFEST.json`, `README.md`, and the remaining unchanged `.py` modules (`cli.py`, `orchestrator.py`, `validator.py`, `approval_signer.py`, etc.) were not read — the REQUEST states only 6 files + 1 new test changed, and I scoped reading to the diff plus call sites.
- The exact text of the v0.2.28 review's two MINOR findings (Q8) — not provided in this session, so I could not do an item-by-item carry-over check.
- `su_l1`'s flaky-test root cause remains genuinely unresolved per the developer's own note; I classified its risk but did not reproduce it.
- Linux, in-house-LLM, and MCP behavior: out of scope for this Windows static read, per instructions.

### Proposed corrections to common knowledge (GPT decides)
- Consider recording, as durable knowledge, the exact traceability fields needed for a LIVE install of a labeled-`development_not_for_deployment` ZIP (Q9 list above), so future reviews don't need to re-derive this checklist.
- Consider pinning the text of each prior review's findings (not just BLOCKING/MAJOR/MINOR counts) into the REQUEST or knowledge files, so Q8-style carry-over checks can be verified rather than left NOT_RUN.
