# G326 — RM 损失函数为什么用 sigmoid 差值?Pairwise Ranking 讲透
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G326-rm-loss-pairwise.html

## 元信息

- 编号：G326
- 标题：RM 损失函数为什么用 sigmoid 差值?Pairwise Ranking 讲透
- BV：BV1UN3d6iErs
- 时长：04:35
- 发布日期：2026-08-07
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：Bradley-Terry 模型；InstructGPT 的 RM 训练目标

## 一句话总结

RM 损失 $-\log \sigma(r_{\mathrm{chosen}} - r_{\mathrm{rejected}})$ 只约束同一 prompt 内两个回答的相对排序、不约束绝对分数，所以 RM 本质是排序器——跨 prompt 比绝对分数是工程大坑。

## 核心

1. **问题/背景**：为什么不用均方误差让 RM 直接预测一个绝对分数？因为 pairwise ranking 的设计哲学根本不关心分数的绝对值，只关心相对差。均方误差会把模型钉死在具体数值上，而排序损失留了一个「整体平移不变」的自由度：所有分数同时抬高 100，损失一点不变。
2. **机制/方法**：损失函数为：

$$ L = -\log \sigma(r_{\mathrm{chosen}} - r_{\mathrm{rejected}}) $$

   差值很大时 sigmoid 趋近 1、损失趋近 0；差值为 0 时损失为 $\log 2 \approx 0.693$ ；差值为负（排错方向）时损失迅速上升、梯度狠狠推回。这条曲线有界、平滑、可微，且对错误方向的惩罚强于对正确方向的奖励，难分样本自动获得更大梯度。用 sigmoid 的三个理由：处处可导优化稳定；输出在 0 到 1 之间可直接解释为 Bradley-Terry 概率，负 log 即最大似然；渐进饱和让已拉开的样本自动停手。
3. **关键证据或数字**：与分类损失对比最能说明问题：分类是绝对判断（每样本独立打标签），pairwise 是相对判断（二选一谁更好）——而人类标注偏好时本来就不擅长给绝对分（今天给 7 分明天给 8 分），二选一却稳定得多，损失粒度正好匹配人类能稳定给出的信号粒度。关键性质是分数跨 prompt 不可比：同 prompt 内 8.5 vs 3.2（差 5.3）有意义，因为训练时被强制拉开过；跨 prompt 的 9.0 vs 2.0 毫无意义，因为两个回答从未被任何损失同时约束过。
4. **结论/判断**：工程上切忌用 RM 绝对分数评估单个回答；要么在同一 prompt 内做相对比较，要么报告 pair accuracy（chosen 高于 rejected 的比例）。

## 关键数字

| 分数差 Δ | 损失 $-\log \sigma(\Delta)$ |
|---|---|
| 很大（排对且拉开） | 趋近 0 |
| 0（没分开） | $\log 2 \approx 0.693$ |
| 负（排错） | 迅速上升 |

## 可迁移

- 排查 RM 相关 bug 时先问一句「这个比较是同 prompt 内吗」，能挡掉一类常见的评估误用。
- 面试答「RM 损失为什么不用 MSE」：绝对值无约束、平移不变、与 Bradley-Terry 的最大似然等价，三点即可。

## 疑问 / 下一步

- 多回答排序（K>2 的 listwise 扩展，如 Plackett-Luce）相对两两 pairwise 的收益与成本，值得补一篇。
