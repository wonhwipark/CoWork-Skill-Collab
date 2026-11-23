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


def write_lf(path, data, encoding='utf-8'):
    # Windows text mode writes CRLF; the verified inputs are LF bytes as served by GitHub.
    path.write_bytes(data.encode(encoding))

SCRIPT = Path(__file__).resolve().parents[3] / 'collab/tools/gpt_disposition_actions.py'

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
            inventory = bridge.package_inputs(root, req)
            self.assertIn('design.md', inventory)
            self.assertIn(hashlib.sha256(b'# Design\nHello').hexdigest(), inventory)
            self.assertNotIn('# Design\nHello', inventory)
            req['package_sha256'] = '0' * 64
            with self.assertRaises(bridge.Hold):
                bridge.package_inputs(root, req)

    def test_large_valid_archive_uses_bounded_complete_inventory(self):
        # >8 times the old 110 KB text cap; all bytes remain verified, none
        # silently clipped into the model prompt.
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            folder = root / 'collab/packages'
            folder.mkdir(parents=True)
            archive = folder / 'large.zip'
            names = [f'chunk_{i:02d}.md' for i in range(10)]
            with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as z:
                for i, name in enumerate(names):
                    z.writestr(name, chr(65+i) * 95_000)
                z.writestr('images/binary.bin', b'\\x00\\x01')
            raw = archive.read_bytes()
            req = {'package_path': '/SKILL-COLLAB/packages/large.zip',
                   'package_size_bytes': len(raw),
                   'package_sha256': hashlib.sha256(raw).hexdigest()}
            evidence = bridge.package_inputs(root, req)
            self.assertLessEqual(len(evidence.encode('utf-8')), bridge.MAX_SOURCE)
            self.assertIn('total_text_bytes_verified_not_forwarded: 950000', evidence)
            self.assertIn('member_count: 11', evidence)
            self.assertEqual(sum(name in evidence for name in names), len(names))
            self.assertIn('images/binary.bin', evidence)
            self.assertNotIn('A' * 100, evidence)

    def test_real_v035_package_inventory_preflight_without_network(self):
        # The historical reviewed ZIP is a fixed repository fixture. This test
        # does not verify signatures or call the model; it verifies the package
        # evidence is now bounded while validating all 114 archive entries.
        root = SCRIPT.parents[2]
        req_path = root / 'collab/requests/REQ-COWORK-V035-WATCHER-REVIEW-20261123/REQUEST.md'
        req = bridge.review_chain.metadata(req_path.read_text(encoding='utf-8'))
        evidence = bridge.package_inputs(root, req)
        self.assertIn('member_count: 114', evidence)
        self.assertIn('text_member_count: 109', evidence)
        self.assertIn('total_text_bytes_verified_not_forwarded: 938634', evidence)
        self.assertIn('RELEASE MANIFEST AS PROVIDED', evidence)
        self.assertLessEqual(len(evidence.encode('utf-8')), bridge.MAX_SOURCE)

    def test_secret_in_unforwarded_text_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            folder = root / 'collab/packages'
            folder.mkdir(parents=True)
            archive = folder / 'secret.zip'
            with zipfile.ZipFile(archive, 'w') as z:
                z.writestr('ordinary.md', 'safe')
                z.writestr('unforwarded.txt', 'sk-' + 'X' * 30)
            raw = archive.read_bytes()
            req = {'package_path': '/SKILL-COLLAB/packages/secret.zip',
                   'package_size_bytes': len(raw),
                   'package_sha256': hashlib.sha256(raw).hexdigest()}
            with self.assertRaisesRegex(bridge.Hold, 'POTENTIAL_SECRET_IN_PACKAGE'):
                bridge.package_inputs(root, req)

    def test_release_manifest_evidence_is_not_silently_truncated(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            folder = root / 'collab/packages'
            folder.mkdir(parents=True)
            archive = folder / 'manifest.zip'
            with zipfile.ZipFile(archive, 'w') as z:
                z.writestr('docs/RELEASE_MANIFEST.json', ' ' * 32_001)
                z.writestr('ordinary.md', 'safe')
            raw = archive.read_bytes()
            req = {'package_path': '/SKILL-COLLAB/packages/manifest.zip',
                   'package_size_bytes': len(raw),
                   'package_sha256': hashlib.sha256(raw).hexdigest()}
            with self.assertRaisesRegex(bridge.Hold, 'RELEASE_MANIFEST_EVIDENCE_TOO_LARGE'):
                bridge.package_inputs(root, req)

    def test_output_tokens_bounded_independent_of_cost(self):
        self.assertGreater(bridge.OUT_TOKENS, 0)
        self.assertLessEqual(bridge.OUT_TOKENS, 3000)
        self.assertFalse(hasattr(bridge, 'budget_preflight'))

    def test_github_changed_paths_only(self):
        with patch.object(bridge.subprocess, 'run') as runner:
            runner.return_value.stdout = ('collab/reviews/REQ-ABC-123/REVIEW_RESULT_1.md\n'
                                          'collab/receipts/REQ-ABC-123/RECEIPT_1.md\n'
                                          'collab/reviews/REQ-DEF-123/GPT_DISPOSITION.json\n')
            result = bridge.git_changed('a' * 40, 'b' * 40)
            self.assertEqual(result, ['REQ-ABC-123'])
        with self.assertRaises(bridge.Hold):
            bridge.git_changed('0' * 40, 'b' * 40)

    def test_legacy_cost_flags_do_not_block_explicitly_enabled_valid_call(self):
        def github_get(method, repo, path, token, payload=None):
            return (200, {'private': False}) if path == '' else (404, {})
        evidence = {
            'input': 'test', 'work_id': 'WORK-001',
            'request_revision': '1', 'package_sha256': 'f' * 64,
            'input_sha256': 'e' * 64, 'processing_key': 'TEST',
        }
        writes = []
        def record_write(repo, rel, token, obj, message):
            writes.append((rel, obj))
        env = {
            **self._one_cycle_live_mocks(),
            'COWORK_GPT_COST_POLICY_APPROVED': 'false',
            'COWORK_GPT_PROJECT_SPEND_CAP_CONFIRMED': 'false',
            'COWORK_GPT_MAX_CALL_USD': '0',
            'COWORK_GPT_INPUT_RATE_USD_PER_1M': '',
            'COWORK_GPT_OUTPUT_RATE_USD_PER_1M': '',
        }
        with patch.dict(os.environ, env, clear=True):
            with patch.object(sys, 'argv', ['bridge', '--request-id', 'REQ-TEST-R1']):
                with patch.object(bridge, 'github_json', side_effect=github_get), \
                     patch.object(bridge, 'preflight', return_value=evidence), \
                     patch.object(bridge, 'create_only', side_effect=record_write), \
                     patch.object(bridge, 'call_once', return_value=(
                         {'verdict': 'ACCEPT', 'summary': 'ok', 'findings': [],
                          'limitations': [], 'next_action': 'stop'},
                         {'response_id': 'resp_x', 'usage': {'input_tokens': 17}, 'model': 'gpt-test'})) as model:
                    self.assertEqual(bridge.main(), 0)
                    model.assert_called_once()
        self.assertEqual(len(writes), 3)
        self.assertNotIn('budget_upper_usd', writes[1][1])
        self.assertNotIn('budget_upper_usd', writes[2][1])
        self.assertEqual(writes[2][1]['usage']['input_tokens'], 17)

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

    def test_zip_decompression_limit_before_crc(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            folder = root / 'collab/packages'
            folder.mkdir(parents=True)
            zf = folder / 'test.zip'
            with zipfile.ZipFile(zf, 'w', compression=zipfile.ZIP_DEFLATED) as z:
                z.writestr('giant.bin', b'Z' * 2_000_001)
                z.writestr('design.md', '# tiny')
            raw = zf.read_bytes()
            req = {'package_path': '/SKILL-COLLAB/packages/test.zip',
                   'package_size_bytes': len(raw), 'package_sha256': hashlib.sha256(raw).hexdigest()}
            with self.assertRaisesRegex(bridge.Hold, 'PACKAGE_MEMBER_TOO_LARGE'):
                bridge.package_inputs(root, req)

    def test_no_public_key_blocks_approval(self):
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            write_lf((d / 'REQUEST.md'), '---\nrequest_revision: 1\npackage_sha256: ' + 'f' * 64 + '\nrun_policy_ref: POLICY-STATIC-V1\n---\n')
            write_lf((d / 'READY.md'), '---\nstate: READY\n---\n')
            write_lf((d / 'SOURCE_PIN.json'), json.dumps({'schema': 'SKILL_COLLAB_SOURCE_PIN_V1',
                                                              'repo_id': '1451933830', 'commit': 'a'*40}))
            reqsha = hashlib.sha256((d / 'REQUEST.md').read_bytes()).hexdigest()
            readysha = hashlib.sha256((d / 'READY.md').read_bytes()).hexdigest()
            payload = {'schema': 'SKILL_COLLAB_APPROVAL_PAYLOAD_V1', 'request_id': d.name,
                       'request_revision': '1', 'request_sha256': reqsha, 'ready_sha256': readysha,
                       'package_sha256': 'f'*64, 'package_size_bytes': None, 'repo_id': '1451933830',
                       'source_commit': 'a'*40, 'run_policy_ref': 'POLICY-STATIC-V1'}
            write_lf((d / 'APPROVAL_SIG.json'), json.dumps({'schema': 'SKILL_COLLAB_APPROVAL_SIG_V1',
                                                              'payload': payload, 'signature': ''}))
            with self.assertRaises(bridge.Hold):
                bridge.approval_check(d / 'REQUEST.md', d / 'READY.md', d / 'SOURCE_PIN.json',
                                      d / 'APPROVAL_SIG.json', '1451933830', public_key_b64=None)


    def _one_cycle_fixture(self, root, rid, work_id):
        request = root / 'collab' / 'requests' / rid
        request.mkdir(parents=True, exist_ok=True)
        write_lf((request / 'REQUEST.md'), 
            f'---\nrequest_id: {rid}\nwork_id: {work_id}\n---\n', encoding='utf-8')
        anchor = root / 'collab' / 'projects' / work_id
        anchor.mkdir(parents=True, exist_ok=True)
        write_lf((anchor / 'CURRENT.md'), 'Current', encoding='utf-8')

    def test_one_cycle_first_request_accepted_read_only(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._one_cycle_fixture(root, 'REQ-TEST-R1', 'WORK-001')
            self.assertEqual(bridge.one_cycle_work_id(root, 'REQ-TEST-R1'), 'WORK-001')

    def test_one_cycle_second_request_same_work_blocked(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._one_cycle_fixture(root, 'REQ-TEST-R1', 'WORK-001')
            self._one_cycle_fixture(root, 'REQ-TEST-R2', 'WORK-001')
            with self.assertRaisesRegex(bridge.Hold, 'WORK_SINGLE_CYCLE_ALREADY_REQUESTED'):
                bridge.one_cycle_work_id(root, 'REQ-TEST-R2')

    def test_completed_review_with_prior_requests_allows_first_gpt_disposition(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._one_cycle_fixture(root, 'REQ-TEST-R1', 'WORK-001')
            self._one_cycle_fixture(root, 'REQ-TEST-R2', 'WORK-001')
            # Strict gate remains active for new review request submission.
            with self.assertRaisesRegex(bridge.Hold, 'WORK_SINGLE_CYCLE_ALREADY_REQUESTED'):
                bridge.one_cycle_work_id(root, 'REQ-TEST-R2')
            # Only a completed review chain can enter post-review disposition.
            with patch.object(bridge.review_chain, 'inspect', create=True,
                              return_value={'stage': 'GPT_NOT_OBSERVED'}), \
                 patch.object(bridge, 'approval_check'), \
                 patch.object(bridge, 'package_inputs', return_value='safe source'):
                request = root / 'collab/requests/REQ-TEST-R2'
                write_lf((request / 'REQUEST.md'), 
                    '---\nrequest_id: REQ-TEST-R2\nwork_id: WORK-001\n'
                    'request_revision: 1\npackage_sha256: ' + 'f' * 64 + '\n---\n')
                review = root / 'collab/reviews/REQ-TEST-R2'
                receipt = root / 'collab/receipts/REQ-TEST-R2'
                review.mkdir(parents=True)
                receipt.mkdir(parents=True)
                write_lf((review / 'REVIEW_RESULT_1.md'), '# Completed verified review')
                write_lf((receipt / 'RECEIPT_1.md'), '{"processing_key": "VALID"}')
                output = bridge.preflight(root, 'REQ-TEST-R2', '1451933830', 'fake-public-key')
                self.assertEqual(output['work_id'], 'WORK-001')
                self.assertEqual(output['processing_key'], 'VALID')

    def test_completed_review_still_rejects_invalid_work_identity(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._one_cycle_fixture(root, 'REQ-TEST-R1', 'WORK-001')
            anchor = root / 'collab/projects/WORK-001/CURRENT.md'
            anchor.unlink()
            with self.assertRaisesRegex(bridge.Hold, 'WORK_ANCHOR_MISSING'):
                bridge.one_cycle_work_id(root, 'REQ-TEST-R1', completed_review=True)

    def test_one_cycle_different_work_unaffected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._one_cycle_fixture(root, 'REQ-TEST-R1', 'WORK-001')
            self._one_cycle_fixture(root, 'REQ-TEST-R2', 'WORK-002')
            self.assertEqual(bridge.one_cycle_work_id(root, 'REQ-TEST-R2'), 'WORK-002')

    def test_one_cycle_requires_real_work_and_identity(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._one_cycle_fixture(root, 'REQ-TEST-R1', 'WORK-001')
            p = root / 'collab' / 'requests' / 'REQ-TEST-R1' / 'REQUEST.md'
            write_lf(p, '---\nrequest_id: REQ-TEST-R1\n---\n', encoding='utf-8')
            with self.assertRaisesRegex(bridge.Hold, 'WORK_ID_INVALID'):
                bridge.one_cycle_work_id(root, 'REQ-TEST-R1')
            write_lf(p, '---\nrequest_id: REQ-TEST-R1\nwork_id: WORK-001\n---\n', encoding='utf-8')
            (root / 'collab' / 'projects' / 'WORK-001' / 'CURRENT.md').unlink()
            with self.assertRaisesRegex(bridge.Hold, 'WORK_ANCHOR_MISSING'):
                bridge.one_cycle_work_id(root, 'REQ-TEST-R1')

    def _one_cycle_live_mocks(self):
        return {
            'GITHUB_REPOSITORY': 'wonhwipark/CoWork-Skill-Collab',
            'GITHUB_REPOSITORY_ID': '1451933830',
            'GITHUB_REF': 'refs/heads/main', 'GITHUB_TOKEN': 'fake-token',
            'COWORK_GPT_API_ENABLED': 'true',
            'COWORK_GPT_MODEL': 'gpt-test',
            'OPENAI_API_KEY': 'fake-api-key',
        }

    def test_work_claim_is_first_write_before_one_model_call(self):
        def github_get(method, repo, path, token, payload=None):
            return (200, {'private': False}) if path == '' else (404, {})
        evidence = {
            'input': 'test', 'work_id': 'WORK-001',
            'request_revision': '1', 'package_sha256': 'f' * 64,
            'input_sha256': 'e' * 64, 'processing_key': 'TEST',
        }
        writes = []
        def record_write(repo, rel, token, obj, message):
            writes.append(rel)
        with patch.dict(os.environ, self._one_cycle_live_mocks()):
            with patch.object(sys, 'argv', ['bridge', '--request-id', 'REQ-TEST-R1']):
                with patch.object(bridge, 'github_json', side_effect=github_get), \
                     patch.object(bridge, 'preflight', return_value=evidence), \
                     patch.object(bridge, 'create_only', side_effect=record_write), \
                     patch.object(bridge, 'call_once', return_value=(
                         {'verdict': 'ACCEPT', 'summary': 'ok', 'findings': [],
                          'limitations': [], 'next_action': 'stop'},
                         {'response_id': 'resp_x', 'usage': {}, 'model': 'gpt-test'})) as model:
                    self.assertEqual(bridge.main(), 0)
                    model.assert_called_once()
        self.assertEqual(writes, [
            'collab/projects/WORK-001/ONE_CYCLE_CLAIM.json',
            'collab/reviews/REQ-TEST-R1/GPT_API_EXECUTION_CLAIM.json',
            'collab/reviews/REQ-TEST-R1/GPT_DISPOSITION.json',
        ])

    def test_work_claim_failure_blocks_model_call(self):
        def github_get(method, repo, path, token, payload=None):
            return (200, {'private': False}) if path == '' else (404, {})
        evidence = {
            'input': 'test', 'work_id': 'WORK-001',
            'request_revision': '1', 'package_sha256': 'f' * 64,
            'input_sha256': 'e' * 64, 'processing_key': 'TEST',
        }
        with patch.dict(os.environ, self._one_cycle_live_mocks()):
            with patch.object(sys, 'argv', ['bridge', '--request-id', 'REQ-TEST-R1']):
                with patch.object(bridge, 'github_json', side_effect=github_get), \
                     patch.object(bridge, 'preflight', return_value=evidence), \
                     patch.object(bridge, 'create_only', side_effect=bridge.Hold('OUTPUT_ALREADY_PRESENT_OR_UNREADABLE')), \
                     patch.object(bridge, 'call_once', side_effect=AssertionError('must not call model')):
                    self.assertEqual(bridge.main(), 2)


if __name__ == '__main__':
    unittest.main()
