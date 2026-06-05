import argparse
import csv
import importlib.util
import sys
import time
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CANONICAL_CSV = REPO / "docs" / "state-of-ai-search-2026.csv"

_spec = importlib.util.spec_from_file_location(
    "benchmark_sites", REPO / "tests" / "benchmark_sites.py"
)
if _spec is None or _spec.loader is None:
    raise RuntimeError("could not load benchmark_sites module spec")
benchmark_sites = importlib.util.module_from_spec(_spec)
sys.modules["benchmark_sites"] = benchmark_sites
_spec.loader.exec_module(benchmark_sites)

score = benchmark_sites.score
SITES_61 = benchmark_sites.SITES_61
CARRIED_BASELINE = benchmark_sites.CARRIED_BASELINE
MAX_POINTS = benchmark_sites.MAX_POINTS
BASELINE_DATE = benchmark_sites.BASELINE_DATE

DIMS = ["technical", "onpage", "schema", "geo", "aeo", "eeat"]
CSV_COLUMNS = [
    "published_rank",
    "site",
    "composite",
    "technical",
    "onpage",
    "schema",
    "geo",
    "aeo",
    "eeat",
    "source",
    "scored_at",
]

_BASELINE_BY_SITE = {row["site"]: row for row in CARRIED_BASELINE}


def _live_score(site: str) -> dict | None:
    home = benchmark_sites.fetch(site)
    if home is None or home.status_code != 200:
        return None
    return score(site)


def _row(baseline_index: int, scored: dict, source: str, scored_at: str) -> dict:
    row = {
        "published_rank": baseline_index + 1,
        "site": scored["site"].replace("https://", "").replace("www.", ""),
        "composite": scored["composite"],
    }
    for d in DIMS:
        row[d] = scored[d]
    row["source"] = source
    row["scored_at"] = scored_at
    return row


def baseline_rows() -> list[dict]:
    """The published 61-row leaderboard, verbatim. Writes a canonical CSV that
    stays consistent with docs/state-of-ai-search-2026.md and .json (no live
    fetch, no drift). Used by --rebuild-baseline."""
    return [
        _row(i, b, "carried", BASELINE_DATE) for i, b in enumerate(CARRIED_BASELINE)
    ]


def build_rows(sites: list[str], today: str, sleep: float) -> list[dict]:
    rows: list[dict] = []
    for i, site in enumerate(sites, 1):
        baseline = _BASELINE_BY_SITE.get(site)
        baseline_index = CARRIED_BASELINE.index(baseline) if baseline is not None else i - 1
        fresh = _live_score(site)
        if fresh is not None:
            source, scored_at, scored = "fresh", today, fresh
        elif baseline is not None:
            source, scored_at, scored = "carried", BASELINE_DATE, baseline
        else:
            source, scored_at, scored = "unreachable", today, score(site)
        row = _row(baseline_index, scored, source, scored_at)
        rows.append(row)
        print(
            f"[{i:>2}/{len(sites)}] {row['site']:<24} "
            f"{source:<11} composite={row['composite']:>3}"
        )
        if sleep:
            time.sleep(sleep)
    return rows


def write_csv(rows: list[dict], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Re-score the published State of AI Search 2026 61-site leaderboard "
            "with the SAME canonical rubric (tests/benchmark_sites.py: score()). "
            "A live run writes a dated, timestamped CSV and never touches the "
            "published canonical CSV, because the canonical CSV must stay "
            "consistent with the .md/.json headline findings (which this script "
            "does not edit). To regenerate the canonical CSV verbatim from the "
            "published baseline, use --rebuild-baseline."
        )
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Live-score only the first N published sites (sample / verify).",
    )
    parser.add_argument(
        "--out",
        type=str,
        default=None,
        help="Output CSV path. Default for a live run: a dated /tmp file.",
    )
    parser.add_argument(
        "--sleep",
        type=float,
        default=0.5,
        help="Seconds to sleep between sites (politeness).",
    )
    parser.add_argument(
        "--rebuild-baseline",
        action="store_true",
        help=(
            "Write the published 61-row leaderboard verbatim to the canonical "
            f"CSV ({CANONICAL_CSV.name}). No network. Keeps the CSV consistent "
            "with the .md/.json."
        ),
    )
    args = parser.parse_args()

    if args.rebuild_baseline:
        if args.limit is not None:
            parser.error("--rebuild-baseline writes all 61 rows; drop --limit")
        out_path = Path(args.out) if args.out is not None else CANONICAL_CSV
        rows = baseline_rows()
        write_csv(rows, out_path)
        print(f"wrote {len(rows)} carried baseline rows -> {out_path}")
        return 0

    today = date.today().isoformat()
    sites = SITES_61 if args.limit is None else SITES_61[: args.limit]

    if args.out is not None:
        out_path = Path(args.out)
    else:
        tag = "full" if args.limit is None else f"sample-{len(sites)}"
        out_path = Path(f"/tmp/state-of-ai-search-2026-live-{tag}-{today}.csv")

    if out_path.resolve() == CANONICAL_CSV.resolve():
        parser.error(
            "refusing to overwrite the canonical CSV with live scores; live "
            "composites diverge from the published .md/.json headlines. Use "
            "--rebuild-baseline to regenerate the canonical CSV, or --out to "
            "write live scores elsewhere."
        )

    rows = build_rows(sites, today, args.sleep)
    write_csv(rows, out_path)

    fresh = sum(1 for r in rows if r["source"] == "fresh")
    carried = sum(1 for r in rows if r["source"] == "carried")
    unreachable = sum(1 for r in rows if r["source"] == "unreachable")
    print(
        f"\nwrote {len(rows)} rows -> {out_path}\n"
        f"  fresh={fresh}  carried={carried}  unreachable={unreachable}\n"
        "  NOTE: live composites can diverge from the published .md/.json "
        "(e.g. sites that changed since 2026-04-24). The canonical CSV is "
        "rebuilt only via --rebuild-baseline."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
