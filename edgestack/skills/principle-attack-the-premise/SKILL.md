---
name: principle-attack-the-premise
description: "适用：两次或更多修复基于同一个前提都失败时。"
disable-model-invocation: true
---

# 攻击前提

基于同一前提的两次修复都失败，说明前提可能错了。停下第三次修复，先核查前提本身。

**为什么：** 连续失败的修复常共享一个没被质疑的假设：「瓶颈在算子」「误差来自量化」「这个通道没开火说明它坏了」。继续修只会在错误的方向上越走越远。

**做法：**
- 写下这几次修复共同依赖的假设。
- 设计一个直接检验这个假设的实验（通常比再修一次便宜）。
- 假设被推翻时，回到 **principle-attribute-to-the-layer** 重新归因。

改编自 pstack 的同名原则（MIT，Lauren Tan）。
