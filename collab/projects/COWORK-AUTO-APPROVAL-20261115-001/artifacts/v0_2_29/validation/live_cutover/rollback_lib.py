"""Byte-checked rollback of the install tree, config and protected delegation from a verified backup bundle. The DB is NOT touched here:
it is restored only by an explicit decision when no paid job ran after the cutover (the DB is unchanged while the watcher is stopped)."""
import shutil
from cutover_common import *


def acl_lines(path):
    out = subprocess.run(["icacls", str(path)], capture_output=True, text=True).stdout
    lines = []
    for line in out.splitlines():
        line = line.strip()
        if "(" in line and ":" in line:
            lines.append(line.split(str(path))[-1].strip() if str(path) in line else line)
    return sorted(set(lines))


def atomic_write(path, data):
    tmp = path.with_name(path.name + ".cutover.tmp")
    tmp.write_bytes(data)
    os.replace(tmp, path)


def rollback(bundle):
    bundle = pathlib.Path(bundle)
    res = {"bundle": str(bundle)}
    b_tree = tree(bundle / "install")
    for rel in b_tree:
        dst = LIVE / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        atomic_write(dst, (bundle / "install" / rel).read_bytes())
    removed = []
    for rel in tree(LIVE):
        if rel not in b_tree:
            (LIVE / rel).unlink()
            removed.append(rel)
    atomic_write(DELEG, (bundle / "protected" / "auto_delegation.json").read_bytes())
    res["removed_new_files"] = removed
    res["tree_sha"] = tree_sha(tree(LIVE))
    res["config_sha"] = sha(CFG)
    res["delegation_sha"] = sha(DELEG)
    res["version_line"] = (LIVE / "skill_collab_watcher" / "__init__.py").read_text(encoding="utf-8").strip()
    res["verified"] = (res["tree_sha"] == EXPECT["live_tree"] and res["config_sha"] == EXPECT["config_sha"] and res["delegation_sha"] == EXPECT["delegation_sha"])
    return res
