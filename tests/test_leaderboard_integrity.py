"""Leaderboard integrity tests.

- Benchmark count matches headline claim.
- Ranks are monotonic with valid ties (no gap larger than tie-group size).
- README leaderboard and docs/benchmarks.md agree on sites and composite scores.
"""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
README = REPO / "README.md"
BENCH_DOC = REPO / "docs" / "benchmarks.md"


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


def test_readme_leaderboard_is_13_rows() -> None:
    rows = _parse_leaderboard(README.read_text(encoding="utf-8"), 4, composite_col=2)
    assert len(rows) == 13, f"README leaderboard has {len(rows)} rows, expected 13"


def test_benchmarks_leaderboard_is_13_rows() -> None:
    rows = _parse_leaderboard(BENCH_DOC.read_text(encoding="utf-8"), 9, composite_col=8)
    assert len(rows) == 13, f"benchmarks.md leaderboard has {len(rows)} rows, expected 13"


def test_ranks_are_monotonic_with_valid_ties() -> None:
    for path, cols, composite_col in ((README, 4, 2), (BENCH_DOC, 9, 8)):
        rows = _parse_leaderboard(path.read_text(encoding="utf-8"), cols, composite_col=composite_col)
        ranks = [r["rank"] for r in rows]
        # Ranks must be non-decreasing
        assert ranks == sorted(ranks), f"{path.name}: ranks not monotonic: {ranks}"
        # Max rank cannot exceed row count (no rank 14 in a 13-row table)
        assert max(ranks) <= len(rows), f"{path.name}: max rank {max(ranks)} exceeds row count {len(rows)}"
        # After N tied rows starting at rank R, next non-tied rank must be R + tie_count
        i = 0
        while i < len(ranks):
            r = ranks[i]
            j = i
            while j < len(ranks) and ranks[j] == r:
                j += 1
            if j < len(ranks):
                expected_next = r + (j - i)
                assert ranks[j] == expected_next, (
                    f"{path.name}: after {j - i} tied rows at rank {r}, "
                    f"next rank should be {expected_next}, got {ranks[j]}"
                )
            i = j


def test_composite_scores_agree_across_readme_and_benchmarks() -> None:
    r_rows = {r["site"].replace("**", "").replace("*", ""): r["composite"].replace("**", "")
              for r in _parse_leaderboard(README.read_text(encoding="utf-8"), 4, composite_col=2)}
    b_rows = {r["site"]: r["composite"].replace("**", "")
              for r in _parse_leaderboard(BENCH_DOC.read_text(encoding="utf-8"), 9, composite_col=8)}
    assert set(r_rows.keys()) == set(b_rows.keys()), \
        f"site set mismatch: README {set(r_rows) - set(b_rows)} vs benchmarks {set(b_rows) - set(r_rows)}"
    for site, rscore in r_rows.items():
        assert rscore == b_rows[site], f"composite mismatch for {site}: README={rscore} benchmarks={b_rows[site]}"


if __name__ == "__main__":
    for name in [n for n in dir() if n.startswith("test_")]:
        globals()[name]()
        print(f"ok {name}")
