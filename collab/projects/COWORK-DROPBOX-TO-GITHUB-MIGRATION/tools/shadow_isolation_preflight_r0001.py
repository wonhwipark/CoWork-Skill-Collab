"""Synthetic shadow-isolation preflight for CoWork GitHub migration.

NO production access, NO network, NO review model, NO Telegram, NO key generation.
Does not replace integration tests for skill-collab-watcher v0.2.4.

Run: python shadow_isolation_preflight_r0001.py
"""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import sqlite3
import tempfile
import unittest


def file_digest(path: Path) -> str | None:
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot_files(db: Path) -> dict[str, str | None]:
    return {suffix: file_digest(Path(str(db) + suffix)) for suffix in ("", "-wal", "-shm")}


def assert_disjoint_shadow_paths(live_dir: Path, shadow_dir: Path, live_db: Path) -> None:
    """Reject any shadow-root that is inside the live root, even via symlinks.

    Real Windows implementation must also verify junctions/reparse points, ACLs,
    handles and path identity. This pure-path guard is an offline proof of intent.
    """
    live_dir = live_dir.resolve(strict=True)
    shadow_dir = shadow_dir.resolve(strict=True)
    live_db = live_db.resolve(strict=True)
    if not live_db.is_file() or live_dir not in live_db.parents:
        raise ValueError("DB is not inside designated live directory")
    if shadow_dir == live_dir or shadow_dir in live_dir.parents or live_dir in shadow_dir.parents:
        raise ValueError("SHADOW_DIRECTORY_OVERLAP_WITH_LIVE")


def synthetic_shadow_read_only_scan(shadow_dir: Path) -> None:
    """Simulates shadow's separate *state store*, not actual GitHub adapter.

    A real SHADOW should use separate local-only state and GitHub GET only, and
    must NOT open the operating SQLite database or acquire its WAL/SHM locks.
    """
    db = shadow_dir / "shadow_only.sqlite"
    with sqlite3.connect(db) as c:
        c.execute("create table if not exists scanned(commit_sha text primary key)")
        c.execute("insert or ignore into scanned values ('synthetic-commit')")
    with sqlite3.connect(f"file:{db.as_posix()}?mode=ro", uri=True) as c:
        assert c.execute("select count(*) from scanned").fetchone()[0] == 1


class IsolationPreflight(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.live = root / "live"
        self.shadow = root / "shadow"
        self.live.mkdir()
        self.shadow.mkdir()
        self.db = self.live / "operating.sqlite"
        self.conn = sqlite3.connect(self.db)
        self.addCleanup(self.conn.close)
        self.conn.execute("pragma journal_mode=wal")
        self.conn.execute("pragma wal_autocheckpoint=0")
        self.conn.execute("create table jobs(id integer primary key, status text)")
        self.conn.execute("insert into jobs(status) values ('COMPLETED')")
        self.conn.commit()
        self.assertTrue(Path(str(self.db) + "-wal").exists())
        self.assertTrue(Path(str(self.db) + "-shm").exists())

    def test_disjoint_paths_allow_shadow(self):
        assert_disjoint_shadow_paths(self.live, self.shadow, self.db)

    def test_nested_shadow_rejected(self):
        nested = self.live / "shadow"
        nested.mkdir()
        with self.assertRaisesRegex(ValueError, "OVERLAP"):
            assert_disjoint_shadow_paths(self.live, nested, self.db)

    def test_parent_shadow_rejected(self):
        with self.assertRaisesRegex(ValueError, "OVERLAP"):
            assert_disjoint_shadow_paths(self.live, self.live.parent, self.db)

    def test_symlink_shadow_rejected(self):
        alias = self.shadow / "alias_to_live"
        try:
            alias.symlink_to(self.live, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("symlink not supported on this host")
        with self.assertRaisesRegex(ValueError, "OVERLAP"):
            assert_disjoint_shadow_paths(self.live, alias, self.db)

    def test_operating_main_wal_shm_bytes_unchanged(self):
        before = snapshot_files(self.db)
        self.assertTrue(all(before.values()))
        assert_disjoint_shadow_paths(self.live, self.shadow, self.db)
        synthetic_shadow_read_only_scan(self.shadow)
        after = snapshot_files(self.db)
        self.assertEqual(before, after, "Live DB main/WAL/SHM must be byte-identical")
        self.assertTrue((self.shadow / "shadow_only.sqlite").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
