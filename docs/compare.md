# How seo-geo-skill compares

Honest side-by-side with the other Claude Code SEO skills. Pick the one that matches your workflow.

## Matrix

| Capability | **seo-geo-skill** (this) | AgriciDaniel/claude-seo | aaron-he-zhu/seo-geo-claude-skills | claude-seo.md |
|---|:---:|:---:|:---:|:---:|
| **Files** | 1 file | 19 sub-skills | 20 skills + 35 agents | Multi-page site + skill |
| **Phases** | 20 | ~8 | ~12 | ~10 |
| **Schemas covered** | 16 types | ~10 | ~15 | ~8 |
| **Write capability** | Yes (with `--apply`) | Yes | Yes | Read-only |
| **Dry-run default** | Yes (v1.3.0+) | No | No | N/A |
| **Platform adapters** | WP / Shopify / Webflow / Next.js | Primarily WP | WP + Shopify | WP examples |
| **Paid data** | None | DataForSEO extension | None | None |
| **llms.txt generator** | Yes | No | Partial | Yes |
| **Competitor benchmarking** | Yes (Phase 19) | No | No | No |
| **100-point scoring** | Yes (Phase 0) | No | Partial | No |
| **Public benchmark of top sites** | Yes (`docs/benchmarks.md`) | No | No | No |
| **CI test suite** | Yes (GitHub Actions) | No | No | No |
| **License** | PolyForm Noncommercial | MIT | MIT | ? |
| **Maintained recency** | Active | Active | Active | Semi-active |
| **Best for** | Solo operator / agency running 20+ audits/year on the same checklist | Kitchen-sink agency toolbox | Heavy multi-agent automation | Reading, learning the space |

## When to pick each

**Use seo-geo-skill if you want:**
- A single-file install (no dependency tree)
- Same audit → same score → same fix list every time
- Safe writes (dry-run default, banned-endpoint list)
- Public benchmark data to anchor your claims
- Any CMS support that actually works, not in-theory support

**Use AgriciDaniel/claude-seo if you want:**
- 19 separate sub-skills you can mix/match
- DataForSEO integration for SERP data
- More granular command surface

**Use aaron-he-zhu/seo-geo-claude-skills if you want:**
- Multi-agent orchestration (35+ agents)
- Heavier automation pipelines

**Use claude-seo.md if you want:**
- Reading material / a reference site
- No Claude Code skill install

## The honest trade-off of picking this one

**You lose:** the wider surface of 20+ sub-skills. If your workflow spans ad creative, email copy, and SEO, you'll want something broader.

**You gain:** a scoring system with a public calibration (see `docs/benchmarks.md`), safety gates that match production-use, and writes that match the 4 major CMS targets people actually ship on.

Pick by your workflow, not by feature count.
