# G353 — PD 分离部署：Mooncake / DistServe / Splitwise 三家方案讲透
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G353-pd-disaggregation.html

## 元信息
- 编号：G353
- 标题：PD 分离部署：Mooncake / DistServe / Splitwise 三家方案讲透
- BV：BV1J7gR61EgA
- 时长：03:27
- 发布日期：2026-07-29
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：Mooncake（月之暗面）、DistServe、Splitwise

## 一句话总结
PD 分离把 prefill 和 decode 拆到两组物理 GPU 上：算力强的卡专跑 prefill、带宽型的卡专跑 decode，KV cache 经 RDMA 高速搬运，换来独立扩缩容、无阶段间干扰和更高的资源利用率。

## 核心
1. 问题/背景：传统部署让 prefill 与 decode 共用同一组 GPU：一个长 prompt 的 prefill 要算几秒，期间所有在途 decode 请求全被堵住，TTFT 与 ITL 一起抖动——同一台机器既要拉货又要跑赛道，两头都做不好。
2. 机制/方法：按阶段拆集群：prefill 池用 H100/A100 这类算力卡专算 prompt；decode 池用 H20 等带宽/性价比卡专做逐 token 生成。prefill 算出的 KV cache 按层切片，用 RDMA 直达 decode 节点显存，传输延迟要压到几十毫秒级，否则会被吃掉 TTFT 收益。各池按真实负载独立扩缩，再不用一刀切买同一种卡。
3. 关键证据或数字：Mooncake 是月之暗面支撑 Kimi 的生产方案，除 PD 分离外还把 KV cache 做成独立的中心化缓存池、跨请求复用前缀缓存，论文报告吞吐提升约 75%。DistServe 是学术原型，首次系统提出 PD 分离并给出 goodput 优化框架；Splitwise 是微软方案，强调在异构硬件上分工跑两段。
4. 结论/判断：三家共同验证：把两段拆开是 LLM 推理服务的必然方向，前提是 KV cache 的跨机传输与调度足够快、足够便宜。

## 关键数字
| 系统 | 出处 | 特点 |
| --- | --- | --- |
| Mooncake | 月之暗面（Kimi 生产） | PD 分离 + 中心化 KV 缓存池，吞吐约 +75% |
| DistServe | 学术原型 | 首次系统提出 PD 分离与 goodput 框架 |
| Splitwise | 微软 | 异构硬件上的 PD 分工 |
| KV 传输要求 | RDMA 按层切片 | 延迟压到几十 ms 级 |

## 可迁移
- 推理架构面试主线题：从"为什么混跑会抖"讲到"拆开后 KV 怎么搬、怎么扩缩"，能完整覆盖 TTFT/ITL SLO 的讨论。
- 与 G352 的两阶段画像互为表里：先用 roofline 说清瓶颈差异，再谈 PD 分离的部署解法。

## 疑问 / 下一步
- KV cache 跨机传输在长上下文（单请求 KV 达数 GB）时如何不成为新瓶颈，Mooncake 的分层缓存细节值得细读。
