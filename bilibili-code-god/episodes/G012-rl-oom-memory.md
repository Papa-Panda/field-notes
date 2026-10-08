# G012 — RL 训练为什么总 OOM？18 倍显存账、七级省显存阶梯与 rollout 的 KV cache
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G012-rl-oom-memory.html

## 元信息

- 编号：G012
- 标题：RL 训练为什么总 OOM？18 倍显存账、七级省显存阶梯与 rollout 的 KV cache
- BV：BV15LHn6uEJd
- 时长：03:44
- 发布日期：2026-10-06
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：ZeRO（DeepSpeed）、vLLM rollout 引擎

## 一句话总结

训练 OOM 先别砍 batch：把显存账算清楚（全参训练约参数量的 18 倍字节 + 随 batch×序列走的激活），再按从便宜到贵的七级阶梯逐级拧；RL 还要单独给 rollout 引擎的 KV cache 留预算。

## 核心

1. **问题/背景**：全参训练的静态显存可算：参数 BF16 存一份 2 字节/参数，梯度 2 字节/参数，Adam 要存 FP32 主权重加一阶、二阶动量共 12 字节/参数，合计 16 字节，再加碎片与临时缓冲，经验口径是 18 倍——1B 参数约 18 GB、7B 约 126 GB，单卡 80 GB 根本放不下。第五块是激活，不随参数量走，随 batch × 序列长度走，长序列下它才是主角。
2. **机制/方法**：七级阶梯，从便宜到贵：① 缩 micro batch，或按 token 数上限动态组 batch；② 梯度检查点，不存中间激活、反向时重算，用约 1/3 的额外算力换掉激活大头；③ 激活 offload 到 CPU（FSDP 一个开关）；④ ZeRO 分片，ZeRO-2 把 12 字节的优化器状态与梯度分到多卡，ZeRO-3 连参数也分，代价是通信；⑤ 序列并行，序列超过 32K 时把一条样本的激活切到多卡（同时减小 micro batch 与 token 上限）；⑥ 参数与优化器 offload 到 CPU，能跑但慢；⑦ LoRA/QLoRA，优化器状态只留给少量 LoRA 参数、12 字节那块几乎消失——但 LoRA 省的是优化器状态，激活一分不省，长序列照样 OOM。
3. **关键证据或数字**：RL 的账要多算一段：rollout 引擎（vLLM）常驻一份模型权重，再预留一大块 KV cache，gpu_memory_utilization 就是它占卡的比例，建议 0.5–0.7（推荐起点 0.6）：设太高训练侧一开反向就 OOM，设太低 rollout 慢到训练在等它。rollout 的张量并行越小、副本越多、吞吐越高，但每个副本都要一份 KV 预算。推荐组合起点：梯度检查点 + 激活 offload + utilization 0.6 + 动态 batch；每卡 token 上限设成（prompt + response 最大长度）的 2 倍，只做前向的 logprob 阶段可再放大 2 倍。生成阶段 OOM 还有两招：多开几个 rollout 引擎、把 PPO epoch 从 4 降到 1–2。
4. **结论/判断**：实操顺序是先算账、再从便宜的开始拧、每拧一级看一次日志里的 max_memory_allocated（显存峰值仪表盘）。两个常见误区：一上来就 ZeRO-3 或 offload（速度掉一半，其实梯度检查点就够）；RL 里以为先爆的是训练侧，其实常是 rollout 的 KV cache 先爆。

## 关键数字

| 指标 | 数值 |
|---|---|
| 全参训练静态显存口径 | 约 18 字节/参数（参数 2 + 梯度 2 + Adam 12 + 碎片缓冲） |
| 7B 模型静态显存 | 约 126 GB（单卡 80 GB 放不下） |
| 梯度检查点代价 | 约 +1/3 算力，换掉大部分激活 |
| rollout gpu_memory_utilization | 0.5–0.7，推荐 0.6 |

## 可迁移

- 排 OOM 的标准动作：先按 18 倍口径算静态账、激活单独按 batch×序列估，再逐级拧旋钮并盯 max_memory_allocated，不要一次改多个变量。
- RL infra 调参时把 rollout utilization 与训练侧显存当成一张卡上的零和预算联动调，而不是两个独立问题。

## 疑问 / 下一步

- fully-async RL 下 rollout 与训练分卡部署时，KV cache 预算该怎么按 staleness 上限反推并发度？
