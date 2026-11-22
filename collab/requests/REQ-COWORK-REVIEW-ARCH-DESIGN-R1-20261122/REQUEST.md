---
schema: SKILL_COLLAB_REVIEW_REQUEST_V1
state: SUBMITTED
request_id: REQ-COWORK-REVIEW-ARCH-DESIGN-R1-20261122
request_revision: 1
project_id: COWORK-AUTO-APPROVAL-20261115-001
work_id: COWORK-AUTO-APPROVAL-20261115-001
skill_id: cowork-review-watcher
package_path: /SKILL-COLLAB/packages/skill-collab-watcher_v0_2_29_1120.zip
package_file_id: github:REQ-COWORK-REVIEW-ARCH-DESIGN-R1-20261122
package_rev: v0.2.29
package_sha256: c67bc342fe77547b000fc42e1b886396cbef035c0d265dbcd124947e267ed83f
package_size_bytes: 310753
baseline_package_ref: skill-collab-watcher_v0_2_29_1120.zip (unchanged, LIVE host-reported Nov 20)
knowledge_refs: []
consumer_profiles: [windows-single-user-watcher]
reviewer_os: WINDOWS
test_policy: STATIC_ONLY
run_policy_ref: POLICY-STATIC-V1
output_contract: SKILL_COLLAB_REVIEW_RESULT_V1
goal: One independent Windows Claude Code static review of CoWork formal review submission architecture and security/simplification proposal, max USD 3
---
# Independent review — CoWork formal-request transport, policy gate separation, and architecture simplification

## Intent and authorization boundary
The user expressly requested: review the proposed change that separates GPT-side REQUEST/SOURCE_PIN publication from Windows LIVE policy preflight, AND independently critique the whole present CoWork review-request architecture for unnecessary, unreasonable or redundant design. This is a genuine formal review request for the existing CoWork watcher subsystem (skill_id cowork-review-watcher), not a request to install, edit operating policy, change signer keys, widen delegation, publish READY manually, or deploy the proposal.

Reviewer = **Windows Claude Code, independent of GPT proposal/implementation**. Target Work = COWORK-AUTO-APPROVAL-20261115-001. One review, one revision, STATIC_ONLY, max USD 3 as existing Windows policy/delegation allows; do not ask an additional review automatically. The role-aligned skill_id is cowork-review-watcher, because it owns the review transport/watcher subsystem. Existing unrelated P1/P2 skill_id cowork-context-design and pending request remain separate; never relabel P1/P2 to get automatic signer eligibility.

## Observed problem and evidence (separate verified from reported)
- Different GPT chat, user says "리뷰요청해줘": latest Work/ZIP may be selected but only staged Base64 ZIP + draft REQUEST + handoff are posted. No actual GitHub collab/requests/.../REQUEST.md or SOURCE_PIN.json, so no Windows formal review.
- GPT can read/write the GitHub repository but cannot read Windows local reviewer.config.json or protected signer/SQLite. Current collab/ops/submit_review_request.py calls review_request_gate.check_request(request, package, live_config, intent='unified', budget=USD3) **before any GitHub writes**, making a host-only config check a GPT publication prerequisite.
- Existing review_request_gate.py *itself* says this is a policy compatibility check, **NOT an authorization check**. The protected Windows signer/watcher separately validates local policy, approved scope, expiry, hashes, costs, replay and READY.
- Windows watcher v0.2.29 LIVE, POLICY-STATIC-V1 USD3, delegated max_request_usd=3 and enabled_at Nov 20 are **host-reported as of 2026-11-20**. They are not freshly reverified by GPT and cannot be substituted for current host policy/authorization.
- The existing staged helper adds a roundtrip: GPT Base64 draft -> Windows checkout -> restore ZIP -> host precheck -> Commit A/B. Unit tests 11/11 PASS with mocked submitter, but no real Windows E2E. The actual user request concerns GPT steps ② exact target and ③ actual formal submission; overengineering watcher hooks is not an alternative to those steps.
- For integrity the source-pinned protocol requires Commit A tree containing exact REQUEST and ZIP, followed by Commit B SOURCE_PIN pointing to A with repo_id as string "1451933830". A GitHub request/PIN alone **must not** authorize protected signing or a paid model call. READY must be last only after valid protected signer checks; UNCERTAIN or already reviewed requests must not automatically retry.
- Repository is currently **PUBLIC**, not the stale PRIVATE references in older contracts. Never publish secrets, Windows protected configuration, restricted company code or customer data.

## Proposed redesign to critically REVIEW (NOT automatically accept)
**Option B — separate REQUEST publication from authorization:** GPT performs local/static fields/schema validation, exact package binary SHA-256/length/CRC, immutable source revision, eligibility format, existing request/review/receipt history and two-commit A/B pin/readback; does **not need** Windows LIVE config to publish a syntactically valid REQUEST+PIN. Windows host applies actual installed policy version/cap/scope/expiry/approval signature/READY on the pinned request and refuses everything invalid (zero model calls). Policy info provided by GPT is advisory, never trusted authority. Published but ineligible requests remain non-executed and precisely reported. Explicit user intent alone does not grant signer privilege.
This split is a **design proposal undergoing your review**, not an installed policy change. Analyze if it is genuinely secure under the v0.2.29 signer/watcher code, and whether it creates any new automatic signing or paid-call admission attack given PUBLIC repo with weak branch protection. If unsafe, reject it and specify an equally simple alternative that lets GPT finish formal submission without needing Windows local file access.

## Compare alternatives — require evidence and decision
- A KEEP strict Windows LIVE prepublication check: security gains, observed cross-chat deadlock, source of single point of failure; judge necessity.
- B SPLIT publication vs protected approval/READY (proposal above): security boundaries, queue spamming risk, stale config, silent auto approval under old delegation; recommend exact conditions.
- C Publish a sanitized, authenticated host policy-compatibility metadata snapshot for GPT: compare freshness, tampering, credential risk and operational burden; do not invent an approval oracle.
- D Windows host does all staging and submission using existing helper: compare hook/install overhead, user intent signal semantics, access constraints and complexity.
Which option best meets the exact user experience "리뷰요청해줘" from the current design GPT chat, with **minimal change** and no additional watcher/provider/daemon?

## Mandatory architecture critique — no gratuitous extra systems
For each, classify KEEP / SIMPLIFY / REMOVE / VERIFY_MORE with concrete reason and failure/abuse case, proposed minimal code/contract patch and tests:
1. Two Git commits (A for REQUEST+ZIP; B for SOURCE_PIN). Is an extra commit essential for consistent source pin? What is the simplest backward-compatible alternative? Protect against ZIP-only source pin and repo_id numeric mismatch.
2. Multiple preflight helpers (review_request_gate.py, review_pin_preflight.py, submit_review_request.py, review_staged_submission.py, Windows approve_request/auto signer). Distinguish useful integrity checks from redundant duplicated policy checks or repeated user approval.
3. Staging Base64 ZIP and Markdown handoff under Work before actual REQUEST. Is this justified for new GPT chats, or only for host-only paths? Can direct GPT source-pinned Git publication be canonical without another staging system?
4. Manual vs protected automatic approval, skill allowlist, USD3 cap, local-policy revision and enabled_at. Avoid silent permission widening; preserve actual delegated authority and one-call cost/replay fail-closed.
5. Windows watcher and Telegram notifier separation, review result/receipt writeback, completed/uncertain recovery; avoid duplicate model calls after network or result-post failure.
6. Overgrown CURRENT/history and multiple documents, stale PRIVATE vs now PUBLIC references, old DRAFT REVIEW_TRANSPORT_V1 contradictory dollar tiers and "not active" history. Recommend smallest effective deprecation/entrypoint strategy, no new status ledger.
7. ChatGPT connector vs Windows host boundary and actual hands-free execution. State exactly which steps can truly happen from another GPT chat with present tooling, what requires an installed hook, and what cannot be guaranteed by a Markdown policy alone.
8. GitHub public visibility and unprotected main: evaluate attacker/public-sourced request safety, signature trust-root independence, and what tampering/path/race checks need to remain non-negotiable.

