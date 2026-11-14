"""Apply minimal Kernel public facade to a TEMPORARY extracted candidate only."""
from pathlib import Path
import sys

kernel_file = Path(sys.argv[1])
source = kernel_file.read_text(encoding="utf-8")
needle = "    def work_reference_add(self, work_id: str, ref_type: str, value: str) -> dict:\n"
if source.count(needle) != 1:
    raise SystemExit("KERNEL_API_PATCH_ANCHOR_MISSING_OR_AMBIGUOUS")
if "    def work_reference_find(" in source:
    raise SystemExit("KERNEL_API_PATCH_ALREADY_PRESENT_OR_UNEXPECTED")
new = (
    '    def work_reference_find(self, query: str, *, include_archived: bool = False, limit: int = 50) -> dict:\n'
    '        """Public read-only facade onto existing WorkReferences.find."""\n'
    '        return self._work_refs().find(query, include_archived=include_archived, limit=limit)\n\n'
)
kernel_file.write_text(source.replace(needle, new + needle, 1), encoding="utf-8")
compile(kernel_file.read_text(encoding="utf-8"), str(kernel_file), "exec")
print("ISOLATED_KERNEL_REFERENCE_FIND_FACADE_PATCHED")
