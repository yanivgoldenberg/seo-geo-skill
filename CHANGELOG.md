# Changelog

All notable changes to the seo-geo skill.

Format: [version] - YYYY-MM-DD

---

## [1.4.0] - 2026-04-24

Public benchmark release. Replace self-only case study with 15-site public leaderboard.

### Added
- docs/benchmarks.md: 15 top SaaS sites scored (anthropic.com, stripe.com, linear.app, vercel.com, figma.com, notion.so, supabase.com, mercury.com, elementor.com, riverside.fm, resend.com, ramp.com, fly.io, planetscale.com, yanivgoldenberg.com)
- docs/benchmarks.json: raw scoring data
- tests/benchmark_sites.py: reproducible scoring script (2 minutes to rerun)
- docs/compare.md: honest comparison with AgriciDaniel/claude-seo, aaron-he-zhu/seo-geo-claude-skills, claude-seo.md
- README rewritten: benchmark leaderboard above the fold, hard 10-second CTA at top
- All files swept for em dashes (brand voice: no em dashes)

### Changed
- Version bumped 1.3.0 -> 1.4.0
- README version badge + description updated
- Hero narrative: 53% of top SaaS sites have no llms.txt, 73% have broken schema, anthropic.com itself scores 30/100

## [1.3.0] - 2026-04-24

100/100 polish release. Four new phases, CI, case study, real-world score badge.

### Added
- Phase 17: Dry-run safety gates (`--apply` opt-in, banned endpoint list, audit log)
- Phase 18: Multi-platform adapters (WordPress, Shopify, Webflow, Next.js) with per-platform code snippets + parity matrix
- Phase 19: Competitor benchmarking (head-to-head score + gap-closure plan)
- Table of Contents at top of seo-geo.md linking to all 19 phases
- GitHub Actions CI: skill metadata validation, JSON-LD fixture validation, live endpoint check, link check via lychee
- `tests/` directory with 3 Python test scripts
- `docs/case-studies/yanivgoldenberg.com.md` (61 to 94 score delta with breakdown)
- README: CI + score badges, Real-world results table

### Changed
- Skill frontmatter description updated to reflect 19 phases
- Version bumped 1.2.0 -> 1.3.0
- README version badge 1.0.0 -> 1.3.0

## [Unreleased]

### Added
- `examples/wordpress/yg-geo-fixes/` - reference WordPress plugin implementing the site-wide + per-page GEO pattern (serves `/llms.txt`, patches robots.txt with 5 AI UAs + Sitemap, enriches Person.sameAs, auto-fills Rank Math meta descriptions on publish, injects FAQPage schema on `/services/*` children)
- `docs/patterns/auto-geo-on-publish.md` - architectural pattern doc: 10 fixes that moved composite GEO 61 -> 69 on a real WordPress + Elementor + Rank Math site, split into one-shot vs auto-hook; YGM integration pattern; Next.js / Astro / Ghost adaptation guide

## [1.2.0] - 2026-04-24

Field Patterns appendix added. Sourced from production deployment on yanivgoldenberg.com brand system launch.

### Added
- Phase 16: Field Patterns from Production Deployments (6 patterns)
  1. Entity anchoring across every surface (verbatim phrase repeated across meta/schema/llms.txt/alt/bio)
  2. LLM-grade image metadata (4 fields per image, not just alt - title/alt/caption/description with bulk WP REST snippet)
  3. Plugin-as-SEO-filter (durable code-level overrides surviving UI edits)
  4. llms.txt + llms-full.txt duo (short fast-pass + long deep-read)
  5. Never rename slugs in bulk (301 per-file rule)
  6. Legacy asset purge after rebrand (WP site_icon cleanup checklist)

### Changed
- Description metadata updated to reflect 6 new patterns
- Version bumped 1.1.0 -> 1.2.0

---
## [1.0.0] - 2026-04-18

Initial release.

### Added
- Phase 0: Audit (100-pt scoring rubric, 6 dimensions)
- Phase 1: Technical SEO (robots.txt, canonical, sitemap, mobile)
- Phase 2: On-Page SEO (titles, meta, OG tags, H1 hierarchy)
- Phase 3: Schema (16 types: Person, Organization, Product, Service, Article, FAQPage, HowTo, BreadcrumbList, Review, WebSite, ProfilePage, DefinedTerm, SpeakableSpecification, LocalBusiness, SoftwareApplication, VideoObject)
- Phase 4: GEO - LLM/generative engine optimization (llms.txt, llms-full.txt, entity signals, sameAs, AI crawler access for 9 bots)
- Phase 5: AEO - Answer engine optimization (Speakable schema, direct-answer content)
- Phase 6: E-E-A-T (author schema, trust signals, credentials, external citations)
- Phase 7: Content Strategy (topical authority, skyscraper method, content briefs, SERP features)
- Phase 8: Core Web Vitals (LCP, INP, CLS - measurement and platform-specific fixes)
- Phase 9: Internal Linking (hub-and-spoke, PageRank flow, anchor text audit)
- Phase 10: Content Decay (refresh strategy, GSC impression tracking)
- Phase 11: Programmatic SEO (template + data approach, quality gates)
- Phase 12: Video SEO (VideoObject schema, YouTube optimization, video sitemap)
- Phase 13: International SEO / Hreflang (hreflang tags, x-default, locale detection)
- Phase 14: Debugging and Error Recovery (15-row error matrix, curl verification, cache clearing)
- `--verify` self-test with pass/fail table
- `--page <url>` single-page audit mode
- SPA/JS-rendered site detection and fallback strategy
- Decision tree for phase selection
- Common Issues table (10 issues)
- Platform quick reference (7 platforms: WordPress, Shopify, Webflow, Next.js, Ghost, Static HTML)
- Maintenance schedule
- PolyForm Noncommercial 1.0.0 license
