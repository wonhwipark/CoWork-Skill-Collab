---
schema: SKILL_COLLAB_REVIEW_RESULT_V1
review_id: "REQ-COWORK-V0214-R1-20261114|1|3a221dcdb22ba75208a60ca555b0ee75866313a591148b1f482b7cbb6aa0b367|1"
responds_to_request_id: "REQ-COWORK-V0214-R1-20261114"
responds_to_request_revision: "1"
package_sha256: "3a221dcdb22ba75208a60ca555b0ee75866313a591148b1f482b7cbb6aa0b367"
skill_id: "cowork-review-watcher"
run_policy_ref: "POLICY-STATIC-V1"
knowledge_refs: [{"path": "/SKILL-COLLAB/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/review-inputs/REV-COWORK-V0214-20261114/REVIEW_MANIFEST.md", "sha256": "14e23120a65fa4a67dba67ecb9215a221f3653b2310d6e6c7198be0399a537cb"}, {"path": "/SKILL-COLLAB/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/review-inputs/REV-COWORK-V0214-20261114/diff_v0_2_13_to_v0_2_14.patch", "sha256": "494afd6710a216068b18a127d1e34381d02da644a5bb85568733904680795987"}]
consumer_profiles: ["windows-single-user-watcher"]
reviewer_os: WINDOWS
review_scope: CODE_REVIEW
test_policy: "STATIC_ONLY"
execution_status: COMPLETED
limitations: ["static review by an automatically started Claude Code process; no package code was executed", "knowledge files were delivered as the REQUEST pinned them; which parts were actually read is reported by the reviewer in the text", "reviewer host is Windows; Linux, in-house LLM and MCP behaviour are not verified by this review"]
---

# 리뷰 결과

## Review findings — CoWork watcher v0.2.14, `try_claim` fix

### Blocking

**1. Cross-key double dispatch when `local_policy_revision` changes before first dispatch — not fixed by `try_claim` (Q2)**
- File/function: `skill_collab_watcher/state_store.py: StateStore.find_logical_job`; `skill_collab_watcher/orchestrator.py: _process_request_group`; `skill_collab_watcher/validator.py:206` (`processing_key = f"{request_id}|{request_revision}|{package_sha256}|{policy.local_policy_revision}"`).
- Failure condition: a job that was created but **never dispatched** (state `VALIDATED`/`WAIT_INPUT`/`AUTH_REQUIRED`) and is blocked for a while (e.g. `DAILY_LIMIT_BLOCKED`, `CLAUDE_AUTH_REQUIRED`, `APPROVAL_*`, `REVIEWS_PAUSED` — all return `GroupResult(retry=True)` without touching the job row, `orchestrator.py:479‑609`) stays in that pending state indefinitely. If the operator bumps `local_policy_revision` while it is still pending, the next scan computes a **new** `processing_key` for the same logical request. `find_logical_job` (`state_store.py:366-377`) is only consulted when `existing is None`, and it is restricted by `_process_request_group` (`orchestrator.py:522-524`) to match only when the earlier job's state is in `TERMINAL_STATES + IN_FLIGHT_STATES + RESUMABLE_PUBLISH_STATES` — the never‑dispatched states are explicitly excluded. So the old (rev‑A) row is invisible to the new (rev‑B) flow: a second job row is created, independently passes approval/ceilings, and independently wins `try_claim` on its own distinct key. Once whatever blocked rev‑A clears (e.g. the daily limit resets), rev‑A's own un-changed row can *also* reach `try_claim` and dispatch. Result: two model calls for one logical request — the exact class of bug `try_claim` was introduced to prevent, just reached through a different key instead of a race on the same key.
- Evidence: `orchestrator.py:522-524` (`TERMINAL_STATES + IN_FLIGHT_STATES + RESUMABLE_PUBLISH_STATES`, never-dispatched states omitted) + `validator.py:206` (policy revision baked into the key) + `orchestrator.py:479-489` / `556-559` / `572-575` (blocked paths leave the job row untouched in its pending state).
- Minimal fix: have `find_logical_job` (or a new lookup) also match never‑dispatched states for the same `request_id`+`request_revision`+`package_sha256`, and reuse/update that row's key instead of creating a second one when the policy revision changes — i.e. treat a pending job the same way `_retry_publish_only` treats a resumable one.
- How to verify: add a unit test that creates a job in `VALIDATED` under `local_policy_revision="1"`, then runs `_process_request_group` again with `local_policy_revision="2"` for the same request/revision/package while the first job is still `VALIDATED`; assert only one row/`try_claim` win ever occurs for the logical request.

