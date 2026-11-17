#!/usr/bin/env python3
"""Byte-pinned v0.2.25 development builder: cost-only per-review budgets.

No change to Windows LIVE, its protected delegation, DB, keys or tasks.
Source v0.2.24 is pinned and immutable. CI runs in isolated Linux temp dir.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import re
import stat
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

BASE = "collab/projects/COWORK-AUTO-APPROVAL-20261115-001/candidates/skill-collab-watcher_v0_2_24_1117.zip"
BASE_SHA = "3c78699b734d88202a34ef5fd430f5f278ab1692a437b6affb6b6c64d24ca360"
OUT = "skill-collab-watcher_v0_2_25_1117.zip"


def replace_one(path: Path, before: str, after: str) -> None:
    src = path.read_text(encoding="utf-8")
    count = src.count(before)
    if count != 1:
        raise RuntimeError(f"PATCH_ANCHOR_COUNT {path} {count} for {before[:120]!r}")
    path.write_text(src.replace(before, after), encoding="utf-8", newline="\n")


def safe_extract(source: Path, root: Path) -> None:
    if hashlib.sha256(source.read_bytes()).hexdigest() != BASE_SHA:
        raise RuntimeError("PINNED_SOURCE_SHA256_MISMATCH")
    with zipfile.ZipFile(source) as z:
        if z.testzip() is not None:
            raise RuntimeError("SOURCE_ZIP_CRC_FAILED")
        seen: set[str] = set()
        for item in z.infolist():
            p = PurePosixPath(item.filename)
            if (not item.filename or item.filename.startswith("/")
                or "\\" in item.filename or ".." in p.parts
                or item.filename in seen
                or stat.S_IFMT(item.external_attr >> 16) == stat.S_IFLNK):
                raise RuntimeError("UNSAFE_ZIP_MEMBER: " + item.filename)
            seen.add(item.filename)
        z.extractall(root)


def apply(root: Path) -> None:
    pkg = root / "skill_collab_watcher"
    pure = pkg / "auto_policy.py"
    replace_one(pure, "    max_request_cents: int = 100\n",
                "    max_request_cents: int = 150  # legacy scope; protected local value may raise to 300\n")
    replace_one(pure, "    max_day_cents: int = 300\n", "    max_day_cents: int = 0   # retained only for legacy compatibility\n")
    replace_one(pure, "    max_month_cents: int = 1000\n", "    max_month_cents: int = 0   # retained only for legacy compatibility\n")
    replace_one(pure,
        '    if c.policy != "POLICY-STATIC-V1" or c.max_calls != 1 or c.attempt != 1:',
        '    if c.policy not in ("POLICY-STATIC-V1", "POLICY-STATIC-V1-DESIGN") or c.max_calls != 1 or c.attempt != 1:')
    replace_one(pure,
        '    if (d.max_request_cents > 100 or d.max_day_cents > 300 or d.max_month_cents > 1000):\n        return False, "UNSUPPORTED_DELEGATION_LIMIT"',
        '    if not (1 <= d.max_request_cents <= 10000):\n        return False, "UNSUPPORTED_DELEGATION_LIMIT"')
    replace_one(pure, '''    # Day call counts remain telemetry only; monetary ceilings decide admission.
    if e.day_cents_used_or_reserved + c.estimated_cents > d.max_day_cents:
        return False, "DAY_COST_LIMIT"
    if e.month_cents_used_or_reserved + c.estimated_cents > d.max_month_cents:
        return False, "MONTH_COST_LIMIT"
''',
        '''    # Day/month counts and costs are telemetry, NOT admissibility gates.
    # The protected local per-request cap and one-shot identity remain enforced.
''')
    approver = pkg / "auto_approval.py"
    replace_one(approver,
        'f"limits: per request {d.max_request_cents} c, day {d.max_day_cents} c, month {d.max_month_cents} c"',
        'f"limit: per review {d.max_request_cents} c; no daily/monthly aggregate limits"')
    replace_one(approver,
        'max_request_cents=_cents(raw.get("max_request_usd", 1.0), "max_request_usd"), max_day_calls=0,\n            max_day_cents=_cents(raw.get("max_day_usd", 3.0), "max_day_usd"), max_month_cents=_cents(raw.get("max_month_usd", 10.0), "max_month_usd"),',
        'max_request_cents=_cents(raw.get("max_request_usd", 1.5), "max_request_usd"), max_day_calls=0,\n            max_day_cents=0, max_month_cents=0,  # old day/month keys ignored')
    # Catch malformed protected config before any signing; forbid NaN or inf.
    replace_one(approver,
        '    if isinstance(value, bool) or not isinstance(value, (int, float)) or value <= 0:\n        raise ValueError(f"{name} must be a positive number")',
        '    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:\n        raise ValueError(f"{name} must be a finite positive number")')
    s = approver.read_text(encoding="utf-8")
    if "import math\n" not in s:
        # Preserve imports at the module header without restructuring.
        s = "import math\n" + s if not s.startswith("from __future__") else s.replace(
            "from __future__ import annotations\n", "from __future__ import annotations\nimport math\n", 1)
        approver.write_text(s, encoding="utf-8", newline="\n")
    store = pkg / "state_store.py"
    before = '''            usage = self._auto_usage_locked(now, exclude=(request_id, revision))
            verdict = None
            # Deprecated max_day_calls parameter is intentionally ignored.
            if usage["day_cents"] + cents > max_day_cents:
                verdict = "DAY_COST_LIMIT"
            elif usage["month_cents"] + cents > max_month_cents:
                verdict = "MONTH_COST_LIMIT"
            if verdict:
                self.conn.execute("ROLLBACK")
                return verdict
'''
    after = '''            # No day/month cumulative quota. Keep the same transaction/unique key.
            # Existing reservation rows remain intact as immutable history.
            if not isinstance(cents, int) or isinstance(cents, bool) or cents <= 0:
                self.conn.execute("ROLLBACK")
                return "INVALID_COST"
'''
    replace_one(store, before, after)
    replace_one(store,
        '        Returns CLAIMED, EXISTS, DAY_COST_LIMIT, MONTH_COST_LIMIT or READ_ONLY.',
        '        Returns CLAIMED, EXISTS, INVALID_COST or READ_ONLY. Aggregate quotas removed.')
    cfg = pkg / "config.py"
    replace_one(cfg, "    max_budget_usd: float | None = 1.0\n",
                "    max_budget_usd: float | None = 1.5\n")
    replace_one(cfg, 'max_budget_usd=_check_budget(rp.get("max_budget_usd", 1.0)),',
                'max_budget_usd=_check_budget(rp.get("max_budget_usd", 1.5)),')
    replace_one(cfg,
        '    if isinstance(value, bool) or not isinstance(value, (int, float)) or not value > 0:\n        raise ConfigError(f"{name} must be a number greater than 0 or null, got {value!r}")',
        '    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:\n        raise ConfigError(f"{name} must be a finite number greater than 0 or null, got {value!r}")')
    replace_one(cfg,
        '            if isinstance(amount, bool) or not isinstance(amount, (int, float)) or not amount > 0:',
        '            if isinstance(amount, bool) or not isinstance(amount, (int, float)) or not math.isfinite(amount) or not amount > 0:')
    replace_one(cfg,
        '    if isinstance(value, bool) or not isinstance(value, (int, float)) or not value > 0:',
        '    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not value > 0:')
    replace_one(cfg,
        '            daily_budget_usd=_optional_cap(rp.get("daily_budget_usd"), "review_policy.daily_budget_usd", float),\n            max_dispatches_per_day=_optional_cap(rp.get("max_dispatches_per_day"),\n                                                 "review_policy.max_dispatches_per_day", int),',
        '            daily_budget_usd=None,  # legacy setting ignored: aggregate cap abolished\n            max_dispatches_per_day=None,  # legacy setting ignored: call-count cap abolished')
    s = cfg.read_text(encoding="utf-8")
    if "import math\n" not in s:
        s = s.replace("import json\n", "import json\nimport math\n", 1)
        cfg.write_text(s, encoding="utf-8", newline="\n")

    # Existing non-automatic watcher has a separate rolling 24h admission gate.
    # It too must become inert; requests still use a mandatory per-run max budget.
    orch = pkg / "orchestrator.py"
    s = orch.read_text(encoding="utf-8")
    start = s.find("def _check_ceilings(")
    end = s.find("\ndef _process_request_group(", start)
    if start < 0 or end < 0:
        raise RuntimeError("ORCHESTRATOR_CEILING_ANCHOR_MISSING")
    s = s[:start] + '''def _check_ceilings(store: StateStore, policy: LocalPolicy, final: ValidationResult) -> GroupResult | None:
    """Aggregate review-count and cost ceilings intentionally abolished."""
    return None

''' + s[end:]
    orch.write_text(s, encoding="utf-8", newline="\n")
    replace_one(orch,
        '''    claim = store.claim(final.processing_key, max_dispatches=policy.max_dispatches_per_day,
                        daily_budget_usd=policy.daily_budget_usd,
                        this_run_usd=policy.run_budgets_usd.get(str(final.fields["request"]["run_policy_ref"]), 0.0))''',
        '''    claim = store.claim(final.processing_key)  # only atomic exactly-once; no aggregate quotas''')
    replace_one(orch,
        '''    if claim == "COUNT_CEILING":
        store.log_event_once("DAILY_LIMIT_BLOCKED", processing_key=final.processing_key,
                             detail="daily review count ceiling reached (reserved atomically); the request stays pending")
        return GroupResult(retry=True)
    if claim == "BUDGET_CEILING":
        store.log_event_once("DAILY_BUDGET_BLOCKED", processing_key=final.processing_key,
                             detail="daily spending ceiling reached (reserved atomically); the request stays pending")
        return GroupResult(retry=True)
''', '')
    # Keep the old method's signature for migrations but disable the aggregate checks.
    s = store.read_text(encoding="utf-8")
    start = s.find('            if max_dispatches is not None or daily_budget_usd is not None:\n')
    end = s.find('            cur = self.conn.execute(\n', start)
    if start < 0 or end < 0:
        raise RuntimeError("STORE_CEILING_ANCHOR_MISSING")
    s = s[:start] + '            # Legacy max_dispatches/daily_budget_usd are inert.\n' + s[end:]
    store.write_text(s, encoding="utf-8", newline="\n")

    # Increment only package-owned version metadata, never historical receipts.
    for name in ("skill_collab_watcher/__init__.py", "docs/CUTOVER_RUNBOOK.md"):
        f = root / name
        if f.is_file():
            old = f.read_text(encoding="utf-8")
            if name.endswith("__init__.py"):
                if "0.2.24" not in old:
                    raise RuntimeError("VERSION_IN_INIT_NOT_FOUND")
                new = old.replace("0.2.24", "0.2.25")
            else:
                new = old.replace("Cutover runbook: Dropbox to GitHub (v0.2.24,",
                                  "Cutover runbook: Dropbox to GitHub (v0.2.25,")
                if new == old:
                    raise RuntimeError("VERSION_IN_RUNBOOK_NOT_FOUND")
            f.write_text(new, encoding="utf-8", newline="\n")
    doc = root / "docs" / "BUDGET_POLICY_CONFIGURATION.md"
    doc.write_text('''# Per-review budget policy (v0.2.25 development)

Current requested defaults: skill review USD 1.50; design review USD 3.00.
No daily/monthly cost or count ceilings. Do not auto-upgrade a request.

Configure the existing local reviewer.config.json review_policy block:
  "max_budget_usd": 1.5,
  "known_run_policy_refs": {
    "POLICY-STATIC-V1": {"max_budget_usd": 1.5},
    "POLICY-STATIC-V1-DESIGN": {"max_budget_usd": 3.0}
  },
  "daily_budget_usd": null,
  "max_dispatches_per_day": null

Existing protected delegation JSON must explicitly permit USD 3.00:
  "policy": "POLICY-STATIC-V1",
  "max_request_usd": 3.0

The request names only run_policy_ref, never the price. Both tiers require
the pre-existing permitted project/skill and valid SOURCE_PIN/signature/READY.
Design tier is available only when the local config explicitly lists its name,
and the protected delegation permits its price. Do not silently convert an
unapproved request from BASIC to DESIGN. The existing max_request_usd=1.0
continues to deny higher budget requests until authorized host changes.

Only change the two local values via the existing protected policy process;
ensure new settings, SHA pins, backup/rollback, and Windows host regression.
The published ZIP and this document do not install or activate LIVE settings.
Legacy max_day_usd/max_month_usd/max_day_calls keys are accepted but ignored.
Existing UNCERTAIN requests remain permanently claimed; history is preserved.
''', encoding="utf-8")
    # Execute postcondition checks against source, not deployment.
    policy = pure.read_text(encoding="utf-8")
    state = store.read_text(encoding="utf-8")
    assert '"DAY_COST_LIMIT"' not in policy + state
    assert '"MONTH_COST_LIMIT"' not in policy + state
    assert '"DAY_CALL_LIMIT"' not in policy + state
    assert "PRIMARY KEY (request_id, revision)" in state and "BEGIN IMMEDIATE" in state
    assert 'c.max_calls != 1 or c.attempt != 1' in policy
    assert '"POLICY-STATIC-V1-DESIGN"' in policy
    assert '"--max-budget-usd"' in (pkg / "review_runner.py").read_text(encoding="utf-8")


def make_zip(root: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED, compresslevel=8) as z:
        for f in sorted(root.rglob("*")):
            if not f.is_file() or "__pycache__" in f.parts or f.suffix == ".pyc":
                continue
            info = zipfile.ZipInfo(f.relative_to(root).as_posix(), date_time=(2026, 11, 17, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, f.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=8)
    with zipfile.ZipFile(dest) as z:
        assert z.testzip() is None and len(z.namelist()) == len(set(z.namelist()))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--out", type=Path, required=True)
    a = parser.parse_args()
    source = a.repo.resolve() / BASE
    with tempfile.TemporaryDirectory(prefix="cowork-v025-") as temp:
        root = Path(temp)
        safe_extract(source, root)
        apply(root)
        # Add regression tests before building ZIP so installed bytes have tests.
        from patch_v025_budget_tests import patch_tests
        patch_tests(root)
        out = a.out.resolve() / OUT
        make_zip(root, out)
        print(json.dumps({
            "candidate": str(out), "sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
            "bytes": out.stat().st_size,
            "base_sha256": BASE_SHA, "release": "DEVELOPMENT_NOT_FOR_DEPLOYMENT"
        }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
