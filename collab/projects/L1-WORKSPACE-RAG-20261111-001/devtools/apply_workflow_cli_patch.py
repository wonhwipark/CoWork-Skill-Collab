"""Add a separate opt-in CLPR existing-Work link CLI to temp extracted Workflow."""
from pathlib import Path
import sys

p=Path(sys.argv[1])
s=p.read_text(encoding='utf-8')
parser_anchor='    q=sp.add_parser("guide",'
main_anchor='    if args.cmd == "clpr-issue-plan":'
if s.count(parser_anchor)!=1 or s.count(main_anchor)!=1 or 'clpr-existing-work-link' in s:
    raise SystemExit('CLPR_CLI_PATCH_ANCHOR_INVALID')
parser_add='''    q=sp.add_parser("clpr-existing-work-link", help="Existing Work source references; preview default, explicit --commit")
    q.add_argument("--input-json", required=True)
    q.add_argument("--issue-identity", required=True)
    q.add_argument("--commit", action="store_true", help="opt-in writes to an EXISTING Work only")
'''
main_add='''    if args.cmd == "clpr-existing-work-link":
        from .issue_brief import plan_clpr_issue_cases
        from .clpr_existing_work_link import link_clpr_existing_work
        try:
            if args.commit and (getattr(args, "read_only", False) or __import__("os").environ.get("L1_WORKFLOW_MCP_READ_ONLY") == "1"):
                raise ValueError("CLPR_WRITE_DISABLED_BY_READ_ONLY")
            source = Path(args.input_json).expanduser()
            if source.is_symlink() or not source.is_file() or source.stat().st_size > 131072:
                raise ValueError("Input must be a small regular JSON file")
            if not args.ledger_root or not Path(args.ledger_root).expanduser().is_dir():
                raise ValueError("Existing --ledger-root directory required")
            if args.kernel_path:
                sys.path.insert(0, args.kernel_path)
            from work_ledger_kernel.kernel import WorkLedgerKernel
            from work_ledger_kernel.util import resolve_ledger_root
            plan = plan_clpr_issue_cases(json.loads(source.read_text(encoding="utf-8-sig")))
            kernel = WorkLedgerKernel(resolve_ledger_root(args.ledger_root))
            out = link_clpr_existing_work(plan, kernel,
                                          issue_identity=args.issue_identity, commit=args.commit)
            print(json.dumps(out, ensure_ascii=False, indent=2))
            return 0 if out.get("ok") else 2
        except (ValueError, OSError, TypeError, json.JSONDecodeError) as exc:
            print(json.dumps({"ok": False, "action": "CLPR_WORK_LINK_BLOCKED",
                              "writes": 0, "new_work_created": False,
                              "reason": str(exc)}, ensure_ascii=False))
            return 2
'''
s=s.replace(parser_anchor,parser_add+parser_anchor,1)
s=s.replace(main_anchor,main_add+main_anchor,1)
p.write_text(s, encoding='utf-8')
compile(s,str(p),'exec')
print('ISOLATED_WORKFLOW_EXPLICIT_LINK_CLI_PATCHED')
