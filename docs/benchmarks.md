# Public Benchmark - 13 SaaS sites scored (original cohort)

> **The expanded 61-site benchmark is here:** [State of AI Search Visibility 2026](state-of-ai-search-2026.md). 67% fail. OpenAI and Perplexity both score 7/100. Railway scores 0.

Run date: 2026-04-24 (rescored against canonical rubric in v1.6.0).

**Methodology:** audit-only `/seo-geo` against each site's homepage + robots.txt + /llms.txt + /llms-full.txt. No writes. Same scoring code for every site (`tests/benchmark_sites.py`).

**Rubric (canonical, same as Phase 0 in `seo-geo.md`):** Technical 20 + On-Page 15 + Schema 20 + GEO 25 + AEO 10 + E-E-A-T 10 = 100.

> Two additional SaaS sites were originally scored in v1.4.0 but removed from public display in v1.5.0 due to prior-employer / client-adjacent relationships. Scoring method is unchanged. Total sites benchmarked: 15; publicly listed: 13.

## Leaderboard (max column values reflect canonical rubric)

Column maxes: Technical 20, On-Page 15, Schema 20, GEO 25, AEO 10, E-E-A-T 10.

| Rank | Site | Technical | On-Page | Schema | GEO | AEO | E-E-A-T | Composite |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | yanivgoldenberg.com | 20 | 15 | 20 | 20 | 10 | 5 | **90** |
| 2 | stripe.com | 12 | 15 | 20 | 15 | 5 | 6 | **73** |
| 2 | resend.com | 12 | 15 | 20 | 15 | 5 | 6 | **73** |
| 4 | planetscale.com | 12 | 15 | 15 | 15 | 5 | 3 | **65** |
| 5 | vercel.com | 12 | 15 | 10 | 15 | 5 | 6 | **63** |
| 5 | figma.com | 20 | 15 | 15 | 0 | 5 | 8 | **63** |
| 7 | notion.so | 20 | 15 | 0 | 15 | 5 | 5 | **60** |
| 8 | mercury.com | 12 | 15 | 20 | 0 | 5 | 6 | **58** |
| 9 | supabase.com | 8 | 15 | 0 | 22 | 5 | 5 | **55** |
| 10 | linear.app | 12 | 15 | 0 | 15 | 5 | 6 | **53** |
| 11 | anthropic.com | 12 | 10 | 0 | 0 | 5 | 3 | **30** |
| 12 | ramp.com | 8 | 0 | 0 | 15 | 0 | 2 | **25** |
| 13 | fly.io | 0 | 5 | 0 | 0 | 5 | 0 | **10** |

Note: composite scores are unchanged from v1.4.0 - only the column allocations are rebalanced to match the canonical rubric. Re-run `python3 tests/benchmark_sites.py` to reproduce.

## What the data reveals


**73% have no Person or Organization schema on the homepage.** Of the 13 sites, 9 either have no JSON-LD or an Organization/Person node that's missing core fields like `sameAs`, `logo`, or `description`. These sites will be harder to disambiguate in LLM answer generation.

**Anthropic's own site scores 30/100.** The company building Claude has no llms.txt, no Organization schema with sameAs, and no structured author attribution on its homepage. Even the AI companies are blind to AI.

**Only 3 sites allow AI crawlers explicitly** - supabase.com, ramp.com, and yanivgoldenberg.com have `User-agent: OAI-SearchBot / PerplexityBot / ClaudeBot` with `Allow: /` rules. The rest implicitly allow by omission, which security plugins often treat as disallow.

**Full marks on Technical SEO: only 3 sites** - figma.com, notion.so, and yanivgoldenberg.com scored 25/25 (robots.txt + AI-crawler allow + sitemap + canonical).

## What this means for your site

If you're below 60 on this rubric, you're in the bottom third of well-funded SaaS brands. The three cheapest wins:

1. **Publish /llms.txt and /llms-full.txt** - 25 points, 1 hour of work
2. **Add Organization + Person JSON-LD** - 15 points, 30 minutes with our skill
3. **Allow AI crawlers explicitly in robots.txt** - 10 points, 5 minutes

Our skill automates all three.

## Methodology notes

- Scores use the same weight schedule as Phase 0 of the skill, applied via an audit-only run (no writes to any site).
- Scoring code in `tests/benchmark_sites.py`. Reruns are deterministic given the same HTML snapshots.
- We respect `robots.txt` on every fetch. No site was crawled past its homepage + standard root files (robots.txt, llms.txt, llms-full.txt).
- Points awarded when the signal is present and valid, not just declared. A broken canonical link gets 0 points, not 5.

## Reproducing the benchmark

```bash
git clone https://github.com/yanivgoldenberg/seo-geo-skill
cd seo-geo-skill
python3 tests/benchmark_sites.py > latest-benchmarks.md
```

Add your own site to the `SITES` list at the top of the script. Run takes under 2 minutes.

## Raw data

Full JSON in `docs/benchmarks.json` (attached to v1.4.0 release).
