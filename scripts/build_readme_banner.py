# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Copyright (c) Yaniv Goldenberg - https://yanivgoldenberg.com (see NOTICE)
"""Build the README hero banners (dark + light SVG) and the 1280x640 social preview PNG.

The score card shows a real `scripts/benchmark_demo.py` run; pass the six
dimension scores and the run date explicitly so the image never drifts from a
measurement. The PNG export needs Playwright with a local Chrome.

    py -3.12 scripts/build_readme_banner.py --scores 20,15,20,22,7,8 --date 2026-10-23
"""
import argparse
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "assets"

DIMS = [("Technical", 20), ("On-Page", 15), ("Schema", 20), ("GEO", 25), ("AEO", 10), ("E-E-A-T", 10)]
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"

THEMES = {
    "dark": {"bg": "#000000", "grid": "#FFFFFF", "grid_o": "0.045", "ink": "#FFFFFF", "body": "#C5C5C5",
             "muted": "#8A8A8A", "accent": "#00F7D2", "panel": "#07090A", "line": "#1E2326",
             "track": "#15191B", "glow_o": "0.16"},
    "light": {"bg": "#FFFFFF", "grid": "#0B1F1C", "grid_o": "0.05", "ink": "#0A0F0E", "body": "#2F3A38",
              "muted": "#5E6B69", "accent": "#00866F", "panel": "#F6FAF9", "line": "#D8E3E1",
              "track": "#E3ECEA", "glow_o": "0.10"},
}


def _card(t: dict, x: int, y: int, scores: list[int], date: str) -> str:
    total = sum(scores)
    rows = []
    for i, ((name, cap), val) in enumerate(zip(DIMS, scores)):
        ry = y + 118 + i * 30
        w = round(220 * val / cap)
        rows.append(
            f'<text x="{x + 28}" y="{ry + 9}" font-family="{MONO}" font-size="14" fill="{t["body"]}">{name}</text>'
            f'<rect x="{x + 142}" y="{ry}" width="220" height="10" rx="5" fill="{t["track"]}"/>'
            f'<rect x="{x + 142}" y="{ry}" width="{w}" height="10" rx="5" fill="{t["accent"]}"/>'
            f'<text x="{x + 432}" y="{ry + 10}" text-anchor="end" font-family="{MONO}" font-size="14" '
            f'fill="{t["muted"]}">{val}/{cap}</text>'
        )
    return (
        f'<rect x="{x}" y="{y}" width="460" height="330" rx="16" fill="{t["panel"]}" stroke="{t["line"]}"/>'
        f'<circle cx="{x + 24}" cy="{y + 22}" r="5" fill="{t["line"]}"/>'
        f'<circle cx="{x + 42}" cy="{y + 22}" r="5" fill="{t["line"]}"/>'
        f'<circle cx="{x + 60}" cy="{y + 22}" r="5" fill="{t["line"]}"/>'
        f'<line x1="{x}" y1="{y + 44}" x2="{x + 460}" y2="{y + 44}" stroke="{t["line"]}"/>'
        f'<text x="{x + 28}" y="{y + 76}" font-family="{MONO}" font-size="15" fill="{t["accent"]}">$ python scripts/benchmark_demo.py</text>'
        f'<text x="{x + 28}" y="{y + 100}" font-family="{MONO}" font-size="13" fill="{t["muted"]}">yanivgoldenberg.com  ·  real run {date}</text>'
        + "".join(rows)
        + f'<text x="{x + 28}" y="{y + 312}" font-family="{SANS}" font-size="15" font-weight="600" fill="{t["muted"]}">AI SEARCH READINESS</text>'
        f'<text x="{x + 432}" y="{y + 314}" text-anchor="end" font-family="{SANS}" font-size="38" font-weight="800" '
        f'fill="{t["accent"]}">{total}<tspan font-size="18" font-weight="500" fill="{t["muted"]}">/100</tspan></text>'
    )


