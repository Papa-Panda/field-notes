# G345 — TD 时序差分：MC 采样 + DP bootstrap，SARSA / Q-learning / Actor-Critic 全是它的实例
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G345-td-learning.html

## 元信息
- 编号：G345
- 标题：TD 时序差分：MC 采样 + DP bootstrap，SARSA / Q-learning / Actor-Critic 全是它的实例
- BV：BV1uvgR6PEin
- 时长：03:35
- 发布日期：2026-07-31
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：未标注

## 一句话总结
TD 是免模型 RL 的主力：像蒙特卡洛一样从经验采样，又像动态规划一样用下一步的估计自举，走一步就更新一次，TD error 是整个算法家族的学习引擎。

## 核心
1. 问题/背景：蒙特卡洛（MC）要用完整 episode 的实际回报，无偏但必须等整段结束、方差大；动态规划（DP）一步更新，但需要事先知道状态转移概率与奖励函数，现实里拿不到。TD 想兼得两者之长。
2. 机制/方法：TD 只走一步，用即时奖励加上下一状态的当前价值估计作为更新目标，而不是等真实回报算完。更新量就是 TD error $ \delta $ ：估计目标与当前估计之差；$ \delta > 0 $ 表示现实比预期好，反之是意外失望。
3. 关键证据或数字：本质是偏差-方差权衡——MC 无偏高方差，TD 因目标里含估计而带小偏差，但只依赖一步转移，方差小得多、学习更稳；DP 无偏无方差但要环境模型。数学上可证这种「用估计更新估计」的自举会收敛。
4. 结论/判断：SARSA（同策略 TD 控制）、Q-learning（异策略 TD 控制）、Actor-Critic（critic 用 TD 学价值、actor 用 TD error 当优势信号）都是 TD 的实例；PPO、A2C、TRPO 骨子里都在用 TD error 当学习信号。

## 关键数字
| 方法 | 特点 |
|---|---|
| MC | 无偏、高方差、须等 episode 结束 |
| DP | 无偏无方差、须知环境模型 |
| TD | 小偏差、低方差、免模型、走一步更新一次 |

## 可迁移
- 面试里被问 PPO 的优势函数从哪来，可直接答到源头：GAE 本质是对 TD error 做多步加权，critic 的学习信号就是 TD。
- 理解偏差-方差权衡有助于判断 RL 训练不稳时该调什么：目标估计步数越长越无偏但方差越大。

## 疑问 / 下一步
- 一步 TD 的偏差具体如何随步数（TD(λ) / n-step）过渡到 MC？可接着看 GAE 的推导。
