# G022 — SFT 一定要 mask 掉 prompt 吗？指令长 5 倍、样本少于 1 万时给 prompt 算 loss 反而涨点
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G022-sft-prompt-mask.html

## 元信息

- 编号：G022
- 标题：SFT 一定要 mask 掉 prompt 吗？指令长 5 倍、样本少于 1 万时给 prompt 算 loss 反而涨点
- BV：BV1UTea64E3a
- 时长：04:06
- 发布日期：2026-10-03
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：Instruction Modelling（NeurIPS 2024）、Weighted Instruction Tuning（TACL 2025）；上一期 G465 讲标准 mask 做法

## 一句话总结

「prompt 不算 loss」只是默认值而非铁律：在指令远长于回答、且样本少于约 1 万的低资源场景，给 prompt 以 0.2–0.5 的权重算 loss 是一种正则化，能显著涨点；样本量一大，收益归零。

## 核心

1. 问题/背景：标准指令微调把样本分三段（模板 token、user 指令、assistant 回答），只对回答段算交叉熵，指令与模板的 label 设为 -100。理由很直觉：要学的是怎么回答，不是怎么提问。但 NeurIPS 2024 的 Instruction Modelling 与 TACL 2025 的加权版本（共 21 个基准、525 次训练）发现，这条默认在特定条件下是错的。
2. 机制/方法：Instruction Modelling 只改一处——指令段也算 loss，模板 token 仍不算。加权版进一步把 prompt 权重与 response 权重拆成两个超参分别扫。代码层面只改一行：labels 里 prompt 段由 -100 改成逐 token 权重向量（模板 0、prompt 约 0.3、response 约 0.8），loss 为加权交叉熵除以权重和。
3. 关键证据或数字：生效需要两个条件同时满足：① 长度比（指令 token 数 ÷ 回答 token 数）大——如 Less/MMLU-Chat 类数据比值 26、Science Literature 24.7，这类收益显著；而 Tulu V2 比值 0.58（回答比指令长），收益很小；② 样本量在 1000–9000 条最好，涨到 3.5 万收益接近零，超过 5 万完全没差别。效果上，Less/MMLU-Chat 的 AlpacaEval 从 4.42 涨到 9.78（翻倍，惟基线很低），Science Literature 低资源下提升超过 18%，NLP 基准平均 46.58 → 48.95。机制证据指向正则化：IM 的训练 loss 更高（1.45 vs 1.37），测试 loss 反而更低（1.17 vs 1.32），生成与训练集的 BLEU 重叠更少——训得「更差」却测得更好、更不像背书；它比 KL 正则更全面（KL 保住 NLP 分数却把指令跟随打到接近 0，IM 两者兼顾）。权重扫描结论：标准做法（0, 1）几乎从不是最优，全算（1, 1）也偏冷；81% 的配置里 prompt 权重落在 0–0.6 为最优区间，56% 的情况下非零 prompt 权重最优，response 权重取 1 在 24% 情况下最优；相对标准做法平均涨 6.55%，Mistral-7B + Alpaca Cleaned 涨 20%。不同基准偏好不同（IFEval 偏好 response 权重 0.43，AlpacaEval 0.64，BBH 的 prompt 权重约 0.17）。另外，用加权 SFT 当 DPO 的起点还能再涨 8%，可与 NEFTune 叠加。
4. 结论/判断：边界要讲清：指令短、回答长或样本超 5 万条时，保持标准 mask 别折腾；无论怎么设，模板 token 永远不算 loss；多轮对话下 prompt 权重如何设，两篇论文都没系统覆盖，不要外推。实操上先算自己数据的长度比与样本量，两个条件都满足再开，且别只看一个基准选权重。

## 关键数字

| 场景 | 基线 → 结果 |
|---|---|
| Less/MMLU-Chat AlpacaEval | 4.42 → 9.78 |
| NLP 基准平均 | 46.58 → 48.95 |
| 训练 / 测试 loss（IM vs 标准） | 1.45 / 1.17 vs 1.37 / 1.32 |
| 相对标准做法平均提升 | +6.55%（Mistral-7B + Alpaca Cleaned +20%） |
| 最优 prompt 权重区间 | 0.2–0.5（response 0.6–1.0，模板恒 0） |

## 可迁移

- 做小样本、长上下文指令的 SFT（如长文档 QA、带大段上下文的分类）时，先算长度比：指令是回答 5 倍以上且样本不足 1 万，默认打开 prompt loss 并扫 0.2–0.5 权重。
- 面试被问「SFT 的 loss 怎么算」，补一句适用条件与正则化机制，能明显拉开与只会背 mask 做法的差距。

## 疑问 / 下一步

- 多轮对话场景下各轮 prompt 的权重如何分配尚无系统结论，自己做多轮 SFT 时需小规模对照实验验证。
