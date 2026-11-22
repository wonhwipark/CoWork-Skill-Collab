#!/usr/bin/env python3
"""CoWork REQUEST input verifier plus optional Windows policy-compatibility gate.

Publication validation is host-independent and cannot authorize signing, READY,
or a model call. The existing Windows policy-compatibility check remains available
for diagnostics; the installed protected signer/watcher enforces the real policy.
No GitHub writes or local configuration modifications occur in this module.
"""
from __future__ import annotations

import argparse
from decimal import Decimal, InvalidOperation
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import zipfile

REQ_ID = re.compile(r"REQ-[A-Z0-9][A-Z0-9-]{3,120}\Z")
SHA256 = re.compile(r"[0-9a-f]{64}\Z")
REF = re.compile(r"[A-Z0-9][A-Z0-9-]{2,100}\Z")
COMMIT = re.compile(r"[0-9a-f]{40}\Z")
REPO_ID = re.compile(r"[1-9][0-9]*\Z")
INTENTS = {
    # New requests use a single policy and a single per-review budget.
    # Historical intents remain available for validating frozen legacy inputs.
    "unified": ("POLICY-STATIC-V1",),
    "skill": ("POLICY-STATIC-V1",),
    "design": ("POLICY-STATIC-V1-DESIGN", "POLICY-STATIC-V1-LARGE"),
}
DEFAULT_BUDGETS = {"unified": "3.00", "skill": "1.50", "design": "3.00"}
MAX_REQUEST = 256_000
MAX_PACKAGE = 32 * 1024 * 1024


class GateReject(ValueError):
    pass


def _read_file(path: Path, *, limit: int) -> bytes:
    if path.is_symlink() or not path.is_file() or path.stat().st_size > limit:
        raise GateReject("MISSING_OR_UNSAFE_INPUT_FILE")
    return path.read_bytes()


def _json(path: Path, *, limit: int = MAX_REQUEST) -> dict:
    raw = _read_file(path, limit=limit)
    try:
        obj = json.loads(raw)
    except (ValueError, UnicodeDecodeError) as e:
        raise GateReject("INVALID_LOCAL_JSON") from e
    if not isinstance(obj, dict):
        raise GateReject("INVALID_LOCAL_JSON_ROOT")
    return obj


def _money(value: object) -> Decimal:
    if type(value) not in (float, int):
        raise GateReject("INVALID_POLICY_COST_TYPE")
    try:
        v = Decimal(str(value))
    except InvalidOperation as e:
        raise GateReject("INVALID_POLICY_COST") from e
    if not v.is_finite() or v <= 0 or v > 100 or v.as_tuple().exponent < -2:
        raise GateReject("INVALID_POLICY_COST")
    return v


def _target_money(s: str) -> Decimal:
    try:
        d = Decimal(s)
    except InvalidOperation as e:
        raise GateReject("INVALID_REQUIRED_BUDGET") from e
    if not d.is_finite() or d <= 0 or d > 100 or d.as_tuple().exponent < -2:
        raise GateReject("INVALID_REQUIRED_BUDGET")
    return d


def _registered_policy_map(config: dict) -> dict:
    rp = config.get("review_policy")
    if not isinstance(rp, dict):
        raise GateReject("LIVE_REVIEW_POLICY_MISSING")
    refs = rp.get("known_run_policy_refs")
    if not isinstance(refs, dict) or not refs:
        raise GateReject("LIVE_POLICY_REGISTRY_MISSING")
    return refs


def select_policy(config: dict, intent: str, required_budget: Decimal) -> str:
    """Choose only locally registered refs; unified selects POLICY-STATIC-V1 at USD 3."""
    if intent not in INTENTS:
        raise GateReject("UNKNOWN_REVIEW_INTENT")
    if intent == "unified" and required_budget != Decimal(DEFAULT_BUDGETS["unified"]):
        raise GateReject("UNIFIED_REVIEW_BUDGET_MISMATCH")
    refs = _registered_policy_map(config)
    selected = next((name for name in INTENTS[intent] if name in refs), None)
    if not selected:
        raise GateReject("POLICY_NOT_INSTALLED")
    entry = refs[selected]
    if not isinstance(entry, dict):
        raise GateReject("POLICY_CONFIG_INVALID")
    configured = _money(entry.get("max_budget_usd"))
    if configured != required_budget:
        raise GateReject("POLICY_COST_MISMATCH")
    return selected


