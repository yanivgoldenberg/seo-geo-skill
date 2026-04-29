# Case study: yanivgoldenberg.com

One-session optimization using the seo-geo skill v1.3.0.

**Site:** https://yanivgoldenberg.com (Fractional Head of Growth consultancy)
**Stack:** WordPress + a B2B SaaS + Rank Math + Cloudflare
**Session date:** 2026-04-24
**Operator:** Yaniv Goldenberg

## Score delta

| Dimension | Before | After | Delta |
|---|---|---|---|
| Technical SEO | 72 | 95 | +23 |
| On-page SEO | 58 | 92 | +34 |
| Schema | 40 | 98 | +58 |
| GEO (LLM citation) | 55 | 96 | +41 |
| AEO (answer engine) | 48 | 88 | +40 |
| E-E-A-T | 68 | 92 | +24 |
| **Composite** | **61** | **94** | **+33** |

## What moved the score

1. **Entity anchor** rolled out across 7 surfaces (Phase 16, Pattern 1)
2. **Plugin-as-SEO-filter** pattern - single yg-geo-fixes v1.2.0 plugin hardcodes homepage title, meta, OG image, schema logo, favicon, theme-color, and AI-crawler robots rules (Phase 16, Pattern 3)
3. **Full brand system replaced legacy favicon** - WP Customizer site_icon removed, legacy cropped-favicon-* media purged, new apple-touch-icon + 16/32 favicons + favicon.ico served from plugin directory (Phase 16, Pattern 6)
4. **Media library 4-field metadata** applied to all 18 items via REST batch (Phase 16, Pattern 2)
5. **llms.txt + llms-full.txt duo** served with X-Robots-Tag: all (Phase 4 + Phase 16, Pattern 4)
6. **Organization + Person schema** augmented with logo ImageObject, image, and sameAs including YouTube (Phase 3)
7. **Homepage hero tagline "From Traffic to Revenue"** inserted between H1 and subtitle (entity reinforcement)

## What the skill did NOT touch

- Admin credentials (banned per Phase 17 safety gates)
- Post slugs (Phase 16, Pattern 5 rule: never rename in bulk)
- a B2B SaaS header/footer HTML beyond scoped insertion
