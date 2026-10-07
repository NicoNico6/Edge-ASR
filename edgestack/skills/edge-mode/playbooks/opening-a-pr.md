### Opening a PR（收尾提交）

**每个产出代码的 playbook 结尾调用。**

1. 在独立的分支或工作树上工作。提交勤一点，开 PR 前整理成小而有序的提交，每个提交能单独成立。
2. 只暂存自己改的文件，不用 `git add -A`。
3. 提交信息和 PR 标题用 Conventional Commits：`type(scope): subject`，祈使句，不加句号。
4. PR 正文用这些小节，没内容的省略：`## Why`、`## What changed`、`## Scope`（覆盖什么、故意不做什么）、`## Verification`（真实运行路径和结果，性能改动写一个主数字和口径，`前 → 后`）。详细数据放链接的总账或产物里。
5. 用 **technical-writing** 和 **unslop** 过一遍正文。
6. 推送到共享分支、合并、强推，按「自治与决策权」处理。

**回复：** PR 链接、主数字、未完成项。
