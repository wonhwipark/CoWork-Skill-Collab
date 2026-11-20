"""Work-side writer helpers for the five-window case. NOT part of the watcher ZIP; the watcher's create-only upload is untouched.

1. cas_update: GET latest blob sha -> merge -> PUT with sha -> readback, at most max_retries retries after a stale-sha conflict.
   The merge functions are idempotent, so a repeated or lost-response write never duplicates an entry.
2. merge3 / apply_modification: serial per-skill rebase of modifications that were all made from the same base revision.
   Only non-overlapping changes are merged; an overlap is NEEDS_DECISION and nothing is written.
3. reconcile_uncertain: READ-ONLY cross-check of one UNCERTAIN job against the host DB (opened mode=ro) and remote result/receipt bytes.
   It never changes the DB and never calls a model.
"""
from __future__ import annotations

import difflib
import hashlib
import json
import sqlite3
import threading
import time
from collections import Counter
from dataclasses import dataclass, field


class Conflict(Exception):
    """GitHub 409/422: the supplied blob sha is stale (or the file already exists)."""


class CasExhausted(Exception):
    pass


class ReadbackMismatch(Exception):
    pass


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()


class MockContents:
    """In-memory GitHub Contents API with real sha semantics (PUT of an existing path needs the current sha)."""

    def __init__(self):
        self.files: dict[str, bytes] = {}
        self.lock = threading.Lock()
        self.puts = 0
        self.conflicts = 0

    def get(self, path):
        with self.lock:
            data = self.files.get(path)
        return (None, None) if data is None else (data, blob_sha(data))

    def put(self, path, data, sha, message=""):
        with self.lock:
            cur = self.files.get(path)
            if cur is None:
                if sha is not None:
                    self.conflicts += 1
                    raise Conflict(path)
            elif sha != blob_sha(cur):
                self.conflicts += 1
                raise Conflict(path)
            self.files[path] = data
            self.puts += 1
            return blob_sha(data)


@dataclass
class CasResult:
    path: str
    attempts: int
    conflicts: int
    sha: str | None
    changed: bool


def cas_update(client, path, merge, *, max_retries=3, backoff=0.0, sleep=time.sleep) -> CasResult:
    conflicts = 0
    for attempt in range(1, max_retries + 2):
        old, sha = client.get(path)
        new = merge(old)
        if new == old:
            return CasResult(path, attempt, conflicts, sha, False)
        try:
            new_sha = client.put(path, new, sha)
        except Conflict:
            conflicts += 1
            if backoff:
                sleep(backoff * attempt)
            continue
        got, _ = client.get(path)
        if got != new and merge(got) != got:        # a later writer may already have advanced it; our entry must still be inside
            raise ReadbackMismatch(path)
        return CasResult(path, attempt, conflicts, new_sha, True)
    raise CasExhausted(f"{path}: {conflicts} stale-sha conflicts")


def current_merge(header: str, marker: str, entry: str):
    def merge(old):
        text = (old or b"").decode("utf-8")
        if marker in text:
            return old
        if not text:
            text = header
        if not text.startswith(header):
            raise ValueError("CURRENT.md header changed")
        return (header + entry + text[len(header):]).encode("utf-8")
    return merge


