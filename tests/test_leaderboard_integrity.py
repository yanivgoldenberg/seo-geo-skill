"""Leaderboard integrity tests.

The README carries two distinct tables, each provenanced to a different source:

- Teaser (4 cols): the bottom three rows of the 61-site State of AI Search 2026
  study. Must match docs/state-of-ai-search-2026.csv on published_rank + score.
- Top-13 (3 cols): the original 13-site cohort. Must match docs/benchmarks.md
  (9 cols) on site + composite. These are a DIFFERENT study with different
  scores for the same sites, so they are never conflated into one leaderboard.

Each table is bound to its own universe: ranks monotonic with valid ties, and
max rank within that table's own row count (13-site cohort) or the canonical
61-site CSV length (teaser). No table's bound is hardcoded where the source can
supply it.
"""
import csv
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
README = REPO / "README.md"
BENCH_DOC = REPO / "docs" / "benchmarks.md"
CSV_61 = REPO / "docs" / "state-of-ai-search-2026.csv"


def _parse_leaderboard(md: str, columns_expected: int, composite_col: int) -> list[dict]:
    rows: list[dict] = []
    for line in md.splitlines():
        if not line.startswith("|"):
            continue
        parts = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(parts) != columns_expected:
            continue
        first = parts[0]
        if first in ("Rank", "---:"):
            continue
        try:
            rank = int(first)
        except ValueError:
            continue
        rows.append({"rank": rank, "site": parts[1], "composite": parts[composite_col]})
    return rows


def _clean(value: str) -> str:
    return value.replace("**", "").replace("*", "").strip()


def _readme_top13() -> list[dict]:
    return _parse_leaderboard(README.read_text(encoding="utf-8"), 3, composite_col=2)


def _readme_teaser() -> list[dict]:
    return _parse_leaderboard(README.read_text(encoding="utf-8"), 4, composite_col=2)


def _benchmarks_rows() -> list[dict]:
    return _parse_leaderboard(BENCH_DOC.read_text(encoding="utf-8"), 9, composite_col=8)


def _csv_rows() -> list[dict]:
    return list(csv.DictReader(CSV_61.read_text(encoding="utf-8").splitlines()))


def _assert_monotonic_with_valid_ties(ranks: list[int], label: str) -> None:
    assert ranks == sorted(ranks), f"{label}: ranks not monotonic: {ranks}"
    i = 0
    while i < len(ranks):
        r = ranks[i]
        j = i
        while j < len(ranks) and ranks[j] == r:
            j += 1
        if j < len(ranks):
            expected_next = r + (j - i)
            assert ranks[j] == expected_next, (
                f"{label}: after {j - i} tied rows at rank {r}, "
                f"next rank should be {expected_next}, got {ranks[j]}"
            )
        i = j


def test_readme_top13_is_13_rows() -> None:
    rows = _readme_top13()
    assert len(rows) == 13, f"README Top-13 table has {len(rows)} rows, expected 13"


def test_benchmarks_leaderboard_is_13_rows() -> None:
    rows = _benchmarks_rows()
    assert len(rows) == 13, f"benchmarks.md leaderboard has {len(rows)} rows, expected 13"


def test_readme_top13_matches_benchmarks_doc() -> None:
    """(a) README Top-13 rows == benchmarks.md rows on site + composite."""
    r_rows = {_clean(r["site"]): _clean(r["composite"]) for r in _readme_top13()}
    b_rows = {_clean(r["site"]): _clean(r["composite"]) for r in _benchmarks_rows()}
    assert r_rows, "README Top-13 table parsed empty"
    assert set(r_rows) == set(b_rows), (
        f"site set mismatch: README only={set(r_rows) - set(b_rows)} "
        f"benchmarks only={set(b_rows) - set(r_rows)}"
    )
    for site, score in r_rows.items():
        assert score == b_rows[site], (
            f"composite mismatch for {site}: README={score} benchmarks={b_rows[site]}"
        )


def test_readme_teaser_matches_61_site_csv() -> None:
    """(b) Teaser rows match the canonical 61-site CSV on published_rank + composite."""
    teaser = _readme_teaser()
    assert teaser, "README teaser table parsed empty"
    csv_by_site = {row["site"]: row for row in _csv_rows()}
    for row in teaser:
        site = _clean(row["site"])
        assert site in csv_by_site, f"teaser site {site} not in 61-site CSV"
        ref = csv_by_site[site]
        assert _clean(row["composite"]) == ref["composite"], (
            f"teaser score for {site}: README={_clean(row['composite'])} "
            f"CSV={ref['composite']}"
        )
        assert str(row["rank"]) == ref["published_rank"], (
            f"teaser rank for {site}: README={row['rank']} "
            f"CSV published_rank={ref['published_rank']}"
        )


def test_top13_ranks_monotonic_within_bounds() -> None:
    """(c) Top-13: monotonic ties, max rank within its own 13 rows."""
    for label, table in (("README Top-13", _readme_top13()), ("benchmarks.md", _benchmarks_rows())):
        ranks = [r["rank"] for r in table]
        assert ranks, f"{label}: no ranked rows parsed"
        _assert_monotonic_with_valid_ties(ranks, label)
        assert max(ranks) <= len(table), (
            f"{label}: max rank {max(ranks)} exceeds row count {len(table)}"
        )


def test_teaser_ranks_monotonic_within_61_site_bound() -> None:
    """(c) Teaser: monotonic, max rank within the canonical 61-site universe."""
    teaser = _readme_teaser()
    ranks = [r["rank"] for r in teaser]
    assert ranks, "teaser: no ranked rows parsed"
    _assert_monotonic_with_valid_ties(ranks, "README teaser")
    universe = len(_csv_rows())
    assert universe == 61, f"61-site CSV has {universe} rows, expected 61"
    assert min(ranks) >= 1, f"teaser ranks below 1: {ranks}"
    assert max(ranks) <= universe, (
        f"teaser max rank {max(ranks)} exceeds 61-site universe {universe}"
    )


if __name__ == "__main__":
    for name in [n for n in dir() if n.startswith("test_")]:
        globals()[name]()
        print(f"ok {name}")
