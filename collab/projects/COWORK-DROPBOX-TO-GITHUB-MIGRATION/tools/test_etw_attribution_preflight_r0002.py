import copy
import ctypes
import os
import sys
import tempfile
import unittest

import etw_attribution_preflight_r0002 as m
from etw_attribution_preflight_r0002 import analyze

NOEXPAND = lambda p: p  # noqa: E731  pure-string behaviour, independent of the host
PATH_ONLY = 'NO_ACCESS_EVENTS_BY_PATH_ONLY_ALIAS_NOT_PROVEN'


def example():
    return {
        'collection': {'trace_start': '2026-11-12T12:00:00Z', 'trace_end': '2026-11-12T12:02:00Z',
                       'dropped_events': 0, 'process_provider_verified': True, 'file_provider_verified': True,
                       'event_pid_field_verified': True, 'marker_open_verified': True},
        'probe': {'pid': 14524, 'start': '2026-11-12T12:00:10Z', 'end': '2026-11-12T12:01:00Z',
                  'marker_path': r'C:\sandbox\marker.tmp'},
        'processes': [{'pid': 14524, 'ppid': 8000, 'start': '2026-11-12T12:00:00Z'}],
        'events': [{'pid': 14524, 'tid': 45, 'timestamp': '2026-11-12T12:00:20Z', 'type': 'file_open',
                    'path': r'C:\sandbox\marker.tmp'}],
        'protected_paths': [r'C:\live\state.sqlite3', r'C:\live\state.sqlite3-wal', r'C:\live\state.sqlite3-shm',
                            r'C:\live\watch.lock'],
    }


def run(d):
    return analyze(d, NOEXPAND)


class Baseline(unittest.TestCase):
    """The nine r0001 behaviours still hold."""

    def test_valid_direct_marker(self):
        r = run(example())
        self.assertEqual((r['attribution_preflight'], r['protected_file_hits']), ('PASS', 0))

    def test_wrong_pid_marker_fails(self):
        d = example(); d['events'][0]['pid'] = 25308
        self.assertEqual(run(d)['attribution_preflight'], 'FAIL_UNTRUSTED_MEASUREMENT')

    def test_verified_child_marker_accepted(self):
        d = example(); d['processes'].append({'pid': 25308, 'ppid': 14524, 'start': '2026-11-12T12:00:15Z'})
        d['events'][0]['pid'] = 25308
        self.assertEqual(run(d)['attribution_preflight'], 'PASS')

    def test_unrelated_process_not_accepted(self):
        d = example(); d['processes'].append({'pid': 25308, 'ppid': 123, 'start': '2026-11-12T12:00:15Z'})
        d['events'][0]['pid'] = 25308
        self.assertEqual(run(d)['attribution_preflight'], 'FAIL_UNTRUSTED_MEASUREMENT')

    def test_missing_provider_fails(self):
        d = example(); d['collection']['process_provider_verified'] = False
        self.assertIn('ETW_PROVIDERS_NOT_VERIFIED', run(d)['errors'])

    def test_lost_events_is_not_proven(self):
        d = example(); d['collection']['dropped_events'] = 1
        self.assertEqual(run(d)['operating_file_isolation_evidence'], 'NOT_PROVEN')

    def test_protected_file_access_detected(self):
        d = example(); d['events'].append({'pid': 14524, 'timestamp': '2026-11-12T12:00:25Z', 'type': 'file_open',
                                           'path': r'C:\live\state.sqlite3-wal'})
        self.assertEqual(run(d)['operating_file_isolation_evidence'], 'FAIL_ACCESS_OBSERVED')

    def test_missing_trace_coverage_fails(self):
        d = example(); d['collection']['trace_start'] = '2026-11-12T12:00:30Z'
        self.assertIn('TRACE_COVERAGE_UNPROVEN', run(d)['errors'])

    def test_pid_reuse_fails(self):
        d = example(); d['processes'].append({'pid': 14524, 'ppid': 8000, 'start': '2026-11-12T12:00:30Z'})
        self.assertIn('PROBE_PID_AMBIGUOUS', run(d)['errors'])


