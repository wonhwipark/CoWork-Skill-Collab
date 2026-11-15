---
schema: SKILL_COLLAB_REVIEW_REQUEST_V1
state: SUBMITTED
request_id: REQ-COWORK-AUTO-APPROVAL-V023-R2-20261115
request_revision: 1
project_id: COWORK-AUTO-APPROVAL-20261115-001
work_id: COWORK-AUTO-APPROVAL-20261115-001
skill_id: cowork-review-watcher
package_path: /SKILL-COLLAB/packages/skill-collab-watcher_v0_2_23_1115_DEV_NOT_FOR_DEPLOYMENT.zip
package_file_id: github:REV-COWORK-AUTO-APPROVAL-V023-20261115
package_rev: v0.2.23
package_sha256: f941be8a6b53d00baa10a9b097f234b159470e2aa1242ecc33bcf0bdee080ea7
package_size_bytes: 282340
baseline_package_ref: null
knowledge_refs:
  - path: /SKILL-COLLAB/projects/COWORK-AUTO-APPROVAL-20261115-001/artifacts/v0_2_23/CANDIDATE_MANIFEST.md
    sha256: 1af3bc61d2514e4ce0d33ed16eaae32ccd00e5001f5de9d9657f751d752f9acf
  - path: /SKILL-COLLAB/projects/COWORK-AUTO-APPROVAL-20261115-001/artifacts/v0_2_23/diff_v0_2_22_to_v0_2_23.patch
    sha256: 30c5d7384c7df06f5ca9057a2c98aaedd2e19c0fba1d1fdc2fb6cdb0ae0a7aa0
  - path: /SKILL-COLLAB/projects/COWORK-AUTO-APPROVAL-20261115-001/artifacts/v0_2_22/diff_v0_2_21_to_v0_2_22.patch
    sha256: 94bceec69410688f9c99dccf6e024ff6a0fb7be425e152361a7016b4d56f0ef8
consumer_profiles: [windows-single-user-watcher]
reviewer_os: WINDOWS
test_policy: STATIC_ONLY
run_policy_ref: POLICY-STATIC-V1-LARGE
output_contract: SKILL_COLLAB_REVIEW_RESULT_V1
goal: independent R2 bounded automatic approval review of frozen v0.2.23, one call, max USD 3
---

# Independent R2 — CoWork auto-approval LIVE candidate v0.2.23

**Hard limit: exactly 1 independent Claude review, POLICY-STATIC-V1-LARGE, maximum USD 3.00.** No rerun, no subagents, no followup paid call. A user approved the combined bounded-auto-approval program and has now explicitly requested carrying v0.2.23 through automatic approval; this note alone does not authenticate execution. The existing Windows host must validate the real authorized approval, trust root, budget and pinned inputs before dispatch.

Independently inspect security and integrity of GPT-created REQUEST → protected delegation → signer-verified APPROVAL_SIG → READY posted LAST → single GitHub LIVE watcher 1 review. v0.2.20 remains installed; v0.2.23 is NOT FOR DEPLOYMENT until this review and GPT decision. Read pinned manifest and two patches first, then inspect only relevant ZIP modules/tests. The author reports 890 PASS/12 SKIP, SHADOW 8/8: treat those as self-test claims, not proof.

Priorities (budget first):
1. B1: auto reservation + watcher dispatch identity-union costs/counts under KST day/month, delayed costs, malformed audit logs, missing max_budget, same review and distinct requests, race/DB restore. Find paths exceeding 2 calls/day, USD 3/day, USD 10/month, USD 1/request.
2. B2: delegation shrink/revoke after reserve, before signing and before each publication, terminal POLICY_STOPPED, signer/READY bytes verification, crash/recovery and UNCERTAIN, no duplicate paid calls.
3. M1: within-process and cross-process concurrent RESERVED handling, same review signed more than once, multiple task instances, replay.
4. M2 and v0.2.23: regex fullmatch and owner allowlist for COWORK- (7 chars), L1-WORKSPACE-, adjacent/Unicode/path-lookalike project IDs, mismatched project_id/work_id, skills exact and large policy denied by standing delegation.
5. Request/pin identity, GitHub repository id refresh, source SHA/CRC, ZIP file symlinks, authorization file handling, installation/rollback and notifier: remaining risk and realistic negative tests.

Output: concise BLOCKING / MAJOR / MINOR (max 6 findings). Each finding: exact file/function/condition, reproducer or code evidence, minimal corrective action, test. State clearly what could not be verified. **No deployment, no Windows Task/DB/key change, no PUBLIC release.** Do not trigger second model call if result publication fails; publish-only recovery.
