# REVIEW_MANIFEST — CoWork watcher v0.2.20 candidate (development_not_for_deployment), R1 delta review

Review ID: REV-COWORK-V0220-20261115. Target: skill-collab-watcher_v0_2_20_1115_DEV_NOT_FOR_DEPLOYMENT.zip (the exact pinned bytes).
Tier R1, POLICY-STATIC-V1, one review, hard budget USD 1. Static only. Only the delta below is in scope; v0.2.19 had a full R2 review.

## Why this candidate exists
The independent R2 review of v0.2.19 (REQ-COWORK-V0219-R2-20261114) reported one BLOCKING finding: GitHubTransport.repository_id() cached the
numeric repository id for the life of the transport object. The real watch loop builds one transport per process and reuses it every cycle, so a
long-running watcher would never notice that `owner/name` had been repointed to another repository, and the N2 check (the server id must equal
the trust root's repo_id before an approval is honoured) stayed green. All other R2 questions had no finding.

## The change (author's claims; patch diff_v0_2_19_to_v0_2_20.patch, 4 files, 77 lines)
- github_transport.py: `repository_id()` no longer caches; every call reads GET /repos/{repo} and returns the id as the server reports it now.
  The `_repo_id` field is removed. Errors unchanged: not visible -> AuthRequired, missing/blank/bool id -> TransportError.
- orchestrator._check_approval (unchanged) calls it before every approval verification; mismatch -> APPROVAL_REPO_ID_REMOTE_MISMATCH (retry, no model),
  read failure -> APPROVAL_REPO_ID_UNVERIFIABLE (retry, no model). Cost: one extra GET per approval check.
- tests/test_v018_gates.py: new test reuses ONE transport across two scans, flips the server's repository id between them, and requires the second
  request to be refused. It fails on v0.2.19 (reproduced: a second review ran) and passes on v0.2.20.
- Version and runbook title only otherwise.

## Author's own results (NOT independently reproduced)
Test venv 674 passed / 12 skipped; operating interpreter 607 passed / 17 skipped (no cryptography); rebuild gives identical bytes; secret scan 0.

## Questions for the reviewer
1. Is any path left on which the repository id of an earlier cycle is reused (other caches, memoisation, the pinned reads, SHADOW, ensure_auth)?
2. Same transport, several scans: correct id, other id, unreadable id (403, timeout, 5xx, rate limit), id missing. Is every case fail closed?
3. Regression risk of the extra GET: rate limits, the N1 remote dispatch reservation, signatures and bindings, cost ceilings, concurrent scan/watch.
4. Does the new test really prove the property?
Windows only; Linux, in-house LLMs and MCP out of scope.