## Evidence and reviewer requirements
- Primary baseline ZIP (unchanged installed watcher candidate): collab/packages/skill-collab-watcher_v0_2_29_1120.zip, **310753 bytes**, SHA256 **c67bc342fe77547b000fc42e1b886396cbef035c0d265dbcd124947e267ed83f**, 114 members. Independently verify inside the pinned input; this ZIP is reused, not a newly deployed build.
- Additional exact repository files below are embedded verbatim from GitHub main `828238e9d0c851a47d0342612a9d081052119fa3` to avoid relying on reviewer network or unspecified checkout state. The ZIP covers watcher runtime/auto approval; the embedded code covers GPT-side submission and gate.
- Separate confirmed facts from Windows host prior reports, design assumptions, unverified runtime behavior, and what was actually inspected.
- Do **not** execute package code, run tests, modify repo or host, change permissions, create keys/secrets, publish READY, or install anything. Static review only, one authorized reviewer call if and only if actual protected host policy/signer/READY permit it.
- Output: 1) **single recommended architecture and before/after workflow**; 2) KEEP/SIMPLIFY/REMOVE/VERIFY_MORE table with 5–10 highest-impact items; 3) blocking/major/minor findings each with exact file/function/condition/evidence; 4) smallest implementation plan, explicit invariants and acceptance tests; 5) exact expected user flow and remaining host dependencies. Indicate PASS/FAIL/NOT_RUN and no speculative claims. No automatic second review or operation changes.

## Pinned supplemental source inputs — verbatim

### FILE: collab/ops/review_request_gate.py
Git blob: `be6367bfff912be369f60188e3656df74bbc286d` at main revision `828238e9d0c851a47d0342612a9d081052119fa3`.

```text
#!/usr/bin/env python3
"""Fail-closed, offline CoWork REQUEST prepublication policy compatibility gate.

Reads the actual local Windows reviewer configuration. No GitHub writes, approval,
READY, signing, watcher calls, model calls or local config modification.
This is NOT an authorization check; the host approve_request check is separate.
"""
from __future__ import annotations

import argparse
from decimal import Decimal, InvalidOperation
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import zipfile

REQ_ID = re.compile(r"REQ-[A-Z0-9][A-Z0-9-]{3,120}\Z")
SHA256 = re.compile(r"[0-9a-f]{64}\Z")
REF = re.compile(r"[A-Z0-9][A-Z0-9-]{2,100}\Z")
COMMIT = re.compile(r"[0-9a-f]{40}\Z")
REPO_ID = re.compile(r"[1-9][0-9]*\Z")
INTENTS = {
    # New requests use a single policy and a single per-review budget.
    # Historical intents remain available for validating frozen legacy inputs.
    "unified": ("POLICY-STATIC-V1",),
    "skill": ("POLICY-STATIC-V1",),
    "design": ("POLICY-STATIC-V1-DESIGN", "POLICY-STATIC-V1-LARGE"),
}
DEFAULT_BUDGETS = {"unified": "3.00", "skill": "1.50", "design": "3.00"}
MAX_REQUEST = 256_000
MAX_PACKAGE = 32 * 1024 * 1024


class GateReject(ValueError):
    pass


def _read_file(path: Path, *, limit: int) -> bytes:
    if path.is_symlink() or not path.is_file() or path.stat().st_size > limit:
        raise GateReject("MISSING_OR_UNSAFE_INPUT_FILE")
    return path.read_bytes()


def _json(path: Path, *, limit: int = MAX_REQUEST) -> dict:
    raw = _read_file(path, limit=limit)
    try:
        obj = json.loads(raw)
    except (ValueError, UnicodeDecodeError) as e:
        raise GateReject("INVALID_LOCAL_JSON") from e
    if not isinstance(obj, dict):
        raise GateReject("INVALID_LOCAL_JSON_ROOT")
    return obj


def _money(value: object) -> Decimal:
    if type(value) not in (float, int):
        raise GateReject("INVALID_POLICY_COST_TYPE")
    try:
        v = Decimal(str(value))
    except InvalidOperation as e:
        raise GateReject("INVALID_POLICY_COST") from e
    if not v.is_finite() or v <= 0 or v > 100 or v.as_tuple().exponent < -2:
        raise GateReject("INVALID_POLICY_COST")
    return v


def _target_money(s: str) -> Decimal:
    try:
        d = Decimal(s)
    except InvalidOperation as e:
        raise GateReject("INVALID_REQUIRED_BUDGET") from e
    if not d.is_finite() or d <= 0 or d > 100 or d.as_tuple().exponent < -2:
        raise GateReject("INVALID_REQUIRED_BUDGET")
    return d


def _registered_policy_map(config: dict) -> dict:
    rp = config.get("review_policy")
    if not isinstance(rp, dict):
        raise GateReject("LIVE_REVIEW_POLICY_MISSING")
    refs = rp.get("known_run_policy_refs")
    if not isinstance(refs, dict) or not refs:
        raise GateReject("LIVE_POLICY_REGISTRY_MISSING")
    return refs


def select_policy(config: dict, intent: str, required_budget: Decimal) -> str:
    """Choose only locally registered refs; unified selects POLICY-STATIC-V1 at USD 3."""
    if intent not in INTENTS:
        raise GateReject("UNKNOWN_REVIEW_INTENT")
    if intent == "unified" and required_budget != Decimal(DEFAULT_BUDGETS["unified"]):
        raise GateReject("UNIFIED_REVIEW_BUDGET_MISMATCH")
    refs = _registered_policy_map(config)
    selected = next((name for name in INTENTS[intent] if name in refs), None)
    if not selected:
        raise GateReject("POLICY_NOT_INSTALLED")
    entry = refs[selected]
    if not isinstance(entry, dict):
        raise GateReject("POLICY_CONFIG_INVALID")
    configured = _money(entry.get("max_budget_usd"))
    if configured != required_budget:
        raise GateReject("POLICY_COST_MISMATCH")
    return selected


def _front_matter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise GateReject("REQUEST_FRONTMATTER_MISSING")
    end = text.find("\n---\n", 4)
    if end < 0 or end > 40_000:
        raise GateReject("REQUEST_FRONTMATTER_INVALID")
    fields: dict[str, str] = {}
    # Read simple top-level scalars; disallow duplicate keys. Nested knowledge refs ignored.
    for raw in text[4:end].splitlines():
        if not raw.strip() or raw.startswith("  - ") or raw.startswith("    "):
            continue
        match = re.fullmatch(r"([a-z][a-z0-9_]*):(?: (.*))?", raw)
        if match is None:
            raise GateReject("REQUEST_FRONTMATTER_UNSUPPORTED")
        key = match.group(1)
        if key in fields:
            raise GateReject("REQUEST_DUPLICATE_FIELD")
        fields[key] = (match.group(2) or "").strip()
    return fields


def _check_package(package: Path, *, sha: str, size: int) -> None:
    if package.is_symlink() or not package.is_file() or size <= 0 or size > MAX_PACKAGE:
        raise GateReject("PACKAGE_MISSING_OR_UNSAFE")
    if package.stat().st_size != size:
        raise GateReject("PACKAGE_SIZE_MISMATCH")
    h = hashlib.sha256()
    with package.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    if h.hexdigest() != sha:
        raise GateReject("PACKAGE_SHA256_MISMATCH")
    try:
        with zipfile.ZipFile(package) as archive:
            if archive.testzip() is not None:
                raise GateReject("PACKAGE_ZIP_CRC_FAILURE")
            seen: set[str] = set()
            for member in archive.infolist():
                name = member.filename
                p = PurePosixPath(name)
                if (not name or name.startswith("/") or "\\" in name
                        or ".." in p.parts or "" in p.parts
                        or name in seen or stat.S_IFMT(member.external_attr >> 16) == stat.S_IFLNK):
                    raise GateReject("UNSAFE_PACKAGE_MEMBER")
                seen.add(name)
    except (zipfile.BadZipFile, RuntimeError, OSError) as e:
        raise GateReject("INVALID_PACKAGE_ZIP") from e


def check_request(request: Path, package: Path, live_config: Path,
                  *, intent: str, required_budget: Decimal) -> dict:
    request_bytes = _read_file(request, limit=MAX_REQUEST)
    fields = _front_matter(request_bytes.decode("utf-8"))
    if (fields.get("schema") != "SKILL_COLLAB_REVIEW_REQUEST_V1"
            or fields.get("state") != "SUBMITTED"
            or fields.get("request_revision") != "1"
            or fields.get("test_policy") != "STATIC_ONLY"
            or fields.get("reviewer_os") != "WINDOWS"):
        raise GateReject("REQUEST_CONTRACT_MISMATCH")
    request_id = fields.get("request_id", "")
    if not REQ_ID.fullmatch(request_id):
        raise GateReject("INVALID_REQUEST_ID")
    if fields.get("project_id") != fields.get("work_id"):
        raise GateReject("PROJECT_WORK_SCOPE_MISMATCH")
    for key in ("project_id", "skill_id"):
        value = fields.get(key, "")
        if not value or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{2,100}", value):
            raise GateReject("INVALID_REQUEST_SCOPE")
    policy = fields.get("run_policy_ref", "")
    if not REF.fullmatch(policy):
        raise GateReject("INVALID_RUN_POLICY_REF")
    target = select_policy(_json(live_config), intent, required_budget)
    if policy != target:
        raise GateReject(f"RUN_POLICY_NOT_LIVE_MATCH: requested={policy} supported={target}")
    rawpath = fields.get("package_path", "")
    if not rawpath.startswith("/SKILL-COLLAB/packages/") or ".." in PurePosixPath(rawpath).parts:
        raise GateReject("INVALID_PACKAGE_PATH")
    if Path(rawpath).name != package.name or not package.name.endswith(".zip"):
        raise GateReject("PACKAGE_BASENAME_MISMATCH")
    sha = fields.get("package_sha256", "")
    if not SHA256.fullmatch(sha):
        raise GateReject("INVALID_PACKAGE_SHA256")
    try:
        count = int(fields.get("package_size_bytes", ""))
    except ValueError as e:
        raise GateReject("INVALID_PACKAGE_SIZE") from e
    _check_package(package, sha=sha, size=count)
    return {"status": "PASS_PREPUBLICATION_ONLY", "request_id": request_id,
            "skill_id": fields["skill_id"],
            "request_sha256": hashlib.sha256(request_bytes).hexdigest(),
            "run_policy_ref": policy, "expected_max_budget_usd": str(required_budget),
            "package_sha256": sha, "package_size_bytes": count,
            "authorization": "NOT_CHECKED", "ready": "NOT_CREATED", "model_calls": 0}


def check_source_pin(pin_path: Path, expected_repo_id: str, expected_commit: str) -> None:
    if not REPO_ID.fullmatch(expected_repo_id) or not COMMIT.fullmatch(expected_commit):
        raise GateReject("INVALID_EXPECTED_SOURCE_PIN")
    pin = _json(pin_path, limit=8192)
    if set(pin) != {"schema", "commit", "repo_id"} or pin.get("schema") != "SKILL_COLLAB_SOURCE_PIN_V1":
        raise GateReject("SOURCE_PIN_SCHEMA_MISMATCH")
    if type(pin.get("repo_id")) is not str or pin["repo_id"] != expected_repo_id:
        raise GateReject("SOURCE_PIN_REPO_ID_MISMATCH")
    if type(pin.get("commit")) is not str or pin["commit"] != expected_commit:
        raise GateReject("SOURCE_PIN_COMMIT_MISMATCH")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Offline prepublish gate; never approves/executes/posts")
    subs = parser.add_subparsers(dest="command", required=True)
    for command in ("select", "check"):
        p = subs.add_parser(command)
        p.add_argument("--live-config", type=Path, required=True,
                       help="actual Windows local reviewer.config.json, never GitHub")
        p.add_argument("--intent", choices=sorted(INTENTS), required=True)
        p.add_argument("--required-budget-usd", default=None,
                       help="required per-review budget, default unified=3 (legacy skill=1.5/design=3)")
        if command == "check":
            p.add_argument("--request", required=True, type=Path, help="new REQUEST before publish")
            p.add_argument("--package", required=True, type=Path, help="exact local ZIP bytes")
            p.add_argument("--source-pin", type=Path, help="optional post-commit pin check")
            p.add_argument("--expected-repo-id", help="required with --source-pin")
            p.add_argument("--expected-source-commit", help="required with --source-pin")
    args = parser.parse_args(argv)
    try:
        budget = _target_money(args.required_budget_usd or DEFAULT_BUDGETS[args.intent])
        if args.command == "select":
            ref = select_policy(_json(args.live_config), args.intent, budget)
            print(json.dumps({"status": "POLICY_COMPATIBLE_NOT_APPROVED",
                              "selected_run_policy_ref": ref,
                              "expected_max_budget_usd": str(budget), "approval": "NOT_CHECKED"}))
        else:
            result = check_request(args.request, args.package, args.live_config,
                                   intent=args.intent, required_budget=budget)
            if any((args.source_pin, args.expected_repo_id, args.expected_source_commit)):
                if not all((args.source_pin, args.expected_repo_id, args.expected_source_commit)):
                    raise GateReject("INCOMPLETE_SOURCE_PIN_CHECK")
                check_source_pin(args.source_pin, args.expected_repo_id, args.expected_source_commit)
                result["source_pin"] = "PASS"
            print(json.dumps(result, sort_keys=True))
    except (GateReject, OSError, UnicodeError) as e:
        print("REQUEST_PREFLIGHT_BLOCKED: " + str(e), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

```


