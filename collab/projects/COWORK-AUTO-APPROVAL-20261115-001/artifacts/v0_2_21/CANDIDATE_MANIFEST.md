# CANDIDATE_MANIFEST — CoWork watcher v0.2.21 (bounded automatic approval) — development_not_for_deployment

Work: COWORK-AUTO-APPROVAL-20261115-001. Candidate: skill-collab-watcher_v0_2_21_1115_DEV_NOT_FOR_DEPLOYMENT.zip. Base: v0.2.20 (the deployed GitHub LIVE
watcher; its independent R1 review passed). **No independent review of this candidate exists. Nothing here is installed, enabled or approved.**
These are review inputs only: no REQUEST, READY or approval exists for this candidate and no model call was made.

## What it adds (author's claims, patch diff_v0_2_20_to_v0_2_21.patch)
A REQUEST without READY can receive APPROVAL_SIG.json and READY.md (create-only, READY last) from the existing signer, inside a delegation stored in a
PROTECTED LOCAL file (AUTO_DELEGATION_V1, default enabled=false). Default state of a watcher without an `auto_approval` config section: unchanged.
- skill_collab_watcher/auto_approval.py (new): delegation reader + Win32 DACL check (SID based), the decision order, ToolSigner (calls the existing
  tools.approval_signer in-process; DPAPI passphrase provider), publication with bounded race handling, crash recovery by stored stage.
- skill_collab_watcher/auto_policy.py (new): GPT's pure gate, byte-identical to the prototype (blob 5308a8d7...). tests/test_auto_policy_gpt_proto.py:
  GPT's 25 tests with one import line changed.
- state_store.py: auto_seen / auto_claims tables, created lazily (only when the feature is configured), atomic reservation (BEGIN IMMEDIATE, one row per
  request+revision, day/month ceilings in the same transaction).
- orchestrator.py (+5 lines): the hook, only for a valid REQUEST without READY, only when the watcher may dispatch (not dry-run, not SHADOW).
- cli.py: builds the approver when `auto_approval` is configured; config-check prints its state without secrets. github_transport.py / transport_base.py:
  download_at_commit, commit_time. validator.py: one optional policy field. notify_events.py: AUTO_SIGNING_UNCERTAIN alert event.
- docs/AUTO_APPROVAL.md.

## Invariants the author wants checked (please try to break them)
1. Nothing is signed unless the protected delegation says enabled=true, is not expired, is ACL-protected, and the request was first seen while enabled and
   its pinned commit is not older than enabled_at (no retroactive start).
2. At most one signature per (request id, revision) ever; a crash after the reservation never leads to a second blind signature; an expired stored
   approval is never re-signed.
3. APPROVAL_SIG.json is published before READY.md; the existing SOURCE_PIN.json is never overwritten; READY bytes are fixed before signing and bound by ready_sha256.
4. The automatic part never starts a review: the unchanged READY checks, N1 remote reservation and the single model call decide.
5. The watcher's own ceilings (POLICY-STATIC-V1 $1, 2 per day / $3) are not relaxed; delegation limits may only be equal or stricter.

## Author's own results (NOT independently reproduced)
Test venv and Windows operating interpreter (Python 3.11.9): 817 passed / 12 skipped each (v0.2.20 baseline 674 / 12). New: 25 GPT + 110 integration/unit + 8
real-CLI end-to-end tests (loopback fake GitHub, counting stub for claude, throw-away key). Mutation check: 16 of 17 deliberate defects killed (the survivor
is an equivalent redundant check). Real-host read-only checks: trust root, DPAPI decryption in memory (no signature), Win32 ACL. Isolated install/rollback rehearsal.

## Known limits / questions
- The signing capability runs inside the watcher process (same Windows account) that also reads GitHub-controlled input: the protection is the gate and the
  fail-closed order, not a separate trust domain. Is any GitHub-controlled byte able to influence the signed fields or the delegation decision?
- The request creation time is the pinned commit's committer date as GitHub reports it (a writer can set it when committing through the API); the first-seen flag is the second guard.
- Time source for day/month keys is the local clock (KST calendar) with the existing clock-skew check against the server.
- The installed Notifier has its own event list (AUTO_SIGNING_UNCERTAIN must be added there when enabled).
Windows only; Linux, in-house LLMs and MCP out of scope.
