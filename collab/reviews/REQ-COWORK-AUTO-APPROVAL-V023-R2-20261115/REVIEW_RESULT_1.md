---
schema: SKILL_COLLAB_REVIEW_RESULT_V1
review_id: "REQ-COWORK-AUTO-APPROVAL-V023-R2-20261115|1|f941be8a6b53d00baa10a9b097f234b159470e2aa1242ecc33bcf0bdee080ea7|1"
responds_to_request_id: "REQ-COWORK-AUTO-APPROVAL-V023-R2-20261115"
responds_to_request_revision: "1"
package_sha256: "f941be8a6b53d00baa10a9b097f234b159470e2aa1242ecc33bcf0bdee080ea7"
skill_id: "cowork-review-watcher"
run_policy_ref: "POLICY-STATIC-V1-LARGE"
knowledge_refs: [{"path": "/SKILL-COLLAB/projects/COWORK-AUTO-APPROVAL-20261115-001/artifacts/v0_2_23/CANDIDATE_MANIFEST.md", "sha256": "1af3bc61d2514e4ce0d33ed16eaae32ccd00e5001f5de9d9657f751d752f9acf"}, {"path": "/SKILL-COLLAB/projects/COWORK-AUTO-APPROVAL-20261115-001/artifacts/v0_2_23/diff_v0_2_22_to_v0_2_23.patch", "sha256": "30c5d7384c7df06f5ca9057a2c98aaedd2e19c0fba1d1fdc2fb6cdb0ae0a7aa0"}, {"path": "/SKILL-COLLAB/projects/COWORK-AUTO-APPROVAL-20261115-001/artifacts/v0_2_22/diff_v0_2_21_to_v0_2_22.patch", "sha256": "94bceec69410688f9c99dccf6e024ff6a0fb7be425e152361a7016b4d56f0ef8"}]
consumer_profiles: ["windows-single-user-watcher"]
reviewer_os: WINDOWS
review_scope: CODE_REVIEW
test_policy: "STATIC_ONLY"
execution_status: COMPLETED
limitations: ["static review by an automatically started Claude Code process; no package code was executed", "knowledge files were delivered as the REQUEST pinned them; which parts were actually read is reported by the reviewer in the text", "reviewer host is Windows; Linux, in-house LLM and MCP behaviour are not verified by this review"]
---

# 리뷰 결과

## Independent R2 review — v0.2.23 (candidate: 7‑character family prefix fix)

**Scope read:** the only functional change between v0.2.22 and v0.2.23 is in `skill_collab_watcher/auto_approval.py` (`_FAMILY` regex + `_families()`), plus version string, a doc title, and a new test file `tests/test_v023_prefix_compat.py`. I verified this directly against `02_diff_v0_2_22_to_v0_2_23.patch` and by reading the current `auto_approval.py` (lines 160–235). Everything else in the package (state_store.py reservation/union logic, B2 revalidation, M1 in‑progress guard, zip_safety.py) is byte-identical to the v0.2.22 code I also read directly — the diff touches no other file.

### BLOCKING
None found.

### MAJOR
None found.

### MINOR