### FILE: collab/ops/submit_review_request.py
Git blob: `0bccbb045780ada51ebaa2daf593f9f49ccf5e78` at main revision `828238e9d0c851a47d0342612a9d081052119fa3`.

```text
#!/usr/bin/env python3
"""Fail-closed CoWork formal-review submitter. No signing, READY, or model calls.

Only supported write path: verified Git main -> Commit A (REQUEST + ZIP) ->
remote readback -> Commit B (SOURCE_PIN) -> pinned-tree check -> remote readback.
No automatic retry: partial publications must be reconciled by an operator.
"""
from __future__ import annotations

import argparse
from decimal import Decimal
import json
from pathlib import Path
import re
import subprocess
import sys

from review_request_gate import GateReject, check_request
from review_pin_preflight import PreflightBlocked, inspect
from source_pin import dumps_source_pin

REPO = 'wonhwipark/CoWork-Skill-Collab'
BRANCH = 'main'
REPO_ID = '1451933830'
VALID_ORIGINS = {
    f'https://github.com/{REPO}.git', f'https://github.com/{REPO}',
    f'git@github.com:{REPO}.git', f'git@github.com:{REPO}',
    f'ssh://git@github.com/{REPO}.git',
}
RID_RE = re.compile(r'REQ-[A-Z0-9][A-Z0-9-]{3,120}\Z')


class SubmissionBlocked(ValueError):
    pass


def check_approval_route(skill_id: str, approval_route: str,
                         delegated_skills: tuple[str, ...]) -> dict:
    """Fail closed before any Git writes; does NOT grant signer authority.

    Auto skill IDs must come from the Windows protected signer's currently
    loaded delegation, not a README, prior run, or caller's assumption.
    The protected signer independently revalidates authorization and limits.
    """
    if approval_route not in ('manual', 'auto'):
        raise SubmissionBlocked('INVALID_APPROVAL_ROUTE')
    if approval_route == 'auto':
        if not delegated_skills:
            raise SubmissionBlocked('AUTO_DELEGATION_SCOPE_NOT_SUPPLIED')
        if skill_id not in delegated_skills:
            raise SubmissionBlocked('AUTO_NOT_ELIGIBLE_SCOPE: ' + skill_id)
        return {'approval_route': 'auto',
                'delegation_scope_preflight': 'MATCHES_SUPPLIED_SCOPE_NOT_SIGNER_VERIFIED'}
    return {'approval_route': 'manual',
            'delegation_scope_preflight': 'MANUAL_PROTECTED_APPROVAL_REQUIRED'}


def git(root: Path, *args: str) -> str:
    proc = subprocess.run(['git', '-C', str(root), *args], capture_output=True,
                          text=True, encoding='utf-8', timeout=45, check=False)
    if proc.returncode:
        raise SubmissionBlocked('GIT_FAILURE: ' + ' '.join(args[:2]))
    return proc.stdout.strip()


def require_clean_main(root: Path, *, expected_origin: str | None = None) -> str:
    if Path(git(root, 'rev-parse', '--show-toplevel')).resolve() != root.resolve():
        raise SubmissionBlocked('NOT_REPOSITORY_ROOT')
    if git(root, 'branch', '--show-current') != BRANCH:
        raise SubmissionBlocked('NOT_ON_MAIN')
    if git(root, 'status', '--porcelain', '--untracked-files=normal'):
        raise SubmissionBlocked('DIRTY_WORKTREE')
    remote = git(root, 'remote', 'get-url', 'origin')
    if remote not in ({expected_origin} if expected_origin else VALID_ORIGINS):
        raise SubmissionBlocked('UNTRUSTED_ORIGIN')
    local = git(root, 'rev-parse', 'HEAD')
    ref = git(root, 'ls-remote', 'origin', f'refs/heads/{BRANCH}').split()
    if len(ref) != 2 or ref[1] != f'refs/heads/{BRANCH}' or ref[0] != local:
        raise SubmissionBlocked('STALE_MAIN_OR_REMOTE_UNKNOWN')
    return local


def verify_remote_head(root: Path, expected: str) -> None:
    remote = git(root, 'ls-remote', 'origin', f'refs/heads/{BRANCH}').split()
    if len(remote) != 2 or remote[0] != expected:
        raise SubmissionBlocked('REMOTE_HEAD_READBACK_MISMATCH')


def submit(*, root: Path, request_draft: Path, package: Path,
           live_config: Path, publish: bool, expected_origin: str | None = None,
           approval_route: str = 'manual',
           delegated_skills: tuple[str, ...] = ()) -> dict:
    root = root.resolve()
    original = require_clean_main(root, expected_origin=expected_origin)
    result = check_request(request_draft, package, live_config,
                           intent='unified', required_budget=Decimal('3.00'))
    rid = result['request_id']
    route = check_approval_route(result['skill_id'], approval_route, delegated_skills)
    if not RID_RE.fullmatch(rid):
        raise SubmissionBlocked('INVALID_REQUEST_ID')
    request_rel = f'collab/requests/{rid}/REQUEST.md'
    pin_rel = f'collab/requests/{rid}/SOURCE_PIN.json'
    package_rel = f'collab/packages/{package.name}'
    if (root / request_rel).exists() or (root / pin_rel).exists():
        raise SubmissionBlocked('REQUEST_ID_ALREADY_EXISTS_CREATE_ONLY')
    if git(root, 'ls-tree', '-r', '--name-only', 'HEAD', '--', request_rel, pin_rel):
        raise SubmissionBlocked('REQUEST_ID_ALREADY_IN_HISTORY')
    if package.is_symlink() or request_draft.is_symlink():
        raise SubmissionBlocked('SYMLINK_INPUT')
    source_request = request_draft.read_bytes()
    source_package = package.read_bytes()
    target_package = root / package_rel
    if target_package.exists():
        if target_package.is_symlink() or target_package.read_bytes() != source_package:
            raise SubmissionBlocked('EXISTING_PACKAGE_BYTES_DIFFER')
    if not publish:
        return {'status': 'PREPUBLICATION_PASS_NOT_SUBMITTED', 'request_id': rid,
                **route, 'source_head': original, 'package_sha256': result['package_sha256'],
                'signer_authority': 'NOT_VERIFIED', 'ready': 'NOT_CREATED'}
    request_target = root / request_rel
    request_target.parent.mkdir(parents=True, exist_ok=False)
    request_target.write_bytes(source_request)
    if not target_package.exists():
        target_package.parent.mkdir(parents=True, exist_ok=True)
        target_package.write_bytes(source_package)
    git(root, 'add', '--', request_rel, package_rel)
    git(root, 'commit', '-m', f'review {rid}: immutable REQUEST and ZIP')
    source_commit = git(root, 'rev-parse', 'HEAD')
    git(root, 'push', 'origin', f'HEAD:refs/heads/{BRANCH}')
    verify_remote_head(root, source_commit)
    if (subprocess.check_output(['git', '-C', str(root), 'show', f'{source_commit}:{request_rel}']) != source_request
            or subprocess.check_output(['git', '-C', str(root), 'show', f'{source_commit}:{package_rel}']) != source_package):
        raise SubmissionBlocked('SOURCE_COMMIT_BYTES_READBACK_MISMATCH')
    # Pin refers to Commit A, which already contains REQUEST and ZIP.
    pin_target = root / pin_rel
    pin_target.write_text(dumps_source_pin(source_commit=source_commit, repo_id=REPO_ID),
                          encoding='utf-8', newline='\n')
    git(root, 'add', '--', pin_rel)
    git(root, 'commit', '-m', f'review {rid}: source pin for verified commit A')
    pin_commit = git(root, 'rev-parse', 'HEAD')
    checked = inspect(root=root, request_id=rid, package_repo_path=package_rel,
                      expected_repo_id=REPO_ID, main_commit=pin_commit,
                      approval_mode=approval_route, delegated_skills=delegated_skills)
    if checked['status'] != 'PASS_PINNED_INPUTS_ONLY' or checked['pinned_commit'] != source_commit:
        raise SubmissionBlocked('PINNED_TREE_PREFLIGHT_FAILED')
    git(root, 'push', 'origin', f'HEAD:refs/heads/{BRANCH}')
    verify_remote_head(root, pin_commit)
    return {'status': 'SUBMITTED_AWAITING_PROTECTED_SIGNER', 'request_id': rid,
            **route, 'source_commit': source_commit, 'pin_commit': pin_commit,
            'package_sha256': result['package_sha256'],
            'signer_authority': 'NOT_VERIFIED', 'ready': 'NOT_CREATED',
            'model_calls': 0}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo-root', required=True, type=Path)
    ap.add_argument('--request-draft', required=True, type=Path)
    ap.add_argument('--package', required=True, type=Path)
    ap.add_argument('--live-config', required=True, type=Path,
                    help='actual Windows LIVE reviewer.config.json; never upload')
    ap.add_argument('--approval-route', choices=('manual', 'auto'), default='manual',
                    help='manual is the safe default; never an approval or signature')
    ap.add_argument('--delegated-skill', action='append', default=[],
                    help='auto only: skill IDs from currently loaded protected delegation; not signer proof')
    ap.add_argument('--publish', action='store_true',
                    help='explicitly push Commit A then Commit B to CoWork main')
    args = ap.parse_args()
    try:
        out = submit(root=args.repo_root, request_draft=args.request_draft,
                     package=args.package, live_config=args.live_config, publish=args.publish,
                     approval_route=args.approval_route,
                     delegated_skills=tuple(args.delegated_skill))
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0
    except (SubmissionBlocked, GateReject, PreflightBlocked, OSError, ValueError,
            subprocess.TimeoutExpired) as exc:
        print('FORMAL_REVIEW_SUBMISSION_BLOCKED: ' + str(exc), file=sys.stderr)
        print('No automatic retry. Reconcile Git HEAD, remote, signer and request history.', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())

```


