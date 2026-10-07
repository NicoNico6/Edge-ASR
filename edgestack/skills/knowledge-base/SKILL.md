---
name: knowledge-base
description: "建立和查询项目或领域的结构化知识库：硬件特性、技术、kernel 与模型案例、问题到解法的诊断页、外部 PR 与论文来源，带置信度与截止日期。用于 /knowledge-base，积累可复用的硬件与优化知识，或接入现成的领域知识库时。"
disable-model-invocation: true
---

# Knowledge base

思路来自 mit-han-lab/KernelWiki（MIT）：把散落在 PR、论文、博客、比赛方案、自己实验里的知识整理成带类型、交叉引用、可脚本查询的页面。

## 页面类型

| 类型 | 前缀 | 内容 |
|---|---|---|
| 来源 | `src-` | 一个 PR、论文、文档、博客、比赛方案，附链接与抓取日期 |
| 硬件 | `hw-` | 一个硬件特性或包络约束，附发现版本与复现 |
| 技术 | `tech-` | 一种优化技术：机制、适用条件、证据、来源 |
| 案例 | `case-` | 一个 kernel 或模型的优化案例，附实测数字与口径 |
| 诊断 | `pattern-` | 症状 → 原因 → 解法，链接技术与案例 |

每页 frontmatter 至少有 `id`、`type`、`tags`、`hardware`、`confidence`（实测、原文、转述）、`captured_at`、`sources`。

## 规则

- 每个结论链接到来源页或总账行。没有来源的写 `confidence: 推断`。
- 整个知识库写明截止日期，过期的页面标出。
- 提供查询脚本（按标签、硬件、症状过滤，全文检索），agent 用脚本查，不整库读进上下文（**principle-guard-the-context-window**）。
- 生成按问题、按技术、按硬件的索引页。
- 硬件怪癖文件（`HW_NOTES.md`）里稳定下来的条目，升级成 `hw-` 页。
- 被证伪的技术留着，标「在某条件下不成立」。

## 接入现成知识库

领域有现成的（例如 GPU kernel 方向的 KernelWiki），按它的说明安装成 skill，在任务契约里写明用到了哪个知识库及其截止日期。知识库给的是先例，不是结论，仍按 **paper-judgment** 和 **principle-validate-on-real-workload** 处理。
