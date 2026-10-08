# G324 — importance sampling ratio + clip：同一 batch 训 4 epoch 的秘密
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G324-importance-ratio-clip.html

## 元信息

- 编号：G324
- 标题：importance sampling ratio + clip：同一 batch 训 4 epoch 的秘密
- BV：BV1DP3d6TED7
- 时长：04:36
- 发布日期：2026-08-08
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：PPO（Schulman et al., 2017）

## 一句话总结

PPO 是「伪 on-policy」：它用重要性采样比率 $r_t$ 度量新旧策略的偏差，再用 clip 把偏差超过 ±20% 的样本梯度直接清零，从而敢在同一 batch 上安全地跑 3–4 个 epoch。

## 核心

1. **问题/背景**：PPO 名为 on-policy，却要在同一批数据上跑多个 epoch 做 minibatch 更新——数据用第二次就成了旧策略采的，这不就 off-policy 了吗？答案藏在重要性采样：用旧策略数据估计新策略期望时，按新旧概率比加权即可无偏，但前提是两策略差异不能太大，否则方差爆炸。
2. **机制/方法**：比率定义为同一状态-动作对上当前策略与旧策略的概率比：

$$ r_t(\theta) = \frac{\pi_\theta(a_t \mid s_t)}{\pi_{\theta_{\mathrm{old}}}(a_t \mid s_t)} $$

   目标函数取 $r_t A_t$ 与其 clip 版本的较小者（ $A_t > 0$ 时； $A_t < 0$ 时对称取较大者）。一旦 $r_t$ 越出 $[1-\varepsilon, 1+\varepsilon]$ ，目标被压平、该样本梯度为零，相当于自动退场——clip 就是一层隐式信任域。
3. **关键证据或数字**：看 $r_t$ 分布随 epoch 的演变：第一个 minibatch 时参数未动， $r_t$ 精确等于 1，是真正的 on-policy 更新、根本不需要修正；第 2 个 epoch 分布成以 1 为中心、宽度约 ±0.05 的小山峰；第 3 个 epoch 两边开始撞上 0.8 与 1.2 的 clip 边界；第 4 个 epoch 已有相当比例样本被截断。若跑到 10 个 epoch， $r_t$ 会飘到 0.5–2，绝大多数样本被 clip、有效梯度骤减，白训。
4. **结论/判断**：典型工程参数是 $\varepsilon = 0.2$ 、epoch 3–4 次、minibatch 为总 batch 的 1/4 到 1/64，这是反复调出的甜点位。PPO 的精妙在于分工：ratio 负责度量偏差，clip 负责拒绝偏差过大的样本，一次采样因此能支撑多次更新，样本效率大幅提升。

## 关键数字

| 量 | 典型值 |
|---|---|
| clip 阈值 $\varepsilon$ | 0.2（区间 0.8–1.2） |
| 每 batch 的 epoch 数 | 3–4 |
| minibatch 大小 | 总 batch 的 1/4–1/64 |
| 第 1 个 minibatch 的 $r_t$ | 精确等于 1 |

## 可迁移

- 调 PPO/GRPO 类训练时可监控 $r_t$ 的分布与 clip 比例：clip 比例过高说明 epoch 太多或学习率太大，有效梯度在流失。
- 面试被问「PPO 为什么是 on-policy 还能复用数据」，标准答法是「第一个 minibatch 真 on-policy，后续靠 clip 兜底的 mild off-policy」。

## 疑问 / 下一步

- GRPO 等变体里 epoch 数与 clip 比例的经验法则是否与 PPO 一致，值得在自己训练里实测对照。
