"""Offline synthetic cross-session integration tests; no host/release mutation."""
import copy
import hashlib
import importlib.util
import json
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / 'integration_gate.py'
spec = importlib.util.spec_from_file_location('integration_gate', MODULE)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def run(*cmd, cwd=None):
    return subprocess.check_output(cmd, cwd=cwd, text=True, stderr=subprocess.PIPE).strip()


def zipfile_create(path, entries):
    with zipfile.ZipFile(path, 'w') as z:
        for p, data in entries.items():
            z.writestr(p, data)
    return {'path': path.name, 'sha256': gate.file_sha256(path)}


class IntegrationGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.repo = self.root / 'repo'
        self.repo.mkdir()
        self.remote = self.root / 'origin.git'
        run('git', 'init', '-q', '-b', 'main', str(self.repo))
        run('git', '-C', str(self.repo), 'config', 'user.email', 'test@example.invalid')
        run('git', '-C', str(self.repo), 'config', 'user.name', 'Local Test')
        (self.repo / 'README').write_text('fixture\n')
        run('git', '-C', str(self.repo), 'add', 'README')
        run('git', '-C', str(self.repo), 'commit', '-qm', 'initial')
        run('git', 'init', '-q', '--bare', str(self.remote))
        run('git', '-C', str(self.repo), 'remote', 'add', 'origin', str(self.remote))
        run('git', '-C', str(self.repo), 'push', '-q', '-u', 'origin', 'main')
        self.head = run('git', '-C', str(self.repo), 'rev-parse', 'HEAD')
        self.work = self.root / 'work'
        (self.work / 'streams').mkdir(parents=True)
        self.streams = {
            'UI': {'ui/styles.css': b'blue gray', 'viewer/README.txt': b'base'},
            'Write': {'write/editor.py': b'editable', 'viewer/README.txt': b'base'},
        }
        for sid, entries in self.streams.items():
            artifact = zipfile_create(self.work / (sid + '.zip'), entries)
            descriptor = {'schema': gate.STREAM_SCHEMA, 'work_id': 'L1-WORKSPACE-TEST-001',
                          'stream_id': sid, 'artifact': artifact,
                          'required_entries': {p: sha(b) for p, b in entries.items()}}
            (self.work / 'streams' / (sid + '.json')).write_text(json.dumps(descriptor))
        integrated = {'ui/styles.css': b'blue gray', 'write/editor.py': b'editable',
                      'viewer/README.txt': b'base'}
        self.candidate = zipfile_create(self.work / 'combined.zip', integrated)
        self.manifest = {'schema': gate.SCHEMA, 'work_id': 'L1-WORKSPACE-TEST-001',
                         'branch': 'main', 'mode': 'development_candidate', 'source_base_sha': self.head,
                         'candidate': self.candidate, 'included_streams': ['UI', 'Write'],
                         'merge_resolutions': [], 'checks': []}
        self.add_check('regression', ['UI', 'Write'])
        self.add_check('cross_stream', ['UI', 'Write'])
        self.save()

    def add_check(self, kind, covers):
        f = self.work / (kind + '.txt')
        f.write_text(kind + ' PASS by synthetic fixture')
        self.manifest['checks'].append({'type': kind, 'status': 'PASS', 'covers': covers,
                                        'evidence': {'path': f.name, 'sha256': gate.file_sha256(f)}})

    def save(self):
        (self.work / 'integration.json').write_text(json.dumps(self.manifest))

    def verify(self):
        self.save()
        return gate.check(self.work, self.repo, self.head)

    def must_block(self, text):
        with self.assertRaisesRegex(gate.GateError, text):
            self.verify()

    def test_valid_parallel_zip_integration(self):
        v = self.verify()
        self.assertEqual(v['registered_streams'], ['UI', 'Write'])
        self.assertFalse(v['deployment_approved'])

    def test_missing_registered_stream_blocks(self):
        self.manifest['included_streams'] = ['UI']
        self.must_block('UNINTEGRATED_OR_UNKNOWN_STREAM')

    def test_candidate_missing_write_entry_blocks(self):
        self.manifest['candidate'] = zipfile_create(self.work / 'combined2.zip', {'ui/styles.css': b'blue gray', 'viewer/README.txt': b'base'})
        self.must_block('INTEGRATED_ENTRY_MISSING')

    def test_candidate_overwritten_entry_blocks(self):
        self.manifest['candidate'] = zipfile_create(self.work / 'combined2.zip', {'ui/styles.css': b'wrong', 'write/editor.py': b'editable', 'viewer/README.txt': b'base'})
        self.must_block('INTEGRATED_ENTRY_CHANGED')

    def test_conflicting_parallel_changes_need_explicit_resolution(self):
        p = self.work / 'Write.zip'
        entries = {'write/editor.py': b'editable', 'viewer/README.txt': b'write replaces base'}
        artifact = zipfile_create(p, entries)
        descriptor_path = self.work / 'streams' / 'Write.json'
        d = json.loads(descriptor_path.read_text())
        d['artifact'] = artifact
        d['required_entries'] = {k: sha(v) for k, v in entries.items()}
        descriptor_path.write_text(json.dumps(d))
        self.must_block('UNRESOLVED_OVERLAP')
        f = self.work / 'merge-review.txt'
        f.write_text('manual semantic merge review synthetic fixture')
        self.manifest['merge_resolutions'] = [{'entry': 'viewer/README.txt',
                                               'streams': ['UI','Write'],
                                               'evidence': {'path': f.name, 'sha256': gate.file_sha256(f)}}]
        self.manifest['candidate'] = zipfile_create(self.work / 'merged.zip', {'ui/styles.css': b'blue gray', 'write/editor.py': b'editable', 'viewer/README.txt': b'base + write update'})
        self.assertEqual(self.verify()['gate'], 'INTEGRATION_PRECHECK_PASS')

    def test_stale_remote_head_blocks(self):
        with self.assertRaisesRegex(gate.GateError, 'LOCAL_HEAD_MOVED'):
            gate.check(self.work, self.repo, '0' * 40)

    def test_remote_advances_blocks(self):
        (self.repo / 'README').write_text('new commit\n')
        run('git', '-C', str(self.repo), 'add', 'README')
        run('git', '-C', str(self.repo), 'commit', '-qm', 'advance')
        self.must_block('LOCAL_HEAD_MOVED')

    def test_missing_cross_stream_test_blocks(self):
        self.manifest['checks'] = self.manifest['checks'][:1]
        self.must_block('MISSING_CROSS_STREAM_REGRESSION')

    def test_cross_stream_test_must_cover_every_stream(self):
        self.manifest['checks'][1]['covers'] = ['UI']
        self.must_block('MISSING_CROSS_STREAM_REGRESSION')

    def test_deployment_checks_are_stricter(self):
        self.manifest['mode'] = 'deployment'
        self.must_block('DEPLOYMENT_TEST_GAP')
        self.add_check('security', ['UI', 'Write'])
        self.add_check('host_e2e', ['UI', 'Write'])
        self.assertEqual(self.verify()['mode'], 'deployment')

    def test_dirty_checkout_blocks(self):
        (self.repo / 'README').write_text('uncommitted data')
        self.must_block('LOCAL_TREE_DIRTY')

    def test_corrupted_source_zip_blocks(self):
        (self.work / 'UI.zip').write_bytes(b'bad')
        self.must_block('FILE_SHA_MISMATCH')

    def test_zip_path_traversal_blocks(self):
        self.manifest['candidate'] = zipfile_create(self.work / 'unsafe.zip', {'../escape': b'bad'})
        self.must_block('ZIP_UNSAFE_ENTRY')

    def test_duplicate_zip_entries_blocks(self):
        p = self.work / 'dupe.zip'
        with zipfile.ZipFile(p, 'w') as z:
            z.writestr('ui/styles.css', b'a')
            z.writestr('ui/styles.css', b'b')
        self.manifest['candidate'] = {'path': p.name, 'sha256': gate.file_sha256(p)}
        self.must_block('ZIP_DUPLICATE_ENTRY')

    def test_unknown_check_status_blocks(self):
        self.manifest['checks'][0]['status'] = 'NOT_RUN'
        self.must_block('FAILED_OR_UNKNOWN_TEST')

    def test_missing_evidence_blocks(self):
        self.manifest['checks'][0]['evidence']['path'] = 'missing-test.txt'
        self.must_block('FILE_MISSING_OR_ESCAPE')

    def test_unregistered_stream_file_added_later_blocks(self):
        d = json.loads((self.work / 'streams' / 'UI.json').read_text())
        d['stream_id'] = 'Preferences'
        (self.work / 'streams' / 'Preferences.json').write_text(json.dumps(d))
        self.must_block('UNINTEGRATED_OR_UNKNOWN_STREAM')

    def test_cli_reports_block_code(self):
        self.manifest['included_streams'] = ['Write']
        self.save()
        rc = gate.main(['--work-dir', str(self.work), '--repo-root', str(self.repo), '--expected-head', self.head])
        self.assertEqual(rc, 2)


if __name__ == '__main__':
    unittest.main()
