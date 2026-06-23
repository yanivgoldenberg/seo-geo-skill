"""Static integrity test for the 61-site State of AI Search 2026 benchmark.

Enforces, with no live network fetch, that the runnable scorer's SITES_61 /
CARRIED_BASELINE actually MATCH the published leaderboard
(docs/state-of-ai-search-2026.json). This is what makes "same rubric, every
one of the 61 published sites" a checkable claim rather than an assertion.
"""
import csv
import json
from pathlib import Path

from benchmark_sites import (
    CARRIED_BASELINE,
    MAX_POINTS,
    SITES_61,
)

REPO = Path(__file__).resolve().parent.parent
PUBLISHED_JSON = REPO / "docs" / "state-of-ai-search-2026.json"
PUBLISHED_CSV = REPO / "docs" / "state-of-ai-search-2026.csv"
DIMS = ("technical", "onpage", "schema", "geo", "aeo", "eeat")


def _published_rows() -> list[dict]:
    return json.loads(PUBLISHED_JSON.read_text(encoding="utf-8"))


def test_sites_61_has_61_entries() -> None:
    assert len(SITES_61) == 61, f"SITES_61 has {len(SITES_61)} entries, expected 61"
    assert len(CARRIED_BASELINE) == 61


def test_sites_61_matches_published_set() -> None:
    published = {r["site"] for r in _published_rows()}
    assert set(SITES_61) == published, (
        f"SITES_61 site set differs from published leaderboard: "
        f"missing={published - set(SITES_61)} extra={set(SITES_61) - published}"
    )


def test_sites_61_preserves_published_rank_order() -> None:
    published_order = [r["site"] for r in _published_rows()]
    assert published_order == SITES_61, "SITES_61 must keep published rank order"


def test_carried_baseline_matches_published_scores() -> None:
    published = _published_rows()
    assert len(CARRIED_BASELINE) == len(published)
    for got, exp in zip(CARRIED_BASELINE, published, strict=True):
        for key in ("site", "composite", *DIMS):
            assert got[key] == exp[key], (
                f"{got['site']}: {key} baseline={got[key]} published={exp[key]}"
            )
        assert got.get("notes", []) == exp.get("notes", []), (
            f"{got['site']}: notes baseline={got.get('notes')} "
            f"published={exp.get('notes')}"
        )


def test_carried_baseline_composites_sum_to_dimensions() -> None:
    for row in CARRIED_BASELINE:
        assert row["composite"] == sum(row[d] for d in MAX_POINTS), (
            f"{row['site']}: composite {row['composite']} != sum of dimensions"
        )


def test_canonical_csv_matches_published_json() -> None:
    """The canonical CSV IS the published 61-row leaderboard.

    It carries source/scored_at provenance columns but every score must equal
    the published JSON (and therefore the .md headlines: Railway 0, OpenAI 7,
    yaniv 97). A live re-score writes a dated file elsewhere and never this one;
    the runner enforces that. This is what keeps the leaderboard self-consistent
    across the .md / .json / .csv while staying reproducible.
    """
    rows = list(csv.DictReader(PUBLISHED_CSV.read_text(encoding="utf-8").splitlines()))
    assert len(rows) == 61, f"CSV has {len(rows)} data rows, expected 61"
    json_by_domain = {
        r["site"].replace("https://", "").replace("www.", ""): r
        for r in _published_rows()
    }
    assert {r["site"] for r in rows} == set(json_by_domain), "CSV site set drifted"
    caps = dict(MAX_POINTS)
    for row in rows:
        assert row["source"] in ("fresh", "carried", "unreachable"), row
        assert row["scored_at"], f"{row['site']}: missing scored_at"
        ref = json_by_domain[row["site"]]
        composite = int(row["composite"])
        assert composite == sum(int(row[d]) for d in DIMS), f"{row['site']}: composite != sum"
        assert composite == ref["composite"], f"{row['site']}: composite != published json"
        for d in DIMS:
            assert 0 <= int(row[d]) <= caps[d], f"{row['site']}: {d} out of range"
            assert int(row[d]) == ref[d], f"{row['site']}: {d} != published json"


if __name__ == "__main__":
    for name in [n for n in dir() if n.startswith("test_")]:
        globals()[name]()
        print(f"ok {name}")
