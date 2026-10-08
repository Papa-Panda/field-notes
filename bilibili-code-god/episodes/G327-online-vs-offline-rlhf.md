# G327 — Online RLHF vs Offline RLHF：在线交互与静态数据的取舍
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G327-online-vs-offline-rlhf.html

## 元信息
- 编号：G327
- 标题：Online RLHF vs Offline RLHF：在线交互与静态数据的取舍
- BV：BV1Gc3d6gEDo
- 时长：04:56
- 发布日期：2026-08-07
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：PPO、DPO、Iterative DPO、InstructGPT、Llama 2/3、Anthropic RLAIF

## 一句话总结
Online 与 offline RLHF 的分水岭是数据新鲜度与成本的权衡：PPO 每次更新都用当前策略重新采样，准但贵；DPO 在静态偏好数据上闭式优化，便宜但数据会陈旧；工业界的折中是定期刷新数据的 iterative DPO。

## 核心
1. **问题/背景**：同样是 RLHF，OpenAI 走 PPO、Meta 走 PPO 与 iterative DPO 混合、Anthropic 走 PPO 加 RLAIF，三条路线背后的差异本质上是一道关于算力成本与数据分布的选题。
2. **机制/方法**：Online 路线（PPO）是五步循环——rollout 生成、用 RM 打分、加 KL 惩罚、用 clip 目标更新、再用新策略重新采样，数据始终 on-policy。Offline 路线（DPO 及 KTO 等变种）一次性收集静态偏好对，跳过 RM 与 rollout，把偏好优化化为闭式分类损失直接训练。Iterative DPO 则周期性地用当前模型重新生成回答、由人或更强模型标注偏好、并入训练集再跑 DPO，本质仍是 offline，只是数据定期刷新以追踪策略分布。
3. **关键证据或数字**：业界经验里 rollout 约占 PPO 训练时间的 70%，需要常备一套推理集群；DPO 的痛点是 off-policy 分布偏移，训得越久越容易过拟合、长度爆炸与风格漂移。
4. **结论/判断**：选型看预算与模型规模——算力充足、追上限用 online PPO；预算有限或模型巨大用 iterative DPO；纯 DPO 适合快速验证与小规模实验。模型越大 rollout 越贵，iterative 路线的吸引力越强。

## 可迁移
- 做 RL 训练选型时先算 rollout 占比：若采样成本主导，优先考虑 iterative 式离线刷新而不是全程在线。
- 面试答 RLHF 路线差异时，用"数据新鲜度 × 训练成本"的二维权衡框架组织答案，比罗列算法名更有说服力。

## 疑问 / 下一步
- Iterative DPO 的刷新周期与每轮数据量如何定量选取，视频未展开，可查 Llama 3 技术报告的对齐章节核对。
