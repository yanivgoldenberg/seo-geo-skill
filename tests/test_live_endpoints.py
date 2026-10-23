# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Copyright (c) Yaniv Goldenberg - https://yanivgoldenberg.com (see NOTICE)
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from project_meta import USER_AGENT  # noqa: E402

urls = ['https://yanivgoldenberg.com/llms.txt', 'https://yanivgoldenberg.com/favicon.ico']
for u in urls:
    try:
        r = requests.get(u, timeout=10, headers={"User-Agent": USER_AGENT})
        print(u, r.status_code)
        assert r.status_code == 200
    except Exception as e:
        print(u, 'FAIL', e)
