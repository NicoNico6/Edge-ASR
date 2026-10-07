# edgestack

硬件受约束的 AI 研发工作方式，写成一组 Agent Skills。适用于端侧模型压缩与蒸馏、移植到 NPU 或新运行时、计算图与 kernel 优化、异构计算、多级存储与 offload、自研推理引擎、hardware-aware 设计、端侧研究实验、论文与交付。

参考 [pstack](https://github.com/backnotprop/pstack) 的结构（入口 mode、原则叶子、playbook、工作流 skill）改造而成。pstack 讲怎样写少而好的代码；edgestack 讲怎样在硬件约束下把模型能力搬过去，并让每个数字经得起质询。

## 核心思维

五问：约束是什么、哪条是硬墙？物理上限在哪？差距在栈的哪一层？哪个杠杆每单位花费买到最多？怎么知道它真的成立？

回路：预算卡 → 尺子（评测台、噪声底、上下界）→ 物理上限 → 杠杆（模型侧 ⇄ 系统侧）→ 分层对齐 → 板上实测 → 三轴判决（质量、成本、稳定性）→ 总账 → 交付。

三句话：数字是主张，板子是法官，总账是记忆。

完整内容见 [`skills/edge-mode/SKILL.md`](skills/edge-mode/SKILL.md)。

## 安装

```bash
./install.sh            # 链接到 ~/.claude/skills 和 ~/.claude/agents
./install.sh --project  # 链接到当前目录的 .claude/skills 和 .claude/agents
```

或用 skills CLI：`npx skills add <这个仓库>`，选择需要的 skill。

然后运行 `/setup-edgestack` 配置各角色的模型和路径，之后在任务开头用 `/edge-mode <任务>`。

## 内容

| 类别 | 数量 | 位置 |
|---|---|---|
| 入口 | 1 | `skills/edge-mode/` |
| Playbook | 27 | `skills/edge-mode/playbooks/` |
| 原则 | 34 | `skills/principle-*/` |
| 工作流 skill | 15 | `skills/<名字>/` |
| Agent | 2 | `agents/`（edge-agent、caliber-cop） |
| 模板 | 8 | `templates/`（预算卡、硬件画像卡、总账、对照、底稿、回归、runs.tsv、decisions.tsv） |
| 脚本 | 6 | `scripts/` |

**工作流 skill：** budget、roofline、profile、opcensus、parity、verify-inputs、ledger、side-by-side、stability、benchmark-checklist、interrogate、unslop、technical-writing、show-me-your-work、figure-it-out，外加 setup-edgestack。

**可执行的部分**（必须不发生的事用脚本拦，不靠文字）：

| 脚本 | 作用 |
|---|---|
| `roofline.py` | 按带宽、算力、各组件位宽估算每步时间、实时率、所需带宽，和实测对比 |
| `parity_diff.py` | 两个 dump 目录逐张量比较，报第一个发散点 |
| `runs.py` | 追加总账行，缺 commit、设备、口径、样本数等字段时拒绝写入；检查口径混用 |
| `idle_gpus.sh` | 发现持续空闲的 GPU |
| `log.sh` | 追加决策轨迹 |
| `check-skills.py` | 检查本仓库 skill 的 frontmatter、链接、原则引用、标点 |

## 与 pstack 的关系

保留并改编（标注来源）：explain-the-number、prove-it-works、attack-the-premise、fix-root-causes、laziness-protocol、encode-lessons-in-structure、build-the-lever、guard-the-context-window、never-block-on-the-human、sequence-verifiable-units 十条原则；benchmark-checklist、interrogate、unslop、technical-writing、show-me-your-work、figure-it-out；hillclimb、prototype、autonomous-run、session-pickup、pause-safely、eval、authoring-a-skill、opening-a-pr 等 playbook 的骨架。

新增：约束、物理与系统、测量、研究、记录、资源六组中的 24 条原则；硬件刻画、建尺子、压缩、移植、计算图、kernel、存储层级、异构计算、引擎能力、联合扫描、质量回归、前沿扫描、数据管线、论文、交付、长作业等 playbook；口径、分层对齐、包络普查、总账、并排产物、稳定性等 skill。

去掉：以 PR 流水线为中心的 babysit、shipping、autopilot、orchestrate，以及纯代码风格类 skill。需要时可以同时安装 pstack。

## 许可

MIT。部分文件改编自 pstack（Copyright (c) 2026 Lauren Tan，MIT），见 `LICENSE`。
