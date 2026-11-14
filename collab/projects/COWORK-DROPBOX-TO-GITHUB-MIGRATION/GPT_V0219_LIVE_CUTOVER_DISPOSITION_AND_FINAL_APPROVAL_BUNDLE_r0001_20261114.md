# GPT 최종 컷오버 판정 — v0.2.19 및 남은 1회 승인 묶음
- Revision: r0001 / 2026-11-14 KST
- Repository: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`
- Relative path: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_V0219_LIVE_CUTOVER_DISPOSITION_AND_FINAL_APPROVAL_BUNDLE_r0001_20261114.md`
- Work ID: `COWORK-DROPBOX-TO-GITHUB-MIGRATION`
- Source: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CLAUDE_GITHUB_LIVE_CUTOVER_EXECUTION_RESULT_FOR_GPT_20261114.md`
- Git blob verified by GitHub fetch: `bc0c7b3f90c919e31de485182ade6a94f8ecb0b6`
- Host result commit (per CURRENT.md): `ed007279b1fd56af24969c86817271adc2640c48`
- **GPT_DISPOSITION=ACCEPT_PREPARATION / CUTOVER_BLOCKED**
- **USER_APPROVED_LIVE_INTENT=YES; ACTUAL_LIVE=NO; ACTIVE_PROVIDER=NONE; MIGRATION_NOT_CUTOVER**
- `CLASSIC_PAT` continued use confirmed by user's binding preference; no more token type discussions.

## 1. Acceptance / verification boundary

1. Windows host reported 0 model calls, $0 new review cost, 0 operating DB/Task/Notifier/package changes and no LIVE cutover. Original DB main+WAL unchanged; historical 60 COMPLETE, 1 CONFLICT, 1 PENDING preserved.
2. `v0.2.19` fixes N1 using **create-only remote dispatch reservation before starting a paid reviewer**; local state lost after reservation causes `REVIEW_UNCERTAIN` rather than duplicate model call, and remote access failure prevents launch. Crash injection + resumed/old-backup tests and live GitHub isolated branch reservation are reported PASS. **Self tests only**: venv `673 passed/12 skipped`, host interpreter `606 passed/17 skipped`. Repo ID runtime binding N2 preserved.
3. Candidate `skill-collab-watcher_v0_2_19_1114_DEV_NOT_FOR_DEPLOYMENT.zip` reported **239143 B**, SHA-256 `6e7fee3340cc6d0282d1c18fe3db42a90360259dd73fa6d7c0a7698af7afe5c0`, 93 files, CRC/secret scan PASS by host. ZIP + `REVIEW_MANIFEST.md` + diff indexed at `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/review-inputs/REV-COWORK-V0219-20261114/`. GPT independently **read the manifest**, which states no REQUEST/READY. GitHub's text fetch for raw binary ZIP returned UnicodeDecodeError: **GPT independent raw ZIP SHA/CRC=NOT_RUN**. Host must rehash original bytes before review dispatch.
4. Notifier **newly discovered regression**: single global `last_id` makes new GitHub DB alerts silently skipped after provider switch. Host prepared provider-specific watermark candidate and 11 non-sending checks PASS; **not installed**.
5. Existing Dropbox request `L1-KNOWLEDGE-ROADMAP-DESIGN-20261109-001` PENDING stays in preserved historical DB, **not imported to GitHub**. Must not disappear or be replayed as new paid review; user/operational policy can later resubmit if required. It is explicitly isolated legacy pending, not completed.
6. Recovery rehearsal copied main+WAL to isolated backup and restored there, integrity OK per host. No production restore/cutover rehearsal. Actual operational Python 3.11.9 lacks `cryptography` so signed approval verifier would fail closed. Notifier runs; Dropbox reviewer watcher and Bridge/Updater Task disabled per host. GitHub watcher Task does not exist.
7. No v0.2.19 independent Claude review; previous R2 v0.2.17 review **cannot be inherited**.

## 2. GPT acceptance

| Item | Verdict | Boundary |
|---|---|---|
| Classic PAT real GitHub write / Watcher upload | ACCEPT (HOST_PASS, isolated branch) | No token replacement demanded |
| N1 remote dispatch reservation + crash matrix | ACCEPT DEVELOPMENT / REVIEW_REQUIRED | Require independent scrutiny of atomicity, owned vs foreign reservation, old backups, revision changes, usage-limit retry, double worker, transient GitHub error |
| N2 numeric repo ID | ACCEPT SELF_TEST / REVIEW_REQUIRED | Verify same package after fixed SHA |
| Candidate ZIP/manifest/diff | ACCEPT PREPARED / RAW_HASH_INDEPENDENTLY_NOT_RUN | Host must recheck before committing new REQUEST |
| Notifier per-provider watermark | ACCEPT PREPARATION / HOST_INSTALL_NOT_RUN | Validate no silent missed new notifications and no old duplicate notifications |
| Pending legacy request & rollback | ACCEPT PRESERVATION / LIVE_GUARD | Never silently mark pending as completed or trigger duplicate paid call |
| Cutover | BLOCKED | No operating modification, no LIVE until reviewed, installed and verified |

## 3. One combined approval bundle: do NOT request general LIVE approval again

**Item A: exactly one paid independent Claude review, not yet approved.**
- Target review request ID: `REQ-COWORK-V0219-R2-20261114` (proposed new distinct ID)
- Review input: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/review-inputs/REV-COWORK-V0219-20261114/`, target exact candidate ZIP.
- Package expected SHA-256: `6e7fee3340cc6d0282d1c18fe3db42a90360259dd73fa6d7c0a7698af7afe5c0`, size 239143 B; validate **raw ZIP bytes and manifest** before requesting. If mismatch, STOP. Do not relabel or silently swap target.
- Policy `POLICY-STATIC-V1-LARGE` / R2; `MAX_MODEL_CALLS=1`, **MAX_COST_USD=3.00**, `review_attempt=1`, independent *separate review session* of N1 and N2 plus diff v0.2.17→v0.2.19. Other historical requests/R2 must not be re-run; on interrupted/unknown state, fail closed 0 retries unless new approval.
- Signed approval/request/READY procedure only after this **specific paid review item is explicitly approved**. Preserve receipts and remote readback, self-test != independent review.
- If BLOCKING finding, do not deploy or spend on another review without new narrow approval; fix and report candidate only.

