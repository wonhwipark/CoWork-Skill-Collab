#!/usr/bin/env python3
"""Fail-closed check of an anonymized, normalized ETW correlation export (revision r0002 of the r0001 tool).

Changes against r0001 (r0001 stays untouched):
  * an event of a probe-tree process that falls outside that process's recorded lifetime is an ERROR
    (r0001 dropped it silently, which could hide a protected-file access at the edge of a trace);
  * events of the tree outside the probe window are counted and checked against the protected paths;
  * path comparison expands 8.3 short names; a short name that cannot be expanded makes isolation NOT_PROVEN;
  * optional file identity (events[].file_id, protected_file_ids) catches hard links and junction paths;
    without identities the best possible isolation result is a path-only status that says so.
Scope: normalized offline data only. Raw ETW to normalized conversion must be verified on the host.
Usage: python etw_attribution_preflight_r0002.py <local-normalized-export.json>
"""
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SHORT_NAME = re.compile(r'~\d')
FILE_TYPES = ('file_open', 'file_read', 'file_create', 'file_write')


def stamp(s):
    if not isinstance(s, str):
        raise ValueError('timestamp must be ISO-8601 string')
    d = datetime.fromisoformat(s.replace('Z', '+00:00'))
    if d.tzinfo is None:
        raise ValueError('timezone required')
    return d.astimezone(timezone.utc)


def long_path(path):
    """Expand 8.3 names using the longest existing ancestor (the file itself may be gone)."""
    if os.name != 'nt':
        return path
    import ctypes
    buf = ctypes.create_unicode_buffer(32768)
    head, tail = path, []
    while head:
        n = ctypes.windll.kernel32.GetLongPathNameW(head, buf, 32768)
        if 0 < n < 32768:
            return os.path.join(buf.value, *reversed(tail)) if tail else buf.value
        parent, name = os.path.split(head)
        if not name or parent == head:
            break
        tail.append(name)
        head = parent
    return path


def canonical(path, expand=long_path):
    p = str(path).replace('/', '\\')
    if p.startswith('\\\\?\\'):
        p = p[4:]
    return expand(p.rstrip('\\')).rstrip('\\').casefold()


def has_short_name(path):
    return any(SHORT_NAME.search(part) for part in str(path).replace('/', '\\').split('\\'))


