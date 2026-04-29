# State of AI Search Visibility 2026

**Benchmark:** 61 top SaaS and AI sites scored against a 100-point AI Search Readiness rubric.
**Method:** Reproducible Python script. Same rubric every site. Audit-only, no writes. Public-host checks enforced.
**Rubric:** Technical 20 + On-Page 15 + Schema 20 + GEO 25 + AEO 10 + E-E-A-T 10 = 100
**Date:** 2026-04-24

## Headline findings

- **67% of top SaaS sites scored 60 or lower.** Failing AI Search Readiness is the norm, not the exception.
- **Mean score: 49.4 / 100. Median: 52 / 100.**
- **OpenAI and Perplexity - the two biggest AI search companies - score 7/100 each.** The category leaders are almost invisible to their own category of search.
- **Railway scores 0.** Blocked AI crawlers, no schema, no llms.txt.
- **yanivgoldenberg.com tops the leaderboard at 97/100** - full stack: llms.txt, Organization + Person schema, AI-crawler allow, speakable markup.

## Top 20 (best AI Search Readiness)

| Rank | Site | Score | Notable |
|---:|---|---:|---|
| 1 | yanivgoldenberg.com | **97** | Full stack |
| 2 | heroku.com | 80 | |
| 3 | amplitude.com | 77 | |
| 4 | beehiiv.com | 76 | |
| 5 | resend.com | 70 | |
| 6 | monday.com | 69 | |
| 7 | workos.com | 68 | |
| 8 | render.com | 66 | |
| 9 | stripe.com | 65 | |
| 10 | webflow.com | 65 | |
| 11 | asana.com | 65 | |
| 12 | auth0.com | 64 | |
| 13 | planetscale.com | 62 | |
| 14 | figma.com | 62 | |
| 15 | retool.com | 62 | |
| 16 | mercury.com | 61 | |
| 17 | cursor.com | 61 | |
| 18 | framer.com | 61 | |
| 19 | mongodb.com | 61 | |
| 20 | algolia.com | 61 | |

## Bottom 10 (worst AI Search Readiness)

| Rank | Site | Score | Main failure |
|---:|---|---:|---|
| 52 | databricks.com | 36 | Schema gaps |
| 53 | snowflake.com | 36 | Schema gaps |
| 54 | datadog.com | 34 | Schema + GEO |
| 55 | replicate.com | 32 | Schema + GEO |
| 56 | fly.io | 22 | Blocked crawlers |
| 57 | ramp.com | 21 | Blocked crawlers |
| 58 | canva.com | 12 | Almost nothing |
| 59 | openai.com | 7 | No llms.txt, no schema, minimal AI-allow |
| 60 | perplexity.ai | 7 | Same profile as OpenAI |
| 61 | railway.app | 0 | Blocked everything |

## The 3 cheapest wins (replicable in under an hour)

1. **Publish `/llms.txt` and `/llms-full.txt`** - entity hygiene; most winners have it, most losers do not.
2. **Add Organization + Person JSON-LD** - schema deficiency is the single biggest score gap in the bottom half.
3. **Allow GPTBot, ClaudeBot, PerplexityBot in robots.txt** - many sites silently block the crawlers they most want to be cited by.

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

If your score came in under 60, you have the same pattern of gaps as 67% of the sites above. I run a paid **AI Search Visibility Audit** for post-PMF SaaS and e-commerce brands. Application-only, starts at $7.5K, credited into the Implementation Sprint if you continue.

[Apply for the audit](https://yanivgoldenberg.com/contact)
