# G514 — 大模型面试：为什么现在的大模型都是Decoder-Only架构？

> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G514-decoder-only.html

## 元信息

- 编号：G514
- 标题：大模型面试：为什么现在的大模型都是Decoder-Only架构？
- BV：BV1uiXmBUEfp
- 时长：03:41
- 发布日期：2026-03-28
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：BERT、T5、GLM；苏剑林关于 encoder 双向注意力低秩问题的论述；Qwen3-Embedding

## 一句话总结

Decoder-only 胜出不是因为单项能力最强，而是 causal 自回归 + 自监督的范式不需要任何人工标注设计、数据可无限扩展；另外两条路线都卡在 scaling 的门槛上。

## 核心

1. **问题/背景**：架构分三家——encoder-only（BERT，做理解）、encoder-decoder（T5、BART，做 seq2seq）、decoder-only（GPT、LLaMA、Qwen，做通用生成）。要回答的是为什么最后一家通吃。
2. **机制/方法**：逐家看淘汰原因。Encoder-only 的 MLM 预训练要人工设计 mask 策略，且预训练与微调之间存在范式 gap，阻碍大规模 scaling；同时 decoder-only 规模上来后表征能力已全面反超（Qwen3-Embedding 只需百 M 级微调就能登顶 MTEB）。Encoder-decoder 有两伤：双向注意力引入特定 mask 模式使注意力矩阵低秩、表达受限（而 causal 掩码矩阵是满秩的；T5 当年看起来好主要是参数量翻倍，并非架构更优），且 prompt 要先过 encoder 再经 cross-attention 传给 decoder，信息损耗使 ICL 明显更弱。同为 decoder-only 还有内部之争：non-causal 的 GLM 范式理论上限更高，但其 mask 需要人工标注介入，无法像 causal 那样靠自监督无限扩数据，GLM 后来也向 causal 靠拢。
3. **关键证据或数字**：字幕以定性论证为主：causal decoder 的胜负手是「训练目标零设计、数据无限扩展」；反直觉的一点是 infra 视角下 decoder-only 并不占优——BERT 训练推理都是计算饱和、infra 统一高效，decoder-only 却是训练 compute-bound、推理 memory-bound，两阶段不统一，这正是当下大量推理优化研究存在的原因。而「decoder-only 有 KV Cache 所以更好」是把因果讲反了：KV Cache 是为缓解自回归冗余计算的补救（以存储换计算），BERT 根本不需要自回归、不存在这个问题。
4. **结论/判断**：胜负不在架构精巧，而在谁的训练范式能无摩擦地吃无限数据——causal 自回归赢在 scaling 的复利。

## 可迁移

- 面试答这道题按「三家逐一淘汰 + 淘汰原因都指向 scaling」的结构讲，最后补 infra 反直觉点（KV Cache 是补救不是优势），能显著区别于背诵型答案。
- 选型时提醒自己：理解类小任务上 encoder 系并未死（如 embedding 榜单），decoder-only 通吃的是通用生成与 ICL 生态，不是所有场景。

## 疑问 / 下一步

- 苏剑林指出的双向注意力低秩问题在现代 encoder-decoder 复兴尝试（如带改进 mask 的方案）里是否已被绕过，值得查一下原文论证。
