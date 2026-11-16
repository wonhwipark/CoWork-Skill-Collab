#!/usr/bin/env python3
"""Executable tests for existing MSC route/managed CLI allowlist contract."""
import json
import unittest
from msc_skill_contract_gate import (
    GateError, ROUTES, audit_managed_actions, validate_matrix,
)


def base():
    return {
        "contract": "MSC_SKILL_IO_MATRIX_V1",
        "routes": [
            {"entry": entry, "source_class": source,
             "output_class": "MSC_HTML", "raw_puml_direct": False,
             "advance_lifecycle": False}
            for entry, source in ROUTES.items()
        ],
        "managed_action_flags": [
            {"action": a, "flag": "--view-mode", "package": "doc-converter"}
            for a in ("msc-package", "msc-scenario-build")
        ],
    }


def files(policy=True, include_second=True, code=True):
    actions = {
        "msc-package": {"allowed_flags": ["--view-mode", "--input"]},
        "msc-scenario-build": {"allowed_flags": ["--view-mode", "--input"]
                                if include_second else ["--input"]},
    }
    result = {"SKILL.md": b"---\nname: doc-converter\n---\n",
              "scripts/render.py": (b"parser.add_argument('--view-mode')" if code
                                    else b"parser.add_argument('--input')")}
    if policy:
        result["skillsilent/policy.json"] = json.dumps({"actions": actions}).encode()
    return result


class ContractGateTest(unittest.TestCase):
    def test_two_routes_are_consistent(self):
        validate_matrix(base())

    def test_raw_puml_as_verified_ir_is_rejected(self):
        config = base()
        config["routes"][0]["source_class"] = "RAW_PUML"
        with self.assertRaisesRegex(GateError, "ROUTE_AUTHORITY_MISMATCH"):
            validate_matrix(config)

    def test_policy_declares_reachable_cli_flags(self):
        config = base()
        validate_matrix(config)
        self.assertEqual(audit_managed_actions(files(), config)["checked_actions"], 2)

    def test_missing_second_action_flag_blocks(self):
        with self.assertRaisesRegex(GateError, "CODE_FLAG_MISSING_IN_POLICY"):
            audit_managed_actions(files(include_second=False), base())

    def test_code_without_flag_blocks(self):
        with self.assertRaisesRegex(GateError, "POLICY_FLAG_MISSING_IN_CODE"):
            audit_managed_actions(files(code=False), base())

    def test_open_code_direct_path_requires_no_policy(self):
        self.assertEqual(
            audit_managed_actions(files(policy=False), base())["managed_policy"],
            "NOT_APPLICABLE_DIRECT_OPENCODE",
        )
        with self.assertRaisesRegex(GateError, "MANAGED_POLICY_REQUIRED"):
            audit_managed_actions(files(policy=False), base(), require_policy=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
