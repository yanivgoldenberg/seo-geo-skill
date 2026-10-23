# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Copyright (c) Yaniv Goldenberg - https://yanivgoldenberg.com (see NOTICE)
import glob
import json
import sys

errs = []
for path in glob.glob('examples/**/*.json', recursive=True):
    try:
        with open(path) as fh:
            json.load(fh)
    except json.JSONDecodeError as e:
        errs.append(f'{path}: {e}')
if errs:
    print('\n'.join(errs))
    sys.exit(1)
print(f'ok - {len(glob.glob("examples/**/*.json", recursive=True))} JSON fixtures valid')
