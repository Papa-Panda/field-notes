# G225 — Prefill 与 Decode 为什么差 140 倍？PD 分离架构的由来
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G225-pd-separation.html

## 元信息

- 编号：G225
- 标题：Prefill 与 Decode 为什么差 140 倍？PD 分离架构的由来
- BV：BV1Xj8S6zEe1
- 时长：03:37
- 发布日期：2026-08-30
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：PD 分离（Prefill-Decode Disaggregation）、Mooncake（Kimi）、DeepSeek 部署实践

## 一句话总结

Prefill 一次性并行处理全部输入 token、是计算密集型；Decode 逐 token 串行生成、每步都要搬一遍全量权重、是访存密集型——两者吞吐差约 140 倍且资源需求相反，挤在同一 GPU 上互相打架，于是有了把两阶段拆到不同 GPU 池的 PD 分离架构。

## 核心

1. **问题/背景**：同一个模型、同一张卡，读 1000 字 prompt 只要零点几秒，生成回答却要几秒——线上推理的 TTFT 与 TPOT 必须分开优化，根源就在两阶段的瓶颈完全不同。
2. **机制/方法**：Prefill 把整个 prompt 一次灌入，所有 token 并行算 QKV 并生成 KV cache，大块矩阵乘法让 GPU 算力利用率冲到 90% 以上，瓶颈在算力。Decode 每生成一个 token 都要把全量权重从显存搬进计算单元、只产出一个 token 再重复搬运，算力利用率只有百分之十几，瓶颈在显存带宽。
3. **关键证据或数字**：实测 Prefill 每秒可处理的 token 数可达 Decode 的约 140 倍。混跑时 Prefill 嫌算力不够、Decode 嫌带宽不够，谁都跑不满。
4. **结论/判断**：PD 分离把 Prefill 与 Decode 部署到不同 GPU 池：Prefill 池堆算力，Decode 池堆带宽与显存；请求先在 Prefill 池算出 KV cache，再传给 Decode 池续生成。DeepSeek、Kimi（Mooncake）、SGLang 等都在用这套架构，吞吐可翻倍。

## 关键数字

| 对比项 | Prefill | Decode |
|---|---|---|
| 处理方式 | 全部输入 token 并行 | 逐 token 串行 |
| 瓶颈 | 算力（计算密集） | 显存带宽（访存密集） |
| GPU 算力利用率 | 90% 以上 | 10% 出头 |
| 相对吞吐 | 约 140× Decode | 基准 |

## 可迁移

- RL rollout 本质是大量 Decode：推理侧优化（continuous batching、KV cache 管理、PD 分离）对 rollout 吞吐的影响远大于训练侧小修小补，排 RL 训练瓶颈时先看生成段。
- 面试讲推理优化时用"算力 vs 带宽"这条主线串起 TTFT / TPOT、batch size 对两阶段的不同影响，比罗列框架特性更有说服力。

## 疑问 / 下一步

- PD 分离引入 KV cache 跨池传输成本，短 prompt / 低并发场景下分离收益可能被传输开销吃掉，实际选型需要按请求长度分布测算。