**Item B: narrow Windows operating changes, not yet individually approved.**
1. Pin/verify `cryptography` dependency in Windows operating Python 3.11.9. Backup environment/package metadata, install only necessary version on operating interpreter, verify Ed25519 real approval E2E and regressions, rollback on failure.
2. Replace existing Notifier only with tested provider-specific DB/cursor/watermark candidate; back up current config/watermark; no duplicate old messages, no lost new GitHub messages; dry-run/non-sending verification before any actual notification. Live Telegram sending only as part of verified new GitHub provider normal authorized events; do not send test or replay notices.
3. Install one GitHub watcher v0.2.19 **only after independent review PASS and all gates** into separate Windows state folder/config/Task, preserving original Dropbox watcher/DB/WAL/SHM/old Task disabled. Run isolated preflight; one active provider only. CUTOVER at end after checkout and no unsettled replay. Verify 2 cycles+restart, readback, notifier event path (prefer no model call), correct signed READY only, rollback readiness; fail closed stop on any discrepancy.
- **No original DB overwrite, no migration of that one pending item into a LIVE request, no unapproved PUBLIC release, no key rotation, no automatic extra paid reviews.** The LIVE intent is already explicitly approved by the user; avoid another generic LIVE confirmation.

**Current approval statuses:** `PAID_REVIEW_APPROVAL=AWAITING_EXPLICIT_USER_ACTION`; `OPERATING_CHANGE_APPROVAL=AWAITING_EXPLICIT_USER_ACTION`. This written proposed bundle is **not** the approval/READY itself. Only after user's direct confirmation may the operations and one model call begin.

## 4. Execution sequence after specific approvals

1. Windows Claude Code read `collab/START_HERE.md`, this file and CURRENT top. Validate branch/repo, v0.2.19 fixed ZIP raw byte hash/CRC and diff; pin commit A.
2. Stage signed `REQUEST/READY` for **one** v0.2.19 R2; reviewer independent from developer; invoke once within $3 with receipts. Stop on invalid approval, uncertainty, blocking review, exceeded cost; no replays.
3. On PASS: pin verified install ZIP and cryptography runtime after safe local backup and isolated compatibility test; install Notifier candidate and GitHub watcher only with authorized scope. Block if individual operating permission absent.
4. Check legacy request preservation, provider-unique cursors, notifier watermark, main/WAL/SHM invariants, single process/lease/Task, restore plan. Enable GitHub LIVE **once** and confirm running state; never start old Dropbox watcher in parallel.
5. Verify two cycles plus restart, no duplicated paid calls or notifications, normal publish-only sample/fixture without new paid reviewer, event/readback. On failure stop GitHub provider, preserve both DBs and logs, restore config; only activate Dropbox under separate rollback authorization/contract.
6. Only when host evidence confirms: `ACTIVE_PROVIDER=GITHUB`, `CUTOVER=LIVE`, `INDEPENDENT_REVIEW=PASS`, `HOST_APPLIED=PASS`. Publish `CLAUDE_V0219_R2_AND_GITHUB_LIVE_ACTIVATION_RESULT_FOR_GPT_20261114.md`, CURRENT, TRACKER to PRIVATE main PR-free and readback SHA/bytes. If not, report `BLOCKED` with exact reasons; no false PASS.

## 5. NEXT_ONE_ACTION

User can approve **both A and B together** with a single reply such as `v0.2.19 R2 리뷰 1회 최대 $3 및 위 운영 변경 3종을 승인해. LIVE 전환 승인 유지.` Then prepare one-shot Windows execution handoff bound to this exact approval, no further generic LIVE approvals. If only part approved, only that part can run; leave other blockers isolated.

`ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER` until measured Windows host activation.
