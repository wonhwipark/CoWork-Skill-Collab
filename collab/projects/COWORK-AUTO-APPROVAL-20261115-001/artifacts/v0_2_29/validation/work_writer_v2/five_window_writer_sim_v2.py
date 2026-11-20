"""Five independent rounds of the Work-side recovery flow (mock GitHub contents API, mock skill repo, throw-away watcher DB from the
pinned package's StateStore). Windows: D1, D2 = design reviews; S1, S2, S3 = three modifications of the SAME skill made from one base.
Nothing here starts a model or touches an operating file. Usage: five_window_writer_sim.py <extracted_pkg_root> <out.json>"""
import hashlib
import json
import os
import random
import sys
import tempfile
import threading
from pathlib import Path

PKG = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(PKG))
sys.path.insert(0, str(Path(__file__).parent.parent / "work_writer"))     # v1 module, published unchanged
import work_writer as w  # noqa: E402
import work_writer_v2 as w2  # noqa: E402
from skill_collab_watcher.models import JobState  # noqa: E402
from skill_collab_watcher.state_store import StateStore  # noqa: E402

HEADER = "# SHARED — CURRENT\n"
WINDOWS = [{"id": "D1", "skill": "design-a"}, {"id": "D2", "skill": "design-b"},
           {"id": "S1", "skill": "wiki-skill"}, {"id": "S2", "skill": "wiki-skill"}, {"id": "S3", "skill": "wiki-skill"}]
BASE = "line1\nline2\nline3\nline4\nline5\nline6\nline7\nline8\n"
# round -> (uncertain window or None, has remote evidence, inject semantic conflict between S2 and S3)
PLAN = {1: ("S1", True, False), 2: ("S1", False, False), 3: ("D1", True, False), 4: ("D2", False, True), 5: (None, False, False)}


def entry(wid, r):
    return f"\n## round {r} window {wid}\n- result of {wid}\n\n---\n"


