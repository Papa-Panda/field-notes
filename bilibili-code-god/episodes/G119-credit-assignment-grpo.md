# G119 — credit assignment 与 GRPO 的 advantage 分配机制
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G119-credit-assignment-grpo.html

## 元信息

- 编号：G119
- 标题：credit assignment 与 GRPO 的 advantage 分配机制
- BV：BV1PTb76YEVw
- 时长：01:42
- 发布日期：2026-09-17
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：REINFORCE、GRPO、DAPO（字幕 ASR 作「DEO」，应为 DAPO 的 token-level loss 处理）

## 一句话总结

奖励只给整条序列一个分数、训练却要落到每个 token——这就是 credit assignment；从 REINFORCE 的全员共享一个 advantage，到 GRPO 的组内 z-score 归一化广播，再到 DAPO 式 token 级加权/剔除，趋势是优势算得越细，模型越知道是哪一步做对了。

## 核心

1. **问题/背景**：RL 的 reward 通常是序列级的单个分数，但梯度更新发生在 token 级，必须把序列奖励分配到每个 token 头上，这就是 credit assignment 问题；分得太粗，每个 token 被一视同仁，好步坏步同奖同罚。
2. **机制/方法**：三档粒度——REINFORCE 最粗：每条序列的 reward 减 baseline 得到一个 advantage，该序列所有 token 共享；GRPO：对同一 prompt 采样一组回答，各自 reward 在组内做 z-score 归一化，归一化值即该回答的 advantage，再广播给它的每个 token，省掉 critic；更细的 token 级方案（如 DAPO）在算 loss 时对不同 token 加权，并提出去掉特殊 token 的 loss 以免其梯度干扰。
3. **关键证据或数字**：未给具体实验数字，选择建议按场景分档：入门或资源紧张用 REINFORCE + 序列级 baseline 先跑通；通用场景首选 GRPO（组内归一化、省 critic、效果不错）；长序列且追求高质量时上 token 级方案，把每个 token 的贡献分开算。
4. **结论/判断**：advantage 的分配粒度决定信用分配的精度；工程上要监控 token 级 loss 分布，确认特殊 token 没有污染梯度。

## 可迁移

- 面试答 credit assignment 可按「序列奖励 → token 梯度」的错位开题，再按 REINFORCE → GRPO 组内归一化 → token 级加权三档展开；自己实现 GRPO 时记得 advantage 是序列级广播、细粒度文章只能做在 loss 加权与特殊 token 剔除上。

## 疑问 / 下一步

- token 级加权的具体形式（如按 token 概率或熵加权）与组内归一化的交互，视频只点到为止，可与 G005（CrEST 轮级信用分配）、G017（GiGPO）对照着看。
