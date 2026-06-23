import ipaddress
import json
import re
import socket
import time
from urllib.parse import urljoin, urlparse

import requests


def _is_public_url(url: str) -> bool:
    try:
        p = urlparse(url)
        if p.scheme not in ("http", "https"):
            return False
        host = (p.hostname or "").strip()
        if not host or host.endswith(".local") or host in ("localhost",):
            return False
        infos = socket.getaddrinfo(host, None)
        for info in infos:
            ip = ipaddress.ip_address(info[4][0])
            if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast:
                return False
        return True
    except Exception:
        return False

SITES = [
    "https://anthropic.com",
    "https://stripe.com",
    "https://linear.app",
    "https://vercel.com",
    "https://ramp.com",
    "https://mercury.com",
    "https://supabase.com",
    "https://fly.io",
    "https://planetscale.com",
    "https://resend.com",
    "https://notion.so",
    "https://figma.com",
    "https://yanivgoldenberg.com",
]

# The published "State of AI Search Visibility 2026" leaderboard: 61 sites,
# scored 2026-06-23 against the canonical rubric below. SITES_61 preserves the
# exact published rank order. CARRIED_BASELINE holds the published per-dimension
# scores so the 61-site runner can carry any row it cannot freshly re-fetch and
# clearly mark fresh vs carried. Both are derived from
# docs/state-of-ai-search-2026.json (the leaderboard's machine-readable form).
CARRIED_BASELINE = [
    {"site": "https://yanivgoldenberg.com", "technical": 20, "onpage": 15, "schema": 20, "geo": 22, "aeo": 7, "eeat": 8, "composite": 92, "notes": ["has llms.txt", "has llms-full.txt"]},
    {"site": "https://heroku.com", "technical": 20, "onpage": 15, "schema": 20, "geo": 15, "aeo": 10, "eeat": 6, "composite": 86, "notes": ["has llms.txt"]},
    {"site": "https://retool.com", "technical": 20, "onpage": 15, "schema": 20, "geo": 23, "aeo": 4, "eeat": 0, "composite": 82, "notes": ["has llms.txt"]},
    {"site": "https://amplitude.com", "technical": 20, "onpage": 15, "schema": 16, "geo": 22, "aeo": 4, "eeat": 3, "composite": 80, "notes": ["has llms.txt", "has llms-full.txt"]},
    {"site": "https://beehiiv.com", "technical": 20, "onpage": 15, "schema": 17, "geo": 17, "aeo": 10, "eeat": 0, "composite": 79, "notes": ["has llms.txt", "has llms-full.txt"]},
    {"site": "https://zapier.com", "technical": 20, "onpage": 15, "schema": 20, "geo": 24, "aeo": 0, "eeat": 0, "composite": 79, "notes": ["has llms.txt", "has llms-full.txt"]},
    {"site": "https://resend.com", "technical": 20, "onpage": 15, "schema": 17, "geo": 17, "aeo": 4, "eeat": 2, "composite": 75, "notes": ["has llms.txt", "has llms-full.txt"]},
    {"site": "https://render.com", "technical": 20, "onpage": 15, "schema": 17, "geo": 21, "aeo": 0, "eeat": 0, "composite": 73, "notes": []},
    {"site": "https://auth0.com", "technical": 20, "onpage": 15, "schema": 13, "geo": 16, "aeo": 3, "eeat": 3, "composite": 70, "notes": ["has llms.txt", "has llms-full.txt"]},
    {"site": "https://cloudflare.com", "technical": 17, "onpage": 15, "schema": 13, "geo": 25, "aeo": 0, "eeat": 0, "composite": 70, "notes": ["has llms.txt", "has llms-full.txt"]},
    {"site": "https://webflow.com", "technical": 17, "onpage": 12, "schema": 20, "geo": 15, "aeo": 3, "eeat": 3, "composite": 70, "notes": ["has llms.txt"]},
    {"site": "https://mercury.com", "technical": 20, "onpage": 15, "schema": 17, "geo": 13, "aeo": 3, "eeat": 0, "composite": 68, "notes": []},
    {"site": "https://stripe.com", "technical": 17, "onpage": 15, "schema": 17, "geo": 15, "aeo": 4, "eeat": 0, "composite": 68, "notes": ["has llms.txt"]},
    {"site": "https://supabase.com", "technical": 20, "onpage": 15, "schema": 13, "geo": 20, "aeo": 0, "eeat": 0, "composite": 68, "notes": ["has llms.txt", "has llms-full.txt"]},
    {"site": "https://figma.com", "technical": 20, "onpage": 15, "schema": 13, "geo": 19, "aeo": 0, "eeat": 0, "composite": 67, "notes": []},
    {"site": "https://railway.app", "technical": 20, "onpage": 15, "schema": 13, "geo": 15, "aeo": 4, "eeat": 0, "composite": 67, "notes": ["has llms.txt"]},
    {"site": "https://asana.com", "technical": 17, "onpage": 12, "schema": 17, "geo": 15, "aeo": 4, "eeat": 0, "composite": 65, "notes": ["has llms.txt"]},
    {"site": "https://calendly.com", "technical": 17, "onpage": 15, "schema": 13, "geo": 16, "aeo": 4, "eeat": 0, "composite": 65, "notes": ["has llms.txt"]},
    {"site": "https://clerk.com", "technical": 17, "onpage": 15, "schema": 17, "geo": 12, "aeo": 4, "eeat": 0, "composite": 65, "notes": ["has llms.txt", "has llms-full.txt"]},
    {"site": "https://monday.com", "technical": 17, "onpage": 15, "schema": 13, "geo": 20, "aeo": 0, "eeat": 0, "composite": 65, "notes": ["has llms.txt"]},
    {"site": "https://planetscale.com", "technical": 20, "onpage": 15, "schema": 13, "geo": 17, "aeo": 0, "eeat": 0, "composite": 65, "notes": ["has llms.txt"]},
    {"site": "https://runwayml.com", "technical": 20, "onpage": 15, "schema": 17, "geo": 13, "aeo": 0, "eeat": 0, "composite": 65, "notes": []},
    {"site": "https://cursor.com", "technical": 17, "onpage": 15, "schema": 13, "geo": 15, "aeo": 4, "eeat": 0, "composite": 64, "notes": ["has llms.txt"]},
    {"site": "https://mongodb.com", "technical": 17, "onpage": 15, "schema": 13, "geo": 15, "aeo": 4, "eeat": 0, "composite": 64, "notes": ["has llms.txt"]},
    {"site": "https://workos.com", "technical": 20, "onpage": 12, "schema": 12, "geo": 17, "aeo": 3, "eeat": 0, "composite": 64, "notes": ["has llms.txt", "has llms-full.txt"]},
    {"site": "https://cohere.com", "technical": 20, "onpage": 15, "schema": 17, "geo": 8, "aeo": 3, "eeat": 0, "composite": 63, "notes": ["has llms.txt"]},
    {"site": "https://sentry.io", "technical": 20, "onpage": 13, "schema": 13, "geo": 13, "aeo": 0, "eeat": 2, "composite": 61, "notes": []},
    {"site": "https://algolia.com", "technical": 17, "onpage": 15, "schema": 13, "geo": 15, "aeo": 0, "eeat": 0, "composite": 60, "notes": ["has llms.txt"]},
    {"site": "https://framer.com", "technical": 17, "onpage": 15, "schema": 13, "geo": 15, "aeo": 0, "eeat": 0, "composite": 60, "notes": ["has llms.txt"]},
    {"site": "https://gitlab.com", "technical": 17, "onpage": 15, "schema": 12, "geo": 13, "aeo": 0, "eeat": 2, "composite": 59, "notes": []},
    {"site": "https://vercel.com", "technical": 20, "onpage": 15, "schema": 16, "geo": 8, "aeo": 0, "eeat": 0, "composite": 59, "notes": ["has llms.txt"]},
    {"site": "https://hubspot.com", "technical": 17, "onpage": 12, "schema": 13, "geo": 13, "aeo": 3, "eeat": 0, "composite": 58, "notes": []},
    {"site": "https://zoom.us", "technical": 20, "onpage": 13, "schema": 12, "geo": 13, "aeo": 0, "eeat": 0, "composite": 58, "notes": []},
    {"site": "https://loom.com", "technical": 20, "onpage": 12, "schema": 8, "geo": 14, "aeo": 0, "eeat": 0, "composite": 54, "notes": []},
    {"site": "https://clickup.com", "technical": 17, "onpage": 5, "schema": 13, "geo": 16, "aeo": 0, "eeat": 0, "composite": 51, "notes": ["has llms.txt", "has llms-full.txt"]},
    {"site": "https://basecamp.com", "technical": 20, "onpage": 15, "schema": 5, "geo": 6, "aeo": 3, "eeat": 0, "composite": 49, "notes": []},
    {"site": "https://github.com", "technical": 14, "onpage": 15, "schema": 5, "geo": 8, "aeo": 4, "eeat": 0, "composite": 46, "notes": ["has llms.txt"]},
    {"site": "https://mailchimp.com", "technical": 17, "onpage": 13, "schema": 5, "geo": 8, "aeo": 3, "eeat": 0, "composite": 46, "notes": ["has llms.txt"]},
    {"site": "https://slack.com", "technical": 20, "onpage": 15, "schema": 0, "geo": 8, "aeo": 0, "eeat": 2, "composite": 45, "notes": ["has llms.txt"]},
    {"site": "https://airtable.com", "technical": 20, "onpage": 15, "schema": 0, "geo": 6, "aeo": 3, "eeat": 0, "composite": 44, "notes": []},
    {"site": "https://coda.io", "technical": 20, "onpage": 15, "schema": 0, "geo": 6, "aeo": 3, "eeat": 0, "composite": 44, "notes": []},
    {"site": "https://databricks.com", "technical": 20, "onpage": 12, "schema": 0, "geo": 9, "aeo": 3, "eeat": 0, "composite": 44, "notes": ["has llms.txt", "has llms-full.txt"]},
    {"site": "https://digitalocean.com", "technical": 20, "onpage": 15, "schema": 0, "geo": 6, "aeo": 3, "eeat": 0, "composite": 44, "notes": []},
    {"site": "https://huggingface.co", "technical": 20, "onpage": 15, "schema": 0, "geo": 6, "aeo": 3, "eeat": 0, "composite": 44, "notes": []},
    {"site": "https://linear.app", "technical": 20, "onpage": 15, "schema": 0, "geo": 8, "aeo": 0, "eeat": 0, "composite": 43, "notes": ["has llms.txt"]},
    {"site": "https://n8n.io", "technical": 17, "onpage": 15, "schema": 5, "geo": 6, "aeo": 0, "eeat": 0, "composite": 43, "notes": []},
    {"site": "https://notion.so", "technical": 20, "onpage": 12, "schema": 0, "geo": 9, "aeo": 0, "eeat": 0, "composite": 41, "notes": ["has llms.txt"]},
    {"site": "https://replicate.com", "technical": 20, "onpage": 10, "schema": 0, "geo": 8, "aeo": 3, "eeat": 0, "composite": 41, "notes": []},
    {"site": "https://snowflake.com", "technical": 20, "onpage": 15, "schema": 0, "geo": 6, "aeo": 0, "eeat": 0, "composite": 41, "notes": []},
    {"site": "https://posthog.com", "technical": 17, "onpage": 12, "schema": 0, "geo": 8, "aeo": 3, "eeat": 0, "composite": 40, "notes": ["has llms.txt"]},
    {"site": "https://anthropic.com", "technical": 20, "onpage": 12, "schema": 0, "geo": 6, "aeo": 0, "eeat": 0, "composite": 38, "notes": []},
    {"site": "https://convertkit.com", "technical": 20, "onpage": 12, "schema": 0, "geo": 6, "aeo": 0, "eeat": 0, "composite": 38, "notes": []},
    {"site": "https://mixpanel.com", "technical": 17, "onpage": 15, "schema": 0, "geo": 6, "aeo": 0, "eeat": 0, "composite": 38, "notes": []},
    {"site": "https://segment.com", "technical": 17, "onpage": 15, "schema": 0, "geo": 6, "aeo": 0, "eeat": 0, "composite": 38, "notes": []},
    {"site": "https://fly.io", "technical": 13, "onpage": 12, "schema": 0, "geo": 8, "aeo": 3, "eeat": 0, "composite": 36, "notes": ["has llms.txt"]},
    {"site": "https://netlify.com", "technical": 13, "onpage": 15, "schema": 0, "geo": 8, "aeo": 0, "eeat": 0, "composite": 36, "notes": ["has llms.txt"]},
    {"site": "https://datadog.com", "technical": 13, "onpage": 10, "schema": 0, "geo": 8, "aeo": 0, "eeat": 0, "composite": 31, "notes": ["has llms.txt"]},
    {"site": "https://ramp.com", "technical": 10, "onpage": 0, "schema": 0, "geo": 8, "aeo": 0, "eeat": 0, "composite": 18, "notes": ["has llms.txt"]},
    {"site": "https://canva.com", "technical": 7, "onpage": 0, "schema": 0, "geo": 6, "aeo": 0, "eeat": 0, "composite": 13, "notes": []},
    {"site": "https://openai.com", "technical": 7, "onpage": 0, "schema": 0, "geo": 0, "aeo": 0, "eeat": 0, "composite": 7, "notes": []},
    {"site": "https://perplexity.ai", "technical": 7, "onpage": 0, "schema": 0, "geo": 0, "aeo": 0, "eeat": 0, "composite": 7, "notes": []},
]

