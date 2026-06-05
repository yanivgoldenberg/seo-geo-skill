"""Deep-link discovery tests.

discover_deep_links is the pure (no-network) function the multi-page scorer
uses to pick which same-host pages to sample alongside the homepage. These
tests pin its same-host filtering, preferred-path ordering, dedupe, homepage
exclusion, and cap so a refactor cannot silently widen the crawl surface.
"""
from benchmark_sites import discover_deep_links

HTML = """
<a href="/about">About</a>
<a href="https://example.com/blog/post-1">Blog</a>
<a href="/team">Team</a>
<a href="https://other.com/docs">External</a>
<a href="/">Home</a>
<a href="https://example.com/">Home abs</a>
<a href="/about">Dup About</a>
<a href="mailto:x@y.com">mail</a>
<a href="/docs/guide#section">Docs anchor</a>
<a href="//169.254.169.254/latest">metadata</a>
"""


def test_prefers_known_paths_dedupes_and_caps() -> None:
    got = discover_deep_links("https://example.com", HTML, limit=3)
    assert got == [
        "https://example.com/about",
        "https://example.com/blog/post-1",
        "https://example.com/team",
    ]


def test_excludes_cross_host_homepage_and_nonhttp() -> None:
    got = discover_deep_links("https://example.com", HTML, limit=99)
    assert "https://other.com/docs" not in got
    assert "https://169.254.169.254/latest" not in got
    assert "https://example.com/" not in got
    assert all(g.startswith("https://example.com/") for g in got)
    assert all("#" not in g for g in got)
    assert len(got) == len(set(got))
