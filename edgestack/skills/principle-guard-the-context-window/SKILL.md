---
name: principle-guard-the-context-window
description: "适用：面对大输出、长日志、长 transcript、批量文件、扇出规划时。"
disable-model-invocation: true
---

# 看住上下文

原始材料留在子 agent 里，主线只留摘要和路径。

**为什么：** 上下文满了，早先的约束和决定会被挤掉或压缩丢失。日志、dump、transcript 一次就能塞满上下文。

**做法：**
- 大文件按区间读，或交给子 agent 读完返回结构化摘要。
- 子 agent 返回文件路径和关键数字，不返回原文。
- 长任务的中间状态写到文件里（总账、决策轨迹），不靠上下文记住。

改编自 pstack 的同名原则（MIT，Lauren Tan）。