SITES_61 = [row["site"] for row in CARRIED_BASELINE]
BASELINE_DATE = "2026-06-23"

UA = {"User-Agent": "seo-geo-skill/1.6.0 benchmark (+https://github.com/yanivgoldenberg/seo-geo-skill)"}

def fetch(url, timeout=10, max_redirects=5):
    for _ in range(max_redirects + 1):
        if not _is_public_url(url):
            return None
        try:
            r = requests.get(url, headers=UA, timeout=timeout, allow_redirects=False)
        except Exception:
            return None
        if r.status_code in (301, 302, 303, 307, 308):
            loc = r.headers.get("location")
            if not loc:
                return r
            url = urljoin(url, loc)
            continue
        return r
    return None

PREFERRED_DEEP = ("/docs", "/blog", "/product", "/about", "/guide", "/help", "/pricing", "/features")


def discover_deep_links(base_url, html, limit=3):
    base = urlparse(base_url)
    base_host = (base.hostname or "").lower()
    home_path = (base.path or "/").rstrip("/") or "/"
    preferred: list[str] = []
    other: list[str] = []
    seen: set[str] = set()
    for href in re.findall(r'<a[^>]+href=["\']([^"\'#]+)["\']', html, re.I):
        absolute = urljoin(base_url, href.strip())
        p = urlparse(absolute)
        if p.scheme not in ("http", "https"):
            continue
        if (p.hostname or "").lower() != base_host:
            continue
        norm = absolute.split("#")[0]
        path = (p.path or "/").rstrip("/") or "/"
        if path == home_path:
            continue
        if norm in seen:
            continue
        seen.add(norm)
        low = path.lower()
        if any(low.startswith(pref) for pref in PREFERRED_DEEP):
            preferred.append(norm)
        else:
            other.append(norm)
    return (preferred + other)[:limit]


