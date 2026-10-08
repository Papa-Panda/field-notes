# G232 — Medusa 多解码头讲透：一次预测 k 个 token，无需草稿模型的内嵌方案

> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G232-medusa.html

## 元信息

- 编号：G232
- 标题：Medusa 多解码头讲透：一次预测 k 个 token，无需草稿模型的内嵌方案
- BV：BV1j4826KEUb
- 时长：04:03
- 发布日期：2026-08-29
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：Medusa（多解码头 + tree attention）；EAGLE（特征层自回归改进）

## 一句话总结

Medusa 在主模型最后一层 hidden state 上并联几个极小的解码头，一次 forward 同时猜出未来 $k$ 个位置的候选，再用 tree attention 一次验证、只接受最长正确前缀，免草稿模型拿到 2–3 倍解码加速。

## 核心

1. **问题/背景**：自回归解码每生成一个 token 就要把全部参数从显存搬一遍，decode 阶段是带宽瓶颈，GPU 算力利用率常不足 10%；生成越长，搬运浪费越严重。破局的唯一方向是让一次 forward 产出多个 token。
2. **机制/方法**：主模型不动，在其 hidden state 上挂 $k$ 个小头（小前馈网络 + LM head），第 $i$ 个头预测 $i+1$ 位置的 token；小头参数量可忽略且并行计算，不引入新的串行依赖。预测不一定对，靠 tree attention 兜底：把各头的 top-k 候选组织成一棵候选树，所有路径拼成一条序列，用特制 attention mask 保证每个 token 只看自己路径上的祖先，一次 forward 并行验证全部路径，接受最长的正确前缀。
3. **关键证据或数字**：原论文在 Vicuna 系列上 7B 约 2.2 倍、13B 约 2.3 倍、33B 约 2.8 倍加速；模型越大、batch 越小收益越明显；vLLM、SGLang、TensorRT-LLM 等主流框架已支持。与投机解码（外置草稿模型、需单独训练并对齐分布、部署多占显存）相比，Medusa 是内嵌方案：共享 hidden state 天然对齐，可冻结主模型只训小头。
4. **结论/判断**：Medusa 与投机解码是两条不同路线——一个「自己长本事」，一个请外援；EAGLE 是其后续改进（在特征层做自回归、输入拼上一层特征与当前 token），加速比可到 3 倍以上，但范式源头在 Medusa。

## 关键数字

| 模型（Vicuna） | 加速比 |
|---|---|
| 7B | 约 2.2× |
| 13B | 约 2.3× |
| 33B | 约 2.8× |

## 可迁移

- 面试必答对比题：投机解码 vs Medusa——外置草稿 + 分布对齐成本 vs 内嵌小头 + 共享表征；选型时看部署约束与是否允许改模型结构。
- 「一次 forward 平均接受 2–3 个 token」是这类方法的统一收益口径；输出分布与原自回归一致，加速不牺牲正确性（与 G120 投机解码加速 rollout 呼应）。

## 疑问 / 下一步

- 小头数量与树宽如何随 batch size 调？batch 变大后 decode 不再纯带宽受限，Medusa 的收益拐点在哪，值得实测。
