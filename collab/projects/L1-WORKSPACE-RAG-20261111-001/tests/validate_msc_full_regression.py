"""Full regression and safety inventory on two exact PRIVATE candidate ZIPs (no host)."""
from pathlib import Path
import hashlib, json, os, re, subprocess, sys, tempfile, zipfile, stat
root=Path(os.environ.get("MSC_RELEASE_OUTPUT_DIR", str(Path(__file__).resolve().parents[1]/"candidates")) )
items=[
 ("doc-converter_v0_2_24_1116.zip","2ef0929bc0a80a1c0aca67bf3c8fc02f967bddba223b45c27807c363e96229f7","doc-converter"),
 ("work-ledger-kernel_v0_7_41_1116.zip","48d1bf5e24c613e7e0ba04df9946c427c5d1ee39d8d16204966afff07e93497b","."),
]
if os.environ.get("MSC_RELEASE_OUTPUT_DIR"):
 manifest=json.loads((root/"release_manifest.json").read_text(encoding="utf-8"))
 assert len(manifest["candidates"])==2
 items=[(r["filename"],r["sha256"],"doc-converter" if r["filename"].startswith("doc-converter") else ".") for r in manifest["candidates"]]
secret=[
 ("PEM PRIVATE KEY",rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
 ("Github PAT",rb"gh[pousr]_[A-Za-z0-9]{34,}"),
 ("OpenAI secret",rb"sk-(?:proj-)?[A-Za-z0-9_\-]{35,}"),
 ("AWS id",rb"AKIA[0-9A-Z]{16}"),
]
errors=[]
for filename,expected,relative in items:
 data=(root/filename).read_bytes()
 assert hashlib.sha256(data).hexdigest()==expected, filename+" SHA mismatch"
 with zipfile.ZipFile(root/filename) as z:
  assert z.testzip() is None
  names=z.namelist()
  assert len(names)==len(set(names))
  assert all(not n.startswith('/') and '..' not in Path(n).parts and '\\' not in n for n in names)
  assert all(not stat.S_ISLNK(i.external_attr>>16) for i in z.infolist())
  assert all(i.file_size < 20*1024*1024 for i in z.infolist())
  nested=[n for n in names if n.lower().endswith(('.zip','.7z','.tar','.gz','.rar'))]
  findings=[]
  for i in z.infolist():
   if i.is_dir():continue
   raw=z.read(i.filename)
   for typ,pattern in secret:
    if re.search(pattern,raw):findings.append((typ,i.filename))
  assert not findings,findings
  print("STATIC_RELEASE_GATES_PASS",filename,"members",len(names),"nested_archives",nested,"secret_flags",len(findings),flush=True)
  for name in names:
   if name.endswith("test_low_spec_execution_contract.py"):
    print("VERSIONED_TEST",name,"\n"+z.read(name).decode("utf-8")[:1000],flush=True)
  with tempfile.TemporaryDirectory(prefix="msc-full-regression-") as td:
   z.extractall(td)
   # Python's zipfile.extractall ignores Unix executable mode; restore the modes
   # from the ZIP central directory to model the actual Linux unzip installer.
   for member in z.infolist():
    restored=Path(td)/member.filename
    if restored.is_file():
     bits=stat.S_IMODE(member.external_attr>>16)
     if bits:os.chmod(restored,bits)
   if filename.startswith("work-ledger-kernel"):
    launcher=z.getinfo("work-ledger-kernel")
    assert (launcher.external_attr>>16)&0o111,"Linux kernel launcher not executable in distribution"
   cwd=Path(td)/relative
   module_tests=sorted((cwd/"tests").rglob("test_*.py"))
   print("FULL_REGRESSION_START",filename,"tests_files",len(module_tests),flush=True)
   p=subprocess.run([sys.executable,"-m","pytest","-q","--disable-warnings","--maxfail=1","tests"],cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=350)
   print("FULL_REGRESSION_OUTPUT",filename,"\n"+p.stdout[-12000:],flush=True)
   if p.returncode != 0:
    errors.append(filename)
    print("FULL_REGRESSION_FAIL",filename,flush=True)
   else:
    print("FULL_REGRESSION_PASS",filename,flush=True)
print("FULL_REGRESSION_TOTAL_ERRORS",errors,flush=True)
assert not errors,"Full regression failed: "+repr(errors)
print("FULL_REGRESSION_GATE=PASS",flush=True)