### FILE: collab/ops/review_staged_submission.py
Git blob: `d33b3b5a4669cfb1e25a9c78d0b92209b0ffdbe7` at main revision `828238e9d0c851a47d0342612a9d081052119fa3`.

```text
#!/usr/bin/env python3
"""One-shot Windows entry for a Git-pinned CoWork staged review candidate.

Reuses submit_review_request.py for policy validation and two-commit submission.
Does NOT sign, authorize, publish READY, dispatch a review, or install a watcher.
Default is dry run. Never retries a partially published request.
"""
from __future__ import annotations

import argparse
import base64
import binascii
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile

from review_request_gate import GateReject, _front_matter, MAX_PACKAGE
from submit_review_request import SubmissionBlocked, require_clean_main, submit

WORK_ID = re.compile(r"[A-Z0-9][A-Z0-9-]{2,120}\Z")
SHA256 = re.compile(r"[a-f0-9]{64}\Z")
MAX_REQUEST = 256_000


def valid_staged_path(value: str, work_id: str, suffix: str) -> str:
    """Only read files under the designated Work, never arbitrary local paths."""
    root = f"collab/projects/{work_id}/"
    p = PurePosixPath(value)
    if (not value.startswith(root) or value.startswith("/")
            or "\\" in value or ".." in p.parts or value.endswith("/")
            or not value.endswith(suffix) or len(value) > 400):
        raise SubmissionBlocked("UNSAFE_STAGED_SOURCE_PATH")
    return value


def pinned_git_blob(root: Path, path: str, head: str, max_bytes: int) -> bytes:
    """Read only committed bytes at the verified HEAD; no checkout mutation."""
    try:
        # The immutable tree entry must be a regular file, not a symlink or submodule.
        meta = subprocess.run(["git", "-C", str(root), "ls-tree", head, "--", path],
                              capture_output=True, timeout=10, check=False)
        if meta.returncode or not meta.stdout.startswith((b"100644 blob ", b"100755 blob ")):
            raise SubmissionBlocked("STAGED_SOURCE_NOT_REGULAR_GIT_BLOB")
        size = subprocess.run(["git", "-C", str(root), "cat-file", "-s", f"{head}:{path}"],
                              capture_output=True, timeout=10, check=False)
        if size.returncode or not size.stdout.strip().isdigit() or not 0 < int(size.stdout) <= max_bytes:
            raise SubmissionBlocked("STAGED_SOURCE_UNAVAILABLE_OR_OVERSIZED")
        proc = subprocess.run(["git", "-C", str(root), "show", f"{head}:{path}"],
                              capture_output=True, timeout=30, check=False)
    except (OSError, subprocess.TimeoutExpired):
        raise SubmissionBlocked("STAGED_GIT_READ_UNCERTAIN") from None
    if proc.returncode != 0 or len(proc.stdout) != int(size.stdout):
        raise SubmissionBlocked("STAGED_SOURCE_UNAVAILABLE_OR_OVERSIZED")
    return proc.stdout


def prepare_staged_inputs(root: Path, work_id: str, draft_path: str,
                          candidate_path: str, head: str) -> tuple[bytes, bytes, str]:
    if not WORK_ID.fullmatch(work_id):
        raise SubmissionBlocked("INVALID_WORK_ID")
    draft_path = valid_staged_path(draft_path, work_id, ".md")
    candidate_path = valid_staged_path(candidate_path, work_id, ".zip.base64")
    if draft_path == candidate_path:
        raise SubmissionBlocked("STAGED_PATH_CONFLICT")
    request = pinned_git_blob(root, draft_path, head, MAX_REQUEST)
    try:
        fields = _front_matter(request.decode("utf-8"))
    except (UnicodeDecodeError, GateReject):
        raise SubmissionBlocked("INVALID_STAGED_REQUEST") from None
    if fields.get("project_id") != work_id or fields.get("work_id") != work_id:
        raise SubmissionBlocked("STAGED_WORK_MISMATCH")
    pkgpath = fields.get("package_path", "")
    name = PurePosixPath(pkgpath).name
    if pkgpath != f"/SKILL-COLLAB/packages/{name}":
        raise SubmissionBlocked("STAGED_PACKAGE_PATH_MISMATCH")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{4,180}\.zip", name):
        raise SubmissionBlocked("STAGED_PACKAGE_NAME_INVALID")
    try:
        size = int(fields.get("package_size_bytes", ""))
    except ValueError:
        raise SubmissionBlocked("INVALID_STAGED_PACKAGE_SIZE") from None
    sha = fields.get("package_sha256", "")
    if not 0 < size <= MAX_PACKAGE or not SHA256.fullmatch(sha):
        raise SubmissionBlocked("INVALID_STAGED_PACKAGE_PIN")
    base64_max = ((size + 2) // 3) * 4 + 4096
    encoded = pinned_git_blob(root, candidate_path, head, base64_max)
    try:
        package = base64.b64decode(b"".join(encoded.split()), validate=True)
    except (ValueError, binascii.Error):
        raise SubmissionBlocked("STAGED_BASE64_INVALID") from None
    if len(package) != size or hashlib.sha256(package).hexdigest() != sha:
        raise SubmissionBlocked("STAGED_PACKAGE_SHA_OR_SIZE_MISMATCH")
    return request, package, name


def run(*, root: Path, work_id: str, draft_path: str, candidate_path: str,
        live_config: Path, publish: bool = False, approval_route: str = "manual",
        delegated_skills: tuple[str, ...] = ()) -> dict:
    root = root.resolve()
    # Verifies clean main and exact remote HEAD before any local files or Git writes.
    head = require_clean_main(root)
    draft, package, name = prepare_staged_inputs(root, work_id, draft_path,
                                                  candidate_path, head)
    with tempfile.TemporaryDirectory(prefix="cowork-staged-review-") as tmp:
        work = Path(tmp)
        req = work / "REQUEST.md"
        pkg = work / name
        req.write_bytes(draft)
        pkg.write_bytes(package)
        result = submit(root=root, request_draft=req, package=pkg,
                        live_config=live_config, publish=publish,
                        approval_route=approval_route,
                        delegated_skills=delegated_skills)
    result.update({"source_head": head,
                   "staged_draft": draft_path,
                   "staged_candidate": candidate_path,
                   "host_signer": "NOT_INVOKED",
                   "ready": "NOT_CREATED",
                   "no_model_calls_by_entry": True})
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo-root", type=Path, required=True)
    ap.add_argument("--work-id", required=True)
    ap.add_argument("--draft-path", required=True)
    ap.add_argument("--candidate-path", required=True)
    ap.add_argument("--live-config", type=Path, required=True)
    ap.add_argument("--approval-route", choices=("manual", "auto"), default="manual")
    ap.add_argument("--delegated-skill", action="append", default=[])
    ap.add_argument("--publish", action="store_true", help="only submit REQUEST/ZIP and SOURCE_PIN; never READY")
    args = ap.parse_args()
    try:
        result = run(root=args.repo_root, work_id=args.work_id,
                     draft_path=args.draft_path, candidate_path=args.candidate_path,
                     live_config=args.live_config, publish=args.publish,
                     approval_route=args.approval_route,
                     delegated_skills=tuple(args.delegated_skill))
        print(json.dumps(result, sort_keys=True, ensure_ascii=False))
        return 0
    except (SubmissionBlocked, GateReject, OSError, ValueError) as exc:
        print("STAGED_REVIEW_SUBMISSION_BLOCKED: " + str(exc), file=sys.stderr)
        print("Do not retry automatically. Inspect source HEAD and protected signer history.", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

```


