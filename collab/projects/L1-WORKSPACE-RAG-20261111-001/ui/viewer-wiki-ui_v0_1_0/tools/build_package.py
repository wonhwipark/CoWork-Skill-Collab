"""Build standalone HTML and deterministic ZIP. No third-party dependency."""
from pathlib import Path
import base64, hashlib, json, re, zipfile, sys
ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT.parent/'output'
OUTPUT.mkdir(exist_ok=True)
SINGLE='L1_Workspace_Wiki_UI_v0_1_0_20261119_KST.html'
ZIP='l1-workspace-wiki-ui_v0_1_0_1119.zip'
SCRIPT_FILES=['fixtures/demo-data.js','adapters/adapter.js','assets/markdown.js','assets/app.js']
def sha(data):return hashlib.sha256(data).hexdigest()
def standalone():
 html=(ROOT/'index.html').read_text()
 css=(ROOT/'assets/style.css').read_text()
 scripts=[(ROOT/p).read_text().replace('</script','<\\/script') for p in SCRIPT_FILES]
 hashes=["'sha256-"+base64.b64encode(hashlib.sha256(s.encode()).digest()).decode()+"'" for s in scripts]
 csshash="'sha256-"+base64.b64encode(hashlib.sha256(css.encode()).digest()).decode()+"'"
 html=html.replace("script-src 'self'","script-src "+' '.join(hashes)).replace("style-src 'self'","style-src "+csshash)
 html=html.replace('<link rel="stylesheet" href="assets/style.css">','<style>'+css+'</style>')
 favicon=base64.b64encode((ROOT/'assets/favicon.svg').read_bytes()).decode()
 html=html.replace('href="assets/favicon.svg"','href="data:image/svg+xml;base64,'+favicon+'"')
 html=re.sub(r'\s*<script defer src="[^"]+"></script>','',html)
 html=html.replace('</body>','\n'+'\n'.join('<script>'+s+'</script>' for s in scripts)+'\n</body>')
 (ROOT/SINGLE).write_text(html)
 return html
standalone()
files=sorted(p for p in ROOT.rglob('*') if p.is_file() and p.name!='manifest.sha256' and '__pycache__' not in p.parts)
(ROOT/'manifest.sha256').write_text(''.join(f'{sha(p.read_bytes())}  {p.relative_to(ROOT).as_posix()}\n' for p in files))
files=sorted(p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts)
with zipfile.ZipFile(OUTPUT/ZIP,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
 for p in files:
  info=zipfile.ZipInfo('viewer-wiki-ui/'+p.relative_to(ROOT).as_posix(),date_time=(2026,11,19,9,0,0))
  info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
  archive.writestr(info,p.read_bytes())
with zipfile.ZipFile(OUTPUT/ZIP) as archive:
 assert archive.testzip() is None
 assert all(not p.startswith('/') and '..' not in Path(p).parts for p in archive.namelist())
meta={'filename':ZIP,'bytes':(OUTPUT/ZIP).stat().st_size,'sha256':sha((OUTPUT/ZIP).read_bytes()),'files':len(files),'zip_crc':'PASS','path_safety':'PASS','package_status':'development_not_for_deployment'}
(OUTPUT/'package-info.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(meta,ensure_ascii=False,indent=2))
