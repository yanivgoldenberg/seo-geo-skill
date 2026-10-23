# Contributing to seo-geo-skill

Thanks for considering a contribution. This skill is under the PolyForm Noncommercial 1.0.0 license (see `LICENSE`). Commercial use, including client work, needs written permission (see `COMMERCIAL.md`). Contributions are accepted under the same license, and every copy must keep the attribution in `NOTICE`.

By participating you agree to the [Code of Conduct](CODE_OF_CONDUCT.md).

## What's welcome

- **Bug reports** on specific phases that produce incorrect scores or writes
- **Platform adapter additions** (Ghost, Astro, Craft CMS, etc.) following the Phase 18 pattern
- **Schema type additions** with validated JSON-LD fixtures in `examples/`
- **Case studies** - before/after audit reports following `docs/case-studies/yanivgoldenberg.com.md` format
- **Test additions** in `tests/` that catch regressions

## What to avoid

- Adding dependencies without strong justification (the skill is a single file by design)
- Vendor lock-in to paid APIs without a free fallback
- Breaking changes to the Phase 0-15 scoring rubric (1.0.0 numbers must stay comparable forever)
- Password-reset, credential-mutation, or user-deletion flows (Phase 17 banned endpoints)

## Process

1. Open an issue first. Describe the gap or regression.
2. Fork, branch off `main`, run the test suite locally.
3. Open a PR with a one-paragraph summary + any new test coverage.
4. CI must pass. I review within 7 days.

## Testing

Python 3.12, from the repository root:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
PYTHONUTF8=1 .venv/bin/python -m pytest -q --ignore=tests/test_live_endpoints.py
```

`tests/test_live_endpoints.py` contacts live websites and runs separately in CI. CI also rejects em dashes in Markdown (except `seo-geo.md`) and checks links in `README.md` and `seo-geo.md`.

## Style

- Match the existing tone: direct, specific, no fluff
- Use real URLs and real numbers in examples
- Avoid marketing language in the skill file itself
