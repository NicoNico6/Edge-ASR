---
name: roofline
description: "用物理上限估算 batch 小的推理：受带宽还是算力限制、放不放得下、离实测多远。用于 /roofline，动手优化前或怀疑一个性能数字时。"
disable-model-invocation: true
---

# Roofline

## 运行

```
python3 scripts/roofline.py --bw <GB/s> --tops <TOPS> --mem <GB> \
  --part enc:0.6e9:8 --part dec:3e9:4 --rate <每秒步数> [--eff 0.6] [--kv-mb 50] [--measured-ms 87.7]
```

`--part 名称:参数量:位宽` 每个权重组一个。`--eff` 是 batch 1 时实际达到的带宽比例，先用 0.6，能实测就用实测值。`--kv-mb` 是每步额外读取的 KV cache 或激活。

## 读结果

- `bound by`：受带宽还是算力限制。batch 1 解码通常是带宽。
- `estimate` 与 `RTF`：预计每步时间和实时率。
- `needs`：持续需要的带宽和设备余量。余量小于 1 时，只靠工程优化达不到，必须减少字节（降位宽、缩模型、少搬运）。
- `measured`：和实测对比。实测超过估算 1.5 倍，瓶颈不在权重搬运（下发开销、跨界、未融合的小算子、预处理），先用 **profile** skill 拆分，不要继续压模型。实测快于上限，先怀疑测量。

## 限制

这是一阶估算：不含缓存复用、计算与搬运重叠的细节、热降频。估算标「推断」，和实测并排写进总账。多单元并行、MoE 只激活部分专家、分层 offload 时，按实际每步读取的字节填 `--part`。
