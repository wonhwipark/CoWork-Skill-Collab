"""Synthetic functional contract test for physical recovery/ view."""
import tempfile
from pathlib import Path
import pytest
from work_ledger_kernel.recovery_physical import project_physical_recovery


def test_physical_index_and_reference_idempotence():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        def wc(directory, name, content):
            directory.mkdir(parents=True, exist_ok=True)
            (directory / name).write_text(content, encoding='utf-8')
        def wf(path, content):
            path.write_text(content, encoding='utf-8')
        row = {'work_id':'DEMO-REC-001','id':'E-123456abcdef','summary':'synthetic',
               'code_rev':'fixture-r1','integrity':'MATCH','published_path':'artifacts/report.md'}
        assert project_physical_recovery(root,[row],wc,wf)==1
        assert (root/'recovery/README.md').is_file()
        assert (root/'recovery/index.json').is_file()
        assert (root/'recovery/works/DEMO-REC-001/E-123456abcdef.md').is_file()
        assert project_physical_recovery(root,[row],wc,wf)==1


@pytest.mark.parametrize('bad', ['../outside', '/etc/passwd', 'x/../../secret'])
def test_rejects_unsafe_published_path(bad):
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp)
        row={'work_id':'W-1','id':'E-123456abcdef','published_path':bad}
        with pytest.raises(ValueError):
            project_physical_recovery(root,[row],lambda *_:None,lambda *_:None)
