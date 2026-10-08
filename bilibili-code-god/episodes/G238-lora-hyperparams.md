# G238 — LoRA 超参调优：rank、alpha、target modules 与学习率怎么设

> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G238-lora-hyperparams.html

## 元信息

- 编号：G238
- 标题：LoRA 超参调优：rank、alpha、target modules 与学习率怎么设
- BV：BV1VY826wEd2
- 时长：02:30
- 发布日期：2026-08-28
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：LoRA、DoRA、PiSSA、LoRA-GA

## 一句话总结

LoRA 效果不好先别换模型：rank 定表达上限、alpha 按两倍 rank 设缩放、target modules 必须带上 FFN、学习率比全参高 5–10 倍，这四处是最常见的翻车点。

## 核心

1. **问题/背景**：LoRA 在冻结权重旁插入低秩增量 $\Delta W = BA$ ，实际更新量还要乘缩放系数 ， $\alpha / r$ ，。效果上限由 rank、alpha、挂载位置和学习率四个超参共同决定，任何一个设错都会让微调「像没训一样」。
2. **机制/方法**：逐项给经验值。rank 决定低秩增量能表达多复杂的变化：太小学不动复杂任务，太大则参数变多、训练变慢。alpha 控制增量幅度，常用 ， $\alpha = 2r$ ，使缩放比为 2；alpha 太小等于把增量压没。target modules 决定 LoRA 挂在哪些矩阵上——只挂 attention 是常见误区。学习率因为可训参数少、梯度信号集中，要比全参微调明显调高。
3. **关键证据或数字**：rank 经验区间——简单任务 8–16，代码/数学 32–64，需要大幅改变模型行为时 64 以上。全参微调学习率量级约 $1 \times 10^{-5}$ 到 $5 \times 10^{-5}$ ，LoRA 常用 $1 \times 10^{-4}$ 到 $5 \times 10^{-4}$ ，高约 5–10 倍；学习率太低是 LoRA 效果差的高频原因。
4. **结论/判断**：推荐配置是 attention 的 Q、K、V、O 加上 FFN 的 gate、up、down 全部挂载——FFN 才是参数量与知识存储的大头，只挂 attention 会把效果上限锁死。若超参都调对仍不够，再考虑 DoRA（把权重拆成方向与幅度分别学）、PiSSA（主成分初始化，收敛更快）、LoRA-GA（梯度对齐初始化，效果逼近全参）等改进，成本增幅不大。

## 关键数字

| 超参 | 经验设置 |
|---|---|
| rank ， $r$ ， | 简单任务 8–16；代码/数学 32–64；大改行为 64+ |
| alpha ， $\alpha$ ， | ， $\alpha = 2r$ ，（缩放比 ， $\alpha / r = 2$ ，） |
| target modules | attention 的 QKVO + FFN 的 gate/up/down 全挂 |
| 学习率 | $1 \times 10^{-4}$ – $5 \times 10^{-4}$ ，约为全参的 5–10 倍 |

## 可迁移

- 自己跑 LoRA SFT 时先按这张表起步：全挂模块、 $\alpha = 2r$ 、学习率从 $1 \times 10^{-4}$ 试，效果不好按 rank → 学习率 → 模块顺序逐个排查。
- 面试聊 LoRA 调参，能点出「只挂 Q/V 漏掉 FFN」和「学习率要比全参高一个量级」这两条，是实操经验的标志。

## 疑问 / 下一步

- rank 与任务难度的对应关系目前主要是经验值，有没有按目标任务梯度谱分布自动定 rank 的系统方法，值得再查。
