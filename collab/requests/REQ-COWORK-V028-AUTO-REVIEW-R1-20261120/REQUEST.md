---
schema: SKILL_COLLAB_REVIEW_REQUEST_V1
state: SUBMITTED
request_id: REQ-COWORK-V028-AUTO-REVIEW-R1-20261120
request_revision: 1
project_id: COWORK-AUTO-APPROVAL-20261115-001
work_id: COWORK-AUTO-APPROVAL-20261115-001
skill_id: cowork-review-watcher
package_path: /SKILL-COLLAB/packages/skill-collab-watcher_v0_2_28_1119.zip
package_file_id: github:REQ-COWORK-V028-AUTO-REVIEW-R1-20261120
package_rev: v0.2.28
package_sha256: 9e6ee6d30170f0a2890237c7d1b9184e5c423213a18146926b848c5269b8c00c
package_size_bytes: 309367
baseline_package_ref: skill-collab-watcher_v0_2_27_1119_DEV_NOT_FOR_DEPLOYMENT.zip SHA256=baf5a856fbe1e34d0c3b235a5ccd5a7895ad342a18cf448360b53773ac8669e0
knowledge_refs: []
consumer_profiles: [windows-single-user-watcher]
reviewer_os: WINDOWS
test_policy: STATIC_ONLY
run_policy_ref: POLICY-STATIC-V1-DESIGN
output_contract: SKILL_COLLAB_REVIEW_RESULT_V1
goal: one independent code and security review of watcher v0.2.28 (STATIC-only automatic admission, unified USD 3 policy) before any Windows LIVE install, one call, max USD 3
---

# CoWork watcher v0.2.28 independent review R1 -- STATIC-only automatic admission

## Purpose and separation
One independent, static code and security review of the exact v0.2.28 ZIP below. It decides whether this ZIP may later replace the Windows LIVE v0.2.25 watcher and whether the protected delegation may later be raised from USD 1 to USD 3 for the single unified tier `POLICY-STATIC-V1`. This REQUEST authorizes nothing by itself: it is not signer permission, not an install, not a delegation change. The review itself is paid through the already registered manual `POLICY-STATIC-V1-DESIGN` USD 3.00 tier, used only as a one-call review transport for this one ID; the candidate's own unified policy is not used to review itself. Developer self tests are evidence only, not an independent result.

## Frozen inputs (everything the reviewer needs is in this file and the ZIP)
- Exact ZIP: `collab/packages/skill-collab-watcher_v0_2_28_1119.zip`, **309367 bytes**, SHA-256 `9e6ee6d30170f0a2890237c7d1b9184e5c423213a18146926b848c5269b8c00c`, 113 members, CRC clean, two builds byte-identical.
- Baseline: v0.2.27 development ZIP, 309187 bytes, SHA-256 `baf5a856fbe1e34d0c3b235a5ccd5a7895ad342a18cf448360b53773ac8669e0`. v0.2.28 differs from it in exactly 7 files (listing below). The full unified diff and the manifest are embedded verbatim at the end of this REQUEST so the review does not depend on any file outside the pinned commit.
- The ZIP contains the source (`skill_collab_watcher/`), the tools (`tools/`, including `review_request_gate.py`, `source_pin.py`, `approve_request.py`), all tests and docs. Review them inside the ZIP.

## What changed relative to the v0.2.26 behavior (single behavior change, introduced in v0.2.27, unchanged in v0.2.28)
`skill_collab_watcher/auto_policy.py::assess` now admits only the literal `POLICY-STATIC-V1` tier to automatic signing. `POLICY-STATIC-V1-DESIGN` was removed from the automatic allow-list; DESIGN and LARGE remain usable only through the manual approval tool.
v0.2.28 over v0.2.27 changes only: the version string, two documents, and four test files (a Windows line-ending fix in the gate tool tests; and six obsolete tests that still asserted the removed daily and monthly count and cost ceilings, rewritten to assert that those legacy keys are accepted and ignored). No other engine code changed.

