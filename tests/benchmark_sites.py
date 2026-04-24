import requests, re, json, time
from urllib.parse import urljoin

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
    "https://elementor.com",
    "https://riverside.fm",
    "https://notion.so",
    "https://figma.com",
    "https://yanivgoldenberg.com",
]

UA = {"User-Agent":"seo-geo-skill/1.4.0 benchmark (+https://github.com/yanivgoldenberg/seo-geo-skill)"}

def fetch(url, timeout=15):
    try:
        r = requests.get(url, headers=UA, timeout=timeout, allow_redirects=True)
        return r
    except Exception as e:
        return None

def score(site):
    s = {"site": site, "technical":0, "schema":0, "geo":0, "onpage":0, "aeo":0, "eeat":0, "notes":[]}
    # Technical SEO (25 pts)
    rob = fetch(urljoin(site, "/robots.txt"))
    if rob and rob.status_code == 200:
        s["technical"] += 5
        body = rob.text.lower()
        ai_bots = ["oai-searchbot","perplexitybot","chatgpt-user","claudebot","gptbot","bytespider","google-extended","amazonbot","cohere-ai"]
        if any(b in body for b in ai_bots):
            allows_ai = any(f"user-agent: {b}" in body and "allow:" in body.split(f"user-agent: {b}",1)[1][:300] for b in ai_bots)
            s["technical"] += 10 if allows_ai else 3
            if allows_ai: s["notes"].append("allows AI bots")
        else:
            s["notes"].append("no AI bot rules in robots.txt")
        if "sitemap:" in body: s["technical"] += 5

    home = fetch(site)
    if home and home.status_code == 200:
        html = home.text
        # canonical
        if re.search(r'<link[^>]+rel=["\']canonical["\']', html, re.I):
            s["technical"] += 5

        # Schema (20 pts)
        schemas = re.findall(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html, re.S)
        if schemas:
            s["schema"] += 5
            all_schema_text = " ".join(schemas).lower()
            if '"organization"' in all_schema_text: s["schema"] += 5
            if '"person"' in all_schema_text: s["schema"] += 5
            if 'sameas' in all_schema_text: s["schema"] += 5

        # On-page (15 pts)
        if re.search(r'<title>[^<]{10,}</title>', html, re.I): s["onpage"] += 5
        if re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'][^"\']{50,}', html, re.I): s["onpage"] += 5
        if re.search(r'<meta[^>]+property=["\']og:image["\']', html, re.I): s["onpage"] += 5

        # AEO (10 pts)
        all_schema_text = " ".join(schemas).lower() if schemas else ""
        if '"faqpage"' in all_schema_text or '"speakable"' in all_schema_text: s["aeo"] += 5
        if re.search(r'<h1[^>]*>.*?</h1>', html, re.I | re.S): s["aeo"] += 3
        if re.search(r'<h2[^>]*>', html, re.I): s["aeo"] += 2

        # E-E-A-T (5 pts)
        if 'author' in html.lower() or '"author"' in all_schema_text: s["eeat"] += 3
        if 'datemodified' in all_schema_text or 'datepublished' in all_schema_text: s["eeat"] += 2

    # GEO (25 pts) - llms.txt + llms-full.txt
    llms = fetch(urljoin(site, "/llms.txt"), timeout=10)
    if llms and llms.status_code == 200 and 'text/plain' in (llms.headers.get('content-type','').lower()):
        s["geo"] += 15
        s["notes"].append("has llms.txt")
    llmsfull = fetch(urljoin(site, "/llms-full.txt"), timeout=10)
    if llmsfull and llmsfull.status_code == 200 and 'text/plain' in (llmsfull.headers.get('content-type','').lower()):
        s["geo"] += 10
        s["notes"].append("has llms-full.txt")

    s["composite"] = s["technical"] + s["schema"] + s["geo"] + s["onpage"] + s["aeo"] + s["eeat"]
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
