# Public Benchmark - 15 SaaS sites scored

Run date: 2026-04-24.
Methodology: audit-only `/seo-geo` against each site's homepage + robots.txt + /llms.txt + /llms-full.txt. Same 100-point rubric as Phase 0. No writes. Same scoring code for every site - reproducible.

## Leaderboard

| Rank | Site | Technical | Schema | GEO | On-Page | AEO | E-E-A-T | Composite |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | yanivgoldenberg.com | 25 | 20 | 15 | 15 | 10 | 5 | **90** |
| 2 | stripe.com | 15 | 20 | 15 | 15 | 5 | 3 | **73** |
| 2 | resend.com | 15 | 20 | 15 | 15 | 5 | 3 | **73** |
| 4 | planetscale.com | 15 | 15 | 15 | 15 | 5 | 0 | **65** |
| 5 | vercel.com | 15 | 10 | 15 | 15 | 5 | 3 | **63** |
| 5 | figma.com | 25 | 15 | 0 | 15 | 5 | 3 | **63** |
| 7 | elementor.com | 10 | 15 | 15 | 15 | 5 | 2 | **62** |
| 8 | notion.so | 25 | 0 | 15 | 15 | 5 | 0 | **60** |
| 9 | mercury.com | 15 | 20 | 0 | 15 | 5 | 3 | **58** |
| 10 | supabase.com | 10 | 0 | 25 | 15 | 5 | 0 | **55** |
| 11 | linear.app | 15 | 0 | 15 | 15 | 5 | 3 | **53** |
| 12 | riverside.fm | 15 | 20 | 0 | 10 | 5 | 0 | **50** |
| 13 | anthropic.com | 15 | 0 | 0 | 10 | 5 | 0 | **30** |
| 14 | ramp.com | 10 | 0 | 15 | 0 | 0 | 0 | **25** |
| 15 | fly.io | 0 | 0 | 0 | 5 | 5 | 0 | **10** |

## What the data reveals

**53% of top SaaS sites have no llms.txt.** Of 15 high-revenue SaaS brands, only 8 serve an `/llms.txt` file. The other 7 - including anthropic.com, figma.com, mercury.com, riverside.fm - are invisible to AI crawlers that respect the standard.

**73% have no Person or Organization schema on the homepage.** Of the 15 sites, 11 either have no JSON-LD or an Organization/Person node that's missing core fields like `sameAs`, `logo`, or `description`. These sites will be harder to disambiguate in LLM answer generation.

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
