---
name: principle-parity-ladder
description: "适用：引入新的精度、运行时、图变换或硬件时，或设备结果和参考对不上时。"
disable-model-invocation: true
---

# 分层对齐阶梯

按阶梯逐级对齐：浮点参考 → 低精度浮点 → 量化模拟 → 运行时量化 → 板上。每级和上一级比，不跨两级。对不上就逐层 dump，找第一个发散的层。

**为什么：** 跨好几级直接比，差异混在一起无法归因。量化模拟的损伤和运行时真实量化的损伤可能差好几倍，只看模拟会去解决不存在的问题。

**做法：**
- 用 **parity** skill 和 `scripts/parity_diff.py`，逐张量比较 max abs、cosine、相关系数，报第一个超阈值的层。
- 每级定阈值，并写明阈值依据。
- 对不上时先怀疑观测：dump 位置、数据布局、预处理、dtype 转换、探针本身。确认观测无误再怀疑系统。
- 量化方案先拿运行时实际的量化名单和标定方法，再在训练侧模拟，不要自己推断。

**边界：** 区别于 **principle-attribute-to-the-layer**（栈层面的归因）和 **principle-board-is-truth**（最终以板上为准）。
