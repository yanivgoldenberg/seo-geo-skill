import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tests"))

from benchmark_sites import MAX_POINTS, score

SITES = ["https://yanivgoldenberg.com", "https://openai.com"]
DIMS = ["technical", "schema", "geo", "onpage", "aeo", "eeat"]
HEAD = ["Site", "Tech", "Sch", "GEO", "OnP", "AEO", "EEAT", "TOTAL"]


def main() -> None:
    rows = sorted((score(u) for u in SITES), key=lambda r: -r["composite"])
    print(f"{HEAD[0]:<22}" + "".join(f"{h:>6}" for h in HEAD[1:7]) + f"{HEAD[7]:>7}")
    print("-" * 61)
    for r in rows:
        name = r["site"].replace("https://", "").replace("www.", "")
        cells = "".join(f"{r[d]:>6}" for d in DIMS)
        print(f"{name:<22}{cells}{r['composite']:>7}")
    print("-" * 61)
    caps = "".join(f"{MAX_POINTS[d]:>6}" for d in DIMS)
    print(f"{'max points':<22}{caps}{'100':>7}")


if __name__ == "__main__":
    main()
