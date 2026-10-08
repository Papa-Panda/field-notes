# G159 — rollout 是 RL 训练的瓶颈：vLLM 加速与异步训练详解
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G159-rollout-bottleneck-vllm.html

## 元信息

- 编号：G159
- 标题：rollout 是 RL 训练的瓶颈：vLLM 加速与异步训练详解
- BV：BV1N1b76qEif
- 时长：03:14
- 发布日期：2026-09-10
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：vLLM（continuous batching、PagedAttention）、verl、OpenRLHF

## 一句话总结

RL 训练七成以上时间花在 rollout 生成而非参数更新：解法是 vLLM 接管生成（提速 5–10 倍）加异步训练让生成与训练重叠，权重同步用频繁推送或重要性采样修正兜底。

## 核心

1. **问题/背景**：每一步 RL 都要让当前策略自回归生成几十到几百条回答，逐 token 生成天然慢；用普通 HF 推理一条要数秒，参数更新本身只要几秒，于是训练 GPU 七成以上时间在等 rollout。
2. **机制/方法**：两层加速。推理层：vLLM 用 continuous batching 把多请求生成动态拼批、PagedAttention 管理 KV cache，显存浪费减少 60% 以上，rollout 提速 5–10 倍；verl、OpenRLHF 均已内置。系统层：异步训练打破「先 rollout 再 train」的串行——actor 训练时 rollout 引擎同时用旧策略生成下一批数据，GPU 不再交替空闲。代价是权重同步问题：rollout 引擎里是旧权重，数据是 off-policy 的；两种解法混用——频繁把新权重推送给推理引擎（牺牲并行度换准确性），或接受 off-policy 数据、用重要性采样比率修正梯度。
3. **关键证据或数字**：某团队 8 卡 A100 跑 GRPO：同步模式一轮 120 秒（rollout 占 85 秒），切换 vLLM + 异步后 rollout 降到 35 秒、整轮 55 秒，整体提速约 2 倍；continuous batching 让 batch 利用率从 40% 升到 85%。
4. **结论/判断**：优化 RL 训练速度不要盯着反向传播，先优化 rollout；vLLM + 异步已是主流框架的标配组合，整体可达 2–3 倍提速。

## 关键数字

| 事项 | 基线（同步 + HF 推理） | 结果（vLLM + 异步） |
|---|---|---|
| rollout 占总时间 | 70% 以上 | — |
| 单轮总时长 | 120 秒 | 55 秒 |
| 其中 rollout | 85 秒 | 35 秒 |
| batch 利用率 | 40% | 85% |
| KV cache 显存浪费 | — | 减少 60% 以上 |

## 可迁移

- 这是 RL infra 的核心图景：rollout/训练时间比决定系统设计，异步化引入的 off-policy 程度需要用权重同步频率与重要性采样来管控——与 staleness、partial rollout 等设计点直接相连。
- 面试被问「RL 训练怎么提速」：先报时间构成（rollout 占比），再讲推理引擎替换与训练-生成重叠，最后讲 off-policy 修正，层次完整。

## 疑问 / 下一步

- 异步程度（允许几步 staleness）对收敛的定量影响视频未给；可结合 verl 的 partial rollout / one-step-off 配置再核。
