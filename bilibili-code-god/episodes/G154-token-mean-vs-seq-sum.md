# G154 — token level mean vs sequence level sum：一个除法决定训练稳定还是崩溃

> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G154-token-mean-vs-seq-sum.html

## 元信息

- 编号：G154
- 标题：token level mean vs sequence level sum：一个除法决定训练稳定还是崩溃
- BV：BV1qNbE6XEfw
- 时长：02:37
- 发布日期：2026-09-11
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：DPO、DAPO、GSPO（视频字幕转写为「DEO / double / JSPO」，按上下文应为此三者）

## 一句话总结

loss 聚合方式决定序列间的权重分配：token-level mean 让每条序列等权、放大短序列每个 token 的权重，模型会慢慢学会「少说话」；sequence-level sum 让每个 token 等权、长序列贡献更大，在 DPO 与数学推理 RL 中被发现稳定得多。

## 核心

1. **问题/背景**：DPO 训练一跑就崩、loss 跌向负无穷，问题可能不在数据也不在学习率，而在 loss 的聚合方式。两种算式只差一个除法：token-level mean 把一条序列内所有 token 的 loss 相加再除以该序列 token 数；sequence-level sum 只加不除。
2. **机制/方法**：mean 的问题在长度差异大的 batch 里暴露：它把每条序列的贡献归一化到相同权重，于是短序列每个 token 的权重被放大、长序列被缩小，模型偏向优化短序列、忽略长序列。sum 不除以长度，长序列天然贡献更大，符合「长序列包含更多信息」的直觉，在 DPO 里被发现比 mean 稳定得多，不容易出现 loss 崩溃与策略漂移；视频称 DPO 论文明确指出过 token-level mean 导致的长序列信号稀释问题。
3. **关键证据或数字**：数学推理 RL 是典型受害场景：推理链越训越长时，mean 让长链每个 token 的贡献被稀释，模型不愿产生长推理链，推理能力受限；改用 sum 或更精细的 token-level weighting 可解。GSPO 则更进一步，直接在 sequence level 做 importance sampling ratio，避免 token 数量差异带来的梯度偏移，代价是序列级统计量方差更大、需要更多采样来稳定（视频称其被用在 Qwen 团队的新论文中）。
4. **结论/判断**：实操建议：DPO 优先用 sum loss，不稳定再试 mean；RL 训练关注 token-level weighting 并对长序列适当加权，同时监控不同长度序列的 reward 分布（短序列 reward 偏高可能是 mean 偏差的信号）。还要特别注意框架默认值差异：verl 与 OpenRLHF 的默认 loss reduction 方式不同，一个 mean 一个 sum，搞混了就会崩。

## 可迁移

- 读 RL 框架源码时，loss reduction 是必查项：同一算法在不同框架默认 mean/sum 不同，迁移配置时最容易在这里翻车。
- 「模型输出越来越短」这类行为漂移，先怀疑聚合方式对长度的隐性激励，再怀疑奖励设计。

## 疑问 / 下一步

- DAPO 的 token-level loss 与 GSPO 的 sequence-level ratio 在长链推理上的实际差距，值得结合两篇原论文再对读一遍。
