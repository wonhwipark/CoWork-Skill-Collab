---
schema: SKILL_COLLAB_REVIEW_RESULT_V1
review_id: "REQ-L1-WORK-KNOWLEDGE-FIXED-R1-20261116|1|58d39bcf884d9fbd22d03a14e5fffde5e1b69a8ecec482d2e9c8b2b125add7bb|1"
responds_to_request_id: "REQ-L1-WORK-KNOWLEDGE-FIXED-R1-20261116"
responds_to_request_revision: "1"
package_sha256: "58d39bcf884d9fbd22d03a14e5fffde5e1b69a8ecec482d2e9c8b2b125add7bb"
skill_id: "l1-knowledge-updater"
run_policy_ref: "POLICY-STATIC-V1"
knowledge_refs: []
consumer_profiles: ["work-to-knowledge-design"]
reviewer_os: WINDOWS
review_scope: CODE_REVIEW
test_policy: "STATIC_ONLY"
execution_status: COMPLETED
limitations: ["static review by an automatically started Claude Code process; no package code was executed", "knowledge files were delivered as the REQUEST pinned them; which parts were actually read is reported by the reviewer in the text", "reviewer host is Windows; Linux, in-house LLM and MCP behaviour are not verified by this review"]
---

# 리뷰 결과

# Review: L1 Knowledge ①~④ Fixed Design — REQ-L1-WORK-KNOWLEDGE-FIXED-R1-20261116

## Scope note
This package contains **only 3 non-sensitive Markdown design documents** (README.md, DECISIONS_1TO4.md, REVIEW_QUESTIONS.md) — no skill code, no ZIP, no pinned knowledge files. This is a pure design/requirements review; there is nothing executable to run or test directly.

## Duplicate-execution check (cannot verify myself)
My tool access is restricted to the snapshot directory, so I cannot read `collab/receipts/` or `collab/dispatch/` for the prior `REQ-L1-WORK-KNOWLEDGE-DESIGN-20261115-001` request. I found **no evidence inside this package** of a prior executed review, but I also have no way to confirm it is still unexecuted or that no concurrent run exists. **This must be confirmed by GPT/the watcher before the receipt is finalized** — I am not asserting it is safe, only that I found nothing contradicting it within my restricted view.

---

## BLOCKING

**①-③ backlink mechanism is self-contradictory (DECISIONS_1TO4.md §4, lines 38–40 vs §6 table row for `work-ledger-kernel`, line 71)**
- Failure condition: Decision ③ requires that Work-originated knowledge record a backlink "기존 허용 Kernel 기록 계약 안에서" (within the existing allowed Kernel contract), using `work_refs.REF_TYPES` which the doc itself states (§1, line 15) is limited to `jira, alias, github_pr, p4_cl, code_root` and does **not** include a knowledge-shaped type. The same decision explicitly **forbids** reusing `alias`/`code_root` for this different meaning (line 40). Meanwhile §6 explicitly tells `work-ledger-kernel`'s scope to **preempt** any "신규 Knowledge profile/원장" (new Knowledge profile/ledger).
- Evidence: there is no ref_type and no new-profile path left that satisfies all three constraints simultaneously as written. Decision ③ cannot be implemented literally without either (a) adding a new ref_type/profile to `work-ledger-kernel` — which contradicts the explicit prohibition — or (b) silently reusing an existing ref_type with a different meaning — which is explicitly forbidden.
- Proposed fix: have GPT/user resolve this before implementation — either approve a minimal, proven `knowledge`-shaped ref_type as a justified EXTEND to `work_refs.REF_TYPES` (reversing the §6 prohibition), or define the backlink to live entirely inside the knowledge file's own metadata/front-matter with no Kernel ref_type at all (and drop the "within existing Kernel contract" framing for this path).
- How to verify: T06 below — attempt to create a Work-originated knowledge backlink under the stated constraints and confirm whether any valid code path exists.

---

## MAJOR

1. **Decision ② enforcement mechanism is declared "FIXED" but admittedly unspecified (DECISIONS_1TO4.md §3, line 33)**
   The same section that states the write-block is FIXED also states bootstrap guidance alone does not complete "OS/Git credential 차원의 절대 권한 분리." No concrete mechanism (pre-commit hook, server-side push protection, path canonicalization) is named — only application-level intent in `l1-fix-workflow`. If enforcement is purely inside that skill's own call path, any other tool/raw `git` invocation in the same checkout bypasses it trivially (this is exactly R03/R04). Treat decision ② as "policy FIXED, enforcement mechanism NOT YET FIXED" until a concrete, verifiable boundary is named.
   Verify: T03, T04 below.

2. **Shared-clone concurrency between Workflow `docs_sync` and Updater commit/push is acknowledged but unresolved (§3 line 33, §1 line 13)**
   The doc correctly flags that dirty/untracked checks and competing staging/push on the same clone need a "별도 공통 Git writer의 직렬화/충돌 검사" but no such writer/lock is specified in this package. Without it, decision ④'s CAS/HEAD-recheck guarantees can be undermined by an interleaved Workflow operation on the same working tree.
   Verify: T05 below.

