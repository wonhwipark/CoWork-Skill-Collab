#!/usr/bin/env python3
"""Check that a GitHub token file is a single-repository, Contents-read-only fine-grained token.

Usage: python github_token_check_r0001.py --token-file FILE --repo OWNER/REPO [--branch main] [--probe-write]

The token is read from the file and sent only to api.github.com. It is never printed, logged or copied.
Output is one PASS/FAIL line per check. Exit code 0 only when every check passes.

--probe-write sends ONE deliberately invalid PUT (empty JSON body) to the contents API. GitHub authorizes the
request before validating it: a read-only token gets 403, a token with write access gets 422 and nothing is
written because the body is invalid. Run it once at installation time; it is off by default.
"""
import argparse
import json
import sys
import urllib.error
import urllib.request

API = "https://api.github.com"
MAX_EXPIRY_DAYS = 90


def urllib_http(method, url, headers, body=None):
    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, {k.lower(): v for k, v in resp.headers.items()}, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, {k.lower(): v for k, v in exc.headers.items()}, exc.read()


def token_class(token):
    if token.startswith("github_pat_"):
        return "FINE_GRAINED_PAT"
    if token.startswith("ghp_"):
        return "CLASSIC_PAT"
    if token.startswith(("gho_", "ghu_", "ghs_", "ghr_")):
        return "OAUTH_OR_APP_TOKEN"
    return "UNKNOWN"


def check(token, repo, branch="main", probe_write=False, http=None, today=None):
    from datetime import datetime, timezone
    http = http or urllib_http
    results = []

    def add(name, ok, detail=""):
        results.append((name, bool(ok), detail))

    headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json",
               "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "token-check"}
    cls = token_class(token)
    add("token type is a fine-grained personal access token", cls == "FINE_GRAINED_PAT", cls)

    status, hdrs, _ = http("GET", f"{API}/user", headers)
    add("token is accepted by GitHub", status == 200, f"HTTP {status}")
    if status != 200:
        return results
    add("no classic OAuth scopes are attached", "x-oauth-scopes" not in hdrs or not hdrs["x-oauth-scopes"].strip(),
        "header absent or empty")
    expiry = hdrs.get("github-authentication-token-expiration")
    if expiry:
        try:
            stamp = datetime.strptime(expiry.replace(" UTC", ""), "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
            days = (stamp - (today or datetime.now(timezone.utc))).days
            add(f"token expires within {MAX_EXPIRY_DAYS} days", 0 <= days <= MAX_EXPIRY_DAYS, f"{days} days left")
        except ValueError:
            add("token expiry is readable", False, "unparsable header")
    else:
        add(f"token has an expiry (<= {MAX_EXPIRY_DAYS} days)", False, "no expiry header")

    status, _, body = http("GET", f"{API}/user/repos?per_page=100", headers)
    names = []
    if status == 200:
        try:
            names = sorted(r.get("full_name", "") for r in json.loads(body))
        except (ValueError, AttributeError):
            names = ["<unparsable>"]
    add("the token can reach exactly this one repository", status == 200 and names == [repo],
        f"{len(names)} repositories visible" if status == 200 else f"HTTP {status}")

    status, _, _ = http("GET", f"{API}/repos/{repo}/contents/collab/START_HERE.md?ref={branch}", headers)
    add("Contents read works on the branch", status == 200, f"HTTP {status}")

    if probe_write:
        status, _, _ = http("PUT", f"{API}/repos/{repo}/contents/.token-write-probe", headers, b"{}")
        add("Contents write is denied (invalid probe got 403, not 422)", status == 403, f"HTTP {status}")
    else:
        add("write probe", True, "SKIPPED (use --probe-write once at installation)")
    return results


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--token-file", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--branch", default="main")
    parser.add_argument("--probe-write", action="store_true")
    args = parser.parse_args(argv)
    try:
        token = open(args.token_file, "r", encoding="utf-8-sig").read().strip()
    except OSError as exc:
        print(f"FAIL token file is not readable by this account ({type(exc).__name__})")
        return 2
    if not token:
        print("FAIL token file is empty")
        return 2
    results = check(token, args.repo, args.branch, args.probe_write)
    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'} {name}" + (f" [{detail}]" if detail else ""))
    return 0 if all(ok for _n, ok, _d in results) else 1


if __name__ == "__main__":
    sys.exit(main())
