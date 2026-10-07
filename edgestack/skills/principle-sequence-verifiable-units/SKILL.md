---
name: principle-sequence-verifiable-units
description: "适用：任何多步工作：批量改动、迁移、扫描、一组实验、一串提交。"
disable-model-invocation: true
---

# 可验证单元

拆成小单元，每个单元以一次检查结束，验证一个再开始下一个。

**为什么：** 批量做完再统一验证，错误会叠加，无法知道是哪一步引入的。

**做法：**
- 每个单元定义它的检查：对拍通过、指标在噪声内、板上跑通。
- 检查失败就停下修，不继续堆。
- 提交顺序本身讲清楚故事：失败的复现在前，修复在后。

改编自 pstack 的同名原则（MIT，Lauren Tan）。
