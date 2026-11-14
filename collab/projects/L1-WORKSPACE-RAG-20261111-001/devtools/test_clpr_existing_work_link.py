"""Isolated synthetic WorkRefs integration tests; never use a real ledger."""
from __future__ import annotations

import copy
import hashlib
import pathlib
import tempfile
import unittest
from unittest.mock import patch

from l1_fix_workflow.issue_brief import plan_clpr_issue_cases
from l1_fix_workflow.clpr_existing_work_link import link_clpr_existing_work
from work_ledger_kernel.kernel import WorkLedgerKernel


def p4(n, key="SOC-321"):
    return {"type": "p4", "server_alias": "TEST", "cl": n, "jira_keys": [key]}


def pr(n, key="SOC-321"):
    return {"type": "github_pr", "url": "https://github.com/example/repo/pull/" + str(n),
            "jira_keys": [key]}


def make_plan(*changes):
    return plan_clpr_issue_cases({"changes": list(changes)})


def sole_identity(plan):
    assert len(plan["issue_cases"]) == 1
    return plan["issue_cases"][0]["issue_identity"]


class CLPRExistingWorkLinkE2(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="clpr-e2-")
        self.addCleanup(self.temp.cleanup)
        self.ledger = pathlib.Path(self.temp.name) / "ledger"
        self.kernel = WorkLedgerKernel(self.ledger)
        self.work_id = self.kernel.work_create("Synthetic CLPR issue")["work_id"]
        self.kernel.work_reference_add(self.work_id, "jira", "SOC-321")

    def snapshot_record(self):
        return (self.ledger / self.work_id / "record.json").read_bytes()

    def test_preview_does_not_mutate_and_commit_readback(self):
        plan = make_plan(p4(101), pr(11))
        before = self.snapshot_record()
        preview = link_clpr_existing_work(plan, self.kernel, issue_identity=sole_identity(plan))
        self.assertEqual(preview["action"], "LINK_PREVIEW")
        self.assertEqual(preview["would_add"], 2)
        self.assertFalse(preview["workspace_written"])
        self.assertEqual(self.snapshot_record(), before)
        out = link_clpr_existing_work(plan, self.kernel, issue_identity=sole_identity(plan), commit=True)
        self.assertTrue(out["ok"])
        self.assertEqual(out["work_id"], self.work_id)
        self.assertEqual(out["writes"], 2)
        self.assertFalse(out["new_work_created"])
        self.assertEqual(out["evidence_registration"], "NOT_RUN")
        self.assertEqual(self.snapshot_record(), before)
        for ref in ("p4:TEST:101", "https://github.com/example/repo/pull/11"):
            found = self.kernel.work_reference_find(ref)
            self.assertEqual([r["work_id"] for r in found["matches"] if r["match_type"] == "external_ref"], [self.work_id])

    def test_idempotent_with_reorder_and_added_source(self):
        a = make_plan(p4(101), pr(11))
        self.assertEqual(link_clpr_existing_work(a, self.kernel, issue_identity=sole_identity(a), commit=True)["writes"], 2)
        before = list(self.ledger.rglob("record.json"))
        b = make_plan(pr(12), pr(11), p4(101))
        self.assertEqual(link_clpr_existing_work(b, self.kernel, issue_identity=sole_identity(b), commit=True)["writes"], 1)
        self.assertEqual(link_clpr_existing_work(b, self.kernel, issue_identity=sole_identity(b), commit=True)["writes"], 0)
        self.assertEqual(list(self.ledger.rglob("record.json")), before)

    def test_not_found_refuses_work_creation(self):
        a = make_plan(p4(222, "SOC-999"))
        result = link_clpr_existing_work(a, self.kernel, issue_identity=sole_identity(a), commit=True)
        self.assertFalse(result["ok"])
        self.assertEqual(result["reason"], "NOT_FOUND")
        self.assertEqual(result["writes"], 0)
        self.assertEqual(len(list(self.ledger.rglob("record.json"))), 1)

    def test_conflicting_reference_refuses_all_writes(self):
        other = self.kernel.work_create("Unrelated")["work_id"]
        self.kernel.work_reference_add(other, "p4_cl", "p4:TEST:101")
        plan = make_plan(p4(101), pr(11))
        before = self.snapshot_record()
        result = link_clpr_existing_work(plan, self.kernel, issue_identity=sole_identity(plan), commit=True)
        self.assertFalse(result["ok"])
        self.assertEqual(result["reason"], "CONFLICT_MULTIPLE_WORKS")
        self.assertEqual(self.snapshot_record(), before)
        self.assertEqual(self.kernel.work_reference_find("https://github.com/example/repo/pull/11")["count"], 0)

    def test_partial_lookup_refuses(self):
        plan = make_plan(p4(101), pr(11))
        real = self.kernel.work_reference_find
        def partial(ref, **kwargs):
            if ref == "p4:TEST:101":
                return {"count": 201, "matches": []}
            return real(ref, **kwargs)
        with patch.object(self.kernel, "work_reference_find", side_effect=partial):
            result = link_clpr_existing_work(plan, self.kernel, issue_identity=sole_identity(plan), commit=True)
        self.assertFalse(result["ok"])
        self.assertEqual(result["writes"], 0)

    def test_reject_unsafe_modified_plan_and_ambiguous_identity(self):
        plan = make_plan(p4(101), pr(11))
        corrupt = copy.deepcopy(plan)
        corrupt["issue_cases"][0]["source_refs"] = ["http://evil/pull/11"]
        with self.assertRaises(ValueError):
            link_clpr_existing_work(corrupt, self.kernel, issue_identity=sole_identity(plan), commit=True)
        with self.assertRaises(ValueError):
            link_clpr_existing_work(plan, self.kernel, issue_identity="jira:UNKNOWN", commit=True)
        with self.assertRaises(ValueError):
            link_clpr_existing_work(plan, self.kernel, issue_identity=sole_identity(plan), commit="true")


if __name__ == "__main__":
    unittest.main()