**2. `seal_interrupted(exclusive=True)` can seal (and notify as failed) a job actually owned by a live `scan` process (Q3)**
- File/function: `skill_collab_watcher/state_store.py: StateStore.seal_interrupted`; `skill_collab_watcher/cli.py: cmd_scan` (no lock) vs `cmd_watch` (`SingleInstanceLock` + `rt.exclusive = True`, `cli.py:448-468`).
- Failure condition: `cmd_scan` never acquires `watch.lock`/`SingleInstanceLock` — only `cmd_watch` does, and only `cmd_watch` passes `exclusive=True` into `run_scan_cycle`/`seal_interrupted`. The docstring/comment in `seal_interrupted` assumes `exclusive=True` means "no other watcher can still be inside a model call" (`state_store.py:250-253`), but a concurrently running `scan` process is not a "watcher" and holds no lock at all. If a `scan` claims a job and is mid model-call (`REVIEW_RUNNING`, owned by its own `job_claims.owner`) when a `watch` process starts and takes the lock, `watch`'s `seal_interrupted(exclusive=True)` finds that row via the `job_claims.owner <> self.owner` check (`state_store.py:262-287`) — true, because the owner uuid belongs to the live scan, not to this new watch instance — and marks it `REVIEW_UNCERTAIN`, writing an audit event that is in `notify_events.NOTIFY_EVENTS` and will be delivered to the operator as "[불확실] ... 모델 호출 중 감시기가 끊겼습니다" even though the review is in fact still running and will complete normally afterward (the scan process's subsequent `update_job_state` calls are unconditional UPDATEs by key, so the row does get overwritten to `COMPLETED` later, but the false notification has already gone out).
- Evidence: `cli.py:448-468` (scan has no lock, `exclusive` defaults False only for scan; watch sets `rt.exclusive = True`); `state_store.py:246-287` (`seal_interrupted` owner check, no distinction between "a dead watcher" and "a live scan"); `notify_events.py:17-21` (`REVIEW_UNCERTAIN` in `NOTIFY_EVENTS`).
- Minimal fix: either (a) have `scan` also take a shared/short-lived marker so `seal_interrupted` can tell a live scan apart from a dead one (e.g. a liveness heartbeat row per `owner`, not just presence in `job_claims`), or (b) narrow `seal_interrupted` to only touch rows whose owning process is actually gone (PID liveness check) rather than "owner != me".
- How to verify: in a test, start a fake `scan`-style `StateStore` instance, `try_claim`+`record_claim` a job, leave it `REVIEW_RUNNING`; open a second `StateStore` instance and call `seal_interrupted(exclusive=True)`; assert it does **not** seal a job whose claimant process is still alive (requires adding a liveness signal — right now the test suite has no case for "a live non-watcher owns the job", only for dead/startup sealing).

### Non-blocking

**3. Daily dispatch/budget ceilings are check-then-act across processes, not reserved (Q4)**
- File/function: `orchestrator.py: _check_ceilings`, using `StateStore.dispatches_since`/`spend_since`.
- Failure condition: the ceiling check is a plain `SELECT COUNT(*)`/aggregate with no `BEGIN IMMEDIATE` and no reservation row; it runs strictly before `try_claim`. Two different processing keys handled by two different processes (e.g. a manual `scan` run while `watch` is also scanning — exactly the scenario Q3 highlights the lock does not prevent) can both read the ceiling before either has written `REVIEW_DISPATCHED`, and both proceed, overshooting the daily ceiling by up to the number of concurrently racing dispatches. In the single-user Windows profile this is realistically bounded (1–2 extra dispatches at most), but it is a genuine non-atomic reservation.
- Evidence: `orchestrator.py:475-489` (plain reads, no lock/transaction) vs. `try_claim`'s single atomic `UPDATE` (`state_store.py:222-236`) — the ceiling check has no equivalent.
- Minimal fix: fold the ceiling check into the same atomic claim, e.g. a conditional `UPDATE ... WHERE (SELECT COUNT... ) < limit` or a reserved-counter row updated inside the `try_claim` transaction.
- How to verify: two concurrent `StateStore`s set `max_dispatches_per_day=1`, both race `_check_ceilings` + `try_claim` for two different jobs; assert at most one dispatch proceeds (will currently fail).

