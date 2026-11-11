"""Read-only GitHub PRIVATE review-chain dashboard projection, not an approval verifier."""
import hashlib
import html
import json
import re
from pathlib import Path
from urllib.parse import quote

VALID_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,100}\Z")
SHA_RE = re.compile(r"[0-9a-f]{64}\Z")
DECISIONS = {"ACCEPT", "ACCEPT_WITH_CHANGE", "REJECT", "DEFER", "NEED_INFO"}
FINDING_RE = re.compile(r"^(?:#{2,5}\s*|[-*]\s*\*{0,2})([A-Z]{1,5}-\d{1,4})\b[\s:.)*\]-]*(.{0,160})$")


def read(path, limit=300000):
    try:
        if path.is_symlink() or not path.is_file() or path.stat().st_size > limit:
            return None
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return None


def metadata(raw):
    if raw is None:
        return {}
    if raw.lstrip().startswith("{"):
        try:
            obj = json.loads(raw)
            return obj if isinstance(obj, dict) else {}
        except ValueError:
            return {}
    if not raw.startswith("---\n"):
        return {}
    end = raw.find("\n---", 4)
    if end == -1 or end > 16000:
        return {}
    result = {}
    for line in raw[4:end].splitlines():
        m = re.fullmatch(r"([A-Za-z][A-Za-z0-9_]*)\s*:\s*(.*?)\s*", line)
        if m and m[2] and m[2][0] not in "[{|>" and len(m[2]) <= 512:
            s = m[2].strip().strip("'\"")
            result[m[1]] = {"true": True, "false": False}.get(s.lower(), s)
    return result


def source(root, family, rid, filenames):
    folder = root / "collab" / family / rid
    if not folder.is_dir() or folder.is_symlink():
        return "", None, {}
    for name in filenames:
        raw = read(folder / name)
        if raw is not None:
            return f"collab/{family}/{rid}/{name}", raw, metadata(raw)
    return "", None, {}


def matches(obj, rid, rev, sha, idfield="request_id", revfield="request_revision"):
    return obj.get(idfield) == rid and str(obj.get(revfield)) == rev and obj.get("package_sha256") == sha


def receipt_matches(receipt, review, rid, rev, sha):
    if not matches(receipt, rid, rev, sha) or receipt.get("ok") is not True:
        return False
    key = receipt.get("processing_key")
    parts = key.split("|") if isinstance(key, str) else []
    return (len(parts) == 4 and parts[:3] == [rid, rev, sha] and
            parts[3].isdigit() and int(parts[3]) > 0 and review.get("review_id") in (None, key))


def extract_findings(raw, disposition):
    found = []
    structured = disposition.get("findings")
    if isinstance(structured, list):
        for item in structured[:25]:
            if not isinstance(item, dict):
                continue
            fid, decision = item.get("id"), item.get("decision")
            if isinstance(fid, str) and re.fullmatch(r"[A-Z]{1,5}-\d{1,4}", fid) and decision in DECISIONS:
                found.append({"id": fid, "decision": decision, "summary": " ".join(str(item.get("summary", "")).split())[:115]})
        return found
    if raw:
        for line in raw.splitlines()[:4000]:
            match = FINDING_RE.match(line.strip())
            if match and not any(x["id"] == match[1] for x in found):
                found.append({"id": match[1], "decision": "NOT_ADJUDICATED", "summary": " ".join(match[2].split())[:115]})
                if len(found) >= 25:
                    break
    return found


def inspect(root, rid):
    rp, raw, req = source(root, "requests", rid, ("REQUEST.md", "REQUEST.json"))
    yp, yr, ready = source(root, "requests", rid, ("READY.md", "READY.json"))
    vp, vr, review = source(root, "reviews", rid, ("REVIEW_RESULT_1.md", "REVIEW_RESULT.md", "REVIEW_RESULT.json"))
    cp, cr, receipt = source(root, "receipts", rid, ("RECEIPT_1.md", "RECEIPT.md", "RECEIPT.json"))
    gp, gr, gpt = source(root, "reviews", rid, ("GPT_DISPOSITION.json",))
    paths = dict(request=rp, ready=yp, review=vp, receipt=cp, gpt=gp)
    flags = {k: False for k in paths}
    rev, sha = str(req.get("request_revision", "")), req.get("package_sha256")
    valid = (raw is not None and req.get("request_id") == rid and rev.isdigit() and
             int(rev) > 0 and isinstance(sha, str) and SHA_RE.fullmatch(sha))
    stage, tone = "REQUEST_INVALID", "danger"
    if valid:
        flags["request"] = True
        stage, tone = "READY_NOT_OBSERVED", "warning"
        if yr is not None:
            good = (matches(ready, rid, rev, sha) and ready.get("state") == "READY"
                    and ready.get("request_sha256") == hashlib.sha256(raw.encode("utf-8")).hexdigest())
            if not good:
                stage, tone = "READY_MISMATCH", "danger"
            else:
                flags["ready"] = True
                stage, tone = "REVIEW_NOT_OBSERVED", "warning"
                if vr is not None:
                    if not matches(review, rid, rev, sha, "responds_to_request_id", "responds_to_request_revision") or review.get("execution_status") != "COMPLETED":
                        stage, tone = "REVIEW_INCOMPLETE_OR_MISMATCH", "danger"
                    else:
                        flags["review"] = True
                        stage, tone = "RECEIPT_NOT_OBSERVED", "warning"
                        if cr is not None:
                            if not receipt_matches(receipt, review, rid, rev, sha):
                                stage, tone = "RECEIPT_MISMATCH", "danger"
                            else:
                                flags["receipt"] = True
                                stage, tone = "GPT_NOT_OBSERVED", "warning"
                                if gr is not None:
                                    if not matches(gpt, rid, rev, sha) or gpt.get("verdict") not in DECISIONS:
                                        stage, tone = "GPT_DISPOSITION_MISMATCH", "danger"
                                    else:
                                        flags["gpt"] = True
                                        stage, tone = "GPT_RECORDED_UNAUTHENTICATED", "neutral"
    return {"id": rid, "work_id": str(req.get("work_id") or "미확인")[:100] if valid else "미확인",
            "revision": rev if valid else "미확인", "stage": stage, "tone": tone,
            "flags": flags, "paths": paths,
            "findings": extract_findings(vr if flags["review"] else None, gpt if flags["gpt"] else {}),
            "disposition": gpt.get("verdict") if flags["gpt"] else "NOT_VERIFIED",
            "trust": "DOCUMENT_FIELDS_MATCH_ONLY_SIGNATURE_NOT_VERIFIED"}


