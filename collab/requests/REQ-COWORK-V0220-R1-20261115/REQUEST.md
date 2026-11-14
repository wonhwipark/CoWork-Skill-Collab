---
schema: SKILL_COLLAB_REVIEW_REQUEST_V1
state: SUBMITTED
request_id: REQ-COWORK-V0220-R1-20261115
request_revision: 1
project_id: COWORK-DROPBOX-TO-GITHUB-MIGRATION
work_id: COWORK-DROPBOX-TO-GITHUB-MIGRATION
skill_id: cowork-review-watcher
package_path: /SKILL-COLLAB/packages/skill-collab-watcher_v0_2_20_1115_DEV_NOT_FOR_DEPLOYMENT.zip
package_file_id: github:REV-COWORK-V0220-20261115
package_rev: v0.2.20
package_sha256: 6a8626375e5e711535abdd261ff48781114802bb345cabe2ed5940b75968f386
package_size_bytes: 239432
baseline_package_ref: null
knowledge_refs:
  - path: /SKILL-COLLAB/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/review-inputs/REV-COWORK-V0220-20261115/REVIEW_MANIFEST.md
    sha256: 8be786ec0566a3828608822ff8a4361acfb915fe6a2f1fc82933d13584678033
  - path: /SKILL-COLLAB/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/review-inputs/REV-COWORK-V0220-20261115/diff_v0_2_19_to_v0_2_20.patch
    sha256: f58c3c90f4eafc82a8a0ca19efe0b2ec42a37f6c6d183d25f5976d6e31ec0fb2
consumer_profiles: [windows-single-user-watcher]
reviewer_os: WINDOWS
test_policy: STATIC_ONLY
run_policy_ref: POLICY-STATIC-V1
output_contract: SKILL_COLLAB_REVIEW_RESULT_V1
goal: independent R1 delta review of v0.2.20 (repository id no longer cached, repeated scans on one transport)
---

# R1 delta review of the CoWork watcher v0.2.20 (repository id is no longer cached)

Tier R1 under POLICY-STATIC-V1: exactly one review, hard budget USD 1, no follow-up call. You are independent of the author; the author's test
results are claims, not evidence. Be economical: the change is 77 lines. Read the two pinned knowledge files first (REVIEW_MANIFEST.md and
diff_v0_2_19_to_v0_2_20.patch), then at most these package parts: skill_collab_watcher/github_transport.py (repository_id, _get, _raise_for,
ensure_auth, pinning), skill_collab_watcher/orchestrator.py (_check_approval and its call site, _reserve_dispatch) and
tests/test_v018_gates.py (the new test). Stop reading after about 12 tool calls and write the report while budget remains: an unfinished review
is lost and cannot be repeated.

Questions:
Q1. Is any path left on which a repository id from an earlier cycle is reused (other caches or memoisation, pinned reads, SHADOW, ensure_auth)?
Q2. One transport object, several scans: correct id, another id, unreadable id (403, timeout, 5xx, rate limit), id missing or blank. Is every
    case fail closed, with no model started?
Q3. Regression risk of the extra GET per approval check: rate limits, the remote dispatch reservation, signature bindings, cost ceilings,
    concurrent scan and watch.
Q4. Does the new test really prove the property, or could it pass for the wrong reason?

Report BLOCKING findings separately from non-blocking ones, at most 6 findings in total, each with file/function, failure condition, evidence,
minimal fix and how to verify it. State plainly what you could not verify. Windows only.
