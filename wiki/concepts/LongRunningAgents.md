---
title: "LongRunningAgents"
type: concept
tags: [概念, agent, 持续学习, 泛化]
sources: [raw/05-ai-builders/2026-04-21/digest-zh.md]
last_updated: 2026-04-21
---

## 定义
LongRunningAgents 指能够在较长时间范围内持续执行任务、维持状态、跨环境行动并在陌生情境中保持稳定行为的 agent 系统能力。

## 关键信息
- 本批播客把持续学习、alignment 下的泛化，以及 harness 演进视为 long-running agents 成立的关键前提。
- 这说明 agent 的未来能力不只是更会写代码，而是更能在长时程、多步骤、低监督条件下稳定完成任务。
- 当前 builder 在 OpenClaw 等工具上遇到的执行不稳定问题，可以视为通往 long-running agents 之前暴露出的早期工程约束。
- 该概念也与安全问题相关，因为 agent 运行时间越长、接触系统越多，默认安全边界就越重要。

## 关联连接
- [[ai-builders-2026-04-21]] — 来源批次总结
- [[AgenticWorkflows]] — long-running agents 的现实前置形态
- [[OpenClaw]] — 当前实践中暴露约束的工具例子
