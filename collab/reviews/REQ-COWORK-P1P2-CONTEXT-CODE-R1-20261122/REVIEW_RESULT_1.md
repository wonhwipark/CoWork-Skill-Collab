---
schema: SKILL_COLLAB_REVIEW_RESULT_V1
review_id: "REQ-COWORK-P1P2-CONTEXT-CODE-R1-20261122|1|35de54934944807518e0141daaedde1888a42c08c1d264584e9b341f65dcd5f3|1"
responds_to_request_id: "REQ-COWORK-P1P2-CONTEXT-CODE-R1-20261122"
responds_to_request_revision: "1"
package_sha256: "35de54934944807518e0141daaedde1888a42c08c1d264584e9b341f65dcd5f3"
skill_id: "cowork-context-design"
run_policy_ref: "POLICY-STATIC-V1"
knowledge_refs: []
consumer_profiles: ["cowork-p1p2-context-code-design-and-e2e-plan-review"]
reviewer_os: WINDOWS
review_scope: CODE_REVIEW
test_policy: "STATIC_ONLY"
execution_status: COMPLETED
limitations: ["static review by an automatically started Claude Code process; no package code was executed", "knowledge files were delivered as the REQUEST pinned them; which parts were actually read is reported by the reviewer in the text", "reviewer host is Windows; Linux, in-house LLM and MCP behaviour are not verified by this review"]
---

# 리뷰 결과

## Independent review — REQ-COWORK-P1P2-CONTEXT-CODE-R1-20261122

Scope read: `context_query.py`, `test_context_query.py`, `context-view.js`, `index.html`, and the four CoWork design/result/handoff docs. Static read-only review only; no execution performed.

### BLOCKING
None found.

### MAJOR

**1. Unhandled `ValueError` in `related()` can crash every `snapshot()` call as `collab/requests/` grows**
- File/function: `cowork/collab/dashboard/context_query.py:96-104` (`related`), called unguarded from `snapshot()` at `:179`.
- Failure condition: `related()` does `candidates = sorted(request_dir.glob("REQ-*"))` over **all** REQUEST folders in `collab/requests/` (not filtered by `work_id` yet), then raises `ValueError("request scan limit exceeded")` if there are more than `max_requests=200`. `snapshot()` calls `related(root, work)` directly with no try/except, so this exception propagates out of `main()` uncaught.
- Evidence: `test_request_scan_is_bounded` (`test_context_query.py:90-96`) only asserts that `related()` itself raises — there is no test that exercises `snapshot()` (the actual CLI entry point) once the bound is exceeded. Since the cap counts *all* REQ-* folders regardless of which Work they belong to, and CoWork's own review workflow continuously creates new `REQ-*` folders (this very request is one more), the tool will eventually — and foreseeably — fail for every topic/question, not just the one tied to an oversized history.
- Proposed fix: catch the bound-exceeded condition inside `snapshot()` (or inside `related()` itself) and return a structured degraded state, e.g. `{"state": "RELATIONS_SCAN_LIMIT_EXCEEDED", ...}` instead of raising past the public API boundary. Add a test that calls `context_query.snapshot(...)` (not just `related()`) with >200 request folders and asserts a graceful, non-crashing result.
- How to verify: create >200 `collab/requests/REQ-*` directories in a temp root and call `context_query.snapshot(root, "질문", topic="skill")`; confirm it returns a dict rather than raising.

### MINOR

**2. `safe_file()` Windows drive-absolute escape is only caught post-hoc, after a stat/is_file oracle**
- File/function: `context_query.py:48-68` (`safe_file`).
- Failure condition: the function rejects `rel` strings starting with `/` or containing `\\`, but does not reject Windows drive-absolute forward-slash paths such as `"C:/windows/win.ini"`. `pathlib`'s `root / rel` silently discards `root` when `rel` is itself absolute (drive-qualified), so `target = root / rel` becomes the attacker-chosen absolute path. The function still calls `target.is_file()` / `target.stat().st_size` on that escaped path *before* the final `target.resolve().is_relative_to(root.resolve())` containment check, which is what ultimately returns `None` and prevents an actual read.
- Evidence: code at `context_query.py:54,61,64`; no current call site passes such a `rel` (all call sites use literal paths or `REQ_ID`-regex-validated folder names, so this is not exploitable today), but the function is general-purpose and the only safety net is the final containment check, not an upfront rejection.
- Proposed fix: add an explicit guard before any filesystem access — e.g. `if Path(rel).is_absolute() or Path(rel).drive: return None` — so attacker-shaped input never reaches `is_file()`/`stat()` even as an existence/size oracle.
- How to verify: add a Windows-specific unit test, e.g. `self.assertIsNone(context_query.safe_file(self.root, "C:/Windows/System32/drivers/etc/hosts"))`, and confirm it returns `None` without any stat call on the real path (can be checked by passing a non-existent drive letter and confirming no `OSError`/timing difference).

