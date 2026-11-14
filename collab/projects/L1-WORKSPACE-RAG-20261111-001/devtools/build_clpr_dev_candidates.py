"""Build isolated development-only ZIP candidates from pinned original bytes.

This script never touches checked-in candidate ZIP files or a production host.
"""
from __future__ import annotations
import hashlib
import json
import os
import pathlib
import stat
import sys
import zipfile

BASE=pathlib.Path('collab/projects/L1-WORKSPACE-RAG-20261111-001/candidates')
ROOT=pathlib.Path(os.environ['CLPR_TEMP'])
OUT=ROOT/'dev-output'
OUT.mkdir(parents=True,exist_ok=True)
cases=[
 ('workflow','l1-fix-workflow_v1_6_68_1114.zip','046b7968ff552d590a72c4e7ebb0a29df6760b5a6d07196f17f6eef09770e31a','l1-fix-workflow_v1_6_69_1115.zip','1.6.69','l1-fix-workflow/'),
 ('kernel','work-ledger-kernel_v0_7_38_1114.zip','6797f509d005377f9ba0d6312cc6cfb7017c7502cfcaab3ee61332c7f0a6e788','work-ledger-kernel_v0_7_39_1115.zip','0.7.39-dev.1',''),
]
for kind,original,expected,new_name,version,prefix in cases:
    raw=(BASE/original).read_bytes()
    assert hashlib.sha256(raw).hexdigest()==expected, ('SOURCE_HASH_MISMATCH',original)
    patches={}
    if kind=='workflow':
        f=ROOT/'workflow/l1-fix-workflow/l1_fix_workflow'
        patches[prefix+'l1_fix_workflow/cli.py']=(f/'cli.py').read_bytes()
        patches[prefix+'l1_fix_workflow/clpr_existing_work_link.py']=(f/'clpr_existing_work_link.py').read_bytes()
        patches[prefix+'tests/test_clpr_existing_work_link.py']=pathlib.Path('collab/projects/L1-WORKSPACE-RAG-20261111-001/devtools/test_clpr_existing_work_link.py').read_bytes()
    else:
        f=ROOT/'kernel/work_ledger_kernel/kernel.py'
        patches['work_ledger_kernel/kernel.py']=f.read_bytes()
    with zipfile.ZipFile(BASE/original) as z:
        info=z.infolist()
        assert z.testzip() is None and len({x.filename for x in info})==len(info)
        files={}
        for zi in info:
            p=pathlib.PurePosixPath(zi.filename)
            assert not p.is_absolute() and '..' not in p.parts and '\\' not in zi.filename
            assert not stat.S_ISLNK((zi.external_attr>>16)&0xffff)
            if not zi.is_dir():files[zi.filename]=z.read(zi)
        files.update(patches)
        rel=prefix+'.skill-release.json'
        version_name=prefix+'VERSION'
        manifest_name=prefix+'MANIFEST_SHA256.json'
        assert rel in files and version_name in files and manifest_name in files
        meta=json.loads(files[rel].decode('utf-8'))
        prior=meta.get('version')
        meta.update(version=version,skill_version=version,release_date='2026-11-15',
                    archive=new_name,release_kind='development_not_for_deployment',
                    channel='development_not_for_deployment',based_on=prior,
                    revision=int(meta.get('revision',0))+1)
        files[rel]=(json.dumps(meta,ensure_ascii=False,indent=2,sort_keys=True)+'\n').encode('utf-8')
        files[version_name]=(version+'\n').encode('utf-8')
        files[manifest_name]=(json.dumps(
            {key[len(prefix):]:hashlib.sha256(value).hexdigest()
             for key,value in sorted(files.items())
             if key!=manifest_name and not key.endswith('/')},
            ensure_ascii=False,indent=2,sort_keys=True)+'\n').encode('utf-8')
        # Preserve original archive metadata, append only new files.
        archive_path=OUT/new_name
        with zipfile.ZipFile(archive_path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=7) as out:
            consumed=set()
            for zi in info:
                if zi.is_dir():out.writestr(zi,b'');continue
                out.writestr(zi,files[zi.filename])
                consumed.add(zi.filename)
            for name in sorted(set(files)-consumed):
                info_new=zipfile.ZipInfo(name,date_time=(2026,11,15,0,0,0))
                info_new.compress_type=zipfile.ZIP_DEFLATED
                info_new.external_attr=(0o100644<<16)
                out.writestr(info_new,files[name])
    with zipfile.ZipFile(archive_path) as verify:
        assert verify.testzip() is None
        names=verify.namelist()
        assert len(names)==len(set(names))
        for zi in verify.infolist():
            assert not stat.S_ISLNK((zi.external_attr>>16)&0xffff)
            assert '..' not in pathlib.PurePosixPath(zi.filename).parts
            if zi.filename.endswith('.py'):
                compile(verify.read(zi),zi.filename,'exec')
        assert verify.read(version_name).decode().strip()==version
        manifest=json.loads(verify.read(manifest_name))
        actual={key[len(prefix):]:hashlib.sha256(verify.read(key)).hexdigest()
                for key in names if not key.endswith('/') and key!=manifest_name}
        assert manifest==actual,(kind,len(manifest),len(actual))
        m=json.loads(verify.read(rel));assert m['channel']=='development_not_for_deployment'
        assert m['archive']==new_name
    body=archive_path.read_bytes()
    print('DEV_ZIP_VERIFIED',new_name,len(body),hashlib.sha256(body).hexdigest(),
          'manifest_entries',len(manifest),'DEPLOYMENT_NOT_APPROVED',flush=True)
print('DEV_ONLY_PACKAGING_COMPLETE',flush=True)
