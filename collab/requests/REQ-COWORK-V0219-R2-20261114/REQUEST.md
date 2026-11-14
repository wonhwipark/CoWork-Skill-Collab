---
schema: SKILL_COLLAB_REVIEW_REQUEST_V1
state: SUBMITTED
request_id: REQ-COWORK-V0219-R2-20261114
request_revision: 1
project_id: COWORK-DROPBOX-TO-GITHUB-MIGRATION
work_id: COWORK-DROPBOX-TO-GITHUB-MIGRATION
skill_id: cowork-review-watcher
package_path: /SKILL-COLLAB/packages/skill-collab-watcher_v0_2_19_1114_DEV_NOT_FOR_DEPLOYMENT.zip
package_file_id: github:REV-COWORK-V0219-20261114
package_rev: v0.2.19
package_sha256: 6e7fee3340cc6d0282d1c18fe3db42a90360259dd73fa6d7c0a7698af7afe5c0
package_size_bytes: 239143
baseline_package_ref: null
knowledge_refs:
  - path: /SKILL-COLLAB/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/review-inputs/REV-COWORK-V0219-20261114/REVIEW_MANIFEST.md
    sha256: a67d4bd346f1afc0e1d01171e8565470c21c387ed1101010a5373007c00e1657
  - path: /SKILL-COLLAB/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/review-inputs/REV-COWORK-V0219-20261114/diff_v0_2_17_to_v0_2_19.patch
    sha256: 8a194eb0d1363a4d93f1763b1503ff59683be5674837a778f14b70c640dfa4f4
consumer_profiles: [windows-single-user-watcher]
reviewer_os: WINDOWS
test_policy: STATIC_ONLY
run_policy_ref: POLICY-STATIC-V1-LARGE
output_contract: SKILL_COLLAB_REVIEW_RESULT_V1
goal: independent R2 review of v0.2.19 (remote dispatch reservation N1, repository id binding N2, restart and recovery paths)
---

# R2 independent review of the CoWork watcher v0.2.19 (N1 remote dispatch reservation, N2 repository id binding)

Tier R2 under POLICY-STATIC-V1-LARGE: exactly one review, hard budget USD 3, no follow-up call. You are independent of the author; the
author's own test results are claims, not evidence. Spend effort on the changed code and its call boundaries. Stop and write the report while
budget remains: an unfinished review is lost.

Read the two pinned knowledge files first (REVIEW_MANIFEST.md: claims and known gaps; diff_v0_2_17_to_v0_2_19.patch: the change relative to
v0.2.17, which already had an R2 review that does NOT carry over). Then read only what you need: skill_collab_watcher/orchestrator.py
(_reserve_dispatch, _remote_result_published, _check_approval, the dispatch path), state_store.py (claim, seal_interrupted, job rows),
github_transport.py (upload, get_metadata, download_latest, repository_id, pinning), review_runner.py, and the tests
tests/test_v019_crash_matrix.py and tests/test_v018_gates.py.

Questions (answer each; "no finding" with evidence is a valid answer):

Q1. Atomicity of the remote reservation: is create-only really atomic on GitHub's contents API (two writers, check-then-write, pinned reads)?
    Can two workers or two processes both get RESERVED for one request id and revision?
Q2. Duplicate keys and bindings: the record is keyed by request id and revision only. Can a different package, policy revision, re-signed
    approval or resubmitted request wrongly share, bypass or be blocked by it? Is the approval still bound to the exact package?
Q3. Classification: RESERVED, ALREADY_OURS (attempt_count >= 2 and same processing key), FOREIGN, ERROR. Find any state where a paid review can
    start twice, or where a legitimate review is wrongly refused forever. Include a lost or reset local row and the usage-limit retry.
Q4. Crash and restore: backup restored after a review, local history lost, crash before/after the reservation, before result save, before
    publish. Is there any path to a second model start, or to a lost job (no row, no event, no remote record)?
Q5. Remote errors: read/write failures, 403/422/409/5xx, timeouts, stale pin, eventual visibility of a just-written record. Fail-closed everywhere?
Q6. N2: the numeric repository id check before an approval is honoured: other repository, id missing, API failure, caching. Any bypass?
Q7. Cost and gates: daily ceilings, claim() reservation counting, and whether a reservation that was never followed by paid work can block the
    ceiling or the request forever. SHADOW (read-only) must never write a reservation or start a model: confirm.
Q8. Anything else in the interaction of the v0.2.18 and v0.2.19 changes with scan/watch locking, seal_interrupted and publish-only retry.

Report BLOCKING findings separately from non-blocking ones, at most 10 findings in total, each with file/function, failure condition, evidence,
minimal fix and how to verify it. State plainly what you could not verify. Windows only; do not speculate about Linux.
