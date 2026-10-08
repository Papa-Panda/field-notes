# G378 — self-attention 自注意力：一个公式讲透 Transformer 的心脏
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G378-self-attention-formula.html

## 元信息
- 编号：G378
- 标题：self-attention 自注意力：一个公式讲透 Transformer 的心脏
- BV：BV1d7gD6FEUe
- 时长：03:24
- 发布日期：2026-07-22
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：Attention Is All You Need（Vaswani et al., 2017）

## 一句话总结
自注意力就是让每个 token 用 Q 去匹配所有 token 的 K 得到权重，再按权重加权汇总 V；一个公式拆开只有打分、缩放、softmax、加权求和四步。

## 核心
1. 问题/背景：目标是让序列中每个 token 看过其他所有 token 后，再决定关注谁、关注多少。实现靠三组线性投影：query 表示「我想找什么」，key 表示「我能提供什么标签」，value 表示「我真正的内容」。
2. 机制/方法：第一步用 $Q$ 与 $K$ 的转置做点积得到两两相关性分数矩阵；第二步除以 $\sqrt{d}$ 缩放（ $d$ 为向量维度），因为维度高时点积数值过大、直接进 softmax 会使梯度极小、训练不动；第三步如有掩码先把屏蔽位置填负无穷，再逐行 softmax 归一化成权重；第四步用权重乘 $V$ 加权求和，最后过一个输出线性层整合。整体公式为：

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^{T}}{\sqrt{d}}\right) V$$

3. 关键证据或数字：输入输出形状完全一致（batch × 序列长度 × 维度）；手撕代码顺序固定——三个线性层生成 QKV、打分、缩放、masked fill、softmax（可加 dropout）、乘 V、输出层，共七步。
4. 结论/判断：这道题是手撕头号高频题，答题关键是把公式背后的每一步动机讲出来，尤其是缩放稳梯度、掩码填负无穷这两处「为什么」。

## 可迁移
- 写实现时最容易漏的两处：缩放因子 $\sqrt{d}$ 的位置（在 softmax 之前）和掩码要在 softmax 之前填负无穷而非之后置零。
- 理解这四步是读 FlashAttention、GQA 等后续优化的前提——它们改的都是这条流水线的存取与分组方式，数学骨架不变。

## 疑问 / 下一步
- 多头版本只是把维度切成多份并行跑同一公式再拼接，手撕时可顺手补上 reshape 与多头的维度账。
