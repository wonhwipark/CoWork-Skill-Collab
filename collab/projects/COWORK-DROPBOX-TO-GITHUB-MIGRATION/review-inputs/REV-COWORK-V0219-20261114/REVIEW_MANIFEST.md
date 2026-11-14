# REVIEW_MANIFEST — CoWork watcher v0.2.19 candidate (development_not_for_deployment)

Review ID (proposed, NOT requested): REV-COWORK-V0219-20261114. Target: skill-collab-watcher_v0_2_19_1114_DEV_NOT_FOR_DEPLOYMENT.zip.
This file only prepares inputs. No REQUEST, READY or approval exists for this candidate and no model call was made.

## Lineage
v0.2.14 (R1 review: 5 findings) -> v0.2.17 (R2 review: 0 blocking, N1/N2/S1/S2 non-blocking) -> v0.2.18 (N1/N2/S1/S2 fixes) -> v0.2.19
(this candidate). The R2 review covered v0.2.17 only; nothing in v0.2.18 or v0.2.19 has an independent review. Patch: v0.2.17 -> v0.2.19.

## v0.2.18 changes (author's claims)
- N1: before a request is dispatched, a receipt or result already on the remote for the same request id, revision and package stops it.
- N2: before an approval is honoured the provider's own numeric repository id must equal the trust root's repo_id (fail closed).
- S1 dead code removed; S2 taskkill exit status logged.

## v0.2.19 change (author's claim)
Closes the remaining N1 gap "model ran, then the local database or result was lost before the result was uploaded":
- orchestrator._reserve_dispatch writes a create-only remote record `dispatch/<request_id>/DISPATCH_<revision>.md` AFTER the claim and the
  snapshot, BEFORE the job becomes REVIEW_RUNNING and before runner.run.
- RESERVED -> proceed. ALREADY_OURS (record names this job and the local row shows an earlier attempt, i.e. the usage-limit retry) -> proceed.
  FOREIGN (record exists, no local history) -> job REVIEW_UNCERTAIN, no model. ERROR (cannot write/read) -> job back to VALIDATED, wait, no model.
- Behaviour change: without write access to the remote no paid review starts at all.
- tests/test_v019_crash_matrix.py: crash injected at 7 points x state kept/lost, restore of an OLD backup, unwritable/unreadable/foreign
  reservation. tests/test_v018_gates.py: N1, N2 and a composite scenario. Two older tests were adjusted because they assumed a review
  runs while every upload fails.

## Author's own results (NOT independently reproduced)
Test venv 673 passed / 12 skipped; operating interpreter (no cryptography) 606 passed / 17 skipped. ZIP rebuilds to identical bytes, secret scan 0.
On real GitHub (throw-away branch): create-only reservation accepted once, a watcher with no local history gets FOREIGN, another revision
reserves independently, main untouched.

## Known gaps / questions for a reviewer (please judge, do not assume)
1. A crash between the reservation write and the first model second leaves a reservation without any paid work; the request then needs a new
   revision (accepted, fail-closed). Is any state wrongly reported as paid?
2. ALREADY_OURS depends on attempt_count >= 2 in the local row. Can a lost or reset row turn a legitimate retry into FOREIGN (safe) or a
   foreign record into ALREADY_OURS (unsafe)?
3. get_metadata/upload/download_latest pin behaviour on GitHub inside one cycle (reservation visible to the same cycle's reads?).
4. Interaction of the reservation with SHADOW (read-only transport), the daily ceilings, and seal_interrupted.
5. The Notifier is outside this package (single database path and single watermark); it is not part of the review target.
Windows only; Linux, in-house LLMs and MCP are out of scope.
