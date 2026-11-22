"""Offline supplementary check; never imports/runs AutoApprover or signer."""
import ast
import hashlib
import importlib.util
import json
import sys
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace

root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / 'r2-review-input/validation_source/v0_2_33'
spec = importlib.util.spec_from_file_location('offline_auto_policy', root / 'skill_collab_watcher/auto_policy.py')
auto_policy = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = auto_policy
spec.loader.exec_module(auto_policy)
tree = ast.parse((root / 'skill_collab_watcher/auto_approval.py').read_text())
cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'AutoApprover')
fn = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == '_revalidate')
now = 2_000_000_000
intent_expiry = now - 1
rid = 'SYNTHETIC-R2-EXPIRY'
d = auto_policy.Delegation(True, '1', 'main', frozenset({'P'}), frozenset({'original'}), now + 86400, now - 100)
env = dict(json=json, replace=replace, auto_policy=auto_policy,
           load_delegation=lambda *a: (d, 'ok'), project_scope=lambda *a: d,
           review_intent=SimpleNamespace(INTENT_KEY_PURPOSE='REVIEW_INTENT'),
           TransportError=type('SyntheticTransportError', (Exception,), {}),
           AuthRequired=type('SyntheticAuthRequired', (Exception,), {}))
exec(compile(ast.Module(body=[fn], type_ignores=[]), '<verbatim candidate _revalidate AST>', 'exec'), env)
stored = dict(project='P', skill='extra', repo_id='1', branch='main', created_at=now-50,
              commit='a'*40, request_sha256='b'*64, zip_sha256='c'*64,
              policy='POLICY-STATIC-V1', cents=0, state='REQUESTED',
              intent_nonce='synthetic-once', intent_key_id='synthetic-key')
obj = SimpleNamespace(s=SimpleNamespace(delegation_file=None, acl_check=None))
store = SimpleNamespace(window_usage=lambda *a, **kw: dict(day_calls=0, day_cents=0, month_cents=0),
                        review_intent_nonce_owner=lambda n: rid)
transport = SimpleNamespace(repository_id=lambda: '1')
trust = SimpleNamespace(keys={'synthetic-key': SimpleNamespace(status='ACTIVE', purpose='REVIEW_INTENT')})
observed = env['_revalidate'](obj, transport, store, rid, '1', {'candidate_json': json.dumps(stored)}, now, trust)
# The original envelope/deadline is absent in the real persisted candidate_json;
# intent_expiry describes the earlier consumed intent in this synthetic scenario.
assert observed == (True, 'ok')
manifest = json.loads((root / 'docs/RELEASE_MANIFEST.json').read_text())
missing, mismatch = [], []
for entry in manifest['files']:
    p = root / entry['path']
    if not p.is_file():
        missing.append(entry['path'])
    else:
        raw = p.read_bytes()
        if len(raw) != entry['bytes'] or hashlib.sha256(raw).hexdigest() != entry['sha256']:
            mismatch.append(entry['path'])
out = dict(scope='GPT offline supplementary check; actual function/pure gate with synthetic dependencies; no signer, network, host DB or model',
           revalidation=dict(original_intent_expiry=intent_expiry, now=now, delegation_expiry=d.expires_at,
                             observed=list(observed), verdict='FAIL_SECURITY_INVARIANT',
                             limitation='Not full pipeline or cryptographic verification; original intent deadline is not persisted or read'),
           manifest=dict(version=manifest['version'], mismatches=mismatch, missing=missing))
Path(__file__).with_name('supplementary_evidence.json').write_text(json.dumps(out, ensure_ascii=False, indent=2)+'\n')
print(json.dumps(dict(revalidation=out['revalidation'], manifest_version=manifest['version'], mismatches=len(mismatch), missing=len(missing))))
