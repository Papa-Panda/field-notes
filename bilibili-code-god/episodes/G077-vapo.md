# G077 — VAPO：通过 value 预训练与解耦 GAE 改进长思维链上 critic 训不准的问题（字节 Seed）

> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G077-vapo.html

## 元信息

- 编号：G077
- 标题：VAPO：通过 value 预训练与解耦 GAE 改进长思维链上 critic 训不准的问题（字节 Seed）
- BV：BV1rnea6mE4y
- 时长：03:30
- 发布日期：2026-09-26
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：VAPO（字节 Seed，2025）、PPO / GAE、DAPO、DeepSeek R1-Zero

## 一句话总结

value 模型在长思维链上不是不能用，而是难训准；VAPO 用七招（value 预训练、解耦 GAE、长度自适应 GAE、clip-higher、token 级 loss、正样本 LM loss、组采样）把 critic 训准后，在 Qwen2.5-32B 上 AIME24 达 60.4、比无 value 方法高 10 分以上且零崩溃。

## 核心

1. **问题/背景**：PPO 的 value 模型预测「从当前 token 起未来能拿多少奖励」，用实际回报减预测值得到逐 token 优势，方差比 GRPO 的组内均值基线更小；但长 CoT 上有三个难点：① value 偏差——初始化的 value 模型对几千 token 的推理链一无所知，前期基线全是噪声；② 序列长度异构——同一 batch 里 500 token 与 8000 token 并存，GAE 的 $\lambda$ 一刀切，要么偏差大要么方差大；③ 奖励稀疏——几千 token 只在末尾有一个 0/1。
2. **机制/方法**：前三招治前两个难点：value 预训练（先固定策略只训 value 到能预测准回报，再联合训练）；解耦 GAE（value 的学习目标用 $\lambda = 1$ 的完整蒙特卡洛回报保持无偏，策略的优势估计用较小 $\lambda$ 降方差，两边各取所需）；长度自适应 GAE（ $\lambda$ 随序列长度调，长序列用更大 $\lambda$ ，避免折扣累积让优势在几千 token 上失真）。后四招治稀疏与稳定：clip-higher 放宽 clip 上界给低概率 token 上涨空间；token 级 loss 按 token 而非按序列平均，长序列不被稀释；正样本 LM loss 对答对的轨迹额外加一项语言模型损失，放大稀疏正信号；组采样同题多采，让 value 模型看到对比结果。
3. **关键证据或数字**：Qwen2.5-32B 上 AIME24 达 60.4，高于 DeepSeek R1-Zero Qwen-32B 与 DAPO 10 分以上；不到 5000 步达峰值、收敛比无 value 方法更快，多次运行零崩溃。
4. **结论/判断**：问题不是要不要 value，而是 value 怎么训才不拖后腿（这也解释了为何有团队从 GRPO 换回 critic-based PPO）。选型建议：任务长、奖励稀疏、要长训稳定，值得上 critic；短任务、算力紧，GRPO 够用。上 critic 前务必先做 value 预训练，别让噪声基线毁掉前几百步。

## 关键数字

| 项 | 数值 |
|---|---|
| AIME24（Qwen2.5-32B，VAPO） | 60.4 |
| vs R1-Zero Qwen-32B / DAPO | 高 10 分以上 |
| 达峰步数 | < 5000 步 |
| 多次运行崩溃 | 0 次 |

## 可迁移

- RL infra 排障视角：critic 路线前期不稳，先怀疑 value 预训练不足与 GAE 的 $\lambda$ 设置，而不是急着换算法；value 目标与策略优势解耦是可直接借用的配方。
- 面试谈 PPO vs GRPO 时，用「value 的三难（偏差、长度异构、稀疏）+ 对应解法」组织回答，比只说「GRPO 省一个模型」完整得多。

## 疑问 / 下一步

- 长度自适应 GAE 中 $\lambda$ 随长度的具体函数形式，值得查 VAPO 原文确认。
