#!/usr/bin/env python3

from __future__ import annotations

import re
from datetime import datetime


def _extract_summary(digest_text: str) -> str:
    match = re.search(r"## 核心摘要\s+(.*?)(?:\n## |\Z)", digest_text, flags=re.S)
    if not match:
        return ''
    return match.group(1).strip()


def _extract_paragraphs(summary_text: str) -> list[str]:
    return [paragraph.strip() for paragraph in summary_text.split('\n\n') if paragraph.strip()]


def _extract_sentences(summary_text: str) -> list[str]:
    normalized = summary_text.replace('\n', ' ')
    parts = re.split(r'(?<=[。！？])', normalized)
    return [part.strip() for part in parts if part.strip()]


def _extract_section_items(digest_text: str, heading: str) -> list[str]:
    pattern = rf"## {re.escape(heading)}\s+(.*?)(?:\n## |\Z)"
    match = re.search(pattern, digest_text, flags=re.S)
    if not match:
        return []

    block = match.group(1).strip()
    items = []
    current = []
    for line in block.splitlines():
        if line.startswith('- '):
            if current:
                items.append(' '.join(current).strip())
            current = [line[2:].strip()]
        elif current and line.strip():
            current.append(line.strip())
    if current:
        items.append(' '.join(current).strip())
    return items


def _pick_summary_points(summary_text: str) -> list[str]:
    sentences = _extract_sentences(summary_text)
    picked = []
    preferred_keywords = [
        '注意力从',
        '执行稳定性',
        '定义问题',
        '安全',
        '长时运行 agent',
        '持续学习',
    ]

    for sentence in sentences:
        if any(keyword in sentence for keyword in preferred_keywords):
            picked.append(sentence)
    for sentence in sentences:
        if sentence not in picked:
            picked.append(sentence)
    return picked[:2]


def _pick_section_signal(items: list[str], preferred_keywords: list[str]) -> str | None:
    for item in items:
        if any(keyword in item for keyword in preferred_keywords):
            return item
    return items[0] if items else None


def _build_key_points(digest_text: str, summary_text: str) -> list[str]:
    key_points = []

    for sentence in _pick_summary_points(summary_text):
        if sentence not in key_points:
            key_points.append(sentence)

    x_items = _extract_section_items(digest_text, 'X / Twitter')
    podcasts_items = _extract_section_items(digest_text, 'Podcasts')

    x_signal = _pick_section_signal(x_items, ['OpenClaw', '执行稳定性', 'GStack', 'agent'])
    if x_signal and x_signal not in key_points:
        key_points.append(x_signal)

    podcast_signal = _pick_section_signal(podcasts_items, ['长时运行 agents', '持续学习', 'generalization', '未来研究方向'])
    if podcast_signal and podcast_signal not in key_points:
        key_points.append(podcast_signal)

    if len(key_points) < 4:
        security_or_org = _pick_section_signal(
            _extract_sentences(summary_text),
            ['安全', 'Vercel', '定义问题', '岗位复杂度', '对外沟通'],
        )
        if security_or_org and security_or_org not in key_points:
            key_points.append(security_or_org)

    return key_points[:4]


def _format_date(date_string: str) -> str:
    return datetime.fromisoformat(date_string.replace('Z', '+00:00')).strftime('%Y-%m-%d')


def _contains_any(text: str, keywords: list[str]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def _contains_positive_long_running_signal(text: str) -> bool:
    lowered = text.lower()
    if '没有讨论长时运行 agent' in lowered or '没有讨论长时运行 agents' in lowered:
        return False
    return any(keyword in lowered for keyword in ['long running agent', 'long-running agent', '长时运行 agent'])


def build_ai_builders_update_payload(digest_text: str, feed_x: dict, feed_podcasts: dict, feed_blogs: dict) -> dict[str, list | str]:
    summary = _extract_summary(digest_text)
    key_points = _build_key_points(digest_text, summary)
    normalized_digest = digest_text.lower()

    x_builders = len(feed_x.get('x', []))
    total_tweets = sum(len(builder.get('tweets', [])) for builder in feed_x.get('x', []))
    podcast_count = len(feed_podcasts.get('podcasts', []))
    blog_count = len(feed_blogs.get('blogs', []))

    published_dates = []
    for builder in feed_x.get('x', []):
        for tweet in builder.get('tweets', []):
            created_at = tweet.get('createdAt')
            if created_at:
                published_dates.append(_format_date(created_at))
    for podcast in feed_podcasts.get('podcasts', []):
        published_at = podcast.get('publishedAt')
        if published_at:
            published_dates.append(_format_date(published_at))

    published_range = '未知'
    if published_dates:
        published_range = f"{min(published_dates)} 至 {max(published_dates)}（按同批次 feed 文件）"

    urls = []
    for builder in feed_x.get('x', []):
        for tweet in builder.get('tweets', []):
            if tweet.get('url'):
                urls.append(tweet['url'])
    for podcast in feed_podcasts.get('podcasts', []):
        if podcast.get('url'):
            urls.append(podcast['url'])

    handles = []
    for builder in feed_x.get('x', []):
        label = builder.get('name') or builder.get('handle')
        if label:
            handles.append(label)
    for podcast in feed_podcasts.get('podcasts', []):
        if podcast.get('name'):
            handles.append(podcast['name'])

    concepts = []
    links = []

    if _contains_any(normalized_digest, ['openclaw']):
        concepts.append('[[OpenClaw]] — 代表 agent 执行稳定性约束')
    if _contains_any(normalized_digest, ['gstack']):
        concepts.append('[[GStack]] — 代表浏览器与技能补层')
    if _contains_any(normalized_digest, ['agent 工作流', 'agentic task', '执行链条', 'subagent', 'cron']):
        links.append('[[AgenticWorkflows]] — 代表执行链路主题')
    if _contains_positive_long_running_signal(normalized_digest):
        links.append('[[LongRunningAgents]] — 代表长期能力目标')

    return {
        'summary': summary,
        'key_points': key_points,
        'evidence_lines': [
            f"来源类型统计：X {x_builders} 位 builder、{total_tweets} 条推文；Podcast {podcast_count} 期节目；Blog {blog_count} 篇文章",
            f"关键账号或作者：{'、'.join(handles)}",
            f"发布时间范围：{published_range}",
            f"原始链接：{'、'.join(urls)}",
            '缺失项说明：本批没有新的博客文章' if blog_count == 0 else '缺失项说明：无',
        ],
        'concepts': concepts,
        'links': links,
    }
