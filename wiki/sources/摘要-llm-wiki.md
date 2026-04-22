---
title: "摘要-llm-wiki"
type: source
tags: [来源, 原始文件, llm-wiki]
sources:
  - raw/01-articles/llm-wiki.md
last_updated: 2026-04-22
---

## 核心摘要
这篇文章是 Karpathy 对 `LLM Wiki` 模式的抽象说明。它提出的核心不是把原始资料直接丢给 RAG 系统按需检索，而是在原始资料与提问之间维护一层由 LLM 持续编译、更新和交叉链接的持久 wiki，让知识以结构化形式逐步累积。

![[Karpathy LLM Wiki.png]]

![[WikiLLM.jpg]]

文章把这种模式概括成三层结构：不可变的原始资料层、由 LLM 维护的 wiki 层，以及规定目录结构和工作流的 schema 层。这样一来，LLM 不再每次从零检索和拼接知识，而是持续把新资料沉淀到一个会增长、会修正、会互链的知识图谱中。

对实践者而言，这个模式最重要的价值在于把“知识维护”从高摩擦的人力工作，转成低边际成本的持续编译过程。人负责找资料、提问题和判断价值，LLM 负责摘要、归档、互链、更新和维护一致性。

## 关键论点
- `LLM Wiki` 的关键区别在于：知识不是在查询时临时从原文中重新拼出来，而是先被编译进一个持久的、可累积的 wiki。
- 该模式把知识系统拆成三层：`raw sources` 作为不可变事实层，`wiki` 作为结构化中间层，`schema` 作为约束 LLM 行为的工作流规范。
- 相比传统 RAG，这种方法更强调知识的长期积累、冲突标注、页面互链和持续更新，因此更适合需要长期维护的研究型、项目型或个人知识库。
- 文章明确指出 Obsidian 适合作为这类 wiki 的浏览和编辑界面，而 LLM 承担的是“知识维护程序员”的角色。
- 文中还特别提到图片本地化下载、附件目录、graph view、Marp、Dataview 等配套工具，说明这个模式天然适合在带附件和图谱视图的本地知识库中落地。

## 证据来源
- 作者：karpathy（依据 `source` URL `gist.github.com/karpathy/...` 推断）
- 来源类型：GitHub Gist 文章
- 原始链接：https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- 发布时间：原文未提供，raw 文件创建时间为 2026-04-22
- 图示引用：![[Karpathy LLM Wiki.png]]、![[WikiLLM.jpg]]
- 关键证据：文中明确对比了 RAG 与 LLM Wiki；提出 `raw sources`、`wiki`、`schema` 三层架构；强调 index/log、ingest/query/lint 等操作；并建议使用本地附件目录来保存图片等媒体资源。

## 可沉淀概念
- [[AgenticWorkflows]] — 文中 ingest、query、lint 体现出的多步知识维护工作流
- [[ClaudeCode]] — 文中列举的可承载该模式的 LLM agent 环境之一

## 关联连接
- [[AgenticWorkflows]] — 文中多次出现的 ingest / query / lint 工作流逻辑
- [[ClaudeCode]] — 文中提到的可用宿主之一
