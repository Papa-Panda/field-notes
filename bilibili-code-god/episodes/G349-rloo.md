# G349 — REINFORCE Leave-One-Out：不要 Critic、不要 greedy 假想敌，同组 response 互卷就够了
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G349-rloo.html

## 元信息
- 编号：G349
- 标题：REINFORCE Leave-One-Out：不要 Critic、不要 greedy 假想敌，同组 response 互卷就够了
- BV：BV13agR6KEDw
- 时长：04:04
- 发布日期：2026-07-30
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：RLOO（REINFORCE Leave-One-Out）、ReMax、GRPO

## 一句话总结
RLOO 不用 critic、不用额外解码：同一 prompt 采样 $ M $ 条回复，每条的 baseline 就是其余 $ M-1 $ 条的平均奖励，高于同伴平均就鼓励、低于就压制。

## 核心
1. 问题/背景：RLHF 的 baseline 一直在做减法——原始 REINFORCE 直接用奖励当梯度权重，方差大到训不动；PPO 引入 critic 估值，效果好但多一份显存算力还怕估不准；ReMax 用 greedy 解码那条回复的奖励当 baseline，零训练成本但只有一条样本、代表性弱。
2. 机制/方法：RLOO 对每个 prompt 采样 $ M $ 条回复并逐条打分，第 $ j $ 条的 baseline 是除它之外其余 $ M-1 $ 条奖励的均值，advantage 就是自身奖励减这个 baseline。关键在 leave-one-out：必须把自己排除，否则高分样本会抬高自己的 baseline、低分样本会压低自己的 baseline，advantage 被自我稀释；排除后每条面对的都是真实对手，比较无偏。
3. 关键证据或数字：论文在多个 RLHF 基准上达到与 PPO 相当、优于 ReMax 的效果。实操上 $ M $ 常取 2–16，4 或 8 性价比最高：太小 baseline 噪声大，太大采样成本线性上涨；采样温度一般给到 0.8–1.2 并配较高的 top-p，否则同组回复太像、奖励挤在一起、advantage 近零等于白训；KL 惩罚照常保留。
4. 结论/判断：与 GRPO 的组内归一化相比，RLOO 的 baseline 不含自己、也不除以标准差，工程上更干净；三者的分野就是 baseline 怎么构造。

## 关键数字
| 方法 | Baseline | 额外成本 |
|---|---|---|
| PPO | 训练 critic 网络估值 | 一份显存 + 算力 |
| ReMax | greedy 解码单条回复的奖励 | 一次额外解码、信号单一 |
| RLOO | 同组其余 $ M-1 $ 条奖励均值 | 无（复用组内采样） |
| GRPO | 同组全部 $ M $ 条均值（含自己）再除标准差 | 无 |

## 可迁移
- 做 RL infra 时，组内 baseline 路线（RLOO/GRPO）省掉 critic 后，显存与流水线复杂度都下降一截，代价是每个 prompt 必须采多条——rollout 吞吐成了真正的瓶颈。
- 面试对比 RLOO 与 GRPO 必答两点：是否包含自己、是否做标准差归一化。

## 疑问 / 下一步
- 当同组奖励全相同（全对或全错）时 advantage 恒为零，这类 prompt 的采样算力如何回收？可对比 DAPO 的动态采样。
