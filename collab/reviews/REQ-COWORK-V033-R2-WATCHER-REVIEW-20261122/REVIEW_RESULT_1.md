---
schema: SKILL_COLLAB_REVIEW_RESULT_V1
review_id: "REQ-COWORK-V033-R2-WATCHER-REVIEW-20261122|1|23579a5c8c6690b5831116410fc623e3a8bbc5c659cb6fdea8628e765fa7c206|1"
responds_to_request_id: "REQ-COWORK-V033-R2-WATCHER-REVIEW-20261122"
responds_to_request_revision: "1"
package_sha256: "23579a5c8c6690b5831116410fc623e3a8bbc5c659cb6fdea8628e765fa7c206"
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

I have enough evidence to write the review now.

---

# Independent review — CoWork watcher v0.2.33 r2 (intent wiring, dispatch idempotency)

**Scope:** static read-only review on Windows of the package at the pinned SHA-256. No tests executed, no model calls made, no live checks on GitHub/Dropbox transports.

## Summary

The r2 candidate wires `review_intent.py` into `auto_approval.py`'s scope-fallback path (`_intent_scope`) and adds revalidation hooks (`_revalidate`) that run before every signature and every publication. Dispatch idempotency is enforced by a durable remote create-only file (`DISPATCH_<rev>.md`) plus a local atomic `CLAIMED` transition, and `seal_interrupted` is correctly gated on the OS-level `SingleInstanceLock`. I did not find any BLOCKING defect in the logic I could read.

## BLOCKING findings

None identified from static reading. I want to flag one item that borders on blocking severity because it is a trust-boundary subtlety, but on reading the code I could not actually construct a bypass — see non-blocking item 1 below for why I downgraded it.

## Non-blocking findings / observations

**1. `review_intent.py::verify_review_intent_with_key` — nonce consumed only after full validation (verified correct, not a defect)**
`skill_collab_watcher/review_intent.py:86-90` — `consume_nonce(nonce)` is called last, after signature verification (line 69), repo/field binding (71-75), skill-exactness (76-78), and time-window checks (79-85). This means a forged, mis-bound, or expired intent can never burn a legitimate nonce, and the "replay" nonce check cannot be used as an oracle to invalidate someone else's future intent. Confirmed by `test_v033_intent_wiring.py`'s forged/expired/revoked-key tests, which all assert `auto.signer.calls == 0` without needing a distinct nonce. This is correct design; no action needed, noting it so it is not re-litigated.

**2. `auto_approval.py::_intent_scope` (line 388) — `package_size` expected value is taken from request front-matter as a string, compared via `str(...)` in `review_intent.py` (line 74)**
`front.get("package_size_bytes")` can be any front-matter string (e.g. `"12345"`), and the bound field comparison in `review_intent.py` stringifies both sides (`str(payload.get(name)) != str(expected.get(name))`). This is consistent (both sides become strings) so there's no type-confusion bypass, but it means a request with a non-canonical numeric front-matter value (leading zeros, e.g. `"007"`) could still bind correctly only if the intent's `package_size` field is also written as `"007"` — i.e. byte-exact string matching, not numeric. This is fine since both the request and the intent are controlled by the same approver, but it's worth the author confirming the `approval_signer.py`/intent-issuing tooling always emits `package_size` as a plain decimal integer with no leading zeros, matching how `front.get("package_size_bytes")` is typically parsed elsewhere (`int(front.get(...))`). Not exploitable as far as I can tell; recommend a comment or a stricter int-vs-int compare for defense in depth.

**3. `tools/review_request_gate.py` — budget/gate removal confirmed in scope, matches request text**
I confirmed `orchestrator.py::_check_ceilings` (line 554-556) is a stub that always returns `None` with the comment "Aggregate review-count and cost ceilings intentionally abolished," and `review_runner.py::build_argv` never emits `--max-budget-usd` (confirmed directly, and by `test_review_runner_argv.py` lines 25/31). The signer's own gates are intact and separate: `state_store.py::auto_claim` (line 401) still enforces `max_day_calls`/`max_day_cents`/`max_month_cents` atomically inside `BEGIN IMMEDIATE`, and `_revalidate` re-checks usage windows (`window_usage`, excluding the candidate's own prior reservation) before every signature and publish. This matches the REQUEST's stated intent exactly — not a new finding, just confirmed.

