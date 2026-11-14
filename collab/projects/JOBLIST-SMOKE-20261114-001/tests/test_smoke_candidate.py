from pathlib import Path
import importlib.util
import json
import tempfile
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("smoke", ROOT / "scripts/joblist_e2e_smoke.py")
smoke = importlib.util.module_from_spec(spec)
spec.loader.exec_module(smoke)

def test_manifest_only_one_new_one_shot():
    d = json.loads((ROOT / "requests/candidate-one-shot-jobs.json").read_text())
    assert d['schema_version'] == 1 and len(d['jobs']) == 1
    j = d['jobs'][0]
    assert j['job_id'] == smoke.JOB_ID
    assert j['profile'] == smoke.PROFILE
    assert j['params'] == {} and j['platform'] == 'linux'
    assert j['job_id'] != 'JOB-20261112-NR-L1TX-KNOWLEDGE-MSC-EXEC-01'

def test_without_runner_identity_does_not_write():
    with tempfile.TemporaryDirectory() as td:
        home = Path(td)
        root = home / 'l1sw-private-skills/job-list'
        root.mkdir(parents=True)
        with mock.patch.object(smoke.os, 'geteuid', return_value=1000):
            try:
                smoke.run(root=root, home=home, environ={})
            except ValueError as ex:
                assert str(ex) == 'JOB_RUNNER_ATTESTATION_MISSING'
            else:
                raise AssertionError('should block')
        assert not (root / 'output').exists()

def test_valid_runner_record_and_duplicate_refused():
    with tempfile.TemporaryDirectory() as td:
        home = Path(td)
        root = home / 'l1sw-private-skills/job-list'
        root.mkdir(parents=True)
        env = {'JOB_LIST_JOB_ID': smoke.JOB_ID,
               'JOB_LIST_PROFILE': smoke.PROFILE,
               'JOB_LIST_RUN_ID': 'core_20261114_214100_1234abcd'}
        with mock.patch.object(smoke.os, 'geteuid', return_value=1000):
            r = smoke.run(root=root, home=home, environ=env)
            assert r['status'] == 'SUCCESS'
            assert r['llm_invoked'] is False
            assert r['analysis'] == 'NOT_RUN'
            saved = json.loads((root/smoke.RESULT).read_text())
            assert saved['run_id'] == env['JOB_LIST_RUN_ID']
            try:
                smoke.run(root=root, home=home, environ=env)
            except ValueError as ex:
                assert str(ex) == 'SMOKE_RUN_ALREADY_RECORDED'
            else:
                raise AssertionError('duplicate should fail')
