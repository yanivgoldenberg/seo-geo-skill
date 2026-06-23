# Next.js (App Router) GEO adapter

Minimal, runnable example of the seo-geo skill's Phase 18 Next.js adapter. Drop these into a Next.js 14+ App Router project (`app/` directory) and replace the placeholder values.

## Files

| File | Serves | Notes |
|------|--------|-------|
| `app/robots.ts` | `/robots.txt` | Splits search/answer crawlers from training crawlers. Allowing GPTBot (training) does not make you visible in ChatGPT search; that needs OAI-SearchBot + ChatGPT-User. |
| `app/sitemap.ts` | `/sitemap.xml` | Build `ROUTES` from your real routes (filesystem, CMS, or DB). |
| `app/llms.txt/route.ts` | `/llms.txt` | Served as `text/plain` with `X-Robots-Tag: all`. Low-cost hygiene; no AI search engine consumes it as of 2026. |
| `app/components/JsonLd.tsx` | inline JSON-LD | XSS-safe (`<` escaped). Never pass untrusted user content. |

## Setup

1. Copy the files into your project's `app/` directory.
2. Replace `https://yoursite.com` and the placeholder content with your real values.
3. Wire `<JsonLd>` into pages that need schema (see the usage comment in the component).
4. Verify after deploy:
   ```bash
   curl -sI https://yoursite.com/llms.txt | grep -i content-type   # text/plain
   curl -s  https://yoursite.com/robots.txt | grep -i oai-searchbot
   curl -s  https://yoursite.com/sitemap.xml | head
   ```

For the full audit and the other platform adapters (WordPress, Shopify, Webflow), see the main skill: [`seo-geo.md`](../../seo-geo.md).
