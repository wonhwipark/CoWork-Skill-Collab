from pathlib import Path
import inspect, json, sys, tempfile, zipfile
ROOT=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as tmp:
 for kind,name,root in [('KERNEL','work-ledger-kernel_v0_7_41_1116.zip',Path(tmp)),('CONVERTER','doc-converter_v0_2_24_1116.zip',Path(tmp)/'doc-converter')]:
  with zipfile.ZipFile(ROOT/'candidates'/name) as z:
   for member in z.namelist(): 
    if member.endswith(".py") and ('work_ux.py' in member or 'artifact_names.py' in member or 'kernel.py' in member or 'msc_tool.py' in member or 'scenario_ir_adapter.py' in member):
     raw=z.read(member).decode('utf-8').splitlines()
     print('FILE',member,'LINES',len(raw))
     if 'work_ux.py' in member:
      for i,x in enumerate(raw):
       if ('def export_docs' in x or 'is_msc_svg' in x or 'def _validate_safe_msc_svg' in x or 'evidence_category(e)' in x or 'source_rel' in x):
        print('CONTEXT',i+1,'\n'+'\n'.join(f'{j+1:04d}: {raw[j]}' for j in range(max(0,i-9),min(len(raw),i+17))))
     if 'work_ux.py' in member:
      for a,b in [(609,690),(870,915)]:
       print('RANGE',a,b,'\n'+'\n'.join(f'{j+1:04d}: {raw[j]}' for j in range(a-1,min(len(raw),b))))
     if 'kernel.py' in member:
      for a,b in [(529,574),(1350,1370),(1457,1465)]:
       print('RANGE',a,b,'\n'+'\n'.join(f'{j+1:04d}: {raw[j]}' for j in range(a-1,min(len(raw),b))))
      for i,x in enumerate(raw):
       if x.startswith('    def ') and any(k in x for k in ['evidence','new(', 'work_ux','export','register']):
        print('METHOD',i+1,x)
     if 'artifact_names.py' in member:
      for i,x in enumerate(raw[:145]): print(f'{i+1:04d}: {x}')
     if 'msc_tool.py' in member:
      for i,x in enumerate(raw):
       if ('def cmd_scenario_build' in x or 'def cmd_package' in x or 'def main' in x or 'view_mode = ' in x):
        print('CONTEXT',i+1,'\n'+'\n'.join(f'{j+1:04d}: {raw[j]}' for j in range(max(0,i-4),min(len(raw),i+20))))
