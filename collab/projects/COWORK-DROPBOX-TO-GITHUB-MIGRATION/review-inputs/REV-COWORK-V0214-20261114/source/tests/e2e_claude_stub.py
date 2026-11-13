"""Stand-in for the `claude` executable in the E2E tests. Never contacts a model.
`auth status --json` answers logged-in; any other call is one 'model call': it appends one line to the counter file
(E2E_COUNTER), optionally sleeps (E2E_STUB_SLEEP seconds, to widen a race window) and prints a CLI-shaped result."""
import json
import os
import sys
import time

args = sys.argv[1:]
if args[:2] == ["auth", "status"]:
    print(json.dumps({"loggedIn": True}))
    sys.exit(0)
prompt = sys.stdin.read()
with open(os.environ["E2E_COUNTER"], "a", encoding="utf-8") as fh:
    fh.write(f"CALL pid={os.getpid()} prompt_chars={len(prompt)}\n")
time.sleep(float(os.environ.get("E2E_STUB_SLEEP", "0")))
print(json.dumps({"type": "result", "subtype": "success", "is_error": False,
                  "result": "E2E STUB REVIEW (no model was called)", "total_cost_usd": 0.0,
                  "usage": {"input_tokens": 1, "output_tokens": 1}}))
