"""Finalize checked MSC code into uniquely-versioned PUBLIC-delivery ZIPs.
No external services, host installs, secrets, background jobs or paid review.
"""
from __future__ import annotations
import copy, hashlib, json, os, re, stat, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
INPUT=ROOT/"candidates"
OUT=Path(os.environ.get("MSC_RELEASE_OUTPUT_DIR",str(INPUT/"release-ready"))).resolve()
OUT.mkdir(parents=True,exist_ok=True)
DATE=(2026,11,16,13,30,0)
SPECS=[
 ("doc-converter_v0_2_24_1116.zip","2ef0929bc0a80a1c0aca67bf3c8fc02f967bddba223b45c27807c363e96229f7","doc-converter_v0_2_25_1116.zip","0.2.25"),
 ("work-ledger-kernel_v0_7_41_1116.zip","48d1bf5e24c613e7e0ba04df9946c427c5d1ee39d8d16204966afff07e93497b","work-ledger-kernel_v0_7_42_1116.zip","0.7.42"),
]
def digest(a):return hashlib.sha256(a).hexdigest()
def valid(v,msg):
 if not v:raise ValueError(msg)
def txt(data,n):
 valid(n in data,n+" missing")
 return data[n].decode("utf-8")
def write(data,n,s):data[n]=s.encode("utf-8")
def replace(src,old,new,where):
 valid(src.count(old)==1,where+" anchor mismatch "+str(src.count(old)))
 return src.replace(old,new,1)

def read_zip(file,expected):
 raw=file.read_bytes()
 valid(digest(raw)==expected,file.name+" input sha changed")
 data={}
 with zipfile.ZipFile(file) as z:
  valid(z.testzip() is None,"bad source CRC "+file.name)
  for member in z.infolist():
   name=member.filename
   valid(not name.startswith("/") and ".." not in Path(name).parts and "\\" not in name,"unsafe member "+name)
   valid(not stat.S_ISLNK(member.external_attr>>16),"symlink "+name)
   valid(name not in data,"duplicate "+name)
   if not member.is_dir():data[name]=z.read(member)
 return data

def publish_metadata(data,prefix,new_version,filename,revision):
 rel=prefix+".skill-release.json"
 meta=json.loads(txt(data,rel))
 valid(meta["schema_version"]==1,"unsupported release schema")
 meta.update({
   "version":new_version,"skill_version":new_version,
   "revision":revision,"archive":filename,
   "release_date":"2026-11-16","built_at":"2026-11-16T13:30:00+09:00",
   "channel":"public","release_kind":"approved_final_zip",
 })
 write(data,rel,json.dumps(meta,ensure_ascii=False,indent=2)+"\n")

def release_converter(data,outname,version):
 pre="doc-converter/"
 # Previous fixed source code is retained verbatim; only release metadata and tests change.
 valid(txt(data,pre+"VERSION").strip()=="0.2.24","converter previous version mismatch")
 write(data,pre+"VERSION",version+"\n")
 skill=txt(data,pre+"SKILL.md")
 skill=replace(skill,"version: 0.2.24","version: "+version,"converter frontmatter")
 skill=replace(skill,"# doc-converter v0.2.24 —","# doc-converter v"+version+" —","converter heading")
 write(data,pre+"SKILL.md",skill)
 man=json.loads(txt(data,pre+"skillsilent/manifest.json"));man["skill_version"]=version
 write(data,pre+"skillsilent/manifest.json",json.dumps(man,ensure_ascii=False,indent=2)+"\n")
 contract=json.loads(txt(data,pre+"skillsilent/contract.json"))
 valid("skill_version" in contract,"contract version missing")
 contract["skill_version"]=version
 write(data,pre+"skillsilent/contract.json",json.dumps(contract,ensure_ascii=False,indent=2)+"\n")
 ver=txt(data,pre+"VERSION.md")
 write(data,pre+"VERSION.md",
       "# doc-converter "+version+" — PUBLIC delivery\n\n"
       "## 2026-11-16\n"
       "- Procedure/Feature verified synthetic MSC output and standalone HTML+SVG B viewer.\n"
       "- NFC-normalized, Windows-case-safe names; duplicate/ambiguous phase reporting.\n"
       "- Existing ISSUE default retained; OpenCode direct CLI supported.\n"
       "- skillsilent static policy/metadata retained for compatibility; no managed runner installation assumed.\n"
       "- Group Knowledge writer and actual host URL/readback remain separate integration checks.\n\n"
       +ver)
 publish_metadata(data,pre,version,outname,25)
 notes=pre+"MSC_RELEASE_NOTES_v0_2_25.md"
 write(data,notes,"# doc-converter "+version+"\n\nMSC Procedure/Feature HTML+SVG B viewer and name collision fixes. Synthetic regression and direct CLI validation; no automatic Knowledge publication.\n")
 # Retain prior development ZIPs in PRIVATE; do not propagate development-only notes as release contents.
 for name in list(data):
  if name.startswith(pre+"DEVELOPMENT_"):del data[name]
 checks=[f"{digest(raw)}  {name[len(pre):]}" for name,raw in sorted(data.items())
         if name.startswith(pre) and name != pre+"PACKAGE_CONTENTS.sha256"]
 write(data,pre+"PACKAGE_CONTENTS.sha256","\n".join(checks)+"\n")

