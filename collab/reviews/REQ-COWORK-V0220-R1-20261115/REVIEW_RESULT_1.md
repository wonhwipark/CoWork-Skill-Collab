---
schema: SKILL_COLLAB_REVIEW_RESULT_V1
review_id: "REQ-COWORK-V0220-R1-20261115|1|6a8626375e5e711535abdd261ff48781114802bb345cabe2ed5940b75968f386|1"
responds_to_request_id: "REQ-COWORK-V0220-R1-20261115"
responds_to_request_revision: "1"
package_sha256: "6a8626375e5e711535abdd261ff48781114802bb345cabe2ed5940b75968f386"
skill_id: "cowork-review-watcher"
run_policy_ref: "POLICY-STATIC-V1"
knowledge_refs: [{"path": "/SKILL-COLLAB/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/review-inputs/REV-COWORK-V0220-20261115/REVIEW_MANIFEST.md", "sha256": "8be786ec0566a3828608822ff8a4361acfb915fe6a2f1fc82933d13584678033"}, {"path": "/SKILL-COLLAB/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/review-inputs/REV-COWORK-V0220-20261115/diff_v0_2_19_to_v0_2_20.patch", "sha256": "f58c3c90f4eafc82a8a0ca19efe0b2ec42a37f6c6d183d25f5976d6e31ec0fb2"}]
consumer_profiles: ["windows-single-user-watcher"]
reviewer_os: WINDOWS
review_scope: CODE_REVIEW
test_policy: "STATIC_ONLY"
execution_status: COMPLETED
limitations: ["static review by an automatically started Claude Code process; no package code was executed", "knowledge files were delivered as the REQUEST pinned them; which parts were actually read is reported by the reviewer in the text", "reviewer host is Windows; Linux, in-house LLM and MCP behaviour are not verified by this review"]
---

# 리뷰 결과

No `repository_id` usage inside `shadow_guard.py`, confirming SHADOW doesn't bypass this check. I now have sufficient evidence to write the report.

---

# R1 delta review — CoWork watcher v0.2.20 (REQ-COWORK-V0220-R1-20261115)

## BLOCKING findings

None found. The fix matches the R1 patch claims: `repository_id()` (`skill_collab_watcher/github_transport.py:157-167`) no longer has a cache field, performs a fresh `GET /repos/{repo}` on every call, and the only call site (`orchestrator.py:443`, inside `_check_approval`) runs that GET before every approval verification, for every scan cycle, on the same long-lived transport object.

## Non-blocking findings

**1. `orchestrator.py:448` — mismatch check silently permits a missing id.**
`if remote_repo_id is not None and remote_repo_id != str(trust.repo_id):` — but `repository_id()` (github_transport.py:157-167) never returns `None`; it either returns a non-empty string or raises `TransportError`. So the `remote_repo_id is not None` guard is dead code reachable only if a future change made `repository_id()` return `None` on some path without raising. Today this is harmless (not a live bug), but it's a latent fail-open trap: if someone later "fixes" `repository_id()` to return `None` for some edge case instead of raising, the mismatch check would silently skip verification for that case. Minimal fix: drop the `is not None` clause, or add a comment at the call site noting the invariant it depends on. Verify by reading `github_transport.py:164-167`: every return path other than the one `return str(value).strip()` raises.

**2. Q2 case "id missing or blank" is handled, but only on the GET path, not via the empty-dict fallback used by `ensure_auth`.**
For 403/timeout/5xx/429, `_get` raises `AuthRequired`/`TransientTransportError`→caught as `TransportError`/`AuthRequired` at `orchestrator.py:444`, producing `APPROVAL_REPO_ID_UNVERIFIABLE` with `retry=True`, no model call — fail closed, verified against `github_transport.py:127-138`. For "id missing or blank or bool", `github_transport.py:165-166` raises `TransportError("GitHub returned no repository id")`, caught the same way — also fail closed. I could not find a code path where `repository_id()` returns successfully with an empty/falsy value; this is consistent with GPT's manifest claim. Nothing to fix; stating this explicitly because it's exactly Q2's enumerated case list.

## Answers to the Questions

**Q1 — reused repo id from an earlier cycle?** No path found. The `_repo_id` field is removed (confirmed via diff and by reading the current `__init__`, `github_transport.py:65-77`, which has no such field). The only caller is `_check_approval`, called fresh every scan cycle at `orchestrator.py:648`. `ensure_auth()` (`github_transport.py:151-155`) and the upload/download/list paths never read or store the id. No grep hit for `repository_id`/`_repo_id` outside these two files and `transport_base.py`'s abstract declaration. SHADOW (`shadow_guard.py`) does not reference `repository_id` at all, so it cannot be a bypass for this check specifically — but note SHADOW was out of deep scope here (see "left unverified").

