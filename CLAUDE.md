# 语言设定与核心角色 (Global Rules)
- **语言指令**：无论输入何种语言，你必须始终使用**简体中文**进行思考、回复和知识库的编写。
- **角色定义**：你正在维护一个 **LLM Wiki**（根据 [Karpathy 的规范](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f))，你的任务是将碎片化的信息编译成结构化、高度相互链接的 Obsidian 知识库。

# 核心目录与权限边界 (Immutability & Architecture)
你必须严格遵守以下文件操作权限，这是不可逾越的底线：

- `/raw/` (不可变层 - Immutable)：
  - **绝对只读**。这里存放我的原始素材、网页剪藏和自媒体文案。
  - **禁止修改或删除此目录下的任何文件**。它是事实的唯一真相来源。
- `/assets/` (媒体资产层)：
  - 存放图片、PDF和媒体。引用时使用 Obsidian 标准语法 `![[文件名称.png]]`。
  - 默认只存放会被 `wiki/` 页面长期引用的媒体，不作为杂项下载目录。
  - 当图片、截图或 PDF 满足以下任一条件时，应优先放入 `/assets/` 并在对应 wiki 页面中引用：
    - 该媒体承载核心结构信息、流程图、架构图或关键证据。
    - 该媒体比正文更适合解释某个概念或来源页。
    - 该媒体后续大概率会被多个页面复用。
  - 默认优先将媒体引用放在来源页（`wiki/sources/`）中；仅当某张媒体服务于长期稳定的概念或实体时，才升级到 `wiki/concepts/` 或 `wiki/entities/` 页面中复用。
  - 不要为纯装饰性图片、头像、banner、无信息增量配图自动创建 `/assets/` 引用。
  - 除非用户明确要求，否则不要修改 `raw/` 原文来插入媒体；媒体引用应放在 `wiki/` 编译输出层。
- `/wiki/` (编译输出层 - You Own This)：
  - 这是你的专属工作区。你需要在此处创建、更新、提炼知识并解决矛盾。

# Wiki 核心文件契约 (The Wiki Schema)
当你在 `/wiki/` 中工作时（尤其是执行写入操作后），必须维护以下基石：

1. **`wiki/index.md` (总目录)**：
   每次向 wiki 新增知识页后，必须同步更新此文件，将其按分类加入目录中。
   格式要求： [[页面名称]] — 一句话描述。
    - Entities/Concepts: 使用 TitleCase 命名。
    - Sources/Syntheses: 使用 kebab-case 命名。
    范例：
    ```markdown
    # Wiki Index

    ## Sources
    - [[摘要-source-slug]] — 该资料的核心主旨摘要。

    ## Entities
    - [[EntityName]] — 该实体的身份定义或核心功能。

    ## Concepts
    - [[ConceptName]] — 该概念或框架的核心定义。

    ## Syntheses
    - [[synthesis-slug]] — 该页面回答的复杂问题。
    ```
2. **`wiki/log.md` (操作日志)**：
    只能追加写入（Append-only）。每次操作后记录：`## [YYYY-MM-DD] <动作> | <操作简述>`。
    操作类型： ingest, query, lint, sync
    范例：
    ```markdown
    ## [2026-04-11] ingest | 引入项目 Claude Code 核心概念
    - **变更**: 新增 [[ClaudeCode]], [[摘要-claude-code-docs]]; 更新 [[index.md]]
    - **冲突**: 无 (或: 冲突 [[RAG架构]], 已标注)

    ## [2026-04-11] query | 解析 Karpathy LLM-Wiki 理念
    - **输出**: 已保存至 [[分析-karpathy-wiki-philosophy]]

    ## [2026-04-11] lint | 周度健康检查
    - **结果**: 修复 2 处死链，发现 1 个孤儿页面 [[UnlinkedPage]]
    ```
3. **内容分类**：
   - `/wiki/concepts/`：存放概念、框架、方法论（如 `Agent_Skill.md`）。
   - `/wiki/entities/`：存放人物、公司、工具、产品（如 `Claude_Code.md`）。
   - `/wiki/sources/`：存放从 `raw/` 提炼出的原始素材摘要。
