# Documentation

Start with the [project README](../README.md). Everything below is plain Markdown, JSON or CSV in this folder.

## Use the skill

| Document | What it covers |
|---|---|
| [Installation](setup/installation.md) | Windows, Linux, macOS, WSL2 and connector-based agents; offline validation |
| [Scoring rubric](SCORING.md) | The canonical 100-point rubric and exactly what the automated benchmark scores |
| [Comparison](compare.md) | How this skill compares with other Claude Code SEO skills |
| [Auto-GEO on publish](patterns/auto-geo-on-publish.md) | Pattern: keep per-page GEO fixes from rotting after the audit |
| [Sample audit](sample-paid-audit.md) | Illustrative audit deliverable (fictional site and numbers) |

## Benchmark data

| Document | What it covers |
|---|---|
| [State of AI Search Visibility 2026](state-of-ai-search-2026.md) | The 61-site report, leaderboard and methodology |
| [Dataset (JSON)](state-of-ai-search-2026.json) and [dataset (CSV)](state-of-ai-search-2026.csv) | Canonical scores, scored 2026-06-23; the last 3 rows are flagged canaries |
| [Monthly history](state-of-ai-search-history/README.md) | One CSV per monthly Action run |
| [Original 13-site cohort](benchmarks.md) | The first public benchmark (v1.6.0 calibration) |
| [benchmarks.json](benchmarks.json) | Machine-readable 13-site cohort |

## Case studies and research

| Document | What it covers |
|---|---|
| [yanivgoldenberg.com](case-studies/yanivgoldenberg.com.md) | One-session optimization of the reference site |
| [OpenAI fix blueprint](case-study-openai.md) | What a 7 to 70 path looks like on the rubric |
| [Content integrity research](research/ai-slop-2026-10-18.md) | Source dispositions behind Phase 22 |
| [Scoring reliability proposal](proposals/scoring-reliability.md) | Why llms.txt was de-weighted (implemented 2026-06-23) |
