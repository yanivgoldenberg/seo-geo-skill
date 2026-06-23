# Changelog

All notable changes to the seo-geo skill.

Format: [version] - YYYY-MM-DD

---

## [Unreleased]

### Changed (llms.txt re-weighting + leaderboard re-run - Bucket C2)
- **Re-weighted GEO scoring**: llms.txt dropped from 12 to 3 of 25 GEO points (no AI search engine consumes it as of 2026); the freed points moved to entity presence/sameAs (7), citation-magnet content (6), and AI search-crawler access (6). GEO now sums to exactly 25 (was over-subscribed at 30). Updated in `benchmark_sites.py`, `BENCHMARK_CHECKS`, Phase 0 rubric, and `docs/SCORING.md`.
- Also fixed two scorer bugs surfaced in the audit: the `sameAs` GEO check used a fragile operator-precedence expression, and the Link-header check was dead code (never matched).
- **Re-ran the full 61-site leaderboard under the new rubric, dated 2026-06-23.** Regenerated `state-of-ai-search-2026.{json,csv,md}`, the history snapshot, `CARRIED_BASELINE`, the README leaderboard/prose, the case study, and the brand banners. Headline shifts (mostly 2 months of web drift, not the reweight): 67% fail -> 56%; mean 49.4 -> 54.3; yanivgoldenberg.com 97 -> 92 (still rank 1); Railway 0 -> 67 (they added llms.txt + content since April). OpenAI and Perplexity still 7/100 each.

### Changed (scoring integrity - Bucket C1, no published score moves)
- `docs/SCORING.md` now honestly separates the **manual-audit rubric** from the **automated benchmark**. Removed the false "identical / no methodology drift" claims; documented exactly what `benchmark_sites.py` scores (crawl-observable proxies) and which criteria are manual-audit-only (Core Web Vitals, broken-link crawl, GSC submission, keyword placement, validation errors, Wikidata verification, proof points, external links, ...). Stated plainly that the GEO checks are over-subscribed (sum 30, clamped to 25), over-weighting llms.txt.
- Added a `BENCHMARK_CHECKS` table to `benchmark_sites.py` documenting every observable check and its points; `test_scoring_parity.py` now pins it against `docs/SCORING.md` so documented scoring cannot silently drift from the scorer (previously only the six bucket totals were checked).
- README: corrected the "no methodology drift" line to reflect that the benchmark scores the crawl-observable subset.
- Deferred (Bucket C2): the llms.txt re-weighting (which lowers published scores) remains tracked in `docs/proposals/scoring-reliability.md`.

## [1.12.0] - 2026-06-23

Correctness, safety, and freshness release. First update that improves the installed skill itself (not just the repo), driven by a four-dimension audit (freshness, dogfood, coverage, accuracy).

### Fixed (correctness + safety)
- **SSRF guard was bypassable** (`tests/benchmark_sites.py`): `fetch()` followed redirects without re-validating each hop, so a public URL could 302 to cloud-metadata or localhost. Now validates every hop and stops at the first private/loopback/link-local target.
- **`_is_banned()` only blocked POST/DELETE** (`seo-geo.md` Phase 17): `PUT`/`PATCH /wp/v2/users/{id}` bypassed the safety guard. PUT/PATCH are now treated as writes.
- **Malformed JSON-LD**: `mainEntityOfPage` used `"id"` instead of `"@id"` (dropped on every Article).
- **Invalid schema advice**: "add `dateModified`/`datePublished` to every schema block" is invalid on non-CreativeWork types (Person, Organization, Product, FAQPage, ...); now scoped to CreativeWork.
- **Plugin corrupted Hebrew/UTF-8 meta descriptions** (`examples/wordpress/yg-geo-fixes`): byte-based `substr()`/`strlen()` truncated mid-character; switched to `mb_*`.
- **Plugin injected invented FAQPage schema** with placeholder Q&A not visible on the page (Google manual-action risk); now only emits FAQPage when real Q&A content is provided.
- **`rel` mismatch**: the scorer credited `rel="describedby"` but the skill taught `rel="llms-txt"`/`"llms"`, so sites that followed the skill scored 0. Standardized on `rel="llms-txt"`; scorer accepts both.

