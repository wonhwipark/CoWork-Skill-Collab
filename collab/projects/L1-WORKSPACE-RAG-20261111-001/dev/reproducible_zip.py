#!/usr/bin/env python3
"""Deterministic packaging helper for pinned development candidates only."""
from __future__ import annotations
import stat
import zipfile
from pathlib import Path, PurePosixPath

ZIP_TIME=(2026,11,18,0,0,0)

def rezip(root: Path, output: Path) -> None:
    root=root.resolve()
    output.parent.mkdir(parents=True,exist_ok=True)
    members=sorted((p for p in root.rglob("*") if p.is_file()),
                   key=lambda p:p.relative_to(root).as_posix())
    seen=set()
    with zipfile.ZipFile(output,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=8) as z:
        for p in members:
            rel=p.relative_to(root).as_posix()
            parts=PurePosixPath(rel).parts
            if ("__pycache__" in parts or rel.endswith(".pyc")
                or parts[0]=="artifacts"):
                continue
            if (rel.startswith("/") or ".." in parts or "\\" in rel
                or rel in seen or p.is_symlink()):
                raise RuntimeError("UNSAFE_ARCHIVE_MEMBER:"+rel)
            seen.add(rel)
            mode=0o100755 if p.stat().st_mode & (stat.S_IXUSR|stat.S_IXGRP|stat.S_IXOTH) else 0o100644
            info=zipfile.ZipInfo(rel,date_time=ZIP_TIME)
            info.create_system=3
            info.external_attr=(mode<<16)
            info.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=8)
    with zipfile.ZipFile(output) as z:
        if z.testzip() is not None:raise RuntimeError("ZIP_CRC_FAILED")
        if len(z.namelist())!=len(set(z.namelist())):raise RuntimeError("DUPLICATE_ZIP_MEMBERS")
