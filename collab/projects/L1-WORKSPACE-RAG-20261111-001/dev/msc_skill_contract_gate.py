#!/usr/bin/env python3
"""Validate existing MSC entrypoint contract and packaged managed-action flags.

No runtime dependency on skillsilent is added. Missing policy is reported as
NOT_APPLICABLE for direct OpenCode operation unless --require-policy is set.
"""
from __future__ import annotations
import argparse
import json
import sys
import zipfile
from pathlib import Path
from skill_release_quality_gate import GateError, normalize_members

ROUTES = {
    "WORKFLOW_ISSUE_MSC": "VERIFIED_SCENARIO_IR",
    "UPDATER_PROCEDURE_FEATURE_MSC": "VERIFIED_SEMANTIC_SPEC",
}


def find_action(node, name: str):
    if isinstance(node, dict):
        if node.get("name") == name or node.get("action") == name or node.get("id") == name:
            return node
        if name in node and isinstance(node[name], (dict, list)):
            return node[name]
        for value in node.values():
            found = find_action(value, name)
            if found is not None:
                return found
    elif isinstance(node, list):
        for item in node:
            found = find_action(item, name)
            if found is not None:
                return found
    return None


def validate_matrix(matrix: dict) -> None:
    if matrix.get("contract") != "MSC_SKILL_IO_MATRIX_V1":
        raise GateError("CONTRACT_ID_MISMATCH")
    routes = {row.get("entry"): row for row in matrix.get("routes", [])}
    if set(routes) != set(ROUTES):
        raise GateError("ROUTE_SET_MISMATCH")
    for name, source in ROUTES.items():
        row = routes[name]
        if (row.get("source_class") != source or row.get("output_class") != "MSC_HTML"
            or row.get("raw_puml_direct") is not False
            or row.get("advance_lifecycle") is not False):
            raise GateError("ROUTE_AUTHORITY_MISMATCH: " + name)
    required = matrix.get("managed_action_flags")
    if not isinstance(required, list) or not required:
        raise GateError("MANAGED_FLAGS_MISSING")
    seen = set()
    for row in required:
        if row.get("package") != "doc-converter" or row.get("flag") != "--view-mode":
            raise GateError("FLAG_CONTRACT_UNEXPECTED")
        action = row.get("action")
        if action in seen:
            raise GateError("DUPLICATE_MANAGED_ACTION")
        seen.add(action)
    if seen != {"msc-package", "msc-scenario-build"}:
        raise GateError("MANAGED_ACTION_SET_MISMATCH")


def audit_managed_actions(files: dict[str, bytes], matrix: dict,
                          *, require_policy=False) -> dict:
    policy_path = "skillsilent/policy.json"
    if policy_path not in files:
        if require_policy:
            raise GateError("MANAGED_POLICY_REQUIRED_BUT_MISSING")
        return {"managed_policy": "NOT_APPLICABLE_DIRECT_OPENCODE"}
    policy = json.loads(files[policy_path].decode("utf-8"))
    scripts = "\n".join(body.decode("utf-8", errors="replace")
                        for name, body in files.items() if name.endswith(".py"))
    for row in matrix["managed_action_flags"]:
        action = find_action(policy, row["action"])
        if action is None:
            raise GateError("MANAGED_ACTION_NOT_FOUND: " + row["action"])
        if not isinstance(action, dict) or "allowed_flags" not in action:
            raise GateError("POLICY_ALLOWLIST_NOT_FOUND: " + row["action"])
        flags = action["allowed_flags"]
        if isinstance(flags, dict):
            allowed = set(flags)
        elif isinstance(flags, list):
            allowed = {x if isinstance(x, str) else x.get("name") or x.get("flag")
                       for x in flags}
        else:
            raise GateError("POLICY_ALLOWLIST_UNSUPPORTED: " + row["action"])
        if row["flag"] not in allowed:
            raise GateError("CODE_FLAG_MISSING_IN_POLICY: " + row["action"])
        if row["flag"] not in scripts:
            raise GateError("POLICY_FLAG_MISSING_IN_CODE: " + row["flag"])
    return {"managed_policy": "PASS", "checked_actions": len(matrix["managed_action_flags"])}


def validate(matrix_path: Path, package: Path | None,
             *, require_policy=False) -> dict:
    matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    validate_matrix(matrix)
    result = {"contract": matrix["contract"], "status": "PASS",
              "routes": len(matrix["routes"])}
    if package is not None:
        with zipfile.ZipFile(package) as z:
            files = normalize_members(z)
        result.update(audit_managed_actions(files, matrix, require_policy=require_policy))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix", type=Path, required=True)
    parser.add_argument("--package", type=Path)
    parser.add_argument("--require-policy", action="store_true")
    args = parser.parse_args()
    try:
        print(json.dumps(validate(args.matrix, args.package,
                                  require_policy=args.require_policy), sort_keys=True))
        return 0
    except (GateError, ValueError, OSError, KeyError, zipfile.BadZipFile) as exc:
        print("CONTRACT_GATE_FAIL: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
