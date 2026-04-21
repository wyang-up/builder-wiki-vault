---
title: "OpenClaw"
type: entity
tags: [工具, agent, ai-builder]
sources: [raw/05-ai-builders/2026-04-21/digest-zh.md]
last_updated: 2026-04-21
---

## 定义
OpenClaw 是一个面向 agent 工作流的执行工具，常被用于把模型接入定时任务、子代理协作和更长链路的软件执行场景。

## 关键信息
- 在本批资料里，OpenClaw 被放在真实 builder 工作流中讨论，而不是作为单纯的聊天模型界面。
- Peter Yang 的实际体验显示，OpenClaw 配合 GPT 在简单的每周统计邮件任务上仍会出现执行混乱，暴露出 agentic task 稳定性问题。
- Garry Tan 把 OpenClaw 视为当前可以拿来替代部分 cron 和 subagent 需求的工具，但同时承认更好的插件 API 仍是后续关键。

## 关联连接
- [[ai-builders-2026-04-21]] — 来源批次总结
- [[GStack]] — 常与 OpenClaw 组合使用的能力补层
- [[AgenticWorkflows]] — OpenClaw 所处的主要应用语境
- [[LongRunningAgents]] — OpenClaw 相关问题最终指向的长期目标