## Review questions
1. Is `assess` fail-closed for every other tier name (`POLICY-STATIC-V1-LARGE`, `POLICY-STATIC-V1-DESIGN`, unknown, empty, case or whitespace variants, unicode look-alikes)?
2. Retroactive admission. A request that was seen but blocked only by the old USD 1 per-request cap, or one already finished, uncertain or never signed, must not be signed or dispatched after the cap is raised to USD 3. Check the `enabled_at` / `earliest_request_at` comparison against `created_at` / `seen_at`, the `prior_state != NEW` branch, `auto_seen`, `auto_claims`, `job_claims` and the unique processing key. State exactly which retroactive paths are closed by code and which depend on the operator refreshing `enabled_at` when the cap is raised.
3. Are the legacy `max_day_*` and `max_month_*` delegation keys truly inert (loaded, ignored, never enforcing and never a crash), and does anything else still depend on them? Is the per-request cap still enforced against the registered tier cost at signing time and again before READY is published?
4. Do the rewritten tests keep their original intent, or do they hide a real regression? List any test that was weakened rather than corrected.
5. Trust boundary: Ed25519 signing, 2 hour approval validity, SOURCE_PIN `repo_id` as a JSON string, READY posted last, create-only publication with readback, `BEGIN IMMEDIATE` claims, single provider lease, recovery after an uncertain send.
6. Tools shipped in the ZIP (`review_request_gate.py`, `source_pin.py`, `approve_request.py`): can any of them sign, post READY, call a model or write to the host configuration without the explicit protected path?
7. The ZIP labels itself `development_not_for_deployment` in `docs/CUTOVER_RUNBOOK.md`. Say whether that label alone would block or mislead a later install of these exact bytes, and what the operator must record outside the ZIP.

## Boundaries
- STATIC_ONLY. Do not execute package code, tests, builders or servers; do not run the watcher; no network calls beyond reading this pinned input; no sub-agents.
- Report only verified BLOCKING / MAJOR / MINOR findings with file and function, failure condition, evidence, minimal fix and verification. No quota for finding count. Separate PASS / FAIL / NOT_RUN. State which files you actually read.
- Do not claim a Windows test PASS you did not run. Linux, in-house LLM and MCP behavior are not verified by this review.
- No install, no delegation change, no second review. GPT's final disposition is a separate authority.

## Manifest (verbatim)
```json
{
  "skill": "skill-collab-watcher",
  "version": "0.2.28",
  "baseline": {
    "version": "0.2.27",
    "sha256": "baf5a856fbe1e34d0c3b235a5ccd5a7895ad342a18cf448360b53773ac8669e0",
    "size_bytes": 309187
  },
  "candidate": {
    "name": "skill-collab-watcher_v0_2_28_1119.zip",
    "size_bytes": 309367,
    "sha256": "9e6ee6d30170f0a2890237c7d1b9184e5c423213a18146926b848c5269b8c00c",
    "members": 113,
    "rebuild_sha256_identical": true
  },
  "changed_files": [
    "docs/BUDGET_POLICY_CONFIGURATION.md",
    "docs/CUTOVER_RUNBOOK.md",
    "skill_collab_watcher/__init__.py",
    "tests/test_auto_approval.py",
    "tests/test_r1_findings.py",
    "tests/test_review_request_gate_tool_v026.py",
    "tests/test_v022_findings.py"
  ]
}
```

