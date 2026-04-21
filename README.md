# Builder Wiki Vault

一个把 AI builders 高信号信息流与其他原始资料一起编译进本地知识库的 Obsidian LLM Wiki。

这个项目融合了两个很有代表性的方向：

- [follow-builders](https://github.com/zarazhangrui/follow-builders) 的信息流捕获能力：把高信号来源组织成可持续消费的资料流
- [karpathy-llm-wiki-vault](https://github.com/jason-effi-lab/karpathy-llm-wiki-vault) 的知识编译能力：把原始资料沉淀为结构化、可链接、可复用的 wiki

在这两者之上，Builderwiki Vault 补上了更适合长期维护的本地工作流：资料采集、知识编译、增量更新、知识查询和全局巡检。

这个 vault 不只服务于单一资料类型。它为文章、论文、转录稿、会议纪要，以及按批次组织的专题资料预留了统一的编译入口，用同一套 wiki schema 把不同类型的信息沉淀到一个知识网络里。

## 什么是 AI builders

这个项目关注的不是“谁在谈 AI”，而是“谁在真正构建 AI”。

这里的 `AI builders` 指的是那些正在一线推动 AI 能力落地的人，比如研究者、创始人、工程师、产品经理和技术负责人。他们在参与模型、产品、工具链和工作流的真实构建，而不是只做转述、追热点或泛泛评论。

这个项目的基本判断是：与其持续追踪二手观点和流量内容，不如持续跟踪那些真正把 AI 做出来的人。因为他们更可能提供高信号输入，包括产品方向、工程实践、模型能力边界、组织协作方式以及值得长期沉淀的原始判断。

## 目录结构

```text
🏛️ Builderwiki Vault
├── 🖼️ assets/                   ← 媒体资源层：图片、PDF、附件等，供 Obsidian 引用
│
├── 📥 raw/                      ← 原始资料层：事实入口，只读，不在这里表达处理状态
│   ├── 📄 01-articles/          ← 网页剪藏、技术文章、产品博文、官方文档节选
│   ├── 🎓 02-papers/            ← 论文、研究报告、PDF 文献
│   ├── 🎙️ 03-transcripts/       ← 播客、视频、采访、演讲等转录稿
│   ├── 💡 04-meeting_notes/     ← 会议纪要、brainstorming、项目讨论记录
│   ├── 🤖 05-ai-builders/       ← AI builders 信息批次：研究者、创始人、工程师、PM 等一线构建者的高信号动态
│   │   └── YYYY-MM-DD/
│   │       ├── digest-zh.md     ← 该批次唯一 ingest 主入口
│   │       ├── feed-x.json      ← X / Twitter 证据层
│   │       ├── feed-podcasts.json ← 播客证据层
│   │       ├── feed-blogs.json  ← 博客证据层
│   │       └── manifest.json    ← 批次元信息
│   └── 🗃️ 09-archive/           ← 人工维护归档区：不参与 ingest 扫描
│
├── 🧠 wiki/                     ← 知识编译输出层：所有结构化知识沉淀在这里
│   ├── 📑 index.md              ← 总目录：记录所有 wiki 页面及一句话说明
│   ├── 📜 log.md                ← 追加式日志：记录 ingest / query / lint / sync
│   ├── 🏗️ concepts/             ← 概念页：框架、方法、模式、原理
│   ├── 👥 entities/             ← 实体页：人物、公司、工具、产品
│   ├── 🔍 sources/              ← 来源页：对 raw 文件或批次的结构化摘要
│   └── 💎 syntheses/            ← 综合页：围绕复杂问题的深度整理
│
├── 🤖 CLAUDE.md                 ← 项目最高优先级规则：语言、权限边界、wiki schema
│
├── ⚙️ .claude/                  ← Claude / agent 配置目录
│   └── 🛠️ skills/
│       ├── ai/                  ← 生成专题资料批次到 raw/05-ai-builders/
│       ├── ingest/              ← 把 raw 编译进 wiki，并处理 update / status
│       ├── query/               ← 基于 wiki 进行检索、阅读和回答
│       └── lint/                ← 对 wiki 做全局健康检查
│
└── 📘 README.md                 ← 项目统一说明文档
```

这个结构表达的是一条很清晰的知识流水线：

- `raw/` 负责接收和保存原始事实
- `wiki/` 负责把原始事实编译成可链接知识
- `.claude/skills/` 负责把 `/ai`、`/ingest`、`/query`、`/lint` 这些工作流落地

## 为什么这个项目值得看

很多知识工具只做到“收集”，很多信息产品只做到“摘要”。

这个项目想做的是更完整的一条链：

1. 收集高价值原始资料
2. 把资料整理进统一的原始资料层
3. 再把这些原始资料编译成来源页、实体页、概念页和综合页
4. 让这些内容最终变成一个可更新、可查询、可持续维护的本地知识库

所以它不是“又一个资料收集箱”，也不是“又一个 Obsidian 模板”，而是把两件事接起来：

- 前端是可持续进入 vault 的资料入口
- 后端是面向长期维护的知识编译器

## 核心功能

### 1. 多来源资料进入同一个知识系统

这个项目把不同来源的资料统一放进同一套结构里处理：

- 网页文章和博客可以进入 `raw/01-articles/`
- 论文和研究报告可以进入 `raw/02-papers/`
- 视频、播客、访谈转录可以进入 `raw/03-transcripts/`
- 会议纪要和讨论记录可以进入 `raw/04-meeting_notes/`
- 按日期组织的专题资料可以进入 `raw/05-ai-builders/`

不管资料从哪里来，最终都会走向同一个 `wiki/`。

### 2. 原始资料不会停留在收集层

`/ingest` 会把原始资料编译进 `wiki/`，而不是只是把 Markdown 堆在文件夹里：

- 生成来源页
- 抽取可复用的实体和概念
- 更新索引与日志
- 把页面连接进知识网络

这样资料就从“存档”变成“知识资产”。

### 3. 支持增量更新，而不是重复导入

这个项目不是一次性 ingest。当前工作流已经支持：

- 扫描 `wiki/sources/` frontmatter 的 `sources` 字段，判断原始资料是否已处理
- `/ingest` 默认跳过已处理文件
- `/ingest <path>` 命中已处理来源时进入 update 模式
- 对按批次组织的专题资料采用混合更新策略

当前专题批次来源页的 update 逻辑是：

- 重建：`核心摘要`、`关键论点`、`证据来源`
- 保守合并：`可沉淀概念`、`关联连接`

这让知识库更像一个持续演化的系统，而不是一堆导入后就失控的 Markdown。

### 4. 它保留了 LLM Wiki 的“知识网络”属性

项目延续了 Karpathy 风格 LLM Wiki 的核心理念：

- `raw/` 保存原始事实
- `wiki/` 保存编译后的知识
- 来源页、实体页、概念页之间用双链连起来
- 用 `wiki/index.md` 做总目录
- 用 `wiki/log.md` 做追加式操作日志

最终目标不是堆页面，而是构建一个可穿行的知识网络。

## 它融合了什么

### 来自 `follow-builders`

- “Follow builders, not influencers” 这条筛选哲学
- 围绕高信号来源的 source curation 思路
- X / Podcasts / Blogs 三类来源的批次化组织方式
- 把连续信息流整理成可消费批次的工作流意识

### 来自 `karpathy-llm-wiki-vault`

- `raw/` 与 `wiki/` 的分层结构
- 以 wiki 为中心的知识编译思路
- `sources / entities / concepts / syntheses` 的页面分工
- 双向链接、索引页、日志页这些知识库骨架

### 这个项目自己的补充

- 专题批次目录的入口约定
- `digest-zh.md` 作为唯一 ingest 主入口
- `feed-*.json` 只做证据层，不独立建来源页
- `/ingest status` 的状态观察语义
- 已处理文件的 update 模式
- ingest 后接全局 lint 的巡检规则
- 更贴合本地 Obsidian vault 的脚本与 skill 组合

## 工作流

这个项目当前最完整的一条自动化路径是专题批次资料流：

```text
专题信息流
  -> /ai 生成原始批次
  -> raw/05-ai-builders/YYYY-MM-DD/
  -> /ingest digest-zh.md
  -> wiki/sources/ai-builders-YYYY-MM-DD.md
  -> wiki/entities/ + wiki/concepts/
  -> /query 消费知识
  -> /lint 巡检知识网络
```

除此之外，文章、论文、转录稿和会议纪要也都可以直接进入 `raw/01-04/`，再通过 `/ingest` 进入同一个知识网络。

其中：

- `/ai` 负责“抓取并组织一批专题资料”
- `/ingest` 负责“把原始资料编译为知识”
- `/query` 负责“在知识库上提问和综合回答”
- `/lint` 负责“检查整个 wiki 的结构健康度”

## 快速开始

在 Obsidian 中打开这个 vault，然后用 Claude Code 或兼容的 agent 工作流操作。

最典型的使用顺序：

1. 运行 `/ai` 生成最新一批专题原始资料，或手动把资料放入 `raw/01-04/`
2. 运行 `/ingest raw/05-ai-builders/YYYY-MM-DD/digest-zh.md`
3. 运行 `/query <问题>` 在知识库上提问
4. 需要时运行 `/lint` 做全局巡检

如果你要收集网页文章、博客或在线文档，也可以先用 [Obsidian Web Clipper](https://obsidian.md/clipper) 把内容裁剪到本地，再放入 `raw/01-articles/` 交给 `/ingest`。

## 核心约束

- `raw/` 是不可变事实层，禁止修改、删除、移动其内容
- `wiki/` 是唯一知识编译输出层
- `raw/09-archive/` 不属于 ingest 输入范围
- `raw/05-ai-builders/YYYY-MM-DD/` 中只有 `digest-zh.md` 是 ingest 主入口
- `feed-x.json`、`feed-podcasts.json`、`feed-blogs.json` 只作为证据文件读取，不作为独立来源页

对 `01-04` 目录来说，它们仍然遵循同一原则：原始资料停留在 `raw/`，结构化知识沉淀到 `wiki/`。

## 当前实现重点

当前项目已经围绕专题批次资料建立了一套较完整的本地处理链路，重点包括：

- ingest 前基于 `wiki/sources/` 建立已处理映射
- 支持 `/ingest status` 的只读状态观察
- 支持专题来源页 update
- 支持来源页五段式结构：
  - `核心摘要`
  - `关键论点`
  - `证据来源`
  - `可沉淀概念`
  - `关联连接`
- ingest 后执行全局 lint 等级检查

## 关键文件

- `CLAUDE.md`：本项目最高优先级的本地规则
- `.claude/skills/ai/SKILL.md`：专题批次生成规则
- `.claude/skills/ingest/SKILL.md`：知识编译与 update 工作流
- `.claude/skills/lint/SKILL.md`：wiki 健康检查规则
- `.claude/skills/query/SKILL.md`：知识检索与回答规则

当前与专题批次 update 直接相关的脚本位于：

- `.claude/skills/ingest/scripts/ingest_status.py`
- `.claude/skills/ingest/scripts/update_source_page.py`
- `.claude/skills/ingest/scripts/apply_update_target.py`
- `.claude/skills/ingest/scripts/ai_builders_payload.py`

## 当前追踪的来源

这个项目当前会重点关注三类高信号来源，它们也是专题批次资料的主要输入：

### 网站与平台

- `X / Twitter`：跟踪一线构建者的短内容动态、产品判断、工程经验和工具发布
- `YouTube / Podcasts`：跟踪高质量 AI 播客与访谈节目，提取长内容中的观点、推演和方法论
- `官方博客与工程博客`：跟踪 AI 公司和团队发布的产品更新、工程实践与研究说明

当前对应的专题批次证据文件是：

- `feed-x.json`
- `feed-podcasts.json`
- `feed-blogs.json`

### AI builders

当前重点跟踪的 AI builders 包括：

- Andrej Karpathy
- Swyx
- Josh Woodward
- Kevin Weil
- Peter Yang
- Nan Yu
- Madhu Guru
- Amanda Askell
- Cat Wu
- Thariq
- Google Labs
- Amjad Masad
- Guillermo Rauch
- Alex Albert
- Aaron Levie
- Ryo Lu
- Garry Tan
- Matt Turck
- Zara Zhang
- Nikunj Kothari
- Peter Steinberger
- Dan Shipper
- Aditya Agarwal
- Sam Altman
- Claude

这些来源并不是为了追求“覆盖一切 AI 新闻”，而是为了持续追踪那些真正参与模型、产品、工具链和工作流构建的人与团队。

### 当前重点跟踪的播客与博客

播客包括：

- Latent Space
- Training Data
- No Priors
- Unsupervised Learning
- The MAD Podcast with Matt Turck
- AI & I by Every

博客包括：

- Anthropic Engineering
- Claude Blog

## 适合谁

这个项目尤其适合：

- 想把分散资料持续沉淀成长期知识库的人
- 想把信息流、网页剪藏、论文和转录稿统一管理的人
- 想把 Obsidian、agent workflow 和本地知识编译结合起来的人
- 想拥有一个“既能吸收新资料，又能积累旧知识”的 AI 研究工作台的人

## 一句话总结

如果说 `follow-builders` 更像高信号资料入口，`karpathy-llm-wiki-vault` 更像知识容器，那么 Builderwiki Vault 想做的是把两者接起来，形成一条从原始资料到长期知识资产的完整流水线。
