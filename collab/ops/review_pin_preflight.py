#!/usr/bin/env python3
"""Read-only pre-READY source pin / request / package git-tree coherence gate.

Designed to be run before any protected signer or READY action. This script
cannot approve, sign, post READY, run a watcher, or perform model calls.
Requires a locally fetched repository commit explicitly supplied by the caller;
remote main freshness and actual signer authority remain separate host gates.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

from source_pin import SourcePinError, verify_source_pin

HEX40 = re.compile(r"[0-9a-f]{40}\Z")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
DECIMAL = re.compile(r"[1-9][0-9]*\Z")
YAML_SIMPLE = re.compile(r"^([a-zA-Z_][a-zA-Z_0-9]*):[ \t]*(.*?)\s*$")
REQUEST_LIMIT = 262_144
PIN_LIMIT = 8192
PACKAGE_LIMIT = 200 * 1024 * 1024


class PreflightBlocked(ValueError):
    """Fail-closed; errors are not authorization or execution signals."""


def checked_path(value: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        raise PreflightBlocked("INVALID_REPO_PATH")
    p = PurePosixPath(value)
    if p.is_absolute() or any(part in (".", "..", "") for part in value.split("/")):
        raise PreflightBlocked("INVALID_REPO_PATH")
    if str(p) != value:
        raise PreflightBlocked("INVALID_REPO_PATH")
    return value


def run_git(root: Path, *argv: str, timeout: int = 25) -> bytes:
    try:
        p = subprocess.run(
            ["git", "-C", str(root), *argv],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            timeout=timeout, check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise PreflightBlocked("GIT_UNAVAILABLE_OR_TIMEOUT") from exc
    if p.returncode:
        raise PreflightBlocked("GIT_REF_OR_OBJECT_UNAVAILABLE")
    return p.stdout


def git_blob_at(root: Path, commit: str, path: str, limit: int, *, missing_code: str) -> bytes:
    checked_path(path)
    if not HEX40.fullmatch(commit):
        raise PreflightBlocked("INVALID_PIN_COMMIT")
    tree_line = run_git(root, "ls-tree", commit, "--", path).decode("utf-8", "replace").rstrip("\n")
    # A single exact path, regular file only; symlink/submodule/tree is unsafe.
    match = re.fullmatch(r"(100644|100755) blob ([0-9a-f]{40})\t(.+)", tree_line)
    if not match or match.group(3) != path:
        raise PreflightBlocked(missing_code)
    size_raw = run_git(root, "cat-file", "-s", match.group(2))
    try:
        size = int(size_raw.strip())
    except ValueError as exc:
        raise PreflightBlocked("UNREADABLE_BLOB_SIZE") from exc
    if size > limit:
        raise PreflightBlocked("INPUT_TOO_LARGE")
    data = run_git(root, "cat-file", "blob", match.group(2))
    if len(data) != size:
        raise PreflightBlocked("INCONSISTENT_BLOB_SIZE")
    return data


def yaml_header(blob: bytes) -> dict[str, str]:
    try:
        value = blob.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise PreflightBlocked("REQUEST_NOT_UTF8") from exc
    lines = value.splitlines()
    if not lines or lines[0] != "---":
        raise PreflightBlocked("REQUEST_MISSING_FRONTMATTER")
    fields: dict[str, str] = {}
    ended = False
    for line in lines[1:]:
        if line == "---":
            ended = True
            break
        m = YAML_SIMPLE.fullmatch(line)
        if not m:
            raise PreflightBlocked("REQUEST_UNPARSABLE_FRONTMATTER")
        k, v = m.groups()
        if k in fields:
            raise PreflightBlocked("REQUEST_DUPLICATE_FRONTMATTER_KEY")
        fields[k] = v.strip().strip('"\'')
    if not ended:
        raise PreflightBlocked("REQUEST_MISSING_FRONTMATTER_END")
    needed = ("schema", "state", "request_id", "request_revision", "skill_id", "package_path", "package_sha256", "package_size_bytes", "run_policy_ref")
    if any(not fields.get(k) for k in needed):
        raise PreflightBlocked("REQUEST_REQUIRED_FIELD_MISSING")
    if fields["schema"] != "SKILL_COLLAB_REVIEW_REQUEST_V1" or fields["state"] != "SUBMITTED":
        raise PreflightBlocked("REQUEST_SCHEMA_OR_STATE_MISMATCH")
    if not DECIMAL.fullmatch(fields["request_revision"]):
        raise PreflightBlocked("REQUEST_REVISION_INVALID")
    if not HEX64.fullmatch(fields["package_sha256"]):
        raise PreflightBlocked("REQUEST_PACKAGE_SHA_INVALID")
    if not DECIMAL.fullmatch(fields["package_size_bytes"]):
        raise PreflightBlocked("REQUEST_PACKAGE_SIZE_INVALID")
    if not re.fullmatch(r"[A-Za-z][A-Za-z_0-9-]{2,127}", fields["skill_id"]):
        raise PreflightBlocked("REQUEST_SKILL_ID_INVALID")
    return fields


def inspect(
    *, root: Path, request_id: str, package_repo_path: str,
    expected_repo_id: str, main_commit: str,
    approval_mode: str, delegated_skills: tuple[str, ...] = (),
) -> dict[str, object]:
    if not HEX40.fullmatch(main_commit):
        raise PreflightBlocked("INVALID_MAIN_COMMIT")
    if not re.fullmatch(r"REQ-[A-Za-z_0-9-]{4,180}", request_id):
        raise PreflightBlocked("INVALID_REQUEST_ID")
    package_repo_path = checked_path(package_repo_path)
    if approval_mode not in ("auto", "manual"):
        raise PreflightBlocked("INVALID_APPROVAL_MODE")
    if not DECIMAL.fullmatch(expected_repo_id):
        raise PreflightBlocked("INVALID_EXPECTED_REPO_ID")
    request_path = f"collab/requests/{request_id}/REQUEST.md"
    pin_path = f"collab/requests/{request_id}/SOURCE_PIN.json"
    pin_data = git_blob_at(root, main_commit, pin_path, PIN_LIMIT, missing_code="SOURCE_PIN_MISSING")
    try:
        pin = verify_source_pin(json.loads(pin_data.decode("utf-8")), expected_repo_id=expected_repo_id)
    except (ValueError, UnicodeError, SourcePinError) as exc:
        raise PreflightBlocked("SOURCE_PIN_FORMAT_OR_REPO_ID_MISMATCH") from exc
    pinned_commit = pin["commit"]
    current_req = git_blob_at(root, main_commit, request_path, REQUEST_LIMIT, missing_code="REQUEST_MISSING_AT_MAIN")
    pinned_req = git_blob_at(root, pinned_commit, request_path, REQUEST_LIMIT, missing_code="COMMIT_UNREADABLE_REQUEST_ABSENT")
    if current_req != pinned_req:
        raise PreflightBlocked("REQUEST_BYTES_CHANGED_SINCE_PIN")
    data = yaml_header(current_req)
    if data["request_id"] != request_id:
        raise PreflightBlocked("REQUEST_ID_MISMATCH")
    if PurePosixPath(data["package_path"]).name != PurePosixPath(package_repo_path).name:
        raise PreflightBlocked("PACKAGE_PATH_NAME_MISMATCH")
    package = git_blob_at(root, pinned_commit, package_repo_path, PACKAGE_LIMIT, missing_code="COMMIT_UNREADABLE_PACKAGE_ABSENT")
    if len(package) != int(data["package_size_bytes"]):
        raise PreflightBlocked("PACKAGE_SIZE_MISMATCH")
    if hashlib.sha256(package).hexdigest() != data["package_sha256"]:
        raise PreflightBlocked("PACKAGE_SHA256_MISMATCH")
    current_package = git_blob_at(root, main_commit, package_repo_path, PACKAGE_LIMIT, missing_code="PACKAGE_MISSING_AT_MAIN")
    if current_package != package:
        raise PreflightBlocked("PACKAGE_BYTES_CHANGED_SINCE_PIN")
    # This is a *pre-sign* gate. Existing READY must be reconciled, not replayed.
    for name in ("READY.md", "APPROVAL_SIG.json"):
        path = f"collab/requests/{request_id}/{name}"
        line = run_git(root, "ls-tree", main_commit, "--", path).decode("utf-8", "replace").strip()
        if line:
            raise PreflightBlocked("REQUEST_ALREADY_SIGNED_OR_READY_RECONCILE")
    if approval_mode == "auto":
        if not delegated_skills:
            raise PreflightBlocked("DELEGATION_SCOPE_NOT_SUPPLIED")
        if data["skill_id"] not in delegated_skills:
            raise PreflightBlocked("AUTO_NOT_ELIGIBLE_SKILL_ID")
    return {
        "status": "PASS_PINNED_INPUTS_ONLY",
        "request_id": request_id,
        "request_revision": int(data["request_revision"]),
        "pinned_commit": pinned_commit,
        "request_sha256": hashlib.sha256(pinned_req).hexdigest(),
        "package_sha256": data["package_sha256"],
        "package_size_bytes": len(package),
        "skill_id": data["skill_id"],
        "run_policy_ref": data["run_policy_ref"],
        "approval_mode": approval_mode,
        "signer_authority": "NOT_VERIFIED",
        "ready_or_model_calls": 0,
        "next_gate": "PROTECTED_SIGNER_AUTHORITY_AND_DUPLICATE_CHECK",
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Read-only CoWork pre-READY pinned request/package check")
    p.add_argument("--repo-root", required=True, type=Path)
    p.add_argument("--main-commit", required=True, help="Verified remote main commit SHA fetched separately")
    p.add_argument("--request-id", required=True)
    p.add_argument("--package-repo-path", required=True)
    p.add_argument("--expected-repo-id", required=True)
    p.add_argument("--approval-mode", choices=("auto", "manual"), required=True)
    p.add_argument("--delegated-skill", action="append", default=[], help="Actual signer loaded allowlist; for auto mode only")
    args = p.parse_args(argv)
    try:
        result = inspect(root=args.repo_root, request_id=args.request_id,
                         package_repo_path=args.package_repo_path,
                         expected_repo_id=args.expected_repo_id,
                         main_commit=args.main_commit,
                         approval_mode=args.approval_mode,
                         delegated_skills=tuple(args.delegated_skill))
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except (PreflightBlocked, OSError) as exc:
        print(f"REVIEW_PIN_PREFLIGHT_BLOCKED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
