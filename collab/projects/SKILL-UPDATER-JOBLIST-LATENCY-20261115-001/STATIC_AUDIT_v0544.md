# Skill-Updater v0.5.44 — isolated public ZIP code audit
- Source: `wonhwipark/L1Work/main/skill-updater_v0_5_44_1027.zip`
- Source size: 210717
- Source SHA-256: `0185778e44f7cce2d11a5e6b78f6e3f86e4b886ea07861984caa7fc7965b4fcd`
- Git blob SHA: `d83faa021549835a40e3ddc134b8e936dc962e65`
- ZIP CRC: PASS
- Scope: STATIC source inspection; not the currently installed Linux binary. Never ran updater, activated Jobs or touched host.
- Source files: 74

## `skill-updater_v0_5_44_1027/bootstrap/l1sw_bootstrap.py`
- total lines: 345
- matching lines: 19
- related functions:
```python
...
00001: #!/usr/bin/env python3
00002: """Externally installed and deliberately independent Skill-Updater maintenance tool.
00003:
00004: Use after updater process exit. Does not start Jobs, touch MCP, or change scheduler.
00005: Manual canary is mandatory unless an administrator deploys a separate, audited
00006: scheduled launcher. This file MUST be copied outside the updater skill root.
00007: """
00008: from __future__ import annotations
00009: import argparse
00010: import datetime as dt
00011: import hashlib
00012: import json
00013: import os
00014: from pathlib import Path, PurePosixPath
00015: import re
00016: import shutil
00017: import subprocess
00018: import sys
00019: import tempfile
00020: import uuid
00021: import zipfile
00022:
00023: SHA = re.compile(r"^[a-f0-9]{64}$")
...
00103: def canary(root):
00104:     # Pure offline; no network or job activation; avoid running arbitrary package
00105:     # installers/self-tests as a precondition for code replacement.
00106:     checks = [(root / 'scripts' / 'skill_updater.py', '--version')]
00107:     for script, arg in checks:
00108:         cp = subprocess.run([sys.executable, '-B', str(script), arg], cwd=str(root),
00109:                             stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=35)
00110:         if cp.returncode or not cp.stdout.strip():
00111:             raise ValueError('offline version canary failed: ' + (cp.stderr or '')[-300:])
00112:     return True
00113:
00114:
00115: def apply(intent_path, *, approved=False):
00116:     if not approved: raise ValueError('manual canary approval required; pass --approve-manual-canary')
...
00219:     root = updater_root.expanduser().resolve()
00220:     config = config.expanduser().resolve()
00221:     if not (root / 'scripts/skill_updater.py').is_file():
00222:         raise ValueError('updater executable missing')
00223:     intent_path = root.parent.parent / 'l1sw-bootstrap/pending_self_update.json'
00224:     out = {'status':'NOT_STARTED', 'update_returncode':None,
00225:            'self_update_phase':'NONE', 'scheduled':scheduled,
00226:            'preinstall_phase':'NONE', 'postinstall_phase':'NONE',
00227:            'followup_phase':'NOT_REQUIRED', 'installed_version_before':_installed_version(root)}
00228:     auto_allowed = bool(apply_after_exit and _auto_policy_authorized(config))
00229:     out['auto_policy_authorized'] = auto_allowed
00230:
00231:     # Already-staged candidates are intentionally evaluated BEFORE launching the
00232:     # updater. No timestamp requirement here: a previous cycle may have exited.
00233:     if intent_path.is_file():
00234:         try:
00235:             pending = json.loads(intent_path.read_text(encoding='utf-8'))
00236:             if pending.get('state') == 'STAGED':
00237:                 intent = read_intent(intent_path)
...
00253:                        self_update_phase='DEFERRED',
00254:                        reason='PENDING_SELF_UPDATE_INVALID: ' + type(exc).__name__ + ': ' + str(exc),
00255:                        installed_version_after=_installed_version(root))
00256:             return out
00257:
00258:     # Newly installed files are now the source for this *new* subprocess.
00259:     if scheduled:
00260:         script = root / 'scripts/skill_updater_auto.py'
00261:         argv = [sys.executable, '-B', str(script), '--config', str(config), '--yes']
00262:     else:
00263:         script = root / 'scripts/skill_updater.py'
00264:         argv = [sys.executable, '-B', str(script), 'update', '--config', str(config)]
00265:     import time
00266:     started_ns = time.time_ns()
00267:     result = subprocess.run(argv, cwd=str(root), stdin=subprocess.DEVNULL, check=False)
00268:     out.update(status='UPDATE_COMPLETED' if result.returncode == 0 else 'UPDATE_FAILED',
00269:                update_returncode=result.returncode,
00270:                updater_version_executed=_installed_version(root))
00271:
00272:     # POST applies only the freshly staged candidate from THIS execution,
00273:     # not an unrelated old STAGED (which may be manual-only).
00274:     try:
00275:         if not intent_path.is_file() or intent_path.stat().st_mtime_ns < started_ns:
...
00282:         intent = read_intent(intent_path)
00283:         if Path(intent.get('target_root','')).resolve() != root:
00284:             raise ValueError('newly staged target_root mismatch')
00285:         out['postinstall_phase'] = 'STAGED'
00286:         out['self_update_phase'] = 'STAGED'
00287:         if result.returncode != 0:
00288:             out['reason']='UPDATE_FAILED_BEFORE_AUTO_APPLY'
00289:         elif intent['policy_ref'] != 'automatic_after_exit':
00290:             out['reason']='MANUAL_CANARY_REQUIRED'
00291:         elif not (apply_after_exit and _auto_policy_authorized(config)):
00292:             out['reason']='AUTO_POLICY_NOT_AUTHORIZED'
00293:         else:
00294:             installed = apply(intent_path, approved=True)
00295:             out['postinstall_phase'] = installed['phase']
00296:             out['self_update_phase'] = installed['phase']
00297:             out['postinstall_receipt'] = str(intent_path.parent / 'receipts' / (str(installed['run_id']) + '.json'))
00298:             # Do not rerun the scheduled script: that would activate Jobs twice.
00299:             # Re-running the plain updater is update-only; bounded to ONE try.
00300:             followup = subprocess.run(
00301:                 [sys.executable, '-B', str(root / 'scripts/skill_updater.py'),
00302:                  'update', '--config', str(config)],
00303:                 cwd=str(root), stdin=subprocess.DEVNULL, check=False)
00304:             out['followup_phase']='COMPLETED' if followup.returncode == 0 else 'FAILED'
00305:             out['followup_returncode']=followup.returncode
00306:             if followup.returncode:
00307:                 out['status']='UPDATE_FAILED'
00308:                 out['reason']='POSTINSTALL_FOLLOWUP_FAILED'
00309:     except Exception as exc:
00310:         out['postinstall_phase']='FAILED'
00311:         out['self_update_phase']='DEFERRED'
00312:         out['status']='UPDATE_FAILED'
...
00334:             if not args.updater_root or not args.config:
00335:                 raise ValueError('--updater-root and --config required')
00336:             result = cycle(Path(args.updater_root), Path(args.config),
00337:                            scheduled=args.scheduled,apply_after_exit=args.apply_after_exit)
00338:         print(json.dumps(result, ensure_ascii=False, indent=2))
00339:         return 0 if result.get('status') not in ('BLOCKED', 'UPDATE_FAILED') else int(result.get('update_returncode') or result.get('followup_returncode') or 1)
00340:     except Exception as e:
00341:         print(json.dumps({'status':'BLOCKED','reason':str(e)},ensure_ascii=False),file=sys.stderr)
00342:         return 1
00343:
00344: if __name__ == '__main__':
00345:     sys.exit(main())
```

