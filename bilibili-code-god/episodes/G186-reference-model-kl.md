# G186 — reference model 为什么不能丢？KL 约束的数学体现
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G186-reference-model-kl.html

## 元信息

- 编号：G186
- 标题：reference model 为什么不能丢？KL 约束的数学体现
- BV：BV1uN8t6zEwx
- 时长：02:48
- 发布日期：2026-09-06
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：DPO（Direct Preference Optimization）、SimPO、RLHF 的 KL 约束目标

## 一句话总结

Reference model 是 DPO 的安全带：它把 RLHF 的 KL 约束写进损失函数，去掉它策略可以靠整体压低概率钻空子，最终漂移崩塌。

## 核心

1. **问题/背景**：DPO 训练需要两个模型——更新的策略模型与冻结的 reference model，后者占一份显存却不更新参数，看似累赘，问题是能否去掉。
2. **机制/方法**：DPO 损失由四项 log 概率构成，策略与 reference 各贡献对 chosen 与 rejected 的两项，reference 提供固定基准，策略的改进是相对它衡量的。数学上 DPO 由带 KL 约束的 RLHF 目标推导而来，reference 的 log 概率正是 KL 约束的体现。没有这个锚，损失退化为直接拉大 chosen 与 rejected 的概率差，策略可以通过把所有输出概率整体降低（只要 chosen 降得比重 rejected 少）来「完成任务」。
3. **关键证据或数字**：去掉 KL 保护的后果是策略随意漂移、语言崩塌输出乱码。免 reference 的变体 SimPO 用 chosen 与 rejected 的（长度归一化）log 概率差直接作信号，省掉一份模型显存、训练更快，但失去了 KL 保护，必须靠更精细的超参调优防漂移。工程上 reference 一般用 SFT 后的 checkpoint 初始化、冻结只做前向，显存紧张时可 offload 到 CPU（代价是算 log 概率变慢）。
4. **结论/判断**：资源够用标准 DPO 带 reference 更稳；资源紧可用 SimPO，但要把防漂移的调参成本算进去。

## 关键数字

| 项 | 说明 |
|---|---|
| 损失构成 | 4 项 log 概率，策略与 reference 各半 |
| Reference 成本 | 一份模型显存 + 前向计算 |
| 免 reference 变体 | SimPO，省显存但需更细调参 |

## 可迁移

- 理解任何偏好优化变体时先问一句「KL 锚还在不在、换成了什么」，能快速定位 SimPO、KTO 等方法的风险点。
- RL infra 排障时若 DPO/GRPO 出现输出退化，先查约束项是否被实现细节（offload、截断）悄悄削弱。

## 疑问 / 下一步

- SimPO 的长度归一化在长 CoT 场景下是否会引入新的长度偏置，值得找其消融实验细看。
