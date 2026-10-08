# G190 — critic value function 详解：为什么难训准、GAE 怎么补、GRPO 怎么砍
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G190-critic-value-gae.html

## 元信息

- 编号：G190
- 标题：critic value function 详解：为什么难训准、GAE 怎么补、GRPO 怎么砍
- BV：BV1uP8t6uE9J
- 时长：03:08
- 发布日期：2026-09-05
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：PPO、GAE、GRPO（DeepSeek）

## 一句话总结

Critic 的职责只是给 advantage 提供一个降方差的基线，但它在大模型上系统性训不准；GAE 用 ， $\lambda$ ，在偏差与方差间折中续命，GRPO 则干脆砍掉 critic、用组内平均 reward 当基线。

## 核心

1. **问题/背景**：Actor 的更新方向由 advantage 决定，而 advantage 等于实际回报减去 critic 的 value 预测。Critic 高估某状态，advantage 被低估、actor 在那里学不够；低估则反之；系统性偏差会直接把 actor 往错误方向带，表现为 reward 曲线震荡或收敛到次优解。
2. **机制/方法**：Critic 难训准有结构性原因：大模型状态空间巨大、每个上下文都是没见过的新状态，训练数据覆盖不了；奖励又稀疏，中间步 reward 多为零，value 很难学出有意义的信号，于是预测方差大。GAE 的补法是用 ， $\lambda$ ，混合多步回报：， $\lambda = 0$ ，完全依赖 critic（低方差高偏差，critic 不准就惨），， $\lambda = 1$ ，完全依赖实际回报（无偏高方差），默认 0.95 是折中；发现 critic 不准时可调大 ， $\lambda$ ，降低对它的依赖。GRPO 的砍法是同一 prompt 采样多个回答、用组内平均 reward 作共享基线，不再单独训 value 网络。
3. **关键证据或数字**：监控指标是 critic 的 value loss 与 explained variance，低于 0.5 说明 critic 严重不准、应考虑调大 ， $\lambda$ ，；GRPO 省掉 critic 约省一半相关显存与训练开销，实际效果反而更稳。若必须用 critic：给它单独的学习率（通常比 actor 小），网络可与 actor 共享底层、只分一个 value head。
4. **结论/判断**：Critic 存在的意义是提供基线，能用组内均值替代就别硬训——这是 GRPO 在 LLM 场景胜出的工程逻辑，而非算法优越性的证明。

## 关键数字

| 量 | 取值/判据 |
|---|---|
| GAE ， $\lambda$ ，默认 | 0.95 |
| explained variance 警戒线 | < 0.5 视为 critic 严重不准 |
| GRPO 基线 | 组内平均 reward（无 critic） |

## 可迁移

- 面试被问「GRPO 为什么不要 critic」时按这条链答：基线的作用是降方差 → critic 在稀疏奖励+巨大状态空间下训不准、偏差会系统性误导 actor → 组内统计量是够用且免费的替代基线。
- 排查 PPO 训练震荡时，先看 explained variance 再调 actor 的超参，顺序别反。

## 疑问 / 下一步

- 组内基线在 prompt 难度差异极大时方差如何，是否需要按难度分层采样来补，视频未展开（可与 G189 的难度分档合起来想）。
