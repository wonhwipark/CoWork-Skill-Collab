#!/usr/bin/env python3
"""Executable, negative-case release quality tests using real ZIP bytes."""
import hashlib
import json
import stat
import tempfile
import unittest
import zipfile
from pathlib import Path

from skill_release_quality_gate import GateError, validate

HASHES = ("MANIFEST_SHA256.json", "PACKAGE_CONTENTS.sha256")


def make_archive(dest: Path, *, version="0.7.44", mismatch=None,
                 uncovered=False, corrupt=False, unsafe=False, symlink=False):
    archive_name = dest.name
    files = {
        "SKILL.md": ("---\nname: test-kernel\nversion: " + version + "\n---\n").encode(),
        "VERSION": (version + "\n").encode(),
        "VERSION.md": ("# Version v" + version + "\n").encode(),
        ".skill-release.json": json.dumps({"version": version, "archive": archive_name}).encode(),
        "pkg/export.py": b"def export(value):\n    return value\n",
    }
    digests = {k: hashlib.sha256(v).hexdigest() for k, v in sorted(files.items())}
    if uncovered:
        digests.pop("pkg/export.py")
    if corrupt:
        digests["pkg/export.py"] = "0" * 64
    files[HASHES[0]] = (json.dumps(digests) + "\n").encode()
    files[HASHES[1]] = "".join(h + "  " + k + "\n" for k, h in digests.items()).encode()
    if mismatch:
        files["VERSION"] = (mismatch + "\n").encode()
    with zipfile.ZipFile(dest, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for name, data in files.items():
            z.writestr("root/" + name, data)
        if unsafe:
            z.writestr("root/../escape.txt", b"bad")
        if symlink:
            info = zipfile.ZipInfo("root/symlink")
            info.create_system = 3
            info.external_attr = (stat.S_IFLNK | 0o777) << 16
            z.writestr(info, b"../secret")


class ReleaseGateTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.zip = Path(self.tmp.name) / "sample_v0_7_44_1117.zip"

    def test_valid_bytes(self):
        make_archive(self.zip)
        result = validate(self.zip, "0.7.44")
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["hash_files"], 2)
        self.assertEqual(result["covered"], 5)

    def test_version_mismatch_blocks(self):
        make_archive(self.zip, mismatch="0.7.43")
        with self.assertRaisesRegex(GateError, "VERSION_MISMATCH"):
            validate(self.zip, "0.7.44")

    def test_unlisted_member_blocks(self):
        make_archive(self.zip, uncovered=True)
        with self.assertRaisesRegex(GateError, "MANIFEST_COVERAGE_MISMATCH"):
            validate(self.zip, "0.7.44")

    def test_wrong_hash_blocks(self):
        make_archive(self.zip, corrupt=True)
        with self.assertRaisesRegex(GateError, "MANIFEST_HASH_MISMATCH"):
            validate(self.zip, "0.7.44")

    def test_zip_traversal_blocks(self):
        make_archive(self.zip, unsafe=True)
        with self.assertRaisesRegex(GateError, "UNSAFE_OR_DUPLICATE"):
            validate(self.zip, "0.7.44")

    def test_zip_symlink_blocks(self):
        make_archive(self.zip, symlink=True)
        with self.assertRaisesRegex(GateError, "UNSAFE_OR_DUPLICATE"):
            validate(self.zip, "0.7.44")

    def test_manifest_absence_blocks(self):
        make_archive(self.zip)
        with zipfile.ZipFile(self.zip) as z:
            members = [(i.filename, z.read(i)) for i in z.infolist()
                       if not i.filename.endswith(HASHES)]
        with zipfile.ZipFile(self.zip, "w") as z:
            for name, body in members:
                z.writestr(name, body)
        with self.assertRaisesRegex(GateError, "MISSING_HASH_MANIFEST"):
            validate(self.zip, "0.7.44")


if __name__ == "__main__":
    unittest.main(verbosity=2)
