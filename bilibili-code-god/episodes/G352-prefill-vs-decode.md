# G352 — Prefill vs Decode：一个拼算力一个拼带宽，推理框架的灵魂
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G352-prefill-vs-decode.html

## 元信息
- 编号：G352
- 标题：Prefill vs Decode：一个拼算力一个拼带宽，推理框架的灵魂
- BV：BV1JjgR6jEgH
- 时长：04:03
- 发布日期：2026-07-29
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：Roofline 模型、chunked prefill、PagedAttention、PD 分离（见 G353）

## 一句话总结
LLM 推理天然两段：prefill 一次性并行算完整段 prompt、是 compute-bound；decode 逐 token 自回归、每步都要重读全部权重与 KV cache、是 memory-bound——两段瓶颈完全不同，必须分开优化。

## 核心
1. 问题/背景：用户感受是"读 prompt 秒回、写答案逐字蹦"，同一模型同一张卡为何读写差这么多？答案是推理分两个阶段，资源画像截然相反。
2. 机制/方法：prefill 把 $L$ 个 prompt token 拼成大矩阵做一次前向，注意力是 $L \times L$ ，所有 KV 一次算好写入 KV cache，权重只读一遍、算力吃满，耗时大致正比于 $L^2$ 除以算力。decode 每步只处理 1 个 token，计算量极小，却要把全部权重加完整 KV cache 从 HBM 读一遍，单步延迟基本由带宽决定。用 roofline 看：prefill 算术强度高达几百上千，落在算力天花板区；decode 算术强度约 1 ，死死贴在带宽斜线上，加算力没用。
3. 关键证据或数字：一个 2048 prompt、生成 512 token 的请求里，prefill 只占约 30% 时间却完成约 80% 计算量；decode 占约 70% 时间只完成约 20% 计算量。用户指标也随之分家：TTFT 由 prefill 决定，ITL 由 decode 决定。
4. 结论/判断：主流框架的招数本质都在"别让两段互相拖累"：chunked prefill 把长 prompt 切块与 decode 混批，防长 prompt 卡住生成；PagedAttention、continuous batching 缓解 decode 的带宽与调度浪费；更激进的是 PD 分离，把两段拆到不同 GPU 池各自扩缩。

## 关键数字
| 阶段 | 时间占比（示例请求） | 计算量占比 | 瓶颈 |
| --- | --- | --- | --- |
| Prefill | 约 30% | 约 80% | 算力（compute-bound） |
| Decode | 约 70% | 约 20% | HBM 带宽（memory-bound） |

## 可迁移
- 推理系统设计/面试的万能框架：任何优化先问它作用于 prefill 还是 decode、改善 TTFT 还是 ITL，再谈细节。
- RL rollout 也是同样的两段画像：长 prompt 的 rollout 延迟分析可以直接套这套 roofline 语言。

## 疑问 / 下一步
- batch 增大时 decode 的算术强度如何变化、何时能爬出带宽区，值得结合具体 batch size 做一次量化估算。
