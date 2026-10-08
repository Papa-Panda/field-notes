# G023 — PPO 的四个模型：谁在学、谁在看，以及显存为什么是它的死穴
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G023-ppo-four-models.html

## 元信息

- 编号：G023
- 标题：PPO 的四个模型：谁在学、谁在看，以及显存为什么是它的死穴
- BV：BV1vEhU6VE81
- 时长：00:57
- 发布日期：2026-10-03
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：InstructGPT（critic 与 RM 均为 6B，critic 由 RM 初始化）；本期为「RL 入门到 GRPO」系列第 16 期

## 一句话总结

训一个 7B 的策略，显存里却要同时放四个 7B：actor 与 critic 在学，reward model 与 reference model 冻住只看——四模型驻留正是 PPO 的显存死穴，也是 GRPO 砍掉 critic 的出发点。

## 核心

1. 问题/背景：为什么 RLHF 版 PPO 要四个模型，而不是一个？各自不干什么、干什么，必须先分清。
2. 机制/方法：分工是两学两冻——actor（策略）要训练，负责写回答；critic（价值函数）要训练；reward model 冻住，只负责打分；reference model（SFT 那一版）冻住，只负责算 KL。一次迭代的数据流是：提问进来，actor 生成回答，reward model 在句尾给一个分，reference model 给每个 token 一个 KL 距离，critic 给每个 token 一个价值估计，由此算 GAE 优势，再同时更新 actor 与 critic。
3. 关键证据或数字：InstructGPT 的配置细节：critic 从 reward model 初始化，两者都是 6B；优势按小批做白化（均值 0、方差 1），价值函数也要 clip；每批数据过 4 个 epoch；策略必须从 SFT 起步，随机初始化会失败。
4. 结论/判断：显存账是关键——critic 和策略一样大、还带优化器状态，四模型同驻使显存成为 PPO 的结构性瓶颈。DeepSeekMath 正是从这句话出发把 critic 砍掉，通向 GRPO（系列第 18 期）。

## 可迁移

- 估算 RLHF 训练显存时按「四份模型 + 两份优化器状态」起算，而不是只算策略本身。
- 面试讲 PPO 先讲四模型分工与一次迭代的数据流，再讲 clip 与 GAE，结构会清楚得多。

## 疑问 / 下一步

- critic 由 RM 初始化这一细节在现代开源框架（TRL、OpenRLHF、verl）里是否还保留，下次读框架源码时核对。