def release_kernel(data,outname,version):
 valid(txt(data,"VERSION").strip()=="0.7.41-dev.1","kernel previous version mismatch")
 write(data,"VERSION",version+"\n")
 skill=txt(data,"SKILL.md")
 skill=replace(skill,'version: "0.7.38-dev.1"','version: "'+version+'"',"kernel frontmatter")
 # Replace the current title only, preserving historic change log versions.
 current_re=re.search(r"(?m)^# [^\n]*v0\.7\.41-dev\.1[^\n]*$",skill)
 if current_re: skill=skill[:current_re.start()]+skill[current_re.start():].replace("v0.7.41-dev.1","v"+version,1)
 write(data,"SKILL.md",skill)
 for key in ("skillsilent/manifest.json","skillsilent/contract.json"):
  if key in data:
   try:meta=json.loads(txt(data,key))
   except ValueError as e:raise ValueError("bad "+key) from e
   if "skill_version" in meta: meta["skill_version"]=version
   if "version" in meta and isinstance(meta["version"],str):meta["version"]=version
   write(data,key,json.dumps(meta,ensure_ascii=False,indent=2)+"\n")
 # Existing test had an unrelated missing import, preventing all-suite collection.
 t="tests/test_work_inventory_v0735.py"
 body=txt(data,t)
 valid("unittest.TestCase" in body,"missing unittest test reference")
 if not re.search(r"(?m)^import unittest\s*$",body):
  body="import unittest\n"+body
 write(data,t,body)
 publish_metadata(data,"",version,outname,42)
 notes="MSC_RELEASE_NOTES_v0_7_42.md"
 write(data,notes,"# work-ledger-kernel "+version+"\n\nMSC Evidence SVG filename/export support, safe SVG gate and bounded export. Existing Work and published-path mapping rules retained. Synthetic Work export regression verified, no automatic host or Knowledge publication.\n")
 for name in list(data):
  if name.startswith("DEVELOPMENT_"):del data[name]
 checks={key:digest(raw) for key,raw in sorted(data.items()) if key!="MANIFEST_SHA256.json"}
 write(data,"MANIFEST_SHA256.json",json.dumps(checks,ensure_ascii=False,indent=2)+"\n")

def make_zip(path,data):
 with zipfile.ZipFile(path,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for name in sorted(data):
   info=zipfile.ZipInfo(name,DATE)
   info.compress_type=zipfile.ZIP_DEFLATED
   info.external_attr=0o644<<16
   z.writestr(info,data[name])
 with zipfile.ZipFile(path) as z:
  valid(z.testzip() is None,"release CRC failed "+path.name)
  valid(len(z.namelist())==len(set(z.namelist())),"duplicates")
  valid(all(z.read(n)==data[n] for n in data),"release byte mismatch")
 print("RELEASE_BUILT",path.name,"bytes",path.stat().st_size,"sha256",digest(path.read_bytes()),"members",len(data),flush=True)
 return {"filename":path.name,"size":path.stat().st_size,"sha256":digest(path.read_bytes()),"members":len(data)}

results=[]
for source,expected,dest,version in SPECS:
 data=read_zip(INPUT/source,expected)
 if source.startswith("doc-converter"):release_converter(data,dest,version)
 else:release_kernel(data,dest,version)
 results.append(make_zip(OUT/dest,data))
(OUT/"release_manifest.json").write_text(json.dumps({"schema":"msc-public-release-v1","candidates":results},indent=2)+"\n",encoding="utf-8")
print("RELEASE_MANIFEST_PATH",str(OUT/"release_manifest.json"),flush=True)
