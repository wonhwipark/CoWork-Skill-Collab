"""work_writer v2 (Work-side, NOT part of the watcher ZIP; v1 stays published unchanged). Changes required by the GPT decision of 2026-11-20:
 1. cas_two_wave: bounded idempotent caller rule. Wave 1 = cas_update (<= 1 + 3 PUT attempts). Only on CasExhausted (stale sha) ONE more wave with a
    fresh fetch and jitter (total <= 8 attempts). Anything else (auth, readback mismatch, semantic conflict, bad merge) is NEVER re-called.
    Both waves exhausted -> POST_CONFLICT_PENDING with evidence; the caller continues with other Works. No last-writer-wins, no force, no model call.
 2. cas_update readback tolerates GitHub's short read-after-write staleness (re-GET a few times before ReadbackMismatch).
 3. tracker_merge_strict: if another writer changed the same Work's phase/next_action since this writer read it, and the value differs from ours,
    it is NEEDS_DECISION, never an overwrite.
 4. GhContents: the real GitHub adapter (gh api). 409/422 -> Conflict. Only get() is exercised live; put() is tested through an injected fake runner.
 5. reconcile_uncertain: the processing-key policy revision is no longer hard coded. Jobs are found by (request_id, revision, package sha) under ANY
    policy revision, evidence must match the exact key it settles, and READ-ONLY / no model call is unchanged."""
from __future__ import annotations

import base64
import hashlib
import json
import random
import sqlite3
import subprocess
import time
from collections import Counter
from dataclasses import dataclass

from work_writer import (CasExhausted, CasResult, Conflict, MockContents, ReadbackMismatch, blob_sha, current_merge,  # noqa: F401
                         merge3, plan_after_uncertain, tracker_merge)


class NeedsDecision(Exception):
    """Two writers disagree about the same Work state: a human/GPT decision, never an automatic overwrite."""


class TransportError(Exception):
    pass


def cas_update(client, path, merge, *, max_retries=3, backoff=0.0, sleep=time.sleep, readback_retries=3, readback_wait=0.0) -> CasResult:
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
        for k in range(readback_retries + 1):
            got, _ = client.get(path)
            try:
                contained = got == new or merge(got) == got
            except (ValueError, KeyError):                 # content our merge cannot even read is not our write
                contained = False
            if contained:
                return CasResult(path, attempt, conflicts, new_sha, True)
            if k < readback_retries and readback_wait:
                sleep(readback_wait)
        raise ReadbackMismatch(path)
    raise CasExhausted(f"{path}: {conflicts} stale-sha conflicts")


@dataclass
class TwoWaveResult:
    status: str                 # DONE | UNCHANGED | POST_CONFLICT_PENDING
    waves: int
    attempts: int
    conflicts: int
    sha: str | None
    evidence: str = ""


def cas_two_wave(client, path, merge, *, jitter=(0.005, 0.03), sleep=time.sleep, rng=None, **kw) -> TwoWaveResult:
    rng = rng or random.Random()
    attempts = conflicts = 0
    for wave in (1, 2):
        try:
            r = cas_update(client, path, merge, **kw)
            attempts += r.attempts
            conflicts += r.conflicts
            return TwoWaveResult("DONE" if r.changed else "UNCHANGED", wave, attempts, conflicts, r.sha)
        except CasExhausted:
            attempts += kw.get("max_retries", 3) + 1
            conflicts += kw.get("max_retries", 3) + 1
            if wave == 1:
                sleep(rng.uniform(*jitter))
    return TwoWaveResult("POST_CONFLICT_PENDING", 2, attempts, conflicts, None, f"{path}: both waves exhausted after {attempts} stale-sha attempts")


def tracker_merge_strict(work_id: str, fields: dict, expected: dict | None):
    """expected = the values of these fields as this writer last read them (None = Work did not exist yet)."""
    base = tracker_merge(work_id, fields)

    def merge(old):
        if old and expected is not None:
            doc = json.loads(old.decode("utf-8"))
            work = next((x for x in doc["works"] if x.get("work_id") == work_id), None)
            if work is not None:
                for k, v in fields.items():
                    cur = work.get(k)
                    if k in expected and cur != expected[k] and cur != v:
                        raise NeedsDecision(f"{work_id}.{k} changed by another writer since it was read")
        return base(old)
    return merge


class GhContents:
    """Real GitHub contents adapter through the gh CLI. run(args, stdin) -> (rc, stdout_bytes, stderr_str) is injectable for tests."""

    def __init__(self, repo: str, branch: str = "main", run=None):
        self.repo, self.branch = repo, branch
        self.run = run or self._gh

    @staticmethod
    def _gh(args, stdin=None):
        r = subprocess.run(["gh", *args], input=stdin, capture_output=True)
        return r.returncode, r.stdout, r.stderr.decode("utf-8", "replace")

    def get(self, path):
        rc, out, err = self.run(["api", f"repos/{self.repo}/contents/{path}?ref={self.branch}"], None)
        if rc != 0:
            if "404" in err:
                return None, None
            raise TransportError(err[:200])
        meta = json.loads(out)
        if meta.get("encoding") == "base64" and meta.get("content") is not None and meta.get("size", 0) == len(base64.b64decode(meta["content"])):
            data = base64.b64decode(meta["content"])
        else:
            rc, blob, err = self.run(["api", f"repos/{self.repo}/git/blobs/{meta['sha']}"], None)
            if rc != 0:
                raise TransportError(err[:200])
            data = base64.b64decode(json.loads(blob)["content"])
        if blob_sha(data) != meta["sha"]:
            raise TransportError("blob sha does not match the bytes received")
        return data, meta["sha"]

    def put(self, path, data, sha, message="work writer"):
        body = {"message": message, "content": base64.b64encode(data).decode("ascii"), "branch": self.branch}
        if sha:
            body["sha"] = sha
        rc, out, err = self.run(["api", "--method", "PUT", f"repos/{self.repo}/contents/{path}", "--input", "-"], json.dumps(body).encode("utf-8"))
        if rc != 0:
            if "409" in err or "422" in err:
                raise Conflict(path)
            raise TransportError(err[:200])
        return json.loads(out)["content"]["sha"]


def reconcile_uncertain(db_path: str, remote_get, rid: str, rev: str, zip_sha: str) -> dict:
    """Read-only. The policy revision is taken from the DB row, not assumed."""
    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        rows = con.execute("SELECT processing_key, state FROM jobs WHERE request_id=? AND request_revision=? AND package_sha256=? ORDER BY processing_key",
                           (rid, rev, zip_sha)).fetchall()
        dispatch = {k: Counter(e for (e,) in con.execute("SELECT event FROM audit_log WHERE processing_key=?", (k,)))["REVIEW_DISPATCHED"] for k, _ in rows}
    finally:
        con.close()
    out = {"request_id": rid, "revision": rev, "keys": [k for k, _ in rows], "policy_revisions": [k.split("|")[-1] for k, _ in rows],
           "dispatch_events_total": sum(dispatch.values()), "model_calls_started_by_reconcile": 0}
    if not rows:
        return {**out, "verdict": "NO_JOB_HOLD"}
    uncertain = [k for k, s in rows if s == "REVIEW_UNCERTAIN"]
    if not uncertain:
        return {**out, "verdict": "NOT_UNCERTAIN", "db_states": [s for _, s in rows]}
    if len(uncertain) > 1:
        return {**out, "verdict": "AMBIGUOUS_POLICY_REVISION_HOLD", "uncertain_keys": uncertain}
    key = uncertain[0]
    out["processing_key"] = key
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
