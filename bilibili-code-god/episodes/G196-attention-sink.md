# G196 — attention sink 详解：成因、后果与 StreamingLLM 的解法
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G196-attention-sink.html

## 元信息

- 编号：G196
- 标题：attention sink 详解：成因、后果与 StreamingLLM 的解法
- BV：BV1Tg8t6NE6U
- 时长：02:19
- 发布日期：2026-09-04
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：StreamingLLM（字幕提及）

## 一句话总结

长文本生成后期质量暴降的根源常是 attention sink：开头几个 token 吸走过多注意力；解法不是消除它，而是保留 sink token 再配滑动窗口。

## 核心

1. **问题/背景**：长文本生成越往后质量越差，甚至重复、乱码，根源可能是序列开头的前几个 token 获得了异常高的注意力权重，后面的 token 被「饿死」，信息传递断裂。
2. **机制/方法**：成因在 softmax 的数学约束——所有注意力权重之和必须为 1；当某个 token 与其他 token 都不太相关时，多余的权重无处可去，只能堆给模型最不排斥的位置，通常就是序列开头，于是开头 token 成为注意力汇聚点。序列越长，sink 吸走的注意力越多，后果越严重。
3. **关键证据或数字**：StreamingLLM 的解法是保留开头的 sink token 再加最近的滑动窗口，即可支撑无限长度生成——核心判断是 sink 是模型稳定运行的必需品，不能丢。另一解法是在序列前加可学习的 sink token（虚拟 token），让多余注意力扔给虚拟 token，不抢真实内容。实操上：做长文本生成不要丢弃开头前 3–4 个 token；做 KV cache 压缩时优先保留开头与结尾的 KV，中间可淘汰。
4. **结论/判断**：开头那几个 token 是模型的「注意力垃圾桶」，朴素滑窗一旦把它们丢掉，困惑度立刻飙升。

## 可迁移

- 做长上下文推理/KV cache 压缩时，把 sink token 保护写进淘汰策略，而不是按纯 LRU 淘汰。
- 训练新模型时可考虑 learnable sink token，把汇聚点从真实内容上移走。

## 疑问 / 下一步

- 不同模型/任务下 sink 强度差异很大，部署前如何快速量化一个模型的 sink 依赖程度？
