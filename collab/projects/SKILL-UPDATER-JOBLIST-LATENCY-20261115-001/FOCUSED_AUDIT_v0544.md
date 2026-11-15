# Skill-Updater v0.5.44 dispatch and discovery — exact source excerpts

- Public ZIP; static audit only, not Linux installed files

## scripts/skill_updater.py
Source functions of interest: _github_cache_path:670, _github_cache_key:722, _load_github_cache:731, _cache_age_sec:743, _github_run_cache_key:750, _github_run_cached_value:754, _store_github_run_cached_value:759, _record_stale_cache_diagnostic:764, _github_cached_value:773, _store_github_cached_value:795, _github_request_kind:815, _record_github_request:826, github_raw_url:841, github_contents_url:1891, github_contents_listing:1918, github_release:1967, github_contents_bytes:1981, parse_root_zip_asset:2058, parse_root_zip_filename:2165, root_zip_candidate_lists:2191, select_root_zip_candidates:2229, load_root_zip_manifest:2258, _job_list_version_changed:5059, run_job_list_post_update:5071, reconcile_discovery_entry:5938, main:7556, update:490, update:561

```python
...
00035: from pathlib import Path
00036: from typing import Any, Iterable
00037:
00038: VERSION = "0.5.44"
00039: JOBLIST_ACTIVATION_EVERY_CYCLE = False  # scheduled entry only; MCP update-only
00040: JOBLIST_ROOT_ZIP_FRESH_DISCOVERY = True
00041: USER_AGENT = f"skill-updater/{VERSION}"
00042: DEFAULT_TIMEOUT = 60
00043: DEBUG_LOG_KEEP = 10
00044: MANUAL_HEARTBEAT_SEC = 5
00045: FAILURE_FINGERPRINT_SCHEMA = 1
00046: TLS_PROFILE_SCHEMA = 1
00047: TLS_VERIFY_ENV = "SKILL_UPDATER_TLS_VERIFY"
00048: TLS_PROFILE_FILENAME = "network-profile.json"
00049: GITHUB_REMOTE_CACHE_SCHEMA = 1
00050: DEFAULT_GITHUB_MIN_POLL_INTERVAL_SEC = 3600
00051: DEFAULT_GITHUB_CACHE_MAX_STALE_SEC = 86400
00052: DEFAULT_GITHUB_API_MAX_REQUESTS_PER_RUN = 3
00053: CANONICAL_RELEASE_FILES = (".skill-release.json", "VERSION", "VERSION.txt", "VERSION.md", "SKILL.md")
00054: UNATTENDED_HEARTBEAT_SEC = 15
00055: _DEBUG_STREAM_LOCK = threading.RLock()
00056: _DEBUG_LOG_HANDLE = None
00057: _DEBUG_LOG_PATH: Path | None = None
00058: DEFAULT_PRESERVE_PATHS = (
00059:     "knowledge/**", "knowledge-source/**", "sam-knowledge-source/**",
...
00486:     def start(self) -> None:
00487:         self._write(emit=False)
00488:         self._thread.start()
00489:
00490:     def update(self, stage: str, target: str | None = None, index: int | None = None,
00491:                detail: str = "", emit: bool = True, waiting_on: str = "none") -> None:
00492:         with self._lock:
00493:             if stage != self.stage:
00494:                 self.stage_started_monotonic = time.monotonic()
00495:                 self.stage_started_at = now_iso()
00496:             self.stage = stage
00497:             self.waiting_on = waiting_on
00498:             self.target = target
...
00557:     def start(self) -> None:
00558:         self._write(True)
00559:         self._thread.start()
00560:
00561:     def update(self, stage: str, detail: str) -> None:
00562:         with self._lock:
00563:             self.stage, self.detail = stage, detail
00564:         self._write(True)
00565:
00566:     def stop(self) -> None:
00567:         self._stop.set()
00568:         if self._thread.is_alive(): self._thread.join(timeout=1)
00569:
...
00574: @dataclass
00575: class Decision:
00576:     name: str
00577:     installed_version: str | None
00578:     remote_version: str | None
00579:     status: str
00580:     apply: bool = False
00581:     detail: str = ""
00582:     asset: str | None = None
00583:     sha256: str | None = None
00584:     git_blob_sha: str | None = None
00585:     installed_revision: int | None = None
00586:     remote_revision: int | None = None
...
00629:     name: str
00630:     result_status: str
00631:     decision_status: str
00632:     installed_version: str | None = None
00633:     remote_version: str | None = None
00634:     started_at: str | None = None
00635:     completed_at: str | None = None
00636:     detail: str = ""
00637:     error: str | None = None
00638:     applied: bool = False
00639:     backup: str | None = None
00640:     success_kind: str | None = None
00641:     failure_code: str | None = None
...
00666: def atomic_json(path: Path, payload: Any) -> None:
00667:     atomic_write(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
00668:
00669:
00670: def _github_cache_path(cfg: dict[str, Any]) -> Path:
00671:     return Path(cfg["download_dir"]) / "state" / "github-remote-cache.json"
00672:
00673:
00674: def _fresh_cycle_reset(cfg: dict[str, Any]) -> dict[str, Any]:
00675:     """Reset ephemeral state for a new updater cycle.
00676:
00677:     Freshness contract (v0.5.36): every cycle must re-observe GitHub before it
00678:     decides whether a registered skill is CURRENT or needs an update. The
00679:     persistent remote cache is retained only as last-known diagnostic evidence;
...
00682:     """
00683:     runtime = Path(cfg["download_dir"])
00684:     removed: list[str] = []
00685:     preserved: list[str] = []
00686:     cfg["_github_run_cache"] = {}
00687:     cfg["_github_freshness"] = {
00688:         "required": True,
00689:         "status": "PENDING",
00690:         "started_at": now_iso(),
00691:     }
00692:
00693:     staging = runtime / "staging"
00694:     if staging.exists():
...
00699:     downloads = runtime / "downloads"
00700:     downloads.mkdir(parents=True, exist_ok=True)
00701:     preserved.append(str(downloads))
00702:
00703:     cache_file = _github_cache_path(cfg)
00704:     if cache_file.exists():
00705:         preserved.append(str(cache_file))
00706:
00707:     # Stale progress is not a durable state contract. The active heartbeat will
00708:     # recreate it after the reset. Do not touch current_run/last_run/history.
00709:     progress = runtime / "state" / "current_progress.json"
00710:     if progress.exists():
00711:         progress.unlink(missing_ok=True)
...
00718:         "at": now_iso(),
00719:     }
00720:
00721:
00722: def _github_cache_key(cfg: dict[str, Any], kind: str, repo_path: str) -> str:
00723:     source = cfg.get("source") or {}
00724:     identity = "|".join([
00725:         str(source.get("repository") or ""), str(source.get("ref") or "main"),
00726:         kind, str(repo_path or "").strip("/"),
00727:     ])
00728:     return hashlib.sha256(identity.encode("utf-8")).hexdigest()
00729:
00730:
00731: def _load_github_cache(cfg: dict[str, Any]) -> dict[str, Any]:
00732:     path = _github_cache_path(cfg)
00733:     try:
00734:         data = json.loads(path.read_text(encoding="utf-8"))
00735:         if isinstance(data, dict) and data.get("schema_version") == GITHUB_REMOTE_CACHE_SCHEMA \
00736:                 and isinstance(data.get("items"), dict):
00737:             return data
00738:     except Exception:
00739:         pass
00740:     return {"schema_version": GITHUB_REMOTE_CACHE_SCHEMA, "items": {}}
00741:
00742:
00743: def _cache_age_sec(row: dict[str, Any]) -> float:
00744:     try:
00745:         return max(0.0, time.time() - float(row.get("fetched_epoch", 0)))
00746:     except Exception:
00747:         return float("inf")
00748:
00749:
00750: def _github_run_cache_key(cfg: dict[str, Any], kind: str, repo_path: str) -> str:
00751:     return _github_cache_key(cfg, kind, repo_path)
00752:
00753:
00754: def _github_run_cached_value(cfg: dict[str, Any], kind: str, repo_path: str) -> Any | None:
00755:     cache = cfg.setdefault("_github_run_cache", {})
00756:     return cache.get(_github_run_cache_key(cfg, kind, repo_path))
00757:
00758:
00759: def _store_github_run_cached_value(cfg: dict[str, Any], kind: str, repo_path: str, value: Any) -> None:
00760:     cache = cfg.setdefault("_github_run_cache", {})
00761:     cache[_github_run_cache_key(cfg, kind, repo_path)] = value
00762:
00763:
00764: def _record_stale_cache_diagnostic(cfg: dict[str, Any], kind: str, repo_path: str, value: Any | None) -> None:
00765:     if value is None:
00766:         return
00767:     rows = _transient_list(cfg, "_github_stale_cache_diagnostics")
00768:     key = f"{kind}:{repo_path or '/'}"
00769:     if key not in rows:
00770:         rows.append(key)
00771:
00772:
00773: def _github_cached_value(cfg: dict[str, Any], kind: str, repo_path: str,
00774:                          *, allow_stale: bool = False) -> Any | None:
00775:     data = _load_github_cache(cfg)
00776:     row = data.get("items", {}).get(_github_cache_key(cfg, kind, repo_path))
00777:     if not isinstance(row, dict):
00778:         return None
00779:     network = cfg.get("network") or {}
00780:     max_age = int(network.get(
00781:         "github_cache_max_stale_sec" if allow_stale else "github_min_poll_interval_sec",
00782:         DEFAULT_GITHUB_CACHE_MAX_STALE_SEC if allow_stale else DEFAULT_GITHUB_MIN_POLL_INTERVAL_SEC,
00783:     ))
00784:     if _cache_age_sec(row) > max_age:
00785:         return None
00786:     value = row.get("value")
00787:     if row.get("encoding") == "base64" and isinstance(value, str):
00788:         try:
00789:             return base64.b64decode(value.encode("ascii"))
00790:         except Exception:
00791:             return None
00792:     return value
00793:
00794:
00795: def _store_github_cached_value(cfg: dict[str, Any], kind: str, repo_path: str, value: Any) -> None:
00796:     data = _load_github_cache(cfg)
00797:     stored = value
00798:     encoding = None
00799:     if isinstance(value, (bytes, bytearray)):
00800:         stored = base64.b64encode(bytes(value)).decode("ascii")
00801:         encoding = "base64"
00802:     data.setdefault("items", {})[_github_cache_key(cfg, kind, repo_path)] = {
00803:         "kind": kind,
00804:         "repository": str((cfg.get("source") or {}).get("repository") or ""),
00805:         "ref": str((cfg.get("source") or {}).get("ref") or "main"),
00806:         "repo_path": str(repo_path or "").strip("/"),
00807:         "fetched_at": now_iso(),
00808:         "fetched_epoch": time.time(),
00809:         "encoding": encoding,
00810:         "value": stored,
00811:     }
00812:     atomic_json(_github_cache_path(cfg), data)
00813:
00814:
00815: def _github_request_kind(url: str) -> str:
00816:     host = urllib.parse.urlsplit(url).netloc.lower()
00817:     if host == "api.github.com":
00818:         return "api"
00819:     if host in {"raw.githubusercontent.com", "objects.githubusercontent.com"}:
00820:         return "raw"
...
00869: def default_main_root() -> Path:
00870:     return expand_path(default_main_root_value())
00871:
00872:
00873: def main_skill_root(main_root: Path, name: str) -> Path:
00874:     return (main_root / safe_filename(name)).resolve()
00875:
00876:
00877: def default_private_install_root_value() -> str:
00878:     explicit = os.environ.get("L1SW_PRIVATE_SKILLS_ROOT")
00879:     if explicit and explicit.strip():
00880:         return explicit.strip()
00881:     return r"%USERPROFILE%\l1sw-private-skills" if os.name == "nt" else "~/l1sw-private-skills"
...
01087:         "tls_verify": bool(tls_verify),
01088:         "route": route,
01089:         "updated_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
01090:         "updater_version": VERSION,
01091:         "source": "last-successful-github-connection",
01092:     }
01093:     comparable_previous = {k: previous.get(k) for k in ("schema_version", "tls_verify", "route", "source")}
01094:     comparable_new = {k: payload.get(k) for k in ("schema_version", "tls_verify", "route", "source")}
01095:     if comparable_previous == comparable_new:
01096:         cfg["_network_profile"] = previous
01097:         return
01098:     atomic_json(path, payload)
01099:     payload["_path"] = str(path)
...
01236:     cfg["install_root"] = str(expand_path(str(raw["install_root"]), path.parent))
01237:     cfg["output_dir"] = str(canonical_updater_output_dir(private_root))
01238:     # v0.5.28: legacy configurable job_sync remains ignored. The active runtime uses
01239:     # one fixed post-update hook: if canonical job-list is installed, invoke its
01240:     # own `activate --launch` entry once. Skill-Updater never parses job requests.
01241:     cfg.pop("job_sync", None)
01242:     _apply_persisted_network_profile(cfg)
01243:     if not read_only:
01244:         migrate_legacy_updater_runtime(cfg)
01245:     return cfg
01246:
01247: def migrate_legacy_updater_runtime(cfg: dict[str, Any]) -> dict[str, Any]:
01248:     """Missing-only reconcile from legacy updater runtime into canonical storage.
...
01314:     source = cfg.get("source")
01315:     if not isinstance(source, dict):
01316:         errors.append("source object가 필요합니다")
01317:     else:
01318:         if source.get("provider") != "github":
01319:             errors.append("source.provider는 github만 지원합니다")
01320:         repo = str(source.get("repository") or "")
01321:         if not REPO_RE.fullmatch(repo):
01322:             errors.append("source.repository는 OWNER/REPOSITORY 형식이어야 합니다")
01323:         mode = source.get("mode")
01324:         if mode not in ("auto", "release", "contents", "root-zips"):
01325:             errors.append("source.mode는 auto/release/contents/root-zips 중 하나여야 합니다")
01326:         if mode == "release" and not str(source.get("manifest_asset") or "skill-index.json"):
01327:             errors.append("release 모드에는 manifest_asset이 필요합니다")
01328:         if mode == "contents" and not str(source.get("manifest_path") or "skill-index.json"):
01329:             errors.append("contents 모드에는 manifest_path가 필요합니다")
01330:         if "allow_root_zip_discovery" in source and not isinstance(source.get("allow_root_zip_discovery"), bool):
01331:             errors.append("source.allow_root_zip_discovery는 boolean이어야 합니다")
01332:         if "zip_path" in source and not isinstance(source.get("zip_path"), str):
01333:             errors.append("source.zip_path는 문자열이어야 합니다")
01334:         if source.get("channel", "stable") not in ALLOWED_CHANNELS:
01335:             errors.append("source.channel은 stable/rc/beta/dev/all 중 하나여야 합니다")
01336:         if source.get("version_policy", "latest") not in ("latest", "manifest"):
01337:             errors.append("source.version_policy는 latest/manifest 중 하나여야 합니다")
01338:     for key in ("download_dir", "install_root"):
01339:         if not isinstance(cfg.get(key), str) or not cfg.get(key, "").strip():
...
01380:         for bool_key in ("allow_insecure_tls_fallback", "remember_successful_tls"):
01381:             if bool_key in network and not isinstance(network.get(bool_key), bool):
01382:                 errors.append(f"network.{bool_key}는 boolean이어야 합니다")
01383:         for int_key, minimum in (
01384:             ("github_min_poll_interval_sec", 0),
01385:             ("github_cache_max_stale_sec", 0),
01386:             ("github_api_max_requests_per_run", 1),
01387:         ):
01388:             if int_key in network:
01389:                 value = network.get(int_key)
01390:                 if not isinstance(value, int) or isinstance(value, bool) or value < minimum:
01391:                     errors.append(f"network.{int_key}는 {minimum} 이상의 정수여야 합니다")
01392:     preservation = cfg.get("preservation") or {}
01393:     if not isinstance(preservation, dict):
...
01408:     return errors
01409:
01410:
01411: def token_from_config(cfg: dict[str, Any]) -> str | None:
01412:     env_name = str((cfg.get("source") or {}).get("token_env") or "GITHUB_TOKEN")
01413:     return os.environ.get(env_name) or None
01414:
01415:
01416: VCS_READ_ONLY_SUBCOMMANDS = {"version", "--version", "help"}
01417: GIT_CONFIG_READ_FLAGS = {
01418:     "--get", "--get-all", "--get-regexp", "--get-urlmatch", "--list", "-l",
01419:     "--show-origin", "--show-scope", "--name-only",
01420: }
...
01914:         raise UpdateError(f"GitHub 응답이 object가 아닙니다: {url}")
01915:     return data
01916:
01917:
01918: def github_contents_listing(cfg: dict[str, Any], repo_path: str = "") -> list[dict[str, Any]]:
01919:     """Return a GitHub directory listing with per-cycle freshness.
01920:
01921:     Cross-run persistent cache is deliberately *not* consulted before the first
01922:     request of a cycle. Once a fresh response is obtained it may be memoized
01923:     inside the current cycle to avoid duplicate API calls. Persistent cache is
01924:     retained only as last-known diagnostics and is never used to decide CURRENT.
01925:     """
01926:     cache_kind = "contents-listing"
01927:     run_cached = _github_run_cached_value(cfg, cache_kind, repo_path)
01928:     if isinstance(run_cached, list):
01929:         _transient_list(cfg, "_github_run_cache_hits").append(f"{cache_kind}:{repo_path or '/'}")
01930:         return [item for item in run_cached if isinstance(item, dict)]
01931:
01932:     url = github_contents_url(cfg, repo_path)
01933:     try:
01934:         data = http_json_value(cfg, url, token_from_config(cfg))
01935:     except UpdateError as exc:
01936:         stale = _github_cached_value(cfg, cache_kind, repo_path, allow_stale=True)
01937:         _record_stale_cache_diagnostic(cfg, cache_kind, repo_path, stale)
01938:         cfg["_github_freshness"] = {
01939:             "required": True,
01940:             "status": "UNVERIFIED",
01941:             "failed_at": now_iso(),
01942:             "kind": cache_kind,
01943:             "repo_path": repo_path or "/",
01944:             "error": str(exc),
01945:             "stale_diagnostic_available": isinstance(stale, list),
01946:         }
01947:         raise UpdateError(
01948:             f"REMOTE_FRESHNESS_UNVERIFIED: GitHub 최신 목록을 새로 확인하지 못했습니다: "
01949:             f"path={repo_path or '/'}; cause={exc}"
01950:         ) from exc
01951:
01952:     if not isinstance(data, list):
01953:         raise UpdateError(f"GitHub contents 경로가 폴더가 아닙니다: {repo_path or '/'}")
01954:     rows = [item for item in data if isinstance(item, dict)]
01955:     _store_github_run_cached_value(cfg, cache_kind, repo_path, rows)
01956:     _store_github_cached_value(cfg, cache_kind, repo_path, rows)
01957:     cfg["_github_freshness"] = {
01958:         "required": True,
01959:         "status": "FRESH",
01960:         "verified_at": now_iso(),
01961:         "kind": cache_kind,
01962:         "repo_path": repo_path or "/",
01963:     }
01964:     return rows
...
01981: def github_contents_bytes(cfg: dict[str, Any], repo_path: str) -> bytes:
01982:     """Read GitHub content fresh once per updater cycle.
01983:
01984:     A successful read is memoized only for this run. Persistent cache is
01985:     diagnostic-only across cycles and is never accepted as current remote data.
01986:     """
01987:     cache_kind = "raw-content"
01988:     run_cached = _github_run_cached_value(cfg, cache_kind, repo_path)
01989:     if isinstance(run_cached, (bytes, bytearray)):
01990:         _transient_list(cfg, "_github_run_cache_hits").append(f"{cache_kind}:{repo_path}")
01991:         return bytes(run_cached)
01992:
01993:     raw_url = github_raw_url(cfg, repo_path)
01994:     try:
01995:         raw = http_bytes(cfg, raw_url, token_from_config(cfg))
01996:     except UpdateError as raw_exc:
01997:         # Corporate networks can block raw.githubusercontent.com. Fall back to
01998:         # one REST request, still protected by the per-run API budget.
01999:         url = github_contents_url(cfg, repo_path)
02000:         try:
02001:             raw = http_bytes(cfg, url, token_from_config(cfg), "application/vnd.github.raw+json")
02002:         except UpdateError as api_exc:
02003:             stale = _github_cached_value(cfg, cache_kind, repo_path, allow_stale=True)
02004:             _record_stale_cache_diagnostic(cfg, cache_kind, repo_path, stale)
02005:             cfg["_github_freshness"] = {
02006:                 "required": True,
02007:                 "status": "UNVERIFIED",
02008:                 "failed_at": now_iso(),
02009:                 "kind": cache_kind,
02010:                 "repo_path": repo_path,
02011:                 "error": f"raw={raw_exc}; api={api_exc}",
02012:                 "stale_diagnostic_available": isinstance(stale, (bytes, bytearray)),
02013:             }
02014:             raise UpdateError(
02015:                 f"REMOTE_FRESHNESS_UNVERIFIED: GitHub 최신 내용을 새로 확인하지 못했습니다: "
02016:                 f"path={repo_path}; raw={raw_exc}; api={api_exc}"
02017:             ) from api_exc
02018:         # GitHub may still return the JSON representation depending on API/proxy.
02019:         if raw[:1] == b"{":
02020:             try:
02021:                 data = json.loads(raw.decode("utf-8"))
02022:                 if isinstance(data, dict) and data.get("content"):
02023:                     raw = base64.b64decode(str(data["content"]).replace("\n", ""))
02024:             except Exception:
02025:                 pass
02026:     _store_github_run_cached_value(cfg, cache_kind, repo_path, raw)
02027:     _store_github_cached_value(cfg, cache_kind, repo_path, raw)
02028:     cfg["_github_freshness"] = {
02029:         "required": True,
02030:         "status": "FRESH",
02031:         "verified_at": now_iso(),
02032:         "kind": cache_kind,
02033:         "repo_path": repo_path,
02034:     }
02035:     return raw
...
02054:     match = re.search(r"(?:^|[-._])(alpha|beta|rc|dev|pre|preview|snapshot)(?:[.-]?\d+)?(?:$|[-+._])", value)
02055:     return _canonical_channel(match.group(1)) if match else "stable"
02056:
02057:
02058: def parse_root_zip_asset(filename: str) -> dict[str, Any] | None:
02059:     """Parse a root ZIP filename without treating dates as version fields.
02060:
02061:     The release identity is the semantic version token immediately following
02062:     ``_v``/``-v``.  Exactly ``major.minor.patch`` is consumed; arbitrary
02063:     filename suffixes (for example ``last``, dates, timestamps, timezone labels
02064:     and copy suffixes) are packaging metadata only and never participate in
02065:     semantic-version ordering.  Recognized prerelease/revision tokens remain
02066:     supported.  The downloaded package's internal release metadata remains
02067:     authoritative during validation.
02068:
02069:     Supported examples:
02070:       skill_v1_2_3_0804.zip
02071:       skill_v1_2_3_20260804.zip
02072:       skill_v1_2_3_r2_0804.zip
02073:       skill_v1_2_3_rc1_r2_20260804.zip
02074:       skill-20260804-KST_v1.2.3-beta2.zip
02075:     Missing revision means revision 1.
02076:     """
02077:     base = Path(filename).name
02078:     if not base.lower().endswith(".zip"):
02079:         return None
02080:     stem = re.sub(r"\s*\(\d+\)$", "", base[:-4]).strip()
...
04251:     extracted = work / "extract"
04252:     try:
04253:         root = safe_extract(archive, extracted)
04254:         observed_names, observed_versions, identity_warnings = validate_package_identity(
04255:             root, archive, decision.name, decision.remote_version or ""
04256:         )
04257:         package_name, package_version, name_source, version_source, metadata_diag = skill_metadata_detailed(
04258:             root, archive=archive, expected_name=decision.name, selected_version=decision.remote_version
04259:         )
04260:         metadata_diag.append("observed_names=" + json.dumps(observed_names, ensure_ascii=False, sort_keys=True))
04261:         metadata_diag.append("observed_versions=" + json.dumps(observed_versions, ensure_ascii=False, sort_keys=True))
04262:         if canonical_skill_name(package_name or "") != canonical_skill_name(decision.name):
04263:             raise ClassifiedUpdateError(
04264:                 f"패키지 이름 불일치: selected={decision.name} actual={package_name}",
04265:                 failure_code="RELEASE_IDENTITY_MISMATCH", disposition="BLOCKED", retryable=False,
04266:                 stage="PACKAGE_IDENTITY",
04267:             )
04268:         if not package_version or not same_release_version(package_version, decision.remote_version or ""):
04269:             raise ClassifiedUpdateError(
04270:                 f"패키지 버전 불일치: selected={decision.remote_version} actual={package_version}",
04271:                 failure_code="RELEASE_IDENTITY_MISMATCH", disposition="BLOCKED", retryable=False,
04272:                 stage="PACKAGE_IDENTITY",
04273:             )
04274:         # Core updater validation is intentionally limited to archive safety,
04275:         # immutable identity, version and hash. Skill runtime checks belong to
04276:         # the skill itself and must not block package installation.
04277:         return PreparedCandidate(
04278:             decision=decision, archive=str(archive), root=str(root),
...
04298: def resolve_latest_valid_manifest(cfg: dict[str, Any], manifest: dict[str, Any], release: dict[str, Any] | None,
04299:                                   selected: set[str] | None, heartbeat: ProgressHeartbeat,
04300:                                   run_id: str) -> dict[str, Any]:
04301:     """Choose highest package that passes immutable staging preflight."""
04302:     candidate_lists = dict(cfg.get("_root_zip_candidates") or {})
04303:     prepared: dict[str, PreparedCandidate] = {}
04304:     blocked: dict[str, dict[str, Any]] = {}
04305:     broken_newer: dict[str, list[dict[str, Any]]] = {}
04306:     install_root = Path(cfg["install_root"])
04307:     for target in enabled_targets(cfg):
04308:         name = target["name"]
04309:         if selected and name not in selected:
04310:             continue
...
04334:         for index, item in enumerate(items, start=1):
04335:             heartbeat.update("PREFLIGHT_CANDIDATE", name, None,
04336:                              f"후보 {index}/{len(items)} v{item.get('version')} r{item.get('revision',1)}", emit=True,
04337:                              waiting_on="package-validation")
04338:             remote_version = str(item.get("version") or "0")
04339:             remote_revision = max(1, int(item.get("revision") or 1))
04340:             repair_current = False
04341:             if local_version:
04342:                 version_cmp = compare_versions(remote_version, local_version)
04343:                 # Never downgrade. Equal versions are normally current; a forced
04344:                 # repair cycle downloads/preflights them only when the installed
04345:                 # package-owned files drift from the receipt baseline.
04346:                 if version_cmp < 0:
04347:                     chosen = item
04348:                     break
04349:                 if version_cmp == 0:
04350:                     if bool(cfg.get("_repair_current")):
...
04378:             if same_installed and not repair_current:
04379:                 chosen = item
04380:                 break
04381:             decision = Decision(
04382:                 name=name, installed_version=local_version, remote_version=str(item.get("version")),
04383:                 status="PREFLIGHT", apply=False, asset=str(item.get("asset")),
04384:                 sha256=str(item.get("sha256")) if item.get("sha256") else None,
04385:                 git_blob_sha=str(item.get("git_blob_sha")) if item.get("git_blob_sha") else None,
04386:                 remote_revision=int(item.get("revision") or 1),
04387:                 remote_channel=str(item.get("channel") or infer_channel(str(item.get("version")))),
04388:                 installed_version_source=local_version_source,
04389:                 download_url=str(item.get("download_url") or "") or None,
04390:             )
04391:             try:
04392:                 archive = download_archive(cfg, decision, release)
04393:                 prepared[name] = prepare_candidate(cfg, decision, archive, run_id)
04394:                 chosen = item
04395:                 break
...
04481:
04482:     Native installers preserve unknown files by design.  Older canonical roots can
04483:     therefore retain `.skill-release.json`/`VERSION*` that are absent from a new
04484:     package and shadow the newly installed SKILL.md.  We repair those files only
04485:     when the installed SKILL.md itself exactly matches the selected remote version.
04486:     User data and package-provided metadata are never touched.
04487:     """
04488:     if not expected_version:
04489:         return []
04490:     _sn, src_versions = package_identity_observations(package_root, None, skill_name)
04491:     _dn, dst_versions = package_identity_observations(canonical, None, skill_name)
04492:     skill_version = dst_versions.get("SKILL.md")
04493:     if not skill_version or compare_versions(skill_version, expected_version) != 0:
...
04581:                 retryable=False, stage="CANONICAL_INSTALL_VERIFY",
04582:             )
04583:
04584:         stale_meta_diag = _reconcile_stale_native_version_metadata(
04585:             root, canonical, decision.name, decision.remote_version
04586:         )
04587:         _name, observed_version, _nsrc, vsrc, diag = skill_metadata_detailed(
04588:             canonical, expected_name=decision.name
04589:         )
04590:         diag = list(stale_meta_diag) + list(diag or [])
04591:         if observed_version and decision.remote_version and not same_release_version(observed_version, decision.remote_version):
04592:             raise ClassifiedUpdateError(
04593:                 f"canonical version mismatch: expected={decision.remote_version} actual={observed_version}",
04594:                 failure_code="CANONICAL_VERSION_MISMATCH", disposition="BLOCKED",
04595:                 retryable=False, stage="CANONICAL_INSTALL_VERIFY",
04596:             )
04597:
04598:         archive_sha = decision.sha256 or prepared.archive_sha256 or sha256_file(archive)
04599:         baseline_hashes = _package_baseline_hashes(root)
04600:         _write_receipt(
04601:             cfg, decision.name, decision.remote_version or observed_version or "",
04602:             baseline_hashes, None,
04603:             revision=decision.remote_revision or 1,
04604:             channel=decision.remote_channel or infer_channel(decision.remote_version or observed_version or ""),
04605:             archive_sha256=archive_sha, git_blob_sha=decision.git_blob_sha,
04606:             installed_root=canonical,
04607:         )
04608:         return Applied(
04609:             decision.name, decision.installed_version, decision.remote_version or observed_version or "",
04610:             None, str(archive), str(entry), None, 0, 0,
04611:             old_revision=decision.installed_revision, new_revision=decision.remote_revision or 1,
04612:             config_backup=None,
04613:             main_data_root=str(canonical / "data"),
04614:             migration_report=None, migrated_files=0, migrated_tasks=[],
04615:             package_name_source=prepared.package_name_source,
04616:             package_version_source=prepared.package_version_source,
04617:             metadata_diagnostics=list(prepared.metadata_diagnostics) + [
...
04764:             raise
04765:         if old_at_install.exists(): shutil.rmtree(old_at_install, ignore_errors=True)
04766:         archive_sha = decision.sha256 or prepared.archive_sha256 or sha256_file(archive)
04767:         _write_receipt(
04768:             cfg, decision.name, decision.remote_version or "", baseline_hashes,
04769:             str(preservation_report) if preservation_report else None,
04770:             revision=decision.remote_revision or 1, channel=decision.remote_channel or infer_channel(decision.remote_version or ""),
04771:             archive_sha256=archive_sha, git_blob_sha=decision.git_blob_sha,
04772:             installed_root=target,
04773:         )
04774:         return Applied(
04775:             decision.name, decision.installed_version, decision.remote_version or "",
04776:             str(backup) if backup else None, str(archive), str(target),
04777:             str(preservation_report) if preservation_report else None, preserved_files, conflicts,
04778:             old_revision=decision.installed_revision, new_revision=decision.remote_revision or 1,
04779:             config_backup=str(config_backup) if config_backup else None,
04780:             main_data_root=str(canonical_private_skill_root(cfg, decision.name)),
04781:             migration_report=str(migration_report) if migration_report else None,
04782:             migrated_files=migrated_files, migrated_tasks=migrated_tasks,
04783:             package_name_source=prepared.package_name_source,
...
05055:         [path for path in (_DEBUG_LOG_PATH, log_root / str(cfg.get("_active_run_id") or "")) if path],
05056:     )
05057:
05058:
05059: def _job_list_version_changed(outcomes: list[TargetOutcome]) -> bool:
05060:     """Compatibility diagnostic only; activation no longer depends on this edge."""
05061:     for outcome in outcomes:
05062:         if outcome.name != "job-list" or outcome.result_status != "UPDATED":
05063:             continue
05064:         old = (outcome.installed_version or "").strip()
05065:         new = (outcome.remote_version or "").strip()
05066:         if new and old != new:
05067:             return True
05068:     return False
05069:
05070:
05071: def run_job_list_post_update(cfg: dict[str, Any], outcomes: list[TargetOutcome]) -> dict[str, Any]:
05072:     """Best-effort Job-list activation after every non-check updater cycle.
05073:
05074:     Rescue contract v1 intentionally decouples package installation from job
05075:     delivery. Job-list owns platform/expiry/dedupe/profile/queue semantics, so
05076:     calling activate repeatedly is safe and lets failed activation recover on
05077:     the next updater cycle even when the Job-list package is CURRENT.
05078:     """
05079:     root = (_cfg_private_root(cfg) / "job-list").resolve()
05080:     core = root / "bin" / "job-list-core.py"
05081:     source = root / "requests" / "one-shot-jobs.json"
05082:     result: dict[str, Any] = {
05083:         "status": "NOT_AVAILABLE",
05084:         "root": str(root),
05085:         "core": str(core),
05086:         "source": str(source),
05087:         "returncode": None,
05088:         "version_changed_this_cycle": _job_list_version_changed(outcomes),
05089:         "activation_policy": "SCHEDULED_ENTRY_ONLY",
05090:     }
05091:     if not core.is_file() or not source.is_file():
05092:         missing = []
05093:         if not core.is_file():
05094:             missing.append("core")
05095:         if not source.is_file():
05096:             missing.append("source")
05097:         result["status"] = "NOT_AVAILABLE"
05098:         result["detail"] = "missing:" + ",".join(missing)
05099:         print(f"job_sync: [SKIP] {result['detail']}", flush=True)
05100:         return result
05101:
05102:     command = [
05103:         sys.executable, str(core), "activate",
05104:         "--root", str(root),
05105:         "--source", str(source),
05106:         "--launch",
05107:     ]
05108:     try:
05109:         completed = subprocess.run(
05110:             command, cwd=str(root), stdin=subprocess.DEVNULL,
05111:             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
05112:             text=True, encoding="utf-8", errors="replace",
05113:             timeout=180, check=False,
05114:         )
05115:         result["returncode"] = int(completed.returncode)
05116:         out = (completed.stdout or "").strip()
05117:         err = (completed.stderr or "").strip()
05118:         if out:
05119:             result["stdout_tail"] = "\n".join(out.splitlines()[-20:])[-4000:]
05120:         if err:
05121:             result["stderr_tail"] = "\n".join(err.splitlines()[-20:])[-4000:]
05122:         if completed.returncode == 0:
05123:             result["status"] = "CALLED"
05124:             result["detail"] = "job-list activate --launch completed"
05125:             print("job_sync: [CALLED] job-list activate --launch", flush=True)
05126:         else:
05127:             result["status"] = "FAILED_NONBLOCKING"
05128:             result["detail"] = f"job-list activate returned rc={completed.returncode}; next updater cycle will retry"
05129:             print(f"job_sync: [WARN] {result['detail']}", file=sys.stderr, flush=True)
05130:     except subprocess.TimeoutExpired:
05131:         result["status"] = "FAILED_NONBLOCKING"
05132:         result["detail"] = "job-list activate timed out after 180s; next updater cycle will retry"
05133:         print(f"job_sync: [WARN] {result['detail']}", file=sys.stderr, flush=True)
05134:     except Exception as exc:
05135:         result["status"] = "FAILED_NONBLOCKING"
05136:         result["detail"] = f"job-list activate error: {exc}; next updater cycle will retry"
05137:         print(f"job_sync: [WARN] {result['detail']}", file=sys.stderr, flush=True)
05138:     return result
05139:
05140:
05141: def report_paths(cfg: dict[str, Any]) -> tuple[Path, Path]:
05142:     output = Path(os.environ.get("AUTOTASK_OUTPUT_DIR") or cfg["output_dir"])
05143:     output.mkdir(parents=True, exist_ok=True)
05144:     return output / "update_result.json", output / "update_report.md"
...
05228:     ]
05229:     if payload.get("source_note"):
05230:         lines.append(f"- 조회 설명: {payload['source_note']}")
05231:     if payload.get("source_fallbacks"):
05232:         lines.append("- 인덱스 미발견 후 root ZIP 자동 탐색 사용")
05233:     if payload.get("duplicate_version_assets"):
05234:         lines.append(f"- 동일 버전 ZIP 중복: `{len(payload['duplicate_version_assets'])}`개 대상; 날짜는 무시하고 무인 결정")
05235:     if payload.get("main_migrations"):
05236:         lines.append(f"- main 사전 이관: `{len(payload['main_migrations'])}`개 스킬")
05237:     if payload.get("autotask_refresh"):
05238:         refresh = payload["autotask_refresh"]
05239:         lines.append(
05240:             f"- autotask 재등록: `{refresh.get('status')}` "
...
05245:         lines.append(f"- Job-list post-update launch: `{js.get('status')}` ({js.get('detail') or '-'})")
05246:     lines += ["", "## 대상 판정", "", "| 스킬 | 로컬 | 로컬 버전 근거 | 원격 | 채널 | 판정 | 적용 |", "|---|---:|---|---:|---|---|---|"]
05247:     for d in ds:
05248:         local_label = (d.installed_version or "-") + (f" r{d.installed_revision}" if d.installed_revision else "")
05249:         remote_label = (d.remote_version or "-") + (f" r{d.remote_revision}" if d.remote_revision else "")
05250:         source_label = (d.installed_version_source or "-").replace("|", "\\|")
05251:         lines.append(f"| {d.name} | {local_label} | {source_label} | {remote_label} | {d.remote_channel or '-'} | {d.status} | {'Y' if d.apply else 'N'} |")
05252:     lines += ["", "## 적용 결과", ""]
05253:     if applied:
05254:         for item in applied:
05255:             lines.append(
05256:                 f"- `{item.name}`: `{item.old_version or '-'}` → `{item.new_version}`; "
05257:                 f"backup=`{item.backup or '-'}`; preserved={item.preserved_files}; "
...
05352:     version = str(top.get("version") or "unknown")
05353:     failure = str(top.get("failure_code") or "PREFLIGHT_FAILED")
05354:     message = str(top.get("message") or "archive validation failed")
05355:     return (f"{name}: GitHub 상위 버전 v{version} 발견, 검증 실패({failure}): "
05356:             f"{message}; 정상 후보 v{decision.remote_version or '-'} 유지. "
05357:             "최신 버전 설치 완료가 아닙니다")
05358:
05359:
05360: def _overall_run_status(outcomes: list[TargetOutcome], errors: list[str]) -> str:
05361:     summary = _outcome_summary(outcomes)
05362:     failed = bool(errors) or summary["FAILED"] > 0
05363:     progressed = summary["UPDATED"] + summary["SKIPPED"] > 0
05364:     if failed and progressed:
...
05396:         if sha256_file(dest) != digest:
05397:             raise UpdateError("self-update staging copy digest mismatch")
05398:         intent = {
05399:             "schema_version": 1, "request_id": run_id, "run_id": run_id,
05400:             "from_version": decision.installed_version, "to_version": decision.remote_version,
05401:             "package_digest": digest, "staging_path": str(dest),
05402:             "target_root": str(private_root / "skill-updater"),
05403:             "policy_ref": _self_policy(cfg), "created_at": now_iso(),
05404:             "state": "STAGED", "phase": "STAGED", "installer_owner": "stable_bootstrap",
05405:         }
05406:         atomic_json(stage / "pending_self_update.json", intent)
05407:         atomic_json(bootstrap_root / "pending_self_update.json", intent)
05408:         return {k:v for k,v in intent.items() if k not in {"staging_path", "target_root"}}
...
05477:             "applied": [asdict(item) for item in applied],
05478:             "blocked_candidates": cfg.get("_blocked_candidates") or {},
05479:             "broken_newer": cfg.get("_broken_newer") or {},
05480:             "github_requests": cfg.get("_github_request_counts") or {},
05481:             "github_cache_hits": cfg.get("_github_cache_hits") or [],
05482:             "github_run_cache_hits": cfg.get("_github_run_cache_hits") or [],
05483:             "github_stale_cache_hits": cfg.get("_github_stale_cache_hits") or [],
05484:             "github_stale_cache_diagnostics": cfg.get("_github_stale_cache_diagnostics") or [],
05485:             "github_freshness": cfg.get("_github_freshness") or {},
05486:             "fresh_cycle_reset": cfg.get("_fresh_cycle_reset"),
05487:             "self_update": cfg.get("_self_update_result") or {"phase": "NONE", "self_update_policy": _self_policy(cfg)},
05488:             "workflow_provider_sync": cfg.get("_workflow_provider_sync") or {"result":"NOT_INVOKED"},
05489:         })
05490:         if final:
05491:             run_state["completed_at"] = now_iso()
05492:             run_state["status"] = _overall_run_status(target_outcomes, errors)
...
05556:                             decision = target_decisions[0]
05557:                             ds.append(decision)
05558:                             outcome.decision_status = decision.status
05559:                             outcome.installed_version = decision.installed_version
05560:                             outcome.remote_version = decision.remote_version
05561:                             broken = (cfg.get("_broken_newer") or {}).get(name) or []
05562:                             if decision.status == "CURRENT_WITH_BROKEN_NEWER":
05563:                                 outcome.result_status = "FAILED"
05564:                                 outcome.failure_code = "NEWER_RELEASE_INVALID"
05565:                                 outcome.failed_stage = "CANDIDATE_VALIDATION"
05566:                                 outcome.error = _unusable_newer_release(name, decision, broken)
05567:                                 outcome.detail = outcome.error
05568:                                 errors.append(outcome.error)
...
05608:                     ds.append(decision)
05609:
05610:                     outcome.decision_status = decision.status
05611:                     outcome.installed_version = decision.installed_version
05612:                     outcome.remote_version = decision.remote_version
05613:                     outcome.detail = decision.detail or decision.status
05614:                     broken = (cfg.get("_broken_newer") or {}).get(name) or []
05615:                     if broken:
05616:                         outcome.warnings = [f"상위 불량 원격 후보 {len(broken)}개 제외"]
05617:
05618:                     blocked = (cfg.get("_blocked_candidates") or {}).get(name)
05619:                     if decision.status in ("BLOCKED_RELEASE", "REBUILD_CONFLICT"):
05620:                         outcome.result_status = "FAILED"
...
05738:             _cleanup_prepared_candidate(prepared)
05739:         cfg["_prepared_candidates"] = {}
05740:
05741:     if action != "check":
05742:         # Default is update-only; only the separate OS scheduled entry may activate Jobs.
05743:         cfg["_job_sync_result"] = {"status": "NOT_INVOKED", "activation_policy": "SCHEDULED_ENTRY_ONLY", "job_activation_invoked": False}
05744:
05745:     json_path, md_path = write_report(
05746:         cfg, action, ds, applied, errors, started, now_iso(), target_outcomes
05747:     )
05748:     run_state["result_json"] = str(json_path)
05749:     run_state["report_md"] = str(md_path)
05750:
...
05814:         }
05815:         artifacts: dict[str, Any] = {
05816:             "masked_config.json": _mask_sensitive_payload(raw_cfg),
05817:             "candidate_selection.json": {
05818:                 "root_zip_candidates": cfg.get("_root_zip_candidates") or {},
05819:                 "ambiguous_candidates": cfg.get("_ambiguous_candidates") or {},
05820:                 "duplicate_version_assets": cfg.get("_duplicate_version_assets") or {},
05821:                 "blocked_candidates": cfg.get("_blocked_candidates") or {},
05822:                 "broken_newer": cfg.get("_broken_newer") or {},
05823:                 "selected_manifest": cfg.get("_last_manifest") or {},
05824:             },
05825:             "metadata_observations.json": {
05826:                 name: {
...
05940:
05941:     This is intentionally independent of SkillSilent.  The canonical Private Skill
05942:     implementation owns SKILL.md; the Claude discovery entry is a derived copy.
05943:     During update runs we repair only a missing/stale SKILL.md so an already-current
05944:     Skill cannot remain undiscoverable merely because no new remote version exists.
05945:     """
05946:     install_root=Path(cfg["install_root"]).expanduser().resolve()
05947:     entry=_isolated_target_path(install_root,name)
05948:     canonical=canonical_private_skill_root(cfg,name)
05949:     source=canonical/"SKILL.md"
05950:     target=entry/"SKILL.md"
05951:     result={
05952:         "skill":name,"canonical_root":str(canonical),"discovery_root":str(entry),
...
06351:             raise ClassifiedUpdateError("canonical/entry SKILL.md checksum mismatch after auto repair",
06352:                 failure_code="AUTO_CANONICAL_ENTRY_CHECKSUM_MISMATCH", disposition="BLOCKED", retryable=False,
06353:                 stage="AUTO_CANONICAL_REPAIR_VERIFY")
06354:         _name, observed_version, _nsrc, vsrc, diag = skill_metadata_detailed(canonical, expected_name=decision.name)
06355:         if observed_version and decision.remote_version and not same_release_version(observed_version, decision.remote_version):
06356:             raise ClassifiedUpdateError(f"auto-repaired canonical version mismatch: expected={decision.remote_version} actual={observed_version}",
06357:                 failure_code="AUTO_CANONICAL_VERSION_MISMATCH", disposition="BLOCKED", retryable=False,
06358:                 stage="AUTO_CANONICAL_REPAIR_VERIFY")
06359:
06360:         report_dir = canonical / "data" / "state" / "migration" / "skill-updater-canonical-repair"
06361:         report_dir.mkdir(parents=True, exist_ok=True)
06362:         report_path = report_dir / f"{stamp()}.json"
06363:         report_payload = {
06364:             "schema": "skill-updater-canonical-repair/v1", "skill": decision.name,
06365:             "version": decision.remote_version or observed_version, "repair": repair,
06366:             "legacy_reconcile": reconcile, "canonical_root": str(canonical), "entry": str(entry),
06367:             "force_overwrite": "DISABLED", "legacy_delete": "DISABLED",
06368:         }
06369:         atomic_json(report_path, report_payload)
06370:
06371:         archive_sha = decision.sha256 or prepared.archive_sha256 or sha256_file(archive)
06372:         baseline_hashes = _package_baseline_hashes(root)
06373:         _write_receipt(cfg, decision.name, decision.remote_version or observed_version or "", baseline_hashes, None,
06374:             revision=decision.remote_revision or 1, channel=decision.remote_channel or infer_channel(decision.remote_version or observed_version or ""),
06375:             archive_sha256=archive_sha, git_blob_sha=decision.git_blob_sha, installed_root=canonical)
06376:         return Applied(decision.name, decision.installed_version, decision.remote_version or observed_version or "",
06377:             None, str(archive), str(entry), None, 0, reconcile.get("conflicts",0), old_revision=decision.installed_revision,
06378:             new_revision=decision.remote_revision or 1, config_backup=None, main_data_root=str(canonical/"data"),
06379:             migration_report=str(report_path), migrated_files=int(reconcile.get("copied",0)), migrated_tasks=[],
06380:             package_name_source=prepared.package_name_source, package_version_source=prepared.package_version_source,
06381:             metadata_diagnostics=list(prepared.metadata_diagnostics)+[
06382:                 "install_mode=AUTO_REPAIRED_CANONICAL_PRIVATE_ROOT", f"canonical_root={canonical}", f"entry_root={entry}",
06383:                 f"auto_repair_changes={repair.get('changes',0)}", f"repair_report={report_path}", f"canonical_version_source={vsrc}",
06384:             ]+list(diag or []))
...
06565:     repository = args.repository or (ask("GitHub 저장소 OWNER/REPOSITORY") if interactive else "")
06566:     if not REPO_RE.fullmatch(repository):
06567:         print("--repository OWNER/REPOSITORY가 필요합니다", file=sys.stderr)
06568:         return 2
06569:     mode = args.mode or (ask("조회 방식 auto/release/contents/root-zips", "auto") if interactive else "auto")
06570:     channel = args.channel or (ask("배포 채널 stable/rc/beta/dev/all", "stable") if interactive else "stable")
06571:     detected_proxy_mode = "env" if _process_env_proxies() else "auto"
06572:     proxy_mode = args.proxy_mode or (
06573:         ask("프록시 방식 auto/env/git/explicit/none", detected_proxy_mode) if interactive else detected_proxy_mode
06574:     )
06575:     private_root = default_private_install_root()
06576:     main_value = args.main_root or str(private_root)  # compatibility alias; canonical Private Skill root
06577:     main_root = expand_path(main_value)
...
06591:         "source": {
06592:             "provider": "github", "repository": repository, "mode": mode,
06593:             "manifest_asset": args.manifest_asset, "ref": args.ref,
06594:             "manifest_path": args.manifest_path, "token_env": args.token_env,
06595:             "allow_root_zip_discovery": True, "zip_path": args.zip_path, "channel": channel,
06596:             "version_policy": "latest",
06597:         },
06598:         "network": {
06599:             "proxy_mode": proxy_mode,
06600:             "proxy_url_env": args.proxy_url_env,
06601:             "use_git_config_proxy": True,
06602:             "allow_direct_fallback": proxy_mode == "auto",
06603:             "ca_bundle_env": "SKILL_UPDATER_CA_BUNDLE",
...
06606:             "allow_insecure_tls_fallback": True,
06607:             "remember_successful_tls": True,
06608:             "connect_timeout_sec": 60,
06609:             "download_timeout_sec": 300,
06610:             "github_min_poll_interval_sec": DEFAULT_GITHUB_MIN_POLL_INTERVAL_SEC,
06611:             "github_cache_max_stale_sec": DEFAULT_GITHUB_CACHE_MAX_STALE_SEC,
06612:             "github_api_max_requests_per_run": DEFAULT_GITHUB_API_MAX_REQUESTS_PER_RUN
06613:         },
06614:         "main_root": str(main_root),
06615:         "private_install_root": str(private_root),
06616:         "download_dir": download_value, "install_root": install_value,
06617:         "output_dir": str(canonical_updater_output_dir(private_root)),
06618:         "targets": [default_target_entry(name) for name in targets],
06619:         "retention": {"downloads_per_skill": 3, "backups_per_skill": 3, "config_backups_per_skill": 5},
...
06885:     if payload.get("diagnostic_bundle"): print(f"diagnostic_bundle: {payload['diagnostic_bundle']}")
06886:     return 0
06887:
06888: def _job_cleanup_snapshot(cfg: dict[str, Any] | None = None) -> dict[str, Any]:
06889:     """Run the allowlisted read-only Job-list bridge; never update/activate Jobs."""
06890:     private_root = _cfg_private_root(cfg) if cfg is not None else (Path.home() / "l1sw-private-skills")
06891:     root = (private_root / "job-list").resolve()
06892:     cmd = root / "bin" / "job-list-core.py"
06893:     if not cmd.is_file():
06894:         return {"status": "NOT_AVAILABLE", "error": "job-list core not installed", "read_only": True}
06895:     try:
06896:         proc = subprocess.run([sys.executable, str(cmd), "cleanup-result", "--root", str(root)],
06897:                               cwd=str(root), stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
...
07110:     config_path = resolve_config_path(args.config)
07111:     load_env_file(config_path.parent / "skill-updater.env")
07112:     cfg = normalized_config(config_path)
07113:     repo = cfg["source"]["repository"]
07114:     token = os.environ.get(cfg["source"].get("token_env", "GITHUB_TOKEN"))
07115:     url = f"https://api.github.com/repos/{repo}"
07116:     try:
07117:         value = http_json_value(cfg, url, token)
07118:     except Exception as exc:
07119:         print(f"[FAIL] GitHub API: {exc}", file=sys.stderr)
07120:         return 1
07121:     print(f"[OK] GitHub API: {repo}")
07122:     if isinstance(value, dict):
...
07271:         "확인만", "체크만", "비교만", "업데이트 여부", "업데이트 가능한지",
07272:         "dry-run", "dry run", "조회만",
07273:     )
07274:     if any(x in normalized for x in check_only_markers):
07275:         return ["check", "--refresh-remote"]
07276:
07277:     # v0.5.36 natural-language contract: a request to *perform* the updater means
07278:     # "observe GitHub now and apply the latest registered-skill versions".  Fresh
07279:     # remote observation is the default execution contract, so operator words such
07280:     # as "강제" no longer imply reinstalling an already-current package.  Explicit
07281:     # repair/reinstall wording is required for --repair-current.
07282:     once_markers = ("1회", "한 번", "한번", "one-shot", "one shot", "once")
07283:     test_markers = ("테스트", "시험")
...
07318:
07319:
07320: def _add_init_arguments(parser: argparse.ArgumentParser) -> None:
07321:     parser.add_argument("--repository")
07322:     parser.add_argument("--mode", choices=["auto", "release", "contents", "root-zips"])
07323:     parser.add_argument("--manifest-asset", default="skill-index.json")
07324:     parser.add_argument("--manifest-path", default="skill-index.json")
07325:     parser.add_argument("--zip-path", default="", help="ZIP 파일이 있는 저장소 폴더; 기본은 루트")
07326:     parser.add_argument("--channel", choices=list(ALLOWED_CHANNELS), default="stable")
07327:     parser.add_argument("--ref", default="main")
07328:     parser.add_argument("--token-env", default="GITHUB_TOKEN")
07329:     parser.add_argument("--proxy-mode", choices=["auto", "env", "git", "explicit", "none"])
07330:     parser.add_argument("--proxy-url-env", default="SKILL_UPDATER_PROXY")
...
07388:         p.add_argument("--config")
07389:         p.add_argument("--skill", action="append", dest="skills")
07390:         p.add_argument("--yes", action="store_true")
07391:         p.add_argument("--resume", action="store_true", help="최신 FAILED/NOT_ATTEMPTED 대상만 재개")
07392:         p.add_argument("--refresh-remote", action="store_true", help="호환 옵션: v0.5.36부터 모든 실행이 기본적으로 GitHub를 fresh 조회")
07393:         p.add_argument("--repair-current", action="store_true", help="동일 버전 설치본의 package drift를 검사하고 손상된 대상만 재설치")
07394:         p.set_defaults(func=None)
07395:
07396:     update = sub.add_parser("update", help="승인 인자 없이 로컬 업데이트 실행")
07397:     update.add_argument("--config")
07398:     update.add_argument("--skill", action="append", dest="skills")
07399:     update.add_argument("--refresh-remote", action="store_true")
07400:     update.add_argument("--repair-current", action="store_true", help="동일 버전 설치본 손상 시에만 강제 복구")
07401:     update.set_defaults(func=None)
07402:
07403:     retry = sub.add_parser("retry", help="이전 실패·미처리 대상만 재개")
07404:     retry.add_argument("--config")
07405:     retry.add_argument("--skill", action="append", dest="skills")
07406:     retry.add_argument("--refresh-remote", action="store_true")
07407:     retry.add_argument("--repair-current", action="store_true", help="동일 버전 설치본 손상 시에만 강제 복구")
07408:     retry.set_defaults(func=None)
07409:
07410:     natural = sub.add_parser("natural", help="자연어 요청을 간편 명령으로 변환")
07411:     natural.add_argument("text", nargs=argparse.REMAINDER)
07412:     natural.set_defaults(func=None)
07413:
07414:     proxy = sub.add_parser("proxy")
...
07491:             print(str(exc), file=sys.stderr, flush=True)
07492:             return 1
07493:         # v0.5.36 contract: every updater cycle is fresh by default, whether it
07494:         # was started manually, by natural language, or by AutoTask Builder.
07495:         # --refresh-remote remains accepted for backward compatibility.
07496:         cfg["_force_remote_refresh"] = True
07497:         cfg["_fresh_remote_contract"] = True
07498:         cfg["_refresh_remote_requested"] = bool(getattr(args, "refresh_remote", False))
07499:         cfg["_repair_current"] = bool(getattr(args, "repair_current", False))
07500:         selected = set(args.skills) if args.skills else None
07501:         configured = {str(t.get("name")) for t in (cfg.get("targets") or []) if isinstance(t, dict) and t.get("name")}
07502:         enabled = {str(t["name"]) for t in enabled_targets(cfg)}
07503:         if selected:
07504:             unconfigured = sorted(selected - configured)
07505:             disabled = sorted((selected & configured) - enabled)
07506:             if unconfigured or disabled:
...
07552:         print("취소되었습니다", file=sys.stderr, flush=True)
07553:         return 130
07554:
07555:
07556: def main(argv: list[str] | None = None) -> int:
07557:     global _BOOTSTRAP_HEARTBEAT
07558:     for stream in (sys.stdout, sys.stderr):
07559:         try: stream.reconfigure(errors="replace", line_buffering=True, write_through=True)
07560:         except Exception: pass
07561:     actual_argv = list(sys.argv[1:] if argv is None else argv)
07562:     actual_argv = normalize_cli_argv(actual_argv)
07563:     # An offline canary must not initialize logs, network or runtime migrations.
07564:     if actual_argv == ["--version"]:
07565:         print(VERSION)
07566:         return 0
07567:     if actual_argv and actual_argv[0] == "natural":
07568:         mapped = natural_language_command(" ".join(actual_argv[1:]))
07569:         if not mapped:
07570:             print("자연어 요청을 이해하지 못했습니다", file=sys.stderr, flush=True); return 2
07571:         actual_argv = mapped
07572:     query_commands = {"logs", "result", "status", "cleanup-result"}
07573:     if actual_argv and actual_argv[0] in query_commands:
07574:         load_env_file()
07575:         return _dispatch_main(actual_argv)
07576:     with DebugLogSession(actual_argv) as session:
07577:         debug_event("LOG_PATH", path=str(session.path))
07578:         action = actual_argv[0] if actual_argv else "-"
07579:         print(f"[STARTED] skill-updater v{VERSION} pid={os.getpid()} action={action} debug_log={session.path}", flush=True)
07580:         if action in {"check", "run", "apply", "update", "retry"}:
07581:             _BOOTSTRAP_HEARTBEAT = StartupHeartbeat(action)
07582:             _BOOTSTRAP_HEARTBEAT.start()
07583:         try:
07584:             if _BOOTSTRAP_HEARTBEAT is not None: _BOOTSTRAP_HEARTBEAT.update("LOAD_ENV", "환경·프록시 설정 로딩")
07585:             debug_event("ENV_LOAD_START")
07586:             load_env_file()
07587:             debug_event("ENV_LOAD_END")
07588:             rc = _dispatch_main(actual_argv)
07589:         except BaseException as exc:
07590:             debug_event("FATAL", error=str(exc))
07591:             raise
07592:         finally:
07593:             if _BOOTSTRAP_HEARTBEAT is not None:
07594:                 _BOOTSTRAP_HEARTBEAT.stop(); _BOOTSTRAP_HEARTBEAT = None
07595:         debug_event("EXIT", returncode=rc)
07596:         return rc
```
## scripts/skill_updater_auto.py
Source functions of interest: main:31

