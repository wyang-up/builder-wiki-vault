#!/usr/bin/env python3

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


SOURCES_PATTERN = re.compile(r"^sources:\s*\[(.*?)\]\s*$", re.MULTILINE)


def _to_posix_relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _extract_sources(markdown_text: str) -> list[str]:
    match = SOURCES_PATTERN.search(markdown_text)
    if not match:
        return []

    raw_items = match.group(1).strip()
    if not raw_items:
        return []

    items = []
    for item in raw_items.split(','):
        cleaned = item.strip().strip('"').strip("'")
        if cleaned:
            items.append(cleaned)
    return items


def build_source_map(sources_dir: Path) -> dict[str, str]:
    source_map: dict[str, str] = {}
    if not sources_dir.exists():
        return source_map

    for page in sorted(sources_dir.glob('*.md')):
        content = page.read_text(encoding='utf-8')
        for raw_path in _extract_sources(content):
            source_map[raw_path] = page.stem
    return source_map


def _collect_raw_candidates(root: Path) -> tuple[list[str], list[str]]:
    raw_root = root / 'raw'
    candidates: list[str] = []
    batch_entries: list[str] = []

    if not raw_root.exists():
        return candidates, batch_entries

    for path in sorted(raw_root.rglob('*')):
        if not path.is_file():
            continue

        rel = _to_posix_relative(path, root)
        if rel.startswith('raw/09-archive/'):
            continue

        if '/05-ai-builders/' in rel:
            if path.name == 'digest-zh.md':
                candidates.append(rel)
                batch_entries.append(rel)
            continue

        if path.suffix.lower() in {'.md', '.pdf'}:
            candidates.append(rel)

    return candidates, batch_entries


def collect_ingest_status(root: Path) -> dict[str, list]:
    source_map = build_source_map(root / 'wiki' / 'sources')
    candidates, batch_entries = _collect_raw_candidates(root)

    processed = [
        {'rawPath': raw_path, 'sourcePage': source_map[raw_path]}
        for raw_path in candidates
        if raw_path in source_map
    ]
    unprocessed = [raw_path for raw_path in candidates if raw_path not in source_map]
    updatable = list(processed)

    return {
        'unprocessed': unprocessed,
        'processed': processed,
        'batchEntries': batch_entries,
        'updatable': updatable,
    }


def resolve_ingest_target(root: Path, raw_path: str) -> dict[str, str]:
    normalized = raw_path.strip().lstrip('./')
    full_path = root / normalized

    if normalized.endswith(('feed-x.json', 'feed-podcasts.json', 'feed-blogs.json')) and '/05-ai-builders/' in normalized:
        redirect_path = normalized.rsplit('/', 1)[0] + '/digest-zh.md'
        if (root / redirect_path).exists():
            return {
                'mode': 'batch_redirect',
                'rawPath': normalized,
                'redirectPath': redirect_path,
            }

    if not full_path.exists() or not full_path.is_file():
        return {
            'mode': 'not_found',
            'rawPath': normalized,
        }

    source_map = build_source_map(root / 'wiki' / 'sources')
    if normalized in source_map:
        return {
            'mode': 'update',
            'rawPath': normalized,
            'sourcePage': source_map[normalized],
        }

    return {
        'mode': 'ingest',
        'rawPath': normalized,
    }


def render_status_report(status: dict[str, list]) -> str:
    lines = ['## Ingest Status', '']

    lines.append('### 未处理')
    if status['unprocessed']:
        lines.extend(f"- `{raw_path}`" for raw_path in status['unprocessed'])
    else:
        lines.append('- 无')
    lines.append('')

    lines.append('### 已处理')
    if status['processed']:
        lines.extend(
            f"- `{item['rawPath']}` -> [[{item['sourcePage']}]]" for item in status['processed']
        )
    else:
        lines.append('- 无')
    lines.append('')

    lines.append('### 批次入口')
    if status['batchEntries']:
        lines.extend(f"- `{raw_path}`" for raw_path in status['batchEntries'])
    else:
        lines.append('- 无')
    lines.append('')

    lines.append('### 可更新')
    if status['updatable']:
        lines.extend(
            f"- `{item['rawPath']}` -> [[{item['sourcePage']}]]" for item in status['updatable']
        )
    else:
        lines.append('- 无')

    return '\n'.join(lines)


def render_target_report(result: dict[str, str]) -> str:
    lines = ['## Ingest Target', '']
    lines.append(f"- 模式：`{result['mode']}`")
    lines.append(f"- 路径：`{result['rawPath']}`")

    if result['mode'] == 'update':
        lines.append(f"- 来源页：[[{result['sourcePage']}]]")
    elif result['mode'] == 'batch_redirect':
        lines.append(f"- 建议改用：`{result['redirectPath']}`")
    elif result['mode'] == 'not_found':
        lines.append('- 结果：目标路径不存在')
    elif result['mode'] == 'ingest':
        lines.append('- 结果：该文件将按首次 ingest 处理')

    return '\n'.join(lines)


def main() -> None:
    root = Path(__file__).resolve().parents[4]
    if '--target' in sys.argv:
        index = sys.argv.index('--target')
        if index + 1 >= len(sys.argv):
            raise SystemExit('Missing raw path after --target')
        print(render_target_report(resolve_ingest_target(root, sys.argv[index + 1])))
        return

    status = collect_ingest_status(root)
    if '--json' in sys.argv:
        print(json.dumps(status, ensure_ascii=False, indent=2))
        return
    print(render_status_report(status))


if __name__ == '__main__':
    main()
