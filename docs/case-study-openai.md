# Case Study: OpenAI.com Scores 7/100 on AI Search Readiness

**The AI company that serves billions of ChatGPT queries has zero structured data on its homepage.**

## Phase 0 Audit (2026-04-24)

| Signal | State | Points |
|---|---|---:|
| robots.txt allows AI crawlers | Yes (`Allow: /` for `*`) | 7 / 20 |
| /llms.txt | Missing (HTTP 403 from CloudFront) | 0 / 25 (GEO) |
| /llms-full.txt | Missing (HTTP 403) | 0 |
| Organization JSON-LD | Missing | 0 / 20 |
| Person JSON-LD | Missing | 0 |
| WebSite JSON-LD | Missing | 0 |
| BreadcrumbList JSON-LD | Missing | 0 |
| `<meta name="description">` | Missing in first 8KB | 0 / 15 |
| `<meta property="og:title">` | Missing | 0 |
| `<link rel="canonical">` | Missing | 0 |
| SpeakableSpecification | Missing | 0 / 10 (AEO) |
| E-E-A-T signals (author, sameAs) | Missing | 0 / 10 |

**Composite: 7 / 100**

## What a Phase 1-20 Fix Plan Would Deliver

| Fix | Rubric lift | Effort |
|---|---:|---|
| Publish `/llms.txt` + `/llms-full.txt` with product summary, entity facts, sitemap | +15 GEO | 30 min |
| Add Organization + Person + WebSite + BreadcrumbList JSON-LD on homepage | +20 Schema | 2 hours |
| Add `<meta name="description">`, `<meta property="og:*">`, `<link rel="canonical">` | +10 On-Page | 1 hour |
| Add SpeakableSpecification on the product positioning paragraph | +5 AEO | 30 min |
| Add Person schema with `sameAs` linking to founder/CEO Wikipedia + LinkedIn | +5 E-E-A-T | 1 hour |
| Add `sameAs` Organization links (Crunchbase, Wikipedia, X, LinkedIn) | +5 GEO | 30 min |
| Explicit `Allow: /` for GPTBot, ClaudeBot, PerplexityBot, Google-Extended, CCBot (currently covered by wildcard but not explicit - explicit is recommended) | +3 Technical | 10 min |

**Projected composite: 7 → 70 (+63 points) in under a day of engineering work.**

## Why This Matters

OpenAI's ChatGPT answers depend on being able to parse structured content from cited sources. Their own homepage provides none of those signals to other AI systems that might cite OpenAI as a source. The irony is obvious, but it is also a specific, fixable engineering gap.

Every fix above is deterministic, reproducible, and testable with the public `tests/benchmark_sites.py` script in this repo. Re-run the score before and after any change to measure the lift.

## Reproducibility

```bash
git clone https://github.com/yanivgoldenberg/seo-geo-skill
cd seo-geo-skill
python3 - <<PY
import importlib.util
spec = importlib.util.spec_from_file_location("bs", "tests/benchmark_sites.py")
m = importlib.util.module_from_spec(spec)
m.UA = {"User-Agent": "Mozilla/5.0"}
spec.loader.exec_module(m)
print(m.score("https://openai.com"))
PY
```

Expected output (as of 2026-04-24):
```
{'site': 'https://openai.com', 'technical': 7, 'schema': 0, 'geo': 0, 'onpage': 0, 'aeo': 0, 'eeat': 0, 'composite': 7}
```

Anyone can verify this score in 10 seconds. No claims without evidence.

## The Methodology Site (yanivgoldenberg.com, 97/100)

For contrast, `yanivgoldenberg.com` tops the same 61-site leaderboard at **97/100** using exactly the same rubric and script. That is the methodology proof, not the case study - a canonical reference deployment of every fix listed above. Replicate those fixes on any CMS (WordPress, Shopify, Webflow, Next.js) using the platform adapters in this repo.