def collect(root):
    base = root / "collab" / "requests"
    if base.is_symlink() or not base.is_dir():
        return []
    folders = sorted((x for x in base.iterdir() if x.is_dir() and not x.is_symlink() and VALID_ID.fullmatch(x.name)), key=lambda x: x.name)
    return [inspect(root, f.name) for f in folders[:300] if (f / "REQUEST.md").exists() or (f / "REQUEST.json").exists()]


def href(repo, path):
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo) or not re.fullmatch(r"collab/(?:requests|reviews|receipts)/[A-Za-z0-9_-]{1,101}/[A-Za-z0-9_.-]{1,80}", path):
        raise ValueError("invalid source")
    return "https://github.com/" + repo + "/blob/main/" + quote(path, safe="/")


def render_html(chains, repo):
    e = html.escape
    cards = []
    for x in chains:
        rows = []
        for label, field in (("요청", "request"), ("READY", "ready"), ("리뷰", "review"), ("영수증", "receipt"), ("GPT 판정", "gpt")):
            path = x["paths"][field]
            status = "일치 기록" if x["flags"][field] else ("불일치/미검증" if path else "미확인")
            link = f'<a href="{e(href(repo, path), quote=True)}" rel="noopener noreferrer">{e(label)}</a>' if path else e(label)
            rows.append(f"<li>{link} · {e(status)}</li>")
        items = "".join(f'<li><b>{e(f["id"])}</b> · {e(f["decision"])} · {e(f["summary"])}</li>' for f in x["findings"])
        feedback = f'<strong>피드백 {len(x["findings"])}건</strong><ul>{items}</ul>' if items else '<p class="minor">항목별 피드백 미확인</p>'
        cards.append(f'<article class="card"><div class="card-top"><span class="pill {e(x["tone"])}">{e(x["stage"])}</span></div><h3>{e(x["id"])}</h3><p class="topic">Work {e(x["work_id"])} · revision {e(x["revision"])}</p><ol>{"".join(rows)}</ol>{feedback}</article>')
    rendered = "\n".join(cards) if cards else '<p class="empty">GitHub 리뷰 요청 미이관 · 리뷰 완료 0건이 아닙니다.</p>'
    return '<section aria-label="GitHub 리뷰 진행"><div class="toolbar"><h2>REQUEST → READY → REVIEW → RECEIPT → GPT 판정</h2></div><p class="sub">문서 간 ID·개정·해시 연결만 확인. 승인 서명·Windows 실행 미검증.</p><div class="grid">' + rendered + "</div></section>"


def render_markdown(chains, repo):
    lines = ["## GitHub 리뷰·GPT 판정 연결", "", "문서 연결은 승인 서명·운영 실행 검증이 아닙니다.", "", "| 요청 | Work | 단계 | GPT 판정 |", "|---|---|---|---|"]
    for item in chains:
        clean = lambda x: " ".join(str(x).split())[:100].replace("|", "\\|")
        lines.append(f'| [{clean(item["id"])}]({href(repo, item["paths"]["request"])}) | {clean(item["work_id"])} | {item["stage"]} | {clean(item["disposition"])} |')
        for finding in item["findings"]:
            lines.append(f'| ↳ {clean(finding["id"])} | {clean(finding["summary"])} | {clean(finding["decision"])} | - |')
    if not chains:
        lines.append("| 미이관 | - | 미확인 | - |")
    return "\n".join(lines + ["", "비차단 지적도 GPT 판정 기록 전에는 해결 처리하지 않습니다.", ""])
