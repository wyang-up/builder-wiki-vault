import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, writeFile, mkdir } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

import { loadJSONWithFallback, loadTextWithFallback } from './prepare-digest.js';

test('loadJSONWithFallback falls back to local file when remote returns not found', async () => {
  const dir = await mkdtemp(join(tmpdir(), 'ai-builders-'));
  const localPath = join(dir, 'feed-x.json');
  await writeFile(localPath, JSON.stringify({ x: [{ name: 'Local Builder', tweets: [] }] }), 'utf-8');

  const result = await loadJSONWithFallback('https://example.com/feed-x.json', localPath, async () => ({
    ok: false,
    json: async () => {
      throw new Error('should not read json when response is not ok');
    },
  }));

  assert.deepEqual(result, { x: [{ name: 'Local Builder', tweets: [] }] });
});

test('loadTextWithFallback falls back to local prompt when remote returns not found', async () => {
  const dir = await mkdtemp(join(tmpdir(), 'ai-builders-'));
  const promptsDir = join(dir, 'prompts');
  await mkdir(promptsDir, { recursive: true });
  const localPath = join(promptsDir, 'translate.md');
  await writeFile(localPath, 'local prompt', 'utf-8');

  const result = await loadTextWithFallback('https://example.com/translate.md', localPath, async () => ({
    ok: false,
    text: async () => {
      throw new Error('should not read text when response is not ok');
    },
  }));

  assert.equal(result, 'local prompt');
});