def run_round(r):
    rec = {"round": r}
    uncertain_win, has_evidence, inject = PLAN[r]
    rng = random.Random(r)

    # ---- A. shared CURRENT.md: all five windows read the same stale snapshot first (4 stale-sha conflicts), then retry
    gh = w.MockContents()
    w.cas_update(gh, "CURRENT.md", w.current_merge(HEADER, "seed", "\n## seed\n"))
    stale = gh.get("CURRENT.md")
    res = []

    class StaleOnce:
        def __init__(self):
            self.first = True

        def get(self, p):
            if self.first and p == "CURRENT.md":
                self.first = False
                return stale
            return gh.get(p)

        def put(self, *a):
            return gh.put(*a)

    for win in WINDOWS:
        res.append(w.cas_update(StaleOnce(), "CURRENT.md", w.current_merge(HEADER, f"round {r} window {win['id']}", entry(win["id"], r))))
    text = gh.files["CURRENT.md"].decode()
    rec["cas_stale"] = {"conflicts": sum(x.conflicts for x in res), "max_attempts": max(x.attempts for x in res),
                        "entries_present": all(text.count(f"round {r} window {x['id']}") == 1 for x in WINDOWS), "seed_kept": "seed" in text}

    # ---- B. shared TRACKER.json: five threads at once, retry cap 3, jittered backoff
    exhausted, attempts, conflicts, lock = [], [], [], threading.Lock()

    class Latency:
        """Network-like delay between the GET and the PUT so that the five writers really overlap (without it the threads serialize)."""

        def get(self, p):
            out = gh.get(p)
            import time as _t
            _t.sleep(random.Random().uniform(0.01, 0.04))
            return out

        def put(self, *a):
            return gh.put(*a)

    wave2, pending, statuses = [], [], {}

    def worker(win):
        x = w2.cas_two_wave(Latency(), "TRACKER.json", w.tracker_merge(f"W-{win['id']}", {"phase": "REVIEW", "next_action": f"round {r} {win['id']}"}),
                            max_retries=3, backoff=rng.uniform(0.002, 0.012), rng=random.Random(r * 100 + ord(win["id"][0]) + int(win["id"][1])))
        with lock:
            attempts.append(x.attempts)
            conflicts.append(x.conflicts)
            statuses[win["id"]] = x.status
            if x.waves == 2:
                wave2.append(win["id"])
            if x.status == "POST_CONFLICT_PENDING":
                pending.append(win["id"])

    ts = [threading.Thread(target=worker, args=(x,)) for x in WINDOWS]
    [t.start() for t in ts]
    [t.join() for t in ts]
    exhausted, caller_retry = wave2, [x for x in wave2 if x not in pending]
    works = {x["work_id"]: x for x in json.loads(gh.files["TRACKER.json"])["works"]}
    rec["cas_threaded"] = {"conflicts": sum(conflicts), "max_attempts": max(attempts) if attempts else None, "needed_wave_2": exhausted,
                           "post_conflict_pending": pending, "statuses": statuses, "total_attempts_per_writer_max_8": max(attempts) <= 8,
                           "recovered_by_caller_retry": caller_retry, "all_five_works_present": len(works) == 5,
                           "no_duplicates": len(works) == len({x['work_id'] for x in json.loads(gh.files['TRACKER.json'])['works']}),
                           "puts": gh.puts, "stale_conflicts_total": gh.conflicts}

    # ---- C. same-skill modifications S1..S3 from one base revision, serial rebase, regression before pin
    repo = w.SkillRepo({"a.py": BASE, "b.py": BASE, "c.py": BASE})
    pins = {}
    s3_a = "line1\nline2\nline3\nline4\nline5\nline6\nline7\nS3\n" if not inject else "line1\nline2\nline3\nline4\nline5\nline6\nS3CLASH\nline8\n"
    mods = [w.Modification("S1", 1, {"a.py": BASE.replace("line2", "S1-line2"), "b.py": BASE.replace("line7", "S1-line7")}),
            w.Modification("S2", 1, {"a.py": BASE.replace("line6", "S2-line6"), "c.py": BASE.replace("line1", "S2-line1")}),
            w.Modification("S3", 1, {"a.py": s3_a if not inject else BASE.replace("line6", "S3CLASH-line6")})]
    seen_markers = []

    def regression(files):
        return all(any(m in t for t in files.values()) for m in seen_markers), "earlier change lost"

    outs = []
    for m in mods:
        seen_markers_before = list(seen_markers)
        o = w.apply_modification(repo, m, regression, pins)
        outs.append(o)
        if o["written"]:
            seen_markers.append({"S1": "S1-line2", "S2": "S2-line6", "S3": "S3"}[m.mid])
    merged_a = repo.files["a.py"]
    rec["skill_rebase"] = {"statuses": {o["mid"]: o["status"] for o in outs}, "head_rev": repo.rev,
                           "head_tree_sha": w.tree_sha(repo.files), "candidate_shas": {k: v.sha[:16] for k, v in pins.items()},
                           "earlier_changes_kept": all(mk in merged_a or mk in "".join(repo.files.values()) for mk in seen_markers),
                           "pinned_unchanged_after_later_changes": w.pins_unchanged(pins)}
    if inject:
        rec["skill_rebase"]["semantic_conflict_blocked_without_write"] = outs[2]["status"] == "NEEDS_DECISION" and not outs[2]["written"] and "S3CLASH" not in merged_a
    else:
        rec["skill_rebase"]["all_three_merged"] = [o["status"] for o in outs] in (["APPLIED", "APPLIED", "REBASED"], ["APPLIED", "REBASED", "REBASED"]) and "S1-line2" in merged_a and "S2-line6" in merged_a

    # ---- D. one UNCERTAIN job, read-only reconciliation against a throw-away watcher DB (own DB per round)
    d = Path(tempfile.mkdtemp(prefix=f"sim5w-r{r}-"))
    dbp = d / "state.sqlite3"
    store = StateStore(dbp)
    zshas, keys = {}, {}
    pol = 2 if r == 3 else 1                               # round 3 runs under policy revision 2: a hard coded "|1" key would miss every job
    for win in WINDOWS:
        zshas[win["id"]] = hashlib.sha256(f"zip-{r}-{win['id']}".encode()).hexdigest()
        keys[win["id"]] = f"REQ-{r}-{win['id']}|1|{zshas[win['id']]}|{pol}"
        store.create_job(keys[win["id"]], f"REQ-{r}-{win['id']}", "1", zshas[win["id"]], JobState.CLAIMED)
        store.log_event("REVIEW_DISPATCHED", processing_key=keys[win["id"]], detail="{}")
        store.update_job_state(keys[win["id"]], JobState.REVIEW_UNCERTAIN if win["id"] == uncertain_win else JobState.COMPLETED)
    store.close()
    remote = {}
    for win in WINDOWS:
        rid, key, z = f"REQ-{r}-{win['id']}", keys[win["id"]], zshas[win["id"]]
        if win["id"] == uncertain_win and not has_evidence:
            continue
        remote[f"reviews/{rid}/REVIEW_RESULT_1.md"] = f'---\nreview_id: "{key}"\npackage_sha256: "{z}"\n---\nresult bytes {rid}\n'.encode()
        remote[f"receipts/{rid}/RECEIPT_1.md"] = json.dumps({"processing_key": key, "request_id": rid, "package_sha256": z, "ok": True}).encode()
    before = hashlib.sha256(dbp.read_bytes()).hexdigest()
    verdicts = {win["id"]: w2.reconcile_uncertain(str(dbp), remote.get, f"REQ-{r}-{win['id']}", "1", zshas[win["id"]]) for win in WINDOWS}
    after = hashlib.sha256(dbp.read_bytes()).hexdigest()
    plan = w.plan_after_uncertain(WINDOWS, {k: v["verdict"] for k, v in verdicts.items()})
    expect_uncertain = None
    if uncertain_win:
        expect_uncertain = "SETTLED_BY_EVIDENCE" if has_evidence else "UNCERTAIN_HOLD"
    rec["uncertain"] = {"window": uncertain_win, "remote_evidence_present": has_evidence,
                        "verdict": verdicts[uncertain_win]["verdict"] if uncertain_win else None, "expected": expect_uncertain,
                        "others_not_uncertain": all(v["verdict"] == "NOT_UNCERTAIN" for k, v in verdicts.items() if k != uncertain_win),
                        "db_unchanged_by_reconcile": before == after,
                        "model_calls_started_by_reconcile": sum(v["model_calls_started_by_reconcile"] for v in verdicts.values()),
                        "dispatch_events_per_window": {k: v["dispatch_events_total"] for k, v in verdicts.items()},
                        "policy_revisions_seen": sorted({x for v in verdicts.values() for x in v["policy_revisions"]}),
                        "plan": plan, "remote_result_sha256": verdicts[uncertain_win].get("remote_result_sha256") if uncertain_win else None}
    wait_expected = {x["id"]: "PROCEED" for x in WINDOWS}
    if uncertain_win and not has_evidence:
        wait_expected[uncertain_win] = "UNCERTAIN_HOLD"
        for x in WINDOWS:
            if x["skill"] == next(y["skill"] for y in WINDOWS if y["id"] == uncertain_win) and x["id"] > uncertain_win:
                wait_expected[x["id"]] = "WAIT_DEPENDENCY"
    rec["uncertain"]["plan_as_expected"] = plan == wait_expected

    c, t, s, u = rec["cas_stale"], rec["cas_threaded"], rec["skill_rebase"], rec["uncertain"]
    rec["pass"] = bool(c["conflicts"] == 4 and c["entries_present"] and c["seed_kept"] and t["all_five_works_present"] and t["no_duplicates"]
                       and s["earlier_changes_kept"] and s["pinned_unchanged_after_later_changes"]
                       and (s.get("semantic_conflict_blocked_without_write") if inject else s.get("all_three_merged"))
                       and u["verdict"] == u["expected"] and u["others_not_uncertain"] and u["db_unchanged_by_reconcile"]
                       and u["model_calls_started_by_reconcile"] == 0 and u["plan_as_expected"])
    return rec


rounds = [run_round(r) for r in range(1, 6)]
report = {"schema": "COWORK_V029_WORK_WRITER_5_ROUNDS_V1", "package_root": str(PKG), "real_live": False, "real_model_calls": 0, "rounds": rounds,
          "rounds_pass": f'{sum(x["pass"] for x in rounds)}/5',
          "threaded_cap3_exhaustions": sum(len(x["cas_threaded"]["needed_wave_2"]) for x in rounds),
          "post_conflict_pending_total": sum(len(x["cas_threaded"]["post_conflict_pending"]) for x in rounds),
          "overall": "PASS" if all(x["pass"] for x in rounds) else "FAIL"}
OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("OVERALL", report["overall"], report["rounds_pass"], "threaded cap-3 exhaustions:", report["threaded_cap3_exhaustions"])
for x in rounds:
    print(x["round"], "PASS" if x["pass"] else "FAIL", "stale", x["cas_stale"]["conflicts"], "threaded", x["cas_threaded"]["conflicts"],
          "max_att", x["cas_threaded"]["max_attempts"], x["skill_rebase"]["statuses"], x["uncertain"]["verdict"])