**4. A job claimed and crashed under `scan`-only usage can stay `CLAIMED`/`REVIEW_RUNNING` forever, silently (Q1)**
- File/function: `state_store.py: seal_interrupted` (only runs when `exclusive=True`, i.e. only under `watch`'s lock); `cli.py: cmd_recover` explicitly refuses `--requeue` for stuck jobs (`cli.py:572-575`).
- Failure condition: if the operator's workflow only ever runs `windows\run_scan.cmd` (manual/scheduled `scan`, never `watch`), a `scan` process killed between `try_claim` and the final `update_job_state` leaves the job `CLAIMED`/`REVIEW_RUNNING` permanently — nothing ever calls `seal_interrupted(exclusive=True)` to move it to `REVIEW_UNCERTAIN`, and `REVIEW_UNCERTAIN`/`FAILED`/etc. are the only states in `NOTIFY_EVENTS`, so the operator gets **no notification at all**; `cmd_recover` will list the stuck job but refuses to requeue it. This is plausibly intentional fail-closed design, but it is a real operational gap worth confirming is documented for the `windows-single-user-watcher` profile, since `run_scan.cmd` is shipped as a first-class entry point alongside `run_watch.cmd`.
- Evidence: `state_store.py:259-261` (`if not exclusive: log_event_once("SEAL_SKIPPED", ...); return 0`); `cli.py:448-455` (`cmd_scan` never sets `exclusive`); `cli.py:572-575` (recover refuses requeue).
- Minimal fix: run `seal_interrupted` (or an equivalent "is this claimant's process still alive" check) from `scan` too, scoped to jobs this same `scan` invocation could not have claimed, or add a `SEAL_SKIPPED`/stuck-job alert to `NOTIFY_EVENTS` so a scan‑only crash is at least visible to the operator.
- How to verify: run `scan` against a job, kill it mid-`REVIEW_RUNNING` (simulate via test), run `scan` again repeatedly and confirm no event ever reaches `NOTIFY_EVENTS`/`recover --requeue`.

**5. No Windows process-tree kill on `claude` timeout (Q6)**
- File/function: `skill_collab_watcher/review_runner.py: RealReviewRunner.run`, `subprocess.run(argv, ..., timeout=self.timeout_sec)`.
- Failure condition: on `TimeoutExpired`, `subprocess.run`'s default cleanup only calls `kill()`/`TerminateProcess` on the immediate `claude` child; it does not create a job object or kill a process tree. If the `claude` CLI spawns any helper/child processes (e.g. a Node.js runtime, tool subprocesses), those can survive the timeout as orphans, continuing to run (and potentially write to disk or consume the budget) with the watcher believing the run ended.
- Evidence: `review_runner.py:207-228` — plain `subprocess.run(..., timeout=...)`, no `CREATE_NEW_PROCESS_GROUP`/job-object/`psutil`-based tree termination anywhere in the file.
- Minimal fix: launch with a Windows Job Object (or `CREATE_NO_WINDOW`+`subprocess.Popen` + `taskkill /T /F /PID`) so a timeout kills the whole process tree, not just the immediate child.
- How to verify: have the `e2e_claude_stub.py` spawn one grandchild process that sleeps far past the test's `E2E_STUB_SLEEP`/timeout, trigger a timeout, and check (via a marker file) whether the grandchild is still alive afterward.

---

**What I did not verify**
- Could not execute anything (static review only, read-only tools); the author's reported "9 PASS ×3" / "666 passed, 13 skipped" are their own claims, not independently reproduced here.
- Whether `subprocess.run([claude.cmd, ...], shell=False)` actually launches a `.cmd` file correctly on this Windows host was not executed by me; I only read the code and the test harness that relies on exactly this pattern (`tests/test_cli_entrypoint_e2e.py` creates `claude.cmd` and launches it the same way `RealReviewRunner` does), which is reasonable but not something I ran myself.
- Did not check `su_l1/*`, `dropbox_transport.py`, `approval.py` internals, `config.py`, or `tools/*` — out of the REQUEST's stated file scope and not needed to answer Q1–Q6.
- `trust_root_independence=warn` (manifest item (d)) and the token-file format (manifest item (f)) were visible in the E2E test config but are outside the six Q1–Q6 questions I was asked to answer, so I did not analyze them further.
- Linux / in-house-LLM / MCP behavior: not applicable to any of these findings, which are either Python-logic-level (Q1–Q4) or explicitly Windows-only (Q6).

**Knowledge files read:** `__SKILL_COLLAB_CONTEXT__/01_REVIEW_MANIFEST.md`, `__SKILL_COLLAB_CONTEXT__/02_diff_v0_2_13_to_v0_2_14.patch`, `__SKILL_COLLAB_CONTEXT__/FILE_INDEX.txt`.
**Package files read:** `skill_collab_watcher/state_store.py`, `orchestrator.py`, `review_runner.py`, `github_transport.py`, `lock.py`, `watch_loop.py`, `models.py`, `cli.py` (targeted excerpts), `notify_events.py`; `tests/test_try_claim.py` and `tests/test_cli_entrypoint_e2e.py` were read in full via the diff patch. `windows/run_scan.cmd`, `windows/run_watch.cmd` read for the lock-usage check.
**Consumer profile judged against:** `windows-single-user-watcher`.
**Proposed corrections to common knowledge (for GPT to accept/reject):** the `REVIEW_MANIFEST.md` claim that `try_claim` is "the unique gate on every dispatch path" and that `seal_interrupted(exclusive=True)` is safe because "the caller holds the watcher lock and therefore no other watcher can still be inside a model call" should be revised — both the key-change race (finding 1) and the scan/watch lock gap (finding 2) show gates it doesn't cover.
