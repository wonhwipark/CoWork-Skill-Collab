from __future__ import annotations

import sqlite3
import uuid
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path

from .models import JobRecord, JobState

SCHEMA = """
CREATE TABLE IF NOT EXISTS jobs (
    processing_key TEXT PRIMARY KEY,
    request_id TEXT NOT NULL,
    request_revision TEXT NOT NULL,
    package_sha256 TEXT NOT NULL,
    state TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    attempt_count INTEGER NOT NULL DEFAULT 0,
    last_error TEXT,
    result_path TEXT
);

CREATE TABLE IF NOT EXISTS cursors (
    name TEXT PRIMARY KEY,
    cursor_value TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL,
    event TEXT NOT NULL,
    processing_key TEXT,
    detail TEXT
);

CREATE TABLE IF NOT EXISTS counters (
    name TEXT PRIMARY KEY,
    value INTEGER NOT NULL DEFAULT 0
);

-- A request id stays here from the moment a delta mentions it until it
-- reaches a final decision, independent of the Dropbox cursor.
CREATE TABLE IF NOT EXISTS pending_requests (
    request_id TEXT PRIMARY KEY,
    reason TEXT,
    updated_at TEXT NOT NULL
);

-- Single active provider. Exactly one row; epoch increases on every switch.
CREATE TABLE IF NOT EXISTS provider_lease (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    provider TEXT NOT NULL,
    epoch INTEGER NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS provider_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL,
    from_provider TEXT,
    to_provider TEXT NOT NULL,
    epoch INTEGER NOT NULL
);

-- Which watcher process claimed a job. Used to tell a job still owned by a
-- live process from one left behind by a process that died (B-3).
CREATE TABLE IF NOT EXISTS job_claims (
    processing_key TEXT PRIMARY KEY,
    owner TEXT NOT NULL,
    claimed_at TEXT NOT NULL
);
"""

IN_FLIGHT = (JobState.CLAIMED.value, JobState.REVIEW_RUNNING.value)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class ProviderConflict(RuntimeError):
    """Another provider already holds the LIVE lease, or a switch is not safe now."""


