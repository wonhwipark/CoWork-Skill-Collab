import copy
import unittest
from etw_attribution_preflight_r0001 import analyze


def example():
    return {
        'collection': {'trace_start':'2026-11-12T12:00:00Z', 'trace_end':'2026-11-12T12:02:00Z',
                       'dropped_events':0, 'process_provider_verified':True,
                       'file_provider_verified':True, 'event_pid_field_verified':True,
                       'marker_open_verified':True},
        'probe': {'pid':14524, 'start':'2026-11-12T12:00:10Z', 'end':'2026-11-12T12:01:00Z', 'marker_path':r'C:\sandbox\marker.tmp'},
        'processes':[{'pid':14524,'ppid':8000,'start':'2026-11-12T12:00:00Z'}],
        'events':[{'pid':14524, 'tid':45, 'timestamp':'2026-11-12T12:00:20Z','type':'file_open','path':r'C:\sandbox\marker.tmp'}],
        'protected_paths':[r'C:\live\state.sqlite3',r'C:\live\state.sqlite3-wal',r'C:\live\state.sqlite3-shm',r'C:\live\watch.lock'],
    }

class CorrelationTests(unittest.TestCase):
    def test_valid_direct_marker(self):
        r=analyze(example()); self.assertEqual(r['attribution_preflight'],'PASS'); self.assertEqual(r['protected_file_hits'],0)
    def test_wrong_pid_marker_fails(self):
        d=example();d['events'][0]['pid']=25308
        r=analyze(d);self.assertEqual(r['attribution_preflight'],'FAIL_UNTRUSTED_MEASUREMENT')
    def test_verified_child_marker_accepted(self):
        d=example();d['processes'].append({'pid':25308,'ppid':14524,'start':'2026-11-12T12:00:15Z'})
        d['events'][0]['pid']=25308
        self.assertEqual(analyze(d)['attribution_preflight'],'PASS')
    def test_unrelated_process_not_accepted(self):
        d=example();d['processes'].append({'pid':25308,'ppid':123,'start':'2026-11-12T12:00:15Z'}); d['events'][0]['pid']=25308
        self.assertEqual(analyze(d)['attribution_preflight'],'FAIL_UNTRUSTED_MEASUREMENT')
    def test_missing_provider_fails(self):
        d=example();d['collection']['process_provider_verified']=False
        self.assertIn('ETW_PROVIDERS_NOT_VERIFIED',analyze(d)['errors'])
    def test_lost_events_fails(self):
        d=example();d['collection']['dropped_events']=1
        self.assertEqual(analyze(d)['operating_file_isolation_evidence'],'NOT_PROVEN')
    def test_protected_file_access_detected(self):
        d=example();d['events'].append({'pid':14524,'timestamp':'2026-11-12T12:00:25Z', 'type':'file_open','path':r'C:\live\state.sqlite3-wal'})
        self.assertEqual(analyze(d)['operating_file_isolation_evidence'],'FAIL_ACCESS_OBSERVED')
    def test_missing_trace_coverage_fails(self):
        d=example();d['collection']['trace_start']='2026-11-12T12:00:30Z'
        self.assertIn('TRACE_COVERAGE_UNPROVEN',analyze(d)['errors'])
    def test_pid_reuse_fails(self):
        d=example();d['processes'].append({'pid':14524,'ppid':8000,'start':'2026-11-12T12:00:30Z'})
        self.assertIn('PROBE_PID_AMBIGUOUS',analyze(d)['errors'])

if __name__ == '__main__':unittest.main()
