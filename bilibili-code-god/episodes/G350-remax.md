# G350 — ReMax：PPO 的轻量替代，砍 Critic 用 greedy 解码当 baseline
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G350-remax.html

## 元信息
- 编号：G350
- 标题：ReMax：PPO 的轻量替代，砍 Critic 用 greedy 解码当 baseline
- BV：BV1gYgR6vEt4
- 时长：03:26
- 发布日期：2026-07-30
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：ReMax（A Simple, Effective and Efficient RL Method）、REINFORCE、PPO、GRPO

## 一句话总结
ReMax 砍掉 PPO 的 critic：每个 prompt 只多跑一次 greedy 解码，用它的奖励当 baseline，优势就是采样奖励减去 greedy 奖励，一次前向换掉整个价值网络的训练开销。

## 核心
1. 问题/背景：PPO 训练要同时挂 actor、critic、reward、reference 四个模型，actor 与 critic 都要反向更新，显存翻倍、超参爆炸。回到 REINFORCE 本身，序列级奖励只在末尾给一次、中间 token 奖励为零，直接拿原始奖励当优势方差极大，必须有个 baseline 把方差压下去——critic 是最重的一种造 baseline 的方式。
2. 机制/方法：对每个 prompt 先正常采样得回复及其奖励，再做一次 greedy 解码（每步取概率最大的 token）得另一条回复及其奖励，优势 = 采样奖励 − greedy 奖励。比 greedy 好就鼓励、差就压制。greedy 输出是当前策略最自信的轨迹，与采样同模型同分布，天然把"prompt 本身难不难"这个干扰项减掉。
3. 关键证据或数字：论文实验中 ReMax 在对话、摘要、代码等任务上效果接近 PPO，训练速度约快 2 倍、显存约省一半。前提是 SFT 之后的模型已足够稳定，greedy 轨迹波动小，才配当基准线。
4. 结论/判断：三种 baseline 路线各有取舍——PPO 用学出来的 critic 最准但最重；GRPO 用同组多样本均值效果好但采样成本高；ReMax 用单个 greedy 样本最省，适合算力/显存受限时先跑通 RL 闭环。

## 关键数字
| 对比 | PPO | ReMax |
| --- | --- | --- |
| baseline 来源 | 训练 critic 网络 | greedy 解码奖励 |
| 额外成本 | 一整个模型的训练 | 每 prompt 一次贪心前向 |
| 训练速度 / 显存 | 基线 | 约 2 倍快 / 约省一半 |

## 可迁移
- 面试答"GRPO/ReMax/PPO 区别"时抓住一条主线：它们只是在"baseline 怎么造"上不同，策略梯度骨架没变。
- RL infra 选型：显存紧、想快速验证奖励设计时，ReMax 式无 critic 方案是低成本起点；要精度再上 critic 或组采样。

## 疑问 / 下一步
- greedy baseline 在策略熵较高、greedy 与采样分布差距大时是否仍低方差，值得查 ReMax 原论文的方差分析。
