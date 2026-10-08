# G158 — reward 归一化详解：running mean-std、batch 归一化与三个常见坑
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G158-reward-normalization.html

## 元信息

- 编号：G158
- 标题：reward 归一化详解：running mean-std、batch 归一化与三个常见坑
- BV：BV1CDb76AEk8
- 时长：02:14
- 发布日期：2026-09-10
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：GRPO（group 内 z-score 归一化）

## 一句话总结

reward 归一化解决的不是奖励对不对，而是尺度稳不稳：running mean-std 与 batch 内归一化二选一或叠加，顺序必须是先归一化再 clip，统计量要用 EMA 而非全量平均。

## 核心

1. **问题/背景**：reward 的尺度直接决定梯度大小，动辄数百上千会让梯度爆炸；不同任务、不同训练阶段的 reward 尺度可差几个数量级，不归一化则训练不稳定、超参难调，归一化做错则直接发散。
2. **机制/方法**：两种方式。Running mean-std：维护滑动的均值与标准差，每步把 reward 标准化，最常用、实现简单效果稳，但统计量必须用滑动平均，全量统计会引入未来信息。Batch 内归一化：在当前 batch 内算均值标准差做标准化；GRPO 天然是这种方式的变体——在同一 prompt 的 group 内做 z-score，这也是它不需要 critic 的原因之一。实现上可两层叠加：先用 running stats 归一化 reward，再算 advantage，最后对 advantage 再做一次 batch 归一化。
3. **关键证据或数字**：三个常见坑——（1）顺序错：必须先归一化再 clip，反过来会破坏尺度；（2）running stats 用简单平均而非指数移动平均（EMA）；（3）把 reward 归一化与 advantage 归一化混为一谈，两者是两件不同的事。
4. **结论/判断**：归一化的目标是让进入梯度的量始终处在可控尺度；选哪种方式取决于算法（PPO 系常用 running + EMA，GRPO 系用 group 内 z-score），但三个坑与算法无关，普遍适用。

## 可迁移

- 读 verl / OpenRLHF 等框架源码时，先定位 reward 与 advantage 各自的归一化位置与顺序，能快速判断实现是否踩坑。
- 面试高频题：「GRPO 为什么不需要 critic」可答一半在此——group 内 z-score 同时充当了基线与尺度校准。

## 疑问 / 下一步

- running std 在 reward 分布突变（如课程学习换难度）时如何避免旧统计量污染，视频未展开。
