#!/usr/bin/env python3
"""Fail-closed CoWork formal-review submitter. No signing, READY, or model calls.

Only supported write path: verified Git main -> Commit A (REQUEST + ZIP) ->
remote readback -> Commit B (SOURCE_PIN) -> pinned-tree check -> remote readback.
No automatic retry: partial publications must be reconciled by an operator.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

from review_request_gate import GateReject, check_request_for_publication
from review_pin_preflight import PreflightBlocked, inspect
from source_pin import dumps_source_pin

REPO = 'wonhwipark/CoWork-Skill-Collab'
BRANCH = 'main'
REPO_ID = '1451933830'
VALID_ORIGINS = {
    f'https://github.com/{REPO}.git', f'https://github.com/{REPO}',
    f'git@github.com:{REPO}.git', f'git@github.com:{REPO}',
    f'ssh://git@github.com/{REPO}.git',
}
RID_RE = re.compile(r'REQ-[A-Z0-9][A-Z0-9-]{3,120}\Z')


class SubmissionBlocked(ValueError):
    pass


def check_approval_route(skill_id: str, approval_route: str,
                         delegated_skills: tuple[str, ...]) -> dict:
    """The publisher does not decide which skill is permitted to run.

    The Windows protected signer alone verifies execution authorization.
    """
    if approval_route not in ('manual', 'auto'):
        raise SubmissionBlocked('INVALID_APPROVAL_ROUTE')
    if approval_route == 'auto':
        return {'approval_route': 'auto',
                'delegation_scope_preflight': 'NOT_CHECKED_HOST_AUTHORITY'}
    return {'approval_route': 'manual',
            'delegation_scope_preflight': 'MANUAL_PROTECTED_APPROVAL_REQUIRED'}


def git(root: Path, *args: str) -> str:
    proc = subprocess.run(['git', '-C', str(root), *args], capture_output=True,
                          text=True, encoding='utf-8', timeout=45, check=False)
    if proc.returncode:
        raise SubmissionBlocked('GIT_FAILURE: ' + ' '.join(args[:2]))
    return proc.stdout.strip()


def require_clean_main(root: Path, *, expected_origin: str | None = None) -> str:
    if Path(git(root, 'rev-parse', '--show-toplevel')).resolve() != root.resolve():
        raise SubmissionBlocked('NOT_REPOSITORY_ROOT')
    if git(root, 'branch', '--show-current') != BRANCH:
        raise SubmissionBlocked('NOT_ON_MAIN')
    if git(root, 'status', '--porcelain', '--untracked-files=normal'):
        raise SubmissionBlocked('DIRTY_WORKTREE')
    remote = git(root, 'remote', 'get-url', 'origin')
    if remote not in ({expected_origin} if expected_origin else VALID_ORIGINS):
        raise SubmissionBlocked('UNTRUSTED_ORIGIN')
    local = git(root, 'rev-parse', 'HEAD')
    ref = git(root, 'ls-remote', 'origin', f'refs/heads/{BRANCH}').split()
    if len(ref) != 2 or ref[1] != f'refs/heads/{BRANCH}' or ref[0] != local:
        raise SubmissionBlocked('STALE_MAIN_OR_REMOTE_UNKNOWN')
    return local


def verify_remote_head(root: Path, expected: str) -> None:
    remote = git(root, 'ls-remote', 'origin', f'refs/heads/{BRANCH}').split()
    if len(remote) != 2 or remote[0] != expected:
        raise SubmissionBlocked('REMOTE_HEAD_READBACK_MISMATCH')


def submit(*, root: Path, request_draft: Path, package: Path,
           live_config: Path | None = None, publish: bool = False, expected_origin: str | None = None,
           approval_route: str = 'manual',
           delegated_skills: tuple[str, ...] = ()) -> dict:
    root = root.resolve()
    original = require_clean_main(root, expected_origin=expected_origin)
    # REQUEST/PIN publication neither prices the review nor authorizes execution.
    # The installed Windows protected signer retains its own current gates.
    result = check_request_for_publication(request_draft, package,
                                           intent='independent')
    policy_advisory = 'NOT_APPLICABLE_HOST_OWNS_EXECUTION_AUTHORITY'
    rid = result['request_id']
    route = check_approval_route(result['skill_id'], approval_route, delegated_skills)
    if not RID_RE.fullmatch(rid):
        raise SubmissionBlocked('INVALID_REQUEST_ID')
    request_rel = f'collab/requests/{rid}/REQUEST.md'
    pin_rel = f'collab/requests/{rid}/SOURCE_PIN.json'
    package_rel = f'collab/packages/{package.name}'
    if (root / request_rel).exists() or (root / pin_rel).exists():
        raise SubmissionBlocked('REQUEST_ID_ALREADY_EXISTS_CREATE_ONLY')
    if git(root, 'ls-tree', '-r', '--name-only', 'HEAD', '--', request_rel, pin_rel):
        raise SubmissionBlocked('REQUEST_ID_ALREADY_IN_HISTORY')
    if package.is_symlink() or request_draft.is_symlink():
        raise SubmissionBlocked('SYMLINK_INPUT')
    source_request = request_draft.read_bytes()
    source_package = package.read_bytes()
    # The same bytes verified above must be the bytes committed. Prevent a
    # concurrent edit between preflight and the immutable Git source commit.
    if hashlib.sha256(source_request).hexdigest() != result['request_sha256']:
        raise SubmissionBlocked('REQUEST_CHANGED_AFTER_PREFLIGHT')
    if (len(source_package) != result['package_size_bytes']
            or hashlib.sha256(source_package).hexdigest() != result['package_sha256']):
        raise SubmissionBlocked('PACKAGE_CHANGED_AFTER_PREFLIGHT')
    target_package = root / package_rel
    if target_package.exists():
        if target_package.is_symlink() or target_package.read_bytes() != source_package:
            raise SubmissionBlocked('EXISTING_PACKAGE_BYTES_DIFFER')
    if not publish:
        return {'status': 'PREPUBLICATION_PASS_NOT_SUBMITTED', 'request_id': rid,
                **route, 'source_head': original, 'package_sha256': result['package_sha256'],
                'host_policy_advisory': policy_advisory,
                'signer_authority': 'NOT_VERIFIED', 'ready': 'NOT_CREATED'}
    request_target = root / request_rel
    request_target.parent.mkdir(parents=True, exist_ok=False)
    request_target.write_bytes(source_request)
    if not target_package.exists():
        target_package.parent.mkdir(parents=True, exist_ok=True)
        target_package.write_bytes(source_package)
    git(root, 'add', '--', request_rel, package_rel)
    git(root, 'commit', '-m', f'review {rid}: immutable REQUEST and ZIP')
    source_commit = git(root, 'rev-parse', 'HEAD')
    git(root, 'push', 'origin', f'HEAD:refs/heads/{BRANCH}')
    verify_remote_head(root, source_commit)
    if (subprocess.check_output(['git', '-C', str(root), 'show', f'{source_commit}:{request_rel}']) != source_request
            or subprocess.check_output(['git', '-C', str(root), 'show', f'{source_commit}:{package_rel}']) != source_package):
        raise SubmissionBlocked('SOURCE_COMMIT_BYTES_READBACK_MISMATCH')
    # Pin refers to Commit A, which already contains REQUEST and ZIP.
    pin_target = root / pin_rel
    pin_target.write_text(dumps_source_pin(source_commit=source_commit, repo_id=REPO_ID),
                          encoding='utf-8', newline='\n')
    git(root, 'add', '--', pin_rel)
    git(root, 'commit', '-m', f'review {rid}: source pin for verified commit A')
    pin_commit = git(root, 'rev-parse', 'HEAD')
    checked = inspect(root=root, request_id=rid, package_repo_path=package_rel,
                      expected_repo_id=REPO_ID, main_commit=pin_commit,
                      approval_mode="manual", delegated_skills=())
    if checked['status'] != 'PASS_PINNED_INPUTS_ONLY' or checked['pinned_commit'] != source_commit:
        raise SubmissionBlocked('PINNED_TREE_PREFLIGHT_FAILED')
    git(root, 'push', 'origin', f'HEAD:refs/heads/{BRANCH}')
    verify_remote_head(root, pin_commit)
    return {'status': 'SUBMITTED_AWAITING_PROTECTED_SIGNER', 'request_id': rid,
            **route, 'source_commit': source_commit, 'pin_commit': pin_commit,
            'package_sha256': result['package_sha256'],
            'host_policy_advisory': policy_advisory,
            'signer_authority': 'NOT_VERIFIED', 'ready': 'NOT_CREATED',
            'model_calls': 0}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo-root', required=True, type=Path)
    ap.add_argument('--request-draft', required=True, type=Path)
    ap.add_argument('--package', required=True, type=Path)
    ap.add_argument('--live-config', type=Path,
                    help='deprecated and ignored; no local price check is used for publication')
    ap.add_argument('--approval-route', choices=('manual', 'auto'), default='manual',
                    help='manual is the safe default; never an approval or signature')
    ap.add_argument('--delegated-skill', action='append', default=[],
                    help='deprecated publication hint; does not prove execution authority')
    ap.add_argument('--publish', action='store_true',
                    help='explicitly push Commit A then Commit B to CoWork main')
    args = ap.parse_args()
    try:
        out = submit(root=args.repo_root, request_draft=args.request_draft,
                     package=args.package, live_config=args.live_config, publish=args.publish,
                     approval_route=args.approval_route,
                     delegated_skills=tuple(args.delegated_skill))
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0
    except (SubmissionBlocked, GateReject, PreflightBlocked, OSError, ValueError,
            subprocess.TimeoutExpired) as exc:
        print('FORMAL_REVIEW_SUBMISSION_BLOCKED: ' + str(exc), file=sys.stderr)
        print('No automatic retry. Reconcile Git HEAD, remote, signer and request history.', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