def _front_matter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise GateReject("REQUEST_FRONTMATTER_MISSING")
    end = text.find("\n---\n", 4)
    if end < 0 or end > 40_000:
        raise GateReject("REQUEST_FRONTMATTER_INVALID")
    fields: dict[str, str] = {}
    # Read simple top-level scalars; disallow duplicate keys. Nested knowledge refs ignored.
    for raw in text[4:end].splitlines():
        if not raw.strip() or raw.startswith("  - ") or raw.startswith("    "):
            continue
        match = re.fullmatch(r"([a-z][a-z0-9_]*):(?: (.*))?", raw)
        if match is None:
            raise GateReject("REQUEST_FRONTMATTER_UNSUPPORTED")
        key = match.group(1)
        if key in fields:
            raise GateReject("REQUEST_DUPLICATE_FIELD")
        fields[key] = (match.group(2) or "").strip()
    return fields


def _check_package(package: Path, *, sha: str, size: int) -> None:
    if package.is_symlink() or not package.is_file() or size <= 0 or size > MAX_PACKAGE:
        raise GateReject("PACKAGE_MISSING_OR_UNSAFE")
    if package.stat().st_size != size:
        raise GateReject("PACKAGE_SIZE_MISMATCH")
    h = hashlib.sha256()
    with package.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    if h.hexdigest() != sha:
        raise GateReject("PACKAGE_SHA256_MISMATCH")
    try:
        with zipfile.ZipFile(package) as archive:
            if archive.testzip() is not None:
                raise GateReject("PACKAGE_ZIP_CRC_FAILURE")
            seen: set[str] = set()
            for member in archive.infolist():
                name = member.filename
                p = PurePosixPath(name)
                if (not name or name.startswith("/") or "\\" in name
                        or ".." in p.parts or "" in p.parts
                        or name in seen or stat.S_IFMT(member.external_attr >> 16) == stat.S_IFLNK):
                    raise GateReject("UNSAFE_PACKAGE_MEMBER")
                seen.add(name)
    except (zipfile.BadZipFile, RuntimeError, OSError) as e:
        raise GateReject("INVALID_PACKAGE_ZIP") from e


def _check_request_inputs(request: Path, package: Path,
                          *, intent: str, required_budget: Decimal) -> dict:
    request_bytes = _read_file(request, limit=MAX_REQUEST)
    fields = _front_matter(request_bytes.decode("utf-8"))
    if (fields.get("schema") != "SKILL_COLLAB_REVIEW_REQUEST_V1"
            or fields.get("state") != "SUBMITTED"
            or fields.get("request_revision") != "1"
            or fields.get("test_policy") != "STATIC_ONLY"
            or fields.get("reviewer_os") != "WINDOWS"):
        raise GateReject("REQUEST_CONTRACT_MISMATCH")
    request_id = fields.get("request_id", "")
    if not REQ_ID.fullmatch(request_id):
        raise GateReject("INVALID_REQUEST_ID")
    if fields.get("project_id") != fields.get("work_id"):
        raise GateReject("PROJECT_WORK_SCOPE_MISMATCH")
    for key in ("project_id", "skill_id"):
        value = fields.get(key, "")
        if not value or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{2,100}", value):
            raise GateReject("INVALID_REQUEST_SCOPE")
    policy = fields.get("run_policy_ref", "")
    if not REF.fullmatch(policy):
        raise GateReject("INVALID_RUN_POLICY_REF")
    if intent not in INTENTS:
        raise GateReject("UNKNOWN_REVIEW_INTENT")
    if intent == "unified" and required_budget != Decimal(DEFAULT_BUDGETS["unified"]):
        raise GateReject("UNIFIED_REVIEW_BUDGET_MISMATCH")
    rawpath = fields.get("package_path", "")
    if not rawpath.startswith("/SKILL-COLLAB/packages/") or ".." in PurePosixPath(rawpath).parts:
        raise GateReject("INVALID_PACKAGE_PATH")
    if Path(rawpath).name != package.name or not package.name.endswith(".zip"):
        raise GateReject("PACKAGE_BASENAME_MISMATCH")
    sha = fields.get("package_sha256", "")
    if not SHA256.fullmatch(sha):
        raise GateReject("INVALID_PACKAGE_SHA256")
    try:
        count = int(fields.get("package_size_bytes", ""))
    except ValueError as e:
        raise GateReject("INVALID_PACKAGE_SIZE") from e
    _check_package(package, sha=sha, size=count)
    return {"status": "PASS_REQUEST_INPUT_ONLY", "request_id": request_id,
            "skill_id": fields["skill_id"],
            "request_sha256": hashlib.sha256(request_bytes).hexdigest(),
            "run_policy_ref": policy, "expected_max_budget_usd": str(required_budget),
            "package_sha256": sha, "package_size_bytes": count,
            "authorization": "NOT_CHECKED", "ready": "NOT_CREATED", "model_calls": 0}


