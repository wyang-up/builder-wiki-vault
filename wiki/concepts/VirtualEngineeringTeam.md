---
title: "VirtualEngineeringTeam"
type: concept
tags: [概念, 工作流, agent, 软件生产]
sources:
  - "raw/01-articles/garrytangstack Use Garry Tan's exact Claude Code setup 23 opinionated tools that serve as CEO, Designer, Eng Manager, Release Manager, Doc Engineer, and QA.md"
last_updated: 2026-04-21
---

## 定义
VirtualEngineeringTeam 指把 CEO、设计、工程管理、代码审查、QA、安全和发布等不同软件角色的职责，封装成一组可调用的 AI 技能与工具链，再由单个 builder 统一编排的一种软件生产方式。

## 关键信息
- 在这篇文章中，VirtualEngineeringTeam 不是比喻性的营销说法，而是一种具体的工作流设计：每个角色对应一个 skill 或一类工具，按 sprint 顺序接力工作。
- 这种建模方式的目标，是把 AI 从“帮你写一段代码”提升到“帮你跑完整条产品与交付链路”，从而让单人 builder 获得接近多角色团队的执行面宽。
- 它依赖两个前提：一是宿主环境能够稳定调用技能、浏览器和外部工具；二是工作流本身具有足够强的流程纪律，避免 AI 在多步执行中失控。
- `gstack` 对这一路线的贡献，是把角色分工、审查节点和发布顺序显式写进技能系统，而不是把它们留在作者脑中或散落在 prompt 里。

## 关联连接
- [[GStack]] — 当前最典型的 VirtualEngineeringTeam 实现样例
- [[ClaudeCode]] — 文中这套虚拟团队的主要宿主环境
- [[AgenticWorkflows]] — VirtualEngineeringTeam 所依赖的多步执行基础
- [[GarryTan]] — 明确提出并公开实践这套 framing 的作者
- [[摘要-garrytan-gstack-claude-code-setup]] — 主要来源文章