def _score_page_signals(html, all_schema_text):
    sig = {"onpage": 0, "schema": 0, "aeo": 0}

    if re.search(r'<title>[^<]{10,}</title>', html, re.I):
        sig["onpage"] += 3
    if re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'][^"\']{50,}', html, re.I):
        sig["onpage"] += 3
    if re.search(r'<meta[^>]+property=["\']og:image["\']', html, re.I):
        sig["onpage"] += 3
    if re.search(r'<meta[^>]+property=["\']og:title["\']', html, re.I):
        sig["onpage"] += 2
    if re.search(r'<meta[^>]+name=["\']twitter:card["\']', html, re.I):
        sig["onpage"] += 2
    if re.search(r'<h1[^>]*>', html, re.I):
        sig["onpage"] += 2

    if re.search(r'<script[^>]*type=["\']application/ld\+json["\']', html, re.I):
        sig["schema"] += 5
    if '"organization"' in all_schema_text:
        sig["schema"] += 5
    if '"person"' in all_schema_text:
        sig["schema"] += 4
    if 'sameas' in all_schema_text:
        sig["schema"] += 3
    if '"datemodified"' in all_schema_text:
        sig["schema"] += 3

    if '"faqpage"' in all_schema_text:
        sig["aeo"] += 4
    if '"speakable"' in all_schema_text:
        sig["aeo"] += 3
    if re.search(r'<h2[^>]*>[^<]*\?', html, re.I):
        sig["aeo"] += 3

    return sig

