---
schema: SKILL_COLLAB_REVIEW_RESULT_V1
review_id: "REQ-COWORK-REVIEW-ARCH-DESIGN-R1-20261122|1|c67bc342fe77547b000fc42e1b886396cbef035c0d265dbcd124947e267ed83f|1"
responds_to_request_id: "REQ-COWORK-REVIEW-ARCH-DESIGN-R1-20261122"
responds_to_request_revision: "1"
package_sha256: "c67bc342fe77547b000fc42e1b886396cbef035c0d265dbcd124947e267ed83f"
skill_id: "cowork-review-watcher"
run_policy_ref: "POLICY-STATIC-V1"
knowledge_refs: []
consumer_profiles: ["windows-single-user-watcher"]
reviewer_os: WINDOWS
review_scope: CODE_REVIEW
test_policy: "STATIC_ONLY"
execution_status: COMPLETED
limitations: ["static review by an automatically started Claude Code process; no package code was executed", "knowledge files were delivered as the REQUEST pinned them; which parts were actually read is reported by the reviewer in the text", "reviewer host is Windows; Linux, in-house LLM and MCP behaviour are not verified by this review"]
---

# 리뷰 결과

## Independent Static Review — CoWork Formal-Request Transport & Architecture Simplification

### 1. Recommended architecture (single recommendation)

**Adopt Option B (split publication from authorization), because the host watcher already treats GitHub-published artifacts as non-authoritative — the split does not weaken anything that currently protects the signer.**

Verified directly in the ZIP baseline (`skill_collab_watcher/`, v0.2.29):
- `skill_collab_watcher/validator.py` independently re-parses REQUEST front matter, re-checks `schema`, `package_sha256`/`size`, and `run_policy_ref` against the **host's own** `policy.known_run_policy_refs` (`validator.py:137-228`). It never imports or calls `review_request_gate.py`.
- `skill_collab_watcher/auto_approval.py` (`AutoApprover._process`, lines ~442-556) independently re-validates `SOURCE_PIN`, repo id, commit-pinned bytes, and delegation scope before ever reserving or signing. It never imports `review_request_gate.py` or `submit_review_request.py` either.
- Neither `review_request_gate.py` nor `submit_review_request.py` nor `review_pin_preflight.py` appears anywhere under `skill_collab_watcher/` (grep returned no matches). They are **GPT/operator-side convenience tools, not part of the trust boundary**.
- `docs/AUTO_APPROVAL.md:3`: *"A READY file alone never authorises a model call."* `docs/CUTOVER_RUNBOOK.md` §1: *"GPT / repository writers … Never hold: any ability to start a review: a commit alone is never an approval."*

Given this, letting GPT publish a syntactically valid REQUEST+PIN without reading Windows LIVE config **does not create a new auto-signing or paid-call admission path** — the real gates (delegation file ACL/enabled/enabled_at, SOURCE_PIN re-derivation from committed bytes, atomic reservation, Ed25519 signature, validator re-check) are unchanged and still run entirely host-side. The current design's requirement that GPT read a *local* `reviewer.config.json` before writing to GitHub is exactly the self-inflicted deadlock the REQUEST text describes, and it buys no additional security since the host revalidates everything anyway.