### Added / Changed (freshness + coverage)
- Refreshed stale GEO stats with dated, sourced 2026 figures: top-10 dependency for AI Overviews (now ~38-54%, down from ~76-92%), and fixed the mis-attributed "11% overlap" stat (ChatGPT vs Perplexity, not vs AI Overviews).
- Added **Google AI Mode + query fan-out** to per-platform intelligence (a 2025 citation surface the skill omitted).
- Split robots.txt AI crawlers into **search/answer vs training** classes and added the 2025 search bots (`OAI-SearchBot`, `ChatGPT-User`, `Claude-SearchBot`, `Perplexity-User`, ...). Flagged the #1 mistake: allowing GPTBot but not OAI-SearchBot.
- Re-dated the GEO paper (Aggarwal et al., Nov 2023 / KDD 2024), corrected +40% to +41%, flagged the unverified "2.1x" definition-opening stat.
- Added the missing **`ItemList`** schema template (listicle / "best X" / alternatives - the most AI-cited format the skill routes pages to).
- Added **shippingDetails + hasMerchantReturnPolicy** to the Product schema (Google merchant-listing requirements).
- Added a runnable **`examples/nextjs/`** App Router adapter (robots, sitemap, llms.txt route, JsonLd component) backing the multi-platform claim.
- Reconciled the schema count (now 18 types), cross-listed `ItemList`/`VideoObject`, and softened the "same patterns, four CMS targets" claim to reflect WordPress as the reference adapter.

### Known / deferred (see `docs/proposals/scoring-reliability.md`)
- The scoring rubric documented in `seo-geo.md` and `docs/SCORING.md` diverges from the heuristics in `tests/benchmark_sites.py` (the parity test only checks dimension totals, not sub-checks), and `llms.txt` is weighted 7/25 GEO points despite no AI search engine consuming it as of 2026. Fixing either re-scores the published 94/100 and the 61-site leaderboard, so it is deferred to a dedicated release.

### Repo hygiene (also in this release)
- README version badge corrected; CI runs the full `pytest` suite (persona-hygiene + banned-endpoint guards now block regressions); case study/pattern docs scrubbed of operational specifics; brand banners refreshed (dark/cyan/Inter, reproducible via `scripts/build_brand_banners.py`); test suite ruff-clean.

## [1.11.0] - 2026-06-16

Headless content-model release. Adds the two highest-leverage patterns for scaling SEO + GEO on dynamic, JS-rendered sites: a rendering contract that keeps dynamic blocks citable by AI engines, and a content-model archetype map for programmatic SEO at scale.

### Added
- **Rendering contract for JS-built feeds and cards** (seo-geo.md, Phase 4 GEO): SSR-plus-hydrate over client-only fetch, a pinned crawlable seed that doubles as the live-fetch fallback, `ItemList` JSON-LD only for SSR-visible items (anti-cloaking), thin/empty-state gating, real `<a href>` links with sponsored disclosure, and locale parity. Includes the one-line curl test for whether an AI crawler can see a dynamic block.
- **Content-model archetypes** (Phase 11 Programmatic SEO): an 8-archetype map (comparison, alternative, integration, listicle, use-case, glossary, guide, customer story) with URL patterns and primary schema types; the headless CMS-as-structure / front-end-as-design pattern with a composable section builder and per-type block gating; and a global singleton for publisher (Organization/WebSite) identity referenced by every page `@graph`.
- **Deploy discipline for generated artifacts** (Phase 11): data-source-as-truth, stage-validate-atomic-rename, OPcache invalidation, and build-time key-uniqueness assertions.

### Changed
- seo-geo.md version bumped 1.10.0 -> 1.11.0.

## [1.10.0] - 2026-06-05

The heavy-lifting release. The skill now generates deployable fixes (not just reports), the benchmark re-scores itself monthly, the scorer samples deep pages so headline claims survive re-crawls, and the README proves the output with a real reproducible terminal capture.

