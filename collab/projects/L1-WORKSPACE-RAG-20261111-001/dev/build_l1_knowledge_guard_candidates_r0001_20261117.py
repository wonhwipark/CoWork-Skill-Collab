#!/usr/bin/env python3
"""One-shot, pinned source patch builder. Development packages only.

Inputs: exact L1 zip packages under the given repository working tree.
Does not install skills, publish group knowledge, or change a live host.
"""
from __future__ import annotations
import argparse
import compileall
import hashlib
import json
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

PINS = {
    'workflow': {
        'path': 'collab/projects/L1-WORKSPACE-RAG-20261111-001/candidates/l1-fix-workflow_v1_6_69_1115.zip',
        'sha256': 'd4ba119298cd5763fd18ace2d54223fff010a8d2a1703ebab80eb4fa1b35846b',
        'version_from': '1.6.69', 'version_to': '1.6.70',
        'output': 'l1-fix-workflow_v1_6_70_1117.zip', 'root': 'l1-fix-workflow',
    },
    'github': {
        'path': 'collab/projects/L1-WORKSPACE-RAG-20261111-001/candidates/l1-github_v0_3_57_1114.zip',
        'sha256': 'f1b8fb43d3af427f2c5d52864051c65894f3cb45969ab35ca502f344735611ce',
        'version_from': '0.3.57', 'version_to': '0.3.59',
        'output': 'l1-github_v0_3_59_1117.zip', 'root': '',
    },
    'kernel': {
        'path': 'artifacts/work-ledger-kernel_v0_7_42_1116.zip',
        'sha256': 'ece2bce143ef35a1c8cc3bc12ddf6a73e27e0f218fc69fec87844759d9dfc164',
        'version_from': '0.7.42', 'version_to': '0.7.43',
        'output': 'work-ledger-kernel_v0_7_43_1117.zip', 'root': '',
    },
}

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(path: Path, before: str, after: str, *, label: str) -> None:
    s = path.read_text(encoding='utf-8')
    count = s.count(before)
    if count != 1:
        raise RuntimeError(f'{label}: exact anchor matched {count} times, expected 1 in {path}')
    path.write_text(s.replace(before, after), encoding='utf-8', newline='\n')


def safe_unzip(source: Path, dest: Path) -> None:
    with zipfile.ZipFile(source, 'r') as z:
        bad = z.testzip()
        if bad:
            raise RuntimeError(f'ZIP CRC FAIL: {bad}')
        names = set()
        for info in z.infolist():
            name = info.filename
            p = PurePosixPath(name)
            if (not name or name.startswith('/') or '..' in p.parts or '\\' in name
                    or name in names or stat.S_IFMT(info.external_attr >> 16) == stat.S_IFLNK):
                raise RuntimeError(f'Unsafe ZIP member: {name!r}')
            names.add(name)
        z.extractall(dest)


WORKFLOW_HELPER = '''\n\ndef _reject_personal_knowledge_write_paths(root: Path, paths: list[str]) -> None:
    """Workflow is only a reader of personal knowledge/. This is a local defense.

    Not a security boundary against an agent holding raw Git write credentials;
    that must be checked at the installed writer/OS boundary.
    """
    base = root.expanduser().resolve()
    protected = (base / "knowledge").resolve()
    for candidate in paths:
        raw = str(candidate).replace("\\\\", "/")
        pure = PurePosixPath(raw)
        if not raw or pure.is_absolute() or any(p in ("", ".", "..") for p in pure.parts):
            raise GitHubDocsError("WORK_DOCS_PATH_INVALID: ambiguous publication path")
        if pure.parts[0].casefold() == "knowledge":
            raise GitHubDocsError("WORK_DOCS_KNOWLEDGE_WRITE_BLOCKED: Workflow may not write knowledge/")
        target = (base / raw).resolve()
        if target == protected or protected in target.parents:
            raise GitHubDocsError("WORK_DOCS_KNOWLEDGE_WRITE_BLOCKED: protected path alias")
        if base not in target.parents and target != base:
            raise GitHubDocsError("WORK_DOCS_PATH_ESCAPE_BLOCKED")
\n'''


