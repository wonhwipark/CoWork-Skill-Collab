#!/usr/bin/env python3
"""Actual Kernel Work/Evidence -> export_docs regression (not source-token checks)."""
import hashlib
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ARCHIVE = Path(__file__).resolve().parent / "output" / "work-ledger-kernel_v0_7_43_1117.zip"


class KernelSvgFunctionalTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix="kernel-svg-functional-")
        cls.root = Path(cls.temp.name) / "package"
        with zipfile.ZipFile(ARCHIVE) as archive:
            if archive.testzip():
                raise AssertionError("KERNEL_ZIP_CRC_INVALID")
            archive.extractall(cls.root)
        reg = cls.root / "contracts" / "registry_v1.json"
        cls.registry = json.loads(reg.read_text(encoding="utf-8"))
        print("KERNEL_REGISTRY_KEYS", list(cls.registry.keys()))
        print("KERNEL_REGISTRY_HEAD", str(cls.registry)[:4400])
        sys.path.insert(0, str(cls.root))
        from work_ledger_kernel.kernel import WorkLedgerKernel
        from work_ledger_kernel.work_ux import WorkUX
        cls.Kernel = WorkLedgerKernel
        cls.WorkUX = WorkUX

    @classmethod
    def tearDownClass(cls):
        sys.path.remove(str(cls.root))
        cls.temp.cleanup()

    def setUp(self):
        self.base = Path(self.temp.name) / self._testMethodName
        self.base.mkdir()
        self.ledger = self.Kernel(self.base / "ledger")

    def add(self, kind, name, content, work_title):
        work = self.ledger.work_create(work_title, profile="BUG")
        wid = work["work_id"]
        source = self.base / ("in-" + wid) / name
        source.parent.mkdir(parents=True)
        source.write_text(content, encoding="utf-8")
        evidence = self.ledger.record_evidence(
            wid, source, kind, "utility", "doc-converter", "0.2.26",
            "test-source-rev", "Synthetic test artifact", "AUTO_CANDIDATE",
        )
        self.assertIsInstance(evidence, dict)
        return wid, source, evidence

    def test_msc_svg_is_published_with_hash_and_idempotent(self):
        wid, source, e = self.add(
            "render_output", "msc_scenario.svg",
            '<svg xmlns="http://www.w3.org/2000/svg"><rect width="2" height="2"/></svg>',
            "MSC SVG export",
        )
        dest = self.base / "published-svg"
        a = self.ledger.work_docs_export(str(dest), wid)
        self.assertIsNot(a.get("ok"), False, a)
        published = list(dest.rglob("*.svg"))
        self.assertEqual(len(published), 1, published)
        self.assertEqual(published[0].read_bytes(), source.read_bytes())
        mappings = [json.loads(p.read_text(encoding="utf-8"))
                    for p in dest.rglob("*.json") if "artifact" in p.name.lower()]
        flattened = [x for m in mappings for x in m.get("entries", [])]
        self.assertTrue(any(x.get("sha256") == hashlib.sha256(source.read_bytes()).hexdigest()
                            and x.get("published_path", "").endswith(".svg")
                            for x in flattened), mappings)
        b = self.ledger.work_docs_export(str(dest), wid)
        self.assertIsNot(b.get("ok"), False, b)
        self.assertEqual(published[0].read_bytes(), source.read_bytes())
        print("KERNEL_SVG_EVIDENCE_EXPORT_HASH_IDEMPOTENT_PASS", wid)

    def test_large_msc_svg_is_rejected(self):
        wid, source, e = self.add(
            "render_output", "msc_oversize.svg",
            '<svg xmlns="http://www.w3.org/2000/svg">' + " " * 256 + "</svg>",
            "Large MSC SVG",
        )
        from work_ledger_kernel.errors import KernelError
        with self.assertRaisesRegex(KernelError, "MSC_SVG_TOO_LARGE"):
            self.WorkUX(self.ledger).export_docs(
                str(self.base / "published-large"), work_id=wid, max_copy_bytes=64,
            )
        print("KERNEL_MSC_SVG_SIZE_FAIL_CLOSED_PASS", wid)

    def test_unrelated_svg_does_not_break_md_export(self):
        work = self.ledger.work_create("Unrelated SVG plus MD", profile="BUG")
        wid = work["work_id"]
        source_dir = self.base / "unrelated"
        source_dir.mkdir()
        svg = source_dir / "figure.svg"
        svg.write_text('<svg xmlns="http://www.w3.org/2000/svg"/>', encoding="utf-8")
        md = source_dir / "report.md"
        md.write_text("# Existing evidence\n", encoding="utf-8")
        for path in (svg, md):
            self.ledger.record_evidence(
                wid, path, "impact", "analyze", "code-analyzer", "0.15.3",
                "test-rev", "Existing evidence", "AUTO_CANDIDATE",
            )
        dest = self.base / "published-unrelated"
        result = self.ledger.work_docs_export(str(dest), wid)
        self.assertIsNot(result.get("ok"), False, result)
        self.assertEqual(list(dest.rglob("*.svg")), [])
        self.assertEqual(len(list(dest.rglob("*.md"))) > 0, True)
        print("KERNEL_UNRELATED_SVG_NO_REGRESSION_PASS", wid)


if __name__ == "__main__":
    unittest.main(verbosity=2)