class R0002Changes(unittest.TestCase):
    def test_clean_path_only_trace_does_not_claim_alias_safety(self):
        self.assertEqual(run(example())['operating_file_isolation_evidence'], PATH_ONLY)

    def test_tree_event_after_the_process_ended_is_an_error_not_a_silent_drop(self):
        d = example(); d['processes'][0]['end'] = '2026-11-12T12:00:50Z'
        d['probe']['end'] = '2026-11-12T12:00:50Z'
        d['events'].append({'pid': 14524, 'timestamp': '2026-11-12T12:00:55Z', 'type': 'file_open',
                            'path': r'C:\live\state.sqlite3'})
        r = run(d)
        self.assertIn('EVENT_OUTSIDE_PROCESS_LIFETIME', r['errors'])
        self.assertEqual((r['attribution_preflight'], r['tree_events_outside_process_lifetime']),
                         ('FAIL_UNTRUSTED_MEASUREMENT', 1))
        self.assertEqual(r['operating_file_isolation_evidence'], 'FAIL_ACCESS_OBSERVED')

    def test_tree_event_before_the_probe_window_is_counted_and_checked(self):
        d = example()
        d['events'].append({'pid': 14524, 'timestamp': '2026-11-12T12:00:05Z', 'type': 'file_open',
                            'path': r'C:\live\state.sqlite3-shm'})
        r = run(d)
        self.assertEqual((r['tree_events_outside_probe_window'], r['protected_file_hits']), (1, 1))
        self.assertEqual(r['operating_file_isolation_evidence'], 'FAIL_ACCESS_OBSERVED')

    def test_unexpanded_short_name_makes_isolation_not_proven(self):
        d = example(); d['events'].append({'pid': 14524, 'timestamp': '2026-11-12T12:00:25Z', 'type': 'file_open',
                                           'path': r'C:\live\STATE~1.SQL'})
        r = run(d)
        self.assertEqual(r['operating_file_isolation_evidence'], 'NOT_PROVEN')
        self.assertIn('SHORT_NAME_UNRESOLVED', r['isolation_notes'])

    def test_expanded_short_name_is_recognised_as_the_protected_file(self):
        d = example(); d['events'].append({'pid': 14524, 'timestamp': '2026-11-12T12:00:25Z', 'type': 'file_open',
                                           'path': r'C:\live\STATE~1.SQL'})
        r = analyze(d, lambda p: p.replace('STATE~1.SQL', 'state.sqlite3'))
        self.assertEqual((r['protected_file_hits'], r['operating_file_isolation_evidence']), (1, 'FAIL_ACCESS_OBSERVED'))

    def test_hard_link_under_another_name_is_caught_by_file_identity(self):
        d = example(); d['protected_file_ids'] = ['0x1:0xABC']
        d['events'][0]['file_id'] = '0x1:0x1'
        d['events'].append({'pid': 14524, 'timestamp': '2026-11-12T12:00:25Z', 'type': 'file_open',
                            'path': r'C:\sandbox\innocent-name.db', 'file_id': '0x1:0xabc'})
        r = run(d)
        self.assertEqual((r['protected_file_hits'], r['operating_file_isolation_evidence']), (1, 'FAIL_ACCESS_OBSERVED'))

    def test_complete_identities_without_hits_give_the_strong_status(self):
        d = example(); d['protected_file_ids'] = ['0x1:0xabc']; d['events'][0]['file_id'] = '0x1:0x1'
        self.assertEqual(run(d)['operating_file_isolation_evidence'], 'NO_ACCESS_EVENTS_IN_VERIFIED_TRACE')

    def test_one_event_without_identity_keeps_the_weaker_status(self):
        d = example(); d['protected_file_ids'] = ['0x1:0xabc']
        self.assertEqual(run(d)['operating_file_isolation_evidence'], PATH_ONLY)

    def test_input_is_not_mutated(self):
        d = example(); before = copy.deepcopy(d); run(d)
        self.assertEqual(d, before)


@unittest.skipUnless(sys.platform == 'win32', 'Windows file system')
class RealWindowsFileSystem(unittest.TestCase):
    def test_real_8_3_name_expands_to_the_long_name(self):
        with tempfile.TemporaryDirectory() as root:
            long_dir = os.path.join(root, 'a quite long folder name')
            os.mkdir(long_dir)
            target = os.path.join(long_dir, 'protected state file.sqlite3')
            open(target, 'wb').close()
            buf = ctypes.create_unicode_buffer(520)
            ctypes.windll.kernel32.GetShortPathNameW(target, buf, 520)
            if not buf.value or buf.value.lower() == target.lower():
                self.skipTest('8.3 names are disabled on this volume')
            self.assertEqual(m.canonical(buf.value), m.canonical(target))
            d = example(); d['protected_paths'] = [target]
            d['events'].append({'pid': 14524, 'timestamp': '2026-11-12T12:00:25Z', 'type': 'file_open', 'path': buf.value})
            r = analyze(d)
            self.assertEqual((r['protected_file_hits'], r['operating_file_isolation_evidence']), (1, 'FAIL_ACCESS_OBSERVED'))

    def test_real_hard_link_has_the_same_file_identity(self):
        with tempfile.TemporaryDirectory() as root:
            a, b = os.path.join(root, 'a.db'), os.path.join(root, 'other-name.db')
            open(a, 'wb').close()
            try:
                os.link(a, b)
            except OSError:
                self.skipTest('hard links not supported here')
            ident = lambda p: '%x:%x' % (os.stat(p).st_dev, os.stat(p).st_ino)  # noqa: E731
            self.assertEqual(ident(a), ident(b))
            d = example(); d['protected_paths'] = [a]; d['protected_file_ids'] = [ident(a)]
            d['events'][0]['file_id'] = '0x1:0x1'
            d['events'].append({'pid': 14524, 'timestamp': '2026-11-12T12:00:25Z', 'type': 'file_open', 'path': b,
                                'file_id': ident(b)})
            self.assertEqual(analyze(d)['operating_file_isolation_evidence'], 'FAIL_ACCESS_OBSERVED')


if __name__ == '__main__':
    unittest.main()
