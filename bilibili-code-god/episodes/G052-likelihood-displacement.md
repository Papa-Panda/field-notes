# G052 — Likelihood Displacement：为什么 DPO 越训 chosen 的概率越低？安全 DPO 拒答率反降 55%
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G052-likelihood-displacement.html

## 元信息

- 编号：G052
- 标题：Likelihood Displacement：为什么 DPO 越训 chosen 的概率越低？安全 DPO 拒答率反降 55%
- BV：BV1ivea6MEGr
- 时长：03:34
- 发布日期：2026-09-29
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：Likelihood Displacement（ICLR 2025，字幕述）；修法涉及 DPOP

## 一句话总结

DPO 只优化 chosen 与 rejected 的相对差（margin），chosen 的绝对概率可以一路下降；当两者语义太像时，被挤出的概率甚至会流向反义 token，能把安全对齐训成反效果。

## 核心

1. **问题/背景**：跑 DPO 时常见曲线：chosen 与 rejected 的 reward 一起往下掉、margin 在涨、loss 看着健康，但 chosen 的绝对概率持续走低。
2. **机制/方法**：DPO 损失只看 chosen 与 rejected 相对参考模型的对数概率之差，margin 变大既可以靠抬 chosen，也可以靠压 rejected，哪怕 chosen 自己也在降。被挤出的概率质量必然流向别的 token：流向近义表达是良性的，流向反义表达就是灾难。机制在于梯度方向是 chosen 与 rejected 的输出向量之差，两者越相似，差向量越短、方向越接近随机，且可能与某个反义 token 对齐。论文用隐藏表示相似度（CHES 分数）量化：chosen/rejected 越像，位移越严重，编辑距离预测不了、只有隐藏层相似度能预测。
3. **关键证据或数字**：单 token 最小实验里，chosen 为 NO、rejected 为近义的 never，训后 NO 概率 0.85 → 0.01，反义的 yes 反而上涨。安全对齐真实翻车：Sorry-Bench 偏好数据中七成以上样本两边都是拒答、只是措辞不同（高度相似），DPO 后 Gemma-2 2B 拒答率 80.5% → 54.8%，Llama-3 8B 74.4% → 33.4%（相对降幅 55%）——越训越不安全。
4. **结论/判断**：修法顺序是先筛数据、再加正则：按 CHES 只保留相似度最低的 5% 样本，拒答率可恢复到约 80%（与金标准数据持平）；给 chosen 加 SFT/NLL 正则（Llama-3.1 的做法）能拉回到七成左右；DPOP 则在损失里加惩罚项，chosen 概率低于参考模型即受罚。

## 关键数字

| 项 | 基线 → 结果 |
|---|---|
| 单 token 实验 NO 概率 | 0.85 → 0.01 |
| Gemma-2 2B 拒答率（安全 DPO 后） | 80.5% → 54.8% |
| Llama-3 8B 拒答率（安全 DPO 后） | 74.4% → 33.4% |
| CHES 筛至最低 5% 后拒答率 | 恢复至 ≈80% |

## 可迁移

- 监控 DPO 不能只看 loss 与 margin，必须单独盯 chosen 的绝对 log-prob；双降加 margin 涨就是位移在发生。
- 构造偏好数据时先算 chosen/rejected 的表示相似度：高度相似的对子优先剔除，这比事后调 ， $\beta$ ， 更治本。

## 疑问 / 下一步

- CHES 阈值（保留最低 5%）在非安全类偏好数据上是否同样适用，视频未给对照。
