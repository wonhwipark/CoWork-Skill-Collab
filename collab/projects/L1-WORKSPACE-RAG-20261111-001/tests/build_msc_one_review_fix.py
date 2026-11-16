"""One review cycle: deterministic skill ZIP fixes, entirely isolated from operating hosts.
All inputs are exact hash-pinned PRIVATE development ZIPs. Does not call LLM or install.
"""
from __future__ import annotations

import copy
import datetime
import hashlib
import json
from pathlib import Path
import re
import stat
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
CAND = ROOT / "candidates"
FIXED_DATE = (2026, 11, 16, 12, 10, 0)

INPUTS = [
    ("doc-converter_v0_2_23_1116.zip", "43805ae0ce1b08205125441f383f6bdfc6f114ef53bb2609295827f10b1ce23e",
     "doc-converter_v0_2_24_1116.zip"),
    ("work-ledger-kernel_v0_7_40_1116.zip", "b8077fd717f326fb7bc556407b8e8b8a7f32a580e143ec3a6d646d3b1e9df7ce",
     "work-ledger-kernel_v0_7_41_1116.zip"),
]

def ensure(condition, msg):
    if not condition:
        raise RuntimeError(msg)

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def rep(src: str, old: str, new: str, key: str) -> str:
    ensure(src.count(old) == 1, f"ANCHOR_{key}: {src.count(old)}")
    return src.replace(old, new, 1)

