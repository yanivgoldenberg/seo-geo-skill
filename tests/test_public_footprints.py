# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Copyright (c) Yaniv Goldenberg - https://yanivgoldenberg.com (see NOTICE)
"""Disclosed attribution footprints of the public edition.

Everything checked here is visible and documented in README "Attribution &
fingerprint": NOTICE, license headers, the project fingerprint, the canary rows
in the benchmark dataset and the outbound User-Agent. Nothing phones home.
"""
import csv
import json
import re
from pathlib import Path

from benchmark_sites import SITES_61, UA
from project_meta import CANARY_CSV_SOURCE, CANARY_ROWS, PROJECT_ID, USER_AGENT, VERSION

REPO = Path(__file__).resolve().parent.parent
PUBLISHED_JSON = REPO / "docs" / "state-of-ai-search-2026.json"
PUBLISHED_CSV = REPO / "docs" / "state-of-ai-search-2026.csv"
CODE_SUFFIXES = {".py", ".php", ".ts", ".tsx"}
SPDX = "SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0"
CANARY_HOST = re.compile(r"^https://[a-z0-9-]+\.(example|invalid)$")


def _code_files() -> list[Path]:
    return [
        p for p in REPO.rglob("*")
        if p.suffix in CODE_SUFFIXES and ".git" not in p.parts and ".venv" not in p.parts
    ]


def test_fingerprint_format() -> None:
    assert re.fullmatch(r"YG-SEOGEO-[0-9A-F]{12}", PROJECT_ID), PROJECT_ID


def test_fingerprint_in_code_data_and_docs() -> None:
    for rel in ("seo-geo.md", "README.md", "NOTICE", "docs/state-of-ai-search-2026.json",
                "docs/state-of-ai-search-2026.csv", "tests/project_meta.py"):
        assert PROJECT_ID in (REPO / rel).read_text(encoding="utf-8"), f"fingerprint missing in {rel}"


def test_user_agent_format_and_use() -> None:
    assert USER_AGENT == f"seo-geo-skill/{VERSION} (+https://yanivgoldenberg.com/)"
    assert UA == {"User-Agent": USER_AGENT}


def test_version_matches_skill_frontmatter() -> None:
    body = (REPO / "seo-geo.md").read_text(encoding="utf-8")
    assert re.search(rf"^version:\s*{re.escape(VERSION)}$", body, re.M), VERSION


def test_no_other_user_agent_strings() -> None:
    for path in _code_files():
        text = path.read_text(encoding="utf-8")
        for literal in re.findall(r"User-Agent\"?\s*[:=,]\s*\"([^\"]+)\"", text):
            assert literal.startswith("seo-geo-skill/"), f"{path.name}: foreign UA {literal!r}"


def test_spdx_header_in_every_source_file() -> None:
    missing = [str(p.relative_to(REPO)) for p in _code_files()
               if SPDX not in "\n".join(p.read_text(encoding="utf-8").splitlines()[:6])]
    assert not missing, f"missing SPDX header: {missing}"


def test_notice_license_trademark_commercial() -> None:
    notice = (REPO / "NOTICE").read_text(encoding="utf-8")
    assert "Required Notice: Built by Yaniv Goldenberg — https://yanivgoldenberg.com" in notice
    lic = (REPO / "LICENSE").read_text(encoding="utf-8")
    assert "PolyForm Noncommercial License 1.0.0" in lic
    assert "Yaniv Goldenberg" in (REPO / "TRADEMARK.md").read_text(encoding="utf-8")
    assert "https://yanivgoldenberg.com/contact/" in (REPO / "COMMERCIAL.md").read_text(encoding="utf-8")


def test_canary_constants_are_fictional() -> None:
    assert 3 <= len(CANARY_ROWS) <= 5
    for row in CANARY_ROWS:
        assert CANARY_HOST.match(row["site"]), row["site"]
        assert row["canary"] is True
        assert PROJECT_ID in row["notes"]
    assert not {r["site"] for r in CANARY_ROWS} & set(SITES_61), "canaries must never be fetched"


def test_canary_rows_in_published_json() -> None:
    rows = json.loads(PUBLISHED_JSON.read_text(encoding="utf-8"))
    canaries = [r for r in rows if r.get("canary") is True]
    assert canaries == CANARY_ROWS
    assert len(rows) - len(canaries) == 61
    assert rows[-len(canaries):] == canaries, "canaries are appended after the 61 real rows"


def test_canary_rows_in_published_csv() -> None:
    rows = list(csv.DictReader(PUBLISHED_CSV.read_text(encoding="utf-8").splitlines()))
    flags = {r["canary"] for r in rows}
    assert flags == {"true", "false"}, flags
    canary_sites = {r["site"] for r in rows if r["canary"] == "true"}
    assert canary_sites == {r["site"].replace("https://", "") for r in CANARY_ROWS}
    for r in rows:
        if r["canary"] == "true":
            assert r["source"] == CANARY_CSV_SOURCE and r["published_rank"] == "" and r["scored_at"] == ""
