"""기존 watcher StateStore를 재사용하는 읽기 전용 pending 정산.

운영 설치/DB/승인/READY를 변경하거나 리뷰를 실행하지 않는다.
현재 REQUEST의 id/revision/ZIP SHA가 일치할 때만 완료 이력을 분리한다.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib
import json
from pathlib import Path
import re
import sqlite3
import sys

NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")
DIGEST = re.compile(r"[0-9a-f]{64}\Z")
HELD_STATES = {
    "CLAIMED", "REVIEW_RUNNING", "REVIEW_UNCERTAIN", "FAILED", "CONFLICT",
    "REJECTED", "RESULT_SAVED", "UPLOAD_PENDING",
}
KNOWN_STATES = HELD_STATES | {"COMPLETED", "DISCOVERED", "WAIT_INPUT", "VALIDATED", "AUTH_REQUIRED"}


def _request(root: Path, rid: str, parse_front_matter):
    """원문과 서명은 출력하지 않고 현재 입력의 식별값과 해시만 반환."""
    if not NAME.fullmatch(rid):
        return None, "UNSAFE_REQUEST_ID"
    path = (root / rid / "REQUEST.md").resolve()
    if not path.is_relative_to(root):
        return None, "REQUEST_OUTSIDE_ROOT"
    try:
        if path.stat().st_size > 262144:
            return None, "REQUEST_TOO_LARGE"
        raw = path.read_bytes()
        if raw.startswith(b"\xef\xbb\xbf"):
            return None, "REQUEST_BOM"
        front = parse_front_matter(raw.decode("utf-8"))
    except Exception as exc:  # untrusted text/parser failures stay unverified; never print the text
        return None, type(exc).__name__
    rev, digest = front.get("request_revision"), front.get("package_sha256")
    if (front.get("schema") != "SKILL_COLLAB_REVIEW_REQUEST_V1"
            or str(front.get("request_id")) != rid or isinstance(rev, bool)
            or not NAME.fullmatch(str(rev or "")) or not isinstance(digest, str)
            or not DIGEST.fullmatch(digest)):
        return None, "REQUEST_IDENTITY_INVALID"
    return {
        "request_revision": str(rev), "package_sha256": digest,
        "request_sha256": hashlib.sha256(raw).hexdigest(),
    }, None


def _claims(store, rid):
    if not store._table_exists("auto_claims"):
        return []
    return [dict(zip(("request_revision", "package_sha256", "stage", "attempts"), row))
            for row in store.conn.execute(
                "SELECT revision, package_sha256, stage, attempts FROM auto_claims "
                "WHERE request_id=? ORDER BY revision", (rid,))]


def _row(store, scope, rid, input_scope, root, parse_front_matter):
    ident, error = _request(root, rid, parse_front_matter) if scope == input_scope else (None, "OTHER_PROVIDER_SCOPE")
    jobs = [dict(zip(("request_revision", "package_sha256", "state", "attempt_count"), row))
            for row in store.conn.execute(
                "SELECT request_revision, package_sha256, state, attempt_count "
                "FROM jobs WHERE request_id=? ORDER BY request_revision, package_sha256, state", (rid,))]
    # auto_claims has no provider key: never attribute those claims to another scope.
    claims = _claims(store, rid) if scope == input_scope else []
    out = {"scope": scope, "request_id": rid, "identity": ident,
           "identity_error": error, "jobs": jobs, "auto_claims": claims,
           "manual_signing_admission": "NOT_ASSESSED", "requeue_allowed": False}
    if ident is None:
        out["category"] = "HELD" if any(c["stage"] == "UNCERTAIN" for c in claims) else "UNVERIFIED"
        return out
    rev, digest = ident["request_revision"], ident["package_sha256"]
    same_rev_jobs = [j for j in jobs if j["request_revision"] == rev]
    exact_jobs = [j for j in same_rev_jobs if j["package_sha256"] == digest]
    exact_claims = [c for c in claims if c["request_revision"] == rev]
    conflict = (any(j["package_sha256"] != digest for j in same_rev_jobs)
                or any(c["package_sha256"] != digest for c in exact_claims))
    held = (conflict or any(j["state"] in HELD_STATES or j["state"] not in KNOWN_STATES for j in exact_jobs)
            or any(c["stage"] not in ("READY_POSTED",) for c in exact_claims))
    if held:
        out["category"] = "HELD"
    elif any(j["state"] == "COMPLETED" for j in exact_jobs):
        out["category"] = "COMPLETED"
    else:
        out["category"] = "WAITING"
    prefix = f"{rid}|{rev}|{digest}|"
    if store._table_exists("audit_log"):
        out["recorded_execution_events"] = dict(store.conn.execute(
            "SELECT event, COUNT(*) FROM audit_log WHERE substr(processing_key, 1, ?)=? "
            "AND event IN ('REVIEW_DISPATCHED', 'REVIEW_COST', 'REVIEW_UNCERTAIN') GROUP BY event",
            (len(prefix), prefix)))
    return out


def audit(store, request_root: Path, scope: str, parse_front_matter):
    """하나의 SQLite 읽기 스냅샷. 어떠한 분류도 실행/서명 승인은 아님."""
    if not store.read_only or store.conn.in_transaction:
        raise ValueError("a fresh read-only StateStore is required")
    root = request_root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError("request root must be a directory")
    store.conn.execute("BEGIN")
    try:
        manifest = store.reconciliation_manifest()
        rows = [_row(store, provider, rid, scope, root, parse_front_matter)
                for provider, ids in manifest["pending"].items() for rid in ids]
        counts = {}
        for provider in manifest["pending"]:
            selected = [row for row in rows if row["scope"] == provider]
            values = {label.lower(): sum(row["category"] == label for row in selected)
                      for label in ("COMPLETED", "HELD", "WAITING", "UNVERIFIED")}
            values["tracked_total"] = len(selected)
            values["unresolved_total"] = len(selected) - values["completed"]
            counts[provider] = values
        return {
            "mode": "READ_ONLY", "model_execution": "NOT_RUN", "automatic_requeue": False,
            "request_source": "LOCAL_BYTES_REMOTE_FRESHNESS_NOT_VERIFIED",
            "counts": counts, "requests": rows,
            "limits": ["완료=현재 로컬 REQUEST 식별값과 일치하는 로컬 완료 이력",
                       "WAITING은 실행 가능 판정이 아님", "실행 이벤트 부재만으로 과거 유료 호출 0을 증명하지 않음",
                       "UNCERTAIN은 보존; 별도 호스트 정산·유효 승인·공식 signer 검증 필요"],
        }
    finally:
        store.conn.execute("ROLLBACK")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--watcher-root", type=Path, required=True)
    parser.add_argument("--db", type=Path, required=True)
    parser.add_argument("--requests-root", type=Path, required=True)
    parser.add_argument("--scope", choices=("github", "dropbox"), required=True)
    args = parser.parse_args(argv)
    store = None
    try:
        root = args.watcher_root.resolve(strict=True)
        db = args.db.resolve(strict=True)
        args.requests_root.resolve(strict=True)
        if not db.is_file() or not (root / "skill_collab_watcher/state_store.py").is_file():
            raise ValueError("existing watcher root and database are required")
        sys.path.insert(0, str(root))
        state = importlib.import_module("skill_collab_watcher.state_store")
        validator = importlib.import_module("skill_collab_watcher.validator")
        if not Path(state.__file__).resolve().is_relative_to(root):
            raise ValueError("imported StateStore is outside watcher root")
        store = state.StateStore(db, read_only=True)
        result = audit(store, args.requests_root, args.scope, validator.parse_front_matter)
        result["state_store_sha256"] = hashlib.sha256(Path(state.__file__).read_bytes()).hexdigest()
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except (OSError, ValueError, ImportError, sqlite3.Error) as exc:
        print(f"BLOCKED: {type(exc).__name__}; no state or approval changed", file=sys.stderr)
        return 2
    finally:
        if store is not None:
            store.close()


if __name__ == "__main__":
    raise SystemExit(main())
