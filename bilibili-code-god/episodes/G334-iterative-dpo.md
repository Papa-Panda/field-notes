# G334 — Iterative DPO：让模型自我改进，PPO 效果的 1/10 成本
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G334-iterative-dpo.html

## 元信息
- 编号：G334
- 标题：Iterative DPO：让模型自我改进，PPO 效果的 1/10 成本
- BV：BV1JC3R6QE5N
- 时长：03:48
- 发布日期：2026-08-05
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：Llama 3 技术报告（Iterative DPO 对齐配方）；DPO（Direct Preference Optimization）

## 一句话总结
把 DPO 的静态偏好数据换成「当前模型生成 → 打分标注 → 训练」的滚动循环，让离线算法吃到 on-policy 红利，效果追平 PPO 而成本只有约 1/10。

## 核心
1. **问题/背景**：普通 DPO 用一份固定偏好集一次训完；模型训着训着就偏离数据采集时的分布（off-policy 偏移），在 70B 量级、几十万步的训练里很快撞天花板。
2. **机制/方法**：循环三步——当前模型对每个 prompt 采样 4~8 个回答；标注方挑出最好与最差组成偏好对；跑一轮 DPO 得到更强的模型，再回到第一步重新生成。标注有三条路，成本依次降低：奖励模型打分（Llama 3 主路）、更强的 LLM 当裁判（AI feedback，Zephyr/Starling 一派）、规则标注（代码跑通测试、数学答案对错）。
3. **关键证据或数字**：Llama 3 在 SFT 后跑 6 轮 Iterative DPO，每轮约 1 万对偏好数据（与历史数据混合防遗忘），DPO 的 $\beta$ 取 0.01；最终 70B Instruct 达到 GPT-4 早期版本水平。视频判断其胜过 PPO 的根本原因不是效果而是性价比：采样可并行离线跑、训练只是普通对比损失，没有 KL 系数调参、没有 value model、没有 rollout server。
4. **结论/判断**：DPO 不是一次到位的算法，滚起来（数据随模型分布滚动刷新）才厉害；能用规则标注的地方优先用规则，成本最低、噪声最小。

## 关键数字
| 项 | 值 |
|---|---|
| 每 prompt 采样数 | 4~8 个回答 |
| Llama 3 迭代轮数 | 6 轮 |
| 每轮偏好对 | 约 1 万对 |
| DPO $\beta$ | 0.01 |
| 相对 PPO 成本 | 约 1/10 |

## 可迁移
- 做 post-training 选型时先算性价比：Iterative DPO 是离线迭代，工程复杂度远低于 PPO 的在线采样 + advantage + clip 流水线，适合作为 RLHF 的默认起点。
- 面试高频点：静态 DPO 的 off-policy 分布偏移是其核心缺陷，「生成-标注-训练」循环 + best-of-n/worst-of-n 组对是标准答法。

## 疑问 / 下一步
- 每轮 RM 都要用最新数据/模型刷新，否则标注分布同样会过时——RM 本身的迭代节奏和成本如何与策略轮数配比？
