---
schema: SKILL_COLLAB_REVIEW_REQUEST_V1
state: SUBMITTED
request_id: REQ-COWORK-V035-WATCHER-REVIEW-20261123
request_revision: 1
project_id: COWORK-AUTO-APPROVAL-20261115-001
work_id: COWORK-AUTO-APPROVAL-20261115-001
skill_id: cowork-review-watcher
package_path: /SKILL-COLLAB/packages/v0_2_35_intent_scope_candidate.zip
package_file_id: github:REQ-COWORK-V035-WATCHER-REVIEW-20261123
package_rev: v0.2.35
package_sha256: 658a6f3da8bd018b96b64453892aec77d96868e19bc5788745c1591b1729a740
package_size_bytes: 307418
baseline_package_ref: v0.2.34 (ecb071c4a57b48d9d3ff00e713df35fc086db7c1127b5dc31ef00c358f4f2160, previous candidate)
knowledge_refs: []
consumer_profiles: [windows-single-user-watcher]
reviewer_os: WINDOWS
test_policy: STATIC_ONLY
run_policy_ref: POLICY-STATIC-V1
output_contract: SKILL_COLLAB_REVIEW_RESULT_V1
goal: One independent Windows Claude Code static review of the v0.2.35 watcher candidate (commit-pinned review intent, dispatch idempotency), max USD 3
---
# Independent review — CoWork watcher v0.2.35 (F3 commit-pinned intent, F1 revalidation, F2 manifest)

## Intent and authorization boundary
The user approved publication of this exact ZIP (SHA-256 658a6f3da8bd018b96b64453892aec77d96868e19bc5788745c1591b1729a740, 307418 bytes, 114 entries) as the review input for one independent review. The review is requested under the existing protected cowork-review-watcher delegation. It does not install the candidate, change policy, delegation, keys, trust root, tasks or notifier. The protected signer and watcher decide approval and dispatch under their existing gates.

## Review focus
- Commit-pinned review intent: a single snapshot commit C that is a descendant of the request commit A, with identical REQUEST and ZIP bytes; pin of C and the intent bytes hash; revalidation that re-reads the pinned commit.
- Revalidation before signature and before READY: re-verification of the signed intent (signature, expiry, bindings, key status), nonce ownership without re-consumption.
- Dispatch idempotency: one model call per request id, UNCERTAIN sealing, no re-run after interruption.
- Release manifest: 113 listed files match the ZIP bytes.

## Verification already done by the candidate author (not a review result)
Full suite 1075 PASS / 0 FAIL / 8 SKIP (GUI opt-in). QA28 28/28 PASS. Real Git CLI commit-semantics check 6/6 PASS.

## Expected output
Report findings with file/function, failure condition, evidence and proposed fix. Separate BLOCKING from non-blocking.