**Q2 — fail-closed matrix.** Verified by reading code (not by running tests): correct id → proceeds; different id → `APPROVAL_REPO_ID_REMOTE_MISMATCH`, `retry=True`, no model (orchestrator.py:448-451); 403/timeout/5xx/rate-limit → caught as `TransportError`/`AuthRequired` → `APPROVAL_REPO_ID_UNVERIFIABLE`, `retry=True`, no model (orchestrator.py:443-447, github_transport.py:127-138); missing/blank/bool id → `TransportError` → same unverifiable path. All cases retry rather than reject outright, which is correct for transient conditions but means a permanently-repointed repo will retry forever rather than surface distinctly from a transient 5xx — that's an existing design choice (both produce `retry=True`), not a new regression from this patch, so not raised as a finding.

**Q3 — regression risk of the extra GET.** The added GET is identical in cost/shape to the one `ensure_auth()` already performs each cycle elsewhere, so it roughly doubles GitHub API calls per approval check but doesn't introduce a new endpoint or new rate-limit class. `_reserve_dispatch` (orchestrator.py:520-551) and the signature/approval verification (orchestrator.py:452-486) run after `_check_approval` and are unaffected by this change — they don't consult `repository_id`. Cost ceilings (`_check_ceilings`, called later at orchestrator.py:683) are untouched since no model call happens until well after this gate. Concurrent scan+watch: the extra read is a plain GET with no side effects and no shared mutable state beyond the per-object `_server_date`/`_etag` fields (unrelated to repo id), so I see no new concurrency hazard. I did not load-test actual GitHub rate-limit headroom; this is a code-level assessment only.

**Q4 — does the new test prove the property?** Yes, with code read directly (not just trusting the author's claim): `tests/fake_github.py:36,105` shows the fake server's `/repos/{REPO}` GET handler returns `self.repo_id` live on every call — not memoized in the fixture — so flipping `github_env.http.repo_id = "the-repository-was-replaced"` between the two `run()` calls in `test_n2_...` (tests/test_v018_gates.py, added lines) genuinely changes what a fresh GET would return. The test reuses one `GitHubTransport` instance (`shared = make_transport(...)`) across both `run()` calls, matching the real watch loop's one-transport-per-process behavior described in the manifest. It asserts both the behavioral effect (`runner.calls == 1` after the flip) and the specific event (`APPROVAL_REPO_ID_REMOTE_MISMATCH`), so it can't pass for an unrelated reason (e.g., a different gate silently also blocking) without also producing that exact event — unless two independent gates happened to fire on the same cycle, which I did not rule out by execution, only by reading the gate ordering in `_check_approval`, where the repo-id check is the first gate reached after the pin check (orchestrator.py:436-451).

## What I could not verify
- I did not execute any tests; "passes on v0.2.20 / fails on v0.2.19" is the author's claim, read but not reproduced by me (no code execution occurred in this review).
- Did not verify `REPO_ID` constant value in `tests/bundle.py` lines outside the window I read lines up to ~96; inferred from context that it matches the fake server's default `repo_id` so the "correct id" baseline case passes — consistent with test comments but not hex-confirmed.
- SHADOW path (`shadow_guard.py`) was only grep-checked for `repository_id` references, not fully read — I can state it has none, but did not review its overall approval logic for a parallel/independent bypass of N2.
- Actual GitHub API rate-limit behavior under the doubled GET load — assessed from code shape only, no live or load testing.
- Linux/in-house-LLM/MCP behavior — explicitly out of scope per request, Windows-only review.

## Knowledge files read
- `__SKILL_COLLAB_CONTEXT__/01_REVIEW_MANIFEST.md`
- `__SKILL_COLLAB_CONTEXT__/02_diff_v0_2_19_to_v0_2_20.patch`
- `__SKILL_COLLAB_CONTEXT__/FILE_INDEX.txt`

## Consumer profile judged against
`windows-single-user-watcher` (single long-running process, one transport object reused across scan cycles, as stated in the manifest and request).

## Proposed corrections to common knowledge (GPT decides)
- Minor: the manifest's Q2 wording ("id missing or blank") maps in code to a single catch-all `TransportError` branch that also covers bool values and non-str/int types — worth noting in future manifests that this is one branch, not several, so reviewers don't go hunting for separate handling.
- Suggest the dead-code guard in finding #1 (`remote_repo_id is not None`) be tracked as a tiny cleanup item for a future low-priority patch, not blocking for R1.
