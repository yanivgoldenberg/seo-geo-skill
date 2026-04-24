import json, os, sys, glob
errs = []
for path in glob.glob('examples/**/*.json', recursive=True):
    try:
        json.load(open(path))
    except json.JSONDecodeError as e:
        errs.append(f'{path}: {e}')
if errs:
    print('\n'.join(errs)); sys.exit(1)
print(f'ok - {len(glob.glob("examples/**/*.json", recursive=True))} JSON fixtures valid')