**Before/after:**
- **Before:** GPT must obtain/trust a local Windows config path → run `review_request_gate.check_request` → only then two-commit publish. If GPT cannot read Windows local files (it can't), "리뷰요청해줘" structurally cannot reach a real REQUEST.
- **After:** GPT performs purely self-contained checks (schema, exact SHA-256/length/CRC, immutable source revision, two-commit pin/readback, no history collision) and publishes Commit A + Commit B unconditionally advisory. Windows host (unchanged `validator.py` + `auto_approval.py`/manual signer) applies the actual installed policy, cap, scope, expiry, and signature, and silently/explicitly refuses anything that doesn't match — zero model calls, zero widened trust.

### 2. KEEP / SIMPLIFY / REMOVE / VERIFY_MORE

| # | Item | Verdict | Reason |
|---|------|---------|--------|
| 1 | Two Git commits A (REQUEST+ZIP) / B (SOURCE_PIN) | **SIMPLIFY** | Verified: nothing host-side requires a *separate* commit; `validator.py` doesn't read SOURCE_PIN at all, only `auto_approval.py`/manual signer do, and the signer's own `approval_signer.cmd_sign` already independently writes its own fresh `SOURCE_PIN.json` from an operator-supplied `--source-commit` (not from GPT's). A single commit containing REQUEST+ZIP+SOURCE_PIN (computed from the commit's own parent/predicted-hash problem aside) is not trivially safe since you can't self-reference your own commit hash — **keep two commits**, but drop the separate `review_pin_preflight.py`/`check_source_pin` duplication (see #2). |
| 2 | Multiple preflight helpers (`review_request_gate.py`, `review_pin_preflight.py`, `submit_review_request.py`, `review_staged_submission.py`) | **SIMPLIFY/REMOVE** | Confirmed drift: packaged `tools/review_request_gate.py` (ZIP, tested) has only `INTENTS = {"skill","design"}`; the embedded `collab/ops/review_request_gate.py` that `submit_review_request.py` actually imports has an added `"unified"` intent hardcoded to `Decimal('3.00')`. These two copies have **diverged** — the live submission path depends on logic that was never exercised by the packaged 11/11 unit tests. One canonical gate module should exist, imported (not duplicated) by both the packager and the submitter. |
| 3 | Staging Base64 ZIP + Markdown handoff under Work before REQUEST | **SIMPLIFY** | Only useful as a GPT-authoring convenience inside a Work folder before any Git identity exists; it's not needed once GPT can do the two-commit publish directly (Option B). Treat `review_staged_submission.py` as the one canonical "new-chat" entrypoint and retire ad hoc per-request staging variants. |
| 4 | Manual vs auto approval, allowlist, USD3 cap, `enabled_at` | **KEEP** | This is the one real trust boundary. `auto_approval.py` enforces ACL-protected delegation file, `enabled_at` non-retroactivity, per-request cost refusal permanence (`POLICY_STOPPED` never auto-admitted later even if cap raised) — all independent of anything GPT publishes. No change recommended. |
| 5 | Watcher/notifier separation, receipt writeback, UNCERTAIN recovery | **KEEP** | `orchestrator.py` and `auto_approval.py` already fail-closed to `REVIEW_UNCERTAIN`/`AUTO_SIGNING_UNCERTAIN` with no automatic retry (confirmed in `docs/AUTO_APPROVAL.md` "Stops" section and `orchestrator.py:742-804`). This correctly prevents duplicate model calls after a failure. |
| 6 | Overgrown CURRENT/history docs, stale PRIVATE vs PUBLIC refs, old DRAFT contract | **SIMPLIFY** | `docs/REQUEST_PIN_REPAIR.md` still says "PRIVATE 정본" while the request text states the repo is now PUBLIC — a live contradiction inside the shipped docs. Recommend one `STATUS.md`/entrypoint per subsystem with "superseded by" pointers instead of parallel dated documents; no new status ledger. |
| 7 | ChatGPT connector vs Windows host boundary | **VERIFY_MORE** | Confirmed GPT can write Git commits (its own code does exactly that) but has no path to read `reviewer.config.json`, the delegation file, or the signing key — all are Windows-local by design (`docs/CUTOVER_RUNBOOK.md` roles table). No code in this package gives GPT or any installed hook the ability to trigger watcher/auto-approval execution; that remains manual host action (`run_watch.cmd`) or scheduled Task, outside this package. |
| 8 | Public repo, unprotected main | **VERIFY_MORE** | `submit_review_request.require_clean_main` pins to a specific remote origin and checks local HEAD == remote HEAD before writing, which blocks local tampering, but nothing in this package verifies GitHub branch protection rules server-side — that is an operational GitHub setting outside static review scope. |

### 3. Findings

**Blocking**
- None found that would make Option B *less* safe than the status quo. (The status quo itself has an internal contract bug below, which is arguably blocking for anyone trying to use `submit_review_request.py --approval-route auto intent=unified` today.)

**Major**
- **F1 — Policy-budget contract mismatch for `intent='unified'`.** `collab/ops/review_request_gate.py:select_policy` requires `required_budget == Decimal('3.00')` for `unified`, and then requires the config's `known_run_policy_refs["POLICY-STATIC-V1"].max_budget_usd == 3.00`. But `config/reviewer.config.example.json:24` shows `POLICY-STATIC-V1: {"max_budget_usd": 1.0}` (and the $3 tier is a *separate* key `POLICY-STATIC-V1-LARGE`). As shipped, `submit_review_request.submit(..., intent='unified')` would raise `POLICY_COST_MISMATCH` against this example config. Evidence: `collab/ops/review_request_gate.py` (embedded, lines with `DEFAULT_BUDGETS = {"unified": "3.00", ...}` and `INTENTS["unified"] = ("POLICY-STATIC-V1",)`) vs `config/reviewer.config.example.json:24`. Fix: either rename the `unified` intent's target ref to `POLICY-STATIC-V1-LARGE`, or document that live config must set `POLICY-STATIC-V1.max_budget_usd = 3.0` before any `unified` publish; add a regression test pinning the example config's values. Verify: run `review_request_gate.py select --intent unified --live-config config/reviewer.config.example.json` and confirm it currently fails.
- **F2 — Packaged `tools/review_request_gate.py` (tested, in ZIP) and live `collab/ops/review_request_gate.py` (imported by the submitter) have diverged.** The packaged/tested copy has no `unified` intent at all. The 11/11 "PASS" unit tests referenced in the Work document never exercised the code path `submit_review_request.py` actually calls. Evidence: diff of `tools/review_request_gate.py` (`INTENTS = {"skill","design"}`) vs the embedded `collab/ops/review_request_gate.py` text in the REQUEST (`INTENTS` includes `"unified"`). Fix: single source of truth — either import `tools.review_request_gate` from `collab/ops/submit_review_request.py` (no separate ops copy), or add the `unified` intent to the packaged/tested module and re-run the regression suite against it. Verify: byte-diff the two files; they must be identical or explicitly versioned with a reconciling test.

**Minor**
- `docs/REQUEST_PIN_REPAIR.md:11` still refers to "PRIVATE 정본" while the operative request text states the repo is now PUBLIC — stale, should be corrected or removed to avoid an operator trusting outdated confidentiality assumptions.
- `tools/approval_signer.py cmd_sign` independently regenerates its own `SOURCE_PIN.json` from an operator-supplied `--source-commit`, separate from any `SOURCE_PIN.json` GPT may have already committed in Commit B. The content is deterministic (same commit+repo_id ⇒ identical bytes) so this is not currently unsafe, but it is a second, uncoordinated pin-generation path worth consolidating under the single-canonical-gate recommendation (F2).

### 4. Smallest implementation plan (for GPT/owner to action, not installed by me)

1. Decide and fix F1 (rename ref or require config value) — one-line change + one test.
2. Make `collab/ops/review_request_gate.py` and `tools/review_request_gate.py` the same file (symlink/copy-at-build in `tools/build_release.py`, or import directly) — removes F2 drift risk permanently.
3. Adopt Option B: drop the `--live-config`/LIVE policy precheck as a *publication prerequisite* in `submit_review_request.py`; keep it as an optional advisory `select` command GPT may run for its own sanity, never gating the Git writes.
4. Keep two-commit A/B exactly as implemented (`require_clean_main`, remote-head readback, `REQUEST_ID_ALREADY_EXISTS_CREATE_ONLY`) — these are genuine integrity checks, not authorization theater.
5. No change to `skill_collab_watcher/auto_approval.py`, `approval.py`, delegation ACL/enabled_at semantics.

**Invariants to preserve:** (a) host validator/auto-approver never trust anything GPT asserts about policy compatibility — "advisory, never authority"; (b) no automatic retry after `REVIEW_UNCERTAIN`/`POLICY_STOPPED`; (c) `max_request_usd` raises never retroactively admit previously cost-refused requests; (d) signing key never leaves the approver device.

**Acceptance tests:** (1) publish a REQUEST+PIN with a `live-config`-style precheck removed — confirm host `validator.py`/`auto_approval.py` still independently reject an out-of-cap or out-of-scope request; (2) confirm `intent='unified'` publish now matches a corrected example config; (3) confirm `tools/` and `collab/ops/` gate files are identical via CI diff check.

### 5. Expected user flow and remaining host dependencies

**"리뷰요청해줘" flow (after adopting Option B):** GPT selects the latest Work/ZIP → runs local SHA-256/schema/history self-checks (no Windows file access needed) → publishes Commit A then Commit B directly to `main` → reports `SUBMITTED_AWAITING_PROTECTED_SIGNER`. **Remaining host dependency (unchanged, cannot be removed):** an actual Windows session must still run the watcher/manual signer to apply real policy, delegation, cap, expiry, and Ed25519 signature before any model call — this is intentional and correct, not a gap to close.

### Knowledge files read
None pinned in this REQUEST ("(none pinned)" as stated). I read package files directly: `__SKILL_COLLAB_CONTEXT__/FILE_INDEX.txt`, `tools/review_request_gate.py`, `tools/source_pin.py`, `tools/approval_signer.py`, `config/reviewer.config.example.json`, `skill_collab_watcher/auto_approval.py` (grep), `skill_collab_watcher/approval.py` (grep), `skill_collab_watcher/validator.py` (grep), `skill_collab_watcher/orchestrator.py` (grep), `skill_collab_watcher/github_transport.py` (grep, no matches), `docs/AUTO_APPROVAL.md`, `docs/REQUEST_PIN_REPAIR.md`, `docs/CUTOVER_RUNBOOK.md` (partial). Plus the verbatim embedded files in the REQUEST text itself (`collab/ops/review_request_gate.py`, `submit_review_request.py`, `review_staged_submission.py`, `review_pin_preflight.py`, `source_pin.py`, and the Korean status document).

### Consumer profile judged against
`windows-single-user-watcher` — single Windows operator running the watcher/signer locally, GitHub repo as sole GPT↔Windows transport.

### Left unverified
- Actual real reviewer.config.json / delegation file on the operator's machine (not in this package; the `.example.json` is a proxy and may not reflect the true installed `max_budget_usd` values).
- Live execution of the 11 `review_staged_submission` unit tests or any CLI invocation — this was a static read-only review; "11/11 PASS" is the package's own claim, not independently re-executed by me.
- GitHub branch-protection/server-side settings for the now-PUBLIC repo — outside file-content review.
- Whether `tools/build_release.py` actually keeps `tools/` in sync with `collab/ops/` at package time (I read its presence in the index but did not open it) — recommend GPT/owner check this to see if F2 is a packaging bug or a genuine source fork.

### Proposed corrections to common knowledge (GPT to accept/reject)
1. Record as fact: the Windows watcher's real authorization path (`validator.py`, `auto_approval.py`) does **not** consume `review_request_gate.py`/`submit_review_request.py` output at all — these GPT-side tools are advisory-only, confirmed by absence of any import/reference in `skill_collab_watcher/`.
2. Record as fact: packaged `tools/review_request_gate.py` (tested in ZIP v0.2.29) and the `collab/ops/review_request_gate.py` module actually imported by `submit_review_request.py` have diverged (missing `unified` intent in the packaged/tested copy) — this should be fixed before further `unified`-intent usage is trusted.
3. Record as fact: the shipped example config's `POLICY-STATIC-V1` budget ($1.00) does not match the `unified` intent's required $3.00 — any claim that `submit_review_request.py --approval-route auto` "just works" at $3 cap should be treated as unverified until this is reconciled.
