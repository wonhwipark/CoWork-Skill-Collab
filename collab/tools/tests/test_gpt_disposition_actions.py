"""Offline boundary tests. No GitHub writes and no model calls."""
import base64
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch
import zipfile

SCRIPT = Path(__file__).resolve().parents[1] / 'collab/tools/gpt_disposition_actions.py'

# The live script imports existing repo modules; use narrow stubs in isolated fixture.
def metadata(raw):
    if raw.startswith('---\n'):
        lines = raw.split('---', 2)[1].strip().splitlines()
        return {k.strip(): v.strip().strip('"') for ln in lines if ':' in ln
                for k, v in [ln.split(':', 1)]}
    return {}

sys.modules['review_chain'] = types.SimpleNamespace(metadata=metadata)


def pin_check(o, expected_repo_id):
    if o.get('schema') != 'SKILL_COLLAB_SOURCE_PIN_V1' or o.get('repo_id') != expected_repo_id:
        raise ValueError('invalid source pin')
    return o

sys.modules['source_pin'] = types.SimpleNamespace(verify_source_pin=pin_check)
spec = importlib.util.spec_from_file_location('bridge', SCRIPT)
bridge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bridge)


class BridgeTests(unittest.TestCase):
    def test_default_off_no_network(self):
        with patch.dict(os.environ, {'GITHUB_REPOSITORY': 'wonhwipark/CoWork-Skill-Collab',
                                     'GITHUB_REPOSITORY_ID': '1451933830', 'GITHUB_REF': 'refs/heads/main',
                                     'COWORK_GPT_API_ENABLED': 'false'}):
            with patch.object(sys, 'argv', ['bridge']):
                with patch.object(bridge, 'github_json', side_effect=AssertionError('network should not occur')):
                    self.assertEqual(bridge.main(), 0)

    def test_strict_verdict_schema(self):
        d = bridge.response_schema()
        self.assertEqual(d['properties']['verdict']['enum'], list(bridge.DECISIONS))
        self.assertFalse(d['additionalProperties'])
        self.assertEqual(len(d['required']), 5)

    def test_package_ok_and_bad_hash(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            folder = root / 'collab/packages'
            folder.mkdir(parents=True)
            zf = folder / 'test.zip'
            with zipfile.ZipFile(zf, 'w') as z:
                z.writestr('design.md', '# Design\nHello')
            raw = zf.read_bytes()
            req = {'package_path': '/SKILL-COLLAB/packages/test.zip',
                   'package_size_bytes': len(raw), 'package_sha256': hashlib.sha256(raw).hexdigest()}
            self.assertIn('Design', bridge.package_inputs(root, req))
            req['package_sha256'] = '0' * 64
            with self.assertRaises(bridge.Hold):
                bridge.package_inputs(root, req)

    def test_budget_gate_fail_closed(self):
        self.assertEqual(bridge.budget_preflight('x' * 1000, '2.00', '10.00', '0.10'), '0.040192')
        for value in ('', 'nan', '-1', 'oops'):
            with self.assertRaises(bridge.Hold):
                bridge.budget_preflight('x', '2', '10', value)
        with self.assertRaises(bridge.Hold):
            bridge.budget_preflight('x' * 140000, '4', '24', '0.20')

    def test_github_changed_paths_only(self):
        with patch.object(bridge.subprocess, 'run') as runner:
            runner.return_value.stdout = ('collab/reviews/REQ-ABC-123/REVIEW_RESULT_1.md\n'
                                          'collab/receipts/REQ-ABC-123/RECEIPT_1.md\n'
                                          'collab/reviews/REQ-DEF-123/GPT_DISPOSITION.json\n')
            result = bridge.git_changed('a' * 40, 'b' * 40)
            self.assertEqual(result, ['REQ-ABC-123'])
        with self.assertRaises(bridge.Hold):
            bridge.git_changed('0' * 40, 'b' * 40)

    def test_no_api_call_without_external_spend_cap(self):
        with patch.dict(os.environ, {'GITHUB_REPOSITORY': 'wonhwipark/CoWork-Skill-Collab',
                                     'GITHUB_REPOSITORY_ID': '1451933830', 'GITHUB_REF': 'refs/heads/main',
                                     'COWORK_GPT_API_ENABLED': 'true', 'GITHUB_TOKEN': 'not-a-real-token',
                                     'COWORK_GPT_MODEL': 'gpt-6', 'OPENAI_API_KEY': 'fake-key',
                                     'COWORK_GPT_COST_POLICY_APPROVED': 'false',
                                     'COWORK_GPT_PROJECT_SPEND_CAP_CONFIRMED': 'false'}):
            with patch.object(sys, 'argv', ['bridge', '--request-id', 'REQ-TEST-123']):
                def github_get(method, repo, path, token, payload=None):
                    if path == '': return 200, {'private': False}
                    return 404, {}
                with patch.object(bridge, 'github_json', side_effect=github_get), \
                     patch.object(bridge, 'preflight', return_value={'input': 'x' * 1000,
                         'request_revision': '1', 'package_sha256': 'f' * 64,
                         'input_sha256': 'e' * 64, 'processing_key': 'TEST'}), \
                     patch.object(bridge, 'call_once', side_effect=AssertionError('no model call')):
                    self.assertEqual(bridge.main(), 2)

    def test_symlink_zip_member_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            folder = root / 'collab/packages'
            folder.mkdir(parents=True)
            zf = folder / 'test.zip'
            info = zipfile.ZipInfo('link.md')
            info.create_system = 3
            info.external_attr = (0o120777 << 16)
            with zipfile.ZipFile(zf, 'w') as z:
                z.writestr(info, 'design.md')
            raw = zf.read_bytes()
            req = {'package_path': '/SKILL-COLLAB/packages/test.zip',
                   'package_size_bytes': len(raw), 'package_sha256': hashlib.sha256(raw).hexdigest()}
            with self.assertRaises(bridge.Hold):
                bridge.package_inputs(root, req)

    def test_no_public_key_blocks_approval(self):
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            (d / 'REQUEST.md').write_text('---\nrequest_revision: 1\npackage_sha256: ' + 'f' * 64 + '\nrun_policy_ref: POLICY-STATIC-V1\n---\n')
            (d / 'READY.md').write_text('---\nstate: READY\n---\n')
            (d / 'SOURCE_PIN.json').write_text(json.dumps({'schema': 'SKILL_COLLAB_SOURCE_PIN_V1',
                                                              'repo_id': '1451933830', 'commit': 'a'*40}))
            reqsha = hashlib.sha256((d / 'REQUEST.md').read_bytes()).hexdigest()
            readysha = hashlib.sha256((d / 'READY.md').read_bytes()).hexdigest()
            payload = {'schema': 'SKILL_COLLAB_APPROVAL_PAYLOAD_V1', 'request_id': d.name,
                       'request_revision': '1', 'request_sha256': reqsha, 'ready_sha256': readysha,
                       'package_sha256': 'f'*64, 'package_size_bytes': None, 'repo_id': '1451933830',
                       'source_commit': 'a'*40, 'run_policy_ref': 'POLICY-STATIC-V1'}
            (d / 'APPROVAL_SIG.json').write_text(json.dumps({'schema': 'SKILL_COLLAB_APPROVAL_SIG_V1',
                                                              'payload': payload, 'signature': ''}))
            with self.assertRaises(bridge.Hold):
                bridge.approval_check(d / 'REQUEST.md', d / 'READY.md', d / 'SOURCE_PIN.json',
                                      d / 'APPROVAL_SIG.json', '1451933830', public_key_b64=None)


if __name__ == '__main__':
    unittest.main()