## `skill-updater_v0_5_44_1027/scripts/skill_updater.py`
- total lines: 7599
- matching lines: 138
- related functions: `_job_list_version_changed` at 5059–5068, `run_job_list_post_update` at 5071–5138
```python
...
00018: import platform
00019: import re
00020: import shutil
00021: import ssl
00022: import stat
00023: import subprocess
00024: import sys
00025: import tempfile
00026: import threading
00027: import time
00028: import traceback
00029: import urllib.error
...
00034: from dataclasses import dataclass, asdict
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
...
00148:         code, disposition, retryable = "PACKAGE_HASH_MISMATCH", "BLOCKED", False
00149:     elif "self-check" in low or "self_check" in low:
00150:         code, disposition, retryable = "PACKAGE_SELF_CHECK_FAILED", "BLOCKED", False
00151:     elif "skillsilent" in low and ("contract" in low or "policy" in low or "registration" in low or "후처리" in text):
00152:         code, disposition, retryable = "SKILLSILENT_CONTRACT_OR_REGISTRATION_FAILED", "BLOCKED", False
00153:     elif "http 429" in low or "http 5" in low or "timed out" in low or "timeout" in low or "temporary" in low:
00154:         code, disposition, retryable = "NETWORK_TRANSIENT", "RETRYABLE", True
00155:     elif "proxy" in low and ("failed" in low or "오류" in text):
00156:         code, disposition, retryable = "PROXY_TRANSIENT", "RETRYABLE", True
00157:     elif "lock" in low or "사용 중" in text or "진행 중" in text:
00158:         code, disposition, retryable = "FILE_LOCKED", "RETRYABLE", True
00159:     elif "rollback" in low or "복구" in text:
...
00279:
00280: def _managed_log_entries(root: Path) -> list[Path]:
00281:     """Return every top-level artifact in the updater-owned log directory.
00282:
00283:     The directory is dedicated to updater logs.  A normal periodic execution
00284:     creates both launch logs and run directories, so all top-level artifacts
00285:     share one quota rather than retaining ten entries per filename pattern.
00286:     """
00287:     if not root.is_dir():
00288:         return []
00289:     return [path for path in root.iterdir()]
00290:
...
00475:             debug_event("HEARTBEAT", **payload)
00476:             if emit:
00477:                 print(self._display(), flush=True)
00478:
00479:     def _loop(self) -> None:
00480:         while not self._stop.wait(self.interval):
00481:             try:
00482:                 self._write(emit=True)
00483:             except Exception as exc:
00484:                 debug_event("HEARTBEAT_ERROR", error=str(exc))
00485:
00486:     def start(self) -> None:
...
00501:         self._write(emit=emit)
00502:
00503:     def finish(self, status: str, detail: str = "") -> None:
00504:         self._stop.set()
00505:         if self._thread.is_alive():
00506:             self._thread.join(timeout=min(2, self.interval))
00507:         with self._lock:
00508:             self.status = status
00509:             self.stage = "COMPLETED" if status in ("SUCCESS", "PARTIAL_SUCCESS") else status
00510:             self.detail = detail
00511:         self._write(emit=False)
00512:
...
00548:             if emit:
00549:                 elapsed=int(time.monotonic()-self.started)
00550:                 print(f"[RUNNING 00:{elapsed//60:02d}:{elapsed%60:02d}] {self.stage} - {self.detail}", flush=True)
00551:
00552:     def _loop(self) -> None:
00553:         while not self._stop.wait(self.interval):
00554:             try: self._write(True)
00555:             except Exception as exc: debug_event("BOOTSTRAP_HEARTBEAT_ERROR", error=str(exc))
00556:
00557:     def start(self) -> None:
00558:         self._write(True)
00559:         self._thread.start()
...
00563:             self.stage, self.detail = stage, detail
00564:         self._write(True)
00565:
00566:     def stop(self) -> None:
00567:         self._stop.set()
00568:         if self._thread.is_alive(): self._thread.join(timeout=1)
00569:
00570:
00571: _BOOTSTRAP_HEARTBEAT: StartupHeartbeat | None = None
00572:
00573:
00574: @dataclass
...
01233:     canonical_runtime = canonical_updater_runtime_dir(private_root)
01234:     cfg["_legacy_download_dir"] = str(legacy_download)
01235:     cfg["download_dir"] = str(canonical_runtime)
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
...
01401:         errors.append("execution은 object여야 합니다")
01402:     else:
01403:         for key in ("continue_on_error", "resume_previous"):
01404:             if key in execution and not isinstance(execution.get(key), bool):
01405:                 errors.append(f"execution.{key}는 boolean이어야 합니다")
01406:     # Obsolete job_sync input is tolerated by the lightweight loader but never normalized
01407:     # into runtime behavior. One-shot Job lifecycle belongs to the installed Job-list itself.
01408:     return errors
01409:
01410:
01411: def token_from_config(cfg: dict[str, Any]) -> str | None:
01412:     env_name = str((cfg.get("source") or {}).get("token_env") or "GITHUB_TOKEN")
01413:     return os.environ.get(env_name) or None
...
01470:     _assert_vcs_read_only_command(command)
01471:     env = dict(kwargs.get("env") or os.environ)
01472:     env.setdefault("SKILL_UPDATER_VCS_READ_ONLY", "1")
01473:     env.setdefault("GIT_OPTIONAL_LOCKS", "0")
01474:     kwargs["env"] = env
01475:     return subprocess.run(command, *args, **kwargs)
01476:
01477:
01478: def _run_process_streaming(command: list[str], *, cwd: str | None = None, timeout: int = 900,
01479:                            log_path: Path | None = None, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
01480:     """Stream child stdout/stderr immediately while retaining a bounded transcript."""
01481:     _assert_vcs_read_only_command(command)
01482:     child_env = dict(os.environ if env is None else env)
01483:     child_env.setdefault("PYTHONUTF8", "1")
01484:     child_env["PYTHONIOENCODING"] = "utf-8"
01485:     popen_kwargs: dict[str, Any] = {
01486:         "cwd": cwd, "env": child_env, "stdin": subprocess.DEVNULL,
01487:         "stdout": subprocess.PIPE, "stderr": subprocess.PIPE, "text": True,
01488:         "encoding": "utf-8", "errors": "replace", "bufsize": 1,
01489:     }
01490:     if os.name == "nt": popen_kwargs["creationflags"] = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
01491:     else: popen_kwargs["start_new_session"] = True
01492:     proc = subprocess.Popen(command, **popen_kwargs)
01493:     out: list[str] = []; err: list[str] = []; lock = threading.Lock()
01494:     log_handle = None
01495:     if log_path is not None:
01496:         log_path.parent.mkdir(parents=True, exist_ok=True)
01497:         log_handle = log_path.open("a", encoding="utf-8", buffering=1)
01498:         log_handle.write("$ " + subprocess.list2cmdline(command) + "\n")
01499:     def drain(stream, bucket, destination):
01500:         try:
01501:             for line in iter(stream.readline, ""):
01502:                 with lock: bucket.append(line)
01503:                 destination.write(line); destination.flush()
01504:                 if log_handle is not None: log_handle.write(line); log_handle.flush()
...
01507:             except Exception: pass
01508:     threads = [threading.Thread(target=drain, args=(proc.stdout, out, sys.stdout), daemon=True),
01509:                threading.Thread(target=drain, args=(proc.stderr, err, sys.stderr), daemon=True)]
01510:     for t in threads: t.start()
01511:     try:
01512:         proc.wait(timeout=timeout)
01513:     except subprocess.TimeoutExpired:
01514:         try:
01515:             if os.name == "nt": subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
01516:             else: os.killpg(os.getpgid(proc.pid), 15)
01517:         except Exception:
01518:             proc.kill()
01519:         proc.wait(timeout=10)
01520:         err.append(f"timeout after {timeout}s\n")
01521:     for t in threads: t.join(timeout=2)
01522:     if log_handle is not None: log_handle.close()
01523:     return subprocess.CompletedProcess(command, proc.returncode if proc.returncode is not None else 124, "".join(out), "".join(err))
01524:
01525:
01526: def _audit_self_check_vcs(root: Path) -> None:
01527:     script = root / "scripts" / "self_check.py"
01528:     if not script.is_file():
01529:         return
...
01539:
01540: def _git_proxy() -> str | None:
01541:     try:
01542:         result = _run_process(
01543:             ["git", "config", "--global", "--get", "http.proxy"],
01544:             capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=10,
01545:         )
01546:         value = (result.stdout or "").strip()
01547:         return value or None
01548:     except Exception:
01549:         return None
01550:
...
01775:         else:
01776:             current = getattr(current, "__cause__", None) or getattr(current, "__context__", None)
01777:     return False
01778:
01779:
01780: def _open_url(cfg: dict[str, Any], request: urllib.request.Request, timeout: int):
01781:     method = request.get_method().upper()
01782:     if method not in {"GET", "HEAD"} or request.data is not None:
01783:         raise UpdateError(f"GitHub read-only 정책 위반: HTTP {method}")
01784:     original_url = request.full_url
01785:     original_data = request.data
01786:     original_headers = dict(request.header_items())
...
01804:             fresh_request = urllib.request.Request(
01805:                 original_url, data=original_data, headers=original_headers, method=original_method
01806:             )
01807:             tls_label = "verified" if verify else "insecure"
01808:             try:
01809:                 response = opener.open(fresh_request, timeout=timeout)
01810:                 routes = _transient_list(cfg, "_network_routes_used")
01811:                 route_key = f"{label}/{tls_label}"
01812:                 if route_key not in routes:
01813:                     routes.append(route_key)
01814:                 _remember_network_success(cfg, tls_verify=verify, route=label)
01815:                 return response, label
...
01842:     suffix = " (인증서 검증 오류 감지)" if cert_failure_seen else ""
01843:     raise UpdateError("GitHub 연결 실패" + suffix + ": " + " | ".join(errors))
01844:
01845:
01846: def http_bytes(cfg: dict[str, Any], url: str, token: str | None = None, accept: str | None = None,
01847:                timeout: int = DEFAULT_TIMEOUT) -> bytes:
01848:     if timeout == DEFAULT_TIMEOUT:
01849:         timeout = int((cfg.get("network") or {}).get("connect_timeout_sec", DEFAULT_TIMEOUT))
01850:     _record_github_request(cfg, url)
01851:     headers = {"User-Agent": USER_AGENT, "X-GitHub-Api-Version": "2022-11-28"}
01852:     if accept:
01853:         headers["Accept"] = accept
01854:     if token:
01855:         headers["Authorization"] = f"Bearer {token}"
01856:     request = urllib.request.Request(url, headers=headers)
01857:     response = None
01858:     try:
01859:         response, _ = _open_url(cfg, request, timeout)
01860:         with response:
01861:             return response.read()
01862:     except UpdateError:
01863:         raise
01864:     except Exception as exc:
01865:         raise UpdateError(f"GitHub 요청 실패: {url}: {exc}")
01866:
01867:
01868: def http_download(cfg: dict[str, Any], url: str, destination: Path, token: str | None = None,
01869:                   accept: str | None = None, timeout: int = 180) -> None:
01870:     _record_github_request(cfg, url)
01871:     headers = {"User-Agent": USER_AGENT, "X-GitHub-Api-Version": "2022-11-28"}
01872:     if accept:
01873:         headers["Accept"] = accept
01874:     if token:
01875:         headers["Authorization"] = f"Bearer {token}"
01876:     request = urllib.request.Request(url, headers=headers)
01877:     destination.parent.mkdir(parents=True, exist_ok=True)
01878:     try:
01879:         response, _ = _open_url(cfg, request, timeout)
01880:         with response, destination.open("wb") as out:
01881:             while True:
01882:                 chunk = response.read(1024 * 1024)
01883:                 if not chunk:
01884:                     break
01885:                 out.write(chunk)
...
03128:         if release is None:
03129:             raise UpdateError("Release 정보가 없습니다")
03130:         asset = release_asset(release, decision.asset)
03131:         asset_url = str(asset.get("browser_download_url") or asset["url"])
03132:         http_download(cfg, asset_url, part, token_from_config(cfg), "application/octet-stream",
03133:                       timeout=int((cfg.get("network") or {}).get("download_timeout_sec", 300)))
03134:     else:
03135:         # Root/contents discovery already returned an immutable blob SHA. Use
03136:         # the non-API download URL so installing N skills does not consume N
03137:         # GitHub REST requests.
03138:         url = decision.download_url or github_raw_url(cfg, decision.asset)
03139:         http_download(cfg, url, part, token_from_config(cfg),
03140:                       timeout=int((cfg.get("network") or {}).get("download_timeout_sec", 300)))
03141:     actual_sha256 = sha256_file(part)
03142:     if decision.sha256 and actual_sha256 != decision.sha256:
03143:         part.unlink(missing_ok=True)
03144:         raise UpdateError(
03145:             f"SHA-256 불일치: {decision.name}: expected={decision.sha256} actual={actual_sha256}"
03146:         )
...
03202:         return
03203:     script = root / "scripts" / "self_check.py"
03204:     if not script.is_file():
03205:         return
03206:     verification = cfg.get("verification") or {}
03207:     timeout = int(verification.get("self_check_timeout_sec", 600))
03208:     if os.environ.get("SKILL_UPDATER_UNATTENDED") == "1" and not verification.get("allow_unattended_self_check", False):
03209:         output_log.parent.mkdir(parents=True, exist_ok=True)
03210:         output_log.write_text("SKIPPED: arbitrary package self_check.py is not executed in unattended mode.\n", encoding="utf-8")
03211:         return
03212:     _audit_self_check_vcs(root)
03213:     text = script.read_text(encoding="utf-8", errors="replace")
03214:     command = [sys.executable, "-u", str(script)]
03215:     if "--mode" in text and ("package" in text or "choices=(\"package\"" in text):
03216:         command += ["--mode", "package"]
03217:     result = _run_process_streaming(
03218:         command, cwd=str(root), timeout=timeout, log_path=output_log,
03219:         env={**os.environ, "PYTHONUNBUFFERED": "1"},
03220:     )
03221:     combined = (result.stdout or "") + (result.stderr or "")
03222:     if result.returncode != 0:
03223:         tail = " | ".join(combined.splitlines()[-20:])[-3000:] or "<no output>"
03224:         raise ClassifiedUpdateError(
03225:             f"self-check 실패 rc={result.returncode}: {root.name}; last_output={tail}; log={output_log}",
03226:             failure_code="PACKAGE_SELF_CHECK_FAILED", disposition="BLOCKED", retryable=False,
03227:             stage="PACKAGE_SELF_CHECK", log_path=str(output_log),
03228:         )
03229:
03230:
03231: def run_environment_check(root: Path, cfg: dict[str, Any], output_log: Path) -> list[str]:
...
03236:     text = script.read_text(encoding="utf-8", errors="replace")
03237:     if "--mode" not in text or "environment" not in text:
03238:         return []
03239:     result = _run_process_streaming(
03240:         [sys.executable, "-u", str(script), "--mode", "environment"],
03241:         cwd=str(root), timeout=120, log_path=output_log,
03242:         env={**os.environ, "PYTHONUNBUFFERED": "1"},
03243:     )
03244:     combined = (result.stdout or "") + (result.stderr or "")
03245:     warning_status = False
03246:     for line in combined.splitlines():
03247:         try:
...
03249:         except Exception:
03250:             continue
03251:         if isinstance(payload, dict) and str(payload.get("status") or "").upper() in ("SKIPPED", "WARN", "WARNING"):
03252:             warning_status = True
03253:             break
03254:     if result.returncode == 0 and not warning_status:
03255:         return []
03256:     tail = " | ".join(combined.splitlines()[-10:])[-1500:] or "environment check warning"
03257:     return [f"ENVIRONMENT_PREREQUISITE_MISSING: {tail}; log={output_log}"]
03258:
03259: def _rel_paths(root: Path) -> list[str]:
03260:     """Return relative regular-file paths without reading file contents.
...
03849:     if os.name == "nt":
03850:         binary = shutil.which("schtasks.exe") or shutil.which("schtasks")
03851:         if not binary:
03852:             return tasks
03853:         result = _run_process([binary, "/Query", "/FO", "CSV", "/NH"], capture_output=True,
03854:                                 text=True, encoding="utf-8", errors="replace", timeout=60)
03855:         if result.returncode != 0:
03856:             return tasks
03857:         names: dict[str, str] = {}
03858:         for row in csv.reader(result.stdout.splitlines()):
03859:             if not row:
03860:                 continue
03861:             full_name = row[0]
03862:             name = full_name.replace("\\", "/").rsplit("/", 1)[-1]
03863:             if name.lower().startswith("autotask-"):
03864:                 names[name[len("autotask-"):]] = full_name
03865:         for tid, full_name in names.items():
03866:             query = _run_process([binary, "/Query", "/TN", full_name, "/XML"], capture_output=True,
03867:                                    text=True, encoding="utf-8", errors="replace", timeout=30)
03868:             enabled = True
03869:             if query.returncode == 0:
03870:                 match = re.search(r"<Enabled>\s*(true|false)\s*</Enabled>", query.stdout, re.IGNORECASE)
03871:                 if match:
03872:                     enabled = match.group(1).lower() == "true"
03873:             tasks[tid] = enabled
03874:         return tasks
03875:     systemctl = shutil.which("systemctl")
03876:     if not systemctl:
03877:         return tasks
03878:     result = _run_process([systemctl, "--user", "list-unit-files", "autotask-*.timer", "--no-legend", "--no-pager"],
03879:                             capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
03880:     if result.returncode != 0:
03881:         return tasks
03882:     for line in result.stdout.splitlines():
03883:         unit = line.split()[0] if line.split() else ""
03884:         if unit.startswith("autotask-") and unit.endswith(".timer"):
03885:             tid = unit[len("autotask-"):-len(".timer")]
03886:             status = _run_process([systemctl, "--user", "is-enabled", unit], capture_output=True,
03887:                                     text=True, encoding="utf-8", errors="replace", timeout=30)
03888:             tasks[tid] = status.returncode == 0 and status.stdout.strip() in ("enabled", "enabled-runtime", "linked")
03889:     return tasks
03890:
03891:
03892: def rebind_migrated_autotasks(cfg: dict[str, Any], task_paths: Iterable[str],
03893:                               registered_before: dict[str, bool] | set[str], log_path: Path) -> None:
03894:     states = ({key: True for key in registered_before} if isinstance(registered_before, set)
...
03913:     commands: list[list[str]] = []
03914:     for task, _tid in selected:
03915:         commands.append([sys.executable, str(render), str(task), "--out", str(rendered), "--platform", "auto"])
03916:     with log_path.open("w", encoding="utf-8") as log:
03917:         for cmd in commands:
03918:             result = _run_process(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300)
03919:             log.write("$ " + subprocess.list2cmdline(cmd) + "\n" + result.stdout + result.stderr + "\n")
03920:             if result.returncode != 0:
03921:                 raise UpdateError(f"autotask main 경로 렌더 실패 rc={result.returncode}; log={log_path}")
03922:         units = sorted(str(path) for path in rendered.glob("autotask-*"))
03923:         if not units:
03924:             raise UpdateError(f"autotask main 경로 렌더 결과가 없습니다: {rendered}")
03925:         cmd = [sys.executable, str(deploy)] + units + ["--yes", "--platform", "auto"]
03926:         result = _run_process(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300)
03927:         log.write("$ " + subprocess.list2cmdline(cmd) + "\n" + result.stdout + result.stderr + "\n")
03928:         if result.returncode != 0:
03929:             raise UpdateError(f"기존 autotask main 경로 재등록 실패 rc={result.returncode}; log={log_path}")
03930:         disabled = [tid for _task, tid in selected if not states.get(tid, True)]
03931:         for tid in disabled:
03932:             if os.name == "nt":
03933:                 binary = shutil.which("schtasks.exe") or shutil.which("schtasks") or "schtasks.exe"
03934:                 disable_cmd = [binary, "/Change", "/TN", f"autotask-{tid}", "/DISABLE"]
03935:             else:
03936:                 systemctl = shutil.which("systemctl") or "systemctl"
03937:                 disable_cmd = [systemctl, "--user", "disable", f"autotask-{tid}.timer"]
03938:             disabled_result = _run_process(disable_cmd, capture_output=True, text=True,
03939:                                              encoding="utf-8", errors="replace", timeout=60)
03940:             log.write("$ " + subprocess.list2cmdline(disable_cmd) + "\n" +
03941:                       disabled_result.stdout + disabled_result.stderr + "\n")
03942:             if disabled_result.returncode != 0:
03943:                 raise UpdateError(f"기존 autotask 비활성 상태 복원 실패: {tid}; log={log_path}")
03944:
03945:
03946: def _main_autotask_task_paths(cfg: dict[str, Any]) -> list[str]:
03947:     # Historical function name retained for API compatibility; active tasks are canonical private data.
03948:     private_root = _cfg_private_root(cfg)
...
04044:     normalized = current.replace("\\", "/")
04045:     script_text = str(script).replace("\\", "/")
04046:     output_contract_current = (
04047:         "update_result.json" in current
04048:         and "update_report.md" in current
04049:         and "job_sync_result.json" not in current
04050:     )
04051:     already_canonical = (
04052:         script_text in normalized
04053:         and "--yes" in current
04054:         and "skillsilent" not in current.lower()
04055:         and "claude_once" not in current.lower()
...
04548:             sys.executable, str(installer),
04549:             "--dest", str(canonical),
04550:             "--entry", str(entry),
04551:         ]
04552:         proc = _run_process_streaming(
04553:             command, cwd=str(root), timeout=900,
04554:             log_path=_target_log(cfg, str(cfg.get("_active_run_id") or "adhoc"), "install", decision.name),
04555:             env={**os.environ, "PYTHONUNBUFFERED": "1"},
04556:         )
04557:         if proc.returncode != 0:
04558:             tail = " | ".join(((proc.stdout or "") + (proc.stderr or "")).splitlines()[-30:])[-4000:]
04559:             raise ClassifiedUpdateError(
04560:                 f"canonical package installer failed rc={proc.returncode}; last_output={tail}",
04561:                 failure_code="CANONICAL_INSTALLER_FAILED", disposition="BLOCKED",
04562:                 retryable=False, stage="CANONICAL_INSTALLER",
04563:             )
04564:
04565:         if not (canonical / "SKILL.md").is_file():
04566:             raise ClassifiedUpdateError(
...
04656:     root = canonical if (canonical/'l1_fix_workflow'/'provider_bootstrap.py').is_file() else entry
04657:     required = root/'l1_fix_workflow'/'provider_bootstrap.py'
04658:     if not required.is_file():
04659:         return {"result":"WORKFLOW_BOOTSTRAP_UNAVAILABLE", "next_action":"Install updated l1-fix-workflow through its approved company GitHub deployment path"}
04660:     policy = Path.home()/'.l1-ledger'/'provider_bootstrap_policy.json'
04661:     # No approval file means no writes and no subprocess invocation.
04662:     if not policy.is_file():
04663:         return {"result":"PENDING_APPROVAL", "next_action":"Run installed l1-fix-workflow provider-onboard --approve once in an authorized in-house Linux session; then updater can reconcile automatically"}
04664:     env={**os.environ,'L1_WORKFLOW_INSTALL_CONTEXT':'SKILL_UPDATER_POST_INSTALL'}
04665:     # Target only the installed Workflow package, not current working directory.
04666:     env['PYTHONPATH']=str(root)
04667:     try:
04668:         proc=subprocess.run([sys.executable,'-B','-m','l1_fix_workflow','provider-bootstrap',
04669:                              '--policy',str(policy),'--apply'],
04670:                             cwd=str(root),env=env,stdin=subprocess.DEVNULL,
04671:                             capture_output=True,text=True,timeout=90,check=False)
04672:         if proc.returncode:
04673:             try:
04674:                 failed=json.loads((proc.stdout or '').strip())
04675:                 reason=str(failed.get('reason') or 'PROVIDER_BOOTSTRAP_FAILED')[:240]
04676:             except (ValueError,TypeError):
04677:                 reason='PROVIDER_BOOTSTRAP_FAILED'
04678:             return {"result":"BLOCKED","reason":reason,
04679:                     "returncode":proc.returncode}
04680:         obj=json.loads(proc.stdout.strip())
04681:         return {"result":str(obj.get('result') or 'UNKNOWN'),
04682:                 "applied":obj.get('applied') is True,
04683:                 "runner_executed":False,
04684:                 "next_action":"Issue explicit analyze-code request with function name, then check actual provider receipt and Evidence"}
04685:     except (OSError,subprocess.TimeoutExpired,ValueError,json.JSONDecodeError) as exc:
04686:         return {"result":"BLOCKED","reason":type(exc).__name__}
04687:
04688:
04689: def install_candidate(cfg: dict[str, Any], decision: Decision, archive: Path,
04690:                       prepared: PreparedCandidate | None = None) -> Applied:
04691:     download_dir = Path(cfg["download_dir"])
...
04897:         shutil.copytree(runtime_root, snapshot)
04898:
04899:     command = _skillsilent_installer_command(shell, script, runtime_root)
04900:     try:
04901:         result = _run_process_streaming(
04902:             command, cwd=str(root), timeout=900, log_path=log_path,
04903:             env={**os.environ, "PYTHONUNBUFFERED": "1"},
04904:         )
04905:         if result.returncode != 0:
04906:             tail = " | ".join(((result.stdout or "") + (result.stderr or "")).splitlines()[-20:])[-3000:]
04907:             raise ClassifiedUpdateError(
04908:                 f"skillsilent installer 실패 rc={result.returncode}; last_output={tail}",
04909:                 failure_code="SKILLSILENT_INSTALLER_FAILED", disposition="BLOCKED",
04910:                 retryable=False, stage="SKILLSILENT_INSTALLER", log_path=str(log_path) if log_path else None,
04911:             )
04912:     except BaseException as install_exc:
04913:         try:
04914:             _restore_runtime_snapshot(runtime_root, snapshot if existed else None, existed)
...
04966:         target = str(Path(item.target).resolve())
04967:         commands.append(executable + ["reconcile-skill", target, "--yes", "--json"])
04968:     if include_doctor and post.get("doctor", True):
04969:         commands.append(executable + ["doctor"])
04970:     for command in commands:
04971:         result = _run_process_streaming(command, timeout=900, log_path=log_path,
04972:                                         env={**os.environ, "PYTHONUNBUFFERED": "1"})
04973:         if result.returncode != 0:
04974:             tail = " | ".join(((result.stdout or "") + (result.stderr or "")).splitlines()[-20:])[-3000:]
04975:             raise ClassifiedUpdateError(
04976:                 f"skillsilent 대상별 후처리 실패 rc={result.returncode}; last_output={tail}; log={log_path}",
04977:                 failure_code="SKILLSILENT_REGISTRATION_FAILED", disposition="BLOCKED", retryable=False,
04978:                 stage="SKILLSILENT_RECONCILE", log_path=str(log_path),
04979:             )
04980:
04981:
04982:
...
05054:         log_root, DEBUG_LOG_KEEP,
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
```

