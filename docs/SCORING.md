# Canonical Scoring Rubric: AI Search Readiness (100 pts)

> One rubric. One scale. Every GEO/SEO surface in this project scores against
> the same 100 points defined here.

## What the score means

The score measures **AI Search Readiness**: how machine-legible a site is to
the systems that now decide visibility (Google AI Overviews, ChatGPT, Perplexity,
Gemini, Bing Copilot) and to classic crawlers. It is a readiness score, not a
promise. Citations, rankings, and AI-referred traffic are **outcomes** that a
high readiness score makes more likely. This rubric never claims a guaranteed
position.

## Two scoring contexts: manual audit vs automated benchmark

This rubric is the **manual-audit standard** that the skill applies interactively
to a single site (Phase 0). The public 61-site leaderboard is produced by an
**automated benchmark** (`tests/benchmark_sites.py`) that scores only the
crawl-observable subset of this rubric, using documented proxies. The two share
the same six buckets and the same 100-point total, but they are NOT identical at
the per-check level: the automated benchmark cannot measure criteria that need a
field-data API, a full-site crawl, or private data, so it omits or approximates
them (see "What the automated benchmark scores" below). Treat the benchmark score
as an automated approximation of the manual rubric, not a substitute for it.

## The canonical 100-pt rubric (manual audit)

Six buckets, 100 points. These bucket weights are the single source of truth and
are shared by `seo-geo.md` Phase 0, `tests/benchmark_sites.py` MAX_POINTS, and
`tests/test_scoring_parity.py` (which fails the build if the bucket totals drift).

| Bucket | Points | What it measures |
|--------|--------|------------------|
| Technical SEO | 20 | HTTPS, robots.txt + AI crawler access, sitemap, canonical, single H1, mobile viewport, Core Web Vitals, no broken links |
| On-Page SEO | 15 | Title, meta description, OG tags, Twitter card, primary keyword placement, internal links with descriptive anchors |
| Schema / Structured Data | 20 | Page-type schema, FAQPage, BreadcrumbList, dateModified freshness, zero validation errors |
| GEO / LLM Optimization | 25 | llms.txt + llms-full.txt, AI crawler explicit-allow, sameAs with Wikidata, citation-magnet content, Link header, entity disambiguation |
| AEO / Answer Engine | 10 | Speakable schema, HowTo schema, question-style H2s for direct-answer extraction, featured-snippet target structure |
| E-E-A-T | 10 | Author bio + credentials, author schema, specific proof points, external links to authoritative sources |

**Total: 20 + 15 + 20 + 25 + 10 + 10 = 100**

### Per-check breakdown (manual audit)

The verbatim sub-checks and point values live in `seo-geo.md` Phase 0 under
"Scoring rubric (100 points)". They are reproduced here for reference; Phase 0
remains the authoritative copy. The parity test pins the six bucket totals (not
every sub-check) across Phase 0, `benchmark_sites.py`, and this file.

**Technical SEO (20 pts)** -- HTTPS active (2), robots.txt clean + AI crawlers allowed (3), valid XML sitemap submitted to GSC (2), canonical on every page (2), single H1 per page (2), mobile viewport meta (2), Core Web Vitals LCP/INP/CLS in budget (5), no broken internal links (2).

**On-Page SEO (15 pts)** -- Title 39-60 chars keyword-first (3), meta description 150-178 chars (3), OG title + description + image 1200x630 absolute URL (3), Twitter card tags (1), primary keyword in H1 + title + first 100 words (3), 3+ internal links with descriptive anchors (2).

**Schema / Structured Data (20 pts)** -- Schema type matches page type (5), FAQPage where Q&A exists (4), BreadcrumbList on all non-home pages (3), dateModified present and under 90 days (3), no validation errors (5).

**GEO / LLM Optimization (25 pts)** -- llms.txt + llms-full.txt comprehensive (7), all 14+ AI crawlers explicitly allowed (5), sameAs with 4+ verified profiles incl. Wikidata (5), specific claims/numbers/named entities (4), Link header to llms.txt (2), entity disambiguation across 3+ external sources (2).

**AEO / Answer Engine (10 pts)** -- Speakable schema on citable paragraphs (3), HowTo schema for process content (2), question-style H2s for direct-answer extraction (3), featured-snippet target structure (2).

**E-E-A-T (10 pts)** -- Author bio with credentials on page (3), author schema with knowsAbout + hasOccupation (2), specific proof points: numbers, named companies, dates (3), external links to authoritative sources (2).

### What the automated benchmark scores (crawl-observable proxies)

`tests/benchmark_sites.py` scores the 61-site leaderboard from a small set of
HTTP fetches (robots.txt, homepage, up to 3 deep pages, llms.txt, llms-full.txt).
It awards points only for what is observable from that crawl. The table below is
the exact benchmark scoring; it is pinned by `test_scoring_parity.py` against the
`BENCHMARK_CHECKS` table in the scorer.

