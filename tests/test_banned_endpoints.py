"""Banned-endpoint tests.

The skill's Phase 17 safety contract bans writes to credential/identity
endpoints. These tests pin the policy so a refactor cannot silently
remove a banned entry or add an example that calls one.
"""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "seo-geo.md"
SECURITY = REPO / "SECURITY.md"
EXAMPLES = REPO / "examples"

REQUIRED_BANS = (
    r"POST /wp-json/wp/v2/users/\{id\}",
    r"DELETE /wp-json/wp/v2/users/\{id\}",
)

DANGEROUS_CALL_PATTERNS = (
    re.compile(r"DELETE\s+/wp-json/wp/v2/users/"),
    re.compile(r"POST\s+/wp-json/wp/v2/users\b(?!/\{id\})"),
)


def test_skill_declares_banned_list() -> None:
    body = SKILL.read_text(encoding="utf-8")
    for pattern in REQUIRED_BANS:
        assert re.search(pattern, body), f"seo-geo.md missing banned endpoint: {pattern}"


def test_security_policy_mirrors_banned_list() -> None:
    body = SECURITY.read_text(encoding="utf-8")
    assert "Banned endpoint list" in body
    assert "users/{id}" in body


def test_examples_do_not_call_banned_endpoints() -> None:
    if not EXAMPLES.exists():
        return
    offenders: list[str] = []
    for path in EXAMPLES.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix not in {".md", ".py", ".sh", ".js", ".ts", ".json", ".yaml", ".yml"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in DANGEROUS_CALL_PATTERNS:
            if pattern.search(text):
                offenders.append(f"{path.relative_to(REPO)}: matches {pattern.pattern}")
    assert not offenders, "Examples call banned endpoints:\n  " + "\n  ".join(offenders)


def test_skill_body_has_is_banned_guard() -> None:
    body = SKILL.read_text(encoding="utf-8")
    assert "_is_banned" in body, "seo-geo.md must document an _is_banned() guard"
    assert "BANNED_ENDPOINTS" in body, "seo-geo.md must define a BANNED_ENDPOINTS constant"


if __name__ == "__main__":
    for name in [n for n in dir() if n.startswith("test_")]:
        globals()[name]()
        print(f"ok {name}")
