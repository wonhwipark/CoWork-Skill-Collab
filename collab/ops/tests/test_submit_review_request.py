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
from unittest.mock import patch

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

    def submit(self, publish=False, approval_route='manual', delegated_skills=()):
        return mod.submit(root=self.local, request_draft=self.req, package=self.pkg,
                          live_config=self.config, publish=publish,
                          expected_origin=str(self.origin),
                          approval_route=approval_route, delegated_skills=delegated_skills)

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

    def test_input_package_changed_after_preflight_is_blocked(self):
        original = mod.check_request_for_publication
        def altered(*args, **kwargs):
            result = original(*args, **kwargs)
            self.pkg.write_bytes(b'changed-after-validation')
            return result
        with patch.object(mod, 'check_request_for_publication', side_effect=altered):
            with self.assertRaisesRegex(mod.SubmissionBlocked, 'PACKAGE_CHANGED_AFTER_PREFLIGHT'):
                self.submit(publish=True)
        self.assertFalse((self.local / f'collab/requests/{RID}').exists())

    def test_input_request_changed_after_preflight_is_blocked(self):
        original = mod.check_request_for_publication
        def altered(*args, **kwargs):
            result = original(*args, **kwargs)
            self.req.write_bytes(self.req.read_bytes() + b'\npost-check-change\n')
            return result
        with patch.object(mod, 'check_request_for_publication', side_effect=altered):
            with self.assertRaisesRegex(mod.SubmissionBlocked, 'REQUEST_CHANGED_AFTER_PREFLIGHT'):
                self.submit(publish=True)
        self.assertFalse((self.local / f'collab/requests/{RID}').exists())

    def test_package_hash_mismatch_blocks(self):
        self.pkg.write_bytes(b'invalid zip')
        with self.assertRaises(Exception):
            self.submit(publish=True)
        self.assertFalse((self.local / f'collab/requests/{RID}').exists())

    def test_live_budget_mismatch_is_advisory_not_submission_blocker(self):
        self.config.write_text(json.dumps({
            'review_policy': {'known_run_policy_refs': {
                'POLICY-STATIC-V1': {'max_budget_usd': 1.50}}}}))
        result = self.submit(publish=True)
        self.assertEqual(result['status'], 'SUBMITTED_AWAITING_PROTECTED_SIGNER')
        self.assertEqual(result['host_policy_advisory'], 'NOT_APPLICABLE_HOST_OWNS_EXECUTION_AUTHORITY')
        self.assertEqual(result['signer_authority'], 'NOT_VERIFIED')
        self.assertFalse((self.local / f'collab/requests/{RID}/READY.md').exists())

    def test_publish_without_windows_config_is_allowed(self):
        self.config.unlink()
        result = mod.submit(root=self.local, request_draft=self.req, package=self.pkg,
                            expected_origin=str(self.origin), publish=True)
        self.assertEqual(result['status'], 'SUBMITTED_AWAITING_PROTECTED_SIGNER')
        self.assertEqual(result['host_policy_advisory'], 'NOT_APPLICABLE_HOST_OWNS_EXECUTION_AUTHORITY')
        self.assertFalse((self.local / f'collab/requests/{RID}/APPROVAL_SIG.json').exists())
        self.assertFalse((self.local / f'collab/requests/{RID}/READY.md').exists())

    def test_wrong_policy_ref_still_blocks_before_git_publication(self):
        self.req.write_bytes(self.req.read_bytes().replace(
            b'run_policy_ref: POLICY-STATIC-V1\n',
            b'run_policy_ref: POLICY-STATIC-V1-LARGE\n'))
        with self.assertRaisesRegex(Exception, 'RUN_POLICY_NOT_PUBLISHABLE_FOR_INTENT'):
            self.submit(publish=True)
        self.assertFalse((self.local / f'collab/requests/{RID}').exists())

    def test_untrusted_origin_blocks(self):
        with self.assertRaisesRegex(mod.SubmissionBlocked, 'UNTRUSTED_ORIGIN'):
            mod.submit(root=self.local, request_draft=self.req, package=self.pkg,
                       live_config=self.config, publish=True)


    def test_out_of_scope_skill_can_be_published_not_authorized(self):
        result = self.submit(publish=True, approval_route='auto',
                             delegated_skills=('l1-knowledge-updater', 'cowork-dashboard'))
        self.assertEqual(result['delegation_scope_preflight'], 'NOT_CHECKED_HOST_AUTHORITY')
        self.assertEqual(result['signer_authority'], 'NOT_VERIFIED')
        self.assertEqual(result['ready'], 'NOT_CREATED')

    def test_auto_without_delegation_data_is_only_publication(self):
        result = self.submit(publish=True, approval_route='auto')
        self.assertEqual(result['status'], 'SUBMITTED_AWAITING_PROTECTED_SIGNER')
        self.assertEqual(result['delegation_scope_preflight'], 'NOT_CHECKED_HOST_AUTHORITY')
        self.assertEqual(result['model_calls'], 0)

    def test_auto_scope_match_is_only_preflight_not_signature(self):
        output = self.submit(publish=True, approval_route='auto',
                             delegated_skills=('synthetic-review',))
        self.assertEqual(output['approval_route'], 'auto')
        self.assertEqual(output['delegation_scope_preflight'], 'NOT_CHECKED_HOST_AUTHORITY')
        self.assertEqual(output['signer_authority'], 'NOT_VERIFIED')
        self.assertEqual(output['ready'], 'NOT_CREATED')

    def test_bad_cost_config_is_not_read_for_publication(self):
        self.config.write_text('{not valid json}')
        result = self.submit(publish=True)
        self.assertEqual(result['status'], 'SUBMITTED_AWAITING_PROTECTED_SIGNER')
        self.assertEqual(result['host_policy_advisory'], 'NOT_APPLICABLE_HOST_OWNS_EXECUTION_AUTHORITY')
        self.assertEqual(result['ready'], 'NOT_CREATED')

    def test_manual_route_preserves_explicit_approval_requirement(self):
        output = self.submit(publish=False, approval_route='manual')
        self.assertEqual(output['delegation_scope_preflight'],
                         'MANUAL_PROTECTED_APPROVAL_REQUIRED')
        self.assertEqual(output['signer_authority'], 'NOT_VERIFIED')
        self.assertEqual(output['ready'], 'NOT_CREATED')



    def observe(self, **kwargs):
        return mod.observe_remote_status(self.local, RID, expected_origin=str(self.origin), **kwargs)

    def advance_remote(self, files):
        foreign = Path(self.temp.name) / 'status_other'
        subprocess.check_call(['git', 'clone', '-q', str(self.origin), str(foreign)])
        git(foreign, 'config', 'user.name', 'Regression')
        git(foreign, 'config', 'user.email', 'regression@example.invalid')
        for rel, body in files.items():
            path = foreign / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body, encoding='utf-8')
        git(foreign, 'add', '.')
        git(foreign, 'commit', '-qm', 'synthetic status')
        git(foreign, 'push', 'origin', 'HEAD:refs/heads/main')

    def test_post_submission_is_observed_not_authorized(self):
        out = self.submit(publish=True)['post_submission']
        self.assertEqual(out['stage'], 'SUBMITTED_AWAITING_PROTECTED_SIGNER')
        self.assertEqual(out['host_ack'], 'UNKNOWN')
        self.assertFalse(out['authorization_verified'])
        self.assertFalse(out['requeue_allowed'])

    def test_status_accepts_remote_descendant_without_updating_checkout(self):
        out = self.submit(publish=True)
        local = git(self.local, 'rev-parse', 'HEAD')
        tracking = git(self.local, 'rev-parse', 'refs/remotes/origin/main')
        base = f'collab/requests/{RID}'
        self.advance_remote({f'{base}/APPROVAL_SIG.json': 'fake', f'{base}/READY.md': 'fake'})
        state = self.observe(submitted_commit=out['pin_commit'],
                             frozen_paths=(f'{base}/REQUEST.md', f'{base}/SOURCE_PIN.json',
                                           f'collab/packages/{self.pkg.name}'))
        self.assertEqual(state['stage'], 'READY_ARTIFACTS_PRESENT_UNVERIFIED')
        self.assertFalse(state['execution_verified'])
        self.assertEqual(git(self.local, 'rev-parse', 'HEAD'), local)
        self.assertEqual(git(self.local, 'rev-parse', 'refs/remotes/origin/main'), tracking)
        self.assertFalse(git(self.local, 'status', '--porcelain'))

    def test_status_rejects_frozen_input_change(self):
        out = self.submit(publish=True)
        path = f'collab/requests/{RID}/REQUEST.md'
        self.advance_remote({path: 'changed'})
        with self.assertRaisesRegex(mod.SubmissionBlocked, 'FROZEN_INPUT_CHANGED'):
            self.observe(submitted_commit=out['pin_commit'], frozen_paths=(path,))

    def test_status_partial_ready_does_not_authorize(self):
        self.submit(publish=True)
        self.advance_remote({f'collab/requests/{RID}/READY.md': 'fake'})
        self.assertEqual(self.observe()['stage'], 'PARTIAL_APPROVAL_ARTIFACTS')

    def test_result_and_receipt_presence_does_not_prove_execution(self):
        self.submit(publish=True)
        self.advance_remote({f'collab/reviews/{RID}/REVIEW_RESULT_1.md': 'fake',
                             f'collab/receipts/{RID}/RECEIPT_1.md': 'fake'})
        state = self.observe()
        self.assertEqual(state['stage'], 'REVIEW_RECEIPT_PRESENT_UNVERIFIED')
        self.assertFalse(state['execution_verified'])

    def test_status_untrusted_origin_rejected(self):
        with self.assertRaisesRegex(mod.SubmissionBlocked, 'UNTRUSTED_ORIGIN'):
            mod.observe_remote_status(self.local, RID)

    def test_status_invalid_request_id_rejected(self):
        with self.assertRaisesRegex(mod.SubmissionBlocked, 'INVALID_REQUEST_ID'):
            mod.observe_remote_status(self.local, '../escape', expected_origin=str(self.origin))


if __name__ == '__main__':
    unittest.main()
