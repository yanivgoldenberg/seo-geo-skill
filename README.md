# seo-geo-skill

<p align="center">
  <img src="docs/assets/seo-geo-cover-1600x900.png" alt="seo-geo-skill - 19-phase SEO + GEO + AEO skill for Claude Code" width="100%" />
</p>

<div align="center">

**53% of top SaaS sites have no /llms.txt. 73% have broken Organization schema. This fixes both in one session.**

*The only Claude Code skill that closes every SEO, GEO, and AEO gap in one session.*

[![Version](https://img.shields.io/badge/version-1.4.0-blue?style=flat-square)](https://github.com/yanivgoldenberg/seo-geo-skill/releases)
[![CI](https://img.shields.io/github/actions/workflow/status/yanivgoldenberg/seo-geo-skill/ci.yml?style=flat-square)](https://github.com/yanivgoldenberg/seo-geo-skill/actions)
[![Benchmark](https://img.shields.io/badge/15_sites_benchmarked-brightgreen?style=flat-square)](docs/benchmarks.md)
[![License](https://img.shields.io/badge/license-PolyForm%20Noncommercial-orange?style=flat-square)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-skill-purple?style=flat-square)](https://claude.ai/code)

</div>

---

## Run it on your site in 10 seconds

```bash
curl -fsSL https://raw.githubusercontent.com/yanivgoldenberg/seo-geo-skill/main/seo-geo.md \
  -o ~/.claude/skills/seo-geo.md

# then in Claude Code:
/seo-geo https://yoursite.com
```

One command. Full audit. Ranked fix list. Works on any CMS.

---

## We benchmarked 15 top SaaS sites. Most are invisible to AI.

| Rank | Site | Score | Why |
|---:|---|---:|---|
| 1 | **yanivgoldenberg.com** | **90** | Full stack: llms.txt, Organization + Person schema, AI-crawler allow |
| 2 | stripe.com | 73 | No llms.txt |
| 2 | resend.com | 73 | No AI-crawler allow in robots |
| 4 | planetscale.com | 65 | No Person schema |
| 5 | vercel.com | 63 | Thin Organization schema |
| 5 | figma.com | 63 | No llms.txt |
| 7 | elementor.com | 62 | Partial schema |
| 8 | notion.so | 60 | No Organization schema on homepage |
| 9 | mercury.com | 58 | No llms.txt |
| 10 | supabase.com | 55 | No Organization schema |
| 11 | linear.app | 53 | No schema on homepage at all |
| 12 | riverside.fm | 50 | No llms.txt, thin meta |
| 13 | **anthropic.com** | **30** | *The AI company itself: no llms.txt, no Organization schema* |
| 14 | ramp.com | 25 | Minimal homepage markup |
| 15 | fly.io | 10 | No robots.txt, no schema, no meta |

**Full methodology + reproduce-yourself script:** [`docs/benchmarks.md`](docs/benchmarks.md)

### What the data shows

- **53% of top SaaS sites have no llms.txt.** They are invisible to AI crawlers that respect the standard.
- **73% have no proper Person or Organization schema on their homepage.**
- **Only 3 sites explicitly allow AI crawlers in robots.txt.** The rest rely on implicit allow, which security plugins often treat as deny.
- **Anthropic.com - the company building Claude - scores 30/100.** Even the AI companies are blind to AI.

If your site scores below 60 on this rubric, you're in the bottom third of well-funded SaaS brands. The three cheapest wins:

1. Publish `/llms.txt` and `/llms-full.txt` → +25 points
2. Add Organization + Person JSON-LD → +15 points
3. Allow AI crawlers explicitly in robots.txt → +10 points

This skill automates all three in one session.

---

## Who this is for

- Marketers who want citations in ChatGPT, Perplexity, and Google AI Overviews
- Developers adding SEO to a client site and need it done right the first time
- Agencies running the same 20-point audit on 50+ client sites per year

**Not a fit** if you want a 20-sub-skill toolbox. See [`docs/compare.md`](docs/compare.md) for honest comparisons to other Claude Code SEO skills.

---

## What it does (19 phases)

Open `seo-geo.md` for the full skill. At a glance:

**The audit** (non-destructive, always safe):
- Phase 0 - 100-point scoring rubric across 6 dimensions
- Phases 1-3 - Technical SEO, on-page, schema (16 types)
- Phase 4 - LLM citation (llms.txt + entity anchoring)
- Phase 5 - Answer engine optimization
- Phase 6 - E-E-A-T trust signals
- Phases 7-14 - Content, speed, hreflang, debugging

**The writes** (opt-in via `--apply`):
- Phase 15 - WordPress security hardening
- Phase 16 - Field patterns from production
- Phase 17 - Dry-run safety gates + banned endpoint list
- Phase 18 - Multi-platform adapters (WordPress / Shopify / Webflow / Next.js)
- Phase 19 - Competitor benchmarking

---

## Install

```bash
# Global install
curl -fsSL https://raw.githubusercontent.com/yanivgoldenberg/seo-geo-skill/main/seo-geo.md \
  -o ~/.claude/skills/seo-geo.md
```

<details>
<summary>Project-level install + plugin use</summary>

```bash
# Project-level only
curl -fsSL https://raw.githubusercontent.com/yanivgoldenberg/seo-geo-skill/main/seo-geo.md \
  -o .claude/skills/seo-geo.md
```
</details>

---

## Usage

```bash
# Start here
/seo-geo https://yoursite.com

# Variants
/seo-geo --verify                # self-test: tools accessible?
/seo-geo --audit-only            # score only, no writes
/seo-geo --phase geo             # LLM citation only (fastest ROI)
/seo-geo --phase technical       # technical SEO only
/seo-geo --page <url>            # single page audit
/seo-geo --apply                 # writes enabled (opt-in, see Phase 17)
/seo-geo --benchmark <competitor> # head-to-head score
```

---

## Schemas supported

`Person` `Organization` `SoftwareApplication` `LocalBusiness` `Product` `Service` `Article` `BlogPosting` `FAQPage` `HowTo` `BreadcrumbList` `WebSite` `ProfilePage` `DefinedTerm` `Review` `SpeakableSpecification` `VideoObject`

---

## Author

**[Yaniv Goldenberg](https://yanivgoldenberg.com)** | [LinkedIn](https://www.linkedin.com/in/yanivgoldenberg/)

Former Head of Growth at a PLG SaaS with 20M+ users (100x ARR), a consumer SaaS (+337% MRR), an MLOps SaaS acquired by a Fortune 100. $100M+ in ad spend managed.

If this saved you an afternoon - star the repo. If you want help applying it at scale: [book a 15-min call](https://yanivgoldenberg.com/contact).

---

## License

[PolyForm Noncommercial 1.0.0](https://polyformproject.org/licenses/noncommercial/1.0.0)

Free for personal use, internal business use, and client work. Commercial use - reselling, white-labeling, or packaging as a paid product - requires a commercial license: [yanivgoldenberg.com/contact](https://yanivgoldenberg.com/contact)
