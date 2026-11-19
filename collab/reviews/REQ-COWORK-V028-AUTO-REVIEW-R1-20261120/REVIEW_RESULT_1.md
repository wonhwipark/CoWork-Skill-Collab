---
schema: SKILL_COLLAB_REVIEW_RESULT_V1
review_id: "REQ-COWORK-V028-AUTO-REVIEW-R1-20261120|1|9e6ee6d30170f0a2890237c7d1b9184e5c423213a18146926b848c5269b8c00c|1"
responds_to_request_id: "REQ-COWORK-V028-AUTO-REVIEW-R1-20261120"
responds_to_request_revision: "1"
package_sha256: "9e6ee6d30170f0a2890237c7d1b9184e5c423213a18146926b848c5269b8c00c"
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

## CoWork Watcher v0.2.28 — Independent Static Review R1

**Scope read:** `skill_collab_watcher/auto_policy.py` (full), `auto_approval.py` (full), `config.py` (partial, delegation/run-policy sections), `state_store.py` (claims/lease/auto_claims sections), `approval.py` (full), `github_transport.py` (grep + key sections), `tools/review_request_gate.py`, `tools/source_pin.py`, `tools/approval_signer.py` (grep), `docs/CUTOVER_RUNBOOK.md`, `docs/BUDGET_POLICY_CONFIGURATION.md`, `docs/AUTO_APPROVAL.md`, `tests/test_auto_approval.py`, `tests/test_v022_findings.py` (relevant sections), `__SKILL_COLLAB_CONTEXT__/FILE_INDEX.txt`. No pinned knowledge files existed for this REQUEST (none listed). No code was executed — static read only.

---

### BLOCKING / MAJOR findings

**1. MAJOR — Retroactive admission on a per-request cap raise is possible unless the operator manually bumps `enabled_at`; this is undocumented for the cap-raise case and untested.**

- **File/function:** `skill_collab_watcher/auto_approval.py::AutoApprover._process` (lines ~442–569), `auto_policy.py::assess`, `auto_approval.py::load_delegation`.
- **Failure condition:** A request seen while the delegation was `enabled=true` but rejected only by `PER_REQUEST_COST` (old `max_request_usd=1.0`, i.e. `assess()` returns `False, "PER_REQUEST_COST"`) never reaches `store.auto_claim(...)`. No claim row, no `auto_jobs_for` entry is written, so `_prior_state` keeps returning `"NEW"` on every poll forever. When the operator later raises `max_request_usd` to `3.0` **without also bumping `enabled_at`**, the next poll cycle re-runs `assess()` fresh with the new cap, the request now passes `PER_REQUEST_COST`, and — if nothing else changed — it is admitted, claimed, signed and published automatically. This is exactly the scenario Q2 of the REQUEST warns against.
- **Evidence:** `auto_policy.py:79` (`PER_REQUEST_COST` gate), `auto_approval.py:456-458` (only the boolean `enabled` flag is sticky via `auto_note_seen`/`seen_enabled`; there is no equivalent sticky record of the cap value seen at first sight), `auto_approval.py:545` (`created_at < delegation.earliest_request_at or seen_at < delegation.earliest_request_at` — the only retroactivity guard, keyed to `earliest_request_at = enabled_at`, not to the cap). `tests/test_v022_findings.py` and `tests/test_auto_approval.py` `test_B2_a_narrowed_delegation_stops_the_request_at_every_boundary` only cover *lowering* the cap **after a claim already exists**; there is no test for *raising* the cap for a request that was rejected **before** ever being claimed.
- **Mitigating factor (code does provide a close path):** `first_seen_at` in `auto_seen` is write-once and immutable (`INSERT OR IGNORE`). If the operator sets `enabled_at` to "now" at the moment of raising the cap, the previously-seen request's `seen_at < delegation.earliest_request_at` becomes true and it is permanently blocked (`RETROACTIVE_OR_FUTURE_REQUEST`). This is the same mechanism `docs/AUTO_APPROVAL.md`'s "Enabling procedure" describes — but only for the *initial* enable, not for a later cap increase.
- **Proposed fix:** (a) Add an explicit step to `docs/CUTOVER_RUNBOOK.md`/`BUDGET_POLICY_CONFIGURATION.md`: "every time `max_request_usd` is raised, `enabled_at` must also be set to the current time," and (b) add a regression test: seed a pending request that is cost-rejected under the old cap, raise `max_request_usd` without touching `enabled_at`, assert it becomes `READY_POSTED` (documents the current gap) and a second test asserting that bumping `enabled_at` at the same time blocks it permanently.
- **Verification:** Add/run the two tests above; confirm the runbook is updated. (Review-only; not executed here.)

