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

UA = {"User-Agent": "seo-geo-skill/1.6.0 benchmark (+https://github.com/yanivgoldenberg/seo-geo-skill)"}

def fetch(url, timeout=10):
    if not _is_public_url(url):
        return None
    try:
        r = requests.get(url, headers=UA, timeout=timeout, allow_redirects=True)
        return r
    except Exception:
        return None

# Canonical scoring rubric (seo-geo v1.6.0):
#   Technical 20, On-Page 15, Schema 20, GEO 25, AEO 10, E-E-A-T 10 = 100
# Phase 0 in seo-geo.md and this script MUST use the same weights.
MAX_POINTS = {"technical": 20, "onpage": 15, "schema": 20, "geo": 25, "aeo": 10, "eeat": 10}
assert sum(MAX_POINTS.values()) == 100, "rubric must sum to 100"


def score(site):
    s = {"site": site, "technical": 0, "schema": 0, "geo": 0, "onpage": 0, "aeo": 0, "eeat": 0, "notes": []}

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

        # Schema (20 pts)
        schemas = re.findall(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html, re.S)
        all_schema_text = " ".join(schemas).lower() if schemas else ""
        if schemas:
            s["schema"] += 5
        if '"organization"' in all_schema_text:
            s["schema"] += 5
        if '"person"' in all_schema_text:
            s["schema"] += 4
        if 'sameas' in all_schema_text:
            s["schema"] += 3
        if '"datemodified"' in all_schema_text:
            s["schema"] += 3

        # On-Page (15 pts)
        if re.search(r'<title>[^<]{10,}</title>', html, re.I):
            s["onpage"] += 3
        if re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'][^"\']{50,}', html, re.I):
            s["onpage"] += 3
        if re.search(r'<meta[^>]+property=["\']og:image["\']', html, re.I):
            s["onpage"] += 3
        if re.search(r'<meta[^>]+property=["\']og:title["\']', html, re.I):
            s["onpage"] += 2
        if re.search(r'<meta[^>]+name=["\']twitter:card["\']', html, re.I):
            s["onpage"] += 2
        if re.search(r'<h1[^>]*>', html, re.I):
            s["onpage"] += 2

        # AEO (10 pts)
        if '"faqpage"' in all_schema_text:
            s["aeo"] += 4
        if '"speakable"' in all_schema_text:
            s["aeo"] += 3
        if re.search(r'<h2[^>]*>[^<]*\?', html, re.I):
            s["aeo"] += 3

        # E-E-A-T (10 pts)
        if '"author"' in all_schema_text:
            s["eeat"] += 3
        if '"datemodified"' in all_schema_text or '"datepublished"' in all_schema_text:
            s["eeat"] += 3
        if re.search(r'<meta[^>]+name=["\']author["\']', html, re.I):
            s["eeat"] += 2
        if 'knowsabout' in all_schema_text or 'hasoccupation' in all_schema_text:
            s["eeat"] += 2

    # GEO (25 pts)
    llms = fetch(urljoin(site, "/llms.txt"), timeout=10)
    if llms and llms.status_code == 200 and 'text/plain' in (llms.headers.get('content-type', '').lower()):
        s["geo"] += 7
        s["notes"].append("has llms.txt")
    llmsfull = fetch(urljoin(site, "/llms-full.txt"), timeout=10)
    if llmsfull and llmsfull.status_code == 200 and 'text/plain' in (llmsfull.headers.get('content-type', '').lower()):
        s["geo"] += 5
        s["notes"].append("has llms-full.txt")
    if rob and rob.status_code == 200:
        body = rob.text.lower()
        ai_bots = ["oai-searchbot", "perplexitybot", "chatgpt-user", "claudebot", "gptbot",
                   "bytespider", "google-extended", "amazonbot", "cohere-ai",
                   "meta-externalagent", "duckassistbot", "facebookbot", "applebot-extended", "ccbot"]
        explicit_allows = sum(1 for b in ai_bots
                              if re.search(rf'user-agent:\s*{re.escape(b)}\b[\s\S]{{0,300}}?allow:\s*/', body, re.I))
        s["geo"] += min(5, explicit_allows)
    if home and home.status_code == 200:
        html_lower = home.text.lower()
        if '"sameas"' in " ".join(schemas).lower() if schemas else False:
            s["geo"] += 5
        # generic citation magnets heuristic
        if re.search(r'\$\d+[km]?\b|\d+%|\d+x\b|\d+\+\s+(?:clients|users|customers)', html_lower):
            s["geo"] += 4
        if re.search(r'rel=["\']describedby["\'][^>]+href=["\'][^"\']*llms\.txt', home.text, re.I):
            s["geo"] += 2
        if re.search(r'link:[\s\S]{0,200}llms\.txt', " ".join(str(v) for v in (home.headers or {}).items()), re.I):
            s["geo"] += 2

    # Clamp each dimension to its max
    for k, cap in MAX_POINTS.items():
        s[k] = min(s[k], cap)
    s["composite"] = sum(s[k] for k in MAX_POINTS)
    return s

results = []
for url in SITES:
    print(f"scoring {url}...")
    r = score(url)
    results.append(r)
    time.sleep(0.5)

# sort desc
results.sort(key=lambda x: -x["composite"])
with open('/tmp/benchmarks.json','w') as f: json.dump(results, f, indent=2)
print("\n=== LEADERBOARD ===")
print(f"{'Rank':<5} {'Site':<30} {'Tech':>4} {'Sch':>4} {'GEO':>4} {'OnP':>4} {'AEO':>4} {'EEAT':>5} {'TOTAL':>6}")
for i, r in enumerate(results, 1):
    name = r['site'].replace('https://','').replace('www.','')
    print(f"{i:<5} {name:<30} {r['technical']:>4} {r['schema']:>4} {r['geo']:>4} {r['onpage']:>4} {r['aeo']:>4} {r['eeat']:>5} {r['composite']:>6}")
