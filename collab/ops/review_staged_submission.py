#!/usr/bin/env python3
"""One-shot Windows entry for a Git-pinned CoWork staged review candidate.

Reuses submit_review_request.py for policy validation and two-commit submission.
Does NOT sign, authorize, publish READY, dispatch a review, or install a watcher.
Default is dry run. Never retries a partially published request.
"""
from __future__ import annotations

import argparse
import base64
import binascii
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile

from review_request_gate import GateReject, _front_matter, MAX_PACKAGE
from submit_review_request import SubmissionBlocked, require_clean_main, submit

WORK_ID = re.compile(r"[A-Z0-9][A-Z0-9-]{2,120}\Z")
SHA256 = re.compile(r"[a-f0-9]{64}\Z")
MAX_REQUEST = 256_000


def valid_staged_path(value: str, work_id: str, suffix: str) -> str:
    """Only read files under the designated Work, never arbitrary local paths."""
    root = f"collab/projects/{work_id}/"
    p = PurePosixPath(value)
    if (not value.startswith(root) or value.startswith("/")
            or "\\" in value or ".." in p.parts or value.endswith("/")
            or not value.endswith(suffix) or len(value) > 400):
        raise SubmissionBlocked("UNSAFE_STAGED_SOURCE_PATH")
    return value


def pinned_git_blob(root: Path, path: str, head: str, max_bytes: int) -> bytes:
    """Read only committed bytes at the verified HEAD; no checkout mutation."""
    try:
        # The immutable tree entry must be a regular file, not a symlink or submodule.
        meta = subprocess.run(["git", "-C", str(root), "ls-tree", head, "--", path],
                              capture_output=True, timeout=10, check=False)
        if meta.returncode or not meta.stdout.startswith((b"100644 blob ", b"100755 blob ")):
            raise SubmissionBlocked("STAGED_SOURCE_NOT_REGULAR_GIT_BLOB")
        size = subprocess.run(["git", "-C", str(root), "cat-file", "-s", f"{head}:{path}"],
                              capture_output=True, timeout=10, check=False)
        if size.returncode or not size.stdout.strip().isdigit() or not 0 < int(size.stdout) <= max_bytes:
            raise SubmissionBlocked("STAGED_SOURCE_UNAVAILABLE_OR_OVERSIZED")
        proc = subprocess.run(["git", "-C", str(root), "show", f"{head}:{path}"],
                              capture_output=True, timeout=30, check=False)
    except (OSError, subprocess.TimeoutExpired):
        raise SubmissionBlocked("STAGED_GIT_READ_UNCERTAIN") from None
    if proc.returncode != 0 or len(proc.stdout) != int(size.stdout):
        raise SubmissionBlocked("STAGED_SOURCE_UNAVAILABLE_OR_OVERSIZED")
    return proc.stdout


def prepare_staged_inputs(root: Path, work_id: str, draft_path: str,
                          candidate_path: str, head: str) -> tuple[bytes, bytes, str]:
    if not WORK_ID.fullmatch(work_id):
        raise SubmissionBlocked("INVALID_WORK_ID")
    draft_path = valid_staged_path(draft_path, work_id, ".md")
    candidate_path = valid_staged_path(candidate_path, work_id, ".zip.base64")
    if draft_path == candidate_path:
        raise SubmissionBlocked("STAGED_PATH_CONFLICT")
    request = pinned_git_blob(root, draft_path, head, MAX_REQUEST)
    try:
        fields = _front_matter(request.decode("utf-8"))
    except (UnicodeDecodeError, GateReject):
        raise SubmissionBlocked("INVALID_STAGED_REQUEST") from None
    if fields.get("project_id") != work_id or fields.get("work_id") != work_id:
        raise SubmissionBlocked("STAGED_WORK_MISMATCH")
    pkgpath = fields.get("package_path", "")
    if not pkgpath.startswith("/SKILL-COLLAB/packages/"):
        raise SubmissionBlocked("STAGED_PACKAGE_PATH_MISMATCH")
    name = PurePosixPath(pkgpath).name
    if (not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{4,180}\.zip", name)
            or name != pkgpath.rsplit("/", 1)[-1]):
        raise SubmissionBlocked("STAGED_PACKAGE_NAME_INVALID")
    try:
        size = int(fields.get("package_size_bytes", ""))
    except ValueError:
        raise SubmissionBlocked("INVALID_STAGED_PACKAGE_SIZE") from None
    sha = fields.get("package_sha256", "")
    if not 0 < size <= MAX_PACKAGE or not SHA256.fullmatch(sha):
        raise SubmissionBlocked("INVALID_STAGED_PACKAGE_PIN")
    base64_max = ((size + 2) // 3) * 4 + 4096
    encoded = pinned_git_blob(root, candidate_path, head, base64_max)
    try:
        package = base64.b64decode(b"".join(encoded.split()), validate=True)
    except (ValueError, binascii.Error):
        raise SubmissionBlocked("STAGED_BASE64_INVALID") from None
    if len(package) != size or hashlib.sha256(package).hexdigest() != sha:
        raise SubmissionBlocked("STAGED_PACKAGE_SHA_OR_SIZE_MISMATCH")
    return request, package, name


def run(*, root: Path, work_id: str, draft_path: str, candidate_path: str,
        live_config: Path, publish: bool = False, approval_route: str = "manual",
        delegated_skills: tuple[str, ...] = ()) -> dict:
    root = root.resolve()
    # Verifies clean main and exact remote HEAD before any local files or Git writes.
    head = require_clean_main(root)
    draft, package, name = prepare_staged_inputs(root, work_id, draft_path,
                                                  candidate_path, head)
    with tempfile.TemporaryDirectory(prefix="cowork-staged-review-") as tmp:
        work = Path(tmp)
        req = work / "REQUEST.md"
        pkg = work / name
        req.write_bytes(draft)
        pkg.write_bytes(package)
        result = submit(root=root, request_draft=req, package=pkg,
                        live_config=live_config, publish=publish,
                        approval_route=approval_route,
                        delegated_skills=delegated_skills)
    result.update({"source_head": head,
                   "staged_draft": draft_path,
                   "staged_candidate": candidate_path,
                   "host_signer": "NOT_INVOKED",
                   "ready": "NOT_CREATED",
                   "no_model_calls_by_entry": True})
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo-root", type=Path, required=True)
    ap.add_argument("--work-id", required=True)
    ap.add_argument("--draft-path", required=True)
    ap.add_argument("--candidate-path", required=True)
    ap.add_argument("--live-config", type=Path, required=True)
    ap.add_argument("--approval-route", choices=("manual", "auto"), default="manual")
    ap.add_argument("--delegated-skill", action="append", default=[])
    ap.add_argument("--publish", action="store_true", help="only submit REQUEST/ZIP and SOURCE_PIN; never READY")
    args = ap.parse_args()
    try:
        result = run(root=args.repo_root, work_id=args.work_id,
                     draft_path=args.draft_path, candidate_path=args.candidate_path,
                     live_config=args.live_config, publish=args.publish,
                     approval_route=args.approval_route,
                     delegated_skills=tuple(args.delegated_skill))
        print(json.dumps(result, sort_keys=True, ensure_ascii=False))
        return 0
    except (SubmissionBlocked, GateReject, OSError, ValueError) as exc:
        print("STAGED_REVIEW_SUBMISSION_BLOCKED: " + str(exc), file=sys.stderr)
        print("Do not retry automatically. Inspect source HEAD and protected signer history.", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
