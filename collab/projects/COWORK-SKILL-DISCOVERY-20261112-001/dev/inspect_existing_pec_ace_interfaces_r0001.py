#!/usr/bin/env python3
"""Read only inspect two pinned, shareable skill development ZIP candidates.

No business host, network, source checkout mutation, package install, or writes.
Outputs only bounded relevant function context to the PRIVATE CI job log.
"""
import ast
import zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
CA=ROOT/"collab/projects/L1-WORKSPACE-RAG-20261111-001/candidates/code-analyzer_v0_15_3_1114.zip"
WF=ROOT/"collab/projects/L1-WORKSPACE-RAG-20261111-001/candidates/l1-fix-workflow_v1_6_70_1117.zip"
TASKS=[
(CA,"code-analyzer/scripts/ca_core/reuse_validator.py",("validate",)),
(CA,"code-analyzer/scripts/ca_core/provenance_resolver.py",("resolve",)),
(WF,"l1-fix-workflow/l1_fix_workflow/work_inspection.py",("inspect_work",)),
(WF,"l1-fix-workflow/l1_fix_workflow/continuity_flow.py",("work_resume",)),
]
for zp,needle,names in TASKS:
    print("==== ZIP",zp.name,"MEMBER",needle,"====")
    with zipfile.ZipFile(zp) as z:
        z.testzip()
        try: s=z.read(needle).decode("utf-8")
        except KeyError: print("NOT_FOUND");continue
    lines=s.splitlines()
    try: t=ast.parse(s)
    except SyntaxError as exc: print("SYNTAX_ERROR",exc);continue
    fn=[n for n in ast.walk(t) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name in names]
    print("MODULE_IMPORTS",[(type(n).__name__,ast.unparse(n)) for n in t.body if isinstance(n,(ast.Import,ast.ImportFrom))][:20])
    for f in fn:
        print("FUNCTION",f.name,"LINE",f.lineno,"END",f.end_lineno)
        for k,line in enumerate(lines[max(0,f.lineno-15):min(len(lines),f.lineno+115)],start=max(0,f.lineno-15)+1):
            print(f"{k:04d}|{line[:300]}")
    print("OTHER_TOP_FUNCTIONS",[n.name for n in t.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))][:32])
