import json
import os
import sys
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / "docs" / "assets" / "src"
OUT = REPO / "docs" / "assets"

BANNERS = [
    ("cover.html", "seo-geo-cover-v4.png", 1600, 900),
    ("og.html", "seo-geo-og-1200x630.png", 1200, 630),
    ("github-social.html", "seo-geo-github-1280x640.png", 1280, 640),
]


def render(html: str, out_path: Path, width: int, height: int) -> None:
    burl = os.environ["BROWSERLESS_URL"].rstrip("/")
    token = os.environ["BROWSERLESS_TOKEN"]
    body = {
        "html": html,
        "options": {"type": "png", "clip": {"x": 0, "y": 0, "width": width, "height": height}},
        "viewport": {"width": width, "height": height, "deviceScaleFactor": 1},
        "gotoOptions": {"waitUntil": "networkidle0"},
    }
    req = urllib.request.Request(
        f"{burl}/screenshot?token={token}",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    out_path.write_bytes(urllib.request.urlopen(req, timeout=90).read())


def main() -> int:
    if "BROWSERLESS_URL" not in os.environ or "BROWSERLESS_TOKEN" not in os.environ:
        print("Set BROWSERLESS_URL and BROWSERLESS_TOKEN to render banners.", file=sys.stderr)
        return 1
    for src_name, out_name, width, height in BANNERS:
        html = (SRC / src_name).read_text(encoding="utf-8")
        render(html, OUT / out_name, width, height)
        print(f"ok {out_name} ({width}x{height})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
