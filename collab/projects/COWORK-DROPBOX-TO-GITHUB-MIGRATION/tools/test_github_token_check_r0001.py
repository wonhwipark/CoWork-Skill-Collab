import json
import os
import tempfile
import unittest
from datetime import datetime, timezone

import github_token_check_r0001 as m

REPO = "owner/one-repo"
GOOD = "github_pat_" + "A" * 40
NOW = datetime(2026, 11, 13, tzinfo=timezone.utc)


def scripted(user=200, repos=(REPO,), contents=200, write=403, expiry="2026-12-20 00:00:00 UTC", scopes=None, seen=None):
    def http(method, url, headers, body=None):
        if seen is not None:
            seen.append((method, url.replace(m.API, "")))
        if url.endswith("/user"):
            h = {}
            if expiry:
                h["github-authentication-token-expiration"] = expiry
            if scopes is not None:
                h["x-oauth-scopes"] = scopes
            return user, h, b"{}"
        if "/user/repos" in url:
            return 200, {}, json.dumps([{"full_name": r} for r in repos]).encode()
        if method == "PUT":
            return write, {}, b"{}"
        return contents, {}, b"{}"
    return http


def failed(results):
    return sorted(n for n, ok, _d in results if not ok)


class TokenCheck(unittest.TestCase):
    def run_check(self, token=GOOD, probe=False, **kw):
        return m.check(token, REPO, probe_write=probe, http=scripted(**kw), today=NOW)

    def test_a_single_repo_read_only_token_passes_everything(self):
        self.assertEqual(failed(self.run_check(probe=True)), [])

    def test_the_broad_classic_style_tokens_fail(self):
        for token in ("ghp_" + "a" * 36, "gho_" + "a" * 36):
            self.assertIn("token type is a fine-grained personal access token", failed(self.run_check(token=token)))

    def test_a_token_that_sees_more_than_one_repository_fails(self):
        self.assertIn("the token can reach exactly this one repository", failed(self.run_check(repos=(REPO, "owner/other"))))

    def test_a_token_that_sees_a_different_repository_fails(self):
        self.assertIn("the token can reach exactly this one repository", failed(self.run_check(repos=("owner/other",))))

    def test_attached_oauth_scopes_fail(self):
        self.assertIn("no classic OAuth scopes are attached", failed(self.run_check(scopes="repo, workflow")))

    def test_missing_or_distant_expiry_fails(self):
        self.assertTrue(failed(self.run_check(expiry=None)))
        self.assertTrue(failed(self.run_check(expiry="2027-06-01 00:00:00 UTC")))

    def test_a_rejected_token_stops_at_once(self):
        results = self.run_check(user=401)
        self.assertIn("token is accepted by GitHub", failed(results))
        self.assertEqual(len(results), 2)

    def test_the_write_probe_is_off_by_default_and_sends_no_put(self):
        seen = []
        m.check(GOOD, REPO, http=scripted(seen=seen), today=NOW)
        self.assertNotIn("PUT", [method for method, _u in seen])

    def test_a_token_with_write_access_is_caught_by_the_probe(self):
        self.assertIn("Contents write is denied (invalid probe got 403, not 422)", failed(self.run_check(probe=True, write=422)))

    def test_the_token_never_appears_in_the_output(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "t.txt")
            open(path, "w").write(GOOD)
            import io, contextlib
            buf = io.StringIO()
            real = m.urllib_http
            m.urllib_http = scripted()
            try:
                with contextlib.redirect_stdout(buf):
                    m.main(["--token-file", path, "--repo", REPO])
            finally:
                m.urllib_http = real
            self.assertNotIn(GOOD, buf.getvalue())

    def test_an_unreadable_token_file_is_a_clean_failure(self):
        self.assertEqual(m.main(["--token-file", "does-not-exist.txt", "--repo", REPO]), 2)


if __name__ == "__main__":
    unittest.main()