### Added
- **Generate fixes as files** (seo-geo.md, Phase 4): the skill now emits ready-to-deploy `llms.txt`, `llms-full.txt`, and JSON-LD schema files built from the audited site's real data into `./seo-geo-output/{domain}/`, with output templates and a placeholder-regex validation gate.
- **Research-backed citation findings** (Phase 4): Princeton/Georgia Tech/IIT Delhi 2024 GEO findings as an actionable table (+40% statistics, up to +115% authority quotes, +30% fluency, 2.1x definition openings, 134-167 word extraction window).
- **Per-platform selection intelligence** (Phases 4-5): which optimizations move Google AI Overviews vs ChatGPT vs Perplexity vs Gemini vs Bing Copilot (only ~11% of domains are cited by both ChatGPT and AIO; 92% of AIO citations come from top-10 organic pages).
- `.github/workflows/benchmark.yml`: monthly self-refreshing benchmark. Re-scores the 61 sites on the 1st of each month and commits a dated CSV to `docs/state-of-ai-search-history/`. The leaderboard is now a moving, self-auditing proof engine.
- `docs/assets/benchmark-terminal.png` + `scripts/benchmark_demo.py` + `scripts/build_terminal_capture.py`: real captured terminal output (yanivgoldenberg.com 94/100, openai.com 7/100, six-dimension breakdown) embedded in the README; one command reproduces it.
- `tests/test_deep_link_discovery.py`: tests for deep-page link discovery.

### Changed
- `tests/benchmark_sites.py`: multi-page sampling. `score(site, pages=4)` discovers up to 3 same-host deep pages (docs/blog/product/about preferred) and scores On-Page, Schema, and AEO best-of across them; Technical, GEO, and E-E-A-T stay homepage-derived. `pages=1` default preserves single-page behavior byte-for-byte; every discovered URL passes the same SSRF public-host guard.
- `scripts/run_state_of_ai_search_2026.py`: gained `--out` for dated history snapshots; the benchmark now runs with `pages=4`.
- `docs/SCORING.md`: documented the multi-page sampling rule.

## [1.9.1] - 2026-06-05

Proof + reproducibility release. Reconciles every score claim to the latest live re-run, hardens the leaderboard against drift, and ships the AI Engine Citation Grid.

### Added
- `docs/SCORING.md`: the canonical 100-point rubric extracted to a single shared spec (skill body, modular geo-* skills, and `tests/benchmark_sites.py` all point here).
- `docs/assets/citation-grid.png` + `scripts/build_citation_grid.py`: 4-engine citation proof (Google AI Overview, ChatGPT, Bing-LinkedIn AI, Hebrew AI) for "best fractional CMO Israel", each citing the reference deployment first. Reproducible composer script.
- `tests/test_sites_61.py`: pins the 61-site leaderboard roster so the benchmark set cannot drift silently.
- `scripts/run_state_of_ai_search_2026.py`: one-command reproduction of the State of AI Search 2026 report.
- CI gate: no em dashes in markdown (brand voice), `.github/workflows/ci.yml`.

### Changed
- README score claim reconciled from 97/100 to **94/100 on the latest live re-run (2026-06-05)**, dated and falsifiable ("run it yourself and you get today's number").
- `tests/test_leaderboard_integrity.py` repaired: README/benchmarks agreement restored, anti-drift assertions pass (24/24).
- `seo-geo.md`: rubric section now points to `docs/SCORING.md` as the canonical spec; version 1.9.0 -> 1.9.1.
- CHANGELOG backfilled for 1.7.0 and 1.8.0 (released 2026-04-24, previously undocumented).

## [1.9.0] - 2026-05-29

Production deployment session on a WordPress + Elementor Pro site surfaced eight new gotchas not covered by v1.8.0. All added to the existing "Elementor Pro + REST API Gotchas" and "Common Issues and Fixes" sections. No new phases; additive only.

### Added