def check_request_for_publication(request: Path, package: Path,
                                  *, intent: str, required_budget: Decimal) -> dict:
    """Strict schema/ZIP/source-input check; no Windows config and no authority."""
    result = _check_request_inputs(request, package, intent=intent,
                                   required_budget=required_budget)
    if result["run_policy_ref"] not in INTENTS[intent]:
        raise GateReject("RUN_POLICY_NOT_PUBLISHABLE_FOR_INTENT")
    return result


def check_request(request: Path, package: Path, live_config: Path,
                  *, intent: str, required_budget: Decimal) -> dict:
    """Existing host-specific policy compatibility check (NOT authorization)."""
    result = _check_request_inputs(request, package, intent=intent,
                                   required_budget=required_budget)
    target = select_policy(_json(live_config), intent, required_budget)
    if result["run_policy_ref"] != target:
        raise GateReject(f"RUN_POLICY_NOT_LIVE_MATCH: requested={result['run_policy_ref']} supported={target}")
    result["status"] = "PASS_PREPUBLICATION_ONLY"
    return result



def check_source_pin(pin_path: Path, expected_repo_id: str, expected_commit: str) -> None:
    if not REPO_ID.fullmatch(expected_repo_id) or not COMMIT.fullmatch(expected_commit):
        raise GateReject("INVALID_EXPECTED_SOURCE_PIN")
    pin = _json(pin_path, limit=8192)
    if set(pin) != {"schema", "commit", "repo_id"} or pin.get("schema") != "SKILL_COLLAB_SOURCE_PIN_V1":
        raise GateReject("SOURCE_PIN_SCHEMA_MISMATCH")
    if type(pin.get("repo_id")) is not str or pin["repo_id"] != expected_repo_id:
        raise GateReject("SOURCE_PIN_REPO_ID_MISMATCH")
    if type(pin.get("commit")) is not str or pin["commit"] != expected_commit:
        raise GateReject("SOURCE_PIN_COMMIT_MISMATCH")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Offline prepublish gate; never approves/executes/posts")
    subs = parser.add_subparsers(dest="command", required=True)
    for command in ("select", "check"):
        p = subs.add_parser(command)
        p.add_argument("--live-config", type=Path, required=True,
                       help="actual Windows local reviewer.config.json, never GitHub")
        p.add_argument("--intent", choices=sorted(INTENTS), required=True)
        p.add_argument("--required-budget-usd", default=None,
                       help="required per-review budget, default unified=3 (legacy skill=1.5/design=3)")
        if command == "check":
            p.add_argument("--request", required=True, type=Path, help="new REQUEST before publish")
            p.add_argument("--package", required=True, type=Path, help="exact local ZIP bytes")
            p.add_argument("--source-pin", type=Path, help="optional post-commit pin check")
            p.add_argument("--expected-repo-id", help="required with --source-pin")
            p.add_argument("--expected-source-commit", help="required with --source-pin")
    args = parser.parse_args(argv)
    try:
        budget = _target_money(args.required_budget_usd or DEFAULT_BUDGETS[args.intent])
        if args.command == "select":
            ref = select_policy(_json(args.live_config), args.intent, budget)
            print(json.dumps({"status": "POLICY_COMPATIBLE_NOT_APPROVED",
                              "selected_run_policy_ref": ref,
                              "expected_max_budget_usd": str(budget), "approval": "NOT_CHECKED"}))
        else:
            result = check_request(args.request, args.package, args.live_config,
                                   intent=args.intent, required_budget=budget)
            if any((args.source_pin, args.expected_repo_id, args.expected_source_commit)):
                if not all((args.source_pin, args.expected_repo_id, args.expected_source_commit)):
                    raise GateReject("INCOMPLETE_SOURCE_PIN_CHECK")
                check_source_pin(args.source_pin, args.expected_repo_id, args.expected_source_commit)
                result["source_pin"] = "PASS"
            print(json.dumps(result, sort_keys=True))
    except (GateReject, OSError, UnicodeError) as e:
        print("REQUEST_PREFLIGHT_BLOCKED: " + str(e), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
