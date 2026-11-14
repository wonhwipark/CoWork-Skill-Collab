# REVIEW_MANIFEST — CoWork watcher v0.2.17 (R2 structural review)

Review ID: REV-COWORK-V0217-R2-20261114. Target: skill-collab-watcher_v0_2_17_1114.zip (the exact pinned bytes). Contains only CoWork's own
non-sensitive code. Windows single-user watcher; consumer profile windows-single-user-watcher.

## What the target is
v0.2.17 = v0.2.14 (already reviewed once at tier R1: five findings) + v0.2.16 changes (never independently reviewed) + fixes for those five
findings (never independently reviewed). The patch `diff_v0_2_14_to_v0_2_17.patch` is the full change, 20 files, about 1100 lines.

## Change groups and what the author CLAIMS (claims, not facts)
1. v0.2.16 usage-limit wait/resume (review_runner.py, orchestrator.py, config.py, models.py, notify_events.py): when the claude CLI reports a
   session/weekly/opus/sonnet usage limit before doing any work, the job is deferred (state keeps the request retryable, no model work counted)
   and retried after the reset time parsed from the CLI message or a configured wait; bounded by usage_limit_max_wait_sec and
   usage_limit_max_deferrals; limits that never reset by themselves (admin/spend cap) are an ordinary failure. Claim: a deferral never causes
   a second paid review for work that already started (BEFORE_START_MAX_ELAPSED_SEC = 120 s decides "refused before start").
2. v0.2.16 GitHub token JSON file support (cli.py read_github_token): JSON {token, repo, scope, expires} read in memory only.
3. F1 (state_store.py, orchestrator.py): a never-dispatched job under another local_policy_revision must not allow a second review of the same
   logical request (request_id|request_revision|package_sha256). Author reproduced it only with re-signed approval + rollback of the policy
   revision + lost cursor.
4. F2/F4 (cli.py): `scan` now takes the same single-instance lock as `watch` and runs exclusive, so it can seal an interrupted job of a dead
   process and never seals a job of a live one; a second scan/watch is refused with exit 3.
5. F3 (state_store.py StateStore.claim): daily dispatch/cost ceilings are checked and reserved inside one BEGIN IMMEDIATE transaction
   together with the claim, counting jobs that are CLAIMED/REVIEW_RUNNING without REVIEW_DISPATCHED. try_claim remains as a wrapper.
6. F5 (review_runner.py): the claude process is started through Popen and on timeout the whole tree is killed (taskkill /T /F on Windows).
7. SHADOW isolation refusal keeps exit code 6 in both scan and watch (ShadowIsolationError is a RuntimeError and used to be swallowed by the
   new lock handler).

## Author's own test results (NOT independently reproduced)
- Test venv (with cryptography): 644 passed, 12 skipped. Operating interpreter (no cryptography installed): 578 passed, 17 skipped; the 5 extra
  skips are the real-Ed25519 tests, so the operating interpreter does not exercise signature verification at all.
- New regression tests tests/test_r1_findings.py (6 + 2 parametrized), tests/test_usage_limit_resume.py, tests/test_token_file_formats.py.
- The ZIP rebuilds to identical bytes; the release secret scan reports 0 findings.

## Known gaps the author does NOT claim to have closed (please judge them, do not assume)
- repo_id in the approval/trust root is a label compared between payload and pin; it is not bound to the real GitHub repository identity.
- Engine write path to GitHub was only tested against a loopback fake; no real write token existed for the engine.
- Several state machines changed together; combined behaviour across usage-limit deferral + restart + policy revision + cursor loss is only
  covered by unit/loopback tests.
- Windows-only evidence; Linux, in-house LLMs and MCP are out of scope.

## Review tier and limits
R2, POLICY-STATIC-V1-LARGE, one call, hard budget USD 3, static review only. Token/turn numbers (about 5 turns, 40k in / 6k out) are targets,
not enforced. No follow-up call exists.