3. **Non-overlapping ≠ semantically safe for structural Markdown changes (R07)**
   Decision ④ item 4 relies on git's native 3-way merge for "겹치지 않는 변경" and treats automatic merge success as merely a preview, not auto-approval — that's good. But nothing in item 4/5 says a detected **rename/move/delete** on the group side during the same window must *always* route to the conflict path rather than being accepted via git's rename-detection heuristics (which can misfire on short/renamed Markdown files). This should be made explicit, not implicit.
   Verify: T10 below.

4. **`knowledge/` coexistence with Kernel exporter is explicitly unverified (§1 line 12), yet §6 only assigns it "보존" obligation, not a regeneration-safety test**
   If `work_ux.export_docs` ever does a full regen of its output tree, an unrecognized `knowledge/` folder sitting alongside `works/`/`index/`/root `README.md` could be silently affected (hidden from README links, or in a worse case touched by a careless regen). The doc defers this to "E2E 미검증" but doesn't list it as a required pre-implementation test.
   Verify: T01, T02 below.

## MINOR (improvement suggestions, not defects)

- Clarify the granularity of "그룹 기준 revision" in §5 item 1/3 — per-file content hash vs. whole-group commit SHA — since 3-way diffing correctness depends on knowing exactly what unit is being compared.
- Decision ④ item 9 (recovery) is thorough but doesn't state a retry-count/backoff bound for "개인 상태만 재시도" — worth a cap to avoid silent infinite retry loops.

---

## REUSE / CONNECT / EXTEND assessment (R10/R11)
The design is largely **REUSE-first and well-disciplined**: git's native 3-way merge, existing `push_guard`, existing Work-ledger ref types, no new storage engine or schema proposed for sync state. The one place it strays into EXTEND territory is the backlink mechanism in decision ③ (see BLOCKING above), and that EXTEND is currently self-contradicted by the same document's own constraints rather than being an approved, minimal, justified addition. No other unnecessary engine/schema expansion was found.

## Proposed T01–T10 (for the eventual code-level review, not run here)
- T01: Confirm `work_ux.export_docs` regen does not delete/overwrite an existing `knowledge/` folder.
- T02: Confirm root `README.md` generation doesn't hide or orphan a `knowledge/` link.
- T03: From outside `l1-fix-workflow`'s own call path, attempt a raw `git add/commit` touching `knowledge/` and confirm whether it's actually blocked, and at what layer.
- T04: Attempt rename/symlink/path-escape writes into `knowledge/` via Workflow and confirm rejection.
- T05: Interleave Workflow `docs_sync` dirty-check with Updater staging/commit on the same clone; confirm serialization prevents mixed/corrupted staging.
- T06: Attempt to create a Work-originated knowledge backlink per decision ③ and determine whether any valid ref_type/profile path currently satisfies the stated constraints (expected to fail given the BLOCKING finding above).
- T07: Base v10 → group advances to v11 (non-overlapping edit) → confirm Preview, user confirmation, and CAS re-check before push.
- T08: Same but overlapping/conflicting edits → confirm auto-publish halts and both sides are shown, no auto-merge.
- T09: Simulate publish success + readback failure → confirm no duplicate group republish, only individual-state retry.
- T10: Simulate a group-side rename/move concurrent with an individual content edit → confirm it is routed to the conflict/user-review path rather than accepted via git's rename heuristics.

## Verdict: **ACCEPT_WITH_CHANGE**
Direction, REUSE priority, optional Work ID, and the Base/Ours/Theirs/CAS/readback/partial-failure sync model are sound and don't require redesign. Required changes before this is implementation-ready:
1. Resolve the backlink/ref_type contradiction in decision ③ (BLOCKING).
2. Name a concrete, verifiable enforcement boundary for decision ② (not just application-level intent).
3. Specify a common-clone serialization mechanism for decision ②/④ concurrency.
4. Make structural (rename/move/delete) changes explicitly fail-closed in decision ④, not merely implicit.

---

**Knowledge files actually read:** README.md, DECISIONS_1TO4.md, REVIEW_QUESTIONS.md (all 3 package files; no pinned knowledge files were listed in this REQUEST).

**Consumer profile judged against:** work-to-knowledge-design.

**Left unverified (explicitly, not assumed safe):**
- Whether the 2026-11-15 prior request remains unexecuted / no concurrent run exists (outside my tool access).
- All claims about actual code in `l1-fix-workflow`, `l1-github`, `work-ledger-kernel`, `l1-knowledge-updater`, `l1sw-dev-knowledge` — none of that code was in this package; everything about it here is the document's own claim, not something I read or ran.
- Actual current folder structure of group `l1sw-dev-knowledge` — not available to me, and the design itself defers to it.

**Proposed corrections to common knowledge (GPT to decide):** record the §4 ref_type contradiction and the recommendation to track "경로 구조 동일" dependency on the real group structure as an explicit implementation precondition rather than a resolved fact.
