# G228 — PPO 训练显存爆炸怎么办？四模型驻留、offload 与稳定性调参

> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G228-ppo-memory.html

## 元信息

- 编号：G228
- 标题：PPO 训练显存爆炸怎么办？四模型驻留、offload 与稳定性调参
- BV：BV15V8S6kEkq
- 时长：01:58
- 发布日期：2026-08-30
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：PPO / RLHF；verl 框架的 actor–reference 共进程实现

## 一句话总结

PPO 显存爆炸的根源是 actor、critic、reference、reward 四模型同时驻留，解法是把不更新的模型 offload 或共享骨干，再用 KL 系数、clip range、GAE λ 三板斧守住稳定性。

## 核心

1. **问题/背景**：四个模型各司其职——actor 是被训练的策略，reference 冻结用于算 KL 散度，reward model 给输出打分，critic 估计状态价值算优势。7B 模型四份权重约 56 GB，再叠加各自的优化器状态、梯度和激活，轻松超过 200 GB，远超单卡容量。
2. **机制/方法**：省显存两招——其一，offload 不更新参数的 reference 与 reward 到 CPU 或降精度，只让 actor 与 critic 全精度驻留，可省约一半显存；其二，四个模型同源初始化时共享冻结的 embedding 与大部分 transformer 层，各自只维护差异部分（小头）。工程上 reference 只需前向算 log-prob、无需梯度，可与 actor 共进程顺带算出（verl 即如此），省掉一份独立 forward。
3. **关键证据或数字**：稳定性三板斧的经验值——KL 系数一般取 0.05（太小策略跑飞、太大学不动），clip range 默认 0.2，GAE 的 ， $\lambda$ ，默认 0.95 平衡偏差与方差。
4. **结论/判断**：PPO 的工程难点不在算法而在资源组织：先用 offload + 共享骨干把显存压进卡内，再用三个超参守住 reward 崩塌、KL 爆炸、输出发散三类不稳定信号。

## 关键数字

| 项目 | 数值 |
| --- | --- |
| 7B × 4 模型权重 | 约 56 GB |
| 叠加优化器/梯度/激活后总需求 | >200 GB |
| KL 系数经验值 | 0.05 |
| clip range 默认 | 0.2 |
| GAE λ 默认 | 0.95 |

## 可迁移

- RL infra 选型时先算四模型驻留账：reference/reward 能否 offload 或与 actor 共进程，是显存预算的第一杠杆，先于切分策略。
- GRPO 砍掉 critic 的动机一半在算法、一半在显存——面试聊 PPO→GRPO 演进时可从四模型驻留成本切入。

## 疑问 / 下一步

- 共进程共享前向在多大模型规模上仍成立、与独立部署的吞吐差多少，值得查 verl 的实测数据。
