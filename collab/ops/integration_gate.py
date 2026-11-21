#!/usr/bin/env python3
"""Fail-closed, read-only parallel-development integration preflight.

Reads per-stream descriptors from an existing Work directory. This checks exact
ZIP inclusion and pinned Git source state, not functional correctness or host
installation. No network is used except `git ls-remote` for the authorized repo.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

SCHEMA = 'COWORK_INTEGRATION_GATE_V1'
STREAM_SCHEMA = 'COWORK_INTEGRATION_STREAM_V1'
SHA256 = re.compile(r'^[0-9a-f]{64}$')
GIT_SHA = re.compile(r'^[0-9a-f]{40}$')
STREAM_ID = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_-]{0,79}$')
MAX_UNCOMPRESSED = 100 * 1024 * 1024


class GateError(ValueError):
    pass


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise GateError(reason)


def load_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise GateError(f'INVALID_JSON:{path.name}:{exc}') from exc
    require(isinstance(data, dict), f'OBJECT_REQUIRED:{path.name}')
    return data


def safe_file(root: Path, relative: str) -> Path:
    require(isinstance(relative, str) and relative and '\\' not in relative, 'UNSAFE_PATH')
    p = Path(relative)
    require(not p.is_absolute() and all(part not in ('', '.', '..') for part in p.parts), 'UNSAFE_PATH')
    full = (root / p).resolve()
    require(full.is_relative_to(root.resolve()) and full.is_file(), f'FILE_MISSING_OR_ESCAPE:{relative}')
    return full


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def verify_file(root: Path, record: dict) -> Path:
    require(isinstance(record, dict), 'FILE_RECORD_REQUIRED')
    expected = record.get('sha256')
    require(isinstance(expected, str) and SHA256.fullmatch(expected) is not None, 'INVALID_FILE_SHA256')
    path = safe_file(root, record.get('path'))
    require(file_sha256(path) == expected, f'FILE_SHA_MISMATCH:{record.get("path")}')
    return path


def safe_entry(name: str) -> bool:
    p = Path(name)
    return bool(name and '\\' not in name and not p.is_absolute() and all(x not in ('', '.', '..') for x in p.parts))


def zip_hashes(path: Path) -> dict[str, str]:
    try:
        with zipfile.ZipFile(path) as z:
            infos = z.infolist()
            names = [i.filename for i in infos]
            require(len(set(names)) == len(names), 'ZIP_DUPLICATE_ENTRY')
            require(all(safe_entry(n) for n in names), 'ZIP_UNSAFE_ENTRY')
            require(sum(i.file_size for i in infos) <= MAX_UNCOMPRESSED, 'ZIP_SIZE_LIMIT')
            require(all(not (i.external_attr >> 16 & 0o170000) == 0o120000 for i in infos), 'ZIP_SYMLINK_ENTRY')
            return {i.filename: hashlib.sha256(z.read(i)).hexdigest() for i in infos if not i.is_dir()}
    except (OSError, zipfile.BadZipFile, RuntimeError) as exc:
        raise GateError(f'INVALID_ZIP:{path.name}:{exc}') from exc


def git_cmd(repo: Path, *args: str) -> str:
    try:
        p = subprocess.run(['git', '-C', str(repo), *args], check=True, text=True,
                           capture_output=True, timeout=15)
        return p.stdout.strip()
    except (OSError, subprocess.SubprocessError) as exc:
        raise GateError(f'GIT_CHECK_FAILED:{" ".join(args)}:{exc}') from exc


def verify_git(repo: Path, head: str, branch: str, remote: str) -> None:
    require(isinstance(head, str) and GIT_SHA.fullmatch(head) is not None, 'INVALID_HEAD_SHA')
    require(re.fullmatch(r'[A-Za-z0-9._/-]+', branch or '') is not None, 'INVALID_BRANCH')
    require(re.fullmatch(r'[A-Za-z0-9._-]+', remote or '') is not None, 'INVALID_REMOTE')
    require(git_cmd(repo, 'rev-parse', 'HEAD') == head, 'LOCAL_HEAD_MOVED')
    require(git_cmd(repo, 'status', '--porcelain') == '', 'LOCAL_TREE_DIRTY')
    lines = git_cmd(repo, 'ls-remote', '--exit-code', remote, f'refs/heads/{branch}').splitlines()
    require(len(lines) == 1 and lines[0].split()[0] == head, 'REMOTE_HEAD_MOVED')


def check(work: Path, repo: Path, expected_head: str, branch: str = 'main', remote: str = 'origin') -> dict:
    manifest = load_json(work / 'integration.json')
    require(manifest.get('schema') == SCHEMA, 'INVALID_RELEASE_SCHEMA')
    work_id = manifest.get('work_id')
    require(isinstance(work_id, str) and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{2,99}', work_id) is not None,
            'INVALID_WORK_ID')
    require(manifest.get('branch') == branch, 'BRANCH_MISMATCH')
    mode = manifest.get('mode')
    require(mode in ('development_candidate', 'deployment'), 'INVALID_MODE')
    descriptors = sorted((work / 'streams').glob('*.json'))
    require(bool(descriptors), 'NO_REGISTERED_STREAMS')
    registered = {}
    for path in descriptors:
        s = load_json(path)
        sid = s.get('stream_id')
        require(s.get('schema') == STREAM_SCHEMA and s.get('work_id') == work_id, 'STREAM_SCHEMA_OR_WORK_MISMATCH')
        require(isinstance(sid, str) and STREAM_ID.fullmatch(sid) is not None and sid == path.stem,
                'INVALID_STREAM_ID')
        require(sid not in registered, 'DUPLICATE_STREAM_ID')
        source = verify_file(work, s.get('artifact'))
        entries = s.get('required_entries')
        require(isinstance(entries, dict) and bool(entries), f'EMPTY_STREAM_ENTRIES:{sid}')
        source_hashes = zip_hashes(source)
        for entry, expected in entries.items():
            require(isinstance(entry, str) and safe_entry(entry), f'UNSAFE_STREAM_ENTRY:{sid}')
            require(isinstance(expected, str) and SHA256.fullmatch(expected) is not None,
                    f'INVALID_STREAM_ENTRY_SHA:{sid}:{entry}')
            require(source_hashes.get(entry) == expected, f'STREAM_SOURCE_MISMATCH:{sid}:{entry}')
        registered[sid] = entries
    included = manifest.get('included_streams')
    require(isinstance(included, list) and len(included) == len(set(map(str, included)))
            and set(included) == set(registered), 'UNINTEGRATED_OR_UNKNOWN_STREAM')
    candidate = verify_file(work, manifest.get('candidate'))
    integrated = zip_hashes(candidate)
    merged = manifest.get('merge_resolutions', [])
    require(isinstance(merged, list), 'INVALID_MERGE_RESOLUTIONS')
    resolutions = {}
    for m in merged:
        require(isinstance(m, dict) and isinstance(m.get('entry'), str) and safe_entry(m['entry']),
                'INVALID_MERGE_ENTRY')
        e = m['entry']
        require(e not in resolutions, 'DUPLICATE_MERGE_RESOLUTION')
        verify_file(work, m.get('evidence'))
        require(isinstance(m.get('streams'), list), 'INVALID_MERGE_STREAMS')
        resolutions[e] = set(m['streams'])
    shared = {}
    for sid, entries in registered.items():
        for e, h in entries.items():
            shared.setdefault(e, {})[sid] = h
    for e, claims in shared.items():
        require(e in integrated, f'INTEGRATED_ENTRY_MISSING:{e}')
        expected = set(claims.values())
        if len(expected) == 1:
            require(integrated[e] in expected, f'INTEGRATED_ENTRY_CHANGED:{e}')
            require(e not in resolutions, f'UNNECESSARY_RESOLUTION:{e}')
        else:
            require(e in resolutions and resolutions[e] == set(claims), f'UNRESOLVED_OVERLAP:{e}')
            require(integrated[e] not in expected, f'OVERLAP_NOT_ACTUALLY_MERGED:{e}')
    require(set(resolutions).issubset(shared), 'UNKNOWN_MERGE_RESOLUTION')
    checks = manifest.get('checks')
    require(isinstance(checks, list) and bool(checks), 'NO_TEST_EVIDENCE')
    coverage = set()
    tests = set()
    for c in checks:
        require(isinstance(c, dict) and c.get('status') == 'PASS', 'FAILED_OR_UNKNOWN_TEST')
        require(c.get('type') in ('regression', 'cross_stream', 'security', 'host_e2e'), 'INVALID_TEST_TYPE')
        verify_file(work, c.get('evidence'))
        require(isinstance(c.get('covers'), list) and set(c['covers']).issubset(registered),
                'INVALID_TEST_COVERAGE')
        if c['type'] == 'cross_stream':
            coverage |= set(c['covers'])
        tests.add(c['type'])
    require({'regression', 'cross_stream'}.issubset(tests) and coverage == set(registered),
            'MISSING_CROSS_STREAM_REGRESSION')
    if mode == 'deployment':
        require({'security', 'host_e2e'}.issubset(tests), 'DEPLOYMENT_TEST_GAP')
    baseline = manifest.get('source_base_sha')
    require(isinstance(baseline, str) and GIT_SHA.fullmatch(baseline) is not None, 'INVALID_BASE_SHA')
    verify_git(repo, expected_head, branch, remote)
    require(git_cmd(repo, 'merge-base', '--is-ancestor', baseline, expected_head) == '', 'SOURCE_BASE_NOT_ANCESTOR')
    return {'gate': 'INTEGRATION_PRECHECK_PASS', 'mode': mode,
            'work_id': work_id, 'registered_streams': sorted(registered),
            'candidate_sha256': manifest['candidate']['sha256'],
            'head_sha': expected_head, 'integration_checks': sorted(tests),
            'deployment_approved': False}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--work-dir', type=Path, required=True)
    p.add_argument('--repo-root', type=Path, required=True)
    p.add_argument('--branch', default='main')
    p.add_argument('--expected-head', required=True, help='Live remote SHA read just before publication')
    p.add_argument('--remote', default='origin')
    args = p.parse_args(argv)
    try:
        report = check(args.work_dir.resolve(), args.repo_root.resolve(), args.expected_head, args.branch, args.remote)
        print(json.dumps(report, ensure_ascii=False, sort_keys=True))
        return 0
    except (GateError, TypeError, KeyError) as exc:
        print(json.dumps({'gate': 'INTEGRATION_BLOCKED', 'reason': str(exc),
                          'deployment_approved': False}, ensure_ascii=False, sort_keys=True))
        return 2


if __name__ == '__main__':
    sys.exit(main())
