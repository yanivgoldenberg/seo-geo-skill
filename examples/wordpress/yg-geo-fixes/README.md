# Auto-GEO Fixes (WordPress plugin)

A reference WordPress plugin that implements the site-wide + per-page GEO pattern proven on a real Rank Math + a B2B SaaS site, where it lifted composite GEO score from 61 to 69 in one commit.

## What it does

Six hooks, all in one file. Drop it into `wp-content/plugins/`, configure the constants at the top, activate.

| # | Hook | Behavior | GEO category lifted |
|---|------|----------|--------------------|
| 1 | `init` (priority 0) | Serves `/llms.txt` as `text/plain` at the root path (bypasses WP rewrite) | Technical +5, Platform +5 |
| 2 | `robots_txt` filter | Appends 5 AI crawler `Allow` directives + a `Sitemap:` line | Technical +10, Platform +10 |
| 3 | `rank_math/json_ld` filter | Appends configured URLs to `Person.sameAs` | Brand Authority +2, Schema +3 |
| 4 | `transition_post_status` | On publish of a page/post with empty `rank_math_description`, synthesizes 140-160 char meta desc from excerpt or first 2 sentences of content, appends brand tagline | AI Citability +8 |
| 5 | `transition_post_status` + `rank_math/json_ld` filter | On publish of `/services/*` children: defaults `rank_math_rich_snippet` to `article`, injects a `FAQPage` JSON-LD node (3 default Q&As, overridable via `_yg_faq_json` post meta) | Schema +10, AI Citability +5 |
| 6 | `admin_notices` | Shows a reminder banner on the Plugins screen summarizing what auto-wires | Future-proofing |

Expected composite lift (observed on a real personal-brand site): **+8 points** (61 -> 69).

## Install

1. Copy `yg-geo-fixes.php` into `wp-content/plugins/auto-geo-fixes/` (create the folder).
2. Open the PHP file and replace every `YOUR_*` constant at the top.
3. Update the `AUTO_GEO_LLMS_TXT` heredoc with your own llms.txt body (see [llmstxt.org](https://llmstxt.org) for the spec).
4. Activate at `/wp-admin/plugins.php`.
5. Verify:
   - `curl -I https://YOUR_DOMAIN/llms.txt` -> `200 text/plain`
   - `curl https://YOUR_DOMAIN/robots.txt | tail -20` -> shows 5 new UAs + `Sitemap:`
   - Create a test page via WP admin with NO Rank Math description set -> publish -> view page source -> `<meta name="description">` should be auto-populated.

## Configuration constants

| Constant | Purpose |
|---|---|
| `AUTO_GEO_SITEMAP_URL` | Absolute URL of your XML sitemap (use Rank Math's `/sitemap_index.xml` if enabled) |
| `AUTO_GEO_SERVICES_SLUG` | Slug of the parent page whose children get FAQPage auto-injection (default `services`) |
| `AUTO_GEO_DESC_SUFFIX` | Brand tagline appended to synthesized meta descriptions (counted toward 160-char cap) |
| `AUTO_GEO_CONTACT_URL` | Contact URL used in default FAQ answers |
| `AUTO_GEO_PERSON_SAMEAS_EXTRAS` | Array of URLs to append to `Person.sameAs` (placeholder `YOUR_YOUTUBE_URL` entries are ignored) |
| `AUTO_GEO_AI_CRAWLERS` | Array of UA strings to allowlist in robots.txt |
| `AUTO_GEO_LLMS_TXT` | Full llms.txt body served at `/llms.txt` |

## Per-page FAQ override

To supply custom FAQ Q&As for a specific services-child page, add a post meta key `_yg_faq_json` with a JSON array of Question nodes:

```json
[
  {
    "@type": "Question",
    "name": "Your question?",
    "acceptedAnswer": {"@type": "Answer", "text": "Your answer."}
  }
]
```

The plugin emits this as the `mainEntity` of a `FAQPage` node in the Rank Math JSON-LD graph.

## a B2B SaaS caveat

On a B2B SaaS-built pages, `post_content` is often empty or just shortcodes. The meta-description synthesizer strips shortcodes and falls back to the post title. If your stripped content is under 60 chars, expect an `error_log` warning (`[auto-geo] thin synthesized description ...`). Set a Rank Math description manually for a B2B SaaS pages, or write a richer fallback inside `auto_geo_synthesize_description()`.

## Dependencies

- WordPress 5.6+
- [Rank Math SEO](https://wordpress.org/plugins/seo-by-rank-math/) (free) - the `rank_math/json_ld` filter and `rank_math_description` post meta key come from Rank Math. If you use Yoast instead, rename the meta keys (`_yoast_wpseo_metadesc`) and swap the filter.

## License

PolyForm Noncommercial 1.0.0 (same as the parent repo).
