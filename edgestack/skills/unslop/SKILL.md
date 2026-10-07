---
name: unslop
description: "去掉中文和英文文字里的 AI 腔。任何要给人看的文字都适用。"
disable-model-invocation: true
---

# Unslop

改编自 pstack 的 unslop（MIT，Lauren Tan），加了中文规则。

## 中文

- 不用空泛动词和套话：赋能、助力、打造、抓手、全方位、深度融合、无缝、一站式、深入探讨、不难发现、值得注意的是、需要指出的是、总而言之、综上所述。
- 不用「不仅……而且……」「不是……而是……」来制造对比感，直接说结论。
- 不用三连排比凑数，有几个说几个。
- 不加结尾小结段，不加「希望对你有帮助」「如有需要请告诉我」。
- 不堆形容词和程度副词（非常、极其、显著地），用数字代替。
- 一句一个意思，长短交替，不全是短句也不全是长句。
- 不滥用加粗、引号、表情符号。不用破折号串联句子，拆成两句。
- 术语保留英文原样，不硬译（healing、roofline、RTF）。

## 英文

- AI vocabulary: delve, crucial, pivotal, showcase, landscape, tapestry, testament, underscore, vibrant, seamless, robust (as filler).
- "serves as / stands as / boasts" → "is / has". No "not just X, but Y". No forced groups of three.
- No superficial -ing tails ("highlighting...", "ensuring..."). No vague attributions ("experts say").
- No long dashes. No closing summary.

## 内容

- 每个主张带证据或标签。
- 模糊的说法（「效果有所提升」「性能较好」）换成数字和口径。
- 不编造引用、链接、数据。
