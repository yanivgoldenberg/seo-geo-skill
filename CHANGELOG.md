# Changelog

All notable changes to the seo-geo skill.

Format: [version] - YYYY-MM-DD

---

## [1.6.1] - 2026-04-24

Paid-offer + trust hardening pass following the external 78/100 audit. Scoring rubric, phase count, and benchmark count were already aligned in 1.6.0; this release adds the paid audit CTA, a sample audit artifact, and a banned-endpoint policy test so the policy cannot regress silently.

### Added
- `docs/sample-paid-audit.md` - redacted version of the artifact every paid audit client receives. Same structure as production deliverables: composite score, 6-dimension breakdown, competitor benchmark, top 10 ranked fixes with impact/effort/risk, before-after diff example, 30-day implementation plan. Linked from README so buyers see the output before applying.
- `tests/test_banned_endpoints.py` - pins the Phase 17 safety contract: required bans present in `seo-geo.md`, `SECURITY.md` mirrors the list, `_is_banned()` guard + `BANNED_ENDPOINTS` constant are documented, no example under `examples/` calls a banned user-mutation endpoint.

### Changed
- README closing section replaced the generic "book a 15-min call" line with an application-only **AI Search Visibility Audit** offer: deliverables, format, credited-toward-implementation pricing, and a link to the sample audit doc. GitHub stars remain the secondary ask.

---

## [1.6.0] - 2026-04-24

Bundled audit/fix release. Addresses three converging audit reports (internal phase-by-phase, security, and external 78/100 audit). Biggest win: one canonical scoring rubric shared by the skill body AND the benchmark script, enforced by a new parity test.

### Changed - scoring rubric made canonical and consistent
- Phase 0 rubric rebalanced to **Technical 20, On-Page 15, Schema 20, GEO 25, AEO 10, E-E-A-T 10 = 100**. Previous split (20/20/20/20/10/10) under-weighted the skill's core differentiation (GEO).
- `tests/benchmark_sites.py` rewritten to use the canonical rubric with explicit `MAX_POINTS` declaration, per-dimension clamping, SSRF guard, and 14-bot AI crawler detection.
- `docs/benchmarks.md` column weights aligned; scores rebalanced across the 6 dimensions while preserving composite totals.
- Leaderboard note added explaining the "15 benchmarked, 13 public" framing.

### Changed - documentation accuracy
- "19 phases" -> "Phase 0 audit + 19 optimization phases" everywhere it was ambiguous.
- README hero replaced "closes every gap" with a credibility-safe "finds the gaps and produces a safe ranked fix plan" positioning.
- Restored "Elementor" as the named page-builder in technical WordPress sections (a prior anonymization pass had garbled 22 lines with "a B2B SaaS" while leaving `/wp-json/elementor/v1/cache` URL paths intact).
- Phase 0 audit micro-examples adjusted so every `(-N pts)` is reachable under the rubric (prior examples cited -4 and -7 which exceeded max dimension weights).
- TOC anchor fixed for Phase 4 GEO heading (slash in heading generates double-hyphen slug on GitHub).
- Benchmark leaderboard ranks renumbered after v1.5.0 removed two rows (no more 13/14/15 in a 13-site list).
- CHANGELOG v1.0.0 error-matrix row count corrected from 15 to 16.

### Added - new tests (all green)
- `tests/test_scoring_parity.py` - Phase 0 rubric in seo-geo.md must match `MAX_POINTS` in benchmark_sites.py and must sum to 100.
- `tests/test_leaderboard_integrity.py` - README and benchmarks.md leaderboards must each have 13 rows, ranks must be monotonic with valid tie-jumps, composite scores must agree across both files.
- `tests/test_identifier_hygiene.py` - skill body must not contain author name, handle, former-employer names, or YANIV_* env vars. PHP plugin must not call unserialize() in code. admin_notices must check current_user_can().

### Security - hardening pass
- Added explicit **Trust and safety boundaries** section near the top of seo-geo.md: public-hosts-only SSRF guard, banned endpoints, log redaction rules, author-identifier non-injection, scope discipline. Seven non-negotiable rules.
- Expanded Phase 17 banned endpoint list: user creation, settings mutations (siteurl/home/admin_email), plugin/theme management, token/JWT/API-key rotation.
- Rewrote Phase 17 reference Python adapter: `_is_banned()` pre-check, SHA-256 body hash in audit log, no response body logged, no credential logging.
- Phase 15 WP hardening snippet no longer prints `r.text` (WordPress error bodies often echo auth data).
- Phase 15 AI crawler robots template now covers 14 bots (added Amazonbot, Meta-ExternalAgent, FacebookBot, OAI-SearchBot, DuckAssistBot).
- Phase 16 bulk-media update snippet gained try/except, 429 retry-with-Retry-After, polite pacing, and fail-closed logging without bodies.
- `tests/benchmark_sites.py` now validates every target URL against private/loopback/link-local/reserved IP ranges before sending a request.
- PHP plugin (`examples/wordpress/yg-geo-fixes/yg-geo-fixes.php` bumped to 1.2.0):
  - Removed `unserialize()` from three call sites; constants now use plain PHP 7+ array literals.
  - Added `current_user_can('activate_plugins')` gate on admin_notices.
  - URL validation via `filter_var(..., FILTER_VALIDATE_URL)` on sameAs inputs.
  - UA strings sanitized before being written into robots.txt.
  - `esc_url_raw()` on sitemap URL; `(int) $crawler_count` cast in output.
  - Crawler list expanded to 14 bots.

