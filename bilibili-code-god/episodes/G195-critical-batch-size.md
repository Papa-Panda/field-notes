# G195 — Batch size 怎么选？Critical Batch Size 与线性缩放规则详解
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G195-critical-batch-size.html

## 元信息

- 编号：G195
- 标题：Batch size 怎么选？Critical Batch Size 与线性缩放规则详解
- BV：BV1TM8t6iEFL
- 时长：03:07
- 发布日期：2026-09-04
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：OpenAI 关于梯度噪声尺度与 critical batch size 的研究（字幕提及）

## 一句话总结

Batch size 不是越大越好：存在一个 critical batch size 拐点，超过后收益急剧递减；调 batch 必须同步按线性缩放规则调学习率。

## 核心

1. **问题/背景**：batch 开太小训练慢，开太大泛化变差，且它与学习率强绑定，改一个必须改另一个。先分清全局 batch size（真正影响训练效果的参数）与单卡 batch（只是显存约束下的妥协）。
2. **机制/方法**：全局 batch = 单卡 batch × GPU 数 × 梯度累积步数，三者任一变化全局值就变。Critical batch size 是 OpenAI 发现的临界值：临界值之前增大 batch 可同时提速与改善收敛；超过后速度不再明显提升，泛化反而可能变差。batch 与学习率按线性缩放规则联动：batch 翻倍、学习率翻倍（大 batch 梯度更平滑，能承受更大步长）；batch 特别大时线性缩放失效，改用平方根缩放。
3. **关键证据或数字**：预训练全局 batch 经验值约 400 万 token；SFT 阶段 128–512；DPO 32–128；RLHF/PPO 的 rollout batch 与 update batch 是两个独立参数，需分别设置。实操找最优值：以 128 为锚点先跑一轮，再试 64 与 256 看方向，在更好的方向上继续微调并同步调学习率，同时监控 GPU 利用率（不到 90% 说明 batch 还可加大或 IO 有瓶颈）。
4. **结论/判断**：过了临界点再加大 batch 就是在烧卡；找 critical batch size 才是关键。

## 关键数字

| 项 | 数值 |
|---|---|
| 预训练全局 batch | 约 400 万 token |
| SFT 全局 batch | 128–512 |
| DPO 全局 batch | 32–128 |
| GPU 利用率健康线 | ≥ 90% |

## 可迁移

- 面试被问 batch 与学习率关系时，先报全局 batch 的三因子定义，再讲线性缩放规则及其在大 batch 下的失效与平方根替代。
- RL 训练调参时记住 rollout batch 与 update batch 解耦设置，别用一个数套全程。

## 疑问 / 下一步

- Critical batch size 随训练进程（loss 下降）会漂移，实操中是否值得做 batch size 动态增长调度？
