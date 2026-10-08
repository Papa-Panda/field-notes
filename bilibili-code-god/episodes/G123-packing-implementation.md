# G123 — 序列 Packing 实现详解：装箱算法、cu_seqlens 与 block diagonal mask
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G123-packing-implementation.html

## 元信息

- 编号：G123
- 标题：序列 Packing 实现详解：装箱算法、cu_seqlens 与 block diagonal mask
- BV：BV1KPb76vEWq
- 时长：02:10
- 发布日期：2026-09-16
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：FlashAttention varlen 接口（视频提及）

## 一句话总结

Packing 把多条短样本拼满一条定长序列以消除 padding 浪费，正确性全靠边界隔离——用 cu_seqlens/varlen attention（等价于 block diagonal mask）保证样本间不互相 attend、position 在边界重置。

## 核心

1. **问题/背景**：batch 内序列长短参差，传统 padding 补齐到最长；当多数样本很短时，近一半算力喂给了 padding（视频称可达约 80% 浪费的极端情形）。
2. **机制/方法**：实现四步——按长度排序，用装箱算法（常用 first-fit decreasing）把短样本拼成恰好填满 max length 的包，用边界数组记录每条样本的起止，再用 varlen attention 让注意力只在同一样本内计算。其本质是 block diagonal mask：拼在一起的样本绝不能互相看见，否则内容串扰（与本系列 G011 的串样本问题同源）。
3. **关键证据或数字**：视频称预训练数据上 packing 可带来约 2 倍训练速度提升、显存下降三成以上；是否值得做先量化 padding 浪费率，超过约 40% 就值得上。
4. **结论/判断**：优先用 FlashAttention 的变长接口传 cu_seqlens 天然隔离，不要手写 mask；开启后必须做等价性验证，确认结果与不 packing 时一致；TRL、LLaMA-Factory 等框架都有一键开关。

## 关键数字

| 指标 | 数值 |
|---|---|
| 值得启用 packing 的 padding 浪费率 | > 约 40% |
| 吞吐提升 | 约 2 倍 |
| 显存下降 | 三成以上 |

## 可迁移

- 这是 G011（串样本根因）的实现篇：面试或排障时能把「position ids 重置 + varlen 分块」落到 cu_seqlens 的具体传参，比只说概念更可信。
- 任何 packing 改造都要带等价性验证（同数据开/关 packing 对比 loss），这是防止 silent error 的标准动作。

## 疑问 / 下一步

Packing 与变长梯度累积归一化（G039 的 bug）叠加时，token 计数口径如何统一才不重复踩坑？
