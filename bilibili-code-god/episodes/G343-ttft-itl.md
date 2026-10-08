# G343 — TTFT vs ITL：推理体验的两个 SLO，优化路径完全不同
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G343-ttft-itl.html

## 元信息
- 编号：G343
- 标题：TTFT vs ITL：推理体验的两个 SLO，优化路径完全不同
- BV：BV1VxgR6gEmj
- 时长：04:55
- 发布日期：2026-07-31
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：未标注

## 一句话总结
TTFT 由 prefill 决定、ITL 由 decode 决定，总时延是两者的加权和；短回答看 TTFT、长回答看 ITL，优化手段完全分属两套。

## 核心
1. 问题/背景：用户感知的两种卡顿——转圈半天不出字、出字后逐字往外蹦——对应推理系统的两个一级 SLO。TTFT 是从请求发出到吐出第一个 token 的时间，ITL 是 decode 阶段相邻 token 的间隔（也称 TPOT）；总时延等于 TTFT 加上（输出长度 − 1）× ITL。
2. 机制/方法：TTFT 由 prefill 耗时决定，prefill 是 compute-bound，要把整段 prompt 一次过完并算好 KV cache，prompt 越长 TTFT 越大（线性甚至超线性）。ITL 由 decode 每步耗时决定，decode 是 memory-bound，每生成一个 token 都要把全部权重从 HBM 搬一遍，瓶颈在带宽不在算力；单用户视角下 TPS 就等于 ITL 的倒数。
3. 关键证据或数字：人类舒适阅读速度约每秒 20–30 个 token，ITL 压到 50ms 以下即感觉流畅；行业共识 SLO 是聊天场景 TTFT < 500ms、ITL < 50ms。反直觉点有二：长 prompt 不必然 TTFT 长，命中前缀缓存时几千 token 也能毫秒级出首字；对几十字的短回答 TTFT 占大头、ITL 无所谓，对千字长文则 ITL 才是杀手。
4. 结论/判断：两类优化路径完全不同：TTFT 靠 chunked prefill、prompt cache、prefix caching、PD 分离；ITL 靠 continuous batching、投机解码、量化（权重减半直接减带宽压力）、更高带宽的 GPU。场景侧重也不同：RAG 的 TTFT 天然偏大（可放宽到约 2 秒，但必须靠缓存兜住重复部分），Agent 多步调用会把 TTFT 反复累加、缓存近乎救命。选 SLO 不能一刀切，要看应用形态。

## 关键数字
| 项 | 值 |
|---|---|
| 聊天场景 TTFT 共识 SLO | < 500 ms |
| ITL 共识 SLO | < 50 ms |
| 人类舒适阅读速度 | 约 20–30 token/s |
| RAG 场景可接受 TTFT | 约 2 s（需缓存兜底） |

## 可迁移
- 评估任何推理框架先分口径：prefill 优化看 TTFT、decode 优化看 ITL，把两类手段混着报等于没测明白。
- 做 RL rollout 服务时同样适用：rollout 的长输出场景由 ITL 主导，batch 与投机解码的收益要按 ITL 口径算。

## 疑问 / 下一步
- PD 分离之后，TTFT 与 ITL 分别落在不同节点池，容量规划时两者的配比如何按流量形态估算？