**3. Keyword-substring router (`choose`) has an unconditional "skill" fallback and can misclassify on coincidental substrings**
- File/function: `context_query.py:30-45` (`choose`).
- Failure condition: routing is plain substring containment over short Korean/English tokens (e.g. `"그룹"` for knowledge, `"live"`, `"정책"`). Any question with zero keyword overlap silently routes to `"skill"` regardless of actual intent, and short generic tokens can match unrelated questions (e.g. `"그룹웨어"` would score as `knowledge`). This is exactly the class of problem the package's own GPT 5-question check already surfaced for CURRENT top-sections (`P1_P2_AUTO_USE_READONLY_E2E_CHECK_r0001.md`, Q4/Q5: "L0 불충분") — i.e., the routing/summary layer is openly disclosed as not yet validated to generalize, which matches Q1's concern directly.
- Evidence: `ROUTES` dict at `context_query.py:16-23`; fallback at `:39-40`.
- Proposed fix: not urgent to change code given the explicit disclaimers already present in the docs, but recommend documenting this fallback bias plainly for operators (e.g., a comment/README note: "unmatched questions default to `skill`, not `NOT_CLASSIFIED`") and treating it as a known limitation to be exercised by the still-`NOT_RUN` 30-question benchmark (Q7) before relying on it operationally.
- How to verify: run a few adversarial substring probes (e.g. `choose("그룹웨어 설치 문의")`) and confirm whether misrouting occurs as predicted.

### RECOMMENDATION
- Add a Windows-drive-letter traversal test case to `test_context_query.py`, given the Windows E2E plan (`r0002`) re-runs exactly this suite via `unittest discover` on a Windows host as its only automated path-safety check — currently it only covers POSIX-style `/etc/passwd` and `..` traversal, not drive-absolute forms.
- Keep P1/P2 at current scope (no new Agent/RAG/graph engine, no PUBLIC schema expansion, no new exporter) until the already-deferred A3 (visual/mobile) and A4 (30-question benchmark) steps are actually executed — the design doc's own boundary list (§2, §6) is correctly respected in the code I read, and I found no scope creep to flag for Q10.

### What looked correct on static read
- `context-view.js` / `index.html`: strict `approved()` allowlist gate (schema, field set, length/char checks, `Object.hasOwn` guard against prototype-pollution via `category`), `textContent`-only rendering, no `innerHTML`/`document.write`, same-origin-only `fetch('status.json')`, CSP (`script-src 'self'`, no `unsafe-inline` for scripts) consistent with the no-exfiltration requirement (Q5).
- The 4-card P1 quick-summary section and the B/D-style timeline are kept visually and semantically separate in the HTML/CSS, with explicit Korean copy distinguishing "fresh" vs ">6h stale, last-published-not-current" states in `context-view.js` (`stale()`, `STALE_AFTER_MS`) — addresses Q6 at the code level (not verified in an actual browser).
- `related()`'s P2 output is honestly scoped: it reports `PRESENT_LOCAL_UNVALIDATED` / `NOT_FOUND_LOCAL` and a hardcoded `execution_verdict: "NOT_INFERRED_FROM_FILES"` rather than inferring completion from file existence — matches Q3's safety requirement.
- `diff_summary()`'s `git show` call uses a regex-validated 40-hex commit and `subprocess.run` with a list (no shell), so no command-injection surface.
- The four CoWork markdown docs are internally consistent about distinguishing PASS/SKIP/NOT_RUN/NOT_VERIFIED (e.g., `INDEPENDENT_REVIEW=SKIP_BY_USER` is never conflated with PASS; `HANDOFF_POSTED` is explicitly separated from `WINDOWS_E2E=NOT_RUN`) — I did not find a false-PASS claim in the text itself (Q2, Q8).
- The 9 unit tests in `test_context_query.py` are accurately described in `P1_P2_CONTEXT_IMPLEMENTATION_RESULT.md` ("PRIVATE Python 격리 단위시험 9개") — count matches what I read (Q7).

---

**Knowledge files actually read:** none — the REQUEST lists no pinned knowledge files ("(none pinned in this REQUEST)"), and `__SKILL_COLLAB_CONTEXT__/FILE_INDEX.txt` confirmed only the 10 package files (no separate knowledge files present to read).

**Consumer profiles judged against:** `cowork-p1p2-context-code-design-and-e2e-plan-review` (the single profile named in the REQUEST).

**Left unverified (explicitly, not claimed as PASS):**
- I did not execute any code (Python tests, `context_query.py` CLI) or render the HTML/JS in a browser; all findings above are from static reading only.
- I did not recompute or verify SHA-256/CRC/byte-size of any package file against `MANIFEST.json` or the REQUEST's stated `package_sha256` — no hashing tool was available in this session, and the task explicitly says the watcher already verified this.
- I did not check GitHub `main` for drift from the blob SHAs recorded in `MANIFEST.json` — reviewed only the fixed snapshot contents.
- I did not verify the real-world behavior of REQUEST/SOURCE_PIN/APPROVAL_SIG/READY/RECEIPT chains beyond what `related()`'s code logic implies; cryptographic/signature validity is out of this tool's scope and out of mine.
- I did not test mobile/PC visual rendering, the 30-question benchmark, or any Windows host session — consistent with the package's own `NOT_RUN` labels for those items.

**Proposed corrections to common knowledge (GPT to decide):**
- Record finding #1 (unguarded `ValueError` on >200 `collab/requests/REQ-*` folders) as a standing MAJOR risk against `context_query.py` until fixed — this is a systemic availability risk that will recur as review history accumulates, not a one-off.
- Record findings #2 and #3 as MINOR hardening/test-gap items tracked against the same file, to be picked up opportunistically rather than blocking current usage.
