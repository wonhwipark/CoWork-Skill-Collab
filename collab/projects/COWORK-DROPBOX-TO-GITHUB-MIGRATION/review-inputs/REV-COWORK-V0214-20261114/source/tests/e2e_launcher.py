"""Subprocess entry for the isolated entry-point E2E tests (test_cli_entrypoint_e2e.py).

It runs the REAL `skill_collab_watcher.cli.main` (config load -> runtime -> trust root -> transport -> scan ->
orchestrator -> RealReviewRunner -> publish). Only the network layer is replaced: GitHubTransport's HTTP object
forwards every request to a local synthetic GitHub server (127.0.0.1). The reviewer executable is a stub that
counts its own invocations. No real GitHub, no model, no Telegram."""
import base64
import json
import os
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from skill_collab_watcher import cli  # noqa: E402
from skill_collab_watcher import github_transport as gt  # noqa: E402

SERVER = os.environ["E2E_FAKE_GITHUB"]
assert SERVER.startswith("http://127.0.0.1:"), "the E2E bridge only talks to loopback"


class Bridge:
    def request(self, method, url, headers, body=None):
        env = {"method": method, "url": url, "headers": dict(headers),
               "body": base64.b64encode(body).decode() if body is not None else None}
        req = urllib.request.Request(SERVER, data=json.dumps(env).encode(), method="POST",
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            out = json.loads(resp.read())
        if out.get("raise"):
            raise OSError(out["raise"])
        return out["status"], out["headers"], base64.b64decode(out["body"])


gt.UrllibHttp = Bridge
sys.exit(cli.main(sys.argv[1:]))
