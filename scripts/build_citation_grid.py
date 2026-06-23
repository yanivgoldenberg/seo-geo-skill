from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ASSETS = Path(__file__).resolve().parent.parent / "docs" / "assets"
OUT = ASSETS / "citation-grid.png"

CELLS = [
    ("ChatGPT", "crop-chatgpt.png",
     "Cited first for \"best fractional CMO Israel\": scaled Elementor, Riverside.fm, cnvrg.io"),
    ("Perplexity", "crop-perplexity.png",
     "Names Yaniv Goldenberg as the operator-first fractional CMO pick for B2B SaaS"),
    ("Google AI Overview", "crop-google-ai-overview.png",
     "Top-cited expert: ties marketing to revenue, $200K to $20M ARR at Elementor"),
    ("Microsoft Copilot", "crop-copilot.png",
     "Leads the shortlist: best-for aggressive, revenue-owned growth"),
]

W, PAD, GAP = 1600, 40, 24
CELL_W = (W - 2 * PAD - GAP) // 2
IMG_H, LABEL_H, CAP_H = 540, 44, 64
CELL_H = LABEL_H + IMG_H + CAP_H + 28
HEADER = 116
H = HEADER + 2 * CELL_H + GAP + PAD

CANVAS = (6, 7, 8)
CARD = (13, 15, 17)
BORDER = (29, 31, 33)
INK = (255, 255, 255)
MUTED = (150, 154, 156)
CYAN = (0, 247, 210)

FontT = ImageFont.FreeTypeFont | ImageFont.ImageFont


def font(size: int, bold: bool = False) -> FontT:
    candidates = [
        f"/usr/share/fonts/truetype/dejavu/DejaVuSans{'-Bold' if bold else ''}.ttf",
        f"/config/.fonts/Inter-{'Bold' if bold else 'Regular'}.ttf",
    ]
    for c in candidates:
        if Path(c).exists():
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()


def wrap(d: ImageDraw.ImageDraw, text: str, f: FontT, max_w: int) -> list[str]:
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=f) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


im = Image.new("RGB", (W, H), CANVAS)
d = ImageDraw.Draw(im)

d.rectangle([PAD, PAD, W - PAD, PAD + 3], fill=CYAN)
d.text((PAD, PAD + 18), "AI Engine Citation Grid", font=font(34, True), fill=INK)
d.text((PAD, PAD + 62),
       "What four AI engines answer for \"best fractional CMO in Israel.\" One name, four receipts.",
       font=font(19), fill=MUTED)

for i, (label, fname, caption) in enumerate(CELLS):
    cx = PAD + (i % 2) * (CELL_W + GAP)
    cy = HEADER + (i // 2) * (CELL_H + GAP)
    d.rounded_rectangle([cx, cy, cx + CELL_W, cy + CELL_H], radius=14, fill=CARD, outline=BORDER, width=1)
    d.text((cx + 22, cy + 14), label, font=font(21, True), fill=INK)

    shot = Image.open(ASSETS / fname)
    shot.thumbnail((CELL_W - 44, IMG_H), Image.Resampling.LANCZOS)
    px = cx + (CELL_W - shot.width) // 2
    im.paste(shot, (px, cy + LABEL_H + 6))

    cap_f = font(18)
    ly = cy + LABEL_H + IMG_H + 18
    for line in wrap(d, caption, cap_f, CELL_W - 44)[:2]:
        d.text((cx + 22, ly), line, font=cap_f, fill=CYAN)
        ly += 26

im.save(OUT)
print("wrote", OUT, im.size)