### FILE: collab/ops/review_pin_preflight.py
Git blob: `7a8c0a1dcc4c1430d5a14957a52d3d7db0b720aa` at main revision `828238e9d0c851a47d0342612a9d081052119fa3`.

```text
#!/usr/bin/env python3
"""Read-only pre-READY source pin / request / package git-tree coherence gate.

Designed to be run before any protected signer or READY action. This script
cannot approve, sign, post READY, run a watcher, or perform model calls.
Requires a locally fetched repository commit explicitly supplied by the caller;
remote main freshness and actual signer authority remain separate host gates.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

from source_pin import SourcePinError, verify_source_pin

HEX40 = re.compile(r"[0-9a-f]{40}\Z")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
DECIMAL = re.compile(r"[1-9][0-9]*\Z")
YAML_SIMPLE = re.compile(r"^([a-zA-Z_][a-zA-Z_0-9]*):[ \t]*(.*?)\s*$")
REQUEST_LIMIT = 262_144
PIN_LIMIT = 8192
PACKAGE_LIMIT = 200 * 1024 * 1024


class PreflightBlocked(ValueError):
    """Fail-closed; errors are not authorization or execution signals."""


def checked_path(value: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        raise PreflightBlocked("INVALID_REPO_PATH")
    p = PurePosixPath(value)
    if p.is_absolute() or any(part in (".", "..", "") for part in value.split("/")):
        raise PreflightBlocked("INVALID_REPO_PATH")
    if str(p) != value:
        raise PreflightBlocked("INVALID_REPO_PATH")
    return value


def run_git(root: Path, *argv: str, timeout: int = 25) -> bytes:
    try:
        p = subprocess.run(
            ["git", "-C", str(root), *argv],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            timeout=timeout, check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise PreflightBlocked("GIT_UNAVAILABLE_OR_TIMEOUT") from exc
    if p.returncode:
        raise PreflightBlocked("GIT_REF_OR_OBJECT_UNAVAILABLE")
    return p.stdout


def git_blob_at(root: Path, commit: str, path: str, limit: int, *, missing_code: str) -> bytes:
    checked_path(path)
    if not HEX40.fullmatch(commit):
        raise PreflightBlocked("INVALID_PIN_COMMIT")
    tree_line = run_git(root, "ls-tree", commit, "--", path).decode("utf-8", "replace").rstrip("\n")
    # A single exact path, regular file only; symlink/submodule/tree is unsafe.
    match = re.fullmatch(r"(100644|100755) blob ([0-9a-f]{40})\t(.+)", tree_line)
    if not match or match.group(3) != path:
        raise PreflightBlocked(missing_code)
    size_raw = run_git(root, "cat-file", "-s", match.group(2))
    try:
        size = int(size_raw.strip())
    except ValueError as exc:
        raise PreflightBlocked("UNREADABLE_BLOB_SIZE") from exc
    if size > limit:
        raise PreflightBlocked("INPUT_TOO_LARGE")
    data = run_git(root, "cat-file", "blob", match.group(2))
    if len(data) != size:
        raise PreflightBlocked("INCONSISTENT_BLOB_SIZE")
    return data


def yaml_header(blob: bytes) -> dict[str, str]:
    try:
        value = blob.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise PreflightBlocked("REQUEST_NOT_UTF8") from exc
    lines = value.splitlines()
    if not lines or lines[0] != "---":
        raise PreflightBlocked("REQUEST_MISSING_FRONTMATTER")
    fields: dict[str, str] = {}
    ended = False
    for line in lines[1:]:
        if line == "---":
            ended = True
            break
        m = YAML_SIMPLE.fullmatch(line)
        if not m:
            raise PreflightBlocked("REQUEST_UNPARSABLE_FRONTMATTER")
        k, v = m.groups()
        if k in fields:
            raise PreflightBlocked("REQUEST_DUPLICATE_FRONTMATTER_KEY")
        fields[k] = v.strip().strip('"\'')
    if not ended:
        raise PreflightBlocked("REQUEST_MISSING_FRONTMATTER_END")
    needed = ("schema", "state", "request_id", "request_revision", "skill_id", "package_path", "package_sha256", "package_size_bytes", "run_policy_ref")
    if any(not fields.get(k) for k in needed):
        raise PreflightBlocked("REQUEST_REQUIRED_FIELD_MISSING")
    if fields["schema"] != "SKILL_COLLAB_REVIEW_REQUEST_V1" or fields["state"] != "SUBMITTED":
        raise PreflightBlocked("REQUEST_SCHEMA_OR_STATE_MISMATCH")
    if not DECIMAL.fullmatch(fields["request_revision"]):
        raise PreflightBlocked("REQUEST_REVISION_INVALID")
    if not HEX64.fullmatch(fields["package_sha256"]):
        raise PreflightBlocked("REQUEST_PACKAGE_SHA_INVALID")
    if not DECIMAL.fullmatch(fields["package_size_bytes"]):
        raise PreflightBlocked("REQUEST_PACKAGE_SIZE_INVALID")
    if not re.fullmatch(r"[A-Za-z][A-Za-z_0-9-]{2,127}", fields["skill_id"]):
        raise PreflightBlocked("REQUEST_SKILL_ID_INVALID")
    return fields


def inspect(
    *, root: Path, request_id: str, package_repo_path: str,
    expected_repo_id: str, main_commit: str,
    approval_mode: str, delegated_skills: tuple[str, ...] = (),
) -> dict[str, object]:
    if not HEX40.fullmatch(main_commit):
        raise PreflightBlocked("INVALID_MAIN_COMMIT")
    if not re.fullmatch(r"REQ-[A-Za-z_0-9-]{4,180}", request_id):
        raise PreflightBlocked("INVALID_REQUEST_ID")
    package_repo_path = checked_path(package_repo_path)
    if approval_mode not in ("auto", "manual"):
        raise PreflightBlocked("INVALID_APPROVAL_MODE")
    if not DECIMAL.fullmatch(expected_repo_id):
        raise PreflightBlocked("INVALID_EXPECTED_REPO_ID")
    request_path = f"collab/requests/{request_id}/REQUEST.md"
    pin_path = f"collab/requests/{request_id}/SOURCE_PIN.json"
    pin_data = git_blob_at(root, main_commit, pin_path, PIN_LIMIT, missing_code="SOURCE_PIN_MISSING")
    try:
        pin = verify_source_pin(json.loads(pin_data.decode("utf-8")), expected_repo_id=expected_repo_id)
    except (ValueError, UnicodeError, SourcePinError) as exc:
        raise PreflightBlocked("SOURCE_PIN_FORMAT_OR_REPO_ID_MISMATCH") from exc
    pinned_commit = pin["commit"]
    current_req = git_blob_at(root, main_commit, request_path, REQUEST_LIMIT, missing_code="REQUEST_MISSING_AT_MAIN")
    pinned_req = git_blob_at(root, pinned_commit, request_path, REQUEST_LIMIT, missing_code="COMMIT_UNREADABLE_REQUEST_ABSENT")
    if current_req != pinned_req:
        raise PreflightBlocked("REQUEST_BYTES_CHANGED_SINCE_PIN")
    data = yaml_header(current_req)
    if data["request_id"] != request_id:
        raise PreflightBlocked("REQUEST_ID_MISMATCH")
    # Match the complete canonical repo path, not just a possibly reused ZIP basename.
    requested_path = data["package_path"]
    canonical_prefix = "/SKILL-COLLAB/packages/"
    if (not requested_path.startswith(canonical_prefix)
            or package_repo_path != "collab/packages/" + requested_path[len(canonical_prefix):]
            or "/" in requested_path[len(canonical_prefix):]):
        raise PreflightBlocked("PACKAGE_PATH_NAME_MISMATCH")
    package = git_blob_at(root, pinned_commit, package_repo_path, PACKAGE_LIMIT, missing_code="COMMIT_UNREADABLE_PACKAGE_ABSENT")
    if len(package) != int(data["package_size_bytes"]):
        raise PreflightBlocked("PACKAGE_SIZE_MISMATCH")
    if hashlib.sha256(package).hexdigest() != data["package_sha256"]:
        raise PreflightBlocked("PACKAGE_SHA256_MISMATCH")
    current_package = git_blob_at(root, main_commit, package_repo_path, PACKAGE_LIMIT, missing_code="PACKAGE_MISSING_AT_MAIN")
    if current_package != package:
        raise PreflightBlocked("PACKAGE_BYTES_CHANGED_SINCE_PIN")
    # This is a *pre-sign* gate. Existing READY must be reconciled, not replayed.
    for name in ("READY.md", "APPROVAL_SIG.json"):
        path = f"collab/requests/{request_id}/{name}"
        line = run_git(root, "ls-tree", main_commit, "--", path).decode("utf-8", "replace").strip()
        if line:
            raise PreflightBlocked("REQUEST_ALREADY_SIGNED_OR_READY_RECONCILE")
    if approval_mode == "auto":
        if not delegated_skills:
            raise PreflightBlocked("DELEGATION_SCOPE_NOT_SUPPLIED")
        if data["skill_id"] not in delegated_skills:
            raise PreflightBlocked("AUTO_NOT_ELIGIBLE_SKILL_ID")
    return {
        "status": "PASS_PINNED_INPUTS_ONLY",
        "request_id": request_id,
        "request_revision": int(data["request_revision"]),
        "pinned_commit": pinned_commit,
        "request_sha256": hashlib.sha256(pinned_req).hexdigest(),
        "package_sha256": data["package_sha256"],
        "package_size_bytes": len(package),
        "skill_id": data["skill_id"],
        "run_policy_ref": data["run_policy_ref"],
        "approval_mode": approval_mode,
        "signer_authority": "NOT_VERIFIED",
        "ready_or_model_calls": 0,
        "next_gate": "PROTECTED_SIGNER_AUTHORITY_AND_DUPLICATE_CHECK",
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Read-only CoWork pre-READY pinned request/package check")
    p.add_argument("--repo-root", required=True, type=Path)
    p.add_argument("--main-commit", required=True, help="Verified remote main commit SHA fetched separately")
    p.add_argument("--request-id", required=True)
    p.add_argument("--package-repo-path", required=True)
    p.add_argument("--expected-repo-id", required=True)
    p.add_argument("--approval-mode", choices=("auto", "manual"), required=True)
    p.add_argument("--delegated-skill", action="append", default=[], help="Actual signer loaded allowlist; for auto mode only")
    args = p.parse_args(argv)
    try:
        result = inspect(root=args.repo_root, request_id=args.request_id,
                         package_repo_path=args.package_repo_path,
                         expected_repo_id=args.expected_repo_id,
                         main_commit=args.main_commit,
                         approval_mode=args.approval_mode,
                         delegated_skills=tuple(args.delegated_skill))
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except (PreflightBlocked, OSError) as exc:
        print(f"REVIEW_PIN_PREFLIGHT_BLOCKED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

```


