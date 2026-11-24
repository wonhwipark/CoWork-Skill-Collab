"""Synthetic read-model contract tests."""
import tempfile
import unittest
from pathlib import Path
from work_ledger_kernel.recovery_physical import project_physical_recovery


class PhysicalRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        def wc(d,name,body):
            d.mkdir(parents=True,exist_ok=True)
            (d/name).write_text(body,encoding='utf-8')
        self.wc=wc
        self.wf=lambda p,s:p.write_text(s,encoding='utf-8')

    def tearDown(self):
        self.tmp.cleanup()

    def test_index_references_and_idempotence(self):
        entry={'work_id':'DEMO-REC-001','id':'E-123456abcdef','summary':'synthetic',
               'code_rev':'fixture-r1','integrity':'MATCH','published_path':'artifacts/report.md'}
        self.assertEqual(project_physical_recovery(self.root,[entry],self.wc,self.wf),1)
        self.assertTrue((self.root/'recovery/README.md').is_file())
        self.assertTrue((self.root/'recovery/index.json').is_file())
        self.assertTrue((self.root/'recovery/works/DEMO-REC-001/E-123456abcdef.md').is_file())
        self.assertEqual(project_physical_recovery(self.root,[entry],self.wc,self.wf),1)

    def test_unsafe_paths(self):
        for bad in ('../outside','/etc/passwd','x/../../secret','dir\\hidden'):
            with self.assertRaises(ValueError):
                project_physical_recovery(self.root,[{'work_id':'W-1','id':'E-123456abcdef','published_path':bad}],self.wc,self.wf)


if __name__=='__main__':
    unittest.main()