def _left(t: dict, x: int, y: int, scale: float = 1.0) -> str:
    s = scale
    return (
        f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="{round(18 * s)}" fill="{t["muted"]}">yanivgoldenberg / '
        f'<tspan fill="{t["ink"]}">seo-geo-skill</tspan></text>'
        f'<text x="{x}" y="{y + round(70 * s)}" font-family="{SANS}" font-size="{round(54 * s)}" font-weight="800" '
        f'letter-spacing="-1.5" fill="{t["ink"]}">SEO + GEO audits</text>'
        f'<text x="{x}" y="{y + round(132 * s)}" font-family="{SANS}" font-size="{round(54 * s)}" font-weight="800" '
        f'letter-spacing="-1.5" fill="{t["ink"]}">for the <tspan fill="{t["accent"]}">AI search</tspan> era.</text>'
        f'<text x="{x}" y="{y + round(182 * s)}" font-family="{SANS}" font-size="{round(20 * s)}" fill="{t["body"]}">'
        "A Claude agent skill: 100-point readiness score, schema, llms.txt,</text>"
        f'<text x="{x}" y="{y + round(210 * s)}" font-family="{SANS}" font-size="{round(20 * s)}" fill="{t["body"]}">'
        "robots.txt and E-E-A-T. Audit-only by default.</text>"
        f'<text x="{x}" y="{y + round(258 * s)}" font-family="{MONO}" font-size="{round(15 * s)}" fill="{t["muted"]}">'
        "61-site benchmark  ·  reproducible scorer  ·  no telemetry</text>"
    )


def svg(theme: str, w: int, h: int, scores: list[int], date: str) -> str:
    t = THEMES[theme]
    tall = h > 500
    card_y = (h - 330) // 2
    left_y = 150 if tall else 92
    scale = 1.08 if tall else 1.0
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
        f'aria-labelledby="title"><title id="title">seo-geo-skill: SEO + GEO audits for the AI search era. '
        f'Real run {date}: yanivgoldenberg.com scores {sum(scores)}/100.</title>'
        f'<defs><pattern id="g" width="48" height="48" patternUnits="userSpaceOnUse"><path d="M48 0H0V48" fill="none" '
        f'stroke="{t["grid"]}" stroke-opacity="{t["grid_o"]}"/></pattern>'
        f'<radialGradient id="glow" cx="72%" cy="50%" r="45%"><stop offset="0" stop-color="{t["accent"]}" '
        f'stop-opacity="{t["glow_o"]}"/><stop offset="1" stop-color="{t["accent"]}" stop-opacity="0"/></radialGradient>'
        f'<linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="{t["bg"]}" stop-opacity="0"/>'
        f'<stop offset="1" stop-color="{t["bg"]}" stop-opacity="0.85"/></linearGradient></defs>'
        f'<rect width="{w}" height="{h}" fill="{t["bg"]}"/><rect width="{w}" height="{h}" fill="url(#g)"/>'
        f'<rect width="{w}" height="{h}" fill="url(#fade)"/><rect width="{w}" height="{h}" fill="url(#glow)"/>'
        f'<rect width="{w}" height="4" fill="{t["accent"]}"/>'
        + _left(t, 64, left_y, scale)
        + _card(t, w - 460 - 64, card_y, scores, date)
        + "</svg>\n"
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scores", required=True, help="technical,onpage,schema,geo,aeo,eeat from a real run")
    ap.add_argument("--date", required=True, help="date of that run, YYYY-MM-DD")
    ap.add_argument("--no-png", action="store_true")
    a = ap.parse_args()
    scores = [int(v) for v in a.scores.split(",")]
    if len(scores) != 6 or any(not 0 <= v <= cap for v, (_, cap) in zip(scores, DIMS)):
        raise SystemExit("--scores needs six values within the rubric caps")
    OUT.mkdir(exist_ok=True)
    for theme in THEMES:
        (OUT / f"banner-{theme}.svg").write_text(svg(theme, 1280, 400, scores, a.date), encoding="utf-8")
    social = OUT / "social-preview.svg"
    social.write_text(svg("dark", 1280, 640, scores, a.date), encoding="utf-8")
    if a.no_png:
        return
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome")
        page = browser.new_page(viewport={"width": 1280, "height": 640})
        page.goto(social.resolve().as_uri())
        page.screenshot(path=str(OUT / "social-preview.png"))
        browser.close()
    social.unlink()


if __name__ == "__main__":
    main()
