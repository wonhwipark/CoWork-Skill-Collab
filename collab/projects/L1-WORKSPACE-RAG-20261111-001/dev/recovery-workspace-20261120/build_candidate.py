"""Reproduce pinned Recovery development candidates; never install or publish.

Keep this file and recovery_workspace.patch together under the existing Work's
dev/recovery-workspace-20261120 directory. Parent dev helpers remain canonical.
"""
from __future__ import annotations
import argparse, compileall, hashlib, json, os, subprocess, sys, tempfile, zipfile
from pathlib import Path

KERNEL_43_SHA='80c955790aaa65f695c061f7ec2664bd1c7c5ba7e0a7534045960eea7fe2d5f6'
KERNEL_45_SHA='1bccbbffeaafcefda27b75ca8f430e502bc8c2b475b63bd76425ca7ee1c5d7f8'
WORKFLOW_74_SHA='b810ce0cf072609431737c58b0ef2b7a0a8ec0701a0746e6a94283c374224989'

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def build(kernel43, workflow74, patch, helpers, out):
    assert digest(kernel43)==KERNEL_43_SHA,'Kernel input differs'
    assert digest(workflow74)==WORKFLOW_74_SHA,'Workflow input differs'
    sys.path.insert(0,str(helpers))
    from build_msc_kernel_html_links_r0001_20261118 import run
    from build_l1_knowledge_guard_candidates_r0001_20261117 import safe_unzip
    from reproducible_zip import rezip
    from skill_release_quality_gate import validate
    out.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='recovery-candidate-') as td:
        root=Path(td);run(kernel43,root/'base')
        kernel45=root/'base/work-ledger-kernel_v0_7_45_1118.zip'
        assert digest(kernel45)==KERNEL_45_SHA,'Kernel .45 reconstruction differs'
        kernel=root/'packages/kernel';kernel.mkdir(parents=True);safe_unzip(kernel45,kernel)
        wf_extract=root/'wf';wf_extract.mkdir();safe_unzip(workflow74,wf_extract)
        workflow=root/'packages/workflow';(wf_extract/'l1-fix-workflow').rename(workflow)
        protected={p: (kernel/p).read_bytes() for p in ['contracts/record.schema.json','contracts/evidence.schema.json','contracts/fsm_v1.json','contracts/profile_policies_v1.json']}
        subprocess.run(['git','apply','--check',str(patch.resolve())],cwd=root,check=True)
        subprocess.run(['git','apply',str(patch.resolve())],cwd=root,check=True)
        assert all((kernel/p).read_bytes()==b for p,b in protected.items()),'Existing authority schema/FSM changed'
        assert compileall.compile_dir(root/'packages',quiet=1)
        rows=[]
        for package,version,name,module in [(kernel,'0.7.46','work-ledger-kernel_v0_7_46_1120.zip','work_ledger_kernel'),(workflow,'1.6.75','l1-fix-workflow_v1_6_75_1120.zip','l1_fix_workflow')]:
            env={**os.environ,'PYTHONPATH':str(package)+os.pathsep+str(kernel)}
            actual=subprocess.check_output([sys.executable,'-m',module,'--version'],cwd=root,env=env,text=True).strip()
            assert actual==version,'CLI version differs'
            output=out/name;rezip(package,output)
            second=root/'repeat'/name;rezip(package,second)
            assert output.read_bytes()==second.read_bytes(),'ZIP is not reproducible'
            qa=validate(output,version)
            rows.append({**qa,'reproducible':True,'cli_version':actual,'channel':'development_not_for_deployment'})
        result={'status':'CANDIDATES_BUILT_NOT_FOR_DEPLOYMENT','source_pins':{'kernel43':KERNEL_43_SHA,'kernel45':KERNEL_45_SHA,'workflow74':WORKFLOW_74_SHA},'patch_sha256':digest(patch),'schema_fsm_unchanged':True,'artifacts':rows,'independent_review':'NOT_RUN','host_integration':'NOT_RUN'}
        (out/'BUILD_RESULT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
        print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--kernel43',type=Path,required=True);p.add_argument('--workflow74',type=Path,required=True)
    p.add_argument('--patch',type=Path,default=Path(__file__).with_name('recovery_workspace.patch'))
    p.add_argument('--helpers',type=Path,default=Path(__file__).resolve().parent.parent)
    p.add_argument('--out',type=Path,required=True);a=p.parse_args();build(a.kernel43,a.workflow74,a.patch,a.helpers,a.out)