def tracker_merge(work_id: str, fields: dict):
    def merge(old):
        doc = json.loads(old.decode("utf-8")) if old else {"schema": "COWORK_WORK_TRACKER_V1", "works": []}
        work = next((w for w in doc["works"] if w.get("work_id") == work_id), None)
        if work is None:
            doc["works"].append({"work_id": work_id, **fields})
        elif all(work.get(k) == v for k, v in fields.items()):
            return old
        else:
            work.update(fields)
        return (json.dumps(doc, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    return merge


# ---------------------------------------------------------------------------------------------------------------------------------
def merge3(base: str, head: str, mine: str) -> tuple[str | None, bool]:
    """Line based three-way merge. Returns (merged, conflict). Overlapping or touching changes are a conflict."""
    if head == base:
        return mine, False
    if mine == base or mine == head:
        return head, False
    b, h, m = (x.splitlines(keepends=True) for x in (base, head, mine))

    def hunks(other):
        ops = difflib.SequenceMatcher(None, b, other, autojunk=False).get_opcodes()
        return [(i1, i2, tuple(other[j1:j2])) for tag, i1, i2, j1, j2 in ops if tag != "equal"]

    hh, mh = hunks(h), hunks(m)
    for a1, a2, at in hh:
        for b1, b2, bt in mh:
            if (a1, a2, at) == (b1, b2, bt):
                continue
            if a1 < b2 and b1 < a2:
                return None, True
            if a1 == a2 and a1 in (b1, b2):
                return None, True
            if b1 == b2 and b1 in (a1, a2):
                return None, True
    merged = sorted(set(hh) | set(mh), key=lambda x: (x[0], x[1]))
    out, pos = [], 0
    for i1, i2, new in merged:
        out.extend(b[pos:i1])
        out.extend(new)
        pos = i2
    out.extend(b[pos:])
    return "".join(out), False


def tree_sha(files: dict[str, str]) -> str:
    h = hashlib.sha256()
    for path in sorted(files):
        h.update(f"{path}\0{hashlib.sha256(files[path].encode('utf-8')).hexdigest()}\n".encode("utf-8"))
    return h.hexdigest()


@dataclass
class SkillRepo:
    files: dict[str, str]
    rev: int = 1
    history: dict[int, dict[str, str]] = field(default_factory=dict)
    lock: threading.Lock = field(default_factory=threading.Lock)

    def __post_init__(self):
        self.history[self.rev] = dict(self.files)

    def commit(self, files: dict[str, str]) -> int:
        self.rev += 1
        self.files = dict(files)
        self.history[self.rev] = dict(files)
        return self.rev


@dataclass
class Modification:
    mid: str
    base_rev: int
    changes: dict[str, str]


@dataclass
class Pinned:
    mid: str
    rev: int
    sha: str
    snapshot: dict[str, str]


def apply_modification(repo: SkillRepo, mod: Modification, regression, pins: dict[str, Pinned]) -> dict:
    """Serial per skill: latest head is re-read under the lock, only non-overlapping changes are merged, the relevant regression runs on the
    merged tree BEFORE it is committed and pinned for a review REQUEST. Any conflict writes nothing."""
    with repo.lock:
        head, base = dict(repo.files), repo.history[mod.base_rev]
        merged, rebased = dict(head), False
        for path, new in mod.changes.items():
            res, conflict = merge3(base.get(path, ""), head.get(path, ""), new)
            if conflict:
                return {"mid": mod.mid, "status": "NEEDS_DECISION", "path": path, "head_rev": repo.rev, "written": False}
            if head.get(path, "") != base.get(path, ""):
                rebased = True
            merged[path] = res
        ok, why = regression(merged)
        if not ok:
            return {"mid": mod.mid, "status": "REGRESSION_FAILED", "why": why, "head_rev": repo.rev, "written": False}
        rev = repo.commit(merged)
        pin = Pinned(mod.mid, rev, tree_sha(merged), dict(merged))
        pins[mod.mid] = pin
        return {"mid": mod.mid, "status": "REBASED" if rebased else "APPLIED", "head_rev": rev, "candidate_sha": pin.sha, "written": True}


def pins_unchanged(pins: dict[str, Pinned]) -> bool:
    return all(tree_sha(p.snapshot) == p.sha for p in pins.values())


# ---------------------------------------------------------------------------------------------------------------------------------
def reconcile_uncertain(db_path: str, remote_get, rid: str, rev: str, zip_sha: str) -> dict:
    """Read-only. remote_get(path) -> bytes | None. Returns a verdict; never writes the DB, never starts a review."""
    key = f"{rid}|{rev}|{zip_sha}|1"
    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        row = con.execute("SELECT state FROM jobs WHERE processing_key=?", (key,)).fetchone()
        events = Counter(e for (e,) in con.execute("SELECT event FROM audit_log WHERE processing_key=?", (key,)))
    finally:
        con.close()
    out = {"processing_key": key, "db_state": row[0] if row else None, "dispatch_events": events["REVIEW_DISPATCHED"], "model_calls_started_by_reconcile": 0}
    if row is None:
        return {**out, "verdict": "NO_JOB_HOLD"}
    if row[0] != "REVIEW_UNCERTAIN":
        return {**out, "verdict": "NOT_UNCERTAIN"}
    result = remote_get(f"reviews/{rid}/REVIEW_RESULT_{rev}.md")
    receipt = remote_get(f"receipts/{rid}/RECEIPT_{rev}.md")
    out["remote_result_sha256"] = hashlib.sha256(result).hexdigest() if result else None
    out["remote_receipt_sha256"] = hashlib.sha256(receipt).hexdigest() if receipt else None
    if not (result and receipt):
        return {**out, "verdict": "PARTIAL_EVIDENCE_HOLD" if (result or receipt) else "UNCERTAIN_HOLD"}
    try:
        rc = json.loads(receipt.decode("utf-8"))
    except ValueError:
        return {**out, "verdict": "PARTIAL_EVIDENCE_HOLD", "why": "receipt not JSON"}
    text = result.decode("utf-8", "replace")
    good = (rc.get("ok") is True and rc.get("processing_key") == key and rc.get("request_id") == rid and rc.get("package_sha256") == zip_sha
            and f'review_id: "{key}"' in text and f'package_sha256: "{zip_sha}"' in text)
    return {**out, "verdict": "SETTLED_BY_EVIDENCE" if good else "EVIDENCE_MISMATCH_HOLD"}


def plan_after_uncertain(windows: list[dict], verdicts: dict[str, str]) -> dict[str, str]:
    """Per window status. Only later windows of the SAME skill wait behind an unsettled UNCERTAIN window; everything else proceeds."""
    status, blocked_skills = {}, set()
    for w in windows:
        v = verdicts.get(w["id"])
        if w["skill"] in blocked_skills:
            status[w["id"]] = "WAIT_DEPENDENCY"
        elif v in ("UNCERTAIN_HOLD", "PARTIAL_EVIDENCE_HOLD", "EVIDENCE_MISMATCH_HOLD", "NO_JOB_HOLD"):
            status[w["id"]] = "UNCERTAIN_HOLD"
            blocked_skills.add(w["skill"])
        else:
            status[w["id"]] = "PROCEED"
    return status
