import sys, json
sys.dont_write_bytecode = True
sys.path.insert(0, r"D:\User\whpark\skill-collab-watcher-github")
sys.path.insert(0, r"D:\User\whpark\cowork-phase1\a_review")
import approver_ops as ops
st = ops.status()
print(json.dumps({k: st.get(k) for k in ("folder_exists", "files", "key_id", "private_key_decrypts", "key_file_has_plain_base64_key", "repo_id", "fingerprint")}, indent=2))
