# G463 — Encoder-Only 和 Decoder-Only 建模有何区别？BERT 与 GPT 的分水岭

> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G463-encoder-vs-decoder-only.html

> ⚠️ 还原版：本期字幕经多轮尝试未能取得，本纪要依据标题主题与公开论文/资料整理，非视频逐字内容；视频特有表述与数字未收录。

## 元信息

- 编号：G463
- 标题：Encoder-Only 和 Decoder-Only 建模有何区别？BERT 与 GPT 的分水岭
- BV：BV1HLNA6tEX9
- 时长：02:41
- 发布日期：2026-07-11
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：Transformer（Vaswani et al., 2017）；BERT（Devlin et al., 2019）；GPT / GPT-2 / GPT-3（Radford et al., 2018–2020）

## 一句话总结

Encoder-only 与 decoder-only 的分水岭在注意力可见性与预训练目标：BERT 用双向自注意力 + 掩码语言模型把每个词的表示建立在全文之上，天生为理解而生；GPT 用因果掩码 + 自回归语言模型只看左侧，天生为生成而生——而统一、自回归、无标注数据的规模化能力，最终让 decoder-only 赢下了大模型时代。

## 核心

1. **问题/背景**：同为 Transformer 堆叠，为什么 NLP 在 2018 年分叉出 BERT 与 GPT 两条路线，此后又几乎全面倒向 decoder-only？这是理解架构选型的经典面试题。

2. **机制/方法**：差别在三处。①注意力可见性：encoder 的自注意力无掩码，每个位置能看全序列（双向）；decoder 的自注意力带因果掩码（上三角屏蔽），位置 $t$ 只能看 $t$ 及其之前的 token。②预训练目标：BERT 是 MLM，随机遮住约 15% 的 token 让模型用双向上下文恢复，外加 NSP 句间任务；GPT 是标准 LM，把整句概率分解为逐词条件概率之积做 next-token 预测：

$$P(x) = \prod_{t} P(x_t \mid x_{<t})$$

③下游用法：BERT 预训练后接任务头做微调（分类、抽取、序列标注），一个模型一个任务；GPT 靠 prompt / few-shot 把任务统一成续写，一个模型通吃，扩展到 GPT-3 后 in-context learning 成为主流范式。

3. **关键证据或数字**：BERT-base 为 12 层、约 1.1 亿参数，发布时在 GLUE 等 11 项理解任务上刷新纪录，确立「预训练 + 微调」范式；GPT-3 则以 1750 亿参数证明 decoder-only 的自回归目标能随规模持续扩展，并以 few-shot 方式免微调完成多类任务。两条路线的此消彼长，本质是「双向理解的精度优势」输给了「自回归目标的规模化与任务统一优势」。

4. **结论/判断**：生成即一切的时代，decoder-only 胜在三点：训练目标与推理方式完全一致（无 MLM 式预训练—应用落差）、每个 token 都有监督信号（ MLM 只有被遮的约 15% 有 loss ）、可用 KV Cache 高效自回归推理。Encoder-only 并未消失：嵌入、检索、重排序、分类等纯理解场景仍是它的主场，现代系统常是「decoder-only 生成 + encoder-only 检索」的混合体。

## 可迁移

- 选型判断：需要生成或统一多任务接口选 decoder-only；只需要高质量向量表示（检索、聚类、分类）选 encoder-only，后者参数小、推理便宜且表示质量不输。
- 面试可迁移点：回答此题要落到三个机制差异（掩码、目标、监督密度）与一个工程点（KV Cache），只背「BERT 做理解、GPT 做生成」的结论句拿不到高分。

## 疑问 / 下一步

- 双向注意力在生成模型中的价值被重新挖掘（如扩散语言模型、带双向编码的混合架构），decoder-only 的一统地位是否会在非自回归生成路线上松动，值得持续跟踪。
