---
name: setup-edgestack
description: "配置 edgestack：各角色用哪个模型、硬件画像卡目录、集群环境、总账路径。写入 ~/.agents/edgestack.md。用于 /setup-edgestack。"
---

# Setup edgestack

写 `~/.agents/edgestack.md`，所有 harness 共用。

## 步骤

1. 列出当前会话可以传给子 agent 的模型名。确认不了的不写。
2. 读已有的设置文件（如果有），作为当前值。
3. 用结构化提问工具（Claude Code 的 `AskUserQuestion`）确认每个角色的模型，以及下面的路径。
4. 整个文件覆盖写入，保证重跑结果一致。

## 文件格式

```
# edgestack 设置。删除一行就回到默认。
judgment and prose: opus
hardest changes: opus
code and sweeps: sonnet
log and transcript mining: haiku
reviewers: opus, sonnet
device cards: ~/edge/devices/
cluster env: ~/edge/cluster.env
ledger: ./runs.tsv
budget: ./docs/budget.md
hw notes: ./HW_NOTES.md
```

`cluster env` 文件里写登录方式、账户、分区、环境激活命令、缓存目录，供 **Long job** playbook 读取。不要把密钥写进这个文件。

## 确认

告诉用户写了哪个文件。edge-mode 在任务开始时读取它。
