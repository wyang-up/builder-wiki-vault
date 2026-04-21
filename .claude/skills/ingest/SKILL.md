---
name: ingest
description: Use when the user wants to ingest files from raw/ into the wiki, compile new source notes, update linked entity or concept pages, or import articles, papers, transcripts, or other raw materials into the knowledge base.
user-invocable: true
---

# ingest 技能

## 核心工作流：Compile Into Wiki

你正在维护一个 **LLM Wiki**（Obsidian 知识库）。`raw/` 目录是不可变的原始资料层，`wiki/` 是持续累积和维护的编译输出层。

**目录结构约定：**
- `raw/01-articles/` — 网页剪藏的 Markdown 文章
- `raw/02-papers/` — 论文和 PDF 文献
- `raw/03-transcripts/` — 视频转录文案
- `raw/09-archive/` — 由人工维护的归档目录，不作为 ingest 工作流的一部分，也不作为输入源读取
- `wiki/sources/` — 资料摘要
- `wiki/entities/` — 实体（人物、公司、工具、产品）
- `wiki/concepts/` — 概念（框架、方法论、理论）

### ai-builders 批次约定

- `raw/05-ai-builders/YYYY-MM-DD/digest-zh.md` 是该批次的主 ingest 入口
- `feed-x.json`、`feed-podcasts.json`、`feed-blogs.json` 是同批次证据文件
- ingest `digest-zh.md` 时，可补充读取同目录 JSON 作为来源证据
- 第一阶段不直接 ingest JSON 文件本身，不为每条推文或每期播客自动建独立页面

## 触发逻辑

1. **用户执行 `/ingest`**：扫描 `raw/` 所有子目录（排除 `09-archive/`），找出尚未处理的文件。
2. **用户执行 `/ingest <path>`**：仅处理指定文件；如果该文件已处理，则进入更新模式。
3. **隐式触发**：用户说"把这个资料摄入知识库"、"导入这篇文章"时，自动执行 ingest。
4. **兼容触发**：如果外层系统把用户原本输入的 `/ingest` 展开成以 `# ingest 技能` 开头的一整段规则文本，而该消息没有附带新的任务约束，应将其视为一次真实的 `/ingest` 触发，直接开始扫描，而不是只重复确认规则。
5. **状态观察触发**：用户执行 `/ingest status` 时，不写入任何文件，只基于当前 `wiki/sources/` 的处理状态输出 `未处理`、`已处理`、`批次入口`、`可更新` 四组结果。

**扫描候选规则：**
- 对 `raw/05-ai-builders/YYYY-MM-DD/`，第一阶段只将 `digest-zh.md` 作为 ingest 候选文件
- `feed-x.json`、`feed-podcasts.json`、`feed-blogs.json` 仅作为同批次证据文件读取，不在 `/ingest` 扫描时作为独立候选文件

**显式路径规则：**
- 若用户显式执行 `/ingest raw/05-ai-builders/YYYY-MM-DD/feed-x.json`、`/ingest raw/05-ai-builders/YYYY-MM-DD/feed-podcasts.json` 或 `/ingest raw/05-ai-builders/YYYY-MM-DD/feed-blogs.json`，不要将该 JSON 作为独立来源页处理
- 应提示用户改为 ingest 同批次的 `digest-zh.md`，并将这 3 个 JSON 作为该批次的辅助证据文件读取
- 若运行环境可访问本地脚本，显式 `/ingest <path>` 前优先执行 `python3 .claude/skills/ingest/scripts/ingest_status.py --target <raw-path>` 判断分支：`ingest`、`update`、`batch_redirect` 或 `not_found`
- 若脚本返回 `update`，直接进入更新模式；若返回 `batch_redirect`，提示并改走同批次 `digest-zh.md`；若返回 `not_found`，报告路径不存在；若返回 `ingest`，按首次 ingest 处理

## 处理状态判定

- ingest 前必须扫描 `wiki/sources/` 中所有来源页，读取 frontmatter `sources` 字段，建立 `raw-path -> source-page` 映射
- 当 `wiki/sources/` 中已存在某个来源页，且其 frontmatter `sources` 字段包含当前 `raw/` 文件路径时，该文件默认视为“已处理”
- 执行 `/ingest` 扫描时，默认跳过已处理文件，只处理未处理文件
- 执行 `/ingest <path>` 且目标文件已处理时，不重复创建来源页，而是进入更新模式，更新既有来源页及相关实体/概念页
- 执行 `/ingest status` 时，复用同一套 `raw-path -> source-page` 映射输出状态，不再维护额外状态文件
- 处理状态由 `wiki/sources/`、`wiki/index.md` 与 `wiki/log.md` 共同表达，不通过移动 `raw/` 文件表达