### FILE: collab/ops/source_pin.py
Git blob: `0f270bf247e2dd0e4104acf89ac973ae2c3c08f0` at main revision `828238e9d0c851a47d0342612a9d081052119fa3`.

```text
#!/usr/bin/env python3
"""Canonical CoWork SOURCE_PIN V1 serializer and strict pre-publication verifier.

Local/offline helper only: no GitHub writes, READY, signing, watcher, or LLM calls.
A blocked/uncertain review must be reconciled separately; never patch its pinned
inputs in place to force another processing attempt.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

SCHEMA = "SKILL_COLLAB_SOURCE_PIN_V1"
_COMMIT_RE = re.compile(r"[0-9a-f]{40}\Z")
_REPO_ID_RE = re.compile(r"[1-9][0-9]*\Z")
_EXACT_KEYS = frozenset({"schema", "commit", "repo_id"})


class SourcePinError(ValueError):
    """Malformed pin or unsafe publication input; refuse rather than coerce."""


def canonical_repo_id(value: str | int) -> str:
    """Normalize only producer inputs. Never silently normalize a published pin."""
    if type(value) is int:
        value = str(value)
    if not isinstance(value, str) or _REPO_ID_RE.fullmatch(value) is None:
        raise SourcePinError("repo_id must be a nonzero decimal identifier")
    return value


def make_source_pin(*, source_commit: str, repo_id: str | int) -> dict[str, str]:
    if not isinstance(source_commit, str) or _COMMIT_RE.fullmatch(source_commit) is None:
        raise SourcePinError("commit must be the exact lowercase, 40-hex source commit A")
    return {"schema": SCHEMA, "commit": source_commit, "repo_id": canonical_repo_id(repo_id)}


def verify_source_pin(pin: object, *, expected_repo_id: str | None = None) -> dict[str, str]:
    """Strict consumer/pre-publish check. Numeric JSON repo_id is ALWAYS invalid."""
    if not isinstance(pin, dict) or set(pin) != _EXACT_KEYS or pin.get("schema") != SCHEMA:
        raise SourcePinError("invalid SOURCE_PIN_V1 schema or keys")
    commit, repo_id = pin["commit"], pin["repo_id"]
    if not isinstance(commit, str) or _COMMIT_RE.fullmatch(commit) is None:
        raise SourcePinError("invalid commit pin")
    if type(repo_id) is not str or _REPO_ID_RE.fullmatch(repo_id) is None:
        raise SourcePinError("repo_id MUST be a JSON string, not a number")
    if expected_repo_id is not None and repo_id != canonical_repo_id(expected_repo_id):
        raise SourcePinError("REPO_ID_MISMATCH")
    return pin


def dumps_source_pin(*, source_commit: str, repo_id: str | int) -> str:
    pin = make_source_pin(source_commit=source_commit, repo_id=repo_id)
    verify_source_pin(pin)
    return json.dumps(pin, ensure_ascii=False, indent=2) + "\n"


def _read_checked(path: Path, expected_repo_id: str | None) -> dict[str, str]:
    if path.is_symlink() or not path.is_file() or path.stat().st_size > 8192:
        raise SourcePinError("unsafe or oversized input path")
    pin = json.loads(path.read_text(encoding="utf-8"))
    return verify_source_pin(pin, expected_repo_id=expected_repo_id)


def audit_source_pins(root: Path, *, expected_repo_id: str) -> int:
    """Check all published request pins; no GitHub API or mutation.

    A malformed historical pin is a failure, never silently rewritten.
    """
    base = root / "collab" / "requests"
    if base.is_symlink() or not base.is_dir():
        raise SourcePinError("missing or unsafe collab/requests directory")
    count = 0
    for directory in sorted(base.iterdir()):
        if directory.is_symlink() or not directory.is_dir():
            continue
        path = directory / "SOURCE_PIN.json"
        if path.is_symlink():
            raise SourcePinError(f"unsafe source pin: {path}")
        if path.exists():
            try:
                _read_checked(path, expected_repo_id)
            except (SourcePinError, json.JSONDecodeError) as exc:
                raise SourcePinError(f"{path}: {exc}") from exc
            count += 1
    if count == 0:
        raise SourcePinError("no published SOURCE_PIN.json found")
    return count


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Offline CoWork SOURCE_PIN_V1 generator / validator")
    sub = parser.add_subparsers(dest="command", required=True)
    make = sub.add_parser("create", help="build new pin; never change existing REQUEST or READY")
    make.add_argument("--commit", required=True, help="verified source commit A (40 lowercase hex)")
    make.add_argument("--repo-id", required=True, help="numeric GitHub repository ID (encoded as JSON string)")
    make.add_argument("--output", type=Path, help="local new file only; refuses overwrite")
    audit = sub.add_parser("audit", help="check all published pins without modifying them")
    audit.add_argument("--root", type=Path, default=Path("."))
    audit.add_argument("--expected-repo-id", required=True)
    check = sub.add_parser("check", help="validate existing file without modifying it")
    check.add_argument("path", type=Path)
    check.add_argument("--expected-repo-id", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "create":
            content = dumps_source_pin(source_commit=args.commit, repo_id=args.repo_id)
            if args.output is None:
                sys.stdout.write(content)
            else:
                # No implicit directories or writes to existing pinned input.
                with args.output.open("x", encoding="utf-8", newline="\n") as out:
                    out.write(content)
                print("CREATED: local SOURCE_PIN candidate only; no request/READY posted")
        elif args.command == "audit":
            count = audit_source_pins(args.root, expected_repo_id=args.expected_repo_id)
            print(f"PASS: {count} SOURCE_PIN_V1 files match the repo_id string contract")
        else:
            _read_checked(args.path, args.expected_repo_id)
            print("PASS: SOURCE_PIN_V1 repo_id is a JSON string and matches trust root")
    except (SourcePinError, json.JSONDecodeError, OSError, UnicodeError) as exc:
        print(f"SOURCE_PIN_REJECTED: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

```


