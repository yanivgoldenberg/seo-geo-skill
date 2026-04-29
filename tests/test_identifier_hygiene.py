"""Identifier hygiene tests.

The skill body (seo-geo.md) that installers copy to ~/.claude/skills/ MUST
be author-neutral. Author credit lives in README.md and CONTRIBUTING.md, which
are NOT installed by end users.

We check:
- No author name or LinkedIn handle in seo-geo.md body
- No former-employer or client names in seo-geo.md body
- No YANIV_* env var names anywhere in the skill body
- No banned endpoint patterns leak into example snippets
"""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "seo-geo.md"
PHP_PLUGIN = REPO / "examples" / "wordpress" / "yg-geo-fixes" / "yg-geo-fixes.php"

SKILL_BANNED_PATTERNS = [
    r"\bYaniv Goldenberg\b",
    r"\byaniv\.goldenberg\b",
    r"linkedin\.com/in/yanivgoldenberg",
    r"\bElementor Ltd\b",
    r"\bRiverside\.fm\b",
    r"\bcnvrg\.io\b",
    r"YANIV_WP_APP_PASSWORD",
    r"YANIV_WEBSITE_URL",
    r"WEBSITE_WP_ADMIN_USER",
]

# Author URL and handle are allowed ONLY in the "Author: see repo README" pointer
# and the one `/seo-geo-skill` repo URL. Anything else is a leak.
ALLOWED_AUTHOR_REFERENCES = [
    "github.com/yanivgoldenberg/seo-geo-skill",
]

# In any code snippet, these banned endpoints must NOT appear as live calls.
# (They may appear in documentation/"banned list" context.)
BANNED_ENDPOINT_CALLS = [
    (r"httpx\.post\([^)]*/wp/v2/users/1[^)]*password", "password write to users/{id}"),
    (r"httpx\.post\([^)]*/wp/v2/users\s*['\"]", "user creation via httpx"),
    (r"httpx\.delete\([^)]*/wp/v2/users/", "user deletion via httpx"),
]


def test_skill_body_has_no_persona_leaks() -> None:
    body = SKILL.read_text(encoding="utf-8")
    for pattern in SKILL_BANNED_PATTERNS:
        matches = re.findall(pattern, body, re.IGNORECASE)
        if pattern == r"\bYaniv Goldenberg\b":
            # This pattern is allowed inside the repo URL only; scrub allowed refs first.
            body_scrubbed = body
            for allowed in ALLOWED_AUTHOR_REFERENCES:
                body_scrubbed = body_scrubbed.replace(allowed, "<ALLOWED_REF>")
            matches = re.findall(pattern, body_scrubbed, re.IGNORECASE)
        assert not matches, f"skill body contains banned pattern {pattern!r} ({len(matches)} hits)"


def test_skill_body_has_no_banned_endpoint_calls() -> None:
    body = SKILL.read_text(encoding="utf-8")
    for pattern, label in BANNED_ENDPOINT_CALLS:
        matches = re.findall(pattern, body, re.IGNORECASE | re.DOTALL)
        assert not matches, f"skill body contains banned endpoint call ({label}): {matches[:1]}"


def test_php_plugin_uses_no_unserialize() -> None:
    body = PHP_PLUGIN.read_text(encoding="utf-8")
    code_only = "\n".join(
        line for line in body.splitlines()
        if not line.lstrip().startswith(("//", "*", "#")) and not line.lstrip().startswith("/*")
    )
    assert "unserialize(" not in code_only, "PHP plugin must not call unserialize() in code"


def test_php_plugin_admin_notice_requires_cap() -> None:
    body = PHP_PLUGIN.read_text(encoding="utf-8")
    assert "current_user_can" in body, "admin_notices hook must check current_user_can()"


if __name__ == "__main__":
    for name in [n for n in dir() if n.startswith("test_")]:
        globals()[name]()
        print(f"ok {name}")