class StateStore:
    _ONCE_LIMIT = 5000

    def __init__(self, db_path: Path, *, read_only: bool = False):
        self.read_only = read_only
        self.owner = uuid.uuid4().hex
        self.sealed_at_open = False
        self.shadow_log: list[tuple[str, str | None, str | None]] = []
        db_path.parent.mkdir(parents=True, exist_ok=True)
        if read_only:
            # mode=ro: a plain connection checkpoints the WAL into the main file on
            # close, which changes the database file even when nothing is written.
            self.conn = sqlite3.connect(f"file:{db_path.as_posix()}?mode=ro", uri=True,
                                        isolation_level=None, timeout=15)
            self.conn.execute("PRAGMA query_only=ON")
        else:
            # busy timeout: `status` may read while the watch loop writes.
            self.conn = sqlite3.connect(str(db_path), isolation_level=None, timeout=15)
            self.conn.execute("PRAGMA journal_mode=WAL")
            # WAL+NORMAL never corrupts and replays commits in order, so the
            # "pending row written before cursor" ordering survives a crash.
            self.conn.execute("PRAGMA synchronous=NORMAL")
            self.conn.executescript(SCHEMA)
        self._once: set[tuple] = set()

    def close(self) -> None:
        self.conn.close()

    def _skip_write(self, event: str, processing_key: str | None = None, detail: str | None = None) -> bool:
        """True when this store is read-only; the write is recorded in memory only."""
        if self.read_only:
            self.shadow_log.append((event, processing_key, detail))
            return True
        return False

    # --- provider lease (B-4) -------------------------------------------------

    def check_provider(self, provider: str, mode: str) -> None:
        """LIVE: this provider must be the only active one. SHADOW: no writes."""
        if mode not in ("LIVE", "SHADOW"):
            raise ValueError(f"unknown provider mode {mode!r}")
        if mode == "SHADOW":
            # SHADOW starts before the database is migrated, so the lease table may not exist yet.
            return
        row = self.conn.execute("SELECT provider FROM provider_lease WHERE id=1").fetchone()
        if row is None:
            self.conn.execute("BEGIN IMMEDIATE")
            try:
                self.conn.execute(
                    "INSERT INTO provider_lease (id, provider, epoch, updated_at) VALUES (1, ?, 1, ?)",
                    (provider, _now()),
                )
                self.conn.execute(
                    "INSERT INTO provider_history (ts, from_provider, to_provider, epoch) VALUES (?, NULL, ?, 1)",
                    (_now(), provider),
                )
                self.conn.execute("COMMIT")
            except Exception:
                self.conn.execute("ROLLBACK")
                raise
            return
        if row[0] != provider:
            raise ProviderConflict(f"active provider is {row[0]!r}; {provider!r} may not run LIVE")

    def switch_provider(self, from_provider: str, to_provider: str, *, hold_pending: bool = False) -> int:
        """Cutover or rollback. Refused unless from_provider is the active one,
        no job is in flight, and the leaving provider has no unsettled backlog.
        hold_pending=True keeps that backlog untouched under its own scope and
        records exactly which ids were held. Returns the new epoch."""
        if self.read_only:
            raise ProviderConflict("a read-only store cannot switch providers")
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            row = self.conn.execute("SELECT provider, epoch FROM provider_lease WHERE id=1").fetchone()
            if row is None or row[0] != from_provider:
                raise ProviderConflict(f"active provider is not {from_provider!r}")
            busy = self.conn.execute(
                "SELECT COUNT(*) FROM jobs WHERE state IN (?, ?)", IN_FLIGHT,
            ).fetchone()[0]
            if busy:
                raise ProviderConflict(f"{busy} job(s) in flight; switch refused")
            backlog = self.list_pending(from_provider)
            if backlog and not hold_pending:
                raise ProviderConflict(
                    f"{len(backlog)} unsettled pending request(s) for {from_provider!r}; "
                    "settle them or switch with hold_pending=True")
            epoch = row[1] + 1
            now = _now()
            if backlog:
                self.conn.execute(
                    "INSERT INTO audit_log (ts, event, processing_key, detail) VALUES (?, ?, NULL, ?)",
                    (now, "PENDING_HELD", f"{from_provider}: {', '.join(backlog)}"),
                )
            self.conn.execute(
                "UPDATE provider_lease SET provider=?, epoch=?, updated_at=? WHERE id=1",
                (to_provider, epoch, now),
            )
            self.conn.execute(
                "INSERT INTO provider_history (ts, from_provider, to_provider, epoch) VALUES (?, ?, ?, ?)",
                (now, from_provider, to_provider, epoch),
            )
            self.conn.execute("COMMIT")
        except Exception:
            self.conn.execute("ROLLBACK")
            raise
        return epoch

    def check_trust_version(self, version: int) -> None:
        """Rollback protection for the trust root: a lower version than the highest
        one ever accepted is refused. A read-only store compares but never records."""
        from .approval import TrustRootError

        current = self.get_counter("trust_root_version")
        if version < current:
            raise TrustRootError(f"TRUST_ROOT_ROLLBACK: version {version} is lower than accepted {current}")
        if version > current and not self.read_only:
            self.increment_counter("trust_root_version", version - current)

    def check_time_ratchet(self, provider_epoch_seconds: int, max_back_seconds: int = 300) -> None:
        """The provider's clock must not run backwards. A high-water mark of the provider time is kept,
        so an attacker who controls the clock source cannot bring an expired approval back to life.
        A read-only store compares but never records."""
        from .approval import ClockUntrusted

        current = self.get_counter("provider_time_epoch")
        if provider_epoch_seconds < current - max_back_seconds:
            raise ClockUntrusted("provider clock moved backwards")
        if provider_epoch_seconds > current and not self.read_only:
            self.increment_counter("provider_time_epoch", provider_epoch_seconds - current)

    # --- claims and sealing after a crash (B-3) ---------------------------------

    _CLAIMABLE = ("DISCOVERED", "WAIT_INPUT", "VALIDATED", "AUTH_REQUIRED")

    def try_claim(self, processing_key: str) -> bool:
        """Atomic compare-and-set into CLAIMED: exactly one process wins a never-dispatched job. Two `scan`
        processes (or a scan beside a running watch) used to both read VALIDATED and both start the reviewer
        because the old claim was an unconditional UPDATE after a plain read. One UPDATE ... WHERE state IN
        (never dispatched) is a single SQLite write transaction, so the loser sees rowcount 0 and must not dispatch.
        A read-only (SHADOW) store never claims."""
        if self._skip_write("TRY_CLAIM", processing_key, None):
            return False
        marks = ",".join("?" for _ in self._CLAIMABLE)
        cur = self.conn.execute(
            f"UPDATE jobs SET state='CLAIMED', updated_at=?, last_error=NULL, attempt_count=attempt_count+1 "
            f"WHERE processing_key=? AND state IN ({marks})",
            (_now(), processing_key, *self._CLAIMABLE),
        )
        return cur.rowcount == 1

    def record_claim(self, processing_key: str) -> None:
        if self._skip_write("CLAIM_OWNER", processing_key, None):
            return
        self.conn.execute(
            "INSERT OR REPLACE INTO job_claims (processing_key, owner, claimed_at) VALUES (?, ?, ?)",
            (processing_key, self.owner, _now()),
        )

    def seal_interrupted(self, *, exclusive: bool) -> int:
        """Jobs left CLAIMED or REVIEW_RUNNING by a process that is no longer
        running become REVIEW_UNCERTAIN. Nothing is re-run.

        Only sealed when exclusive is True, meaning the caller holds the watcher
        lock and therefore no other watcher can still be inside a model call.
        Rows claimed by this same process are never touched. Runs at most once
        per store instance."""
        if self.sealed_at_open:
            return 0
        if self.read_only:
            self.sealed_at_open = True
            return 0
        if not exclusive:
            self.log_event_once("SEAL_SKIPPED", detail="watcher lock not held; in-flight jobs left untouched")
            return 0
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            rows = self.conn.execute(
                "SELECT j.processing_key FROM jobs j "
                "LEFT JOIN job_claims c ON c.processing_key = j.processing_key "
                "WHERE j.state IN (?, ?) AND (c.owner IS NULL OR c.owner <> ?)",
                (*IN_FLIGHT, self.owner),
            ).fetchall()
            now = _now()
            for (key,) in rows:
                self.conn.execute(
                    "UPDATE jobs SET state=?, updated_at=?, last_error=? WHERE processing_key=?",
                    (JobState.REVIEW_UNCERTAIN.value, now,
                     "sealed at startup: the previous process ended during a model call; no model call was made",
                     key),
                )
                self.conn.execute(
                    "INSERT INTO audit_log (ts, event, processing_key, detail) VALUES (?, ?, ?, ?)",
                    (now, "REVIEW_UNCERTAIN", key, "sealed at startup after an interrupted model call"),
                )
            self.conn.execute("COMMIT")
        except Exception:
            self.conn.execute("ROLLBACK")
            raise
        self.sealed_at_open = True
        return len(rows)

    # --- jobs -----------------------------------------------------------

    def get_job(self, processing_key: str) -> JobRecord | None:
        with closing(self.conn.execute(
            "SELECT processing_key, request_id, request_revision, package_sha256, "
            "state, created_at, updated_at, attempt_count, last_error, result_path "
            "FROM jobs WHERE processing_key = ?",
            (processing_key,),
        )) as cur:
            row = cur.fetchone()
        if row is None:
            return None
        return JobRecord(
            processing_key=row[0],
            request_id=row[1],
            request_revision=row[2],
            package_sha256=row[3],
            state=JobState(row[4]),
            created_at=row[5],
            updated_at=row[6],
            attempt_count=row[7],
            last_error=row[8],
            result_path=row[9],
        )

    def create_job(
        self,
        processing_key: str,
        request_id: str,
        request_revision: str,
        package_sha256: str,
        state: JobState,
    ) -> None:
        if self._skip_write("CREATE_JOB", processing_key, state.value):
            return
        now = _now()
        self.conn.execute(
            "INSERT OR IGNORE INTO jobs "
            "(processing_key, request_id, request_revision, package_sha256, state, "
            "created_at, updated_at, attempt_count) VALUES (?, ?, ?, ?, ?, ?, ?, 0)",
            (processing_key, request_id, request_revision, package_sha256, state.value, now, now),
        )

    def update_job_state(
        self,
        processing_key: str,
        state: JobState,
        last_error: str | None = None,
        result_path: str | None = None,
        bump_attempt: bool = False,
    ) -> None:
        if self._skip_write("JOB_STATE", processing_key, state.value):
            return
        now = _now()
        if bump_attempt:
            self.conn.execute(
                "UPDATE jobs SET state=?, updated_at=?, last_error=?, "
                "result_path=COALESCE(?, result_path), attempt_count=attempt_count+1 "
                "WHERE processing_key=?",
                (state.value, now, last_error, result_path, processing_key),
            )
        else:
            self.conn.execute(
                "UPDATE jobs SET state=?, updated_at=?, last_error=?, "
                "result_path=COALESCE(?, result_path) WHERE processing_key=?",
                (state.value, now, last_error, result_path, processing_key),
            )

    def jobs_in_states(self, states: list[JobState]) -> list[JobRecord]:
        placeholders = ",".join("?" for _ in states)
        with closing(self.conn.execute(
            f"SELECT processing_key FROM jobs WHERE state IN ({placeholders})",
            [s.value for s in states],
        )) as cur:
            keys = [r[0] for r in cur.fetchall()]
        return [j for k in keys if (j := self.get_job(k)) is not None]

    def find_logical_job(self, request_id: str, request_revision: str, package_sha256: str) -> JobRecord | None:
        """Policy-independent duplicate lookup (B-5). The processing key keeps
        its local_policy_revision suffix for compatibility, so a policy change
        yields a new key; this finds the earlier job for the same request
        revision and package, preferring COMPLETED."""
        with closing(self.conn.execute(
            "SELECT processing_key FROM jobs WHERE request_id=? AND request_revision=? AND package_sha256=? "
            "ORDER BY CASE state WHEN 'COMPLETED' THEN 0 ELSE 1 END, updated_at DESC LIMIT 1",
            (request_id, request_revision, package_sha256),
        )) as cur:
            row = cur.fetchone()
        return self.get_job(row[0]) if row else None

    def job_for_other_package(self, request_id: str, request_revision: str, package_sha256: str) -> JobRecord | None:
        """A revision that is already bound to a different package (T08)."""
        with closing(self.conn.execute(
            "SELECT processing_key FROM jobs WHERE request_id=? AND request_revision=? AND package_sha256<>? LIMIT 1",
            (request_id, request_revision, package_sha256),
        )) as cur:
            row = cur.fetchone()
        return self.get_job(row[0]) if row else None

    # --- rolling 24 h usage, for the unattended ceilings --------------------------

    @staticmethod
    def _cutoff(hours: float) -> str:
        from datetime import timedelta

        return (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()

    def dispatches_since(self, hours: float = 24) -> int:
        with closing(self.conn.execute(
            "SELECT COUNT(*) FROM audit_log WHERE event='REVIEW_DISPATCHED' AND ts >= ?", (self._cutoff(hours),)
        )) as cur:
            return cur.fetchone()[0]

    def spend_since(self, hours: float = 24) -> float:
        """Sum of recorded model costs. A dispatch without a recorded cost (crash,
        timeout, CLI failure) counts at its cap, so a failing loop cannot spend
        unseen money."""
        import json

        cutoff = self._cutoff(hours)
        with closing(self.conn.execute(
            "SELECT event, processing_key, detail FROM audit_log "
            "WHERE event IN ('REVIEW_DISPATCHED', 'REVIEW_COST') AND ts >= ? ORDER BY id", (cutoff,)
        )) as cur:
            rows = cur.fetchall()
        capped: dict[str, float] = {}
        cost: dict[str, float] = {}
        for event, key, detail in rows:
            try:
                data = json.loads(detail or "{}")
            except ValueError:
                continue
            if event == "REVIEW_DISPATCHED":
                capped[key] = float(data.get("max_budget_usd") or 0.0)
            elif data.get("total_cost_usd") is not None:
                cost[key] = float(data["total_cost_usd"])
        return sum(cost.get(k, cap) for k, cap in capped.items()) + sum(v for k, v in cost.items() if k not in capped)

    # --- cursors ----------------------------------------------------------

    def get_cursor(self, name: str) -> str | None:
        with closing(self.conn.execute(
            "SELECT cursor_value FROM cursors WHERE name=?", (name,)
        )) as cur:
            row = cur.fetchone()
        return row[0] if row else None

    def set_cursor(self, name: str, value: str) -> None:
        if self._skip_write("CURSOR", None, name):
            return
        self.conn.execute(
            "INSERT INTO cursors (name, cursor_value, updated_at) VALUES (?, ?, ?) "
            "ON CONFLICT(name) DO UPDATE SET cursor_value=excluded.cursor_value, "
            "updated_at=excluded.updated_at",
            (name, value, _now()),
        )

    # --- pending requests -----------------------------------------------------

    # Pending ids are scoped per provider without a schema change: the legacy
    # Dropbox scope keeps bare ids, any other scope stores "<scope>:<id>". Request
    # ids are plain names ([A-Za-z0-9._-]) and never contain ':'. A scan of one
    # provider therefore cannot see, consume or delete another provider's backlog (C-1).
    pending_scope = "dropbox"

    def _pending_key(self, request_id: str, scope: str | None = None) -> str:
        scope = scope or self.pending_scope
        return request_id if scope == "dropbox" else f"{scope}:{request_id}"

    def add_pending(self, request_id: str, reason: str | None = None) -> None:
        if self._skip_write("PENDING", request_id, reason):
            return
        self.conn.execute(
            "INSERT INTO pending_requests (request_id, reason, updated_at) VALUES (?, ?, ?) "
            "ON CONFLICT(request_id) DO UPDATE SET reason=excluded.reason, updated_at=excluded.updated_at",
            (self._pending_key(request_id), reason, _now()),
        )

    def remove_pending(self, request_id: str) -> None:
        if self._skip_write("PENDING_REMOVE", request_id, None):
            return
        self.conn.execute("DELETE FROM pending_requests WHERE request_id=?", (self._pending_key(request_id),))

    def list_pending(self, scope: str | None = None) -> list[str]:
        scope = scope or self.pending_scope
        with closing(self.conn.execute("SELECT request_id FROM pending_requests ORDER BY request_id")) as cur:
            keys = [r[0] for r in cur.fetchall()]
        if scope == "dropbox":
            return [k for k in keys if ":" not in k]
        prefix = f"{scope}:"
        return [k[len(prefix):] for k in keys if k.startswith(prefix)]

    def reconciliation_manifest(self) -> dict:
        """Counts and ids per provider scope plus job states. Nothing is read
        from the network and nothing is changed."""
        with closing(self.conn.execute("SELECT request_id FROM pending_requests")) as cur:
            keys = [r[0] for r in cur.fetchall()]
        scopes: dict[str, list[str]] = {}
        for key in keys:
            scope, _, rid = key.rpartition(":") if ":" in key else ("dropbox", "", key)
            scopes.setdefault(scope.split(":")[0] if scope else "dropbox", []).append(rid)
        with closing(self.conn.execute("SELECT state, COUNT(*) FROM jobs GROUP BY state")) as cur:
            jobs = dict(cur.fetchall())
        lease = self.conn.execute("SELECT provider, epoch FROM provider_lease WHERE id=1").fetchone() \
            if self._table_exists("provider_lease") else None
        return {"pending": {s: sorted(ids) for s, ids in sorted(scopes.items())}, "jobs": jobs,
                "lease": {"provider": lease[0], "epoch": lease[1]} if lease else None}

    def _table_exists(self, name: str) -> bool:
        return self.conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (name,)).fetchone() is not None

    # --- audit log ----------------------------------------------------------

    def log_event(self, event: str, processing_key: str | None = None, detail: str | None = None) -> None:
        if self._skip_write(event, processing_key, detail):
            return
        self.conn.execute(
            "INSERT INTO audit_log (ts, event, processing_key, detail) VALUES (?, ?, ?, ?)",
            (_now(), event, processing_key, detail),
        )

    def log_event_once(self, event: str, processing_key: str | None = None, detail: str | None = None) -> bool:
        """Like log_event, but a repeat of the exact same (event, key, detail)
        within one process lifetime is not written again. A request that is
        re-evaluated every poll while it waits for its READY would otherwise
        add the same WAIT_INPUT row every 30 seconds."""
        marker = (event, processing_key, detail)
        if marker in self._once:
            return False
        if len(self._once) >= self._ONCE_LIMIT:
            self._once.clear()
        self._once.add(marker)
        self.log_event(event, processing_key=processing_key, detail=detail)
        return True

    def recent_events(self, limit: int = 50) -> list[tuple]:
        with closing(self.conn.execute(
            "SELECT ts, event, processing_key, detail FROM audit_log ORDER BY id DESC LIMIT ?",
            (limit,),
        )) as cur:
            return cur.fetchall()

    # --- counters ----------------------------------------------------------

    def increment_counter(self, name: str, by: int = 1) -> int:
        if self._skip_write("COUNTER", None, name):
            return self.get_counter(name)
        self.conn.execute(
            "INSERT INTO counters (name, value) VALUES (?, ?) "
            "ON CONFLICT(name) DO UPDATE SET value = value + excluded.value",
            (name, by),
        )
        return self.get_counter(name)

    def get_counter(self, name: str) -> int:
        with closing(self.conn.execute("SELECT value FROM counters WHERE name=?", (name,))) as cur:
            row = cur.fetchone()
        return row[0] if row else 0