class Archive:
    def __init__(self, path: Path, expected: str):
        raw = path.read_bytes()
        ensure(sha(raw) == expected, "SOURCE_SHA_PIN_MISMATCH " + path.name)
        self.infos = {}
        self.data = {}
        with zipfile.ZipFile(path) as z:
            ensure(z.testzip() is None, "BASE_ZIP_CRC")
            for info in z.infolist():
                name = info.filename
                ensure(not name.startswith("/") and ".." not in Path(name).parts
                       and "\\" not in name and not stat.S_ISLNK(info.external_attr >> 16),
                       "ZIP_UNSAFE " + name)
                ensure(name not in self.data, "ZIP_DUPLICATE " + name)
                if not info.is_dir():
                    self.infos[name] = copy.copy(info)
                    self.data[name] = z.read(info)
        print(f"PIN_PASS {path.name} {sha(raw)}")

    def get(self, name: str) -> str:
        ensure(name in self.data, "MISSING_MEMBER " + name)
        return self.data[name].decode("utf-8")

    def put(self, name: str, text: str):
        ensure(not name.startswith("/") and ".." not in Path(name).parts, "UNSAFE_OUTPUT")
        self.data[name] = text.encode("utf-8")

    def json(self, name: str):
        return json.loads(self.get(name))

    def put_json(self, name: str, obj):
        self.put(name, json.dumps(obj, ensure_ascii=False, indent=2) + "\n")

    def emit(self, dest: Path):
        dest.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(dest, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
            for name in sorted(self.data):
                info = self.infos.get(name)
                if info is None:
                    info = zipfile.ZipInfo(name, FIXED_DATE)
                    info.compress_type = zipfile.ZIP_DEFLATED
                    info.external_attr = 0o644 << 16
                z.writestr(info, self.data[name])
        with zipfile.ZipFile(dest) as z:
            ensure(z.testzip() is None, "OUTPUT_CRC " + dest.name)
            ensure(len(z.namelist()) == len(set(z.namelist())), "OUTPUT_DUPLICATE")
            ensure(all(z.read(n) == self.data[n] for n in self.data), "OUTPUT_BYTES")
        print(f"OUTPUT {dest.name} bytes={dest.stat().st_size} sha256={sha(dest.read_bytes())} members={len(self.data)}", flush=True)

def patch_converter(z: Archive):
    p = "doc-converter/"
    tool = z.get(p + "scripts/msc_tool.py")
    ensure("DIAGRAM_NAME_DUPLICATE" in tool and "PROCEDURE_FEATURE" in tool, "BASE_NOT_V023")
    tool = rep(tool, "import hashlib\n", "import hashlib\nimport unicodedata\n", "UNICODE_IMPORT")
    tool = rep(tool,
        '    specs_by_name: dict[str, dict[str, Any]] = {}\n',
        '    specs_by_name: dict[str, dict[str, Any]] = {}\n    used_names: set[str] = set()\n',
        "USED_NAMES")
    tool = rep(tool,
        '        raw_name = _clean_label(row.get("name") or f"diagram_{index}")',
        '        raw_name = unicodedata.normalize("NFC", _clean_label(row.get("name") or f"diagram_{index}"))',
        "NFC")
    tool = rep(tool,
        "        if name in specs_by_name:\n",
        "        if name.casefold() in used_names:\n",
        "CASEFOLD")
    tool = rep(tool,
        '        spec = row.get("spec")\n',
        '        used_names.add(name.casefold())\n        spec = row.get("spec")\n',
        "MARK_USED")
    tool = rep(tool,
        '                result["html_sha256"] = _sha256(html)\n',
        '                result["html_sha256"] = _sha256(html)\n'
        '                from msc_b_viewer import phase_button_report\n'
        '                result["html_phase_buttons"] = phase_button_report(svg, phases)\n',
        "PHASE_MANIFEST_RESULT")
    # Retain the contract and populate a small optional diagnostic on the existing public manifest rows.
    tool = rep(tool,
        '"html":r["name"]+".html" if r.get("html") else None}',
        '"html":r["name"]+".html" if r.get("html") else None, '
        '"html_phase_buttons":r.get("html_phase_buttons")}',
        "PHASE_PUBLIC_MANIFEST")
    # adapt_scenario_ir does not need a new writer; CLI and explicit IR source work through this existing entrypoint.
    tool = rep(tool,
        '        package=adapt_scenario_ir(_json_load(Path(ns.input)))\n',
        '        ir_payload=_json_load(Path(ns.input))\n'
        '        package=adapt_scenario_ir(ir_payload)\n'
        '        if "view_mode" in ir_payload:\n'
        '            if ir_payload["view_mode"] not in {"ISSUE", "PROCEDURE_FEATURE"}:\n'
        '                raise ValueError("SCENARIO_VIEW_MODE_INVALID")\n'
        '            package["view_mode"] = ir_payload["view_mode"]\n',
        "SCENARIO_IR_VIEW_MODE")
    z.put(p + "scripts/msc_tool.py", tool)

    viewer = z.get(p + "scripts/msc_b_viewer.py")
    addition = '''
def phase_button_report(svg_path: Path, phases: list[str]) -> dict:
    """Expose disabled phase navigation; never claim successful phase jumps for ambiguous SVG."""
    root = ET.fromstring(Path(svg_path).read_bytes())
    labels = list(dict.fromkeys(phases))
    enabled = []
    disabled = []
    for phase in labels:
        matches = []
        for element in root.iter():
            if element.tag.rsplit("}", 1)[-1].lower() != "text":
                continue
            label = "".join(element.itertext()).strip()
            if label == phase or label.strip("= ").strip() == phase:
                try:
                    matches.append(float(element.attrib["y"]))
                except (ValueError, KeyError):
                    continue
        if len(matches) == 1:
            enabled.append(phase)
        else:
            disabled.append({"phase": phase, "reason": "AMBIGUOUS" if len(matches) > 1 else "NOT_FOUND"})
    return {"requested": len(labels), "enabled": len(enabled), "disabled": disabled}


'''
    ensure("def phase_button_report(" not in viewer, "VIEWER_ALREADY_PATCHED")
    z.put(p + "scripts/msc_b_viewer.py", viewer + "\n" + addition)
    policy = z.json(p + "skillsilent/policy.json")
    acts = policy["actions"]
    act = acts["msc-package"]
    for flag in ("--view-mode",):
        if flag not in act["allowed_flags"]:
            act["allowed_flags"].append(flag)
        if flag not in act["value_flags"]:
            act["value_flags"].append(flag)
    if "msc-scenario-build" not in acts:
        scenario = copy.deepcopy(act)
        scenario["prefix_args"] = ["scenario-build"]
        scenario["summary"] = "Verified Scenario IR -> canonical MSC package with opt-in Procedure/Feature viewer"
        scenario["usage"] = "skillsilent run doc-converter msc-scenario-build -- --input <scenario-ir.json> --output-dir <outdir> --view-mode PROCEDURE_FEATURE --json"
        acts["msc-scenario-build"] = scenario
    else:
        scenario = acts["msc-scenario-build"]
        if "--view-mode" not in scenario["allowed_flags"]:
            scenario["allowed_flags"].append("--view-mode")
        if "--view-mode" not in scenario["value_flags"]:
            scenario["value_flags"].append("--view-mode")
    for action in ("msc-package", "msc-scenario-build"):
        a = acts[action]
        ensure("--view-mode" in a["allowed_flags"] and "--view-mode" in a["value_flags"]
               and a["prefix_args"][0] in {"package", "scenario-build"}, "POLICY_GATE_BAD")
    z.put_json(p + "skillsilent/policy.json", policy)

    version = "0.2.24"
    z.put(p + "VERSION", version + "\n")
    md = z.get(p + "SKILL.md")
    md = rep(md, "version: 0.2.21", "version: " + version, "SKILL_FRONTMATTER_VERSION")
    md = rep(md, "# doc-converter v0.2.21 —", "# doc-converter v0.2.24 —", "SKILL_TITLE_VERSION")
    z.put(p + "SKILL.md", md)
    z.put(p + "VERSION.md",
          "# doc-converter v0.2.24\n\n"
          "## v0.2.24 — one-cycle MSC patch, 2026-11-16 KST\n"
          "- Managed skillsilent package/scenario-build supports --view-mode PROCEDURE_FEATURE.\n"
          "- Windows case-insensitive names are collision-safe, NFC hashes deterministic.\n"
          "- HTML phase navigation omissions are visible in the existing public manifest.\n"
          "- Complete PACKAGE_CONTENTS.sha256 rebuilt from candidate bytes. No host writer or Knowledge publish assumed.\n\n"
          + z.get(p + "VERSION.md"))
    m = z.json(p + "skillsilent/manifest.json")
    m["skill_version"] = version
    z.put_json(p + "skillsilent/manifest.json", m)
    rel = z.json(p + ".skill-release.json")
    rel.update({"version": version, "revision": 24, "archive": "doc-converter_v0_2_24_1116.zip",
                "release_date": "2026-11-16", "built_at": "2026-11-16T12:10:00+09:00",
                "channel": "development_not_for_deployment",
                "release_kind": "development_not_for_deployment"})
    z.put_json(p + ".skill-release.json", rel)
    z.put(p + "tests/test_msc_review_fix_v0224.py", r'''import argparse
import json
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import msc_tool
from msc_b_viewer import phase_button_report


def _spec():
    return {"schema":"doc-converter/msc-spec/v1","kind":"AS_IS","title":"Synthetic",
            "participants":[{"id":"L1","label":"L1"},{"id":"RF","label":"RF"}],
            "steps":[{"type":"divider","label":"INIT"},
                     {"type":"message","id":"S1","from":"L1","to":"RF",
                      "label":"INIT_REQ","evidence_status":"CODE_CONFIRMED"}]}


def _fake_render(puml, svg, timeout=60):
    Path(svg).write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 300">'
                         '<text x="60" y="140">INIT</text></svg>', encoding="utf-8")
    return {"ok": True, "status": "READY"}


def _run(names, mode="PROCEDURE_FEATURE"):
    with tempfile.TemporaryDirectory() as t:
        root = Path(t)
        pkg = root / "pkg.json"
        pkg.write_text(json.dumps({"schema":"doc-converter/msc-package/v1","issue_id":"SYNTHETIC",
                                   "view_mode":mode,"diagrams":[{"name":n,"spec":_spec()} for n in names]}),encoding="utf-8")
        ns=argparse.Namespace(input=str(pkg),output_dir=str(root/"out"),overwrite=False,
                              allow_unrendered=False,timeout=5,json=True,view_mode=mode)
        with patch.object(msc_tool, "_render_puml",side_effect=_fake_render):
            status=msc_tool.cmd_package(ns)
        mf=root/"out"/"MSC_MANIFEST.json"
        return status,json.loads(mf.read_text(encoding="utf-8")),root/"out"


def test_case_only_names_hard_fail(capsys):
    code,man,_=_run(["Init","init"])
    assert code != 0
    assert any(e["code"]=="DIAGRAM_NAME_DUPLICATE" for e in man["package_errors"])


def test_nfc_nfd_stability(capsys):
    import unicodedata
    a="한글초기화"
    b=unicodedata.normalize("NFD",a)
    code1,man1,_=_run([a])
    code2,man2,_=_run([b])
    assert code1 == code2 == 0
    assert man1["diagrams"][0]["name"] == man2["diagrams"][0]["name"]
    code3,man3,_=_run([a,b])
    assert code3 != 0
    assert any(e["code"]=="DIAGRAM_NAME_DUPLICATE" for e in man3["package_errors"])


def test_policy_has_both_actions():
    policy=json.loads((Path(__file__).resolve().parents[1]/"skillsilent"/"policy.json").read_text(encoding="utf-8"))
    for name in ("msc-package","msc-scenario-build"):
        flags=policy["actions"][name]
        assert "--view-mode" in flags["allowed_flags"]
        assert "--view-mode" in flags["value_flags"]


def test_phase_missing_and_ambiguous_are_visible(tmp_path):
    svg=tmp_path/"sample.svg"
    svg.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
                   '<text y="20">INIT</text><text y="50">INIT</text></svg>',encoding="utf-8")
    report=phase_button_report(svg,["INIT","UNKNOWN"])
    assert report["requested"]==2 and report["enabled"]==0
    assert {r["reason"] for r in report["disabled"]}=={"AMBIGUOUS","NOT_FOUND"}
''')
    z.put(p + "DEVELOPMENT_MSC_ONE_CYCLE_v0_2_24.md",
          "# One review cycle development fix (2026-11-16)\n"
          "- R1 review findings B1/M1/M2/m1/m2/m3 corrected or guarded. No additional Claude review requested.\n"
          "- Installation/host writer G0 and Knowledge publish remain separate; development_not_for_deployment.\n"
          "- Scope: doc-converter only; workflow/analyzer unchanged.\n")
    # Recreate checksum list from all actual packaged bytes (do not include the list itself).
    lines = []
    for name, data in sorted(z.data.items()):
        if not name.startswith(p) or name.endswith("/") or name == p + "PACKAGE_CONTENTS.sha256":
            continue
        lines.append(f"{sha(data)}  {name[len(p):]}")
    z.put(p + "PACKAGE_CONTENTS.sha256", "\n".join(lines) + "\n")
    ensure(len(lines) >= 80, "DOC_CHECKSUM_COUNT")
    print("DOC_POLICY_ACTIONS",len(acts),"CHECKSUMS",len(lines),flush=True)

def patch_kernel(z: Archive):
    names = z.get("work_ledger_kernel/artifact_names.py")
    names = rep(names,
        "if suffix not in ('.md', '.txt', '.html', '.json'):",
        "if suffix not in ('.md', '.txt', '.html', '.json', '.svg'):",
        "SVG_NAME_FOR")
    names = rep(names,
        "html|json)$')",
        "html|json|svg)$')",
        "SVG_LEGACY_SCAN")
    z.put("work_ledger_kernel/artifact_names.py", names)

    export = z.get("work_ledger_kernel/work_ux.py")
    # Only explicitly identified MSC images can be published, other SVGs continue being silently skipped (v0.7.39 behavior).
    old = '''                if (safe_source and e.get("kind") != "change_provenance" and copy_small_evidence
                        and src.is_file() and src.suffix.lower() == ".svg" and src.stat().st_size > max_copy_bytes):
                    raise KernelError("MSC_SVG_TOO_LARGE", "MSC SVG exceeds the authorized export size limit")
                if safe_source and e.get("kind") != "change_provenance" and copy_small_evidence and src.is_file() and src.suffix.lower() in {".md", ".html", ".json", ".txt", ".svg"} and src.stat().st_size <= max_copy_bytes:'''
    new = '''                # Explicit MSC evidence only; unrelated SVGs retain v0.7.39 skip behavior.
                is_msc_svg = (src.suffix.lower() == ".svg"
                              and ("msc" in str(e.get("kind") or "").lower()
                                   or "msc" in str(e.get("artifact_role") or "").lower()
                                   or "msc" in source_rel.lower()))
                if (safe_source and e.get("kind") != "change_provenance" and copy_small_evidence
                        and src.is_file() and is_msc_svg and src.stat().st_size > max_copy_bytes):
                    raise KernelError("MSC_SVG_TOO_LARGE", "MSC SVG exceeds the authorized export size limit")
                if safe_source and e.get("kind") != "change_provenance" and copy_small_evidence and src.is_file() and (src.suffix.lower() in {".md", ".html", ".json", ".txt"} or is_msc_svg) and src.stat().st_size <= max_copy_bytes:'''
    export = rep(export,old,new,"MSC_SCOPE")
    export = rep(export, '                    category = evidence_category(e)\n',
        '                    if is_msc_svg:\n'
        '                        _validate_safe_msc_svg(src)\n'
        '                    category = evidence_category(e)\n',
        "VALIDATE_SVG")
    helper = '''
def _validate_safe_msc_svg(path: Path) -> None:
    """Reject active content in an SVG that can be opened directly in a published Work."""
    from xml.etree import ElementTree as ET
    data = path.read_bytes()
    if b"<!DOCTYPE" in data.upper() or b"<!ENTITY" in data.upper():
        raise KernelError("MSC_SVG_UNSAFE", "DTD or entity forbidden")
    try:
        root = ET.fromstring(data)
    except ET.ParseError as exc:
        raise KernelError("MSC_SVG_INVALID", "not valid SVG") from exc
    if root.tag.rsplit("}", 1)[-1].lower() != "svg":
        raise KernelError("MSC_SVG_INVALID", "not SVG root")
    for node in root.iter():
        if node.tag.rsplit("}", 1)[-1].lower() in {"script", "foreignobject", "iframe", "object", "embed"}:
            raise KernelError("MSC_SVG_UNSAFE", "active SVG element")
        for key, value in node.attrib.items():
            field = key.rsplit("}", 1)[-1].lower()
            if field.startswith("on") or (field in {"href", "src"} and not str(value).startswith("#")):
                raise KernelError("MSC_SVG_UNSAFE", "active/external SVG attribute")


'''
    anchor="from .artifact_names import name_for, scan as scan_artifact_publication, sha as artifact_sha, MAP_PATH\n"
    export = rep(export, anchor, anchor + "\n" + helper, "SVG_SAFE_HELPER")
    z.put("work_ledger_kernel/work_ux.py", export)

    version = "0.7.41-dev.1"
    z.put("VERSION", version + "\n")
    md = z.get("SKILL.md")
    if "version: 0.7.38-dev.1" in md:
        md = rep(md, "version: 0.7.38-dev.1","version: "+version,"KERNEL_SKILL_FRONTMATTER")
    first = re.search(r'(?m)^# (work-ledger-kernel.*v0\.7\.38-dev\.1.*)$', md)
    if first:
        md = md[:first.start()] + md[first.start():].replace("v0.7.38-dev.1","v0.7.41-dev.1",1)
    z.put("SKILL.md",md)
    rel = z.json(".skill-release.json")
    rel.update({"version": version, "skill_version": version, "revision": 41, "archive": "work-ledger-kernel_v0_7_41_1116.zip",
                "based_on": "0.7.40-dev.1", "release_date":"2026-11-16",
                "channel":"development_not_for_deployment", "release_kind":"development_not_for_deployment"})
    z.put_json(".skill-release.json",rel)

    z.put("tests/test_msc_svg_export_v0741.py", r'''from pathlib import Path
import pytest
from work_ledger_kernel.artifact_names import name_for
from work_ledger_kernel.work_ux import _validate_safe_msc_svg
from work_ledger_kernel.errors import KernelError


def test_msc_svg_name_is_supported():
    value=name_for("analysis","MSC_INIT.svg","E-1234567890ab")
    assert value.endswith(".svg") and "1234567890ab" in value


def test_safe_svg_blocks_script(tmp_path):
    path=tmp_path/"MSC.svg"
    path.write_text('<svg xmlns="http://www.w3.org/2000/svg"><script>bad()</script></svg>',encoding="utf-8")
    with pytest.raises(KernelError):
        _validate_safe_msc_svg(path)


def test_safe_svg_accepts_simple_svg(tmp_path):
    path=tmp_path/"MSC.svg"
    path.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
                    '<text y="20">INIT</text></svg>',encoding="utf-8")
    _validate_safe_msc_svg(path)
''')
    z.put("DEVELOPMENT_MSC_ONE_CYCLE_v0_7_41.md",
          "# Kernel one-cycle MSC SVG export fix (2026-11-16)\n"
          "- Extend artifact publication naming to .svg for verified, explicitly MSC-identified Evidence.\n"
          "- Preserve old behavior for unrelated SVG and oversize MD/HTML. Active/direct-open SVG content blocks.\n"
          "- Continue using existing published_path digest and collision checks. G0 writer/host not validated.\n"
          "- One reviewer cycle; no subsequent review requested. development_not_for_deployment.\n")
    checksum={}
    for name, data in sorted(z.data.items()):
        if name == "MANIFEST_SHA256.json":
            continue
        checksum[name] = sha(data)
    z.put_json("MANIFEST_SHA256.json",checksum)
    print("KERNEL_MANIFEST_FILES",len(checksum),flush=True)

def main():
    for original, expected, outname in INPUTS:
        z=Archive(CAND / original, expected)
        if original.startswith("doc-converter"):
            patch_converter(z)
        else:
            patch_kernel(z)
        z.emit(CAND / outname)

if __name__ == "__main__":
    main()
