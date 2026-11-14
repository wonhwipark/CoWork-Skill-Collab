---
schema: SKILL_COLLAB_REVIEW_REQUEST_V1
state: SUBMITTED
request_id: REQ-COWORK-V0217-R2-20261114
request_revision: 1
project_id: COWORK-DROPBOX-TO-GITHUB-MIGRATION
work_id: COWORK-DROPBOX-TO-GITHUB-MIGRATION
skill_id: cowork-review-watcher
package_path: /SKILL-COLLAB/packages/skill-collab-watcher_v0_2_17_1114.zip
package_file_id: github:REV-COWORK-V0217-R2-20261114
package_rev: v0.2.17
package_sha256: 824f26c4e28fcc804ed1dd3942a34408c54b9091be34ecb1693cc4cb9d46df03
package_size_bytes: 232575
baseline_package_ref: null
knowledge_refs:
  - path: /SKILL-COLLAB/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/review-inputs/REV-COWORK-V0217-R2-20261114/REVIEW_MANIFEST.md
    sha256: ee53d49daff277ffaa6d407cc4a7696024b47d7760bfb1c4274e5209bfa0280e
  - path: /SKILL-COLLAB/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/review-inputs/REV-COWORK-V0217-R2-20261114/diff_v0_2_14_to_v0_2_17.patch
    sha256: 84ac72659f0a317914ddf13a144da0ce5befb7325a36e4433597a97160a12700
consumer_profiles: [windows-single-user-watcher]
reviewer_os: WINDOWS
test_policy: STATIC_ONLY
run_policy_ref: POLICY-STATIC-V1-LARGE
output_contract: SKILL_COLLAB_REVIEW_RESULT_V1
goal: R2 structural review of v0.2.17 (usage-limit resume, F1-F5 fixes, scan/watch lock, trust and identity)
---

# R2 structural review of the CoWork watcher v0.2.17

Tier R2 under POLICY-STATIC-V1-LARGE: exactly one review, hard budget USD 3, no follow-up call. Spend your effort on the risky parts below,
not on a line-by-line read of everything. Stop and write the report while you still have budget left: an unfinished review is lost.

Read the two pinned knowledge files first: REVIEW_MANIFEST.md (change groups, the author's claims, the known gaps) and
diff_v0_2_14_to_v0_2_17.patch (the complete change from the already-reviewed v0.2.14). Then read only the package files needed:
skill_collab_watcher/state_store.py, orchestrator.py, review_runner.py, cli.py, config.py, models.py, notify_events.py,
approval.py, signature_backend.py, shadow_guard.py, github_transport.py, and the new tests tests/test_r1_findings.py and
tests/test_usage_limit_resume.py.

Questions (judge each; answer "no finding" with the evidence when it holds):

Q1. v0.2.16 usage-limit wait/resume: can any path start a second paid review for work that already began, lose a job, wait forever,
    or misread the CLI's limit message (time zone, am/pm, date rollover, a normal review text that merely mentions a limit)?
Q2. StateStore.claim (BEGIN IMMEDIATE ceilings + reservation): can two processes or two different keys still exceed the daily dispatch or
    cost ceiling? Can a stale CLAIMED/REVIEW_RUNNING reservation block the whole day forever, or be released wrongly after a crash?
Q3. F1: logical-request lookup across policy revisions, re-signed approvals, cursor loss and rollback. Is the invariant "one paid review per
    request_id|request_revision|package_sha256" now unconditional, and is the author's narrowing of the finding right?
Q4. scan/watch single-instance lock and exclusive seal_interrupted: false seals of a live job, missed seals of a dead job, lock left behind
    after a crash or a SHADOW refusal, exit codes (3 locked, 6 SHADOW refused) on every path.
Q5. A model call succeeded but publishing the result or receipt fails: is the model ever called again? What is retried and what does the operator see?
Q6. Windows timeout handling: claude.cmd wrapper, Popen plus taskkill /T /F, stdin encoding, a failed taskkill, zombie output pipes.
Q7. Trust and identity: repo_id is only a label in the approval/trust root. What can an attacker with repository write access or a forked
    repository do with that? Also the replay protection, expiry, and what happens when the optional cryptography package is missing in the
    interpreter that runs the watcher (does it fail closed?).
Q8. Anything in the combination of these changes (usage-limit deferral + restart + policy revision + cursor loss + lock) that single-feature tests miss.

Report BLOCKING findings separately from non-blocking ones, at most 10 findings in total, each with file/function, failure condition, evidence,
minimal fix and how to verify it. State plainly what you could not verify. Windows only; do not speculate about Linux.