def patch_workflow(root: Path) -> None:
    p = root / 'l1_fix_workflow/github_docs.py'
    replace_once(p, '\ndef docs_sync(kernel, ', WORKFLOW_HELPER + '\ndef docs_sync(kernel, ', label='workflow guard declaration')
    anchor = '    out=kernel.work_docs_export(resolved["repo_root"],work_id)\n'
    extra = '''    # Updater exclusively owns personal knowledge/. Reject a changed-path leak.
    # Kernel exporter is separately required to preserve all knowledge files.
'''
    replace_once(p, anchor,
                 anchor + '    try:\n'
                 + '        _reject_personal_knowledge_write_paths(Path(resolved["repo_root"]), list(out.get("changed_files") or []))\n'
                 + '    except GitHubDocsError as exc:\n'
                 + "        return {'ok':False,'action':'WORK_DOCS_KNOWLEDGE_WRITE_BLOCKED','reason':str(exc)}\n",
                 label='workflow post-export guard')
    anchor = '    extra_paths=sorted(set(extra_paths or []))\n'
    replace_once(p, anchor,
                 anchor + '    try:\n'
                 + '        _reject_personal_knowledge_write_paths(Path(sync.get("repo_root") or repo_root or "."),\n'
                 + '            extra_paths + list(sync.get("changed_files") or []))\n'
                 + '    except GitHubDocsError as exc:\n'
                 + "        return {'ok':False,'action':'WORK_DOCS_KNOWLEDGE_WRITE_BLOCKED','reason':str(exc)}\n",
                 label='workflow pre-synced/extra-path guard')
    sk = root / 'SKILL.md'
    s = sk.read_text(encoding='utf-8')
    s += '\n\n### 개인 Knowledge 보호 (개발 후보 v1.6.70)\n\n'
    s += '- `l1-workspace/knowledge/`는 `l1-knowledge-updater`만 쓰기 요청, Workflow는 READ_ONLY.\n'
    s += '- 실제 `docs_sync`/`docs_push`의 changed_files·extra_paths를 검증하고 knowledge/ 변경·경로 우회를 거부.\n'
    s += '- 이 검사는 raw Git/동일 OS credential을 차단하지 않으므로 HARD_ENFORCEMENT는 호스트 검증 전 NOT_VERIFIED.\n'
    sk.write_text(s.replace('1.6.69','1.6.70'), encoding='utf-8', newline='\n')

GITHUB_GUARD = '''\n\ndef assert_work_docs_knowledge_unchanged(root: Path | str) -> dict:
    """Fail-closed defense when l1-github handles a Workflow Work-docs write.

    Caller identity/OS permissions are not proven by this function. Do not use
    it as authorization for l1-knowledge-updater or unguarded raw Git commands.
    """
    root = Path(root).expanduser().resolve()
    try:
        cp = subprocess.run(['git', '-C', str(root), 'status', '--porcelain=v1',
                             '-z', '--untracked-files=all'], capture_output=True,
                            timeout=12, check=False)
    except (OSError, subprocess.TimeoutExpired):
        raise PushGuardError('WORK_DOCS_STATUS_UNVERIFIED') from None
    if cp.returncode:
        raise PushGuardError('WORK_DOCS_STATUS_UNVERIFIED')
    parts = cp.stdout.split(b'\\x00')
    names = []
    i = 0
    while i < len(parts):
        item = parts[i]
        i += 1
        if not item:
            continue
        if len(item) < 4 or item[2:3] != b' ':
            raise PushGuardError('WORK_DOCS_STATUS_MALFORMED')
        status = item[:2].decode('ascii', errors='replace')
        names.append(item[3:].decode('utf-8', errors='surrogateescape'))
        if 'R' in status or 'C' in status:
            if i >= len(parts) or not parts[i]:
                raise PushGuardError('WORK_DOCS_RENAME_SOURCE_MISSING')
            names.append(parts[i].decode('utf-8', errors='surrogateescape'))
            i += 1
    for name in names:
        path = name.replace('\\\\', '/')
        components = path.split('/')
        if (not path or path.startswith('/') or path.startswith('../')
            or any(x in ('', '.', '..') for x in components)):
            raise PushGuardError('WORK_DOCS_PATH_INVALID')
        if components[0].casefold() == 'knowledge':
            raise PushGuardError('WORK_DOCS_KNOWLEDGE_WRITE_BLOCKED')
        candidate = (root / path).resolve()
        if root not in candidate.parents and candidate != root:
            raise PushGuardError('WORK_DOCS_PATH_ESCAPE')
        protected = (root / 'knowledge').resolve()
        if candidate == protected or protected in candidate.parents:
            raise PushGuardError('WORK_DOCS_KNOWLEDGE_WRITE_BLOCKED')
    return {'ok': True, 'action': 'WORK_DOCS_KNOWLEDGE_PATH_PREFLIGHT_PASS',
            'checked_paths': len(names), 'hard_enforcement': False}
\n'''



