"""Supplementary non-production tests for the *extracted, pinned* v0.2.29 ZIP.

Copy to extracted_root/tests/test_five_windows_actual_zip.py; run pytest from
extracted_root with the package's existing fixtures and synthetic GitHub.
No live network, operational signer, DB or paid model should be used.
"""
from __future__ import annotations

from auto_helpers import auto, make_request, remote, write_delegation  # noqa: F401
from bundle import make_transport
from test_cli_entrypoint_e2e import e2e  # noqa: F401  required existing fixture
from test_auto_approval_e2e import configure, has_file, puts, watch


def process(auto_ns, info):
    transport = make_transport(auto_ns.env.http)
    transport.ensure_auth()
    return auto_ns.approver.process(
        transport, auto_ns.env.store, auto_ns.policy,
        "/SKILL-COLLAB", info.rid, info.request.decode("utf-8"), info.request,
    ).status


def test_five_independent_windows_ready_once_in_sequence(auto):
    """Two design reviews and three skill reviews, with one unified STATIC tier.

    This verifies watcher admission and READY, not source-code merge/rebase.
    """
    write_delegation(auto.delegation, max_request_usd=3.0, projects=[f"SIM-WORK-{i}" for i in range(1, 6)])
    kinds = ("DESIGN", "DESIGN", "SKILL", "SKILL", "SKILL")
    cases = []
    for idx, kind in enumerate(kinds, start=1):
        rid = f"SIM-5W-{idx}"
        info = make_request(auto.env.http, rid, project=f"SIM-WORK-{idx}",
                            body_extra=f"chat_window: {idx}\nreview_kind: {kind}")
        assert process(auto, info) == "READY_POSTED", (idx, kind)
        assert remote(auto.env, f"requests/{rid}/APPROVAL_SIG.json") is not None
        assert remote(auto.env, f"requests/{rid}/READY.md") is not None
        assert auto.env.store.auto_get_claim(rid, "1")["stage"] == "READY_POSTED"
        cases.append(info)

    # Already approved requests are never signed/published a second time.
    assert auto.signer.calls == 5
    for info in cases:
        before = len([c for c in auto.env.http.calls if c[0] == "PUT"])
        again = process(auto, info)
        after = len([c for c in auto.env.http.calls if c[0] == "PUT"])
        # An already READY_POSTED request may *return* READY_POSTED; that is
        # idempotent and not a new signature or a new remote publication.
        assert again in ("READY_POSTED", "REMOTE_HISTORY", "DUPLICATE_OR_UNCERTAIN"), (info.rid, again)
        assert after == before, (info.rid, before, after)
    assert auto.signer.calls == 5
    for idx in range(1, 6):
        rid = f"SIM-5W-{idx}"
        assert remote(auto.env, f"requests/{rid}/READY.md") is not None


def test_two_legacy_design_requests_are_rejected_without_blocking_three_skills(auto):
    """The old DESIGN tier cannot be silently upgraded into unified STATIC."""
    write_delegation(auto.delegation, max_request_usd=3.0)
    for idx in range(1, 6):
        rid = f"SIM-POLICY-{idx}"
        info = make_request(auto.env.http, rid,
                            policy_ref="POLICY-STATIC-V1-DESIGN" if idx <= 2 else "POLICY-STATIC-V1")
        result = process(auto, info)
        if idx <= 2:
            assert result == "REVIEW_POLICY", result
            assert remote(auto.env, f"requests/{rid}/READY.md") is None
        else:
            assert result == "READY_POSTED", result
    assert auto.signer.calls == 3


def test_old_cost_rejection_persists_across_five_independent_requests(auto):
    """v0.2.29 POLICY_STOPPED must survive the cap raise; new requests proceed."""
    previous = write_delegation(auto.delegation, max_request_usd=0.5)
    old = make_request(auto.env.http, "SIM-COST-OLD")
    assert process(auto, old) == "PER_REQUEST_COST"
    assert auto.env.store.auto_get_claim(old.rid, "1")["stage"] == "POLICY_STOPPED"
    write_delegation(auto.delegation, max_request_usd=3.0,
                     enabled_at=previous["enabled_at"])
    assert process(auto, old) == "POLICY_STOPPED"
    assert remote(auto.env, "requests/SIM-COST-OLD/READY.md") is None
    for idx in range(1, 6):
        info = make_request(auto.env.http, f"SIM-COST-NEW-{idx}")
        assert process(auto, info) == "READY_POSTED"
    assert auto.signer.calls == 5


def test_real_cli_watch_five_windows_one_model_stub_call_each(e2e):
    """Real CLI subprocess + synthetic transport and counting Claude stub only.

    The package's e2e fixture must ensure the runner is a stub. In this test,
    'model_calls' counts stub invocations, not real paid calls.
    """
    configure(e2e, max_request_usd=3.0, projects=[f"SIM-WORK-{i}" for i in range(1, 6)])
    for idx, kind in enumerate(("design", "design", "skill", "skill", "skill"), 1):
        rid = f"SIM-CLI-5W-{idx}"
        make_request(e2e.fake, rid, project=f"SIM-WORK-{idx}",
                     body_extra=f"request_kind: {kind}")
        code, out, err = watch(e2e, 3)
        assert code == 0, (idx, out[-250:], err[-250:])
        assert e2e.model_calls == idx, (idx, e2e.model_calls)
        assert has_file(e2e, f"receipts/{rid}/RECEIPT_1.md")
        assert has_file(e2e, f"reviews/{rid}/REVIEW_RESULT_1.md")
        assert has_file(e2e, f"requests/{rid}/READY.md")
        approval_first = [url for url in puts(e2e, f"requests/{rid}/")]
        assert approval_first[0].endswith("APPROVAL_SIG.json")
        assert approval_first[1].endswith("READY.md")

    # Restart must not lead to another review/approval or additional stubs.
    code, out, err = watch(e2e, 3)
    assert code == 0, (out[-250:], err[-250:])
    assert e2e.model_calls == 5
    assert len(puts(e2e, "APPROVAL_SIG.json")) == 5
    assert len(puts(e2e, "READY.md")) == 5
