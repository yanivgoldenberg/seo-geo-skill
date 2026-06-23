"""Scoring parity test.

Pins two things so the documented scoring cannot silently drift from the code:
1. The six bucket totals match across seo-geo.md Phase 0, benchmark_sites.py
   MAX_POINTS, and the canonical set.
2. The per-check BENCHMARK_CHECKS table in benchmark_sites.py matches the
   "What the automated benchmark scores" table in docs/SCORING.md, and its
   per-bucket sums are the documented benchmark maxima (GEO is over-subscribed
   to 30 and clamped to its 25 cap).
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "seo-geo.md"
BENCH = REPO / "tests" / "benchmark_sites.py"
SCORING = REPO / "docs" / "SCORING.md"

sys.path.insert(0, str(REPO / "tests"))
from benchmark_sites import BENCHMARK_CHECKS, MAX_POINTS  # noqa: E402

CANONICAL = {"technical": 20, "onpage": 15, "schema": 20, "geo": 25, "aeo": 10, "eeat": 10}

# Documented per-bucket benchmark maxima. GEO checks sum to 30 (clamped to 25).
BENCHMARK_MAXIMA = {"technical": 20, "onpage": 15, "schema": 20, "geo": 30, "aeo": 10, "eeat": 10}


def _phase0_weights() -> dict[str, int]:
    body = SKILL.read_text(encoding="utf-8")
    idx = body.index("## Phase 0")
    end = body.index("## Phase 1", idx)
    block = body[idx:end]
    patterns = {
        "technical": r"Technical SEO \((\d+) pts\)",
        "onpage": r"On-Page SEO \((\d+) pts\)",
        "schema": r"Schema / Structured Data \((\d+) pts\)",
        "geo": r"GEO / LLM Optimization \((\d+) pts\)",
        "eeat": r"E-E-A-T \((\d+) pts\)",
        "aeo": r"AEO / Answer Engine \((\d+) pts\)",
    }
    return {k: int(re.search(v, block).group(1)) for k, v in patterns.items()}


def _benchmark_weights() -> dict[str, int]:
    body = BENCH.read_text(encoding="utf-8")
    match = re.search(r"MAX_POINTS\s*=\s*\{([^}]+)\}", body)
    weights: dict[str, int] = {}
    for pair in re.findall(r'"(\w+)"\s*:\s*(\d+)', match.group(1)):
        weights[pair[0]] = int(pair[1])
    return weights


def test_phase0_sums_to_100() -> None:
    assert sum(_phase0_weights().values()) == 100


def test_benchmark_sums_to_100() -> None:
    assert sum(_benchmark_weights().values()) == 100


def test_phase0_matches_benchmark() -> None:
    assert _phase0_weights() == _benchmark_weights()


def test_phase0_matches_canonical() -> None:
    assert _phase0_weights() == CANONICAL


def test_benchmark_checks_cover_all_buckets() -> None:
    assert set(BENCHMARK_CHECKS) == set(MAX_POINTS)


def test_benchmark_check_sums_match_documented_maxima() -> None:
    for bucket, checks in BENCHMARK_CHECKS.items():
        total = sum(points for _label, points in checks)
        assert total == BENCHMARK_MAXIMA[bucket], (
            f"{bucket}: BENCHMARK_CHECKS sum {total} != documented {BENCHMARK_MAXIMA[bucket]}"
        )


def test_scoring_md_documents_benchmark_checks() -> None:
    body = SCORING.read_text(encoding="utf-8")
    assert "What the automated benchmark scores" in body
    # Every check's point value must appear in the SCORING.md benchmark table.
    idx = body.index("What the automated benchmark scores")
    end = body.index("### Multi-page sampling", idx)
    table = body[idx:end]
    for bucket, checks in BENCHMARK_CHECKS.items():
        for label, points in checks:
            assert f"({points})" in table, f"{bucket} check '{label}' ({points}) missing from SCORING.md"


if __name__ == "__main__":
    for name in [n for n in dir() if n.startswith("test_")]:
        globals()[name]()
        print(f"ok {name}")
