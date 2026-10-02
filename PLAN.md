# Post-training / RL Infra 实操备考计划

2026-10-02 定稿。目标：frontier lab post-training / RL-infra 岗的实操轮次手感训练，约 10 天读完 + 动手跑完。

## 面试轮次地图（两个 track）

**Training track**
1. Research PyTorch —— 现场调 post-training 训练代码（DPO debugging 形态）
2. Production PyTorch —— tensor parallel 线性层亲手实现（Megatron 式）

**RL track**
1. Research PyTorch —— 同上
2. RL infra foundations —— 并行概念 coding + verbal（TP/DP/PP）
3. RL systems coding —— rollout/训练系统的现场搭建（异步 actor-learner、trajectory 存储、reward 服务）

外加一轮 non-AI session（通用代码轮），不在本计划范围。

## 阶段 1 — Research PyTorch（公共科目，先打）

| # | 主题 | 文件 |
|---|---|---|
| 01 | 训练循环零起 + 6 个 debug case | `pytorch/research/01-training-loop` |
| 02 | DPO loss 手写 + debug | `pytorch/research/02-dpo-loss` |
| 03 | PPO/GRPO loss、clip、advantage、KL | `pytorch/research/03-ppo-grpo-loss` |
| 04 | 注意力机制手写（SDPA/多头/KV cache） | `pytorch/research/04-attention` |

## 阶段 2 — 并行基础（RL foundations + Production 共用）

| # | 主题 | 文件 |
|---|---|---|
| Day 01 | 集合通信与 DDP（因果链版） | `pytorch/day-01-distributed-ddp` |
| 05 | ZeRO / FSDP：分片的账 | `pytorch/parallel/05-zero-fsdp` |
| 06 | TP 手写 linear（column/row-parallel） | `pytorch/parallel/06-tensor-parallel` |

## 阶段 3 — RL systems coding

| # | 主题 | 文件 |
|---|---|---|
| 07 | rollout→train 系统骨架：trajectory 存储、权重同步、异步 actor-learner | `pytorch/rl-systems/07-rl-systems` |

## 阶段 4 — 缺口（不占实操主线，单独补）

- system design：大规模训练 / RLHF / rollout 系统设计（架构→瓶颈→容错→可观测）
- ML/RL 理论：概率、优化、policy gradient、off-policy、reward modeling
- behavioral：project deep dive、跨团队协作

## 10 天节奏建议

- Day 1–4：Research 01–04（一篇/天，notebook 必须亲手跑通）
- Day 5：DDP 因果链重读 + ZeRO/FSDP
- Day 6：TP 手写 linear
- Day 7：RL systems 骨架
- Day 8：三方对照复盘（01–07 的 debug 清单默写）
- Day 9：模拟一轮 Research PyTorch（任选 DPO/GRPO 代码现场 debug）
- Day 10：system design 框架 + behavioral 素材整理

---
*状态：阶段 1 已完成（2026-10-02），阶段 2 进行中。*
