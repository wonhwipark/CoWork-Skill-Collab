"""STAGED cutover rehearsal with the REAL watcher CLI process (python -m skill_collab_watcher.cli watch) against the package's loopback fake GitHub and a counting
model STUB. Registry STATIC = 3.0, delegation cap = 3.0 and a NEW enabled_at are applied together after old requests exist. No real model, no real GitHub, no operating DB."""
import json
import os
import time

from auto_helpers import iso, make_request
from test_auto_approval_e2e import configure, has_file, puts, watch
from test_cli_entrypoint_e2e import e2e  # noqa: F401

OUT = os.environ.get("STAGED_RESULTS")


def note(case, **kw):
    if OUT:
        with open(OUT, "a", encoding="utf-8") as fh:
            fh.write(json.dumps({"case": case, **kw}, ensure_ascii=False) + "\n")


def set_registry_usd3(e2e):
    cfg = json.loads(e2e.cfg_path.read_text(encoding="utf-8"))
    cfg["review_policy"]["known_run_policy_refs"]["POLICY-STATIC-V1"]["max_budget_usd"] = 3.0
    e2e.cfg_path.write_text(json.dumps(cfg), encoding="utf-8")


def test_cli_cutover_rehearsal_two_cycles_and_restart(e2e):
    old_a = make_request(e2e.fake, "CLI-OLD-A-STATIC")
    old_b = make_request(e2e.fake, "CLI-OLD-B-DESIGN", policy_ref="POLICY-STATIC-V1-DESIGN")
    time.sleep(2.2)
    configure(e2e, max_request_usd=3.0, enabled_at=iso(time.time()))     # cutover: cap 3.0 + NEW enabled_at together
    set_registry_usd3(e2e)                                              # and the registered STATIC cost 3.0 in the same staged state
    time.sleep(2.2)
    code, out, err = watch(e2e, 2)                                      # two cycles after the cutover
    assert code == 0, (out + err)[-300:]
    assert e2e.model_calls == 0
    assert not has_file(e2e, "requests/CLI-OLD-A-STATIC/READY.md") and not has_file(e2e, "requests/CLI-OLD-B-DESIGN/READY.md")
    note("cli_after_cutover_two_cycles", model_calls=e2e.model_calls, old_ready=0, approvals=len(puts(e2e, "APPROVAL_SIG.json")))

    make_request(e2e.fake, "CLI-NEW-1")
    code, out, err = watch(e2e, 3)
    assert code == 0 and e2e.model_calls == 1 and has_file(e2e, "requests/CLI-NEW-1/READY.md")
    assert has_file(e2e, "reviews/CLI-NEW-1/REVIEW_RESULT_1.md") and has_file(e2e, "receipts/CLI-NEW-1/RECEIPT_1.md")
    code, out, err = watch(e2e, 2)                                      # restart: nothing is reviewed or signed again
    assert code == 0 and e2e.model_calls == 1 and len(puts(e2e, "APPROVAL_SIG.json")) == 1
    note("cli_new_request_then_restart", model_calls=e2e.model_calls, approvals=len(puts(e2e, "APPROVAL_SIG.json")), readys=len(puts(e2e, "READY.md")))

    make_request(e2e.fake, "CLI-NEW-2")
    make_request(e2e.fake, "CLI-NEW-LEGACY-DESIGN", policy_ref="POLICY-STATIC-V1-DESIGN")
    code, out, err = watch(e2e, 3)
    assert code == 0 and e2e.model_calls == 2
    assert has_file(e2e, "requests/CLI-NEW-2/READY.md") and not has_file(e2e, "requests/CLI-NEW-LEGACY-DESIGN/READY.md")
    code, out, err = watch(e2e, 2)
    assert code == 0 and e2e.model_calls == 2
    note("cli_second_request_and_legacy_design", model_calls=e2e.model_calls, approvals=len(puts(e2e, "APPROVAL_SIG.json")), readys=len(puts(e2e, "READY.md")),
         old_a_ready=has_file(e2e, "requests/CLI-OLD-A-STATIC/READY.md"), old_b_ready=has_file(e2e, "requests/CLI-OLD-B-DESIGN/READY.md"),
         legacy_design_ready=has_file(e2e, "requests/CLI-NEW-LEGACY-DESIGN/READY.md"))
