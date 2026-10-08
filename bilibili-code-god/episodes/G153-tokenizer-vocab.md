# G153 — tokenizer 词表设计：vocab size、中英混合与 Byte-level BPE

> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G153-tokenizer-vocab.html

## 元信息

- 编号：G153
- 标题：tokenizer 词表设计：vocab size、中英混合与 Byte-level BPE
- BV：BV1BPbE6WELv
- 时长：03:18
- 发布日期：2026-09-11
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：未标注（提及 LLaMA、GPT-2/GPT-4、LLaMA 3 的 tokenizer 实践）

## 一句话总结

词表大小是在序列长度与参数量之间做交易：太小则序列变长、attention 计算量翻倍，太大则 embedding 参数膨胀且低频 token 训练不充分；中英混合还要额外保证中文压缩率，Byte-level BPE 解决未登录词已是主流标配。

## 核心

1. **问题/背景**：训大模型的第一步不是写训练代码而是设计 tokenizer。词表太小，常用词被拆成多个 token，序列变长，训练推理都慢；词表太大，embedding 层参数按 $vocab \times hidden$ 膨胀，且低频 token 训练不充分反而有害。
2. **机制/方法**：中英混合是中文模型的特有挑战：英文 BPE 自然分词没问题，中文若直接 BPE 而不处理，一个汉字可能被拆成几个 byte token，极度浪费。两种方案：按字分词（每汉字一个 token，简单直接，但词表需 6000 以上覆盖常用字）；或中文也用 BPE 但在中文语料上单独训练，让常用词组（如「机器学习」）合成一个 token，LLaMA 3 走的是后者。Byte-level BPE 是解决 OOV 的终极方案：先把文本转成 UTF-8 字节序列再做 BPE merge，任何字符都能表示、不会出现未知 token，GPT-2、GPT-4 都采用，代价是词表大小固定为 256 的倍数。
3. **关键证据或数字**：参考词表规模：LLaMA 32K、GPT-2 50257、中文模型常用 65K 甚至更大；中文在 32K 词表下平均一个字约 1.5 个 token。从零训练流程：准备至少几 GB 代表性语料 → 选 SentencePiece 或 HuggingFace tokenizers → 设 vocab（英文 32K 起步、中文 65K 起步）→ 训练 BPE merge 规则 → 验证常用词 token 数、压缩率与覆盖率。
4. **结论/判断**：最容易踩的坑是 tokenizer 训练语料与预训练语料分布不一致：tokenizer 在英文为主的数据上训练、模型却主要处理中文，token 效率会很低（一个汉字三四个 token）；LLaMA 3 的 tokenizer 就因中文训练不充分导致中文 token 效率明显低于预期。正确做法是让 tokenizer 语料的语言分布与预训练语料一致。

## 关键数字

| 项 | 数值 |
| --- | --- |
| LLaMA / GPT-2 词表 | 32K / 50257 |
| 中文模型词表起点 | 约 65K |
| 中文在 32K 词表下 | 平均约 1.5 token/字 |

## 可迁移

- 评估一个模型的中文能力成本时先看其 tokenizer 的中文压缩率：同样的上下文窗口，压缩率差意味着有效容量差。
- 做中英混合 SFT 数据时，token 效率差异会影响 packing 与长度分布，配比计算要按 token 而非按条数。

## 疑问 / 下一步

- 视频未给词表大小与模型规模的配比经验公式（如 vocab 随参数量如何缩放），可另查相关 scaling 讨论。
