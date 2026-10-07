---
name: show-me-your-work
description: "为长时间或无人值守的工作留决策轨迹：一个 TSV，每个决定一行（做了什么、为什么、证据、结果）。用于 /show-me-your-work、自主长跑、分阶段工作。"
disable-model-invocation: true
---

# Show me your work

改编自 pstack 的 show-me-your-work（MIT，Lauren Tan）。

## 格式

一个 TSV，每个决定一行，单元格单行。列：`ts  phase  decision  why  evidence  result`。

- `evidence` 是指针：commit、文件:行、总账 run_id、产物路径，不写段落。
- `result`：通过、回退、已证伪、不确定、进行中。

用 `scripts/log.sh <logfile> <phase> <decision> <why> <evidence> <result>` 追加，它会补时间戳、写表头、清理换行。

实验结果本身记在 runs.tsv（**ledger** skill），这里记决定：选了哪个分叉、为什么回退、为什么转向。

## 位置

默认在工作目录的 `decisions.tsv`，不提交。需要审阅者凭轨迹信任结果时再提交。

## 规则

- 只追加。错误的决定用新行更正，不删改。
- 新的一段会话或新 agent 接手时，第一行 phase 写 `start`，说明接续的范围。
- 结束前对照 transcript 检查轨迹：每行对应真实的动作，证据能打开，漏掉的分叉补上。
- 结束前派一个不同模型族的子 agent 读轨迹和 transcript，指出证据薄弱、跳过验证、事后看有风险的决定。回复末尾写「注意」一节，第一行写评审模型。
