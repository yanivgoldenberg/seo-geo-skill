# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Attribution and required notices: see NOTICE and LICENSE.
"""Offline semantic acceptance integrity, never ranking or real-world certification."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Callable

PROFILE = "composed-content/2"
CONTROLS = (
    "buyer_decision", "claim_evidence_status", "original_useful_artifact",
    "locale_type_routing", "identity_offer_faq_parity", "metadata_date_parity",
    "contextual_link_journeys", "derived_content_freshness", "reader_task_review",
    "measurement_boundaries",
)
RELEASE_STAGES = ("source_review", "local_checks", "ci", "preview", "canonical_readback", "production", "public_readback")
CONTENT_TYPES = ("BLOG_POST", "GUIDE", "SERVICE", "HUB", "UTILITY")


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_semantic(data: dict[str, Any], evidence_root: Any, evidence_check: Callable,
                      *, expected_phase: str | None = None) -> list[str]:
    """Require every named control and current bindings; hashes do not prove truth.

    Candidate means current semantic/source/local proof. Hosted and publication
    stages remain explicitly pending until observed; they cannot be called live.
    """
    errors: list[str] = []
    if not _text(data.get("revision")) or not isinstance(data.get("inputs"), dict) or not data["inputs"]:
        errors.append("SEMANTIC_INPUTS_REQUIRED")
    if data.get("method_profile") != PROFILE:
        errors.append("SEMANTIC_PROFILE_REQUIRED")
    acceptance = data.get("semantic_acceptance")
    if not isinstance(acceptance, dict) or acceptance.get("schema") != "semantic-content-acceptance/1":
        return errors + ["SEMANTIC_ACCEPTANCE_REQUIRED"]
    phase = acceptance.get("phase")
    if phase not in ("candidate", "publication") or expected_phase is not None and phase != expected_phase:
        errors.append("SEMANTIC_PHASE_BINDING")
    if not _text(acceptance.get("reviewer")) or acceptance.get("findings") != []:
        errors.append("SEMANTIC_UNRESOLVED_REVIEW")
    release = acceptance.get("release_checks")
    if not isinstance(release, list) or any(not isinstance(row, dict) for row in release):
        release = []
    if len(release) != len(RELEASE_STAGES) or {row.get("id") for row in release if isinstance(row.get("id"), str)} != set(RELEASE_STAGES):
        errors.append("SEMANTIC_RELEASE_SET")
    for row in release:
        rid = row.get("id")
        required = phase == "publication" or rid in ("source_review", "local_checks")
        if row.get("status") == "PASS":
            if (not _text(row.get("reviewer")) or row.get("revision") != data.get("revision") or
                    row.get("inputs") != data.get("inputs") or evidence_check(row.get("evidence"), evidence_root)):
                errors.append("SEMANTIC_RELEASE_EVIDENCE:" + str(rid))
        elif required or row.get("status") != "PENDING" or not _text(row.get("reason")):
            errors.append("SEMANTIC_RELEASE_NOT_PASS:" + str(rid))
    pages = data.get("pages")
    if not isinstance(pages, list) or not pages or any(not isinstance(page, dict) for page in pages):
        errors.append("SEMANTIC_PAGE_SET")
    for page in pages if isinstance(pages, list) else []:
        if not isinstance(page, dict):
            continue
        path = str(page.get("route"))
        if not path.startswith('/') or path.startswith('//') or not _text(page.get('locale')):
            errors.append("SEMANTIC_PAGE_IDENTITY:" + path)
        if page.get("content_type") not in CONTENT_TYPES:
            errors.append("SEMANTIC_CONTENT_TYPE:" + path)
        rows = page.get("semantic_checks")
        if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
            rows = []
        if len(rows) != len(CONTROLS) or {r.get("id") for r in rows if isinstance(r.get("id"), str)} != set(CONTROLS):
            errors.append("SEMANTIC_CONTROL_SET:" + path)
        method = page.get("method")
        whole = method.get("whole_page_review") if isinstance(method, dict) else None
        source = whole.get("source_sha256") if isinstance(whole, dict) else None
        if not isinstance(source, str) or not re.fullmatch(r'[0-9a-f]{64}', source):
            errors.append("SEMANTIC_SOURCE_BINDING:" + path)
        proposed = page.get("content_sha256")
        if not isinstance(proposed, str) or not re.fullmatch(r'[0-9a-f]{64}', proposed):
            errors.append("SEMANTIC_COPY_BINDING:" + path)
        for row in rows:
            cid = str(row.get("id"))
            if row.get("status") != "PASS" or row.get("findings") != []:
                errors.append("SEMANTIC_CONTROL_NOT_PASS:" + path + ":" + cid)
            if (not _text(row.get("reviewer")) or not _text(row.get("method")) or
                    row.get("revision") != data.get("revision") or row.get("inputs") != data.get("inputs") or
                    row.get("locale") != page.get("locale") or row.get("source_sha256") != source or
                    row.get("content_sha256") != page.get("content_sha256") or
                    evidence_check(row.get("evidence"), evidence_root)):
                errors.append("SEMANTIC_CONTROL_BINDING:" + path + ":" + cid)
        questions = page.get("subquestions")
        if not isinstance(questions, list) or not questions or any(not isinstance(q, dict) for q in questions):
            errors.append("SEMANTIC_QUESTION_SET:" + path)
        for q in questions if isinstance(questions, list) else []:
            if not isinstance(q, dict):
                continue
            journey = q.get("semantic_journey")
            if (not isinstance(journey, dict) or journey.get("destination_type") not in CONTENT_TYPES or
                    not all(_text(journey.get(k)) for k in ("reader_task", "offer_route", "next_action")) or
                    not journey.get("offer_route", "").startswith("/") or journey.get("offer_route", "").startswith("//")):
                errors.append("SEMANTIC_QUESTION_JOURNEY:" + str(q.get("id")))
    return sorted(set(errors))


MAX_LOCAL_BYTES = 16 * 1024 * 1024


def _bounded_bytes(path: Path) -> bytes:
    """Read at most cap plus one, including files that grow after metadata checks."""
    with path.open('rb') as stream:
        data = stream.read(MAX_LOCAL_BYTES + 1)
    if len(data) > MAX_LOCAL_BYTES:
        raise ValueError('FILE_BOUND')
    return data


def evidence_problem(value: Any, root: Path) -> str | None:
    """Bounded regular local bytes only. Never follows links or reads credentials."""
    if not isinstance(value, dict) or not _text(value.get('path')) or not isinstance(value.get('sha256'), str) or not re.fullmatch(r'[0-9a-f]{64}', value['sha256']):
        return 'EVIDENCE_SHAPE'
    name = value['path']
    rel = Path(name)
    if rel.is_absolute() or re.match(r'^[A-Za-z]:', name) or '\\' in name or any(p in {'.', '..'} or p.startswith('.') for p in rel.parts):
        return 'EVIDENCE_PATH'
    try:
        current = root.resolve()
        for part in rel.parts:
            current = current / part
            if current.is_symlink() or (hasattr(current, 'is_junction') and current.is_junction()):
                return 'EVIDENCE_PATH'
        if not current.is_file() or not current.resolve().is_relative_to(root.resolve()) or current.stat().st_size > 16 * 1024 * 1024:
            return 'EVIDENCE_PATH'
        return None if hashlib.sha256(_bounded_bytes(current)).hexdigest() == value['sha256'] else 'EVIDENCE_HASH'
    except (OSError, ValueError, TypeError):
        return 'EVIDENCE_PATH'


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('record', type=Path)
    parser.add_argument('--evidence-root', required=True, type=Path)
    parser.add_argument('--phase', choices=('candidate', 'publication'), required=True)
    args = parser.parse_args()
    try:
        if args.record.stat().st_size > 16 * 1024 * 1024:
            raise ValueError('RECORD_BOUND')
        data = json.loads(_bounded_bytes(args.record).decode('utf-8'))
        if not isinstance(data, dict):
            raise ValueError('RECORD_SHAPE')
        errors = validate_semantic(data, args.evidence_root, evidence_problem, expected_phase=args.phase)
    except (OSError, ValueError, TypeError) as exc:
        print(json.dumps({'status':'INPUT_REFUSED','error':str(exc)}))
        return 2
    print(json.dumps({'status':'FAIL' if errors else 'PASS_SEMANTIC_CONTROL_INTEGRITY_ONLY','phase':args.phase,'errors':errors,'ranking_citation_revenue':'NOT_ESTABLISHED'}))
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
