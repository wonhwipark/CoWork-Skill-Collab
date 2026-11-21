"""Synthetic, local-only regression tests. No GitHub API, reviewer, or paid calls."""
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
import review_pin_preflight as mod

RID='REQ-L1-KNOWLEDGE-PREFLIGHT-V020-R2-20261121'
PZIP='collab/packages/knowledge_analysis_preflight_v0_2_0_1121_REVIEW_INPUT.zip'
REPO='1451933830'


def git(root: Path,*args:str)->str:
    return subprocess.check_output(['git','-C',str(root),*args],stderr=subprocess.DEVNULL).decode().strip()


class SyntheticRepo(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        git(self.root,'init','-q')
        git(self.root,'config','user.name','Synthetic')
        git(self.root,'config','user.email','synthetic@example.invalid')
        self.zip_bytes=self.make_zip()
        self.write(PZIP,self.zip_bytes)
        self.commit('package-only')
        self.zip_only=git(self.root,'rev-parse','HEAD')
        self.write(f'collab/requests/{RID}/REQUEST.md',self.make_request())
        self.commit('request-and-package')
        self.correct_pin=git(self.root,'rev-parse','HEAD')
        self.pin(self.correct_pin)
        self.commit('pin')

    def make_zip(self):
        b=io.BytesIO()
        with zipfile.ZipFile(b,'w') as z:
            z.writestr('synthetic.txt','test data')
        return b.getvalue()

    def make_request(self):
        return f'''---
schema: SKILL_COLLAB_REVIEW_REQUEST_V1
state: SUBMITTED
request_id: {RID}
request_revision: 1
skill_id: knowledge_analysis_preflight
package_path: /SKILL-COLLAB/packages/{Path(PZIP).name}
package_sha256: {hashlib.sha256(self.zip_bytes).hexdigest()}
package_size_bytes: {len(self.zip_bytes)}
run_policy_ref: POLICY-STATIC-V1
---
# Synthetic request
'''.encode()

    def pin(self,commit,repo_id=REPO):
        self.write(f'collab/requests/{RID}/SOURCE_PIN.json',json.dumps({'schema':'SKILL_COLLAB_SOURCE_PIN_V1','commit':commit,'repo_id':repo_id}).encode())

    def write(self,path,data):
        p=self.root/path
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_bytes(data)

    def commit(self,message):
        git(self.root,'add','.')
        git(self.root,'commit','-qm',message)

    def inspect(self,mode='manual',skills=()):
        return mod.inspect(root=self.root,request_id=RID,package_repo_path=PZIP,
            expected_repo_id=REPO,main_commit=git(self.root,'rev-parse','HEAD'),approval_mode=mode,delegated_skills=skills)

    def test_correct_request_package_pin_pass_but_not_authority(self):
        result=self.inspect()
        self.assertEqual(result['status'],'PASS_PINNED_INPUTS_ONLY')
        self.assertEqual(result['signer_authority'],'NOT_VERIFIED')
        self.assertEqual(result['ready_or_model_calls'],0)

    def test_R1_package_only_commit_is_blocked(self):
        self.pin(self.zip_only)
        self.commit('bad-R1-pin')
        with self.assertRaisesRegex(mod.PreflightBlocked,'COMMIT_UNREADABLE_REQUEST_ABSENT'):
            self.inspect()

    def test_changed_request_after_pin_is_blocked(self):
        self.write(f'collab/requests/{RID}/REQUEST.md',self.make_request()+b'\nChanged.\n')
        self.commit('tamper-request')
        with self.assertRaisesRegex(mod.PreflightBlocked,'REQUEST_BYTES_CHANGED_SINCE_PIN'):
            self.inspect()

    def test_changed_zip_after_pin_is_blocked(self):
        self.write(PZIP,b'not same')
        self.commit('tamper-package')
        with self.assertRaisesRegex(mod.PreflightBlocked,'PACKAGE_BYTES_CHANGED_SINCE_PIN'):
            self.inspect()

    def test_pin_to_missing_commit_is_blocked(self):
        self.pin('a'*40)
        self.commit('invalid-commit')
        with self.assertRaises(mod.PreflightBlocked): self.inspect()

    def test_repo_id_numeric_is_blocked(self):
        self.pin(self.correct_pin,1451933830)
        self.commit('numeric-repo')
        with self.assertRaisesRegex(mod.PreflightBlocked,'SOURCE_PIN_FORMAT_OR_REPO_ID_MISMATCH'):
            self.inspect()

    def test_request_skill_outside_auto_delegation(self):
        with self.assertRaisesRegex(mod.PreflightBlocked,'AUTO_NOT_ELIGIBLE_SKILL_ID'):
            self.inspect('auto',('l1-knowledge-updater','cowork-dashboard'))

    def test_auto_no_loaded_delegation_blocks(self):
        with self.assertRaisesRegex(mod.PreflightBlocked,'DELEGATION_SCOPE_NOT_SUPPLIED'):
            self.inspect('auto')

    def test_auto_with_same_skill_does_not_mean_signed(self):
        result=self.inspect('auto',('knowledge_analysis_preflight',))
        self.assertEqual(result['signer_authority'],'NOT_VERIFIED')

    def test_existing_ready_causes_no_requeue(self):
        self.write(f'collab/requests/{RID}/READY.md',b'not a valid READY')
        self.commit('ready-exists')
        with self.assertRaisesRegex(mod.PreflightBlocked,'REQUEST_ALREADY_SIGNED_OR_READY_RECONCILE'):
            self.inspect()

    def test_existing_signature_causes_no_requeue(self):
        self.write(f'collab/requests/{RID}/APPROVAL_SIG.json',b'{}')
        self.commit('approval-exists')
        with self.assertRaisesRegex(mod.PreflightBlocked,'REQUEST_ALREADY_SIGNED_OR_READY_RECONCILE'):
            self.inspect()

    def test_unexpected_request_path_blocked(self):
        with self.assertRaisesRegex(mod.PreflightBlocked,'INVALID_REPO_PATH'):
            mod.checked_path('../outside.zip')

    def test_duplicate_metadata_key_blocked(self):
        self.write(f'collab/requests/{RID}/REQUEST.md',self.make_request().replace(b'request_id:',b'request_id: BAD\nrequest_id:'))
        self.commit('duplicate-key')
        # Create new pin to new request revision to avoid triggering byte drift first
        new=git(self.root,'rev-parse','HEAD')
        self.pin(new)
        self.commit('new-pin')
        with self.assertRaisesRegex(mod.PreflightBlocked,'REQUEST_DUPLICATE_FRONTMATTER_KEY'):
            self.inspect()

    def test_wrong_sha_in_request_blocked(self):
        self.write(f'collab/requests/{RID}/REQUEST.md',self.make_request().replace(hashlib.sha256(self.zip_bytes).hexdigest().encode(),b'b'*64))
        self.commit('bad-hash')
        new=git(self.root,'rev-parse','HEAD')
        self.pin(new)
        self.commit('new-pin')
        with self.assertRaisesRegex(mod.PreflightBlocked,'PACKAGE_SHA256_MISMATCH'):
            self.inspect()

    def test_incorrect_zip_path_blocked(self):
        with self.assertRaisesRegex(mod.PreflightBlocked,'PACKAGE_PATH_NAME_MISMATCH'):
            mod.inspect(root=self.root,request_id=RID,package_repo_path='collab/packages/not.zip',expected_repo_id=REPO,main_commit=git(self.root,'rev-parse','HEAD'),approval_mode='manual')


    def test_same_zip_basename_in_another_directory_is_blocked(self):
        with self.assertRaisesRegex(mod.PreflightBlocked, 'PACKAGE_PATH_NAME_MISMATCH'):
            mod.inspect(root=self.root, request_id=RID,
                        package_repo_path='other/' + Path(PZIP).name,
                        expected_repo_id=REPO, main_commit=git(self.root, 'rev-parse', 'HEAD'),
                        approval_mode='manual')


if __name__=='__main__':unittest.main()