## `/ingest status`

- 这是一个只读状态观察命令，不修改任何文件
- 输出必须分为 `未处理`、`已处理`、`批次入口`、`可更新` 四组
- `未处理`：`raw/` 中存在、但未在任何来源页 `sources` 中出现的文件
- `已处理`：已经映射到某个来源页的文件
- `批次入口`：命中 `raw/05-ai-builders/YYYY-MM-DD/digest-zh.md` 的入口文件
- `可更新`：用户显式指定时会进入更新模式的已处理文件
- 若运行环境可访问本地脚本，优先执行 `python3 .claude/skills/ingest/scripts/ingest_status.py` 获取用户可读报告；若需要结构化数据则执行 `python3 .claude/skills/ingest/scripts/ingest_status.py --json`

## 编译流水线

对每个待处理源文件，严格按以下步骤执行：

### 步骤 1：读取源文件

- **如果是 `.md` 文件**：使用读取工具完整读取内容。
- **如果是 `.pdf` 文件**：使用读取工具尝试提取文本。如果无法提取或内容为空，改为记录文件元信息（文件名、页数）在 sources 页面中。

### 步骤 2：提炼核心并翻译

从源文件中提取：
- **核心主旨**：这段资料讲什么（1-2句话）
- **实体**：人物、公司、工具、产品等具体名词
- **概念**：框架、方法论、理论等抽象名词

**作者提取规则：**
- 优先使用源文件 frontmatter 中非空的 `author`
- 若 `author` 为空，则读取 frontmatter 中的 `source` URL 作为兜底依据
- 若 `source` 匹配 `github.com/<owner>/<repo>/...` 或 `gist.github.com/<owner>/...`，则将 `<owner>` 视为候选作者
- 若 `source` 无法推断，则尝试从 `title` 中的 `owner/repo:` 结构提取 `owner`
- 若以上都无法确定，则保留为未知作者，不编造作者信息

**说明：**
- GitHub 仓库 README、blob 页面和类似页面常缺少标准文章作者元数据，因此允许基于 URL 或标题结构做兜底推断
- 作者兜底仅在原始 `author` 为空时触发，不能覆盖已有作者字段

如果是非中文内容，则翻译成中文。

### 步骤 3：创建来源摘要

在 `wiki/sources/` 创建 Markdown 文件：

```markdown
---
title: "摘要-文件slug"
type: source
tags: [来源, 原始文件]
sources: [raw/01-articles/xxx.md]
last_updated: YYYY-MM-DD
---

## 核心摘要
[3-5句话的核心总结]

## 关键论点
- [关键判断或结论]

## 证据来源
- [结构化来源证据]

## 可沉淀概念
- [[ConceptName]] — 值得升级为稳定概念或实体的节点

## 关联连接
- [[EntityName]] — 关联实体
- [[ConceptName]] — 关联概念
```

文件名使用 kebab-case：`摘要-{文件slug}.md`

**slug 规则：**
- 默认使用源文件名去掉扩展名后的结果生成 slug
- 连续空格和分隔符统一转换为 `-`
- 去除不安全字符，避免路径和文件名冲突
- 同一源文件重复 ingest 时，必须复用原有 slug，禁止生成语义重复的新来源页面

### ai-builders 批次识别

- 当目标路径匹配 `raw/05-ai-builders/YYYY-MM-DD/digest-zh.md` 时，按 ai-builders 批次模式处理
- 该模式下仍由 `digest-zh.md` 决定核心摘要、实体与概念提炼
- 若同目录存在 `feed-x.json`、`feed-podcasts.json`、`feed-blogs.json`，则读取它们补充原始链接、来源名称、账号和发布时间等证据
- `## 证据来源` 区块必须结构化保留：来源类型统计、关键账号或作者、发布时间、原始链接、缺失项说明

### ai-builders 来源页命名

- 对 `raw/05-ai-builders/YYYY-MM-DD/digest-zh.md`，来源页固定命名为 `ai-builders-YYYY-MM-DD.md`
- 重复 ingest 同一日期批次时，必须更新既有来源页而不是创建新 slug
- 命中 ai-builders 批次模式时，优先使用 `ai-builders-YYYY-MM-DD.md`；仅在未命中该模式时，才回退到通用 `摘要-{slug}.md`

### 步骤 4：知识网络化（实体/概念页面）

对于步骤 2 提取的每个实体和概念：

**目标目录：**
- 实体 → `wiki/entities/`
- 概念 → `wiki/concepts/`

**处理逻辑：**
1. 页面不存在 → 按照 CLAUDE.md 的 Frontmatter 规范创建新页面
2. 页面已存在 → 读取现有内容，**增量合并**新信息
3. **发现冲突** → **立即暂停**，向用户报告冲突内容，询问处理方式后再继续