GITHUB_OUTBOUND_GUARD = r'''

def assert_work_docs_outbound_knowledge_unchanged(root: Path | str) -> dict:
    """Deny a Work-docs push if an outgoing commit changes knowledge/.

    This is a local defense; a raw Git command with shared write credentials
    can bypass it, so host OS/credential isolation remains a separate gate.
    """
    root = Path(root).expanduser().resolve()

    def call(*args: str) -> bytes:
        try:
            cp = subprocess.run(['git', '-C', str(root), *args],
                                capture_output=True, timeout=12, check=False)
        except (OSError, subprocess.TimeoutExpired):
            raise PushGuardError('WORK_DOCS_OUTBOUND_GIT_UNVERIFIED') from None
        if cp.returncode:
            raise PushGuardError('WORK_DOCS_OUTBOUND_GIT_UNVERIFIED')
        return cp.stdout.strip()

    upstream = call('rev-parse', '--symbolic-full-name', '@{upstream}').decode('utf-8')
    if not upstream.startswith('refs/remotes/') or '..' in upstream:
        raise PushGuardError('WORK_DOCS_OUTBOUND_UPSTREAM_UNVERIFIED')
    commits = call('rev-list', '--reverse', upstream + '..HEAD').splitlines()
    if len(commits) > 500:
        raise PushGuardError('WORK_DOCS_OUTBOUND_HISTORY_TOO_LARGE')
    for raw_sha in commits:
        sha = raw_sha.decode('ascii')
        paths = call('diff-tree', '--root', '-m', '--no-renames', '--name-only',
                     '-r', '-z', sha).split(b'\x00')
        for raw in paths:
            if not raw:
                continue
            path = raw.decode('utf-8', 'surrogateescape').replace('\\', '/')
            parts = path.split('/')
            if not path or any(p in ('', '.', '..') for p in parts):
                raise PushGuardError('WORK_DOCS_OUTBOUND_PATH_UNSAFE')
            if parts[0].casefold() == 'knowledge':
                raise PushGuardError('WORK_DOCS_COMMITTED_KNOWLEDGE_BLOCKED')
    return {'ok': True, 'action': 'WORK_DOCS_OUTBOUND_HISTORY_PASS',
            'inspected_commits': len(commits), 'hard_enforcement': False}

'''


def patch_github(root: Path) -> None:
    p = root / 'scripts/push_guard.py'
    replace_once(p, '\ndef verify(*, root:', GITHUB_GUARD + GITHUB_OUTBOUND_GUARD + '\ndef verify(*, root:', label='github shared protection declaration')
    script = root / 'scripts/l1_github.py'
    s = script.read_text(encoding='utf-8')
    for tag in ('work_docs_commit', 'work_docs_push'):
        before = f'        return cross_host_git.{tag}(args, globals())'
        after = '        push_guard.assert_work_docs_knowledge_unchanged(repo_root())\n' + (('        push_guard.assert_work_docs_outbound_knowledge_unchanged(repo_root())\n') if tag == 'work_docs_push' else '') + before
        if s.count(before) != 1:
            raise RuntimeError(f'github {tag} anchor count={s.count(before)}')
        s = s.replace(before, after)
    script.write_text(s, encoding='utf-8', newline='\n')
    sk = root / 'SKILL.md'
    txt = sk.read_text(encoding='utf-8')
    txt += '\n\n### Workflow 개인 Knowledge 경로 보호 (개발 후보 v0.3.59)\n'
    txt += '- Work-docs commit/push entrypoint의 status-staged/unstaged/untracked 경로에 `knowledge/` 변경이 있으면 fail-closed.\n'
    txt += '- raw Git/동일 자격증명 우회 가능성은 별도 호스트 권한 경계의 G0 검증 조건이며 본 guard만으로 완전 차단 주장 금지.\n'
    sk.write_text(txt.replace('0.3.57','0.3.59'), encoding='utf-8', newline='\n')


