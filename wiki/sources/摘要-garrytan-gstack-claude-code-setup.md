---
title: 摘要-garrytan-gstack-claude-code-setup
type: source
tags:
- 来源
- 原始文件
- gstack
- ClaudeCode
sources:
  - raw/01-articles/garrytangstack Use Garry Tan's exact Claude Code setup 23 opinionated tools that serve as CEO, Designer, Eng Manager, Release Manager, Doc Engineer, and QA.md
last_updated: 2026-04-21
---

## 核心摘要
这篇文章是 Garry Tan 对 `gstack` 的系统性说明，核心主张是：借助一组分工明确的技能与工具，单个 builder 可以把 Claude Code 组织成一个近似“虚拟工程团队”的工作体系，而不再只是把模型当作补全器或聊天助手。

文章一方面展示了这套体系的角色分工，例如 CEO、设计师、工程经理、QA、安全和发布负责人等；另一方面也强调它背后的方法论是按真实 sprint 顺序组织 AI 工作流，把产品思考、计划、实现、审查、测试、发布和复盘串成一条连续链路。

从 builder 视角看，这篇文章最重要的价值不只是列出一批命令，而是把 `gstack` 定义为一种面向高并行、高反馈速度和多代理协作的软件生产方式。它试图回答的问题是：当 AI 已经能够大量生成代码后，怎样让执行质量、流程纪律和跨角色协同也一起工程化。

## 关键论点
- `gstack` 被描述成 Garry Tan 自己的 Claude Code 工作流封装，其目标不是单点提效，而是把 AI 编程过程组织成一支具备明确角色分工的“虚拟工程团队”。
- 文章强调真正的变化不在于 AI 写了多少原始代码，而在于一个人能否用合适的工具链持续完成产品设计、架构评审、代码审查、QA、发布和复盘。
- `gstack` 的技能设计遵循 sprint 流程：先思考和规划，再实现、审查、测试、发布，最后沉淀文档与复盘，这意味着它本质上是一套工作流系统，而不是一组零散命令。
- 文中将 `Claude Code` 视为主要宿主，把 `OpenClaw`、浏览器自动化、多代理协作和安全审查等能力接入进去，目标是支持更高并行度的软件生产。
- Garry Tan 特别强调 builder 应该把 AI 工具用于真实交付，衡量标准是 shipped features、可验证测试和生产工作流，而不是表面上的代码行数或单次对话效果。

## 证据来源
- 作者：Garry Tan（依据 `source` URL `github.com/garrytan/gstack/...` 推断）
- 来源类型：GitHub 仓库说明文档
- 原始链接：https://github.com/garrytan/gstack/tree/main
- 发布时间：原文未提供，raw 文件创建时间为 2026-04-21
- 关键证据：文中将 `gstack` 定义为 Garry Tan 的 Claude Code 配置与技能体系；明确列出 23 个 specialist skills 与 8 个 power tools；反复强调它服务于完整 sprint、真实浏览器 QA、多代理协作和发布流程。

## 可沉淀概念
- [[GStack]] — 作为整套工作流和技能系统的核心工具实体
- [[ClaudeCode]] — 作为 gstack 主要宿主环境的工具实体
- [[GarryTan]] — 文章作者，也是这套工作流的提出者和实践者
- [[VirtualEngineeringTeam]] — 把多种角色能力封装进单个 AI 工作流的组织方式
- [[AgenticWorkflows]] — 文中技能链路和多步执行的基础工作流范式

## 关联连接
- [[GStack]] — 文章的核心工具对象
- [[ClaudeCode]] — 文章默认的执行宿主
- [[GarryTan]] — 作者与实践者
- [[VirtualEngineeringTeam]] — 文章最鲜明的工作流 framing
- [[AgenticWorkflows]] — 这套方法背后的执行逻辑
