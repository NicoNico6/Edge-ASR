# edgestack

硬件受约束的 AI 研发工作方式，写成一组 Agent Skills。适用于端侧模型压缩与蒸馏、移植到 NPU 或新运行时、计算图与 kernel 优化、异构计算、多级存储与 offload、自研推理引擎、hardware-aware 设计、端侧研究实验、论文与交付。

参考 [pstack](https://github.com/backnotprop/pstack) 的结构（入口 mode、原则叶子、playbook、工作流 skill）改造而成。pstack 讲怎样写少而好的代码；edgestack 讲怎样在硬件约束下把模型能力搬过去，并让每个数字经得起质询。

## 核心思维

五问：约束是什么、哪条是硬墙？物理上限在哪？差距在栈的哪一层？哪个杠杆每单位花费买到最多？怎么知道它真的成立？

回路：预算卡 → 尺子（评测台、噪声底、上下界）→ 物理上限 → 杠杆（模型侧 ⇄ 系统侧）→ 分层对齐 → 板上实测 → 三轴判决（质量、成本、稳定性）→ 总账 → 交付。

三句话：数字是主张，板子是法官，总账是记忆。

完整内容见 [`skills/edge-mode/SKILL.md`](skills/edge-mode/SKILL.md)。

## 解决的典型问题

- **为硬件定制模型**：一块芯片上要跑唤醒、识别、LLM、合成、说话人分离。`System on device` 先分系统预算和时延链，`Custom model` 按差距选路线（量化、剪枝加修复、蒸馏、预训练、后训练、DMD、强化学习、OPD），每个阶段有进入、退出、中止的门，参考 `skills/edge-mode/references/training-stages.md`。
- **按硬件设计结构**：`Architecture design` 和 `references/architecture-patterns.md` 把 GQA、MLA、局部注意力、线性注意力与 delta rule（Gated DeltaNet、KDA）、混合比例、MoE、草稿头按「省了什么字节、付出什么、端侧注意什么」整理，以 KDA 为样本说明结构要和它的 kernel 一起设计。
- **agent 陷入无意义的多轮实验**：`converge` 要求每轮先写预测和决策表（所有结果导向同一决定就不跑），跑完先提炼现象和机制再开下一轮，维护 `STATE.md` 认知状态；连续两轮没有新现象就停止换配置、转向或上报。
- **对论文缺乏判断**：`paper-judgment` 按机制、条件、证据强度、基线公平性判断，给出采用、先复现锚点、忽略三种判决和预计收益。

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
| Playbook | 30 | `skills/edge-mode/playbooks/` |
| 原则 | 39 | `skills/principle-*/` |
| 工作流 skill | 17 | `skills/<名字>/` |
| Agent | 2 | `agents/`（edge-agent、caliber-cop） |
| 模板 | 8 | `templates/`（预算卡、硬件画像卡、总账、对照、底稿、回归、runs.tsv、decisions.tsv） |
| 脚本 | 6 | `scripts/` |

**工作流 skill：** converge（实验收敛协议）、paper-judgment（论文判断）、budget、roofline、profile、opcensus、parity、verify-inputs、ledger、side-by-side、stability、benchmark-checklist、interrogate、unslop、technical-writing、show-me-your-work、figure-it-out，外加 setup-edgestack。

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
