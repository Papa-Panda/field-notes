# G235 — 大模型学习率怎么选？LR Range Test、warmup 与 cosine decay 实操

> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G235-lr-selection.html

> ⚠️ 还原版：本期字幕经多轮尝试未能取得，本纪要依据标题主题与公开论文/资料整理，非视频逐字内容；视频特有表述与数字未收录。

## 元信息

- 编号：G235
- 标题：大模型学习率怎么选？LR Range Test、warmup 与 cosine decay 实操
- BV：BV13i826FEjB
- 时长：02:25
- 发布日期：2026-08-28
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：Cyclical Learning Rates / LR Range Test（Smith, 2015, arXiv:1506.01186）；Adam（Kingma & Ba, 2015）；SGDR 余弦退火（Loshchilov & Hutter, 2017）；GPT-3 / LLaMA 训练配置中的 warmup + cosine 惯例；µP（Yang et al.）

## 一句话总结

学习率没有万能数值，但有一套可复制的实操：先用 LR Range Test 让学习率指数增长、看 loss 从陡降到发散的拐点定峰值量级，再用短 warmup 熬过训练初期的不稳定，最后用 cosine 把学习率衰减到峰值的约十分之一收尾。

## 核心

1. **问题/背景**：学习率是训练最敏感的超参：太小收敛慢且易陷差的极小值，太大直接震荡发散。且最优值随模型规模、batch size、优化器漂移，抄别人的数值往往失效，需要低成本的自测方法。

2. **机制/方法**：LR Range Test（Smith 2015）：从极小学习率起步，让它随 step 指数增长，记录 loss 曲线——loss 先平、后陡降、再到最低点后回升发散；峰值学习率一般取陡降区间内、最低点之前约一个数量级内偏保守的值（常见取法为最速下降段中点附近，或发散点除以 10 左右）。Warmup：训练最初若干步把学习率从 0 线性抬到峰值，因为初期 Adam 的二阶矩估计样本太少、方差大，加上权重随机初始时梯度方向不可靠，直接上大 LR 易把模型打崩；大模型预训练常用数百到数千步 warmup（GPT-3 约前 3.75 亿 token 线性升温）。衰减段：cosine decay 平滑降到峰值的约 10% 附近（LLaMA 等配置衰减到峰值 10% 是常见口径），末期小 LR 做精细收敛。

3. **关键证据或数字**：经验规律方面，临界 batch size 之内，batch 翻倍时峰值 LR 大致可同步放大（线性缩放律对 SGD 成立，Adam 下更接近平方根缩放，需实测）；模型越大最优峰值 LR 越小，GPT-3 从小模型到 175B，峰值 LR 从约 $6 \times 10^{-4}$ 量级降到 $3 \times 10^{-4}$ 量级（175B 取 $3.0 \times 10^{-4}$ ）；µP 的主张则是固定宽度无关的超参迁移：小模型调好的 LR 可直接迁移到大模型。

4. **结论/判断**：实操顺序是「range test 定量级 → warmup 保命 → cosine 收尾」，且任何一条经验规律（缩放律、终点 10%）都只是先验，新规模、新架构下仍要用小规模实验复核再放大。

## 可迁移

- 自己的 post-training 实验（SFT/GRPO）起步时，先花几十步跑一次 mini range test 再定峰值 LR，比抄论文数值稳妥；SFT 常用峰值量级在 $1 \times 10^{-5}$ 到 $2 \times 10^{-5}$ ，与预训练差一个数量级以上，不要混用。
- 面试可迁移点：能完整说出 range test 的曲线判读、warmup 的两个理由（优化器矩估计未热、初始梯度不可靠）、cosine 终点取峰值约 10%，是训练实操题的标准答法。

## 疑问 / 下一步

- RL 阶段（如 GRPO）的 LR 规律与 SFT 差异很大（通常再低 1–2 个数量级且常配常数 LR 而非 cosine），其 range test 判据是否仍适用，公开讨论较少，值得单独整理。
