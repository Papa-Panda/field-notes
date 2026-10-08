# G359 — Continuous Batching：同样 8 张卡，凭啥 vLLM 比 HF 快 24 倍？
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G359-continuous-batching-2.html

## 元信息

- 编号：G359
- 标题：Continuous Batching：同样 8 张卡，凭啥 vLLM 比 HF 快 24 倍？
- BV：BV1jpgR6GEM1
- 时长：04:22
- 发布日期：2026-07-28
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：Orca（OSDI 2022）；vLLM / PagedAttention

## 一句话总结

模型、权重、硬件都一样，吞吐差距来自调度：静态批处理以「请求」为调度单位太粗，continuous batching 改为以「迭代」为单位、每步都能增删请求，把 GPU 槽位始终填满。

## 核心

1. **问题/背景**：HuggingFace Transformers 的静态批处理有三大痛点。一是迟到进不来：新请求晚到一步就只能等下一批，而下一批要等当前批里最长的请求跑完。二是早完成陪跑：只生成十来个 token 的短请求，必须陪同批生成两千 token 的长请求一起占着槽位。三是取消白跑：用户中途取消的请求照样算完。根源都是调度粒度太粗——以整个请求为单位。
2. **机制/方法**：Continuous batching（Orca 的核心思想，TensorRT-LLM 里也叫 in-flight batching）把调度单位换成单次 decode 迭代：每轮迭代结束后，调度器把已完成的请求踢出、释放槽位，再把排队的新请求做一次 prefill、灌入 KV 后并入下一轮。效果是槽位永不空转、先到先跑，TTFT 也不再受「凑齐一批」的拖累。但它有个硬前提：batch 成员每轮都在变，每个请求每轮新增一个 token 的 KV，还随时有进出——传统「每请求预留一整块连续显存」的布局根本应付不了，所以必须配套 PagedAttention，把 KV cache 切成固定大小的页、用页表映射，像操作系统虚拟内存一样按需分配与回收。两者是绑死的一对。
3. **关键证据或数字**：视频引用的量级：静态批处理下 GPU 利用率只有约 30%–40%，continuous batching 可达 80%–90%；吞吐上 Orca 论文报告比 FasterTransformer 高约 36 倍，vLLM 论文报告比 HF Transformers 高约 24 倍，其中 continuous batching 占大头、PagedAttention 补上其余部分。
4. **结论/判断**：从「按请求调度」到「按迭代调度」是大模型推理系统最关键的一次范式升级，2023 年之后的生产推理框架已全面切换；面试与系统设计里谈推理吞吐，先讲清这一层，再谈 KV 管理与量化才有地基。

## 关键数字

| 指标 | 静态批处理 | Continuous Batching |
|---|---|---|
| GPU 利用率 | 约 30%–40% | 约 80%–90% |
| 吞吐（对 HF Transformers） | 基线 | vLLM 报告约 24 倍 |

## 可迁移

- 对 RL infra 的直接相关性：rollout 阶段的生成吞吐就是被这套调度决定的——GRPO/PPO 的采样瓶颈、请求长尾（长回答陪跑）本质上是同一问题，理解 iteration-level scheduling 是看懂 verl/vLLM rollout 优化的前提。
- 系统设计面试被问「推理框架为什么快」，按「调度粒度 → 槽位利用率 → KV 分页配套」三层回答，比罗列框架特性更有说服力。

## 疑问 / 下一步

- 视频未展开 continuous batching 与 chunked prefill 的关系（长 prompt 的 prefill 如何与 decode 混批而不互相阻塞），这是当前推理框架的下一个关键话题。
