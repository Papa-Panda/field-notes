# G243 — Linear Attention 讲透：核函数替代 softmax，O(n²) 降到 O(n)
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G243-linear-attention.html

## 元信息

- 编号：G243
- 标题：Linear Attention 讲透：核函数替代 softmax，O(n²) 降到 O(n)
- BV：BV1JE826rEVe
- 时长：04:57
- 发布日期：2026-08-27
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：Linear Transformer（Katharopoulos et al., 2020）；Performer / FAVOR+（Choromanska et al., ICLR 2021）；RFA（Random Feature Attention）

## 一句话总结

Linear Attention 不近似 softmax，而是把它换成可分解的核函数，让相似度写成两个特征映射的内积，再靠矩阵乘法结合律先算与序列长度无关的 $ d \times d $ 小矩阵，复杂度便从 $ O(n^2) $ 降到对 $ n $ 线性。

## 核心

1. 问题/背景：标准注意力要先算 $ Q K^\top $ 得到 $ n \times n $ 相似度矩阵再逐行 softmax，序列翻倍则计算与显存翻四倍——4K 尚可忍，64K 爆显存；Flash Attention 靠分块与重算省了显存和 IO，但理论复杂度仍是 $ O(n^2) $ 。
2. 机制/方法：关键洞察是注意力的本质只是相似度函数，softmax 只是其中一种选择，却强制先显式构造大矩阵、无法拆解。换成核函数后，相似度可写成 $ \phi(q) $ 与 $ \phi(k) $ 的内积，于是计算顺序可改写为：

$$
\mathrm{out} = \phi(Q) \big( \phi(K)^\top V \big)
$$

括号内先算出 $ d \times d $ 矩阵、与 $ n $ 无关，再左乘 $ \phi(Q) $ ，总复杂度 $ O(n d^2) $ ，对 $ n $ 线性——秘诀就是换了括号位置。
3. 关键证据或数字：核函数三档选择——ReLU 最简单但砍掉负值、表达力有限； $ \mathrm{elu}(x) + 1 $ 在负半轴平滑、保留负值信息，是 Linear Transformer 的默认；随机特征映射在期望意义上严格逼近 softmax 的指数核，是 Performer 的 FAVOR+ 方案。64K 序列实测：推理约快 10 倍、显存省约 50%、精度损失控制在 1% 以内，多个 benchmark 与标准注意力基本持平。
4. 结论/判断：Linear Transformer 还能改写成 RNN 形式做自回归推理；简单任务选 elu+1，要逼近标准注意力选随机特征。这条核函数路线与 Flash Attention 的工程路线互补：前者改复杂度，后者改常数。

## 关键数字

| 指标 | 标准注意力 | Linear Attention |
| --- | --- | --- |
| 时间复杂度 | $ O(n^2) $ | $ O(n d^2) $ |
| 64K 推理速度 | 基线 | 约 10 倍 |
| 64K 显存 | 基线 | 省约 50% |
| 精度损失 | — | < 1% |

## 可迁移

- 面试问长上下文优化时，把方案分三层讲：工程层（Flash Attention、KV Cache 压缩）、近似层（稀疏/滑窗）、改写层（线性注意力与状态空间模型），并能点出线性注意力的代价是表达力和精确检索能力。
- 理解「结合律换序降复杂度」这一招可迁移到一切先算大中间矩阵的算子优化分析里。

## 疑问 / 下一步

- 线性注意力把历史压进固定大小的状态，精确召回（needle 类任务）通常弱于全注意力；当前主流是混合架构（少数全注意力层 + 多数线性层），其配比与召回损失的实测关系值得跟进。