### FILE: collab/projects/COWORK-AUTO-APPROVAL-20261115-001/REVIEW_INTAKE_ONE_SHOT_HOST_INTEGRATION_r0001_20261122_KST.md
Git blob: `8519ad45a78c09003b90d9235b59e070ffe67789` at main revision `828238e9d0c851a47d0342612a9d081052119fa3`.

```text
# CoWork 단축 리뷰 요청 → Windows 정식 제출 연결 r0001

- 작성: 2026-11-22 KST
- 기존 Work: `COWORK-AUTO-APPROVAL-20261115-001`
- 참조 Work: `COWORK-SKILL-DISCOVERY-20261112-001` (P1/P2 실제 입력 후보)
- 정본: GitHub PUBLIC `wonhwipark/CoWork-Skill-Collab`, branch `main`
- **상태:** `STAGED_INPUT_ADAPTER=CODE_PUBLISHED_TESTED`, `WINDOWS_RELAY_HOOK=NOT_INSTALLED`, `FORMAL_REQUEST=NOT_POSTED`, `MODEL_CALLS=0`

## 1. 사용자 목표·확인된 연결 공백

- 동일 설계 대화창에서 사용자 **“리뷰요청해줘”** → 해당 Work 최신 설계·소스·시험을 선택 → **정식 Windows Claude Code 리뷰 요청**. 긴 프롬프트와 Windows 수동 명령을 반복 요구하지 않는 것이 최종 목표.
- 현재 GPT가 정상적으로 GitHub에 후보 ZIP(Base64)·REQUEST 초안·인계를 게시할 수 있으나, 기존 Windows v0.2.29 LIVE watcher는 유효한 REQUEST/서명/READY 기반 처리기다. **후보에서 실제 Windows 정책 사전검사 → Git Commit A/B 요청 게시**를 자동 실행하도록 연결된 host-side 접수 단계는 확인되지 않았다.
- 등록된 자동 위임 허용 목록 외 `skill_id`는 기존 정책상 공식 수동 signer 검증이 필요하다. 새 연결이 생겨도 **GitHub 게시/ChatGPT 지시/문서의 승인 주장으로 보호 서명을 대신할 수 없다**.

## 2. 구현: 기존 제출기 재사용, 기본 읽기 전용

- [새 보조 진입 코드](../../ops/review_staged_submission.py): 실제 Windows checkout의 **클린 main·원격 HEAD 일치**를 기존 `submit_review_request.require_clean_main`으로 확인 → 기존 Work 하위 **커밋된 REQUEST 초안·Base64 ZIP**만 Git object에서 읽음 → 일반 파일 모드·크기·path 탈출·YAML Work·ZIP 경로/크기/SHA-256 확인 → 격리 임시 폴더로 바이트 복원 → 기존 `submit_review_request.submit` 재사용.
- `--publish`가 없으면 **기본 dry-run**. `--publish`가 있어도 기존 LIVE `review_request_gate.check_request`와 제출기 게이트가 성공할 때만 Commit A(REQUEST+ZIP), Commit B(SOURCE_PIN), 원격 readback을 수행. **서명/READY/모델 호출·알림·호스트 설정 변경 없음.**
- [시험 원문](../../ops/tests/test_review_staged_submission.py): 임시 실제 Git repository를 사용한 11건 격리 단위시험 PASS. `submit`과 보호 signer/네트워크는 mock. 테스트한 로컬 코드 파일과 GitHub main 원격 **Git blob SHA 완전 일치**.
- 코드 SHA-256: `review_staged_submission.py` = `5d4dfffe0f1fd92d543a7a352d60d3d5aed5196d6e7f2e5b2183d9605276b518`, Git blob = `d33b3b5a4669cfb1e25a9c78d0b92209b0ffdbe7`.
- 테스트 SHA-256: `test_review_staged_submission.py` = `3fb6a9dd0937a3b14ccc08b537b4784179bfff944a1ca7c5c234ba16b1c2c1e2`, Git blob = `ebe467de726048f223c94a92336ae4f4d7ed1c60`.
- **제약:** 이 코드는 기존 제출기로 연결하는 로컬 진입점이며 Windows에 자동 설치·호출된 watcher hook이 아니다. 호스트 환경에서 실제 CLI 및 다른 기존 회귀 전체 실행은 `NOT_RUN`. P1/P2 94,843B ZIP의 Windows 새 독립 재검증도 `NOT_RUN`.

## 3. 기존 P1/P2의 정확한 입력과 검증 경로

입력은 다음 기존 **동일 Work**에 이미 고정되어 있으며 새 ZIP이나 REVIEW ID를 만들지 않는다.

- Work: `COWORK-SKILL-DISCOVERY-20261112-001`
- Request 후보: `REQ-COWORK-P1P2-CONTEXT-CODE-R1-20261122` (새 재큐잉 금지)
- Draft: `collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/P1_P2_FORMAL_REVIEW_REQUEST_UNPOSTED_DRAFT_r0001_20261122_KST.md`
- Candidate: `collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/P1_P2_REVIEW_CANDIDATE_r0001_1122.zip.base64`
- ZIP 고정 94,843 bytes, SHA-256 `35de54934944807518e0141daaedde1888a42c08c1d264584e9b341f65dcd5f3`
- Skill ID `cowork-context-design` **변경 금지**. 과거 위임 허용 목록 밖 → 공식 signer의 실제 AUTO 갱신 여부 또는 유효한 수동 승인 확인.

Windows의 **승인된 기존 세션**에서 다음 명령은 첫 단계 `--publish` 없는 사전검사다. `<ACTUAL_WINDOWS_LIVE_CONFIG_PATH>`는 운영 PC에서 실제 경로 확인 후 대체하며 토큰·설정 본문 공유 금지.

```powershell
python collab/ops/review_staged_submission.py --repo-root . --work-id COWORK-SKILL-DISCOVERY-20261112-001 --draft-path collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/P1_P2_FORMAL_REVIEW_REQUEST_UNPOSTED_DRAFT_r0001_20261122_KST.md --candidate-path collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/P1_P2_REVIEW_CANDIDATE_r0001_1122.zip.base64 --live-config "<ACTUAL_WINDOWS_LIVE_CONFIG_PATH>" --approval-route manual
```

`PREPUBLICATION_PASS_NOT_SUBMITTED` 이후에도 **Windows official signer의 정책/대상/권한·과거 기록**을 확인해야 한다. 기존 유효 승인과 권한이 확인될 때만 동일 명령에 `--publish`를 추가하고, `SUBMITTED_AWAITING_PROTECTED_SIGNER` 이후 승인·서명·READY 마지막 게시·리뷰 1회를 기존 계약대로 별도 처리한다.

## 4. 진짜 원샷을 위한 Windows 기존 watcher 연결 (아직 미적용)

- 권장: **기존 watcher/정기 run_cycle에 후보 접수 단계 1개를 안전하게 연결**. 별도 상주 watcher, 새로운 예약 작업, 유료 GPT/Claude 자동 승인 엔진을 만들지 않는다. v0.2.29 실제 설치본과 운용 중인 `orchestrator`·`watch_loop` 인터페이스를 Windows에서 실측한 뒤 기존 Task의 승인된 업데이트 절차로만 연결한다.
- 입력 발견은 **사용자가 리뷰 요청한 동일 Work의 고정 후보**에 한정. SOURCE_PIN 없는 초안/ZIP 및 일반 `CURRENT.md` 변화 자체는 watcher **리뷰 실행 트리거가 아니다**. 별도 사용자 리뷰 요청의 출처·단일 Work·commit pin을 확인한 후 사전검사만 연결한다.
- 이미 있는 REQUEST/PIN, APPROVAL_SIG/READY, REVIEW/RECEIPT, 감사 DB/UNCERTAIN이 발견되면 **중복 제출·재서명·재큐잉 없이 기존 건 정산**. 멀티창 HEAD 충돌/미확인/승인 범위 밖은 fail-closed, 오류 후 무조건 재시도 없음.
- Windows 기존 설치 파일·Task·DB/WAL/SHM·보호 signer/키/위임·Notifier 및 유료 운영 설정 수정은 **현재 이번 코드 게시에서 하지 않았음**. 호스트 hook 설치·재시작·롤백은 해당 유효 운영 승인/백업/실측이 확인될 때만 진행.
- **남은 직접 검증:** Windows에서 `--publish` 없는 정확한 P1/P2 사전검사와 11건 회귀 소스를 실제 실행 → 보호 수동 signer 권한 여부·비용·중복 확인 → 기존 run_cycle에 안전한 후크 위치와 비승인 우회 여부 독립 검토 → 허용 범위의 설치·SHADOW→실제로 새 user-intent 1건 E2E. 그 전에는 `AUTO_FORMAL_REVIEW_INTAKE=NOT_APPLIED`.

## 5. 상태 및 다음 한 행동

- `CODE_PUBLISHED=PASS`, `GIT_BLOB_REMOTE_READBACK=PASS`, `ISOLATED_LOCAL_TEST=10_PASS`
- `REAL_SUBMITTER_INTEGRATION_TEST=NOT_RUN`, `WINDOWS_HOST_PREFLIGHT=NOT_RUN`, `WATCHER_INTAKE_HOOK=NOT_APPLIED`
- `P1P2_REQUEST=NOT_POSTED`, `APPROVAL_SIG/READY=NOT_POSTED`, `INDEPENDENT_REVIEW=NOT_RUN`, `PAID_MODEL_CALLS=0`.
- **NEXT_ONE_ACTION:** Windows Claude Code가 기존 호스트의 실제 권한·설정·watcher hook 가능성을 무과금 G0 점검하고 위 코드 `--publish` 없는 dry-run과 11개 회귀 시험을 1회 수행. 통합 설치가 승인 범위 밖이면 필요한 운영 변경 승인만 요청하고 기존 Work에 BLOCKED/NOT_RUN 게시. 기존 P1/P2 유료 리뷰는 보호 승인 확인 전 절대 실행하지 않음.

```

