#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from pathlib import Path


SECTION_ORDER = [
    '## 核心摘要',
    '## 关键论点',
    '## 证据来源',
    '## 可沉淀概念',
    '## 关联连接',
]


def _render_bullets(lines: list[str]) -> str:
    cleaned = [line.strip() for line in lines if line and line.strip()]
    if not cleaned:
        return ''
    return '\n'.join(f'- {line}' if not line.startswith('- ') else line for line in cleaned)


def _extract_wikilink_key(line: str) -> str:
    match = re.search(r'\[\[([^\]]+)\]\]', line)
    return match.group(1) if match else line.strip()


def _merge_bullets(existing: str, new_lines: list[str]) -> str:
    merged: list[str] = []
    seen: set[str] = set()

    for line in existing.splitlines():
        cleaned = line.strip()
        if not cleaned:
            continue
        key = _extract_wikilink_key(cleaned)
        if key not in seen:
            merged.append(cleaned)
            seen.add(key)

    for line in new_lines:
        cleaned = line.strip()
        if not cleaned:
            continue
        bullet = cleaned if cleaned.startswith('- ') else f'- {cleaned}'
        key = _extract_wikilink_key(bullet)
        if key not in seen:
            merged.append(bullet)
            seen.add(key)

    return '\n'.join(merged)


def _update_last_updated(text: str, date: str) -> str:
    return re.sub(r'^last_updated:\s*.+$', f'last_updated: {date}', text, flags=re.MULTILINE)


def _split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith('---\n'):
        return '', text.strip()

    parts = text.split('\n---\n', 1)
    if len(parts) != 2:
        return '', text.strip()
    return parts[0] + '\n---', parts[1].strip()


def _extract_sections(body: str) -> dict[str, str]:
    matches = list(re.finditer(r'^##\s+.+$', body, flags=re.MULTILINE))
    sections: dict[str, str] = {}

    for idx, match in enumerate(matches):
        header = match.group(0).strip()
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(body)
        content = body[start:end].strip()
        sections[header] = content

    return sections


def normalize_source_page(markdown_text: str, updated_date: str) -> str:
    frontmatter, body = _split_frontmatter(markdown_text)
    if frontmatter:
        frontmatter = _update_last_updated(frontmatter, updated_date)

    sections = _extract_sections(body)
    rendered_sections = []
    for header in SECTION_ORDER:
        content = sections.get(header, '')
        if content:
            rendered_sections.append(f'{header}\n{content}')
        else:
            rendered_sections.append(f'{header}\n')

    if frontmatter:
        return f"{frontmatter}\n\n" + '\n\n'.join(rendered_sections).rstrip() + '\n'
    return '\n\n'.join(rendered_sections).rstrip() + '\n'


def rebuild_source_page(
    *,
    original_markdown: str,
    updated_date: str,
    summary: str,
    key_points: list[str],
    evidence_lines: list[str],
    concepts: list[str],
    links: list[str],
) -> str:
    frontmatter, body = _split_frontmatter(original_markdown)
    if frontmatter:
        frontmatter = _update_last_updated(frontmatter, updated_date)

    sections = _extract_sections(body)
    rebuilt_sections = {
        '## 核心摘要': summary.strip(),
        '## 关键论点': _render_bullets(key_points),
        '## 证据来源': _render_bullets(evidence_lines),
        '## 可沉淀概念': _merge_bullets(sections.get('## 可沉淀概念', ''), concepts),
        '## 关联连接': _merge_bullets(sections.get('## 关联连接', ''), links),
    }

    rendered_sections = []
    for header in SECTION_ORDER:
        content = rebuilt_sections.get(header, '')
        if content:
            rendered_sections.append(f'{header}\n{content}')
        else:
            rendered_sections.append(f'{header}\n')

    if frontmatter:
        return f"{frontmatter}\n\n" + '\n\n'.join(rendered_sections).rstrip() + '\n'
    return '\n\n'.join(rendered_sections).rstrip() + '\n'


def update_source_page_file(page_path: Path, updated_date: str) -> str:
    normalized = normalize_source_page(page_path.read_text(encoding='utf-8'), updated_date)
    page_path.write_text(normalized, encoding='utf-8')
    return normalized


def main() -> None:
    if '--file' not in sys.argv or '--date' not in sys.argv:
        raise SystemExit('Usage: update_source_page.py --file <path> --date <YYYY-MM-DD>')

    file_index = sys.argv.index('--file')
    date_index = sys.argv.index('--date')
    if file_index + 1 >= len(sys.argv) or date_index + 1 >= len(sys.argv):
        raise SystemExit('Missing value for --file or --date')

    page_path = Path(sys.argv[file_index + 1])
    updated_date = sys.argv[date_index + 1]
    print(update_source_page_file(page_path, updated_date), end='')


if __name__ == '__main__':
    main()
