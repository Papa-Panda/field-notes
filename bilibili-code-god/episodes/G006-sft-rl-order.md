# G006 — SFT 和 RL 该混着训还是先后训？两个基线 bug 让先 SFT 再 RL 反超 22.2 分

> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G006-sft-rl-order.html

## 元信息

- 编号：G006
- 标题：SFT 和 RL 该混着训还是先后训？两个基线 bug 让先 SFT 再 RL 反超 22.2 分
- BV：BV1EuHn6VE7k
- 时长：04:13
- 发布日期：2026-10-07
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：ETH Zürich 2026-04 复查论文（字幕所称）；涉事框架 DeepSpeed、OpenRLHF、LLaMA-Factory，verl 于 2025-11 修复聚合问题；对照混合方法 SRFT、HPT 等

## 一句话总结

一批「混合训练优于两阶段」的论文，对照组共用了两个 silent bug——梯度累积丢了 7/8 的梯度、loss 按 mini-batch 均值再平均——修好后最普通的先 SFT 再 RL 反超最高 22.2 分，算力还省近一半。

## 核心

1. **问题/背景**：两阶段（先 SFT 学格式示范、再 RL 用奖励打磨）与混合训练（SRFT、HPT 等把 SFT 与 RL 信号放进同一目标或交替使用）之争，过去一年多篇论文声称混合更好。ETH 团队回头查对照组，发现基线被两个 bug 共同拖累。
2. **机制/方法**：bug 一在梯度累积：DeepSpeed 开 ZeRO + CPU offload 时，2024-09 的一处改动让梯度拷贝函数只在 micro-step id 为 0 时执行，8 个 micro-batch 只有第一份梯度真正交给优化器，其余累加完就被清掉——有效 batch 缩小 8 倍且不报错，走这条路径的框架（OpenRLHF、LLaMA-Factory、TRL 等）全部中招。bug 二在 loss 聚合：正确做法是所有 token 的 loss 求和除以总 token 数；涉事框架先算每个 mini-batch 内部均值再对均值平均，短序列每个 token 的权重被放大（100 token 与 1000 token 两个 batch 等权平均时短者单 token 权重是长者 10 倍），分布式下各 rank token 数不同扭曲更大。
3. **关键证据或数字**：两个 bug 让 Qwen2.5-Math-7B 基线掉 5.7 分（优化器 bug 占 5.1、聚合 bug 占 0.8）：有 bug 48.3、修好 54.0。在修好的机器上再比：数学基准先 SFT 再 RL 拿 57.0，最好混合方法 SRFT 53.2，领先 3.8；Llama-3.1-8B 上 43.7 对 HPT 的 21.5，领先 22.2。算力账：SFT 做扎实后只需 50 步 RL 就超过混合方法，总算力约 $3.63\times10^{9}$ FLOPs 量级（字幕口径），混合方法近其两倍。诚实边界：分布外的 ARC/GPQA/MMLU-Pro 上 SRFT 62.5 略高于两阶段的 59.9，混合方法并非一无是处，但其声称的主战场结论被翻转。
4. **结论/判断**：两阶段更好的机理与 G007 互通：SFT 把格式与示范学透，RL 只用奖励打磨；混在一起时示范梯度与奖励梯度方向不同、互相拖拽。

## 关键数字

| 指标 | 有 bug 基线 | 修好后 |
|---|---|---|
| Qwen2.5-Math-7B 基线分 | 48.3 | 54.0 |
| 两阶段 vs 最好混合（Qwen 数学） | — | 57.0 vs 53.2 |
| 两阶段 vs 最好混合（Llama-3.1-8B） | — | 43.7 vs 21.5 |

## 可迁移

- RL infra 三个自检：关键结论在两个独立框架交叉验证；loss 聚合先全局汇 token 的 sum 与 count 再求均值；写等价性单元测试——8 个 micro-batch 累积一次更新与一次大 batch 更新的参数差应在浮点误差内，不相等就是丢梯度。
- 面试讲顺序问题：先给结论（先 SFT 再 RL），再用这个 bug 故事说明「基线可信度」比方法新意更先决。

## 疑问 / 下一步

- 分布外基准上混合方法仍略胜，是否说明交替训练对防灾难性遗忘有真实收益，值得看原文的 OOD 设定。