## `skill-updater_v0_5_44_1027/scripts/skill_updater_auto.py`
- total lines: 153
- matching lines: 2
- related functions:
```python
...
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
```

## `skill-updater_v0_5_44_1027/tests/test_v0528_job_list_post_update.py`
- total lines: 83
- matching lines: 26
- related functions: `make_job_list` at 15–22, `test_unchanged_job_list_still_activates_for_retry` at 37–42, `test_same_version_reinstall_still_activates_for_retry` at 45–50, `test_missing_job_list_after_version_change_is_nonblocking_noop` at 53–55, `test_changed_job_list_is_called_once_with_activate_launch` at 58–67, `test_job_list_failure_does_not_raise` at 70–74, `test_legacy_job_sync_config_still_not_required` at 77–83
```python
...
00010: def cfg_for(tmp_path: Path) -> dict:
00011:     private = tmp_path / "l1sw-private-skills"
00012:     return {"private_install_root": str(private), "install_root": str(tmp_path / "discovery")}
00013:
00014:
00015: def make_job_list(tmp_path: Path, body: str):
00016:     cfg = cfg_for(tmp_path)
00017:     root = Path(cfg["private_install_root"]) / "job-list"
00018:     (root / "bin").mkdir(parents=True)
00019:     (root / "requests").mkdir(parents=True)
00020:     (root / "bin" / "job-list-core.py").write_text(body, encoding="utf-8")
00021:     (root / "requests" / "one-shot-jobs.json").write_text('{"schema_version":1,"jobs":[]}', encoding="utf-8")
00022:     return cfg, root
00023:
00024:
00025: def changed(old="0.3.51", new="0.3.52"):
00026:     return [SU.TargetOutcome("job-list", "UPDATED", "UPDATE", installed_version=old, remote_version=new)]
00027:
00028:
00029: def unchanged():
00030:     return [SU.TargetOutcome("job-list", "SKIPPED", "LATEST", installed_version="0.3.52", remote_version="0.3.52")]
00031:
00032:
00033: def same_version_updated():
00034:     return [SU.TargetOutcome("job-list", "UPDATED", "UPDATE", installed_version="0.3.52", remote_version="0.3.52")]
00035:
00036:
00037: def test_unchanged_job_list_still_activates_for_retry(tmp_path):
00038:     body = 'from pathlib import Path\nPath("called.txt").write_text("yes")\n'
00039:     cfg, root = make_job_list(tmp_path, body)
00040:     result = SU.run_job_list_post_update(cfg, unchanged())
00041:     assert result["status"] == "CALLED"
00042:     assert (root / "called.txt").exists()
00043:
00044:
00045: def test_same_version_reinstall_still_activates_for_retry(tmp_path):
00046:     body = 'from pathlib import Path\nPath("called.txt").write_text("yes")\n'
00047:     cfg, root = make_job_list(tmp_path, body)
00048:     result = SU.run_job_list_post_update(cfg, same_version_updated())
00049:     assert result["status"] == "CALLED"
00050:     assert (root / "called.txt").exists()
00051:
00052:
00053: def test_missing_job_list_after_version_change_is_nonblocking_noop(tmp_path):
00054:     result = SU.run_job_list_post_update(cfg_for(tmp_path), changed())
00055:     assert result["status"] == "NOT_AVAILABLE"
00056:
00057:
00058: def test_changed_job_list_is_called_once_with_activate_launch(tmp_path):
00059:     body = 'import json,sys\nfrom pathlib import Path\nPath("called.json").write_text(json.dumps(sys.argv[1:]))\n'
00060:     cfg, root = make_job_list(tmp_path, body)
00061:     result = SU.run_job_list_post_update(cfg, changed())
00062:     assert result["status"] == "CALLED"
00063:     args = json.loads((root / "called.json").read_text())
00064:     assert args[0] == "activate"
00065:     assert "--launch" in args
00066:     assert "--root" in args
00067:     assert "--source" in args
00068:
00069:
00070: def test_job_list_failure_does_not_raise(tmp_path):
00071:     cfg, _ = make_job_list(tmp_path, 'import sys\nsys.exit(9)\n')
00072:     result = SU.run_job_list_post_update(cfg, changed())
00073:     assert result["status"] == "FAILED_NONBLOCKING"
00074:     assert result["returncode"] == 9
00075:
00076:
00077: def test_legacy_job_sync_config_still_not_required(tmp_path):
00078:     private = tmp_path / "private"
00079:     cfg_path = tmp_path / "cfg.json"
00080:     cfg = {"schema_version":1,"source":{"provider":"github","repository":"o/r","mode":"auto"},"download_dir":str(tmp_path/"runtime"),"install_root":str(private),"targets":[{"name":"job-list","enabled":True}],"job_sync":{"enabled":False}}
00081:     cfg_path.write_text(json.dumps(cfg), encoding="utf-8")
00082:     normalized = SU.normalized_config(cfg_path)
00083:     assert "job_sync" not in normalized
```

