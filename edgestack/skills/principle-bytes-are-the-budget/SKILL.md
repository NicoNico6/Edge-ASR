---
name: principle-bytes-are-the-budget
description: "适用：batch 小、内存受限、存在分层存储（片上、缓存、DRAM、主机内存、SSD）或 offload 时。"
disable-model-invocation: true
---

# 字节就是预算

batch 为 1 的推理多数时候受数据搬运限制。按层级记录每步搬运的字节，先减少搬运、提高复用和局部性，再谈算得更快。

**为什么：** 权重、KV cache、激活每一步都要从某一级存储读进来。搬运的时间和能量通常超过计算。降低位宽、提高缓存命中率、让数据留在近处，往往比换更快的算子收益大。

**做法：**
- 每级存储记三个数：容量、带宽、每步实际搬运字节。
- 评估缓存、预取、offload 策略时，看命中率和搬运字节，不看直觉。
- 搬运和计算能重叠就重叠（下一层的数据在本层计算时搬），并测重叠是否真的发生。
- 压缩方案先算它省下的字节，再测它带来的解压或反量化开销。

**边界：** 区别于 **principle-ceiling-from-physics**（算上限的方法）和 **principle-price-every-crossing**（跨单元、跨精度的固定开销）。
