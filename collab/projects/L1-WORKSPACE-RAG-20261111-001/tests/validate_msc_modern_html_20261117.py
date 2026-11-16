"""Isolated release QA. Only public skill code and synthetic MSC input are used."""
from __future__ import annotations

import argparse
import base64
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys
import tempfile
import unicodedata
import zipfile


VERSION = "0.2.26"
FILENAME = "doc-converter_v0_2_26_1117.zip"


def safety(archive: Path, target: Path) -> Path:
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        seen = set()
        assert sum(x.file_size for x in z.infolist()) < 12 * 1024 * 1024
        for item in z.infolist():
            p = PurePosixPath(item.filename)
            assert not p.is_absolute() and ".." not in p.parts and p.parts[0] == "doc-converter"
            assert "\\" not in item.filename
            key = unicodedata.normalize("NFC", item.filename).casefold()
            assert key not in seen
            seen.add(key)
            assert not stat.S_ISLNK(item.external_attr >> 16)
            assert not item.filename.endswith((".zip", ".tar", ".gz", ".pem", ".key"))
            out = target.joinpath(*p.parts)
            if item.is_dir():
                out.mkdir(parents=True, exist_ok=True)
                continue
            out.parent.mkdir(parents=True, exist_ok=True)
            data = z.read(item)
            assert b"-----BEGIN PRIVATE KEY-----" not in data
            assert b"-----BEGIN OPENSSH PRIVATE KEY-----" not in data
            out.write_bytes(data)
            mode = (item.external_attr >> 16) & 0o777
            out.chmod(mode or 0o644)
    root = target / "doc-converter"
    entries = {}
    for line in (root / "PACKAGE_CONTENTS.sha256").read_text().splitlines():
        digest, name = line.split("  ", 1)
        assert name not in entries
        entries[name] = digest
        assert hashlib.sha256((root / name).read_bytes()).hexdigest() == digest, name
    actual = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file() and p.name != "PACKAGE_CONTENTS.sha256"}
    assert actual == set(entries)
    assert (root / "VERSION").read_text().strip() == VERSION
    for name in ["skillsilent/contract.json", "skillsilent/manifest.json"]:
        assert json.loads((root / name).read_text())["skill_version"] == VERSION
    return root


def fixture() -> dict:
    ids = ["Controller", "Resource", "TxMngr", "HAL", "RF", "PHY"]
    steps = []
    for phase in ["INIT", "CHANGE", "FINISH"]:
        steps.append({"type": "divider", "label": phase})
        for n in range(12):
            i = len([s for s in steps if s.get("type") == "message"]) + 1
            steps.append({"type": "message", "id": "S" + str(i), "from": ids[n % 6], "to": ids[(n + 1) % 6],
                          "label": "SYNTHETIC_REQ_" + str(i), "evidence_status": "CODE_CONFIRMED"})
    return {"schema": "doc-converter/msc-package/v1", "issue_id": "SYNTHETIC_UI_QA_ONLY",
            "view_mode": "PROCEDURE_FEATURE", "diagrams": [{"name": "synthetic", "spec": {
                "schema": "doc-converter/msc-spec/v1", "kind": "AS_IS", "title": "MSC 모던 양식 · 가상 흐름",
                "participants": [{"id": p, "label": p} for p in ids], "steps": steps,
                "source_provenance": {"revision": "SYNTHETIC-r1"},
                "explanation": "화면과 변환 기능을 확인하는 가상 MSC예요. 실제 코드·제품 동작을 검증한 자료는 아니에요."}}]}


def real_cli(root: Path, output: Path) -> Path:
    source = output / "input.json"
    source.write_text(json.dumps(fixture(), ensure_ascii=False), encoding="utf-8")
    env = os.environ.copy()
    env.pop("PLANTUML_CMD", None)
    env.pop("PLANTUML_JAR", None)
    proc = subprocess.run(["sh", str(root / "doc-converter"), "msc-package", "--", "--input", str(source),
                           "--output-dir", str(output / "msc"), "--view-mode", "PROCEDURE_FEATURE", "--json"],
                          env=env, text=True, capture_output=True, timeout=90)
    print("REAL_CLI_RETURN", proc.returncode, proc.stdout[-3000:], proc.stderr[-1000:])
    assert proc.returncode == 0
    manifest = json.loads((output / "msc/MSC_MANIFEST.json").read_text())
    row = manifest["diagrams"][0]
    assert row["status"] == "READY"
    assert row["html_phase_buttons"] == {"requested": 3, "enabled": 3, "disabled": []}
    html = output / "msc/synthetic.html"
    assert hashlib.sha256(html.read_bytes()).hexdigest() == row["html_sha256"]
    return html


