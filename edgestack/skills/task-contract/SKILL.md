---
name: task-contract
description: "实现或优化任务开始前写任务契约和计划草稿：目标、正确性、目标指标、允许的做法、验证命令、评测命令、真实负载、晋升条件。用于 /task-contract，kernel、算子、引擎能力、移植、压缩等有候选迭代的任务。"
disable-model-invocation: true
---

# Task contract

思路来自 NVlabs/kda（Kernel Design Agents，代码 Apache 2.0、文档 CC BY 4.0）的任务契约与 `docs/draft.md` 规则，扩展了真实负载与预算字段。

## 步骤

1. 在任务工作区（不是方法论仓库）复制 `../../templates/task-contract.md`，填契约部分。
2. 读本地代码、测试、任务文档，找到基线和验证路径，再写草稿。
3. 写 `docs/draft.md`：基线、风险、按预期价值与风险排序的候选、第一步、命令原文、晋升与拒绝所需证据。
4. 把草稿转成可执行计划 `docs/plan.md`（每步一个可检查的结果）。
5. 草稿存在之前不改实现代码。

## 工作区分离

方法论（edgestack）保持通用。任务专属的提示、数据、验证器、阈值、生成的实现、基准日志、候选产物，都放在任务工作区，生成物进 `runs/`、`outputs/`、`profile/` 并在 git 中忽略。任务专属的规则写在任务仓库的 `.claude/skills/` 或 `CLAUDE.md`。

## 晋升规则

候选满足契约，并有证据表明它改进或保持了目标指标，才晋升。拒绝的候选记录原因，不静默丢弃（`scripts/candidates.py`）。验证必须包含真实负载与留出集（**principle-validate-on-real-workload**）。