# Canonical scoring rubric (seo-geo v1.6.0):
#   Technical 20, On-Page 15, Schema 20, GEO 25, AEO 10, E-E-A-T 10 = 100
# Phase 0 in seo-geo.md and this script MUST use the same weights.
MAX_POINTS = {"technical": 20, "onpage": 15, "schema": 20, "geo": 25, "aeo": 10, "eeat": 10}
assert sum(MAX_POINTS.values()) == 100, "rubric must sum to 100"

# Exact crawl-observable checks this scorer awards, per bucket. This table is the
# documented contract for the automated benchmark; it mirrors docs/SCORING.md
# ("What the automated benchmark scores") and is pinned by test_scoring_parity.py.
# Each bucket's checks sum to its MAX_POINTS cap (no over-subscription).
BENCHMARK_CHECKS = {
    "technical": [("robots.txt 200", 4), ("Sitemap: directive", 3), ("canonical link", 4),
                  ("viewport meta", 3), ("HTTPS", 3), ("single H1", 3)],
    "onpage": [("title >=10 chars", 3), ("meta description >=50 chars", 3), ("og:image", 3),
               ("og:title", 2), ("twitter:card", 2), ("H1 present", 2)],
    "schema": [("any JSON-LD", 5), ("Organization", 5), ("Person", 4), ("sameAs", 3),
               ("dateModified", 3)],
    "geo": [("homepage sameAs / entity", 7), ("citation-magnet regex", 6),
            ("AI search-crawler allows min(6,n)", 6), ("llms.txt text/plain", 2),
            ("llms-full.txt text/plain", 1), ("rel=llms-txt link", 1), ("Link header", 2)],
    "aeo": [("FAQPage", 4), ("Speakable", 3), ("question-style H2", 3)],
    "eeat": [("author in schema", 3), ("date in schema", 3), ("meta author", 2),
             ("knowsAbout/hasOccupation", 2)],
}


