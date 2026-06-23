# Proposal: scoring-reliability and llms.txt re-weighting (deferred)

Status: deferred. Flagged in the v1.12.0 audit. Touching either item below re-scores the published 94/100 reference number and the 61-site leaderboard, so it needs a deliberate, separately-versioned release with the leaderboard re-run.

## C1 - The rubric and the scorer disagree

`tests/test_scoring_parity.py` only asserts that the six dimension TOTALS sum to 100 and match across files. It never checks that the sub-checks match. As a result `tests/benchmark_sites.py` implements a different set of sub-checks than the Phase 0 rubric in `seo-geo.md` and `docs/SCORING.md`, while CI stays green. Examples:

- Technical: the scorer never fetches Core Web Vitals (the rubric's largest single line item, 5 pts) or broken links (2 pts); it redistributes points across robots/sitemap/canonical/viewport/HTTPS/H1 with different weights than the rubric.
- On-Page: the scorer never checks keyword placement (3 pts) or internal-link count (2 pts); it scores og/twitter tags with a different split than the rubric's grouping.
- E-E-A-T: the scorer credits `datePublished` (no rubric counterpart here) and never checks proof points or external authority links.
- GEO: `sameAs` uses a fragile operator-precedence expression and never checks for a Wikidata entry; the Link-header llms.txt check is dead code (`link:` substring never matches stringified header items); the llms.txt point hinges on a `Content-Type: text/plain` header the rubric never states.

Consequence: the documented rubric and the actual scorer produce different per-dimension scores for the same site. The published leaderboard reflects the scorer's heuristics, not the documented rubric.

Two ways to resolve (pick one in a future release):
1. Make `test_scoring_parity.py` assert sub-check parity (parse the Phase 0 tables, map each line item to a scorer branch with the same point value), then fix the scorer to match. Re-run the leaderboard and update every published number.
2. Explicitly demote `benchmark_sites.py` to "heuristic approximation" in `docs/SCORING.md` and stop describing its output as scored against the canonical rubric. Lower effort, no number changes, but concedes the "no methodology drift" claim in the README.

## C2 - llms.txt is over-weighted

llms.txt is worth 7 of 25 GEO points (plus 5 for llms-full.txt). As of 2026 no major AI search engine consumes llms.txt in production (Google publicly declined it in 2025; server-log studies show near-zero AI-bot hits). Its real value is dev tooling (Cursor, Claude Code, Copilot), not AI-search citation.

Proposed: cut its weight substantially and redistribute toward entity presence (Wikipedia/Wikidata) and quotable passages, which carry the citation load it was credited with. This changes the GEO sub-totals and therefore the published scores, so it ships with C1.
