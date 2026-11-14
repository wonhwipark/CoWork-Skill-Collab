from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path


def default_local_root() -> Path:
    base = os.environ.get("LOCALAPPDATA") or str(Path.home() / "AppData" / "Local")
    return Path(base) / "skill-collab-watcher"


class ConfigError(ValueError):
    """The config file is present but a value cannot be trusted."""


def _strict_bool(value, name: str, default: bool) -> bool:
    """Only JSON true/false are accepted.

    bool("false") is True in Python, so coercing would let a quoted value
    switch model-calling reviews on. A wrong type stops the program instead.
    """
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    raise ConfigError(f"{name} must be a JSON true/false, got {value!r}")


EFFORT_LEVELS = ("low", "medium", "high", "xhigh", "max")   # as printed by `claude --help`
CACHE_TTLS = ("1h", "5m")


def _check_effort(value, name: str) -> str | None:
    if value is None:
        return None
    if value not in EFFORT_LEVELS:
        raise ConfigError(f"{name} must be one of {list(EFFORT_LEVELS)} or null, got {value!r}")
    return value


def _positive_int(value, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ConfigError(f"{name} must be a positive integer, got {value!r}")
    return value


@dataclass
class ReviewPolicy:
    enabled: bool = False
    dry_run: bool = True
    concurrent_reviews: int = 1
    model: str | None = None
    allowed_tools: list[str] = field(default_factory=lambda: ["Read", "Grep", "Glob"])
    max_budget_usd: float | None = 1.0
    timeout_sec: int = 1800
    known_run_policy_refs: list[str] = field(default_factory=list)
    run_budgets: dict[str, float] = field(default_factory=dict)
    run_efforts: dict[str, str] = field(default_factory=dict)
    effort: str | None = None            # default reasoning effort; null = whatever the user's Claude settings say
    prompt_cache_ttl: str = "1h"         # "5m" makes cache writes cost 37.5% less (measured 2026-11-04)
    save_transcript: bool = False        # keep the CLI's per-turn stream on this PC only, for cost analysis
    enabled_source: str = "default (off)"
    daily_budget_usd: float | None = None      # unattended spending ceiling over any rolling 24 h; null = off
    max_dispatches_per_day: int | None = None  # unattended review-count ceiling over any rolling 24 h; null = off
    usage_limit_wait_sec: int = 1800
    usage_limit_max_wait_sec: int = 86400
    usage_limit_max_deferrals: int = 12

    @property
    def dispatch_allowed(self) -> bool:
        """The only condition under which a claude process may be started."""
        return self.enabled and not self.dry_run

    def budget_for(self, run_policy_ref: str) -> float | None:
        """Per-run spending cap. A REQUEST can only pick one of the locally
        registered tiers by name; it can never state an amount itself."""
        return self.run_budgets.get(run_policy_ref, self.max_budget_usd)

    def effort_for(self, run_policy_ref: str) -> str | None:
        return self.run_efforts.get(run_policy_ref, self.effort)


def _parse_run_policy_refs(value) -> tuple[list[str], dict[str, float], dict[str, str]]:
    """`known_run_policy_refs` is either a list of names (all use
    `max_budget_usd`) or an object
    {name: {"max_budget_usd": number, "effort": "low|medium|high|xhigh|max"}}."""
    if value is None:
        return [], {}, {}
    if isinstance(value, list):
        if not all(isinstance(v, str) and v for v in value):
            raise ConfigError("review_policy.known_run_policy_refs list must contain non-empty strings")
        return list(value), {}, {}
    if not isinstance(value, dict):
        raise ConfigError("review_policy.known_run_policy_refs must be a list of names or an object")
    budgets: dict[str, float] = {}
    efforts: dict[str, str] = {}
    for name, spec in value.items():
        if not name or not isinstance(spec, dict):
            raise ConfigError(f"run policy {name!r} must be an object such as {{\"max_budget_usd\": 3.0}}")
        unknown = set(spec) - {"max_budget_usd", "effort"}
        if unknown:
            raise ConfigError(f"run policy {name!r} has unknown keys {sorted(unknown)}")
        if "max_budget_usd" in spec:
            amount = spec["max_budget_usd"]
            if isinstance(amount, bool) or not isinstance(amount, (int, float)) or not amount > 0:
                raise ConfigError(f"run policy {name!r}: max_budget_usd must be a number greater than 0")
            budgets[name] = float(amount)
        if spec.get("effort") is not None:
            efforts[name] = _check_effort(spec["effort"], f"run policy {name!r}: effort")
    return list(value), budgets, efforts


def _optional_cap(value, name: str, kind):
    """null/absent = no ceiling. A present value must be a number greater than 0:
    0 or a quoted string must stop the program, never silently disable the cap."""
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not value > 0:
        raise ConfigError(f"{name} must be a number greater than 0 or null, got {value!r}")
    if kind is int and int(value) != value:
        raise ConfigError(f"{name} must be a whole number, got {value!r}")
    return kind(value)


def _check_budget(value) -> float:
    """A missing/null cap would start reviews with no spending limit."""
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not value > 0:
        raise ConfigError(f"review_policy.max_budget_usd must be a number greater than 0, got {value!r}")
    return float(value)


def _resolve_enabled(raw: dict, rp: dict) -> tuple[bool, str]:
    """`review_policy.enabled` is the contract (README + shipped configs).

    A top-level `enabled` is what the first implementation actually read, so
    it stays accepted as a legacy alias with the same meaning: permission to
    dispatch reviews. Neither key means "run the watcher": watching is only
    started by hand. If both are present and disagree, reviews stay off.
    """
    nested = _strict_bool(rp.get("enabled"), "review_policy.enabled", default=False) if "enabled" in rp else None
    legacy = _strict_bool(raw.get("enabled"), "enabled", default=False) if "enabled" in raw else None
    if nested is not None and legacy is not None and nested != legacy:
        return False, (
            f"CONFLICT (review_policy.enabled={str(nested).lower()}, "
            f"top-level enabled={str(legacy).lower()}) -> off"
        )
    if nested is not None:
        return nested, "review_policy.enabled"
    if legacy is not None:
        return legacy, "top-level enabled (legacy alias)"
    return False, "default (off)"


@dataclass
class Config:
    schema_version: int
    example_only: bool
    baseline_id: str
    remote_root: str
    transport: str
    local_state_dir: str
    poll_interval_sec: int
    longpoll_timeout_sec: int
    review_policy: ReviewPolicy
    claude_executable: str | None
    python_executable: str | None
    raw: dict
    provider_mode: str = "LIVE"          # LIVE or SHADOW (read-only); see StateStore.check_provider
    github_repo: str | None = None       # owner/name of the PRIVATE collaboration repository
    github_branch: str = "main"
    github_token_file: str | None = None  # path only; the file is read at use and never printed
    trust_root_file: str | None = None    # path only; approval trust root kept outside the repository
    trust_root_sha256: str | None = None  # pins the exact bytes of the trust root file
    trust_root_independence: str = "enforce"  # enforce | warn: the watcher's own account must not be able to change the trust root
    shadow_state_dir: str | None = None   # SHADOW's own folder (database, lock, runs); required for provider_mode SHADOW
    shadow_account_isolation: str = "warn"  # enforce: refuse to start when this account can reach the live folder
    config_path: str | None = None        # where this config was loaded from (its permissions matter for the pin)

    @property
    def state_dir(self) -> Path:
        p = Path(self.local_state_dir)
        p.mkdir(parents=True, exist_ok=True)
        return p

    @classmethod
    def load(cls, path: str | Path) -> "Config":
        # utf-8-sig: Windows PowerShell 5.1 and Notepad write a BOM, which
        # plain utf-8 rejects with an unreadable JSON error.
        try:
            raw = json.loads(Path(path).read_text(encoding="utf-8-sig"))
        except json.JSONDecodeError as exc:
            raise ConfigError(f"{path} is not valid JSON: {exc}") from exc
        if not isinstance(raw, dict):
            raise ConfigError(f"{path} must contain a JSON object")
        rp = raw.get("review_policy") or {}
        enabled, enabled_source = _resolve_enabled(raw, rp)
        run_refs, run_budgets, run_efforts = _parse_run_policy_refs(rp.get("known_run_policy_refs"))
        ttl = rp.get("prompt_cache_ttl", "1h")
        if ttl not in CACHE_TTLS:
            raise ConfigError(f"review_policy.prompt_cache_ttl must be one of {list(CACHE_TTLS)}, got {ttl!r}")
        policy = ReviewPolicy(
            enabled=enabled,
            enabled_source=enabled_source,
            dry_run=_strict_bool(rp.get("dry_run"), "review_policy.dry_run", default=True),
            concurrent_reviews=int(rp.get("concurrent_reviews", 1)),
            model=rp.get("model"),
            allowed_tools=list(rp.get("allowed_tools", ["Read", "Grep", "Glob"])),
            max_budget_usd=_check_budget(rp.get("max_budget_usd", 1.0)),
            timeout_sec=int(rp.get("timeout_sec", 1800)),
            known_run_policy_refs=run_refs,
            run_budgets=run_budgets,
            run_efforts=run_efforts,
            effort=_check_effort(rp.get("effort"), "review_policy.effort"),
            prompt_cache_ttl=ttl,
            save_transcript=_strict_bool(rp.get("save_transcript"), "review_policy.save_transcript", default=False),
            daily_budget_usd=_optional_cap(rp.get("daily_budget_usd"), "review_policy.daily_budget_usd", float),
            max_dispatches_per_day=_optional_cap(rp.get("max_dispatches_per_day"),
                                                 "review_policy.max_dispatches_per_day", int),
            usage_limit_wait_sec=_positive_int(rp.get("usage_limit_wait_sec", 1800), "review_policy.usage_limit_wait_sec"),
            usage_limit_max_wait_sec=_positive_int(rp.get("usage_limit_max_wait_sec", 86400), "review_policy.usage_limit_max_wait_sec"),
            usage_limit_max_deferrals=_positive_int(rp.get("usage_limit_max_deferrals", 12), "review_policy.usage_limit_max_deferrals"),
        )
        local_state_dir = raw.get("local_state_dir") or str(default_local_root())
        github = raw.get("github") or {}
        if not isinstance(github, dict):
            raise ConfigError("github must be a JSON object")
        provider_mode = raw.get("provider_mode", "LIVE")
        if provider_mode not in ("LIVE", "SHADOW"):
            raise ConfigError(f"provider_mode must be LIVE or SHADOW, got {provider_mode!r}")
        shadow = raw.get("shadow") or {}
        if not isinstance(shadow, dict):
            raise ConfigError("shadow must be a JSON object")
        shadow_dir = shadow.get("state_dir")
        if provider_mode == "SHADOW":
            if raw.get("transport", "dropbox") != "github":
                raise ConfigError("provider_mode SHADOW is only defined for transport github")
            if not isinstance(shadow_dir, str) or not shadow_dir.strip():
                raise ConfigError("provider_mode SHADOW needs shadow.state_dir: its own folder, never the live one")
        account_isolation = shadow.get("account_isolation", "warn")
        if account_isolation not in ("enforce", "warn"):
            raise ConfigError(f"shadow.account_isolation must be enforce or warn, got {account_isolation!r}")
        independence = github.get("trust_root_independence", "enforce")
        if independence not in ("enforce", "warn"):
            raise ConfigError(f"github.trust_root_independence must be enforce or warn, got {independence!r}")
        return cls(
            trust_root_independence=independence,
            shadow_state_dir=shadow_dir if isinstance(shadow_dir, str) else None,
            shadow_account_isolation=account_isolation,
            config_path=str(Path(path).resolve()),
            provider_mode=provider_mode,
            github_repo=github.get("repo"),
            github_branch=str(github.get("branch", "main")),
            github_token_file=github.get("token_file"),
            trust_root_file=github.get("trust_root_file"),
            trust_root_sha256=github.get("trust_root_sha256"),
            schema_version=int(raw.get("schema_version", 1)),
            example_only=bool(raw.get("example_only", False)),
            baseline_id=raw.get("baseline_id", "UNKNOWN"),
            remote_root=raw.get("remote_root", "/SKILL-COLLAB"),
            transport=raw.get("transport", "dropbox"),
            local_state_dir=local_state_dir,
            poll_interval_sec=int(raw.get("poll_interval_sec", 30)),
            longpoll_timeout_sec=int(raw.get("longpoll_timeout_sec", 60)),
            review_policy=policy,
            claude_executable=raw.get("claude_executable"),
            python_executable=raw.get("python_executable"),
            raw=raw,
        )
