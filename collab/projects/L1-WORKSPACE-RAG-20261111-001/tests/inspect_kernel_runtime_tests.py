"""Inspect only existing kernel tests for a real export_docs MSC regression harness."""
from pathlib import Path
import zipfile
root = Path(__file__).resolve().parents[1]
p = root / "candidates" / "work-ledger-kernel_v0_7_41_1116.zip"
if not p.is_file():
    # External Work main checkout copied this file to the isolated branch's fixed-input directory.
    p = Path("latest/collab/projects/L1-WORKSPACE-RAG-20261111-001/candidates/work-ledger-kernel_v0_7_41_1116.zip")
with zipfile.ZipFile(p) as z:
    for name in z.namelist():
        if not name.startswith("tests/") or not name.endswith(".py"):
            continue
        src = z.read(name).decode("utf-8")
        lines=src.splitlines()
        matches = [i for i,l in enumerate(lines) if "export_docs(" in l or "WorkUX(" in l or "name_for(" in l or "artifact_publish_map" in l or "add_evidence(" in l or "register_evidence(" in l]
        if name in ("tests/test_discussion_continuity_v0728.py", "tests/test_discussion_patch_v0729.py"):
            matches = list(range(min(len(lines),90)))
        if not matches: continue
        print("TEST_FILE",name,"MATCHES",len(matches),flush=True)
        shown=set()
        for i in matches[:8]:
            for j in range(max(0,i-7),min(len(lines),i+12)):
                if j not in shown:
                    print(f"{j+1:04d} {lines[j]}",flush=True)
                    shown.add(j)
