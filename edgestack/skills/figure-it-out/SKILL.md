---
name: figure-it-out
description: "没有现成 playbook 匹配、或工作大而跨多个领域时，设计一个可审计的专用 playbook。用于 /figure-it-out。"
disable-model-invocation: true
---

# Figure it out

改编自 pstack 的 figure-it-out（MIT，Lauren Tan）。

1. **定框架。** 写出完成的谓词（可证伪）、范围（大致的单元数和工作量）、严格程度（不可逆和影响大的步骤要求更多门）。读 edge-mode 的五问，答不上的先补。
2. **设计流程。** 拆成能单独落地的单元，风险最大的未知数排最前。尺子和对拍工具在功能之前建（**Baseline harness**）。只在边界清楚的地方并行。把流程写下来给负责人看。
3. **跑循环。** 每个单元是一个实验：假设、最小改动、在真实产物上对照谓词测量、前进就保留、否则回退。判决只有三种：验证通过、未通过、不确定。不确定不算通过。
4. **留轨迹。** 用 **show-me-your-work** 和 **ledger** 记录，这类工作通常值得提交轨迹。
5. **验收。** 在真实产物上对照谓词检查整体。重复出现的纠正写成检查脚本（**principle-encode-lessons-in-structure**）。

**回复：** 设计的流程、严格程度和理由、轨迹路径、已验证的部分、未完成的部分。
