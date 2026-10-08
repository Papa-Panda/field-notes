# G330 — Adam 统治 10 年，三个新挑战者正在分庭抗礼——Lion/Sophia/Adafactor 讲透
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G330-adam-challengers.html

## 元信息
- 编号：G330
- 标题：Adam 统治 10 年，三个新挑战者正在分庭抗礼——Lion/Sophia/Adafactor 讲透
- BV：BV1F13R6nEAV
- 时长：03:54
- 发布日期：2026-08-06
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：AdamW、Lion（Google 2023）、Sophia（Stanford 2023）、Adafactor（Google 2018）、PaLM 2、T5

## 一句话总结
Lion、Sophia、Adafactor 不是要取代 AdamW，而是在不同约束下的更优解：Lion 用符号函数砍掉二阶动量省显存，Sophia 用对角 Hessian 近似换收敛速度，Adafactor 把二阶矩低秩分解把显存降一个数量级。

## 核心
1. **问题/背景**：AdamW 要为每个参数存一阶、二阶两份状态，显存与自适应细粒度在大模型时代成为负担，三个挑战者分别从"更简、更准、更省"三个方向切入。
2. **机制/方法**：Lion 认为 Adam 的 $m / \sqrt{v}$ 本质是方向归一化，干脆把更新量改成动量的符号函数，只存一份动量、每步步长一致，超参更少更鲁棒，代价是失去逐参数自适应粒度。Sophia 反其道而行，只算 Hessian 的对角元（忽略参数间耦合）再加 EMA 平滑，以略高于 Adam 的计算量拿到曲率信息。Adafactor 观察到二阶矩矩阵近似低秩，把它分解成行向量与列向量的外积，显存从 $N^2$ 量级降到 $2N$ 量级，并配合相对步长省掉全局学习率，代价是低秩近似损失一点精度。
3. **关键证据或数字**：显存上 Lion 只存一份动量、约为 AdamW 的一半，Sophia 约两份，Adafactor 最低；速度上 Sophia 在部分语言模型任务上收敛约为 Adam 的两倍，Lion 在大批量下与 Adam 持平；实际采用上 PaLM 2 用 Lion、T5 用 Adafactor。
4. **结论/判断**：选型经验法则——大模型预训练、批量大且显存紧选 Lion；中等模型精调、想要更快收敛选 Sophia；显存极度受限选 Adafactor；AdamW 仍是默认起点，但不再是唯一答案。

## 可迁移
- 估算训练显存时按优化器状态份数分别核算（AdamW 两份、Lion 一份），这是显存预算里最容易漏的一项。
- 面试答优化器选型时用"约束驱动"框架：先说清当前瓶颈是显存、速度还是调参成本，再对应到三者的设计哲学。

## 疑问 / 下一步
- Sophia 的对角 Hessian 估计在超大模型与 RL 训练（梯度噪声更大）场景下是否稳定，视频未涉及，可查原文的规模实验。
