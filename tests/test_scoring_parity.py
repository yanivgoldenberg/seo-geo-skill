"""Scoring parity test.

Ensures the canonical rubric defined in seo-geo.md Phase 0 matches the
MAX_POINTS declared in tests/benchmark_sites.py. No drift allowed.
"""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "seo-geo.md"
BENCH = REPO / "tests" / "benchmark_sites.py"

CANONICAL = {"technical": 20, "onpage": 15, "schema": 20, "geo": 25, "aeo": 10, "eeat": 10}


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


if __name__ == "__main__":
    for name in [n for n in dir() if n.startswith("test_")]:
        globals()[name]()
        print(f"ok {name}")
