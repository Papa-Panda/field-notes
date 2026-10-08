# G041 — PPO 完整训练流程：三步一轮、三项损失，以及大模型版的参数
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G041-ppo-full-loop.html

## 元信息

- 编号：G041
- 标题：PPO 完整训练流程：三步一轮、三项损失，以及大模型版的参数
- BV：BV1WFhU6xEmR
- 时长：00:58
- 发布日期：2026-09-30
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：PPO（Schulman et al. 2017）；InstructGPT 的 PPO 配置

## 一句话总结

PPO 的一轮 = 采样 → 算优势 → 多 epoch 更新，损失由 clipped 策略项、critic 价值项、熵奖励三项合成；大模型版把 epoch 压到 1、batch 换成回答条数，其余骨架不变。

## 核心

1. **问题/背景**：系列前十期把 PPO 的零件（比率、clip、GAE、critic 等）逐个讲完，这一期把它们装成完整的训练循环，顺带对照大模型版的参数差异。
2. **机制/方法**：第一步，多个并行 actor 用当前策略各跑若干步，攒一批轨迹；第二步，对每条轨迹用 GAE 递推算出优势；第三步，把这批数据切成 minibatch 反复过 $K$ 个 epoch 做更新——每过一遍，重要性比率就偏离 1 一点，clip 在比率越界时截断梯度；更新完用新策略替换旧策略，回到第一步。损失共三项：clip 目标管策略，价值预测的平方误差管 critic，再加一项熵奖励防过早收敛。
3. **关键证据或数字**：原论文（MuJoCo）每轮采 2048 步、过 10 个 epoch、clip $\varepsilon$ 取 0.2 ，Atari 实验的熵系数为 0.01 ；大模型版（InstructGPT）每轮 512 条回答、切 8 个 minibatch、只过 1 个 epoch，clip 同样是 0.2 。
4. **结论/判断**：大模型 PPO 相对经典 PPO 的改动主要是数据形态（轨迹变回答）和 epoch 数（10 → 1，防止对同一批回答过拟合），算法骨架完全一致。

## 关键数字

| 项 | 经典 PPO（MuJoCo） | 大模型版（InstructGPT） |
|---|---|---|
| 每轮数据量 | 2048 步 | 512 条回答 |
| 每轮 epoch | 10 | 1 |
| minibatch 切分 | — | 8 个 |
| clip $\varepsilon$ | 0.2 | 0.2 |

## 可迁移

- 面试讲 PPO 时用「三步一轮、三项损失」作骨架，再逐项展开，比直接背公式更稳。
- 工程上注意 epoch 数：on-policy 数据复用越多越容易过拟合/偏离，大模型场景普遍只过 1 个 epoch。

## 疑问 / 下一步

- 大模型版为什么批大小以「条回答」而非 token 计？与序列长度方差、GAE 的计算粒度有关，值得对照 verl 等框架的实现再确认。
