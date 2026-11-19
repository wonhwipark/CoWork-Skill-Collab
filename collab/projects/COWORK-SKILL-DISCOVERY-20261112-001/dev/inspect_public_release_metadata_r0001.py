"""Inspect public, already-released ZIP metadata only (no host/business data)."""
import io, json, urllib.request, zipfile
for name in ("code-analyzer_v0_15_2_1107.zip", "l1-fix-workflow_v1_6_67_1110.zip"):
    url="https://raw.githubusercontent.com/wonhwipark/L1Work/main/"+name
    with urllib.request.urlopen(url, timeout=30) as resp:
        raw=resp.read()
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        matches=[p for p in z.namelist() if p.endswith("/.skill-release.json")]
        if len(matches)!=1:
            print(json.dumps({"archive":name,"release_meta_matches":len(matches)}))
            continue
        info=json.loads(z.read(matches[0]).decode("utf-8"))
        keys=("version","channel","release_kind","review","review_status","approved","public_release","archive","based_on","release_date")
        print(json.dumps({"archive":name,"size":len(raw),"release_meta":{k:info.get(k) for k in keys if k in info}},ensure_ascii=False,sort_keys=True))
