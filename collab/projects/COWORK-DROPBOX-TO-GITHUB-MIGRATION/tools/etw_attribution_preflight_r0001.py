#!/usr/bin/env python3
"""Validate an anonymized, normalized Windows ETW correlation export.

This is a standalone FAIL-CLOSED diagnostic for ETW process attribution,
NOT an ETW collector, Windows host verifier, or proof of operational isolation.
It reads local JSON data only. Never upload raw ETW/operational paths to GitHub.

Usage: python etw_attribution_preflight_r0001.py <local-normalized-export.json>
Schema: UTC ISO8601 instants; processes have pid, ppid, start, optional end;
events have pid, timestamp, type (file_open/file_read/etc), path and optional tid.
Probe must contain pid, start, end, marker_path. Protected paths are optional;
if absent, operating_file_isolation_status = NOT_ASSESSED.
Raw ETW-to-normalized conversion must be explicitly verified on the host.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def stamp(s):
    if not isinstance(s, str):
        raise ValueError('timestamp must be ISO-8601 string')
    d = datetime.fromisoformat(s.replace('Z', '+00:00'))
    if d.tzinfo is None:
        raise ValueError('timezone required')
    return d.astimezone(timezone.utc)


def match_path(a, b):
    """Comparison is illustrative; actual Win32 canonical/file-id mapping is required."""
    return str(a).replace('/', '\\').rstrip('\\').casefold() == str(b).replace('/', '\\').rstrip('\\').casefold()


def analyze(document):
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
    marker = probe['marker_path']
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
    # PID reuse or contradictory lifetimes must be disambiguated, never silently merged.
    if not candidates.get(pid):
        errors.append('PROBE_PROCESS_NOT_IN_TRACE')
    elif len(candidates[pid]) != 1:
        errors.append('PROBE_PID_AMBIGUOUS')
    else:
        ps, pe = interval(candidates[pid][0])
        if ps > pstart or pe < pend:
            errors.append('PROBE_LIFETIME_NOT_COVERED')

    # Include verified children recursively; no arbitrary PID attribution.
    known = {pid}
    for _ in range(len(procs)):
        new = set(known)
        for childpid, recs in candidates.items():
            for p in recs:
                if int(p.get('ppid', -1)) in known and stamp(p['start']) >= pstart and stamp(p['start']) <= pend:
                    new.add(childpid)
        if new == known:
            break
        known = new
    if any(len(candidates[k]) > 1 for k in known if k in candidates):
        errors.append('PID_REUSE_AMBIGUOUS')

    attributable = []
    for e in events:
        try:
            eid = int(e['pid'])
            et = stamp(e['timestamp'])
            if eid not in known or not (pstart <= et <= pend):
                continue
            recs = candidates.get(eid, [])
            if len(recs) != 1:
                errors.append('EVENT_PID_LIFETIME_AMBIGUOUS')
                continue
            es, ee = interval(recs[0])
            if es <= et <= ee:
                attributable.append(e)
        except (KeyError, TypeError, ValueError):
            errors.append('FILE_EVENT_UNPARSABLE')

    controls = [e for e in attributable if e.get('type') in ('file_open', 'file_read', 'file_create') and match_path(e.get('path',''), marker)]
    if not controls:
        errors.append('POSITIVE_CONTROL_NOT_ATTRIBUTED_TO_PROBE_TREE')
    protected = document.get('protected_paths')
    isolation = 'NOT_ASSESSED'
    hits = 0
    if isinstance(protected, list) and protected:
        hits = sum(any(match_path(e.get('path', ''), p) for p in protected)
                   for e in attributable if e.get('type', '').startswith('file_'))
        if errors:
            isolation = 'NOT_PROVEN'
        else:
            isolation = 'FAIL_ACCESS_OBSERVED' if hits else 'NO_ACCESS_EVENTS_IN_VERIFIED_TRACE'
    # Even positive result is conditional on trustworthiness of Windows normalization and path identities.
    return {
        'attribution_preflight': 'PASS' if not errors else 'FAIL_UNTRUSTED_MEASUREMENT',
        'control_events_attributable': len(controls),
        'probe_tree_process_count': len(known),
        'attributed_file_events': sum(e.get('type', '').startswith('file_') for e in attributable),
        'protected_file_hits': hits,
        'operating_file_isolation_evidence': isolation,
        'errors': sorted(set(errors)),
        'scope': 'NORMALIZED_OFFLINE_DATA_ONLY_NO_WINDOWS_HOST_PASS',
    }


def main():
    if len(sys.argv) != 2:
        print('Usage: python etw_attribution_preflight_r0001.py <local-normalized-export.json>', file=sys.stderr)
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
