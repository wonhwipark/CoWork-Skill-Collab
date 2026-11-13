#!/usr/bin/env python3
"""GET-only GitHub credential precheck; never certifies a token's full permissions.

Exit 1: a check failed. Exit 2: GET checks passed but grant policy is NOT_PROVEN.
This diagnostic intentionally never returns 0 for credential/installation readiness.
Verify selected repositories and all permission grants in GitHub settings separately.
No token value, response body, credential path or exception text is printed.
"""
import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

API = "https://api.github.com"
MAX_EXPIRY_DAYS = 90
MAX_BODY = 1024 * 1024
PASS, FAIL, NOT_PROVEN = "PASS", "FAIL", "NOT_PROVEN"
REPO = re.compile(r"[A-Za-z0-9][A-Za-z0-9-]*/[A-Za-z0-9_.-]+\Z")


class ProbeError(Exception):
    pass


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def urllib_http(method, url, headers, body=None):
    target = urllib.parse.urlsplit(url)
    if (method != "GET" or body is not None or target.scheme != "https"
            or target.netloc != "api.github.com" or target.fragment):
        raise ProbeError("request refused")
    opener = urllib.request.build_opener(NoRedirect())
    request = urllib.request.Request(url, method="GET", headers=headers)
    try:
        response = opener.open(request, timeout=30)
    except urllib.error.HTTPError as exc:
        with exc:
            return exc.code, {k.lower(): v for k, v in exc.headers.items()}, b""
    with response:
        data = response.read(MAX_BODY + 1)
        if len(data) > MAX_BODY:
            raise ProbeError("oversized response")
        return response.status, {k.lower(): v for k, v in response.headers.items()}, data


def expiry_time(value):
    # GitHub's documented expiration header, plus ISO-8601 UTC timestamps.
    try:
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S UTC").replace(tzinfo=timezone.utc)
    except ValueError:
        stamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if stamp.tzinfo is None:
            raise ValueError("timezone missing")
        return stamp.astimezone(timezone.utc)


def check(token, repo, branch="main", http=None, today=None):
    http = http or urllib_http
    results = []

    def add(name, state, detail=""):
        results.append((name, state, detail))

    if (not isinstance(repo, str) or not REPO.fullmatch(repo)
            or repo.split("/")[1] in {".", ".."}
            or not isinstance(branch, str) or not branch or len(branch) > 255
            or any(ord(c) < 32 for c in branch)):
        return [("input", FAIL, "invalid repository or branch")]
    if (not isinstance(token, str) or len(token) > 512
            or not re.fullmatch(r"github_pat_[A-Za-z0-9_]+", token)):
        return [("token_type", FAIL, "fine-grained PAT required")]
    add("token_type", PASS, "prefix/format only; grants not established")
    headers = {"Authorization": "Bearer " + token, "Accept": "application/vnd.github+json",
               "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "cowork-token-precheck-r0002"}

    def get(path):
        status, hdrs, data = http("GET", API + path, headers)
        return status, {str(k).lower(): v for k, v in hdrs.items()}, data

    try:
        status, hdrs, _ = get("/user")
        add("authentication", PASS if status == 200 else FAIL, "HTTP " + str(status))
        if status != 200:
            return results
        add("classic_scopes_absent", FAIL if hdrs.get("x-oauth-scopes", "").strip() else PASS,
            "not a proof of fine-grained permission limits")
        try:
            now = today or datetime.now(timezone.utc)
            remaining = expiry_time(hdrs.get("github-authentication-token-expiration", "")) - now
            valid = timedelta(0) < remaining <= timedelta(days=MAX_EXPIRY_DAYS)
        except (ValueError, TypeError, OverflowError):
            valid = False
        add("expiry_within_90_days", PASS if valid else FAIL,
            "strict timestamp check; missing/expired/over-limit is FAIL")

        status, hdrs, data = get("/user/repos?visibility=private&per_page=100&page=1")
        visible_ok = False
        if status == 200:
            try:
                repos = json.loads(data)
                visible_ok = (isinstance(repos, list) and len(repos) == 1
                              and isinstance(repos[0], dict) and repos[0].get("private") is True
                              and repos[0].get("full_name", "").casefold() == repo.casefold()
                              and not hdrs.get("link"))
            except (ValueError, TypeError, AttributeError, UnicodeError):
                pass
        add("observed_private_repository_set", PASS if visible_ok else FAIL,
            "one expected private repository, no pagination; not a grant inventory")

        ref = urllib.parse.quote(branch, safe="")
        status, _, data = get(f"/repos/{repo}/contents/collab/START_HERE.md?ref={ref}")
        read_ok = False
        if status == 200:
            try:
                item = json.loads(data)
                read_ok = isinstance(item, dict) and item.get("type") == "file"
            except (ValueError, TypeError, UnicodeError):
                pass
        add("contents_read", PASS if read_ok else FAIL, "HTTP " + str(status))
    except Exception:
        # Network/injected transport errors may embed credentials. Do not echo them.
        add("transport", FAIL, "request/response failed; no automatic retry")
    add("configured_repository_selection", NOT_PROVEN, "verify Only select repositories in GitHub settings")
    add("configured_permission_grants", NOT_PROVEN, "verify Contents:read, Metadata:read and no other grants")
    return results


def exit_code(results):
    if not results or any(state == FAIL for _, state, _ in results):
        return 1
    if any(state != PASS for _, state, _ in results):
        return 2
    # Remain fail-closed even if a future edit accidentally omits pending rows.
    return 2


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--token-file", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--branch", default="main")
    parser.add_argument("--probe-write", action="store_true", help="obsolete: rejected without network access")
    args = parser.parse_args(argv)
    if args.probe_write:
        print("FAIL write probe is disabled; this tool sends GET requests only")
        return 1
    try:
        with open(args.token_file, "r", encoding="utf-8-sig") as source:
            token = source.read(513).strip()
        if not token or len(token) > 512:
            raise ValueError("empty or oversized credential")
    except (OSError, UnicodeError, ValueError):
        print("FAIL credential file cannot be used")
        return 1
    results = check(token, args.repo, args.branch)
    for name, state, detail in results:
        print(f"{state} {name} [{detail}]")
    code = exit_code(results)
    print("CREDENTIAL_READINESS=" + ("FAIL" if code == 1 else "NOT_PROVEN"))
    return code


if __name__ == "__main__":
    sys.exit(main())
