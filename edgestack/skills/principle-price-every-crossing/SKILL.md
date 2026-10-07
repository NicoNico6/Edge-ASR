---
name: principle-price-every-crossing
description: "适用：做异构切分、精度切换、主机与设备交互、跨进程或线程边界时。"
disable-model-invocation: true
---

# 每次跨界都有价

每一次跨界都要付费：精度转换、内存拷贝、同步、kernel 下发、唤醒、缓存刷新。把这些单独计时入账，跨界次数本身就是设计变量。

**为什么：** 单个算子在 NPU 上很快，不代表整条路径快。频繁在 NPU 与 CPU、int8 与 fp16、主机与设备之间来回，固定开销会吞掉加速。小 kernel 很多时，主机侧下发开销可能比 GPU 执行还长。

**做法：**
- 剖析时把跨界开销单独列一行（转换、拷贝、同步、下发），不要摊进算子时间。
- 每个调用记固定开销和随数据量增长的部分，判断合并调用是否值得。
- 切分方案先数跨界次数，再比较各单元的算子速度。
- 用 CUDA Graph、批量下发、算子融合、整段留在一个单元上来减少跨界。

**边界：** 区别于 **principle-bytes-are-the-budget**（搬运量）和 **principle-envelope-before-port**（能不能跑）。
