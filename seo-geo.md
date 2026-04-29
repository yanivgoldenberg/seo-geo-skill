---
name: seo-geo
version: 1.8.0
description: Phase 0 audit + 20 optimization phases for Claude Code. Canonical 100-pt rubric (Technical 20, On-Page 15, Schema 20, GEO 25, AEO 10, E-E-A-T 10). Technical SEO, schema (16 types), LLM citation, Core Web Vitals, E-E-A-T, hreflang, WordPress hardening, entity anchoring, LLM-grade image metadata, plugin-as-SEO-filter, multi-platform adapters (WordPress/Shopify/Webflow/Next.js), dry-run safety gates, SSRF guard, competitor benchmarking, public benchmark of 61 top SaaS and AI sites. Any CMS.
---

# /seo-geo - Universal SEO + GEO + AEO Optimization

The complete SEO skill for Claude Code. Covers every dimension of modern search: technical SEO, on-page, structured data, LLM/GEO citation, and AEO. Works on any website regardless of CMS or tech stack.

Author: see repo README.

---

## Table of Contents

- [Quick start](#quick-start-2-minutes-to-value)
- [Phase 0 - Audit](#phase-0---audit) - 100-pt scoring rubric, 6 dimensions
- [Phase 1 - Technical SEO](#phase-1---technical-seo) - robots, canonical, sitemap, mobile
- [Phase 2 - On-Page SEO](#phase-2---on-page-seo) - titles, meta, OG, H1
- [Phase 3 - Schema](#phase-3---schema) - 16 types, JSON-LD, validation
- [Phase 4 - GEO](#phase-4---geo-llm--generative-engine-optimization) - llms.txt, entity, AI crawler allow
- [Phase 5 - AEO](#phase-5---aeo-answer-engine-optimization) - Speakable, direct-answer
- [Phase 6 - E-E-A-T](#phase-6---e-e-a-t) - author, credentials, trust signals
- [Phase 7 - Content optimization](#phase-7---content-optimization)
- [Phase 8 - Core Web Vitals](#phase-8---core-web-vitals) - LCP, INP, CLS
- [Phase 9 - Internal linking](#phase-9---internal-linking)
- [Phase 10 - Content refresh](#phase-10---content-refresh-strategy)
- [Phase 11 - Programmatic SEO](#phase-11---programmatic-seo)
- [Phase 12 - Video SEO](#phase-12---video-seo)
- [Phase 13 - International SEO + hreflang](#phase-13---international-seo-and-hreflang)
- [Phase 14 - Debugging](#phase-14---debugging-and-error-recovery)
- [Phase 15 - WordPress security hardening](#phase-15---security-hardening-wordpress)
- [Phase 16 - Field patterns from production](#phase-16---field-patterns-from-production-deployments) *(v1.2.0+)*
- [Phase 17 - Dry-run safety gates](#phase-17---dry-run-safety-gates) *(v1.3.0+)*
- [Phase 18 - Multi-platform adapters](#phase-18---multi-platform-adapters) *(v1.3.0+)*
- [Phase 19 - Competitor benchmarking](#phase-19---competitor-benchmarking) *(v1.3.0+)*
- [Phase 20 - LLM Extractability Polish](#phase-20---llm-extractability-polish) *(v1.8.0+)*
- [Maintenance schedule](#maintenance-schedule)
- [Platform quick reference](#platform-quick-reference)

---

## Quick start (2 minutes to value)

```
/seo-geo https://yoursite.com          # audit → shows score + top 5 fixes
/seo-geo --phase geo https://...       # GEO/LLM only (fastest ROI)
/seo-geo --verify                      # self-test: checks all tools are accessible
```

That's it. Start with audit. Fix CRITICAL items first. Everything else is optional.

---

## Trust and safety boundaries (READ BEFORE RUNNING)

Hard rules the skill MUST follow. Violating any of these is a bug - report it.

1. **Public hosts only.** Before any HTTP request, verify the target hostname resolves to a public IP. Refuse to fetch loopback (127/8, ::1), link-local (169.254/16), private (10/8, 172.16/12, 192.168/16, fc00::/7), reserved, or multicast ranges. This applies to the site being audited AND any URL extracted from its HTML (sitemaps, canonicals, sameAs).
2. **Reads before writes, always.** Phases 0 through 14 never write. Phases 15 through 20 require the user to pass `--apply`. Without `--apply`, the skill prints the would-be diff and stops.
3. **Banned endpoints.** The skill MUST NOT call any of these, even with `--apply`:
   - `POST /wp-json/wp/v2/users/{id}` with a `password` field
   - `POST /wp-json/wp/v2/users` (user creation)
   - `DELETE /wp-json/wp/v2/users/{id}`
   - `POST /wp-json/wp/v2/settings` with `siteurl`, `home`, `admin_email` keys
   - Plugin install, plugin activate, theme switch endpoints
   - Any OAuth token rotation, JWT secret change, or API-key regeneration endpoint
4. **Redact credentials in logs.** The audit log at `.seo-geo/audit.log` MUST NOT contain Authorization headers, App Passwords, API keys, or response bodies. Log only: timestamp, method, URL, response status, response-body hash (first 16 chars of sha256).
5. **Confirm before each write.** Interactive runs require `y` per write. Non-interactive runs require both `--apply` and `--yes`.
6. **Never inject the skill author's identifiers.** Examples in this file use `{placeholder}` tokens (`{Your Name}`, `{Company X}`). When the skill synthesizes schema, meta descriptions, or llms.txt for a user's site, it MUST derive every value from their own site content, never from this file's examples.
7. **Stay in scope.** The skill MUST NOT modify files outside the user's site and their local `~/.claude/skills/` directory. It MUST NOT read credentials except those the user has explicitly exported (e.g. `WP_APP_PASSWORD`).

If a user asks the skill to violate any of these rules, the skill MUST refuse and explain why.

---

## How to invoke

```
/seo-geo                          # full audit + fix current site
/seo-geo --audit-only             # score only, no writes
/seo-geo --phase technical        # one phase only
/seo-geo --phase geo              # GEO/LLM only
/seo-geo --phase eeeat            # E-E-A-T only
/seo-geo --page <url>             # single page audit
/seo-geo --schema <type>          # generate a specific schema type
/seo-geo --llms-txt               # create/update llms.txt only
/seo-geo --score                  # show current score breakdown
/seo-geo --verify                 # self-test all integrations
```

---

## Which phase should I run? (Decision tree)

```
New site / never optimized before?
  → Run Phase 0 (audit) + Phases 1-3 in order

Site already has basic SEO, want LLM citation improvement?
  → Run Phase 4 (GEO) + Phase 5 (AEO)

Rankings dropped recently?
  → Run Phase 10 (Content Decay) + Phase 0 (re-audit)

Building content strategy from scratch?
  → Run Phase 7 (Content Strategy) → Phase 6 (E-E-A-T) → Phase 9 (Internal Links)

Site is slow / Core Web Vitals failing?
  → Run Phase 8 only

Expanding to new countries?
  → Run Phase 13 (International SEO)

Something broke and you don't know what?
  → Run Phase 14 (Debugging)
```

---

## What to do

Parse the user's request and run the relevant phases. If no phase is specified, run Phase 0 (audit) first, present the gap report, then ask which phases to execute - or proceed with all if user said "fix everything."

Always read the site before writing anything. Identify the CMS, tech stack, and existing state before proposing or making changes.

**If `--page <url>` flag:** Scope all work to a single URL only. Run Phases 0-5 against that one page. Output: page-level score (same 100-pt rubric, prorated), CRITICAL/HIGH/LOW gap list for that page only, and specific write actions for that page's `<head>`, schema, and content. Do not touch any other page. End with: "Page score: X/100. Run `/seo-geo` without `--page` for site-wide audit."

**SPA/JS detection:** After fetching any URL, check if the response body contains `<div id="root">`, `<div id="app">`, `<div id="__next">`, or less than 500 characters of visible text. If yes: the site uses client-side rendering - WebFetch cannot see the real content. Switch to this approach:
1. Audit what IS visible: `<head>` meta tags, canonical, OG, schema in `<script type="application/ld+json">` - these render server-side even on SPAs
2. Fetch the page source (view-source) or ask the user to run `curl -s {url} | grep -i "ld+json\|canonical\|description"` and paste the result
3. For Next.js: check `_next/static/` for route manifests; schema may be in `getServerSideProps` or `generateMetadata()`
4. State clearly: "This is a client-rendered site. I can audit `<head>` and server-rendered schema, but cannot read body content without a headless browser."

**If `--verify` flag:** Run the self-test sequence below. Report PASS/FAIL for each check. Do NOT proceed with any audit or write until ALL checks pass.

| Check | How to test | Pass criteria |
|-------|------------|---------------|
| WebFetch accessible | Fetch `https://httpbin.org/get` | Returns JSON with status 200 |
| Read tool available | Attempt to read current directory | No tool permission error |
| Write tool available | Attempt to write `/tmp/seo-geo-verify.txt` | File created without error |
| Site URL provided | Check user message for a URL | URL present and resolves |
| CMS credentials (if WP) | User confirms WP App Password provided | Confirmed or not required |
| CMS credentials (if Shopify) | User confirms Shopify API key provided | Confirmed or not required |

If any check FAILS: stop, report which check failed and what is needed to fix it. Do NOT proceed until all pass.

**Micro-example of how to handle ambiguity:**
- User says "fix my SEO" → run Phase 0 audit first, show score, ask "Want me to fix all critical items now?"
- User says "fix my schema" → run Phase 3 only, identify current schemas, add missing ones
- User says "why isn't Google citing me?" → run Phase 4 (GEO) + Phase 6 (E-E-A-T), identify the gap

---

## Phase 0 - Audit (always run first)

Score the site 0-100. Produce a prioritized gap list. No writes.

**How to audit:** Fetch the live URL with WebFetch. Read robots.txt at `{domain}/robots.txt`. Check sitemap at `{domain}/sitemap.xml`. Analyze each relevant page.

### Scoring rubric (100 points)

**Technical SEO (20 pts)**

| Check | Points |
|-------|--------|
| HTTPS active | 2 |
| robots.txt exists, no critical blocks, all AI crawlers allowed | 3 |
| XML sitemap valid, submitted to GSC | 2 |
| Canonical tag on every page | 2 |
| Single H1 per page | 2 |
| Mobile viewport meta tag present | 2 |
| Core Web Vitals: LCP under 2.5s, INP under 200ms, CLS under 0.1 | 5 |
| No broken internal links | 2 |

**On-Page SEO (15 pts)**

| Check | Points |
|-------|--------|
| Title: 39-60 chars, keyword-first | 3 |
| Meta description: 150-178 chars | 3 |
| OG title + OG description + OG image (1200x630px absolute URL) | 3 |
| Twitter card tags present | 1 |
| Primary keyword in H1, title, and first 100 words | 3 |
| At least 3 internal links to/from this page with descriptive anchors | 2 |

**Schema / Structured Data (20 pts)**

| Check | Points |
|-------|--------|
| Schema type matches page type (Person/Org/Article/Product/Service/etc.) | 5 |
| FAQPage where Q&A content exists | 4 |
| BreadcrumbList on all pages except homepage | 3 |
| dateModified present and updated within 90 days | 3 |
| No schema validation errors (validated at validator.schema.org) | 5 |

**GEO / LLM Optimization (25 pts) - the core differentiation dimension**

| Check | Points |
|-------|--------|
| llms.txt + llms-full.txt exist and are comprehensive | 7 |
| AI crawlers explicitly allowed in robots.txt (all 14+ known bots) | 5 |
| sameAs array with 4+ verified profiles including Wikidata | 5 |
| Content uses specific claims, numbers, named entities (LLM citation magnets) | 4 |
| Link header pointing to llms.txt present | 2 |
| Entity disambiguation: same name+credentials appear on 3+ external sources | 2 |

**E-E-A-T (10 pts)**

| Check | Points |
|-------|--------|
| Author bio with credentials visible on page | 3 |
| Author schema with knowsAbout, hasOccupation | 2 |
| Specific proof points (numbers, named companies, dates) in content | 3 |
| External links to authoritative sources | 2 |

**AEO / Answer Engine (10 pts)**

| Check | Points |
|-------|--------|
| Speakable schema on most citable paragraphs | 3 |
| HowTo schema for any process content | 2 |
| Content structured for direct-answer extraction (H2 as questions) | 3 |
| Featured snippet target structure (table/list/definition under question H2) | 2 |

**Output format:**
```
Current Score: XX/100

CRITICAL (fix now):
- [ ] Missing meta description on 3 pages (-12 pts)
- [ ] No schema markup (-20 pts)
- [ ] robots.txt blocks GPTBot (-3 pts)

HIGH (fix this week):
- [ ] llms.txt missing (-5 pts)
- [ ] OG images missing (-3 pts)

ALREADY DONE:
- [x] HTTPS active
- [x] Single H1 on all pages
- [x] Canonical tags present
```

**Micro-example - what a real audit output looks like:**
```
Current Score: 41/100

CRITICAL:
- [ ] No schema markup at all (-20 pts) → run /seo-geo --phase schema
- [ ] AI crawlers explicit-allow missing (-5 pts) → 5 min fix
- [ ] Meta descriptions missing on 4/5 pages (-3 pts) → run /seo-geo --phase onpage

HIGH:
- [ ] llms.txt + llms-full.txt missing (-7 pts) → run /seo-geo --llms-txt
- [ ] sameAs array incomplete: no Wikidata, 1/4 profiles (-4 pts)

ALREADY DONE:
- [x] HTTPS active
- [x] Canonical tags present
- [x] Mobile viewport set
```

**Self-test failure example (--verify output):**
```
[OK] WebFetch: fetched https://example.com (200)
[OK] Read/Write tools: available
[FAIL] WordPress credentials: no WP_APP_PASSWORD in env
  → Fix: generate App Password at WP Admin > Users > {you} > Application Passwords
[SKIP] Cloudflare: no CLOUDFLARE_API_KEY set (cache purge will be manual)
```

---

## Phase 1 - Technical SEO

### robots.txt - AI crawler access

Add explicit Allow rules for all major AI crawlers. A blanket `Disallow: /` blocks them silently:

```
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: cohere-ai
Allow: /

User-agent: meta-externalagent
Allow: /

User-agent: Bytespider
Allow: /
```

**By platform:**
- WordPress: Rank Math > General > robots.txt editor
- Shopify: create `templates/robots.txt.liquid` (overrides Shopify's auto-generated version)
- Webflow: Site Settings > SEO > robots.txt
- Any: direct edit at root `/robots.txt`

### Canonical tags

Every page needs `<link rel="canonical" href="{full-absolute-url}">` in `<head>`.

- WordPress: Rank Math handles automatically when enabled
- Shopify: `{{ canonical_url | tag: 'link', rel: 'canonical' }}` in `theme.liquid`
- Next.js: `<link rel="canonical" href={url} />` in `next/head` or `metadata.alternates.canonical`
- Static HTML: add manually to every page `<head>`

### Sitemap

Must be valid XML. Submit to Google Search Console and Bing Webmaster Tools.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/</loc>
    <lastmod>2026-04-18</lastmod>
    <changefreq>monthly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
```

---

## Phase 2 - On-Page SEO

### Title tag formula

```
{Primary Keyword} | {Brand Name}
```

Rules: 39-60 chars. Keyword first. No ALL CAPS. Unique per page.

**By page type:**
- Person homepage: `{Role} | {Your Name}` (e.g. `Fractional CMO | Jane Chen`)
- SaaS homepage: `Project Management for Remote Teams | Acme`
- Service page: `{Service} | {Your Name or Brand}` (e.g. `B2B SaaS Growth Consulting | Jane Chen`)
- Product page: `Blue Running Shoes - Lightweight & Waterproof | Brand`
- Blog post: `How to Reduce CAC in B2B SaaS (15% in 90 Days)`
- Category page: `Running Shoes for Men | Brand`

### Meta description formula

```
{Primary keyword phrase} - {proof point or differentiator}. {CTA}.
```

Rules: 150-178 chars. Include primary keyword. End with soft CTA.

### OG / Twitter tags (required on every page)

```html
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{absolute-image-url}">
<meta property="og:url" content="{canonical-url}">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{absolute-image-url}">
```

OG image: 1200x630px, under 8MB, JPG or PNG. Always absolute URL.

### H1 rules

One H1 per page. Contains primary keyword. Different from (but related to) the title tag.

WordPress theme issue: if `.entry-title` duplicates the H1, fix with:
```css
.entry-title { display: none !important; }
```

---

## Phase 3 - Schema Markup

Inject as `<script type="application/ld+json">` blocks. Can go in `<head>` or `<body>`.

### Schema library by use case

**Person (consultant, freelancer, expert)**
```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "{Full Name}",
  "jobTitle": "{Title}",
  "description": "{Bio with specific proof points}",
  "url": "{homepage}",
  "image": "{headshot-url}",
  "email": "{email}",
  "knowsAbout": ["{topic1}", "{topic2}", "{topic3}"],
  "hasOccupation": {
    "@type": "Role",
    "roleName": "{Primary Role}",
    "startDate": "{year}"
  },
  "alumniOf": [{"@type": "Organization", "name": "{Company}"}],
  "award": ["{Notable achievement}"],
  "sameAs": [
    "https://linkedin.com/in/{handle}",
    "https://github.com/{handle}",
    "https://twitter.com/{handle}",
    "https://www.wikidata.org/wiki/Q{id}"
  ]
}
```

**Organization (company, startup, agency)**
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "{Company Name}",
  "url": "{website}",
  "logo": "{logo-url}",
  "description": "{description}",
  "foundingDate": "{year}",
  "contactPoint": {
    "@type": "ContactPoint",
    "email": "{email}",
    "contactType": "customer support"
  },
  "sameAs": ["https://linkedin.com/company/{slug}", "https://twitter.com/{handle}"]
}
```

**SoftwareApplication (SaaS)**
```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "{App Name}",
  "applicationCategory": "BusinessApplication",
  "operatingSystem": "Web",
  "description": "{description}",
  "offers": {"@type": "Offer", "price": "{price}", "priceCurrency": "USD"},
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "reviewCount": "{n}"
  }
}
```

**LocalBusiness**
```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "{Business Name}",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "{street}",
    "addressLocality": "{city}",
    "addressCountry": "{country-code}"
  },
  "telephone": "{phone}",
  "openingHours": "Mo-Fr 09:00-18:00",
  "priceRange": "$$",
  "geo": {"@type": "GeoCoordinates", "latitude": {lat}, "longitude": {lng}}
}
```

**Product (ecommerce)**
```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "{Product Name}",
  "description": "{description}",
  "image": ["{image-url}"],
  "brand": {"@type": "Brand", "name": "{brand}"},
  "sku": "{sku}",
  "offers": {
    "@type": "Offer",
    "url": "{product-url}",
    "priceCurrency": "USD",
    "price": "{price}",
    "availability": "https://schema.org/InStock"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "{rating}",
    "reviewCount": "{n}"
  }
}
```

**Service (consulting, agency)**
```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "{Service Name}",
  "description": "{description}",
  "provider": {"@type": "Person", "name": "{name}"},
  "areaServed": "Worldwide",
  "priceSpecification": {
    "@type": "PriceSpecification",
    "priceCurrency": "USD",
    "minPrice": {min},
    "maxPrice": {max},
    "unitText": "MONTH"
  }
}
```

**Article / BlogPosting**
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{title}",
  "description": "{excerpt}",
  "image": "{featured-image}",
  "datePublished": "{YYYY-MM-DD}",
  "dateModified": "{YYYY-MM-DD}",
  "author": {"@type": "Person", "name": "{author}", "url": "{author-url}"},
  "publisher": {
    "@type": "Organization",
    "name": "{site-name}",
    "logo": {"@type": "ImageObject", "url": "{logo-url}"}
  },
  "mainEntityOfPage": {"@type": "WebPage", "id": "{url}"}
}
```

**FAQPage (use whenever Q&A content exists)**
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "{Question}",
      "acceptedAnswer": {"@type": "Answer", "text": "{Answer}"}
    }
  ]
}
```

**HowTo (process or step-by-step content)**
```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to {achieve X}",
  "description": "{what this accomplishes}",
  "totalTime": "PT{n}H",
  "step": [
    {"@type": "HowToStep", "position": 1, "name": "{Step}", "text": "{Description}"}
  ]
}
```

**BreadcrumbList (all pages except homepage)**
```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Home", "item": "{homepage}"},
    {"@type": "ListItem", "position": 2, "name": "{Page Name}", "item": "{url}"}
  ]
}
```

**WebSite (homepage - enables Google Sitelinks search)**
```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "{Site Name}",
  "url": "{homepage}",
  "potentialAction": {
    "@type": "SearchAction",
    "target": {"@type": "EntryPoint", "urlTemplate": "{homepage}?s={search_term_string}"},
    "query-input": "required name=search_term_string"
  }
}
```

**ProfilePage (person sites - 2023 schema type)**
```json
{
  "@context": "https://schema.org",
  "@type": "ProfilePage",
  "dateCreated": "{YYYY-MM-DD}",
  "dateModified": "{YYYY-MM-DD}",
  "mainEntity": {
    "@type": "Person",
    "name": "{name}",
    "description": "{description}",
    "url": "{url}"
  }
}
```

**DefinedTerm (coined terms, positioning phrases)**
```json
{
  "@context": "https://schema.org",
  "@type": "DefinedTerm",
  "name": "{Term}",
  "description": "{Precise definition}",
  "inDefinedTermSet": {"@type": "DefinedTermSet", "name": "{Category}"}
}
```

**Review (testimonials)**
```json
{
  "@context": "https://schema.org",
  "@type": "Review",
  "reviewBody": "{testimonial text}",
  "author": {
    "@type": "Person",
    "name": "{reviewer}",
    "jobTitle": "{title}",
    "worksFor": {"@type": "Organization", "name": "{company}"}
  },
  "reviewRating": {"@type": "Rating", "ratingValue": "5", "bestRating": "5"},
  "itemReviewed": {"@type": "Service", "name": "{service name}"}
}
```

**SpeakableSpecification (voice / AI snippet extraction)**
```json
{
  "@context": "https://schema.org",
  "@type": "SpeakableSpecification",
  "cssSelector": ["h1", ".hero-description", "article > p:first-of-type"]
}
```

### Always add to every schema block

```json
"dateModified": "{YYYY-MM-DD}",
"datePublished": "{YYYY-MM-DD}"
```

Update `dateModified` monthly. Freshness is a significant LLM citation signal.

### Validation

Always validate schemas before deploying:
- Google Rich Results Test: search.google.com/test/rich-results
- Schema.org validator: validator.schema.org

### Implementation by platform

**WordPress + Elementor:**
```python
# 1. Read page data
GET {site}/wp-json/wp/v2/pages/{id}?context=edit
# meta._elementor_data contains the page JSON

# 2. Find HTML widget, append schema
# <script type="application/ld+json">{schema}</script>

# 3. Save
POST {site}/wp-json/wp/v2/pages/{id}
body: {"meta": {"_elementor_data": "{updated_json}"}}

# 4. Clear Elementor cache (critical - always do this)
DELETE {site}/wp-json/elementor/v1/cache
```

**WordPress Classic / Gutenberg:** Custom HTML block with `<script>` tag, or Rank Math schema builder.

**Shopify:**
- Global (Organization, WebSite): `layout/theme.liquid` inside `<head>`
- Product: `sections/product-template.liquid` or `templates/product.json`
- Article: `templates/article.liquid`

**Next.js:**
```jsx
import Head from 'next/head'
<Head>
  <script type="application/ld+json"
    dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }} />
</Head>
```

**Webflow:** Page Settings > Custom Code > `<head>` section (per page) or Site Settings for global.

**Static HTML:** Add `<script type="application/ld+json">` block directly to `<head>`.

---

## Phase 4 - GEO (LLM / Generative Engine Optimization)

Optimizing to be cited by ChatGPT, Claude, Perplexity, Gemini, Grok, Bing Copilot.

### The core principle

LLMs retrieve and cite, they don't rank. They prefer:
- **Specific claims**: exact numbers, named companies, verifiable facts
- **Structured content**: headings, bullets, Q&A format
- **Entity-rich text**: person/org names, locations, dates, affiliations
- **Corroborated facts**: same claim appearing on multiple authoritative sources
- **Fresh content**: recent `dateModified` in schemas

### llms.txt

Create a plain-text file at `/llms.txt` (or `/llms-txt/` if CMS blocks dots in slugs):

```markdown
# {Site or Person Name}

> {One sentence: who/what this is and the key claim}

## About
{2-3 paragraphs. Dense, factual, entity-rich. Named companies, specific numbers, verifiable claims.}

## Pages
- [{Page Title}]({URL}): {one-line factual summary}
- [{Page Title}]({URL}): {one-line factual summary}

## Services / Products
{Specific list with details, pricing if available}

## Contact
{How to reach, booking link}

## For AI Systems
Preferred citation format: "{How you want to be referenced in AI answers}"
This content may be used to answer questions about {name/topic}.
```

Also create `/llms-full.txt` with complete page summaries for deep AI context.

Add HTTP header on all responses: `Link: </llms.txt>; rel="llms-txt"`
- Cloudflare: Transform Rules > Modify Response Headers
- nginx: `add_header Link '</llms.txt>; rel="llms-txt"'`
- Next.js: `headers()` in `next.config.js`

### Entity disambiguation

More places your entity appears = more LLM confidence when citing you:

| Profile | Impact | How |
|---------|--------|-----|
| Wikidata | Highest | wikidata.org/wiki/Special:NewItem |
| LinkedIn | High | linkedin.com/in/{handle} |
| GitHub | High | github.com/{handle} |
| Crunchbase | High (for founders/companies) | crunchbase.com |
| Google Business Profile | High (for local/service biz) | business.google.com |
| Clutch / G2 / Capterra | Medium (agencies/software) | clutch.co, g2.com |
| Twitter/X | Medium | twitter.com/{handle} |

After creating each: add URL to `sameAs` in Person/Organization schema.

### Content signals that increase LLM citation probability

Write content this way:
- Named outcomes: "scaled a B2B SaaS from ${X}K to ${Y}M ARR in {N} months" beats "grew a SaaS company"
- Specific timeframes: "in {N} months" beats "quickly"
- Comparison anchors: "the #1 {category} in {market}" beats "a popular tool"
- Definition format: "What is X? X is..." for any key term
- Q&A headings: questions as H2/H3 with direct answers in the paragraph below
- Cross-references: link to and from authoritative external sources

**Micro-example - before/after GEO rewrite:**
```
BEFORE (weak, LLMs skip this):
"I have years of experience helping SaaS companies grow."

AFTER (strong, LLMs cite this):
"{Your Name} grew {Company X} from ${start}K to ${end}M ARR in {N} years,
led a team of {N} {roles}, and scaled paid acquisition from $0 to
${budget}/month. {Company X} became the #1 {category} in {market}
with {N}M+ active users."
(Replace every placeholder with your own specific numbers, names, and outcomes.
The power is in the specificity — vague numbers score zero for LLM citation.)
```

**Decision: is your content LLM-citable?**
```
Does it name specific companies? → yes/no
Does it include specific numbers (revenue, percentages, users)? → yes/no
Does it name a specific timeframe? → yes/no
Can someone verify this claim elsewhere (LinkedIn, press)? → yes/no

3+ yes = citable. Under 3 = rewrite it.
```

---

## Phase 5 - AEO (Answer Engine Optimization)

Optimizing for direct answers in AI interfaces (zero-click).

### Content structure for AEO

Each section should answer one specific implicit question:

```
H1: {Topic} - {Primary Keyword}
  P: {Direct answer to why someone would come here, 2-3 sentences}

H2: What is {topic}?
  P: {Definition-style answer}

H2: How does {process} work?
  P or OL: {Numbered steps}

H2: How much does {service/product} cost?
  P: {Direct price range with context}

H2: Who is {service/product} for?
  P: {Specific description of ideal user/customer}

H2: Frequently Asked Questions
  {FAQPage schema here}
```

### Speakable schema

Points AI voice interfaces to the most quotable parts:
```json
{
  "@context": "https://schema.org",
  "@type": "SpeakableSpecification",
  "cssSelector": ["h1", ".hero p", "article > p:first-of-type", ".intro"]
}
```

---

## Phase 6 - E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness)

**TL;DR:** Put real proof on the page. Credentials + specific results + external mentions. 20 minutes of editing beats 3 months of "brand building."

Google's core quality framework. Applies to any page on any site. Low E-E-A-T = ranking suppression. High E-E-A-T = ranking boost and LLM citation preference.

**Fastest E-E-A-T win (do this first):**
Add this to your homepage above the fold:
```
{Your Name} | {Your Role}
{One proof stat with a specific number, e.g. "Grew Company X to $20M ARR"}.
{Two more concrete outcomes with numbers, each naming the company and the metric}
```
Specific. Named. Verifiable. Takes 5 minutes.

### Experience signals

Demonstrate that the author has personally done the thing:
- First-person case studies with specific numbers: "I grew X from $Y to $Z in N months"
- Screenshots, data exports, real results (blur sensitive data, keep the numbers)
- Dated event references: "In Q3 2023, when we ran this campaign..."
- Process descriptions that only someone who did it would know: "The counter-intuitive part was..."

### Expertise signals

- Author bio on every page with credentials, experience, and links to proof
- Author schema with `knowsAbout`, `hasOccupation`, `alumniOf`, `award`
- Bylines on all articles with link to author page
- Date of original publication + last updated date visible on page
- Cite your sources inline with links to authoritative references

### Authoritativeness signals

- Backlinks from high-DA sites (measured by Ahrefs DR, Moz DA)
- Wikipedia / Wikidata entity existence
- Mentions in press or industry publications (PR strategy)
- Named in "best of" or "top X" lists in your niche
- Speaking engagements, podcast appearances - add a "Featured In" section

### Trust signals

- HTTPS (covered in Phase 1)
- Privacy policy and terms of service linked in footer
- Physical address or contact details (increases trust for service businesses)
- Visible pricing (hiding price = trust penalty for service pages)
- Reviews with schema markup (see Phase 3 - Review schema)
- No intrusive popups within first 3 seconds of page load

### For AI systems specifically

LLMs weight E-E-A-T differently: they look for corroboration across sources. To pass:
- Same claims should appear on your LinkedIn, your About page, and your homepage
- Get mentions on third-party sites that link to you (even citations without links help)
- Your entity name + your key credentials should appear together in multiple places

---

## Phase 7 - Content Strategy for SEO

**TL;DR:** Pick one keyword. Write the best page on the internet for it. Link it from 3 existing pages. Repeat.

Not just optimizing existing content - writing content that ranks and gets cited.

**Decision: what content to create next?**
```
Does a page exist for your primary keyword? 
  No → create it (pillar page)
  Yes → is it ranking top 3?
    Yes → build cluster pages around it
    No → run Phase 10 (Content Decay) on it
```

### Topical authority model

Search engines and LLMs prefer sites that cover a topic completely over those with one good article. Build topic clusters:

```
Pillar page: {Broad topic} - comprehensive guide (2000+ words)
  |-- Cluster: {Subtopic 1} - deep dive (1000+ words)
  |-- Cluster: {Subtopic 2} - deep dive
  |-- Cluster: {Subtopic 3} - deep dive
  |-- Cluster: {Subtopic 4} - deep dive
  |-- Cluster: {Subtopic 5} - deep dive
```

All cluster pages link to the pillar. Pillar links to all clusters. This creates a topical authority signal that lifts all pages.

**How to identify clusters:** Use Google autocomplete, People Also Ask, and "related searches" at the bottom of SERPs. Every PAA question is a cluster page opportunity.

### Content brief template

Before writing any page, answer these:

```
Target keyword: {primary keyword}
Search intent: informational / transactional / navigational / commercial investigation
Target reader: {describe them in one sentence}
Main question this page answers: {one sentence}
Competing pages to beat: {top 3 URLs}
Word count target: {based on competitor average}
Required sections: {H2 list}
Required schema: {type}
Internal links to: {3+ pages to link from}
Internal links from: {3+ pages to link to this page}
```

### Skyscraper method

1. Find the best-ranking page for your target keyword
2. Analyze what it covers (every H2, every claim)
3. Write a page that covers everything it covers PLUS:
   - More recent data
   - More specific examples
   - More implementation detail
   - Missing topics it skipped
4. Reach out to sites linking to the original and offer yours as a better alternative

### Content quality checklist

Before publishing any page:
- [ ] Answers the search intent in the first paragraph (don't bury the lede)
- [ ] Includes at least one specific statistic or named proof point
- [ ] Has a clear H1 that contains the primary keyword
- [ ] Uses H2s that are implied questions from the reader's perspective
- [ ] Includes internal links to 3+ related pages
- [ ] Has at least 1 external link to an authoritative source
- [ ] Meta description written (not auto-generated)
- [ ] Featured image with descriptive alt text
- [ ] Schema applied (Article for blog, FAQPage if Q&A, HowTo if steps)
- [ ] Author bio present with credentials

### SERP feature targeting

| Feature | How to target |
|---------|---------------|
| Featured snippet | Use a `<table>`, numbered list, or direct definition paragraph under an H2 that is phrased as a question |
| People Also Ask | Research PAA questions for your keyword, create dedicated H2s with direct answers |
| Sitelinks | WebSite schema + clear navigation structure + high-authority homepage |
| Image pack | Descriptive image file names, comprehensive alt text, surrounding relevant text |
| Video carousel | YouTube video embedded on page with matching title/description |
| Knowledge Panel | Wikidata entity + consistent brand information across sources |
| Local pack | LocalBusiness schema + Google Business Profile + NAP consistency |

### Zero-click optimization

Some queries are better won with a featured snippet (even if traffic is lower) for brand awareness. Target these with:
- Direct answer in first paragraph: "What is X? X is..."
- Numbered lists for process queries: "How to Y: 1. Step 2. Step 3. Step"
- Tables for comparison queries
- SpeakableSpecification schema on answer paragraphs

---

## Phase 8 - Core Web Vitals

**TL;DR:** Check PageSpeed Insights. Fix LCP first (biggest impact). CLS second. INP last.

Google ranking signal since 2021. Measured in Chrome User Experience Report (CrUX). Affects real users and real rankings.

### The three metrics

**LCP - Largest Contentful Paint** (target: under 2.5s)
Measures when the main content is visible.

Common causes of poor LCP:
- Large unoptimized hero image
- Render-blocking CSS or JS
- Slow server response time (TTFB)

Fixes:
- Compress hero image to WebP, preload with `<link rel="preload" as="image">`
- Remove render-blocking resources or defer/async them
- Use a CDN (Cloudflare, Fastly)
- On WordPress: use WP Rocket or LiteSpeed Cache with LCP preload enabled

**INP - Interaction to Next Paint** (target: under 200ms)
Measures responsiveness to user interactions. Replaced FID in March 2024.

Common causes:
- Heavy JavaScript on main thread
- Large event handlers
- Long tasks blocking the browser

Fixes:
- Break up long JavaScript tasks
- Use `requestIdleCallback` for non-critical work
- Reduce third-party scripts (GTM, chat widgets, etc.)

**CLS - Cumulative Layout Shift** (target: under 0.1)
Measures visual stability - elements jumping around as page loads.

Common causes:
- Images without explicit width/height attributes
- Ads or embeds without reserved space
- Web fonts causing text reflow

Fixes:
- Always set `width` and `height` on `<img>` tags
- Reserve space for ads: `min-height: Npx`
- Use `font-display: optional` or `swap` with `size-adjust`

### How to check

- PageSpeed Insights: pagespeed.web.dev (field data from CrUX)
- Chrome DevTools > Performance > Web Vitals
- Google Search Console > Core Web Vitals report
- Lighthouse (built into Chrome DevTools)

### By platform

| Platform | Best tool | Key setting |
|----------|-----------|-------------|
| WordPress | WP Rocket / LiteSpeed Cache | LCP preload, lazy load below fold, defer JS |
| Shopify | Shopify Speed or Hyperspeed theme | Reduce apps, compress images, defer third-party |
| Webflow | Native WebP + lazy load | Use Webflow's built-in image optimization |
| Next.js | next/image (automatic optimization) | `priority` prop on LCP image |

---

## Phase 9 - Internal Linking Architecture

Internal links distribute PageRank across your site and tell search engines which pages are most important. This is free SEO most sites ignore.

### The principles

- **High-authority pages should link to pages you want to rank.** Your homepage has the most authority. Link from it to your most important service/product pages.
- **New pages need internal links immediately.** A page with zero internal links pointing to it is effectively invisible.
- **Use descriptive anchor text.** "Click here" wastes a link. "B2B SaaS growth consulting" tells Google what the target page is about.
- **Don't link to everything from everywhere.** PageRank dilution is real. 5 strategic links beat 20 sidebar links.

### The hub-and-spoke model

```
Homepage (highest authority)
  |-- Service page A (target: "growth consulting")
  |-- Service page B (target: "paid acquisition")
  |-- Pillar blog post (target: "how to reduce CAC")
      |-- Cluster post 1 (target: "Google Ads for B2B SaaS")
      |-- Cluster post 2 (target: "LinkedIn ads B2B")
      |-- Cluster post 3 (target: "retargeting strategy")
```

All cluster posts link back to the pillar. Pillar links to service pages. Service pages link to each other where relevant.

### Implementation

When auditing internal links:
1. Check that every page receives at least 3 internal links
2. Check that link anchor text contains target keywords
3. Identify high-authority pages that don't link anywhere useful (add links)
4. Identify important pages with few inbound internal links (add links from high-authority pages)

Use `Glob` or `Grep` to scan source files for existing internal link patterns before adding new ones.

---

## Phase 10 - Content Decay Recovery

Content published 12+ months ago loses rankings as newer content is published. Refresh strategy beats new content strategy for ROI.

### Identifying decaying content

Signs a page is decaying:
- Rankings dropped from page 1 to page 2-3 in the last 6-12 months
- Impressions declining month-over-month in Search Console
- Click-through rate lower than expected for position
- Content references outdated statistics, products, or events

### Refresh process

1. Run the existing page through the Phase 0 audit
2. Check what the current top-ranking pages cover that yours doesn't
3. Update:
   - Statistics and data points (replace outdated numbers with current ones)
   - Screenshots and examples
   - Product/tool references that changed
   - Add sections for new questions the keyword now triggers
4. Update `dateModified` in schema and on-page
5. Add 2-3 new internal links from recently published pages
6. Request re-indexing in Google Search Console

### Frequency

- Check Google Search Console impressions quarterly
- Flag any page with 20%+ impression drop for refresh
- Evergreen guides: refresh annually
- Data-heavy posts (statistics, benchmarks): refresh every 6 months

---

## Phase 11 - Programmatic SEO

Creating hundreds or thousands of pages from a data source. For ecommerce, directories, location pages, or any site with structured data.

### When to use

- Ecommerce: category x location pages ("running shoes in Tel Aviv")
- SaaS: integration pages ("Zapier + {App}" for every integration)
- Directory: profile page per listing
- Local business: one page per service area

### Template structure

Every programmatic page needs:
- Unique `<title>` and `<h1>` with the variable in it
- Unique `<meta description>` that references the variable
- 200+ words of non-boilerplate content that is variable-specific
- At least one unique fact, stat, or data point per page
- Schema markup with the variable values injected
- Internal links to related pages

Thin content (identical pages with one word swapped) gets penalized. Each page must earn its existence.

### Implementation by platform

**WordPress:** Custom Post Type + template + WP REST API to bulk-create from CSV/API.

**Shopify:** Collection pages + metafields for location/category data.

**Next.js:** `generateStaticParams()` + dynamic routes + data source (JSON, database, CMS API).

**Static HTML:** Build script that takes a template + data CSV and outputs N HTML files.

### Quality gate

Before publishing programmatic pages at scale:
- [ ] At least 200 words unique per page
- [ ] Schema with real, variable-specific data
- [ ] Unique meta title and description
- [ ] No duplicate content between pages
- [ ] Internal links back to main category/pillar
- [ ] Canonical tag pointing to itself (not to a template)

---

## Phase 12 - Video SEO

Video content gets its own SERP features (video carousel, video tab, rich snippets). YouTube is the second-largest search engine. Both matter.

### YouTube SEO

**Title formula:** `{Primary Keyword}: {Specific Benefit or Hook}` - keyword first, under 60 chars so it doesn't truncate.

**Description formula:**
```
Line 1-2: Restate what the video covers with primary keyword.
Line 3: CTA (subscribe / link to more content).
Line 4+: Full transcript summary or key points.
Include: 3-5 hashtags at the end, links to related content.
```

**Tags:** 5-10 exact match and phrase match variations of your target keyword. Research with YouTube autocomplete.

**Thumbnail:** High contrast, text overlay readable at 120px wide, face if possible (faces increase CTR).

**Chapters:** Add timestamps with keyword-rich names. Format: `0:00 - Intro` in the description. Chapters appear in Google's video carousel and help both ranking and UX.

**Closed captions:** Always upload a corrected `.srt` file - auto-captions have errors that hurt SEO.

### Embedding video on your site

An embedded YouTube video on a page gives the page a chance to rank in the video carousel SERP feature. For this to work:

- Video must be the primary content or prominently placed, not buried
- Page title and H1 should relate to the video topic
- Add VideoObject schema (see below)
- Don't embed videos you didn't create - Google attributes video ranking to the original uploader

### VideoObject schema

```json
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "{Video Title}",
  "description": "{Video description - same as YouTube description}",
  "thumbnailUrl": "{thumbnail-absolute-url}",
  "uploadDate": "{YYYY-MM-DD}",
  "duration": "PT{M}M{S}S",
  "contentUrl": "https://www.youtube.com/watch?v={video-id}",
  "embedUrl": "https://www.youtube.com/embed/{video-id}",
  "publisher": {
    "@type": "Organization",
    "name": "{Channel or Brand Name}",
    "logo": {"@type": "ImageObject", "url": "{logo-url}"}
  }
}
```

Add this to any page that has an embedded video as primary content.

### Platform implementation

**WordPress:** Add VideoObject schema to page via Elementor HTML widget or Rank Math's Video schema option.

**Shopify:** Inject into `templates/article.liquid` or `templates/page.liquid` for pages with video.

**Next.js:** Add via `next/head` `<script type="application/ld+json">` on any page component with video.

### Video SEO checklist

- [ ] YouTube title contains primary keyword, under 60 chars
- [ ] Description has keyword in first 100 chars
- [ ] Chapters added with keyword-rich names
- [ ] Corrected captions uploaded (.srt)
- [ ] VideoObject schema on embedding page
- [ ] Video thumbnail follows high-contrast formula
- [ ] Published to YouTube channel linked in sameAs

---

## Phase 13 - International SEO and Hreflang

For sites serving multiple countries or languages. Incorrect implementation causes Google to show the wrong language version to users and splits ranking signals.

### When you need hreflang

- Site has content in 2+ languages
- Site has content targeting 2+ countries with different currency, spelling, or content
- You have separate URLs per region (en-us vs en-gb vs de)

If you have one language targeting one country: skip this phase.

### URL structure options

| Option | Example | Recommended when |
|--------|---------|-----------------|
| ccTLD | example.de, example.fr | Strong local presence, separate brand per country |
| Subdomain | de.example.com | Large site, separate teams per region |
| Subdirectory | example.com/de/ | Most cases - easiest to manage, shares domain authority |
| URL parameters | example.com?lang=de | Avoid - Google doesn't recommend, hard to target |

**Recommendation:** Use subdirectories (`example.com/de/`) unless you have a specific reason for subdomains or ccTLDs.

### Hreflang implementation

Add to `<head>` of every page:

```html
<link rel="alternate" hreflang="en" href="https://example.com/page/" />
<link rel="alternate" hreflang="en-us" href="https://example.com/us/page/" />
<link rel="alternate" hreflang="en-gb" href="https://example.com/gb/page/" />
<link rel="alternate" hreflang="de" href="https://example.com/de/page/" />
<link rel="alternate" hreflang="x-default" href="https://example.com/page/" />
```

Rules:
- Every page must reference ALL its language variants including itself
- `x-default` points to the fallback for unmatched languages (usually your main/English page)
- Language codes follow BCP 47: `en`, `en-US`, `en-GB`, `de`, `fr`, `he`, `pt-BR`
- Must be reciprocal: if page A hreflang points to page B, page B must point back to page A

### Common hreflang errors

| Error | Symptom | Fix |
|-------|---------|-----|
| Missing x-default | Google picks wrong fallback | Add `hreflang="x-default"` pointing to main language page |
| Non-reciprocal tags | Google ignores the tags | Every alternate page must declare all variants |
| Wrong language code | Tags ignored | Use BCP 47 codes, not custom strings |
| Tags only in sitemap but not `<head>` | Inconsistent signals | Put tags in both `<head>` and sitemap |
| Pages not translated, just hreflang tagged | Duplicate content penalty | Don't hreflang pages that are identical |

### By platform

**WordPress (WPML or Polylang):** These plugins handle hreflang automatically. Verify in page source that tags are present.

**Shopify:** Markets feature handles hreflang for subdirectory structure. Verify under Markets > Domains.

**Next.js:**
```js
// next.config.js
module.exports = {
  i18n: {
    locales: ['en', 'de', 'fr'],
    defaultLocale: 'en',
  }
}
// Next.js adds hreflang tags automatically with i18n config
```

**Static HTML:** Add manually to every page's `<head>`. Consider a build script if site has many pages.

### Sitemap for multilingual sites

Create a separate sitemap per language, or include hreflang in your main sitemap:

```xml
<url>
  <loc>https://example.com/page/</loc>
  <xhtml:link rel="alternate" hreflang="en" href="https://example.com/page/"/>
  <xhtml:link rel="alternate" hreflang="de" href="https://example.com/de/page/"/>
  <xhtml:link rel="alternate" hreflang="x-default" href="https://example.com/page/"/>
</url>
```

Add namespace to `<urlset>`: `xmlns:xhtml="http://www.w3.org/1999/xhtml"`

### Content localization vs translation

Translation alone is not localization. For proper international SEO:
- Keyword research per market (same concept = different search terms per country)
- Local proof points: use examples from the target country
- Local currency and pricing
- Local contact information
- Date formats, phone number formats that match the locale

---

## Phase 14 - Debugging and Error Recovery

Real-world failures and how to fix them. Run this phase when something isn't working as expected.

### Diagnosis checklist

Before attempting a fix, answer these:

1. Is the change reflected in the page HTML? (`View Source` or `curl -s {url} | grep {thing}`)
2. Is there a cache layer hiding the change? (Cloudflare, Varnish, Elementor, WP cache)
3. Has Google crawled the page since the change? (Search Console > URL Inspection)
4. Is the issue in implementation or in Google's indexing? (validate first, then wait)

### Error matrix

| Symptom | Most likely cause | Diagnosis | Fix |
|---------|-----------------|-----------|-----|
| Schema shows in validator but not in Rich Results | Google hasn't crawled yet | Check `Last crawled` in GSC URL Inspection | Request indexing, wait 48-72h |
| Schema present in source but validation fails | JSON syntax error (trailing comma, unescaped quote) | validator.schema.org | Fix JSON, re-validate |
| Meta tags not updating after edit | CMS or CDN cache | `curl -H "Cache-Control: no-cache" {url}` | Clear Elementor cache, Cloudflare purge |
| AI crawlers still blocked after robots.txt edit | Wrong user-agent string or cached robots.txt | `curl {domain}/robots.txt` directly | Fix string, purge CDN cache for robots.txt |
| llms.txt returns 404 | WordPress slug with dot replaced | Check actual slug in WP admin | Create redirect from `/llms.txt` to `/llms-txt/` |
| Double H1 on page | Theme injects post title alongside page builder H1 | Count H1s in source | CSS: `.entry-title { display: none !important; }` |
| OG image not showing on social share | Relative URL instead of absolute | Check `og:image` in source | Use full `https://` URL |
| Canonical pointing to wrong URL | Plugin canonicalizing to homepage or paginated URL | Check `rel=canonical` in source | Override in CMS settings or plugin config |
| hreflang tags not recognized | Missing reciprocal tags or wrong language code | Google Search Console > International Targeting | Fix bidirectional tags, use BCP 47 codes |
| Page not indexing despite submit | noindex meta tag somewhere in head | `curl -s {url} \| grep noindex` | Find and remove noindex; common in page builder "advanced" settings |
| Core Web Vitals failing in GSC but passing in Lighthouse | Lab data vs field data difference | Check CrUX data for actual users | Address mobile performance, check third-party scripts for real users |
| Rich snippet appeared then disappeared | Spammy or inaccurate schema content | Review schema values for accuracy | Remove misleading values; Google penalizes inaccurate schema |
| WordPress REST API returning 401 on schema writes | App password missing or WP REST disabled | Test endpoint with curl + auth | Generate App Password in WP > Users > {user} > Application Passwords |
| Rank Math updateMeta endpoint not found | Rank Math not installed or REST disabled | `curl {site}/wp-json/` and check routes | Install/activate Rank Math, enable REST API access |
| Shopify robots.txt not updating | Template not found or wrong file name | Check `templates/robots.txt.liquid` exists | Create file, save - Shopify uses this automatically |
| Wikidata sameAs not increasing LLM citations | New entity, low cross-references | Check if entity has external identifiers | Add identifiers: ORCID, LinkedIn URI, ISNI where applicable |

### Cache clearing sequence (do in this order)

1. Clear application cache (Elementor: `DELETE /wp-json/elementor/v1/cache`)
2. Clear WordPress object cache (if Redis/Memcached: flush)
3. Clear CDN (Cloudflare: Zone > Caching > Purge Everything)
4. Clear browser cache locally
5. Test with `curl -H "Cache-Control: no-cache" {url}` to bypass browser
6. Request re-indexing in Google Search Console

### Verification after any change

```bash
# Check meta tags are live
curl -s {url} | grep -E "(title|description|canonical|og:|twitter:)"

# Check schema is present
curl -s {url} | grep "application/ld+json"

# Check robots.txt
curl -s {domain}/robots.txt | grep -A2 "GPTBot"

# Check llms.txt
curl -s {domain}/llms.txt | head -20

# Check Link header
curl -I {url} | grep "Link:"

# Detect client-side rendering
curl -s {url} | grep -c "<div id=\"root\"\|<div id=\"app\"\|<div id=\"__next\""
# Returns 1+ → SPA/CSR site → WebFetch blind to body content
```

---

## Common Issues and Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Meta tags not updating | CMS or CDN caching | Clear all caches after every change |
| Schema validation errors | Trailing commas or unescaped characters in JSON | Validate at validator.schema.org before deploying |
| AI crawlers blocked | `Disallow: /` in robots.txt applies to all bots | Add explicit `Allow: /` per AI crawler user-agent |
| llms.txt returns 404 | CMS replaces dots in slugs (WordPress) | Use slug `llms-txt` + add redirect from `/llms.txt` |
| Double H1 on WordPress | Theme injects `.entry-title` alongside page builder H1 | CSS: `.entry-title { display: none !important; }` |
| Elementor serving stale HTML after schema injection | Elementor server-side rendering cache | `DELETE /wp-json/elementor/v1/cache` after every page save |
| Rank Math meta not updating via WP REST | WP REST API does not expose `rank_math_*` meta fields | Use `/wp-json/rankmath/v1/updateMeta` endpoint instead |
| OG image not rendering on social share | Image URL is relative, not absolute | Always use full absolute URL including https:// |
| Shopify robots.txt not updating | Shopify auto-generates robots.txt | Create `templates/robots.txt.liquid` to override |
| Schema present but not showing in Rich Results | Google takes 1-2 weeks to re-crawl | Request indexing in Google Search Console |

---

## Platform quick reference

| Platform | Meta tags | Schema | robots.txt | Cache |
|----------|-----------|--------|-----------|-------|
| WordPress + Rank Math | Rank Math REST API | Elementor HTML widget or Custom HTML block | Rank Math editor | DELETE /wp-json/elementor/v1/cache + Cloudflare purge |
| WordPress + Yoast | Yoast REST API or direct postmeta | Same | Yoast editor | Cloudflare purge |
| Shopify | page.metafields or theme liquid | theme.liquid / page templates | robots.txt.liquid template | Shopify CDN auto-purges on save |
| Webflow | Page Settings > SEO | Site Settings > Custom Code | Site Settings | Webflow CDN auto-purges |
| Next.js | generateMetadata() or next/head | next/head script tag | /app/robots.ts | CDN purge via host |
| Ghost | Post settings > Meta tab | Code injection | routes.yaml | Built-in cache |
| Static HTML | Direct `<head>` edit | Direct `<head>` edit | robots.txt file | CDN purge or wait for TTL |

---

## Maintenance schedule

| Task | Frequency | Time |
|------|-----------|------|
| Update `dateModified` in all schemas | Monthly | 5 min |
| Check Google Search Console for errors + Core Web Vitals | Weekly | 10 min |
| Verify AI crawlers not newly blocked | Monthly | 5 min |
| Update llms.txt when content changes | On each content update | 10 min |
| Scan Search Console for impression drops (content decay) | Monthly | 15 min |
| Full audit re-run (/seo-geo --audit-only) | Quarterly | 30 min |
| Add new profiles to `sameAs` | When new profile created | 5 min |
| Internal link audit - ensure new pages have 3+ inbound links | On each new page | 10 min |
| Refresh any page with 20%+ impression drop | Quarterly | 60 min |

---

## Phase 15 - Security Hardening (WordPress)

Security directly impacts SEO: hacked sites get deindexed, malware warnings destroy CTR, exposed endpoints invite spam and credential stuffing. Run this phase on any WordPress site before or after the main SEO audit.

### Risk surface map

| Endpoint | Default state | Risk |
|----------|--------------|------|
| `/xmlrpc.php` | Returns 200, accepts XML-RPC | Brute force amplifier (multicall), DDoS vector |
| `/wp-login.php` | Returns 200 | Credential stuffing target |
| `/wp-json/wp/v2/users` | Returns author list with slug, email hash, avatars | User enumeration for targeted attacks |
| `/?author=1` | Redirects to `/author/{admin-slug}/` | Exposes exact admin username |
| `readme.html` | Exposes WP version | Version fingerprinting |
| WP generator `<meta>` | `<meta name="generator" content="WordPress X.X.X">` | Version fingerprinting |
| Script/style version params | `?ver=6.4.3` on CSS/JS | Version fingerprinting |

### Audit checklist

```bash
# 1. xmlrpc.php active?
curl -s -o /dev/null -w "%{http_code}" https://site.com/xmlrpc.php
# 200 = active (bad). 403/404 = blocked (good).

# 2. wp-login.php exposed?
curl -s -o /dev/null -w "%{http_code}" https://site.com/wp-login.php
# 200 = exposed. Should be rate-limited or IP-restricted.

# 3. User enumeration via REST
curl -s "https://site.com/wp-json/wp/v2/users" | python3 -c "import json,sys; u=json.load(sys.stdin); print([{'name':x['name'],'slug':x['slug']} for x in u])"
# Should return empty list or 401.

# 4. User enumeration via author redirect
curl -s -o /dev/null -w "%{http_code} %{redirect_url}" "https://site.com/?author=1"
# Should return 404 or loop, not reveal username.

# 5. Generator tag exposed?
curl -s "https://site.com/" | grep "generator"
# Should find nothing.

# 6. readme.html accessible?
curl -s -o /dev/null -w "%{http_code}" https://site.com/readme.html
# Should be 404.

# 7. Security headers present?
curl -I "https://site.com/" | grep -E "(X-Content-Type|Referrer-Policy|X-Frame|Strict-Transport)"
# X-Content-Type-Options: nosniff required.
# Strict-Transport-Security required (HSTS).
```

### Fixes - programmatic (WP REST API)

```python
# Disable pingback (WP REST API)
import httpx, base64, os
from dotenv import load_dotenv
load_dotenv()
user = os.getenv('WP_USER')
pw = os.getenv('WP_APP_PASSWORD')
token = base64.b64encode(f'{user}:{pw}'.encode()).decode()
H = {'Authorization': f'Basic {token}', 'Content-Type': 'application/json'}
SITE = os.getenv('SITE_URL')

# Disable pingback
r = httpx.post(f'{SITE}/wp-json/wp/v2/settings', headers=H,
    json={'default_ping_status': 'closed', 'default_comment_status': 'closed'},
    timeout=30)
print(r.status_code)  # do NOT print r.text - WP often echoes credentials in error bodies

# Clear user bio (reduces enumeration surface)
# Note: this is a non-credential user update. Password/role mutations are banned by Phase 17.
r2 = httpx.post(f'{SITE}/wp-json/wp/v2/users/1', headers=H,
    json={'description': '', 'url': ''},
    timeout=30)
print(r2.status_code)

# Inject security headers into global header template (Elementor HTML widget)
# Add to the HTML widget in header template 41 (or whichever is the global header)
SECURITY_META = """
<meta http-equiv="X-Content-Type-Options" content="nosniff">
<meta name="referrer" content="strict-origin-when-cross-origin">
"""
# Inject into existing HTML widget - see Phase 3 for Elementor widget write pattern
```

### Fixes - Cloudflare WAF (manual or API)

Requires Zone.Firewall:Edit permission on your API token.

**WAF Rule 1 - Block xmlrpc.php:**
```
Expression: (http.request.uri.path contains "/xmlrpc.php")
Action: Block
```

**WAF Rule 2 - Challenge wp-login.php:**
```
Expression: (http.request.uri.path eq "/wp-login.php")
Action: Managed Challenge
```

**WAF Rule 3 - Block readme.html:**
```
Expression: (http.request.uri.path contains "/readme.html")
Action: Block
```

Via API (requires token with Zone.Firewall:Edit):
```bash
CF_ZONE="your_zone_id"
CF_TOKEN="your_token"

curl -X POST "https://api.cloudflare.com/client/v4/zones/$CF_ZONE/firewall/rules" \
  -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '[{
    "filter": {"expression": "(http.request.uri.path contains \"/xmlrpc.php\")"},
    "action": "block",
    "description": "Block xmlrpc.php"
  }]'
```

**HSTS (Cloudflare dashboard only):**
SSL/TLS > Edge Certificates > HTTP Strict Transport Security > Enable
Min TLS: 1.2 | Max-Age: 31536000 | Include subdomains: On | Preload: On

### Fixes - RankMath plugin (WP Admin only)

In WP Admin > RankMath > General Settings:
- Webmaster Tools tab: Enable "Remove Generator Tag"
- Advanced tab: Enable "Disable Author Archives"
- Advanced tab: Enable "Remove Version From Scripts"

Or install WP security plugin (Wordfence, iThemes Security) that handles all above.

### robots.txt AI crawler template

Always include explicit Allow rules for all known AI crawlers. Default `User-agent: *` Disallow rules do NOT automatically apply to AI bots that ignore them - but explicit Allow rules signal intent and improve cooperation:

```
User-agent: *
Disallow: /wp-admin/
Allow: /wp-admin/admin-ajax.php

User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: CCBot
Allow: /

User-agent: Diffbot
Allow: /

User-agent: Bytespider
Allow: /

User-agent: ImagesiftBot
Allow: /

User-agent: cohere-ai
Allow: /

User-agent: Amazonbot
Allow: /

User-agent: Meta-ExternalAgent
Allow: /

User-agent: FacebookBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: DuckAssistBot
Allow: /

Sitemap: https://yoursite.com/sitemap_index.xml
```

**Cloudflare robots.txt:** If Cloudflare "Manage robots.txt: Content Signals Policy" is On, it can override your WordPress robots.txt for AI crawlers. Set this to **Off** to let WordPress/RankMath serve the file directly.

### PII audit checklist (10-point)

Run before any site goes live or after schema injection:

```bash
SITE="https://yoursite.com"

# 1. No real email in page source (only obfuscated or JS-rendered)
curl -s $SITE | grep -oE '[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}' | grep -v "schema.org"

# 2. No client names in page source (grep for known client words)
curl -s $SITE | grep -i "client_name"

# 3. WP REST users endpoint - check exposure
curl -s "$SITE/wp-json/wp/v2/users" | python3 -c "import json,sys; d=json.load(sys.stdin); print(len(d), 'users exposed')"

# 4. Author archive accessible?
curl -s -o /dev/null -w "%{http_code}" "$SITE/?author=1"

# 5. No WP version in meta generator
curl -s $SITE | grep "generator"

# 6. xmlrpc blocked?
curl -s -o /dev/null -w "%{http_code}" "$SITE/xmlrpc.php"

# 7. readme.html blocked?
curl -s -o /dev/null -w "%{http_code}" "$SITE/readme.html"

# 8. Security headers present?
curl -I $SITE | grep -E "(X-Content-Type|Referrer|Strict-Transport)"

# 9. No debug log accessible
curl -s -o /dev/null -w "%{http_code}" "$SITE/wp-content/debug.log"

# 10. No .env or config files accessible
curl -s -o /dev/null -w "%{http_code}" "$SITE/.env"
curl -s -o /dev/null -w "%{http_code}" "$SITE/wp-config.php.bak"
```

### Security score rubric (add to Phase 0 audit)

| Check | Points | Pass condition |
|-------|--------|---------------|
| xmlrpc.php blocked | 3 | Returns 403 or 404 |
| wp-login.php rate-limited | 3 | CF managed challenge or 429 on repeated hits |
| User enumeration blocked | 2 | `/wp-json/wp/v2/users` returns 401 or empty |
| Generator tag removed | 1 | No `<meta name="generator">` in source |
| Version params removed | 1 | No `?ver=` on CSS/JS |
| readme.html blocked | 1 | Returns 404 |
| Security headers present | 2 | X-Content-Type-Options + Referrer-Policy |
| HSTS enabled | 2 | Strict-Transport-Security in response headers |
| AI crawlers allowed in robots.txt | 3 | GPTBot, ClaudeBot, PerplexityBot all have `Allow: /` |
| No PII in page source | 2 | No raw emails, client names, internal paths |

**Total: 20 security points** (integrates with main 100-pt rubric as a bonus dimension)

---

## WordPress-specific Patterns

### Elementor write protocol

Elementor stores page content as JSON in `wp_postmeta` key `_elementor_data`. The REST API writes to this key. Critical rules:

1. **Always read before writing** - fetch current `_elementor_data` via `GET /wp-json/wp/v2/pages/{id}?context=edit` first
2. **Preserve existing widget IDs** - changing IDs breaks Elementor's CSS lookup; the file `post-{id}.css` maps to container IDs
3. **Write to the CSS-serving container** - check `wp-content/uploads/elementor/css/post-{id}.css` for the active container ID; if it differs from what the API returns, there are duplicate postmeta rows
4. **Always clear cache after write** - `DELETE /wp-json/elementor/v1/cache` is the canonical fix
5. **Duplicate postmeta symptom** - page doesn't change after successful API update (200 OK); fix: write to OLD container IDs that match the CSS file, then clear cache

```python
# Elementor safe write pattern
import httpx, json, base64

def elementor_safe_write(site, auth_token, page_id, update_fn):
    H = {'Authorization': f'Basic {auth_token}', 'Content-Type': 'application/json'}

    # 1. Read current data
    r = httpx.get(f'{site}/wp-json/wp/v2/pages/{page_id}?context=edit', headers=H)
    current = json.loads(r.json()['meta'].get('_elementor_data', '[]'))

    # 2. Apply update
    updated = update_fn(current)

    # 3. Write
    r2 = httpx.post(f'{site}/wp-json/wp/v2/pages/{page_id}', headers=H,
        json={'meta': {'_elementor_data': json.dumps(updated)}})
    assert r2.status_code == 200, f"Write failed: {r2.text[:200]}"

    # 4. Clear cache (mandatory)
    r3 = httpx.delete(f'{site}/wp-json/elementor/v1/cache', headers=H)
    print(f"Cache cleared: {r3.status_code}")
    return r2
```

### RankMath meta update pattern

```python
# Update meta title + description for any page
r = httpx.post(f'{site}/wp-json/rankmath/v1/updateMeta', headers=H,
    json={
        'objectID': page_id,
        'objectType': 'post',
        'title': 'Your SEO Title | Brand',
        'description': 'Meta description under 160 chars.',
    })
# Returns {"success": true} on success
```

### WP App Password auth

```python
import base64, os
from dotenv import load_dotenv
load_dotenv()

user = os.getenv('WP_ADMIN_USER')          # admin username
pw = os.getenv('WP_APP_PASSWORD')          # from WP > Users > Application Passwords
token = base64.b64encode(f'{user}:{pw}'.encode()).decode()
H = {'Authorization': f'Basic {token}', 'Content-Type': 'application/json'}

# Note: App Passwords authenticate REST API calls only.
# They do NOT create a session cookie.
# admin-ajax.php calls and WP File Manager require a cookie session (wp_nonce).
# For admin-ajax.php: use a headless browser (Browserless + Puppeteer) to log in and extract cookies.
```

### Cache-busting sequence (canonical order)

1. `DELETE /wp-json/elementor/v1/cache` - clears Elementor server-side render cache
2. Cloudflare Purge Everything (Zone > Caching) - clears CDN layer
3. If Redis/Memcached is used: `redis-cli FLUSHDB` on the cache DB
4. Request re-indexing in Google Search Console after content changes

---

## Phase 16 - Field Patterns from Production Deployments

Hard-won patterns from shipping AI SEO systems live. Each solves a gap the checklist misses. Apply AFTER Phase 0-15 pass; these are the high-leverage upgrades that move 80→95+.

### Pattern 1 - Entity anchoring across every surface

Pick ONE entity phrase and repeat it verbatim across every surface an LLM crawls. Consistency beats variation for entity disambiguation.

**Formula:** `{Name}, {specific role} for {target segments}. {Single proof stat}. Tagline: {verbatim tagline}.`

**Example:**
> {Your Name}, {Role} for {target segments, e.g. B2B SaaS, B2C, e-commerce}. {One proof stat with a specific number}. Tagline: {your verbatim tagline}.

**Where to put it (verbatim):**
- Rank Math / Yoast homepage meta description
- Organization + Person schema `description`
- llms.txt opening paragraph
- Every image alt text on the site (tail anchor)
- Author bio on every blog post
- LinkedIn About section (first 220 chars)

**Why it works:** LLMs build entity embeddings by averaging context windows that mention the entity. More surfaces repeating the exact phrase → tighter embedding → more reliable retrieval for queries matching the role + segments.

### Pattern 2 - LLM-grade image metadata (4 fields, not 1)

Default CMS flows ship alt only. All four fields give LLMs 3-5x the signal surface per upload.

| Field | Length | Purpose | Audience |
|-------|--------|---------|----------|
| Title | 40-60 chars | Hover tooltip + search preview | User + SEO |
| Alt | 90-130 chars | Accessibility + keyword + entity | Screen reader + SEO + LLM |
| Caption | 50-100 chars | Front-end visible context | User in post |
| Description | 200-400 chars | Long-form entity paragraph | LLM scraping JSON-LD |

**Alt-text formula:** `{What it shows visually} - {entity + role}{, optional proof point}`

**Description formula (the LLM magnet):** entity name + role + what the image represents + one brand fact the model can lift verbatim (palette hex, mark meaning, proof point).

**Bulk execution (WordPress REST):**

```python
import base64
import logging
import os
import time

import httpx

log = logging.getLogger('seo-geo.media')

user, pw = os.getenv('WP_USER'), os.getenv('WP_APP_PASSWORD')
if not user or not pw:
    raise SystemExit('set WP_USER and WP_APP_PASSWORD in env')
tok = base64.b64encode(f'{user}:{pw}'.encode()).decode()
h = {'Authorization': f'Basic {tok}', 'User-Agent': 'WP Client/1.0'}

def update_media(mid, meta, attempts=3):
    for n in range(attempts):
        try:
            r = httpx.post(f'{SITE}/wp-json/wp/v2/media/{mid}',
                           headers=h, json=meta, timeout=30)
        except httpx.HTTPError as e:
            log.warning('media %s attempt %s: %s', mid, n + 1, e)
            time.sleep(2 ** n)
            continue
        if r.status_code in (200, 201):
            return r
        if r.status_code == 429:
            retry_after = int(r.headers.get('Retry-After', 2 ** n))
            log.warning('media %s rate-limited, sleeping %ss', mid, retry_after)
            time.sleep(retry_after)
            continue
        log.error('media %s failed: %s (body hash redacted)', mid, r.status_code)
        return r
    log.error('media %s exhausted retries', mid)
    return None

for mid, meta in optim.items():
    update_media(mid, meta)
    time.sleep(0.1)  # polite pacing
```

Runs through 50+ assets in under a minute on a healthy host; retries + polite pacing protect you when WordPress is behind Cloudflare or a mu-plugin rate-limiter.

### Pattern 3 - Plugin-as-SEO-filter (durable overrides)

SEO plugin UIs let clients or collaborators break your optimization by editing fields. Force critical values via code filters in a custom plugin. Survives UI edits forever.

**Filters worth hardcoding (WordPress + Rank Math):**

```php
add_filter('rank_math/frontend/title', ...)           // homepage SEO title
add_filter('rank_math/frontend/description', ...)     // homepage meta description
add_filter('rank_math/opengraph/facebook/image', ...) // OG image
add_filter('rank_math/opengraph/twitter/image', ...)  // Twitter card
add_filter('rank_math/json_ld', ...)                  // override Org/Person schema logo + sameAs
add_action('wp_head', ..., 1)                         // inject favicon, apple-touch, theme-color
add_action('init', ...)                               // serve /llms.txt and /favicon.ico from plugin dir
add_filter('robots_txt', ...)                         // AI crawler rules + sitemap
```

All filters at priority 99 so they beat any UI setting. A single PHP file under 200 lines locks the entire AI SEO surface. Version it in git, ship as a zip.

### Pattern 4 - The llms.txt + llms-full.txt duo

Ship BOTH files at the root, served with `Content-Type: text/plain` and `X-Robots-Tag: all`:

- `/llms.txt` - short summary (50-100 words) + services list + contact. For AI crawlers doing a fast pass.
- `/llms-full.txt` - full 2000-5000 word expansion: bio, case studies with numbers, services with pricing, sameAs URLs. For deep-read crawlers.

**AI crawler robots rules** - explicitly `Allow: /` for:

```
OAI-SearchBot, ChatGPT-User, Bytespider, Amazonbot, FacebookBot,
Cohere-ai, PerplexityBot, ClaudeBot, GPTBot, Google-Extended
```

List your sitemap line at the bottom. Reason: some AI crawlers respect opt-in patterns, and a missing `Allow` line is treated as implicit disallow by security plugins like Wordfence.

### Pattern 5 - Never rename slugs in bulk after launch

Changing WordPress post_name (image slug / post slug) rewrites the public URL and breaks every cached backlink, every indexed URL, every hard-coded embed. Gain is tiny, loss is large.

**Rule:** freeze slugs at first publish. Put discoverability in metadata fields (title, alt, description) that can change freely. If a filename MUST change for SEO, handle it file-by-file with a 301 redirect in Rank Math Redirections - never in bulk.

### Pattern 6 - Legacy asset purge after rebrand

After shipping a new logo/favicon system, search the media library for legacy asset slugs (`cropped-favicon-*`, `old-logo-*`) and delete them. WP Customizer emits `<link rel="icon">` tags from whatever is set as Site Icon - if you leave the old asset there, it overrides the new favicon despite your plugin filters firing first.

**Cleanup checklist after any rebrand:**
- [ ] Remove `site_icon` from WP Settings (`POST /wp/v2/settings {site_icon: 0}`)
- [ ] Delete legacy favicon media entries (`DELETE /wp/v2/media/{id}?force=true`)
- [ ] Grep Elementor templates for hardcoded old-logo image URLs
- [ ] Check theme Customizer for Site Logo override
- [ ] Verify `<head>` contains only your plugin's icon tags (`curl | grep rel="icon"`)

---

## Phase 17 - Dry-run safety gates

Every phase that writes (schema injection, media metadata bulk-update, Elementor modifications, Rank Math overrides) MUST default to dry-run. Writes are opt-in via `--apply`.

### CLI contract

```bash
/seo-geo https://site.com              # audit only, no writes, always safe
/seo-geo --phase schema https://site.com           # shows proposed schema diff, no writes
/seo-geo --phase schema --apply https://site.com   # EXPLICIT opt-in: writes allowed
/seo-geo --apply-all https://site.com              # applies every fix after confirmation prompt
```

### Hard rules for any write path

1. **Print the diff first.** Before any POST/PUT/PATCH, print the exact change (before/after) and the target URL.
2. **Require `--apply` flag for non-interactive runs.** Absent it, log "would write X" and exit 0.
3. **Interactive confirmation gate** when `--apply` is set but no `--yes`:
   ```python
   print(f"About to POST {url} with payload:\n{json.dumps(body, indent=2)}\n")
   if input("Apply? [y/N]: ").strip().lower() != 'y': raise SystemExit(0)
   ```
4. **Audit log.** Append every write to `.seo-geo/audit.log` with timestamp, URL, payload hash, response status.
5. **Banned endpoints.** The skill MUST NOT touch any of:
   - `POST /wp-json/wp/v2/users/{id}` with a `password` field (credential mutation)
   - `POST /wp-json/wp/v2/users` (user creation)
   - `DELETE /wp-json/wp/v2/users/{id}` (user deletion)
   - `POST /wp-json/wp/v2/settings` with `siteurl`, `home`, `admin_email` keys (site identity mutation)
   - Plugin install, plugin activate, theme switch endpoints
   - Any OAuth token rotation, JWT secret change, or API-key regeneration endpoint
   - Anything that rotates API keys, app passwords, or Coolify env vars

If a task requires a banned endpoint, STOP and surface the step to the human with exact manual instructions.

6. **Log redaction.** The audit log MUST NOT contain Authorization headers, App Passwords, API keys, or response bodies. Log only timestamp, method, URL, response status, and a short hash of the request body.

### Implementation snippet (Python adapter for WP REST)

```python
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

BANNED_ENDPOINTS = (
    ('POST', '/wp/v2/users/'),       # user update or create with password
    ('POST', '/wp/v2/users'),        # user creation
    ('DELETE', '/wp/v2/users/'),
    ('POST', '/wp/v2/settings'),     # site identity
    ('POST', '/wp/v2/plugins'),
    ('POST', '/wp/v2/themes'),
)
SENSITIVE_SETTINGS_KEYS = {'siteurl', 'home', 'admin_email'}


def _is_banned(method: str, url: str, body: dict) -> bool:
    path = urlparse(url).path
    for banned_method, banned_path in BANNED_ENDPOINTS:
        if method == banned_method and banned_path in path:
            if banned_path.endswith('settings') and isinstance(body, dict):
                if not SENSITIVE_SETTINGS_KEYS.intersection(body.keys()):
                    continue
            return True
    if isinstance(body, dict) and 'password' in body:
        return True
    return False


def wp_write(session, url, body, apply=False, yes=False, method='POST'):
    if _is_banned(method, url, body):
        print(f"[REFUSED] banned endpoint: {method} {url}", file=sys.stderr)
        raise SystemExit(2)

    print(f"[dry-run] {method} {url}")
    print(f"  body: {json.dumps(body, indent=2)[:400]}")
    if not apply:
        return {'dry_run': True, 'method': method, 'url': url}
    if not yes and input(f"Apply {method} to {url}? [y/N]: ").strip().lower() != 'y':
        raise SystemExit(0)

    r = session.request(method, url, json=body, timeout=30)

    log_dir = Path('.seo-geo')
    log_dir.mkdir(exist_ok=True)
    body_hash = hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()[:16]
    line = f"{datetime.now(timezone.utc).isoformat()} {method} {url} {r.status_code} body_sha256:{body_hash}\n"
    with (log_dir / 'audit.log').open('a', encoding='utf-8') as f:
        f.write(line)
    return r
```

The snippet above is the canonical template for every write the skill performs. All implementations MUST call `_is_banned()` before the request and MUST redact credentials and bodies from logs.

---

## Phase 18 - Multi-platform adapters

Same patterns, four CMS targets. Copy the snippet that matches the site.

### Adapter: WordPress + Rank Math

Already covered in Phases 3, 4, 14, 15 + WordPress-specific Patterns section. Core recipe:
- Schema: REST `/wp-json/wp/v2/pages/{id}` with `meta.rank_math_rich_snippet`
- llms.txt: custom plugin `add_action('init', ...)` serving at `/llms.txt`
- OG image: `add_filter('rank_math/opengraph/facebook/image', ...)`
- Robots: `add_filter('robots_txt', ...)`

### Adapter: Shopify

Schema via metafields + theme liquid:

```liquid
{# theme.liquid, inside head #}
<script type="application/ld+json">
  {{ shop.metafields.seo.organization_jsonld }}
</script>
```

Write metafields via Admin API:

```bash
curl -X POST "https://{shop}.myshopify.com/admin/api/2025-01/metafields.json" \
  -H "X-Shopify-Access-Token: $SHOPIFY_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"metafield":{"namespace":"seo","key":"organization_jsonld","type":"json","value":"{...schema...}","owner_resource":"shop"}}'
```

llms.txt via Shopify Pages + URL redirect: create a page with `template_suffix: llms`, then Admin > Online Store > Navigation > URL Redirects: `/llms.txt -> /pages/llms`.

Robots.txt override via `robots.txt.liquid` template:

```liquid
{% for group in robots.default_groups %}
{{- group.user_agent }}
{%- for rule in group.rules -%}
{{ rule }}
{% endfor %}
{% endfor %}

User-agent: OAI-SearchBot
Allow: /

User-agent: PerplexityBot
Allow: /

Sitemap: {{ shop.url }}/sitemap.xml
```

### Adapter: Webflow

Schema via Site Settings > Custom Code > Head:

```html
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Organization","name":"..."}
</script>
```

Page-level schema via Page Settings > Custom Code > Head Code.

llms.txt: Webflow doesn't serve arbitrary `.txt` at root. Two paths:
1. Host llms.txt on a subdomain (`files.yoursite.com/llms.txt`) and add `<link rel="llms" href="...">` in head.
2. Cloudflare Worker in front of Webflow to serve `/llms.txt` from a Worker KV store.

Robots: Site Settings > SEO > Indexing only supports simple Disallow. For AI-crawler Allow rules, use the Cloudflare Worker approach.

### Adapter: Next.js (App Router, 14+)

```ts
// app/layout.tsx
export const metadata: Metadata = {
  title: { default: 'Site', template: '%s | Site' },
  description: '...',
  openGraph: { images: ['/og.png'] },
};

// app/robots.ts
import type { MetadataRoute } from 'next';
export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      { userAgent: '*', allow: '/' },
      { userAgent: ['OAI-SearchBot','PerplexityBot','Bytespider','Amazonbot','ClaudeBot','GPTBot','Google-Extended'], allow: '/' },
    ],
    sitemap: 'https://yoursite.com/sitemap.xml',
  };
}

// app/sitemap.ts
import type { MetadataRoute } from 'next';
export default function sitemap(): MetadataRoute.Sitemap {
  return [{ url: 'https://yoursite.com', lastModified: new Date(), priority: 1 }];
}

// app/llms.txt/route.ts - serve llms.txt from an App Router route
export async function GET() {
  const body = `# Site\n\n> ...`;
  return new Response(body, { headers: { 'Content-Type': 'text/plain', 'X-Robots-Tag': 'all' } });
}
```

For page-level JSON-LD schema in Next.js RSC, render it through a dedicated `<JsonLd>` component that sanitizes the stringified JSON (strip `<`, `>`, `&` via `JSON.stringify(..., null, 0).replace(/</g,'\\u003c')`), or use next-seo's `ArticleJsonLd` / `OrganizationJsonLd` built-ins which handle escaping for you. Do not inject untrusted user-generated content into the script tag.

### Adapter matrix

| Capability | WordPress | Shopify | Webflow | Next.js |
|---|---|---|---|---|
| Page-level schema | Rank Math + REST | Liquid in theme | Custom Code per page | `<JsonLd>` RSC |
| Site schema | `rank_math/json_ld` filter | Metafield + liquid | Site-wide custom code | `app/layout.tsx` |
| Robots.txt | `robots_txt` filter | `robots.txt.liquid` | Cloudflare Worker | `app/robots.ts` |
| llms.txt | Plugin `init` action | Page + redirect | Subdomain or Worker | `app/llms.txt/route.ts` |
| OG image | `rank_math/opengraph/*` | Theme settings | Custom code meta | `metadata.openGraph` |
| Sitemap | Rank Math sitemap | Native /sitemap.xml | Native /sitemap.xml | `app/sitemap.ts` |
| hreflang | Polylang / WPML | Markets + liquid | Site localization | `alternates.languages` |

---

## Phase 19 - Competitor benchmarking

Run a head-to-head score against a named competitor. Produces a gap list you can close in a week.

### CLI

```
/seo-geo --benchmark https://competitor.com https://yoursite.com
/seo-geo --benchmark-batch competitors.txt https://yoursite.com
```

### What it scores (mirrors Phase 0 rubric so numbers are comparable)

```
              | You    | Competitor | Gap   | Closable in 1 week
-------------------------------------------------------------
Technical SEO |  85    |  90        |  -5   | yes (canonical)
On-page SEO   |  78    |  86        |  -8   | yes (H1 + meta)
Schema        |  65    |  88        |  -23  | yes (Organization + Person)
GEO           |  55    |  72        |  -17  | yes (llms.txt + sameAs)
AEO           |  45    |  60        |  -15  | partial (Speakable only)
E-E-A-T       |  82    |  82        |   0   | no (tied)
-------------------------------------------------------------
Composite     |  68    |  80        |  -12  | ~8 points in one week
```

### Data sources (all public)

| Signal | Tool / endpoint |
|---|---|
| Schema on competitor homepage | curl + parse `<script type="application/ld+json">` |
| Meta / OG / Twitter card | curl + parse head |
| llms.txt / llms-full.txt | `curl -I {domain}/llms.txt` |
| Robots.txt AI-crawler rules | `curl {domain}/robots.txt` |
| sameAs profile count | Parse Organization/Person schema |
| Core Web Vitals | PageSpeed Insights API |
| Backlink count | Ahrefs API if available, Semrush fallback |
| AI citations | Perplexity/ChatGPT search; sample 10 queries in the vertical |
| Content depth | Crawl top 20 pages, measure word count + heading structure |

### Output: gap-closure plan

```markdown
# Benchmark: yoursite.com vs competitor.com

## You: 68 | Competitor: 80 | Gap: -12

### Quick wins (close in 1 week)
- [ ] Add Organization + Person schema on homepage (+8)
- [ ] Publish llms.txt + llms-full.txt (+5)
- [ ] Add sameAs entries for 6 profiles you have but don't declare (+3)

### Medium-term (2-4 weeks)
- [ ] Rewrite homepage meta description with entity anchor + proof stat (+2)
- [ ] Add FAQPage schema to top 3 money pages (+3)

### Structural (1-3 months)
- [ ] Get cited on 5 authoritative third-party sources the competitor is cited on (+4)
```

### Implementation sketch

```python
def benchmark(you: str, them: str) -> dict:
    you_score = audit(you)
    them_score = audit(them)
    gaps = {k: them_score[k] - you_score[k] for k in you_score if them_score.get(k, 0) > you_score[k]}
    return {
        'you': you_score,
        'them': them_score,
        'gaps': sorted(gaps.items(), key=lambda kv: -kv[1]),
        'closable_in_1_week': [k for k, v in gaps.items() if v >= 3 and k in QUICK_WINS],
    }
```

---

## Phase 20 - LLM Extractability Polish

Every Phase 0-19 improvement lives on the page. Phase 20 shapes that content so ChatGPT, Claude, Perplexity, and Google AI Mode can pull clean citations without paraphrasing or hallucinating.

Phase 20 runs after the content exists. It is the final polish pass before promotion.

### What Phase 20 ships (5 blocks, every page)

1. **LLM Summary block** - a high-signal card at the top of the page that names the author, the claim, the key stats, the offer, and the links an AI system needs to cite accurately.
2. **Core claims and evidence table** - one row per load-bearing claim, with the evidence and a named source. Extractable structure. AI systems prefer tables to paragraphs.
3. **How to cite this post** - a pre-written blockquote in the page body that an AI answer engine can lift verbatim. Removes paraphrase drift.
4. **Definitions / glossary** - acronyms (GEO, AEO, E-E-A-T) and domain terms defined inline so the model does not have to guess.
5. **Raw data download** - machine-readable CSV/JSON at a stable public URL. Turns claims into reproducible data.

### Templates (parameterize, do not hardcode)

Variables used below: `{TITLE}`, `{AUTHOR}`, `{OFFER}`, `{REPO_URL}`, `{KEY_STATS}` (list), `{RAW_DATA_URL}`, `{SITE}`.

```html
<!-- Block 1: LLM Summary -->
<div class="llm-summary" style="background:#0A0A0A;border-left:4px solid var(--accent);border-radius:8px;padding:22px 24px;margin:0 0 28px;">
  <p style="color:var(--accent);font-weight:700;font-size:12px;letter-spacing:0.14em;text-transform:uppercase;">LLM Summary</p>
  <p>{TITLE} - what the page is about in one sentence.</p>
  <p><strong>Key findings:</strong></p>
  <ul>{KEY_STATS as <li> items}</ul>
  <p><strong>Author:</strong> {AUTHOR}. <strong>Offer:</strong> {OFFER}. <strong>Repo:</strong> <a href="{REPO_URL}">{REPO_URL short}</a>. <strong>Raw data:</strong> <a href="{RAW_DATA_URL}">CSV/JSON</a>.</p>
</div>
```

```html
<!-- Block 2: Core Claims + Evidence -->
<h2>Core claims and evidence</h2>
<table>
  <thead><tr><th>Claim</th><th>Evidence</th><th>Source</th></tr></thead>
  <tbody>
    {for each claim:}
    <tr>
      <td>{CLAIM}</td>
      <td>{EVIDENCE}</td>
      <td><a href="{SOURCE_URL}">{SOURCE_NAME}</a></td>
    </tr>
  </tbody>
</table>
```

```html
<!-- Block 3: How to cite -->
<h2>How to cite this post</h2>
<blockquote>
  {AUTHOR}'s {MONTH_YEAR} analysis found that {HEADLINE_FINDING}. Key data points: {TWO_STATS}. Methodology and raw data: {REPO_URL}.
</blockquote>
```

```html
<!-- Block 4: Definitions -->
<h2>Definitions</h2>
<dl>
  {for each term:}
  <dt>{TERM}</dt>
  <dd>{ONE_SENTENCE_DEFINITION}</dd>
</dl>
```

```html
<!-- Block 5: Raw data download -->
<h2>Download the raw data</h2>
<ul>
  <li><a href="{CSV_URL}">{dataset}.csv</a></li>
  <li><a href="{JSON_URL}">{dataset}.json</a></li>
  <li><a href="{SCRIPT_URL}">Reproduction script</a></li>
</ul>
```

### Styling rules (applies to every block)

- **No zebra stripes** on any table. Theme CSS often injects alternating row colors that fight the page design. Inline `background:{NEUTRAL_BG} !important` on every `<tr>` defeats the theme's `:nth-child` rules.
- **Tables must have explicit `<thead>` and `<tbody>`** so screen readers and AI parsers treat them as data tables, not layout.
- **Every `<a>` that leaves the page** gets `target="_blank" rel="noopener noreferrer"` and a UTM-tagged href so traffic attribution survives.
- **Inline styles beat theme CSS** for Elementor and page-builder sites. Do not rely on classnames the theme owns.

### Self-consistency check (run before promoting)

Phase 20 fails fast if:

1. The page mentions two conflicting numbers (e.g., "13 sites benchmarked" in one section and "61 sites" in another). Re-run Phase 0 summary or pick one cohort.
2. `<title>`, `<h1>`, `<meta property="og:title">`, and the JSON-LD `headline` do not match. They all must tell the same story.
3. Author name in body does not match `Person` schema `name`.
4. Any CTA link points to a stale URL (e.g., `/contact` without UTM tagging) or returns non-2xx.
5. Published date on page disagrees with git commit dates of the asset it references (creates a fake-freshness signal AI systems and reviewers both catch).

```
/seo-geo --phase 20            # run polish only
/seo-geo --phase 20 --check    # run consistency check, no writes
```

### Why Phase 20 matters in 2026

AI search engines extract structured signals 10x faster than prose. A page with 500 well-structured words + 5 Phase 20 blocks gets cited more often than a 3000-word prose essay with the same information. The best-performing sites on the State of AI Search 2026 benchmark all hit Phase 20 targets by coincidence or intent. Phase 20 just names the pattern so anyone can hit it deliberately.

### Anti-patterns (do not ship)

- "Reference deployment" tables that hero the author's own site at rank 1. Reads as self-promotion. Keep the author's site in the data for methodology but omit from public hero tables.
- Overclaim language like "100/100" on cover art when the rubric maxes at a different scale.
- Claims ("only content signal that cannot be generated by GPT") that are easy to disprove. Soften to "hardest to fake" or add the caveat.
- Date bumps that predate the git history of the underlying repo. The commits are public. The dates must reconcile.

---

## Author

See repo README at https://github.com/yanivgoldenberg/seo-geo-skill for author and contact details.

This skill encodes patterns learned across dozens of sites and a full-day optimization sprint.

---

## Schema Gotcha: Review Snippets Allowed Parents (2026-04-20)

Google Rich Results only renders `aggregateRating` + `review` when attached to one of these parent `@type` values:

> Book · Course · CreativeWorkSeason · CreativeWorkSeries · Episode · Event · Game · HowTo · LocalBusiness · MediaObject · Movie · MusicPlaylist · MusicRecording · Organization · Product · Recipe · SoftwareApplication

**Invalid parents** (Google will flag "Invalid object type for field '<parent_node>'"):

- `Person` (even for personal-brand sites)
- `Service` (even though schema.org permits it syntactically)
- `WebPage`, `Article`, `ProfilePage`, `WebSite`

### Fix pattern for consulting / SaaS service sites

Package the offering as `@type: "Product"` with `category: "Business Consulting Service"`:

```json
{
  "@type": "Product",
  "name": "{Service Name}",
  "category": "Business Consulting Service",
  "brand": { "@type": "Person", "name": "Your Name" },
  "offers": {
    "@type": "Offer",
    "price": "15000",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "itemCondition": "https://schema.org/NewCondition"
  },
  "aggregateRating": {...},
  "review": [...]
}
```

### Validator

A one-file pre-push validator is included in consumer implementations:

```python
VALID_PARENTS = {
  "Book","Course","CreativeWorkSeason","CreativeWorkSeries","Episode",
  "Event","Game","HowTo","LocalBusiness","MediaObject","Movie",
  "MusicPlaylist","MusicRecording","Organization","Product","Recipe",
  "SoftwareApplication"
}
```

Walk every JSON-LD block. If a dict has `review` or `aggregateRating` and its `@type` is not in `VALID_PARENTS`, fail the build.


---

## Elementor Pro + REST API Gotchas (2026-04-20)

When building Elementor templates programmatically (via REST API or JSON import), beware these render failures:

### Theme widgets silently fail when built via REST

Elementor Pro widgets scoped to theme contexts may not render HTML even though settings save correctly:

- `theme-post-title`
- `theme-archive-title`
- `theme-post-featured-image`
- `theme-post-excerpt`

**Fix pattern**: Replace with a standard widget + Elementor dynamic tag:

```json
{
  "widgetType": "heading",
  "settings": {
    "header_size": "h1",
    "__dynamic__": {
      "title": "[elementor-tag id=\"post-title\" name=\"post-title\" settings=\"%7B%7D\"]"
    }
  }
}
```

Standard widgets (`heading`, `text-editor`, `html`, `image`, `posts`) save and render reliably via REST.

### WordPress `the_content` filter strips H1 from post body

Inline `<h1>` tags in post body HTML are stripped during rendering (reserved for the theme template). Detection: `<h1` exists in `?context=edit` raw content but not in live HTML output.

**Fix**: Put H1 in the Elementor template (via heading widget as above) - never in the post body.

### /llms.txt at root requires a plugin

WordPress routes root-level file paths through `index.php` → 404 handler before redirection plugins can catch them. WP Media uploads + Rank Math Redirections do not work for `/llms.txt`.

**Fix**: Use a purpose-built plugin that hooks `template_redirect` early and streams the content directly. Shipping the llms.txt via `/wp-content/uploads/` URL also works if you accept the non-root path.