def analyze(document, expand=long_path):
    errors = []
    procs = document.get('processes', [])
    events = document.get('events', [])
    probe = document.get('probe', {})
    collection = document.get('collection', {})
    if not isinstance(procs, list) or not isinstance(events, list):
        raise ValueError('processes and events must be arrays')
    pid = int(probe['pid'])
    pstart, pend = stamp(probe['start']), stamp(probe['end'])
    if not pstart < pend:
        raise ValueError('probe time interval invalid')
    marker = canonical(probe['marker_path'], expand)
    coverage = collection.get('trace_start'), collection.get('trace_end')
    if not all(coverage) or not stamp(coverage[0]) <= pstart or not stamp(coverage[1]) >= pend:
        errors.append('TRACE_COVERAGE_UNPROVEN')
    if collection.get('dropped_events') is None:
        errors.append('TRACE_DROP_COUNT_MISSING')
    elif not isinstance(collection['dropped_events'], int) or collection['dropped_events'] != 0:
        errors.append('TRACE_EVENTS_DROPPED_OR_UNKNOWN')
    if collection.get('process_provider_verified') is not True or collection.get('file_provider_verified') is not True:
        errors.append('ETW_PROVIDERS_NOT_VERIFIED')
    if collection.get('event_pid_field_verified') is not True:
        errors.append('PID_FIELD_MAPPING_UNVERIFIED')
    if collection.get('marker_open_verified') is not True:
        errors.append('CONTROL_OPERATION_UNVERIFIED')

    def interval(p):
        return stamp(p['start']), stamp(p['end']) if p.get('end') else pend

    candidates = {}
    for p in procs:
        try:
            start, end = interval(p)
            if start <= pend and end >= pstart:
                candidates.setdefault(int(p['pid']), []).append(p)
        except (KeyError, ValueError, TypeError):
            errors.append('PROCESS_RECORD_UNPARSABLE')
    if not candidates.get(pid):
        errors.append('PROBE_PROCESS_NOT_IN_TRACE')
    elif len(candidates[pid]) != 1:
        errors.append('PROBE_PID_AMBIGUOUS')
    else:
        ps, pe = interval(candidates[pid][0])
        if ps > pstart or pe < pend:
            errors.append('PROBE_LIFETIME_NOT_COVERED')

    known = {pid}
    for _ in range(len(procs)):
        new = set(known)
        for childpid, recs in candidates.items():
            for p in recs:
                if int(p.get('ppid', -1)) in known and pstart <= stamp(p['start']) <= pend:
                    new.add(childpid)
        if new == known:
            break
        known = new
    if any(len(candidates[k]) > 1 for k in known if k in candidates):
        errors.append('PID_REUSE_AMBIGUOUS')

    attributable, outside_window, outside_lifetime = [], [], []
    for e in events:
        try:
            eid = int(e['pid'])
            if eid not in known:
                continue
            et = stamp(e['timestamp'])
            recs = candidates.get(eid, [])
            if len(recs) != 1:
                errors.append('EVENT_PID_LIFETIME_AMBIGUOUS')
                continue
            es, ee = interval(recs[0])
            if not es <= et <= ee:
                outside_lifetime.append(e)
                errors.append('EVENT_OUTSIDE_PROCESS_LIFETIME')
            elif not pstart <= et <= pend:
                outside_window.append(e)
            else:
                attributable.append(e)
        except (KeyError, TypeError, ValueError):
            errors.append('FILE_EVENT_UNPARSABLE')

    controls = [e for e in attributable if e.get('type') in FILE_TYPES[:3] and canonical(e.get('path', ''), expand) == marker]
    if not controls:
        errors.append('POSITIVE_CONTROL_NOT_ATTRIBUTED_TO_PROBE_TREE')

    protected = document.get('protected_paths')
    protected_ids = {str(i).casefold() for i in document.get('protected_file_ids', [])}
    isolation, hits, notes = 'NOT_ASSESSED', 0, []
    checked = [e for e in attributable + outside_window + outside_lifetime if str(e.get('type', '')).startswith('file_')]
    if isinstance(protected, list) and protected:
        wanted = {canonical(p, expand) for p in protected}
        for e in checked:
            path = e.get('path', '')
            name = canonical(path, expand)
            if has_short_name(name):
                notes.append('SHORT_NAME_UNRESOLVED')
            if name in wanted or (protected_ids and str(e.get('file_id', '')).casefold() in protected_ids):
                hits += 1
        identity_complete = bool(protected_ids) and all(e.get('file_id') for e in checked)
        if errors or notes:
            isolation = 'NOT_PROVEN' if not hits else 'FAIL_ACCESS_OBSERVED'
        elif hits:
            isolation = 'FAIL_ACCESS_OBSERVED'
        elif identity_complete:
            isolation = 'NO_ACCESS_EVENTS_IN_VERIFIED_TRACE'
        else:
            isolation = 'NO_ACCESS_EVENTS_BY_PATH_ONLY_ALIAS_NOT_PROVEN'
    return {
        'attribution_preflight': 'PASS' if not errors else 'FAIL_UNTRUSTED_MEASUREMENT',
        'control_events_attributable': len(controls),
        'probe_tree_process_count': len(known),
        'attributed_file_events': sum(str(e.get('type', '')).startswith('file_') for e in attributable),
        'tree_events_outside_probe_window': len(outside_window),
        'tree_events_outside_process_lifetime': len(outside_lifetime),
        'protected_file_hits': hits,
        'operating_file_isolation_evidence': isolation,
        'errors': sorted(set(errors)),
        'isolation_notes': sorted(set(notes)),
        'scope': 'NORMALIZED_OFFLINE_DATA_ONLY_NO_WINDOWS_HOST_PASS',
    }


def main():
    if len(sys.argv) != 2:
        print('Usage: python etw_attribution_preflight_r0002.py <local-normalized-export.json>', file=sys.stderr)
        return 2
    try:
        result = analyze(json.loads(Path(sys.argv[1]).read_text(encoding='utf-8')))
    except (ValueError, KeyError, TypeError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({'attribution_preflight': 'FAIL_INVALID_INPUT', 'error_type': type(exc).__name__}))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['attribution_preflight'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
