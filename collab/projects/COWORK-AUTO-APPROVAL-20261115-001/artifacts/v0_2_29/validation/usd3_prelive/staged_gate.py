"""STAGED unified USD3 gate checks. Everything is written under ./staged only; the real reviewer.config.json is only read.
Positive: staged config (STATIC=3.00) + a synthetic STATIC REQUEST for the pinned ZIP. Negative: wrong price, wrong tier label, tampered size/hash, numeric repo_id pin."""
import hashlib, json, pathlib, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).parent / "staged"
ZIP = pathlib.Path(r"D:\User\whpark\cowork-phase1\v029_rev\skill-collab-watcher_v0_2_29_1120.zip")
REAL = pathlib.Path(r"D:\User\whpark\skill-collab-watcher-github\config\reviewer.config.json")
GATE = ROOT / "review_request_gate.py"
PIN = ROOT / "source_pin.py"

cfg = json.loads(REAL.read_text(encoding="utf-8"))
real_sha = hashlib.sha256(REAL.read_bytes()).hexdigest()
staged = json.loads(json.dumps(cfg))
staged["review_policy"]["known_run_policy_refs"]["POLICY-STATIC-V1"]["max_budget_usd"] = 3.0
(ROOT / "reviewer.config.staged.json").write_text(json.dumps(staged, indent=2), encoding="utf-8")
bad = json.loads(json.dumps(staged))
bad["review_policy"]["known_run_policy_refs"]["POLICY-STATIC-V1"]["max_budget_usd"] = 2.0
(ROOT / "reviewer.config.bad_price.json").write_text(json.dumps(bad, indent=2), encoding="utf-8")
shutil_zip = ROOT / ZIP.name
shutil_zip.write_bytes(ZIP.read_bytes())
zb = ZIP.read_bytes()
sha, size = hashlib.sha256(zb).hexdigest(), len(zb)


def request(rid="REQ-STAGED-USD3-CHECK-20261120", policy="POLICY-STATIC-V1", sha_=sha, size_=size):
    return f"""---
schema: SKILL_COLLAB_REVIEW_REQUEST_V1
state: SUBMITTED
request_id: {rid}
request_revision: 1
project_id: COWORK-AUTO-APPROVAL-20261115-001
work_id: COWORK-AUTO-APPROVAL-20261115-001
skill_id: cowork-review-watcher
package_path: /SKILL-COLLAB/packages/{ZIP.name}
package_file_id: github:{rid}
package_rev: v0.2.29
package_sha256: {sha_}
package_size_bytes: {size_}
baseline_package_ref: null
knowledge_refs: []
consumer_profiles: [windows-single-user-watcher]
reviewer_os: WINDOWS
test_policy: STATIC_ONLY
run_policy_ref: {policy}
output_contract: SKILL_COLLAB_REVIEW_RESULT_V1
goal: staged local check only, never published
---

# staged check
"""


def run(args):
    r = subprocess.run([sys.executable, str(GATE), *args], capture_output=True, text=True)
    return r.returncode, (r.stdout or r.stderr).strip()[:300]


def check(cfgname, req, intent="unified", budget="3.00"):
    p = ROOT / f"req_{abs(hash(req)) % 10**8}.md"
    p.write_bytes(req.encode("utf-8"))
    return run(["check", "--live-config", str(ROOT / cfgname), "--intent", intent, "--required-budget-usd", budget, "--request", str(p), "--package", str(shutil_zip)])


res = {}
res["select_real_live_config"] = run(["select", "--live-config", str(REAL), "--intent", "unified", "--required-budget-usd", "3.00"])
res["select_staged_config"] = run(["select", "--live-config", str(ROOT / "reviewer.config.staged.json"), "--intent", "unified", "--required-budget-usd", "3.00"])
res["check_staged_positive"] = check("reviewer.config.staged.json", request())
res["neg_wrong_price_config_2_00"] = run(["select", "--live-config", str(ROOT / "reviewer.config.bad_price.json"), "--intent", "unified", "--required-budget-usd", "3.00"])
res["neg_request_names_design_tier"] = check("reviewer.config.staged.json", request(policy="POLICY-STATIC-V1-DESIGN"))
res["neg_request_names_large_tier"] = check("reviewer.config.staged.json", request(policy="POLICY-STATIC-V1-LARGE"))
res["neg_package_sha_tampered"] = check("reviewer.config.staged.json", request(sha_="0" * 64))
res["neg_package_size_tampered"] = check("reviewer.config.staged.json", request(size_=size + 1))
res["neg_unified_with_budget_1_50"] = run(["select", "--live-config", str(ROOT / "reviewer.config.staged.json"), "--intent", "unified", "--required-budget-usd", "1.50"])
# SOURCE_PIN string/number
good = ROOT / "pin_good.json"
num = ROOT / "pin_numeric.json"
good.write_text(json.dumps({"schema": "SKILL_COLLAB_SOURCE_PIN_V1", "commit": "a" * 40, "repo_id": "1451933830"}), encoding="utf-8")
num.write_text(json.dumps({"schema": "SKILL_COLLAB_SOURCE_PIN_V1", "commit": "a" * 40, "repo_id": 1451933830}), encoding="utf-8")
for name, f in (("pin_string_repo_id", good), ("pin_numeric_repo_id", num)):
    r = subprocess.run([sys.executable, str(PIN), "check", str(f), "--expected-repo-id", "1451933830"], capture_output=True, text=True)
    res[name] = (r.returncode, (r.stdout or r.stderr).strip()[:200])
res["real_config_unchanged"] = hashlib.sha256(REAL.read_bytes()).hexdigest() == real_sha
for k, v in res.items():
    print(k.ljust(34), v)
(ROOT / "staged_gate_result.json").write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
