# G207 — StreamingLLM 讲透：保留 4 个 sink token 让模型记住无限长对话
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G207-streamingllm-sink.html

## 元信息

- 编号：G207
- 标题：StreamingLLM 讲透：保留 4 个 sink token 让模型记住无限长对话
- BV：BV1Rd846yETR
- 时长：03:31
- 发布日期：2026-09-02
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：StreamingLLM（Xiao et al.）、attention sink 现象

## 一句话总结

开头几个 token 是注意力的锚点而非内容载体，滑动窗口只要永远保留它们，KV cache 固定大小即可支撑无限长流式对话。

## 核心

1. **问题/背景**：窗口外 token 被滚动丢弃时，一旦开头的 token 被踢出，困惑度瞬间爆炸、输出崩坏——不是记不全，而是注意力的「地基」被抽走。
2. **机制/方法**：逐层画注意力热力图发现，无论内容是什么，前几个 token（典型 4 个，哪怕是无语义的特殊符号）永远吸走大量注意力，这就是 attention sink。softmax 要求注意力权重和为 1，有些位置其实无可看之处，多余的注意力就被倒进这几个锚点里。StreamingLLM 的策略因此极简：永久保留前 4 个 sink token + 最近 4K token 的滑动窗口，中间旧 token 直接丢弃，KV cache 大小恒定。作者还验证过把 sink 换成无意义的换行符效果几乎不变——重要的是位置，不是内容。
3. **关键证据或数字**：在 400 万 token 的流式输入上困惑度全程稳定，而不带 sink 的纯滚动窗口基线早早崩掉；显存占用固定，不随对话轮数增长。
4. **结论/判断**：这是纯推理侧技巧，不需要重新训练，本质是给滑动窗口补上一个注意力锚点，让它真正可用。

## 关键数字

| 项目 | 数值 |
|---|---|
| 保留 sink token 数 | 4 |
| 滑动窗口 | 最近 4K token |
| 流式测试长度 | 400 万 token，困惑度稳定 |

## 可迁移

- 做长对话/Agent 多轮 rollout 的 KV cache 管理时，淘汰策略不能无脑 FIFO——丢掉开头 token 会引发质量悬崖，sink 必须豁免。
- attention sink 也解释了为什么某些压缩/量化 KV cache 的方案要对前几个 token 做特殊保护。

## 疑问 / 下一步

- sink 数量（4 个）是经验值，不同模型/层是否需要不同数量，论文与后续工作如何确定？
