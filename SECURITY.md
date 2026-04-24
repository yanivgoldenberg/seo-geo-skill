# Security policy

If you find a security issue in this skill (a write path that exfiltrates data, a code path that mutates credentials, a filter that injects unescaped content into someone's site), please email yaniv@yanivgoldenberg.com directly. Do NOT open a public issue.

Include:
- Which phase / file
- Reproducer
- Suspected blast radius

I respond within 48 hours. Fixes ship as a point release.

## Banned endpoint list

Phase 17 explicitly bans the skill from touching:
- `POST /wp-json/wp/v2/users/{id}` with a password field
- `DELETE /wp-json/wp/v2/users/{id}`
- Any API key / app password / Coolify env var rotation

If you find the skill calling any of these, that is a security bug. Email.
