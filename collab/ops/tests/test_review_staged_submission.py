"""Isolated, model-free tests for Git-pinned staged review intake."""
import base64
import hashlib
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest
import zipfile
from unittest.mock import patch

# Only the entrypoint adapter is new. The real submitter and gate have their
# independent regression suites; network and live signer are stubbed here.
gate = types.ModuleType('review_request_gate')
class GateReject(ValueError): pass
gate.GateReject = GateReject
gate.MAX_PACKAGE = 32*1024*1024
def front(text):
    if not text.startswith('---\n'): raise GateReject('bad frontmatter')
    return dict(line.split(': ', 1) for line in text.split('---')[1].strip().split('\n'))
gate._front_matter = front
sys.modules['review_request_gate'] = gate
submitter = types.ModuleType('submit_review_request')
class SubmissionBlocked(ValueError): pass
submitter.SubmissionBlocked = SubmissionBlocked
submitter.require_clean_main = lambda root: subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD']).decode().strip()
submitter.submit = lambda **kwargs: {'status':'PREPUBLICATION_PASS_NOT_SUBMITTED'}
sys.modules['submit_review_request'] = submitter
sys.path.insert(0, str(Path(__file__).resolve().parent))
import review_staged_submission as mod

WORK = 'COWORK-CONTEXT-20261122'
DRAFT = f'collab/projects/{WORK}/REVIEW_DRAFT.md'
CAND = f'collab/projects/{WORK}/REVIEW_CANDIDATE.zip.base64'

class IntakeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'repo'
        self.root.mkdir()
        subprocess.check_call(['git','init','-q','-b','main',str(self.root)])
        subprocess.check_call(['git','-C',str(self.root),'config','user.name','Test'])
        subprocess.check_call(['git','-C',str(self.root),'config','user.email','test@example.invalid'])
        self.zipdata = self.buildzip()
        self.draft = self.make_draft(self.zipdata)
        self.write(DRAFT, self.draft)
        self.write(CAND, base64.b64encode(self.zipdata)+b'\n')
        self.commit()

    def buildzip(self):
        f=io.BytesIO()
        with zipfile.ZipFile(f,'w') as z:z.writestr('design.md','synthetic')
        return f.getvalue()

    def make_draft(self, z):
        return (f'---\nschema: SKILL_COLLAB_REVIEW_REQUEST_V1\nstate: SUBMITTED\n'
            f'request_id: REQ-COWORK-TEST-R1-20261122\nrequest_revision: 1\n'
            f'project_id: {WORK}\nwork_id: {WORK}\n'
            'skill_id: cowork-context-design\n'
            'package_path: /SKILL-COLLAB/packages/cowork_review_v0_1_0_1122.zip\n'
            f'package_size_bytes: {len(z)}\n'
            f'package_sha256: {hashlib.sha256(z).hexdigest()}\n'
            '---\n# Review\n').encode()

    def write(self, rel, bytes_):
        p=self.root / rel
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_bytes(bytes_)

    def commit(self):
        subprocess.check_call(['git','-C',str(self.root),'add','.'])
        subprocess.check_call(['git','-C',str(self.root),'commit','-qm','test'])

    def test_git_pinned_staging_and_default_no_publish(self):
        invoked=[]
        def submit(**args):
            invoked.append(args)
            self.assertEqual(args['request_draft'].read_bytes(),self.draft)
            self.assertEqual(args['package'].read_bytes(),self.zipdata)
            self.assertFalse(args['publish'])
            return {'status':'PREPUBLICATION_PASS_NOT_SUBMITTED'}
        with patch.object(mod,'submit',side_effect=submit):
            r=mod.run(root=self.root,work_id=WORK,draft_path=DRAFT,candidate_path=CAND,live_config=Path('fake'))
        self.assertEqual(len(invoked),1)
        self.assertEqual(r['host_signer'],'NOT_INVOKED')
        self.assertEqual(r['ready'],'NOT_CREATED')

    def test_publish_propagates_only_to_existing_submitter(self):
        with patch.object(mod,'submit',return_value={'status':'SUBMITTED_AWAITING_PROTECTED_SIGNER'}) as s:
            r=mod.run(root=self.root,work_id=WORK,draft_path=DRAFT,candidate_path=CAND,live_config=Path('fake'),publish=True)
        self.assertEqual(r['status'],'SUBMITTED_AWAITING_PROTECTED_SIGNER')
        self.assertEqual(s.call_args.kwargs['approval_route'],'manual')
        self.assertTrue(s.call_args.kwargs['publish'])

    def test_auto_delegation_passed_without_faking_signer(self):
        with patch.object(mod,'submit',return_value={'status':'PREPUBLICATION_PASS_NOT_SUBMITTED'}) as s:
            mod.run(root=self.root,work_id=WORK,draft_path=DRAFT,candidate_path=CAND,live_config=Path('fake'),approval_route='auto',delegated_skills=('other',))
        self.assertEqual(s.call_args.kwargs['delegated_skills'],('other',))
        self.assertEqual(s.call_args.kwargs['approval_route'],'auto')

    def test_wrong_work_blocks_before_submit(self):
        self.write(DRAFT,self.draft.replace(f'work_id: {WORK}'.encode(),b'work_id: WRONG-WORK'))
        self.commit()
        with patch.object(mod,'submit') as s:
            with self.assertRaisesRegex(SubmissionBlocked,'STAGED_WORK_MISMATCH'):
                mod.run(root=self.root,work_id=WORK,draft_path=DRAFT,candidate_path=CAND,live_config=Path('fake'))
            s.assert_not_called()

    def test_path_traversal_and_unrelated_work_blocked(self):
        for name in (f'collab/projects/{WORK}/../secret.md', '/tmp/REVIEW_DRAFT.md', 'OTHER/REVIEW_DRAFT.md'):
            with self.assertRaisesRegex(SubmissionBlocked,'UNSAFE_STAGED_SOURCE_PATH'):
                mod.valid_staged_path(name,WORK,'.md')

    def test_tampered_base64_blocks(self):
        self.write(CAND,base64.b64encode(self.zipdata)[:-4]+b'!!!!')
        self.commit()
        with patch.object(mod,'submit') as s:
            with self.assertRaisesRegex(SubmissionBlocked,'STAGED_BASE64_INVALID'):
                mod.run(root=self.root,work_id=WORK,draft_path=DRAFT,candidate_path=CAND,live_config=Path('fake'))
            s.assert_not_called()

    def test_bad_zip_hash_blocks(self):
        self.write(CAND,base64.b64encode(b'badzip'))
        self.commit()
        with patch.object(mod,'submit') as s:
            with self.assertRaisesRegex(SubmissionBlocked,'STAGED_PACKAGE_SHA_OR_SIZE_MISMATCH'):
                mod.run(root=self.root,work_id=WORK,draft_path=DRAFT,candidate_path=CAND,live_config=Path('fake'))
            s.assert_not_called()

    def test_bad_utf8_request_blocks(self):
        self.write(DRAFT,b'\xff\xfe')
        self.commit()
        with patch.object(mod,'submit') as s:
            with self.assertRaisesRegex(SubmissionBlocked,'INVALID_STAGED_REQUEST'):
                mod.run(root=self.root,work_id=WORK,draft_path=DRAFT,candidate_path=CAND,live_config=Path('fake'))
            s.assert_not_called()

    def test_absent_committed_source_blocks_even_if_local_file_exists(self):
        subprocess.check_call(['git','-C',str(self.root),'rm','-q',CAND])
        self.commit()
        with patch.object(mod,'submit') as s:
            with self.assertRaisesRegex(SubmissionBlocked,'STAGED_SOURCE_NOT_REGULAR_GIT_BLOB'):
                mod.run(root=self.root,work_id=WORK,draft_path=DRAFT,candidate_path=CAND,live_config=Path('fake'))
            s.assert_not_called()

    def test_submitter_failure_does_not_retry_or_sign(self):
        with patch.object(mod,'submit',side_effect=SubmissionBlocked('OUT_OF_SCOPE')) as s:
            with self.assertRaisesRegex(SubmissionBlocked,'OUT_OF_SCOPE'):
                mod.run(root=self.root,work_id=WORK,draft_path=DRAFT,candidate_path=CAND,live_config=Path('fake'),publish=True)
        self.assertEqual(s.call_count,1)

if __name__=='__main__':unittest.main()
