# G504 — 内存墙 Memory-Bound 到底是什么？H100 算力利用率不足 1% 的真相

> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G504-memory-wall.html

## 元信息

- 编号：G504
- 标题：内存墙 Memory-Bound 到底是什么？H100 算力利用率不足 1% 的真相
- BV：BV1euTj6dEqX
- 时长：03:28
- 发布日期：2026-07-03
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：Roofline 模型；FlashAttention、PagedAttention、投机解码（均为破墙手段）

## 一句话总结

Decode 阶段每生成一个 token 都要把全部权重从 HBM 搬一遍，算术强度只有约 2、远低于 H100 的分水岭 295，生成速度上限由「带宽 ÷ 模型体积」决定，与算力无关。

## 核心

1. **问题/背景**：H100 有近千万亿次每秒的算力，跑推理时却 99% 在闲置——瓶颈不在「算」，在「搬」。自回归生成一次只吐一个 token，每吐一个字就要把模型全部参数从 HBM 搬进计算核心完整跑一遍。
2. **机制/方法**：用 Roofline 模型判定：横轴是算术强度（每搬 1 字节做多少次计算），纵轴是实际性能；斜坡段被带宽封顶、平台段被算力封顶，交点（ridge point）是分水岭。逐 token 解码的强度只有个位数，被死死钉在斜坡最左端，属 memory-bound，此时堆算力毫无用处。破墙只有两条思路：一趟多算（批处理把强度乘上 batch size、投机解码一次验证一串 token），或少搬（量化压缩权重体积、GQA 与 PagedAttention 省 KV Cache 搬运、FlashAttention 减少显存读写）。
3. **关键证据或数字**：见下表。另一重背景是剪刀差：过去 20 年芯片算力约每两年翻 3 倍，显存带宽每两年只长约 1.6 倍，内存墙是硬件演进的必然，不是一代产品的意外。
4. **结论/判断**：推理的快慢看的不是你多能算，而是你多能搬；单请求生成速度上限 = 带宽 ÷ 模型体积，这个数在买卡、选模型尺寸、定量化方案时可以直接手算。

## 关键数字

| 量 | 数值 |
| --- | --- |
| H100 算力 / 带宽 | 约 989 TFLOPS / 3.35 TB/s |
| 分水岭（ridge point） | 约 295 次计算/字节 |
| 逐 token 解码的算术强度 | 约 2 |
| 算力利用率 | 不足 1% |
| 7B 模型 FP16 权重 | 14 GB |
| 7B 单请求生成速度上限 | 约 239 token/s（3.35 TB/s ÷ 14 GB） |
| INT4 量化后权重 | 约 3.5 GB（上限随之约 ×4） |

## 可迁移

- 做 RL rollout / 推理服务容量估算时，先用「带宽 ÷ 模型体积」算单请求 token 速率上限，再谈 batch 与并发——这是 rollout 吞吐的第一性估算式。
- 面试讲推理优化时按 Roofline 组织答案：所有主流手段（continuous batching、量化、FlashAttention、PagedAttention、投机解码）本质都是在爬带宽斜坡，分两类讲不会乱。

## 疑问 / 下一步

- Prefill 阶段是 compute-bound、decode 是 memory-bound，混合调度（如 chunked prefill）如何在这条屋顶线两侧找平衡，值得单独看 vLLM/SGLang 的实现。
