---
title: "GStack"
type: entity
tags: [工具, 浏览器, skill, ai-builder]
sources:
  - raw/05-ai-builders/2026-04-21/digest-zh.md
  - "raw/01-articles/garrytangstack Use Garry Tan's exact Claude Code setup 23 opinionated tools that serve as CEO, Designer, Eng Manager, Release Manager, Doc Engineer, and QA.md"
last_updated: 2026-04-21
---

## 定义
GStack 是一层面向 AI builder 的工具与技能能力封装，用来补齐 agent 在浏览器操作、技能调用和工作流扩展上的能力缺口。

## 关键信息
- 在本批材料中，Garry Tan 将 GStack 描述为既适合在 OpenClaw/Hermes 中使用，也适合在 Claude Code 中使用的工具层。
- 它代表的不是单一模型能力，而是把浏览器交互和可调用技能纳入 agent 执行链路的一种工程化方式。
- 这类工具出现的背景，是 builder 关注点已经转向多步执行、外部系统交互和工作流可靠性。
- 在 `gstack` 的系统性说明文章中，GStack 被进一步定义成一套完整的软件生产工作流，而不只是浏览器或技能补丁。它通过 23 个 specialist skills 和多种 power tools，把 Claude Code 组织成近似“虚拟工程团队”的执行环境。
- 这意味着 GStack 的定位已经从“能力补层”扩展到“流程操作系统”，目标是把产品思考、架构评审、代码审查、QA、发布和复盘串成一条连续链路。

## 关联连接
- [[ai-builders-2026-04-21]] — 来源批次总结
- [[OpenClaw]] — 被明确提到的协同使用环境
- [[AgenticWorkflows]] — GStack 主要服务的工作流场景
- [[ClaudeCode]] — GStack 最典型的原生宿主环境
- [[VirtualEngineeringTeam]] — GStack 在本文中被赋予的核心工作流 framing
- [[摘要-garrytan-gstack-claude-code-setup]] — 对 GStack 的系统性来源说明
