# G394 — softmax / safe softmax / online softmax：从会溢出到一遍算完（FlashAttention 核心）

> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G394-online-softmax.html

## 元信息

- 编号：G394
- 标题：softmax / safe softmax / online softmax：从会溢出到一遍算完（FlashAttention 核心）
- BV：BV1ETKW67EXG
- 时长：03:40
- 发布日期：2026-07-20
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：Online Softmax（Milakov & Gimelshein, 2018）；FlashAttention（Dao et al., 2022）

## 一句话总结

softmax 的三连问层层递进：朴素实现会因指数溢出崩掉，减最大值得到 safe softmax 但要扫三遍数据；online softmax 边遍历边维护最大值 $m$ 与指数和 $\ell$ ，最大值更新时用校正因子把旧和换算到新基准，一趟算完——这正是 FlashAttention 能分块计算注意力的底层原理。

## 核心

1. **问题/背景**：softmax 把一组 logits 变成概率分布（取指数再归一化），但指数增长太快：FP16 最大只能表示 65504，而 $e^{11}$ 已接近 6 万，logit 只要超过约 11，指数就溢出成无穷大，整个输出作废。
2. **机制/方法**：safe softmax 利用恒等变换——分子分母同除一个常数结果不变：先取最大值 $m$ ，每个数减 $m$ 再取指数，指数恒落在 $(0, 1]$ ，永不溢出且结果与原式一模一样。代价是要扫三遍：找最大值、算指数和、逐个输出，访存频繁。online softmax 把它压成流式一遍：遍历时同时维护已见最大值 $m$ 与指数和 $\ell$ ；新元素到来时先更新最大值，再把旧的 $\ell$ 乘以校正因子 $e^{m_{old} - m_{new}}$ 换算到新基准，然后加上新元素的贡献。这个校正因子是整个算法的灵魂。
3. **关键证据或数字**：手撕验证显示 online 版结果与普通 softmax 完全一致，却不需要把全部数据存下来、也不用回头重扫；三遍变（近）一遍，且天然处理流式数据。
4. **结论/判断**：FlashAttention 之所以能把注意力分块、边算边合并，靠的就是这套在线维护：每个分块本地维护 $(m, \ell)$ ，合并时用同样的校正因子对齐基准再相加。手撕题答到这一层，才算答到骨头上。

## 关键数字

| 版本 | 遍历遍数 | 关键性质 |
|---|---|---|
| 朴素 softmax | 1（但会溢出） | logit > 约 11 时 FP16 溢出 |
| safe softmax | 3 | 减最大值，指数恒 $\le 1$ |
| online softmax | 约 1（流式） | 校正因子 $e^{m_{old} - m_{new}}$ ，可分块合并 |

## 可迁移

- 面试手撕题高频三连：写 softmax → 说溢出与 safe 版 → 推出 online 版的校正因子，是区分「背过」与「懂 FlashAttention」的分水岭。
- 写 RL/inference 的 kernel 或读 vLLM、FlashAttention 源码时，分块合并注意力的数值稳定性逻辑就是这一套 $(m, \ell)$ 维护。

## 疑问 / 下一步

- online softmax 用在 log-sum-exp、在线归一化等其他场景时，校正因子的形式是否完全一致，还是需要按算子改造？