**增量合并规则：**
- `## 定义`：补充更清晰的定义或别名，不覆盖已有有效定义
- `## 关键信息`：追加来自新源文件的事实、要点、例子或限制条件
- `sources`：追加新的源文件路径，避免重复
- `## 关联连接`：补充新的双链，避免重复
- 若页面已存在且信息仅为补充、例子扩展或上下文细化，直接合并，不视为冲突

**冲突判定规则：**
- 仅当新旧知识在定义、结论、数值或因果归因上出现明确矛盾时，才视为“知识冲突”
- 信息补充、表述细化、范围扩展、案例增加，不视为冲突

**冲突报告格式：**
- 页面：`[[PageName]]`
- 旧说法：`...`
- 新说法：`...`
- 冲突类型：定义 / 数值 / 结论 / 因果
- 建议动作：A / B / C

**页面模板：**

```markdown
---
title: "页面名称"
type: entity | concept
tags: [标签]
sources: [关联的源文件]
last_updated: YYYY-MM-DD
---

## 定义
[对该实体/概念的定义]

## 关键信息
[从源文件中提取的详细信息]

## 关联连接
- [[摘要-source-slug]] — 来源
- [[RelatedEntity]] — 相关实体
```

### 步骤 5：更新全局注册表

**更新 `wiki/index.md`：**
按照 CLAUDE.md 规定的格式，将新增页面添加到对应分类下：
- Sources: `[[摘要-source-slug]] — 该资料的核心主旨`
- Entities: `[[EntityName]] — 该实体的身份定义`
- Concepts: `[[ConceptName]] — 该概念的核心定义`

如果条目已存在于 `wiki/index.md` 中，则只更新描述，不重复注册。

**更新 `wiki/log.md`：**
追加操作日志（Append-only）：
```markdown
## [YYYY-MM-DD] ingest | 操作简述
- **变更**: 新增 [[PageName]]; 更新 [[index.md]]
- **冲突**: 无 (或: 冲突 [[ConflictingPage]], 已暂停等待决策)
```

### 步骤 6：记录处理状态

在确认以下全部完成后，视为该源文件已被成功编译到 wiki：
- sources 页面已创建或更新
- 实体/概念页面已创建或更新
- index.md 已更新
- log.md 已更新

处理完成后，不移动、不修改、不删除 `raw/` 下的源文件。`raw/` 是不可变事实层，处理状态应由 wiki 层表达。

### 步骤 7：执行全局 lint

- 每次 ingest 成功后，自动执行一次全局 lint，而不是只检查本次变更页面
- 全局 lint 检查 `wiki/index.md` 注册、`## 关联连接`、死链、孤儿页与显式知识冲突
- 全局 lint 只报告，不自动修复
- ingest 后自动触发的全局 lint 不单独追加 `lint` 日志；只有用户显式执行 `/lint` 时才追加 `lint` 日志
- 若当前环境支持 skill 调用，ingest 在完成写入后应直接调用 `lint` skill 执行一次全局巡检，而不是再实现一份平行的 lint 脚本

## 幂等性与重复处理

- 同一源文件重复 ingest 时，应优先更新既有 `wiki/sources/` 页面，而不是重复创建新页面
- 已存在的实体页、概念页和 `index.md` 条目不得重复创建
- `/ingest` 扫描时应跳过已处理文件；`/ingest <path>` 对已处理文件执行更新模式
- 若 PDF 无法提取正文，来源摘要中至少记录文件名、源路径、页数、是否可提取文本以及降级原因

### ai-builders 建模限制

- 默认只生成一个批次来源页
- 仅当 digest 中存在具有长期复用价值的稳定实体或概念时，才更新 `wiki/entities/` 与 `wiki/concepts/`
- 单条推文、单期播客和一次性热点默认只保留在来源页中

## 冲突处理流程

当发现新旧知识冲突时：

1. **暂停**：停止当前 ingest 流程
2. **报告**：向用户说明冲突内容（哪个页面、冲突点是什么）
3. **询问**：请用户选择处理方式：
   - A) 保留新旧两者，标注为"知识冲突"
   - B) 用新知识覆盖旧知识
   - C) 放弃本次 ingest
4. **继续**：根据用户选择继续或终止

## 注意事项

- 绝对不修改、删除或移动 `raw/` 下的源文件
- 绝对不将 `raw/09-archive/` 作为 ingest 输入源读取或扫描
- 所有 wiki 页面必须包含 `## 关联连接` 区域，不能产生孤岛页面
- 使用简体中文编写所有内容
- 英文实体命名使用 TitleCase；中文实体保持自然中文名称
- 概念和来源使用 kebab-case
