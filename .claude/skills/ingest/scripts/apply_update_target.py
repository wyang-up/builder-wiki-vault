#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from pathlib import Path

from ingest_status import resolve_ingest_target
from update_source_page import rebuild_source_page


def apply_update_target(
    root: Path,
    raw_path: str,
    updated_date: str,
    *,
    summary: str | None = None,
    key_points: list[str] | None = None,
    evidence_lines: list[str] | None = None,
    concepts: list[str] | None = None,
    links: list[str] | None = None,
) -> dict[str, str]:
    target = resolve_ingest_target(root, raw_path)
    if target['mode'] != 'update':
        raise ValueError(f"Expected update mode, got {target['mode']}")

    if not any([
        summary and summary.strip(),
        key_points,
        evidence_lines,
        concepts,
        links,
    ]):
        raise ValueError('Rebuild payload is empty')

    source_path = root / 'wiki' / 'sources' / f"{target['sourcePage']}.md"
    original = source_path.read_text(encoding='utf-8')
    rebuilt = rebuild_source_page(
        original_markdown=original,
        updated_date=updated_date,
        summary=summary if summary is not None else '',
        key_points=key_points or [],
        evidence_lines=evidence_lines or [],
        concepts=concepts or [],
        links=links or [],
    )
    source_path.write_text(rebuilt, encoding='utf-8')

    return {
        'mode': 'update',
        'rawPath': target['rawPath'],
        'sourcePage': target['sourcePage'],
        'sourcePath': source_path.relative_to(root).as_posix(),
    }


def main() -> None:
    if '--target' not in sys.argv or '--date' not in sys.argv:
        raise SystemExit('Usage: apply_update_target.py --target <raw-path> --date <YYYY-MM-DD>')

    target_index = sys.argv.index('--target')
    date_index = sys.argv.index('--date')
    if target_index + 1 >= len(sys.argv) or date_index + 1 >= len(sys.argv):
        raise SystemExit('Missing value for --target or --date')

    root = Path(__file__).resolve().parents[4]
    result = apply_update_target(root, sys.argv[target_index + 1], sys.argv[date_index + 1])
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