4. **强制双向链接**：
   每一个 wiki 页面必须包含 `## 关联连接` 区域，使用 Obsidian 双链 `[[页面名称]]` 链接到其他相关概念。绝不能产生孤岛页面。
5. **矛盾处理原则**：
   如果新摄入的知识与旧知识冲突，不要静默覆盖。在页面中新建 `## 知识冲突` 区块，将两种说法都保留并做对比。

# 工作流指令说明 (Workflows / Skills)
当被要求执行以下操作时，请遵循核心逻辑（未来可能由专用 Agent Skills 接管）：

- `/ai`：围绕 AI builders 生成专题资料批次，持续搜集研究者、创始人、工程师、PM 和技术负责人等一线构建者在 X / Twitter、播客、博客等平台上的高信号公开内容，并将结果整理到 `raw/05-ai-builders/YYYY-MM-DD/`。其中 `digest-zh.md` 是该批次唯一主入口，`feed-x.json`、`feed-podcasts.json`、`feed-blogs.json` 是辅助证据层。`/ai` 只负责原始资料的抓取、筛选与组织，不直接更新 `wiki/`；如需进入知识网络，必须再执行 `/ingest raw/05-ai-builders/YYYY-MM-DD/digest-zh.md`。
- **`/ingest` 触发兼容规则**：如果上层前端、插件或转发层没有把裸 `/ingest` 原样传入，而是将其展开为以 `# ingest 技能` 开头的一整段 ingest 规则文本，只要该消息的意图明显是在触发 ingest，就必须将其视为一次真实的 `/ingest` 执行请求，而不是仅把它当作规则说明重复确认。
- **已处理状态判定**：执行 ingest 前，必须扫描 `wiki/sources/` 中所有来源页 frontmatter 的 `sources` 字段，建立 `raw 路径 -> 来源页` 映射。`/ingest` 依此跳过已处理文件，`/ingest <路径>` 若命中映射则进入更新模式。
- **`/ingest status`**：这是一个只读状态观察命令，输出 `未处理`、`已处理`、`批次入口`、`可更新` 四组结果，不修改任何文件。
- **来源页模板升级**：来源页应逐步收敛到 `## 核心摘要`、`## 关键论点`、`## 证据来源`、`## 可沉淀概念`、`## 关联连接` 五个固定区块。
- **冲突报告格式**：命中规则型知识冲突时，必须结构化报告页面、旧说法、新说法、冲突类型、建议动作 A/B/C。
- **ingest 后 lint**：每次 ingest 成功后，自动执行一次全局 `/lint` 同等级别的健康检查，检查 index 注册、关联连接、死链、孤儿页和显式知识冲突，但只报告不自动修复，也不单独追加 `lint` 日志。
- `/ingest <路径>`：读取指定的 `raw/` 文件，将其核心价值提炼并整合到 `wiki/` 目录的相关概念/实体中。必须更新 index 和 log。
- `/query <问题>`：通过读取 `wiki/index.md` 寻找相关文件，进行深度阅读后综合回答，并在回答中必须使用指向真实 wiki 页面的 `[[页面名称]]` 标注引用来源。仅在规则文档中，`[[wikilink]]`、`[[页面名称]]`、`[[PageName]]` 可作为 Obsidian 双链语法示例保留，不要求对应真实页面。
- `/lint`：全局扫描 `wiki/` 目录，找出孤岛页面（没有双链）、死链（链接不存在的页面）以及存在逻辑冲突的地方，并向我报告。

# 页面 Frontmatter (YAML) 规范
所有生成的 wiki 页面必须包含以下 YAML 头部：
---
title: "页面标题"
type: concept | entity | source | synthesis
tags: [知识标签]
sources:[关联的raw文件相对路径]
last_updated: YYYY-MM-DD
---

## 标签命名规则
- `tags` 中的标签不得包含空格。
- 英文标签统一使用 kebab-case，例如 `ai-builder`、`llm-wiki`、`claude-code`、`y-combinator`。
- 中文标签保持简短自然中文，但不要包含空格。
- 如果需要显示自然语言短语，应放在正文中，或使用双链显示别名语法 `[[PageName|Display Name]]`，不要把自然语言短语直接写进 `tags`。
