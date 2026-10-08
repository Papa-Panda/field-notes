# G459 — Encoder 和 Decoder 中的 Mask 有什么不同？两层掩码一次讲透
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G459-encoder-decoder-mask.html

## 元信息

- 编号：G459
- 标题：Encoder 和 Decoder 中的 Mask 有什么不同？两层掩码一次讲透
- BV：BV1cENA6xEtb
- 时长：02:57
- 发布日期：2026-07-12
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：Transformer（Attention Is All You Need）、因果掩码（causal mask）

## 一句话总结

两边共用 padding mask 屏蔽凑数的 PAD；decoder 额外多一层 causal mask 用上三角负无穷挡住未来——encoder 屏蔽的是「无意义」，decoder 还要屏蔽「未来」，这正是并行训练与严格自回归能同时成立的原因。

## 核心

### 1. 问题/背景

同是注意力机制，为什么 encoder 一层 mask 就够、decoder 非要两层？答案藏在两者的任务性质里：理解是双向的，生成是单向的。

### 2. 机制/方法

- **Padding mask（两边都有）**：批训练时句子长短不一，短句用 PAD 补齐成矩阵，但 PAD 无意义、被关注会引入噪声。做法是在注意力分数矩阵 $\frac{QK^T}{\sqrt{d}}$ 上，把 PAD 对应列加上负无穷，softmax 后权重近零，模型当它们不存在；
- **Causal mask（只有 decoder）**：decoder 自回归生成，预测第 $i$ 个词只能依据前面已生成的词；但训练时完整答案是一次性喂入并行计算的，有偷看未来的作弊风险。做法是构造上三角为负无穷的掩码（代码里一行 `torch.tril` 即可生成），使每个位置只能看到从开头到自己为止；
- **交叉注意力例外**：完整 encoder-decoder 结构里，decoder 看 encoder 输出的那层交叉注意力只需对源句 PAD 做 padding mask，不需要因果掩码——源句是已知完整信息，可以随便看。

### 3. 关键证据或数字

无实验数字，属机制题：一句话判据是 encoder 双向全可见（适合理解类任务），decoder 单向只看自己与过去（适合生成类任务）。

### 4. 结论/判断

Mask 的本质是在分数矩阵进 softmax 前做加法屏蔽；两种 mask 回答两个不同问题——padding mask 回答「哪些位置不存在」，causal mask 回答「哪些位置现在还不能看」。

## 关键数字

| 结构 | Padding mask | Causal mask | 可见范围 |
|---|---|---|---|
| Encoder 自注意力 | 有 | 无 | 全句有效词（双向） |
| Decoder 自注意力 | 有 | 有 | 自己与此前位置（单向） |
| Decoder 交叉注意力 | 有（对源句） | 无 | 全部源句 |

## 可迁移

- 面试速答模板：「encoder 屏蔽无意义，decoder 多屏蔽未来」；再补一句交叉注意力不需因果掩码，是常被追问的细节分。
- 工程上与 KV cache / 推理实现直接相关：causal mask 在解码期由「只缓存已生成 token」天然实现，训练期的上三角掩码只为并行计算服务。

## 疑问 / 下一步

现代 decoder-only 模型训练普遍用 FlashAttention 的因果模式代替显式掩码矩阵，两者在数值与显存上还有哪些差异，值得结合实现再看一遍。
