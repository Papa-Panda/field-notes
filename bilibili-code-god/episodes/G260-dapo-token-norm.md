# G260 — DAPO：通过 token 级归一化改进 GRPO 长答案被稀释的问题

> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G260-dapo-token-norm.html

## 元信息

- 编号：G260
- 标题：DAPO：通过 token 级归一化改进 GRPO 长答案被稀释的问题
- BV：BV1Ff8265E3j
- 时长：02:31
- 发布日期：2026-08-24
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：DAPO（An Open-Source LLM Reinforcement Learning System at Scale）、GRPO

## 一句话总结

GRPO 的两级平均让每条序列等权、长答案的 token 被系统性稀释；DAPO 改成除以全组总 token 数，让每个 token 等权、长推理链拿到与长度成正比的梯度信号。

## 核心

1. **问题/背景**：同一道题采样出的多条回答长短悬殊（几个 token 到几十个 token），而长答案恰恰承载着长链推理这种关键能力，却在 GRPO 下学得最慢。
2. **机制/方法**：GRPO 先在序列内对 token 损失取平均（除以该序列长度），再在组内对序列取平均（除以组大小 $G$ ），结果每条序列权重恒为 $1/G$ ，与长度无关。DAPO 取消两级平均：把全组所有 token 的损失直接相加，除以全组总 token 数。
3. **关键证据或数字**：在 GRPO 下，一条 10 token 答案中每个 token 的权重只有 3 token 短答案的约三分之一；换成 token 级归一化后，序列权重正比于其 token 数，短答案占 3 份、长答案占 10 份。
4. **结论/判断**：本质是从「序列级归一化」换成「token 级归一化」——每个 token 公平发声，长答案不再被短答案主导的梯度埋没。

## 关键数字

| 项 | GRPO | DAPO |
|---|---|---|
| 归一化分母 | 先除序列长度、再除组大小 $G$ | 全组总 token 数 |
| 每条序列权重 | 恒为 $1/G$ ，与长度无关 | 正比于 token 数 |
| 单 token 权重（10 token vs 3 token 答案） | 长答案约为短答案的 1/3 | 完全相等 |

## 可迁移

- 写 GRPO 类 loss 时先问一句：归一化分母是序列数还是 token 数？这一个除法决定了长 CoT 样本在梯度里的实际话语权，框架默认实现（如 token-mean vs seq-mean）要逐项核对。
- 面试被问 GRPO 的已知缺陷时，「长答案稀释」是标准答案之一，且能顺势引出 DAPO 的 token-level loss 与动态采样一整套改法。

## 疑问 / 下一步

- token 级归一化让长错答也拿到更大权重，负样本侧是否需要配合 clip 或过滤？可结合 DAPO 的 clip-higher 与动态采样一起看。