**1. `auto_approval.py::_families` / `_FAMILY` — new 7-char floor widens the single-point-of-control for a whole project family (acknowledged trade-off).**
- Condition: an owner delegation entry such as `"ABCDEF-"` (7 chars, no vowel/word meaning) now authorizes every future project whose id starts with that 7-byte literal prefix, same as the previously-required 8-char floor did at one character more.
- Evidence: `_FAMILY = re.compile(r"[A-Za-z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)*-")`, `len(x) < 7 or _FAMILY.fullmatch(x) is None` (auto_approval.py:194-205). Confirmed by direct test reading in `tests/test_v023_prefix_compat.py` that `ABCDEF-` is accepted and `ABCDE-` (6) is refused.
- This is not a bug — the author's own manifest states the trade-off plainly and asks the reviewer to judge the floor. I confirmed the regex itself is strict: case-sensitive, ASCII-only (`[A-Za-z0-9]`, no `re.UNICODE` effect since the class is explicit), rejects wildcards, whitespace, leading dash, double dash, bare words, and does not fullmatch Unicode homoglyphs (confirmed by inspection, not execution — see "left unverified" below).
- Fix/consideration: none required for correctness; if GPT wants a tighter control than a bare length floor, an explicit owner-approved-prefix allowlist (manifest's own Q2) is the alternative, trading flexibility for a closed list.
- Verify: `tests/test_v023_prefix_compat.py::test_the_shortest_well_formed_family_is_accepted_at_the_new_minimum` and the malformed-family parametrized test already cover this; no new test needed.

**2. `state_store.py::_auto_usage_locked` — unguarded `.get()` on non-dict JSON `detail` would raise inside the reservation transaction (pre-existing, unchanged by this diff).**
- Condition: `data = json.loads(detail or "{}")` only catches `ValueError`/`JSONDecodeError`; if `detail` parses to valid JSON that is not an object (e.g. `"null"`, `"true"`, `"[1,2]"`), the subsequent `data.get("max_budget_usd")` / `data.get("total_cost_usd")` raises `AttributeError`, which is **not** caught by the `except ValueError` guard and propagates out of `auto_claim`'s `try/except Exception: ROLLBACK; raise`, aborting that reservation attempt (and, since it's in the shared usage-computation path, any call that needs `window_usage`).
- Evidence: state_store.py:356-375 (`_auto_usage_locked`) and :419-421 (reraise). In normal operation `orchestrator.py` only ever writes `json.dumps({...})` dict payloads for `REVIEW_DISPATCHED`/`REVIEW_COST` (orchestrator.py:767-780), so this is not reachable through the watcher's own normal writes — only through a corrupted/hand-edited `audit_log` row, which the REQUEST explicitly asked me to consider ("malformed audit logs").
- This code is identical in v0.2.22 and v0.2.23 — the current diff neither introduces nor fixes it, so it is **not a reason to block v0.2.23** specifically, but it remains open risk carried forward.
- Fix: widen the except to `(ValueError, AttributeError, TypeError)` or validate `isinstance(data, dict)` before `.get()`.
- Verify: add a test that inserts an `audit_log` row with `detail='null'` or `detail='[1]'` directly via SQL, then call `store.window_usage(now)` and assert it returns a sane result instead of raising.

### What I could not verify
- I did not execute any test (own or the author's). The reported 890 PASS/12 SKIP, SHADOW 8/8, and "v0.2.22 findings tests still PASS on v0.2.23" are author claims, not independently reproduced results.
- Unicode/homoglyph behavior of the new regex was reasoned about statically (ASCII-only character classes, case-sensitive `startswith` in `project_scope`), not fuzz-tested.
- I did not re-inspect `tools/approval_signer.py`, `tools/trust_root_tool.py`, `auth_flow.py`, `github_transport.py`, install/rollback scripts, or the notifier — none of these files are touched by this diff, and a prior R-series review presumably already covered them; re-reviewing unchanged files was out of budget/scope for this incremental R2.
- Concurrency/race behavior (M1, B1/B2) was confirmed structurally by reading the code (the `_in_progress` set + lock, `_revalidate` called before every signature/publication, `POLICY_STOPPED` terminal stage, `window_usage` union logic) but not exercised at runtime.
- Linux/in-house-LLM/MCP behavior is out of scope per the manifest and REQUEST; this review is Windows-only static inspection.

### Knowledge files read
- `__SKILL_COLLAB_CONTEXT__/01_CANDIDATE_MANIFEST.md`
- `__SKILL_COLLAB_CONTEXT__/02_diff_v0_2_22_to_v0_2_23.patch`
- `__SKILL_COLLAB_CONTEXT__/03_diff_v0_2_21_to_v0_2_22.patch`
- `__SKILL_COLLAB_CONTEXT__/FILE_INDEX.txt`

### Consumer profile judged against
`windows-single-user-watcher` (sole profile named in the REQUEST).

### Proposed corrections to common knowledge (for GPT to accept/reject)
- Record that the v0.2.21→v0.2.22→v0.2.23 B1/B2/M1 fixes (union usage accounting, pre-publication revalidation, in-process signing guard) remain structurally present and unmodified in v0.2.23 — confirmed by direct read, not just by the manifest's claim that "v0.2.22 findings tests still pass."
- Carry forward MINOR finding #2 (non-dict `detail` JSON crashing `_auto_usage_locked`) as a tracked, pre-existing, non-blocking item for a future hardening pass — it predates v0.2.23 and should not gate this candidate's approval, but should not be forgotten either.

**Bottom line:** the v0.2.23 diff is minimal, matches its stated purpose exactly (lowering the family-prefix floor from 8 to 7 bytes while keeping the shape strict), and I found no new regression or widened attack surface introduced by it. No BLOCKING or MAJOR findings against this specific change; the two MINOR items above are an acknowledged design trade-off and a pre-existing, narrow robustness gap unrelated to this diff. Final accept/reject decision, as always, is GPT's and the user's — this candidate remains NOT FOR DEPLOYMENT pending that decision.
