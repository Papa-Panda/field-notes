# G470 — 推理过程中的 KV Cache 怎么估算？从原理到 Qwen/DeepSeek 实算
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G470-kv-cache-estimate.html

## 元信息

- 编号：G470
- 标题：推理过程中的 KV Cache 怎么估算？从原理到 Qwen/DeepSeek 实算
- BV：BV1KTMW6NE9t
- 时长：04:55
- 发布日期：2026-07-10
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：Qwen 30B、DeepSeek V3（MLA），字幕举例

## 一句话总结

KV Cache 用显存换计算：每 token 占用 = 2 × 层数 × KV 头数 × 头维度 × 字节数，随上下文线性增长，往往才是长上下文高并发下真正的显存瓶颈。

## 核心

1. **问题/背景**：自回归生成时，每出一个新 token 都要拿它的 query 与全部历史 token 的 key/value 算注意力；若每步重算历史 KV，序列越长重复劳动越多。KV Cache 把每个 token 的 K、V 在首次出现时算好存下，后续只算新 token 自己的 QKV。只存 K、V 不存 Q，是因为历史 token 的 query 用完即弃。
2. **机制/方法**：单 token 的 KV 占用由五项联乘：K 和 V 两份 × 层数 $L$ × 每层 KV 头数 × 头维度 × 每元素字节数（如 BF16 为 2 字节）。注意现在主流是 GQA——多个 query 头共享一组 KV 头，公式里乘的是较少的 KV 头数，这本身就是省显存设计。

$$ \text{每 token KV 字节} = 2 \times L \times \text{KV 头数} \times \text{头维度} \times \text{字节数} $$

3. **关键证据或数字**：以 Qwen 30B 实算：48 层、GQA 只有 4 个 KV 头、头维度 128、BF16，得 $2 \times 48 \times 4 \times 128 \times 2 = 98304$ 字节 ≈ 96 KB/token；16K 上下文一条请求即约 1.5 GB。部署账：两张 A100 80 GB 共 160 GB，30B 权重 BF16 约 60 GB（张量并行每卡 30 GB），剩约 100 GB 给 KV Cache，理论可放 60 多条 16K 请求，生产留余量一般设 32–48 条并发；上下文砍到 8K 则每条占用减半、并发翻倍，共享系统提示词还能用前缀缓存只存一份。
4. **结论/判断**：架构演进就是一路压 KV：MHA 每 query 头配独立 KV 最费 → GQA 共享 KV 头砍掉一大半 → DeepSeek 的 MLA 干脆把 KV 压成一个低维向量存、用时再解压，V3 每 token 只需约 35 KB，同等显存能装下多得多的上下文与并发。

## 关键数字

| 项目 | MHA/GQA 例（Qwen 30B） | MLA（DeepSeek V3） |
| --- | --- | --- |
| 每 token KV 占用 | 约 96 KB | 约 35 KB |
| 16K 上下文单请求 | 约 1.5 GB | — |

## 可迁移

- RL rollout / 推理服务做容量规划时，先算单 token KV 字节，再用「总显存 − 权重」反推并发上限，这是估批大小和上下文长度的标准动作。
- 面试被问「怎么提升并发」可按序答：缩上下文、GQA/MLA、KV 量化、共享前缀缓存。

## 疑问 / 下一步

- MLA 的低秩压缩与解压细节、以及 KV 量化对精度的影响，本篇只给了量级对比，未展开。
