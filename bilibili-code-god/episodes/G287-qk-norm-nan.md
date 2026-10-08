# G287 — 大模型训练为何突然 NaN？QK-Norm 两行代码治好注意力 logit 爆炸

> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G287-qk-norm-nan.html

## 元信息

- 编号：G287
- 标题：大模型训练为何突然 NaN？QK-Norm 两行代码治好注意力 logit 爆炸
- BV：BV1UUua6wEVU
- 时长：03:11
- 发布日期：2026-08-17
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：QK-Norm（Qwen3、Llama 4 等现代模型采用）

## 一句话总结

训练中 attention logit 爆炸的根源是 query/key 向量模长随训练失控增长，在点积前给 Q、K 各做一次 RMSNorm 即可把 logit 锁回可控范围，成本几乎为零。

## 核心

1. 问题/背景：大模型训练跑着跑着 loss 冒出尖峰甚至直接 NaN，凶手常在注意力内部——logit 爆炸。
2. 机制/方法：注意力分数由 Q、K 点积再除以 ， $\sqrt{d}$ ，得到；模型为了让注意力更集中，最省事的路径是把 Q、K 的模长撑大，而点积正比于两模长之积，于是 logit 水涨船高，实测可飙到 5 万以上。一旦某个 logit 大得离谱，softmax 尖成一根针，权重几乎全压给单个 token，梯度剧烈震荡，训练发散。QK-Norm 的做法是在点积之前先对 Q、K 分别做 RMSNorm，按均方根把模长拉回可控范围，点积自然稳定。
3. 关键证据或数字：不加 QK-Norm 时 loss 曲线时不时窜尖峰、一言不合就发散；加上后曲线平顺下降，有实验显示学习率横跨三个数量级仍能稳定训练。
4. 结论/判断：QK-Norm 只作用于 Q、K 两个向量、不碰注意力其他部分，多出的计算量可忽略，却已成现代大模型的标配稳定件。

## 可迁移

- 排障顺序：loss 尖峰/NaN 先怀疑 logit 尺度，再查学习率与数据；监控 Q、K 模长和 logit 最大值是便宜的早期预警。
- 面试答法：把「模长增长 → 点积放大 → softmax 饱和 → 梯度震荡」这条因果链讲清，比只背「加个 norm」高一个层次。

## 疑问 / 下一步

QK-Norm 与 logit soft-capping（如 Gemma 2 早期方案）在大 batch、高学习率下谁更稳，值得找消融对比。
