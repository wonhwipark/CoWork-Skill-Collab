#!/usr/bin/env python3
"""Fail-closed, read-only quality gate for immutable skill ZIP releases.

Checks archive safety, version declarations, manifest accuracy and coverage.
Does not modify packages, install skills, publish a release, or call a model.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import stat
import sys
import zipfile
from pathlib import Path, PurePosixPath

HASH_FILES = {"MANIFEST_SHA256.json", "PACKAGE_CONTENTS.sha256"}
SEMVER = re.compile(r"(?<![0-9])v?([0-9]+\.[0-9]+\.[0-9]+)(?![0-9])")
SHA256 = re.compile(r"^[0-9a-f]{64}$")


class GateError(RuntimeError):
    pass


def normalize_members(archive: zipfile.ZipFile) -> dict[str, bytes]:
    files: dict[str, bytes] = {}
    all_names: set[str] = set()
    for info in archive.infolist():
        name = info.filename
        p = PurePosixPath(name)
        if (not name or name.startswith("/") or "\\" in name
                or any(part in ("", ".", "..") for part in p.parts)
                or name in all_names
                or stat.S_IFMT(info.external_attr >> 16) == stat.S_IFLNK):
            raise GateError("UNSAFE_OR_DUPLICATE_MEMBER: " + repr(name))
        all_names.add(name)
        if info.is_dir():
            continue
        if name in files:
            raise GateError("DUPLICATE_MEMBER: " + name)
        files[name] = archive.read(info)
    if not files:
        raise GateError("EMPTY_PACKAGE")
    roots = set(x.split("/", 1)[0] for x in files)
    if "SKILL.md" not in files and len(roots) == 1:
        prefix = next(iter(roots)) + "/"
        if all(x.startswith(prefix) for x in files):
            files = {x[len(prefix):]: data for x, data in files.items()}
    if "SKILL.md" not in files:
        raise GateError("MISSING_SKILL_MD")
    return files


def semver(text: str, label: str, *, required: bool = True) -> str | None:
    match = SEMVER.search(text)
    if match:
        return match.group(1)
    if required:
        raise GateError("VERSION_UNREADABLE: " + label)
    return None


def version_checks(files: dict[str, bytes], expected: str, archive_name: str) -> None:
    if "VERSION" not in files:
        raise GateError("MISSING_VERSION")
    actual = semver(files["VERSION"].decode("utf-8").strip(), "VERSION")
    if actual != expected:
        raise GateError("VERSION_MISMATCH: VERSION " + str(actual) + " != " + expected)
    if ".skill-release.json" in files:
        release = json.loads(files[".skill-release.json"].decode("utf-8"))
        for key in ("version", "skill_version"):
            if key in release and str(release[key]).lstrip("v") != expected:
                raise GateError("VERSION_MISMATCH: release." + key)
        if release.get("archive") and release["archive"] != archive_name:
            raise GateError("ARCHIVE_NAME_MISMATCH")
    if ".skill-main.json" in files:
        main = json.loads(files[".skill-main.json"].decode("utf-8"))
        for key in ("version", "skill_version"):
            if key in main and SEMVER.fullmatch(str(main[key])) and str(main[key]).lstrip("v") != expected:
                raise GateError("VERSION_MISMATCH: main." + key)
    # Only canonical version declarations, never historic release notes.
    skill = files["SKILL.md"].decode("utf-8")
    head = skill[:2000].splitlines()[:45]
    declarations = []
    for line in head:
        if re.match(r"^\s*(version|skill_version|버전)\s*[:：]\s*", line, re.I):
            declarations.append(line)
        elif re.match(r"^\s*[-#* ]{0,6}(current version|현재 버전)\s*[:：]", line, re.I):
            declarations.append(line)
    for line in declarations:
        v = semver(line, "SKILL.md declaration")
        if v != expected:
            raise GateError("VERSION_MISMATCH: SKILL.md " + v + " line=" + repr(line[:160]))
    if "VERSION.md" in files:
        head = "\n".join(files["VERSION.md"].decode("utf-8").splitlines()[:15])
        v = semver(head, "VERSION.md")
        if v != expected:
            raise GateError("VERSION_MISMATCH: VERSION.md " + v)
    if "skillsilent/manifest.json" in files:
        meta = json.loads(files["skillsilent/manifest.json"].decode("utf-8"))
        for key in ("skill_version", "package_version"):
            if key in meta and str(meta[key]).lstrip("v") != expected:
                raise GateError("VERSION_MISMATCH: skillsilent/manifest." + key)


def manifest_checks(files: dict[str, bytes]) -> dict[str, int]:
    targets = {x for x in files if x not in HASH_FILES}
    result = {"hash_files": 0, "covered": 0}
    for manifest_name in sorted(HASH_FILES & files.keys()):
        result["hash_files"] += 1
        data = files[manifest_name].decode("utf-8")
        if manifest_name.endswith(".json"):
            mapping = json.loads(data)
            if not isinstance(mapping, dict):
                raise GateError("MANIFEST_FORMAT_UNSUPPORTED: " + manifest_name)
        else:
            mapping = {}
            for line in data.splitlines():
                if not line.strip():
                    continue
                m = re.fullmatch(r"([0-9a-fA-F]{64})  (.+)", line)
                if not m or m.group(2) in mapping:
                    raise GateError("MANIFEST_FORMAT_UNSUPPORTED: " + manifest_name)
                mapping[m.group(2)] = m.group(1).lower()
        if set(mapping) != targets:
            missing = sorted(targets - set(mapping))
            extra = sorted(set(mapping) - targets)
            raise GateError("MANIFEST_COVERAGE_MISMATCH: " + manifest_name
                            + " unlisted=" + repr(missing[:12]) + " extra=" + repr(extra[:12]))
        for filename, digest in mapping.items():
            if not isinstance(digest, str) or not SHA256.fullmatch(digest.lower()):
                raise GateError("MANIFEST_INVALID_HASH: " + filename)
            if hashlib.sha256(files[filename]).hexdigest() != digest.lower():
                raise GateError("MANIFEST_HASH_MISMATCH: " + filename)
        result["covered"] = max(result["covered"], len(mapping))
    if not result["hash_files"]:
        raise GateError("MISSING_HASH_MANIFEST")
    return result


def validate(path: Path, expected: str) -> dict:
    if not re.fullmatch(r"\d+\.\d+\.\d+", expected):
        raise GateError("BAD_EXPECTED_VERSION")
    with zipfile.ZipFile(path) as z:
        bad = z.testzip()
        if bad:
            raise GateError("ZIP_CRC_FAILED: " + bad)
        files = normalize_members(z)
    version_checks(files, expected, path.name)
    hashes = manifest_checks(files)
    return {"status": "PASS", "archive": path.name, "version": expected,
            "members": len(files), **hashes,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "bytes": path.stat().st_size}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--zip", type=Path, required=True)
    parser.add_argument("--expected-version", required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(validate(args.zip, args.expected_version), sort_keys=True))
        return 0
    except (GateError, ValueError, OSError, zipfile.BadZipFile, UnicodeError, KeyError) as exc:
        print("RELEASE_GATE_FAIL: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
