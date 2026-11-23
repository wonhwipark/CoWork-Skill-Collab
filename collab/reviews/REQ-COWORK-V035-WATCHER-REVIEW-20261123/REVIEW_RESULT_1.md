---
schema: SKILL_COLLAB_REVIEW_RESULT_V1
review_id: "REQ-COWORK-V035-WATCHER-REVIEW-20261123|1|658a6f3da8bd018b96b64453892aec77d96868e19bc5788745c1591b1729a740|1"
responds_to_request_id: "REQ-COWORK-V035-WATCHER-REVIEW-20261123"
responds_to_request_revision: "1"
package_sha256: "658a6f3da8bd018b96b64453892aec77d96868e19bc5788745c1591b1729a740"
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

Matches `orchestrator.IN_FLIGHT_STATES = (JobState.CLAIMED, JobState.REVIEW_RUNNING)` — consistent, no mismatch. I now have enough evidence to write the review.

---

## Independent review — CoWork watcher v0.2.35 (REQ-COWORK-V035-WATCHER-REVIEW-20261123)

### BLOCKING findings
None identified from static reading.

### Non-blocking observations / confirmations

**1. F3 commit-pinned review intent — confirmed as designed, no issue found**
`v0_2_35/skill_collab_watcher/review_intent.py` + the `_intent_scope` caller in `v0_2_35/skill_collab_watcher/auto_approval.py:368-420` bind the intent to `request_id, request_revision, skill_id, source_commit, request_sha256, zip_sha256, package_size`, require exactly-one commit touching `REVIEW_INTENT.json` (`transport.commits_touching(path, limit=3)`, rejects if `len(found) != 1`), require that commit to be a strict descendant of request commit A (`pinned == commit` is itself rejected before calling `is_ancestor`), and re-verify REQUEST/package bytes at the pinned commit C still equal the request's own bytes. `v0_2_35/tests/test_v035_commit_pinned_intent.py` exercises: later-commit pinning, later replacement not affecting an already-approved claim, intent predating the request, two ambiguous intent commits, and intent only on a side commit — all asserting `auto.signer.calls == 0` where appropriate. The stored claim records `intent_commit`, `intent_raw_sha`, `intent_path` for later re-verification (confirmed by `test_v035_commit_pinned_intent.py:20-31`).
*Evidence*: I read the source and the test file directly; I did not execute the suite myself, so "PASS" is the author's claim, not mine.

**2. F1 revalidation before signature / before READY — confirmed, nonce is checked without re-consumption**
`AutoApprover._revalidate` (`auto_approval.py:660-719`) is called immediately before signing (`_sign_and_post`, line 735), before posting `APPROVAL_SIG.json` (line 755), and before posting `READY.md` (line 767) — three call sites, matching the "before signature and before READY" requirement. Crucially, revalidation uses `consume_nonce=lambda value: store.review_intent_nonce_owner(value) == rid` (line 710), which only reads `review_intent_nonces` (`state_store.py:320-323`), whereas the *first* verification at line 407 uses `store.consume_review_intent_nonce(...)`, which does the one-time INSERT. This is the correct separation the REQUEST asked me to check: nonce ownership is re-checked on every revalidation pass without re-consuming it.
*Evidence*: read directly; confirmed by `test_v033_intent_wiring.py` tests `test_revalidation_passes_for_the_unchanged_consumed_intent` and `test_revalidation_refuses_a_nonce_this_request_did_not_consume` (lines 178-206), which I read but did not execute.

**3. Dispatch idempotency — confirmed, one model call per request id, no re-run after interruption**
- Exactly-one claim: `store.claim()` is a single `BEGIN IMMEDIATE` SQLite `UPDATE ... WHERE state IN (never-dispatched)`; only the winner with `rowcount==1` proceeds (`state_store.py:272-299`; `orchestrator.py:714-719`).
- `runner.run()` (the model call) is invoked exactly once per `processing_key`, after `_reserve_dispatch` writes a remote dispatch record (`orchestrator.py:735-758`).
- On interruption, `seal_interrupted` moves orphaned `CLAIMED`/`REVIEW_RUNNING` rows (owned by a now-dead process) to `REVIEW_UNCERTAIN` and explicitly does not re-run them (`state_store.py:461-489`); it only acts when `exclusive=True` (watcher lock held), and never touches rows owned by the live process.
- If a job is left at `RESULT_SAVED`/`UPLOAD_PENDING` (model call already completed, only the publish step failed), the resume path only retries the upload (`_retry_publish_only`); the code comment at `orchestrator.py:827-828` states `runner.run()` is never called again, and `_handle_existing_job` routes `RESUMABLE_PUBLISH_STATES` to that same retry-only path (`orchestrator.py:397-401`).
*Evidence*: read directly from `orchestrator.py` and `state_store.py`.

**4. F2 release manifest — partially verified**
`docs/RELEASE_MANIFEST.json` lists `file_count: 113`, excludes itself (`self_excluded_path`), and `version: 0.2.35`. `FILE_INDEX.txt` lists 114 package entries total (113 + the manifest itself), which is arithmetically consistent. I grepped the manifest and confirmed byte sizes for 5 spot-checked files (`auto_approval.py`, `orchestrator.py`, `state_store.py`, `test_v035_commit_pinned_intent.py`, `source_pin.py`) exactly match the sizes in `FILE_INDEX.txt`.
*Unverified*: I have no hashing tool in this read-only session, so I could not independently recompute or check any of the 113 SHA-256 values in the manifest against the actual file bytes — this rests entirely on the candidate's own claim and its own test (`tests/test_release_manifest_v034.py`), which I read but did not execute.

### Knowledge files actually read
None — the REQUEST listed no pinned knowledge files ("(none pinned in this REQUEST)").

### Consumer profiles judged against
`windows-single-user-watcher` (the only profile named in the REQUEST).

### What I left unverified
- All 113 SHA-256 values in `docs/RELEASE_MANIFEST.json` (no hashing tool available to me in this session).
- The author's reported test results (1075 PASS/0 FAIL/8 SKIP, QA28 28/28, Git CLI 6/6) — these are read as claims, not reproduced; I did not execute any test.
- GitHub API behavior at runtime (`commits_touching`, `is_ancestor`, `compare`) — I read the implementation but did not exercise it against a live GitHub repository.
- Linux-specific paths, the in-house LLM/runner behavior, and MCP behavior — out of scope for a Windows static read.
- The Windows Notifier/live delegation/protected-signer installation path, which `docs/REQUEST_PIN_REPAIR.md` itself states is a separate, not-yet-complete gate from this package.

### Proposed corrections to common knowledge
None — nothing I read contradicted the pinned knowledge or request text (no knowledge files were pinned for this request).
