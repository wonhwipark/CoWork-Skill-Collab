"""Read-only, no-LLM detector for newly matched review results in dashboard snapshots.

No host/watcher calls, repository writes, GitHub API, or notifications are made.
The PRIVATE GitHub Actions job summary is the only optional output.
A single cycle is REQUEST -> Claude review -> GPT disposition; never re-review.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

SCHEMA = "COWORK_GITHUB_DASHBOARD_SHADOW_V4"
ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,100}\Z")
COMPLETE_STAGES = {"GPT_NOT_OBSERVED", "GPT_RECORDED_UNAUTHENTICATED", "GPT_DISPOSITION_MISMATCH"}
EXPECTED_FLAGS = {"request", "ready", "review", "receipt", "gpt"}
MAX_SIZE = 4_000_000


def _validated_chains(snapshot: object) -> dict[str, dict]:
    """Reject partial/invalid snapshot data; a forged status is not an approval."""
    if not isinstance(snapshot, dict) or snapshot.get("schema") != SCHEMA:
        raise ValueError("invalid dashboard snapshot schema")
    chains = snapshot.get("review_chains")
    if not isinstance(chains, list) or len(chains) > 300:
        raise ValueError("invalid review chains")
    result = {}
    for item in chains:
        if not isinstance(item, dict):
            raise ValueError("invalid review chain item")
        rid, flags, stage = item.get("id"), item.get("flags"), item.get("stage")
        if not isinstance(rid, str) or ID_RE.fullmatch(rid) is None or rid in result:
            raise ValueError("invalid or duplicate review ID")
        if not isinstance(flags, dict) or set(flags) != EXPECTED_FLAGS or any(type(x) is not bool for x in flags.values()):
            raise ValueError("invalid review completion flags")
        if not isinstance(stage, str) or len(stage) > 80:
            raise ValueError("invalid review stage")
        # The upstream read-only review_chain.inspect() validates pinned request,
        # READY, RESULT and RECEIPT; do not treat a status string alone as proof.
        if flags["receipt"] and not all(flags[k] for k in ("request", "ready", "review")):
            raise ValueError("receipt without matching review/request/READY")
        if flags["gpt"] and not flags["receipt"]:
            raise ValueError("GPT disposition without matching receipt")
        if stage == "GPT_NOT_OBSERVED" and (not flags["receipt"] or flags["gpt"]):
            raise ValueError("inconsistent pending disposition stage")
        if stage == "GPT_RECORDED_UNAUTHENTICATED" and not flags["gpt"]:
            raise ValueError("inconsistent recorded disposition stage")
        result[rid] = item
    return result


def newly_pending(previous: object, current: object) -> list[str]:
    """Emit only a NEW, complete reviewer result awaiting the single GPT decision."""
    old = _validated_chains(previous)
    now = _validated_chains(current)
    pending = []
    for rid, item in sorted(now.items()):
        if item["stage"] != "GPT_NOT_OBSERVED" or not item["flags"]["receipt"]:
            continue
        before = old.get(rid)
        # Never re-notify a completed result, even after unrelated commits,
        # workflow retries, or a later GPT decision.
        if before is not None and before["flags"]["receipt"]:
            continue
        pending.append(rid)
    return pending


def _read_json(path: Path) -> object:
    if path.is_symlink() or not path.is_file() or path.stat().st_size > MAX_SIZE:
        raise ValueError("invalid dashboard snapshot file")
    return json.loads(path.read_text(encoding="utf-8"))


def summary(ids: list[str]) -> str:
    lines = ["### Review completion detector (PRIVATE / no model calls)", "",
             "GitHub document fields matched; **approval signatures and Windows execution are not verified here**.",
             "One cycle = REQUEST → Claude review (once) → GPT disposition. No retry or automatic model call.", ""]
    if not ids:
        lines.append("No newly completed review awaiting GPT disposition.")
    else:
        for rid in ids:
            url = ("https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/"
                   f"collab/reviews/{rid}/REVIEW_RESULT_1.md")
            lines.append(f"- **GPT 판정 필요:** [{rid}]({url}) — 결과·영수증 문서 일치")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--previous", type=Path, required=True)
    parser.add_argument("--current", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()
    report = summary(newly_pending(_read_json(args.previous), _read_json(args.current)))
    # This file is PRIVATE GitHub Actions' job summary, not a Telegram send.
    with args.summary.open("a", encoding="utf-8") as fh:
        fh.write(report)
    print("Review completion summary generated (zero model calls)")


if __name__ == "__main__":
    main()
