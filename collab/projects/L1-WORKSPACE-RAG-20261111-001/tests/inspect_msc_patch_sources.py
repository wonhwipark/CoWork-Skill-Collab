"""Print only the skill code regions required by the accepted one-cycle fix."""
from pathlib import Path
import re
import zipfile

ROOT=Path(__file__).resolve().parents[1]
specs={
"doc-converter_v0_2_23_1116.zip":{
    "doc-converter/scripts/msc_tool.py":["import ", "def cmd_package","def cmd_scenario_build","def msc_view_text","raw_name =","if name in","specs_by_name","public_manifest","diagram_results.append(result)","def main", "view_mode ="],
    "doc-converter/scripts/scenario_ir_adapter.py":["def ","payload","view_mode", "argparse", "package"],
    "doc-converter/scripts/msc_b_viewer.py":["def build_html", "controls.append", "for phase","return ("],
    "doc-converter/skillsilent/policy.json":["msc-package", "msc-scenario-build", "allowed_flags"],
    "doc-converter/skillsilent/manifest.json":[],
    "doc-converter/SKILL.md":["version","Version","0.2.21"],
    "doc-converter/VERSION.md":[],
    "doc-converter/PACKAGE_CONTENTS.sha256":[],
    "doc-converter/.skill-release.json":[],
},
"work-ledger-kernel_v0_7_40_1116.zip":{
    "work_ledger_kernel/work_ux.py":["def export_docs","MSC_SVG_TOO_LARGE","name_for", "copy_small_evidence","safe_source"],
    "work_ledger_kernel/artifact_names.py":[],
    "tests/test_msc_svg_export_v0740.py":[],
    "SKILL.md":["version","Version","0.7.38"],
    "VERSION":[],
    ".skill-release.json":[],
}
}
with_opts={"doc-converter/skillsilent/policy.json","doc-converter/skillsilent/manifest.json"}
for zname,files in specs.items():
    print("\n### ZIP",zname,flush=True)
    with zipfile.ZipFile(ROOT/"candidates"/zname) as z:
        available=set(z.namelist())
        for name,needles in files.items():
            if name not in available:
                print("MISSING",name,flush=True)
                continue
            text=z.read(name).decode("utf-8")
            lines=text.splitlines()
            if name.endswith("PACKAGE_CONTENTS.sha256"):
                print("FILE",name, "COUNT",len(lines), "HEAD", "\n".join(lines[:12]),flush=True)
                continue
            selected=set()
            if not needles:
                selected.update(range(min(len(lines),100)))
            else:
                for i,line in enumerate(lines):
                    if any(n in line for n in needles):
                        selected.update(range(max(0,i-7),min(len(lines),i+13)))
            if name in with_opts:
                selected.update(range(0,min(40,len(lines))))
            print("\nFILE",name,"TOTAL_LINES",len(lines),flush=True)
            for i in sorted(selected)[:430]:
                print(f"{i+1:04d}: {lines[i]}",flush=True)
