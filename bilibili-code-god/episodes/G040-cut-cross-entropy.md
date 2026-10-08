# G040 — 大词表训练时 logits 为什么吃掉 89% 显存？Cut Cross-Entropy 与 Liger Kernel 讲透
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G040-cut-cross-entropy.html

## 元信息

- 编号：G040
- 标题：大词表训练时 logits 为什么吃掉 89% 显存？Cut Cross-Entropy 与 Liger Kernel 讲透
- BV：BV19Reh6vEk5
- 时长：04:12
- 发布日期：2026-09-30
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：Cut Cross-Entropy（Apple，arXiv:2411.09009）；Liger Kernel（LinkedIn，arXiv:2410.10989）

## 一句话总结

训练显存除了参数、梯度、优化器状态，还有第四件——logits：它随词表大小线性膨胀，在大词表模型上能占到总显存的 89%；解法是不物化完整 logits，靠分块在线计算（CCE）或融合内核（Liger）把这块从几十 GB 压到 MB 量级。

## 核心

1. **问题/背景**：logits 是最后一层对每个位置、每个词表词打出的分数，张量形状为 batch × 序列长度 × 词表大小。以 Gemma-2 2B（词表约 25.6 万）为例，8192 个 token 的 logits 在 FP32 下单次前向就是 8.4 GB，反向还要存 softmax 与梯度，峰值约 24 GB。词表越大这块越大：Phi-3.5-mini（词表 3.2 万）logits 占训练显存 40%，Llama-3 8B（词表 12.8 万）占 65%，Gemma-2 2B 占 89%；一条 8 万 token 的长序列，光 logits 就能吃满一张 80 GB 的 H100。

2. **机制/方法（为什么贵）**：交叉熵拆开是两项——正确 token 的 logit，减去全词表的 log-sum-exp。第一项只需要一个数，第二项却要把 25.6 万个 logit 全算出来做分母；反向时 softmax 减 one-hot 使每个词表位置都有梯度，一列都省不掉；再加上交叉熵通常会 upcast 到 FP32 计算，于是这块中间量成了整个训练里最大的单个张量。

3. **机制/方法（CCE）**：Apple 的 Cut Cross-Entropy 分两路处理。正确 token 的 logit 用索引矩阵乘只取那一列，不碰其他列；log-sum-exp 把词表切块，在 GPU 片上 SRAM 里逐块维护在线的运行最大值与累加和，算完即弃，永不把完整 logits 写回显存；反向时同样在片上重算——思路与 FlashAttention 一致，用重算换显存。还有一层免费加速：softmax 后绝大多数词的概率小到连 BF16 都表示不了（ $2^{-12}$ 以下直接截零），前沿模型上超过 99.98% 的梯度块全为零，可以整块跳过，反向快 3.4 倍；再按平均 logit 重排词表让空块聚拢，又快 15%。

4. **机制/方法（Liger Kernel）**：LinkedIn 的 Liger Kernel 走融合路线：把 LM head 的矩阵乘与交叉熵融进一个内核，按 chunk 算一小块 logits，在前向里直接算出这一块的梯度，存梯度而不存 logits 本身。

5. **结论/判断**：两条路线的代价也要认清——词表/隐层比很低的模型（如 Phi-3.5-mini）上 CCE 比 torch.compile 慢约一半；需要更高精度开 Kahan 求和时，显存涨到 2.3 GB、耗时翻倍。所以选型原则是：显存估算先把 logits 这第四项算进去，词表超 10 万或序列超 8K 默认开 Liger，追求极致再换 CCE，开完必须对比 loss 曲线确认数值一致。

## 关键数字

| 指标 | 基线 | 优化后 |
|---|---|---|
| Gemma-2 2B、8192 token，loss 计算显存（CCE） | 24 GB | 1 MB |
| 同上，loss + 梯度峰值（CCE） | 28 GB | 164 MB |
| 同上，loss 计算耗时（CCE vs 朴素基线 208 ms） | 208 ms | 145 ms（与 torch.compile 的 143 ms 持平） |
| Llama-3 8B、4×A100 吞吐（Liger） | — | +42.8% |
| Llama-3 8B 显存（Liger） | — | −54.8% |
| Qwen2 吞吐 / 显存（Liger） | — | +25.5% / −56.8% |

## 可迁移

- **显存估算公式要补第四项**：估算训练显存时在参数/梯度/优化器状态之外，加上 logits 项——batch × 序列长 × 词表 × 4 字节，再乘 3 估反向峰值。面试被问「训练显存怎么算」时漏掉这一项，在大词表模型上会差出近一个数量级。
- **工程默认动作**：词表 >10 万或序列 >8K 时，一行配置开 Liger（TRL 里 `use_liger=True`，或 `apply_liger_kernel_to_*`）；启用后先对 loss 曲线验数值、再看显存曲线确认最后一层的尖峰消失，这是低成本高收益的标准排障顺序。

## 疑问 / 下一步

- CCE 的梯度块跳过依赖 softmax 概率的极端稀疏性；在 RL 训练（如 GRPO 大量采样、温度较高）场景下分布更平坦时，99.98% 的零块比例还成立吗，值得查 CCE 后续工作或实测。
