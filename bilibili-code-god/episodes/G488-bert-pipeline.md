# G488 — 请介绍 BERT 的流程：五大部件 + 预训练全讲透
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G488-bert-pipeline.html

## 元信息

- 编号：G488
- 标题：请介绍 BERT 的流程：五大部件 + 预训练全讲透
- BV：BV1SGMt67EEq
- 时长：02:45
- 发布日期：2026-07-07
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：BERT（Devlin et al., 2018）

## 一句话总结

BERT 是双向 Encoder 的堆叠：三嵌入相加进料、多头自注意力 + FFN 逐层加深理解，靠 MLM 与 NSP 预训练、接任务头微调收尾。

## 核心

1. **问题/背景**：面试高频题——一句话输入 BERT 后，中间到底发生了什么、它如何学会语言理解。
2. **机制/方法**：输入先拼成特殊格式（开头 [CLS]、句间与结尾 [SEP]），再过五大部件。部件一是 Embedding 层：每个词的向量 = token embedding + segment embedding（区分句子 A/B）+ position embedding（可学习位置向量）三者相加。其余四部件组成一个 Encoder 层并反复堆叠：多头自注意力（双向，每个词同时看左右全部上下文）、残差连接 + LayerNorm、前馈网络（两层全连接提供非线性）、再一次残差 + LayerNorm。BERT-Base 共堆 12 层，末端每个位置输出融合全文语义的向量，[CLS] 位置的输出通常代表整句。
3. **关键证据或数字**：预训练两任务——MLM 随机遮住 15% 的词让模型据上下文猜词；NSP 判断两句是否相邻。微调只需在预训练模型上接一个小任务头、用少量标注数据训练（如用 [CLS] 向量做文本分类）。
4. **结论/判断**：记住一条数据流即可复述全流程：拼接特殊标记 → 三嵌入相加 → 12 层 Encoder → [CLS] 表征；训练范式是「预训练打底、微调收尾」。

## 可迁移

- 对照 Decoder-only 模型答题：BERT 的双向注意力使其主攻理解类任务，与 GPT 的因果掩码形成分水岭，这是 encoder-only / decoder-only 选型题的标准切入点。
- 三嵌入相加与残差 + LayerNorm 的位置是手撕 Transformer 代码时的易错点，面试前值得默写一遍数据流。

## 疑问 / 下一步

- NSP 后来在 RoBERTa 等工作中被证明收益有限甚至被移除，追问时需知道这一后续演进。
