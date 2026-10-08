# G515 — 大模型KV Cache原理详解

> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G515-kv-cache-basics.html

## 元信息

- 编号：G515
- 标题：大模型KV Cache原理详解
- BV：BV12fXyBKEor
- 时长：01:51
- 发布日期：2026-03-28
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：未标注（涉及 Transformer 自回归解码、GQA/MQA、FlashAttention 等概念）

## 一句话总结

KV Cache 把历史 token 的 $K$ 、 $V$ 向量存下来复用，使自回归解码每步只需算当前 token，总计算复杂度从 $O(n^2)$ 降到 $O(n)$ ，代价是显存随序列长度线性增长。

## 核心

1. **问题/背景**：自回归解码每生成一个新 token，若重算全部历史 token 的 $K$ 、 $V$ ，随序列变长总代价高达 $O(n^2)$ ，推理极慢。
2. **机制/方法**：核心洞察是每步的 query 只来自当前 token，而历史 token 的 $K$ 、 $V$ 不会随新 token 改变，完全相同、可直接复用。于是把每步算出的 $K$ 、 $V$ 存入缓存，下一步只算当前 token 的 $K$ 、 $V$ 并读取历史缓存做注意力。
3. **关键证据或数字**：无缓存时第 $N$ 步要重算 $N$ 个 token 的 $K$ 、 $V$ ，总复杂度 $O(n^2)$ ；有缓存时每步计算量为常数，总复杂度降为 $O(n)$ ；代价是缓存占用显存，且随序列长度增长。
4. **结论/判断**：KV Cache 只在自回归解码阶段生效；缓存大小正比于层数、注意力头数与序列长度；prefill 阶段无法复用历史缓存。GQA、MQA 通过共享 KV 头压缩缓存，FlashAttention 与 KV Cache 是两种正交的优化，可叠加。

## 可迁移

- 面试答 KV Cache 按「为什么能缓存（历史 K/V 不变）→ 省了什么（重复计算）→ 代价是什么（显存）→ 怎么压（GQA/MQA）」四步讲，是完整的推理优化叙事。
- 做 RL rollout 的推理侧优化时，KV Cache 的显存账（层数 × 头数 × 序列长度）直接决定可并行的采样条数与批量大小。

## 疑问 / 下一步

- 长上下文下 KV Cache 显存爆炸的进一步解法（如量化、驱逐策略）可结合本系列其他期继续补。
