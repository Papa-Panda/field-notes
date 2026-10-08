# G314 — 删掉开头几个 token 大模型当场崩盘？一图看透 Attention Sink 与 StreamingLLM

> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G314-attention-sink.html

## 元信息

- 编号：G314
- 标题：删掉开头几个 token 大模型当场崩盘？一图看透 Attention Sink 与 StreamingLLM
- BV：BV1youa6dEug
- 时长：02:55
- 发布日期：2026-08-10
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：StreamingLLM / Attention Sink（Xiao et al., 2023）

## 一句话总结

开头的几个 token 是 softmax 注意力的「泄压阀」：丢掉它们困惑度瞬间爆涨上千倍；StreamingLLM 永远保留最初 4 个 token 的 KV 再配滑动窗口，长文本既省显存又不崩。

## 核心

1. **问题/背景**：KV cache 随长度线性膨胀，长文本/无限流式对话装不下；最自然的做法是滑动窗口只留最近 token、丢最老的。但实验显示窗口一滑过开头，困惑度不是渐变而是断崖——从 5 点几直接冲到 5000 多。
2. **机制/方法**：softmax 要求注意力权重和为 1，当某一步并没有特别想关注的内容时，多余的注意力必须找地方「倒」，模型自发把开头几个 token 当作倾倒点（attention sink）。注意力热力图上最左一列恒亮与此对应。关键证据：模型看中的是位置而非内容——把开头换成无意义的换行符同样稳，一般保留最前 4 个 token 即可。
3. **关键证据或数字**：丢掉开头 token 后困惑度由约 5.x 飙到 5000+，量级差上千倍；保留 sink + 最近窗口后可稳定处理数百万 token 量级的流式输入。
4. **结论/判断**：KV 驱逐策略不能只按「新旧/内容重要性」排序，位置本身有结构性作用；StreamingLLM 的配方就是 sink token 常驻 + 最近窗口滚动。

## 关键数字

| 操作 | 困惑度变化 |
| --- | --- |
| 保留开头 token | 约 5.x |
| 丢掉开头 token | 5000+（飙升上千倍） |

## 可迁移

- 推理 infra：做 KV cache 压缩/驱逐（如 H2O、SnapKV 一类）时必须给 sink token 留豁免位，否则离线指标再好上线也会崩。
- 面试：这条是「softmax 归一化约束 → 涌现结构」的经典案例，能顺带解释为什么很多模型对 BOS token 有异常大的注意力。

## 疑问 / 下一步

- 不同架构（无 BOS、不同位置编码）下 sink 的强度差异多大？多模态/多轮对话里 sink 位置是否漂移，值得查后续工作。
