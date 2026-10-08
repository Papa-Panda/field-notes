# G450 — SwiGLU 激活函数：GLU 门控 × Swish，为何取代 ReLU/GELU 成大模型 FFN 标配
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G450-swiglu.html

## 元信息

- 编号：G450
- 标题：SwiGLU 激活函数：GLU 门控 × Swish，为何取代 ReLU/GELU 成大模型 FFN 标配
- BV：BV1i3NS62E68
- 时长：04:17
- 发布日期：2026-07-14
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：GLU Variants Improve Transformer（Shazeer, 2020）

## 一句话总结

SwiGLU = GLU 门控（内容与阀门分工、逐元素按需放行）× Swish 平滑门（ $x \cdot \mathrm{sigmoid}(x)$ ），靠中间维度砍到约 2.67 倍保持三矩阵参数与旧 FFN 持平，白赚更低困惑度，成为现代大模型 FFN 事实标配。

## 核心

1. **问题/背景**：没有激活函数，再多层线性变换叠起来仍等价于一个线性变换；Transformer 的 FFN（升维 → 激活 → 降维）负责「掰弯」，但原始 ReLU 负半轴一刀切零，神经元长期落负区就梯度归零死亡。
2. **机制/方法**：两步升级：先平滑——Swish（SiLU）把拐角磨圆，负半轴留一点泄漏、处处可导；再门控——GLU 让输入走两条平行投影，一条当内容、一条过激活压到 0~1 当阀门，逐元素相乘按需放行。SwiGLU 即把 GLU 门上的 sigmoid 换成 Swish：

$$\mathrm{SwiGLU}(x) = \big( \mathrm{Swish}(xW) \odot xV \big) W_2$$

3. **关键证据或数字**：三矩阵比旧 FFN 多一个，解法是把中间维度从惯例的 4 倍砍到约 $\frac{2}{3}$ ，即约 2.67 倍，总参数与算力恰好持平（如 $d = 512$ 时中间层 2048 → 1365）；同规模下困惑度更低。
4. **结论/判断**：参数不涨、效果稳涨，这是它从 PaLM、LLaMA 到 Qwen、Mistral、DeepSeek 几乎全员普及的原因；连原论文作者都坦承无法解释其为何有效——深度学习里经验先行、解释滞后并不罕见。

## 关键数字

| 项 | 基线（ReLU/GELU FFN） | SwiGLU |
|---|---|---|
| 权重矩阵数 | 2 | 3 |
| 中间维度 | $4d$ | 约 $2.67d$ |
| 总参数 | — | 与基线持平 |

## 可迁移

- 手算参数量时 SwiGLU 的 FFN 是 $3 \times d \times 2.67d \approx 8d^2$ ，与旧口径 $2 \times d \times 4d = 8d^2$ 一致——这正是 2.67 这个系数的来历。
- 面试被问「为什么换激活」时，按 ReLU 死亡 → 平滑 → 门控分工 → 参数持平四步答，比只背公式完整得多。

## 疑问 / 下一步

- 门控增益的机理至今无公认解释；若要在自己的小模型上验证，消融应同时控制参数量与 FLOPs 两个变量，否则结论不可比。
