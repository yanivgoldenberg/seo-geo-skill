import re, sys
src = open('seo-geo.md').read()
assert src.startswith('---\n'), 'missing YAML frontmatter'
m = re.search(r'^---\n(.*?)\n---', src, re.S)
assert m, 'frontmatter parse'
fm = m.group(1)
assert re.search(r'name:\s*seo-geo', fm), 'name field'
assert re.search(r'version:\s*\d+\.\d+\.\d+', fm), 'semver version'
assert 'Table of Contents' in src, 'TOC section required'
assert '## Phase 0' in src, 'Phase 0 required'
assert '## Phase 17' in src, 'Phase 17 required'
assert '## Phase 18' in src, 'Phase 18 required'
assert '## Phase 19' in src, 'Phase 19 required'
assert '--apply' in src and '--dry-run' in src, 'dry-run safety gates required'
print('ok')
