---
schema: SKILL_COLLAB_REVIEW_REQUEST_V1
state: SUBMITTED
request_id: REQ-COWORK-V0214-R1-20261114
request_revision: 1
project_id: COWORK-DROPBOX-TO-GITHUB-MIGRATION
work_id: COWORK-DROPBOX-TO-GITHUB-MIGRATION
skill_id: cowork-review-watcher
package_path: /SKILL-COLLAB/packages/skill-collab-watcher_v0_2_14_1114.zip
package_file_id: github:REV-COWORK-V0214-20261114
package_rev: v0.2.14
package_sha256: 3a221dcdb22ba75208a60ca555b0ee75866313a591148b1f482b7cbb6aa0b367
package_size_bytes: 219663
baseline_package_ref: null
knowledge_refs:
  - path: /SKILL-COLLAB/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/review-inputs/REV-COWORK-V0214-20261114/REVIEW_MANIFEST.md
    sha256: 14e23120a65fa4a67dba67ecb9215a221f3653b2310d6e6c7198be0399a537cb
  - path: /SKILL-COLLAB/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/review-inputs/REV-COWORK-V0214-20261114/diff_v0_2_13_to_v0_2_14.patch
    sha256: 494afd6710a216068b18a127d1e34381d02da644a5bb85568733904680795987
consumer_profiles: [windows-single-user-watcher]
reviewer_os: WINDOWS
test_policy: STATIC_ONLY
run_policy_ref: POLICY-STATIC-V1
output_contract: SKILL_COLLAB_REVIEW_RESULT_V1
goal: R1 defect review of the v0.2.14 concurrency fix (see the body for the six questions)
---

# R1 change and defect review of the CoWork watcher v0.2.14

Tier R1 under POLICY-STATIC-V1: one review, effort medium, hard budget USD 1. There is no follow-up call, so answer from
what you read in a few turns and do not widen the scope.

Read the two pinned knowledge files first: REVIEW_MANIFEST.md (what changed and what is claimed) and
diff_v0_2_13_to_v0_2_14.patch (the actual change). Then read only these package files unless a finding needs another one:
skill_collab_watcher/state_store.py, skill_collab_watcher/orchestrator.py, skill_collab_watcher/review_runner.py,
skill_collab_watcher/github_transport.py, tests/test_try_claim.py, tests/test_cli_entrypoint_e2e.py.

Questions (the author found and fixed one real defect: two concurrent scans started the reviewer twice for one approved
request; the fix is a conditional single-statement UPDATE, StateStore.try_claim, used instead of an unconditional CLAIMED
update):

Q1. Is try_claim a correct compare-and-set on this SQLite connection (isolation_level, autocommit, WAL)? Can two processes
    both win, or can a job stay CLAIMED forever after a crash? Which states may be claimed and is that set right?
Q2. One logical request can reach a different processing_key when the local policy revision or request revision changes.
    Can that start a second review of the same logical request? Check find_logical_job and the dispatch path.
Q3. scan versus watch: the single-instance lock is taken by watch only. What happens when a manual scan runs beside a
    running watch, and what does seal_interrupted(exclusive=True) do to a job that another live process owns?
Q4. orchestrator._check_ceilings reads the daily request count and cost with a separate query before try_claim. With two
    different processing keys handled in parallel, can the shared daily ceiling be exceeded? Is a reservation atomic?
Q5. If publishing the result or receipt to GitHub fails after the model call, is the model ever called again for the same
    request? Confirm the state, what is retried, and what the operator sees.
Q6. Windows: how is the claude executable started (claude.exe versus claude.cmd, stdin encoding, timeout and process-tree
    kill)? Is anything unsafe or fragile for a Windows host?

Known and to be confirmed only briefly: the author reports 9 entry-point end-to-end tests x3 PASS and 666 PASS / 13 SKIP for
the full suite; those are the author's own results, not yours.

Report BLOCKING findings separately from non-blocking ones, at most 8 findings in total, each with file/function, failure
condition, evidence, minimal fix and how to verify it. State plainly what you could not verify.