```python
...
00027:     finally:
00028:         tmp.unlink(missing_ok=True)
00029:
00030:
00031: def main(argv=None) -> int:
00032:     parser = argparse.ArgumentParser()
00033:     parser.add_argument("--config", default=str(skill_updater.default_config_path()))
00034:     parser.add_argument("--yes", action="store_true")
00035:     args = parser.parse_args(argv)
00036:     config = skill_updater.resolve_config_path(args.config)
00037:     skill_updater.load_env_file(config.parent / "skill-updater.env")
00038:     canonical = skill_updater.default_config_path().resolve()
00039:     if config != canonical:
00040:         print(f"unattended config must be canonical: {canonical}", file=sys.stderr)
00041:         return 2
00042:     if not args.yes:
00043:         print("unattended execution requires --yes", file=sys.stderr)
00044:         return 2
00045:
00046:     runtime_root = skill_updater.canonical_updater_runtime_dir()
00047:     stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
00048:     run_id = "auto_" + stamp + "_" + uuid.uuid4().hex[:8]
00049:     log_path = skill_updater.canonical_updater_output_dir() / "logs" / run_id / "auto.log"
00050:     state_path = runtime_root / "state" / "auto_run.json"
00051:     history_path = runtime_root / "state" / "history" / (run_id + ".json")
00052:     output_dir = Path(os.environ.get("AUTOTASK_OUTPUT_DIR") or (skill_updater.canonical_updater_output_dir() / dt.datetime.now().strftime("%Y%m%d") / run_id))
00053:     os.environ["AUTOTASK_OUTPUT_DIR"] = str(output_dir)
00054:     os.environ["SKILL_UPDATER_UNATTENDED"] = "1"
00055:     os.environ["SKILL_UPDATER_NONINTERACTIVE"] = "1"
00056:     os.environ["PYTHONUNBUFFERED"] = "1"
00057:     state = {
00058:         "schema_version": 1, "run_id": run_id, "status": "RUNNING", "pid": os.getpid(),
00059:         "started_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
00060:         "config": str(config), "log_path": str(log_path), "output_dir": str(output_dir),
00061:         "exit_code": None, "resume_mode": False, "resume_targets": [],
00062:     }
00063:     atomic(state_path, state)
00064:     atomic(history_path, state)
00065:     log_path.parent.mkdir(parents=True, exist_ok=True)
00066:     skill_updater._prune_log_storage(
00067:         log_path.parent.parent, skill_updater.DEBUG_LOG_KEEP, [log_path.parent]
00068:     )
00069:     rc = 1
00070:     with log_path.open("a", encoding="utf-8", buffering=1) as log, contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
00071:         try:
00072:             # Each scheduler firing is an independent fresh cycle. Previous
00073:             # FAILED/NOT_ATTEMPTED state and failure fingerprints are diagnostics
00074:             # only; only explicit retry/--resume may consume prior run state.
00075:             # Unattended cycles NEVER replace a running engine. The updater may
00076:             # safely STAGE its candidate outside the live root; only a separately
00077:             # installed Bootstrap applies after this process exits. Shared
00078:             # skillsilent remains a manual maintenance-only engine.
00079:             cfg = skill_updater.normalized_config(config)
00080:             frozen = {"skillsilent"}
00081:             unattended_targets = [
00082:                 str(item.get("name")).strip() for item in skill_updater.enabled_targets(cfg)
00083:                 if str(item.get("name") or "").strip()
00084:                 and str(item.get("name") or "").strip().lower() not in frozen
00085:             ]
00086:             print("UNATTENDED_SHARED_ENGINE_SKIPPED: skillsilent; updater is stage-only")
00087:             if not unattended_targets:
00088:                 print("UNATTENDED_NO_MUTABLE_TARGETS")
00089:                 rc = 0
00090:             else:
00091:                 command = ["update", "--config", str(config)]
00092:                 for name in unattended_targets:
00093:                     command.extend(["--skill", name])
00094:                 rc = skill_updater.main(command)
00095:             # This OS-scheduled entry is the *only* compatibility path for the
00096:             # legacy scheduled Job-list hook. Never infer scheduler authority from
00097:             # SKILL_UPDATER_UNATTENDED in an ordinary MCP CLI call.
00098:             scheduled_job_result = skill_updater.run_job_list_post_update(cfg, [])
00099:             print("SCHEDULED_JOB_RESULT=" + json.dumps(scheduled_job_result, ensure_ascii=True))
00100:             state["scheduled_job_result"] = scheduled_job_result
00101:         except BaseException:
00102:             traceback.print_exc()
00103:             rc = 1
00104:     result_path = output_dir / "update_result.json"
00105:     report_path = output_dir / "update_report.md"
00106:     if not result_path.is_file():
00107:         fallback_status = "SUCCESS" if rc == 0 else "FAILED"
00108:         atomic(result_path, {
00109:             "schema_version": 2,
00110:             "run_id": run_id,
00111:             "updater_version": skill_updater.VERSION,
00112:             "action": "update",
00113:             "started_at": state["started_at"],
00114:             "completed_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
00115:             "target_results": [],
00116:             "summary": {"UPDATED": 0, "SKIPPED": 0, "FAILED": 0 if rc == 0 else 1, "NOT_ATTEMPTED": 0, "TOTAL": 0},
00117:             "errors": [] if rc == 0 else ["unattended runner ended before updater report generation"],
00118:             "status": fallback_status,
00119:             "runner_fallback": True,
00120:         })
00121:     if not report_path.is_file():
00122:         result_for_report = json.loads(result_path.read_text(encoding="utf-8"))
00123:         atomic_text(
00124:             report_path,
00125:             "# Skill Updater Report\n\n"
00126:             f"- 상태: **{result_for_report.get('status', 'FAILED')}**\n"
00127:             "- 생성 주체: unattended runner fallback\n"
00128:             f"- run_id: `{run_id}`\n",
00129:         )
00130:     result_status = None
00131:     try:
00132:         result_status = json.loads(result_path.read_text(encoding="utf-8")).get("status")
00133:     except Exception:
00134:         result_status = None
00135:     if result_status not in ("SUCCESS", "PARTIAL_SUCCESS", "FAILED"):
00136:         result_status = "SUCCESS" if rc == 0 else "FAILED"
00137:     state.update({
00138:         "status": result_status,
00139:         "completed_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
00140:         "exit_code": rc, "result_json": str(result_path),
00141:         "report_md": str(report_path),
00142:     })
00143:     atomic(state_path, state)
00144:     atomic(history_path, state)
00145:     skill_updater._prune_log_storage(
00146:         log_path.parent.parent, skill_updater.DEBUG_LOG_KEEP, [log_path.parent]
00147:     )
00148:     print(json.dumps(state, ensure_ascii=True))
00149:     return rc
```\n