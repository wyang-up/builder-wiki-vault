#!/usr/bin/env node

import { mkdir, readFile, writeFile } from 'fs/promises';
import { join } from 'path';

function parseArgs(argv) {
  const args = { language: 'zh' };

  for (let index = 0; index < argv.length; index += 1) {
    const key = argv[index];
    const value = argv[index + 1];

    if (!key.startsWith('--') || value == null || value.startsWith('--')) {
      continue;
    }

    args[key.slice(2)] = value;
    index += 1;
  }

  return args;
}

async function readStdin() {
  const chunks = [];

  for await (const chunk of process.stdin) {
    chunks.push(chunk);
  }

  return Buffer.concat(chunks).toString('utf-8');
}

function toBatchDate(input) {
  const date = input ? new Date(input) : new Date();

  if (Number.isNaN(date.getTime())) {
    throw new Error(`Invalid date: ${input}`);
  }

  const year = String(date.getUTCFullYear());
  const month = String(date.getUTCMonth() + 1).padStart(2, '0');
  const day = String(date.getUTCDate()).padStart(2, '0');

  return `${year}-${month}-${day}`;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const digest = await readStdin();

  if (!args.root) {
    throw new Error('Missing required argument: --root');
  }

  if (!args.payload) {
    throw new Error('Missing required argument: --payload');
  }

  if (!digest.trim()) {
    throw new Error('Digest content is empty');
  }

  const payload = JSON.parse(await readFile(args.payload, 'utf-8'));
  const language = args.language || 'zh';
  const batchDate = toBatchDate(args.date || payload.generatedAt || payload.stats?.feedGeneratedAt);
  const batchDir = join(args.root, 'raw', '05-ai-builders', batchDate);
  const primaryFile = `digest-${language}.md`;

  await mkdir(batchDir, { recursive: true });

  const feedX = {
    generatedAt: payload.stats?.feedGeneratedAt || payload.generatedAt || null,
    x: payload.x || [],
    stats: {
      xBuilders: payload.stats?.xBuilders || 0,
      totalTweets: payload.stats?.totalTweets || 0,
    },
  };

  const feedPodcasts = {
    generatedAt: payload.stats?.feedGeneratedAt || payload.generatedAt || null,
    podcasts: payload.podcasts || [],
    stats: {
      podcastEpisodes: payload.stats?.podcastEpisodes || 0,
    },
  };

  const feedBlogs = {
    generatedAt: payload.stats?.feedGeneratedAt || payload.generatedAt || null,
    blogs: payload.blogs || [],
    stats: {
      blogPosts: payload.stats?.blogPosts || 0,
    },
  };

  const manifest = {
    source: 'ai-builders',
    batchDate,
    generatedAt: payload.generatedAt || null,
    feedGeneratedAt: payload.stats?.feedGeneratedAt || null,
    language,
    primaryFile,
    evidenceFiles: ['feed-x.json', 'feed-podcasts.json', 'feed-blogs.json'],
    stats: {
      xBuilders: payload.stats?.xBuilders || 0,
      totalTweets: payload.stats?.totalTweets || 0,
      podcastEpisodes: payload.stats?.podcastEpisodes || 0,
      blogPosts: payload.stats?.blogPosts || 0,
    },
  };

  await writeFile(join(batchDir, primaryFile), digest, 'utf-8');
  await writeFile(join(batchDir, 'feed-x.json'), `${JSON.stringify(feedX, null, 2)}\n`, 'utf-8');
  await writeFile(join(batchDir, 'feed-podcasts.json'), `${JSON.stringify(feedPodcasts, null, 2)}\n`, 'utf-8');
  await writeFile(join(batchDir, 'feed-blogs.json'), `${JSON.stringify(feedBlogs, null, 2)}\n`, 'utf-8');
  await writeFile(join(batchDir, 'manifest.json'), `${JSON.stringify(manifest, null, 2)}\n`, 'utf-8');

  process.stdout.write(`${JSON.stringify({ status: 'ok', batchDir, primaryFile: join(batchDir, primaryFile) })}\n`);
}

main().catch((error) => {
  console.error(JSON.stringify({ status: 'error', message: error.message }));
  process.exit(1);
});
