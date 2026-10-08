# G032 — APRIL：通过 partial rollout 改进同步 RL 的长尾等待，多发一倍、够了就停、没写完续写
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G032-april-partial-rollout.html

## 元信息

- 编号：G032
- 标题：APRIL：通过 partial rollout 改进同步 RL 的长尾等待，多发一倍、够了就停、没写完续写
- BV：BV1jDeh6uEYy
- 时长：03:57
- 发布日期：2026-10-01
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：APRIL（partial rollout，源自 Kimi K1.5 的 partial rollout 思想）；Selective Rollout；对照 AReaL / AsyncFlow / StreamRL 等全异步方案

## 一句话总结

同步 RL 的瓶颈不是算力而是等最慢的那一条 rollout：APRIL 用「多发一倍、凑够就停、没写完的存进 buffer 下一步续写」三步把长尾等待抹掉，吞吐平均 +22.5%、准确率不降，代价只是约 40% token 来自 5 步以内的旧策略这种温和的 off-policy。

## 核心

1. 问题/背景：同步 RL 每一步要等一个 batch 的 rollout 全部生成完才能更新。在 DAPO-Math-17k、DeepMath 等数据上，超过一半回答在几千 token 内结束，尾巴却拖到 32768 上限；batch 内长度标准差高达 4000–4500 token（同一道题的 8 条之间反而不到 1500）。结果 GPU 利用率从满载一路塌到只剩一条序列在跑，而 rollout 占整个训练时间的 90% 以上——瓶颈是等待，不是计算。
2. 机制/方法：以每步目标 32 道题 × 8 条 = 256 条为例，APRIL 分三步：第一步 over-provision，实际发起 64 道题共 512 条（两倍的量）；第二步够了就停，256 条一写完立刻截断其余生成；第三步续写，没写完的半截回答存入 continuation buffer，下一步优先把它们接着写完再补新题。这样每一步都不用等最慢的那条，那条的前半段也不浪费。代价是续写部分的 token 由旧策略生成：实测约 40% 的 token 来自前几步的策略，但最多不超过 5 步；APRIL 直接按混合策略来估计优势、不加额外重要性修正，训练照样稳定。
3. 关键证据或数字：rollout 吞吐平均提升 22.5%，Qwen3-8B + GRPO 在 DeepMath 上最高 49.5%，DAPO 上约 9%–13%；准确率平均还涨 2.1 分、最高 12.8，个别设置掉 1.6（不是全涨），且部分 baseline 在训练后期出现长度爆炸掉分、APRIL 没出现。与全异步方案（AReaL、AsyncFlow、StreamRL）对比：它们吞吐更高，但 off-policy 程度高一个量级、容易不稳；APRIL 留在同步框架内，只是温和 off-policy。另一条线是 2026 年 5 月的 Selective Rollout，从另一头下手：Agent 任务里约 40% 的组在前十步动作就趋同、奖励一样、方差为零、本来就没有梯度，它用组内动作序列的编辑距离判定「已定型」，整组中途掐掉，省 10.7%——一个是没写完的接着写，一个是注定没用的提前停。
4. 结论/判断：实操三条：先量每步 rollout 的中位长度与最长长度、rollout 占总时间比例，比例超过 80% 且最长是中位数的 5 倍以上才值得上；上 partial rollout 时注意推理引擎必须支持保留未完成序列的状态，这不是纯训练侧的改动；同时监控续写 token 的比例与「年龄」，超过 5 步的直接丢弃，并盯住响应长度别爆炸。

## 关键数字

| 指标 | 数值 |
|---|---|
| rollout 占训练时间 | 90% 以上 |
| batch 内长度标准差 | 4000–4500 token（同题内 <1500） |
| 吞吐提升 | 平均 +22.5%，最高 +49.5% |
| 准确率变化 | 平均 +2.1，最高 +12.8 |
| 续写 token 来源 | 约 40% 来自旧策略，最多不超过 5 步 |
| Selective Rollout 节省 | 10.7%（约 40% 的组前十步即定型） |

## 可迁移

- 这是 RL infra 面试的高频系统题：答长尾不要停在「用异步」，要能说清 over-provision + continuation buffer 的机制、off-policy 代价的量级（步数上限），以及它对推理引擎状态保持的要求。
- 自建训练循环时先埋点量长尾（中位 vs 最长、rollout 占比）再决定优化方向，避免为不存在的瓶颈上复杂方案。

## 疑问 / 下一步

- continuation buffer 与变长打包、prefix cache 的交互（续写序列的 KV 如何复用）在视频里未展开，是落地时要自己验证的工程点。
