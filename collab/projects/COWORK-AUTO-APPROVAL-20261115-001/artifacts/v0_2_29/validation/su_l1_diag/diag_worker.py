"""Diagnostic worker: identical to su_l1/ledger_worker_r0003.py for op=nonce, but _read_anchor is replaced by an
instrumented copy with the SAME semantics. Before raising ContractError it appends the original exception
(type, errno, winerror, stage) and the calling frames to <anchor>.diag.jsonl. Non-production, temp extraction only."""
import json
import os
import sys
import time
import traceback

PKG = sys.argv[7]
sys.path.insert(0, os.path.join(PKG, "su_l1"))
import local_only_contract_r0003 as c  # noqa: E402

op, db, anchor, key, start = sys.argv[1:6]
logfile = sys.argv[6]


def record(stage, exc):
    frames = [f.name for f in traceback.extract_stack()][-6:]
    with open(logfile, "a", encoding="utf-8") as fh:
        fh.write(json.dumps({"pid": os.getpid(), "stage": stage, "type": type(exc).__name__,
                             "errno": getattr(exc, "errno", None), "winerror": getattr(exc, "winerror", None),
                             "msg": str(exc)[:120], "frames": frames}) + "\n")


def diag_read_anchor(path):
    stage = "open"
    try:
        with open(path, "r", encoding="utf-8") as fh:
            stage = "json"
            data = json.load(fh)
        stage = "shape"
        if set(data) != {"genesis", "seq", "head"} or not isinstance(data["seq"], int):
            raise ValueError
        return data
    except (OSError, ValueError, TypeError) as exc:
        record(stage, exc)
        raise c.ContractError("ANCHOR_UNREADABLE_FAIL_CLOSED") from None


c._read_anchor = diag_read_anchor
deadline = time.monotonic() + 30
while not os.path.exists(start) and time.monotonic() < deadline:
    time.sleep(0.002)
try:
    c.Ledger.open(db, anchor).consume_nonce(key, "REQ-" + key)
    print("OK")
except c.ContractError as err:
    print("ERR", err)
