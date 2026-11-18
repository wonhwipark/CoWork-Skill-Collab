"""Source checks complement browser tests; no host security certification."""
from pathlib import Path
import json, subprocess, hashlib, re
root=Path(__file__).resolve().parents[1]
checks=[]
def check(name,ok):checks.append({'test':name,'result':'PASS' if ok else 'FAIL'})
for path in ['assets/app.js','assets/markdown.js','adapters/adapter.js','fixtures/demo-data.js','tests/harness.js']:
 result=subprocess.run(['node','--check',str(root/path)],capture_output=True)
 check('JS syntax '+path,result.returncode==0)
scripts='\n'.join((root/p).read_text() for p in ['assets/app.js','assets/markdown.js','adapters/adapter.js'])
check('No innerHTML/outerHTML/eval/document.write',not re.search(r'innerHTML|outerHTML|\beval\s*\(|document\.write\s*\(',scripts))
check('No fetch/XHR/WebSocket in demo',not re.search(r'\bfetch\s*\(|XMLHttpRequest|WebSocket',scripts))
check('No write storage API',not re.search(r'localStorage|sessionStorage|indexedDB|\.cookie\s*=',scripts))
index=(root/'index.html').read_text()
check('Demo CSP disables connect/frame/object',all(s in index for s in ["connect-src 'none'","frame-src 'none'","object-src 'none'"]))
check('No external asset references',not re.search(r'(?:src|href)=["\']https?://',index))
check('Search accessible name survives mobile', 'id="search-open" aria-label="예시 문서 검색"' in index)
check('No filesystem service/backend in package',not any(root.glob('server.*')))
# Values are source-to-renderer contrast pairs, not a full WCAG audit.
def lum(color):
 c=[int(color[i:i+2],16)/255 for i in (1,3,5)];c=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in c];return sum(x*y for x,y in zip(c,[.2126,.7152,.0722]))
for name,fg,bg in [('body','#4e5b70','#ffffff'),('navigation','#515e73','#f9fafc'),('active','#5144bf','#eeecff'),('preview','#8c5d16','#fcf2df'),('draft','#6756a6','#f0edf9'),('published','#236956','#e9f5ef'),('unknown','#616d80','#edf0f5')]:
 a,b=sorted([lum(fg),lum(bg)]);ratio=(b+.05)/(a+.05);check(f'Critical text contrast {name} {ratio:.2f}:1',ratio>=4.5)
report={'scope':'STATIC_SOURCE_ONLY','counts':{v:sum(x['result']==v for x in checks) for v in ['PASS','FAIL']},'results':checks}
(root/'tests/static-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
raise SystemExit(bool(report['counts']['FAIL']))
