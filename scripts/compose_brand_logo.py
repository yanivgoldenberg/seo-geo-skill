"""Composite the Yaniv brand mark onto a folder of generated slide PNGs.

Usage:
    python3 scripts/compose_brand_logo.py /path/to/raw/folder

Reads every *.png in the folder, composites yg-mark-1024.png at 36px in the
bottom-right corner with a 40px inset, writes <name>_branded.png alongside.

Pre-condition: each input slide must already leave the bottom-right
96x96px transparent reservation zone empty (per the prompt instructions in
the Brand-Locked Visual Pack docs).

Source of truth for the mark:
    https://yanivgoldenberg.com/wp-content/uploads/2026/04/yg-mark-1024.png
The script downloads it once on first run and caches it locally.
"""

from __future__ import annotations

import argparse
import logging
import sys
import urllib.request
from pathlib import Path

from PIL import Image

LOGO_URL = "https://yanivgoldenberg.com/wp-content/uploads/2026/04/yg-mark-1024.png"
LOGO_CACHE = Path.home() / ".cache" / "yaniv-brand" / "yg-mark-1024.png"
LOGO_TARGET_WIDTH_PX = 36
INSET_PX = 40

logger = logging.getLogger(__name__)


def fetch_logo() -> Path:
    if LOGO_CACHE.exists():
        return LOGO_CACHE
    LOGO_CACHE.parent.mkdir(parents=True, exist_ok=True)
    logger.info("Fetching canonical mark from %s", LOGO_URL)
    req = urllib.request.Request(LOGO_URL, headers={"User-Agent": "Mozilla/5.0 yaniv-brand"})
    with urllib.request.urlopen(req, timeout=20) as r:
        LOGO_CACHE.write_bytes(r.read())
    return LOGO_CACHE


def stamp_logo(slide_path: Path, logo: Image.Image) -> Path:
    out_path = slide_path.with_name(f"{slide_path.stem}_branded.png")
    base = Image.open(slide_path).convert("RGBA")
    bw, bh = base.size

    target_w = LOGO_TARGET_WIDTH_PX
    aspect = logo.size[1] / logo.size[0]
    target_h = round(target_w * aspect)
    mark = logo.resize((target_w, target_h), Image.LANCZOS)

    x = bw - target_w - INSET_PX
    y = bh - target_h - INSET_PX
    base.alpha_composite(mark, dest=(x, y))
    base.convert("RGB").save(out_path, format="PNG", optimize=True)
    return out_path


def main(folder: str) -> int:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    src = Path(folder).expanduser().resolve()
    if not src.is_dir():
        logger.error("Not a directory: %s", src)
        return 2

    logo_path = fetch_logo()
    logo = Image.open(logo_path).convert("RGBA")

    pngs = sorted(p for p in src.glob("*.png") if not p.stem.endswith("_branded"))
    if not pngs:
        logger.error("No PNGs found in %s", src)
        return 1

    for p in pngs:
        try:
            out = stamp_logo(p, logo)
            logger.info("  branded: %s", out.name)
        except Exception as exc:  # noqa: BLE001
            logger.error("  failed on %s: %s", p.name, exc)
    logger.info("Done. %d slides processed.", len(pngs))
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="Directory of raw ChatGPT-generated slide PNGs")
    args = parser.parse_args()
    sys.exit(main(args.folder))
