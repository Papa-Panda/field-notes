# G351 — RadixAttention：SGLang 的招牌技术，一棵 Radix Tree 让吞吐提升 2-5×
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G351-radix-attention.html

## 元信息
- 编号：G351
- 标题：RadixAttention：SGLang 的招牌技术，一棵 Radix Tree 让吞吐提升 2-5×
- BV：BV1gYgR6vEas
- 时长：04:40
- 发布日期：2026-07-30
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：SGLang / RadixAttention、PagedAttention（vLLM）

## 一句话总结
大量请求共享同一段前缀（system prompt、few-shot、多轮历史），朴素引擎会把同一段 KV cache 重算 N 遍；RadixAttention 用一棵基数树组织 KV，按最长前缀匹配直接复用，命中部分一分算力不花。

## 核心
1. 问题/背景：100 个请求带着同一段 system prompt 进来，没有复用机制时 GPU 就把这段前缀重算 100 遍，算力、延迟、显存（N 份相同的 KV）全浪费在重复劳动上。
2. 机制/方法：基数树（压缩前缀树）的每条边存一段 token 序列，节点代表这段序列的 KV 已算好可复用。新请求从根出发找最长公共前缀，命中的段直接复用，未命中的后缀才做 prefill 并作为新分支挂回树上；显存紧张时按 LRU 淘汰最久未用的叶子，保住最热的公共前缀。示例中 1500 token 只需新算 300，省掉 80% 的 prefill。
3. 关键证据或数字：四大高命中场景——system prompt（几乎 100% 命中）、few-shot（共用示例可省一半以上算力）、多轮对话（每轮只算新增的一两句，命中率随轮次升高）、Tree-of-Thoughts / self-consistency（同一根长出几十条分支共享一份 KV）。SGLang 论文实测在共享前缀多的真实负载下吞吐提升 2–5 倍，首 token 延迟大幅下降。
4. 结论/判断：它与 PagedAttention 解决的是两个正交问题且互补：PagedAttention 管单条请求的 KV 在显存里怎么分页存放，RadixAttention 管多条请求之间怎么共享——一个让你存得下，一个让你算得少，SGLang 两者都做了。

## 关键数字
| 指标 | 数值 |
|---|---|
| 示例 prefill 节省 | 1500 token 只新算 300，省 80% |
| 吞吐提升（论文实测） | 2–5 倍 |

## 可迁移
- 做推理 infra 选型时先看负载的前缀共享程度：Agent / 多轮 / 批量同模板场景下，前缀缓存的收益远大于单请求优化。
- 面试区分 PagedAttention 与 RadixAttention：一句「一个管存储布局，一个管共享逻辑」即可切中要害。

## 疑问 / 下一步
- 前缀树在高并发下动态增长时的碎片与锁竞争如何处理？SGLang 的实现细节值得翻源码确认。
