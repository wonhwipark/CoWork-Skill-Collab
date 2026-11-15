# CANDIDATE_MANIFEST — CoWork watcher v0.2.22 (bounded automatic approval, after GPT static disposition) — development_not_for_deployment

Work: COWORK-AUTO-APPROVAL-20261115-001. Candidate: skill-collab-watcher_v0_2_22_1115_DEV_NOT_FOR_DEPLOYMENT.zip (280,313 B, sha256 1b67de37…d27bd87).
Base for this delta: v0.2.21 (sha256 16921bf4…). Baseline of the deployed LIVE watcher: v0.2.20 (unchanged).
**No independent review of this candidate exists. Nothing here is installed, enabled, signed or approved. No REQUEST, READY or approval exists for it.**

## What changed (patch diff_v0_2_21_to_v0_2_22.patch, 8 files)
- B1 (auto reservation vs watcher dispatch counting): the ceilings are evaluated INSIDE the reservation transaction with ONE identity rule: an identity
  (request id, revision) counts once, at the larger of its automatic reservation and its watcher dispatch cost; day = KST calendar day, month = KST
  calendar month. The earlier `max()` of two disjoint counters that let a third request through is gone. The reservation stores the candidate it approved.
- B2 (protected delegation narrowed between reserve and publish): before every signature and before each remote publication the STORED candidate is
  re-decided against the CURRENT protected delegation (enabled, expiry, repository, project scope, skill, per-request/day/month limits without its own
  reservation, and the unchanged pure gate). A failing check ends the request in stage POLICY_STOPPED: no further signature, no READY, no model; anything
  already published is left as it is.
- M1 (intermittent failure): the root cause is a REAL defect, not a timing issue. A second call for the same request while the first was between its
  reservation and its signature treated the reservation as a crashed attempt and signed again. Reproduced on v0.2.21: 3 of 12 runs failed. Fixed with an
  in-process in-flight guard (the single-instance watcher lock already serialises separate processes). Deterministic regression added.
- M2 (new Work compatibility, stable scope without wildcard): the owner may list exact projects and/or project FAMILIES (prefix ending with '-', at least 8
  characters, no wildcard, no spaces). The skill list stays exact. Two different project ids in one REQUEST are refused explicitly. Real REQUEST V1 files
  carry both fields (equal in every example seen). The pure gate module is unchanged; the verified project is added to the set it checks only after the scope check.
- Version 0.2.22; runbook title.

## Author's own results (NOT independently reproduced)
- Test venv: 866 passed / 12 skipped (v0.2.21: 817/12, v0.2.20: 674/12). Operating Python 3.11.9: 866 passed / 12 skipped. Both on the extracted final ZIP.
- Regression for the findings (tests/test_v022_findings.py, 48 tests): fixed candidate 48/48 PASS; v0.2.21 FAIL on the real findings (B1 approver-level 2, B2 25, M2 9, M1 1).
- Race test 12/12 PASS on the fixed copy (v0.2.21: 3 failures in 12 runs).
- Isolated real-CLI end-to-end (SHADOW-style, fake GitHub, counting stub claude, throw-away key): 8/8 PASS.
- Isolated install/rollback rehearsal on a copy of the deployed v0.2.20 tree: ALL_PASS (upgrade to v0.2.22 equals the ZIP; rollback byte-identical to v0.2.20).
- Mutation check was NOT repeated for v0.2.22 (it was 16/17 for v0.2.21).

## Questions for the reviewer (please try to break these)
1. B1: is the union rule complete? Any path where one request is counted zero times or twice in the day or month window (KST boundaries, watcher costs
   recorded without a dispatch, cost records arriving after the window start, a revision that differs only in format)?
2. B2: are there boundaries left where the current delegation is not re-decided before a signature, an approval publication or a READY publication?
   Is POLICY_STOPPED terminal in every resume path? Does a stopped request ever publish anything?
3. M1: is the in-process guard enough together with the single-instance watcher lock? Any way for two signers to exist in one process or in two processes?
4. M2: can a family prefix match a foreign project (prefix ambiguity, unicode, case, path-like ids)? Can a GitHub document widen scope?
5. Regression risk: the reservation now reads the audit log for the last day of a month window; cost and timing side effects on the watcher's own ceilings.
Windows only; Linux, in-house LLMs and MCP out of scope. Live signing keys were never used by any test; the real-host checks were read-only.