## [1.5.2] - 2026-04-24

Zero-identifier pass on the skill body. Previous versions baked author persona into schema examples and env var names, which installers would unknowingly copy into their own sites.

### Changed
- seo-geo.md: replaced author-specific bio examples with `{placeholder}` templates across Phase 2 (title patterns), Phase 6 (E-E-A-T AFTER example + fastest-win block), Phase 16 (entity anchoring example), and Phase 17 (Product schema example)
- Env var names in WP hardening code: `YANIV_WP_APP_PASSWORD` -> `WP_APP_PASSWORD`, `YANIV_WEBSITE_URL` -> `SITE_URL`, `WEBSITE_WP_ADMIN_USER` -> `WP_USER`
- Phase 15 security example: `/author/yaniv-goldenberg/` -> `/author/{admin-slug}/`
- Author byline inside the skill body replaced with "Author: see repo README" pointer (full credit remains on GitHub README)
- Footer "Author" block trimmed to a neutral reference; no persona copy, no proof stats, no contact links
- Version bumped 1.5.1 -> 1.5.2

### Security scan (performed during this release)
- No hardcoded secrets (sk-*, ghp_*, AKIA, db URLs)
- No dangerous shell ops (rm -rf, eval, exec, shell_exec, --no-verify, DROP TABLE)
- PHP reference plugin (250 lines): zero user-input surfaces; `unserialize()` operates only on in-file constants (no injection path)

### Hardening recommendation (not blocking)
- Replace `unserialize(CONSTANT)` with plain `array(...)` in examples/wordpress/yg-geo-fixes to remove the code smell (serialized arrays in PHP constants)

## [1.5.1] - 2026-04-24

Consistency fix. v1.5.0 removed elementor.com and riverside.fm from the leaderboard but left README/seo-geo.md references at "15 top SaaS sites". This aligns every surface to 13.

### Changed
- README leaderboard: dropped elementor.com (rank 7) and riverside.fm (rank 12) rows, renumbered
- README hero and version/benchmark badges: 15 -> 13
- seo-geo.md frontmatter version 1.5.0 -> 1.5.1, description now reads "13 top SaaS sites"
- docs/benchmarks.md title and narrative: 15 -> 13
- Corresponding WP blog post (yanivgoldenberg.com/blog/claude-code-seo-geo-skill) title, excerpt, and FAQ updated via REST API (FAQ also fixed stale "15 sequential phases" -> "19")

## [1.5.0] - 2026-04-24

Privacy release. Removed all references to past employers and current clients. Anonymized proof stats.

### Changed
- Removed Elementor, Riverside.fm, cnvrg.io, Intel, and current client names from all docs
- Anonymized case study (yanivgoldenberg.com entry retained as sole self-benchmark)
- Bio now reads: 15+ years operating growth, $100M+ ad budgets managed, multiple B2B SaaS scaled to $20M+ ARR
- Dropped elementor.com and riverside.fm from public benchmark leaderboard (potential conflict of interest as past employers)
- Plugin yg-geo-fixes v1.3.0 deployed with scrubbed llms.txt content
- Homepage Rank Math meta description rewritten to anonymized proof

### Removed
- Specific company names in proof statements across README, seo-geo.md, case-studies, CHANGELOG references

### Added
- Nothing new; this is purely a privacy/positioning pass
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
- `docs/patterns/auto-geo-on-publish.md` - architectural pattern doc: 10 fixes that moved composite GEO 61 -> 69 on a real WordPress + a B2B SaaS + Rank Math site, split into one-shot vs auto-hook; YGM integration pattern; Next.js / Astro / Ghost adaptation guide

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
- Phase 14: Debugging and Error Recovery (16-row error matrix, curl verification, cache clearing)
- `--verify` self-test with pass/fail table
- `--page <url>` single-page audit mode
- SPA/JS-rendered site detection and fallback strategy
- Decision tree for phase selection
- Common Issues table (10 issues)
- Platform quick reference (7 platforms: WordPress, Shopify, Webflow, Next.js, Ghost, Static HTML)
- Maintenance schedule
- PolyForm Noncommercial 1.0.0 license
