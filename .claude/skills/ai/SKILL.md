---
name: ai
description: AI builders raw batch generator — fetches the latest AI builder updates and writes a local batch under raw/05-ai-builders/YYYY-MM-DD/. Use when the user invokes /ai or asks to pull the latest AI builder updates into this vault.
user-invocable: true
---

# ai 技能

## 核心目标

将最新一批 AI builder 动态抓取并整理为本地原始资料，写入当前知识库的 `raw/05-ai-builders/YYYY-MM-DD/` 目录。

本技能只负责生成原始批次，不自动执行 `/ingest`。生成完成后，应明确提示用户下一步可执行 `/ingest`、`/query` 和 `/lint`。

## 触发逻辑

- 用户输入 `/ai`
- 用户要求“拉取最新 AI builder 动态”
- 用户要求“生成今天的 AI builders 原始批次”

## 输出目录规范

每次运行生成一个日期批次目录：

```text
raw/
  05-ai-builders/
    YYYY-MM-DD/
      digest-zh.md
      feed-x.json
      feed-podcasts.json
      feed-blogs.json
      manifest.json
```

规则：

- `digest-zh.md` 是当前批次的唯一主入口
- `feed-x.json`、`feed-podcasts.json`、`feed-blogs.json` 是证据文件
- `manifest.json` 记录批次元数据
- 不写入 `wiki/`
- 不自动执行 `/ingest`

## 执行流水线

### 步骤 1：准备数据载荷

运行：

```bash
cd ${CLAUDE_SKILL_DIR}/scripts && node prepare-digest.js > /tmp/ai-builders-payload.json
```

该 JSON 载荷包含：

- `config`
- `podcasts`
- `x`
- `blogs`
- `prompts`
- `stats`
- `generatedAt`

如果脚本失败或没有输出有效 JSON，应告知用户当前无法获取最新内容，并停止。

### 步骤 2：检查是否有新内容

若以下条件同时成立：

- `stats.podcastEpisodes` 为 0
- `stats.xBuilders` 为 0
- `stats.blogPosts` 为 0

则告诉用户当前没有可生成的新批次，并停止。

### 步骤 3：重混为中文原始摘要

基于 `prepare-digest.js` 生成的 JSON 内容，生成一份中文 Markdown 文件，作为本批次原始摘要：`digest-zh.md`。

要求：

- 只使用 JSON 中已有内容，不访问网页，不补抓数据
- 不编造信息
- 保留原始链接
- 只输出当前批次证据能够支持的结论

建议结构：

```markdown
# AI Builders — YYYY-MM-DD

## 核心摘要

[2-4 段中文总结]

## X / Twitter

- [人物名]：摘要
- 链接：...

## Podcasts

- [播客名 / 标题]：摘要
- 链接：...

## Blogs

- [博客名 / 标题]：摘要
- 链接：...
```

### 步骤 4：写入 raw 批次目录

将上一步生成的 `digest-zh.md` 和 `prepare-digest.js` 载荷中的结构化内容一起写入当前工作区：

```bash
cd ${CLAUDE_SKILL_DIR}/scripts && node save-batch.js --root "${PWD}" --payload /tmp/ai-builders-payload.json --language zh
```

将 Markdown 内容通过 stdin 传给 `save-batch.js`。

### 步骤 5：向用户报告结果

成功后，明确报告：

- 已生成的批次目录
- 主入口文件路径
- 下一步建议命令

输出格式：

```markdown
已生成 AI Builders 批次：
`raw/05-ai-builders/YYYY-MM-DD/`

主入口：
`raw/05-ai-builders/YYYY-MM-DD/digest-zh.md`

下一步可执行：
- `/ingest raw/05-ai-builders/YYYY-MM-DD/digest-zh.md`
- `/query <问题>`
- `/lint`
```

## 硬约束

- 不直接写入 `wiki/`
- 不自动执行 `/ingest`
- 不将 `feed-*.json` 当成独立来源页处理
- 不保留旧命名对外暴露给用户

## 关联连接

- [[ingest]] — 负责将 `raw/` 中的批次编译进 `wiki/`
- [[query]] — 负责查询已进入 wiki 的知识
- [[lint]] — 负责检查 wiki 健康度
