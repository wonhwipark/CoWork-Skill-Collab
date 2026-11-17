---
schema: SKILL_COLLAB_REVIEW_RESULT_V1
review_id: "REQ-COWORK-BUDGET-V025-LARGE-R2-20261117|1|26d63c8a03290499b13b2ceb8ff0b70c06eb1b1bcc1a25fe3d8f65fcc213d228|1"
responds_to_request_id: "REQ-COWORK-BUDGET-V025-LARGE-R2-20261117"
responds_to_request_revision: "1"
package_sha256: "26d63c8a03290499b13b2ceb8ff0b70c06eb1b1bcc1a25fe3d8f65fcc213d228"
skill_id: "cowork-review-watcher"
run_policy_ref: "POLICY-STATIC-V1-LARGE"
knowledge_refs: []
consumer_profiles: ["windows-single-user-watcher"]
reviewer_os: WINDOWS
review_scope: CODE_REVIEW
test_policy: "STATIC_ONLY"
execution_status: COMPLETED
limitations: ["static review by an automatically started Claude Code process; no package code was executed", "knowledge files were delivered as the REQUEST pinned them; which parts were actually read is reported by the reviewer in the text", "reviewer host is Windows; Linux, in-house LLM and MCP behaviour are not verified by this review"]
---

# 리뷰 결과

I have enough evidence to complete the review now.

---

# Independent Design/Security Review — REQ-COWORK-BUDGET-V025-LARGE-R2-20261117

**Scope:** static review of package `skill-collab-watcher_v0_2_25_1117.zip` (104 files) as provided in the snapshot directory. This review does not itself perform or verify the mandatory host preflight (`review_request_gate.py select/check`, `approve_request.py check`), signing, or dispatch — those are watcher/host-side, pre-review steps outside my tool access, and I only had read access to the package snapshot.

## BLOCKING

**None found.** The core budget-policy and trust-chain code I could read is internally consistent and fail-closed everywhere I checked (see below).

## MAJOR

### M1 — `review_request_gate.py` is not present in this package and I have no way to review it
- **File/function:** `collab/ops/review_request_gate.py`, `collab/ops/tests/test_review_request_gate.py`
- **Failure condition:** The REQUEST text explicitly asks me to "Inspect that gate independently as part of the same Windows session," and states it is "not included in the v0.2.25 ZIP." It is also absent from `__SKILL_COLLAB_CONTEXT__/FILE_INDEX.txt` (104 files, all accounted for above — no `ops/` directory at all) and my tool access is restricted to the snapshot directory.
- **Evidence:** `FILE_INDEX.txt` lists only `config/`, `docs/`, `prompts/`, `skill_collab_watcher/`, `su_l1/`, `tests/`, `tools/`, `windows/`. No `collab/ops/review_request_gate.py` anywhere.
- **Impact:** I cannot verify the gate's claimed behavior ("catch wrong tier and stale installed-policy reports," `POLICY_COMPATIBLE_NOT_APPROVED`, `PASS_PREPUBLICATION_ONLY`, SOURCE_PIN repo_id string checks) at all. The CI #44093146832 PASS cited in the REQUEST is developer-reported evidence only, not something I executed or read.
- **Proposed fix:** none — this is a scope gap, not a code defect. GPT/the orchestrating process should either include the gate file in a reviewable location for the Windows reviewer, or treat this item as explicitly NOT_RUN in the disposition and rely on the host's own preflight execution (not this review) as the control.
- **How to verify:** confirm whether `review_request_gate.py` exists in the private repo at the pinned commit, and if a future review of it is wanted, provide it inside the reviewed package/snapshot or an explicitly pinned knowledge file.

## MINOR / observations (not blocking)

### N1 — Legacy list-form `known_run_policy_refs` silently falls back to the default budget per-tier, not per-request
- **File/function:** `skill_collab_watcher/config.py:ReviewPolicy.budget_for`, used by `cli.py:119-134` to build `LocalPolicy.run_budgets_usd`.
- **Observation:** If an operator still configures `known_run_policy_refs` as a bare list (no `{"max_budget_usd": …}` object), `run_budgets_usd` ends up mapping *every* ref — including a hypothetical `POLICY-STATIC-V1-LARGE`/`-DESIGN` name — to the single `max_budget_usd` default, because `budget_for()` falls back rather than erroring. This is intentional and tested (`test_legacy_list_form_uses_default_budget`), and it fails *safe* (under-provisions, never over-provisions a named tier above the default), so it is not a security issue — just worth flagging because it means a config that lists a design-tier name in the legacy list form will quietly cap it at the basic budget instead of refusing to start, which could be an unpleasant surprise to an operator expecting $3.00 but getting $1.50/$1.00. Confirmed by reading `config.py:86-113`, `cli.py:119-134`.
- **Fix suggestion (optional):** could make `_parse_run_policy_refs` reject list form when a design/large-looking name is present, but given tests explicitly codify the current behavior as desired, I'd leave this to GPT's judgment rather than propose a change.

### N2 — Day/month ceiling removal is consistent across all three places I checked
`auto_policy.assess()` (`auto_policy.py:89`), `Config.load()` (`config.py:219-220`, forces `daily_budget_usd`/`max_dispatches_per_day` to `None` regardless of input), and `StateStore.auto_claim()`/`_auto_usage_locked()` (`state_store.py:323-404`, comments explicitly say "Aggregate quotas removed" / "No day/month cumulative quota") all agree: day/month counters are still computed and exposed as telemetry (`window_usage`), but never gate admission. This matches the v0.2.24 "development cost-only admission" note in `docs/AUTO_APPROVAL.md:68-71`. I did not find a code path where a stale `max_day_calls`/`max_day_cents` value from a delegation file could still silently block or silently widen admission — `load_delegation()` in `auto_approval.py:231-233` hard-zeros those fields on load.