**2. MINOR (inventory/documentation) — `tools/approve_request.py` is referenced by the REQUEST manifest and by `docs/BUDGET_POLICY_CONFIGURATION.md` as the manual-approval path for DESIGN/LARGE tiers, but no such file exists in the 113-member package.**

- **Evidence:** `__SKILL_COLLAB_CONTEXT__/FILE_INDEX.txt` lists `tools/__init__.py`, `tools/approval_signer.py`, `tools/build_release.py`, `tools/review_request_gate.py`, `tools/source_pin.py`, `tools/trust_root_tool.py` — no `approve_request.py`. `docs/BUDGET_POLICY_CONFIGURATION.md:5` says DESIGN/LARGE "exist only for manual approval (`approve_request.py`)". `tools/review_request_gate.py:6` only says "the host `approve_request` check is separate" (i.e., it may be an external/host-side check, not a shipped file).
- **Impact:** Not a security hole (DESIGN/LARGE are refused unconditionally by the automatic engine regardless), but the REQUEST's own manifest text ("The ZIP contains... the tools..., including `review_request_gate.py`, `source_pin.py`, `approve_request.py`") is factually wrong about this ZIP's contents — worth correcting before any disposition that assumes a manual-approval tool ships in this package.
- **Fix/verification:** GPT should confirm whether `approve_request.py` is a separate host-side script outside this ZIP (as `review_request_gate.py`'s docstring implies) and correct the manifest/docs accordingly, or add the file if it was meant to ship.

**3. MINOR (documentation drift) — `docs/AUTO_APPROVAL.md` was not touched by v0.2.27/v0.2.28 and still describes the abolished day/month ceilings.**

- **Evidence:** `docs/AUTO_APPROVAL.md:25` ("day <= 2 calls / $3, month <= $10") and the "Configuration" example at line 50 (`max_day_calls`, `max_day_usd`, `max_month_usd`) contradict the actual current behavior confirmed in code and in `BUDGET_POLICY_CONFIGURATION.md:32` ("Legacy ... keys are accepted but ignored"). This is misleading to an operator reading only `AUTO_APPROVAL.md`.
- **Fix:** Update `AUTO_APPROVAL.md` to match `BUDGET_POLICY_CONFIGURATION.md`'s current statement that only the per-request cap and one-shot identity are enforced.

---

### Answers to the review questions

**Q1 — fail-closed for every other tier name: PASS.** `auto_policy.py::assess` line 73: `c.policy != "POLICY-STATIC-V1"` is a strict Python string equality check. `POLICY-STATIC-V1-LARGE`, `POLICY-STATIC-V1-DESIGN`, unknown strings, empty string, case variants, leading/trailing whitespace, and Unicode look-alike characters are all != the exact ASCII literal, so all fail closed to `"REVIEW_POLICY"`. Confirmed in tests `test_only_the_unified_static_tier_is_signed_design_is_always_refused` and `test_design_tier_is_refused_even_with_full_delegation_headroom` (reported PASS by the package, not independently executed by me).

**Q2 — Retroactive admission: see MAJOR finding #1 above.** Paths closed by code: (a) a request first seen while `enabled=false` is permanently excluded (`seen_enabled` sticky flag, `auto_approval.py:456-458`); (b) once a claim exists, `_policy_stop`/`_revalidate` make a `POLICY_STOPPED` or `READY_POSTED`/`UNCERTAIN` stage terminal — no resume, confirmed by `test_B2_a_stopped_request_is_never_resumed_automatically_even_after_the_owner_widens_again`; (c) `auto_claims` PRIMARY KEY `(request_id, revision)` + `job_claims`/`BEGIN IMMEDIATE` give one-shot identity, no double-dispatch. Path **not** closed by code alone, and dependent on the operator: a request rejected purely on `PER_REQUEST_COST` **before any claim exists** will be silently re-admitted on a later poll if the cap is raised, unless the operator also advances `enabled_at` to the current time at the moment of the raise.

**Q3 — Legacy `max_day_*`/`max_month_*` keys: PASS, confirmed inert.** `load_delegation` (`auto_approval.py:230-231`) hardcodes `max_day_calls=0, max_day_cents=0, max_month_cents=0` regardless of the JSON values (old day/month keys ignored). `auto_claim()` (`state_store.py:376-404`) accepts these as keyword parameters but never references them in its body — confirmed by direct read, no crash path, no enforcement. `Config.load` similarly hardcodes `daily_budget_usd=None, max_dispatches_per_day=None` (`config.py:219-220`), and `StateStore.claim()` comments "Legacy max_dispatches/daily_budget_usd are inert" (`state_store.py:281`) with no use of those parameters in the SQL. The per-request cap is enforced against the registered tier cost **at signing time** (`_sign_and_post` → `_revalidate` → `assess()` before the `signer.sign()` call) **and again before READY is published** (`_publish`, two further `_revalidate()` calls, one before posting `APPROVAL_SIG.json` and one before posting `READY.md`) — confirmed by reading `auto_approval.py:644-693`.

**Q4 — Rewritten tests: intent preserved, no hidden regression found in the diff.** The six rewritten assertions in `test_auto_approval.py`/`test_v022_findings.py`/`test_r1_findings.py` all track the documented, intentional removal of aggregate day/month ceilings (v0.2.27) — e.g. `calls==1`→`calls==2`, `!= READY_POSTED`→`== READY_POSTED` for cases that previously hit the now-abolished day/month gates, each with an inline comment explaining the policy change. The `test_review_request_gate_tool_v026.py` `write_text`→`write_bytes` changes are a mechanical Windows CRLF fix, not a logic change. None of the rewrites touch the per-request cap (`max_request_usd`) assertions or the one-shot identity assertions, which remain unchanged and still enforce the protections that matter for the $1→$3 raise. I found no test weakened in a way unrelated to the documented behavior change.

**Q5 — Trust boundary: claims match code (as far as statically verifiable).** `approval.py::verify_approval` enforces trust-root presence, `frozen` kill switch, key status (`ACTIVE` only), purpose, signature verification, repo-id match (both payload and `SOURCE_PIN`), nonce length, timezone-aware timestamps, `max_approval_lifetime_sec` bound, `not_before/not_after`, clock skew, and expiry — all fail-closed (`NotConfigured`/`ApprovalRejected` raised, never a partial pass). `validate_source_pin`/`source_pin.py::verify_source_pin` both reject a non-string `repo_id` (`type(repo_id) is not str`). `github_transport.py::upload` is add-only, checks `get_metadata` first and raises `UploadConflict` on 409/422 (create-only). `_post_create_only` in `auto_approval.py` reads back after a conflict or transport error to recover from an uncertain send, and `_publish` posts `APPROVAL_SIG.json` before `READY.md`, reading back the approval before posting READY (lines 662-692). `state_store.py` uses `BEGIN IMMEDIATE` for `auto_claim`, `try_claim`/`claim`, `check_provider`, and `seal_interrupted`; `check_provider` enforces a single active provider via `provider_lease`. All consistent with `docs/CUTOVER_RUNBOOK.md`'s claims. I did not execute any signature/HTTP code, so this is a structural/static confirmation only, not a runtime PASS.

**Q6 — Tools: no sign/READY/model/host-config path outside the protected engine.** `tools/review_request_gate.py` docstring and code explicitly state no GitHub writes, no approval, no READY, no signing, no watcher/model calls, and that it is "NOT an authorization check." `tools/source_pin.py` is explicitly "Local/offline helper only: no GitHub writes, READY, signing, watcher, or LLM calls." `tools/approval_signer.py` signs locally to files on the approver's own device/session and is only ever invoked in-process by `auto_approval.ToolSigner` (which still goes through the full `_process`/`_revalidate`/`_publish` protected path before any GitHub write happens) — the grep found no network calls, no model calls, and the only `subprocess` use is a local `icacls` ACL-hardening call on the output key file. None of these three tools post READY or call GitHub on their own.

**Q7 — `development_not_for_deployment` label.** The label does not, by itself, block anything programmatically — it's a string in a doc, not a config gate — so it does not prevent an accidental LIVE install of these exact bytes. The operator must record, **outside the ZIP**, independently of this label: (1) that this specific SHA-256 was reviewed and the result accepted by GPT's final disposition, (2) the explicit delegation value change (`max_request_usd: 1.0 → 3.0`) and the paired `enabled_at` bump per finding #1, (3) that `POLICY-STATIC-V1-DESIGN`/`-LARGE` remain intentionally excluded from automatic signing, and (4) the install/cutover date and who approved it. The label is a developer note, not a safety control — the actual safety controls (`enabled`, ACL check, trust root, delegation scope) are in the config/data files, not in this string.

---

### PASS / FAIL / NOT_RUN summary

| Item | Result |
|---|---|
| Q1 fail-closed tier admission | PASS (static) |
| Q2 retroactive admission closed by code alone | **FAIL** (operator-dependent; see finding #1) |
| Q3 legacy keys inert / per-request cap enforced at sign+publish | PASS (static) |
| Q4 rewritten tests preserve intent | PASS (static review of diff) |
| Q5 trust boundary (signing, create-only, BEGIN IMMEDIATE, lease, recovery) | PASS (static) |
| Q6 tools cannot sign/post/model outside protected path | PASS (static), but see finding #2 (file inventory mismatch) |
| Q7 dev label alone does not block install | Answered — operator action required, not a code PASS/FAIL |
| Any Windows runtime behavior (watch loop, ACL checks, actual signing) | NOT_RUN — static read only, per boundary instructions |

---

### What I left unverified
- Nothing was executed: no tests run, no watcher started, no signing performed. Windows ACL/DACL code (`approval.py`, `auto_approval.py`), DPAPI passphrase handling, and the actual GitHub HTTP exchange were read but not exercised.
- `su_l1/*` module was not read (out of scope for this REQUEST's questions).
- I did not open the full `state_store.py` (34KB) or `auto_approval.py` beyond the sections cited; sections not read (e.g. the `jobs` table schema, `watch_loop.py`, `cli.py`) were not reviewed.
- I did not verify that `tools/approve_request.py` genuinely doesn't exist anywhere else in the repo outside this ZIP (I only confirmed its absence from this package's 113-member index).
- Linux/in-house-LLM/MCP behavior: not applicable to this static Windows-only package; not verified.

### Proposed corrections to common knowledge (GPT to decide)
1. Record in the knowledge base that **raising `max_request_usd` on an active delegation must always be paired with bumping `enabled_at` to the current time**, or the raise can retroactively admit previously cost-rejected pending requests (finding #1). This should become a standing precondition for any future cap increase on this watcher, not just this $1→$3 change.
2. Correct the record of this package's tool inventory: `tools/approve_request.py` is **not** part of the v0.2.28 ZIP; the manual approval path for DESIGN/LARGE tiers is either a host-side process outside the ZIP or missing from the build (finding #2) — needs clarification from the skill owner.
3. Note that `docs/AUTO_APPROVAL.md` is stale relative to v0.2.27/28 behavior (finding #3) and should be corrected alongside, or ahead of, any future release.