- **Kit global link color bleeds into anchor-styled buttons** - `link_normal_color` emits `.elementor-kit-N a` at specificity (0,1,1), outranking single-class button CSS. Fix: kit `custom_css` override at (0,2,1) including `:hover`.
- **`-webkit-background-clip:text` + webfont FOUT = frozen glyphs** - clipped text does not re-raster when webfont swaps in; pure CSS cannot fix it. Fix: self-host font or `font-display:block`; fallback: `document.fonts.ready` JS re-raster in HTML widget.
- **Elementor kit `custom_js` is stored but never output** - kit custom JS has no frontend render path; use HTML widget instead. Compound gotcha: `_elementor_page_settings` must be sent as a dict (not `json.dumps`), otherwise 400 `rest_invalid_type`. Verify live `post-N.css` / HTML after every kit write.
- **`wpautop` mangles raw HTML cards in `post_content`** - WordPress `the_content` filter wraps lines in `<p>` and injects `<br>`, breaking hand-authored block markup. Fix: remove filter per page ID, author wpautop-safe HTML, or move content to Elementor HTML widget.
- **`_elementor_data` bad write nulls the page** - malformed write leaves invalid JSON; Elementor renders a narrow fallback. Prevention: backup, write, immediately read back and `json.loads()` the stored value before claiming done.
- **Full-bleed padding formula collides with theme-capped container** - `calc((100vw - 1200px)/2 + 32px)` assumes viewport-width ancestor; a theme `max-width` on `<main>` makes the formula go negative. Fix: walk ancestor width chain before applying; set container width in kit.
- **Hidden text encodings evade grep** - WordPress and Elementor store URLs, emails, and non-ASCII text as HTML numeric entities (`&#NNNN;`) or JSON `\uXXXX` escapes. Plain-text grep misses them. Fix: search all three representations; use `html.unescape()` before regex matching.
- **Kill default visited-link purple** - browser UA stylesheet wins without an explicit reset. Fix: kit global link color + `:where(a:visited){color:inherit}` at (0,0,0) specificity.

### Changed

- seo-geo.md version bumped 1.8.0 -> 1.9.0.
- "Common Issues and Fixes" table: 7 new rows added for the above gotchas.

---

## [1.8.0] - 2026-04-24

Phase 20 release plus the OpenAI live teardown. Adds the 20th optimization phase, a reproducible 7/100 case study on openai.com, and a production-usage section. README badge and `seo-geo.md` frontmatter both moved to 1.8.0; this entry closes the CHANGELOG gap that lagged at 1.6.1.

### Added
- Phase 20: LLM Extractability Polish (LLM Summary block, claims table, cite block, glossary, raw-data download, self-consistency check). Opt-in via `--apply` like Phases 15-19.
- `docs/case-study-openai.md`: openai.com scored 7/100 on the canonical rubric, with the exact reproducibility snippet and a 7 to 70 projected fix plan. Every number reproducible via `tests/benchmark_sites.py`.
- `docs/state-of-ai-search-2026.csv`: machine-readable download of the 61-site leaderboard alongside the existing `.md` and `.json`.
- README "Seen at / Running in production" section: yanivgoldenberg.com at 97/100, the 61-site benchmark, and the public reproducible methodology script.

### Changed
- Phase count moved from 19 to 20 across `seo-geo.md` (TOC + phase headings), `docs/compare.md` (Phases row 19 to 20), and `docs/case-study-openai.md` (Phase 1-19 to Phase 1-20). Phase 19 "Competitor benchmarking" remains a phase name; historical CHANGELOG entries left intact.
- README hero de-heroed yanivgoldenberg.com and now leads with the bottom-3 leaderboard (openai.com 7, perplexity.ai 7, railway.app 0) so the proof is the failure data, not the self-benchmark.
- `seo-geo.md` frontmatter version 1.7.0 -> 1.8.0; README version badge 1.7.0 -> 1.8.0.

## [1.7.0] - 2026-04-24

Public benchmark expansion. Grows the leaderboard from 13 to 61 top SaaS and AI sites and softens the llms.txt framing to match what Google has publicly stated.

### Added
- `docs/state-of-ai-search-2026.md` + `docs/state-of-ai-search-2026.json`: State of AI Search Visibility 2026 report. 61 SaaS and AI sites scored on the canonical 100-point rubric. 67% scored 60 or below; mean 49.4/100; openai.com and perplexity.ai both 7/100; railway.app 0.

### Changed
- README bio rewritten present-tense; added the license use-case matrix (run-on-own-site vs client-resale vs commercial).
- llms.txt framing softened: positioned as entity hygiene, not a guaranteed ranking lever, with the note that Google has stated no special file is required for AI Overviews. The data point (sites that publish it pair with the strongest GEO scores) is kept as correlation, not a guarantee.
- `seo-geo.md` frontmatter version 1.6.1 -> 1.7.0; README version badge and description updated to "61 top SaaS and AI sites".

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
