# G054 — GAE 的 λ 到底在调什么？λ 为什么可以比 γ 小得多
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G054-gae-lambda.html

## 元信息

- 编号：G054
- 标题：GAE 的 λ 到底在调什么？λ 为什么可以比 γ 小得多
- BV：BV1Tohm6bEe4
- 时长：01:00
- 发布日期：2026-09-29
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：GAE（Generalized Advantage Estimation）；PPO 默认配置

## 一句话总结

GAE 把一步 TD 到整局蒙特卡洛之间的一族优势估计按 ， $\gamma\lambda$ ， 的幂加权平均， ， $\lambda$ ， 是纯粹的偏差—方差旋钮，所以它可以比改目标的 ， $\gamma$ ， 小得多。

## 核心

1. **问题/背景**：蒙特卡洛估计无偏但方差大，TD 估计方差小但有偏，能不能有个旋钮在中间任意停？
2. **机制/方法**：一步估计用一个 TD 残差 ， $\delta$ ， ，两步用两个，走完整局就是蒙特卡洛；GAE 把这些不同步数的估计按 ， $\lambda$ ， 的幂加权平均，等价于把 ， $\delta$ ， 按 ， $\gamma\lambda$ ， 的幂累加。实现上就是一行从后往前的递推：当前优势等于当前 ， $\delta$ ， 加上下一步优势乘 ， $\gamma\lambda$ ， 。

$$A_t = \sum_{l=0}^{\infty} (\gamma\lambda)^l \delta_{t+l}$$

3. **关键证据或数字**： ， $\lambda = 0$ ， 时只剩当前 ， $\delta$ ， ，退化为 TD； ， $\lambda = 1$ ， 时变成整局回报减 ， $V$ ， ，即蒙特卡洛。GAE 论文建议 ， $\lambda$ ， 取 0.9–0.99，PPO 用 0.95；大模型里 ， $\gamma$ ， 常取 1， ， $\lambda$ ， 仍是 0.95。
4. **结论/判断**： ， $\gamma$ ， 与 ， $\lambda$ ， 不对称： ， $\gamma$ ， 改的是优化目标本身，价值估计再准它引入的偏差也在； ， $\lambda$ ， 只在价值函数估不准时才引入偏差。所以 ， $\lambda$ ， 可以放心比 ， $\gamma$ ， 小得多，它调的只是偏差与方差的折中。

## 可迁移

- 面试被问 GAE 时抓住一句： ， $\lambda$ ， 是偏差—方差旋钮、 ， $\gamma$ ， 是目标定义，两者不能混为一谈。
- 看 RL 框架代码时，优势计算应是一行反向递推；写成前向展开求和的实现通常有性能或数值问题。

## 疑问 / 下一步

- LLM 场景 ， $\gamma = 1$ ， 且序列很长时 ， $\lambda$ ， 的最优取值是否仍贴近 0.95，本期未展开。
