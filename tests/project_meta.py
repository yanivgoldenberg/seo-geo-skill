# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Copyright (c) Yaniv Goldenberg - https://yanivgoldenberg.com (see NOTICE)
"""Project identity shared by the scorer, scripts and tests.

PROJECT_ID is a public, searchable fingerprint (see README "Attribution &
fingerprint"). CANARY_ROWS are fictional, clearly flagged rows appended to the
published benchmark dataset so copies of it are identifiable. They use reserved
.example / .invalid names, are never fetched and never count in any statistic.
"""

PROJECT_ID = "YG-SEOGEO-754F1B9DC9A7"
VERSION = "1.17.0"
USER_AGENT = f"seo-geo-skill/{VERSION} (+https://yanivgoldenberg.com/)"
CANARY_CSV_SOURCE = f"canary-{PROJECT_ID}"

_CANARY_NOTE = "CANARY: fictional site, not a measurement; identifies copies of this dataset"

CANARY_ROWS = [
    {"site": "https://northwind-lighthouse.example", "technical": 11, "schema": 7, "geo": 9,
     "onpage": 5, "aeo": 3, "eeat": 2, "notes": [_CANARY_NOTE, PROJECT_ID], "composite": 37,
     "canary": True},
    {"site": "https://quillmere-analytics.invalid", "technical": 13, "schema": 3, "geo": 5,
     "onpage": 7, "aeo": 1, "eeat": 4, "notes": [_CANARY_NOTE, PROJECT_ID], "composite": 33,
     "canary": True},
    {"site": "https://brightfern-labs.example", "technical": 9, "schema": 11, "geo": 4,
     "onpage": 6, "aeo": 2, "eeat": 1, "notes": [_CANARY_NOTE, PROJECT_ID], "composite": 33,
     "canary": True},
]