**4. Dispatch idempotency cross-process mechanism relies on the *remote* store, not the local SQLite DB, for cross-database safety**
`orchestrator.py::_reserve_dispatch` (line 520) and `_process_request_group` (lines 713-756) show the actual cross-OS-process primitive is the remote create-only `DISPATCH_<rev>.md` file (atomic `O_CREAT|O_EXCL` in the test harness, `mode="add"` upload against the real transport in production), not the local `state_store.claim()` (which is only atomic within one SQLite file). This is correctly designed for the stated test scenario ("separate OS processes, separate databases") — confirmed by `tests/dispatch_worker.py`'s `SharedDispatchTransport`. However, this means the idempotency guarantee is only as strong as the transport's upload-conflict atomicity. I did not read `dropbox_transport.py` or `github_transport.py` in this review to confirm their real `upload(..., mode="add")` is genuinely atomic create-only against the real services (as opposed to the `MockTransport`/test harness, which is deliberately atomic by construction). **This is a real gap in my verification, not a code defect** — flagging it as unverified rather than blocking since the REQUEST's dev-test claims only cover the mock harness.

**5. `seal_interrupted` / `exclusive` wiring verified correct**
`cli.py::cmd_scan` and `cmd_watch` (lines 490-524) both acquire `SingleInstanceLock` before setting `rt.exclusive = True`, and `run_scan_cycle` defaults `exclusive=False` (line 911) so a caller that forgot to pass it would fail closed (skip sealing, log `SEAL_SKIPPED`) rather than seal unsafely. This correctly satisfies "UNCERTAIN sealing after interruption" without risking sealing jobs that another live process might still be running.

## What I read directly vs. what the package only claims

- Read directly and verified: `review_intent.py`, `tools/review_request_gate.py`, `tools/approval_signer.py`, `auto_approval.py` (intent scope + revalidate + process/sign/publish paths), `state_store.py` (nonce table, `try_claim`/`claim`, `seal_interrupted`, `auto_claim`/`window_usage`), `orchestrator.py` (dispatch reservation, claim, REVIEW_DISPATCHED/REVIEW_RUNNING ordering, `_check_ceilings` stub), `cli.py` (lock acquisition, `exclusive` wiring, absence of `--budget`/`--max-budget-usd` flags), `review_runner.py::build_argv`, `lock.py`, `approval.py` (`TrustRoot`, `canonical`, trust root loading), test sources for `test_v033_intent_wiring.py`, `test_v033_nonce_store.py`, `test_v033_process_dispatch.py`, `dispatch_worker.py`, `nonce_worker.py`, `test_review_runner_argv.py`.
- **Claimed, not verified by me:** the "Full suite 1014 PASS / 0 FAIL / 12 SKIP" result and the "two OS-process dispatch race and crash tests passed" result are the candidate author's own dev run — I read the test *source* and judged the test logic sound, but I did not execute pytest myself in this session.
- **Not reviewed at all:** `dropbox_transport.py`, `github_transport.py` internals (real transport atomicity for `upload(mode="add")` against the live services — see finding 4), `shadow_guard.py`, `notify_events.py`, `validator.py` internals, `zip_safety.py`, `secrets_store.py`/`secret_prompt.py`, the Windows `.cmd` launchers, and `docs/CUTOVER_RUNBOOK.md`/`RELEASE_MANIFEST.json` (process/packaging docs, not code behavior).

## Consumer profiles judged against

`windows-single-user-watcher` — reviewed the Windows-specific lock (`msvcrt` byte-range lock in `lock.py`) and the Windows ACL-restriction code path (`approval.py` SDDL parsing, `_restrict_to_owner` in `approval_signer.py`) only by reading; did not execute on this Windows host to confirm `icacls`/`msvcrt.locking` behavior live.

## What I left unverified

- Real transport atomicity of create-only uploads against GitHub/Dropbox APIs (finding 4).
- Whether the 1014-test suite actually passes (dev-reported only).
- In-house LLM / MCP-related behavior — out of scope for this static Windows review per the standing instruction that Windows reading does not verify Linux/LLM/MCP behavior.
- Runtime behavior of `msvcrt.locking` and `icacls` on this specific Windows host (read-only review, no execution).

## Proposed corrections to common knowledge (GPT decides)

None. The intent-wiring and dispatch-idempotency design as read matches the REQUEST's stated intent and the prior independent-review findings it references (R1 findings 2–4) appear to have been addressed in the code I read. No correction to pinned knowledge is proposed this round (none was pinned for this REQUEST).
