# Pattern: Auto-GEO on Publish

**Problem.** GEO fixes rot. You audit a site, land 10 fixes, composite jumps from 61 to 69. Six weeks later you publish 5 new pages and the score drifts back down because nobody remembered to hand-write meta descriptions, attach FAQ schema, or keep llms.txt in sync with the new services.

**Pattern.** Split the fix set into one-shot (site-wide) vs auto-hook (per-page). Ship the auto-hook half as a platform plugin so every future page inherits the fix without human memory.

---

## The 10 fixes that moved 61 -> 69 on a real WordPress site

Reference site: a personal-brand Fractional Head of Growth site on WordPress + a B2B SaaS + Rank Math SEO + Cloudflare.

### Site-wide (one-shot, fix once)

| # | Fix | Category lift | Effort |
|---|-----|---------------|--------|
| 1 | XML sitemap at `/sitemap_index.xml` (Rank Math generator enabled) | Technical +5 | Toggle in Rank Math admin |
| 2 | `/llms.txt` served as `text/plain` at root (not WP HTML page) | Technical +5, Platform +5 | Plugin hook, see below |
| 3 | robots.txt augmented with 5 AI crawlers (OAI-SearchBot, Bytespider, Amazonbot, FacebookBot, Cohere-ai) + `Sitemap:` directive | Technical +5, Platform +10 | Plugin hook |
| 4 | Delete duplicate thin pages (`/llms/`, `/llms-txt/`, `/llm-txt/`, `/llms-full-txt/` consolidated into the single root `/llms.txt`) | Composite +3 | Delete 4 WP pages |
| 5 | Person.sameAs enriched with YouTube (or other high-authority profile URLs) | Brand Authority +2, Schema +3 | Plugin hook |

### Per-page (must auto-hook or it rots)

| # | Fix | Category lift | Auto-hook |
|---|-----|---------------|-----------|
| 6 | Meta descriptions filled on 7 pages (legal, contact, tools) | AI Citability +6 | `transition_post_status` -> synthesize from content |
| 7 | FAQPage JSON-LD on 3 service pages | Schema +10, AI Citability +5 | `rank_math/json_ld` filter -> inject when parent=services |
| 8 | Rank Math rich-snippet type defaulted to `article` on service children | Schema +2 | `transition_post_status` -> set meta |
| 9 | Canonical URL sanity check (log warnings when Rank Math defaults don't resolve) | Technical +2 | `transition_post_status` -> `error_log` |
| 10 | a B2B SaaS cache flush after any of the above (a B2B SaaS caches rendered HTML + JSON-LD) | Ambient (required for fixes 6-9 to actually show up) | `DELETE /wp-json/elementor/v1/cache` after deploy |

**Composite result: 61 -> 69 (+8).** Technical GEO 79 -> 94, Schema 79 -> 89, Platform 50 -> 65.

---

## Why you need the plugin (not a checklist)

Fixes 1-5 are persistent. Once the sitemap exists, it keeps existing. Once the duplicate pages are deleted, they're gone. Checklist discipline is sufficient.

Fixes 6-9 are per-page. Every new page a human publishes creates another gap. Manual discipline fails within 2-3 months on a live site. Plugin hooks enforce the pattern at `wp_insert_post` / `transition_post_status` / schema-filter time so the fix is always applied without operator memory.

---

## Architecture

```
                     +----------------------+
                     |  wp_insert_post      |
                     |  transition_post_status |
                     +----------+-----------+
                                |
                  +-------------+-------------+
                  |                           |
        +---------v---------+      +----------v---------+
        | Synthesize meta   |      | Default rich_snippet|
        | description if    |      | to "article" on     |
        | rank_math_        |      | /services/* pages  |
        | description empty |      +---------------------+
        +-------------------+

                     +----------------------+
                     | rank_math/json_ld    |
                     +----------+-----------+
                                |
                  +-------------+-------------+
                  |                           |
        +---------v---------+      +----------v---------+
        | Enrich Person     |      | Inject FAQPage on  |
        | sameAs on every   |      | /services/* pages  |
        | page render       |      | (override via      |
        +-------------------+      | _yg_faq_json meta) |
                                   +--------------------+
```

Every hook has an idempotency guard (skip if the target is already set / if autosave / if revision). The plugin is safe to activate on an existing site - it only fills gaps.

---

## YGM integration pattern

If you run a growth memory system (YGM or similar), log the plugin deploy as a client-genome pattern so future audits know the continuity layer is in place:

```bash
python3 -m scripts.media_audit.operator_cli ygm-learn \
  --client <client-slug> \
  --what "Auto-GEO plugin v1.1.0 deployed: auto-fills meta desc on publish, injects FAQPage on /services/* children, enriches Person.sameAs. Composite X->Y post-fix; continuity ensured for future pages."
```

Subsequent monthly re-audits (`/geo-audit` or `/geo-compare`) should see flat or improving per-page scores rather than drift, because every page published in the interval inherits the fix.

---

## Adapting the pattern

### Next.js (App Router)

- **llms.txt:** Static file at `/public/llms.txt` (Next serves it as `text/plain` automatically).
- **robots.txt:** `app/robots.ts` returning `MetadataRoute.Robots` with the 5 AI UAs + sitemap URL.
- **Auto meta description:** Page `generateMetadata()` with a fallback synthesizer when frontmatter/CMS doesn't supply one.
- **FAQPage schema:** `app/services/[slug]/page.tsx` with a `<script type="application/ld+json">` block; data from a shared helper that gates on the route segment.
- **Person.sameAs:** Root layout `generateMetadata()` returning `openGraph` + JSON-LD script tag with the full graph.

### Astro

- **llms.txt:** `public/llms.txt` (static).
- **robots.txt:** `src/pages/robots.txt.ts` endpoint returning text.
- **Meta description:** Layout component with `astro:content` frontmatter check + synthesizer fallback.
- **FAQPage schema:** `src/layouts/ServiceLayout.astro` injects `<script type="application/ld+json">` when present.

### Ghost

- Ghost doesn't expose a hook API equivalent. Options:
  - Use the Ghost Admin API to poll for new posts, compute meta desc / schema, PATCH via `codeinjection_foot`.
  - Or serve an edge worker (Cloudflare) in front of Ghost that injects `<meta name="description">` and JSON-LD when the source HTML lacks them.

The key is that the pattern - "on publish, fill gaps idempotently" - ports cleanly to any CMS that exposes a publish event or an edge layer. WordPress is the easiest target because of `transition_post_status`.

---

## Reference implementation

See `examples/wordpress/yg-geo-fixes/` in this repo for the full PHP plugin source, configuration constants, and install steps.