def score(site, pages=1):
    s = {"site": site, "technical": 0, "schema": 0, "geo": 0, "onpage": 0, "aeo": 0, "eeat": 0, "notes": []}
    schemas: list[str] = []
    all_schema_text = ""

    # Technical SEO (20 pts)
    rob = fetch(urljoin(site, "/robots.txt"))
    if rob and rob.status_code == 200:
        s["technical"] += 4
        body = rob.text.lower()
        if "sitemap:" in body:
            s["technical"] += 3
    home = fetch(site)
    if home and home.status_code == 200:
        html = home.text
        if re.search(r'<link[^>]+rel=["\']canonical["\']', html, re.I):
            s["technical"] += 4
        if re.search(r'<meta[^>]+name=["\']viewport["\']', html, re.I):
            s["technical"] += 3
        if site.startswith("https://"):
            s["technical"] += 3
        if len(re.findall(r'<h1[^>]*>', html, re.I)) == 1:
            s["technical"] += 3

        schemas = re.findall(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html, re.S)
        all_schema_text = " ".join(schemas).lower() if schemas else ""

        # On-Page (15), Schema (20), AEO (10): best-of across homepage + deep pages
        best = _score_page_signals(html, all_schema_text)
        if pages > 1:
            for url in discover_deep_links(site, html, limit=min(3, pages - 1)):
                deep = fetch(url)
                if not (deep and deep.status_code == 200):
                    continue
                dschemas = re.findall(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', deep.text, re.S)
                dtext = " ".join(dschemas).lower() if dschemas else ""
                dsig = _score_page_signals(deep.text, dtext)
                for k in best:
                    best[k] = max(best[k], dsig[k])
        s["onpage"] = best["onpage"]
        s["schema"] = best["schema"]
        s["aeo"] = best["aeo"]

        # E-E-A-T (10 pts)
        if '"author"' in all_schema_text:
            s["eeat"] += 3
        if '"datemodified"' in all_schema_text or '"datepublished"' in all_schema_text:
            s["eeat"] += 3
        if re.search(r'<meta[^>]+name=["\']author["\']', html, re.I):
            s["eeat"] += 2
        if 'knowsabout' in all_schema_text or 'hasoccupation' in all_schema_text:
            s["eeat"] += 2

    # GEO (25 pts) - llms.txt down-weighted (no AI search engine consumes it as
    # of 2026); points redistributed to entity presence, citation-worthy content,
    # and AI search-crawler access. See docs/proposals/scoring-reliability.md.
    llms = fetch(urljoin(site, "/llms.txt"), timeout=10)
    if llms and llms.status_code == 200 and 'text/plain' in (llms.headers.get('content-type', '').lower()):
        s["geo"] += 2
        s["notes"].append("has llms.txt")
    llmsfull = fetch(urljoin(site, "/llms-full.txt"), timeout=10)
    if llmsfull and llmsfull.status_code == 200 and 'text/plain' in (llmsfull.headers.get('content-type', '').lower()):
        s["geo"] += 1
        s["notes"].append("has llms-full.txt")
    if rob and rob.status_code == 200:
        body = rob.text.lower()
        ai_bots = ["oai-searchbot", "perplexitybot", "chatgpt-user", "claudebot", "gptbot",
                   "bytespider", "google-extended", "amazonbot", "cohere-ai",
                   "meta-externalagent", "duckassistbot", "facebookbot", "applebot-extended", "ccbot"]
        explicit_allows = sum(1 for b in ai_bots
                              if re.search(rf'user-agent:\s*{re.escape(b)}\b[\s\S]{{0,300}}?allow:\s*/', body, re.I))
        s["geo"] += min(6, explicit_allows)
    if home and home.status_code == 200:
        html_lower = home.text.lower()
        if 'sameas' in all_schema_text:
            s["geo"] += 7
        # generic citation magnets heuristic
        if re.search(r'\$\d+[km]?\b|\d+%|\d+x\b|\d+\+\s+(?:clients|users|customers)', html_lower):
            s["geo"] += 6
        if re.search(r'rel=["\'](?:llms-txt|describedby)["\'][^>]+href=["\'][^"\']*llms\.txt', home.text, re.I):
            s["geo"] += 1
        if 'llms.txt' in (home.headers.get('link', '') or '').lower():
            s["geo"] += 2

    # Clamp each dimension to its max
    for k, cap in MAX_POINTS.items():
        s[k] = min(s[k], cap)
    s["composite"] = sum(s[k] for k in MAX_POINTS)
    return s

def main():
    results = []
    for url in SITES:
        print(f"scoring {url}...")
        r = score(url, pages=4)
        results.append(r)
        time.sleep(0.5)

    # sort desc
    results.sort(key=lambda x: -x["composite"])
    with open('/tmp/benchmarks.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("\n=== LEADERBOARD ===")
    print(f"{'Rank':<5} {'Site':<30} {'Tech':>4} {'Sch':>4} {'GEO':>4} {'OnP':>4} {'AEO':>4} {'EEAT':>5} {'TOTAL':>6}")
    for i, r in enumerate(results, 1):
        name = r['site'].replace('https://', '').replace('www.', '')
        print(f"{i:<5} {name:<30} {r['technical']:>4} {r['schema']:>4} {r['geo']:>4} {r['onpage']:>4} {r['aeo']:>4} {r['eeat']:>5} {r['composite']:>6}")
    return results


if __name__ == "__main__":
    main()
