---
schema: SKILL_COLLAB_REVIEW_REQUEST_V1
state: SUBMITTED
request_id: REQ-COWORK-V033-R2-WATCHER-REVIEW-20261122
request_revision: 1
project_id: COWORK-AUTO-APPROVAL-20261115-001
work_id: COWORK-AUTO-APPROVAL-20261115-001
skill_id: cowork-review-watcher
package_path: /SKILL-COLLAB/packages/v0_2_33_r2_intent_wired_candidate.zip
package_file_id: github:REQ-COWORK-V033-R2-WATCHER-REVIEW-20261122
package_rev: v0.2.33-r2
package_sha256: 23579a5c8c6690b5831116410fc623e3a8bbc5c659cb6fdea8628e765fa7c206
package_size_bytes: 301136
baseline_package_ref: skill-collab-watcher_v0_2_29_1120.zip (LIVE host-reported baseline, unchanged)
knowledge_refs: []
consumer_profiles: [windows-single-user-watcher]
reviewer_os: WINDOWS
test_policy: STATIC_ONLY
run_policy_ref: POLICY-STATIC-V1
output_contract: SKILL_COLLAB_REVIEW_RESULT_V1
goal: One independent Windows Claude Code static review of the v0.2.33 r2 intent-wired watcher candidate, max USD 3
---
# Independent review — CoWork watcher v0.2.33 r2 (review-intent wiring, dispatch idempotency)

## Intent and authorization boundary
The user explicitly allowed publication of this exact ZIP (SHA-256 23579a5c8c6690b5831116410fc623e3a8bbc5c659cb6fdea8628e765fa7c206, 301136 bytes, 111 entries) as the review input. This request asks one independent Windows Claude Code static review of that watcher candidate. It does not install the candidate, change live policy, widen delegation, change signer keys, or publish READY manually. The protected signer and watcher decide approval and dispatch under their existing gates.

## Review focus
- Review-intent verification connected to the approval path: signature, exact request/revision/skill/commit/SHA/size binding, expiry, same-second time comparison, predates-request rule, one-time nonce consumption in a transactional store.
- Revalidation before signature and before READY: consumed-nonce ownership, intent key status, delegation status; no bypass of the protected delegation.
- Per-request dispatch: at most one model call per request id across OS processes, UNCERTAIN sealing after interruption, no re-run after a crash inside the model call.
- Removal of the CLI budget argument and per-request cost gates in the review path, with the protected signer's own gates intact.

## Verification already done by the candidate author (not a review result)
Full suite 1014 PASS / 0 FAIL / 12 SKIP on the candidate host. Two OS-process dispatch race and crash tests passed. These are development results, not this review.

## Expected output
Report findings with file/function, failure condition, evidence and proposed fix. Separate BLOCKING from non-blocking.