### N3 — NaN/Infinity handling in budget config is correct
`config.py:_parse_run_policy_refs` (line 108) and `_check_budget`/`_optional_cap` all use `math.isfinite(amount)` and reject non-finite or non-positive values with `ConfigError`, matching `test_review_budget_policy_v025.py::test_configurable_tier_budgets_are_locally_registered` which exercises `float("inf")`. I did not find an equivalent check missing for booleans-as-ints (`isinstance(amount, bool)` is explicitly excluded first), so `true`/`false` can't be coerced into a budget number.

### N4 — Auto-approval delegation is correctly restricted to the basic tier only
`auto_approval.py:225-226`: `load_delegation()` rejects any `policy` value other than the literal string `"POLICY-STATIC-V1"`. This means the unattended auto-signing path (v0.2.21+) can never auto-sign a `POLICY-STATIC-V1-LARGE` or `POLICY-STATIC-V1-DESIGN` request — those require the manual `approve_request.py`/`tools/approval_signer.py` path, consistent with the REQUEST's requirement that "existing protected delegation JSON must explicitly permit USD 3.00" via the *manual* signing authority, and that the candidate's own design policy must not be used for its own review. This is a real, verified fail-closed boundary, not just a documentation claim.

### N5 — Trust/approval chain (`approval.py`) looks sound for the properties asked about
Verified by reading, not executing: Ed25519 key lookup requires `ACTIVE` status and correct `purpose`; `TRUST_ROOT_FROZEN` is checked before any key logic; approval lifetime is bounded by `trust.max_approval_lifetime_sec` (60s–7 days); `repo_id` is checked on both payload and pin against the trust root; `source_commit` in the payload must equal the pin's `commit`; nonce must be ≥16 chars; clock skew is bounded at 5 minutes and fails closed (`ClockUntrusted`) if the provider's time is unavailable. I did not find a path where a `RETIRED`/`REVOKED` key, an expired approval, or a repo_id mismatch would pass `verify_approval`.

### N6 — `validator.py` fail-closes on unregistered `run_policy_ref`
`validator.py:207-208`: `if str(req["run_policy_ref"]) not in policy.known_run_policy_refs: return _reject(...)`. Combined with `orchestrator.py:740-742` which only ever dispatches using `policy.run_budgets_usd.get(run_policy_ref)` for a ref that already passed this check, I did not find a path where an unregistered or attacker-named tier (e.g. `POLICY-STATIC-V1-HUGE`) reaches the runner — this matches `test_v014_budget_tiers.py::test_request_cannot_name_an_amount_or_an_unregistered_tier`, which I read but did not execute myself.

## What I verified by reading vs. what is only claimed
- **Read and verified directly (Windows static review):** `auto_policy.py`, `config.py`/`validator.py` budget parsing, `state_store.py` atomic-claim/BEGIN IMMEDIATE path, `approval.py` Ed25519/trust-root verification logic, `auto_approval.py` delegation-scope restriction to `POLICY-STATIC-V1`, `zip_safety.py` zip-bomb/path-escape/symlink guards, `orchestrator.py`'s dispatch-budget wiring, `docs/BUDGET_POLICY_CONFIGURATION.md`, `docs/AUTO_APPROVAL.md`.
- **Claimed only, not verified by me:** CI run #44011874422 (29 PASS/2 SKIP + 582 PASS/30 SKIP/1 deselected on Linux) and CI run #44093146832 for `review_request_gate.py` — these are reports in the REQUEST text, not test runs I executed. I ran no tests and no Claude model call myself (none was authorized or appropriate for a static code review).
- **Not accessible to me at all:** `review_request_gate.py` and its test file (M1, above) — absent from the package snapshot and the file index.
- **Windows-only scope:** I did not attempt to assess Linux-specific regression behavior, in-house LLM behavior, or MCP behavior; "Windows reading does not verify Linux... behaviour" per the task framing.
- **Not performed by me (by design of this task):** the mandatory host preflight (`review_request_gate.py select/check`), `approve_request.py check/approve`, signing, dispatch, or any live GitHub byte read-back. Those are watcher/host-side actions that happen (or fail closed) outside this static code review.

## Consumer profiles judged against
`windows-single-user-watcher` — all Windows-specific trust mechanisms reviewed (ACL/DACL checks in `approval.py`, DPAPI passphrase unwrap in `auto_approval.py`) are consistent with a single local Windows account running the watcher process.

## Knowledge files actually read
None — "(none pinned in this REQUEST)" as stated; I read only package files and the file index inside the snapshot.

## Proposed corrections to common knowledge (GPT to decide)
1. Record that `review_request_gate.py` (and its test) should either be included in future review packages/snapshots for the Windows reviewer, or the REQUEST template should explicitly mark that gate's inspection as a host-only, non-reviewable step rather than asking the Windows Claude reviewer to inspect a file it has no access to.
2. Consider having future REQUESTs state explicitly, for each named tier (`POLICY-STATIC-V1-LARGE`, `-DESIGN`, etc.), whether the auto-approval delegation is expected to ever cover it — the current code already fail-closes this correctly (N4), but making it an explicit, checked assertion in the REQUEST template would make this property auditable without a full code read each time.