def patch_kernel(root: Path) -> None:
    p = root / 'work_ledger_kernel/work_ux.py'
    anchor = '        root = Path(repo_root).expanduser().resolve()\n        root.mkdir(parents=True, exist_ok=True)\n'
    replace_once(p, anchor,
        '        root = Path(repo_root).expanduser().resolve()\n'
        '        # Updater-owned knowledge is never an exporter output.\n'
        '        # Refuse symlink/unsafe replacement without touching its contents.\n'
        '        knowledge_root = root / "knowledge"\n'
        '        knowledge_readme = knowledge_root / "README.md"\n'
        '        if (knowledge_root.is_symlink() or (knowledge_root.exists() and not knowledge_root.is_dir())\n'
        '            or knowledge_readme.is_symlink()):\n'
        '            raise KernelError("WORK_DOCS_KNOWLEDGE_UNSAFE_PATH", "Personal Knowledge path is unsafe")\n'
        '        root.mkdir(parents=True, exist_ok=True)\n',label='kernel knowledge protection')
    before = '        write_communication(root, "README.md", "\\n".join(dashboard))\n'
    after = ('        # Only a human navigation link; all knowledge files remain immutable to Kernel.\n'
             '        if knowledge_readme.is_file():\n'
             '            dashboard += ["## 개인 Knowledge", "", "[Knowledge 탐색](knowledge/README.md)", ""]\n'
             + before)
    replace_once(p, before, after, label='kernel root README knowledge link')
    sk = root / 'SKILL.md'
    txt = sk.read_text(encoding='utf-8')
    txt += '\n\n### 개인 Knowledge와 exporter 공존 (개발 후보 v0.7.43)\n'
    txt += '- `work_ux.export_docs`는 Updater 전용 `knowledge/`를 읽기 전용으로 유지하며 실제 `knowledge/README.md`가 있을 때 루트 탐색 링크만 생성.\n'
    txt += '- Kernel 신규 Knowledge Profile/ref_type/원장은 선제 도입하지 않음. Work-side backlink 실제 계약은 G0 이후 확정.\n'
    sk.write_text(txt.replace('0.7.42','0.7.43'), encoding='utf-8', newline='\n')