## `skill-updater_v0_5_44_1027/tests/test_v0533_job_list_rescue_activation.py`
- total lines: 17
- matching lines: 4
- related functions: `test_post_update_no_longer_has_skip_version_gate` at 13–17
```python
...
00005: spec = importlib.util.spec_from_file_location("su533", ROOT / "scripts" / "skill_updater.py")
00006: m = importlib.util.module_from_spec(spec); sys.modules[spec.name] = m; spec.loader.exec_module(m)
00007:
00008: def test_rescue_feature_flags():
00009:     assert m.VERSION == (ROOT / "VERSION").read_text(encoding="utf-8").strip()
00010:     assert m.JOBLIST_ACTIVATION_EVERY_CYCLE is False
00011:     assert m.JOBLIST_ROOT_ZIP_FRESH_DISCOVERY is True
00012:
00013: def test_post_update_no_longer_has_skip_version_gate():
00014:     src = (ROOT / "scripts" / "skill_updater.py").read_text(encoding="utf-8")
00015:     body = src[src.index("def run_job_list_post_update"):src.index("def report_paths")]
00016:     assert "SKIPPED_NO_VERSION_CHANGE" not in body
00017:     assert "SCHEDULED_ENTRY_ONLY" in body
```

## `skill-updater_v0_5_44_1027/tests/test_v0538_mcp_self_update.py`
- total lines: 104
- matching lines: 2
- related functions:
```python
...
00089:     (scripts/'skill_updater_auto.py').write_text('')
00090:     cfg=tmp_path/'skill-updater.json';cfg.write_text('{}')
00091:     seen=[]
00092:     def fake_run(argv,**kwargs):
00093:         seen.append(argv)
00094:         return SimpleNamespace(returncode=0)
00095:     monkeypatch.setattr(boot.subprocess,'run',fake_run)
00096:     direct=boot.cycle(root,cfg,scheduled=False,apply_after_exit=False)
00097:     scheduled=boot.cycle(root,cfg,scheduled=True,apply_after_exit=False)
00098:     assert direct['status']=='UPDATE_COMPLETED'
00099:     assert scheduled['status']=='UPDATE_COMPLETED'
00100:     assert direct['self_update_phase']=='NONE'
00101:     assert len(seen)==2
```\n