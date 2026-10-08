# G374 — MQA 和 GQA：把 KV 头砍到 8 组为什么效果不掉？｜注意力演化 MHA→MQA→GQA→MLA
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G374-mqa-gqa.html

## 元信息
- 编号：G374
- 标题：MQA 和 GQA：把 KV 头砍到 8 组为什么效果不掉？｜注意力演化 MHA→MQA→GQA→MLA
- BV：BV1tiKx6KE8v
- 时长：03:22
- 发布日期：2026-07-23
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：MQA（Shazeer, 2019）；GQA（Ainslie et al., 2023）；MLA（DeepSeek-V2）

## 一句话总结
KV cache 的大小正比于 KV 头数：MQA 让所有 Q 头共享一套 KV 把缓存除以头数但掉分，GQA 让 Q 头分组共享 KV，在省显存和保精度之间卡住甜点。

## 核心
1. 问题/背景：标准多头注意力（MHA）里每个头各有一套 Q、K、V，KV cache 要为每个头都存一份 K 和 V。几十个头的大模型缓存极大，解码时反复读取 KV 又是访存瓶颈，推理被显存和带宽双重压制。
2. 机制/方法：被共享的永远只是 K 和 V，Q 头始终独立。MQA 让全部 Q 头共享同一套 KV；GQA 把 Q 头分成若干组，组内共享一套 KV——分组数取 1 退化为 MQA，取头数退化为 MHA，中间是可调的折中。
3. 关键证据或数字：以 Llama-2 70B 为例，64 个 Q 头用 GQA 分 8 组，KV 头从 64 压到 8，缓存缩到 1/8，消融效果与满配 MHA 几乎持平；读 KV 变少还顺带加快解码。已训好的 MHA 模型可用原算力约 5% 的 uptraining 平滑改造成 GQA，不必重训。
4. 结论/判断：GQA 是当前开源模型的事实标准折中；演化线是 MHA → MQA（太狠）→ GQA（折中）→ MLA（改走低秩压缩）。

## 关键数字
| 方案 | KV 头数（64 个 Q 头时） | KV cache |
|---|---|---|
| MHA | 64 | 基线 |
| GQA（8 组） | 8 | 约 1/8 |
| MQA | 1 | 约 1/64（掉分、训练不稳） |

## 可迁移
- 估算推理显存时，KV cache 按 KV 头数而非 Q 头数计；面试答 MQA/GQA 要点出「共享的是 KV、Q 不共享」。
- RL rollout 阶段是 decode 主导，GQA/MLA 这类压缩 KV 的结构直接决定长序列采样的吞吐上限。

## 疑问 / 下一步
- MLA 的低秩压缩与 GQA 的分组共享在超长上下文下谁更划算，值得结合 DeepSeek 的数据再对比。
