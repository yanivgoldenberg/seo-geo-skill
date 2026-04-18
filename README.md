# seo-geo-skill

<div align="center">

**Your site is invisible to AI. This fixes it.**

*The only Claude Code skill that closes every SEO, GEO, and AEO gap in one session.*

[![Version](https://img.shields.io/badge/version-1.0.0-blue?style=flat-square)](https://github.com/yanivgoldenberg/seo-geo-skill/releases)
[![License](https://img.shields.io/badge/license-PolyForm%20Noncommercial-orange?style=flat-square)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-skill-purple?style=flat-square)](https://claude.ai/code)
[![Platforms](https://img.shields.io/badge/platforms-WordPress%20%7C%20Shopify%20%7C%20Webflow%20%7C%20Next.js-green?style=flat-square)](#supported-platforms)

</div>

---

From `robots.txt` to `llms.txt` - every signal that affects whether humans and AI find you, scored and fixed in one Claude Code session. 15 phases. 16 schema types. 7 platforms. Any CMS.

**Who this is for:**
- Marketers who want citations in ChatGPT, Perplexity, and Google AI Overviews
- Developers adding SEO to a client site and need it done right the first time
- Agencies who need schema + GEO at scale without a 10-tab checklist

---

## Install

```bash
# Global install (one command, works immediately)
curl -fsSL https://raw.githubusercontent.com/yanivgoldenberg/seo-geo-skill/main/seo-geo.md \
  -o ~/.claude/skills/seo-geo.md
```

<details>
<summary>Other install options</summary>

```bash
# Project-level only
curl -fsSL https://raw.githubusercontent.com/yanivgoldenberg/seo-geo-skill/main/seo-geo.md \
  -o .claude/skills/seo-geo.md

# Via plugin: add to your plugin's skills/ folder
```

</details>

---

## Usage

```bash
/seo-geo https://yoursite.com    # start here: audit → score → top fixes
```

```
/seo-geo --verify                # first time? run this first
/seo-geo --audit-only            # score only, no writes
/seo-geo --phase geo             # LLM citation only (fastest ROI)
/seo-geo --phase technical       # technical SEO only
/seo-geo --page <url>            # single page audit
/seo-geo --schema Person         # generate one schema type
/seo-geo --llms-txt              # create/update llms.txt only
/seo-geo --score                 # current score breakdown
```

> **First time?** Run `/seo-geo --verify` before anything else. It checks tool access and credentials and tells you exactly what's missing before touching your site.

---

## What the audit output looks like

```
Score: 34/100

CRITICAL (fix now):
  [ ] No schema markup on any page                    -20 pts
  [ ] GPTBot, ClaudeBot blocked in robots.txt         -7 pts
  [ ] Meta descriptions missing on 3/4 pages          -6 pts

HIGH:
  [ ] llms.txt missing                                -5 pts
  [ ] No canonical tags                               -4 pts

ALREADY DONE:
  [x] HTTPS active
  [x] Mobile viewport set
  [x] Single H1 per page

Run /seo-geo to fix all CRITICAL items automatically.
```

---

## 15 phases. Every gap covered.

| Phase | What it does |
|-------|-------------|
| **0 - Audit** | Scores site 0-100. Prioritized gap list. No writes. |
| **1 - Technical** | robots.txt, AI crawler access, canonical tags, sitemap |
| **2 - On-Page** | Titles, meta descriptions, OG tags, H1 hierarchy |
| **3 - Schema** | 16+ schema types injected per page type and business |
| **4 - GEO** | llms.txt, entity signals, sameAs, LLM citation structure |
| **5 - AEO** | Speakable schema, answer-first content, SERP features |
| **6 - E-E-A-T** | Author schema, expertise signals, trust indicators |
| **7 - Content Strategy** | Topical authority, skyscraper method, content briefs |
| **8 - Core Web Vitals** | LCP, INP, CLS - measured and fixed per platform |
| **9 - Internal Linking** | Hub-and-spoke architecture, PageRank flow, anchor audit |
| **10 - Content Decay** | Refresh strategy, GSC impression tracking |
| **11 - Programmatic SEO** | Template + data at scale, quality gates |
| **12 - Video SEO** | VideoObject schema, YouTube SEO, video sitemap |
| **13 - International SEO** | Hreflang, x-default, multilingual schema, locale signals |
| **14 - Debugging** | 15-row error matrix, cache clearing, curl verification |

---

## What it delivers

| Metric | Before | After |
|--------|--------|-------|
| Schema types present | 0-1 | 12-16 |
| AI crawlers explicitly allowed | 0 | 9 |
| llms.txt present | No | Yes (+ llms-full.txt) |
| Pages with complete OG tags | 0 of N | All pages |
| Internal linking structure | Flat | Hub-and-spoke |

One session closes all critical gaps. Ongoing work (content decay, programmatic SEO) runs on the built-in maintenance schedule.

---

## Scoring rubric

| Dimension | Points |
|-----------|--------|
| Technical SEO | /20 |
| On-Page SEO | /20 |
| Schema / Structured Data | /20 |
| GEO / LLM Optimization | /20 |
| E-E-A-T | /10 |
| AEO / Answer Engine | /10 |
| **Total** | **/100** |

---

## Supported platforms

| Platform | Meta | Schema | robots.txt |
|----------|------|--------|-----------|
| WordPress + Elementor | Rank Math REST API | HTML widget via WP REST API | Rank Math editor |
| WordPress Classic | Rank Math / Yoast | Custom HTML block | Plugin editor |
| Shopify | Metafields / theme liquid | theme.liquid + page templates | robots.txt.liquid |
| Webflow | Page Settings | Site Settings Custom Code | Site Settings |
| Next.js / React | `generateMetadata()` / next/head | next/head script tag | /app/robots.ts |
| Static HTML | Direct `<head>` edit | Direct `<head>` edit | robots.txt file |
| Ghost | Post meta tab | Code injection | routes.yaml |

---

## Schema types included

`Person` `Organization` `SoftwareApplication` `LocalBusiness` `Product` `Service` `Article` `BlogPosting` `FAQPage` `HowTo` `BreadcrumbList` `WebSite` `ProfilePage` `DefinedTerm` `Review` `SpeakableSpecification` `VideoObject`

---

## Author

**[Yaniv Goldenberg](https://yanivgoldenberg.com)** | [LinkedIn](https://www.linkedin.com/in/yanivgoldenberg/)

Former Head of Growth at Elementor (21M websites), Riverside.fm (337% MRR growth), cnvrg.io (acquired by Intel). $100M+ in ad spend managed. Now Fractional Head of Growth for B2B SaaS and ecommerce.

If this saved you time - star the repo. If you want help applying it: [book a 15-min call](https://yanivgoldenberg.com/contact).

---

## License

[PolyForm Noncommercial 1.0.0](https://polyformproject.org/licenses/noncommercial/1.0.0)

Free for personal use, internal business use, and client work. Commercial use - reselling, white-labeling, or packaging as a paid product - requires a commercial license: [yanivgoldenberg.com/contact](https://yanivgoldenberg.com/contact)
