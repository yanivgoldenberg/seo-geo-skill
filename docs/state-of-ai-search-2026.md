# State of AI Search Visibility 2026

**Benchmark:** 61 top SaaS and AI sites scored against a 100-point AI Search Readiness rubric.
**Method:** Reproducible Python script. Same rubric every site. Audit-only, no writes. Public-host checks enforced.
**Rubric:** Technical 20 + On-Page 15 + Schema 20 + GEO 25 + AEO 10 + E-E-A-T 10 = 100
**Date:** 2026-06-23 (re-scored under the v1.12.0 rubric, which de-weights llms.txt from 12 to 3 GEO points)

## Headline findings

- **56% of top SaaS sites scored 60 or lower.** Failing AI Search Readiness is still the norm.
- **Mean score: 54.3 / 100. Median: 59 / 100.**
- **OpenAI and Perplexity - the two biggest AI search companies - score 7/100 each**, the lowest on the board. The category leaders are almost invisible to their own category of search.
- **44% still lack full Person + Organization schema on their homepage** - the single biggest score gap in the bottom half.
- **yanivgoldenberg.com tops the leaderboard at 92/100** - full stack: Organization + Person schema with Wikidata sameAs, AI-crawler allow, citation-magnet content, speakable markup.

## Top 20 (best AI Search Readiness)

| Rank | Site | Score | Notable |
|---:|---|---:|---|
| 1 | yanivgoldenberg.com | **92** | Full stack |
| 2 | heroku.com | 86 | |
| 3 | retool.com | 82 | |
| 4 | amplitude.com | 80 | |
| 5 | beehiiv.com | 79 | |
| 5 | zapier.com | 79 | |
| 7 | resend.com | 75 | |
| 8 | render.com | 73 | |
| 9 | auth0.com | 70 | |
| 9 | cloudflare.com | 70 | |
| 9 | webflow.com | 70 | |
| 12 | mercury.com | 68 | |
| 12 | stripe.com | 68 | |
| 12 | supabase.com | 68 | |
| 15 | figma.com | 67 | |
| 15 | railway.app | 67 | Was 0 in April; added llms.txt + content since |
| 17 | asana.com | 65 | |
| 17 | calendly.com | 65 | |
| 17 | clerk.com | 65 | |
| 17 | monday.com | 65 | |

## Bottom 10 (worst AI Search Readiness)

| Rank | Site | Score | Main failure |
|---:|---|---:|---|
| 51 | convertkit.com | 38 | Schema + GEO gaps |
| 51 | mixpanel.com | 38 | Schema + GEO gaps |
| 51 | segment.com | 38 | Schema + GEO gaps |
| 55 | fly.io | 36 | Schema + GEO gaps |
| 55 | netlify.com | 36 | Schema + GEO gaps |
| 57 | datadog.com | 31 | Schema + GEO gaps |
| 58 | ramp.com | 18 | Blocked crawlers |
| 59 | canva.com | 13 | Almost nothing |
| 60 | openai.com | 7 | No schema, minimal AI-allow |
| 60 | perplexity.ai | 7 | Same profile as OpenAI |

## The 3 highest-leverage wins

1. **Add Organization + Person JSON-LD with sameAs** - schema deficiency is the single biggest score gap in the bottom half.
2. **sameAs with Wikidata + allow AI search crawlers** (OAI-SearchBot, Perplexity-User, ClaudeBot) - many sites silently block or omit the crawlers they most want to be cited by.
3. **Publish `/llms.txt` and `/llms-full.txt`** - cheap entity hygiene, but no AI search engine consumes it as of 2026, so it is a small part of the score (3 of 25 GEO points).

Full rubric, script, and reproducible methodology: [seo-geo-skill on GitHub](https://github.com/yanivgoldenberg/seo-geo-skill).

## Methodology

- Script: `tests/benchmark_sites.py` (publicly readable, publicly runnable).
- Safety: `_is_public_url()` blocks private IPs, loopback, reserved ranges. Read-only.
- User agent: `seo-geo-skill/1.6.0 benchmark`.
- Each site scored independently; rank by composite.
- **Audit-only.** No writes. Scores reflect the live homepage fetch at the time of benchmarking.
- **Limitation:** a site blocking the benchmark user agent can score lower than it would with a browser fetch. This is intentional - if you block generic bots, you likely block AI crawlers too.

## Reproduce

```bash
git clone https://github.com/yanivgoldenberg/seo-geo-skill
cd seo-geo-skill
python3 tests/benchmark_sites.py
```

Swap the `SITES` list to benchmark any cohort.

## Want this applied to your site?

If your score came in under 60, you have the same pattern of gaps as 56% of the sites above. I run a paid **AI Search Visibility Audit** for post-PMF SaaS and e-commerce brands. Application-only, starts at $7.5K, credited into the Implementation Sprint if you continue.

[Apply for the audit](https://yanivgoldenberg.com/contact/)
