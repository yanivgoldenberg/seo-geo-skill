# Contributing to seo-geo-skill

Thanks for considering a contribution. This skill is under PolyForm Noncommercial license - free for personal and client work, not for resale.

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

```bash
python3 tests/test_skill_metadata.py
python3 tests/test_schema_fixtures.py
python3 tests/test_live_endpoints.py
```

## Style

- Match the existing tone: direct, specific, no fluff
- Use real URLs and real numbers in examples
- Avoid marketing language in the skill file itself
