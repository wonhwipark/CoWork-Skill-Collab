"""Synthetic bare-Git submission tests; no live GitHub/signer/model calls."""
from __future__ import annotations
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import submit_review_request as mod

RID = 'REQ-TEST-FORMAL-REVIEW-R1-20261121'


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args],
                                   stderr=subprocess.DEVNULL).decode().strip()


class SubmitTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        home = Path(self.temp.name)
        self.origin = home / 'origin.git'
        self.local = home / 'clone'
        self.drafts = home / 'drafts'
        self.drafts.mkdir()
        subprocess.check_call(['git', 'init', '--bare', '-q', '-b', 'main', str(self.origin)])
        subprocess.check_call(['git', 'clone', '-q', str(self.origin), str(self.local)])
        git(self.local, 'config', 'user.name', 'Regression')
        git(self.local, 'config', 'user.email', 'regression@example.invalid')
        (self.local / 'README.md').write_text('init')
        git(self.local, 'add', 'README.md')
        git(self.local, 'commit', '-qm', 'init')
        git(self.local, 'push', 'origin', 'HEAD:refs/heads/main')
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, 'w') as z:
            z.writestr('synthetic.txt', 'safe')
        self.pkg = self.drafts / 'synthetic_v0_1_0_1121.zip'
        self.pkg.write_bytes(buf.getvalue())
        self.req = self.drafts / 'REQUEST.md'
        self.req.write_text(f'''---
schema: SKILL_COLLAB_REVIEW_REQUEST_V1
state: SUBMITTED
request_id: {RID}
request_revision: 1
project_id: L1-TEST-20261121
work_id: L1-TEST-20261121
skill_id: synthetic-review
test_policy: STATIC_ONLY
reviewer_os: WINDOWS
package_path: /SKILL-COLLAB/packages/{self.pkg.name}
package_sha256: {hashlib.sha256(self.pkg.read_bytes()).hexdigest()}
package_size_bytes: {self.pkg.stat().st_size}
run_policy_ref: POLICY-STATIC-V1
---
# Synthetic
''')
        self.config = self.drafts / 'reviewer.config.json'
        self.config.write_text(json.dumps({
            'review_policy': {'known_run_policy_refs': {
                'POLICY-STATIC-V1': {'max_budget_usd': 3.0}}}}))

    def submit(self, publish=False):
        return mod.submit(root=self.local, request_draft=self.req, package=self.pkg,
                          live_config=self.config, publish=publish,
                          expected_origin=str(self.origin))

    def test_preview_has_no_side_effects(self):
        original = git(self.local, 'rev-parse', 'HEAD')
        self.assertEqual(self.submit()['status'], 'PREPUBLICATION_PASS_NOT_SUBMITTED')
        self.assertEqual(git(self.local, 'rev-parse', 'HEAD'), original)
        self.assertFalse((self.local / f'collab/requests/{RID}').exists())

    def test_two_commits_and_pin_points_to_source(self):
        result = self.submit(publish=True)
        self.assertEqual(result['status'], 'SUBMITTED_AWAITING_PROTECTED_SIGNER')
        self.assertNotEqual(result['source_commit'], result['pin_commit'])
        paths = git(self.local, 'ls-tree', '-r', '--name-only', result['source_commit'])
        self.assertIn(f'collab/requests/{RID}/REQUEST.md', paths)
        self.assertIn(f'collab/packages/{self.pkg.name}', paths)
        self.assertNotIn(f'collab/requests/{RID}/SOURCE_PIN.json', paths)
        pin = json.loads((self.local / f'collab/requests/{RID}/SOURCE_PIN.json').read_text())
        self.assertEqual(pin['commit'], result['source_commit'])
        self.assertIs(type(pin['repo_id']), str)
        self.assertEqual(result['model_calls'], 0)
        self.assertFalse((self.local / f'collab/requests/{RID}/READY.md').exists())
        self.assertFalse((self.local / f'collab/requests/{RID}/APPROVAL_SIG.json').exists())

    def test_existing_request_is_not_reused(self):
        self.submit(publish=True)
        with self.assertRaisesRegex(mod.SubmissionBlocked, 'REQUEST_ID_ALREADY'):
            self.submit(publish=True)

    def test_stale_remote_blocks(self):
        foreign = Path(self.temp.name) / 'other'
        subprocess.check_call(['git', 'clone', '-q', str(self.origin), str(foreign)])
        git(foreign, 'config', 'user.name', 'Regression')
        git(foreign, 'config', 'user.email', 'regression@example.invalid')
        (foreign / 'other.txt').write_text('new')
        git(foreign, 'add', 'other.txt')
        git(foreign, 'commit', '-qm', 'change')
        git(foreign, 'push', 'origin', 'HEAD:refs/heads/main')
        with self.assertRaisesRegex(mod.SubmissionBlocked, 'STALE_MAIN'):
            self.submit(publish=True)

    def test_dirty_worktree_blocks(self):
        (self.local / 'untracked.txt').write_text('dirty')
        with self.assertRaisesRegex(mod.SubmissionBlocked, 'DIRTY_WORKTREE'):
            self.submit(publish=True)

    def test_package_hash_mismatch_blocks(self):
        self.pkg.write_bytes(b'invalid zip')
        with self.assertRaises(Exception):
            self.submit(publish=True)
        self.assertFalse((self.local / f'collab/requests/{RID}').exists())

    def test_live_budget_mismatch_blocks(self):
        self.config.write_text(json.dumps({
            'review_policy': {'known_run_policy_refs': {
                'POLICY-STATIC-V1': {'max_budget_usd': 1.50}}}}))
        with self.assertRaises(Exception):
            self.submit(publish=True)
        self.assertFalse((self.local / f'collab/requests/{RID}').exists())

    def test_untrusted_origin_blocks(self):
        with self.assertRaisesRegex(mod.SubmissionBlocked, 'UNTRUSTED_ORIGIN'):
            mod.submit(root=self.local, request_draft=self.req, package=self.pkg,
                       live_config=self.config, publish=True)


if __name__ == '__main__':
    unittest.main()
