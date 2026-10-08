# G487 — 什么是 On-Policy Distillation？取 SFT 与 RL 之长（reverse KL 详解）
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G487-on-policy-distillation.html

## 元信息

- 编号：G487
- 标题：什么是 On-Policy Distillation？取 SFT 与 RL 之长（reverse KL 详解）
- BV：BV1BnMh6BEMz
- 时长：03:58
- 发布日期：2026-07-07
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：On-Policy Distillation（OPD）；Qwen3、DeepSeek 后训练实践

## 一句话总结

OPD 让学生从自身分布采样轨迹、老师逐 token 打分，用反向 KL 做 mode-seeking 对齐，同时拿到 RL 的 on-policy 对齐与 SFT 的密集信号。

## 核心

1. **问题/背景**：后训练两条主流路线各有硬伤。RL 让模型自己生成整条回答、最后只得到一个序列级奖励，信号极稀疏、学得慢；SFT 蒸馏每个 token 都有梯度、信号密集，但学生训练时模仿的是老师的轨迹，推理时走自己的路，一旦走出一步老师不会走的棋，就会掉进训练中从未见过的状态并全盘崩坏（exposure bias）。
2. **机制/方法**：OPD 把两者缝合——像 RL 一样由学生从当前分布采样自己的轨迹（训练路径即推理路径，天然对齐），像 SFT 一样由老师对学生生成的每个 token 给出概率评分（信号密集）。优化目标是学生与老师之间的反向 KL：期望取在学生自身分布上，学生只需咬住老师复杂分布中的一种高分模式练到极致（mode-seeking），而不是覆盖老师的全部输出。
3. **关键证据或数字**：前向 KL（SFT 所用）期望取在老师分布上，逼学生覆盖老师每种解法，参数有限的小模型容易把两套逻辑搅成缝合怪；反向 KL 则相反。反向 KL 还带来两点：不可欺骗——学生胡编时老师在其输出上的概率近零，log 比值爆炸触发大惩罚；无分布偏移——训练数据就是学生自己的轨迹。工程上几乎零成本：在 GRPO/PPO 中把 advantage 换成老师与学生的 log 概率之差（对老师加 stop-gradient 防梯度回流），其余 policy gradient 流程照旧。
4. **结论/判断**：OPD 是站在 RL 肩膀上的异形替换，改动极小，已出现在 Qwen3、DeepSeek 等模型的后训练中；对小模型而言，精通一条正道远比模糊复刻十种路子高效。

## 可迁移

- 面试讲蒸馏时抓住一条主线：前向 KL 是 mean-covering、反向 KL 是 mode-seeking，OPD 选反向 KL 的理由（防缝合怪、防欺骗）要能脱口而出。
- RL infra 视角：OPD 不需要新框架，本质是把 GRPO 的 advantage 来源从奖励归一化换成师生 log-prob 差，rollout 与训练管线可直接复用。

## 疑问 / 下一步

- 老师需要对学生轨迹逐 token 输出 log 概率，rollout 侧的推理吞吐与显存开销如何与 GRPO 的奖励计算做统一预算？
