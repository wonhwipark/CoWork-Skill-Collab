"""Read-only host preflight for a new v0.2.29 independent review (no REQUEST, no signature, no READY, no model, no write)."""
import hashlib, json, os, pathlib, sqlite3, subprocess, sys, time

sys.stdout.reconfigure(encoding="utf-8")
PKG = r"D:\User\whpark\cowork-phase1\v029_disp\pkg"
sys.path.insert(0, PKG)
CFG = r"D:\User\whpark\skill-collab-watcher-github\config\reviewer.config.json"
DELEG = r"C:\Users\ME\AppData\Local\cowork-approver\auto_delegation.json"
DB = r"C:\Users\ME\AppData\Local\skill-collab-watcher-github\state.sqlite3"
REPO = "wonhwipark/CoWork-Skill-Collab"
out = {}

# 1. pinned ZIP bytes on main
r = subprocess.run(["gh", "api", "-H", "Accept: application/vnd.github.raw",
                    f"repos/{REPO}/contents/collab/projects/COWORK-AUTO-APPROVAL-20261115-001/artifacts/v0_2_29/skill-collab-watcher_v0_2_29_1120.zip?ref=main"], capture_output=True)
z = r.stdout
out["zip"] = {"bytes": len(z), "sha256": hashlib.sha256(z).hexdigest(), "expected_match": hashlib.sha256(z).hexdigest() == "c67bc342fe77547b000fc42e1b886396cbef035c0d265dbcd124947e267ed83f"}

# 2. registered tiers
cfg = json.loads(pathlib.Path(CFG).read_text(encoding="utf-8"))
out["registered_tiers"] = {k: v["max_budget_usd"] for k, v in cfg["review_policy"]["known_run_policy_refs"].items()}
out["config_signer_repo_id"] = cfg["auto_approval"]["signer"]["repo_id"]
out["config_acl_check"] = cfg["auto_approval"].get("acl_check")

# 3. protected delegation loaded by the package's own loader with the Windows ACL check
d = json.loads(pathlib.Path(DELEG).read_text(encoding="utf-8"))
out["delegation_fields"] = {k: d.get(k) for k in ("enabled", "policy", "max_request_usd", "enabled_at", "expires_at", "project_families", "projects", "skills", "repo_id", "branch")}
try:
    from skill_collab_watcher.auto_approval import load_delegation
    dele, why = load_delegation(pathlib.Path(DELEG), time.time(), "windows")
    out["delegation_loader_windows_acl"] = {"usable": dele is not None, "why": why, "max_request_cents": getattr(dele, "max_request_cents", None)}
except Exception as exc:  # noqa: BLE001
    out["delegation_loader_windows_acl"] = {"error": f"{type(exc).__name__}: {exc}"[:200]}

# 4. signer material present (names only, nothing read or printed)
for k, p in (("approver_key", cfg["auto_approval"]["signer"]["private_key_file"]), ("approver_pass_dpapi", cfg["auto_approval"]["signer"]["passphrase_dpapi_file"]),
             ("trust_root", cfg["github"]["trust_root_file"])):
    out[f"{k}_exists"] = os.path.exists(p)
tr = json.loads(pathlib.Path(cfg["github"]["trust_root_file"]).read_text(encoding="utf-8"))
out["trust_root_repo_id"] = tr.get("repo_id")
sr = subprocess.run(["gh", "api", f"repos/{REPO}", "--jq", ".id"], capture_output=True, text=True)
out["server_repo_id"] = sr.stdout.strip()

# 5. candidate scope check (what a REQUEST for this Work would carry)
fam = d.get("project_families") or []
proj = "COWORK-AUTO-APPROVAL-20261115-001"
out["scope"] = {"project": proj, "in_families_or_projects": any(proj.startswith(f) for f in fam) or proj in (d.get("projects") or []),
                "skill_cowork_review_watcher_allowed": "cowork-review-watcher" in (d.get("skills") or [])}

# 6. legacy pending / UNCERTAIN (DB opened read-only)
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
out["db_auto_claims"] = [(a, b) for a, b in con.execute("SELECT request_id, stage FROM auto_claims")]
out["db_jobs_not_completed"] = [(a, b) for a, b in con.execute("SELECT request_id, state FROM jobs WHERE state != 'COMPLETED'")]
out["db_job_count"] = con.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]
con.close()
print(json.dumps(out, ensure_ascii=False, indent=2))
