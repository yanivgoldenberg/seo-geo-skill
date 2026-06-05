import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parent.parent
ASSETS = REPO / "docs" / "assets"
OUT = ASSETS / "benchmark-terminal.png"
COMMAND = "python scripts/benchmark_demo.py"

FONTS = Path("/config/workspace/claude-code-templates/cli-tool/components/skills/creative-design/canvas-design/canvas-fonts")
BRAND = Path("/config/workspace/docs/reference/brand/fonts")

CANVAS = (6, 7, 8)
CARD = (13, 15, 17)
BAR = (18, 21, 24)
BORDER = (29, 31, 33)
INK = (228, 231, 234)
MUTED = (150, 154, 156)
CYAN = (0, 247, 210)
GREEN = (38, 194, 129)
DOT_R = (255, 95, 86)
DOT_Y = (255, 189, 46)
DOT_G = (39, 201, 63)

FontT = ImageFont.FreeTypeFont | ImageFont.ImageFont


def mono(size: int, bold: bool = False) -> FontT:
    candidates = [
        FONTS / f"JetBrainsMono-{'Bold' if bold else 'Regular'}.ttf",
        FONTS / f"IBMPlexMono-{'Bold' if bold else 'Regular'}.ttf",
    ]
    for c in candidates:
        if c.exists():
            return ImageFont.truetype(str(c), size)
    return ImageFont.load_default()


def sans(size: int, bold: bool = False) -> FontT:
    candidates = [BRAND / f"Inter-{'Bold' if bold else 'Regular'}.ttf"]
    for c in candidates:
        if c.exists():
            return ImageFont.truetype(str(c), size)
    return ImageFont.load_default()


def capture() -> list[str]:
    out = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "benchmark_demo.py")],
        capture_output=True,
        text=True,
        check=True,
        cwd=str(REPO),
    )
    return out.stdout.rstrip("\n").split("\n")


def main() -> None:
    lines = capture()

    W = 1600
    MARGIN = 56
    CARD_X0, CARD_X1 = MARGIN, W - MARGIN
    BAR_H = 64
    PAD_X = 48
    PAD_TOP = 36
    LINE_H = 46
    BODY_F = mono(28)
    BOLD_F = mono(28, True)

    prompt_block = 2
    body_rows = len(lines)
    content_h = (prompt_block + body_rows) * LINE_H
    card_top = MARGIN
    card_h = BAR_H + PAD_TOP + content_h + PAD_TOP
    H = card_top + card_h + MARGIN

    im = Image.new("RGB", (W, H), CANVAS)
    d = ImageDraw.Draw(im)

    d.rounded_rectangle([CARD_X0, card_top, CARD_X1, card_top + card_h], radius=16, fill=CARD, outline=BORDER, width=1)
    d.rounded_rectangle([CARD_X0, card_top, CARD_X1, card_top + BAR_H], radius=16, fill=BAR)
    d.rectangle([CARD_X0, card_top + BAR_H - 16, CARD_X1, card_top + BAR_H], fill=BAR)
    d.line([CARD_X0, card_top + BAR_H, CARD_X1, card_top + BAR_H], fill=BORDER, width=1)

    cy = card_top + BAR_H // 2
    for i, col in enumerate((DOT_R, DOT_Y, DOT_G)):
        dx = CARD_X0 + 30 + i * 30
        d.ellipse([dx, cy - 9, dx + 18, cy + 9], fill=col)
    title = "seo-geo-skill  -  AI Search Readiness benchmark"
    tf = sans(24)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, cy - 14), title, font=tf, fill=MUTED)

    x = CARD_X0 + PAD_X
    y = card_top + BAR_H + PAD_TOP

    d.text((x, y), "$ ", font=BOLD_F, fill=CYAN)
    cmd_x = x + d.textlength("$ ", font=BOLD_F)
    d.text((cmd_x, y), COMMAND, font=BODY_F, fill=INK)
    y += LINE_H
    y += LINE_H

    for line in lines:
        if line.startswith("-"):
            ymid = y + LINE_H // 2
            d.line([x, ymid, CARD_X1 - PAD_X, ymid], fill=BORDER, width=1)
            y += LINE_H
            continue
        is_data = "yanivgoldenberg.com" in line or "openai.com" in line
        is_total = line.lstrip().startswith("max points") or line.startswith("Site")
        if is_data:
            total = line[-7:].strip()
            head = line[: len(line) - 7]
            d.text((x, y), head, font=BODY_F, fill=INK)
            hx = x + d.textlength(head, font=BODY_F)
            score_col = GREEN if int(total) >= 90 else CYAN if int(total) >= 60 else MUTED
            d.text((hx, y), f"{total:>7}", font=BOLD_F, fill=score_col)
        elif is_total:
            d.text((x, y), line, font=BOLD_F, fill=MUTED)
        else:
            d.text((x, y), line, font=BODY_F, fill=INK)
        y += LINE_H

    im.save(OUT)
    print("wrote", OUT, im.size)


if __name__ == "__main__":
    main()
