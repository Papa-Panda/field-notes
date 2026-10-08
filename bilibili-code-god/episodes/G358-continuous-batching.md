# G358 — Continuous Batching：同样 8 张卡，凭啥 vLLM 比 HF 快 24 倍？
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G358-continuous-batching.html

## 元信息
- 编号：G358
- 标题：Continuous Batching：同样 8 张卡，凭啥 vLLM 比 HF 快 24 倍？
- BV：BV1ipgR6GE1K
- 时长：04:22
- 发布日期：2026-07-28
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：Orca（OSDI 2022，iteration-level scheduling）、vLLM（PagedAttention）

## 一句话总结
吞吐差距不在模型而在调度：static batching 以"请求"为调度单位，导致迟到者等车、早完成者陪跑、取消者白跑；continuous batching 把调度单位细化到每轮迭代，随进随出，GPU 槽位始终占满。

## 核心
1. 问题/背景：同样 8 张 A100、同样的模型权重精度，vLLM 吞吐可达 HuggingFace Transformers 的约 24 倍。HF 用最朴素的 static batching：一批请求凑齐发车、全部跑完才接下一批。
2. 机制/方法：static batching 三大痛点同源——调度单位太粗：新请求晚到 10 ms 也只能等当前 batch 里最长的请求跑完；只生成 10 个 token 的短请求要陪 2000 token 的长请求跑完全程；用户取消的请求照样把算力花完。时序图上 GPU 利用率呈阶梯式下滑，大片算力被浪费。continuous batching（Orca 提出，vLLM/TGI/TensorRT-LLM 跟进）把调度点放到每一轮 decode 迭代之间：完成的踢出、新到的做一次 prefill 灌入 KV 后并入下一轮。
3. 关键证据或数字：GPU 利用率从 static 的约 30%–40% 拉到约 80%–90%；Orca 论文报告比 FasterTransformer 高约 36 倍，vLLM 报告比 HF 高约 24 倍，其中 continuous batching 占大头、其余由 PagedAttention 贡献；TTFT 也不再受"凑齐 batch"限制，请求到达即可起跑。
4. 结论/判断：continuous batching 有个硬前提——必须能动态管理 KV cache：batch 成员每轮都在变、每轮每个请求又新增一个 token 的 KV，传统连续显存预留方式一退出就碎片化。所以它与 PagedAttention（把 KV 切成固定页、页表映射）绑死配套，缺一不可。

## 关键数字
| 指标 | Static Batching | Continuous Batching |
| --- | --- | --- |
| GPU 利用率 | 约 30%–40% | 约 80%–90% |
| 吞吐（对 HF Transformers） | 1 倍 | vLLM 约 24 倍 |
| 调度单位 | 整个请求 | 每轮迭代 |

## 可迁移
- 推理框架面试核心题：先讲清三痛点与"调度粒度"这一根源，再带出 PagedAttention 是它的显存前提，逻辑链完整。
- RL rollout 服务化时同理：轨迹长度方差极大，按请求调度的 rollout 必然陪跑，迭代级调度是天然解法。

## 疑问 / 下一步
- continuous batching 下 prefill 与 decode 混批的优先级策略（何时插 prefill 不伤 ITL）各家实现差异值得对比。