| Bucket | Automated checks (points) | Max |
|--------|---------------------------|-----|
| Technical | robots.txt 200 (4), `Sitemap:` directive (3), canonical link (4), viewport meta (3), HTTPS (3), single H1 (3) | 20 |
| On-Page | title >=10 chars (3), meta description >=50 chars (3), og:image (3), og:title (2), twitter:card (2), H1 present (2) | 15 |
| Schema | any JSON-LD (5), Organization (5), Person (4), sameAs (3), dateModified (3) | 20 |
| GEO | llms.txt as text/plain (7), llms-full.txt as text/plain (5), AI crawler explicit-allows min(5,n) (5), homepage sameAs (5), citation-magnet regex (4), rel=llms-txt link (2), Link header (2) | 25 (checks sum to 30, clamped) |
| AEO | FAQPage (4), Speakable (3), question-style H2 (3) | 10 |
| E-E-A-T | author in schema (3), date in schema (3), meta author (2), knowsAbout/hasOccupation (2) | 10 |

**Manual-audit-only criteria (NOT scored by the automated benchmark)** because
they need a field-data API, a full-site crawl, validators, or off-site checks:
Core Web Vitals, broken-internal-link crawl, GSC submission status, primary-keyword
placement, descriptive-anchor internal links, BreadcrumbList coverage, schema
validation-error count, Wikidata-specific verification and cross-source entity
disambiguation, "comprehensive" judgment of llms.txt content, HowTo schema,
featured-snippet structure, proof-point density, and external authoritative links.

Two honest consequences: (1) the benchmark can reach a bucket's cap through
different routes than the manual rubric, so a benchmark score approximates rather
than reproduces a manual audit; (2) the GEO checks are over-subscribed (they sum
to 30 and clamp at 25), which over-weights llms.txt relative to its real-world
citation value. See `docs/proposals/scoring-reliability.md` for the planned
re-weighting.

### Multi-page sampling

The scorer can sample up to 3 deep pages discovered from the homepage (same-host links, preferring docs/blog/product/about) so a headline survives a re-crawl. On-Page, Schema, and AEO use best-of (max per dimension) across homepage plus those pages; Technical, GEO, and E-E-A-T stay homepage-derived. Budget is 4 page fetches per site, and every URL (including discovered links) passes the same SSRF public-host guard. Sampling is opt-in: pages=1 (default) keeps homepage-only scores; the benchmark runner uses pages=4.

## Score interpretation

| Score | Rating | Interpretation |
|-------|--------|----------------|
| 90-100 | Excellent | Top-tier machine-legibility; strong odds of AI citation |
| 75-89 | Good | Solid readiness with room to improve |
| 60-74 | Fair | Moderate readiness; meaningful gaps remain |
| 40-59 | Poor | Weak signals; AI systems struggle to cite or recommend |
| 0-39 | Critical | Largely invisible to AI systems |

## The modular geo-* skills are the engine, not a second scale

This project ships a monolith skill (`seo-geo.md`, single file) and a fleet of
modular `geo-*` skills (`geo-citability`, `geo-brand-mentions`, `geo-crawlers`,
`geo-llmstxt`, `geo-platform-optimizer`, `geo-technical`, `geo-content`,
`geo-schema`, and the `geo-audit` orchestrator). The modular skills are the
**engine** that produces the evidence behind each canonical bucket. They are not
a competing rubric. Earlier versions of the modular skills carried their own
category weights (Citability 25 / Brand 20 / E-E-A-T 20 / Technical 15 / Schema
10 / Platform 10). Those category labels stay useful as **work areas**, but the
**score** is always the canonical 100 above.

### Mapping note (conceptual crosswalk, not arithmetic)

The two partitions do not line up one-to-one, so there is **no conversion
formula**. A modular sub-score is not multiplied or rescaled into a canonical
bucket. To produce a canonical score you re-run the canonical checks; you do not
convert an old modular number. The crosswalk below shows where each modular work
area's concerns land in the canonical rubric.

| Modular work area (engine) | Canonical bucket(s) it feeds |
|----------------------------|------------------------------|
| AI Citability | GEO / LLM (core); answer-block quality also feeds AEO |
| Brand Authority | No standalone bucket. sameAs / entity presence feeds GEO; third-party trust signals feed E-E-A-T |
| Content E-E-A-T | E-E-A-T; content depth and keyword coverage also feed On-Page |
| Technical GEO | Technical SEO |
| Schema | Schema / Structured Data |
| Platform Optimization | AEO; platform readiness also informs GEO |

Two consequences worth stating plainly:

1. Modular **Brand Authority** and **Platform Optimization** have no dedicated
   canonical bucket. Their concerns are absorbed into GEO, E-E-A-T, and AEO.
2. Canonical **On-Page SEO** (15) and **AEO** (10) have no single modular source.
   On-Page is partly covered by the content engine; AEO is assembled from
   citability and platform work plus schema checks.

## Enforcement

`tests/test_scoring_parity.py` asserts:

- `seo-geo.md` Phase 0 bucket weights sum to 100.
- `tests/benchmark_sites.py` MAX_POINTS sums to 100.
- Phase 0 weights equal MAX_POINTS equal `{technical:20, onpage:15, schema:20, geo:25, aeo:10, eeat:10}`.
- The `BENCHMARK_CHECKS` table in `benchmark_sites.py` matches the "What the
  automated benchmark scores" table above (per-bucket observable maxima), so the
  documented benchmark behavior cannot silently drift from the scorer.

The parity test pins bucket totals and the benchmark check table; it does not
assert that every manual sub-check is implemented by the automated benchmark (it
cannot be: some manual criteria are not crawl-observable, see above). Any skill
that reports a score cites this rubric.
