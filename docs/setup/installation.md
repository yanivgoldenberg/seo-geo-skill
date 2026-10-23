# Installation

## Scope and safety

Do not put passwords, API keys, browser profiles, database exports, or
customer data in Git.

These steps clone the source and run offline validation. They do not install
global agent profiles, change a website, start services, or configure
scheduled jobs. Website audits and live benchmarks require network access and
may require separate credentials. Start with audit-only behavior and review
proposed writes.

## ChatGPT or another connector-based agent

Ask the agent to retrieve `README.md`, `seo-geo.md`, and `docs/SCORING.md`
from this repository, and report the revision it used when available. Request
the relevant supporting files explicitly if they are not retrieved
automatically.

Connector file access is not proof that Python tools ran, that a website was
audited, or that publishing credentials are available. Keep operational
secrets outside the repository and grant access separately only when needed.

## Windows PowerShell

Use an isolated folder that does not already exist.

```powershell
git clone https://github.com/yanivgoldenberg/seo-geo-skill.git seo-geo-local
if ($LASTEXITCODE -ne 0) { throw 'Clone failed' }
Set-Location seo-geo-local
git rev-parse HEAD
py -3.12 -m venv .venv
if ($LASTEXITCODE -ne 0) { throw 'Python 3.12 environment creation failed' }
& .\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed' }
$env:PYTHONUTF8 = '1'
& .\.venv\Scripts\python.exe -m pytest -q --ignore=tests/test_live_endpoints.py
if ($LASTEXITCODE -ne 0) { throw 'Offline validation failed' }
```

If the Python launcher does not know Python 3.12, use the full path to your
existing Python 3.12 executable instead. Do not fall back to a different version.

## Linux, macOS or WSL2

```bash
git clone https://github.com/yanivgoldenberg/seo-geo-skill.git seo-geo-local &&
cd seo-geo-local &&
git rev-parse HEAD &&
python3.12 -m venv .venv &&
.venv/bin/python -m pip install -r requirements-dev.txt &&
PYTHONUTF8=1 .venv/bin/python -m pytest -q --ignore=tests/test_live_endpoints.py
```

Run tests from the repository root. The excluded test contacts live websites;
the offline suite does not verify current rankings, live endpoint availability,
or publishing integrations. Scheduled benchmarking is a separate workflow.
Direct dependencies are pinned; transitive dependencies are not a complete lock.

## Agent usage and organization

Open the clone in your agent and explicitly load `seo-geo.md` and
`docs/SCORING.md`. Keep relative supporting files available. Registering a slash
command is agent-specific and is separate from cloning this repository.
Do not overwrite an existing skill installation or another release branch.

| Path | Purpose |
| --- | --- |
| `seo-geo.md` | Skill instructions and safety gates |
| `docs/SCORING.md` | Canonical scoring rubric |
| `docs/` | Reference material, benchmark history, setup |
| `scripts/` | Supporting tools and live benchmark runners |
| `tests/` | Offline checks, fixtures, and the separate live endpoint check |
| `requirements-dev.txt` | Pinned direct dependencies for validation |

Record `git rev-parse HEAD` with each audit. Do not silently switch branches or
update a consuming repository's submodule: alternate branches may contain work
not yet merged into `main`.
