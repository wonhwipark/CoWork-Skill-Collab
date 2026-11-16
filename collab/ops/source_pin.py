#!/usr/bin/env python3
"""Canonical CoWork SOURCE_PIN V1 serializer and strict pre-publication verifier.

Local/offline helper only: no GitHub writes, READY, signing, watcher, or LLM calls.
A blocked/uncertain review must be reconciled separately; never patch its pinned
inputs in place to force another processing attempt.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

SCHEMA = "SKILL_COLLAB_SOURCE_PIN_V1"
_COMMIT_RE = re.compile(r"[0-9a-f]{40}\Z")
_REPO_ID_RE = re.compile(r"[1-9][0-9]*\Z")
_EXACT_KEYS = frozenset({"schema", "commit", "repo_id"})


class SourcePinError(ValueError):
    """Malformed pin or unsafe publication input; refuse rather than coerce."""


def canonical_repo_id(value: str | int) -> str:
    """Normalize only producer inputs. Never silently normalize a published pin."""
    if type(value) is int:
        value = str(value)
    if not isinstance(value, str) or _REPO_ID_RE.fullmatch(value) is None:
        raise SourcePinError("repo_id must be a nonzero decimal identifier")
    return value


def make_source_pin(*, source_commit: str, repo_id: str | int) -> dict[str, str]:
    if not isinstance(source_commit, str) or _COMMIT_RE.fullmatch(source_commit) is None:
        raise SourcePinError("commit must be the exact lowercase, 40-hex source commit A")
    return {"schema": SCHEMA, "commit": source_commit, "repo_id": canonical_repo_id(repo_id)}


def verify_source_pin(pin: object, *, expected_repo_id: str | None = None) -> dict[str, str]:
    """Strict consumer/pre-publish check. Numeric JSON repo_id is ALWAYS invalid."""
    if not isinstance(pin, dict) or set(pin) != _EXACT_KEYS or pin.get("schema") != SCHEMA:
        raise SourcePinError("invalid SOURCE_PIN_V1 schema or keys")
    commit, repo_id = pin["commit"], pin["repo_id"]
    if not isinstance(commit, str) or _COMMIT_RE.fullmatch(commit) is None:
        raise SourcePinError("invalid commit pin")
    if type(repo_id) is not str or _REPO_ID_RE.fullmatch(repo_id) is None:
        raise SourcePinError("repo_id MUST be a JSON string, not a number")
    if expected_repo_id is not None and repo_id != canonical_repo_id(expected_repo_id):
        raise SourcePinError("REPO_ID_MISMATCH")
    return pin


def dumps_source_pin(*, source_commit: str, repo_id: str | int) -> str:
    pin = make_source_pin(source_commit=source_commit, repo_id=repo_id)
    verify_source_pin(pin)
    return json.dumps(pin, ensure_ascii=False, indent=2) + "\n"


def _read_checked(path: Path, expected_repo_id: str | None) -> dict[str, str]:
    if path.is_symlink() or not path.is_file() or path.stat().st_size > 8192:
        raise SourcePinError("unsafe or oversized input path")
    pin = json.loads(path.read_text(encoding="utf-8"))
    return verify_source_pin(pin, expected_repo_id=expected_repo_id)


def audit_source_pins(root: Path, *, expected_repo_id: str) -> int:
    """Check all published request pins; no GitHub API or mutation.

    A malformed historical pin is a failure, never silently rewritten.
    """
    base = root / "collab" / "requests"
    if base.is_symlink() or not base.is_dir():
        raise SourcePinError("missing or unsafe collab/requests directory")
    count = 0
    for directory in sorted(base.iterdir()):
        if directory.is_symlink() or not directory.is_dir():
            continue
        path = directory / "SOURCE_PIN.json"
        if path.is_symlink():
            raise SourcePinError(f"unsafe source pin: {path}")
        if path.exists():
            try:
                _read_checked(path, expected_repo_id)
            except (SourcePinError, json.JSONDecodeError) as exc:
                raise SourcePinError(f"{path}: {exc}") from exc
            count += 1
    if count == 0:
        raise SourcePinError("no published SOURCE_PIN.json found")
    return count


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Offline CoWork SOURCE_PIN_V1 generator / validator")
    sub = parser.add_subparsers(dest="command", required=True)
    make = sub.add_parser("create", help="build new pin; never change existing REQUEST or READY")
    make.add_argument("--commit", required=True, help="verified source commit A (40 lowercase hex)")
    make.add_argument("--repo-id", required=True, help="numeric GitHub repository ID (encoded as JSON string)")
    make.add_argument("--output", type=Path, help="local new file only; refuses overwrite")
    audit = sub.add_parser("audit", help="check all published pins without modifying them")
    audit.add_argument("--root", type=Path, default=Path("."))
    audit.add_argument("--expected-repo-id", required=True)
    check = sub.add_parser("check", help="validate existing file without modifying it")
    check.add_argument("path", type=Path)
    check.add_argument("--expected-repo-id", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "create":
            content = dumps_source_pin(source_commit=args.commit, repo_id=args.repo_id)
            if args.output is None:
                sys.stdout.write(content)
            else:
                # No implicit directories or writes to existing pinned input.
                with args.output.open("x", encoding="utf-8", newline="\n") as out:
                    out.write(content)
                print("CREATED: local SOURCE_PIN candidate only; no request/READY posted")
        elif args.command == "audit":
            count = audit_source_pins(args.root, expected_repo_id=args.expected_repo_id)
            print(f"PASS: {count} SOURCE_PIN_V1 files match the repo_id string contract")
        else:
            _read_checked(args.path, args.expected_repo_id)
            print("PASS: SOURCE_PIN_V1 repo_id is a JSON string and matches trust root")
    except (SourcePinError, json.JSONDecodeError, OSError, UnicodeError) as exc:
        print(f"SOURCE_PIN_REJECTED: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
