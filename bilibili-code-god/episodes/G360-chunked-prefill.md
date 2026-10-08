# G360 — Chunked Prefill：8000 token prompt 一进，Decode 集体卡 1 秒？
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G360-chunked-prefill.html

## 元信息
- 编号：G360
- 标题：Chunked Prefill：8000 token prompt 一进，Decode 集体卡 1 秒？
- BV：BV1jWgR6rEK9
- 时长：04:27
- 发布日期：2026-07-27
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：Sarathi-Serve（chunked prefill 出处）；vLLM、SGLang 的默认调度配置

## 一句话总结
把长 prompt 的 prefill 切成小块、与 decode 交错调度，长 prompt 的总算力不变但不再独占 GPU 一整秒，ITL 抖动被抹平。

## 核心
1. **问题/背景**：推理两阶段性质相反——prefill 一次吃下整段 prompt、是 compute-bound；decode 逐 token 生成、是 memory-bound。传统引擎把 prefill 当作不可分割的整体：一条 8192 token 的 prompt 要独占 GPU 约 800ms，期间所有正在 decode 的请求全部停摆，ITL 从正常的约 50ms 飙到 800ms，用户看到的就是聊着聊着集体卡一秒。这是结构问题，不是 bug。
2. **机制/方法**：chunked prefill 把长 prompt 切成若干块（如 8192 切成 4 块 × 2048），每次迭代只算一块 prefill，其余算力留给 decode。总工作量不变，但时间片变细，调度器有了腾挪空间。更关键的是与 continuous batching 配合：每个 iteration 凑 batch 时，decode 请求不足就用一块 prefill chunk 填满，GPU 利用率从只跑 decode 时的 30%–40% 被填到接近打满。
3. **关键证据或数字**：Sarathi-Serve 论文数据称 P99 ITL 下降约一个数量级，整体吞吐提升 20%–50%，代价是多了 kernel launch 与 KV cache 拼接开销、TTFT 略增。chunk size 是核心旋钮：太小（如 256）启动开销占比高、拖慢 TTFT；太大（如 4096）平滑效果打折。经验区间 512–4096，vLLM 默认 512（保 decode 流畅优先），SGLang 默认 2048（吞吐与延迟折中）；进阶做法是按 GPU 负载动态调 chunk。
4. **结论/判断**：这是用一点 TTFT 换 ITL 平滑与吞吐的调度层优化，不改模型、不改精度；只要服务里长短请求混跑，就该开。

## 关键数字
| 项 | 切分前 | 切分后 |
|---|---|---|
| 单个长 prefill 占用 | 约 800ms 连续独占 | 每块约 200ms，与 decode 交错 |
| decode 的 ITL | 约 50ms → 峰值约 800ms | 基本回到约 50ms |
| P99 ITL | — | 下降约一个数量级 |
| 整体吞吐 | 基线 | +20%–50% |

## 可迁移
- 做推理服务 SLO 时把 TTFT 与 ITL 分开盯：ITL 的 P99 抖动多半是长 prefill 抢占，chunked prefill 是默认就该开的开关。
- 面试答「长 prompt 影响其他用户体验怎么办」：答案在调度不在模型——分块 + 混批 + chunk size 权衡，一条线能讲完整。

## 疑问 / 下一步
- chunk size 与 batch token budget 在 vLLM 里是同一个旋钮（max_num_batched_tokens），实际部署时该按 P99 ITL 目标反推，而不是照抄默认值。