def refresh_package_metadata(root: Path, row: dict) -> None:
    """Regenerate only existing package metadata; keep candidate non-deployable."""
    version = row["version_to"]
    # Update only canonical header declarations; retain historical version notes.
    import re
    skill_md = root / "SKILL.md"
    if skill_md.is_file():
        text = skill_md.read_text(encoding="utf-8")
        lines = text.splitlines(keepends=True)
        for i, line in enumerate(lines[:45]):
            match = re.match(
                r"^(\s*(?:(?:version|skill_version|버전)|(?:[-#* ]{0,6}(?:current version|현재 버전)))\s*[:：]\s*[\"\x27]?)v?\d+\.\d+\.\d+",
                line, re.I)
            if match:
                lines[i] = line[:match.start()] + match.group(1) + version + line[match.end():]
        skill_md.write_text("".join(lines), encoding="utf-8", newline="\n")
    version_md = root / "VERSION.md"
    if version_md.is_file():
        content = version_md.read_text(encoding="utf-8")
        lines = content.splitlines(keepends=True)
        for i, line in enumerate(lines[:15]):
            if re.search(r"\d+\.\d+\.\d+", line):
                lines[i] = re.sub(r"(?<!\d)v?\d+\.\d+\.\d+(?!\d)",
                                  "v" + version, line, count=1)
                break
        version_md.write_text("".join(lines), encoding="utf-8", newline="\n")
    # The embedded skillsilent policy manifest carries the hosting skill version.
    # Synchronize only the package-owned version keys, never skillsilent's tool version.
    policy_manifest = root / "skillsilent" / "manifest.json"
    if policy_manifest.is_file():
        meta = json.loads(policy_manifest.read_text(encoding="utf-8"))
        for key in ("skill_version", "package_version"):
            if key in meta:
                meta[key] = version
        policy_manifest.write_text(
            json.dumps(meta, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8")
    version_file = root / "VERSION"
    if version_file.is_file():
        version_file.write_text(version + "\n", encoding="utf-8")
    release = root / ".skill-release.json"
    if release.is_file():
        data = json.loads(release.read_text(encoding="utf-8"))
        data["version"] = version
        if "skill_version" in data:
            data["skill_version"] = version
        data["revision"] = int(version.split(".")[-1])
        data["archive"] = row["output"]
        data["channel"] = "development_not_for_deployment"
        data["release_kind"] = "development_not_for_deployment"
        data["based_on"] = row["version_from"]
        data["release_date"] = "2026-11-17"
        data["built_at"] = "2026-11-17T01:00:00+09:00"
        release.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    main_meta = root / ".skill-main.json"
    if main_meta.is_file():
        meta = json.loads(main_meta.read_text(encoding="utf-8"))
        if isinstance(meta, dict):
            if str(meta.get("version", "")) in (row["version_from"], version):
                meta["version"] = version
            if str(meta.get("skill_version", "")) in (row["version_from"], version):
                meta["skill_version"] = version
            main_meta.write_text(json.dumps(meta, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    # Derive the hash universe from the files that will actually ship in ZIP.
    # Never reuse an old manifest's key set: it silently loses newly added files.
    rels = sorted(
        p.relative_to(root).as_posix() for p in root.rglob("*")
        if p.is_file()
        and p.name not in ("MANIFEST_SHA256.json", "PACKAGE_CONTENTS.sha256")
        and "__pycache__" not in p.relative_to(root).parts
        and p.suffix != ".pyc"
        and p.relative_to(root).parts[0] != "artifacts"
    )
    manifest = root / "MANIFEST_SHA256.json"
    listing = root / "PACKAGE_CONTENTS.sha256"
    if not manifest.is_file() and not listing.is_file():
        raise RuntimeError("RELEASE_HASH_MANIFEST_MISSING")
    digest_map = {rel: sha(root / rel) for rel in rels}
    if manifest.is_file():
        manifest.write_text(json.dumps(digest_map, ensure_ascii=False, indent=2,
                                       sort_keys=True) + "\n", encoding="utf-8")
    if listing.is_file():
        listing.write_text("".join(f"{digest_map[rel]}  {rel}\n" for rel in rels),
                           encoding="utf-8")


def rezip(root: Path, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=8) as z:
        files = sorted((p for p in root.rglob('*') if p.is_file()), key=lambda p: p.as_posix())
        for p in files:
            rel = p.relative_to(root).as_posix()
            if ('/__pycache__/' in '/' + rel + '/' or rel.endswith('.pyc')
                or rel.startswith('artifacts/')):
                continue
            z.write(p, rel)
    with zipfile.ZipFile(output) as z:
        assert z.testzip() is None
        paths = [x.filename for x in z.infolist()]
        assert len(paths) == len(set(paths)), 'duplicate zip entry'


def run_build(workdir: Path, outdir: Path, *, skip_pin: bool = False) -> dict:
    out = {}
    with tempfile.TemporaryDirectory(prefix='knowledge-guards-build-') as tmp:
        for key, row in PINS.items():
            src = workdir / row['path']
            if not src.is_file():
                raise RuntimeError(f'MISSING_BASELINE: {src}')
            actual = sha(src)
            if not skip_pin and actual != row['sha256']:
                raise RuntimeError(f'BASELINE_SHA_MISMATCH: {key} expected={row["sha256"]} actual={actual}')
            x = Path(tmp) / key
            safe_unzip(src, x)
            p = x / row['root'] if row['root'] else x
            {'workflow':patch_workflow,'github':patch_github,'kernel':patch_kernel}[key](p)
            refresh_package_metadata(p, row)
            if not compileall.compile_dir(str(p), quiet=1):
                raise RuntimeError(f'PYTHON_COMPILE_FAIL: {key}')
            output = outdir / row['output']
            rezip(x, output)
            from skill_release_quality_gate import validate
            checked = validate(output, row["version_to"])
            out[key] = {'baseline':row['path'],'baseline_sha256':actual,'output':str(output),
                        'output_sha256':sha(output),'size_bytes':output.stat().st_size,
                        'verification':'ZIP_CRC_AND_PYTHON_COMPILE_AND_RELEASE_GATE_PASS',
                        'release':'development_not_for_deployment'}
    return out


def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--skip-pin',action='store_true',help='local synthetic diagnostic ONLY')
    args=ap.parse_args()
    results=run_build(args.repo.resolve(), args.out.resolve(), skip_pin=args.skip_pin)
    manifest=args.out/'BUILD_RESULT.json'
    manifest.write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(manifest.read_text(encoding='utf-8'))
    return 0

if __name__=='__main__':
    raise SystemExit(main())