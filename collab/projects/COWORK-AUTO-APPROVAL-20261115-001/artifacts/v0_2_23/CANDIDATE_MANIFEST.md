# CANDIDATE_MANIFEST — CoWork watcher v0.2.23 (approved-prefix compatibility fix) — development_not_for_deployment

Work: COWORK-AUTO-APPROVAL-20261115-001. Candidate: skill-collab-watcher_v0_2_23_1115_DEV_NOT_FOR_DEPLOYMENT.zip (282,340 B, sha256 f941be8a6b53d00baa10a9b097f234b159470e2aa1242ecc33bcf0bdee080ea7).
Base: v0.2.22 (sha256 1b67de37…). Baseline of the deployed LIVE watcher: v0.2.20 (unchanged).
**No independent R2 review of this candidate exists and none was requested. Nothing here is installed, enabled, signed or approved. No REQUEST, READY or approval exists for it.**

## The one change (diff_v0_2_22_to_v0_2_23.patch, 5 files, 145 lines)
- `auto_approval.py::_families` (project families). v0.2.22 required at least 8 characters, so the owner-approved family "COWORK-" (7 characters) was refused and the
  whole protected delegation failed to load. The rule is now: a word-and-dash prefix that ends with '-' (words of letters and digits separated by single dashes),
  at least 7 characters, no wildcard, no spaces, no leading dash, no bare word. Pattern: `[A-Za-z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)*-`.
  Matching is unchanged: a project belongs to a family only if it continues after that prefix. Skills stay an exact list.
- Accepted now: "COWORK-", "L1-WORKSPACE-", "ABCDEF-" (the shortest well-formed family). Still refused: "*", "COWORK-*", "COWORK -", "CO WORK-", "L1-", "A-B-C-",
  "-------", "-COWORK-", "COWORK", "L1-WORKSPACE", "ABCDE-".
- Version 0.2.23; runbook title; new test file tests/test_v023_prefix_compat.py.

## Trade-off stated plainly
The minimum drops from 8 to 7 characters. That lets a 7-character family such as "ABCDEF-" be listed. The protection is the owner's explicit list, not the minimum
length; the minimum only blocks trivially broad or malformed entries. A reviewer may judge whether 7 is the right floor.

## Author's own results (NOT independently reproduced)
- Old candidate v0.2.22 with the new test file: 5 FAILED (the 3 approved-scope approvals, the approved-families load, and the 7-character boundary), 19 PASSED
  (all negative tests). The failures are the intended proof that the approved scope was refused.
- Fixed v0.2.23: test venv 890 passed / 12 skipped; operating Python 3.11.9 890 passed / 12 skipped; both on the extracted final ZIP.
- Isolated real-CLI shadow tests (fake GitHub, counting stub claude, throw-away key): 8/8 PASS on the final tree.
- Isolated install/rollback rehearsal on a copy of the deployed v0.2.20 tree: ALL_PASS.
- The v0.2.22 findings tests (B1, B2, M1, M2) still PASS on v0.2.23.

## Questions for the reviewer
1. Does the new pattern admit anything outside the owner-approved shape (Unicode letters, lookalikes, very long names, case)?
2. Is 7 characters the right floor, or should an explicit approved-prefix list be used instead?
3. Any path where the shorter floor changes the outcome for an existing v0.2.22 delegation? (None known; the v0.2.22 tests still pass.)
Windows only; Linux, in-house LLMs and MCP out of scope.
