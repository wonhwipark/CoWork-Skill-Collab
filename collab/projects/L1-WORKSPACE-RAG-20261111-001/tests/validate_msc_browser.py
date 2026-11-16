"""Headless Chrome smoke for actual doc-converter B HTML produced from review ZIP."""
import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile

REPO = Path(__file__).resolve().parents[4]
ZIP = REPO / "collab/projects/L1-WORKSPACE-RAG-20261111-001/candidates/doc-converter_v0_2_23_1116.zip"
chrome = next((shutil.which(x) for x in ("google-chrome", "chromium", "chromium-browser") if shutil.which(x)), None)
if not chrome:
    print("BROWSER_CHECK_NOT_RUN: no Chromium/Google Chrome on runner", flush=True)
    raise SystemExit(2)
with tempfile.TemporaryDirectory(prefix="msc-browser-") as td:
    temp = Path(td)
    with zipfile.ZipFile(ZIP) as zf:
        zf.extract("doc-converter/scripts/msc_b_viewer.py", temp)
    source = temp / "doc-converter/scripts/msc_b_viewer.py"
    spec = importlib.util.spec_from_file_location("msc_b_viewer_qa", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    image = temp / "source.svg"
    image.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 280">'
                     '<rect x="10" y="10" width="680" height="255" fill="#ffffff"/>'
                     '<text x="40" y="90" font-size="30">INIT</text>'
                     '<text x="40" y="190" font-size="25">synthetic MSC</text></svg>', encoding="utf-8")
    page = temp / "viewer.html"
    page.write_text(module.build_html(image, "Synthetic MSC Viewer", ["INIT"]), encoding="utf-8")
    assert "data:image/svg+xml;base64," in page.read_text(encoding="utf-8")
    png = temp / "viewer.png"
    result = subprocess.run([
        chrome, "--headless", "--disable-gpu", "--disable-dev-shm-usage",
        "--no-sandbox", "--hide-scrollbars", "--window-size=1280,900",
        "--virtual-time-budget=1500", "--screenshot=" + str(png), page.as_uri(),
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=40)
    assert result.returncode == 0, (result.returncode, result.stderr[-1100:])
    assert png.is_file() and png.read_bytes().startswith(b"\x89PNG\r\n\x1a\n") and png.stat().st_size > 12000, str(png.stat().st_size if png.exists() else "missing")
    print("BROWSER_CHROMIUM_SMOKE_PASS: standalone B HTML screenshot PNG " + str(png.stat().st_size) + " bytes", flush=True)
    print("BROWSER_LIMIT: phase-click behavior, production CSP and real host URL NOT_RUN", flush=True)