def browser_check(html: Path, screenshot_dir: Path) -> list:
    from playwright.sync_api import sync_playwright
    result = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for width, height in [(1440, 1000), (390, 844), (320, 800)]:
            page = browser.new_page(viewport={"width": width, "height": height}, reduced_motion="reduce")
            errors, external = [], []
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
            page.on("request", lambda r: external.append(r.url) if r.url.startswith(("http:", "https:")) else None)
            page.goto(html.as_uri())
            page.wait_for_function("document.getElementById('msc').complete && document.getElementById('msc').naturalWidth > 0")
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            assert page.locator(".meta>div").count() == 4
            assert page.locator(".stage-note").count() == 3
            assert page.locator(".meta").inner_text().count("36개") == 1
            assert page.locator(".top").evaluate("e=>getComputedStyle(e).backgroundColor") == "rgb(20, 45, 74)"
            assert page.locator("#pct").inner_text() == "100%"
            page.locator("#plus").click()
            assert page.locator("#pct").inner_text() == "120%"
            page.locator("#minus").click()
            assert page.locator("#pct").inner_text() == "100%"
            page.locator('[data-zoom="fit"]').click()
            fit = page.evaluate("({image:document.getElementById('msc').getBoundingClientRect().width,pane:document.getElementById('pane').clientWidth})")
            assert abs(fit["image"] - fit["pane"]) <= 2
            page.locator('[data-zoom="reset"]').click()
            page.select_option("#stage", "2")
            assert page.locator('.stage-note[aria-current="step"]').inner_text().startswith("03")
            assert page.locator("#pane").evaluate("e=>e.scrollTop") > 0
            page.locator("#plus").click()
            assert "FINISH" in page.locator("#viewstate").inner_text()
            page.locator('button.phase[data-phase-index="0"]').click()
            assert page.locator("#stage").input_value() == "0"
            page.locator('[data-zoom="reset"]').click()
            page.locator("#pane").evaluate("e=>e.scrollTop=0")
            screenshot = screenshot_dir / ("modern_" + str(width) + ".png")
            page.screenshot(path=str(screenshot), full_page=False)
            assert not errors and not external, (errors, external)
            result.append({"width": width, "height": height, "overflow": False, "image_loaded": True,
                           "zoom_fit_reset_phase": "PASS", "js_csp_errors": errors, "external_requests": external,
                           "png_sha256": hashlib.sha256(screenshot.read_bytes()).hexdigest()})
            if width in (1440, 390):
                print("MODERN_PNG", str(width), base64.b64encode(screenshot.read_bytes()).decode(), flush=True)
            page.close()
        browser.close()
    return result


def finalize(root: Path, target: Path) -> tuple[Path, dict]:
    release_file = root / ".skill-release.json"
    release = json.loads(release_file.read_text())
    release.update(channel="public", release_kind="approved_final_zip")
    release_file.write_text(json.dumps(release, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for cache in root.rglob("__pycache__"):
        import shutil
        shutil.rmtree(cache)
    import shutil
    shutil.rmtree(root / ".pytest_cache", ignore_errors=True)
    files = sorted(p for p in root.rglob("*") if p.is_file() and p.name != "PACKAGE_CONTENTS.sha256")
    index = "".join(hashlib.sha256(p.read_bytes()).hexdigest() + "  " + p.relative_to(root).as_posix() + "\n" for p in files)
    (root / "PACKAGE_CONTENTS.sha256").write_text(index, encoding="utf-8")
    archive = target / FILENAME
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in sorted(p for p in root.rglob("*") if p.is_file()):
            item = zipfile.ZipInfo("doc-converter/" + p.relative_to(root).as_posix(), date_time=(2026, 11, 17, 0, 0, 0))
            item.create_system = 3
            mode = 0o755 if p.name == "doc-converter" else 0o644
            item.external_attr = (stat.S_IFREG | mode) << 16
            item.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(item, p.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    safety(archive, target / "final-roundtrip")
    data = archive.read_bytes()
    return archive, {"filename": FILENAME, "size": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    parser.add_argument("--sha256", required=True)
    parser.add_argument("--browser", action="store_true")
    parser.add_argument("--finalize-only", action="store_true")
    args = parser.parse_args()
    assert hashlib.sha256(args.archive.read_bytes()).hexdigest() == args.sha256
    with tempfile.TemporaryDirectory(prefix="msc-modern-qa-") as temp:
        base = Path(temp)
        root = safety(args.archive, base / "unpacked")
        if args.finalize_only:
            final, report = finalize(root, base)
            print("MODERN_FINAL_JSON", json.dumps(report), flush=True)
            print("MODERN_FINAL_B64", base64.b64encode(final.read_bytes()).decode(), flush=True)
            return
        subprocess.run([sys.executable, "-m", "pytest", "-q"], cwd=root, check=True)
        output = base / "runtime"
        output.mkdir()
        html = real_cli(root, output)
        browser_result = browser_check(html, base) if args.browser else "NOT_RUN_THIS_MATRIX_JOB"
        print("MODERN_QA_JSON", json.dumps({"python": sys.version, "full_pytest": "PASS", "real_plantuml_gateway": "PASS", "browser": browser_result}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
