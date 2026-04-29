# Sample AI Search Visibility Audit

This is a redacted version of the artifact every paid audit client receives. Names and URLs are replaced with `acme.com` to protect the real engagement; scoring, structure, and fix list format are identical to what you would get.

---

## 1. Executive summary

**Site audited:** `acme.com` (post-PMF B2B SaaS, ~180K monthly organic visits)
**Audit date:** 2026-03-14
**Composite AI Search Readiness score: 54 / 100** (invisible-to-AI band, below 60)

| Dimension | Score | Max | Verdict |
| --- | ---: | ---: | --- |
| Technical SEO | 16 | 20 | Strong base, 1 canonical leak |
| On-Page SEO | 11 | 15 | Title tags thin on programmatic pages |
| Schema / Structured Data | 6 | 20 | No Organization, no Person, no FAQ |
| GEO / LLM Optimization | 9 | 25 | No `/llms.txt`, implicit crawler allow |
| AEO / Answer Engine | 5 | 10 | No answer-first blocks, no Speakable |
| E-E-A-T | 7 | 10 | Author bios present, no schema backing |
| **Total** | **54** | **100** | |

The three highest-impact fixes (below) recover an estimated 28 composite points in roughly 6 hours of dev time.

---

## 2. Competitor benchmark (same rubric, same day)

| Rank | Site | Composite | Biggest gap |
| ---: | --- | ---: | --- |
| 1 | `competitor-a.com` | 81 | Thin FAQ schema |
| 2 | **`acme.com`** | **54** | No schema, no llms.txt |
| 3 | `competitor-b.com` | 48 | No Organization schema |
| 4 | `competitor-c.com` | 42 | Blocks GPTBot in robots |

Competitor A is the only one in the top band. They beat you on schema depth and entity consolidation, not content. The gap closes inside one Implementation Sprint.

---

## 3. Top 10 ranked fixes

Each fix lists **impact** (composite points), **effort** (developer hours), and **risk** (low / med / high). Sorted by points per hour.

| # | Fix | Impact | Effort | Risk | Points / hr |
| ---: | --- | ---: | ---: | :---: | ---: |
| 1 | Publish `/llms.txt` + `/llms-full.txt` at root | +10 | 1h | low | 10.0 |
| 2 | Add `Organization` + `Person` JSON-LD on homepage + about | +8 | 2h | low | 4.0 |
| 3 | Explicit AI-crawler allow block in `robots.txt` (GPTBot, ClaudeBot, PerplexityBot, Google-Extended) | +4 | 0.5h | low | 8.0 |
| 4 | Add `FAQPage` schema to top-10 docs pages | +6 | 3h | low | 2.0 |
| 5 | Fix duplicate canonical on paginated blog archives | +3 | 2h | med | 1.5 |
| 6 | Rewrite 12 programmatic title tags (>65 chars, no H1 match) | +3 | 3h | low | 1.0 |
| 7 | Add `sameAs` array pointing to LinkedIn, Crunchbase, GitHub | +3 | 1h | low | 3.0 |
| 8 | Add answer-first 40-60 word blocks at top of 8 pillar pages | +4 | 6h | low | 0.67 |
| 9 | Add `SpeakableSpecification` to top 5 ranking posts | +2 | 2h | low | 1.0 |
| 10 | Compress hero image (LCP regression on mobile) | +2 | 1h | low | 2.0 |

**Ship 1-3 first.** Combined: +22 composite points in ~3.5 hours. New projected score: **76 / 100**.

---

## 4. Before / after diff (fix #2 example)

This is what a single fix looks like in the delivered report. Every fix includes the exact code diff.

**Before** - `acme.com/` has no Organization JSON-LD:

```html
<head>
  <title>Acme - The faster way to ship</title>
  <meta name="description" content="...">
</head>
```

**After** - paste before `</head>`:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Acme",
  "url": "https://acme.com",
  "logo": "https://acme.com/logo.png",
  "sameAs": [
    "https://linkedin.com/company/acme",
    "https://twitter.com/acme",
    "https://github.com/acme"
  ],
  "foundingDate": "2019",
  "founder": {
    "@type": "Person",
    "name": "{founder name}",
    "sameAs": "https://linkedin.com/in/{founder}"
  }
}
</script>
```

**Validation:** paste the rendered page into [validator.schema.org](https://validator.schema.org/). Should return 0 errors, 0 warnings.

---

## 5. Implementation plan (30-day ship window)

| Week | Work | Owner |
| ---: | --- | --- |
| 1 | Fixes 1-3 shipped to production. Rescore. | Dev (4h) |
| 2 | Fixes 4-7. Fix #4 needs content team on FAQ answers. | Dev + content |
| 3 | Fixes 8-10. Validate CWV on production. | Dev + perf |
| 4 | Final rescore + 30-day citation delta report (Perplexity, ChatGPT Search, Google AI Overview) | Me |

Target end-state score: **82-86 / 100**. Target citation lift: measurable presence in at least 2 AI answer sets for brand-name + category queries within 30 days.

---

## 6. What this audit does not do

- It does not write your content. Audit the structural layer, then your team (or mine, in the sprint) ships the code.
- It does not guarantee a ranking change in Google classic search. Organic ranking movement takes 6-12 weeks. AI citation movement is typically faster (first fetch cycle).
- It cannot unblock a domain your WAF blocks to AI crawlers. If Cloudflare or a security plugin blocks `GPTBot`, the audit flags it; unblocking is a manual step.

---

## 7. How to apply

Apply for an AI Search Visibility Audit at [yanivgoldenberg.com/contact](https://yanivgoldenberg.com/contact). Post-PMF SaaS, B2B, and e-commerce brands only. Fee is quoted after application and is credited in full if you continue into the Implementation Sprint.