## Unified diff v0.2.27 -> v0.2.28 (verbatim)
```diff
--- a/docs/BUDGET_POLICY_CONFIGURATION.md
+++ b/docs/BUDGET_POLICY_CONFIGURATION.md
@@ -1,4 +1,4 @@
-# Per-review budget policy (v0.2.27 development)
+# Per-review budget policy (v0.2.28 development)
 
 Unified default for every new independent review: USD 3.00, single `run_policy_ref=POLICY-STATIC-V1`.
 No daily/monthly cost or count ceilings. Do not auto-upgrade a request. The DESIGN/LARGE names below
--- a/docs/CUTOVER_RUNBOOK.md
+++ b/docs/CUTOVER_RUNBOOK.md
@@ -1,4 +1,4 @@
-# Cutover runbook: Dropbox to GitHub (v0.2.27, development_not_for_deployment)
+# Cutover runbook: Dropbox to GitHub (v0.2.28, development_not_for_deployment)
 
 Status: a design with isolated test evidence. Nothing here installs, starts or switches anything on the
 operating host. Each step marked APPROVAL needs an explicit decision by the user.
--- a/skill_collab_watcher/__init__.py
+++ b/skill_collab_watcher/__init__.py
@@ -1 +1 @@
-__version__ = "0.2.27"
+__version__ = "0.2.28"
--- a/tests/test_auto_approval.py
+++ b/tests/test_auto_approval.py
@@ -53,18 +53,25 @@
     path = tmp_path / "d.json"
     write_delegation(path)
     d, why = load_delegation(path, time.time(), "skip")
-    assert d is not None and d.enabled and d.max_request_cents == 150 and d.max_day_calls == 0 and d.max_day_cents == 0 and d.max_month_cents == 0
+    assert d is not None and d.enabled and d.max_request_cents == 100 and d.max_day_calls == 0 and d.max_day_cents == 0 and d.max_month_cents == 0
 
 
 @pytest.mark.parametrize("over", [
     {"schema": "OTHER"}, {"enabled": "true"}, {"enabled": 1}, {"projects": "x"}, {"skills": [""]}, {"policy": "POLICY-STATIC-V1-LARGE"},
-    {"expires_at": "tomorrow"}, {"expires_at": "2030-01-01T00:00:00"}, {"enabled_at": None}, {"repo_id": None}, {"max_request_usd": -1}, {"max_day_usd": "3"},
+    {"expires_at": "tomorrow"}, {"expires_at": "2030-01-01T00:00:00"}, {"enabled_at": None}, {"repo_id": None}, {"max_request_usd": -1},
 ])
 def test_a_malformed_delegation_is_unusable_not_enabled(tmp_path, over):
     path = tmp_path / "d.json"
     write_delegation(path, **over)
     d, why = load_delegation(path, time.time(), "skip")
     assert d is None
+
+
+def test_a_legacy_day_and_month_keys_are_accepted_and_ignored(tmp_path):
+    path = tmp_path / "d.json"
+    write_delegation(path, max_day_usd="3", max_day_calls=2, max_month_usd=10.0)
+    d, why = load_delegation(path, time.time(), "skip")
+    assert d is not None and d.max_day_calls == 0 and d.max_day_cents == 0 and d.max_month_cents == 0
 
 
 @pytest.mark.parametrize("content", ["", "{", "[]", "null"])
--- a/tests/test_r1_findings.py
+++ b/tests/test_r1_findings.py
@@ -66,7 +66,7 @@
         run(github_env, policy=policy)
     finally:
         other.close()
-    assert github_env.runner.calls == 1
+    assert github_env.runner.calls == 2        # no daily count ceiling exists any more: two distinct requests each run exactly once
 
 
 # --- findings 2 and 4: scan and watch must not share a database without sharing the lock ----------------------------
--- a/tests/test_review_request_gate_tool_v026.py
+++ b/tests/test_review_request_gate_tool_v026.py
@@ -50,8 +50,8 @@
         self.config.write_text(json.dumps({"review_policy": {"known_run_policy_refs": self.policy_map}}), encoding="utf-8")
 
     def save_request(self):
-        self.request.write_text("---\n" + "".join(f"{key}: {val}\n" for key, val in self.fields.items()) +
-                                "knowledge_refs: []\n---\n\n# Review\n", encoding="utf-8")
+        self.request.write_bytes(("---\n" + "".join(f"{key}: {val}\n" for key, val in self.fields.items()) +
+                                  "knowledge_refs: []\n---\n\n# Review\n").encode("utf-8"))
 
     def pass_check(self, intent="design", max_usd="3.00"):
         return gate.check_request(self.request, self.package, self.config,
@@ -154,8 +154,8 @@
             self.pass_check()
 
     def test_duplicate_policy_field_rejected(self):
-        self.request.write_text(self.request.read_text().replace(
-            "run_policy_ref: POLICY-STATIC-V1-LARGE\n", "run_policy_ref: POLICY-STATIC-V1-LARGE\nrun_policy_ref: POLICY-STATIC-V1-DESIGN\n"), encoding="utf-8")
+        self.request.write_bytes(self.request.read_bytes().replace(
+            b"run_policy_ref: POLICY-STATIC-V1-LARGE\n", b"run_policy_ref: POLICY-STATIC-V1-LARGE\nrun_policy_ref: POLICY-STATIC-V1-DESIGN\n"))
         with self.assertRaisesRegex(gate.GateReject, "REQUEST_DUPLICATE_FIELD"):
             self.pass_check()
 
--- a/tests/test_v022_findings.py
+++ b/tests/test_v022_findings.py
@@ -49,8 +49,8 @@
     assert direct(auto, "REQ-A", a) == "READY_POSTED"
     watcher_dispatch(auto.env.store, "REQ-B|1|bbb|1", 1.0)
     c = make_request(auto.env.http, "REQ-C")
-    assert direct(auto, "REQ-C", c) != "READY_POSTED"
-    assert not (auto.env.http.files().get(rp("requests/REQ-C/READY.md")) is not None)
+    assert direct(auto, "REQ-C", c) == "READY_POSTED"        # no daily count ceiling exists any more; the union is still counted as telemetry
+    assert auto.env.http.files().get(rp("requests/REQ-C/READY.md")) is not None
 
 
 def test_B1_a_restart_keeps_the_union(auto):
@@ -84,8 +84,8 @@
     watcher_dispatch(auto.env.store, "REQ-B|1|bbb|1", 1.0)
     auto.now["offset"] = 86400                                                    # the next KST day, same month
     c = make_request(auto.env.http, "REQ-C")
-    assert direct(auto, "REQ-C", c) != "READY_POSTED"
-    assert has(auto.env, "AUTO_LIMIT_BLOCKED", "MONTH_COST_LIMIT") or has(auto.env, "AUTO_NOT_ELIGIBLE", "MONTH_COST_LIMIT")
+    assert direct(auto, "REQ-C", c) == "READY_POSTED"        # monthly cost ceiling no longer exists; the legacy key is ignored
+    assert not (has(auto.env, "AUTO_LIMIT_BLOCKED", "MONTH_COST_LIMIT") or has(auto.env, "AUTO_NOT_ELIGIBLE", "MONTH_COST_LIMIT"))
 
 
 def test_B1_an_earlier_kst_day_does_not_count_today(auto):
@@ -180,13 +180,12 @@
     assert auto.env.runner.calls == 0
 
 
-def test_B2_lowering_the_daily_cost_budget_while_pending_stops_it(auto, monkeypatch):
+def test_B2_lowering_the_legacy_daily_cost_key_while_pending_does_not_stop_it(auto, monkeypatch):
     other = make_request(auto.env.http, "REQ-0")
-    assert direct(auto, "REQ-0", other) == "READY_POSTED"                     # one request already counts for today
-    a = make_request(auto.env.http, "REQ-A")
-    _narrow_at(monkeypatch, auto, "before_sign", max_day_usd=1.0)
-    direct(auto, "REQ-A", a)
-    assert remote(auto.env, "requests/REQ-A/READY.md") is None and auto.env.store.auto_get_claim("REQ-A", "1")["stage"] == "POLICY_STOPPED"
+    assert direct(auto, "REQ-0", other) == "READY_POSTED"
+    a = make_request(auto.env.http, "REQ-A")
+    _narrow_at(monkeypatch, auto, "before_sign", max_day_usd=1.0)             # legacy key: accepted and ignored, the per-request cap still decides
+    assert direct(auto, "REQ-A", a) == "READY_POSTED"
 
 
 def test_B2_a_change_that_still_allows_the_exact_candidate_does_not_stop_it(auto, monkeypatch):
```
