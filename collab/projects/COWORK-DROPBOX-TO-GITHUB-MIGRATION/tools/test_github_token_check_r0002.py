import contextlib
import io
import json
import tempfile
import unittest
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

import github_token_check_r0002 as m

TOKEN = "github_pat_" + "A" * 40  # synthetic fixture, never a real credential
REPO = "owner/one-repo"
NOW = datetime(2026, 11, 13, tzinfo=timezone.utc)


def transport(user=200, scope="", expiry="2026-12-20 00:00:00 UTC", repos=None,
              link="", contents=200, content_body=None, seen=None):
    repos = [{"full_name": REPO, "private": True}] if repos is None else repos

    def http(method, url, headers, body=None):
        if seen is not None:
            seen.append((method, url, body))
        if url.endswith("/user"):
            return user, {"GitHub-Authentication-Token-Expiration": expiry, "X-OAuth-Scopes": scope}, b"{}"
        if "/user/repos?" in url:
            return 200, {"link": link} if link else {}, json.dumps(repos).encode()
        return contents, {}, json.dumps({"type": "file"} if content_body is None else content_body).encode()
    return http


class TokenPrecheck(unittest.TestCase):
    def check(self, **kw):
        return m.check(TOKEN, REPO, http=transport(**kw), today=NOW)

    def state(self, results, name):
        return next(state for key, state, _ in results if key == name)

    def test_positive_gets_are_partial_never_credential_ready(self):
        r = self.check()
        self.assertEqual(m.exit_code(r), 2)
        self.assertEqual(self.state(r, "contents_read"), m.PASS)
        self.assertEqual(self.state(r, "configured_permission_grants"), m.NOT_PROVEN)

    def test_default_sends_get_only_no_write_probe(self):
        seen = []
        self.check(seen=seen)
        self.assertEqual(len(seen), 3)
        self.assertTrue(all(method == "GET" and body is None for method, _, body in seen))
        self.assertIn("visibility=private", seen[1][1])

    def test_read_success_cannot_distinguish_read_write_token(self):
        # Write-capable credentials can produce exactly the same GET responses.
        self.assertEqual(m.exit_code(self.check()), 2)

    def test_403_never_proves_read_only(self):
        for status in (403, 422, 429, 500, 302):
            with self.subTest(status=status):
                r = self.check(contents=status)
                self.assertEqual(m.exit_code(r), 1)
                self.assertEqual(self.state(r, "configured_permission_grants"), m.NOT_PROVEN)

    def test_rejected_auth_stops_network(self):
        seen = []
        self.assertEqual(m.exit_code(self.check(user=401, seen=seen)), 1)
        self.assertEqual(len(seen), 1)

    def test_bad_token_types_stop_before_network(self):
        for token in ("ghp_example", "gho_example", "", TOKEN + "\nInjected", "github_pat_한글"):
            seen = []
            r = m.check(token, REPO, http=transport(seen=seen))
            self.assertEqual(m.exit_code(r), 1)
            self.assertEqual(seen, [])

    def test_bad_repo_stops_before_network(self):
        for repo in ("../x", "owner/..", "owner/repo?extra", "https://evil/repo", "o/r/#"):
            seen = []
            self.assertEqual(m.exit_code(m.check(TOKEN, repo, http=transport(seen=seen))), 1)
            self.assertEqual(seen, [])

    def test_branch_query_is_escaped(self):
        seen = []
        m.check(TOKEN, REPO, branch="feature/x&other=1", http=transport(seen=seen), today=NOW)
        self.assertTrue(seen[-1][1].endswith("ref=feature%2Fx%26other%3D1"))

    def test_expiry_strict_boundary(self):
        for delta, expected in ((timedelta(days=90), m.PASS),
                                (timedelta(days=90, seconds=1), m.FAIL),
                                (timedelta(0), m.FAIL), (timedelta(seconds=-1), m.FAIL)):
            expiry = (NOW + delta).strftime("%Y-%m-%d %H:%M:%S UTC")
            self.assertEqual(self.state(self.check(expiry=expiry), "expiry_within_90_days"), expected)

    def test_iso_expiry_supported(self):
        self.assertEqual(self.state(self.check(expiry="2026-12-20T00:00:00Z"), "expiry_within_90_days"), m.PASS)

    def test_missing_invalid_or_naive_expiry_fails(self):
        for expiry in ("", None, "tomorrow", "2026-12-20T00:00:00"):
            self.assertEqual(self.state(self.check(expiry=expiry), "expiry_within_90_days"), m.FAIL)

    def test_classic_scope_fails(self):
        self.assertEqual(m.exit_code(self.check(scope="repo, workflow")), 1)

    def test_extra_or_wrong_private_repo_fails(self):
        for repos in ([], [{"full_name": "owner/other", "private": True}],
                      [{"full_name": REPO, "private": True}, {"full_name": "owner/other", "private": True}]):
            self.assertEqual(m.exit_code(self.check(repos=repos)), 1)

    def test_private_visibility_and_response_shape_required(self):
        for repos in ({"full_name": REPO}, [None], ["repo"], [{"full_name": REPO}],
                      [{"full_name": REPO, "private": False}], [{"full_name": 5, "private": True}]):
            self.assertEqual(m.exit_code(self.check(repos=repos)), 1)

    def test_unexamined_pagination_fails_closed(self):
        self.assertEqual(m.exit_code(self.check(link='<https://api.github.com/user/repos?page=2>; rel="next"')), 1)

    def test_contents_200_must_be_file_object(self):
        for body in ([], "hello", {"type": "dir"}):
            self.assertEqual(m.exit_code(self.check(content_body=body)), 1)

    def test_network_exception_never_echoes_token(self):
        def broken(*args, **kw):
            raise urllib.error.URLError(TOKEN)
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "secret.txt"
            path.write_text(TOKEN, encoding="utf-8")
            output = io.StringIO()
            with patch.object(m, "urllib_http", broken), contextlib.redirect_stdout(output):
                self.assertEqual(m.main(["--token-file", str(path), "--repo", REPO]), 1)
            self.assertNotIn(TOKEN, output.getvalue())
            self.assertNotIn(str(path), output.getvalue())

    def test_cli_default_returns_partial_without_secret_output(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "secret.txt"
            path.write_text(TOKEN, encoding="utf-8")
            output = io.StringIO()
            expiry = (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S UTC")
            with patch.object(m, "urllib_http", transport(expiry=expiry)), contextlib.redirect_stdout(output):
                self.assertEqual(m.main(["--token-file", str(path), "--repo", REPO]), 2)
            self.assertIn("CREDENTIAL_READINESS=NOT_PROVEN", output.getvalue())
            self.assertNotIn(TOKEN, output.getvalue())

    def test_obsolete_write_option_rejected_without_read_or_network(self):
        with patch.object(m, "urllib_http") as network, contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(m.main(["--token-file", "unused", "--repo", REPO, "--probe-write"]), 1)
            network.assert_not_called()

    def test_missing_or_invalid_token_file_is_clean_failure(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "secret.txt"
            for data in (None, b"", b"\xff", ("A" * 514).encode()):
                if data is not None:
                    path.write_bytes(data)
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(m.main(["--token-file", str(path), "--repo", REPO]), 1)

    def test_transport_rejects_mutation_and_external_urls_before_open(self):
        for method, url, body in (("PUT", m.API + "/x", b"{}"),
                                  ("GET", "https://example.com/x", None),
                                  ("GET", "http://api.github.com/x", None),
                                  ("GET", "https://api.github.com@evil.example/x", None)):
            with self.assertRaises(m.ProbeError):
                m.urllib_http(method, url, {}, body)

    def test_redirect_handler_does_not_forward_credentials(self):
        self.assertIsNone(m.NoRedirect().redirect_request(None, None, 302, "", {}, "https://evil.example"))

    def test_no_empty_or_omitted_pending_rows_can_give_exit_zero(self):
        self.assertEqual(m.exit_code([]), 1)
        self.assertEqual(m.exit_code([("read", m.PASS, "")]), 2)


if __name__ == "__main__":
    unittest.main()
