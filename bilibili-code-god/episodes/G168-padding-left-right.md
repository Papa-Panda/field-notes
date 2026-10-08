# G168 — 训练 right padding、推理 left padding：搞混就是 silent bug
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G168-padding-left-right.html

## 元信息

- 编号：G168
- 标题：训练 right padding、推理 left padding：搞混就是 silent bug
- BV：BV1cubL6WEQi
- 时长：01:51
- 发布日期：2026-09-09
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：未标注

## 一句话总结

Padding 方向是训练与推理的一条隐形契约：训练右填充、推理左填充，方向搞反不报错但输出质量直接崩坏。

## 核心

1. **问题/背景**：batch 内序列长度不一，矩阵运算要求等长，必须用 PAD 补齐。PAD 位置的 label 设为 -100 不参与 loss，attention mask 也要屏蔽。但补在左边还是右边，训练和推理的要求相反，填错方向不会触发任何报错，属于典型的 silent bug。
2. **机制/方法**：训练用 right padding——真实 token 从位置 0 开始依次排布，与 decoder-only 自回归从左到右生成的顺序、标签对齐方式一致，PAD 只出现在尾部被忽略。推理必须用 left padding——生成是从输入末尾接着往下写，真实内容的末尾必须就是序列末尾；若用 right padding，模型会误以为输入还没结束，在 PAD 之后继续生成。推理侧还要额外处理位置编码：position id 应从第一个真实 token 开始计，而不是从 PAD 开始。
3. **关键证据或数字**：视频未给量化对比，但强调后果是定性的：位置编码与注意力全乱，模型直接输出乱码级别的内容，而训练/推理管线表面上一切正常。
4. **结论/判断**：方向混淆（训练用了 left、或推理框架默认 left 与训练的 right 不一致）是最常见的翻车点；防御手段是打印推理时的 token 序列与 mask 做端到端回归测试，上线前必查。

## 可迁移

- 排查生成质量问题时，先验证 padding 方向与 position id 起点，再怀疑模型本身——这类 bug 不报错、只降质。
- 面试高频点：能说清「为什么推理必须 left padding」（生成锚点在序列末尾）比背 API 更能体现理解深度。

## 疑问 / 下一步

- vLLM 等推理框架内部如何统一处理 left padding 与 position ids，值得结合源码看一遍。
